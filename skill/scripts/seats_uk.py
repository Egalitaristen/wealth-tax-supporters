#!/usr/bin/env python3
"""Refresh the UK seat data from the UK Parliament Members API (members-api.parliament.uk, Open Parliament Licence).

Usage: python skill/scripts/seats_uk.py data/gb [--bootstrap-others] [--dry-run]

Writes, for data/gb:
  bodies.csv     House of Commons and House of Lords (seat_view=y, so they get a Seats tab), as of today
  seats.csv      each house's seats by party (Labour (Co-op) counts as Labour)
  positions.csv  one row per supporter who sits, or sat, in either house: current=y with the date it was checked
                 when they are on the house's list today, current=n and their end date when they are not

Run it again after an election, a by-election or a peerage, and again whenever people are added: a supporter who is no
longer on a house's list loses their seat (current=n), which is what keeps the Seats tab honest.

--bootstrap-others also creates (once) positions for the other offices named in a politician's `role` text: the
Scottish Parliament, Senedd, London Assembly, European Parliament and councils. Those stay current='' (unchecked)
because no official list was read for them; they feed no Seats tab until a body is given seat_view=y and checked.
Standard library only.
"""
import argparse, datetime as dt, json, re, sys, time, unicodedata, urllib.parse, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import wtdb  # noqa: E402

API = "https://members-api.parliament.uk/api/Members/Search"
COMMONS_SEATS = 650
HOUSES = {1: "House of Commons", 2: "House of Lords"}
SOURCE = {1: "https://members.parliament.uk/members/commons", 2: "https://members.parliament.uk/members/lords"}
MERGE = {"Labour (Co-op)": "Labour"}
# Left to right across the chamber; parties not listed sit in the middle, largest first.
ORDER = {1: ["Green Party", "Plaid Cymru", "Scottish National Party", "Your Party", "Labour", "Sinn Féin",
             "Social Democratic & Labour Party", "Liberal Democrat", "Alliance Party", "Independent", "Speaker",
             "Conservative", "Democratic Unionist Party", "Traditional Unionist Voice", "Reform UK"],
         2: ["Green Party", "Plaid Cymru", "Labour", "Liberal Democrat", "Crossbench", "Bishops", "Lord Speaker",
             "Non-affiliated", "Independent Ulster Unionist", "Ulster Unionist Party", "Conservative Independent",
             "Conservative", "Democratic Unionist Party"]}
TITLES = re.compile(r"\b(rt hon|hon|dr|mr|mrs|ms|miss|sir|dame|lord|lady|baroness|baron|prof|professor|reverend|rev|the|of|"
                    r"mp|msp|kc|obe|cbe|mbe|oc|viscount|earl|countess|duke|marquess)\b")


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = TITLES.sub(" ", s)
    return " ".join(re.sub(r"[^a-z ]", " ", s).split())


def get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    for t in range(6):
        try:
            return json.load(urllib.request.urlopen(url, timeout=60))
        except Exception as e:  # the API answers 5xx now and then
            print(f"  retry {t + 1}: {str(e)[:60]}", file=sys.stderr)
            time.sleep(2)
    sys.exit(f"The Parliament API did not answer: {url}")


def current(house):
    out, skip = [], 0
    while True:
        d = get({"House": house, "IsCurrentMember": "true", "take": 20, "skip": skip})
        out += [i["value"] for i in d["items"]]
        skip += 20
        if skip >= d["totalResults"]:
            return out


def last_membership(name, house):
    """The latest membership of a person who is not on today's list: the API gives its end date."""
    d = get({"Name": name, "House": house, "take": 20})
    hits = [i["value"] for i in d["items"] if norm(i["value"]["nameDisplayAs"]) == norm(name)
            or norm(i["value"]["nameDisplayAs"]).split()[-1:] == norm(name).split()[-1:]]
    return hits[0] if len(hits) == 1 else None


def ymd(s):
    return (s or "")[:10]


def party_of(m):
    n = m["latestParty"]["name"]
    return MERGE.get(n, n)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir")
    ap.add_argument("--bootstrap-others", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    today = dt.date.today().isoformat()
    db = wtdb.load_all(a.dir)
    now = {h: current(h) for h in HOUSES}
    print({HOUSES[h]: len(m) for h, m in now.items()})

    # ---- bodies and seats
    bodies = [b for b in db["bodies"] if b["name"] not in HOUSES.values()]
    bid = {}
    for h, name in HOUSES.items():
        row = next((b for b in db["bodies"] if b["name"] == name), None) or {"body_id": wtdb.next_id(db["bodies"] + bodies, "bodies")}
        row.update(name=name, level="national", kind="chamber", seats=str(COMMONS_SEATS if h == 1 else len(now[h])),
                   as_of=today, source_url=SOURCE[h], seat_view="y")
        bodies.append(row)
        bid[h] = row["body_id"]
    seats = [s for s in db["seats"] if s["body_id"] not in bid.values()]
    for h in HOUSES:
        count, colour = {}, {}
        for m in now[h]:
            p = party_of(m)
            count[p] = count.get(p, 0) + 1
            colour.setdefault(p, m["latestParty"].get("backgroundColour") or "")
        if h == 1 and sum(count.values()) < COMMONS_SEATS:
            count["Vacant"] = COMMONS_SEATS - sum(count.values())
        order = ORDER[h]
        ranked = sorted(count, key=lambda p: (order.index(p) if p in order else 50, -count[p]))
        for i, p in enumerate(ranked, start=1):
            seats.append({"seat_id": wtdb.next_id(seats, "seats"), "body_id": bid[h], "party": p, "seats": str(count[p]),
                          "colour": colour.get(p, ""), "order": str(i)})

    # ---- positions for supporters in either house
    actors = [x for x in db["actors"] if x["kind"] == "person" and x["actor_type"] == "politician"]
    index = {}
    for h, ms in now.items():
        for m in ms:
            index.setdefault(norm(m["nameDisplayAs"]), []).append((h, m))
    keep = [o for o in db["positions"] if o["body_id"] not in bid.values()]
    new, report = [], []
    for x in actors:
        n = norm(x["name"])
        hit = index.get(n) or []
        words = set(norm(x["name"] + " " + x["role"]).split())
        if not hit and re.search(r"(?i)\b(peer|lord|baroness)\b", x["role"]):
            # peers appear by title ("Baroness Bennett of Manor Castle"): every word of that name must be in the register's name or role
            hit = [v for k, vs in index.items() for v in vs if v[0] == 2 and set(k.split()) <= words]
            if hit:  # "Lord Jones" fits "Baroness Jones of Moulsecoomb" too: keep the most specific name
                top = max(len(norm(v[1]["nameDisplayAs"]).split()) for v in hit)
                hit = [v for v in hit if len(norm(v[1]["nameDisplayAs"]).split()) == top]
        if not hit:
            # a changed name ("Emma Lewell-Buck" is now "Emma Lewell"): the same seat and two shared words
            seat = re.search(r"\bMP for ([^(;,]+)", x["role"])
            if seat:
                s = norm(seat.group(1))
                hit = [v for vs in index.values() for v in vs if v[0] == 1 and norm(v[1]["latestHouseMembership"]["membershipFrom"]) == s
                       and len(set(norm(v[1]["nameDisplayAs"]).split()) & set(n.split())) >= 2]
        if len(hit) == 1:
            h, m = hit[0]
            mem = m["latestHouseMembership"]
            new.append({"position_id": "", "actor_id": x["actor_id"], "body_id": bid[h],
                        "role": "MP" if h == 1 else "Member of the House of Lords", "party": party_of(m),
                        "geo_unit_id": x["geo_unit_id"] if h == 1 else "", "start": ymd(mem["membershipStartDate"]),
                        "end": "", "current": "y", "member_ref": str(m["id"]), "checked": today, "source_url": f"https://members.parliament.uk/member/{m['id']}/contact"})
            continue
        h = 1 if re.search(r"\bMP\b", x["role"]) else 2 if re.search(r"(?i)\b(peer|lord|baroness)\b", x["role"]) else 0
        if not h:
            continue
        m = last_membership(x["name"], h)
        if m and m["latestHouseMembership"]["membershipEndDate"]:
            mem = m["latestHouseMembership"]
            new.append({"position_id": "", "actor_id": x["actor_id"], "body_id": bid[h],
                        "role": "MP" if h == 1 else "Member of the House of Lords", "party": party_of(m),
                        "geo_unit_id": x["geo_unit_id"] if h == 1 else "", "start": ymd(mem["membershipStartDate"]),
                        "end": ymd(mem["membershipEndDate"]), "current": "n", "member_ref": str(m["id"]), "checked": today,
                        "source_url": f"https://members.parliament.uk/member/{m['id']}/contact"})
        else:
            report.append(f"{x['actor_id']} {x['name']}: role says {x['role'][:50]!r} but no unique match in the {HOUSES[h]} (api: {'found, no end date' if m else 'none'})")
    positions = keep + new
    for o in positions:
        if not o["position_id"]:
            o["position_id"] = wtdb.next_id(positions, "positions")

    if a.bootstrap_others:
        positions += others(actors, bodies, positions, db)

    # ---- what changed for the people already on the site
    cur_actor = {o["actor_id"] for o in new if o["current"] == "y"}
    for x in actors:
        mine = [o for o in new if o["actor_id"] == x["actor_id"]]
        if mine and mine[0]["current"] == "n" and x["status"] == "active":
            report.append(f"{x['actor_id']} {x['name']}: left the {bodies_name(mine[0], bodies)} on {mine[0]['end']} but is status=active, role {x['role'][:50]!r}: update role and status")
    print(f"{len(cur_actor)} supporters currently sit; {sum(1 for o in new if o['current'] == 'n')} sat before and no longer do")
    for r in report:
        print("  check:", r)
    if a.dry_run:
        return
    wtdb.save(a.dir, "bodies", bodies)
    wtdb.save(a.dir, "seats", seats)
    wtdb.save(a.dir, "positions", positions)
    print("Wrote bodies.csv, seats.csv and positions.csv")


def bodies_name(o, bodies):
    return next((b["name"] for b in bodies if b["body_id"] == o["body_id"]), "house")


OTHER = [  # (pattern on the role text, body name, level, kind)
    (r"\bMSPs?\b", "Scottish Parliament", "regional", "chamber"),
    (r"\bSenedd\b|\bMS\b", "Senedd Cymru", "regional", "chamber"),
    (r"London Assembly", "London Assembly", "regional", "chamber"),
    (r"\bMEP\b|European Parliament", "European Parliament", "supranational", "chamber"),
]


def others(actors, bodies, positions, db):
    """Positions for offices other than the two Westminster houses, from the role text. Unchecked (current='')."""
    have = {(o["actor_id"], o["body_id"]) for o in positions}
    out = []

    def body(name, level, kind):
        b = next((b for b in bodies if b["name"] == name), None)
        if not b:
            b = {"body_id": wtdb.next_id(bodies, "bodies"), "name": name, "level": level, "kind": kind, "seats": "",
                 "as_of": "", "source_url": "", "seat_view": "", "notes": ""}
            bodies.append(b)
        return b["body_id"]

    for x in actors:
        role = x["role"]
        if re.search(r"\bMP\b", role) or re.search(r"(?i)\b(peer|lord|baroness)\b", role):
            continue
        found = []
        for pat, name, level, kind in OTHER:
            if re.search(pat, role):
                found.append((name, level, kind))
        for m in re.finditer(r"([A-Z][\w' &-]+?(?: [A-Z][\w'&-]+)*) (?:District |County |Borough |City )?Council", role):
            found.append((m.group(0).strip().split(", ")[-1], "local", "council"))
        for m in re.finditer(r"\b([A-Z][\w'-]+(?: [A-Z][\w'-]+)*) councillor", role):
            found.append((m.group(1) + " Council", "local", "council"))
        if re.search(r"(?i)\bcouncillor\b", role) and not any(k == "council" for _, _, k in found):
            found.append(("(council not named)", "local", "council"))
        for name, level, kind in dict.fromkeys(found):
            b = body(name, level, kind)
            if (x["actor_id"], b) in have:
                continue
            have.add((x["actor_id"], b))
            out.append({"position_id": wtdb.next_id(positions + out, "positions"), "actor_id": x["actor_id"], "body_id": b,
                        "role": role[:120], "party": x["party"], "geo_unit_id": x["geo_unit_id"], "start": "", "end": "",
                        "current": "", "member_ref": "", "checked": "", "source_url": ""})
    return out


if __name__ == "__main__":
    sys.exit(main())
