#!/usr/bin/env python3
"""Re-apply the current accept rules to the accounts profile_scan.py added, and take out those that no longer pass.

Usage: python skill/scripts/profile_scan_recheck.py [--date YYYY-MM-DD] [--dry-run]

Looks at every profiles.csv row whose source starts "linked from" and was checked on the date (default today). For a person the account stays if its
handle matches their name; vendor accounts (Wix and the like) never stay. An
organisation's accounts are not touched. Removed rows are noted in profile_checks.csv, so the check is not repeated blindly.
"""
import argparse, datetime as dt, os, re, sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wtdb  # noqa: E402
import profile_scan as ps  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", default=dt.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    removed_total = 0
    for d in sorted((ROOT / "data").iterdir()):
        if not (d / "profile_checks.csv").exists():
            continue
        actors = {r["actor_id"]: r for r in wtdb.load(str(d), "actors")}
        profiles = wtdb.load(str(d), "profiles")
        checks = wtdb.load(str(d), "profile_checks")
        keep, gone = [], []
        for p in profiles:
            actor = actors.get(p["actor_id"])
            if actor and p["source"].startswith("linked from") and p["checked"] == a.date:
                handle = re.sub(r"[^a-z0-9]", "", p["url"].split("//", 1)[-1].split("/", 1)[-1].lower())  # the whole path: facebook.com/pages/<Name>/<id> carries the name in the middle
                vendor = handle.startswith(ps.VENDOR)
                if actor["kind"] == "person":
                    toks = ps.name_tokens(actor["name"], True)
                    ok = any(t in handle for t in toks)
                else:
                    ok = True
                if vendor or not ok:
                    gone.append(p)
                    continue
            keep.append(p)
        if not gone:
            continue
        for p in gone:
            print(f"{d.name}:{p['actor_id']} {actors[p['actor_id']]['name'][:30]:30} removed {p['platform']} {p['url']}  (from {p['source'][12:60]})")
        removed_total += len(gone)
        if a.dry_run:
            continue
        for c in checks:
            mine = [p for p in gone if p["actor_id"] == c["actor_id"] and c["checked"] == a.date]
            if mine:
                left = [x for x in (c["found"] or "").split(";") if x and x not in {p["platform"] for p in mine}]
                c["found"] = ";".join(left)
                if not left and c["result"] == "found":
                    c["result"] = "none"
                c["note"] = (c["note"] + "; removed on review (employer's or unrelated account): " + ", ".join(f"{p['platform']} {p['url']}" for p in mine))[:400].lstrip("; ")
        wtdb.save(str(d), "profiles", keep)
        wtdb.save(str(d), "profile_checks", checks)
    print("removed", removed_total)


if __name__ == "__main__":
    sys.exit(main())
