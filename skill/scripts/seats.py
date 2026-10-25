#!/usr/bin/env python3
"""Refresh a country's legislature seats from the parliament's own open member list.

Usage: python skill/scripts/seats.py data/<iso2> [--dry-run] [--fix-status]      (iso2 = se, de, nl, no, ...)

For the UK and the US use seats_uk.py and seats_us.py (richer sources). This script holds one small adapter per
country (the ADAPTERS table at the end): each reads the parliament's open data and returns its chambers, the sitting
members (name, party, place, start, an ID) and, where the source has them, former members with their end date. The
rest is shared:
  bodies.csv     the chamber(s), seat_view=y, as of today, with the source link
  seats.csv      each chamber's seats by party (a Vacant row for empty seats)
  positions.csv  one row per supporter who sits (current=y, checked today) or sat (current=n, end date when known)
Supporters are matched to members by Wikidata ID when the source has one, then by name (accents, titles and the order of
names ignored; a unique last name plus first initial as a last resort). A supporter whose role says they sit in the
chamber but who is not on today's list gets current=n and is printed for you to check: a changed name or a spelling
difference looks the same as a departure, so read that list before committing.

Run it again after every election, by-election or resignation, and whenever politicians are added. Standard library only.
"""
import argparse, datetime as dt, json, re, sys, time, unicodedata, urllib.parse, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import wtdb  # noqa: E402

UA = {"User-Agent": "Mozilla/5.0 (wealth-tax-supporters seat refresh; github.com/Egalitaristen/wealth-tax-supporters)"}


def get(url, as_json=True, encoding=None, tries=5):
    # A copy is kept for six hours, so repeated runs (and dry runs) do not hammer a parliament's server.
    import hashlib, tempfile
    cache = Path(tempfile.gettempdir()) / ("wts-seats-" + hashlib.md5(url.encode()).hexdigest())
    for t in range(tries):
        try:
            if cache.exists() and time.time() - cache.stat().st_mtime < 6 * 3600:
                raw = cache.read_bytes()
            else:
                raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180).read()
                cache.write_bytes(raw)
            if not as_json:
                return raw
            if encoding:  # some servers answer in UTF-8, some in Latin-1: take UTF-8 when it decodes, else the stated one
                try:
                    return json.loads(raw.decode("utf-8"))
                except UnicodeDecodeError:
                    return json.loads(raw.decode(encoding))
            return json.loads(raw)
        except Exception as e:
            print(f"  retry {t + 1}: {str(e)[:70]}", file=sys.stderr)
            time.sleep(3)
    sys.exit(f"Could not read {url}")


TITLES = re.compile(r"\b(dr|prof|professor|mr|mrs|ms|sir|dame|hon|jr|sr|ii|iii|von|van|de|der|den|di|da|del|la|le)\b")


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return " ".join(re.sub(r"[^a-z ]", " ", TITLES.sub(" ", s)).split())


def name_keys(name):
    toks = norm(name).split()
    return toks


def match(actor, members, by_q, by_norm):
    """(member, how) for the one member this actor is, or (None, ''). how: qid, exact, or fuzzy (reported for you to check)."""
    if actor["wikidata_qid"] and actor["wikidata_qid"] in by_q:
        return by_q[actor["wikidata_qid"]], "qid"
    n = norm(actor["name"])
    if n in by_norm and len(by_norm[n]) == 1:
        return by_norm[n][0], "exact"
    toks = n.split()
    if len(toks) >= 2:
        # same words in another order, or extra given names: every word of the shorter name is in the longer
        c = [m for m in members if (lambda t: set(toks) <= set(t) or set(t) <= set(toks))(norm(m["name"]).split())
             and toks[-1] in norm(m["name"]).split()]
        if len(c) == 1:
            return c[0], "fuzzy"
        # same last name and the same first name, with other given names in between (Bob / Robert is not caught: add the Wikidata ID instead)
        def alike(m):
            t = norm(m["name"]).split()
            return t[-1:] == toks[-1:] and t[0] == toks[0]
        c = [m for m in members if alike(m)]
        if len(c) == 1:
            return c[0], "fuzzy"
    return None, ""


def run(d, adapter, dry=False, fix=False):
    today = dt.date.today().isoformat()
    db = wtdb.load_all(d)
    chambers = adapter()
    actors = [x for x in db["actors"] if x["kind"] == "person" and x["actor_type"] == "politician"]
    names = {c["name"] for c in chambers}
    bodies = [b for b in db["bodies"] if b["name"] not in names]
    seats = [s for s in db["seats"] if s["body_id"] not in {b["body_id"] for b in db["bodies"] if b["name"] in names}]
    positions = [o for o in db["positions"] if o["body_id"] not in {b["body_id"] for b in db["bodies"] if b["name"] in names}]
    report, sitting_total = [], 0
    for c in chambers:
        row = next((b for b in db["bodies"] if b["name"] == c["name"]), None) or {"body_id": wtdb.next_id(db["bodies"] + bodies, "bodies")}
        total = c["seats"] or len(c["members"])
        row.update(name=c["name"], level=c.get("level", "national"), kind="chamber", seats=str(total), as_of=today,
                   source_url=c["source_url"], seat_view="y", notes=c.get("note", ""))
        bodies.append(row)
        bid = row["body_id"]
        count, colour = {}, {}
        for m in c["members"]:
            count[m["party"]] = count.get(m["party"], 0) + 1
        if sum(count.values()) < total:
            count["Vacant"] = total - sum(count.values())
        order = c.get("party_order", [])
        for i, p in enumerate(sorted(count, key=lambda p: (order.index(p) if p in order else 50, -count[p])), start=1):
            seats.append({"seat_id": wtdb.next_id(seats, "seats"), "body_id": bid, "party": p, "seats": str(count[p]),
                          "colour": "" if p == "Vacant" else c.get("colours", {}).get(p, ""), "order": str(i)})
        members = c["members"]
        by_q, by_norm = {}, {}
        for m in members:
            if m.get("qid"):
                by_q[m["qid"]] = m
            by_norm.setdefault(norm(m["name"]), []).append(m)
        former = c.get("former", [])
        fq, fn = {m["qid"]: m for m in former if m.get("qid")}, {}
        for m in former:
            fn.setdefault(norm(m["name"]), []).append(m)
        role_re = re.compile(c["role_re"])
        for x in actors:
            m, how = match(x, members, by_q, by_norm)
            if m:
                if how == "fuzzy":
                    report.append(f"{x['actor_id']} {x['name']}: matched to {m['name']} ({m['party']}) by name only: confirm it is the same person")
                positions.append(dict(position_id="", actor_id=x["actor_id"], body_id=bid, role=c["role"], party=m["party"],
                                      geo_unit_id=x["geo_unit_id"], start=m.get("start", ""), end="", current="y",
                                      member_ref=str(m.get("ref", "")), checked=today, source_url=m.get("url") or c["source_url"]))
                sitting_total += 1
                if x["status"] != "active":
                    report.append(f"{x['actor_id']} {x['name']}: sits in the {c['name']} but is status={x['status']}")
                continue
            if not role_re.search(x["role"]):
                continue
            f, _ = match(x, former, fq, fn)
            positions.append(dict(position_id="", actor_id=x["actor_id"], body_id=bid, role=c["role"], party=(f or {}).get("party", ""),
                                  geo_unit_id=x["geo_unit_id"], start=(f or {}).get("start", ""), end=(f or {}).get("end", ""),
                                  current="n", member_ref=str((f or {}).get("ref", "")), checked=today,
                                  source_url=(f or {}).get("url") or c["source_url"]))
            if x["status"] == "active" or not f:  # a former member already marked as one needs no attention
                report.append(f"{x['actor_id']} {x['name']}: role {x['role'][:60]!r} but not on today's {c['name']} list"
                              f" ({'former member found, left ' + (f.get('end') or '?') if f else 'not found at all: check the spelling'})"
                              f"{' [status=active]' if x['status'] == 'active' else ''}")
    for o in positions:
        if not o["position_id"]:
            o["position_id"] = wtdb.next_id(positions, "positions")
    if fix:  # a role that starts with the chamber's role, held by someone who has left it: make it a former role
        by_id = {x["actor_id"]: x for x in actors}
        starts = {b["body_id"]: re.compile(c["role_start"]) for c in chambers for b in bodies if b["name"] == c["name"] and c.get("role_start")}
        n = 0
        for o in positions:
            x = by_id.get(o["actor_id"])
            if o["current"] == "n" and x and x["status"] == "active" and o["body_id"] in starts and starts[o["body_id"]].match(x["role"]):
                x["role"] = re.sub(r"(?i)^member", "Former member", x["role"]) + (f", until {dt.date.fromisoformat(o['end']).strftime('%B %Y')}" if o["end"] else "")
                x["status"], x["updated"] = "former_role", today
                n += 1
        print(f"--fix-status: {n} actor(s) made former_role")
        if not dry:
            wtdb.save(d, "actors", db["actors"])
    print(f"{sitting_total} supporters sit today; {len([o for o in positions if o['current'] == 'n'])} sat before and no longer do")
    for r in report:
        print("  check:", r)
    if dry:
        return
    wtdb.save(d, "bodies", bodies)
    wtdb.save(d, "seats", seats)
    wtdb.save(d, "positions", positions)
    print("Wrote bodies.csv, seats.csv and positions.csv")


# ---------------------------------------------------------------- adapters
def sweden():
    """The Riksdag (349 seats): data.riksdagen.se person list; a serving substitute holds the seat of a minister or someone on leave."""
    p = get("https://data.riksdagen.se/personlista/?utformat=json&rdlstatus=tjanstgorande", encoding="latin-1")["personlista"]["person"]
    PARTY = {"S": "Social Democrats", "M": "Moderate Party", "SD": "Sweden Democrats", "V": "Left Party", "C": "Centre Party",
             "MP": "Green Party", "KD": "Christian Democrats", "L": "Liberals", "-": "Independent"}
    cur, former = [], []
    for x in p:
        name = f"{x['tilltalsnamn']} {x['efternamn']}"
        party = PARTY.get(x["parti"], x["parti"])
        ups = [u for u in (x.get("personuppdrag") or {}).get("uppdrag", []) if u.get("organ_kod") == "kam" and u.get("roll_kod") in ("Riksdagsledamot", "Ersättare")]
        if x["status"].startswith("Tjänstgörande"):
            start = min((u["from"] for u in ups if u["roll_kod"] == "Riksdagsledamot"), default="") or min((u["from"] for u in ups), default="")
            cur.append(dict(name=name, party=party, ref=x["intressent_id"], start=start[:10], place=x.get("valkrets", ""),
                            url=f"https://www.riksdagen.se/sv/ledamoter-och-partier/ledamot/{x['intressent_id']}/" if False else ""))
        elif ups:  # former, deceased, or an available substitute who is not sitting
            ends = [u["tom"][:10] for u in ups if u.get("tom")]  # serving as a substitute held the seat too
            if ends:
                former.append(dict(name=name, party=party, ref=x["intressent_id"], end=max(ends),
                                   start=min(u["from"] for u in ups)[:10]))
    return [dict(name="Sveriges riksdag (Riksdag)", seats=349, source_url="https://www.riksdagen.se/sv/ledamoter-och-partier/",
                 note="349 seats. A serving substitute holds the seat of a minister or of a member on leave.",
                 role="Member of the Riksdag", role_re=r"(?i)(member of the riksdag|riksdag member|riksdagsledamot)", role_start=r"(?i)member of the riksdag", members=cur, former=former,
                 party_order=["Left Party", "Green Party", "Social Democrats", "Centre Party", "Liberals", "Independent",
                              "Moderate Party", "Christian Democrats", "Sweden Democrats"],
                 colours={"Social Democrats": "e8112d", "Moderate Party": "52bdec", "Sweden Democrats": "dddd00", "Left Party": "af0000",
                          "Centre Party": "009933", "Green Party": "83cf39", "Christian Democrats": "005ea1", "Liberals": "006ab3"})]


def germany():
    """The Bundestag: abgeordnetenwatch.de API (CC0), mandates of the current period; older periods give former members with end dates."""
    API = "https://www.abgeordnetenwatch.de/api/v2/"
    FRACTION = {"CDU/CSU": "CDU/CSU", "AfD": "AfD", "SPD": "SPD", "BÜNDNIS 90/DIE GRÜNEN": "Alliance 90/The Greens",
                "DIE LINKE": "The Left", "Die Linke": "The Left", "fraktionslos": "Independent", "BSW": "BSW", "FDP": "FDP"}

    def mandates(period):
        out, page = [], 0
        while True:
            d = get(f"{API}candidacies-mandates?parliament_period={period}&type=mandate&pager_limit=1000&page={page}")
            out += d["data"]
            if len(out) >= d["meta"]["result"]["total"] or not d["data"]:
                return out
            page += 1

    def party(m):
        fm = [f for f in m.get("fraction_membership", []) if not f.get("valid_until")] or m.get("fraction_membership", [])
        raw = re.sub(r"\s*\(Bundestag.*$", "", fm[-1]["fraction"]["label"]).replace("­", "") if fm else "fraktionslos"
        return FRACTION.get(raw, raw)

    cur, former = [], []
    for m in mandates(161):
        row = dict(name=m["politician"]["label"], party=party(m), ref=str(m["politician"]["id"]), start=m.get("start_date") or "",
                   place=((m.get("electoral_data") or {}).get("constituency") or {}).get("label", ""), url=m["politician"].get("abgeordnetenwatch_url", ""))
        if m.get("end_date"):
            row["end"] = m["end_date"]
            former.append(row)
        else:
            cur.append(row)
    for period, end in ((132, "2025-03-24"), (111, "2021-10-25"), (97, "2017-10-24"), (83, "2013-10-22")):
        for m in mandates(period):
            former.append(dict(name=m["politician"]["label"], party=party(m), ref=str(m["politician"]["id"]),
                               start=m.get("start_date") or "", end=m.get("end_date") or end, url=m["politician"].get("abgeordnetenwatch_url", "")))
    # keep the latest end date per person
    last = {}
    for m in former:
        if m["ref"] not in last or m["end"] > last[m["ref"]]["end"]:
            last[m["ref"]] = m
    return [dict(name="Deutscher Bundestag", seats=None, source_url="https://www.bundestag.de/abgeordnete",
                 note="The members of the 21st Bundestag (2025-2029) as listed by abgeordnetenwatch.de, with members who moved up included.",
                 role="Member of the Bundestag", role_re=r"(?i)bundestag", role_start=r"(?i)member of the bundestag", members=cur,
                 former=list(last.values()),
                 party_order=["The Left", "Alliance 90/The Greens", "SPD", "BSW", "FDP", "Independent", "CDU/CSU", "AfD"],
                 colours={"CDU/CSU": "6b6b6b", "AfD": "009ee0", "SPD": "e3000f", "Alliance 90/The Greens": "46962b", "The Left": "be3075",
                          "Independent": "8a8680", "FDP": "ffed00", "BSW": "7a1f5c"})]


def netherlands():
    """The Tweede Kamer (150 seats): the Kamer's open data (OData), members with an open seat today; the rest are former members."""
    BASE = "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/"
    seat = "FractieZetelPersoon($filter=Verwijderd eq false;$expand=FractieZetel($expand=Fractie))"
    people, url = [], BASE + "Persoon?" + urllib.parse.quote("$filter=Verwijderd eq false and FractieZetelPersoon/any(z: z/Verwijderd eq false)&$expand=" + seat, safe="$=&,()/:'")
    while url:
        d = get(url)
        people += d["value"]
        url = d.get("@odata.nextLink")
    cur, former = [], []
    for p in people:
        zs = [z for z in p["FractieZetelPersoon"] if z.get("Functie") in ("Lid", "Fractievoorzitter", "Voorzitter")] or p["FractieZetelPersoon"]
        if not zs:
            continue
        name = " ".join(x for x in (p.get("Roepnaam") or p.get("Voornamen", "").split(" ")[0], p.get("Tussenvoegsel"), p.get("Achternaam")) if x)
        open_ = [z for z in zs if not z["TotEnMet"]]
        z = open_[0] if open_ else max(zs, key=lambda z: z["TotEnMet"])
        fr = z["FractieZetel"]["Fractie"]
        party = (fr.get("Afkorting") or fr.get("NaamNL") or "").strip()
        row = dict(name=name, party=party, ref=p["Id"], start=(z["Van"] or "")[:10],
                   url=f"https://www.tweedekamer.nl/kamerleden_en_commissies/alle_kamerleden/{p['Id']}" if False else "")
        if open_:
            cur.append(row)
        else:
            row["end"] = (z["TotEnMet"] or "")[:10]
            former.append(row)
    return [dict(name="Tweede Kamer", seats=150, source_url="https://www.tweedekamer.nl/kamerleden_en_commissies/alle_kamerleden",
                 note="150 seats. Members of the House of Representatives of the Netherlands.",
                 role="Member of the House of Representatives", role_re=r"(?i)tweede kamer|house of representatives|kamerlid",
                 role_start=r"(?i)member of the (dutch )?(house of representatives|tweede kamer)", members=cur, former=former)]


def norway():
    """The Storting (169 seats): data.stortinget.no, the representatives of the current period (deputies serving count)."""
    BASE = "https://data.stortinget.no/eksport/representanter?format=json"
    def load(period=""):
        return get(BASE + (f"&stortingsperiodeid={period}" if period else ""))["representanter_liste"]
    cur, former, seen = [], [], set()
    for x in load():
        cur.append(dict(name=f"{x['fornavn']} {x['etternavn']}", party=x["parti"]["navn"], ref=x["id"], place=x["fylke"]["navn"], start=""))
        seen.add(x["id"])
    for period in ("2021-2025", "2017-2021", "2013-2017"):
        for x in load(period):
            if x["id"] not in seen:
                seen.add(x["id"])
                former.append(dict(name=f"{x['fornavn']} {x['etternavn']}", party=x["parti"]["navn"], ref=x["id"], end="", start=""))
    return [dict(name="Stortinget", seats=169, source_url="https://www.stortinget.no/no/Representanter-og-komiteer/Representantene/",
                 note="169 seats. A deputy (vararepresentant) who is serving holds the seat of a member on leave.",
                 role="Member of the Storting", role_re=r"(?i)storting|stortingsrepresentant", role_start=r"(?i)member of the storting", members=cur, former=former)]


ADAPTERS = {"se": sweden, "de": germany, "nl": netherlands, "no": norway}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--fix-status", action="store_true", help="make actors who have left the chamber former_role")
    a = ap.parse_args()
    cc = Path(a.dir).name.split("-")[0]
    if cc not in ADAPTERS:
        sys.exit(f"No adapter for '{cc}'. Have: {', '.join(sorted(ADAPTERS))}. Add one to ADAPTERS in this file.")
    run(a.dir, ADAPTERS[cc], a.dry_run, a.fix_status)


if __name__ == "__main__":
    sys.exit(main())
