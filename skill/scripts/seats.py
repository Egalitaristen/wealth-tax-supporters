#!/usr/bin/env python3
"""Refresh a country's legislature seats from the parliament's own open member list.

Usage: python skill/scripts/seats.py data/<iso2> [--dry-run] [--fix-status] [--local URL=FILE]      (iso2 = se, de, nl, no, fr, br, ca)

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
                x["role"] = (re.sub(r"(?i)^member", "Former member", x["role"]) if re.match(r"(?i)member", x["role"]) else "Former " + x["role"][:1].lower() + x["role"][1:]) + (f", until {dt.date.fromisoformat(o['end']).strftime('%B %Y')}" if o["end"] else "")
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



ADAPTERS = {"se": sweden, "de": germany, "nl": netherlands, "no": norway, "fr": france, "br": brazil, "ca": canada, "es": spain, "pl": poland, "be": belgium, "in": india, "jp": japan, "my": malaysia}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--fix-status", action="store_true", help="make actors who have left the chamber former_role")
    ap.add_argument("--local", action="append", default=[], metavar="URL=FILE",
                    help="use a file you saved yourself for a URL the site refuses to serve to scripts (ourcommons.ca sometimes does)")
    a = ap.parse_args()
    import hashlib, tempfile
    for pair in a.local:
        url, _, f = pair.rpartition("=")  # the URL may itself contain "="
        (Path(tempfile.gettempdir()) / ("wts-seats-" + hashlib.md5((url + "{}").encode()).hexdigest())).write_bytes(Path(f).read_bytes())
    cc = Path(a.dir).name.split("-")[0]
    if cc not in ADAPTERS:
        sys.exit(f"No adapter for '{cc}'. Have: {', '.join(sorted(ADAPTERS))}. Add one to ADAPTERS in this file.")
    run(a.dir, ADAPTERS[cc], a.dry_run, a.fix_status)


if __name__ == "__main__":
    sys.exit(main())
