#!/usr/bin/env python3
"""Refresh the US Congress seat data from the congress-legislators project (public domain, CC0).

Usage: python skill/scripts/seats_us.py data/us [--bootstrap-others] [--dry-run]

Source: https://github.com/unitedstates/congress-legislators (legislators-current.json and legislators-historical.json),
a public-domain compilation of the Biographical Directory of the US Congress and the chambers' own member lists, updated
by volunteers as members take and leave office.

Writes, for data/us:
  bodies.csv     the US Senate (100) and the US House of Representatives (435 voting seats plus 6 non-voting delegates
                 and resident commissioners = 441), seat_view=y, as of today
  seats.csv      each chamber's seats by party, with a Vacant row for empty seats
  positions.csv  one row per supporter who sits, or sat, in Congress: current=y with the date it was checked when they
                 are on the current list, current=n and their last term's end date when they are not

Run it again after every election, special election, resignation or death, and whenever politicians are added: a supporter
who is no longer on the list loses the seat (current=n), which keeps the Seats tab honest. Supporters are matched by
Wikidata ID, then by name and state.

--bootstrap-others also creates (once) unchecked positions (current='') for state legislators and for mayors and city
councils, from the role text and the place the actor is in. Standard library only.
"""
import argparse, datetime as dt, json, re, sys, time, unicodedata, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import wtdb  # noqa: E402

BASE = "https://unitedstates.github.io/congress-legislators/"
SRC = "https://github.com/unitedstates/congress-legislators"
BODIES = {"sen": ("U.S. Senate", 100, "https://www.senate.gov/senators/index.htm", "The 100 senators."),
          "rep": ("U.S. House of Representatives", 441, "https://www.house.gov/representatives",
                  "435 voting seats plus 5 delegates and the Resident Commissioner of Puerto Rico, who do not vote on the floor.")}
PARTY = {"Democrat": "Democratic Party", "Republican": "Republican Party"}
COLOUR = {"Democratic Party": "3b72d9", "Republican Party": "d64a4a", "Independent": "8a8680", "Libertarian": "e0b030"}
ORDER = ["Democratic Party", "Independent", "Libertarian", "Republican Party", "Vacant"]
CONG = re.compile(r"U\.?S\.? (Representative|Senator|Rep)|Member of Congress|Congress(wo)?man|^Rep\.|^Sen\.|United States (Senator|Representative)|U\.S\. Delegate|Delegate to Congress|\bUS Senator\b|\bUS Rep", re.I)


def fetch(name):
    for t in range(5):
        try:
            return json.load(urllib.request.urlopen(BASE + name, timeout=120))
        except Exception as e:
            print(f"  retry {t + 1}: {str(e)[:60]}", file=sys.stderr)
            time.sleep(3)
    sys.exit(f"Could not read {BASE + name}")


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return " ".join(re.sub(r"[^a-z ]", " ", re.sub(r"\b(jr|sr|ii|iii|iv|dr|hon)\b", " ", s)).split())


def party_of(term):
    return PARTY.get(term["party"], term["party"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir")
    ap.add_argument("--bootstrap-others", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    today = dt.date.today().isoformat()
    db = wtdb.load_all(a.dir)
    cur, hist = fetch("legislators-current.json"), fetch("legislators-historical.json")
    by_q, by_name = {}, {}
    for m in cur + hist:
        q = m["id"].get("wikidata")
        if q:
            by_q[q] = m
        by_name.setdefault((norm(m["name"].get("official_full") or m["name"]["first"] + " " + m["name"]["last"]), m["terms"][-1]["state"]), []).append(m)
    now = {id(m) for m in cur}
    sitting = {"sen": [m for m in cur if m["terms"][-1]["type"] == "sen"], "rep": [m for m in cur if m["terms"][-1]["type"] == "rep"]}
    print({BODIES[k][0]: len(v) for k, v in sitting.items()})

    # ---- bodies and seats
    names = {b[0] for b in BODIES.values()}
    bodies = [b for b in db["bodies"] if b["name"] not in names]
    bid = {}
    for k, (name, total, src, note) in BODIES.items():
        row = next((b for b in db["bodies"] if b["name"] == name), None) or {"body_id": wtdb.next_id(db["bodies"] + bodies, "bodies")}
        row.update(name=name, level="national", kind="chamber", seats=str(total), as_of=today, source_url=src, seat_view="y", notes=note)
        bodies.append(row)
        bid[k] = row["body_id"]
    seats = [s for s in db["seats"] if s["body_id"] not in bid.values()]
    for k, (name, total, src, note) in BODIES.items():
        count = {}
        for m in sitting[k]:
            p = party_of(m["terms"][-1])
            count[p] = count.get(p, 0) + 1
        if sum(count.values()) < total:
            count["Vacant"] = total - sum(count.values())
        for i, p in enumerate(sorted(count, key=lambda p: (ORDER.index(p) if p in ORDER else 3, -count[p])), start=1):
            seats.append({"seat_id": wtdb.next_id(seats, "seats"), "body_id": bid[k], "party": p, "seats": str(count[p]),
                          "colour": COLOUR.get(p, "8a8680") if p != "Vacant" else "", "order": str(i)})

    # ---- positions for supporters in Congress
    actors = [x for x in db["actors"] if x["kind"] == "person" and x["actor_type"] == "politician"]
    keep = [o for o in db["positions"] if o["body_id"] not in bid.values()]
    new, report = [], []

    def pos(x, m, k, term_end, is_now):
        terms = [t for t in m["terms"] if t["type"] == k]
        last = terms[-1]
        role = {"sen": "U.S. Senator", "rep": "U.S. Delegate" if last["state"] in ("DC", "PR", "GU", "VI", "AS", "MP") else "U.S. Representative"}[k]
        return {"position_id": "", "actor_id": x["actor_id"], "body_id": bid[k], "role": role, "party": party_of(last),
                "geo_unit_id": x["geo_unit_id"], "start": terms[0]["start"], "end": "" if is_now else term_end,
                "current": "y" if is_now else "n", "member_ref": m["id"]["bioguide"], "checked": today,
                "source_url": f"https://bioguide.congress.gov/search/bio/{m['id']['bioguide']}"}

    for x in actors:
        if not CONG.search(x["role"]):
            continue
        m = by_q.get(x["wikidata_qid"])
        if not m:
            st = re.search(r"\((?:[A-Z]-)?([A-Z]{2})(?:-\d+)?\)", x["role"])
            c = by_name.get((norm(x["name"]), st.group(1) if st else None)) if st else None
            m = c[0] if c and len(c) == 1 else None
        if not m:  # no state in the role text: a name that is unique among Congress members
            c = [v for (n, _), vs in by_name.items() if n == norm(x["name"]) for v in vs]
            m = c[0] if len(c) == 1 else None
        if not m:
            report.append(f"{x['actor_id']} {x['name']}: role {x['role'][:50]!r} but not found in the Congress files")
            continue
        k = m["terms"][-1]["type"] if id(m) in now else next((t["type"] for t in reversed(m["terms"]) if t["type"] in BODIES), "rep")
        new.append(pos(x, m, k, m["terms"][-1]["end"], id(m) in now))
    positions = keep + new
    for o in positions:
        if not o["position_id"]:
            o["position_id"] = wtdb.next_id(positions, "positions")
    if a.bootstrap_others:
        positions = [o for o in positions if o["body_id"] in bid.values() or o["current"] or o["source_url"]]  # drop earlier unchecked ones
        used = {o["body_id"] for o in positions}
        bodies[:] = [b for b in bodies if b["seat_view"] == "y" or b["body_id"] in used]
        positions += others(actors, bodies, positions, db)

    # ---- what disagrees with the register
    by_actor = {x["actor_id"]: x for x in actors}
    for o in new:
        x = by_actor[o["actor_id"]]
        if o["current"] == "n" and x["status"] == "active":
            report.append(f"{x['actor_id']} {x['name']}: left Congress on {o['end']} but is status=active, role {x['role'][:50]!r}: update role and status")
        if o["current"] == "y" and x["status"] != "active":
            report.append(f"{x['actor_id']} {x['name']}: sits in Congress but is status={x['status']}")
        if o["current"] == "y" and x.get("party") and PARTY.get(x["party"], x["party"]) != o["party"] and x["party"] not in ("Democratic Party", "Republican Party", "Independent"):
            report.append(f"{x['actor_id']} {x['name']}: party {x['party']!r} in the register, {o['party']!r} in Congress")
    sit = sum(1 for o in new if o["current"] == "y")
    print(f"{sit} supporters sit in Congress today ({sum(1 for o in new if o['current'] == 'y' and o['body_id'] == bid['sen'])} Senate, "
          f"{sum(1 for o in new if o['current'] == 'y' and o['body_id'] == bid['rep'])} House); {len(new) - sit} served before and no longer do")
    for r in report:
        print("  check:", r)
    if a.dry_run:
        return
    wtdb.save(a.dir, "bodies", bodies)
    wtdb.save(a.dir, "seats", seats)
    wtdb.save(a.dir, "positions", positions)
    print("Wrote bodies.csv, seats.csv and positions.csv")


LOWER = {"CA": "Assembly", "NV": "Assembly", "NJ": "General Assembly", "NY": "Assembly", "WI": "Assembly",
         "MD": "House of Delegates", "VA": "House of Delegates", "WV": "House of Delegates"}
TYPOS = {"Vallego": "Vallejo", "Monterrey Park": "Monterey Park", "Citrust Heights": "Citrus Heights", "Counil": "Council", "CIty": "City"}
WORD = r"[A-Z][\w.'’-]+"
NAME = rf"({WORD}(?: (?!City\b|Council|Mayor|Vice\b|Deputy\b|Pro\b|Member|Former\b|County\b|District\b|Board\b|Of\b)(?:{WORD})){{0,2}})"
CITY = [rf"(?:City|Town|Village) of {NAME}", rf"Mayor of {NAME}", rf"Mayor,? {NAME}\b(?! Council)", rf"{NAME} (?:City )?(?:Council|Councilmember|Council Member|Mayor|Vice Mayor|Deputy Mayor|Mayor Pro Tem)",
        rf"(?:Councilmember|Council Member|Councilman|Councilwoman),? (?:for )?(?:the )?{NAME}"]
SPECIAL = re.compile(r"((?:[A-Z][\w&.'-]+ ){1,5}(?:Unified School District|Union High School District|School District|USD|Community College District|CCD|Community College|"
                     r"Board of Education|Health District|Park District|Water District|Transit))")


def local_body(role, loc):
    """(name, kind) of a local office from its role text, with the place where the role names one."""
    r = role
    for bad, good in TYPOS.items():
        r = r.replace(bad, good)
    state = loc[1] if len(loc) > 1 else ""
    m = re.search(r"([A-Z][a-z]+(?: [A-Z][a-z]+)*) County (?:Board of Supervisors|Supervisor|Council)", r) or re.search(r"([A-Z][a-z]+(?: [A-Z][a-z]+)*) County Board", r)
    if m:
        return f"{re.sub(r'^Former ', '', m.group(1))} County Board of Supervisors", "council"
    if re.search(r"(?i)\bboard of supervisors\b", r) and re.search(r"San Francisco", r + " ".join(loc)):
        return "San Francisco Board of Supervisors", "council"
    m = SPECIAL.search(r)
    if m:
        return m.group(1).strip().replace(" USD", " Unified School District").replace(" CCD", " Community College District"), "other"
    if re.search(r"(?i)equalization", r):
        return f"{state or 'California'} State Board of Equalization", "other"
    if len(loc) > 2 and loc[-1] and loc[-1] in r and re.search(r"(?i)mayor|council", r):  # the register's own place name: "Culver City", "National City"
        return f"{loc[-1]} city government", "council"
    for pat in CITY:
        m = re.search(pat, r)
        if m and m.group(1).split()[0] not in ("City", "County", "Pro", "Former", "Vice", "Deputy", "Mayor"):
            return f"{m.group(1).strip()} city government", "council"
    if len(loc) > 2 and re.search(r"(?i)mayor|council", r):
        return f"{loc[-1]} city government", "council"
    return f"{state or 'US'} local offices (place not stated)", "other"


def others(actors, bodies, positions, db):
    """Unchecked positions (current='') for state legislators and local officials, from the role text and the place."""
    have = {(o["actor_id"], o["body_id"]) for o in positions}
    out = []

    def body(name, level, kind):
        b = next((b for b in bodies if b["name"] == name), None)
        if not b:
            b = {"body_id": wtdb.next_id(bodies, "bodies"), "name": name, "level": level, "kind": kind, "seats": "", "as_of": "",
                 "source_url": "", "seat_view": "", "notes": ""}
            bodies.append(b)
        return b["body_id"]

    for x in actors:
        role, loc = x["role"], [p.strip() for p in x.get("location", "").split(">")]
        if CONG.search(role):
            continue
        state = loc[1] if len(loc) > 1 else ""
        if re.search(r"(?i)state (senator|senate)|\bsenator\b", role) and state:
            name, level, kind = f"{state} State Senate", "regional", "chamber"
        elif re.search(r"(?i)state rep|assembly|delegate|house of rep", role) and state and not re.search(r"(?i)city|county|council", role):
            code = next((c for c, n in STATES.items() if n == state), "")
            name, level, kind = f"{state} {LOWER.get(code, 'House of Representatives')}", "regional", "chamber"
        elif re.search(r"(?i)mayor|council|supervisor|alderm|commissioner|selectboard|trustee|board|equalization", role):
            name, kind = local_body(role, loc)
            level = "regional" if "State Board" in name else "local"
        else:
            continue
        b = body(name, level, kind)
        if (x["actor_id"], b) in have:
            continue
        have.add((x["actor_id"], b))
        out.append({"position_id": wtdb.next_id(positions + out, "positions"), "actor_id": x["actor_id"], "body_id": b,
                    "role": role[:120], "party": x["party"], "geo_unit_id": x["geo_unit_id"], "start": "", "end": "",
                    "current": "", "member_ref": "", "checked": "", "source_url": ""})
    return out


STATES = {"AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
          "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
          "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana",
          "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
          "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
          "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
          "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota",
          "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington",
          "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"}

if __name__ == "__main__":
    sys.exit(main())
