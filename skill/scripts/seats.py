#!/usr/bin/env python3
"""Refresh a country's legislature seats from the parliament's own open member list.

Usage: python skill/scripts/seats.py data/<iso2> [--adapter NAME] [--dry-run] [--fix-status] [--local URL=FILE]      (iso2 = ar, fi, se, de, nl, no, fr, br, ca, es, pl, be, in, jp, my, sg, id, ng, cn, nz, za; un for the UN General Assembly; au for the Pan-African Parliament)

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
import argparse, datetime as dt, json, re, sys, time, unicodedata, urllib.error, urllib.parse, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import wtdb  # noqa: E402

UA = {"User-Agent": "Mozilla/5.0"}  # some parliaments (ourcommons.ca) refuse an unusual agent


def fetch_raw(url, headers=None):
    """The page's bytes. Some sites (ourcommons.ca) refuse Python's connection but answer curl: fall back to it on a 403."""
    try:
        return urllib.request.urlopen(urllib.request.Request(url, headers={**UA, **(headers or {})}), timeout=180).read()
    except urllib.error.HTTPError as e:
        import shutil, subprocess
        curl = shutil.which("curl") or shutil.which("curl.exe")
        if e.code != 403 or not curl:
            raise
        cmd = [curl, "-s", "-f", "-L", "--max-time", "180", "-A", UA["User-Agent"]] + [x for k, v in (headers or {}).items() for x in ("-H", f"{k}: {v}")] + [url]
        return subprocess.run(cmd, capture_output=True, check=True).stdout


def get(url, as_json=True, encoding=None, tries=5, headers=None):
    # A copy is kept for six hours, so repeated runs (and dry runs) do not hammer a parliament's server. Only a response
    # that parsed is kept.
    import hashlib, tempfile
    cache = Path(tempfile.gettempdir()) / ("wts-seats-" + hashlib.md5((url + json.dumps(headers or {}, sort_keys=True)).encode()).hexdigest())
    for t in range(tries):
        try:
            fresh = not (cache.exists() and time.time() - cache.stat().st_mtime < 6 * 3600)
            raw = fetch_raw(url, headers) if fresh else cache.read_bytes()
            if as_json:
                if encoding:  # some servers answer in UTF-8, some in Latin-1: take UTF-8 when it decodes, else the stated one
                    try:
                        out = json.loads(raw.decode("utf-8-sig"))
                    except UnicodeDecodeError:
                        out = json.loads(raw.decode(encoding))
                else:
                    out = json.loads(raw)
            else:
                out = raw
            if fresh:
                cache.write_bytes(raw)
            return out
        except Exception as e:
            print(f"  retry {t + 1}: {str(e)[:70]}", file=sys.stderr)
            time.sleep(3)
    sys.exit(f"Could not read {url}")


TITLES = re.compile(r"\b(dr|prof|professor|mr|mrs|ms|sir|dame|hon|jr|sr|ii|iii|von|van|de|der|den|di|da|del|la|le)\b")


def norm(s):
    s = unicodedata.normalize("NFKD", s.replace("’", "'").replace("‘", "'")).encode("ascii", "ignore").decode().lower()
    return " ".join(re.sub(r"[^a-z ]", " ", TITLES.sub(" ", s)).split())


def name_keys(name):
    toks = norm(name).split()
    return toks


def match(actor, members, by_q, by_norm):
    """(member, how) for the one member this actor is, or (None, ''). how: qid, exact, or fuzzy (reported for you to check)."""
    if actor["wikidata_qid"] and actor["wikidata_qid"] in by_q:
        return by_q[actor["wikidata_qid"]], "qid"
    cj = re.sub(r"\s", "", actor["name"])  # a name in kanji after the Latin one: 小池晃
    for m in members:
        if m.get("cjk") and m["cjk"] in cj:
            return m, "exact"
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


def run(d, adapter, dry=False, fix=False, actors_in=None):
    today = dt.date.today().isoformat()
    db = wtdb.load_all(d)
    chambers = adapter()
    actors = actors_in if actors_in is not None else [x for x in db["actors"] if x["kind"] == "person" and x["actor_type"] == "politician"]
    names = {c["name"] for c in chambers}
    bodies = [b for b in db["bodies"] if b["name"] not in names]
    seats = [s for s in db["seats"] if s["body_id"] not in {b["body_id"] for b in db["bodies"] if b["name"] in names}]
    positions = [o for o in db["positions"] if o["body_id"] not in {b["body_id"] for b in db["bodies"] if b["name"] in names}]
    report, sitting_total = [], 0
    for c in chambers:
        row = next((b for b in db["bodies"] if b["name"] == c["name"]), None) or {"body_id": wtdb.next_id(db["bodies"] + bodies, "bodies")}
        total = c["seats"] or len(c["members"])
        row.update(name=c["name"], level=c.get("level", "national"), kind="chamber", seats=str(total), as_of=c.get("as_of", today),
                   source_url=c["source_url"], seat_view="y", notes=c.get("note", ""))
        bodies.append(row)
        bid = row["body_id"]
        count, colour = {}, {}
        for m in c["members"]:
            count[m["party"]] = count.get(m["party"], 0) + 1
        vacant = c.get("vacant_label", "Vacant")
        if sum(count.values()) < total:
            count[vacant] = total - sum(count.values())
        order = c.get("party_order", [])
        for i, p in enumerate(sorted(count, key=lambda p: (order.index(p) if p in order else 50, -count[p])), start=1):
            seats.append({"seat_id": wtdb.next_id(seats, "seats"), "body_id": bid, "party": p, "seats": str(count[p]),
                          "colour": "" if p == vacant else c.get("colours", {}).get(p, ""), "order": str(i)})
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
        per_country = {}
        for x in actors:
            pool = (members, by_q, by_norm)
            if c.get("by_country") and x.get("_iso"):  # a supranational body: a supporter can only be a member for their own country
                if x["_iso"] not in per_country:
                    sub = [m for m in members if m.get("country") == x["_iso"]]
                    q, n = {}, {}
                    for m in sub:
                        if m.get("qid"):
                            q[m["qid"]] = m
                        n.setdefault(norm(m["name"]), []).append(m)
                    per_country[x["_iso"]] = (sub, q, n)
                pool = per_country[x["_iso"]]
            m, how = match(x, *pool)
            if m:
                if c.get("enrich"):
                    m = c["enrich"](m)
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
            if f and f.get("on_leave"):  # still the holder of the seat, but a substitute serves it: not "former", and no lit seat
                positions.append(dict(position_id="", actor_id=x["actor_id"], body_id=bid, role=c["role"], party=f.get("party", ""),
                                      geo_unit_id=x["geo_unit_id"], start="", end="", current="", member_ref=str(f["ref"]), checked=today,
                                      source_url=f.get("url") or c["source_url"]))
                report.append(f"{x['actor_id']} {x['name']}: holds a seat in the {c['name']} but is on leave (a substitute serves): left as is")
                continue
            positions.append(dict(position_id="", actor_id=x["actor_id"], body_id=bid, role=c["role"], party=(f or {}).get("party", ""),
                                  geo_unit_id=x["geo_unit_id"], start=(f or {}).get("start", ""), end=(f or {}).get("end", ""),
                                  current="n", member_ref=str((f or {}).get("ref", "")), checked=today,
                                  source_url=(f or {}).get("url") or c["source_url"]))
            if x["status"] == "active":  # someone already marked as a former member needs no attention
                report.append(f"{x['actor_id']} {x['name']}: role {x['role'][:60]!r} but not on today's {c['name']} list"
                              f" ({'former member found, left ' + (f.get('end') or '?') if f else 'not found at all: check the spelling'})"
                              f"{' [status=active]' if x['status'] == 'active' else ''}")
    for o in positions:
        if not o["position_id"]:
            o["position_id"] = wtdb.next_id(positions, "positions")
    if fix and actors_in is not None:
        print("--fix-status does not apply to a supranational body (the actors belong to the country registers): change those roles by hand")
        fix = False
    if fix:  # a role that starts with the chamber's role, held by someone who has left it: make it a former role
        by_id = {x["actor_id"]: x for x in actors}
        starts = {b["body_id"]: re.compile(c["role_start"]) for c in chambers for b in bodies if b["name"] == c["name"] and c.get("role_start")}
        n = 0
        sitting = {o["actor_id"] for o in positions if o["current"] == "y"}  # someone who sits in another chamber is not 'former'
        for o in positions:
            x = by_id.get(o["actor_id"])
            if x and x["actor_id"] in sitting:
                continue
            if o["current"] == "n" and x and x["status"] == "active" and o["body_id"] in starts and starts[o["body_id"]].match(x["role"]):
                x["role"] = (re.sub(r"(?i)^member", "Former member", x["role"]) if re.match(r"(?i)member", x["role"]) else "Former " + (x["role"] if x["role"][:2].isupper() else x["role"][:1].lower() + x["role"][1:])) + (f", until {dt.date.fromisoformat(o['end']).strftime('%B %Y')}" if o["end"] else "")
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


def france():
    """The Assemblée nationale (577 seats; data.assemblee-nationale.fr, deputies with an open mandate) and the Sénat (348; data.senat.fr)."""
    import io, zipfile, csv as _csv
    raw = get("https://data.assemblee-nationale.fr/static/openData/repository/17/amo/deputes_actifs_mandats_actifs_organes/AMO10_deputes_actifs_mandats_actifs_organes.json.zip", as_json=False)
    z = zipfile.ZipFile(io.BytesIO(raw))
    names = set(z.namelist())
    groups = {}

    def group(ref):
        if ref not in groups:
            f = f"json/organe/{ref}.json"
            o = json.loads(z.read(f))["organe"] if f in names else {}
            groups[ref] = (o.get("libelleAbrege") or o.get("libelle") or "Non inscrit").strip()
        return groups[ref]

    an = []
    for n in names:
        if "/acteur/" not in n:
            continue
        a = json.loads(z.read(n))["acteur"]
        ms = a["mandats"]["mandat"]
        ms = ms if isinstance(ms, list) else [ms]
        seat = [m for m in ms if m.get("typeOrgane") == "ASSEMBLEE" and not m.get("dateFin")]
        if not seat:
            continue
        gp = [m for m in ms if m.get("typeOrgane") == "GP" and not m.get("dateFin")]
        ref = gp[0]["organes"]["organeRef"] if gp else None
        ident = a["etatCivil"]["ident"]
        an.append(dict(name=f"{ident['prenom']} {ident['nom']}", party=group(ref) if ref else "Non inscrit", ref=a["uid"]["#text"],
                       start=seat[0].get("dateDebut", ""), place=""))
    # the Sénat: current senators, with their group
    text = get("https://data.senat.fr/data/senateurs/ODSEN_GENERAL.csv", as_json=False).decode("latin-1")
    lines = [l for l in text.splitlines() if not l.startswith("%")]
    se = []
    for r in _csv.DictReader(lines):
        if (r.get("État") or "").strip().upper() != "ACTIF":
            continue
        se.append(dict(name=f"{r['Prénom usuel'].strip()} {r['Nom usuel'].strip()}", party=(r.get("Groupe politique") or "Non inscrit").strip() or "Non inscrit",
                       ref=r["Matricule"].strip(), start="", place=(r.get("Circonscription") or "").strip()))
    return [dict(name="Assemblée nationale", seats=577, source_url="https://www2.assemblee-nationale.fr/deputes/liste/alphabetique",
                 note="577 seats; groups as the Assemblée names them (abbreviations).", role="Member of the National Assembly",
                 role_re=r"(?i)national assembly|assemblée nationale|député", role_start=r"(?i)member of the national assembly", members=an,
                 party_order=["LFI-NFP", "GDR", "EcoS", "SOC", "LIOT", "NI", "EPR", "Non inscrit", "Dem", "HOR", "DR", "UDR", "RN"],
                 colours={"RN": "0d378a", "LFI-NFP": "cc2443", "SOC": "f06c8c", "EcoS": "00c000", "GDR": "dd0000", "EPR": "ffd600", "DR": "0066cc",
                          "LIOT": "ff8040", "Dem": "ff9900", "HOR": "00bcd4", "UDR": "7a7a7a"}),
            dict(name="Sénat", seats=348, source_url="https://www.senat.fr/senateurs/senatl.html", note="348 seats; groups as the Sénat names them.",
                 role="Senator", role_re=r"(?i)\bsenator\b|sénateur", role_start=r"(?i)senator", members=se)]


def brazil():
    """The Câmara dos Deputados (513) and the Senado Federal (81): the houses' open-data APIs, members in office today (substitutes included)."""
    cam = "https://dadosabertos.camara.leg.br/api/v2/deputados"

    def deputies(extra=""):
        out, page = [], 1
        while True:
            d = get(f"{cam}?itens=100&pagina={page}&ordem=ASC&ordenarPor=nome{extra}")
            out += d["dados"]
            if not any(l.get("rel") == "next" for l in d.get("links", [])):
                return out
            page += 1

    cur = [dict(name=x["nome"], party=x["siglaPartido"], ref=str(x["id"]), place=x["siglaUf"], start="",
                url=f"https://www.camara.leg.br/deputados/{x['id']}") for x in deputies()]
    seen = {m["ref"] for m in cur}
    former = []
    for leg in (57, 56, 55):
        for x in deputies(f"&idLegislatura={leg}"):
            if str(x["id"]) not in seen:
                seen.add(str(x["id"]))
                row = dict(name=x["nome"], party=x["siglaPartido"], ref=str(x["id"]), end="", start="")
                if leg == 57:  # in this legislature but not serving: on leave (the seat is theirs, a substitute serves) or gone for good
                    st = get(f"{cam}/{x['id']}")["dados"]["ultimoStatus"]
                    row["on_leave"] = st.get("situacao") in ("Licença", "Afastado") or (st.get("situacao") == "Suplência" and st.get("condicaoEleitoral") == "Titular")
                    row["end"] = (st.get("data") or "")[:10] if st.get("situacao") == "Fim de Mandato" else ""
                former.append(row)
    sen = get("https://legis.senado.leg.br/dadosabertos/senador/lista/atual", headers={"Accept": "application/json"})["ListaParlamentarEmExercicio"]["Parlamentares"]["Parlamentar"]
    senators = [dict(name=s["IdentificacaoParlamentar"]["NomeParlamentar"], party=s["IdentificacaoParlamentar"].get("SiglaPartidoParlamentar", ""),
                     ref=s["IdentificacaoParlamentar"]["CodigoParlamentar"], place=s["IdentificacaoParlamentar"].get("UfParlamentar", ""), start="",
                     url=s["IdentificacaoParlamentar"].get("UrlPaginaParlamentar", "")) for s in sen]
    order = ["PSOL", "PCdoB", "PT", "PV", "REDE", "PSB", "PDT", "Solidariedade", "CIDADANIA", "MDB", "PSD", "PSDB", "PODE", "AVANTE", "UNIÃO", "PP", "REPUBLICANOS", "PL", "NOVO"]
    colours = {"PT": "e30613", "PSOL": "ffd100", "PCdoB": "c8102e", "PSB": "ffcc00", "PDT": "1d4ea1", "PV": "009a44", "REDE": "2da44e", "MDB": "00964b",
               "PSD": "f58220", "PSDB": "0080ff", "PL": "1b3c8c", "PP": "3c6eb4", "UNIÃO": "003c8f", "REPUBLICANOS": "00a2e0", "NOVO": "ff6a13"}
    return [dict(name="Câmara dos Deputados", seats=513, source_url="https://www.camara.leg.br/deputados/quem-sao", note="513 seats; a substitute serving holds the seat of a deputy on leave.",
                 role="Federal deputy", role_re=r"(?i)federal deputy|câmara dos deputados|deputado federal", role_start=r"(?i)federal deputy", members=cur, former=former,
                 party_order=order, colours=colours),
            dict(name="Senado Federal", seats=81, source_url="https://www25.senado.leg.br/web/senadores/em-exercicio", note="81 seats.",
                 role="Federal senator", role_re=r"(?i)federal senator|senado federal|senador", role_start=r"(?i)federal senator", members=senators,
                 party_order=order, colours=colours)]


def canada():
    """The House of Commons (343 seats): ourcommons.ca's member list (members in office; vacant seats shown)."""
    import xml.etree.ElementTree as ET
    root = ET.fromstring(get("https://www.ourcommons.ca/Members/en/search/xml", as_json=False))
    mem = []
    for m in root:
        if m.findtext("ToDateTime"):
            continue
        mem.append(dict(name=f"{m.findtext('PersonOfficialFirstName')} {m.findtext('PersonOfficialLastName')}", party=m.findtext("CaucusShortName") or "Independent",
                        ref=m.findtext("PersonId"), place=m.findtext("ConstituencyName"), start=(m.findtext("FromDateTime") or "")[:10],
                        url=f"https://www.ourcommons.ca/Members/en/{m.findtext('PersonId')}"))
    return [dict(name="House of Commons of Canada", seats=343, source_url="https://www.ourcommons.ca/Members/en/search", note="343 seats; vacant seats are shown as Vacant.",
                 role="Member of Parliament", role_re=r"(?i)member of parliament|\bMP\b", role_start=r"(?i)member of parliament", members=mem,
                 party_order=["Green Party", "NDP", "Bloc Québécois", "Liberal", "Independent", "Conservative"],
                 colours={"Liberal": "d71920", "Conservative": "1a4782", "NDP": "f37021", "Bloc Québécois": "33b2cc", "Green Party": "3d9b35", "Independent": "8a8680"})]



def spain():
    """The Congreso de los Diputados (350 seats): congreso.es open data, deputies with an active mandate.

    A deputy's mandate ends on the day the Cortes are dissolved, except for those who stay on (the standing committee), so
    after a dissolution most seats are empty until the new Cortes meet. The block of seats whose mandate ended is labelled
    with the dissolution date instead of 'Vacant'."""
    BASE = "https://www.congreso.es/webpublica/opendata/diputados/"
    page = get("https://www.congreso.es/es/opendata/diputados", as_json=False).decode("latin-1")

    def latest(prefix):
        names = sorted(set(re.findall(rf"{prefix}__\d+\.json", page)))
        if not names:
            sys.exit(f"The Congreso's open-data page lists no {prefix} file; check congreso.es/es/opendata/diputados")
        return get(BASE + names[-1], encoding="latin-1")

    def person(x):
        s = x["NOMBRE"].strip()
        return " ".join(reversed([t.strip() for t in s.split(",", 1)])) if "," in s else s

    def iso(d):
        return "-".join(reversed(d.split("/"))) if d else ""

    GROUP = [("popular", "PP"), ("socialista", "PSOE"), ("vox", "Vox"), ("sumar", "Sumar"), ("republicano", "ERC"), ("junts", "Junts"),
             ("bildu", "EH Bildu"), ("vasco", "EAJ-PNV"), ("mixto", "Mixto")]

    def party(x):
        g = (x.get("GRUPOPARLAMENTARIO") or "").lower()
        return next((v for k, v in GROUP if k in g), re.sub(r"(?i)^grupo parlamentario\s+", "", x.get("GRUPOPARLAMENTARIO") or "Mixto"))

    active = [dict(name=person(x), party=party(x), ref=x["NOMBRE"], place=x.get("CIRCUNSCRIPCION", ""), start=iso(x.get("FECHAALTA", "")))
              for x in latest("DiputadosActivos")]
    left = latest("DiputadosDeBaja")
    day = max((d for d in {x.get("FECHABAJA") for x in left} if d), key=lambda d: sum(1 for x in left if x.get("FECHABAJA") == d), default="")
    mass = sum(1 for x in left if x.get("FECHABAJA") == day)
    former = [dict(name=person(x), party=party(x), ref=x["NOMBRE"], start=iso(x.get("FECHAALTA", "")), end=iso(x.get("FECHABAJA", ""))) for x in left]
    for x in latest("Diput"):  # deputies of earlier legislatures: no dates in this file
        if x.get("LEGISLATURAACTUAL") != "S":
            former.append(dict(name=f"{x['NOMBRE'].strip()} {x['APELLIDOS'].strip()}", party="", ref="", start="", end=""))
    once = {}  # a person served in several legislatures: one row each, the one with an end date first
    for m in sorted(former, key=lambda m: not m["end"]):
        once.setdefault(norm(m["name"]), m)
    former = list(once.values())
    note = "350 seats."
    vac = "Vacant"
    if mass >= 100:
        vac = f"Mandate ended at dissolution ({iso(day)})"
        note = f"350 seats. The Cortes were dissolved on {iso(day)} and a deputy's mandate ends on the day of dissolution, so only the deputies who stay on hold a seat until the new Cortes meet."
    return [dict(name="Congreso de los Diputados", seats=350, source_url="https://www.congreso.es/es/opendata/diputados", note=note, vacant_label=vac,
                 role="Member of Congress", role_re=r"(?i)member of congress|congreso de los diputados|diputad",
                 role_start=r"(?i)member of congress", members=active, former=former,
                 party_order=["Sumar", "EH Bildu", "ERC", "PSOE", "Junts", "EAJ-PNV", "Mixto", "PP", "Vox"],
                 colours={"PP": "1d84ce", "PSOE": "e30613", "Vox": "63be21", "Sumar": "e5007d", "ERC": "ffb232", "Junts": "00c3b2", "EH Bildu": "b5cf18",
                          "EAJ-PNV": "008b45", "Mixto": "8a8680"})]


def poland():
    """The Sejm (460 seats): api.sejm.gov.pl, the members of the current term who are active."""
    term = 10
    mps = get(f"https://api.sejm.gov.pl/sejm/term{term}/MP")
    cur = [dict(name=x["firstLastName"], party=x.get("club") or "niez.", ref=str(x["id"]), place=x.get("districtName", ""), start="",
                url=f"https://www.sejm.gov.pl/sejm{term}.nsf/posel.xsp?id={x['id']:03d}") for x in mps if x.get("active")]
    former = [dict(name=x["firstLastName"], party=x.get("club") or "niez.", ref=str(x["id"]), end="", start="") for x in mps if not x.get("active")]
    return [dict(name="Sejm", seats=460, source_url=f"https://www.sejm.gov.pl/sejm{term}.nsf/poslowie.xsp?type=A",
                 note=f"460 seats; members of the {term}th term who are active. Clubs as the Sejm names them.",
                 role="Member of the Sejm", role_re=r"(?i)sejm|member of the polish parliament|poseł", role_start=r"(?i)member of the (polish )?(sejm|parliament)",
                 members=cur, former=former,
                 party_order=["Lewica", "KO", "Demokracja", "Polska2050", "PSL-TD", "Centrum", "RozwojPlus", "niez.", "Konfederacja", "PiS"],
                 colours={"KO": "f68f2f", "PiS": "263778", "Lewica": "d4005a", "PSL-TD": "3ba935", "Polska2050": "ffd500", "Konfederacja": "5b6aa3",
                          "Centrum": "7a7a7a", "RozwojPlus": "8a6fc7", "Demokracja": "d26d9f", "niez.": "8a8680"})]



def belgium():
    """The Chamber of Representatives (150 seats): lachambre.be. Its firewall refuses scripts, so the member list is read in a
    browser and passed with --local (see the Belgium guide): rows of [surname given name, party, member key]."""
    url = "https://www.lachambre.be/kvvcr/showpage.cfm?section=/depute&language=fr&cfm=/site/wwwcfm/depute/cvlist54.cfm"
    rows = get(url)
    mem = []
    for name, party, key in rows:
        parts = name.split()
        given = parts[-1]
        mem.append(dict(name=f"{given} {' '.join(parts[:-1])}", party=party, ref=key, start="",
                        url=f"https://www.lachambre.be/kvvcr/showpage.cfm?section=/depute&language=fr&cfm=cvview54.cfm?key={key}" if key else ""))
    return [dict(name="Chamber of Representatives", seats=150, source_url=url, note="150 seats; party names as the Chamber lists them. Read in a browser: the Chamber's site refuses scripts.",
                 role="Member of the Chamber of Representatives", role_re=r"(?i)chamber of representatives|kamerlid|député fédéral",
                 role_start=r"(?i)member of the chamber of representatives", members=mem,
                 party_order=["PVDA-PTB", "Ecolo-Groen", "PS", "Vooruit", "DéFI", "Anders.", "INDEP", "cd&v", "Les Engagés", "MR", "N-VA", "VB"],
                 colours={"PVDA-PTB": "b01c2e", "PS": "e30613", "Ecolo-Groen": "46962b", "Vooruit": "ee2b4a", "N-VA": "f2a900", "VB": "5b4a1f", "MR": "0b5ea8",
                          "Les Engagés": "2aa9b3", "cd&v": "e87722", "DéFI": "d6006e", "Anders.": "7a7a7a", "INDEP": "8a8680"})]


def india():
    """The Lok Sabha (543 seats): sansad.in's member API. The Rajya Sabha (245) endpoint refuses scripts, so it is read in a
    browser and passed with --local as {total, counts: {party: n}, named: [the register's members found]}."""
    ls = get("https://sansad.in/api_ls/member?loksabha=18&")["membersDtoList"]
    cur = [dict(name=x["mpFirstLastName"].strip(), party=x.get("partySname") or "IND", ref=str(x["mpsno"]), place=x.get("constName", ""), start="",
                url=f"https://sansad.in/ls/members/biography/{x['mpsno']}") for x in ls
           if x.get("status", "Sitting") == "Sitting"]  # the list also holds members who died or resigned
    out = [dict(name="Lok Sabha", seats=543, source_url="https://sansad.in/ls/members", note="543 seats; the 18th Lok Sabha.",
                role="Member of the Lok Sabha", role_re=r"(?i)lok sabha", role_start=r"(?i)member of the lok sabha", members=cur,
                party_order=["CPI(ML)L", "CPI(M)", "CPI", "AITC", "SP", "DMK", "INC", "SS(UBT)", "NCP(SP)", "AAP", "TDP", "JD(U)", "BJP"],
                colours={"BJP": "ff9933", "INC": "19aaed", "SP": "e03a3e", "AITC": "20c646", "DMK": "e5262a", "TDP": "ffd400", "JD(U)": "1c7c3c",
                         "CPI(M)": "c8102e", "CPI": "e03a3e", "AAP": "0066a1", "SS(UBT)": "f26a1b", "NCP(SP)": "1f6fbf"})]
    try:
        rs = get("https://sansad.in/api_rs/member/sitting-members")
    except SystemExit:
        print("  (Rajya Sabha skipped: sansad.in refuses scripts for it; pass its summary with --local, see the India guide)", file=sys.stderr)
        return out
    named = [dict(name=x["n"], party=x["p"], ref=x["id"], place=x["s"], start="") for x in rs["named"] if "n" in x]
    filler = [dict(name=f"(another member, {p} #{i})", party=p, ref="", start="") for p, n in rs["counts"].items()
              for i in range(n - sum(1 for x in named if x["party"] == p))]
    out.append(dict(name="Rajya Sabha", seats=245, source_url="https://sansad.in/rs/members", note="245 seats; sitting members as read from sansad.in.",
                    role="Member of the Rajya Sabha", role_re=r"(?i)rajya sabha", role_start=r"(?i)member of the rajya sabha", members=named + filler,
                    party_order=["CPI(M)", "CPI", "AITC", "SP", "DMK", "INC", "AAP", "BJD", "YSRCP", "IND.", "NOM.", "JD(U)", "BJP"],
                    colours={"BJP": "ff9933", "INC": "19aaed", "AITC": "20c646", "DMK": "e5262a", "CPI(M)": "c8102e", "CPI": "e03a3e", "SP": "e03a3e"}))
    return out



def japan():
    """The House of Representatives (465: shugiin.go.jp, ten pages by kana row) and the House of Councillors (248: sangiin.go.jp,
    the page of the latest Diet session). The pages give names in kanji, so supporters are matched on the kanji in brackets after
    their name in the register (小池晃)."""
    PARTY = {"自民": "LDP", "立憲": "CDP", "維新": "Ishin", "国民": "DPP", "公明": "Komeito", "共産": "JCP", "れいわ": "Reiwa", "参政": "Sanseito",
             "無": "Independent", "無所属": "Independent", "みんな": "Your Party", "社民": "SDP", "有志": "Yushi"}

    def party(raw):
        return PARTY.get(raw.strip(), raw.strip())

    def lines(url, enc):
        raw = get(url, as_json=False)
        html = raw.decode(enc, errors="replace")
        text = re.sub(r"<[^>]+>", "\n", html)
        return [re.sub(r"\s+", " ", x.replace("&nbsp;", " ")).strip() for x in text.split("\n") if x.strip() and x.replace("&nbsp;", " ").strip()]

    reps = []
    for n in range(1, 11):
        L = lines(f"https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/{n}giin.htm", "cp932")
        for k, x in enumerate(L):
            if x.endswith("君") and k + 5 < len(L) and re.match(r"\d", L[k + 5]):  # terms won, sometimes with a note such as 1（参2）
                kanji = x[:-1].replace(" ", "").replace("　", "")
                reps.append(dict(name=kanji, cjk=kanji, party=party(L[k + 3]), ref=kanji, place=L[k + 4], start="",
                                 url=f"https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/{n}giin.htm"))
    session, url = None, None
    for s in range(222, 240):  # the latest Diet session that has a page
        try:
            u = f"https://www.sangiin.go.jp/japanese/joho1/kousei/giin/{s}/giin.htm"
            urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read(1)
            session, url = s, u
        except Exception:
            break
    L = lines(url, "utf-8")
    sen = []
    for k, x in enumerate(L):
        if re.fullmatch(r"令和\d+年\d+月\d+日", x) and k >= 4 and "現在" not in x:
            name = re.sub(r"\[.*?\]", "", L[k - 4]).replace(" ", "").replace("　", "")
            sen.append(dict(name=name, cjk=name, party=party(L[k - 2]), ref=name, place=L[k - 1], start="", url=url))
    return [dict(name="House of Representatives (Shūgiin)", seats=465, source_url="https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/1giin.htm",
                 note="465 seats; party blocks are the Diet groups (会派) named on the House's list, abbreviated in English where the abbreviation is well known.",
                 role="Member of the House of Representatives", role_re=r"(?i)house of representatives", role_start=r"(?i)member of the house of representatives", members=reps,
                 party_order=["JCP", "Reiwa", "CDP", "SDP", "DPP", "Komeito", "Independent", "Ishin", "LDP", "Sanseito"],
                 colours={"LDP": "d7263d", "CDP": "1d4ea1", "Ishin": "33a02c", "DPP": "f9a602", "Komeito": "f55881", "JCP": "d90000", "Reiwa": "ed6d9c", "Sanseito": "e6a000"}),
            dict(name="House of Councillors (Sangiin)", seats=248, source_url=url, note=f"248 seats; the member list of the {session}th Diet session. Groups as named on the House's list.",
                 role="Member of the House of Councillors", role_re=r"(?i)house of councillors", role_start=r"(?i)member of the house of councillors", members=sen,
                 party_order=["JCP", "Reiwa", "CDP", "SDP", "DPP", "Komeito", "Independent", "Ishin", "LDP", "Sanseito"],
                 colours={"LDP": "d7263d", "CDP": "1d4ea1", "Ishin": "33a02c", "DPP": "f9a602", "Komeito": "f55881", "JCP": "d90000", "Reiwa": "ed6d9c", "Sanseito": "e6a000"})]


def malaysia():
    """The Dewan Rakyat (222 seats): parlimen.gov.my. The page refuses scripts, so it is read in a browser and summarised with --local
    as {total, counts: {coalition: n}, named: [the register's members found]} (see the Malaysia guide)."""
    d = get("https://www.parlimen.gov.my/ahli-dewan.html?uweb=dr&")
    named = [dict(name=x["n"], party=x["p"], ref=x["id"], place=x["s"], start="") for x in d["named"] if "n" in x]
    filler = [dict(name=f"(another member, {p} #{i})", party=p, ref="", start="") for p, n in d["counts"].items()
              for i in range(n - sum(1 for x in named if x["party"] == p))]
    return [dict(name="Dewan Rakyat", seats=222, source_url="https://www.parlimen.gov.my/ahli-dewan.html?uweb=dr&",
                 note="222 seats; parties shown by coalition as the Dewan lists them (PH, BN, PN, GPS…); unfilled seats show as Vacant.",
                 role="Member of Parliament", role_re=r"(?i)member of parliament|dewan rakyat", role_start=r"(?i)member of parliament", members=named + filler,
                 party_order=["MUDA", "PH", "WARISAN", "BEBAS", "BN", "GPS", "GRS", "KDM", "PBM", "PN"],
                 colours={"PH": "e0281f", "BN": "1b3a8c", "PN": "1d6f3e", "GPS": "c9a227", "GRS": "7a5a9c", "WARISAN": "2ea3d8", "MUDA": "111111", "BEBAS": "8a8680"})]



def singapore():
    """Parliament of Singapore: who sits comes from parliament.gov.sg (every MP, with the constituency or 'Nominated'/'Non-Constituency'
    label); the party of each comes from Wikipedia's table of the current Parliament, because the Parliament's own list has no party.
    Seats: 97 elected, up to 12 minus the elected opposition as non-constituency MPs, 9 nominated; Wikipedia states the seat count."""
    page = get("https://www.parliament.gov.sg/mps/list-of-current-mps", as_json=False).decode("utf-8", errors="replace")
    sitting = []
    for blk in re.findall(r'<li><div class="row list-of-mps-wrap">.*?</li>', page, flags=re.S):
        nm = re.search(r'mp-sort-name"><a href="([^"]+)">(.*?)</a>', blk, flags=re.S)
        co = re.search(r'mp-sort constituency">(.*?)</div>', blk, flags=re.S)
        if nm:
            name = re.sub(r"<[^>]+>|<!-- -->", " ", nm.group(2))
            name = re.sub(r"^\s*(Mr|Ms|Mrs|Mdm|Dr|Prof|Assoc Prof|A/P|Er|Ar|Dr\.)\s+", "", " ".join(name.split()))
            sitting.append((name, re.sub(r"<[^>]+>", "", co.group(1)).strip() if co else "", "https://www.parliament.gov.sg" + nm.group(1)))
    wiki = get("https://en.wikipedia.org/w/index.php?title=15th_Parliament_of_Singapore&action=raw", as_json=False).decode("utf-8")
    party_of = {}
    for row in wiki.split("\n|-"):
        pc = re.search(r"\{\{party color cell\|([^}]+)\}\}", row)
        mem = re.search(r"\[\[([^\]|]+)\|([^\]]*'''[^\]]*)\]\]", row)
        if pc and mem:
            party_of[norm(mem.group(2).replace("'''", ""))] = re.sub(r"\s*\(Singapore\)", "", pc.group(1)).strip()
    short = {"People's Action Party": "PAP", "Workers' Party": "WP", "Progress Singapore Party": "PSP", "Singapore Democratic Party": "SDP"}
    mem = []
    for name, cons, url in sitting:
        if re.search(r"(?i)nominated", cons):
            p = "Independent (nominated)"
        else:
            ns = set(norm(name).split())
            hit = [v for k, v in party_of.items() if set(k.split()) <= ns or ns <= set(k.split())] if len(ns) > 1 else []
            raw = party_of.get(norm(name)) or (hit[0] if len(set(hit)) == 1 else "")
            p = short.get(raw, raw or "Party not found")
        mem.append(dict(name=name, party=p, ref=url.rsplit("/", 1)[-1], place=cons, start="", url=url))
    total = re.search(r"There are (\d+) seats in this parliament", wiki)
    note = ("Elected members, non-constituency members and nominated members. Who sits is from parliament.gov.sg; each member's party is from Wikipedia's "
            "table of the 15th Parliament (the Parliament's own list has no party column).")
    return [dict(name="Parliament of Singapore", seats=int(total.group(1)) if total else 108, source_url="https://www.parliament.gov.sg/mps/list-of-current-mps",
                 note=note, role="Member of Parliament", role_re=r"(?i)member of parliament", role_start=r"(?i)member of parliament", members=mem,
                 party_order=["WP", "PSP", "SDP", "Independent (nominated)", "Party not found", "PAP"],
                 colours={"PAP": "1d4ea1", "WP": "d91e2a", "PSP": "ffb300", "SDP": "1f9d55", "Independent (nominated)": "8a8680"})]


def fixed_chamber(name, seats, source_url, as_of, note, counts, order, colours, role, role_re):
    """A chamber whose seat split is a published figure read by hand, not a member list: no member is named, so no seat is lit unless
    a supporter is added to positions.csv by hand."""
    filler = [dict(name=f"(another member, {p} #{i})", party=p, ref="", start="") for p, n in counts.items() for i in range(n)]
    return dict(name=name, seats=seats, source_url=source_url, as_of=as_of, note=note, role=role, role_re=role_re, role_start=role_re,
                members=filler, party_order=order, colours=colours)


def indonesia():
    """The DPR (580 seats): the faction totals the DPR publishes on dpr.go.id/tentang-dpr/informasi-anggota-dewan (tab Fraksi), read
    in a browser because the site refuses scripts. No member is named."""
    counts = {"PDI-P": 110, "Golkar": 102, "Gerindra": 86, "PKB": 68, "NasDem": 67, "PKS": 53, "PAN": 47, "Demokrat": 44}
    return [fixed_chamber("People's Representative Council (DPR)", 580, "https://www.dpr.go.id/tentang-dpr/informasi-anggota-dewan", "2026-10-25",
                          "580 seats; the faction totals the DPR publishes for 2024-2029 (577 seats filled). Read in a browser on 2026-10-25; no member is named here.",
                          counts, ["PDI-P", "PKB", "Demokrat", "NasDem", "Golkar", "PAN", "PKS", "Gerindra"],
                          {"PDI-P": "d1232a", "Golkar": "f2c500", "Gerindra": "8b1a1a", "PKB": "1b9c4a", "NasDem": "1f5fa8", "PKS": "f58220", "PAN": "2b7bd0", "Demokrat": "1d3f8a"},
                          "Member of the People's Representative Council (DPR)", r"(?i)\bDPR\b|people's representative council|house of representatives of indonesia")]


def nigeria():
    """The House of Representatives (360 seats): the last full tally found (30 Oct 2025, reported by AllAfrica); more than 60 members have since
    changed party and no newer tally was found, so this is flagged as approximate in the note."""
    counts = {"APC": 243, "PDP": 74, "LP": 21, "NNPP": 15, "APGA": 5, "SDP": 2, "ADC": 1, "YPP": 1}
    return [fixed_chamber("House of Representatives", 360, "https://allafrica.com/stories/202510300371.html", "2025-10-30",
                          "360 seats. The last complete party tally found is from 30 October 2025. About 120 members have changed party since July 2024 and at least 60 since that tally, "
                          "so the blocks are out of date; no newer tally has been published. No member is named here.",
                          counts, ["SDP", "LP", "APGA", "NNPP", "PDP", "ADC", "YPP", "APC"],
                          {"APC": "1d7a3a", "PDP": "d62828", "LP": "2a9d8f", "NNPP": "f4a261", "APGA": "3a86ff", "SDP": "6a4c93", "ADC": "8a8680", "YPP": "e9c46a"},
                          "Member of the House of Representatives", r"(?i)house of representatives of nigeria|nigerian house of representatives")]


def china():
    """The National People's Congress (2,977 deputies of the 14th NPC, confirmed 24 Feb 2023). No party split of the deputies is published in the
    official reports found, so the chamber is one block."""
    return [fixed_chamber("National People's Congress", 2977, "https://subsites.chinadaily.com.cn/npc/2023-02/25/c_861912.htm", "2023-02-24",
                          "2,977 deputies of the 14th NPC, whose qualifications the Standing Committee confirmed on 24 February 2023. No count by party has been published in the reports found, "
                          "so the chamber is shown as one block. No member is named here.",
                          {"Deputies (party split not published)": 2977}, [], {"Deputies (party split not published)": "8a8680"},
                          "Deputy to the National People's Congress", r"(?i)national people's congress|\bNPC\b")]



def new_zealand():
    """NZ Parliament's official current/former registers; Jina is a transport fallback for its challenge page."""
    base = "https://www3.parliament.nz/en/mps-and-electorates/"

    def read(url):
        # The official site challenges command-line clients. The reader returns the official
        # page as Markdown; attribution and position URLs remain Parliament's own URLs.
        return get("https://r.jina.ai/" + url, as_json=False).decode("utf-8-sig")

    def date(text):
        return dt.datetime.strptime(text.strip(), "%d %B %Y").date().isoformat()

    parties = {"Labour Party": "Labour", "Independent - not party affiliated": "Independent",
               "NZ First Party": "New Zealand First"}
    url = base + "members-of-parliament"
    text = read(url)
    total_match = re.search(r"represented by (\d+) MPs", text)
    expected = re.search(r"Displaying 1 - (\d+) of \1", text)
    members = []
    for line in text.splitlines():
        if not line.startswith("| ") or "![Image" not in line:
            continue
        cols = line.split("|")
        m = re.search(r"\[([^\]]+)\]\((https://www3\.parliament\.nz/en/mps-and-electorates/members-of-parliament/[^ )]+)", cols[2])
        if not m:
            continue
        surname, first = m[1].split(", ", 1)
        members.append(dict(name=first + " " + surname, party=parties.get(cols[3].strip(), cols[3].strip()),
                            place=cols[4].strip(), ref=m[2].rstrip("/").rsplit("/", 1)[1], url=m[2]))
    if not total_match or not expected or len(members) != int(expected[1]) or len({m["ref"] for m in members}) != len(members):
        raise ValueError("NZ current register incomplete or format changed")
    if not 0 <= int(total_match[1]) - len(members) <= 2:
        raise ValueError("NZ roster and stated House size disagree: review before publishing")

    former_text = read(base + "former-members-of-parliament/")
    former = []
    pattern = r"\[([^\]]+)\]\((https://www3\.parliament\.nz/en/mps-and-electorates/former-members-of-parliament/[^ )]+)[^\n]*\n\s*\n([^\n]+)"
    for m in re.finditer(pattern, former_text):
        terms = re.findall(r"([A-Za-z ]+), (\d{1,2} [A-Za-z]+ \d{4}) - (\d{1,2} [A-Za-z]+ \d{4})", m[3])
        if not terms or ", " not in m[1]:
            continue
        surname, first = m[1].split(", ", 1)
        former.append(dict(name=first + " " + surname, party=parties.get(terms[-1][0].strip(), terms[-1][0].strip()),
                           start=date(terms[0][1]), end=date(terms[-1][2]), url=m[2], ref=m[2].rstrip("/").rsplit("/", 1)[1]))

    def enrich(member):
        detail = read(member["url"])
        first = re.search(r"Date first elected:\s*(\d{1,2} [A-Za-z]+ \d{4})", detail)
        if not first:
            raise ValueError("NZ member profile has no first-election date: " + member["name"])
        return {**member, "start": date(first[1])}

    return [dict(name="New Zealand House of Representatives", seats=int(total_match[1]), source_url=url,
                 note=f"{total_match[1]}-seat Parliament. Party blocks counted from the official current-member register; any difference from the stated House size is shown as Vacant. Position start is first election to Parliament, not the start of the current electorate. Former register currently paginates at 200; the current former-supporter matches are on its first page. Unlit seats mean no supporter found, never opposition.",
                 role="Member of Parliament", role_re=r"(?i)\bMP\b|member of parliament", role_start=r"(?i)(MP|member of parliament)",
                 members=members, former=former, enrich=enrich,
                 party_order=["Green Party", "Te Pāti Māori", "Labour", "Independent", "New Zealand First", "National Party", "ACT Party"],
                 colours={"Green Party": "098137", "Te Pāti Māori": "b21f2d", "Labour": "d82c20", "Independent": "888888",
                          "New Zealand First": "111111", "National Party": "00529f", "ACT Party": "fde401"})]


def ireland():
    """Dáil Éireann (174) and Seanad Éireann (60): the Houses of the Oireachtas members API (api.oireachtas.ie), with each member's
    party, constituency (or Seanad panel) and dates. Run `seats.py data/ie`."""
    def chamber(code, house, seats, name, role, role_re, order, colours, note):
        d = get(f"https://api.oireachtas.ie/v1/members?house_no={house}&chamber={code}&limit=500")["results"]
        cur, former = [], []
        for res in d:
            m = res["member"]
            ms = [x["membership"] for x in m["memberships"] if x["membership"]["house"]["houseCode"] == code and x["membership"]["house"]["houseNo"] == str(house)]
            if not ms:
                continue
            ms.sort(key=lambda x: x["dateRange"]["start"] or "")
            last = ms[-1]
            party = (last["parties"][-1]["party"]["showAs"] if last["parties"] else "Independent")
            place = (last["represents"][0]["represent"]["showAs"] if last["represents"] else "")
            row = dict(name=m["fullName"], party=party, place=place, ref=m["memberCode"], start=(ms[0]["dateRange"]["start"] or ""),
                       url=f"https://www.oireachtas.ie/en/members/member/{m['memberCode']}/")
            if last["dateRange"]["end"]:
                row["end"] = last["dateRange"]["end"]
                former.append(row)
            else:
                cur.append(row)
        return dict(name=name, level="national", seats=seats, source_url=f"https://api.oireachtas.ie/v1/members?house_no={house}&chamber={code}", note=note,
                    role=role, role_re=role_re, role_start=role_re, members=cur, former=former, party_order=order, colours=colours)

    colours = {"People Before Profit-Solidarity": "8e2420", "Social Democrats": "752f8a", "Labour Party": "d82c20", "Sinn Féin": "326760", "Green Party": "99cc33",
               "Fianna Fáil": "66bb66", "Fine Gael": "6699ff", "Independent Ireland": "4f9a9a", "Aontú": "44532a", "Independent": "8a8680"}
    order = ["People Before Profit-Solidarity", "Social Democrats", "Labour Party", "Sinn Féin", "Green Party", "Fianna Fáil", "Fine Gael", "Independent Ireland", "Aontú", "Independent"]
    return [chamber("dail", 34, 174, "Dáil Éireann", "Teachta Dála (TD)", r"(?i)\bTD\b|teachta d|\bdeputy\b", order, colours,
                    "174 seats in the 34th Dáil (elected 29 November 2024). Who sits, their party and constituency are from the Oireachtas members API; the Ceann Comhairle counts as a seat. Unlit seats mean nothing found, never opposition."),
            chamber("seanad", 27, 60, "Seanad Éireann", "Senator", r"(?i)\bsenator\b|seanadóir", order, colours,
                    "60 seats in the 27th Seanad (January 2025): 43 elected from five vocational panels, six by university graduates and 11 nominated by the Taoiseach. A vacancy shows as Vacant. Unlit seats mean nothing found, never opposition.")]


def italy():
    """Camera dei deputati (400): the Chamber's alphabetical member lists (camera.it, legislature XIX). Senato della Repubblica: the Senate's open
    data (dati.senato.it SPARQL: current elected senators and senators for life, with their group). Run `seats.py data/it`."""
    import html, urllib.parse
    deputies = []
    for L in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        try:
            page = get(f"https://www.camera.it/deputati/elenco?leg=19&lettera={L}", as_json=False).decode("utf-8", "ignore")
        except SystemExit:
            continue
        for card in page.split('class="deputato-card"')[1:]:
            nm = re.search(r'class="deputato-nome"\s+title="([^"]+)"', card)
            gr = re.search(r'class="deputato-gruppo"\s+title="([^"]+)"', card)
            ident = re.search(r'/deputati/elenco/19-(\d+)', card)
            if not (nm and gr and ident):
                continue
            deputies.append(dict(name=html.unescape(nm[1]).strip().title(), party=html.unescape(gr[1]).strip(), ref=ident[1], url=f"https://www.camera.it/deputati/elenco/19-{ident[1]}"))
    seen, uniq = set(), []
    for d in deputies:
        if d["ref"] not in seen:
            seen.add(d["ref"]); uniq.append(d)
    deputies = uniq

    def sparql(query):
        u = "https://dati.senato.it/sparql?" + urllib.parse.urlencode({"query": query, "format": "application/sparql-results+json"})
        return get(u, headers={"Accept": "application/sparql-results+json"})["results"]["bindings"]
    pre = "PREFIX osr: <http://dati.senato.it/osr/> PREFIX ocd: <http://dati.camera.it/ocd/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
    names = {b["g"]["value"]: b["tb"]["value"] for b in sparql(pre + "SELECT ?g ?tb WHERE { ?g a ocd:gruppoParlamentare; osr:denominazione ?d . ?d osr:titoloBreve ?tb FILTER NOT EXISTS {?d osr:fine ?f} }")}
    sen = {}
    for b in sparql(pre + """SELECT DISTINCT ?s ?label ?tipo ?regione WHERE { ?s a osr:Senatore; rdfs:label ?label; osr:mandato ?m . ?m osr:legislatura ?l; osr:tipoMandato ?tipo .
        OPTIONAL { ?m osr:regioneElezione ?regione } FILTER(STR(?l)='19') FILTER NOT EXISTS { ?m osr:fine ?f } }"""):
        sen[b["s"]["value"]] = dict(name=b["label"]["value"], place=b.get("regione", {}).get("value", "A vita" if "vita" in b["tipo"]["value"] else ""))
    grp = {}
    for b in sparql(pre + """SELECT DISTINCT ?s ?g ?i WHERE { ?s a osr:Senatore; osr:mandato ?m . ?m osr:legislatura ?l FILTER(STR(?l)='19') FILTER NOT EXISTS { ?m osr:fine ?f }
        ?s ?link ?a . ?a a ocd:adesioneGruppo; osr:gruppo ?g; osr:inizio ?i; osr:legislatura ?al FILTER(STR(?al)='19') FILTER NOT EXISTS { ?a osr:fine ?af } }"""):
        s_, g_, i_ = b["s"]["value"], b["g"]["value"], b["i"]["value"]
        if s_ not in grp or i_ > grp[s_][1]:
            grp[s_] = (g_, i_)
    senators = [dict(name=v["name"], party=names.get(grp.get(k, ("",))[0], "Misto"), place=v["place"], ref=k.rsplit("/", 1)[1], url=k) for k, v in sen.items()]
    colours = {"Fratelli d'Italia": "123f8c", "FdI": "123f8c", "Lega": "1b7f3b", "Forza Italia": "0087dc", "Noi Moderati": "58b4e8", "Partito Democratico": "e4002b", "PD": "e4002b",
               "Movimento 5 Stelle": "f5c518", "MoVimento 5 Stelle": "f5c518", "M5S": "f5c518", "Alleanza Verdi e Sinistra": "78b82a", "Italia Viva": "f58220", "Azione": "ee7d00", "Misto": "8a8680", "Autonomie": "7a5a2e",
               "FI-BP": "0087dc", "LSP": "1b7f3b", "IV-CR": "f58220", "Cd'I": "58b4e8", "Aut (": "7a5a2e", "Futuro Nazionale": "5b3a29", "Sud chiama": "b5651d"}
    def colour_for(party):
        pl = party.lower()
        for key, c in colours.items():
            if key.lower() in pl:
                return c
        return "8a8680"
    def chamber(name, seats, members, note, order_keys, role_re):
        parties = sorted({m["party"] for m in members})
        rank = lambda p: next((i for i, k in enumerate(order_keys) if k in p.lower()), 50)
        return dict(name=name, level="national", seats=seats, source_url="https://www.camera.it/deputati/elenco?leg=19" if name.startswith("Camera") else "https://dati.senato.it/sparql",
                    note=note, role="Member of Parliament", role_re=role_re, role_start=role_re,
                    members=members, former=[],
                    party_order=sorted(parties, key=lambda p: (rank(p), p)), colours={p: colour_for(p) for p in parties})
    order = ["verdi e sinistra", "alleanza verdi", "5 stelle", "m5s", "democratico", "pd-idp", "misto", "aut (", "autonomie", "italia viva", "iv-cr", "azione", "noi moderati", "cd'i", "forza italia", "fi-bp", "lega", "lsp", "fratelli", "fdi"]
    return [chamber("Camera dei deputati", 400, deputies, "400 seats, XIX legislature (elected 25 September 2022). Who sits and their parliamentary group are from the Chamber's own lists; names there are SURNAME Name, so matches by name are printed for checking. Unlit seats mean nothing found, never opposition.", order, r"(?i)deputat|member of the (italian )?chamber of deputies"),
            chamber("Senato della Repubblica", len(senators), senators, "200 elected senators plus senators for life, XIX legislature. Who sits and their group are from the Senate's open data (dati.senato.it). The seat count is the number of senators sitting, since senators for life are not part of the 200. Unlit seats mean nothing found, never opposition.", order, r"(?i)senator|member of the (italian )?senate")]


def mexico():
    """Cámara de Diputados (500) and Senado de la República (128), LXVI Legislatura. The official lists (sitl.diputados.gob.mx, senado.gob.mx)
    refuse or time out for scripts, so this reads the English Wikipedia article for the legislature, whose member lists are kept up to date with
    each substitution (a seat shows its current holder; where one replaced another the pair is printed "A (until date) B (since date)"). It is a
    secondary source: say so in the chamber note, and replace it with the official lists when they can be read (see the Mexico guide)."""
    import html
    api = "https://en.wikipedia.org/w/api.php?action=parse&page=LXVI_Legislature_of_the_Mexican_Congress&prop=text&format=json&redirects=1"
    page = get(api, headers={"User-Agent": "WealthTaxSupporters/1.0 (https://wealthtaxsupporters.com)"})["parse"]["text"]["*"]
    page = re.sub(r"<sup[^>]*>.*?</sup>", "", page, flags=re.S)
    page = re.sub(r'<span class="noprint".*?</span>', "", page, flags=re.S)
    i_sen, i_dep, i_end = page.index('id="Senate_members"'), page.index('id="Chamber_of_Deputies_members"'), page.index('id="See_also"')
    PARTY = {"MORENA": "Morena", "PT": "Partido del Trabajo", "PVEM": "Partido Verde", "MC": "Movimiento Ciudadano", "PRI": "PRI", "PAN": "PAN",
             "PRD": "PRD", "Independent": "Independent", "No party": "Independent"}

    ALIAS = {"Amalia García": "Amalia García Medina"}  # Wikipedia's article title is shorter than the name the register uses

    def members(seg):
        out = []
        for dd in re.findall(r"<dd>(.*?)</dd>", seg, flags=re.S):
            if "(until " in dd:  # a substitution: the second name is the holder now
                parts = re.split(r"\(until [^)]*\)", dd)
                dd = parts[-1]
            names = re.findall(r'<a [^>]*title="([^"]+)"', dd)
            text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", dd))).strip().replace("▌", "").strip()
            text = re.sub(r"^\d+\s+", "", text)
            pm = re.search(r"\(([^()]+)\)", text)
            party = PARTY.get(pm[1].strip(), pm[1].strip()) if pm else ""
            name = (names[-1] if names else text.split(" (")[0]).replace(" (page does not exist)", "").strip()
            name = ALIAS.get(name, name)
            if not name or not party:
                continue
            out.append(dict(name=name, party=party, ref=re.sub(r"\W+", "-", name.lower()), place="", url="https://en.wikipedia.org/wiki/LXVI_Legislature_of_the_Mexican_Congress"))
        return out
    deputies, senators = members(page[i_dep:i_end]), members(page[i_sen:i_dep])
    colours = {"Morena": "8b1a1a", "Partido del Trabajo": "e07a1f", "Partido Verde": "62b04b", "Movimiento Ciudadano": "2aa5c9", "PRI": "1f8f4e", "PAN": "0a5aa8", "PRD": "c9a227", "Independent": "8a8680"}
    order = ["Morena", "Partido del Trabajo", "Partido Verde", "Movimiento Ciudadano", "PRI", "PAN", "PRD", "Independent"]
    role_re = r"(?i)\bdiputad|\bfederal deputy|member of the chamber of deputies"
    srole_re = r"(?i)\bsenator|\bsenador"

    def chamber(name, seats, members, role, rre, note):
        return dict(name=name, level="national", seats=seats, source_url="https://en.wikipedia.org/wiki/LXVI_Legislature_of_the_Mexican_Congress", note=note, role=role,
                    role_re=rre, role_start=rre, members=members, former=[], party_order=order, colours=colours)
    src = " Who sits and their party are from the English Wikipedia list for the legislature, which tracks substitutions, because the official lists (sitl.diputados.gob.mx, senado.gob.mx) could not be read by script. Unlit seats mean nothing found, never opposition."
    return [chamber("Cámara de Diputados", 500, deputies, "Federal deputy", role_re, "500 seats (300 by district and 200 by proportional representation), LXVI Legislatura, elected 2 June 2024." + src),
            chamber("Senado de la República", 128, senators, "Senator", srole_re, "128 seats (96 by state and 32 by proportional representation), LXVI Legislatura, elected 2 June 2024." + src)]


def argentina():
    """Cámara de Diputados (257) and Senado de la Nación (72): the two official lists of sitting members, read as the pages
    www.diputados.gob.ar/diputados/ (name, province, bloc, mandate dates) and www.senado.gob.ar/senadores/listados/listaSenadoRes
    (name, province, bloc, mandate dates). A bloc is the party or interbloc the member sits in; blocs are listed by size."""
    import html

    def cells(row):
        return [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", c))).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", row, flags=re.S)]

    def date(x):
        m = re.search(r"(\d\d)/(\d\d)/(\d{4})", x)
        return f"{m[3]}-{m[2]}-{m[1]}" if m else ""

    def bloc(b):
        b = re.sub(r"\s+", " ", b).strip()
        return b if b != b.upper() else b.title().replace(" Por ", " por ").replace(" De ", " de ").replace(" La ", " la ").replace(" Y ", " y ")

    def flip(n):  # "Aguirre, Hilda" -> "Hilda Aguirre"
        a, _, b = n.partition(",")
        return f"{b.strip()} {a.strip()}".strip()
    dip_url, sen_url = "https://www.diputados.gob.ar/diputados/", "https://www.senado.gob.ar/senadores/listados/listaSenadoRes"
    deputies, senators = [], []
    for row in re.findall(r"<tr>(.*?)</tr>", get(dip_url, as_json=False).decode("utf-8"), flags=re.S):
        c, a = cells(row), re.search(r'href="(/diputados/[^"]+)"', row)
        if a and len(c) >= 7:
            deputies.append(dict(name=flip(c[1]), party=bloc(c[3]), place=c[2].title(), start=date(c[5]), ref=a[1].strip("/").split("/")[-1], url="https://www.diputados.gob.ar" + a[1]))
    for row in re.findall(r"<tr>(.*?)</tr>", get(sen_url, as_json=False).decode("utf-8"), flags=re.S):
        c, a = cells(row), re.search(r'href="(/senadores/senador/(\d+))"', row)
        if a and len(c) >= 5:
            senators.append(dict(name=flip(c[1]), party=bloc(c[3]), place=c[2], start=date(c[4].split(" ")[0]), ref=a[2], url="https://www.senado.gob.ar" + a[1]))
    if len(deputies) < 200 or len(senators) < 60:
        sys.exit(f"Argentina: read {len(deputies)} deputies and {len(senators)} senators; the pages have changed, check the adapter")

    def chamber(name, seats, members, role, rre, note, src):
        count = {}
        for m in members:
            count[m["party"]] = count.get(m["party"], 0) + 1
        order = sorted(count, key=lambda p: -count[p])
        palette = ["6aa4d8", "f2c230", "8b1a1a", "1f8f4e", "e07a1f", "2aa5c9", "c9a227", "9a6fb0", "62b04b", "d36b8f"]
        colours = {p: palette[i] if i < len(palette) else "8a8680" for i, p in enumerate(order)}
        return dict(name=name, level="national", seats=seats, source_url=src, note=note, role=role, role_re=rre, role_start=rre,
                    members=members, former=[], party_order=order, colours=colours)
    tail = " Who sits and their bloc are from the chamber's own list of sitting members. A seat is shown under the member's bloc. Unlit seats mean nothing found, never opposition."
    return [chamber("Cámara de Diputados de la Nación", 257, deputies, "National deputy", r"(?i)diputad[oa].*nacional|national deputy|member of the chamber of deputies|diputad[oa] nacional",
                    "257 seats, elected by province, renewed by halves every two years." + tail, dip_url),
            chamber("Senado de la Nación", 72, senators, "National senator", r"(?i)senador|senator", "72 seats, three per province and three for the City of Buenos Aires, renewed by thirds every two years." + tail, sen_url)]


def finland():
    """The Eduskunta (200 seats): the seating plan of the plenary hall on avoindata.eduskunta.fi (SeatingOfParliament), one row per seat with the
    member's party group. It lists the sitting members only (ministers included, as in Finland they keep their seat; a substitute for a member on
    leave is not a separate row). The legacy MemberOfParliament table is not used: its current-term fields are stale."""
    PARTY = {"kok": "National Coalition Party", "ps": "Finns Party", "sd": "Social Democratic Party", "kesk": "Centre Party", "vihr": "Green League",
             "vas": "Left Alliance", "r": "Swedish People's Party", "kd": "Christian Democrats", "liik": "Movement Now", "tv": "Vornanen (own group)"}
    colours = {"National Coalition Party": "0b4a9b", "Finns Party": "ffd400", "Social Democratic Party": "e11931", "Centre Party": "01954b",
               "Green League": "61bf1a", "Left Alliance": "bf1e2e", "Swedish People's Party": "ffdd93", "Christian Democrats": "2b6cb0",
               "Movement Now": "8a8680", "Vornanen (own group)": "8a8680"}
    rows = []
    for page in range(5):
        d = get(f"https://avoindata.eduskunta.fi/api/v1/tables/SeatingOfParliament/rows?perPage=100&page={page}")
        rows += d.get("rowData", [])
        if not d.get("hasMore"):
            break
    if len(rows) != 200:
        sys.exit(f"Finland: read {len(rows)} seats, expected 200; the table has changed, check the adapter")
    members = [dict(name=f"{r[3]} {r[2]}".strip(), party=PARTY.get(r[4], r[4]), ref=r[0], place="", start="",
                    url="https://www.eduskunta.fi/FI/kansanedustajat/Sivut/" + r[0] + ".aspx") for r in rows]
    order = ["National Coalition Party", "Finns Party", "Social Democratic Party", "Centre Party", "Green League", "Left Alliance",
             "Swedish People's Party", "Christian Democrats", "Movement Now", "Vornanen (own group)"]
    return [dict(name="Parliament of Finland (Eduskunta)", level="national", seats=200, source_url="https://avoindata.eduskunta.fi/api/v1/tables/SeatingOfParliament/rows",
                 note="200 seats, elected in April 2023 by proportional representation in 13 districts. Who sits and their group are from the plenary seating plan in the Parliament's open data (ministers keep their seat). Unlit seats mean nothing found, never opposition.",
                 role="Member of Parliament", role_re=r"(?i)member of parliament|eduskunta|cosponsor|motion signatory|wealth-tax advocate|\bMP\b",
                 role_start=r"(?i)member of parliament", members=members, former=[], party_order=order, colours=colours)]


def european_parliament():
    """The European Parliament (720 seats): data.europarl.europa.eu open data (sitting MEPs, their country and political group).
    Run `seats.py data/eu`: supporters are matched across every country register, by the MEP's own country."""
    d = get("https://data.europarl.europa.eu/api/v2/meps/show-current?format=application%2Fld%2Bjson&offset=0&limit=1000")["data"]
    GROUP = {"The Left": "The Left", "S&D": "S&D", "Verts/ALE": "Greens/EFA", "Renew": "Renew Europe", "PPE": "EPP", "ECR": "ECR",
             "PfE": "Patriots for Europe", "ESN": "Europe of Sovereign Nations", "NI": "Non-attached"}
    members = [dict(name=f"{m['givenName']} {m['familyName']}".strip(), party=GROUP.get(m.get("api:political-group"), m.get("api:political-group", "")),
                    ref=m["identifier"], country=m.get("api:country-of-representation", ""), place=m.get("api:country-of-representation", ""),
                    url=f"https://www.europarl.europa.eu/meps/en/{m['identifier']}") for m in d]
    return [dict(name="European Parliament", level="supranational", seats=720, source_url="https://data.europarl.europa.eu/api/v2/meps/show-current",
                 note="720 seats, elected in June 2024 from the 27 member states. Who sits, their country and political group are from the Parliament's open data. A seat is listed under the member's group, not their national party.",
                 role="MEP", role_re=r"(?i)(?<!former )\bMEP\b|member of the european parliament", role_start=r"(?i)(MEP|member of the european parliament)",
                 members=members, former=[], by_country=True,
                 party_order=["The Left", "S&D", "Greens/EFA", "Renew Europe", "EPP", "ECR", "Patriots for Europe", "Europe of Sovereign Nations", "Non-attached"],
                 colours={"The Left": "8b1a1a", "S&D": "e4003b", "Greens/EFA": "3fa535", "Renew Europe": "ffcc00", "EPP": "3399ff", "ECR": "1a6fa8",
                          "Patriots for Europe": "4b2e83", "Europe of Sovereign Nations": "7a5a2e", "Non-attached": "8a8680"})]


def united_nations():
    """The UN General Assembly (193 seats, one per member state): the UN's own list of member states by regional group
    (un.org/dgacm). A seat is a government, not a person: run `seats.py data/un`; the governments recorded in data/un/actors.csv
    (named "Government of <state>") light the seat of their state. Türkiye and Israel sit in WEOG for electoral purposes."""
    import html as _html
    url = "https://www.un.org/dgacm/en/content/regional-groups"
    page = get(url, as_json=False).decode("utf-8", "ignore")
    page = re.sub(r"(?s)<(script|style).*?</\1>", "", page)
    GROUPS = [("African States", "African Group"), ("Asia-Pacific States", "Asia-Pacific Group"), ("Eastern European States", "Eastern European Group"),
              ("Latin American and Caribbean States", "GRULAC"), ("Western European and other States", "WEOG")]
    heads = [(m.start(), re.sub(r"<[^>]+>", "", m.group(1)).strip()) for m in re.finditer(r"(?s)<h\d[^>]*>(.*?)</h\d>", page)]
    members, seen = [], set()
    for label, group in reversed(GROUPS):  # the last group first, so a state listed in two (Türkiye) stays in WEOG
        start = next(i for i, h in heads if h == label)
        end = min([i for i, h in heads if i > start] or [len(page)])
        text = _html.unescape(re.sub(r"(?s)<[^>]+>", "\n", page[start:end])).split("Special cases")[0]
        for n in (x.strip().rstrip("*").strip() for x in text.split("\n")):
            if n and n != label and n not in seen:
                seen.add(n)
                members.append(dict(name=f"Government of {n}", party=group, ref=n, place=n, url=url))
    return [dict(name="United Nations General Assembly", level="supranational", seats=193, source_url=url,
                 note="193 seats, one per member state, grouped by the UN's regional groups (the United States sits with WEOG for electoral purposes). A seat is a government, not a person: it is lit where the register holds a sourced public position of that state's government for a wealth tax. Observer states (the Holy See and Palestine) have no vote and no seat here.",
                 role="Member state", role_re=r"(?i)member state", role_start=r"(?i)member state", members=members, former=[],
                 party_order=[g for _, g in GROUPS],
                 colours={"African Group": "2f8f5b", "Asia-Pacific Group": "c9622a", "Eastern European Group": "7a5ab3", "GRULAC": "d6a21f", "WEOG": "2d6fb5"})]


def pan_african_parliament():
    """The Pan-African Parliament (up to 275 seats, five per AU member state): the MPs each member state's page on pap.au.int lists
    (/mps/<state>). Run `seats.py data/au`: supporters are matched across every country register, by the MP's own country. The
    list is partial (states whose delegation has not been sworn in show none) and has no party, so seats are grouped by the AU's
    five regions and the rest are shown as "Not on the list"."""
    import html as _html
    base = "https://pap.au.int"
    REGIONS = {
        "Northern": {"Algeria": "DZ", "Egypt": "EG", "Libya": "LY", "Mauritania": "MR", "Morocco": "MA", "Sahrawi": "EH", "Tunisia": "TN"},
        "Western": {"Benin": "BJ", "Burkina Faso": "BF", "Cabo Verde": "CV", "Côte d'Ivoire": "CI", "Gambia": "GM", "Ghana": "GH", "Guinea": "GN",
                    "Guinea-Bissau": "GW", "Liberia": "LR", "Mali": "ML", "Niger": "NE", "Nigeria": "NG", "Senegal": "SN", "Sierra Leone": "SL", "Togo": "TG"},
        "Central": {"Burundi": "BI", "Cameroon": "CM", "Central Africa": "CF", "Chad": "TD", "Congo": "CG", "DRC": "CD", "Equatorial Guinea": "GQ",
                    "Gabon": "GA", "São Tomé and Príncipe": "ST"},
        "Eastern": {"Comoros": "KM", "Djibouti": "DJ", "Eritrea": "ER", "Ethiopia": "ET", "Kenya": "KE", "Madagascar": "MG", "Mauritius": "MU",
                    "Rwanda": "RW", "Seychelles": "SC", "Somalia": "SO", "South Sudan": "SS", "Sudan": "SD", "Tanzania": "TZ", "Uganda": "UG"},
        "Southern": {"Angola": "AO", "Botswana": "BW", "Eswatini": "SZ", "Lesotho": "LS", "Malawi": "MW", "Mozambique": "MZ", "Namibia": "NA",
                     "South Africa": "ZA", "Zambia": "ZM", "Zimbabwe": "ZW"}}
    find = get(base + "/en/find-your-mp", as_json=False).decode("utf-8", "ignore")
    slugs = {}
    for href in dict.fromkeys(_html.unescape(x) for x in re.findall(r'href="(/mps/[^"]+)"', find)):
        slugs[norm(urllib.parse.unquote(href.split("/mps/")[1]))] = href
    members = []
    for region, states in REGIONS.items():
        for state, iso in states.items():
            href = slugs.get(norm(state)) or next((h for k, h in slugs.items() if k.startswith(norm(state)[:6])), None)
            if not href:
                print(f"  no MP page for {state}", file=sys.stderr)
                continue
            page = get(base + urllib.parse.quote(urllib.parse.unquote(href), safe="/:'"), as_json=False).decode("utf-8", "ignore")
            for term, name in re.findall(r'href="/taxonomy/term/(\d+)">.*?people-item-info-title">\s*([^<]+?)\s*</h4>', page, re.S):
                name = _html.unescape(name)
                name = re.sub(r"(?i)\(mrs?\.?\)|\b(H\.E\.|Hon\.?|Sen\.?|Rt\.?|Dr\.?|Prof\.?|Chief|Amb\.?|Eng\.?)(?=\s)", " ", name)
                members.append(dict(name=" ".join(name.split()), party=region, ref=term, country=iso, place=state, url=f"{base}/taxonomy/term/{term}"))
    return [dict(name="Pan-African Parliament", level="supranational", seats=275, source_url=base + "/en/honorable-members-parliament",
                 note="Up to 275 seats, five per member state of the African Union, filled from each state's own parliament. Who sits is from the MP lists on the Parliament's website, which is partial: a state whose delegation has not been listed shows no seats, and the list gives no party, so seats are grouped by the AU's five regions. A seat is lit where a supporter recorded in a country register is on the list.",
                 role="Member of the Pan-African Parliament", role_re=r"(?i)pan-african parliament|\bPAP\b", role_start=r"(?i)(member of the )?pan-african parliament",
                 members=members, former=[], by_country=True, vacant_label="Not on the list",
                 party_order=list(REGIONS),
                 colours={"Northern": "c9622a", "Western": "2f8f5b", "Central": "7a5ab3", "Eastern": "d6a21f", "Southern": "2d6fb5"})]


def south_africa():
    """The National Assembly (400 seats): the Parliamentary Monitoring Group's open API (api.pmg.org.za/member/), which lists
    each member's house, party and whether they currently sit. The API gives initials only ("Maotwe, Ms OMC"), so the full
    name is taken from the member's People's Assembly link (pa.org.za/person/omphile-mankoba-confidence-maotwe/)."""
    NAMES = {"MKP": "MK Party", "Action SA": "ActionSA", "FF+": "FF Plus", "PA": "Patriotic Alliance"}
    url, rows = "https://api.pmg.org.za/member/", []
    while url:
        d = get(url)
        rows += d["results"]
        url = d.get("next")
    members = []
    for m in rows:
        if not (m.get("current") and (m.get("house") or {}).get("name_short") == "NA"):
            continue
        slug = (m.get("pa_link") or "").rstrip("/").rsplit("/", 1)[-1]
        sur, _, rest = m["name"].partition(",")
        words = [w.capitalize() for w in slug.split("-")]
        if words and slug and words[-1].lower() != sur.strip().split()[-1].lower():  # the two sites spell the surname differently: keep PMG's
            words[-1] = sur.strip().split()[-1]
        name = " ".join(words) if slug else f"{rest.split()[-1]} {sur}"
        party = (m.get("party") or {}).get("name", "Independent")
        members.append(dict(name=name, party=NAMES.get(party, party), ref=m["id"], place=(m.get("province") or {}).get("name", ""),
                            start=m.get("start_date") or "", url=f"https://pmg.org.za/member/{m['id']}/"))
    order = ["ANC", "DA", "MK Party", "EFF", "IFP", "Patriotic Alliance", "ActionSA", "FF Plus"]
    return [dict(name="National Assembly", level="national", seats=400, source_url="https://api.pmg.org.za/member/",
                 note="400 seats; who sits and their party are from the Parliamentary Monitoring Group's member list (the National Assembly members flagged as current). The Government of National Unity parties are the ANC, DA, IFP, PA, GOOD and others.",
                 role="Member of the National Assembly", role_re=r"(?i)national assembly|\bMP\b", role_start=r"(?i)(member of the national assembly|MP\b)",
                 members=members, former=[], party_order=order,
                 colours={"ANC": "1a7f3c", "DA": "2d6fb5", "MK Party": "3a3a3a", "EFF": "c8102e", "IFP": "d6a21f", "Patriotic Alliance": "7a5ab3", "ActionSA": "e07b39", "FF Plus": "8a6d3b"})]


def scottish_parliament():
    """The Scottish Parliament (129 seats: 73 constituency + 56 regional): data.parliament.scot open data. Used for the UK register with
    `seats.py data/gb --adapter scottish_parliament` (the Commons and Lords come from seats_uk.py)."""
    base = "https://data.parliament.scot/api/"
    members, mparty, parties = get(base + "members"), get(base + "memberparties"), get(base + "parties")
    cons = {c["ID"]: c["Name"] for c in get(base + "constituencies")}
    TYPOS = {"Central Scot and Lothians West": "Central Scotland and Lothians West", "Central Scotland and Lothains": "Central Scotland and Lothians"}  # as the Parliament's data spells them
    regs = {r["ID"]: TYPOS.get(r["Name"].strip(), r["Name"].strip()) for r in get(base + "regions")}
    seat_rows = get(base + "memberelectionconstituencystatuses") + get(base + "memberelectionregionstatuses")
    SHORT = {"SNP": "Scottish National Party", "Lab": "Labour", "Con": "Conservative", "LD": "Liberal Democrats", "Green": "Scottish Greens",
             "Reform": "Reform UK", "NPA": "No Party Affiliation", "Ind": "Independent"}
    abbr = {p["ID"]: SHORT.get(p["Abbreviation"], p["ActualName"]) for p in parties}
    party_of = {}
    for x in sorted(mparty, key=lambda x: x["ValidFromDate"]):  # the party they hold now, or held last
        party_of[x["PersonID"]] = abbr.get(x["PartyID"], "")
    by_person = {}
    for r in seat_rows:
        by_person.setdefault(r["PersonID"], []).append(r)

    def name(m):
        sur = m["ParliamentaryName"].split(",")[0].strip()
        return f"{m['PreferredName'].strip()} {sur}"

    cur, former = [], []
    for m in members:
        rows = by_person.get(m["PersonID"], [])
        if not rows:
            continue
        if m["IsCurrent"]:
            r = max((r for r in rows if not r["ValidUntilDate"]), key=lambda r: r["ValidFromDate"], default=max(rows, key=lambda r: r["ValidFromDate"]))
            place = cons.get(r.get("ConstituencyID"), "") or regs.get(r.get("RegionID"), "")
            cur.append(dict(name=name(m), party=party_of.get(m["PersonID"], ""), ref=str(m["PersonID"]), place=place,
                            start=min(x["ValidFromDate"] for x in rows)[:10]))  # first election to the Parliament
        else:
            ends = [x["ValidUntilDate"][:10] for x in rows if x["ValidUntilDate"]]
            former.append(dict(name=name(m), party=party_of.get(m["PersonID"], ""), ref=str(m["PersonID"]), end=max(ends) if ends else "",
                               start=min(x["ValidFromDate"] for x in rows)[:10]))
    return [dict(name="Scottish Parliament", level="regional", seats=129, source_url="https://data.parliament.scot/api/members",
                 note="129 seats: 73 constituency and 56 regional members, elected on 7 May 2026. Who sits and each member's party are from the Parliament's open data.",
                 role="MSP", role_re=r"(?i)\bMSP\b|member of the scottish parliament", role_start=r"(?i)(MSP|member of the scottish parliament)",
                 members=cur, former=former,
                 party_order=["Scottish Greens", "Scottish National Party", "Labour", "No Party Affiliation", "Independent", "Liberal Democrats", "Conservative", "Reform UK"],
                 colours={"Scottish National Party": "f2c500", "Labour": "d50000", "Conservative": "0087dc", "Liberal Democrats": "faa61a", "Scottish Greens": "78b82a",
                          "Reform UK": "12b6cf", "No Party Affiliation": "8a8680", "Independent": "8a8680"})]



ADAPTERS = {"nz": new_zealand, "se": sweden, "de": germany, "nl": netherlands, "no": norway, "fr": france, "br": brazil, "ca": canada, "es": spain, "pl": poland, "be": belgium, "in": india, "jp": japan, "my": malaysia, "sg": singapore, "id": indonesia, "ng": nigeria, "cn": china, "scottish_parliament": scottish_parliament, "european_parliament": european_parliament, "eu": european_parliament, "un": united_nations, "au": pan_african_parliament, "za": south_africa, "ie": ireland, "it": italy, "mx": mexico, "ar": argentina, "fi": finland}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--fix-status", action="store_true", help="make actors who have left the chamber former_role")
    ap.add_argument("--adapter", help="an adapter other than the country's own, e.g. scottish_parliament for data/gb")
    ap.add_argument("--local", action="append", default=[], metavar="URL=FILE",
                    help="use a file you saved yourself for a URL the site refuses to serve to scripts (ourcommons.ca sometimes does)")
    a = ap.parse_args()
    import hashlib, tempfile
    for pair in a.local:
        url, _, f = pair.rpartition("=")  # the URL may itself contain "="
        (Path(tempfile.gettempdir()) / ("wts-seats-" + hashlib.md5((url + "{}").encode()).hexdigest())).write_bytes(Path(f).read_bytes())
    cc = a.adapter or Path(a.dir).name.split("-")[0]
    if cc not in ADAPTERS:
        sys.exit(f"No adapter for '{cc}'. Have: {', '.join(sorted(ADAPTERS))}. Add one to ADAPTERS in this file.")
    actors_in = None
    if ADAPTERS[cc] in (european_parliament, pan_african_parliament):  # supporters sit in the register of their own country: look across all of them
        actors_in = []
        for sib in sorted(p for p in Path(a.dir).resolve().parent.iterdir() if (p / "actors.csv").exists() and p.name != Path(a.dir).name):
            iso = json.load(open(sib / "meta.json", encoding="utf-8")).get("iso2", sib.name.split("-")[0]).upper()
            for x in wtdb.load(str(sib), "actors"):
                if x["kind"] == "person" and x["actor_type"] == "politician":
                    actors_in.append(dict(x, actor_id=f"{sib.name}-{x['actor_id']}", _iso=iso))
    if ADAPTERS[cc] is united_nations:  # the governments are actors of data/un itself (most states have no register)
        latest = {}
        for e in sorted(wtdb.load(a.dir, "evidence"), key=lambda e: e["date"]):
            latest[e["actor_id"]] = e["stance"]  # a government whose latest evidence is a retraction lights no seat
        actors_in = [dict(x, actor_id=f"{Path(a.dir).name}-{x['actor_id']}") for x in wtdb.load(a.dir, "actors")
                     if x["actor_type"] == "government_body" and x["status"] == "active" and latest.get(x["actor_id"]) != "retracted"]
    run(a.dir, ADAPTERS[cc], a.dry_run, a.fix_status, actors_in)


if __name__ == "__main__":
    sys.exit(main())
