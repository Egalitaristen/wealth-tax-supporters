#!/usr/bin/env python3
"""List what the register has read but the Resources page does not show yet.

Usage: python skill/scripts/resource_gaps.py [data/<iso2> ...] [--top 25]

Research runs read bills, motions, committee reports and papers (documents.csv) and cite them in evidence rows, but a
document only reaches the site's Resources page (/resources) when it has an entry in data/resources.json. This lists, for
each country folder given (all of them by default):
  * supporters and resource pages, so a register with many supporters and no page stands out;
  * documents.csv rows of kind bill, motion, government_proposal or report whose URL is not the url or a link of any resource
    page of that country (a candidate for a new page; read it first, see skill/references/data-format.md, "Papers, reports and bills");
  * whether the country has any bill, report or paper page at all.
It writes nothing. Standard library only.
"""
import argparse, collections, csv, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
KINDS = ("bill", "motion", "government_proposal", "report", "committee_report", "audit_or_statistics_report")


def norm(u):
    return re.sub(r"^https?://(www\.)?", "", (u or "").strip().lower()).rstrip("/")


def rows(path):
    return list(csv.DictReader(open(path, encoding="utf-8"))) if path.exists() else []


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dirs", nargs="*"); ap.add_argument("--top", type=int, default=25)
    a = ap.parse_args()
    res = json.load(open(ROOT / "data" / "resources.json", encoding="utf-8"))
    pages, urls = collections.defaultdict(collections.Counter), collections.defaultdict(set)
    for r in res:
        pages[r["country"]][r["kind"]] += 1
        urls[r["country"]].add(norm(r.get("url")))
        urls[r["country"]].update(norm(l.get("url")) for l in r.get("links") or [])
    dirs = [Path(d) for d in a.dirs] or sorted(p for p in (ROOT / "data").iterdir() if (p / "actors.csv").exists())
    report = []
    for d in dirs:
        cc = d.name
        supporters = len(rows(d / "actors.csv"))
        docs = [x for x in rows(d / "documents.csv") if x.get("kind") in KINDS and norm(x.get("url")) not in urls[cc]]
        report.append((cc, supporters, sum(pages[cc].values()), pages[cc]["bill"], pages[cc]["report"] + pages[cc]["paper"], docs))
    none = [r for r in report if r[2] == 0]
    print(f"{len(report)} registers; {len(none)} have no resource page ({sum(r[1] for r in none)} supporters).")
    print("\nNo resource page, most supporters first:")
    for cc, n, *_ in sorted(none, key=lambda r: -r[1])[:a.top]:
        print(f"  {cc}: {n} supporters")
    print("\nRead but not on the Resources page (documents.csv rows not linked by any page):")
    for cc, n, p, b, rp, docs in sorted(report, key=lambda r: -len(r[5]))[:a.top]:
        if docs:
            print(f"  {cc}: {len(docs)} documents ({n} supporters, {p} pages: {b} bills, {rp} reports/papers); first: {docs[0]['document_id']} {docs[0]['title'][:60]}")
    print("\nNo bill page / no report or paper page, most supporters first:")
    for cc, n, p, b, rp, _ in sorted(report, key=lambda r: -r[1])[:a.top]:
        if not b or not rp:
            print(f"  {cc}: {n} supporters; bill pages {b}, report/paper pages {rp}")


if __name__ == "__main__":
    sys.exit(main())
