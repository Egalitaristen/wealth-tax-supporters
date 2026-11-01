#!/usr/bin/env python3
"""Build the static site from data/<country>/ into _site/.

Usage: python scripts/build_site.py [--out _site]

Reads every folder in data/ that has a meta.json, writes one JSON file per country plus
world.json (country summary and projected world map paths), and copies the site files.
Needs only the standard library, plus pycountry for ISO codes (pip install pycountry).
"""
import argparse, csv, hashlib, json, math, re, shutil, sys, collections, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
DATA = ROOT / "data"


_HOME = None


def people_home():
    """(home, multi): home is {Wikidata id: home country ISO2} from data/home_countries.csv; multi is the ids that sit on more than one
    country's register. A person on several registers is quoted, and listed first, only for their home country."""
    global _HOME
    if _HOME is None:
        home, seen = {}, collections.defaultdict(set)
        f = DATA / "home_countries.csv"
        if f.exists():
            home = {r["wikidata_qid"]: r["home_iso2"].upper() for r in rd(f)}
        for folder in sorted(DATA.iterdir()):
            a = folder / "actors.csv"
            if a.exists():
                for r in rd(a):
                    if r.get("wikidata_qid"):
                        seen[r["wikidata_qid"]].add(folder.name)
        _HOME = (home, {q for q, s in seen.items() if len(s) > 1})
    return _HOME
SITE = ROOT / "site"
RANK = {"A": 0, "B": 1, "C": 2}

try:
    import pycountry
except ImportError:  # the build still works; countries then match on name only
    pycountry = None


def rd(path):
    p = Path(path)
    if not p.exists():
        return []
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


# ---------- world map: decode world-atlas TopoJSON and project with Equal Earth ----------
def equal_earth(lon, lat):
    A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
    lam, phi = math.radians(lon), math.radians(lat)
    th = math.asin(math.sqrt(3) / 2 * math.sin(phi))
    t2, t6 = th * th, th ** 6
    x = 2 * math.sqrt(3) * lam * math.cos(th) / (3 * (A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2)))
    y = th * (A1 + A2 * t2 + t6 * (A3 + A4 * t2))
    return x, y


def world_paths():
    topo = json.load(open(SITE / "vendor" / "countries-50m.json", encoding="utf-8"))
    sx, sy = topo["transform"]["scale"]
    tx, ty = topo["transform"]["translate"]
    arcs = []
    for arc in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx; y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)

    def ring(idx):
        pts = []
        for i in idx:
            a = arcs[i] if i >= 0 else arcs[~i][::-1]
            pts.extend(a if not pts else a[1:])
        return pts

    def clip(pts, keep, edge):
        """Sutherland-Hodgman against one vertical edge. keep(lon) says which side stays; edge is +-180."""
        out = []
        for i, p in enumerate(pts):
            q = pts[i - 1]
            pin, qin = keep(p[0]), keep(q[0])
            if pin != qin:
                t = (edge - q[0]) / (p[0] - q[0])
                out.append((edge, q[1] + t * (p[1] - q[1])))
            if pin:
                out.append(p)
        return out

    def split_antimeridian(pts):
        """Rings that cross +-180 are unwrapped, then cut into an eastern and a western piece."""
        un, off = [pts[0]], 0.0
        for a, b in zip(pts, pts[1:]):
            if b[0] - a[0] > 180: off -= 360
            elif b[0] - a[0] < -180: off += 360
            un.append((b[0] + off, b[1]))
        if max(p[0] for p in un) <= 180 and min(p[0] for p in un) >= -180:
            return [pts]
        east = clip(un, lambda lon: lon <= 180, 180.0)
        west = clip([(lon - 360, lat) for lon, lat in un], lambda lon: lon >= -180, -180.0)
        return [r for r in (east, west) if len(r) > 2]

    def inside(pt, pts):
        x, y = pt
        c = False
        for i in range(len(pts)):
            x1, y1 = pts[i]
            x2, y2 = pts[i - 1]
            if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                c = not c
        return c

    geoms = {}
    for g in topo["objects"]["countries"]["geometries"]:
        cid = str(g.get("id", ""))
        if cid in geoms:  # the 50 m file gives a few small territories the code of their country (Ashmore and Cartier Islands carry Australia's 036): merge, never replace
            m = geoms[cid]
            more = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
            m["arcs"] = (m["arcs"] if m["type"] == "MultiPolygon" else [m["arcs"]]) + more
            m["type"] = "MultiPolygon"
        else:
            geoms[cid] = g
    # Dependencies are drawn with the country they belong to, so Greenland is Denmark and Puerto Rico is the United States.
    # Left separate on purpose: Hong Kong and Macao (own tax systems), Aruba, Curacao and Sint Maarten (countries within
    # the Kingdom), the Cook Islands and Niue (free association), and the disputed or partly recognised Taiwan,
    # Palestine, Kosovo, Western Sahara and Somaliland.
    belongs_to = {
        "208": ["304", "234"],  # Denmark: Greenland, Faroe Islands
        "246": ["248"],  # Finland: Aland
        "840": ["630", "316", "850", "016", "580"],  # United States: Puerto Rico, Guam, US Virgin Islands, American Samoa, Northern Marianas
        "250": ["258", "540", "876", "666", "652", "663", "260"],  # France: overseas collectivities and the southern lands
        "826": ["060", "092", "136", "238", "239", "086", "500", "612", "654", "660", "796", "831", "832", "833"],  # United Kingdom: overseas territories and Crown dependencies
        "036": ["574", "334"],  # Australia: Norfolk Island, Heard and McDonald Islands
    }
    for home, parts in belongs_to.items():
        h = geoms[home]
        polys = h["arcs"] if h["type"] == "MultiPolygon" else [h["arcs"]]
        for pid in parts:
            g = geoms.pop(pid, None)
            if g:
                polys = polys + (g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]])
        h["arcs"], h["type"] = polys, "MultiPolygon"
    # Ukraine as it was before 2014: Natural Earth draws Crimea (with Sevastopol) in Russia, so move that polygon across.
    ru, ua = geoms["643"], geoms["804"]
    ua_polys = ua["arcs"] if ua["type"] == "MultiPolygon" else [ua["arcs"]]
    crimea = next((poly for poly in ru["arcs"] if inside((34.1, 44.95), ring(poly[0]))), None)
    if crimea is not None:
        ru["arcs"] = [poly for poly in ru["arcs"] if poly is not crimea]
        ua["arcs"], ua["type"] = ua_polys + [crimea], "MultiPolygon"

    def simplify(pts, tol):
        """Douglas-Peucker on a closed ring, so the 50 m shapes stay small enough to ship in world.json."""
        if len(pts) < 12:
            return pts
        keep = [False] * len(pts)
        # a ring starts and ends on the same point, so split it at the point farthest from the start first
        m = max(range(len(pts)), key=lambda i: (pts[i][0] - pts[0][0]) ** 2 + (pts[i][1] - pts[0][1]) ** 2)
        keep[0] = keep[m] = keep[-1] = True
        stack = [(0, m), (m, len(pts) - 1)]
        while stack:
            a, b = stack.pop()
            (x1, y1), (x2, y2) = pts[a], pts[b]
            dx, dy = x2 - x1, y2 - y1
            n = (dx * dx + dy * dy) ** 0.5 or 1e-9
            far, fi = 0, -1
            for i in range(a + 1, b):
                d = abs(dy * pts[i][0] - dx * pts[i][1] + x2 * y1 - y2 * x1) / n
                if d > far:
                    far, fi = d, i
            if far > tol:
                keep[fi] = True
                stack += [(a, fi), (fi, b)]
        return [p for p, k in zip(pts, keep) if k]

    out = {}
    for cid, g in geoms.items():
        if not cid or cid == "010":  # skip Antarctica and unidentified shapes
            continue
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
        pieces = []
        for poly in polys:
            for rg in poly:
                for part in split_antimeridian(ring(rg)):
                    pieces.append([equal_earth(*p) for p in part])
        # tiny islands go (under about 0.4 px at full width) unless it is all the country has
        def size(pts):
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            return max(max(xs) - min(xs), max(ys) - min(ys)) * 100
        big = max(size(pc) for pc in pieces) if pieces else 0
        d = ""
        for pc in pieces:
            if size(pc) < 0.12 and size(pc) < big:
                continue
            pts = simplify([(x * 100, -y * 100) for x, y in pc], 0.1)
            d += "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"
        out[cid] = {"name": g["properties"]["name"], "path": d}
    return out


def numeric_for(iso2):
    if pycountry:
        c = pycountry.countries.get(alpha_2=iso2.upper())
        if c:
            return c.numeric  # three digits, zero-padded, as the world map ids are ("076" for Brazil)
    return ""


# ---------- locations: "Country > Region > Place" paths resolved against geo_units.csv ----------
def _bare(n):
    return re.sub(r"\s*\(.*$", "", n or "").strip().lower()


def geo_index(geo):
    by_id = {g["geo_unit_id"]: g for g in geo}
    kids, roots = collections.defaultdict(dict), {}
    for g in geo:
        if g.get("parent_id") and g["parent_id"] in by_id:
            kids[g["parent_id"]].setdefault(_bare(g["name"]), g["geo_unit_id"])
        elif g.get("unit_type") == "country":
            roots[_bare(g["name"])] = g["geo_unit_id"]
    return by_id, kids, roots


def resolve_location(location, idx):
    by_id, kids, roots = idx
    parts = [p.strip() for p in (location or "").split(">") if p.strip()]
    uid = roots.get(_bare(parts[0])) if parts else None
    if not uid:
        return "", 0, parts
    depth = 1
    for seg in parts[1:]:
        nxt = kids.get(uid, {}).get(_bare(seg))
        if not nxt:
            break
        uid, depth = nxt, depth + 1
    return uid, depth, parts[depth:]


def unit_path(uid, by_id):
    names, seen = [], set()
    while uid and uid in by_id and uid not in seen:
        seen.add(uid); names.append(re.sub(r"\s*\(.*$", "", by_id[uid]["name"]).strip()); uid = by_id[uid]["parent_id"]
    return " > ".join(reversed(names))


# ---------- per-country data ----------
def build_own_actors(folder):
    """The actors and evidence a supranational folder holds itself (governments, for the UN), in the rows build_country makes.
    As there, an actor whose latest evidence is a retraction stays in the files and leaves the site."""
    actors, ev = rd(folder / "actors.csv"), rd(folder / "evidence.csv")
    latest = {}
    for e in sorted(ev, key=lambda e: e["date"]):
        latest[e["actor_id"]] = e.get("stance", "support")
    gone = {i for i, st in latest.items() if st == "retracted"}
    ev = [e for e in ev if e["actor_id"] not in gone]
    E = [[e["actor_id"], e["date"], e["grade"], e["evidence_type"], e["wt_design"], e["design_detail"], e["quote_original"][:420],
          e["source_url"], e["source_title"], e["publisher"], e.get("archive_url", ""), e["evidence_id"]] for e in ev]
    P = []
    for a in actors:
        es = [e for e in ev if e["actor_id"] == a["actor_id"]]
        if not es:
            continue
        dates = sorted(x["date"] for x in es if x["date"])
        P.append([a["actor_id"], a["name"], a["kind"], a["actor_type"], a["role"], a["affiliation"], a["level"], a.get("location", ""),
                  "ABC"[min(RANK.get(x["grade"], 3) for x in es)], len(es), dates[0] if dates else "", dates[-1] if dates else "",
                  sorted({x["wt_design"] for x in es if x["wt_design"]}), a["notes"], a["website"], a.get("party", ""),
                  [x.strip() for x in a.get("other_types", "").split(";") if x.strip()], [], a.get("wikidata_qid", "")])
    return dict(P=P, E=E)


def build_supranational(folder, full):
    """A body above the countries (the European Parliament): its chamber, groups and the supporters who sit in it. The people are
    recorded in their own country's register; positions.csv refers to them as <country folder>-<actor id>, and they are copied here
    (ids prefixed the same way) so the body has its own Seats and profile pages."""
    meta = json.load(open(folder / "meta.json", encoding="utf-8"))
    slug = folder.name
    seats_by = collections.defaultdict(list)
    for x in rd(folder / "seats.csv"):
        seats_by[x["body_id"]].append(x)
    P, E, seen, sitting = [], [], set(), collections.defaultdict(lambda: collections.defaultdict(list))
    own = None
    if rd(folder / "actors.csv"):  # a body whose members are governments (the UN) keeps them in its own folder
        own = build_own_actors(folder)
    for o in rd(folder / "positions.csv"):
        if o["current"] != "y":
            continue
        cslug, aid = o["actor_id"].rsplit("-", 1)
        D = own if (own and cslug == slug) else full.get(cslug)
        row = next((p for p in D["P"] if p[0] == aid), None) if D else None
        if not row:
            continue
        nid = o["actor_id"]
        if nid not in seen:
            seen.add(nid)
            P.append([nid] + row[1:7] + [""] + row[8:])
            E += [[nid] + e[1:] for e in D["E"] if e[0] == aid]
        sitting[o["body_id"]][o["party"]].append(nid)
    legis = []
    for b in rd(folder / "bodies.csv"):
        if b.get("seat_view") != "y" or b["body_id"] not in seats_by:
            continue
        parties = [[x["party"], int(x["seats"]), x["colour"], sitting[b["body_id"]].get(x["party"], [])]
                   for x in sorted(seats_by[b["body_id"]], key=lambda x: int(x["order"] or 0))]
        legis.append(dict(id=b["body_id"], name=b["name"], seats=int(b["seats"]), as_of=b["as_of"], src=b["source_url"], note=b.get("notes", ""), parties=parties))
    grades = collections.Counter(p[8] for p in P)
    summary = dict(slug=slug, iso2=meta.get("iso2", slug.upper()), name=meta["name"], status=meta.get("status", ""), lead=meta.get("lead", ""),
                   notes=meta.get("notes", ""), supporters=len(P), evidence=len(E), A=grades["A"], B=grades["B"], C=grades["C"],
                   member_label=meta.get("member_label", ""), units=0, units_done=0, units_with_supporters=0, updated=max([e[1] for e in E] or [""]), excluded=0, polls=[], supranational=True,
                   chambers=[[b["name"], b["seats"], sum(len(q[3]) for q in b["parties"])] for b in legis],
                   types=dict(collections.Counter(p[3] for p in P).most_common()), designs=dict(collections.Counter(d for p in P for d in p[12]).most_common()),
                   featured=[], map_source="", map_licence=["", ""])
    country = dict(meta=summary, P=P, E=E, C=[], UP=[], vb=[0, 0, 1, 1], O=[], L=[], R=[], R2=[], legis=legis)
    return summary, country


RESOURCE_KINDS = ("poll", "paper", "report", "bill")
BILL_STATES = {"in_force": "In force", "pending": "Pending", "rejected": "Rejected", "lapsed": "Lapsed", "adopted": "Adopted"}


def load_resources(countries, people):
    """Polls (from each country's meta.json) and the papers, reports and bills in data/resources.json, as one list for the Resources page.
    `people` maps (country folder, actor id) to a name, so a resource can link its authors and sponsors to their profiles."""
    names = {c["slug"]: c["name"] for c in countries}
    out = []
    for c in countries:
        for p in c.get("polls", []):
            out.append(dict(kind="poll", country=c["slug"], title=p["question"], by=" for ".join(x for x in (p.get("pollster"), p.get("commissioned_by")) if x),
                            published=str(p.get("published", "")), url=p["url"], fig=p.get("support_text") or (f"{p['support']}%" if p.get("support") is not None else ""),
                            summary=" · ".join(str(x) for x in (p.get("scope"), p.get("sample")) if x)))
    path = DATA / "resources.json"
    for r in json.load(open(path, encoding="utf-8")) if path.exists() else []:
        if r.get("kind") not in RESOURCE_KINDS or r["kind"] == "poll":
            raise SystemExit(f"resources.json: bad kind {r.get('kind')!r} in {r.get('title')!r}")
        if not str(r.get("url", "")).startswith("https://") or not r.get("title") or not r.get("by") or not r.get("published"):
            raise SystemExit(f"resources.json: needs title, by, published and an https url: {r.get('title')!r}")
        if r.get("country") != "global" and r.get("country") not in names:
            raise SystemExit(f"resources.json: unknown country {r.get('country')!r} in {r.get('title')!r}")
        if r["kind"] == "bill" and r.get("state") not in BILL_STATES:
            raise SystemExit(f"resources.json: a bill needs state {sorted(BILL_STATES)}: {r.get('title')!r}")
        row = {k: r[k] for k in ("kind", "country", "title", "by", "published", "url", "summary", "status", "state", "level") if r.get(k)}
        for ref in r.get("people", []):
            key = tuple(str(ref).split(":", 1))
            if key not in people:
                raise SystemExit(f"resources.json: unknown person {ref!r} in {r.get('title')!r} (use 'folder:actor_id')")
            row.setdefault("people", []).append([key[0], key[1], people[key]])
        out.append(row)
    for r in out:
        r["cname"] = names.get(r["country"], "Global")
    out.sort(key=lambda r: (r["published"], r["title"]), reverse=True)
    return out


def build_country(folder):
    meta = json.load(open(folder / "meta.json", encoding="utf-8"))
    slug = folder.name
    actors, ev, geo = rd(folder / "actors.csv"), rd(folder / "evidence.csv"), rd(folder / "geo_units.csv")
    # Supporters whose latest evidence is a retraction (stance=retracted) stay in the files but leave the site.
    latest = {}
    for e in sorted(ev, key=lambda e: e["date"]):
        latest[e["actor_id"]] = e.get("stance", "support")
    gone = {i for i, st in latest.items() if st == "retracted"}
    actors, ev = [a for a in actors if a["actor_id"] not in gone], [e for e in ev if e["actor_id"] not in gone]
    prof = collections.defaultdict(list)
    for p in rd(folder / "profiles.csv"):
        if p["url"].startswith("https://"):
            prof[p["actor_id"]].append([p["platform"], p["url"]])
    links, runs, excl = rd(folder / "links.csv"), rd(folder / "runs.csv"), rd(folder / "exclusions.csv")
    gidx = geo_index(geo)
    by_id = gidx[0]
    by = collections.defaultdict(list)
    for e in ev:
        by[e["actor_id"]].append(e)

    E = [[e["actor_id"], e["date"], e["grade"], e["evidence_type"], e["wt_design"], e["design_detail"],
          e["quote_original"][:420], e["source_url"], e["source_title"], e["publisher"], e.get("archive_url", ""),
          e["evidence_id"]] for e in ev]
    P = []
    for a in actors:
        es = by.get(a["actor_id"], [])
        if not es:
            continue
        best = min(RANK.get(x["grade"], 3) for x in es)
        dates = sorted(x["date"] for x in es if x["date"])
        designs = sorted({x["wt_design"] for x in es if x["wt_design"]})
        P.append([a["actor_id"], a["name"], a["kind"], a["actor_type"], a["role"], a["affiliation"], a["level"],
                  a.get("location", ""), "ABC"[best], len(es), dates[0] if dates else "",
                  dates[-1] if dates else "", designs, a["notes"], a["website"], a.get("party", ""),
                  [x.strip() for x in a.get("other_types", "").split(";") if x.strip()], prof.get(a["actor_id"], []),
                  a.get("wikidata_qid", "")])

    bounds = None
    bfile = meta.get("boundaries")
    if bfile and (folder / bfile).exists():
        bounds = json.load(open(folder / bfile, encoding="utf-8"))
    units = {_bare(g["name"]): g for g in geo}
    by_code = {g["code"]: g for g in geo if g.get("code")}  # codes are safer: names repeat (US counties)
    here, inside = collections.defaultdict(list), collections.defaultdict(list)
    for a in actors:
        if a["actor_id"] not in by:
            continue
        uid = a.get("geo_unit_id") if a.get("geo_unit_id") in by_id else resolve_location(a.get("location", ""), gidx)[0]
        if uid:
            here[uid].append(a["actor_id"])
        seen = set()
        while uid and uid in by_id and uid not in seen:  # an actor counts for its unit and every unit above it
            seen.add(uid); inside[uid].append(a["actor_id"]); uid = by_id[uid]["parent_id"]
    roots = set(gidx[2].values())
    C, vb, mapped = [], None, set()
    # A unit's place path is its parent's path plus its name; send each parent path once (UP) and its index in C,
    # since a commune map repeats "France > Occitanie > Haute-Garonne" thousands of times.
    UP, up_at = [], {}

    def up_index(g):
        par = unit_path(g.get("parent_id"), by_id)
        if par not in up_at:
            up_at[par] = len(UP); UP.append(par)
        return up_at[par]

    if bounds:
        vb = bounds["viewBox"]
        for u in bounds["units"]:
            g = by_code.get(u.get("code")) if by_code else units.get(_bare(u["name"]))
            if not g:
                continue
            mapped.add(g["geo_unit_id"])
            ids = inside.get(g["geo_unit_id"], [])
            state = "support" if ids else ("clear" if g["sweep_status"] == "done" else "open")
            # Supporters known only in the wider area (a province, state or Land, say) tint the area lightly on the map.
            # Anyone inside the widest level above that has supporters (a county, region, state or Land), wherever in it they
            # are placed: someone in Suffolk makes the whole East of England known, not only people placed "at" the region.
            above, near, anc = 0, "", g.get("parent_id")
            while anc and anc in by_id and anc not in roots:
                others = len(set(inside.get(anc, [])) - set(ids))
                if others:  # keep climbing: the widest level below the country is the one that says how much is known nearby
                    above, near = others, re.sub(r"\s*\(.*$", "", by_id[anc]["name"]).strip()
                anc = by_id[anc].get("parent_id")
            C.append([re.sub(r"\s*\(.*$", "", g["name"]).strip(), u.get("code", ""), state, g["sweep_status"], g["hits"],
                      "", ids, u["path"], up_index(g), above, near, bool(u.get("point"))])
    O = []
    for g in geo:
        uid = g["geo_unit_id"]
        if uid in mapped or not here.get(uid):
            continue
        name = g["name"] + (" (country level)" if uid in roots else "")
        O.append([name, g["level"], g["sweep_status"], "", here[uid], unit_path(uid, by_id)])
    L = [[l["from_actor_id"], l["to_actor_id"], l["link_type"], l["note"]] for l in links]
    last = max([r.get("date", "") for r in runs] or [""])
    done = sum(1 for g in geo if g["sweep_status"] == "done")
    with_sup = sum(1 for u, ids in inside.items() if ids and u not in roots)
    grades = collections.Counter(p[8] for p in P)
    summary = dict(slug=slug, iso2=meta.get("iso2", slug.split("-")[0].upper()), name=meta["name"],
                   status=meta.get("status", ""), lead=meta.get("lead", ""), notes=meta.get("notes", ""),
                   supporters=len(P), evidence=len(E), A=grades["A"], B=grades["B"], C=grades["C"],
                   units=len(geo) - len(roots), units_done=done, units_with_supporters=with_sup, updated=last, excluded=len(excl),
                   polls=[p for p in meta.get("polls", []) if str(p.get("url", "")).startswith("https://")])
    summary["map_source"] = (bounds or {}).get("source", "")
    summary["map_licence"] = [(bounds or {}).get("licence", ""), (bounds or {}).get("licence_url", "")]
    R = [r["path"] for r in (bounds or {}).get("regions", [])]
    R2 = [r["path"] for r in (bounds or {}).get("regions_upper", [])]  # a second, bolder outline (régions over départements)
    # Seats tab: each chamber with seat_view=y, its seats by party, and which seats a supporter holds today.
    # Only a position checked as current (current=y) lights a seat, so people who have left a chamber drop off.
    on_site = {p[0] for p in P}
    seats_by, sitting = collections.defaultdict(list), collections.defaultdict(lambda: collections.defaultdict(list))
    for s in rd(folder / "seats.csv"):
        seats_by[s["body_id"]].append(s)
    for o in rd(folder / "positions.csv"):
        if o["current"] == "y" and o["actor_id"] in on_site:
            sitting[o["body_id"]][o["party"]].append(o["actor_id"])
    legis = []
    for b in rd(folder / "bodies.csv"):
        if b.get("seat_view") != "y" or b["body_id"] not in seats_by:
            continue
        parties = [[s["party"], int(s["seats"]), s["colour"], sitting[b["body_id"]].get(s["party"], [])]
                   for s in sorted(seats_by[b["body_id"]], key=lambda s: int(s["order"] or 0))]
        legis.append(dict(id=b["body_id"], name=b["name"], seats=int(b["seats"]), as_of=b["as_of"], src=b["source_url"], note=b.get("notes", ""), parties=parties))
    # the one or two national chambers, for the countries list
    summary["chambers"] = [[b["name"], int(b["seats"]), sum(len(v) for v in sitting[b["body_id"]].values())] for b in rd(folder / "bodies.csv")
                           if b["level"] == "national" and b.get("seat_view") == "y" and b["body_id"] in seats_by][:2]
    country = dict(meta=summary, P=P, E=E, C=C, UP=UP, vb=vb, O=O, L=L, R=R, R2=R2, legis=legis)

    # Search index rows: [slug, id, name, type, role, place, grade, statements]
    index = [[slug, p[0], p[1], p[3], p[4][:80], [x.strip() for x in p[7].split(">")][-1] if p[7] else "", p[8], p[9], p[18]]
             for p in P]
    # Place rows: [slug, unit path, supporters inside]
    places = [[slug, unit_path(u, by_id), len(ids)] for u, ids in inside.items() if ids and u not in roots]
    summary["featured"] = featured(P, ev, summary["iso2"])
    summary["types"] = dict(collections.Counter(p[3] for p in P).most_common())
    summary["designs"] = dict(collections.Counter(d for p in P for d in p[12]).most_common())
    return summary, country, index, places


FEATURE_TYPES = ["economist", "wealthy_individual", "campaigner", "journalist", "politician", "union_official",
                 "academic", "business_leader", "cultural_figure", "legal_tax_professional", "faith"]


def featured(P, ev, iso2=""):
    """A few short, explicit quotes from named people for the home page, spread across types."""
    people = {p[0]: p for p in P if p[2] == "person"}
    spoken = {"speech", "op_ed", "statement", "interview", "social_post", "testimony", "publication", "editorial", "campaign"}
    best = {}
    for e in ev:
        p = people.get(e["actor_id"])
        q = re.sub(r"\s+", " ", e["quote_original"]).strip()
        if not p or e["grade"] != "A" or not (70 <= len(q) <= 230) or not e["source_url"].startswith("http"):
            continue
        home, multi = people_home()
        if p[18] in multi and home.get(p[18]) != iso2.upper():  # quote people only for their own country
            continue
        # Whole sentences in the person's own voice: starts with a capital, ends with punctuation,
        # and does not describe them in the third person.
        surname = p[1].split()[-1].lower()
        if (e["evidence_type"] not in spoken or not q[0].isupper() or q[-1] not in '.!?"”'
                or surname in q.lower() or re.match(r"(He|She|They|His|Her|Their)\s", q)):
            continue
        score = (len(p[17]) > 0, p[3] != "politician" or p[6] == "national", e["date"])
        if e["actor_id"] not in best or score > best[e["actor_id"]][0]:
            best[e["actor_id"]] = (score, [p[0], p[1], p[3], p[4][:90], q, e["source_url"], e["publisher"], e["date"]])
    by_type = collections.defaultdict(list)
    for score, row in sorted(best.values(), key=lambda x: x[0], reverse=True):
        by_type[row[2]].append(row)
    out = []
    while len(out) < 8 and any(by_type.values()):
        for t in FEATURE_TYPES + sorted(by_type):
            if by_type.get(t) and len(out) < 8:
                out.append(by_type[t].pop(0))
    return out


# ---------- share pages: one small HTML file per page with its own title, description and image ----------
SITE_URL = "https://wealthtaxsupporters.com"
TYPE = {"politician": "Politician", "party": "Party", "government_body": "Council or public body", "academic": "Academic",
        "economist": "Economist", "think_tank": "Think tank", "ngo_campaign": "Campaign group", "union": "Union",
        "union_official": "Union official", "journalist": "Commentator", "media_outlet": "Media outlet",
        "legal_tax_professional": "Legal or tax expert", "wealthy_individual": "Wealthy individual",
        "business_leader": "Business leader", "faith": "Faith leader or body", "cultural_figure": "Cultural figure",
        "campaigner": "Campaigner", "international_body": "International body", "funder": "Funder"}
GRADE = {"A": "Explicit support", "B": "Named support", "C": "Implied support"}
SPOKEN = {"speech", "op_ed", "statement", "interview", "social_post", "testimony", "publication", "editorial", "campaign"}


def the(name):
    return ("the " if name.startswith(("United ", "Netherlands", "Philippines", "Czech")) else "") + name


def _attr(s):
    return (s or "").replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


PRELOAD_SLUGS = set()


def page_html(base, title, desc, path, image, alt):
    """The site page with this page's meta tags, so link previews show the right title and image."""
    h = base
    m = re.match(r"/([a-z][a-z0-9-]*)(?:/|$)", path)
    if m and m.group(1) in PRELOAD_SLUGS:  # a country page needs its own data file at once
        v = re.search(r'name="data-version" content="(\w+)"', h)
        tag = '<link rel="preload" href="/data/%s.json?v=%s" as="fetch" crossorigin>' % (m.group(1), v.group(1) if v else "")
        h = h.replace("</head>", tag + chr(10) + "</head>", 1)
    h = re.sub(r"<title>.*?</title>", f"<title>{_attr(title)}</title>", h, count=1)
    for prop, val in (("name=\"description\"", desc), ("property=\"og:title\"", title), ("property=\"og:description\"", desc),
                      ("property=\"og:url\"", SITE_URL + path), ("property=\"og:image\"", SITE_URL + image),
                      ("property=\"og:image:alt\"", alt)):
        h = re.sub(r'(<meta %s content=")[^"]*(")' % prop, lambda m: m.group(1) + _attr(val) + m.group(2), h, count=1)
    return h


def type_rows(counter):
    """(label, count) for a share card's type bars, biggest first, with the smallest types folded into one row."""
    rows = [(TYPE.get(k, k), n) for k, n in counter.most_common()]
    return rows[:5] + ([("Other types", sum(n for _, n in rows[5:]))] if len(rows) > 6 else rows[5:])


def poll_line(c):
    p = (c.get("polls") or [None])[0]
    if not p:
        return ""
    q = re.sub(r"\s*\(.*?\)", "", p["question"])
    return f" In polls, {p.get('support_text') or str(p['support']) + '%'} back {q[0].lower() + q[1:]} ({p['pollster']}, {str(p.get('published', ''))[:4]})."


def share_pages(out, base, countries, full, unique=None, bodies=()):
    PRELOAD_SLUGS.update(c["slug"] for c in countries)
    """Writes per-page HTML (and share images when Pillow is installed). Returns the number of pages."""
    try:
        import share_cards as cards
    except ImportError:
        cards = None
        print("  Pillow not installed: pages get text previews and the default image (pip install pillow)")
    pages = 0

    def write(path, title, desc, image_key, alt, draw):
        nonlocal pages
        img = f"/og/{image_key}.png"
        if cards:
            draw(out / img.lstrip("/"))
            # A version in the image URL, from the picture itself: Discord, Slack and others keep a preview for a URL for weeks,
            # so a card whose numbers changed needs a new URL to be fetched again.
            img += "?v=" + hashlib.md5((out / img.lstrip("/")).read_bytes()).hexdigest()[:8]
        else:
            img = "/og.png"
        dest = out / ("index.html" if path == "/" else path.lstrip("/") + ".html")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page_html(base, title, desc, path, img, alt), encoding="utf-8")
        pages += 1

    # One person on several countries' registers counts once in the world totals (same Wikidata id); each country keeps its own count.
    tot = dict(supporters=unique if unique is not None else sum(c["supporters"] for c in countries), evidence=sum(c["evidence"] for c in countries), countries=len(countries))
    write("/", "Wealth Tax Supporters: who backs a wealth tax near you?",
          f"{tot['supporters']:,} public figures and organisations across {tot['countries']} countries who have backed a wealth tax on the record. Every name links to its source.",
          "home", "Who backs a wealth tax near you?",
          lambda o: cards.home_card(o, tot, type_rows(sum((collections.Counter(c.get("types") or {}) for c in countries), collections.Counter()))))
    write("/method", "How the register is built · Wealth Tax Supporters",
          "What counts as support for a wealth tax, how statements are sourced and graded, and how to report a mistake.",
          "method", "How the register is built", lambda o: cards.page_card(o, "Method", "How the register is built", "Sourced, graded and open: every name links to where they said it."))
    write("/countries", "Countries · Wealth Tax Supporters",
          f"The {tot['countries']} countries researched so far, with supporters found and seats in the national chambers.",
          "countries", "Country by country", lambda o: cards.page_card(o, "Countries", "Country by country", f"{tot['countries']} countries so far, each researched separately."))
    write("/resources", "Resources: polls, papers, reports and bills · Wealth Tax Supporters",
          "Polls, research papers, reports and bills on a wealth tax, from every country in the register and beyond, filterable by place and type.",
          "resources", "Resources on a wealth tax", lambda o: cards.page_card(o, "Resources", "Polls, papers, reports and bills", "What the evidence and the legislation say about a wealth tax."))
    write("/about", "About · Wealth Tax Supporters",
          "An open, sourced register of the public figures and organisations that back a wealth tax on the record: why it exists, how it is made and how to take part.",
          "about", "About Wealth Tax Supporters", lambda o: cards.page_card(o, "About", "A register of who says so", "Open, sourced and made in public."))
    write("/contribute", "Contribute and suggest a supporter · Wealth Tax Supporters",
          "Suggest a public figure or organisation who has backed a wealth tax, help check the entries already here, or start a register for your country.",
          "contribute", "Help build the register", lambda o: cards.page_card(o, "Contribute", "Help build the register", "Suggest a supporter, help check entries, or start a country."))
    write("/directory", "The global directory · Wealth Tax Supporters",
          f"{tot['supporters']:,} public figures and organisations in {tot['countries']} countries who have backed a wealth tax, filterable by country, type and strength of evidence.",
          "directory", "The global directory", lambda o: cards.directory_card(
              o, "Everyone on the record", tot["supporters"], f"public figures and organisations in {tot['countries']} countries, each with the statement they rest on",
              type_rows(sum((collections.Counter(c.get("types") or {}) for c in countries), collections.Counter())),
              [(GRADE[g], sum(c[g] for c in countries)) for g in "ABC"]))
    write("/feedback", "Feedback and bug reports · Wealth Tax Supporters",
          "Something broken, confusing or missing? Send feedback or report a bug. No account needed.",
          "feedback", "Feedback and bug reports", lambda o: cards.page_card(o, "Feedback", "Tell us what to fix or improve", "Feedback, ideas and bug reports. No account needed."))

    # The Parliaments page and the bodies above the countries (the European Parliament, the UN General Assembly): their own previews,
    # a seats page, and one page per sitting supporter.
    write("/parliaments", "Parliaments · Wealth Tax Supporters",
          f"Which seats in the legislatures of {tot['countries']} countries, and in the European Parliament and the UN General Assembly, are held by a sitting supporter of a wealth tax, found so far.",
          "parliaments", "Seats in every parliament",
          lambda o: cards.page_card(o, "Parliaments", "Seats in every parliament", "Who sits today and has backed a wealth tax. Unlit seats mean nothing found, never opposition."))
    for b in bodies:
        D, slug, name = full[b["slug"]], b["slug"], b["name"]
        legis = [dict(name=x["name"], seats=x["seats"], parties=[[q[0], q[1], q[2], len(q[3])] for q in x["parties"]]) for x in D.get("legis", [])]
        lit = sum(q[3] for x in legis for q in x["parties"])
        seats = sum(x["seats"] for x in legis)
        if legis:
            for path, title, kicker in ((f"/{slug}", f"{name} · Wealth Tax Supporters", name), (f"/{slug}/seats", f"Seats · {name} · Wealth Tax Supporters", name)):
                write(path, title,
                      f"{lit:,} of {seats:,} seats in the {legis[0]['name']} and its sister chambers are held by a sitting supporter of a wealth tax, found so far, shown by group." if len(legis) > 1 else
                      f"{lit:,} of {seats:,} seats in the {legis[0]['name']} are held by a sitting supporter of a wealth tax, found so far, shown by group.",
                      slug + ("-seats" if path.endswith("/seats") else ""), f"{name}: {lit:,} seats held by supporters found so far",
                      lambda o, b=b, legis=legis: cards.seats_card(o, b, legis, "held by a sitting supporter of a wealth tax, found so far. Unlit seats mean nothing found, never opposition."))
        ev_by = collections.defaultdict(list)
        for e in D["E"]:
            ev_by[e[0]].append(e)
        for p in D["P"]:
            es = sorted(ev_by[p[0]], key=lambda e: (e[2] != "A", e[3] not in SPOKEN, not e[6], -int((e[1] or "0")[:4] or 0)))
            quote = re.sub(r"\s+", " ", es[0][6]).strip() if es and es[0][6] else ""
            if quote and quote[0].islower():
                quote = "…" + quote
            role = " · ".join(x for x in (p[4], p[5]) if x)
            y0, y1 = (p[10] or "")[:4], (p[11] or "")[:4]
            span = y0 if y0 == y1 else f"{y0}–{y1}"
            gradeline = f"{GRADE.get(p[8], '')} · {p[9]} statement{'s' if p[9] != 1 else ''}" + (f" · {span}" if y0 else "")
            desc = (f"{role}. " if role else "") + (f"“{quote[:200]}{'…' if len(quote) > 200 else ''}” " if quote else "") +                 f"{p[9]} sourced statement{'s' if p[9] != 1 else ''} in support of a wealth tax."
            write(f"/{slug}/{p[0]}", f"{p[1]} backs a wealth tax · Wealth Tax Supporters", desc, f"{slug}/{p[0]}",
                  f"{p[1]}, {TYPE.get(p[3], p[3])}, {name}",
                  lambda o, p=p, quote=quote, gradeline=gradeline, role=role: cards.person_card(
                      o, {"name": p[1], "role": role}, name, quote, [], set(), TYPE.get(p[3], p[3]), gradeline))

    for c in countries:
        D, slug, name = full[c["slug"]], c["slug"], c["name"]
        mx = max([len(u[6]) for u in D["C"]] or [1]) or 1
        mx_up = max([u[9] for u in D["C"]] or [1]) or 1
        # The same shading as the site map: real supporters from 0.42 up, areas known only through the level above
        # a faint 0.08 to 0.28.
        units = [(u[7], (0.42 + 0.58 * math.log(len(u[6]) + 1) / math.log(mx + 1)) if u[6]
                  else (0.08 + 0.2 * math.log(u[9] + 1) / math.log(mx_up + 1)) if u[9] else 0) for u in D["C"]]
        found = f"public figures and organisations in {the(name)} on the record so far"
        years = sorted({e[1][:4] for e in D["E"] if e[1]})
        sections = {
            "": (f"Wealth tax supporters in {the(name)}", "Wealth tax supporters in", found,
                 f"{c['supporters']:,} public figures and organisations in {the(name)} have backed a wealth tax on the record, found so far.{poll_line(c)}"),
            "directory": (f"Directory of wealth tax supporters · {name}", "Directory · every name with its source", found,
                          f"Browse all {c['supporters']:,} public figures and organisations in {the(name)} who back a wealth tax, by place, party and type."),
            "time": (f"When they said it · {name}", "Over time · statements per year", f"sourced statements since {years[0] if years else ''}",
                     f"{c['evidence']:,} sourced statements in support of a wealth tax in {the(name)}, year by year."),
            "method": (f"How it was built · {name}", "Method · polls, bills, sources and downloads", found,
                       f"How the {name} register was built, what polls say about a wealth tax, and the data as CSV.{poll_line(c)}"),
        }
        if D.get("legis"):
            sections["seats"] = (f"Seats · {name}", "Seats · who sits in the legislature", found,
                                 f"Which seats in {the(name)}'s legislature are held by supporters of a wealth tax, found so far, by party.")
        for sec, (title, kicker, sub, desc) in sections.items():
            n_sub = c["evidence"] if sec == "time" else c["supporters"]
            cc = dict(c, supporters=n_sub)
            if sec == "seats":
                bodies = [dict(name=b["name"], seats=b["seats"], parties=[[q[0], q[1], q[2], len(q[3])] for q in b["parties"]]) for b in D["legis"]]
                lit = sum(q[3] for b in bodies for q in b["parties"])
                write(f"/{slug}/seats", f"{title} · Wealth Tax Supporters",
                      f"{lit:,} of {sum(b['seats'] for b in bodies):,} seats in {the(name)}'s legislature are held by a sitting supporter of a wealth tax, found so far, shown by party.",
                      slug + "-seats", f"{title}: {lit:,} seats held by supporters found so far",
                      lambda o, cc=cc, bodies=bodies: cards.seats_card(o, cc, bodies, "held by a sitting supporter of a wealth tax, found so far. Unlit seats mean nothing found, never opposition."))
                continue
            if sec == "directory":
                write(f"/{slug}/directory", f"{title} · Wealth Tax Supporters", desc, slug + "-directory", f"{title}: {c['supporters']:,} found so far",
                      lambda o, cc=cc: cards.directory_card(o, cc["name"], cc["supporters"], "public figures and organisations on the record so far",
                                                            type_rows(collections.Counter(cc.get("types") or {})), [(GRADE[g], cc[g]) for g in "ABC"]))
                continue
            write(f"/{slug}" + (f"/{sec}" if sec else ""), f"{title} · Wealth Tax Supporters", desc, slug + (f"-{sec}" if sec else ""),
                  f"{title}: {c['supporters']:,} found so far",
                  lambda o, cc=cc, kicker=kicker, sub=sub: cards.country_card(o, cc, units, kicker, sub))
        # one page per supporter
        ev_by = collections.defaultdict(list)
        for e in D["E"]:
            ev_by[e[0]].append(e)
        inside = collections.defaultdict(set)
        for i, u in enumerate(D["C"]):
            for a in u[6]:
                inside[a].add(i)
        for p in D["P"]:
            es = sorted(ev_by[p[0]], key=lambda e: (e[2] != "A", e[3] not in SPOKEN, not e[6], -int((e[1] or "0")[:4] or 0)))
            quote = re.sub(r"\s+", " ", es[0][6]).strip() if es and es[0][6] else ""
            if quote and quote[0].islower():
                quote = "…" + quote
            role = " · ".join(x for x in (p[4], p[5]) if x)
            y0, y1 = (p[10] or "")[:4], (p[11] or "")[:4]
            span = y0 if y0 == y1 else f"{y0}–{y1}"
            gradeline = f"{GRADE.get(p[8], '')} · {p[9]} statement{'s' if p[9] != 1 else ''}" + (f" · {span}" if y0 else "")
            desc = (f"{role}. " if role else "") + (f"“{quote[:200]}{'…' if len(quote) > 200 else ''}” " if quote else "") + \
                f"{p[9]} sourced statement{'s' if p[9] != 1 else ''} in support of a wealth tax."
            hl = inside.get(p[0], set())
            write(f"/{slug}/{p[0]}", f"{p[1]} backs a wealth tax · Wealth Tax Supporters", desc, f"{slug}/{p[0]}",
                  f"{p[1]}, {TYPE.get(p[3], p[3])}, {name}",
                  lambda o, p=p, quote=quote, gradeline=gradeline, hl=hl: cards.person_card(
                      o, {"name": p[1], "role": role if (role := " · ".join(x for x in (p[4], p[5]) if x)) else ""}, name, quote,
                      units if hl else [], hl, TYPE.get(p[3], p[3]), gradeline))
    return pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "_site"))
    out = Path(ap.parse_args().out)
    if out.exists():
        shutil.rmtree(out)
    (out / "data").mkdir(parents=True)
    # Every file in site/ except the page and the vendored map source is copied as is.
    assets = [f for f in SITE.iterdir() if f.is_file() and f.name != "index.html"]
    for f in assets:
        shutil.copy(f, out / f.name)
    if (SITE / "fonts").is_dir():  # self-hosted fonts
        shutil.copytree(SITE / "fonts", out / "fonts")
    if (SITE / "vendor" / "flags").is_dir():  # country flags (flag-icons, MIT), shown next to country names
        shutil.copytree(SITE / "vendor" / "flags", out / "flags")
    # A content hash in each asset URL makes updates show at once despite caching.
    html = (SITE / "index.html").read_text(encoding="utf-8")
    for f in assets:
        if f.suffix in (".js", ".css", ".svg"):
            h = hashlib.md5(f.read_bytes()).hexdigest()[:8]
            html = html.replace(f'"/{f.name}"', f'"/{f.name}?v={h}"')
    countries, index, places, full = [], [], [], {}
    supras = []
    for folder in sorted(DATA.iterdir()):
        if folder.is_dir() and (folder / "meta.json").exists():
            if json.load(open(folder / "meta.json", encoding="utf-8")).get("supranational"):
                supras.append(folder)  # built after the countries: its people live in their registers
                continue
            summary, country, idx, pl = build_country(folder)
            summary["numeric"] = numeric_for(summary["iso2"].split("-")[0])
            countries.append(summary)
            full[folder.name] = country
            index += idx
            places += pl
            json.dump(country, open(out / "data" / f"{folder.name}.json", "w", encoding="utf-8"),
                      separators=(",", ":"), ensure_ascii=False)
            dl = out / "download" / folder.name
            dl.mkdir(parents=True)
            for name in ("actors.csv", "evidence.csv", "profiles.csv", "geo_units.csv"):
                if (folder / name).exists():
                    shutil.copy(folder / name, dl / name)
            print(f"  {folder.name}: {summary['supporters']} supporters, {summary['evidence']} evidence rows")
    bodies = []
    for folder in supras:
        summary, country = build_supranational(folder, full)
        json.dump(country, open(out / "data" / f"{folder.name}.json", "w", encoding="utf-8"), separators=(",", ":"), ensure_ascii=False)
        bodies.append(summary)
        full[folder.name] = country
        print(f"  {folder.name}: {summary['supporters']} sitting supporters")
    planned = json.load(open(DATA / "supranational.json", encoding="utf-8")) if (DATA / "supranational.json").exists() else []
    paths = world_paths()
    # Every country's everyday name, for the suggestion form: people may suggest supporters anywhere, not only
    # where a register has started.
    # One name per ISO country: the register's name, else the world map's everyday name, else ISO's common name.
    own = {c["iso2"].upper(): c["name"] for c in countries}
    every = {p["name"] for p in paths.values()} | set(own.values())
    for c in (pycountry.countries if pycountry else []):
        if c.alpha_2 not in own and c.numeric not in paths:
            every.add(getattr(c, "common_name", None) or c.name)
    # Anyone with a Wikidata id on more than one register is one person; rows without an id each count once.
    unique = len({r[8] or f"{r[0]}/{r[1]}" for r in index})
    world_resources = load_resources(countries, {(r[0], r[1]): r[2] for r in index})
    world = dict(unique_supporters=unique, home={q: next((c["slug"] for c in countries if c["iso2"].upper() == h), "") for q, h in people_home()[0].items()}, countries=countries, bodies=bodies, planned=planned, resources=world_resources, all_countries=sorted(every), built=datetime.date.today().isoformat())
    json.dump(world, open(out / "data" / "world.json", "w", encoding="utf-8"), separators=(",", ":"), ensure_ascii=False)
    # The outlines are two thirds of the world file; only the map pages need them, so they load separately.
    json.dump(dict(paths=paths), open(out / "data" / "map.json", "w", encoding="utf-8"), separators=(",", ":"), ensure_ascii=False)
    json.dump(dict(people=index, places=places), open(out / "data" / "index.json", "w", encoding="utf-8"),
              separators=(",", ":"), ensure_ascii=False)
    # A hash of the data files goes into the page (meta data-version) and onto each data request.
    dh = hashlib.md5()
    for f in sorted((out / "data").iterdir()):
        dh.update(f.read_bytes())
    dv = dh.hexdigest()[:8]
    html = html.replace('name="data-version" content=""', f'name="data-version" content="{dv}"')
    html = html.replace('href="/data/world.json" as="fetch"', f'href="/data/world.json?v={dv}" as="fetch"')
    (out / "index.html").write_text(html, encoding="utf-8")
    n = share_pages(out, html, countries, full, unique, bodies)
    print(f"Built {len(countries)} countr{'y' if len(countries) == 1 else 'ies'} and {n} share pages into {out}")


if __name__ == "__main__":
    sys.exit(main())
