#!/usr/bin/env python3
"""Find the official website of supporters who have none, from sources that name it, and log every try.

Usage: python skill/scripts/link_finder.py wikipedia [--country gb] [--limit 200] [--dry-run]
       python skill/scripts/link_finder.py sitelinks [--country de] [--limit 200] [--dry-run]
       python skill/scripts/link_finder.py nber      [--country se] [--limit 200] [--dry-run]

Run `profile_scan.py --due` afterwards: it reads the new sites for the accounts they link.

Sources, each one a page that states the address itself (nothing is guessed from a name):
  wikipedia  the supporter's English Wikipedia article (a profiles.csv row from Wikidata): the address in its "official website" template or
             the website field of its infobox.
  sitelinks  the same, in the other-language Wikipedia articles Wikidata links for the supporter (up to three, their own language first).
  orcid      economists and academics: the researcher URL on the one ORCID record with their exact name, only when its institution matches
             the supporter's affiliation.
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
          "wikidata.org", "wikimedia.org", "archive.org", "web.archive.org", "google.", "goo.gl", "bit.ly", "t.co", "orcid.org", "ideas.repec.org", "scholar.google", "svt.se/nyheter", "dr.dk/nyheder", "nrk.no/valg")  # and election guides of public broadcasters
NBER_OWN = ("nber.org", "twitter.com/nberpubs", "linkedin.com/company/national-bureau", "threads.net/@nber", "nbervideos", "did:plc:v7wvtabl4o6u5f426wqncxcu",
            "facebook.com/pages/National-Bureau")
TYPES_NBER = {"economist", "academic"}


def today():
    return dt.date.today().isoformat()


def http(url, delay=1.0, as_json=False, accept=None):
    time.sleep(delay)
    req = urllib.request.Request(url, headers={"User-Agent": UA, **({"Accept": accept} if accept else {})})
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
    if "." not in host or any(s in host for s in SOCIAL) or host.rsplit(".", 2)[-2] == "example" or any(n in url.lower() for n in ("svt.se/nyheter", "dr.dk/nyheder", "nrk.no/valg")):  # example.com is a placeholder
        return ""
    return url.replace("http://", "https://", 1) if url.startswith("http://") else url


def fold(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z ]", "", s)


WEB_TPL = re.compile(r"\{\{\s*(?:official\s*(?:web)?site|official\s*url|url|website)\s*\|\s*(?:1\s*=\s*)?([^|}\s]+)", re.I)
# The same two shapes in the languages of the registers: the template that names the official site, and the infobox field (not url=, the field of a citation).
OFFICIAL_TPL = (r"official\s*(?:web)?site|site\s+officiel|site\s+web|offizielle\s+(?:website|webseite)|sitio\s+web(?:\s+oficial)?|offici[eë]le\s+website|"
                r"sito\s+(?:web\s+)?ufficiale|site\s+oficial|oficjalna\s+strona|webbplats|hjemmeside|internetpr[aä]senz")
INFOBOX = re.compile(r"^\s*\|\s*(?:website|homepage|webseite|site\s*web|sitio\s*web|sito\s*web|web|site|hjemmeside|webbplats|strona|offizielle\s+website)\s*=\s*([^\n]+)", re.I | re.M)


# A bare list item in the links section: "* [http://example.org Offizielle Website]" (de, nl, sv and others write it so, with no template)
LINK_ITEM = re.compile(r"^\*+\s*\[(https?://[^\s\]]+)\s+([^\]]*)\]", re.I | re.M)
OFFICIAL_WORD = re.compile(r"offiziell|official|officiel|oficial|ufficiale|offici[eë]l|oficjaln|webbplats|hemsida|hjemmeside|homepage|persönliche|personal|eigene|sitio web|site web|website", re.I)


def wikipedia_site(wikitext):
    for m in LINK_ITEM.finditer(wikitext):
        if OFFICIAL_WORD.search(m.group(2)):
            u = clean(m.group(1))
            if u:
                return u
    for rx in (re.compile(r"\{\{\s*(?:" + OFFICIAL_TPL + r")\s*\|\s*(?:1\s*=\s*|url\s*=\s*)?([^|}\s]+)", re.I), INFOBOX):
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
            elif kinds["name"] in ("nber", "orcid") and r["kind"] == "person" and types & TYPES_NBER:
                out.append((d.name, r, ""))
            elif kinds["name"] == "sitelinks" and r.get("wikidata_qid") and r["actor_id"] not in wiki:
                out.append((d.name, r, ""))
            elif kinds["name"] == "sitelinks" and r.get("wikidata_qid"):
                out.append((d.name, r, "en"))  # has an English page that was read; the other languages are tried too
    return out


LANGS = ["de", "fr", "es", "it", "nl", "pt", "sv", "pl", "da", "no", "fi", "ca", "cs", "el", "tr", "ru", "uk", "ro", "hu", "id", "ja", "ko", "zh", "ar", "fa", "sk", "hr", "sr", "bg", "sl", "lt", "lv", "et", "ga", "gl", "eu", "he", "hi", "th", "vi", "ms", "sw", "af", "en"]


def run_sitelinks(items, a):
    """Wikipedia articles in every language Wikidata links (the supporter's own language first), up to three per supporter."""
    by_q = {r["wikidata_qid"]: (cc, r) for cc, r, _ in items}
    qids = list(by_q)
    pages = collections.defaultdict(list)  # lang -> [(title, qid)]
    for i in range(0, len(qids), 50):
        q = urllib.parse.urlencode({"action": "wbgetentities", "ids": "|".join(qids[i:i + 50]), "props": "sitelinks", "format": "json"})
        data = http("https://www.wikidata.org/w/api.php?" + q, delay=1.0, as_json=True)
        if not isinstance(data, dict):
            continue
        for qid, ent in data.get("entities", {}).items():
            sl = ent.get("sitelinks", {})
            langs = [l for l in LANGS if l + "wiki" in sl and l != "en"]
            langs += [k[:-4] for k in sl if k.endswith("wiki") and len(k) <= 7 and k[:-4] not in LANGS and k[:-4] not in langs][:2]
            for l in langs[:3]:
                pages[l].append((sl[l + "wiki"]["title"], qid))
    found = {}
    for lang, lst in pages.items():
        for i in range(0, len(lst), 20):
            chunk = lst[i:i + 20]
            q = urllib.parse.urlencode({"action": "query", "prop": "revisions", "rvprop": "content", "rvslots": "main", "titles": "|".join(t for t, _ in chunk),
                                        "redirects": 1, "format": "json", "formatversion": 2})
            data = http(f"https://{lang}.wikipedia.org/w/api.php?" + q, delay=1.0, as_json=True)
            if not isinstance(data, dict):
                continue
            norm = {x["to"]: x["from"] for x in data.get("query", {}).get("redirects", []) + data.get("query", {}).get("normalized", [])}
            title_q = {t: qid for t, qid in chunk}
            for pg in data.get("query", {}).get("pages", []):
                t = pg.get("title")
                qid = title_q.get(t) or title_q.get(norm.get(t, ""))
                if not qid or qid in found:
                    continue
                text = (pg.get("revisions") or [{}])[0].get("slots", {}).get("main", {}).get("content", "")
                site = wikipedia_site(text)
                if site:
                    found[qid] = (site, f"https://{lang}.wikipedia.org/wiki/" + urllib.parse.quote(t.replace(" ", "_")))
        print(f"  {lang}: {len(lst)} pages", flush=True)
    return {(by_q[q][0], by_q[q][1]["actor_id"]): v for q, v in found.items()}


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


def orcid_site(r):
    """The researcher URL on the one ORCID record with the supporter's exact name, when its institution matches the supporter's."""
    parts = [x for x in re.sub(r"\(.*?\)", " ", r["name"]).split() if x.lower().strip(".") not in {"dr", "prof", "professor", "jr", "sr"}]
    if len(parts) < 2:
        return "", "", "no name"
    q = urllib.parse.quote(f'given-names:"{parts[0]}" AND family-name:"{parts[-1]}"')
    res = http("https://pub.orcid.org/v3.0/expanded-search/?q=" + q + "&rows=5", delay=0.4, as_json=True, accept="application/json")
    if isinstance(res, str):
        return "", "", res
    found = (res or {}).get("expanded-result") or []
    if len(found) != 1:
        return "", "", "no single ORCID record with the name" if not found else "several ORCID records with the name"
    rec = found[0]
    orcid = rec["orcid-id"]
    page = "https://orcid.org/" + orcid
    words = lambda t: {w for w in fold(t).split() if len(w) >= 4 and w not in {"university", "universita", "universidad", "universite", "institute", "school", "department", "faculty", "college"}}
    inst = set().union(*[words(i) for i in rec.get("institution-name", [])]) if rec.get("institution-name") else set()
    mine = words(r.get("affiliation", "") + " " + r.get("role", ""))
    if not inst or not (inst & mine):
        return "", page, "ORCID institution does not match: " + ", ".join(rec.get("institution-name") or ["none listed"])
    urls = http(f"https://pub.orcid.org/v3.0/{orcid}/researcher-urls", delay=0.4, as_json=True, accept="application/json")
    if isinstance(urls, str):
        return "", page, urls
    for x in (urls or {}).get("researcher-url", []):
        u = clean(x["url"]["value"])
        if u:
            return u, page, ""
    return "", page, "record found, no website listed"


def verified(site, r):
    """('ok'|'unread'|'no name', note): the site's home page, or its address, carries a word of the supporter's name."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import profile_scan as ps
    person = r["kind"] == "person"
    toks = ps.name_tokens(r["name"], person)
    host = re.sub(r"[^a-z0-9]", "", urllib.parse.urlparse(site).netloc.lower() + urllib.parse.urlparse(site).path.lower())
    if any(t in host for t in toks):
        return "ok", ""
    h = http(site, delay=1.0)
    if not h or h.startswith("ERR"):
        return "unread", "site not read (" + (h or "404") + ")"
    # the title, the first headings and the site name decide, not the whole text: a page can mention a name without being that person's site
    head = " ".join(re.findall(r"<title[^>]*>(.*?)</title>", h, re.S | re.I) + re.findall(r"<h[12][^>]*>(.*?)</h[12]>", h, re.S | re.I)[:4]
                    + re.findall(r'<meta[^>]+(?:og:title|og:site_name|name="author")[^>]+content="([^"]*)"', h, re.I))
    text = fold(re.sub(r"<[^>]+>", " ", head))
    if any(t in text.replace(" ", "") or t in text for t in toks):
        return "ok", ""
    return "no name", "the page's title and headings do not carry the name"


def ingest(a):
    """Take the results of a search run (by a person or an agent) and write only what passes the same checks as the other sources.

    Each entry: {"country": "gb", "actor_id": "A0001", "url": "https://...", "kind": "website" | "profile", "note": "where it was found"}. An empty url means
    nothing was found (logged, so it is not searched again for a year). The address must pass clean() (no social, wiki or election-guide pages) and, for a
    website, the page's title, headings or address must carry the name; a profile page (a parliament's or an institution's page about the person) is
    kept as an official_page when its text carries the name. Nothing is taken on the word of the entry alone.
    """
    entries = json.load(open(a.file, encoding="utf-8"))
    by_cc = collections.defaultdict(list)
    for e in entries:
        by_cc[e["country"]].append(e)
    stats = collections.Counter()
    for cc, es in by_cc.items():
        d = str(ROOT / "data" / cc)
        actors = {r["actor_id"]: r for r in wtdb.load(d, "actors")}
        profiles = wtdb.load(d, "profiles")
        checks = wtdb.load(d, "profile_checks") if os.path.exists(d + "/profile_checks.csv") else []
        for e in es:
            r = actors[e["actor_id"]]
            url, note = clean(e.get("url") or ""), (e.get("note") or "")[:200]
            result, found = "none", ""
            if url:
                if e.get("kind") == "profile":
                    h = http(url, delay=1.0)
                    import profile_scan as ps
                    toks = ps.name_tokens(r["name"], r["kind"] == "person")
                    ok = bool(h) and not h.startswith("ERR") and any(t in fold(re.sub(r"<[^>]+>", " ", h)).replace(" ", "") for t in toks)
                    state = "ok" if ok else "no name"
                else:
                    state, vnote = verified(url, r)
                if state == "ok" or (state == "unread" and e.get("kind") != "profile"):
                    platform = "official_page" if e.get("kind") == "profile" else "website"
                    if not any(p["actor_id"] == e["actor_id"] and p["url"].rstrip("/").lower() == url.rstrip("/").lower() for p in profiles):
                        profiles.append(dict(profile_id=wtdb.next_id(profiles, "profiles"), actor_id=e["actor_id"], platform=platform, url=url,
                                             source="web search: " + note, checked=today()))
                    result, found = "found", platform
                    note = ("page not read; " if state == "unread" else "") + note
                else:
                    note = f"rejected {url}: {vnote if e.get('kind') != 'profile' else 'the page does not carry the name'}; " + note
            stats[result] += 1
            if url:
                print(f"{cc}:{e['actor_id']} {r['name'][:28]:28} {result:5} {e.get('kind','')[:4]} {url[:70]}" + ("" if result == 'found' else '  <- ' + note[:60]))
            if not a.dry_run:
                checks.append(dict(check_id=wtdb.next_id(checks, "profile_checks"), actor_id=e["actor_id"], method="manual_search", url=url or "", checked=today(),
                                   result=result, found=found, note=note[:300]))
        if not a.dry_run:
            wtdb.save(d, "profiles", profiles)
            wtdb.save(d, "profile_checks", checks)
    print(dict(stats))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", choices=["wikipedia", "sitelinks", "nber", "orcid", "ingest"])
    ap.add_argument("--country")
    ap.add_argument("--file", help="ingest: a JSON list of {country, actor_id, url, kind (website or profile), note}; url empty when nothing was found")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.source == "ingest":
        return ingest(a)
    kinds = {"name": a.source, "method": {"wikipedia": "wikipedia", "sitelinks": "wikipedia_langs", "orcid": "orcid"}.get(a.source, "directory")}
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
    elif a.source == "sitelinks":
        found = run_sitelinks(items, a)
        for cc, r, _ in items:
            k = (cc, r["actor_id"])
            site, page = found.get(k, ("", ""))
            results[k] = (site, page, "" if site else "no official website in the articles in other languages")
    else:
        fn = orcid_site if a.source == "orcid" else nber_site
        for n, (cc, r, _) in enumerate(items, 1):
            results[(cc, r["actor_id"])] = fn(r)
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
            if site:
                state, vnote = verified(site, r)
                if state == "no name":
                    note, site = f"{vnote}: {site}", ""
                elif state == "unread":
                    note = vnote
            err = note.startswith("ERR") or note == "page not read"
            if site:
                n_found += 1
                print(f"{cc}:{r['actor_id']} {r['name'][:32]:32} {site}")
            if a.dry_run or err:
                continue
            if site:
                profiles.append(dict(profile_id=wtdb.next_id(profiles, "profiles"), actor_id=r["actor_id"], platform="website", url=site,
                                     source={"nber": "NBER people page ", "orcid": "ORCID record "}.get(a.source, "Wikipedia ") + page, checked=today()))
            checks.append(dict(check_id=wtdb.next_id(checks, "profile_checks"), actor_id=r["actor_id"], method=kinds["method"], url=page or "",
                               checked=today(), result="found" if site else "none", found="website" if site else "", note=note[:300]))
        if not a.dry_run:
            wtdb.save(d, "profiles", profiles)
            wtdb.save(d, "profile_checks", checks)
    print(f"{n_found} websites found for {len(items)} supporters")


if __name__ == "__main__":
    sys.exit(main())
