#!/usr/bin/env python3
"""Watch media sources for new articles that may carry statements by supporters of a wealth tax, and keep what has been seen.

Usage:
  python skill/scripts/media_scan.py sources                          the registered sources (data/media_sources.json)
  python skill/scripts/media_scan.py scan [--source pm-uk] [--pages 2] [--dry-run]   read each source's listing, record the articles not seen before (status new)
  python skill/scripts/media_scan.py list [--status new] [--source ID] [--newest] [--limit 25]    the articles to review (oldest first unless --newest)
  python skill/scripts/media_scan.py read M0007 [--chars 6000]            title, date and text of one article, to read it
  python skill/scripts/media_scan.py mark M0007 M0008 --status reviewed|used|skipped [--note "..."]

A source is a listing page (a news or press page, an RSS or Atom feed, a Squarespace collection or a WordPress REST list) of an organisation or a news site. `scan` finds the article links on it
and appends the new ones to data/media_seen.csv, so the next scan reports only what appeared since. It only collects: it never writes to a
country register. A reviewer reads each new article with `read`, decides who said what, adds statements and leads as references/media-scan.md
describes, and then marks the article reviewed, used or skipped. Run it about monthly (more often for a source that publishes daily).

Reads politely: identifies itself, honours robots.txt, waits between requests to a host, never works around a block. Standard library only.
"""
import argparse, csv, datetime as dt, html, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import profile_scan as ps  # noqa: E402  (the polite Reader and its user agent)

ROOT = Path(__file__).resolve().parent.parent.parent
SOURCES = ROOT / "data" / "media_sources.json"
SEEN = ROOT / "data" / "media_seen.csv"
COLS = ["seen_id", "source_id", "url", "title", "published", "first_seen", "status", "note"]
STATUS = ("new", "reviewed", "used", "skipped")
CHROME_HOSTS = ("facebook.com", "twitter.com", "x.com", "instagram.com", "youtube.com/channel", "linkedin.com", "bsky.app", "tiktok.com", "threads.net",
                "mailto:", "tel:", "javascript:", "squarespace.com", "wixsite.com/signup")


def today():
    return dt.date.today().isoformat()


def load_seen():
    if not SEEN.exists():
        return []
    with open(SEEN, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def save_seen(rows):
    with open(SEEN, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, lineterminator="\n")
        w.writeheader()
        w.writerows({c: r.get(c, "") for c in COLS} for r in rows)


def load_sources():
    return json.load(open(SOURCES, encoding="utf-8"))


def norm(url):
    """One article, one key: no fragment, no tracking parameters, no trailing slash."""
    u = urllib.parse.urlparse(url)
    q = [(k, v) for k, v in urllib.parse.parse_qsl(u.query) if not k.lower().startswith(("utm_", "fbclid", "gclid", "mc_"))]
    path = u.path.rstrip("/") or "/"
    return urllib.parse.urlunparse((u.scheme.lower(), u.netloc.lower().replace("www.", "", 1) if u.netloc.lower().startswith("www.") else u.netloc.lower(), path, "", urllib.parse.urlencode(q), ""))


def clean_text(s):
    s = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def extract(listing_url, text, src):
    """[(url, title)] of the article links of a listing page or feed, in page order."""
    inc = re.compile(src["include"]) if src.get("include") else None
    exc = re.compile(src["exclude"]) if src.get("exclude") else None
    min_title = src.get("min_title", 25)
    out, seen = [], set()

    def add(url, title):
        url = urllib.parse.urljoin(listing_url, html.unescape(url).strip())
        if not url.startswith(("http://", "https://")) or any(h in url for h in CHROME_HOSTS):
            return
        key = norm(url)
        if key == norm(listing_url) or key in seen:
            return
        if inc and not inc.search(url):
            return
        if exc and exc.search(url):
            return
        title = clean_text(title)
        if len(title) < min_title or "{" in title:
            return
        seen.add(key)
        out.append((url, title))

    head = text.lstrip()[:600].lower()
    if "<rss" in head or "<feed" in head or "<?xml" in head and ("<item" in text[:5000] or "<entry" in text[:5000]):
        for it in re.findall(r"<(?:item|entry)\b.*?</(?:item|entry)>", text, re.S | re.I):
            t = re.search(r"<title[^>]*>(.*?)</title>", it, re.S | re.I)
            link = re.search(r"<link[^>]*href=[\"']([^\"']+)[\"']", it, re.I) or re.search(r"<link[^>]*>\s*(?:<!\[CDATA\[)?([^<\]]+)", it, re.I)
            if t and link:
                add(link.group(1), re.sub(r"<!\[CDATA\[|\]\]>", "", t.group(1)))
        return out
    for m in re.finditer(r"<a\b[^>]*?href=[\"']([^\"'#][^\"']*)[\"'][^>]*>(.*?)</a>", text, re.S | re.I):
        add(m.group(1), m.group(2))
    return out


def fetch_json(reader, url):
    """(data, final_url) or (None, reason). Same manners as Reader.get: robots.txt, a pause per host, our own user agent."""
    if not reader.allowed(url):
        return None, "robots.txt forbids it"
    host = urllib.parse.urlparse(url).netloc
    wait = reader.delay - (time.time() - reader.last.get(host, 0))
    if wait > 0:
        time.sleep(wait)
    reader.last[host] = time.time()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": ps.UA, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read(5_000_000).decode("utf-8", "ignore")), r.geturl()
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:60]}"


def walk(obj, path):
    for k in path.split("."):
        obj = obj.get(k) if isinstance(obj, dict) else None
    return obj


def host_of(u):
    return urllib.parse.urlparse(u).netloc.lower().replace("www.", "", 1)


def json_items(src, reader, pages):
    """[(url, title, published)] from a Squarespace collection (?format=json, with its own paging) or a WordPress REST list (per_page and page)."""
    fmt, out, where, nxt = src["format"], [], src.get("where", {}), None
    for n in range(1, pages + 1):
        sep = "&" if "?" in src["url"] else "?"
        if fmt == "squarespace":
            url = src["url"] + sep + "format=json" + (f"&offset={nxt}" if n > 1 else "")
        else:
            url = src["url"] + sep + f"page={n}"
        data, final = fetch_json(reader, url)
        if data is None:
            if n == 1 or "400" not in str(final):  # a WordPress list answers 400 after its last page
                print(f"{src['id']}: {url} -> {final}")
            break
        if fmt == "squarespace":
            base = src["url"].split("?")[0]
            for it in data.get("items", []):
                link = it.get("sourceUrl") or urllib.parse.urljoin(base, it.get("fullUrl", ""))
                pub = dt.datetime.fromtimestamp(int(it["publishOn"]) / 1000, dt.timezone.utc).date().isoformat() if it.get("publishOn") else ""
                out.append((link, clean_text(it.get("title", "")), pub))
            pg = data.get("pagination") or {}
            if not pg.get("nextPage"):
                break
            nxt = pg.get("nextPageOffset")
        else:
            if not isinstance(data, list) or not data:
                break
            for it in data:
                if any(v not in (walk(it, k) or []) for k, v in where.items()):
                    continue
                link = it.get("link", "")
                blob = json.dumps(it.get("acf") or {}, ensure_ascii=False).replace("\\/", "/")
                ext = [u for u in re.findall(r'href=\\"([^"\\ ]+)', blob) if u.startswith("http") and host_of(u) != host_of(link)]
                out.append((ext[0] if ext else link, clean_text((it.get("title") or {}).get("rendered", "")), (it.get("date") or "")[:10]))
    return out


def cmd_scan(a):
    reader = ps.Reader(a.delay)
    seen = load_seen()
    have = {norm(r["url"]) for r in seen}
    next_id = max([int(r["seen_id"][1:]) for r in seen] + [0]) + 1
    total_new = 0
    for src in load_sources():
        if a.source and src["id"] != a.source:
            continue
        found = []
        is_json = src.get("format") in ("squarespace", "wp-json")
        if is_json:
            found = json_items(src, reader, a.pages)
        for url in [] if is_json else [src["url"]] + src.get("extra_urls", []):
            if not reader.allowed(url):
                print(f"{src['id']}: robots.txt forbids {url}")
                continue
            status, text, final = reader.get(url)
            if status != 200 or not text:
                print(f"{src['id']}: {url} -> {status or 'error'} {text[:60] if not status else ''}")
                continue
            found += [(u, t, "") for u, t in extract(final, text, src)]
        new = []
        for url, title, pub in found:
            if norm(url) in have or not title:
                continue
            have.add(norm(url))
            new.append(dict(seen_id=f"M{next_id:04d}", source_id=src["id"], url=url, title=title[:200], published=pub, first_seen=today(), status="new", note=""))
            next_id += 1
        print(f"{src['id']}: {len(found)} article links, {len(new)} new")
        for r in new[:a.show]:
            print(f"  {r['seen_id']} {r['published']} {r['title'][:85]}")
        seen += new
        total_new += len(new)
    if not a.dry_run:
        save_seen(seen)
    print(f"{total_new} new articles" + (" (dry run, nothing written)" if a.dry_run else f" recorded in {SEEN.name}"))


def cmd_list(a):
    rows = [r for r in load_seen() if (not a.status or r["status"] == a.status) and (not a.source or r["source_id"] == a.source)]
    total = len(rows)
    rows.sort(key=lambda r: r["published"] or r["first_seen"], reverse=a.newest)
    if a.limit:
        rows = rows[:a.limit]
    for r in rows:
        print(f"{r['seen_id']} {r['source_id']:8} {r['published'] or r['first_seen']} {r['status']:8} {r['title'][:80]} | {r['url']}")
    print(f"{len(rows)} of {total} articles")


def cmd_read(a):
    seen = {r["seen_id"]: r for r in load_seen()}
    r = seen.get(a.id)
    url = r["url"] if r else a.id
    reader = ps.Reader(a.delay)
    if not reader.allowed(url):
        print("robots.txt forbids reading", url)
        return
    status, text, final = reader.get(url)
    if status != 200 or not text:
        print(f"{url} -> {status or 'error'} {text[:80] if not status else ''}")
        return
    title = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
    date = re.search(r'(?:article:published_time|datePublished|"date"|pubdate)["\']?[^>]{0,40}?content=["\']([^"\']+)', text, re.I) or re.search(r'datetime=["\']([^"\']+)', text)
    print("URL:", final)
    print("TITLE:", clean_text(title.group(1)) if title else "")
    print("DATE:", date.group(1) if date else "(not found: read it in the text)")
    body = re.search(r"<(article|main)\b.*?</\1>", text, re.S | re.I)
    print(clean_text(body.group(0) if body else text)[:a.chars])


def cmd_mark(a):
    rows = load_seen()
    ids = set(a.ids)
    n = 0
    for r in rows:
        if r["seen_id"] in ids:
            r["status"] = a.status
            if a.note:
                r["note"] = (r["note"] + " " + a.note).strip()
            n += 1
    save_seen(rows)
    print(f"{n} of {len(ids)} marked {a.status}")


def cmd_sources(a):
    seen = load_seen()
    for s in load_sources():
        mine = [r for r in seen if r["source_id"] == s["id"]]
        print(f"{s['id']:8} {s.get('country', ''):3} {len(mine):4} seen, {sum(1 for r in mine if r['status'] == 'new'):3} new  {s['name']}  {s['url']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan"); s.add_argument("--source"); s.add_argument("--dry-run", action="store_true"); s.add_argument("--delay", type=float, default=2.0); s.add_argument("--show", type=int, default=8); s.add_argument("--pages", type=int, default=2, help="pages of an API or JSON source to read (default 2; use 20 for a first full read)")
    l = sub.add_parser("list"); l.add_argument("--status"); l.add_argument("--source"); l.add_argument("--newest", action="store_true", help="newest first (default: oldest first)"); l.add_argument("--limit", type=int, default=0)
    r = sub.add_parser("read"); r.add_argument("id"); r.add_argument("--chars", type=int, default=6000); r.add_argument("--delay", type=float, default=2.0)
    m = sub.add_parser("mark"); m.add_argument("ids", nargs="+"); m.add_argument("--status", required=True, choices=STATUS); m.add_argument("--note", default="")
    sub.add_parser("sources")
    a = ap.parse_args()
    return {"scan": cmd_scan, "list": cmd_list, "read": cmd_read, "mark": cmd_mark, "sources": cmd_sources}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
