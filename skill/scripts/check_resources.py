#!/usr/bin/env python3
"""Check the links and dates of the Resources page: data/resources.json and each country's polls in meta.json.

Usage: python skill/scripts/check_resources.py [--only resources|polls|petitions] [--strict] [--delay 0.5]

It never changes a file. For every link it prints one of:
  ok       the page answers
  moved    it redirects to another address; update the link if the new one is the same document
  dead     404, 410, or the host does not answer: find the document again or drop the entry
  blocked  the site refuses scripts (403, 429, a bot check). It is NOT counted as dead: open the page by hand.
           The script does not try to get past a block.
It also lists bills whose state is still "pending" a year after they were published, and resources with a
malformed date, because a bill's status changes after elections and when a house votes. Reading the page to confirm
a status, a date or a poll figure stays a manual step.

Petitions (kind "petition" in resources.json; docs/petitions-spec.md) get a second pass for every entry whose state is "open":
  recheck       the entry was last checked more than 30 days ago
  ending soon   the stated end date is within 14 days
  old           the stated start date is more than 24 months ago
  closed?       the page text carries a closed, ended or victory marker (read the page, then set state to closed)
Run it monthly with the media scan; each flagged petition is opened in a browser by hand. It never changes a file.
Exit code 1 with --strict when any link is dead. Standard library only.
"""
import argparse, json, re, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UA = "Mozilla/5.0 (compatible; WealthTaxSupporters link check; +https://wealthtaxsupporters.com)"
BOT = re.compile(r"just a moment|attention required|verify you are human|captcha|access denied", re.I)
CLOSED = re.compile(r"petition (is |has )?(closed|ended)|this petition is closed|signing (has )?(closed|ended)|victory|p[eé]tition (termin[eé]e|cl[oô]tur[eé]e)|zeichnungsfrist (ist )?(beendet|abgelaufen)|petitie (is )?gesloten|petizione (chiusa|conclusa)|peticion cerrada|petici[oó]n cerrada", re.I)
HEADS = {}  # url -> the first part of the page, for the petition pass


def items(only):
    out = []
    if only in (None, "resources", "petitions"):
        for r in json.load(open(ROOT / "data" / "resources.json", encoding="utf-8")):
            if only == "petitions" and r.get("kind") != "petition":
                continue
            out.append(("resource", r["country"], r["title"], r["url"], r))
    if only in (None, "polls"):
        for meta in sorted((ROOT / "data").glob("*/meta.json")):
            for p in json.load(open(meta, encoding="utf-8")).get("polls", []):
                if p.get("url"):
                    out.append(("poll", meta.parent.name, p.get("question", "")[:80], p["url"], p))
    return out


def probe(url):
    """Return (verdict, detail)."""
    safe = urllib.parse.quote(url, safe="%/:=&?~#+!$,;'@()*[]")  # a non-ASCII address (a German or French petition page) must be percent-encoded
    req = urllib.request.Request(safe, headers={"User-Agent": UA, "Accept": "text/html,application/pdf,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            final, head = r.geturl(), r.read(60000).decode("utf-8", "replace")
            HEADS[url] = head
            if BOT.search(head[:4000]) and "pdf" not in (r.headers.get("Content-Type") or ""):
                return "blocked", "bot check page"
            a, b = urllib.parse.urlsplit(url), urllib.parse.urlsplit(final)
            if (a.netloc.removeprefix("www."), urllib.parse.unquote(a.path).rstrip("/")) != (b.netloc.removeprefix("www."), urllib.parse.unquote(b.path).rstrip("/")):
                return "moved", final
            return "ok", str(r.status)
    except urllib.error.HTTPError as e:
        if e.code in (401, 403, 429, 451, 503):
            return "blocked", f"HTTP {e.code}"
        if e.code in (404, 410):
            return "dead", f"HTTP {e.code}"
        return "blocked", f"HTTP {e.code}"
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as e:
        return "dead", str(getattr(e, "reason", e))[:80]


def months_ago(d, today):
    y, m = int(d[:4]), int(d[5:7]) if len(d) >= 7 else 1
    return (today.year - y) * 12 + today.month - m


def petition_pass(rows, today):
    """Flags for every open petition: recheck, ending soon, old, closed marker on the page. Returns the flagged titles. Never changes a file."""
    flagged = []
    for kind, where, title, url, r in rows:
        if r.get("kind") != "petition" or r.get("state") != "open":
            continue
        why = []
        try:
            if (today - date.fromisoformat(r.get("checked", ""))).days > 30:
                why.append("recheck: last checked " + r["checked"])
        except ValueError:
            why.append("recheck: no valid checked date")
        if r.get("ends"):
            try:
                left = (date.fromisoformat(r["ends"]) - today).days
                if left < 0:
                    why.append("ended " + r["ends"] + ": set state to closed")
                elif left <= 14:
                    why.append(f"ending soon: {r['ends']} ({left} days)")
            except ValueError:
                why.append("ends is not a full date")
        pub = str(r.get("published", ""))
        if re.fullmatch(r"\d{4}(-\d{2}(-\d{2})?)?", pub) and months_ago(pub, today) > 24:
            why.append("old: started " + pub)
        m = CLOSED.search(HEADS.get(url, ""))
        if m:
            why.append(f"closed? the page says {m.group(0)!r}")
        if why:
            flagged.append(title)
            print(f"petition {where:7} {title[:60]}\n         {url}\n         " + "; ".join(why))
    return flagged


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", choices=["resources", "polls", "petitions"])
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
        if r.get("kind") == "petition" and not pub:
            continue  # a petition may have no start date (the page states none)
        if not re.fullmatch(r"\d{4}(-\d{2}(-\d{2})?)?", pub):
            odd.append(f"bad date {pub!r}: {where} {title[:60]}")
        elif kind == "resource" and r.get("kind") == "bill" and r.get("state") == "pending":
            y = int(pub[:4]); m = int(pub[5:7]) if len(pub) >= 7 else 1
            if (today.year - y) * 12 + today.month - m >= 12:
                odd.append(f"pending for a year, re-check at the parliament's page: {where} {title[:60]}")
    for o in odd:
        print(o)
    flagged = petition_pass(rows, today)
    if flagged:
        print(f"{len(flagged)} open petition(s) to open by hand, see above.")
    if a.strict and count.get("dead"):
        sys.exit(1)


if __name__ == "__main__":
    main()
