#!/usr/bin/env python3
"""Which countries have a records guide, and how much of their official record has been read?

Usage: python skill/scripts/records_status.py [DATA_DIR] [--country xx]

For every data/<folder>: whether skill/references/records/<folder>.md exists, how many documents are tracked in documents.csv by
read status (read / partial / skimmed / unread), how many bills the Resources page lists for the country
(data/resources.json) that documents.csv does not yet track by URL, and the country's vote / sponsorship rows.
Countries are sorted worst first: no guide, then unread or untracked bills. Standard library only.
"""
import argparse, csv, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def rows(p):
    try:
        with open(p, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("data", nargs="?", default=str(ROOT / "data"))
    ap.add_argument("--country")
    a = ap.parse_args()
    data = Path(a.data)
    res = []
    rp = data / "resources.json"
    if rp.exists():
        t = rp.read_text(encoding="utf-8")
        try:
            res = json.loads(t)
        except ValueError:
            res = [json.loads(l) for l in t.splitlines() if l.strip().startswith("{")]
    out = []
    for meta in sorted(data.glob("*/meta.json")):
        c = meta.parent.name
        if a.country and c != a.country:
            continue
        docs = rows(meta.parent / "documents.csv")
        urls = {d["url"] for d in docs if d.get("url")}
        bills = [r for r in res if r.get("country") == c and r.get("kind") == "bill"]
        untracked = [b for b in bills if b.get("url") not in urls]
        st = Counter(d["read_status"] for d in docs)
        ev = Counter(e["evidence_type"] for e in rows(meta.parent / "evidence.csv"))
        guide = (ROOT / "skill" / "references" / "records" / f"{c}.md").exists()
        out.append((guide, st["unread"] + len(untracked) + st["partial"] + st["skimmed"], c, len(docs), st, len(bills), len(untracked), ev))
    out.sort(key=lambda r: (r[0], -r[1], r[2]))
    print(f"{'country':8} {'guide':5} {'docs':>4} {'read':>4} {'part':>4} {'skim':>4} {'unrd':>4} {'bills':>5} {'untracked':>9} {'votes':>5} {'sponsor/motion':>14}")
    for guide, _, c, n, st, nb, nu, ev in out:
        print(f"{c:8} {'yes' if guide else 'NO':5} {n:>4} {st['read']:>4} {st['partial']:>4} {st['skimmed']:>4} {st['unread']:>4} {nb:>5} {nu:>9} "
              f"{ev['vote']:>5} {ev['bill_sponsorship'] + ev['motion_signature'] + ev['motion']:>14}")
    print(f"\n{sum(1 for r in out if r[0])} of {len(out)} countries have a records guide; "
          f"{sum(r[6] for r in out)} bills on the Resources page are not tracked in a documents.csv yet.")


if __name__ == "__main__":
    main()
