#!/usr/bin/env python3
"""Leads found outside the area you are researching, kept so a later run on that area starts from them.

Usage:
  python skill/scripts/leads.py add --country AE --name "Name" --url https://... [--role "..."] [--kind person|organisation]
                                    [--note "what they said, why it is a lead"] [--from data/mx]
  python skill/scripts/leads.py list [--country MX] [--status open]      (a country also matches its regions: US matches US-CA)
  python skill/scripts/leads.py close L0007 --status used|rejected|duplicate [--run R003]
  python skill/scripts/leads.py summary                                  (open leads per country)

Rule of thumb: while researching or refining one area you will meet supporters of another (the UN run finds a UAE minister, the
Mexico run finds a Cuban economist). Do not add them to this area's register, and do not drop them: add a lead. The run that
later starts or refines their country reads `leads.py list --country <iso2>` first. One row per person or organisation, only public
figures and organisations, always with the link where you saw the statement, never personal data. The file is data/leads.csv
(plain CSV, committed with the run's pull request). Standard library only.
"""
import argparse, csv, datetime as dt, sys
from pathlib import Path

FILE = Path(__file__).resolve().parent.parent.parent / "data" / "leads.csv"
COLS = ["lead_id", "country", "name", "kind", "role", "source_url", "note", "found_in", "found_date", "status", "used_in"]
STATUS = ("open", "used", "rejected", "duplicate")


def load():
    if not FILE.exists():
        return []
    with open(FILE, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def save(rows):
    with open(FILE, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, lineterminator="\n")
        w.writeheader()
        w.writerows({c: r.get(c, "") for c in COLS} for r in rows)


def matches(row_country, want):
    r, w = row_country.upper(), want.upper()
    return r == w or r.startswith(w + "-")


def next_id(rows):
    n = max([int(r["lead_id"][1:]) for r in rows if r["lead_id"][1:].isdigit()] or [0]) + 1
    return f"L{n:04d}"


def show(rows):
    for r in rows:
        print(f"{r['lead_id']}  {r['country']:6} {r['status']:9} {r['name']}  [{r['kind']}]  {r['role'][:60]}")
        if r["note"]:
            print(f"        {r['note'][:200]}")
        print(f"        {r['source_url']}   (found in {r['found_in'] or '?'}, {r['found_date']})")
    print(f"{len(rows)} lead(s)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a_ = sub.add_parser("add")
    a_.add_argument("--country", required=True, help="ISO 3166-1 alpha-2 (AE), a region (US-CA), or a body (UN, EU, AU) when it has no country")
    a_.add_argument("--name", required=True); a_.add_argument("--url", required=True)
    a_.add_argument("--role", default=""); a_.add_argument("--kind", default="person", choices=("person", "organisation"))
    a_.add_argument("--note", default=""); a_.add_argument("--from", dest="found_in", default="", help="the area being researched, e.g. data/mx")
    l_ = sub.add_parser("list")
    l_.add_argument("--country"); l_.add_argument("--status", default="open", help="open (default), used, rejected, duplicate or all")
    c_ = sub.add_parser("close")
    c_.add_argument("lead_id"); c_.add_argument("--status", required=True, choices=STATUS[1:]); c_.add_argument("--run", default="")
    sub.add_parser("summary")
    a = ap.parse_args()
    rows = load()
    if a.cmd == "add":
        if not a.url.startswith(("http://", "https://")):
            sys.exit("--url must start with http(s)://")
        same = [r for r in rows if r["name"].lower() == a.name.lower() and matches(r["country"], a.country) and r["status"] == "open"]
        if same:
            sys.exit(f"Already an open lead for {a.name} in {a.country}: {same[0]['lead_id']}. Add the new link to its note instead.")
        row = dict(lead_id=next_id(rows), country=a.country.upper(), name=a.name, kind=a.kind, role=a.role, source_url=a.url, note=a.note,
                   found_in=a.found_in.rstrip("/").split("/")[-1] if a.found_in else "", found_date=dt.date.today().isoformat(), status="open", used_in="")
        rows.append(row)
        save(rows)
        print(f"Added {row['lead_id']}: {a.name} ({row['country']})")
    elif a.cmd == "list":
        sel = [r for r in rows if (not a.country or matches(r["country"], a.country)) and (a.status == "all" or r["status"] == a.status)]
        show(sel)
    elif a.cmd == "close":
        r = next((r for r in rows if r["lead_id"] == a.lead_id), None)
        if not r:
            sys.exit(f"No lead {a.lead_id}")
        r["status"], r["used_in"] = a.status, a.run
        save(rows)
        print(f"{a.lead_id} marked {a.status}")
    else:
        from collections import Counter
        c = Counter(r["country"] for r in rows if r["status"] == "open")
        for k, n in sorted(c.items(), key=lambda x: (-x[1], x[0])):
            print(f"{k:6} {n}")
        print(f"{sum(c.values())} open lead(s) in {len(c)} area(s)")


if __name__ == "__main__":
    sys.exit(main())
