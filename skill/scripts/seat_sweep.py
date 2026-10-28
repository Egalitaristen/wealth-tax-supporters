#!/usr/bin/env python3
"""List the sitting members of a country's chambers who are not in the register yet, party by party, for a seat sweep (refine/SKILL.md section 6).

Usage: python skill/scripts/seat_sweep.py data/<iso2> [--n 40] [--party NAME] [--out batch.csv] [--adapter NAME]

It reads the chambers' own member lists through the country's seats.py adapter (the same one that draws the Seats tab), then drops
everyone who is already an actor, is in exclusions.csv, or was swept before (a queries.csv row with channel `seat_sweep` that holds the name).
Parties come in order of how much support is already logged in them: supporters who sit for the party today, then their share of the
party's seats. A party with no logged supporter still appears, last, because a party platform is only a place to look, not evidence.
--party limits the batch to one party; --out writes the batch with a suggested search for each name. Standard library only.
"""
import argparse, csv, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import seats  # noqa: E402
import wtdb  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir"); ap.add_argument("--n", type=int, default=40); ap.add_argument("--party"); ap.add_argument("--out")
    ap.add_argument("--adapter", help="an adapter other than the country's own, as for seats.py")
    a = ap.parse_args()
    cc = a.adapter or Path(a.dir).name.split("-")[0]
    if cc not in seats.ADAPTERS:
        sys.exit(f"No seats adapter for '{cc}' (seats.py ADAPTERS): there is no official member list to sweep.")
    db = wtdb.load_all(a.dir)
    chambers = seats.ADAPTERS[cc]()
    known = {seats.norm(x["name"]) for x in db["actors"]} | {seats.norm(x["name"]) for x in db["exclusions"]}
    swept = " ".join(seats.norm(q["query"]) for q in db["queries"] if q.get("channel") == "seat_sweep")
    bodies = {b["body_id"]: b["name"] for b in db["bodies"]}
    sitting = Counter()  # supporters who sit today, by (chamber, party)
    for o in db["positions"]:
        if o["current"] == "y":
            sitting[(bodies.get(o["body_id"], ""), o["party"])] += 1
    todo, size = defaultdict(list), Counter()
    for c in chambers:
        for m in c["members"]:
            size[(c["name"], m["party"])] += 1
            n = seats.norm(m["name"])
            if n in known or n in swept:
                continue
            todo[(c["name"], m["party"])].append(dict(name=m["name"], chamber=c["name"], party=m["party"], place=m.get("place", ""), url=m.get("url", "")))
    order = sorted(todo, key=lambda k: (-sitting[k], -sitting[k] / max(size[k], 1), -size[k]))
    if a.party:
        order = [k for k in order if a.party.lower() in k[1].lower()]
    print(f"{sum(len(v) for v in todo.values())} sitting members not yet in the register or swept, in {len(todo)} chamber-party groups\n")
    print(f"{'supporters':>10} {'of seats':>8}  {'to sweep':>8}  chamber / party")
    for k in order[:25]:
        print(f"{sitting[k]:>10} {size[k]:>8}  {len(todo[k]):>8}  {k[0]} / {k[1]}")
    batch = [m for k in order for m in sorted(todo[k], key=lambda m: m["name"])][:a.n]
    print(f"\nNext {len(batch)} names:")
    for m in batch:
        print(f"  {m['name'][:36]:36} {m['party'][:34]:34} {m['place'][:24]}")
    if a.out:
        with open(a.out, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["name", "chamber", "party", "place", "url"])
            for m in batch:
                w.writerow([m["name"], m["chamber"], m["party"], m["place"], m["url"]])
        print(f"Wrote {len(batch)} names to {a.out}")
    print("\nLog each name you search as a queries.csv row: channel=seat_sweep, query='<name> <the wealth-tax term in the local language>' so the next run skips it.")


if __name__ == "__main__":
    sys.exit(main())
