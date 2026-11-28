#!/usr/bin/env python3
"""Refresh a country's legislature seats from the parliament's own open member list.

Usage: python skill/scripts/seats.py data/<iso2> [--adapter NAME] [--dry-run] [--fix-status] [--local URL=FILE]      (iso2 = ar, at, au, ba, bd, be, bg, bo, br, ca, ch, cl, cn, co, cr, cz, de, dk, dz, ec, ee, eg, es, eu, fi, fr, gr, hr, hu, id, ie, in, is, it, jp, ke, kr, lb, lt, lu, ma, mk, mt, mx, my, ng, nl, no, nz, pe, ph, pk, pl, pt, py, ro, ru, se, sg, si, sk, sr, tn, tr, un, uy, za; un for the UN General Assembly; au for the Pan-African Parliament)

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
import countries  # noqa: E402

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


def native_tokens(s):
    """The words of a name in a non-Latin script (Arabic, Greek, Cyrillic, Hebrew, Thai...), folded so spelling variants meet: Arabic diacritics and
    tatweel dropped, alef, yeh, heh and waw forms unified, Greek accents dropped. A register name carries it in brackets after the Latin one: Mostafa Ragheb (مصطفى راغب)."""
    s = unicodedata.normalize("NFKC", s or "")
    s = s.translate(str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ى": "ي", "ئ": "ي", "ة": "ه", "ؤ": "و", "ـ": ""}))
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    return "".join(c.lower() if (unicodedata.category(c).startswith("L") and not unicodedata.name(c, "").startswith(("LATIN", "CJK", "HIRAGANA", "KATAKANA", "HANGUL"))) else " " for c in s).split()


def name_keys(name):
    toks = norm(name).split()
    return toks


def match(actor, members, by_q, by_norm, strict=False, deny=()):
    """(member, how) for the one member this actor is, or (None, ''). how: qid, exact, or fuzzy (reported for you to check)."""
    if actor["wikidata_qid"] and actor["wikidata_qid"] in by_q:
        return by_q[actor["wikidata_qid"]], "qid"
    if norm(actor["name"]) in deny:  # a name an adapter says is a different person from the member with the same words (a namesake)
        return None, ""
    cj = re.sub(r"\s", "", actor["name"])  # a name in kanji after the Latin one: 小池晃
    for m in members:
        if m.get("cjk") and m["cjk"] in cj:
            return m, "exact"
    nt = native_tokens(actor["name"])  # a name in Arabic, Greek, Cyrillic... after the Latin one; the member's own list gives it in "native" (or as the name)
    if len(nt) >= 2:
        c = [(m, set(mt)) for m in members for mt in [native_tokens(m.get("native") or m["name"])] if len(mt) >= 2 and (set(nt) <= set(mt) or set(mt) <= set(nt))]
        if len(c) == 1:
            return c[0][0], "exact" if c[0][1] == set(nt) else "fuzzy"
    n = norm(actor["name"])
    if n in by_norm and len(by_norm[n]) == 1:
        return by_norm[n][0], "exact"
    toks = n.split()
    byinit = [m for m in members if m.get("init") and m.get("sur") and len(toks) >= 2 and " ".join(toks).endswith(" " + m["sur"]) and toks[0][0] in m["init"]]
    if len(byinit) == 1:  # a list that gives initials and a surname only (the Eerste Kamer)
        return byinit[0], "fuzzy"
    if len(toks) >= 2:
        # same words in another order, or extra given names: every word of the shorter name is in the longer
        c = [m for m in members if (lambda t: set(toks) <= set(t) or set(t) <= set(toks))(norm(m["name"]).split())
             and toks[-1] in norm(m["name"]).split()]
        if len(c) == 1:
            return c[0], "fuzzy"
        if strict:  # an adapter whose names carry two surnames (Spanish, Portuguese) leaves out the looser rule below
            return None, ""
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
    actors = actors_in if actors_in is not None else [x for x in db["actors"] if x["kind"] == "person" and (x["actor_type"] == "politician" or "politician" in (x.get("other_types") or "").split(";"))]
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
            m, how = match(x, *pool, strict=c.get("strict", False), deny={norm(d) for d in c.get("fuzzy_deny", ())})
            if m:
                if c.get("enrich"):
                    m = c["enrich"](m)
                if how == "fuzzy":
                    report.append(f"{x['actor_id']} {x['name']}: matched to {m['name']} ({m['party']}) by name only: confirm it is the same person")
                old = [prev for prev in db["positions"] if prev["actor_id"] == x["actor_id"] and prev["body_id"] == bid]
                old = next((prev for prev in old if prev["current"] == "y"), old[0] if old else {})  # what the register already holds for this seat
                if not old.get("start"):  # the body may have been renamed or re-created: keep the start the register had for this person's current seat
                    old = dict(old, start=next((prev["start"] for prev in db["positions"] if prev["actor_id"] == x["actor_id"] and prev["current"] == "y" and prev["start"]), ""))
                positions.append(dict(position_id="", actor_id=x["actor_id"], body_id=bid, role=c["role"],
                                      party=(old.get("party") if c.get("keep_party") and old.get("party") else m["party"]),  # a list with no party column keeps the register's
                                      geo_unit_id=x["geo_unit_id"], start=m.get("start") or old.get("start", ""), end="", current="y",
                                      member_ref=str(m.get("ref") or old.get("member_ref", "")), checked=today, source_url=m.get("url") or c["source_url"]))
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
            existing_pos = next((prev for prev in db["positions"] if prev["actor_id"] == x["actor_id"] and prev["body_id"] == bid), None)
            party_val = (f or {}).get("party") or (existing_pos.get("party") if existing_pos else "")
            start_val = (f or {}).get("start") or (existing_pos.get("start") if existing_pos else "")
            end_val = (f or {}).get("end") or (existing_pos.get("end") if existing_pos else "")
            ref_val = str((f or {}).get("ref") or (existing_pos.get("member_ref") if existing_pos else ""))
            url_val = (f or {}).get("url") or (existing_pos.get("source_url") if existing_pos else "") or c["source_url"]
            positions.append(dict(position_id="", actor_id=x["actor_id"], body_id=bid, role=c["role"], party=party_val,
                                  geo_unit_id=x["geo_unit_id"], start=start_val, end=end_val,
                                  current="n", member_ref=ref_val, checked=today,
                                  source_url=url_val))
            if x["status"] == "active":  # someone already marked as a former member needs no attention
                report.append(f"{x['actor_id']} {x['name']}: role {x['role'][:60]!r} but not on today's {c['name']} list"
                              f" ({'former member found, left ' + (f.get('end') or '?') if f else 'not found at all: check the spelling'})"
                              f"{' [status=active]' if x['status'] == 'active' else ''}")
    replaced = {b["body_id"] for b in db["bodies"] if b["name"] in names}
    sitting_now = {(o["actor_id"], o["body_id"]) for o in positions if o["current"] == "y"}
    have_any = {(o["actor_id"], o["body_id"]) for o in positions}
    for o in db["positions"]:  # an earlier term of someone who sits now, or a former seat the list does not cover (a minister's seat): keep it
        k = (o["actor_id"], o["body_id"])
        if o["body_id"] in replaced and o["current"] != "y" and (k in sitting_now or k not in have_any):
            positions.append(dict(o))
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


def austria():
    """Nationalrat (183 seats): parlament.gv.at open data JSON API."""
    url = "https://www.parlament.gv.at/Filter/api/json/post?jsMode=EVAL&FBEZ=WFW_002&listeId=undefined&showAll=true&export=true"
    body = json.dumps({"STEP": ["1000"], "NRBR": ["NR"], "GP": ["AKT"], "R_WF": ["FR"], "R_PBW": ["WK"], "M": ["M"], "W": ["W"]}).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"})
    data = json.loads(urllib.request.urlopen(req, timeout=30).read().decode("utf-8"))
    rows = data.get("rows", [])
    members = []
    PARTY_MAP = {"FPÖ": "FPÖ", "ÖVP": "ÖVP", "SPÖ": "SPÖ", "NEOS": "NEOS", "GRÜNE": "Grüne", "OK": "Ohne Klub"}
    for r in rows:
        html_info = r[6]
        vorname = re.search(r"Vorname:\s*([^\n<]+)", html_info)
        nachname = re.search(r"Nachname:\s*([^\n<]+)", html_info)
        v = vorname.group(1).strip() if vorname else ""
        n = nachname.group(1).strip() if nachname else ""
        name = f"{v} {n}".strip() if v and n else r[0]
        raw_party = r[9]
        party = PARTY_MAP.get(raw_party, raw_party)
        ref = r[7].split("/")[-1] if r[7] else ""
        bland = re.search(r"Bundesland:\s*([^\n<]+)", html_info)
        place = bland.group(1).strip() if bland else ""
        members.append(dict(name=name, party=party, ref=ref, place=place, url="https://www.parlament.gv.at" + (r[7] or "")))
    order = ["SPÖ", "Grüne", "NEOS", "Ohne Klub", "ÖVP", "FPÖ"]
    return [dict(name="Nationalrat", level="national", seats=183, source_url="https://www.parlament.gv.at/recherchieren/personen/nationalrat",
                 note="183 seats (28th legislative period, elected 29 September 2024). Sitting members and parties from the official Austrian Parliament JSON API.",
                 role="Abgeordnete/r zum Nationalrat", role_re=r"(?i)nationalrat|\babgeordnete[rn]? zum nationalrat\b|\bNR-Abgeordnete[rn]?\b", role_start=r"(?i)(nationalrat|abgeordnete[rn]? zum nationalrat)",
                 members=members, former=[], party_order=order,
                 colours={"SPÖ": "e30613", "Grüne": "88b62a", "NEOS": "e84188", "Ohne Klub": "888888", "ÖVP": "63c3d0", "FPÖ": "0056a2"})]


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
                 role="Member of the Sejm", role_re=r"(?i)sejm|member of the polish parliament|poseł|\bmp\b", role_start=r"(?i)member of the (polish )?(sejm|parliament)",
                 members=cur, former=former,
                 party_order=["Razem", "Lewica", "KO", "Demokracja", "Polska2050", "PSL-TD", "Centrum", "RozwojPlus", "niez.", "Konfederacja", "PiS"],
                 colours={"Razem": "80184b", "KO": "f68f2f", "PiS": "263778", "Lewica": "d4005a", "PSL-TD": "3ba935", "Polska2050": "ffd500", "Konfederacja": "5b6aa3",
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
        # Since November 2026 the endpoint answers scripts when the page's own query is sent: every sitting member in one page
        rs = get("https://sansad.in/api_rs/member/sitting-members?state=&party=&gender=&page=1&size=300&mpFlag=1&locale=en")
    except SystemExit:
        print("  (Rajya Sabha skipped: sansad.in refuses scripts for it; pass its summary with --local, see the India guide)", file=sys.stderr)
        return out
    if "records" in rs:  # names read "Sen, Shri Santanu" or "Wilson, Shri P.": surname, title, given names
        def rs_name(n):
            sur, _, rest = n.partition(",")
            given = [w for w in rest.split() if w.rstrip(".").lower() not in ("shri", "smt", "dr", "ms", "mr", "prof", "kumari", "sushri", "justice", "adv")]
            return " ".join(given + [sur.strip()]).strip()
        named = [dict(name=rs_name(x["name"]), party=x.get("partyCode") or x.get("party") or "IND", ref=str(x["mpsno"]),
                      place=(x.get("state") or "").strip(), start="", url=f"https://sansad.in/rs/members/biography/{x['mpsno']}")
                 for x in rs["records"]]
        filler = []
    else:  # the older summary file passed with --local: {total, counts, named}
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
             "無": "Independent", "無所属": "Independent", "みんな": "Your Party", "社民": "SDP", "有志": "Yushi",
             # Diet groups (会派) whose abbreviations the two Houses print; the English names follow the party or group's own usage
             "中道": "Centrist Reform Alliance", "みらい": "Team Mirai", "みら": "Team Mirai", "志士": "Shishi no Kai", "民主": "DPP",
             "い党": "Inochi no To", "沖縄": "Okinawa no Kaze", "保守": "Conservative Party of Japan", "碧水": "Hekisui-kai"}

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
                 party_order=["JCP", "Reiwa", "CDP", "Centrist Reform Alliance", "SDP", "Okinawa no Kaze", "Inochi no To", "Shishi no Kai", "DPP", "Team Mirai", "Komeito", "Independent", "Hekisui-kai", "Ishin", "LDP", "Sanseito", "Conservative Party of Japan"],
                 colours={"LDP": "d7263d", "CDP": "1d4ea1", "Ishin": "33a02c", "DPP": "f9a602", "Komeito": "f55881", "JCP": "d90000", "Reiwa": "ed6d9c", "Sanseito": "e6a000",
                          "Centrist Reform Alliance": "2a9d8f", "Team Mirai": "4fc3c9", "Shishi no Kai": "8e6bbf", "SDP": "2e7d32", "Inochi no To": "b5651d",
                          "Okinawa no Kaze": "0e7c7b", "Conservative Party of Japan": "6d5acf", "Hekisui-kai": "9aa0a6", "Independent": "8a8680"}),
            dict(name="House of Councillors (Sangiin)", seats=248, source_url=url, note=f"248 seats; the member list of the {session}th Diet session. Groups as named on the House's list.",
                 role="Member of the House of Councillors", role_re=r"(?i)house of councillors", role_start=r"(?i)member of the house of councillors", members=sen,
                 party_order=["JCP", "Reiwa", "CDP", "Centrist Reform Alliance", "SDP", "Okinawa no Kaze", "Inochi no To", "Shishi no Kai", "DPP", "Team Mirai", "Komeito", "Independent", "Hekisui-kai", "Ishin", "LDP", "Sanseito", "Conservative Party of Japan"],
                 colours={"LDP": "d7263d", "CDP": "1d4ea1", "Ishin": "33a02c", "DPP": "f9a602", "Komeito": "f55881", "JCP": "d90000", "Reiwa": "ed6d9c", "Sanseito": "e6a000",
                          "Centrist Reform Alliance": "2a9d8f", "Team Mirai": "4fc3c9", "Shishi no Kai": "8e6bbf", "SDP": "2e7d32", "Inochi no To": "b5651d",
                          "Okinawa no Kaze": "0e7c7b", "Conservative Party of Japan": "6d5acf", "Hekisui-kai": "9aa0a6", "Independent": "8a8680"})]


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


def colombia():
    """The Cámara de Representantes (183 seats, 2026-2030) from the chamber's own page (camara.gov.co/representantes, a JSON object of members by
    department with their party), and the Senado de la República (103 seats) from the Senate's own page (senado.gov.co/index.php/el-senado/senadores; names are listed
    surname first and the page repeats some entries). A seat the source does not name is shown as Vacant."""
    import html
    PARTY = {"Partido Pacto Histórico": "Pacto Histórico", "Coalición Pacto Histórico": "Pacto Histórico", "Partido Liberal Colombiano": "Partido Liberal",
             "Partido Conservador Colombiano": "Partido Conservador", "Partido Alianza Verde": "Alianza Verde", "Partido Demócrata Colombiano": "Partido Demócrata",
             "Partido Alianza Social Independiente – ASI": "ASI", "Partido Nuevo Liberalismo": "Nuevo Liberalismo", "Partido Colombia Renaciente": "Colombia Renaciente"}
    page = get("https://www.camara.gov.co/representantes", as_json=False).decode("utf-8", "ignore")
    i = re.search(r'\{"[A-ZÁÉÍÓÚÑ ]+":\[\{"Nombre"', page)
    if not i:
        sys.exit("Colombia: the Cámara page has no member data any more, check the adapter")
    depth, j = 0, i.start()
    for j in range(i.start(), len(page)):
        depth += (page[j] == "{") - (page[j] == "}")
        if depth == 0:
            break
    data = json.loads(page[i.start():j + 1])
    deputies = []
    for place, lst in data.items():
        for x in lst:
            p = (x.get("Partido") or "").strip()
            deputies.append(dict(name=x["Nombre"].strip(), party=PARTY.get(p, re.sub(r"^Partido ", "", p)) or "Sin partido", ref=re.sub(r"\W+", "-", x["Nombre"].lower()),
                                 place=place.title(), start="", url=(x.get("Perfil") or "https://www.camara.gov.co/representantes")))
    SP = {"Coalición Pacto Histórico - Polo Democrático": "Pacto Histórico", "Colombia Humana - Pacto Histórico": "Pacto Histórico", "Coalición Pacto Histórico - Colombia Humana": "Pacto Histórico",
          "Polo Democrático Alternativo": "Pacto Histórico", "Coalición Cambio Radical / ALMA": "Cambio Radical", "Alianza Verdes": "Alianza Verde", "Coalición Alianza Verdes / En Marcha": "Alianza Verde",
          "Alianza por Colombia / En Marcha": "Alianza Verde", "Partido Alianza Social Independiente – ASI": "ASI", "Movimiento Alternativo Indígena y Social MAIS": "MAIS"}
    sen_url = "https://www.senado.gov.co/index.php/el-senado/senadores"
    senators, seen = [], set()
    for m in re.finditer(r'<div class="modazdirectory__result[^"]*">(.*?)<!-- /modazdirectory__result', get(sen_url, as_json=False).decode("utf-8", "ignore"), flags=re.S):
        h = re.search(r"<h3>(.*?)</h3>", m[1], flags=re.S)
        ps = [html.unescape(re.sub(r"<[^>]+>", "", q)).strip() for q in re.findall(r"<p>(.*?)</p>", m[1], flags=re.S)]
        if not h or not ps or not ps[0]:
            continue
        name = re.sub(r"\s+", " ", html.unescape(h[1])).strip()  # "Surname Given", as the Senate lists it
        if name in seen:  # the page repeats some entries
            continue
        seen.add(name)
        senators.append(dict(name=name, party=SP.get(ps[0], ps[0]), ref=re.sub(r"\W+", "-", name.lower()), place="", start="", url=sen_url))
    if len(senators) < 90 or len(deputies) < 150:
        sys.exit(f"Colombia: read {len(deputies)} representatives and {len(senators)} senators, check the adapter")
    colours = {"Pacto Histórico": "7a1f5c", "Centro Democrático": "1c8fd6", "Partido Liberal": "e11931", "Partido Conservador": "1a4a9c", "Partido de la U": "f2c230",
               "Cambio Radical y Alma": "e07a1f", "Alianza Verde": "62b04b", "Ahora Colombia": "2aa5c9", "Movimiento Salvación Nacional": "6b6b6b"}

    def chamber(name, seats, members, role, rre, note, src):
        count = {}
        for m in members:
            count[m["party"]] = count.get(m["party"], 0) + 1
        order = sorted(count, key=lambda p: -count[p])
        return dict(name=name, level="national", seats=seats, source_url=src, note=note, role=role, role_re=rre, role_start=rre, members=members, former=[],
                    party_order=order, colours={p: colours.get(p, "8a8680") for p in order}, strict=True,
                    fuzzy_deny=("Miguel Ángel Pinto",))
    return [chamber("Senado de la República", 103, senators, "Senator", r"(?i)senator|senador",
                    "103 seats for 2026-2030: 102 elected on 8 March 2026 and one for the runner-up of the presidential election if in opposition. Who sits and their party are from the Senate's own list of senators (surname first); parties are the lists they were elected on, grouped (Pacto Histórico with its coalition partners). Seats the page does not name are shown as Vacant. Unlit seats mean nothing found, never opposition.",
                    sen_url),
            chamber("Cámara de Representantes", 183, deputies, "Representative", r"(?i)representative|representante",
                    "183 seats for 2026-2030. Who sits and their party are from the chamber's own page (camara.gov.co/representantes); seats the page does not name are shown as Vacant. Unlit seats mean nothing found, never opposition.",
                    "https://www.camara.gov.co/representantes")]
# ---------------------------------------------------------------- Latin America (Chile, Uruguay, Ecuador, Paraguay, Peru, Bolivia, Costa Rica)
_PALETTE = ["6aa4d8", "f2c230", "8b1a1a", "1f8f4e", "e07a1f", "2aa5c9", "c9a227", "9a6fb0", "62b04b", "d36b8f", "4a6fa5", "b5651d"]


def _latam(name, seats, source_url, note, role, rre, members, colours=None, strict=True, vacant=None, fuzzy_deny=(), former=()):
    """One chamber of a Latin American legislature: parties ordered by size, colours from a palette unless given."""
    count = {}
    for m in members:
        count[m["party"]] = count.get(m["party"], 0) + 1
    order = sorted(count, key=lambda p: (p in ("Independiente", "Other parties", "Sin partido"), -count[p]))
    colours = dict(colours or {})
    free = [c for c in _PALETTE if c not in colours.values()]
    for p in order:
        if p not in colours:
            colours[p] = free.pop(0) if free else "8a8680"
    d = _upper(name, seats, source_url, note, role, rre, members, colours, order=order, vacant=vacant, strict=strict)
    if fuzzy_deny:
        d["fuzzy_deny"] = fuzzy_deny
    d["former"] = list(former)
    return d


def _flip(n):
    """'Rodríguez González, Blanca' -> 'Blanca Rodríguez González'; a name without a comma is kept."""
    a, sep, b = n.partition(",")
    return re.sub(r"\s+", " ", f"{b} {a}" if sep else a).strip()


def _cl_party(p):
    """One spelling for a Chilean party across the Chamber's feed and the Wikipedia list."""
    p = re.sub(r" de Chile$", "", p.strip()).replace("Partido Por la", "Partido por la")
    return {"Partido Demócratas Chile": "Demócratas", "Partido Acción Humanista": "Acción Humanista"}.get(p, p)


def chile():
    """Cámara de Diputadas y Diputados (155 seats): the Chamber's own web service (opendata.camara.cl, retornarDiputadosPeriodoActual: the deputies of the
    current period and their party memberships; the feed gives no district). Senado (50 seats): senado.cl sits behind a Cloudflare check that is not bypassed and
    the Senate's web service (tramitacion.senado.cl/wspublico/senadores_vigentes.php) still lists only the 2022 cohort, so the Senate is read from the Spanish
    Wikipedia list of current senators (Anexo:Senadores actuales de la República de Chile), a secondary source: the note says so."""
    import xml.etree.ElementTree as ET
    ns = {"n": "http://opendata.camara.cl/camaradiputados/v1"}
    url = "https://opendata.camara.cl/camaradiputados/WServices/WSDiputado.asmx/retornarDiputadosPeriodoActual"
    root = ET.fromstring(get(url, as_json=False))
    today = dt.date.today().isoformat()
    deputies = []
    for dp in root.findall("n:DiputadoPeriodo", ns):
        d = dp.find("n:Diputado", ns)

        def t(tag):
            return (d.findtext(f"n:{tag}", default="", namespaces=ns) or "").strip()
        militancias = []
        for m in d.findall("n:Militancias/n:Militancia", ns):
            militancias.append(((m.findtext("n:FechaInicio", "", ns) or "")[:10], (m.findtext("n:FechaTermino", "", ns) or "9999")[:10], m.findtext("n:Partido/n:Nombre", "", ns).strip()))
        cur = [m for m in militancias if m[0] <= today <= m[1]] or sorted(militancias)[-1:]
        party = cur[0][2] if cur else "Independiente"
        party = "Independiente" if party.startswith("Independiente") else _cl_party(party)
        name = " ".join(x for x in (t("Nombre"), t("Nombre2"), t("ApellidoPaterno"), t("ApellidoMaterno")) if x)
        # the feed's own FechaInicio is the end of the period (2030), so the start is not taken from it: the period began on 11 March 2026
        deputies.append(dict(name=name, party=party, ref=t("Id"), place="", start="2026-03-11", url=f"https://www.camara.cl/diputados/detalle/biografia.aspx?prmId={t('Id')}"))
    # deputies of the three previous periods who do not sit now (the feed gives no end date for a person, so the period's end is used)
    sitting, former = {d["ref"] for d in deputies}, {}
    for pid, (pstart, pend) in ((10, ("2022-03-11", "2026-03-10")), (9, ("2018-03-11", "2022-03-10")), (8, ("2014-03-11", "2018-03-10"))):
        try:
            prev = ET.fromstring(get(f"https://opendata.camara.cl/camaradiputados/WServices/WSDiputado.asmx/retornarDiputadosXPeriodo?prmPeriodoId={pid}", as_json=False))
        except SystemExit:
            continue
        for dp in prev.findall("n:DiputadoPeriodo", ns):
            d = dp.find("n:Diputado", ns)
            if d is None:
                continue
            ref = (d.findtext("n:Id", "", ns) or "").strip()
            if ref in sitting or ref in former:
                continue
            nm = " ".join(x for x in ((d.findtext(f"n:{t}", "", ns) or "").strip() for t in ("Nombre", "Nombre2", "ApellidoPaterno", "ApellidoMaterno")) if x)
            ms = sorted(((m.findtext("n:FechaInicio", "", ns) or "")[:10], m.findtext("n:Partido/n:Nombre", "", ns).strip()) for m in d.findall("n:Militancias/n:Militancia", ns))
            former[ref] = dict(name=nm, party=(ms[-1][1] if ms else ""), ref=ref, start=pstart, end=pend, url=f"https://www.camara.cl/diputados/detalle/biografia.aspx?prmId={ref}")
    if len(deputies) < 140:
        sys.exit(f"Chile: read {len(deputies)} deputies, expected 155; check the adapter")
    wurl = "https://es.wikipedia.org/wiki/Anexo:Senadores_actuales_de_la_Rep%C3%BAblica_de_Chile"
    tables = wiki_tables(wiki_page("es", "Anexo:Senadores actuales de la República de Chile"))
    tbl = next(t for t in tables if t and "Senador" in t[0])
    months = {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12}
    senators, region = [], ""
    for r in tbl[1:]:
        i = next((k for k, c in enumerate(r) if re.search(r"\(n\.? ?\d{4}\)", c)), None)
        if i is None:
            continue
        if i >= 2 and r[0]:
            region = r[0]
        nm = re.sub(r"\(n\.? ?\d{4}\)", "", r[i]).strip()
        party = r[i + 1].split(",")[0].strip()
        party = "Independiente" if party.startswith("Independiente") else _cl_party(party)
        dates = [c for c in r[i + 2:] if re.search(r"\d{4}", c)]
        end = dates[-1] if len(dates) > 1 else ""
        if re.search(r"desafuer|renunci|falleci|destituc", end.lower()):
            continue  # a seat left empty during the term
        sm = re.match(r"(\d+) de (\w+) de (\d{4})", dates[0]) if dates else None
        start = f"{sm[3]}-{months[sm[2]]:02d}-{int(sm[1]):02d}" if sm else ""
        senators.append(dict(name=nm, party=party, ref=re.sub(r"\W+", "-", norm(nm)), place=region, start=start, url=wurl))
    if len(senators) < 45:
        sys.exit(f"Chile: read {len(senators)} senators from the Wikipedia list, expected 49 or 50; check the adapter")
    tail = " Unlit seats mean nothing found, never opposition."
    return [_latam("Cámara de Diputadas y Diputados", 155, url, "155 seats, 2026-2030. Who sits and their party are from the Chamber's own web service for the current period (opendata.camara.cl); independents are shown together." + tail,
                   "Deputy", r"(?i)\bdeputy\b|diputad", deputies, fuzzy_deny=("Daniel Núñez",), former=former.values()),  # the feed's independent of that name is not the PC senator of Coquimbo, whom the Senate lists
            _latam("Senado de la República", 50, wurl, "50 seats. The Senate's own site (senado.cl) is behind a Cloudflare check and its web service lists only the 2022 cohort, so who sits and their party are from the Spanish Wikipedia list of current senators, a secondary source kept by editors; a seat left empty (a senator removed from office) shows as Vacant." + tail,
                   "Senator", r"(?i)\bsenator|senador", senators)]


def uruguay():
    """Senado (30 senators; the Vice President, who presides, is the 31st member and is not counted) and Cámara de Representantes (99): the Parlamento's own
    "Integración" lists (Actuantes: the members who sit today, a substitute counting for the titular they replace). parlamento.gub.uy refuses scripts (CloudFront 403),
    so each list is read once in a browser from .../plenario/integracion/json and passed with --local (see the Uruguay guide)."""
    PARTY = {"PARTIDO FRENTE AMPLIO": "Frente Amplio", "PARTIDO NACIONAL": "Partido Nacional", "PARTIDO COLORADO": "Partido Colorado", "PARTIDO CABILDO ABIERTO": "Cabildo Abierto",
             "PARTIDO IDENTIDAD SOBERANA": "Identidad Soberana", "PARTIDO INDEPENDIENTE": "Partido Independiente"}

    def read(chamber, presiding_counts):
        url = f"https://parlamento.gub.uy/camarasycomisiones/{chamber}/plenario/integracion/json"
        out = []
        for x in get(url):
            if x.get("Cargo") and not presiding_counts:
                continue  # the presiding Vice President (or the senator standing in for them) is not one of the 30 senators
            lema = re.sub(r"\s+", " ", x["Lema"]).strip()
            nm = _flip(x["Nombres"])
            out.append(dict(name=nm, party=PARTY.get(lema, lema.title()), ref=re.sub(r"\W+", "-", norm(nm)), place="", start="", url=f"https://parlamento.gub.uy/camarasycomisiones/{chamber}/plenario/integracion"))
        return out
    senators, deputies = read("senadores", False), read("representantes", True)
    if len(senators) != 30 or len(deputies) != 99:
        sys.exit(f"Uruguay: read {len(senators)} senators and {len(deputies)} representatives, expected 30 and 99; save the lists again (see the Uruguay guide)")
    tail = " Who sits and their party are from the Parlamento's own list of the members acting today (a substitute counts in their party). Unlit seats mean nothing found, never opposition."
    return [_latam("Senado de la República", 30, "https://parlamento.gub.uy/camarasycomisiones/senadores/plenario/integracion", "30 senators elected nationwide; the Vice President presides and is not counted." + tail, "Senator", r"(?i)\bsenator|senador", senators),
            _latam("Cámara de Representantes", 99, "https://parlamento.gub.uy/camarasycomisiones/representantes/plenario/integracion", "99 representatives elected by department." + tail, "Deputy", r"(?i)\bdeputy|representante|diputad", deputies)]


def ecuador():
    """Asamblea Nacional (151 seats): the plenary page of asambleanacional.gob.ec (one pin per asambleísta: name, province or national list, a blog link; the
    party is the icon the page draws, ADN, Revolución Ciudadana, Pachakutik or PSC; other parties get a generic icon and are grouped)."""
    import html
    url = "https://www.asambleanacional.gob.ec/es/pleno-asambleistas"
    x = get(url, as_json=False).decode("utf-8", "replace")
    ICON = {"adn": "ADN", "revolucion-ciudadana": "Revolución Ciudadana", "pachakutik": "Pachakutik", "psc": "PSC"}
    members = []
    for p in re.split(r'<div\s+class="icon-asambleitas-partido"', x)[1:]:
        ic = re.search(r"(?:public/)?([\w-]+)\.(?:png|jpg|gif)", p)
        n = re.search(r"<strong>([^<]+)<br />\s*<em>([^<]+)</em>", p)
        blog = re.search(r'href="(blogs/[^"]+)"', p)
        if not n:
            continue
        party = next((v for k, v in ICON.items() if ic and k in ic[1]), "Other parties")
        place = re.sub(r"(?i)^asamble[ií]sta\s+(por\s+(la\s+provincia\s+de(l)?\s+|el\s+)?)?", "", html.unescape(n[2])).strip()
        nm = re.sub(r"\s+", " ", html.unescape(n[1])).strip()
        members.append(dict(name=nm, party=party, ref=(blog[1].split("/")[-1] if blog else re.sub(r"\W+", "-", nm.lower())), place=place or "Nacional",
                            start="", url=("https://www.asambleanacional.gob.ec/es/" + blog[1]) if blog else url))
    if len(members) != 151:
        sys.exit(f"Ecuador: read {len(members)} asambleístas, expected 151; check the adapter")
    return [_latam("Asamblea Nacional", 151, url, "151 seats, 2025-2029. Who sits is the Assembly's own plenary page; the party is the icon the page shows next to each member (ADN, Revolución Ciudadana, Pachakutik, PSC; a generic icon for the other parties, which are grouped as Other parties). Unlit seats mean nothing found, never opposition.",
                   "Asambleísta", r"(?i)asamble[ií]sta|assembly", members, colours={"ADN": "f2c230", "Revolución Ciudadana": "e11931", "Pachakutik": "7a1f5c", "PSC": "1a4a9c", "Other parties": "8a8680"})]


def paraguay():
    """Cámara de Senadores (45) from senado.gov.py (the list of senators by party and movement; each links to the Congress's SILpy record) and Cámara de
    Diputados (80) from diputados.gov.py (the alphabetical list: name, party or alliance code)."""
    import html
    SP = {"Asociación Nacional Republicana ANR": "ANR", "Partido Liberal Radical Auténtico PLRA": "PLRA", "Partido Cruzada Nacional": "Cruzada Nacional",
          "Movimiento Conciencia Democrática Nacional": "Conciencia Democrática Nacional", "Partido Democrático Progresista PDP": "Partido Democrático Progresista",
          "Partido Encuentro Nacional PEN": "Encuentro Nacional", "Independiente A": "Independiente", "Partido Participación Ciudadana": "Participación Ciudadana"}
    surl = "https://www.senado.gov.py/index.php/menu-senadores/sub-menu-nomina-por-partido-movimiento.html"
    x = get(surl, as_json=False).decode("utf-8", "replace")
    party, senators = None, []
    for m in re.finditer(r'<div class="fs-2 fw-bold">\s*(.*?)\s*<i class|href="https://silpy\.congreso\.gov\.py/legislador/(\d+)"[^>]*>([^<]+)</a>', x, flags=re.S):
        if m[1]:
            party = html.unescape(m[1]).strip()
        else:
            senators.append(dict(name=_flip(html.unescape(m[3]).strip()), party=SP.get(party, party), ref=m[2], place="", start="", url=f"https://silpy.congreso.gov.py/legislador/{m[2]}"))
    durl = "https://diputados.gov.py/diputados/nomina-alfabetica"
    x = get(durl, as_json=False).decode("utf-8", "replace")
    CODE = {"ANR": "ANR", "PLRA": "PLRA", "PCN": "Cruzada Nacional", "AEN": "Encuentro Nacional", "CDN": "Conciencia Democrática Nacional", "PPQ": "Patria Querida",
            "APLP": "Alianza Patria", "CN2023": "Concertación", "ATJPÑ": "Concertación", "APUNP": "Concertación", "APUNG": "Concertación", "AC": "Concertación", "APAD": "Concertación"}

    def tx(s):
        return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()
    deputies = []
    for r in re.findall(r"<tr[^>]*>(.*?)</tr>", x, flags=re.S)[1:]:
        tds = re.findall(r"<td[^>]*>(.*?)</td>", r, flags=re.S)
        if len(tds) < 3:
            continue
        a = re.search(r"parlamentario/(\d+)", r)
        nm = tx(tds[1]).title()
        code = tx(tds[2])
        deputies.append(dict(name=nm, party=CODE.get(code, code or "Sin partido"), ref=a[1] if a else re.sub(r"\W+", "-", nm.lower()), place="", start="",
                             url=f"https://silpy.congreso.gov.py/parlamentario/{a[1]}" if a else durl))
    if len(senators) != 45 or len(deputies) != 80:
        sys.exit(f"Paraguay: read {len(senators)} senators and {len(deputies)} deputies, expected 45 and 80; check the adapter")
    return [_latam("Cámara de Senadores", 45, surl, "45 seats, one nationwide constituency. Who sits and their party or movement are from the Senate's own list of senators by party and movement. Unlit seats mean nothing found, never opposition.",
                   "Senador de la Nación", r"(?i)senador|senator", senators),
            _latam("Cámara de Diputados", 80, durl, "80 seats elected by department. Who sits is the Chamber's own alphabetical list, which gives each deputy a party or alliance code: codes of the departmental alliances of the 2023 election (CN2023, APUNP, APUNG, ATJPÑ, AC, APAD) are grouped as Concertación. Unlit seats mean nothing found, never opposition.",
                   "Diputado Nacional", r"(?i)diputad|deputy", deputies)]


def peru():
    """Senado (60) and Cámara de Diputados (130), 2026-2031: each chamber's own roster page embeds a JSON array (the data-congresista-dataset attribute of a script
    element): name (surname first), parliamentary group, district. Entries with no condition are kept, as the rosters list them."""
    import html

    def read(url):
        x = get(url, as_json=False).decode("utf-8", "replace")
        m = re.search(r"data-congresista-dataset[^>]*>(.*?)</script>", x, flags=re.S)
        if not m:
            sys.exit(f"Peru: no roster data in {url} any more, check the adapter")
        return [dict(name=_flip(r["name"]), party=(r.get("group") or r.get("partido") or "Sin partido").strip(), ref=r["url"].rstrip("/").split("/")[-1],
                     place=r.get("district", ""), start="2026", url=r["url"]) for r in json.loads(html.unescape(m[1]))]
    surl, durl = "https://senado.congreso.gob.pe/senador/", "https://diputados.congreso.gob.pe/diputado/"
    senators, deputies = read(surl), read(durl)
    if len(senators) != 60 or len(deputies) != 130:
        sys.exit(f"Peru: read {len(senators)} senators and {len(deputies)} deputies, expected 60 and 130; check the adapter")
    tail = " Who sits and their parliamentary group are from the chamber's own roster page (a few entries carry no condition field). Unlit seats mean nothing found, never opposition."
    return [_latam("Senado de la República", 60, surl, "60 seats, 2026-2031." + tail, "Senator", r"(?i)\bsenator|senador", senators),
            _latam("Cámara de Diputados", 130, durl, "130 seats, 2026-2031." + tail, "Deputy", r"(?i)\bdeputy|diputad", deputies)]


def _bo_party(p):
    return {"UNIDAD": "Unidad", "APB-SÚMATE": "APB Súmate", "APB-SUMATE": "APB Súmate", "MAS-IPSP": "MAS-IPSP", "BIA-YUQUI": "Bia-Yuqui"}.get(p.strip().upper(), p.strip())


def bolivia():
    """Cámara de Senadores (36) from the Senate's own site API (apisi.senado.gob.bo/page/senadores/pleno: 72 entries, 36 titulares and 36 suplentes, the
    party seats counted among the titulares) and Cámara de Diputados (130) from diputados.gob.bo: the site's WordPress API lists the 255 titulares and
    suplentes; the page does not say which is which, but each photo file is named with a department and TI/SU (a few say TITU, SUPLE or nothing), so
    whoever is not marked suplente is a titular (130, as the Chamber has), and the party (bancada) is read from each titular's own page."""
    import html
    from concurrent.futures import ThreadPoolExecutor
    sen = []
    for x in get("https://apisi.senado.gob.bo/page/senadores/pleno")["data"]:
        if x.get("titular_id") is not None:
            continue  # a suplente carries the id of their titular
        nm = " ".join(f"{x['nombre']} {x['apellidos']}".title().split())
        sen.append(dict(name=nm, party=_bo_party((x.get("bancada") or {}).get("sigla") or "Sin partido"), ref=str(x["id"]), place=(x.get("brigada_catalogo") or {}).get("name", ""), start="", url="https://www.senado.gob.bo/"))
    base = "https://diputados.gob.bo/wp-json/wp/v2/"
    recs = []
    for pg in (1, 2, 3):
        recs += get(f"{base}diputados?per_page=100&page={pg}&_fields=id,slug,title,link,acf")
    media = {}
    ids = [str(r["acf"]["foto"]) for r in recs if r["acf"].get("foto")]
    for k in range(0, len(ids), 100):
        for m in get(f"{base}media?per_page=100&_fields=id,source_url&include={','.join(ids[k:k + 100])}"):
            media[m["id"]] = m["source_url"]
    suple = re.compile(r"(?<![A-Z])(SU|SUP|SUPLE|SUPLENTE)(?![A-Z])")
    tit = [r for r in recs if not suple.search(media.get(r["acf"].get("foto"), "").rsplit("/", 1)[-1].upper())]
    PARTY = {"MAS IPSP": "MAS-IPSP", "APB SUMATE": "APB Súmate", "BIA-YUQUI": "Bia-Yuqui", "PDC": "PDC", "LIBRE": "LIBRE", "UNIDAD": "Unidad", "AP": "AP"}

    def page(r):
        t = get(r["link"], as_json=False, tries=3).decode("utf-8", "replace")
        t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
        t = re.sub(r"(\|\s*)+", "|", re.sub(r"<[^>]+>", "|", re.sub(r"\s+", " ", html.unescape(t))))
        b = re.search(r"Bancada \|([^|]*)", t)
        d = re.search(r"Brigada \|([^|]*)", t)
        sig = re.sub(r"\s*\(.*$", "", b[1]).strip() if b else ""
        return PARTY.get(sig, sig) or "Sin partido", (d[1].strip() if d else "")
    with ThreadPoolExecutor(8) as ex:
        info = list(ex.map(page, tit))
    dep = [dict(name=" ".join(html.unescape(r["title"]["rendered"]).split()), party=p, ref=r["slug"], place=pl, start="", url=r["link"]) for r, (p, pl) in zip(tit, info)]
    if len(sen) != 36 or len(dep) != 130:
        sys.exit(f"Bolivia: read {len(sen)} senators and {len(dep)} deputies, expected 36 and 130; check the adapter")
    return [_latam("Cámara de Diputados", 130, "https://diputados.gob.bo/diputados/", "130 seats, 2025-2030. The Chamber's own site lists 255 titulares and suplentes without saying which is which: the 130 titulares are those whose photo file is not marked suplente, and the party is the bancada on each titular's page. A suplente who has taken a titular's seat is not detected. Unlit seats mean nothing found, never opposition.",
                   "Deputy", r"(?i)\bdeputy|diputad", dep),
            _latam("Cámara de Senadores", 36, "https://www.senado.gob.bo/", "36 seats, 2025-2030. Who sits and their party are from the Senate's own site API: its 36 titulares by bancada (the 36 suplentes are not counted). Unlit seats mean nothing found, never opposition.",
                   "Senator", r"(?i)\bsenator|senador", sen)]


def costa_rica():
    """Asamblea Legislativa (57 seats), 2026-2030: asamblea.go.cr did not answer from here, so the 57 deputies (province and number on the list, party) are
    read from the Spanish Wikipedia list Anexo:Diputados del período legislativo 2026-2030 en Costa Rica, a secondary source; its party counts match the TSE declaratoria
    of 23 March 2026 (31 / 17 / 7 / 1 / 1)."""
    wurl = "https://es.wikipedia.org/wiki/Anexo:Diputados_del_per%C3%ADodo_legislativo_2026-2030_en_Costa_Rica"
    t = wiki_tables(wiki_page("es", "Anexo:Diputados del período legislativo 2026-2030 en Costa Rica"))[0]
    members = []
    for r in t[1:]:
        if len(r) < 4 or not re.search(r"\d", r[0]):
            continue
        party = re.sub(r"^Partido ", "", r[3]).strip()
        members.append(dict(name=r[2], party=party, ref=re.sub(r"\W+", "-", norm(r[2])), place=re.sub(r"\s*\d+$", "", r[0]), start="2026", url=wurl))
    if len(members) != 57:
        sys.exit(f"Costa Rica: read {len(members)} deputies from the Wikipedia list, expected 57; check the adapter")
    return [_latam("Asamblea Legislativa", 57, wurl, "57 seats elected by province, 2026-2030. The Assembly's own site (asamblea.go.cr) did not answer from the machine that built this, so who sits is read from the Spanish Wikipedia list of the 2026-2030 deputies, a secondary source kept by editors (its party counts match the TSE declaratoria of 23 March 2026: 31 / 17 / 7 / 1 / 1); replacements during the term may lag. Unlit seats mean nothing found, never opposition.",
                   "Deputy", r"(?i)\bdeputy|diputad", members)]


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


def south_korea():
    """The National Assembly (300 seats, 22nd Assembly): the member search of the Assembly's open-information portal (open.assembly.go.kr), the
    same list its public search page shows (299 members; a vacancy shows as Vacant). Ministers who keep their seat, as Korean law allows, are on it.
    Only the name, party and constituency are read: never the age, phone, e-mail or staff the service also returns. Each member's Hangul name is kept
    so that supporters are matched by the Hangul in their register name."""
    PARTY = {"더불어민주당": "Democratic Party of Korea", "국민의힘": "People Power Party", "조국혁신당": "Rebuilding Korea Party", "개혁신당": "Reform Party",
             "진보당": "Progressive Party", "기본소득당": "Basic Income Party", "사회민주당": "Social Democratic Party", "무소속": "Independent",
             "새로운미래": "New Future Party", "정의당": "Justice Party"}
    req = urllib.request.Request("https://open.assembly.go.kr/portal/assm/search/searchAssmMemberSch.do", data=b"rows=400&page=1",
                                 headers={**UA, "X-Requested-With": "XMLHttpRequest", "Referer": "https://open.assembly.go.kr/portal/assm/search/memberSchPage.do"})
    rows = json.loads(urllib.request.urlopen(req, timeout=120).read())["data"]
    members = [dict(name=f"{r['engNm'].title()} ({r['hgNm']})" if r.get("engNm") else r["hgNm"], cjk=r["hgNm"], party=PARTY.get(r["polyNm"], r["polyNm"]), ref=r["monaCd"],
                    place=r["origNm"], start="", url="https://open.assembly.go.kr/portal/assm/search/memberSchPage.do") for r in rows]
    if len(members) < 280:
        sys.exit(f"South Korea: read {len(members)} members, expected about 299; the service has changed, check the adapter")
    count = {}
    for m in members:
        count[m["party"]] = count.get(m["party"], 0) + 1
    order = sorted(count, key=lambda p: -count[p])
    colours = {"Democratic Party of Korea": "1a5fb4", "People Power Party": "e11931", "Rebuilding Korea Party": "1f8f4e", "Reform Party": "e07a1f",
               "Progressive Party": "bf1e2e", "Basic Income Party": "62b04b", "Social Democratic Party": "f2c230", "Independent": "8a8680"}
    return [dict(name="National Assembly", level="national", seats=300, source_url="https://open.assembly.go.kr/portal/assm/search/memberSchPage.do",
                 note="300 seats (254 by district and 46 by proportional representation), 22nd Assembly, elected 10 April 2024. Who sits and their party are from the Assembly's open-information portal (its member search); ministers who keep their seat are included, and a seat with no member is shown as Vacant. Unlit seats mean nothing found, never opposition.",
                 role="Member of the National Assembly", role_re=r"(?i)national assembly member|assemblyman|assemblywoman",
                 role_start=r"(?i)national assembly member", members=members, former=[], party_order=order,
                 colours={p: colours.get(p, "8a8680") for p in order},
                 fuzzy_deny=("Kim Jong-min",))]  # the 2020 Minjung Party candidate is not the sitting independent member of the same name


def netherlands_senate():
    """The Eerste Kamer (75 seats): eerstekamer.nl/alle_leden, the sitting members with their parliamentary group. The page gives initials and
    surname ("prof. dr. E.B. van Apeldoorn"), so each member carries `init` and `sur` and a supporter is matched on the surname and the first initial."""
    import html
    page = get("https://www.eerstekamer.nl/alle_leden", as_json=False).decode("utf-8", "ignore")
    DEGREE = re.compile(r"^(MA|MSc|MPA|LLM|BSc|MBA|BA|MPhil|PhD|MD|RA|EMPM|MSM|MHA|FD)$", re.I)
    PARTY = {"PRO": "GroenLinks-PvdA"}
    members = []
    for it in re.findall(r'<li class="persoon.*?</li>', page, flags=re.S):
        n = re.search(r'class="naam">(.*?)</div>', it, flags=re.S)
        grp = re.search(r'persoon_bijschrift"><div><div class="naam">.*?</div></div><div>(.*?)</div>', it, flags=re.S)
        ref = re.search(r'href="/persoon/([^"]+)"', it)
        if not (n and grp and ref):
            continue
        text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", n[1]))).strip()
        toks = [t for t in text.split() if not DEGREE.match(t)]
        while toks and re.match(r"^(prof|dr|drs|mr|ir|ing|dr\.|mr\.)\.?$|^(prof\.|dr\.|drs\.|mr\.|ir\.|ing\.)$", toks[0], re.I):
            toks.pop(0)
        ini = re.match(r"^((?:[A-Za-z]\.)+)\s*(.*)$", " ".join(toks))
        initials, sur = (ini[1], ini[2]) if ini else ("", " ".join(toks))
        party = re.sub(r"^Fractie-", "Fractie ", html.unescape(re.sub(r"<[^>]+>", "", grp[1])).strip())
        members.append(dict(name=f"{initials} {sur}".strip(), init=re.sub(r"[^a-z]", "", initials.lower()), sur=" ".join(norm(sur).split()), party=PARTY.get(party, party),
                            ref=ref[1], place="", start="", url="https://www.eerstekamer.nl/persoon/" + ref[1]))
    if len(members) != 75:
        sys.exit(f"Eerste Kamer: read {len(members)} members, expected 75; the page has changed, check the adapter")
    count = {}
    for m in members:
        count[m["party"]] = count.get(m["party"], 0) + 1
    order = sorted(count, key=lambda p: -count[p])
    return [dict(name="Eerste Kamer", level="national", seats=75, source_url="https://www.eerstekamer.nl/alle_leden",
                 note="75 seats, elected indirectly by the provincial councils in 2023. Who sits and their group are from the Senate's own list of members; a supporter is matched on surname and first initial because the list gives initials only. Unlit seats mean nothing found, never opposition.",
                 role="Senator (Eerste Kamer)", role_re=r"(?i)senator|eerste kamer|senaat", role_start=r"(?i)senator", members=members, former=[], party_order=order,
                 colours={"GroenLinks-PvdA": "c8102e", "BBB": "92b83a", "VVD": "f08a1c", "D66": "00a28b", "CDA": "1c7a3c", "PVV": "1a2a5a", "SP": "e11931", "FVD": "7a1f2b",
                          "ChristenUnie": "00a1de", "JA21": "123b6d", "Volt": "5a2d82", "PvdD": "006b3c", "SGP": "ff6a13"})]


def south_africa_ncop():
    """The National Council of Provinces (90 seats): the Parliamentary Monitoring Group's open API, members of house NCOP flagged as current
    (same source and name handling as the National Assembly)."""
    NAMES = {"MKP": "MK Party", "Action SA": "ActionSA", "FF+": "FF Plus", "PA": "Patriotic Alliance"}
    url, rows = "https://api.pmg.org.za/member/", []
    while url:
        d = get(url)
        rows += d["results"]
        url = d.get("next")
    members = []
    for m in rows:
        if not (m.get("current") and (m.get("house") or {}).get("name_short") == "NCOP"):
            continue
        slug = (m.get("pa_link") or "").rstrip("/").rsplit("/", 1)[-1]
        sur, _, rest = m["name"].partition(",")
        words = [w.capitalize() for w in slug.split("-")]
        if words and slug and words[-1].lower() != sur.strip().split()[-1].lower():
            words[-1] = sur.strip().split()[-1]
        name = " ".join(words) if slug else f"{rest.split()[-1]} {sur}"
        party = (m.get("party") or {}).get("name", "Independent")
        members.append(dict(name=name, party=NAMES.get(party, party), ref=m["id"], place=(m.get("province") or {}).get("name", ""),
                            start=m.get("start_date") or "", url=f"https://pmg.org.za/member/{m['id']}/"))
    count = {}
    for m in members:
        count[m["party"]] = count.get(m["party"], 0) + 1
    order = sorted(count, key=lambda p: -count[p])
    if len(members) < 40:
        sys.exit(f"NCOP: read {len(members)} members, expected about 54; the API has changed, check the adapter")
    return [dict(name="National Council of Provinces", level="national", seats=90, source_url="https://api.pmg.org.za/member/",
                 note="90 seats: ten for each province (six permanent delegates and four special delegates). The Parliamentary Monitoring Group's member list names the 54 permanent delegates; the 36 special delegates, who change with the provinces' business, are not listed and show as 'Special delegates (not listed)'. Unlit seats mean nothing found, never opposition.",
                 vacant_label="Special delegates (not listed)",
                 role="Member of the National Council of Provinces", role_re=r"(?i)national council of provinces|\bNCOP\b", role_start=r"(?i)member of the national council of provinces",
                 members=members, former=[], party_order=order,
                 colours={"ANC": "1a7f3c", "DA": "2d6fb5", "MK Party": "3a3a3a", "EFF": "c8102e", "IFP": "d6a21f", "Patriotic Alliance": "7a5ab3", "ActionSA": "e07b39", "FF Plus": "8a6d3b"})]


def canada_senate():
    """The Senate of Canada (105 seats): the list sencanada.ca's own senators page loads (umbraco/surface/SenatorsAjax/GetSenators), senators in
    office with their group and province; vacant seats are shown as Vacant."""
    import html
    GROUP = {"ISG": "Independent Senators Group", "PSG": "Progressive Senate Group", "CSG": "Canadian Senators Group", "C": "Conservative",
             "GRO": "Government Representative Office", "Non-affiliated": "Non-affiliated"}
    page = get("https://sencanada.ca/umbraco/surface/SenatorsAjax/GetSenators?displayFor=senatorslist&Lang=en", as_json=False,
               headers={"X-Requested-With": "XMLHttpRequest"}).decode("utf-8", "ignore")
    members = []
    for r in re.finditer(r'<tr>\s*<td data-order="([^"]+)">\s*<a href="([^"]+)">.*?</a>\s*</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>', page, flags=re.S):
        sur, _, given = html.unescape(r[1]).partition(",")
        grp = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", r[3]))).strip()
        members.append(dict(name=f"{given.strip()} {sur.strip()}".strip(), party=GROUP.get(grp, grp), ref=r[2].strip("/").rsplit("/", 1)[-1],
                            place=re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", r[4])).strip(), start=re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", r[5]))[:10],
                            url="https://sencanada.ca" + r[2]))
    if len(members) < 80:
        sys.exit(f"Senate of Canada: read {len(members)} senators, expected about 90 to 105; the page has changed, check the adapter")
    count = {}
    for m in members:
        count[m["party"]] = count.get(m["party"], 0) + 1
    order = sorted(count, key=lambda p: -count[p])
    return [dict(name="Senate of Canada", level="national", seats=105, source_url="https://sencanada.ca/en/senators/",
                 note="105 seats, appointed by the Governor General on the Prime Minister's advice until age 75; vacant seats are shown as Vacant. Who sits and their group are from the Senate's own list of senators. Unlit seats mean nothing found, never opposition.",
                 role="Senator", role_re=r"(?i)\bsenator\b", role_start=r"(?i)senator", members=members, former=[], party_order=order,
                 colours={"Independent Senators Group": "5a7fb3", "Progressive Senate Group": "d71920", "Canadian Senators Group": "7a5ab3", "Conservative": "1a4782",
                          "Non-affiliated": "8a8680", "Government Representative Office": "e07a1f"})]


def australia():
    """The House of Representatives (150 seats) and the Senate (76) of the Parliament of Australia. aph.gov.au refuses scripts, so the two lists are read
    once in a browser and passed with --local (see skill/references/countries/australia.md for the browser snippet): rows of [name, division or state,
    party, APH id], one file per chamber, saved for the two addresses below. Names have honorifics and postnominals removed."""
    PARTY = {"Australian Labor Party": "Labor", "Liberal Party of Australia": "Liberal", "Liberal National Party of Queensland": "Liberal National Party",
             "The Nationals": "Nationals", "Australian Greens": "Greens", "One Nation": "One Nation", "Independent": "Independent", "Country Liberal Party": "Country Liberal Party",
             "Katter's Australian Party": "Katter's Australian Party", "Centre Alliance": "Centre Alliance", "Jacqui Lambie Network": "Jacqui Lambie Network",
             "United Australia Party": "United Australia Party", "Australia's Voice": "Australia's Voice"}
    colours = {"Labor": "e11931", "Liberal": "1c4f9c", "Liberal National Party": "0a3a7a", "Nationals": "f2c230", "Greens": "10a64a", "One Nation": "f28c1f",
               "Independent": "8a8680", "Country Liberal Party": "c9a227", "Katter's Australian Party": "b5461f", "Centre Alliance": "e07a1f",
               "Jacqui Lambie Network": "7a5ab3", "United Australia Party": "e8c32a", "Australia's Voice": "2aa5c9"}

    def clean(n):
        n = re.sub(r"^(the Hon |The Hon |Hon |Dr |Mr |Ms |Mrs |Prof )+", "", n).strip().rstrip(",")
        return re.sub(r"( (OAM|AM|AO|AC|KC|SC|CSC|MP))+$", "", n).strip()

    def members(url):
        rows = get(url)
        return [dict(name=clean(r[0]), party=PARTY.get(r[2], r[2]), ref=r[3], place=r[1], start="",
                     url=f"https://www.aph.gov.au/Senators_and_Members/Parliamentarian?MPID={r[3]}") for r in rows]

    def chamber(name, seats, mem, role, rre, note, src, exp):
        if len(mem) < exp:
            sys.exit(f"{name}: read {len(mem)} members, expected {exp}; save the list again (see the Australia guide)")
        count = {}
        for m in mem:
            count[m["party"]] = count.get(m["party"], 0) + 1
        order = sorted(count, key=lambda p: -count[p])
        return dict(name=name, level="national", seats=seats, source_url=src, note=note, role=role, role_re=rre, role_start=rre, members=mem, former=[],
                    party_order=order, colours={p: colours.get(p, "8a8680") for p in order})
    hurl, surl = "https://www.aph.gov.au/Senators_and_Members/Members", "https://www.aph.gov.au/Senators_and_Members/Senators"
    return [chamber("Australian House of Representatives", 150, members(hurl), "Member of the House of Representatives", r"(?i)\bmember for\b|house of representatives|\bMP for\b",
                    "150 seats, one per division, elected 3 May 2025. Who sits and their party are from the Parliament's own list of members (aph.gov.au), read in a browser. Unlit seats mean nothing found, never opposition.", hurl, 140),
            chamber("Australian Senate", 76, members(surl), "Senator", r"(?i)\bsenator\b|australian senate",
                    "76 seats, twelve for each state and two each for the Australian Capital Territory and the Northern Territory. Who sits and their party are from the Parliament's own list of senators (aph.gov.au), read in a browser. Unlit seats mean nothing found, never opposition.", surl, 70)]


def egypt():
    """The House of Representatives (596 seats): parliament.gov.eg/members.aspx lists the members in office (name and membership type, no party), read once
    in a browser and passed with --local (see skill/references/countries/eg.md): rows of [short name in Arabic, "", membership type (Individual, List
    or Appointed), member id, full name]. Seats are grouped by how they were filled, because the site gives no party. The Senate has no list yet."""
    url = "https://www.parliament.gov.eg/members.aspx"
    rows = get(url)
    members = [dict(name=r[0], native=(r[4] if len(r) > 4 and r[4] else r[0]), party=r[2], ref=r[3], place="", start="", url=f"https://www.parliament.gov.eg/MembersDetails.aspx?id={r[3]}") for r in rows]
    if len(members) < 550:
        sys.exit(f"Egypt: read {len(members)} members, expected about 595; save the list again (see the Egypt guide)")
    return [dict(name="House of Representatives", level="national", seats=596, source_url=url,
                 note="596 seats: 284 individual, 284 list and 28 appointed by the President, elected in late 2025. Who sits is from the House's own list of members in office (parliament.gov.eg); the site gives names in Arabic and the way each seat was filled, not the party, so seats are grouped that way. Unlit seats mean nothing found, never opposition.",
                 role="Member of Parliament", role_re=r"(?i)member of parliament|house of representatives|مجلس النواب", role_start=r"(?i)member of parliament",
                 members=members, former=[], party_order=["List", "Individual", "Appointed"],
                 colours={"List": "1a5fb4", "Individual": "e07a1f", "Appointed": "8a8680"})]


def malaysia_senate():
    """The Dewan Negara (70 seats): parlimen.gov.my/ahli-dewan-dn.html. The page refuses scripts, so it is read in a browser and passed with --local
    (see the Malaysia guide): rows of [name, "", party, how the seat was filled]. Seats the page does not name are shown as Vacant."""
    rows = get("https://www.parlimen.gov.my/ahli-dewan-dn.html?uweb=dn&")
    members = [dict(name=re.sub(r"^(Dato'? Sri|Datuk Seri|Dato'|Datuk|Tan Sri|Dr\.|Tuan Haji|Puan|Tuan)\s+", "", r[0]), party=r[2], ref="", place=r[3], start="", url="https://www.parlimen.gov.my/ahli-dewan-dn.html?uweb=dn&") for r in rows]
    if len(members) < 40:
        sys.exit(f"Dewan Negara: read {len(members)} members, expected about 56 to 70; save the list again (see the Malaysia guide)")
    count = {}
    for m in members:
        count[m["party"]] = count.get(m["party"], 0) + 1
    order = sorted(count, key=lambda p: -count[p])
    return [dict(name="Dewan Negara", level="national", seats=70, source_url="https://www.parlimen.gov.my/ahli-dewan-dn.html?uweb=dn&",
                 note="70 seats: 26 elected by the state assemblies (two each) and 44 appointed by the Yang di-Pertuan Agong. Who sits and their party are from the Dewan Negara's own list of members (parlimen.gov.my), 56 of whom were named on 28 October 2026; the other seats show as Vacant. Unlit seats mean nothing found, never opposition.",
                 role="Senator", role_re=r"(?i)dewan negara|\bsenator\b", role_start=r"(?i)senator", members=members, former=[], party_order=order,
                 colours={"PKR": "1a95b8", "UMNO": "e11931", "PAS": "10733c", "DAP": "d2232a", "PBB": "f2c230", "AMANAH": "f28c1f", "PROFESIONAL": "8a8680", "No party": "8a8680"})]


def nigeria_senate():
    """The Senate of Nigeria (109 seats): nass.gov.ng/mps/senators, the list its own page shows (74 senators on 28 October 2026; the page does
    not name the others). The page is a JavaScript table, but the data request behind it
    (/mps/get_legislators/?chamber=1) answers scripts with rows of [name, state, district, party, id]; a saved copy can still be passed with --local."""
    rows = get("https://www.nass.gov.ng/mps/get_legislators/?chamber=1&draw=1&start=0&length=200")  # the table's own data request
    rows = rows["data"] if isinstance(rows, dict) else rows  # or the list passed with --local
    members = [dict(name=re.sub(r"\s+", " ", re.sub(r"^Sen\.\s*", "", r[0])).strip(), party=r[3], ref=r[4], place=f"{r[2]}, {r[1]}", start="",
                    url="https://www.nass.gov.ng/mps/senators") for r in rows]
    if len(members) < 60:
        sys.exit(f"Senate of Nigeria: read {len(members)} senators, expected about 74 to 109; save the list again (see the Nigeria guide)")
    count = {}
    for m in members:
        count[m["party"]] = count.get(m["party"], 0) + 1
    order = sorted(count, key=lambda p: -count[p])
    return [dict(name="Senate of Nigeria", level="national", seats=109, source_url="https://www.nass.gov.ng/mps/senators",
                 note="109 seats: three for each of the 36 states and one for the Federal Capital Territory. Who sits and their party are from the Senate's own list of senators (nass.gov.ng), which named 74 on 28 October 2026; the other seats show as 'Not named on the Senate's page', not as vacant. Unlit seats mean nothing found, never opposition.",
                 role="Senator", role_re=r"(?i)senate of nigeria|nigerian senat|\bsenator\b", role_start=r"(?i)senator", members=members, former=[], party_order=order,
                 vacant_label="Not named on the Senate's page",
                 colours={"APC": "1d7a3a", "PDP": "d62828", "LP": "2a9d8f", "SDP": "6a4c93", "APGA": "3a86ff", "ADP": "8a8680"})]


WIKI_UA = {"User-Agent": "WealthTaxSupporters/1.0 (https://wealthtaxsupporters.com; seat charts)"}


def wiki_page(lang, title):
    """The HTML of a Wikipedia article through the MediaWiki API (a secondary source, used where a parliament's own list cannot be read)."""
    api = f"https://{lang}.wikipedia.org/w/api.php?action=parse&prop=text&format=json&redirects=1&page=" + urllib.parse.quote(title)
    return get(api, headers=WIKI_UA)["parse"]["text"]["*"]


def wiki_tables(page, heading=False):
    """The wikitables of an article as lists of rows of cell text; with heading=True each table comes with the last heading before it."""
    import html

    def clean(c):
        c = re.sub(r"<sup[^>]*>.*?</sup>|<style.*?</style>", "", c, flags=re.S)
        return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", c))).replace("​", "").strip()
    out, cur = [], ""
    for part in re.split(r"(<h[234][^>]*>.*?</h[234]>)", page, flags=re.S):
        h = re.match(r"<h[234][^>]*>(.*?)</h[234]>", part, flags=re.S)
        if h:
            cur = clean(h[1])
            continue
        for t in re.findall(r'<table[^>]*class="[^"]*wikitable[^"]*"[^>]*>(.*?)</table>', part, flags=re.S):
            rows = [[clean(c) for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, flags=re.S)] for r in re.findall(r"<tr[^>]*>(.*?)</tr>", t, flags=re.S)]
            rows = [r for r in rows if r]
            out.append((cur, rows) if heading else rows)
    return out


def _upper(name, seats, source_url, note, role, rre, members, colours, order=None, vacant=None, strict=False):
    count = {}
    for m in members:
        count[m["party"]] = count.get(m["party"], 0) + 1
    o = order or sorted(count, key=lambda p: -count[p])
    d = dict(name=name, level="national", seats=seats, source_url=source_url, note=note, role=role, role_re=rre, role_start=rre, members=members, former=[],
             party_order=o, colours={p: colours.get(p, "8a8680") for p in o})
    if vacant:
        d["vacant_label"] = vacant
    if strict:  # names with two surnames: leave out the looser first-and-last-word match
        d["strict"] = True
    return d


def poland_senate():
    """The Senat (100 seats): the Polish Wikipedia article on the senators of the 11th term (the senat.gov.pl list is behind a Cloudflare check, which is
    not bypassed). It lists the 100 elected in October 2023, the by-election winners and the mandates that ended; the sitting members are
    the first list, less those who left, plus those who replaced them. A secondary source, kept current by editors: the note says so."""
    wurl = "https://pl.wikipedia.org/wiki/Senatorowie_XI_kadencji_Senatu_Rzeczypospolitej_Polskiej"
    ts = wiki_tables(wiki_page("pl", "Senatorowie XI kadencji Senatu Rzeczypospolitej Polskiej"))
    base = next(t for t in ts if t[0][:3] == ["Zdjęcie", "", "Senator"] and "Okręg" in t[0] and "Data wyboru" not in t[0])
    byel = next((t for t in ts if t[0][:3] == ["Zdjęcie", "", "Senator"] and "Data wyboru" in t[0]), [[]])
    gone = next((t for t in ts if t[0][:2] == ["Senator", "Data wygaśnięcia mandatu"]), [[]])

    def nm(c):
        return c.split("!")[-1].strip()

    def committee(c):
        c = re.sub(r"^KKW |^KW ", "", c)
        return "Koalicja Obywatelska" if c.startswith("Koalicja Obywatelska") else "Lewica" if c.endswith("Lewica") else c
    left = {nm(r[1]) for r in gone[1:] if len(r) > 1}
    members, last = [], ""
    for r in base[1:]:  # the photo cell is merged in some rows, so the name is the first cell with the sort key "Surname !Given Surname"
        k = next((x for x in range(len(r)) if "!" in r[x]), None)
        if k is None or len(r) < k + 3:
            continue
        cm = r[k + 1]
        if re.fullmatch(r"\d+", cm):  # the committee cell is merged with the row above: take it from there
            cm, dist = last, cm
        else:
            last, dist = cm, r[k + 2]
        if nm(r[k]) not in left:
            members.append(dict(name=nm(r[k]), party=committee(cm), ref=nm(r[k]), place=f"okręg {dist}", start="", url=wurl))
    for r in byel[1:]:
        k = next((x for x in range(len(r)) if "!" in r[x]), None)
        if k is not None and len(r) > k + 3:
            members.append(dict(name=nm(r[k]), party=committee(r[k + 1]), ref=nm(r[k]), place=f"okręg {r[k + 3]}", start="", url=wurl))
    if len(members) < 90:
        sys.exit(f"Senat: read {len(members)} senators, expected about 99; the article has changed, check the adapter")
    return [_upper("Senat", 100, wurl,
                   "100 seats, one to four per district, elected 15 October 2023. Who sits and their election committee are from the Polish Wikipedia list of the senators of the 11th term (updated for by-elections and mandates that ended), because the Senate's own list could not be read; a secondary source. Unlit seats mean nothing found, never opposition.",
                   "Senator", r"(?i)senat of poland|polish senat|\bsenator\b|senator rp", members,
                   {"Koalicja Obywatelska": "f68f2f", "Prawo i Sprawiedliwość": "263778", "Trzecia Droga": "ffd500", "Lewica": "d4005a", "Bezpartyjni": "8a8680"})]


def belgium_senate():
    """The Senate of Belgium (60 seats): the English Wikipedia list of the members 2024-2029 (senate.be is behind a Cloudflare check, which is not
    bypassed): 50 senators from the community and regional parliaments and 10 co-opted. A secondary source."""
    wurl = "https://en.wikipedia.org/wiki/List_of_members_of_the_Senate_of_Belgium,_2024–2029"
    ts = wiki_tables(wiki_page("en", "List of members of the Senate of Belgium, 2024–2029"))
    t = next(t for t in ts if t[0][:2] == ["Senator", "Party"])
    members = [dict(name=re.sub(r"\s*\[.*?\]", "", r[0]).strip(), party=r[1], ref=r[0], place=r[3] if len(r) > 3 else "", start="", url=wurl) for r in t[1:] if len(r) >= 4 and r[0]]
    if len(members) < 50:
        sys.exit(f"Senate of Belgium: read {len(members)} senators, expected 60; the article has changed, check the adapter")
    return [_upper("Senate of Belgium", 60, wurl,
                   "60 seats: 50 senators designated by the parliaments of the communities and regions and 10 co-opted, for 2024-2029. Who sits and their party are from the English Wikipedia list of the members, because the Senate's own site could not be read; a secondary source. Unlit seats mean nothing found, never opposition.",
                   "Senator", r"(?i)belgian senat|senate of belgium|\bsenator\b", members,
                   {"N-VA": "f4a300", "Vlaams Belang": "5a4a2a", "PS": "e11931", "MR": "1c4f9c", "Les Engagés": "2aa5c9", "PVDA-PTB": "b01c2e", "Vooruit": "e8412a", "CD&V": "f28c1f",
                    "Open Vld": "1f78c8", "Groen": "6aa84f", "Ecolo": "62b04b", "DéFI": "e02c8a"})]


def indonesia_dpd():
    """The Dewan Perwakilan Daerah (152 seats, four for each of the 38 provinces): the Indonesian Wikipedia list of the members 2024-2029 (dpd.go.id
    shows its list only after its province filters). Titles and degrees are removed from the names. Members have no party. A secondary source."""
    wurl = "https://id.wikipedia.org/wiki/Daftar_anggota_Dewan_Perwakilan_Daerah_Republik_Indonesia_2024–2029"
    parts = wiki_tables(wiki_page("id", "Daftar anggota Dewan Perwakilan Daerah Republik Indonesia 2024–2029"), heading=True)
    seen, members = set(), []
    for prov, t in parts:
        for r in t[1:]:
            if len(r) < 3 or not re.match(r"^B[–-]\d+$", r[0]) or r[0] in seen:
                continue
            seen.add(r[0])
            n = re.sub(r"^(?:[A-Za-z]{1,4}\.\s*)+", "", r[2])  # leading titles (Ust. Dr. H. K.H.)
            n = re.sub(r"(?<=[a-z])(?=[A-Z][a-zA-Z]{0,3}\.)", "|", n).split("|")[0]  # degrees glued to the surname (UmaS.Sos.)
            n = re.sub(r"\s+(?:[A-Z][A-Za-z]{0,3}\.){1,4}(?:,?\s*(?:[A-Z][A-Za-z]{0,3}\.){1,4})*$", "", n).strip(" ,")
            members.append(dict(name=n, party="Regional representatives (no party)", ref=r[0], place=prov, start="", url=wurl))
    if len(members) < 140:
        sys.exit(f"DPD: read {len(members)} members, expected 152; the article has changed, check the adapter")
    return [_upper("Dewan Perwakilan Daerah", 152, wurl,
                   "152 seats, four for each of the 38 provinces, elected in February 2024 as individuals without party. Who sits is from the Indonesian Wikipedia list of the members 2024-2029 (the DPD's own list needs its province filters), a secondary source; titles and degrees are removed from the names. Unlit seats mean nothing found, never opposition.",
                   "Member of the Regional Representative Council", r"(?i)\bDPD\b|regional representative council|dewan perwakilan daerah", members, {"Regional representatives (no party)": "7a8f5a"})]


def egypt_senate():
    """The Senate of Egypt (300 seats): the members Wikidata holds for the Senate elected in 2025 (position Q98218748, started 2025 or later, no end).
    Neither senate.gov.eg nor Wikipedia has a complete list, so this is partial (about a third of the seats): the rest show as 'Not named'. Party is
    taken from Wikidata where given."""
    q = ('SELECT ?p ?pLabel ?partyLabel WHERE { ?p p:P39 ?s . ?s ps:P39 wd:Q98218748 . ?s pq:P580 ?start . FILTER(?start >= "2025-01-01T00:00:00Z"^^xsd:dateTime) '
         'OPTIONAL { ?s pq:P582 ?end } FILTER(!BOUND(?end) || ?end > NOW()) OPTIONAL { ?p wdt:P102 ?party } '
         'SERVICE wikibase:label { bd:serviceParam wikibase:language "en,ar". } }')
    d = get("https://query.wikidata.org/sparql?query=" + urllib.parse.quote(q) + "&format=json", headers=WIKI_UA)["results"]["bindings"]
    by = {}
    for x in d:
        qid = x["p"]["value"].rsplit("/", 1)[-1]
        by.setdefault(qid, dict(name=x["pLabel"]["value"], party=x.get("partyLabel", {}).get("value", "Party not given"), qid=qid, ref=qid, place="", start="",
                                url="https://www.wikidata.org/wiki/" + qid))
    members = [m for m in by.values() if not re.match(r"^Q\d+$", m["name"])]
    if len(members) < 50:
        sys.exit(f"Senate of Egypt: read {len(members)} members from Wikidata, expected about 100; check the query")
    return [_upper("Senate of Egypt", 300, "https://www.wikidata.org/wiki/Q98218748",
                   "300 seats: 200 elected (100 by list, 100 individual) and 100 appointed by the President, from 2025. No complete list of members could be found (senate.gov.eg did not answer), so this chart shows only the members Wikidata records for the 2025 Senate, about a third; the other seats show as 'Not named', which is not the same as vacant. Unlit seats mean nothing found, never opposition.",
                   "Senator", r"(?i)senate of egypt|egyptian senat|\bsenator\b", members, {}, vacant="Not named")]


def spain_senate():
    """The Senado (266 seats, XV legislature): the Spanish Wikipedia list of the senators of the XV legislature (senado.es refuses scripts). The Cortes
    were dissolved on 6 October 2026, so these are the senators at the dissolution, not sitting ones: the note says so. After the November 2026
    election, run it against the new legislature's list (or the Senate's own list read in a browser). A secondary source."""
    wurl = "https://es.wikipedia.org/wiki/Anexo:Senadores_de_la_XV_legislatura_de_España"
    ts = wiki_tables(wiki_page("es", "Anexo:Senadores de la XV legislatura de España"))
    t = next(t for t in ts if t[0][:2] == ["Nombre y apellidos", "Grupo"] and "Baja" not in t[0])
    GROUP = {"GPP": "Partido Popular", "GPS": "PSOE", "GPERB": "ERC-Bildu", "GPPLU": "Plural (Junts)", "GPIC": "Izquierda Confederal", "GPV": "Vasco (EAJ-PNV)", "GPMX": "Mixto"}
    members = []
    for r in t[1:]:
        if len(r) < 6 or not r[0]:
            continue
        sur, _, given = r[0].partition(",")
        members.append(dict(name=f"{given.strip()} {sur.strip()}".strip(), party=GROUP.get(r[2], r[2]), ref=r[0], place=r[5], start="", url=wurl))
    if len(members) < 240:
        sys.exit(f"Senado: read {len(members)} senators, expected about 265; the article has changed, check the adapter")
    return [_upper("Senado", 266, wurl,
                   "266 seats (208 elected by province and 58 designated by the autonomous communities), XV legislature elected 23 July 2023. The Cortes were dissolved on 6 October 2026 for the election of 29 November 2026, so the members shown are the senators of the legislature at its end, from the Spanish Wikipedia list (senado.es refuses scripts), a secondary source; replace it with the new Senate's list once it meets. Unlit seats mean nothing found, never opposition.",
                   "Senator", r"(?i)\bsenador|senado de españa|spanish senat|\bsenator\b", members,
                   {"Partido Popular": "1c9be0", "PSOE": "e11931", "ERC-Bildu": "e8a01a", "Plural (Junts)": "37a6b5", "Izquierda Confederal": "a1274a", "Vasco (EAJ-PNV)": "2f8f4a", "Mixto": "8a8680"}, strict=True)]


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



def switzerland():
    """The Federal Assembly: National Council (200) and Council of States (46), from the Swiss Parliament's OData service (ws.parlament.ch),
    MemberCouncil rows with Active=true. Each member carries party, canton (English name, as in the register) and the date they joined."""
    import datetime as _dt
    CANTON = {"ZH": "Zurich", "BE": "Bern", "LU": "Lucerne", "UR": "Uri", "SZ": "Schwyz", "OW": "Obwalden", "NW": "Nidwalden", "GL": "Glarus", "ZG": "Zug",
              "FR": "Fribourg", "SO": "Solothurn", "BS": "Basel-Stadt", "BL": "Basel-Landschaft", "SH": "Schaffhausen", "AR": "Appenzell Ausserrhoden",
              "AI": "Appenzell Innerrhoden", "SG": "St. Gallen", "GR": "Graubünden", "AG": "Aargau", "TG": "Thurgau", "TI": "Ticino", "VD": "Vaud",
              "VS": "Valais", "NE": "Neuchâtel", "GE": "Geneva", "JU": "Jura"}
    PARTY = {"SVP": "Swiss People's Party", "SP": "Social Democratic Party", "M-E": "The Centre", "FDP-Liberale": "FDP.The Liberals", "GRÜNE": "Green Party",
             "glp": "Green Liberal Party", "MCG": "Geneva Citizens' Movement", "EVP": "Evangelical People's Party", "EDU": "Federal Democratic Union",
             "Lega": "Lega dei Ticinesi", "Al": "Green Party", "LDP": "Liberal-Democratic Party", "-": "Independent", "PdA": "Swiss Party of Labour"}
    url = "https://ws.parlament.ch/odata.svc/MemberCouncil?$top=400&$filter=" + urllib.parse.quote("Active eq true and Language eq 'DE'")
    rows = get(url, headers={"Accept": "application/json"})
    rows = rows["d"]["results"] if isinstance(rows["d"], dict) else rows["d"]
    chambers = []
    for council, name, seats, note, role in ((1, "National Council (Nationalrat)", 200, "200 seats, elected by proportional representation in the cantons.", "Member of the National Council"),
                                              (2, "Council of States (Ständerat)", 46, "46 seats: two per canton, one per half-canton.", "Member of the Council of States")):
        members = []
        for x in rows:
            if x["Council"] != council:
                continue
            j = x.get("DateJoining")
            members.append(dict(name=f"{x['FirstName']} {x['LastName']}", party=PARTY.get(x["PartyAbbreviation"], x["PartyName"]), ref=str(x["PersonNumber"]),
                                place=CANTON[x["CantonAbbreviation"]], url=f"https://www.parlament.ch/de/biografie?CouncillorId={x['PersonNumber']}",
                                start=_dt.datetime.fromtimestamp(int(j[6:19]) / 1000, _dt.timezone.utc).strftime("%Y-%m-%d") if j else ""))
        if len(members) != seats:
            sys.exit(f"{name}: read {len(members)} members, expected {seats}; check the adapter")
        count = {}
        for m in members:
            count[m["party"]] = count.get(m["party"], 0) + 1
        chambers.append(dict(name=name, level="national", seats=seats, source_url="https://www.parlament.ch/en/organe/" + ("national-council" if council == 1 else "council-of-states"),
                             note=note + " Who sits and their party are from the Federal Assembly's open data. Unlit seats mean nothing found, never opposition.",
                             role=role, role_re=r"(?i)^(member|former member) of the national council" if council == 1 else r"(?i)council of states|ständerat", role_start=r"(?i)member of the national council" if council == 1 else r"(?i)member of the council of states",
                             members=members, former=[],
                             party_order=["Green Party", "Social Democratic Party", "Green Liberal Party", "The Centre", "Evangelical People's Party", "FDP.The Liberals", "Swiss People's Party", "Federal Democratic Union",
                                          "Geneva Citizens' Movement", "Lega dei Ticinesi", "Liberal-Democratic Party", "Independent"],
                             colours={"Green Party": "84b547", "Social Democratic Party": "e8362d", "Green Liberal Party": "a6cf42", "The Centre": "f39200", "Evangelical People's Party": "f0c800",
                                      "FDP.The Liberals": "2a6ebb", "Swiss People's Party": "3a8a3c", "Federal Democratic Union": "7a6a53", "Geneva Citizens' Movement": "f5a623",
                                      "Lega dei Ticinesi": "1f4e9c", "Liberal-Democratic Party": "5aa9e6", "Independent": "8a8680"}))
    return chambers


def czechia():
    """Poslanecká sněmovna (200 seats): psp.cz member list."""
    import html as _html
    url = "https://www.psp.cz/sqw/snem.sqw?P1=0&P2=0"
    raw = get(url, as_json=False).decode("windows-1250", errors="replace")
    rows = re.findall(r'<tr>\s*<th>(.*?)</tr>', raw, re.DOTALL)
    CLUB_MAP = {
        "ODS": "ODS",
        "ANO2011": "ANO 2011",
        "Piráti": "Piráti",
        "MS": "Motoristé sobě",
        "KDU-ČSL": "KDU-ČSL",
        "STAN": "STAN",
        "TOP09": "TOP 09",
        "SPD": "SPD",
    }
    members = []
    for r in rows:
        m_match = re.search(r'href="detail\.sqw\?id=(\d+)[^"]*">([^<]+)</a>', r)
        if not m_match:
            continue
        mid = m_match.group(1)
        name = _html.unescape(m_match.group(2)).replace("\xa0", " ").strip()
        kraj_match = re.search(r'<a href="snem\.sqw\?id=\d+">([^<]+)</a>', r)
        place = _html.unescape(kraj_match.group(1)).replace("\xa0", " ").strip() if kraj_match else ""
        tds = re.findall(r'<td[^>]*>(.*?)</td>', r, re.DOTALL)
        party = "Nezařazení"
        if len(tds) >= 2:
            m_party = re.search(r'title="[^"]*">([^<]+)</a>', tds[1])
            if m_party:
                raw_p = m_party.group(1).strip()
                party = CLUB_MAP.get(raw_p, raw_p)
        members.append(dict(name=name, party=party, ref=mid, place=place,
                            url=f"https://www.psp.cz/sqw/detail.sqw?id={mid}"))
    order = ["Piráti", "STAN", "TOP 09", "KDU-ČSL", "ODS", "ANO 2011", "Motoristé sobě", "SPD"]
    colours = {
        "Piráti": "000000",
        "STAN": "7ac143",
        "TOP 09": "993366",
        "KDU-ČSL": "ffd700",
        "ODS": "004494",
        "ANO 2011": "261060",
        "Motoristé sobě": "186088",
        "SPD": "e2801e",
    }
    return [dict(name="Poslanecká sněmovna", level="national", seats=200,
                 source_url="https://www.psp.cz/sqw/snem.sqw?P1=0&P2=0",
                 note="200 seats. Sitting members and parliamentary clubs from the official Chamber of Deputies (Poslanecká sněmovna) member register.",
                 role="Poslanec/poslankyně Poslanecké sněmovny",
                 role_re=r"(?i)\bposlan(?:ec|kyně)\s+poslanecké\s+sněmovny\b|\bposlan(?:ec|kyně)\s+psp\b|\bčlen(?:ka)?\s+poslanecké\s+sněmovny\b",
                 role_start=r"(?i)(poslan(?:ec|kyně)\s+poslanecké\s+sněmovny|poslaneck)",
                 members=members, former=[], party_order=order, colours=colours)]


def portugal():
    """The Assembleia da República (230 seats): the Parliament's own list of deputies in office (parlamento.pt, Deputadoslista), one row per sitting
    deputy with the electoral circle and parliamentary group; a substitute who serves holds the seat of a deputy on leave, so the list is always 230."""
    import html as _html
    url = "https://www.parlamento.pt/DeputadoGP/Paginas/Deputadoslista.aspx"
    page = get(url, as_json=False).decode("utf-8", "ignore")
    date = re.search(r"Deputados em fun\S+ à data de\s*(\d{4}-\d{2}-\d{2})", page)
    rows = {}
    for i, field, val in re.findall(r'rptResultsByDate_ctl(\d+)_(hplNome|lblCE|lblGP)"[^>]*>([^<]*)<', page):
        rows.setdefault(i, {})[field] = _html.unescape(val).strip()
    for i, href in re.findall(r'rptResultsByDate_ctl(\d+)_hplNome"[^>]*href="([^"]+)"', page):
        rows[i]["href"] = _html.unescape(href)
    if not date or len(rows) != 230 or any(not {"hplNome", "lblCE", "lblGP"} <= set(r) for r in rows.values()):
        sys.exit(f"Portugal: read {len(rows)} deputies, expected 230 with a date; the page has changed, check the adapter")
    members = []
    for r in rows.values():
        bid = re.search(r"BID=(\d+)", r.get("href", ""))
        members.append(dict(name=r["hplNome"], party=r["lblGP"], place=r["lblCE"], start="", ref=bid.group(1) if bid else "",
                            url="https://www.parlamento.pt" + r["href"] if r.get("href") else ""))
    order = ["L", "BE", "PCP", "PS", "PAN", "PSD", "CDS-PP", "IL", "JPP", "CH"]
    colours = {"L": "008b4a", "BE": "cf252b", "PCP": "bd1725", "PS": "ef5a89", "PAN": "2c9e86", "PSD": "f28c28", "CDS-PP": "1768b3", "IL": "13b9ce", "JPP": "805bb0", "CH": "173e83"}
    unknown = {m["party"] for m in members} - set(order)
    if unknown:
        sys.exit(f"Portugal: unknown parliamentary group(s) {unknown}; add them to the adapter")
    return [dict(name="Assembleia da República", level="national", seats=230, as_of=date.group(1), source_url=url,
                 note="230 seats, XVII legislature. Who sits and their group are from the Parliament's own list of deputies in office (a serving substitute holds the seat of a deputy on leave). Unlit seats mean nothing found, never opposition.",
                 role="Deputy, Assembleia da República", role_re=r"(?i)deputy|deputado|assembleia da rep", role_start=r"(?i)deputy|deputado", members=members, former=[],
                 party_order=order, colours=colours, strict=True)]


def denmark():
    """The Folketing (179 seats): the Folketing's open data (oda.ft.dk): the members of each party group of the current session, with their bio's
    constituency and start date. Leave-takers (orlov) keep their seat but a substitute serves it, so they are not listed as sitting.
    ft.dk itself answers scripts with a bot check."""
    MONTH = {m: i for i, m in enumerate(["januar", "februar", "marts", "april", "maj", "juni", "juli", "august", "september", "oktober", "november", "december"], 1)}

    def q(ent, **p):
        return get("https://oda.ft.dk/api/" + urllib.parse.quote(ent) + "?" + urllib.parse.urlencode(p))["value"]

    ses = q("Periode", **{"$filter": "type eq 'samling'", "$orderby": "startdato desc", "$top": 1})[0]
    groups = q("Aktør", **{"$filter": f"typeid eq 4 and startdato eq datetime'{ses['startdato'][:10]}T00:00:00'"})
    if not groups:
        sys.exit('Denmark: no party groups for the current session yet; check the adapter')
    PARTY = {"S": "Social Democrats", "SF": "Socialist People’s Party", "V": "Venstre", "DF": "Danish People’s Party", "LA": "Liberal Alliance", "M": "Moderates",
             "KF": "Conservative People’s Party", "EL": "Red-Green Alliance", "DD": "Denmark Democrats", "RV": "Social Liberal Party", "ALT": "The Alternative",
             "BP": "Borgernes Parti", "IA": "Inuit Ataqatigiit", "N": "Naleraq", "JF": "Javnaðarflokkurin", "SP": "Sambandsflokkurin", "UFG": "Independent"}
    rows = {}
    for g in groups:
        if g["gruppenavnkort"] not in PARTY:
            sys.exit(f"Denmark: unknown group {g['gruppenavnkort']}; add it to the adapter")
        for r in q("AktørAktør", **{"$filter": f"tilaktørid eq {g['id']}", "$top": 300}):
            if (r["slutdato"] or "9999")[:10] <= dt.date.today().isoformat() or r["startdato"][:10] > dt.date.today().isoformat():
                continue  # an end date in the future (a planned leave or exit) still counts as a member today
            rows[r["fraaktørid"]] = (PARTY[g["gruppenavnkort"]], r["rolleid"])  # 15 medlem; 6 and 12 are leave with and without pay
    ids = sorted(rows)
    people = {}
    for k in range(0, len(ids), 12):
        for a in q("Aktør", **{"$filter": " or ".join(f"id eq {i}" for i in ids[k:k + 12]), "$top": 50}):
            people[a["id"]] = a
    cur, leave = [], []
    for i in ids:
        a, (party, role) = people.get(i), rows[i]
        if not a:
            continue
        bio = a.get("biografi") or ""
        cons = re.findall(r"<constituency>(.*?)</constituency>", bio, re.S)
        c = next((x for x in cons if re.search(r"\bfra\s+\d", x)), "")  # the open one: "... i Fyns Storkreds fra 15. september 2011."
        place = (re.search(r" (?:i|på|for) ([^.]*?(?:Storkreds|Grønland|Færøerne))", c) or [None, ""])[1].strip()
        d = re.search(r"<functionStartDate>(\d+)\. (\w+) (\d{4})</functionStartDate>", bio) or re.search(r"fra (\d+)\. (\w+) (\d{4})", c)
        start = dt.date(int(d[3]), MONTH[d[2]], int(d[1])).isoformat() if d and d[2] in MONTH else ""
        row = dict(name=a["navn"], party=party, ref=str(i), place=place, start=start, url="")
        if role == 15:
            cur.append(row)
        else:
            leave.append(dict(row, on_leave=True))
    order = ["Red-Green Alliance", "The Alternative", "Socialist People’s Party", "Social Democrats", "Social Liberal Party", "Moderates", "Venstre", "Conservative People’s Party",
             "Liberal Alliance", "Danish People’s Party", "Denmark Democrats", "Borgernes Parti", "Inuit Ataqatigiit", "Naleraq", "Javnaðarflokkurin", "Sambandsflokkurin", "Independent"]
    colours = {"Red-Green Alliance": "e53935", "The Alternative": "00a651", "Socialist People’s Party": "e64043", "Social Democrats": "d20a11", "Social Liberal Party": "733280",
               "Moderates": "993399", "Venstre": "0053a0", "Conservative People’s Party": "00513e", "Liberal Alliance": "3db5cc", "Danish People’s Party": "fbd52b",
               "Denmark Democrats": "003c72", "Borgernes Parti": "416f85", "Inuit Ataqatigiit": "b8232c", "Naleraq": "ffbd00", "Javnaðarflokkurin": "b4222a",
               "Sambandsflokkurin": "2173b9", "Independent": "888888"}
    return [dict(name="Folketing", level="national", seats=179, source_url="https://oda.ft.dk/", former=leave, members=cur,
                 note=f"179 seats (175 for Denmark proper, 2 for Greenland, 2 for the Faroe Islands). Who sits and their party are from the Folketing's open data (oda.ft.dk), the members of each party group in session {ses['titel']}: {len(cur)} named, the rest shown as Vacant (a substitute not yet entered, or a seat open). Members on leave are left out (a substitute serves). Unlit seats mean nothing found, never opposition.",
                 role="Member of the Folketing", role_re=r"(?i)folketing|member of parliament", role_start=r"(?i)(former )?member of (the )?folketing|folketing member",
                 party_order=order, colours=colours)]


def iceland():
    """The Althing (63 seats): althingi.is open XML. The list for today names who holds a seat (a member, or a substitute serving; a member with a
    substitute is on leave), and each member's own record (thingseta) gives the party group, constituency and the date of their first seat."""
    import html as _html
    today = dt.date.today()
    s = get(f"https://www.althingi.is/altext/xml/thingmenn/?dagur={today.day}.{today.month}.{today.year}", as_json=False).decode("utf-8")
    PARTY = {"Samfylkingin": "Social Democratic Alliance", "Sjálfstæðisflokkur": "Independence Party", "Viðreisn": "Liberal Reform Party (Viðreisn)",
             "Flokkur fólksins": "People's Party", "Miðflokkurinn": "Centre Party", "Framsóknarflokkur": "Progressive Party", "utan þingflokka": "Non-attached",
             "Píratar": "Pirate Party", "Vinstrihreyfingin - grænt framboð": "Left-Green Movement", "Sósíalistaflokkur Íslands": "Socialist Party of Iceland"}
    cur, leave = [], []
    for pid, body in re.findall(r"<þingmaður id='(\d+)'>(.*?)</þingmaður>", s, re.S):
        kind = re.search(r"<tegund>(.*?)</tegund>", body)[1]
        if kind not in ("þingmaður", "varaþingmaður", "þingmaður með varamann"):
            continue
        name = _html.unescape(re.search(r"<nafn>(.*?)</nafn>", body)[1]).strip()
        seatx = get(f"https://www.althingi.is/altext/xml/thingmenn/thingmadur/thingseta/?nr={pid}", as_json=False).decode("utf-8")
        rec = re.findall(r"<þingseta>(.*?)</þingseta>", seatx, re.S)
        last = rec[-1]
        grp = re.search(r"<þingflokkur[^>]*>(.*?)</þingflokkur>", last)[1].strip()
        party = PARTY.get(grp)
        if not party:
            sys.exit(f"Iceland: unknown party group {grp!r}; add it to the adapter")
        place = re.search(r"<kjördæmi[^>]*><!\[CDATA\[(.*?)\]\]>", last)
        place = place[1] if place else ""
        first = [re.search(r"<inn>(.*?)</inn>", r)[1] for r in rec if re.search(r"<inn>(.*?)</inn>", r)]
        start = min((dt.datetime.strptime(x, "%d.%m.%Y").date() for x in first if x), default=None)
        row = dict(name=name, party=party, ref=pid, place=place, start=start.isoformat() if start else "", url=f"https://www.althingi.is/altext/cv/?nfaerslunr={pid}")
        if kind == "þingmaður með varamann":
            leave.append(dict(row, on_leave=True))
        else:
            cur.append(row)
    if len(cur) != 63:
        sys.exit(f"Iceland: read {len(cur)} seat holders, expected 63; check the adapter")
    order = ["Social Democratic Alliance", "Independence Party", "Liberal Reform Party (Viðreisn)", "People's Party", "Centre Party", "Progressive Party", "Non-attached"]
    colours = {"Social Democratic Alliance": "e4002b", "Independence Party": "0066b3", "Liberal Reform Party (Viðreisn)": "f58220", "People's Party": "f2c200",
               "Centre Party": "00a3a3", "Progressive Party": "00a651", "Non-attached": "8a8680"}
    return [dict(name="Alþingi", level="national", seats=63, source_url="https://www.althingi.is/altext/xml/thingmenn/", members=cur, former=leave,
                 note="63 seats. Who sits and their party group are from the Althing's open XML (althingi.is/altext/xml/thingmenn): members in office today plus substitutes serving; a member who has a substitute is on leave and the substitute holds the seat. Unlit seats mean nothing found, never opposition.",
                 role="Member of Alþingi", role_re=r"(?i)althingi|alþingi|member of parliament", role_start=r"(?i)(former )?member of althingi", party_order=order, colours=colours)]


def luxembourg():
    """The Chambre des Députés (60 seats): chd.lu/en/deputies, the sitting deputies grouped by political group (a substitute serves for a deputy who becomes a minister)."""
    import html as _html
    url = "https://www.chd.lu/en/deputies"
    page = get(url, as_json=False).decode("utf-8", "ignore")
    PARTY = {"CSV": "CSV", "DP": "DP", "LSAP": "LSAP", "ADR": "ADR", "déi gréng": "déi gréng", "Piraten": "Piraten", "déi Lénk": "déi Lénk"}
    members = []
    for sec_id, sec in re.findall(r'<section id="group-([^"]*)"(.*?)</section>', page, re.S):
        party = PARTY.get(sec_id)
        if not party:
            sys.exit(f"Luxembourg: unknown group {sec_id!r}; add it to the adapter")
        for ref, name in re.findall(r'href="/en/deputy/(\d+)".*?<div class="h5">(.*?)</div>', sec, re.S):
            place = re.search(r"Circonscription (\w+)", sec[sec.find(f'/en/deputy/{ref}"'):])
            members.append(dict(name=_html.unescape(name).strip(), party=party, ref=ref, place=place[1] if place else "", start="", url=f"https://www.chd.lu/en/deputy/{ref}"))
    if len(members) != 60:
        sys.exit(f"Luxembourg: read {len(members)} deputies, expected 60; check the adapter")
    order = ["déi Lénk", "Piraten", "déi gréng", "LSAP", "DP", "CSV", "ADR"]
    colours = {"CSV": "e8731c", "DP": "0b6fb8", "LSAP": "e10600", "ADR": "1a4fa0", "déi gréng": "7ab51d", "Piraten": "4c2f7f", "déi Lénk": "b5121b"}
    return [dict(name="Chambre des Députés", level="national", seats=60, source_url=url,
                 note="60 seats, elected 8 October 2023 in four constituencies. Who sits and their group are from the Chamber's own list of deputies (chd.lu), a substitute serving for a deputy who is a minister included. Unlit seats mean nothing found, never opposition.",
                 role="Member of the Chamber of Deputies", role_re=r"(?i)chamber of deputies|chambre des d", role_start=r"(?i)(former )?member of the chamber of deputies", members=members, former=[],
                 party_order=order, colours=colours)]


def malta():
    """The House of Representatives (79 seats): parlament.mt, Parliamentary Groups of the current legislature (one section per party, "Surname, First").
    The site answers scripts with 403: read the page once in a browser and pass it with --local https://parlament.mt/en/15th-leg/political-groups/=FILE
    (see skill/references/countries/mt.md)."""
    import html as _html
    url = "https://parlament.mt/en/15th-leg/political-groups/"
    page = get(url, as_json=False).decode("utf-8", "ignore")
    PARTY = {"Labour Party": "Labour Party", "Nationalist Party": "Nationalist Party"}
    members = []
    for title, sec in re.findall(r"<h3>(.*?)</h3>(.*?)(?=<h3>|$)", page, re.S):
        title = _html.unescape(title).strip()
        if title not in PARTY:
            sys.exit(f"Malta: unknown group {title!r}; add it to the adapter")
        for slug, label in re.findall(r'<a href="/en/\d+th-leg/political-groups/[^/]+/([^/"]+)/?">(.*?)</a>', sec, re.S):
            label = _html.unescape(re.sub(r"\s+", " ", label)).strip().split(" - ")[0]
            sur, _, first = label.partition(", ")
            members.append(dict(name=f"{first} {sur}".strip(), party=PARTY[title], ref=slug, place="", start="", url=""))
    if len(members) != 79:
        sys.exit(f"Malta: read {len(members)} members, expected 79; the page has changed, check the adapter")
    return [dict(name="House of Representatives", level="national", seats=79, source_url=url,
                 note="79 seats after the general election of 30 May 2026 (Labour 42, Nationalist Party 37; no other party won a seat). Who sits and their party are from the Parliament of Malta's own list of the parliamentary groups, read in a browser because the site refuses scripts. Unlit seats mean nothing found, never opposition.",
                 role="Member of the House of Representatives", role_re=r"(?i)house of representatives|member of parliament|\bMP\b", role_start=r"(?i)(former )?member of the house of representatives",
                 members=members, former=[], party_order=["Labour Party", "Nationalist Party"], colours={"Labour Party": "e4002b", "Nationalist Party": "1a3a8c"})]


def estonia():
    """The Riigikogu (101 seats): api.riigikogu.ee plenary-members (open, no key): each member's current parliamentary faction, electoral district and start date.
    Only the name, faction, district and dates are read: never the phone or e-mail the service also returns."""
    FACTION = {"Eesti Reformierakonna fraktsioon": "Reform", "Eesti 200 fraktsioon": "Eesti 200", "Eesti Keskerakonna fraktsioon": "Centre Party", "Isamaa fraktsioon": "Isamaa",
               "Eesti Konservatiivse Rahvaerakonna fraktsioon": "EKRE", "Sotsiaaldemokraatliku Erakonna fraktsioon": "Social Democratic Party",
               "Fraktsiooni mittekuuluvad Riigikogu liikmed": "Non-attached"}
    rows = [x for x in get("https://api.riigikogu.ee/api/plenary-members?lang=et") if x.get("active")]
    members = []
    for x in rows:
        f = [g for g in x.get("factions", []) if g["type"]["code"] == "FRAKTSIOON" and not g["membership"].get("endDate")]
        if len(f) != 1 or f[0]["name"] not in FACTION:
            sys.exit(f"Estonia: {x['fullName']} has faction(s) {[g['name'] for g in f]}; add it to the adapter")
        pm = x["plenaryMembership"]
        dist = next((d["electoralDistrict"]["value"] for d in x.get("electoralDistrictHistory", []) if d["membership"] == pm["membershipNumber"]), "")
        members.append(dict(name=x["fullName"], party=FACTION[f[0]["name"]], ref=x["uuid"], place=dist, start=(pm.get("startDate") or "")[:10],
                            url="https://www.riigikogu.ee/tutvustus-ja-ajalugu/riigikogu-liikmed/"))
    if len(members) != 101:
        sys.exit(f"Estonia: read {len(members)} members, expected 101; check the adapter")
    order = ["Social Democratic Party", "Centre Party", "Reform", "Eesti 200", "Isamaa", "EKRE", "Non-attached"]
    colours = {"Reform": "fed600", "Eesti 200": "0ab4be", "Centre Party": "007f3f", "Isamaa": "009fe3", "EKRE": "8b4513", "Social Democratic Party": "e10600", "Non-attached": "8a8680"}
    return [dict(name="Riigikogu", level="national", seats=101, source_url="https://api.riigikogu.ee/api/plenary-members?lang=et",
                 note="101 seats. Who sits and their faction are from the Riigikogu's own open member list (api.riigikogu.ee, plenary-members); members who are not in a faction are shown as Non-attached. Unlit seats mean nothing found, never opposition.",
                 role="Member of the Riigikogu", role_re=r"(?i)riigikogu", role_start=r"(?i)(former )?member of the riigikogu", members=members, former=[],
                 party_order=order, colours=colours)]


def lithuania():
    """The Seimas (141 seats): the 'Seimo nariai' member list on lrs.lt (name and faction). The open-data XML (apps.lrs.lt, www.lrs.lt/sip/p2b.ad_seimo_nariai)
    does not answer from every network, so the HTML list is read. A member in no faction is shown as Non-attached."""
    import html as _html
    url = "https://www.lrs.lt/sip/portal.show?p_r=35299&p_k=1"
    page = get(url, as_json=False).decode("utf-8", "ignore")
    FACTION = {"Lietuvos socialdemokratų partijos frakcija": "LSDP", "Tėvynės sąjungos-Lietuvos krikščionių demokratų frakcija": "TS-LKD", "„Nemuno aušros“ frakcija": "Nemuno aušra",
               "Demokratų frakcija „Vardan Lietuvos“": "Vardan Lietuvos", "Liberalų sąjūdžio frakcija": "Liberal Movement",
               "Lietuvos valstiečių, žaliųjų ir Krikščioniškų šeimų sąjungos frakcija": "LVŽS", "Mišri Seimo narių grupė": "Mixed group"}
    members = []
    for it in re.findall(r'<div class="list-member photo">(.*?)(?=<div class="list-member photo">|<hr class="container-hr|$)', page, re.S):
        a = re.search(r'class="smn-name link"\s*href="[^"]*p_asm_id=(\d+)">(.*?)</a>', it, re.S)
        f = re.search(r'class="smn-frakcija link"[^>]*>(.*?)</a>', it, re.S)
        if not a:
            continue
        raw = re.sub(r"\s+", " ", _html.unescape(f[1])).strip() if f else ""
        fac = "Non-attached" if not raw else FACTION.get(raw)
        if not fac:
            sys.exit(f"Lithuania: unknown faction {raw!r}; add it to the adapter")
        name = _html.unescape(re.sub(r"<[^>]+>", "", re.sub(r"<br>", " ", re.sub(r"\s+", " ", a[2])))).strip()
        members.append(dict(name=name, party=fac, ref=a[1], place="", start="", url=f"https://www.lrs.lt/sip/portal.show?p_r=35299&p_k=1&p_a=498&p_asm_id={a[1]}"))
    if not 130 <= len(members) <= 141:
        sys.exit(f"Lithuania: read {len(members)} members, expected about 140; check the adapter")
    order = ["LSDP", "Liberal Movement", "LVŽS", "Vardan Lietuvos", "Mixed group", "Non-attached", "TS-LKD", "Nemuno aušra"]
    colours = {"LSDP": "e11931", "TS-LKD": "1b6bb5", "Nemuno aušra": "1f3a93", "Vardan Lietuvos": "e07a1f", "Liberal Movement": "f5a623", "LVŽS": "3a9a3f", "Mixed group": "8a8680", "Non-attached": "8a8680"}
    return [dict(name="Seimas", level="national", seats=141, source_url=url,
                 note="141 seats, 2024-2028 term. Who sits and their faction are from the Seimas's own member list (lrs.lt, Seimo nariai); a seat with no member is shown as Vacant and a member in no faction as Non-attached. Unlit seats mean nothing found, never opposition.",
                 role="Member of the Seimas", role_re=r"(?i)seimas", role_start=r"(?i)(former )?member of the seimas", members=members, former=[],
                 party_order=order, colours=colours)]

# ---------------------------------------------------------------- Turkey, Algeria, Tunisia, Morocco, Lebanon
def _tr_name(raw):
    """TBMM prints 'Given SURNAME' with the surname in capitals: fold the capitals back (Turkish İ and I) so the register's spelling meets it."""
    out = []
    for w in raw.replace("ı", "i").split():
        if w.isupper() and len(w) > 1:
            w = w.replace("İ", "i").lower()
            w = "İ" + w[1:] if w.startswith("i") else w[:1].upper() + w[1:]
        out.append(w)
    return " ".join(out)


def turkey():
    """The Grand National Assembly of Turkey (600 seats): tbmm.gov.tr/milletvekili/AllList, the Assembly's own list of sitting members by province
    (name, party, member id). Vacant seats are the 600 minus the names listed."""
    import html as _h
    raw = get("https://www.tbmm.gov.tr/milletvekili/AllList", as_json=False).decode("utf-8")
    PARTY = {"AK Parti": "Justice and Development Party (AK Parti)", "CHP": "Republican People's Party (CHP)", "DEM PARTİ": "Peoples' Equality and Democracy Party (DEM Parti)",
             "MHP": "Nationalist Movement Party (MHP)", "İYİ Parti": "Good Party (İYİ Parti)", "TİP": "Workers' Party of Turkey (TİP)", "EMEP": "Labour Party (EMEP)",
             "BAĞIMSIZ": "Independent", "YENİDEN REFAH": "New Welfare Party (YRP)", "SAADET Partisi": "Felicity Party (Saadet)", "DBP": "Democratic Regions Party (DBP)",
             "DSP": "Democratic Left Party (DSP)", "DP": "Democrat Party (DP)", "HÜDA PAR": "HÜDA PAR", "YENİ YOL": "Yeni Yol group", "Yeni Parti": "Yeni Parti"}
    prov, members = "", []
    for m in re.finditer(r'tbmm-list-item-active"[^>]*>([^<]+)<|href="(/milletvekili/milletvekilidetay\?DonemId=[^"]+&(?:amp;)?Id=([^"&]+))"[^>]*>([^<]+)</a>\s*</div>\s*<div[^>]*>\s*([^<]+?)\s*</div>', raw):
        if m.group(1):
            prov = _h.unescape(m.group(1)).strip()
            continue
        party = _h.unescape(m.group(5)).strip()
        members.append(dict(name=_tr_name(_h.unescape(m.group(4)).strip()), party=PARTY.get(party, party), ref=m.group(3), place=prov, start="",
                            url="https://www.tbmm.gov.tr" + _h.unescape(m.group(2))))
    if len(members) < 500:
        sys.exit(f"Turkey: read {len(members)} members, expected about 590; the page layout may have changed")
    order = ["Peoples' Equality and Democracy Party (DEM Parti)", "Workers' Party of Turkey (TİP)", "Labour Party (EMEP)", "Democratic Regions Party (DBP)", "Republican People's Party (CHP)", "Yeni Parti",
             "Yeni Yol group", "Democratic Left Party (DSP)", "Good Party (İYİ Parti)", "Independent", "Democrat Party (DP)", "Justice and Development Party (AK Parti)",
             "Nationalist Movement Party (MHP)", "New Welfare Party (YRP)", "HÜDA PAR"]
    colours = {"Justice and Development Party (AK Parti)": "f5a000", "Republican People's Party (CHP)": "e30a17", "Peoples' Equality and Democracy Party (DEM Parti)": "7b2d8e",
               "Nationalist Movement Party (MHP)": "b22222", "Good Party (İYİ Parti)": "00a3e0", "Workers' Party of Turkey (TİP)": "d4002a", "Labour Party (EMEP)": "c1121f",
               "Independent": "8a8680", "New Welfare Party (YRP)": "1e7a3c", "Yeni Yol group": "2a9d8f", "Yeni Parti": "264653"}
    return [dict(name="Grand National Assembly of Turkey", level="national", seats=600, source_url="https://www.tbmm.gov.tr/milletvekili/liste",
                 note="600 seats. Sitting members, party and province from the Assembly's own list (tbmm.gov.tr/milletvekili/AllList); seats the list does not name show as Vacant.",
                 role="Member of Parliament", role_re=r"(?i)member of (?:the )?(?:parliament|grand national assembly)|\bTBMM\b|milletvekili", role_start=r"(?i)member of (?:the )?(?:parliament|grand national assembly)",
                 members=members, former=[], party_order=order, colours=colours)]


def algeria_cn():
    """The Conseil de la Nation (174 seats): the council's own list of current members (majliselouma.dz, name and party or 'presidential third'), read once in a
    browser and passed with --local (see skill/references/countries/dz.md): rows of [name in Arabic, party or group, "", member id]."""
    url = "https://www.majliselouma.dz/ara/الأعضاء/HILO1Dbq"
    rows = get(url)
    PARTY = {"حزب جبهة التحرير الوطني": "Front de Libération Nationale (FLN)", "الثلث الرئاسي": "Presidential third", "التجمع الوطني الديمقراطي": "Rassemblement National Démocratique (RND)",
             "جبهة المستقبل": "Front El Moustakbal", "حركة البناء الوطني": "Mouvement El Bina", "جبهة القوى الاشتراكية": "Front des Forces Socialistes (FFS)",
             "حركة مجتمع السلم": "Mouvement de la Société pour la Paix (MSP)", "مجموعة الأحرار": "Independents",
             "تجمع أمل الجزائر": "Tajamou Amal El-Djazair (TAJ)", "حزب صوت الشعب": "Parti Voix du Peuple", "حزب الفجر الجديد": "Parti El Fadjr El Jadid"}
    members = [dict(name=" ".join(r[0].split()), native=" ".join(r[0].split()), party=PARTY.get(" ".join(r[1].split()), " ".join(r[1].split())), ref=r[3], place="", start="",
                    url=f"https://www.majliselouma.dz/ara/members/{r[3]}") for r in rows]
    if len(members) < 100:
        sys.exit(f"Conseil de la Nation: read {len(members)} members, expected about 150; save the list again (see the Algeria guide)")
    return [dict(name="Conseil de la Nation", level="national", seats=174, source_url=url,
                 note="174 seats: two thirds elected by local councillors, one third appointed by the President (the 'presidential third'). Who sits and their party are from the Council's own list of current members (majliselouma.dz), which names about 150; the rest show as Vacant. Unlit seats mean nothing found, never opposition.",
                 role="Membre du Conseil de la Nation", role_re=r"(?i)conseil de la nation|council of the nation|مجلس الأمة", role_start=r"(?i)(membre du conseil de la nation|member of the council of the nation)",
                 members=members, former=[], party_order=["Front des Forces Socialistes (FFS)", "Mouvement de la Société pour la Paix (MSP)", "Mouvement El Bina", "Independents",
                                                           "Front El Moustakbal", "Rassemblement National Démocratique (RND)", "Presidential third", "Front de Libération Nationale (FLN)"],
                 colours={"Front de Libération Nationale (FLN)": "d62718", "Rassemblement National Démocratique (RND)": "1d4e9e", "Presidential third": "8a8680", "Front El Moustakbal": "2a9d8f",
                          "Mouvement El Bina": "1e7a3c", "Front des Forces Socialistes (FFS)": "e63946", "Mouvement de la Société pour la Paix (MSP)": "3b8d3b", "Independents": "b0a99f"})]


def algeria_apn():
    """The Assemblée Populaire Nationale (407 seats): apn.dz does not answer from outside Algeria (DZSecurity), so this draws on Wikidata: the members whose
    position 'Member of the People's National Assembly of Algeria' (Q21290886) started in 2026 and has no end date. Partial; the rest show as 'Not named'."""
    q = ('SELECT ?p ?pLabel ?partyLabel WHERE { ?p p:P39 ?s . ?s ps:P39 wd:Q21290886 . ?s pq:P580 ?start . FILTER(?start >= "2026-01-01T00:00:00Z"^^xsd:dateTime) '
         'OPTIONAL { ?s pq:P582 ?end } FILTER(!BOUND(?end) || ?end > NOW()) OPTIONAL { ?p wdt:P102 ?party } '
         'SERVICE wikibase:label { bd:serviceParam wikibase:language "en,fr,ar". } }')
    d = get("https://query.wikidata.org/sparql?query=" + urllib.parse.quote(q) + "&format=json", headers=WIKI_UA)["results"]["bindings"]
    by = {}
    for x in d:
        qid = x["p"]["value"].rsplit("/", 1)[-1]
        by.setdefault(qid, dict(name=x["pLabel"]["value"], party=x.get("partyLabel", {}).get("value", "Party not given"), qid=qid, ref=qid, place="", start="",
                                url="https://www.wikidata.org/wiki/" + qid))
    members = [m for m in by.values() if not re.match(r"^Q\d+$", m["name"])]
    if len(members) < 20:
        sys.exit(f"APN: read {len(members)} members from Wikidata, expected about 75; check the query")
    return [_upper("Assemblée Populaire Nationale", 407, "https://www.wikidata.org/wiki/Q633590",
                   "407 seats. apn.dz does not answer from outside Algeria, so this chart shows only the members Wikidata records for the Assembly elected in 2026, a small part of the seats; the rest show as 'Not named', which is not the same as vacant. Unlit seats mean nothing found, never opposition.",
                   "Député", r"(?i)assemblée populaire nationale|people's national assembly|\bAPN\b|المجلس الشعبي الوطني", members, {}, vacant="Not named")]


def tunisia_arp():
    """The Assemblée des représentants du peuple (161 seats): arp.tn/parlementaire/groupes lists each member with their bloc and constituency, read once in a
    browser and passed with --local (see skill/references/countries/tn.md): rows of [name in Arabic, bloc, role in the bloc, constituency, member page]."""
    url = "https://www.arp.tn/parlementaire/groupes"
    rows = get(url)
    BLOC = {"غير المنتمين إلى كتل": "Non-affiliated (no bloc)", "كتلة الأحرار": "Free Bloc (Al-Ahrar)", "كتلة الخط الوطني السيادي": "National Sovereign Line Bloc",
            "كتلة الأمانة والعمل": "Al-Amana wal-Amal Bloc", "كتلة لينتصر الشعب": "Bloc Pour que le peuple triomphe", "كتلة الوطنية المستقلة": "Independent National Bloc",
            "كتلة صوت الجمهورية": "Voice of the Republic Bloc", "": "Non-affiliated (no bloc)"}
    members = [dict(name=" ".join(r[0].split()), native=" ".join(r[0].split()), party=BLOC.get(r[1].strip(), r[1].strip()), ref=r[4].rsplit("/", 1)[-1], place=r[3], start="",
                    url="https://www.arp.tn" + r[4]) for r in rows]
    if len(members) < 120:
        sys.exit(f"ARP: read {len(members)} members, expected about 150; save the list again (see the Tunisia guide)")
    order = ["Non-affiliated (no bloc)", "Bloc Pour que le peuple triomphe", "Independent National Bloc", "Free Bloc (Al-Ahrar)", "Voice of the Republic Bloc", "Al-Amana wal-Amal Bloc", "National Sovereign Line Bloc"]
    return [dict(name="Assemblée des représentants du peuple", level="national", seats=161, source_url=url,
                 note="161 seats. Who sits, their bloc and constituency are from the Assembly's own list of blocs (arp.tn), which names about 150 members; the rest show as Vacant. The Assembly publishes blocs, not parties. Unlit seats mean nothing found, never opposition.",
                 role="Member of the Assembly of the Representatives of the People", role_re=r"(?i)assembl[ée]e des repr[ée]sentants|\bARP\b|representatives of the people|مجلس نواب الشعب", role_start=r"(?i)(member of the assembl|membre de l.assembl|member; )",
                 members=members, former=[], party_order=order,
                 colours={"Non-affiliated (no bloc)": "8a8680", "Bloc Pour que le peuple triomphe": "c1121f", "Independent National Bloc": "e07a1f", "Free Bloc (Al-Ahrar)": "2a9d8f",
                          "Voice of the Republic Bloc": "9ccc65", "Al-Amana wal-Amal Bloc": "ef7a85", "National Sovereign Line Bloc": "6c757d"})]


def tunisia_cnrd():
    """The Conseil national des régions et des districts (77 seats): the chamber's own member list (cnrd.tn, name, governorate, development region). No party is given, so
    seats are grouped by development region."""
    import html as _h
    url = "https://www.cnrd.tn/%d9%82%d8%a7%d8%a6%d9%85%d8%a9-%d8%a7%d9%84%d9%86%d9%88%d8%a7%d8%a8/"
    raw = get(url, as_json=False).decode("utf-8")
    REG = {"الأول": "Region 1", "الثاني": "Region 2", "الثالث": "Region 3", "الرابع": "Region 4", "الخامس": "Region 5"}
    members = []
    for tr in re.findall(r"<tr class=\"row-\d+\">(.*?)</tr>", raw, flags=re.S):
        td = [_h.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, flags=re.S)]
        if len(td) < 3 or not td[0]:
            continue
        reg = REG.get(td[2].replace("الإقليم", "").strip(), td[2])
        members.append(dict(name=" ".join(td[0].split()), native=" ".join(td[0].split()), party=reg, ref="", place=td[1], start="", url=url))
    if len(members) < 60:
        sys.exit(f"CNRD: read {len(members)} members, expected 77; the page layout may have changed")
    return [dict(name="Conseil national des régions et des districts", level="national", seats=77, source_url=url,
                 note="77 seats. Who sits and their governorate are from the chamber's own member list (cnrd.tn). The list gives no party, so seats are grouped by development region.",
                 role="Member of the National Council of Regions and Districts", role_re=r"(?i)conseil national des r[ée]gions|national council of regions|\bCNRD\b|المجلس الوطني للجهات والأقاليم", role_start=r"(?i)(member of the national council|chair of the finance committee, conseil national|vice-chair of the finance committee, conseil national)",
                 members=members, former=[], party_order=["Region 1", "Region 2", "Region 3", "Region 4", "Region 5"],
                 colours={"Region 1": "2a9d8f", "Region 2": "e9c46a", "Region 3": "f4a261", "Region 4": "e76f51", "Region 5": "6a4c93"})]


_MA_PARTY = {"حزب التجمع الوطني للأحرار": "Rassemblement National des Indépendants (RNI)", "حزب الاستقلال": "Parti de l'Istiqlal", "حزب الأصالة والمعاصرة": "Parti Authenticité et Modernité (PAM)",
             "حزب الحركة الديمقراطية الاجتماعية": "Mouvement Démocratique et Social (MDS)", "حزب الإنصاف": "Parti de l'Équité (Al Insaf)", "حزب العدالة والتنمية": "Parti de la Justice et du Développement (PJD)",
             "الاتحاد الاشتراكي للقوات الشعبية": "Union Socialiste des Forces Populaires (USFP)", "حزب الحركة الشعبية": "Mouvement Populaire (MP)", "حزب التقدم والاشتراكية": "Parti du Progrès et du Socialisme (PPS)",
             "حزب الاتحاد الدستوري": "Union Constitutionnelle (UC)", "جبهة القوى الديمقراطية": "Front des Forces Démocratiques (FFD)", "حزب الوحدة والديمقراطية": "Parti de l'Unité et de la Démocratie",
             "حزب فيدرالية اليسار الديمقراطي (تحالف اليسار)": "Fédération de la Gauche Démocratique (FGD)", "الحزب الاشتراكي الموحد": "Parti Socialiste Unifié (PSU)", "حزب الديمقراطيين الجدد": "Parti des Démocrates Nouveaux"}


def morocco():
    """The Chambre des Représentants (395 seats): the House's own directory of members for 2026-2031 (chambredesrepresentants.ma, name, party, member page), read once in a
    browser (the site refuses scripts) and passed with --local (see skill/references/countries/ma.md): rows of [name in Arabic, party, member page]."""
    url = "https://www.chambredesrepresentants.ma/ar/دليل-أعضاء-مجلس-النواب/2026-2031"
    rows = get(url)
    members = [dict(name=" ".join(r[0].split()), native=" ".join(r[0].split()), party=_MA_PARTY.get(r[1].strip(), r[1].strip()), ref=r[2].rsplit("/", 1)[-1], place="", start="2026",
                    url="https://www.chambredesrepresentants.ma" + r[2]) for r in rows]
    if len(members) < 300:
        sys.exit(f"Chambre des Représentants: read {len(members)} members, expected about 383; save the list again (see the Morocco guide)")
    left = ["Fédération de la Gauche Démocratique (FGD)", "Parti Socialiste Unifié (PSU)", "Parti du Progrès et du Socialisme (PPS)", "Union Socialiste des Forces Populaires (USFP)"]
    order = left + ["Parti des Démocrates Nouveaux", "Front des Forces Démocratiques (FFD)", "Parti de l'Unité et de la Démocratie", "Parti de la Justice et du Développement (PJD)", "Mouvement Démocratique et Social (MDS)",
                    "Parti de l'Équité (Al Insaf)", "Parti Authenticité et Modernité (PAM)", "Union Constitutionnelle (UC)", "Mouvement Populaire (MP)", "Parti de l'Istiqlal", "Rassemblement National des Indépendants (RNI)"]
    return [dict(name="Chambre des Représentants", level="national", seats=395, source_url=url,
                 note="395 seats, elected in September 2026. Who sits and their party are from the House's own directory of members for 2026-2031 (chambredesrepresentants.ma), which names 383 so far; the rest show as Vacant. Unlit seats mean nothing found, never opposition.",
                 role="Député à la Chambre des Représentants", role_re=r"(?i)chambre des repr[ée]sentants|house of representatives|مجلس النواب", role_start=r"(?i)(d[ée]put[ée]e? à la chambre des repr|member of the house of repr)",
                 members=members, former=[], party_order=order,
                 colours={"Rassemblement National des Indépendants (RNI)": "2b8fd6", "Parti Authenticité et Modernité (PAM)": "7b4b9a", "Parti de l'Istiqlal": "c8102e", "Parti de la Justice et du Développement (PJD)": "f28c28",
                          "Union Socialiste des Forces Populaires (USFP)": "e63946", "Mouvement Populaire (MP)": "3b8d3b", "Parti du Progrès et du Socialisme (PPS)": "b5121b", "Union Constitutionnelle (UC)": "e9c46a",
                          "Fédération de la Gauche Démocratique (FGD)": "9d0208", "Parti Socialiste Unifié (PSU)": "d00000", "Mouvement Démocratique et Social (MDS)": "2a9d8f", "Parti de l'Équité (Al Insaf)": "6c757d"})]


def lebanon():
    """The Parliament of Lebanon (128 seats): lp.gov.lb/Members.aspx, the Parliament's own page of members (name, region, confession; no party). The members sitting carry a region
    and a confession; earlier members are listed on the same page without them. Seats are grouped by the confession each is reserved for."""
    import html as _h
    raw = get("https://www.lp.gov.lb/Members.aspx", as_json=False).decode("utf-8", errors="ignore")
    SECT = {"ماروني": "Maronite", "سني": "Sunni", "شيعي": "Shia", "روم أرثوذكس": "Greek Orthodox", "درزي": "Druze", "روم كاثوليك": "Greek Catholic", "أرمن أرثوذكس": "Armenian Orthodox",
            "علوي": "Alawite", "إنجيلي": "Evangelical", "أرمن كاثوليك": "Armenian Catholic", "أقليات": "Minorities"}
    members, former = [], []
    for b in raw.split("isotope-item")[1:]:
        n, i = re.search(r"<h3>(.*?)</h3>", b, re.S), re.search(r"MemberDetails\.aspx\?Id=(\d+)", b)
        if not (n and i):
            continue
        name = " ".join(_h.unescape(n.group(1)).split())
        reg, sect = re.search(r"<h4>(.*?)</h4>", b, re.S), re.search(r"المذهب:\s*</strong>\s*([^<]*)", b)
        url = f"https://www.lp.gov.lb/MemberDetails.aspx?Id={i.group(1)}"
        if reg and reg.group(1).strip() and sect:
            s = " ".join(_h.unescape(sect.group(1)).split())
            s = SECT.get(s, SECT.get(s.replace("  ", " "), s))
            members.append(dict(name=name, native=name, party=s, ref=i.group(1), place=_h.unescape(reg.group(1)).strip(" ,"), start="", url=url))
        else:
            former.append(dict(name=name, native=name, party="", ref=i.group(1), end="", start="", url=url))
    if len(members) < 100:
        sys.exit(f"Lebanon: read {len(members)} members, expected 128; the page layout may have changed")
    order = ["Shia", "Sunni", "Druze", "Alawite", "Maronite", "Greek Orthodox", "Greek Catholic", "Armenian Orthodox", "Armenian Catholic", "Evangelical", "Minorities"]
    return [dict(name="Parliament of Lebanon (Majlis al-Nuwwab)", level="national", seats=128, source_url="https://www.lp.gov.lb/Members.aspx",
                 note="128 seats, split equally between Christians and Muslims, each reserved for a confession. Who sits is from the Parliament's own page of members (lp.gov.lb); it gives each member's region and confession, not a party, so seats are grouped by confession. Unlit seats mean nothing found, never opposition.",
                 role="Member of Parliament", role_re=r"(?i)member of parliament|parliament of lebanon|مجلس النواب", role_start=r"(?i)member of parliament",
                 members=members, former=former, party_order=order,
                 colours={"Maronite": "b5121b", "Sunni": "2a9d8f", "Shia": "e9c46a", "Greek Orthodox": "7b4b9a", "Druze": "f28c28", "Greek Catholic": "c9184a", "Armenian Orthodox": "6c757d",
                          "Alawite": "3b8d3b", "Evangelical": "2b8fd6", "Armenian Catholic": "9d0208", "Minorities": "b0a99f"})]

def russia():
    """The State Duma (450 seats; duma.gov.ru, the members page of each faction of the 9th convocation, plus the deputies who belong to none) and the
    Federation Council (council.gov.ru, the senators' list: two for each region and up to thirty appointed by the President, no parties)."""
    import html as _html
    FACTION = {"72100024": "United Russia", "72100004": "Communist Party of the Russian Federation", "72100027": "A Just Russia - For Truth",
               "72100005": "Liberal Democratic Party of Russia", "72100035": "New People", "72100011": "Non-attached"}
    members, seen = [], set()
    for fid, party in FACTION.items():
        raw = get(f"http://duma.gov.ru/duma/factions/{fid}/members/", as_json=False).decode("utf-8", errors="replace")
        for blk in raw.split('<li class="list-persons__item">')[1:]:
            m = re.search(r'person__title__link[^>]*href="/duma/persons/(\d+)/".*?<strong>(.*?)</strong><br/><span\s+class="second-name">(.*?)</span>', blk, re.S)
            if not m or m[1] in seen:
                continue
            seen.add(m[1])
            post = re.search(r'class="person__post">(.*?)</div>', blk, re.S)
            place = re.sub(r"^Депутат Государственной Думы\s*", "", _html.unescape(re.sub(r"\s+", " ", post[1])).strip()) if post else ""
            full = _html.unescape(f"{m[2]} {m[3]}").strip()
            if any(x["name"] == full and x["party"] == party and x["place"] == place for x in members):  # one person listed under two ids (Tkachev, New People)
                continue
            members.append(dict(name=full, native=full, party=party, ref=m[1], place=place, start="", url=f"http://duma.gov.ru/duma/persons/{m[1]}/"))
    if len(members) < 400:
        sys.exit(f"State Duma: read {len(members)} deputies, expected about 450; the site has changed, check the adapter")
    raw = get("http://council.gov.ru/structure/members/", as_json=False).decode("utf-8", errors="replace")
    senators = []
    for m in re.finditer(r'href="/structure/persons/(\d+)/"\s+class="group__persons__item[^"]*"\s+data-title="([^"]+)"\s+data-region-id="[^"]*"\s+data-region-title="([^"]*)"', raw):
        n = _html.unescape(m[2]).strip()
        senators.append(dict(name=n, native=n, party="Regional representatives (no party)", ref=m[1], place=_html.unescape(m[3]), start="", url=f"http://council.gov.ru/structure/persons/{m[1]}/"))
    if len(senators) < 150:
        sys.exit(f"Federation Council: read {len(senators)} senators, expected about 170 to 178; the site has changed, check the adapter")
    duma = dict(name="State Duma", level="national", seats=450, source_url="http://duma.gov.ru/duma/deputies/",
                note="450 seats, 9th convocation (elected 18-20 September 2026): 225 by party list and 225 in single-member districts. Who sits and their faction are from the Duma's own pages (duma.gov.ru), one for each faction and one for the deputies in none. Unlit seats mean nothing found, never opposition.",
                role="Member of the State Duma", role_re=r"(?i)state duma|duma deputy|депутат", role_start=r"(?i)member of the (russian )?state duma",
                members=members, former=[], party_order=["Communist Party of the Russian Federation", "A Just Russia - For Truth", "New People", "Non-attached", "Liberal Democratic Party of Russia", "United Russia"],
                colours={"United Russia": "0054a5", "Communist Party of the Russian Federation": "d71a21", "A Just Russia - For Truth": "f5b803", "Liberal Democratic Party of Russia": "003399",
                         "New People": "00a896", "Non-attached": "888888"})
    return [duma,
            _upper("Federation Council", len(senators), "http://council.gov.ru/structure/members/",
                   f"{len(senators)} senators named on the Council's own list (council.gov.ru): two for each region, one from the regional legislature and one from its executive, and up to thirty appointed by the President. Members have no party. Unlit seats mean nothing found, never opposition.",
                   "Member of the Federation Council", r"(?i)federation council|senator|член совета федерации|сенатор", senators, {"Regional representatives (no party)": "7a8f5a"})]


def bulgaria():
    """The Narodno sabranie (240 seats, 52nd National Assembly): the Assembly's open-data endpoint (parliament.bg/api/v1/coll-list-ns/bg) with the 240 members in
    office, their parliamentary group, constituency and the date they joined it. Names are in Cyrillic (upper case), kept as the native name."""
    GROUP = {"3763": "Progressive Bulgaria", "3764": "GERB-SDS", "3766": "Movement for Rights and Freedoms (DPS)", "3767": "Democratic Bulgaria",
             "3765": "We Continue the Change", "3768": "Vazrazhdane"}
    d = get("https://www.parliament.bg/api/v1/coll-list-ns/bg")
    members = []
    for x in d["colListMP"]:
        if x["A_ns_MSP_date_T"] < "9999":
            continue
        native = " ".join(x[f"A_ns_MPL_Name{i}"].strip().title() for i in (1, 2, 3) if x.get(f"A_ns_MPL_Name{i}"))
        members.append(dict(name=native, native=native, party=GROUP.get(str(x["A_ns_C_id"]), re.sub(r'^Парламентарна група( на)?\s*', "", x["A_ns_CL_value"]).strip('"')),
                            ref=str(x["A_ns_MP_id"]), place=x.get("A_ns_Va_name", ""), start=x["A_ns_MSP_date_F"],
                            url=f"https://www.parliament.bg/bg/MP/{x['A_ns_MP_id']}"))
    if len(members) < 200:
        sys.exit(f"Narodno sabranie: read {len(members)} members, expected 240; the endpoint has changed, check the adapter")
    return [dict(name="Narodno sabranie (National Assembly)", level="national", seats=240, source_url="https://www.parliament.bg/bg/MP",
                 note="240 seats, 52nd National Assembly (opened 30 April 2026). Who sits, their parliamentary group and constituency are from the Assembly's own open-data endpoint (parliament.bg/api/v1/coll-list-ns/bg); the start date is the day the member joined the group they are in now. Groups, not parties: DB and PP formed separate groups. Unlit seats mean nothing found, never opposition.",
                 role="Member of the National Assembly", role_re=r"(?i)national assembly|народно събрание|народен представител", role_start=r"(?i)member of the (bulgarian )?national assembly",
                 members=members, former=[],
                 party_order=["Democratic Bulgaria", "We Continue the Change", "Movement for Rights and Freedoms (DPS)", "GERB-SDS", "Vazrazhdane", "Progressive Bulgaria"],
                 colours={"Progressive Bulgaria": "1d4e89", "GERB-SDS": "1f9bd1", "Movement for Rights and Freedoms (DPS)": "7a4cc2", "Democratic Bulgaria": "f2a71b",
                          "We Continue the Change": "e2572e", "Vazrazhdane": "6b6b6b"})]


def _cdep(cam):
    """One chamber of the Romanian Parliament from cdep.ro's alphabetical list: (sitting members, members whose mandate ended, with their end date). Names are
    'Surname Given'; the order of names does not matter to the matcher."""
    import html as _html
    url = "https://www.cdep.ro/ords/pls/parlam/structura2015.de?idl=1" if cam == 2 else "https://www.cdep.ro/ords/pls/parlam/structura2015.de?idl=1&cam=1&leg=2024"
    raw = get(url, as_json=False).decode("utf-8", errors="replace")
    cut = raw.find("ncetat mandatul")  # the second table: 'Deputati/Senatori care si-au incetat mandatul'
    sitting, ended = (raw[:cut], raw[cut:]) if cut > 0 else (raw, "")
    PARTY = {"Neafiliaţi": "Independent", "Neafiliați": "Independent", "Minoritati": "Minorities", "Minorități": "Minorities", "Minorităţi": "Minorities"}

    def iso(d):
        m = re.fullmatch(r"(\d+)\.(\d+)\.(\d{4})", d.strip())
        return f"{m[3]}-{int(m[2]):02d}-{int(m[1]):02d}" if m else ""

    def rows(part, with_end):
        out = []
        for r in re.findall(r'<tr[^>]*>\s*<td width="5%" nowrap>\d+\.</td>(.*?)</tr>', part, re.S):
            m = re.search(r'structura2015\.mp\?idm=(\d+)[^>]*>(.*?)</a>', r, re.S)
            g = re.search(r'structura2015\.gp[^>]*>(.*?)<br>', r, re.S)
            if not m or not g:
                continue
            cells = [re.sub(r"<[^>]+>", "", c).strip() for c in re.findall(r'<td nowrap>(.*?)</td>', r, re.S)]
            place = re.search(r'structura2015\.ce[^>]*>(.*?)</a>', r, re.S)
            party = _html.unescape(g[1]).strip()
            row = dict(name=_html.unescape(re.sub(r"\s+", " ", m[2])).strip(), party=PARTY.get(party, party), ref=m[1],
                       place=_html.unescape(place[1]).strip() if place else "", url=f"https://www.cdep.ro/ords/pls/parlam/structura2015.mp?idm={m[1]}&cam={cam}&leg=2024")
            d = iso(cells[-1]) if cells else ""
            if with_end:
                row["end"], row["start"] = d, ""
            else:
                row["start"] = d or "2024-12-21"
            out.append(row)
        return out
    return rows(sitting, False), rows(ended, True), url


def romania():
    """The Camera Deputaților (330 seats) and the Senatul României (136), both from cdep.ro's alphabetical lists of the 2024 legislature: the sitting members
    (group, constituency, date they joined) and, below them, the members whose mandate ended before the term did (with the end date). senat.ro
    publishes its list only as a postback grid; cdep.ro carries both chambers."""
    out = []
    for cam, name, seats, role, rre in ((2, "Camera Deputaților", 330, "Deputy", r"(?i)\bdeputy\b|deputat|camera deputa|chamber of deputies"), (1, "Senatul României", 136, "Senator", r"(?i)\bsenator|senatul|senate of romania")):
        cur, former, url = _cdep(cam)
        if len(cur) < seats - 10:
            sys.exit(f"{name}: read {len(cur)} members, expected {seats}; the page has changed, check the adapter")
        out.append(dict(name=name, level="national", seats=seats, source_url=url,
                        note=f"{seats} seats, 2024-2028 legislature (first sitting 21 December 2024). Who sits, their group and constituency are from the Chamber of Deputies' own alphabetical list (cdep.ro, which carries both chambers); affiliated members count with their group, and 'Independent' means unaffiliated. Unlit seats mean nothing found, never opposition.",
                        role=role, role_re=rre, role_start=rre, members=cur, former=former,
                        party_order=["Minorities", "USR", "UDMR", "PACE", "UPR", "SOS RO", "Independent", "PNL", "PSD", "AUR"],
                        colours={"PSD": "e4202d", "Minorities": "9e9e9e", "USR": "00aeef", "UDMR": "2e8b57", "PNL": "1d6fb8", "UPR": "c2185b", "SOS RO": "6d4c41", "AUR": "f2a900",
                                 "Independent": "8a8680", "PACE": "7a3e9d"}))
    return out


def slovenia():
    """The Državni zbor (90 seats): the Assembly's open data file SIF.XML (fotogalerija.dz-rs.si/datoteke/opendata/SIF.XML): the persons who are deputies today
    and the deputy group each belongs to. Only the Assembly's own people file is read (names, group, voting district), nothing personal."""
    import xml.etree.ElementTree as ET
    root = ET.fromstring(get("https://fotogalerija.dz-rs.si/datoteke/opendata/SIF.XML", as_json=False))
    GROUP = {"PS030": "Freedom Movement", "PS013": "Social Democrats", "PS026": "Levica", "PS045": "Democrats (Logar)", "PS017": "NSi, SLS and Fokus",
             "PS044": "Resni.ca", "PS012": "Slovenian Democratic Party (SDS)", "PS018": "Italian and Hungarian minorities"}
    groups = {x.findtext("SUBJEKT_FUNKCIJA_SIFRA"): x for x in root.iter("SUBJEKT_FUNKCIJA") if x.findtext("SUBJEKT_FUNKCIJA_TIP") == "PS"}
    of = {}
    for x in root.iter("POVEZAVA"):
        if x.findtext("SUBJEKTI_FUNKCIJA_SIFRA") in groups:
            of[x.findtext("OSEBA_SIFRA")] = x.findtext("SUBJEKTI_FUNKCIJA_SIFRA")
    members = []
    for o in root.iter("OSEBA"):
        sid = o.findtext("OSEBA_SIFRA")
        if o.findtext("OSEBA_JE_POSLANEC") != "1" or sid not in of:
            continue
        g = groups[of[sid]]
        party = GROUP.get(of[sid]) or re.sub(r"^Poslanska skupina\s*", "", g.findtext("SUBJEKT_FUNKCIJA_NAZIV").split("\n")[0]).strip()
        members.append(dict(name=f"{o.findtext('OSEBA_IME').strip()} {o.findtext('OSEBA_PRIIMEK').strip()}", party=party, ref=sid, start="",
                            place=(o.findtext("OSEBA_POSLANSKI_MANDAT/POSLANSKI_MANDAT_OKRAJ_NAZIV") or "").strip(), url="https://www.dz-rs.si/wps/portal/Home/ODDZ/PoslanskeSkupine"))
    if len(members) < 80:
        sys.exit(f"Državni zbor: read {len(members)} deputies, expected 90; the file has changed, check the adapter")
    return [dict(name="Državni zbor (National Assembly)", level="national", seats=90, source_url="https://www.dz-rs.si/wps/portal/Home/ODDZ/PoslanskeSkupine",
                 note="90 seats (88 general plus 2 minority), 10th term (from 10 April 2026). Who sits and their deputy group are from the Assembly's own open data file SIF.XML (dz-rs.si/wps/portal/Home/ostalo/OpenData). The file gives no start date for a deputy, so none is shown. Unlit seats mean nothing found, never opposition.",
                 role="Member of the National Assembly", role_re=r"(?i)national assembly|državni zbor|poslan(ec|ka)", role_start=r"(?i)member of the (slovenian )?national assembly",
                 members=members, former=[],
                 party_order=["Levica", "Social Democrats", "Resni.ca", "Freedom Movement", "Democrats (Logar)", "NSi, SLS and Fokus", "Slovenian Democratic Party (SDS)", "Italian and Hungarian minorities"],
                 colours={"Freedom Movement": "5fb946", "Social Democrats": "e4002b", "Levica": "8b1a2b", "Democrats (Logar)": "7a4cc2", "NSi, SLS and Fokus": "1f6fb4",
                          "Resni.ca": "6b7280", "Slovenian Democratic Party (SDS)": "f5a800", "Italian and Hungarian minorities": "a3a3a3"})]


def croatia():
    """The Hrvatski sabor (151 seats, 11th Sabor): sabor.hr/hr/zastupnici, the Sabor's own list of representatives with their party, electoral district and mandate
    status: active ones sit; those 'U mirovanju' keep their seat while a substitute serves (on leave, not former); 'Završen' ended."""
    import html as _html
    BASE = "https://www.sabor.hr/hr/zastupnici"
    PARTY = {"NZ": "Independent", "DP": "Domovinski pokret", "stranka Nezavisni": "Nezavisni"}

    def read(status):
        out, page, total = [], 0, None
        while total is None or len(out) < total:
            raw = get(f"{BASE}?field_status_mandata_target_id={status}&page={page}", as_json=False).decode("utf-8", errors="replace")
            total = int(re.search(r"Ukupno rezultata:\s*<strong>(\d+)", raw)[1])
            rows = re.findall(r'<tr><td headers="view-field-prezime.*?</tr>', raw, re.S)
            if not rows:
                break
            for r in rows:
                m = re.search(r'href="(/hr/zastupnici/([a-z0-9-]+)-11-saziv)">([^<]+)</a>', r)
                cells = [_html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in re.findall(r'<td headers="view-view-sabor-data-[12][^>]*>(.*?)</td>', r, re.S)]
                if not m or len(cells) < 2:
                    continue
                sur, _, given = _html.unescape(m[3]).partition(",")
                out.append(dict(name=f"{given.strip()} {sur.strip()}", party=PARTY.get(cells[0], cells[0]), ref=m[2], place=cells[1], start="", url="https://www.sabor.hr" + m[1]))
            page += 1
        return out
    members = read(104)
    if len(members) < 130:
        sys.exit(f"Sabor: read {len(members)} active representatives, expected about 150; the site has changed, check the adapter")
    former = [dict(m, on_leave=True) for m in read(106)] + [dict(m, end="") for m in read(108)]
    return [dict(name="Hrvatski sabor", level="national", seats=151, source_url="https://www.sabor.hr/hr/zastupnici",
                 note="151 seats, 11th Sabor (from 16 May 2024). Who sits (mandate status 'Aktivan', a substitute counting for a member on leave) and their party are from the Sabor's own list of representatives (sabor.hr); the list gives no start date. A seat the list does not account for shows as Vacant. Unlit seats mean nothing found, never opposition.",
                 role="Member of the Croatian Parliament", role_re=r"(?i)sabor|croatian parliament|zastupnik", role_start=r"(?i)member of the (croatian parliament|sabor)",
                 members=members, former=former,
                 party_order=["HDZ", "Domovinski pokret", "Most", "Independent", "SDSS", "SDP", "Možemo!"],
                 colours={"HDZ": "1f4fa3", "SDP": "e4002b", "Domovinski pokret": "0d6b3d", "Most": "f08a00", "Možemo!": "6dc04b", "Independent": "8a8680"})]


def _parlament_ba(kind):
    """The Parliamentary Assembly of Bosnia and Herzegovina's own list (parlament.ba/<kind>/List, ten rows a page): (sitting members, ended ones with their end date).
    A name may carry '* do 10.10.2024.' (until) or '* član od 10.10.2024.' (from); the party is the badge, or the club when none is shown."""
    import html as _html

    def iso(d):
        m = re.fullmatch(r"(\d+)\.(\d+)\.(\d{4})\.?", d.strip())
        return f"{m[3]}-{int(m[2]):02d}-{int(m[1]):02d}" if m else ""
    PARTY = {"HDZ BiH, HSS, HSP BiH, HKDU, HSPAS, HDU, HSPHB, HRAST": "HDZ BiH coalition", "ŽELJKO KOMŠIĆ – ZA GRAĐANSKU DRŽAVU – DF/GS": "DF - Komšić",
             "NES - Za nove generacije": "NES", "Bosanskohercegovačka inicijativa - Kasumović Fuad": "BH Initiative - Kasumović", "DF": "DF - Komšić", "Nezavisni delegat": "Independent",
             "ZA PRAVDU I RED - Lista Nebojše Vukanovića": "Za pravdu i red (Vukanović)"}
    cur, former, page = [], [], 1
    while page < 12:
        raw = get(f"https://www.parlament.ba/{kind}/List?page={page}", as_json=False).decode("utf-8", errors="replace")
        rows = re.findall(r'<tr class="[^"]*"\s*>(.*?)</tr>', raw, re.S)
        if not rows:
            break
        for r in rows:
            m = re.search(rf'href="/{kind}/detail/(\d+)\s*"', r)
            t = [_html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", c))).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)]
            if not m or len(t) < 5:
                continue
            nm, club, badge, place = t[1], t[2], t[3], t[4]
            end = start = ""
            e = re.search(r"\*\s*do\s+([\d.]+)", nm)
            f = re.search(r"\*\s*član od\s+([\d.]+)", nm)
            if e:
                end = iso(e[1])
            if f:
                start = iso(f[1])
            nm = re.sub(r"\s*\*.*$", "", nm).strip()
            sur, _, given = nm.partition(",")
            party = PARTY.get(badge, badge) or (re.sub(r"^Klub poslanika\s*", "", club) if "Naša stranka" in club else "No party shown")
            row = dict(name=f"{given.strip()} {sur.strip()}".strip(), party=party, ref=m[1], place=place, start=start, url=f"https://www.parlament.ba/{kind}/detail/{m[1]}")
            if end:
                row["end"] = end
                former.append(row)
            else:
                cur.append(row)
        page += 1
    return cur, former


def bosnia():
    """Bosnia and Herzegovina: the House of Representatives (42) and the House of Peoples (15) of the Parliamentary Assembly (parlament.ba's own lists) and the House
    of Representatives of the Federation (98; predstavnickidom-pfbih.gov.ba/zastupnici, members grouped by party). The Federation's House of Peoples
    (80 delegates) publishes no current list (its site shows the 2014-2018 term), so it has no chart."""
    import html as _html
    hor, hor_former = _parlament_ba("representative")
    hop, hop_former = _parlament_ba("delegate")
    if len(hor) < 38 or len(hop) < 12:
        sys.exit(f"Parlamentarna skupština: read {len(hor)} representatives and {len(hop)} delegates, expected 42 and 15; the site has changed, check the adapter")
    FB = {"SDA - STRANKA DEMOKRATSKE AKCIJE": "SDA", "HDZ BIH,HSSSR,HSS,HSP BIH,HKDU,HSPAS,HDU,HSPHB,HRAST,HNL": "HDZ BiH coalition", "SDP - SOCIJALDEMOKRATSKA PARTIJA BOSNE I HERCEGOVINE": "SDP BiH",
          "ŽELJKO KOMŠIĆ - ZA GRAĐANSKU DRŽAVU - DF/GS": "DF - Komšić", "POVJERENJE! (NAROD I PRAVDA, SPU BIH)": "Povjerenje! (Narod i pravda, SPU BiH)", "NAŠA STRANKA": "Naša stranka",
          "NES - ZA EVROPSKU BIH": "NES", "STRANKA ZA BOSNU I HERCEGOVINU-SBIH": "SBiH", "HRVATSKA DEMOKRATSKA ZAJEDNICA 1990 - HDZ 1990": "HDZ 1990",
          "BOSANSKOHERCEGOVAČKA INICIJATIVA - KASUMOVIĆ FUAD": "BH Initiative - Kasumović", "HNP - HRVATSKI NACIONALNI POMAK": "HNP", "HRVATSKA REPUBLIKANSKA STRANKA": "HRS",
          "POKRET DEMOKRATSKE AKCIJE - PDA": "PDA", "NEZAVISNI POSLANICI/NEOVISNI ZASTUPNICI": "Independent"}
    furl = "https://predstavnickidom-pfbih.gov.ba/zastupnici"
    raw = get(furl, as_json=False).decode("utf-8", errors="replace")
    fb = []
    for blk in raw.split('<h6 class="toggle-title">')[1:]:
        title = re.sub(r"\s+", " ", _html.unescape(blk.split("</h6>")[0])).strip()
        for n in re.findall(r"<td>([^<]+)</td>\s*<td>\s*<a href=\"mailto", blk):
            n = re.sub(r"\s+", " ", _html.unescape(n)).strip()
            fb.append(dict(name=n, party=FB.get(title, title), ref=n, place="", start="", url=furl))
    if len(fb) < 90:
        sys.exit(f"Predstavnički dom PFBiH: read {len(fb)} members, expected 98; the page has changed, check the adapter")
    cols = {"SDA": "1f8a4c", "SNSD": "1f4fa3", "SDP BiH": "e4002b", "HDZ BiH coalition": "2b3a8c", "DF - Komšić": "9b59b6", "SDS": "c0392b", "PDP": "6a7fb5", "Naša stranka": "f5a800",
            "NES": "7f8c8d", "Narod i pravda": "e67e22", "BH Initiative - Kasumović": "16a085", "HDZ BiH": "2b3a8c", "Independent": "8a8680", "No party shown": "bdbdbd"}
    tail = "Unlit seats mean nothing found, never opposition."
    return [dict(name="Predstavnički dom Parlamentarne skupštine BiH (House of Representatives)", level="national", seats=42, source_url="https://www.parlament.ba/representative/list",
                 note="42 seats (28 from the Federation, 14 from Republika Srpska), the 2022-2026 term. Members and parties from the Parliamentary Assembly's own list of representatives (parlament.ba/representative/list); the party is the badge on the list, and 'No party shown' where it has none. General elections were held in October 2026; this is the outgoing house until the new one is constituted. " + tail,
                 role="Member of the House of Representatives of Bosnia and Herzegovina", role_re=r"(?i)house of representatives of (bosnia|the parliamentary)|predstavni.ki dom (parlamentarne|pskbih)|parliamentary assembly of bosnia",
                 role_start=r"(?i)member of the house of representatives of bosnia", members=hor, former=hor_former, party_order=["Naša stranka", "SDP BiH", "DF - Komšić", "SDA", "SNSD", "HDZ BiH coalition"], colours=cols),
            dict(name="Dom naroda Parlamentarne skupštine BiH (House of Peoples)", level="national", seats=15, source_url="https://www.parlament.ba/delegate/list",
                 note="15 seats (5 delegates for each constituent people), the 2022-2026 term. Delegates and parties from the Parliamentary Assembly's own list (parlament.ba/delegate/list); a delegate who has left shows as former with the end date. General elections were held in October 2026; this is the outgoing house until the new one is constituted. " + tail,
                 role="Delegate to the House of Peoples of Bosnia and Herzegovina", role_re=r"(?i)house of peoples of (bosnia|the parliamentary)|dom naroda (parlamentarne|pskbih)",
                 role_start=r"(?i)delegate to the house of peoples of bosnia", members=hop, former=hop_former, colours=cols),
            dict(name="Predstavnički dom Parlamenta Federacije BiH (FBiH House of Representatives)", level="regional", seats=98, source_url=furl,
                 note="98 seats, the 2022-2026 term. Members and their party are from the House's own list of representatives (predstavnickidom-pfbih.gov.ba/zastupnici), which groups them by party; it gives no constituency or start date. Outgoing house until the result of the October 2026 elections is constituted. " + tail,
                 role="Member of the House of Representatives of the FBiH Parliament", role_re=r"(?i)house of representatives of the (fbih|federation)|fbih house of representatives|predstavni.ki dom (parlamenta|pfbih)",
                 role_start=r"(?i)member,? (of the )?house of representatives of the fbih", members=fb, former=[], colours=cols)]


def greece():
    """The Hellenic Parliament (300 seats): hellenicparliament.gr/Vouleftes/Ana-Koinovouleftiki-Omada lists the sitting members group by group, ten to a page. The site
    refuses scripts, so it is read once in a browser and passed with --local (see skill/references/countries/gr.md): {groups, rows: [group, name in Greek, constituency, member id]}.
    Names are 'Surname Father's-name Given', in Greek; the register carries the Greek name in brackets."""
    url = "https://www.hellenicparliament.gr/Vouleftes/Ana-Koinovouleftiki-Omada"
    d = get(url)
    PARTY = {"ΝΕΑ ΔΗΜΟΚΡΑΤΙΑ": "New Democracy", "ΠΑΣΟΚ-ΚΙΝΗΜΑ ΑΛΛΑΓΗΣ": "PASOK", "ΚΟΜΜΟΥΝΙΣΤΙΚΟ ΚΟΜΜΑ ΕΛΛΑΔΑΣ": "Communist Party of Greece",
             "ΣΥΝΑΣΠΙΣΜΟΣ ΡΙΖΟΣΠΑΣΤΙΚΗΣ ΑΡΙΣΤΕΡΑΣ - ΠΡΟΟΔΕΥΤΙΚΗ ΣΥΜΜΑΧΙΑ": "SYRIZA", "ΕΛΛΗΝΙΚΗ ΛΥΣΗ - ΚΥΡΙΑΚΟΣ ΒΕΛΟΠΟΥΛΟΣ": "Greek Solution",
             'ΔΗΜΟΚΡΑΤΙΚΟ ΠΑΤΡΙΩΤΙΚΟ ΚΙΝΗΜΑ "ΝΙΚΗ"': "NIKI", "ΠΛΕΥΣΗ ΕΛΕΥΘΕΡΙΑΣ-ΖΩΗ ΚΩΝΣΤΑΝΤΟΠΟΥΛΟΥ": "Course of Freedom", "ΑΝΕΞΑΡΤΗΤΟΙ": "Independent"}
    members = [dict(name=r[1], native=r[1], party=PARTY.get(r[0], r[0]), ref=r[3], place=r[2], start="",
                    url=f"https://www.hellenicparliament.gr/Vouleftes/Ana-Koinovouleftiki-Omada?MPId={r[3]}") for r in d["rows"]]
    if len(members) < 280:
        sys.exit(f"Hellenic Parliament: read {len(members)} members, expected about 297; save the lists again (see the Greece guide)")
    return [dict(name="Hellenic Parliament", level="national", seats=300, source_url=url,
                 note="300 seats. Who sits and their parliamentary group are from the Parliament's own list of members by parliamentary group (hellenicparliament.gr), read in a browser because the site refuses scripts; 'Independent' means members outside any group. Seats the list does not name show as Vacant. Unlit seats mean nothing found, never opposition.",
                 role="Member of the Hellenic Parliament", role_re=r"(?i)\bmp for\b|hellenic parliament|member of (the )?(greek )?parliament|βουλευτ", role_start=r"(?i)(member of (the )?(hellenic|greek) parliament|mp for)",
                 members=members, former=[],
                 party_order=["Communist Party of Greece", "SYRIZA", "PASOK", "Course of Freedom", "Independent", "New Democracy", "Greek Solution", "NIKI"],
                 colours={"Communist Party of Greece": "d71920", "SYRIZA": "e6332a", "PASOK": "009b48", "Course of Freedom": "792c91", "Independent": "a8adb3",
                          "New Democracy": "1b78c8", "Greek Solution": "073a84", "NIKI": "274c77"})]


def hungary():
    """The Országgyűlés (199 seats): parlament.hu/aktiv-kepviselok-listaja, the active representatives with their party. The site answers scripts with a CAPTCHA, so a
    person solves it once in a browser and the list is read there and passed with --local (see skill/references/countries/hu.md): rows of [party, name].
    The 13 nationality spokespersons have no vote and are not on the list."""
    url = "https://www.parlament.hu/aktiv-kepviselok-listaja"
    rows = get(url)
    PARTY = {"TISZA": "Tisza", "Fidesz": "Fidesz", "KDNP": "KDNP", "Mi Hazánk": "Mi Hazánk"}
    members = [dict(name=r[1], party=PARTY.get(r[0], r[0]), ref=r[1], place="", start="", url=url) for r in rows]
    if len(members) < 190:
        sys.exit(f"Országgyűlés: read {len(members)} representatives, expected 199; save the list again (see the Hungary guide)")
    return [dict(name="Országgyűlés (National Assembly)", level="national", seats=199, source_url=url,
                 note="199 seats, 2026-2030 term. Who sits and their party are from the Assembly's own list of active representatives (parlament.hu/aktiv-kepviselok-listaja), read in a browser after its CAPTCHA was solved by a person; the list gives no start date. Fidesz and KDNP sit as one group. The 13 nationality spokespersons have no vote and are not counted. Unlit seats mean nothing found, never opposition.",
                 role="Member of the National Assembly", role_re=r"(?i)national assembly|országgyűlés|\bmp\b", role_start=r"(?i)member of the (hungarian )?national assembly",
                 members=members, former=[], party_order=["Tisza", "Mi Hazánk", "KDNP", "Fidesz"],
                 fuzzy_deny=["Tímea Szabó"],  # a former Párbeszéd member, not Tímea Barna-Szabó (Tisza)
                 colours={"Tisza": "1db5e8", "Mi Hazánk": "6b8e23", "KDNP": "e3a900", "Fidesz": "fd8100"})]


def slovakia():
    """The Národná rada (150 seats): nrsr.sk's alphabetical list of deputies with each deputy's club. The site answers scripts with a bot check (not bypassed), so the
    list is read once in a browser and passed with --local (see skill/references/countries/sk.md): rows of ["Surname, Given", deputy id, club]."""
    url = "https://www.nrsr.sk/web/Default.aspx?sid=poslanci/zoznam_abc"
    rows = get(url)
    CLUB = {"Klub SMER - sociálna demokracia": "Smer – Social Democracy", "Klub Sloboda a Solidarita": "Freedom and Solidarity", "Klub Slovenská národná strana": "SNS", "Klub KDH": "KDH",
            "Klub HLAS - sociálna demokracia": "Hlas – Social Democracy", "Klub Progresívne Slovensko": "Progressive Slovakia", "Klub SLOVENSKO - ZA ĽUDÍ": "Slovakia – For the People",
            "Poslanci, ktorí nie sú členmi poslaneckých klubov": "Non-attached"}
    members = []
    for r in rows:
        sur, _, given = r[0].partition(",")
        members.append(dict(name=f"{given.strip()} {sur.strip()}", party=CLUB.get(r[2], r[2]), ref=r[1],
                            place="", start="", url=f"https://www.nrsr.sk/web/Default.aspx?sid=poslanci/poslanec&PoslanecID={r[1]}"))
    if len(members) < 140:
        sys.exit(f"Národná rada: read {len(members)} deputies, expected 150; save the list again (see the Slovakia guide)")
    return [dict(name="Národná rada (National Council)", level="national", seats=150, source_url=url,
                 note="150 seats. Who sits is from the National Council's own alphabetical list of deputies (nrsr.sk) and each deputy's club from the club pages, read in a browser because the site answers scripts with a bot check. 'Non-attached' means deputies in no club. Unlit seats mean nothing found, never opposition.",
                 role="Member of the National Council", role_re=r"(?i)national council|národná rada|\bmp\b", role_start=r"(?i)member of the (slovak )?national council",
                 members=members, former=[],
                 party_order=["Progressive Slovakia", "Freedom and Solidarity", "Slovakia – For the People", "KDH", "Non-attached", "Hlas – Social Democracy", "Smer – Social Democracy", "SNS"],
                 colours={"Progressive Slovakia": "00a3dd", "Freedom and Solidarity": "66ccff", "Slovakia – For the People": "f08a00", "KDH": "ffd500", "Non-attached": "999999",
                          "Hlas – Social Democracy": "c8102e", "Smer – Social Democracy": "e2231a", "SNS": "003a79"})]


def north_macedonia():
    """The Sobranie (120 seats): sobranie.mk/mps-en.nspx lists the 120 members with their party (an Angular page that loads its rows with a 'Show more' button), read once in a
    browser and passed with --local (see skill/references/countries/mk.md): rows of [name, party, member id]. Names are in Latin."""
    url = "https://www.sobranie.mk/mps-en.nspx"
    rows = get(url)
    PARTY = {"Movement BESA": "BESA Movement", "VMRO – DPMNE": "VMRO-DPMNE", "Democratic Union on Integration": "DUI", "Независни пратеници": "Independent", "": "Independent",
             "Social Democratic Union of Macedonia": "SDSM", "Liberal – Democratic Party": "Liberal Democratic Party"}
    members = [dict(name=r[0].replace("М", "M"), party=PARTY.get(r[1], r[1]), ref=r[2], place="", start="",  # a Cyrillic capital Em in "Mile Talevski"
                    url=f"https://www.sobranie.mk/mps-details.nspx?param={r[2]}") for r in rows]
    if len(members) < 110:
        sys.exit(f"Sobranie: read {len(members)} members, expected 120; save the list again (see the North Macedonia guide)")
    return [dict(name="Sobranie (Assembly of North Macedonia)", level="national", seats=120, source_url=url,
                 note="120 seats. Who sits and their party are from the Assembly's own list of members (sobranie.mk), read in a browser because the list is built by script. 'Independent' means members the list shows with no party or as independents. Unlit seats mean nothing found, never opposition.",
                 role="Member of the Assembly", role_re=r"(?i)member of the assembly|sobranie|\bmp\b|собрание", role_start=r"(?i)member of the (macedonian )?assembly",
                 members=members, former=[],
                 party_order=["Levica", "SDSM", "DUI", "Independent", "VMRO-DPMNE"],
                 colours={"VMRO-DPMNE": "9b1c1c", "SDSM": "e4002b", "DUI": "2e8b57", "Levica": "8b1a2b", "Independent": "bdbdbd", "Movement ZNAM": "c9a227", "BESA Movement": "1f6fb4"})]


_ADAPTERS_LOWER = {"at": austria, "austria": austria, "cz": czechia, "czechia": czechia, "nz": new_zealand, "se": sweden, "de": germany, "nl": netherlands, "no": norway, "fr": france, "br": brazil, "ca": canada, "es": spain, "pl": poland, "be": belgium, "in": india, "jp": japan, "my": malaysia, "sg": singapore, "id": indonesia, "ng": nigeria, "cn": china, "scottish_parliament": scottish_parliament, "european_parliament": european_parliament, "eu": european_parliament, "un": united_nations, "au": pan_african_parliament, "za": south_africa, "ie": ireland, "it": italy, "mx": mexico, "ar": argentina, "co": colombia, "fi": finland, "kr": south_korea}
# countries that chart two chambers chain their adapters; the others return one
ADAPTERS = dict(_ADAPTERS_LOWER, nl=lambda: netherlands() + netherlands_senate(), za=lambda: south_africa() + south_africa_ncop(),
                  ca=lambda: canada() + canada_senate(), australia=australia, eg=egypt,
                  ng=lambda: nigeria() + nigeria_senate(),
                  es=lambda: spain() + spain_senate(), pl=lambda: poland() + poland_senate(), belgium_senate=belgium_senate,  # the Chamber needs its own saved page: run the Senate with --adapter belgium_senate
                  id=lambda: indonesia() + indonesia_dpd(), egypt_senate=egypt_senate, malaysia_senate=malaysia_senate, ch=switzerland,
                  pt=portugal, dk=denmark, **{"is": iceland}, lu=luxembourg, mt=malta, ee=estonia, lt=lithuania)  # the Dewan Rakyat needs its own saved page: run the Dewan Negara with --adapter malaysia_senate

ADAPTERS.update(tr=turkey, dz=lambda: algeria_apn() + algeria_cn(), tn=lambda: tunisia_arp() + tunisia_cnrd(), ma=morocco, lb=lebanon,
                algeria_apn=algeria_apn, algeria_cn=algeria_cn, tunisia_cnrd=tunisia_cnrd, tunisia_arp=tunisia_arp)


# ---------------------------------------------------------------- adapters added in the November 2026 seat-gap pass
def _saved(url):
    """A list read once in a browser and passed with --local URL=FILE: the JSON, or the text/plain form post the browser sent to the receiver ("x=[...]")."""
    raw = get(url, as_json=False).decode("utf-8-sig").strip()
    return json.loads(raw[2:] if raw.startswith("x=") else raw)


_HONORIFICS = {"hon", "rt", "sen", "dr", "prof", "eng", "engr", "amb", "capt", "col", "rtd", "mp", "cbs", "egh", "mgh", "ogw", "ebs", "mbs", "cgh", "hsc", "mr", "mrs", "ms", "mst",
               "md", "barrister", "advocate", "alhaj", "haji", "atty", "dpa", "rn", "fpso", "hns", "cs", "lt", "gen", "maj", "brig"}


def _plain(name, drop=_HONORIFICS):
    """A name without titles, credentials or (bracketed) notes, and without single-letter initials."""
    s = re.sub(r"\([^)]*\)", " ", name.replace("�", "").replace('"', " ").replace("“", " ").replace("”", " "))  # a nickname in quotes stays: the register often uses it
    out = []
    for w in re.sub(r"[,;]", " ", s).split():
        k = w.replace(".", "").lower()
        if k in drop or len(k) <= 1:
            continue
        out.append(w.strip())
    return " ".join(out)


def philippines():
    """The House of Representatives (318 seats): congress.gov.ph/house-members, behind a Cloudflare check, so it is read in a browser and passed with --local
    (see the Philippines guide): rows of [member id, "Surname, Given", type, place or party-list]. The members the page hides under 'Inactive' are left out.
    The site gives no party for district members, so seats are grouped as district and party-list."""
    url = "https://www.congress.gov.ph/house-members"
    members = []
    for r in _saved(url):
        mid, name, rest = r[0], r[1], r[2:]
        if rest[0].upper().startswith("SPEAKER"):
            rest = rest[1:]
        kind, place = rest[0], rest[1]
        sur, _, given = name.partition(",")
        members.append(dict(name=_plain(f"{given} {sur}"), party="Party-list" if kind.startswith("Party") else "District", ref=mid,
                            place=place, start="", url=f"https://www.congress.gov.ph/house-members/view/{mid}"))
    if len(members) < 280:
        sys.exit(f"Philippine House: read {len(members)} members, expected about 317; save the list again (see the Philippines guide)")
    return [dict(name="House of Representatives", level="national", seats=318, source_url=url,
                 note="318 seats: 253 district and 65 party-list (20th Congress, from 30 June 2025). Who sits is from the House's own list (congress.gov.ph); the site names the party-list group of a party-list member and no party for a district member, so seats are grouped as district and party-list. Members the site shows as inactive are left out and their seats show as Vacant. Unlit seats mean nothing found, never opposition.",
                 role="Representative", role_re=r"(?i)representative", role_start=r"(?i)(party-list )?representative",
                 members=members, former=[], party_order=["Party-list", "District"], keep_party=True,  # the register records each supporter's own party
                 colours={"District": "1a5fb4", "Party-list": "e07a1f"})]


def pakistan():
    """The National Assembly (336 seats): na.gov.pk/en/all_members.php lists every member under province and reserved-seat headings. The site does not answer
    scripts from every network, so it is read in a browser and passed with --local: rows of [heading, constituency, name, party, profile link]."""
    url = "https://www.na.gov.pk/en/all_members.php"
    PARTY = {"PML (N)": "PML-N", "PPPP": "PPP", "JUI (P)": "JUI-F", "IND": "Independent", "MQM": "MQM-P", "PML": "PML-Q"}
    members = []
    for r in _saved(url):
        if r[3] == "Party":  # a repeated header row
            continue
        place = r[1] if not r[1].isdigit() else re.sub(r"\s*\(\d+\)", "", r[0]).title()
        members.append(dict(name=_plain(r[2]), party=PARTY.get(r[3], r[3]), ref=r[4].rsplit("=", 1)[-1], place=place, start="",
                            url="https://www.na.gov.pk/en/" + r[4]))
    if len(members) < 300:
        sys.exit(f"National Assembly of Pakistan: read {len(members)} members, expected about 332; save the list again (see the Pakistan guide)")
    return [dict(name="National Assembly", level="national", seats=336, source_url=url,
                 note="336 seats: 266 general, 60 reserved for women and 10 for non-Muslims. Who sits and their party are from the Assembly's own list of members (na.gov.pk); seats the list does not fill show as Vacant. Independent is how the Assembly lists members elected as independents, among them many backed by the PTI. Unlit seats mean nothing found, never opposition.",
                 role="Member of the National Assembly", role_re=r"(?i)\bMNA\b|national assembly", role_start=r"(?i)(MNA|member of the national assembly)",
                 members=members, former=[], party_order=["MQM-P", "JUI-F", "IPP", "SIC", "Independent", "PPP", "PML-N"],
                 colours={"PML-N": "1b9c4a", "PPP": "d62828", "Independent": "8a8680", "MQM-P": "2a9d8f", "JUI-F": "3a5a40", "IPP": "9a7b4f", "SIC": "6a4c93"})]


def pakistan_senate():
    """The Senate (96 seats): senate.gov.pk/en/current_members.php (read in a browser and passed with --local if it does not answer): rows of
    [number, name, tenure, party, province, profile link]."""
    url = "https://www.senate.gov.pk/en/current_members.php"
    members = []
    for r in _saved(url):
        ab = re.search(r"\(([A-Z]+)\)\s*$", r[3])
        party = {"PPPP": "PPP", "PMLN": "PML-N", "IND": "Independent", "JUIP": "JUI-F", "MQMP": "MQM-P", "PML": "PML-Q"}.get(ab.group(1), ab.group(1)) if ab else r[3]
        members.append(dict(name=_plain(re.sub(r"\(.*", "", r[1])), party=party, ref=r[5].split("uid=")[-1].split("&")[0], place=r[4], start="",
                            url="https://www.senate.gov.pk/en/" + r[5]))
    if len(members) < 80:
        sys.exit(f"Senate of Pakistan: read {len(members)} senators, expected about 95; save the list again (see the Pakistan guide)")
    return [_upper("Senate", 96, url, "96 seats: 23 for each of the four provinces and 4 for the Islamabad Capital Territory. Who sits and their party are from the Senate's own list of members (senate.gov.pk); seats it does not list show as Vacant. Unlit seats mean nothing found, never opposition.",
                   "Senator", r"(?i)\bsenator\b", members,
                   {"PML-N": "1b9c4a", "PPP": "d62828", "Independent": "8a8680", "PTI": "e9c46a", "JUI-F": "3a5a40", "BAP": "9a7b4f", "ANP": "c1121f", "MQM-P": "2a9d8f"})]


def bangladesh():
    """The Jatiya Sangsad (350 seats): parliament.gov.bd/members/list-of-members, ten members to a page. The page is a script-driven table, so it is read once
    in a browser (clicking through the pages) and passed with --local as {serial: [name, party, constituency]}."""
    url = "https://www.parliament.gov.bd/members/list-of-members"
    SHORT = {"Bangladesh Nationalist Party (BNP)": "BNP", "Bangladesh Jamaat-E-Islami (BJEI)": "Jamaat-e-Islami", "National Citizens Party-NCP": "NCP",
             "Bangladesh Khilafat Majlis": "Khilafat Majlis", "Khilafat Majlis": "Khilafat Majlis", "Independent": "Independent"}
    members = [dict(name=_plain(v[0]), party=SHORT.get(v[1], v[1]), ref=k, place=v[2], start="", url=url) for k, v in _saved(url).items()]
    if len(members) < 300:
        sys.exit(f"Jatiya Sangsad: read {len(members)} members, expected about 349; save the list again (see the Bangladesh guide)")
    return [dict(name="Jatiya Sangsad", level="national", seats=350, source_url=url,
                 note="350 seats: 300 elected by constituency and 50 reserved for women. Who sits and their party are from the Sangsad's own list of current members (parliament.gov.bd); seats the list does not fill show as Vacant. Unlit seats mean nothing found, never opposition.",
                 role="Member of Parliament", role_re=r"(?i)member of parliament|jatiya sangsad", role_start=r"(?i)member of parliament",
                 members=members, former=[], party_order=["NCP", "Independent", "Khilafat Majlis", "Jamaat-e-Islami", "BNP"],
                 colours={"BNP": "1b9c4a", "Jamaat-e-Islami": "e07a1f", "NCP": "d62828", "Independent": "8a8680", "Khilafat Majlis": "3a5a40"})]


def _kenya_rows(path, senate=False):
    """Every row of the parliament's paged member table: (cells, member page path)."""
    rows = []
    for p in range(0, 60):
        t = get(f"https://www.parliament.go.ke/{path}?field_name_value=%20&field_parliament_value=2022&field_employment_history_value=&page={p}", as_json=False).decode("utf-8", "replace")
        if senate:
            t = t.split('<table class="cols-6', 1)[-1]
        got = re.findall(r"<tr[^>]*>(.*?)</tr>", t, re.S)
        n = 0
        for r in got:
            link = re.search(r'href="(/the-(?:senate|national-assembly)/[^"]+)"', r)
            c = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)]
            if link and c and ("class=\"mp" in r or "hreflang" in r) and (c[0] or senate) and "pdf" not in r:
                rows.append((c, link.group(1)))
                n += 1
        if not re.search(rf"page={p + 1}\"", t):
            break
    return rows


def kenya():
    """The National Assembly (349 seats): parliament.go.ke/the-national-assembly/mps, the table of members of the 13th Parliament (10 a page)."""
    members, seen = [], set()
    for c, link in _kenya_rows("the-national-assembly/mps"):
        name = c[0]
        if not name or re.match(r"(?i)vacant", name):
            continue
        county, const, party = c[2], c[3], re.sub(r"\s*\|.*", "", c[4]).strip()
        key = const if const and const != county else name.lower()  # the page lists some seats twice
        if key in seen:
            continue
        seen.add(key)
        party = {"IND.": "IND", "FORD - K": "FORD-K"}.get(party, party) or "Party not listed"
        members.append(dict(name=_plain(name), party=party, ref=link.rsplit("/", 1)[-1], place=const or county or "Nominated", start="", url="https://www.parliament.go.ke" + link))
    if len(members) < 300:
        sys.exit(f"Kenya National Assembly: read {len(members)} members, expected about 349")
    return [dict(name="National Assembly of Kenya", level="national", seats=349, source_url="https://www.parliament.go.ke/the-national-assembly/mps",
                 note="349 seats: 290 constituencies, 47 county women representatives and 12 nominated. Who sits and their party are from the Assembly's own table of members (parliament.go.ke); a few rows leave the party blank and show as 'Party not listed'. Unlit seats mean nothing found, never opposition.",
                 role="Member of the National Assembly", role_re=r"(?i)national assembly|\bMP\b|member of parliament", role_start=r"(?i)(member of the national assembly|MP\b|member of parliament)",
                 members=members, former=[], party_order=["Party not listed", "IND", "UDA", "ODM"],
                 colours={"UDA": "f4c20d", "ODM": "f28c1f", "JP": "d62828", "WDM": "2a9d8f", "IND": "8a8680", "UDM": "1b9c4a", "KANU": "c1121f"})]


def kenya_senate():
    """The Senate (67 seats): parliament.go.ke/the-senate/senators."""
    members = []
    for c, link in _kenya_rows("the-senate/senators", senate=True):
        cells = [x for x in c if x]
        if len(cells) < 3:
            continue
        members.append(dict(name=_plain(cells[0]), party=re.sub(r"[()]", "", cells[2]).strip().replace("Ford K", "FORD-K") or "Party not listed", ref=link.rsplit("/", 1)[-1], place=cells[1], start="", url="https://www.parliament.go.ke" + link))
    if len(members) < 55:
        sys.exit(f"Kenya Senate: read {len(members)} senators, expected about 67")
    return [_upper("Senate of Kenya", 67, "https://www.parliament.go.ke/the-senate/senators", "67 seats: 47 elected by county, 16 women, 2 youth and 2 persons with disabilities, nominated by the parties. Who sits and their party are from the Senate's own table of senators (parliament.go.ke). Unlit seats mean nothing found, never opposition.",
                   "Senator", r"(?i)\bsenator\b", members, {"UDA": "f4c20d", "ODM": "f28c1f", "JP": "d62828", "WDM": "2a9d8f", "IND": "8a8680", "UDM": "1b9c4a", "KANU": "c1121f"})]


ADAPTERS.update(ph=philippines, pk=lambda: pakistan() + pakistan_senate(), bd=bangladesh, ke=lambda: kenya() + kenya_senate())


def suriname():
    """De Nationale Assemblée (51 seats): dna.sr/politiek-college/leden-2025-2030 lists every member with the fractie and party. Substitutes who serve
    for a member are listed on the same page and count as members here."""
    url = "https://www.dna.sr/politiek-college/leden-2025-2030/"
    page = get(url, as_json=False).decode("utf-8", errors="replace")
    body = re.sub(r"<script.*?</script>|<style.*?</style>", "", page, flags=re.S)
    flat = re.sub(r"(\|\s*)+", "|", re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "|", body)))
    slugs = sorted(set(re.findall(r'href="/politiek-college/leden-2025-2030/([^"/]+)/"', page)))
    SHORT = {"Nationale Democratische Partij": "NDP", "Algemene Bevrijdings- en Ontwikkelingspartij": "ABOP", "Vooruitstrevende Hervormingspartij": "VHP",
             "Vooruitstrevende Hervormings Partij": "VHP", "Broederschap en Eenheid in de Politiek": "BEP", "Pertjajah Luhur": "PL", "Nationale Partij Suriname": "NPS", "Alternatief 2020": "A20"}
    drop = _HONORIFICS | {"drs", "ir", "mba", "msc", "ing", "bsc", "ma", "llm", "mpa", "phd", "mr", "rn", "msc.", "ba", "mhm", "mmc", "dr", "h", "c", "llb", "bba", "med", "pt", "mph", "bioetics", "mha", "bed"}
    members = []
    import html as _html
    for name, party, role in re.findall(r"\|([^|]+?) ?\|([^|]+?) ?\|\1 ?\|(?:([^|]+?) ?\|)?Fractie\|", flat):
        n = _plain(_html.unescape(name), drop)
        words = set(norm(n).split())
        slug = next((s for s in slugs if set(s.split("-")) <= words), "")
        members.append(dict(name=n, party=SHORT.get(party.strip(), party.strip()), ref=slug, place="", start="", url=f"{url}{slug}/" if slug else url))
    if len(members) < 45:
        sys.exit(f"Nationale Assemblée of Suriname: read {len(members)} members, expected 51")
    return [dict(name="De Nationale Assemblée", level="national", seats=51, source_url=url,
                 note="51 seats, elected 25 May 2025 for 2025-2030. Who sits and their party are from the Assembly's own list of members (dna.sr), which also carries the members who serve as substitutes. Unlit seats mean nothing found, never opposition.",
                 role="Member of De Nationale Assemblée", role_re=r"(?i)nationale assembl", role_start=r"(?i)member of de nationale",
                 members=members, former=[], party_order=["A20", "ABOP", "VHP", "BEP", "PL", "NPS", "NDP"],
                 colours={"NDP": "1b9c4a", "VHP": "e07a1f", "ABOP": "1a5fb4", "BEP": "c1121f", "PL": "6a4c93", "NPS": "d62828", "A20": "2a9d8f"})]


ADAPTERS.update(sr=suriname)

ADAPTERS["cl"] = chile
ADAPTERS["uy"] = uruguay
ADAPTERS["ec"] = ecuador
ADAPTERS["py"] = paraguay
ADAPTERS["pe"] = peru
ADAPTERS["bo"] = bolivia
ADAPTERS["cr"] = costa_rica

# Group of ten (Greece, Hungary, Romania, Slovakia, Bulgaria, Slovenia, Croatia, Bosnia, North Macedonia, Russia). Greece, Hungary, Slovakia and North Macedonia
# are read once in a browser and passed with --local (see their guides in skill/references/countries).
ADAPTERS.update(gr=greece, hu=hungary, ro=romania, sk=slovakia, bg=bulgaria, si=slovenia, hr=croatia, ba=bosnia, mk=north_macedonia, ru=russia)


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
    cc = a.adapter or countries.code(Path(a.dir).resolve().name)
    if cc not in ADAPTERS:
        sys.exit(f"No adapter for '{cc}'. Have: {', '.join(sorted(ADAPTERS))}. Add one to ADAPTERS in this file.")
    actors_in = None
    if ADAPTERS[cc] in (european_parliament, pan_african_parliament):  # supporters sit in the register of their own country: look across all of them
        actors_in = []
        for sib in sorted(p for p in Path(a.dir).resolve().parent.iterdir() if (p / "actors.csv").exists() and p.name != Path(a.dir).name):
            iso = (json.load(open(sib / "meta.json", encoding="utf-8")).get("iso2") or countries.iso(sib.name)).upper()
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
