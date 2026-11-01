#!/usr/bin/env python3
"""Check the links and dates of the Resources page: data/resources.json and each country's polls in meta.json.

Usage: python skill/scripts/check_resources.py [--only resources|polls] [--strict] [--delay 0.5]

It never changes a file. For every link it prints one of:
  ok       the page answers
  moved    it redirects to another address; update the link if the new one is the same document
  dead     404, 410, or the host does not answer: find the document again or drop the entry
  blocked  the site refuses scripts (403, 429, a bot check). It is NOT counted as dead: open the page by hand.
           The script does not try to get past a block.
It also lists bills whose state is still "pending" a year after they were published, and resources with a
malformed date, because a bill's status changes after elections and when a house votes. Reading the page to confirm
a status, a date or a poll figure stays a manual step.
Exit code 1 with --strict when any link is dead. Standard library only.
"""
import argparse, json, re, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UA = "Mozilla/5.0 (compatible; WealthTaxSupporters link check; +https://wealthtaxsupporters.com)"
BOT = re.compile(r"just a moment|attention required|verify you are human|captcha|access denied", re.I)


def items(only):
    out = []
    if only in (None, "resources"):
        for r in json.load(open(ROOT / "data" / "resources.json", encoding="utf-8")):
            out.append(("resource", r["country"], r["title"], r["url"], r))
    if only in (None, "polls"):
        for meta in sorted((ROOT / "data").glob("*/meta.json")):
            for p in json.load(open(meta, encoding="utf-8")).get("polls", []):
                if p.get("url"):
                    out.append(("poll", meta.parent.name, p.get("question", "")[:80], p["url"], p))
    return out


def probe(url):
    """Return (verdict, detail)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/pdf,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            final, head = r.geturl(), r.read(4000).decode("utf-8", "replace")
            if BOT.search(head[:2000]) and "pdf" not in (r.headers.get("Content-Type") or ""):
                return "blocked", "bot check page"
            a, b = urllib.parse.urlsplit(url), urllib.parse.urlsplit(final)
            if (a.netloc.removeprefix("www."), a.path.rstrip("/")) != (b.netloc.removeprefix("www."), b.path.rstrip("/")):
                return "moved", final
            return "ok", str(r.status)
    except urllib.error.HTTPError as e:
        if e.code in (401, 403, 429, 451, 503):
            return "blocked", f"HTTP {e.code}"
        if e.code in (404, 410):
            return "dead", f"HTTP {e.code}"
        return "blocked", f"HTTP {e.code}"
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return "dead", str(getattr(e, "reason", e))[:80]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", choices=["resources", "polls"])
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--delay", type=float, default=0.5, help="seconds between requests")
    a = ap.parse_args()
    rows, count = items(a.only), {}
    for kind, where, title, url, r in rows:
        v, d = probe(url)
        count[v] = count.get(v, 0) + 1
        if v != "ok":
            print(f"{v:8} {kind:8} {where:7} {title[:60]}\n         {url}" + (f"\n         -> {d}" if v == "moved" else f"  ({d})"))
        time.sleep(a.delay)
    print(f"\nChecked {len(rows)} links: " + ", ".join(f"{n} {k}" for k, n in sorted(count.items())))
    today, odd = date.today(), []
    for kind, where, title, url, r in rows:
        pub = str(r.get("published", ""))
        if not re.fullmatch(r"\d{4}(-\d{2}(-\d{2})?)?", pub):
            odd.append(f"bad date {pub!r}: {where} {title[:60]}")
        elif kind == "resource" and r.get("kind") == "bill" and r.get("state") == "pending":
            y = int(pub[:4]); m = int(pub[5:7]) if len(pub) >= 7 else 1
            if (today.year - y) * 12 + today.month - m >= 12:
                odd.append(f"pending for a year, re-check at the parliament's page: {where} {title[:60]}")
    for o in odd:
        print(o)
    if a.strict and count.get("dead"):
        sys.exit(1)


if __name__ == "__main__":
    main()
