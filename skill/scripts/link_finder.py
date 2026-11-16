#!/usr/bin/env python3
"""Find the official website of supporters who have none, from sources that name it, and log every try.

Usage: python skill/scripts/link_finder.py wikipedia [--country gb] [--limit 200] [--dry-run]
       python skill/scripts/link_finder.py nber      [--country se] [--limit 200] [--dry-run]

Run `profile_scan.py --due` afterwards: it reads the new sites for the accounts they link.

Sources, each one a page that states the address itself (nothing is guessed from a name):
  wikipedia  the supporter's English Wikipedia article (a profiles.csv row from Wikidata): the address in its "official website" template or
             the website field of its infobox.
  nber       economists and academics: nber.org/people/<first>_<last> when the page carries the person's name; the personal website and
             the RePEc profile it links, whose "homepage" field is read too.

Targets are active or former-role supporters that have no website in actors.csv and no website or official_page row in profiles.csv. A
found address is added to profiles.csv as a `website` row (source names the page it came from, checked today). Every target gets a
profile_checks.csv row (method wikipedia or directory; result found or none; none is not retried for a year, as in profile_scan.py).
Social and wiki addresses are never taken as a website. Standard library only; waits between requests and identifies itself.
"""
import argparse, collections, datetime as dt, json, os, re, sys, time, unicodedata, urllib.error, urllib.parse, urllib.request
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wtdb  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
UA = "WealthTaxSupportersBot/1.0 (+https://wealthtaxsupporters.com/about; finds a supporter's own site from pages that name it)"
SOCIAL = ("facebook.", "twitter.", "x.com", "instagram.", "youtube.", "youtu.be", "tiktok.", "linkedin.", "bsky.", "mastodon", "threads.net", "wikipedia.org",
          "wikidata.org", "wikimedia.org", "archive.org", "web.archive.org", "google.", "goo.gl", "bit.ly", "t.co", "orcid.org", "ideas.repec.org", "scholar.google")
NBER_OWN = ("nber.org", "twitter.com/nberpubs", "linkedin.com/company/national-bureau", "threads.net/@nber", "nbervideos", "did:plc:v7wvtabl4o6u5f426wqncxcu",
            "facebook.com/pages/National-Bureau")
TYPES_NBER = {"economist", "academic"}


def today():
    return dt.date.today().isoformat()


def http(url, delay=1.0, as_json=False):
    time.sleep(delay)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        raw = urllib.request.urlopen(req, timeout=40).read()
    except urllib.error.HTTPError as e:
        return None if e.code in (404, 410) else ("ERR %s" % e.code)
    except Exception as e:
        return "ERR %s" % type(e).__name__
    text = raw.decode("utf-8", "ignore")
    return json.loads(text) if as_json else text


def clean(url):
    url = url.strip().strip("[]<>").split("|")[0].split(" ")[0].rstrip(".,;)")
    if not url:
        return ""
    if not re.match(r"https?://", url, re.I):
        if url.startswith("//"):
            url = "https:" + url
        elif re.match(r"^[\w.-]+\.[a-z]{2,}(/|$)", url, re.I):
            url = "https://" + url
        else:
            return ""
    host = urllib.parse.urlparse(url).netloc.lower()
    if "." not in host or any(s in host for s in SOCIAL) or host.rsplit(".", 2)[-2] == "example":  # example.com is a placeholder
        return ""
    return url.replace("http://", "https://", 1) if url.startswith("http://") else url


def fold(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z ]", "", s)


WEB_TPL = re.compile(r"\{\{\s*(?:official\s*(?:web)?site|official\s*url|url|website)\s*\|\s*(?:1\s*=\s*)?([^|}\s]+)", re.I)
INFOBOX = re.compile(r"^\s*\|\s*(?:website|homepage)\s*=\s*([^\n]+)", re.I | re.M)  # not url=: that is the field of a citation


def wikipedia_site(wikitext):
    for rx in (re.compile(r"\{\{\s*official\s*(?:web)?site\s*\|\s*(?:1\s*=\s*)?([^|}\s]+)", re.I), INFOBOX):
        for m in rx.finditer(wikitext):
            chunk = m.group(1)
            inner = WEB_TPL.search(chunk)
            u = clean(inner.group(1) if inner else re.sub(r"^\[|\]$", "", chunk).split(" ")[0])
            if u:
                return u
    return ""


def targets(a, kinds):
    out = []
    data = ROOT / "data"
    cutoff = (dt.date.today() - dt.timedelta(days=365)).isoformat()
    for d in sorted(data.iterdir()):
        if not (d / "actors.csv").exists() or (a.country and d.name != a.country):
            continue
        actors = wtdb.load(str(d), "actors")
        profiles = wtdb.load(str(d), "profiles") if (d / "profiles.csv").exists() else []
        checks = wtdb.load(str(d), "profile_checks") if (d / "profile_checks.csv").exists() else []
        site = {p["actor_id"] for p in profiles if p["platform"] in ("website", "official_page")}
        wiki = {p["actor_id"]: p["url"] for p in profiles if p["platform"] == "wikipedia"}
        tried = {(c["actor_id"], c["method"]) for c in checks if c["checked"] > cutoff}
        for r in actors:
            if r["status"] not in ("active", "former_role") or r.get("website") or r["actor_id"] in site:
                continue
            types = set(wtdb.type_list(r))
            if types == {"wealthy_individual"} or (r["actor_id"], kinds["method"]) in tried:
                continue
            if kinds["name"] == "wikipedia" and r["actor_id"] in wiki:
                out.append((d.name, r, wiki[r["actor_id"]]))
            elif kinds["name"] == "nber" and r["kind"] == "person" and types & TYPES_NBER:
                out.append((d.name, r, ""))
    return out


def run_wikipedia(items, a):
    found = {}
    titles = {}
    for cc, r, url in items:
        titles[urllib.parse.unquote(url.split("/wiki/", 1)[-1]).replace("_", " ")] = (cc, r["actor_id"])
    names = list(titles)
    for i in range(0, len(names), 20):
        chunk = names[i:i + 20]
        q = urllib.parse.urlencode({"action": "query", "prop": "revisions", "rvprop": "content", "rvslots": "main", "titles": "|".join(chunk),
                                    "redirects": 1, "format": "json", "formatversion": 2})
        data = http("https://en.wikipedia.org/w/api.php?" + q, delay=1.0, as_json=True)
        if not isinstance(data, dict):
            continue
        redir = {x["to"]: x["from"] for x in data.get("query", {}).get("redirects", [])}
        for pg in data.get("query", {}).get("pages", []):
            t = redir.get(pg.get("title"), pg.get("title"))
            key = t if t in titles else pg.get("title")
            if key not in titles:
                continue
            text = (pg.get("revisions") or [{}])[0].get("slots", {}).get("main", {}).get("content", "")
            found[key] = (wikipedia_site(text), "https://en.wikipedia.org/wiki/" + urllib.parse.quote(pg["title"].replace(" ", "_")))
        print(f"  wikipedia {min(i + 20, len(names))}/{len(names)}", flush=True)
    return {titles[t]: v for t, v in found.items()}, titles


def nber_site(r):
    parts = fold(re.sub(r"\(.*?\)", " ", r["name"])).split()
    parts = [p for p in parts if p not in {"dr", "prof", "professor", "jr", "sr"}]
    if len(parts) < 2:
        return "", "", "no name"
    first, last = parts[0], parts[-1]
    for slug in (f"{first}_{last}", f"{first}__{last}"):
        url = "https://www.nber.org/people/" + slug
        h = http(url, delay=1.0)
        if h is None:
            continue
        if h.startswith("ERR"):
            return "", "", h
        title = re.search(r"<title>(.*?)</title>", h, re.S)
        t = fold(title.group(1)) if title else ""
        if first not in t or last not in t:
            continue
        links = [m.group(1) for m in re.finditer(r'<a[^>]+href="(https?://[^"]+)"', h)]
        links = [l for l in dict.fromkeys(links) if not any(o in l for o in NBER_OWN)]
        for l in links:
            u = clean(l)
            if u:
                return u, url, ""
        for l in links:  # the RePEc profile has a "homepage" field of its own
            if "ideas.repec.org/e/" in l:
                p = http(l, delay=1.0)
                if p and not p.startswith("ERR"):
                    m = re.search(r'class="homelabel"></td><td><A HREF="([^"]+)"', p, re.I)
                    u = clean(m.group(1)) if m else ""
                    if u:
                        return u, url, "via RePEc " + l
        return "", url, "page found, no website listed"
    return "", "", "no NBER page"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", choices=["wikipedia", "nber"])
    ap.add_argument("--country")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    kinds = {"name": a.source, "method": "wikipedia" if a.source == "wikipedia" else "directory"}
    items = targets(a, kinds)
    if a.limit:
        items = items[:a.limit]
    print(len(items), "targets")
    results = {}  # (cc, actor_id) -> (site, page, note)
    if a.source == "wikipedia":
        found, titles = run_wikipedia(items, a)
        for cc, r, url in items:
            k = (cc, r["actor_id"])
            site, page = found.get(k, ("", url))[0:2]
            results[k] = (site, page, "" if k in found else "page not read")
    else:
        for n, (cc, r, _) in enumerate(items, 1):
            results[(cc, r["actor_id"])] = nber_site(r)
            if n % 25 == 0:
                print(f"  nber {n}/{len(items)}", flush=True)
    by_cc = collections.defaultdict(list)
    for cc, r, _ in items:
        by_cc[cc].append(r)
    n_found = 0
    for cc, rows in by_cc.items():
        d = str(ROOT / "data" / cc)
        profiles = wtdb.load(d, "profiles")
        checks = wtdb.load(d, "profile_checks") if os.path.exists(d + "/profile_checks.csv") else []
        for r in rows:
            site, page, note = results[(cc, r["actor_id"])]
            err = note.startswith("ERR") or note == "page not read"
            if site:
                n_found += 1
                print(f"{cc}:{r['actor_id']} {r['name'][:32]:32} {site}")
            if a.dry_run or err:
                continue
            if site:
                profiles.append(dict(profile_id=wtdb.next_id(profiles, "profiles"), actor_id=r["actor_id"], platform="website", url=site,
                                     source=("Wikipedia infobox " if a.source == "wikipedia" else "NBER people page ") + page, checked=today()))
            checks.append(dict(check_id=wtdb.next_id(checks, "profile_checks"), actor_id=r["actor_id"], method=kinds["method"], url=page or "",
                               checked=today(), result="found" if site else "none", found="website" if site else "", note=note[:300]))
        if not a.dry_run:
            wtdb.save(d, "profiles", profiles)
            wtdb.save(d, "profile_checks", checks)
    print(f"{n_found} websites found for {len(items)} supporters")


if __name__ == "__main__":
    sys.exit(main())
