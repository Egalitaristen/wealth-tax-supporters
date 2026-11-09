#!/usr/bin/env python3
"""Collect Bluesky posts about a wealth tax and the profiles of the people who wrote them, for review.

This script only COLLECTS. It writes nothing to the register. A reviewer (a research run) reads the file it produces,
decides for each author whether they are a public figure or organisation of a kind the register includes, grades the
post under references/definition-and-grades.md, and only then adds a lead (leads.py) or a supporter.

Usage:
  python skill/scripts/bluesky_scan.py open  [--lang en,de,fr] [--since 2026-10-01] [--pages 3] [--out FILE]
  python skill/scripts/bluesky_scan.py known [--country gb] [--since 2026-01-01] [--out FILE]
  python skill/scripts/bluesky_scan.py show  FILE [--min-score 2] [--new-only]

  open   searches the phrases and hashtags in skill/references/bluesky-queries.json (open search: finds people we do not have).
  known  searches the same phrases restricted to the Bluesky accounts already in the register's profiles.csv (more evidence for
         people we have). Lower priority than open.
  show   prints a collected file compactly, best candidates first.

Rules built in:
  - The public AppView endpoint (api.bsky.app) needs no login. Be gentle: a pause between calls, retry on 429.
  - Authors who set the "!no-unauthenticated" label asked not to be shown to logged-out viewers: they are skipped.
  - Only public posts and the public profile (name, handle, bio, counts). Nothing else is collected.
  - A hit is a candidate, not a supporter: the phrase must refer to a tax on the stock of wealth, and the author must be
    someone the register includes (politician, party, organisation, economist, journalist, ...), not a private person.

Output: JSON lines, one per author: profile, a rough score for review order, whether the handle is already in the register,
and their matching posts (url, date, text, language, counts). Standard library only.
"""
import argparse, csv, datetime as dt, json, sys, time, urllib.parse, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
API = "https://api.bsky.app/xrpc/"
QUERIES = Path(__file__).resolve().parent.parent / "references" / "bluesky-queries.json"
UA = {"User-Agent": "wealth-tax-supporters-research/1.0 (+https://wealthtaxsupporters.com)"}
SKIP_LABELS = {"!no-unauthenticated"}


def get(method, **params):
    url = API + method + "?" + urllib.parse.urlencode(params, doseq=True)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                time.sleep(0.35)
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (403, 429) or e.code >= 500:  # 403 comes and goes under load: wait and retry
                time.sleep(4 * (attempt + 1))
                continue
            print(f"  {method} {e.code}: {params.get('q', '')}", file=sys.stderr)
            return {}
        except Exception as e:
            time.sleep(3)
    return {}


def register_handles(country=None):
    """handle -> (country folder, actor_id) for every Bluesky profile already in the register."""
    out = {}
    for f in sorted((ROOT / "data").glob("*/profiles.csv")):
        if country and f.parent.name != country:
            continue
        for row in csv.DictReader(open(f, encoding="utf-8", newline="")):
            if row["platform"] == "bluesky":
                h = row["url"].rstrip("/").split("/profile/")[-1].lower()
                out[h] = (f.parent.name, row["actor_id"])
    return out


def norm(s):
    import unicodedata, re
    s = unicodedata.normalize("NFKD", s.lower())
    return re.sub(r"[^a-z0-9 ]", "", "".join(c for c in s if not unicodedata.combining(c))).strip()


def register_names():
    """normalised name -> (country folder, actor_id) for everyone in the register, so a hit on a known person is marked even if
    the register holds no Bluesky link for them."""
    out = {}
    for f in sorted((ROOT / "data").glob("*/actors.csv")):
        for row in csv.DictReader(open(f, encoding="utf-8", newline="")):
            out.setdefault(norm(row["name"]), (f.parent.name, row["actor_id"]))
    return out


# Words in a bio that suggest a kind of account the register includes. A hint for the reviewer, never a verdict.
HINTS = {
    "politician": ["mp ", "member of parliament", "senator", "deputy", "député", "deputada", "diputad", "abgeordnete", "mdb", "councillor", "mayor", "minister", "ministre", "congress", "assembly", "parliament", "bundestag", "senate", "storting", "riksdag", "mep"],
    "party": ["party", "parti ", "partei", "partido", "partij", "parlamentsgruppe", "fraktion", "group parlementaire"],
    "union": ["union", "syndicat", "gewerkschaft", "sindicato", "vakbond", "fackförbund"],
    "journalist": ["journalist", "reporter", "correspondent", "editor", "columnist", "journaliste", "periodista", "jornalista", "redakteur", "writer"],
    "economist": ["economist", "économiste", "economista", "ökonom", "professor", "researcher", "lecturer", "think tank", "institute", "économie"],
    "campaign": ["campaign", "advocacy", "ngo", "charity", "foundation", "movement", "attac", "oxfam", "justice", "organisation", "organization", "association"],
}


def hints(bio, name):
    b = f" {bio} {name} ".lower()
    return [k for k, ws in HINTS.items() if any(w in b for w in ws)]


def search(q, lang, since, pages, author=None):
    cursor, posts = None, []
    for _ in range(pages):
        # A hashtag goes in the `tag` parameter; in `q` the "#" makes the API answer 400.
        params = dict(limit=100, sort="latest", since=since)
        if q.startswith("#"):
            params["q"], params["tag"] = q, q[1:]
        else:
            params["q"] = q
        if lang:
            params["lang"] = lang
        if author:
            params["author"] = author
        if cursor:
            params["cursor"] = cursor
        d = get("app.bsky.feed.searchPosts", **params)
        posts += d.get("posts", [])
        cursor = d.get("cursor")
        if not cursor or not d.get("posts"):
            break
    return posts


def post_row(p, query):
    rec, a = p.get("record", {}), p["author"]
    rkey = p["uri"].rsplit("/", 1)[-1]
    return dict(url=f"https://bsky.app/profile/{a['handle']}/post/{rkey}", uri=p["uri"], date=rec.get("createdAt", "")[:10],
                text=rec.get("text", ""), langs=rec.get("langs", []), reply=bool(rec.get("reply")), query=query,
                likes=p.get("likeCount", 0), reposts=p.get("repostCount", 0), replies=p.get("replyCount", 0),
                quotes=p.get("quoteCount", 0))


def profiles(dids):
    out, dids = {}, list(dids)
    for i in range(0, len(dids), 25):
        for pr in get("app.bsky.actor.getProfiles", actors=dids[i:i + 25]).get("profiles", []):
            out[pr["did"]] = pr
    return out


def score(profile, handle, n_posts):
    """A rough review order, not a verdict: custom domain, a bio, an audience, several matching posts."""
    s = 0
    if not handle.endswith(".bsky.social"):
        s += 2  # a domain they control is the usual mark of an institution or a person who proves who they are
    if profile.get("description"):
        s += 1
    if profile.get("followersCount", 0) >= 1000:
        s += 1
    if profile.get("followersCount", 0) >= 10000:
        s += 1
    if n_posts >= 2:
        s += 1
    if profile.get("verification", {}).get("verifiedStatus") == "valid":
        s += 3
    return s


def collect(queries, since, pages, known, authors=None, names=None):
    """queries: list of (query, lang). Returns per-author records."""
    by_author, seen, skipped = {}, set(), 0
    for q, lang in queries:
        targets = authors or [None]
        for a in targets:
            for p in search(q, lang, since, pages, a):
                if p["uri"] in seen:
                    continue
                seen.add(p["uri"])
                labels = {l.get("val") for l in p["author"].get("labels", [])}
                if labels & SKIP_LABELS:
                    skipped += 1
                    continue
                by_author.setdefault(p["author"]["did"], []).append(post_row(p, q))
        print(f"  {q!r} ({lang or 'any'}): {len(seen)} posts so far", file=sys.stderr)
    profs = profiles(by_author)
    out = []
    for did, posts in by_author.items():
        pr = profs.get(did, {})
        if {l.get("val") for l in pr.get("labels", [])} & SKIP_LABELS:
            skipped += 1
            continue
        handle = pr.get("handle") or posts[0]["url"].split("/profile/")[1].split("/")[0]
        out.append(dict(did=did, handle=handle, name=pr.get("displayName", ""), bio=pr.get("description", ""),
                        followers=pr.get("followersCount", 0), posts_total=pr.get("postsCount", 0),
                        verified=pr.get("verification", {}).get("verifiedStatus") == "valid",
                        in_register=known.get(handle.lower()) or (names or {}).get(norm(pr.get("displayName", "")) if pr.get("displayName") else None),
                        hints=hints(pr.get("description", ""), pr.get("displayName", "")), score=score(pr, handle, len(posts)),
                        posts=sorted(posts, key=lambda x: x["date"], reverse=True)))
    out.sort(key=lambda r: (r["in_register"] is not None, -r["score"], -len(r["posts"])))
    print(f"{len(out)} authors, {sum(len(r['posts']) for r in out)} posts, {skipped} skipped (opted out of logged-out viewing)", file=sys.stderr)
    return out


def load_queries(langs):
    q = json.load(open(QUERIES, encoding="utf-8"))
    out = []
    for lang, spec in q.items():
        if langs and lang not in langs:
            continue
        out += [(t, lang) for t in spec.get("phrases", [])]
        out += [(t, lang) for t in spec.get("hashtags", [])]
    return out


def write(rows, path):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"wrote {path}", file=sys.stderr)


def show(path, min_score, new_only):
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        if r["score"] < min_score or (new_only and r["in_register"]):
            continue
        tag = f" [in register: {r['in_register'][0]}/{r['in_register'][1]}]" if r["in_register"] else ""
        print(f"\n== {r['name'] or '(no name)'} @{r['handle']} · score {r['score']} · {r['followers']} followers{' · verified' if r['verified'] else ''}{tag}")
        print(f"   bio: {r['bio'][:220].replace(chr(10), ' ')}")
        for p in r["posts"][:3]:
            print(f"   {p['date']} {p['url']}\n     {p['text'][:280].replace(chr(10), ' ')}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["open", "known", "show"])
    ap.add_argument("file", nargs="?")
    ap.add_argument("--lang", default="")
    ap.add_argument("--since", default=(dt.date.today() - dt.timedelta(days=30)).isoformat())
    ap.add_argument("--pages", type=int, default=3)
    ap.add_argument("--country", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--min-score", type=int, default=0)
    ap.add_argument("--new-only", action="store_true")
    a = ap.parse_args()
    if a.mode == "show":
        return show(a.file, a.min_score, a.new_only)
    langs = {x for x in a.lang.split(",") if x}
    since = a.since + "T00:00:00Z"
    known, names = register_handles(), register_names()
    queries = load_queries(langs)
    if a.mode == "open":
        rows = collect(queries, since, a.pages, known, names=names)
    else:
        authors = list(register_handles(a.country))
        # Search each phrase once per batch of known accounts: one query per account would be thousands of calls.
        # The people we have write in their own language: no language filter, and the main phrases of every language.
        main = []
        for lang in dict.fromkeys(l for _, l in queries):
            main += [(q, None) for q, l in queries if l == lang and not q.startswith("#")][:2]
        rows = collect(main, since, 1, known, authors, names)
    write(rows, a.out or f"bluesky_{a.mode}_{dt.date.today().isoformat()}.jsonl")


if __name__ == "__main__":
    main()
