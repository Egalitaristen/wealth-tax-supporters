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
import charts as chartlib  # inline charts for the argument pages
import static_pages as sp  # plain-HTML page bodies for crawlers that do not run the app
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
    if own:
        for row in own["P"]:
            nid = f"{slug}-{row[0]}"
            if nid not in seen:
                seen.add(nid)
                P.append([nid] + row[1:])
                E += [[nid] + e[1:] for e in own["E"] if e[0] == row[0]]
    legis = []
    for b in rd(folder / "bodies.csv"):
        if b.get("seat_view") != "y" or b["body_id"] not in seats_by:
            continue
        parties = [[x["party"], int(x["seats"]), x["colour"], sitting[b["body_id"]].get(x["party"], [])]
                   for x in sorted(seats_by[b["body_id"]], key=lambda x: int(x["order"] or 0))]
        legis.append(dict(id=b["body_id"], name=b["name"], level=b.get("level", ""), seats=int(b["seats"]), as_of=b["as_of"], src=b["source_url"], note=b.get("notes", ""), parties=parties))
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
PAGE_KINDS = ("bill", "report", "paper")  # kinds that get their own page at /resources/<slug>
RESOURCE_RAW = {}  # slug -> the resource's full entry from resources.json, for its page
POLL_RAW = {}  # slug -> the poll's entry from its country's meta.json, for its page


def whole_pct(v):
    """A poll's support as a clear whole percentage: 82.9 -> '83%'."""
    return f"{int(float(v) + 0.5)}%"
BILL_STATES = {"in_force": "In force", "pending": "Pending", "rejected": "Rejected", "lapsed": "Lapsed", "adopted": "Adopted"}


ONLY = set()  # country folders of a --only preview build; empty for a full build


def slugify(text):
    import unicodedata
    t = unicodedata.normalize("NFKD", text.replace("ß", "ss").replace("ø", "o").replace("Ø", "O").replace("æ", "ae").replace("ł", "l").replace("Ł", "L").replace("đ", "d"))
    return re.sub(r"[^a-z0-9]+", "-", "".join(c for c in t if not unicodedata.combining(c)).lower()).strip("-")


def default_slug(r):
    """A readable URL name from the country and the title: the part before the first colon, without brackets, cut at a word."""
    head = re.sub(r"\s*\([^)]*\)", "", re.split(r":\s", r["title"], 1)[0])
    s = slugify(head)
    if len(s) < 6:  # a title in another script: take the English words in brackets
        s = slugify(r["title"])
    if len(s) > 48:
        s = s[:48].rsplit("-", 1)[0]
    return slugify(r["country"] + "-" + s)


def assign_slugs(items):
    """Gives each page resource its slug: the one in resources.json, else the default (with the year, then a number, if two collide)."""
    used = {}
    for r in items:
        if r.get("slug"):
            if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", r["slug"]):
                raise SystemExit(f"resources.json: bad slug {r['slug']!r} (lower-case letters, digits and hyphens)")
            if r["slug"] in used:
                raise SystemExit(f"resources.json: slug {r['slug']!r} is used twice")
            used[r["slug"]] = r
    for r in items:
        if r.get("slug"):
            continue
        base = default_slug(r)
        for cand in (base, f"{base}-{str(r['published'])[:4]}", *(f"{base}-{str(r['published'])[:4]}-{n}" for n in range(2, 50))):
            if cand not in used:
                r["slug"] = cand
                used[cand] = r
                break
    return used


def load_resources(countries, people):
    """Polls (from each country's meta.json) and the papers, reports and bills in data/resources.json, as one list for the Resources page.
    `people` maps (country folder, actor id) to a name, so a resource can link its authors and sponsors to their profiles."""
    names = {c["slug"]: c["name"] for c in countries}
    out = []
    for c in countries:
        for p in c.get("polls", []):
            out.append(dict(kind="poll", country=c["slug"], title=p["question"], by=" for ".join(x for x in (p.get("pollster"), p.get("commissioned_by")) if x),
                            published=str(p.get("published", "")), url=p["url"], fig=whole_pct(p["support"]) if p.get("support") is not None else "",
                            summary=" · ".join(str(x) for x in (p.get("scope"), p.get("sample")) if x), _poll=p))
    path = DATA / "resources.json"
    raw = []
    for r in json.load(open(path, encoding="utf-8")) if path.exists() else []:
        if r.get("kind") not in RESOURCE_KINDS or r["kind"] == "poll":
            raise SystemExit(f"resources.json: bad kind {r.get('kind')!r} in {r.get('title')!r}")
        if not str(r.get("url", "")).startswith("https://") or not r.get("title") or not r.get("by") or not r.get("published"):
            raise SystemExit(f"resources.json: needs title, by, published and an https url: {r.get('title')!r}")
        if ONLY and r.get("country") != "global" and r.get("country") not in names:
            continue  # preview build: resources of countries that were not built
        if r.get("country") != "global" and r.get("country") not in names:
            raise SystemExit(f"resources.json: unknown country {r.get('country')!r} in {r.get('title')!r}")
        if r["kind"] == "bill" and r.get("state") not in BILL_STATES:
            raise SystemExit(f"resources.json: a bill needs state {sorted(BILL_STATES)}: {r.get('title')!r}")
        row = {k: r[k] for k in ("kind", "country", "title", "by", "published", "url", "summary", "status", "state", "level") if r.get(k)}
        if r["kind"] in PAGE_KINDS:
            for l in r.get("links", []):
                if not isinstance(l, dict) or not str(l.get("url", "")).startswith("https://"):
                    raise SystemExit(f"resources.json: links need {{label, https url}}: {r.get('title')!r}")
            for d in r.get("documents", []):
                if not re.fullmatch(r"[a-z-]+:M\d{4}", str(d)):
                    raise SystemExit(f"resources.json: documents use 'folder:M0001': {d!r} in {r.get('title')!r}")
            if "overview" in r and not str(r["overview"]).strip():
                raise SystemExit(f"resources.json: empty overview in {r.get('title')!r} (leave the field out)")
            raw.append(r)
            row["_raw"] = r
        for ref in r.get("people", []):
            key = tuple(str(ref).split(":", 1))
            if ONLY and key not in people and key[0] not in ONLY:
                continue  # preview build: people of countries that were not built; a built country's references are still checked
            if key not in people:
                raise SystemExit(f"resources.json: unknown person {ref!r} in {r.get('title')!r} (use 'folder:actor_id')")
            row.setdefault("people", []).append([key[0], key[1], people[key]])
        out.append(row)
    used = assign_slugs(raw)  # slugs are assigned over every page resource, so a preview build gets the same URLs as a full one
    RESOURCE_RAW.clear()
    POLL_RAW.clear()
    for r in out:
        if "_poll" in r:  # a poll's page: <country>-poll-<pollster>-<year>, numbered if two share all three
            p = r.pop("_poll")
            who = re.sub(r"\s*\([^)]*\)", "", p.get("pollster") or "").split(",")[0]
            base = slugify(f"{r['country']}-poll-{' '.join(who.split()[:3])}-{str(p.get('published', ''))[:4]}")[:60].strip("-")
            slug, n = base, 2
            while slug in used:
                slug, n = f"{base}-{n}", n + 1
            used[slug] = r
            r["slug"] = slug
            POLL_RAW[slug] = p
        r["cname"] = names.get(r["country"], "Global")
        if "_raw" in r:
            raw_r = r.pop("_raw")
            r["slug"] = raw_r["slug"]
            RESOURCE_RAW[r["slug"]] = raw_r
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
        legis.append(dict(id=b["body_id"], name=b["name"], level=b.get("level", ""), seats=int(b["seats"]), as_of=b["as_of"], src=b["source_url"], note=b.get("notes", ""), parties=parties))
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


# ---------- country stories: content/stories/<folder>.md -> data/story-<folder>.json ----------
# Front matter (a small YAML subset: `key: value`, and lists of `- key: value` items), then a markdown body. See content/stories/README.md.
STORIES = ROOT / "content" / "stories"
STORY_LAYOUTS = ("article",)
STORY_LISTS = {"facts": ("label", "value"), "timeline": ("year", "text"), "sources": ("id", "title", "url"), "charts": ("id", "type", "title", "desc", "caption")}  # charts: argument pages only


def _unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1]
    return v


def parse_front_matter(text, name):
    """(dict, body). Tolerant: unknown keys are kept, blank lines and # comments are skipped, quotes around values are optional."""
    m = re.match(r"﻿?---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n?(.*)\Z", text, re.S)
    if not m:
        raise SystemExit(f"{name}: a story starts with a --- front matter block")
    fm, cur_list, item = {}, None, None
    for raw in m.group(1).splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        line = raw.strip()
        if raw[:1] not in " \t":
            k, _, v = line.partition(":")
            k, v = k.strip(), v.strip()
            if v == "" and k in STORY_LISTS:
                cur_list, item = fm.setdefault(k, []), None
            else:
                fm[k], cur_list, item = _unquote(v), None, None
            continue
        if cur_list is None:
            raise SystemExit(f"{name}: unexpected indented line {raw!r}")
        if line.startswith("-"):
            item = {}
            cur_list.append(item)
            line = line[1:].strip()
        if line:
            if item is None:
                raise SystemExit(f"{name}: list item must start with '-': {raw!r}")
            k, _, v = line.partition(":")
            item[k.strip()] = _unquote(v)
    return fm, m.group(2)


def _safe_href(u):
    """Only http(s) links and site-relative paths; anything else (javascript:, data:, protocol-relative) is dropped."""
    u = u.strip()
    return u if (re.match(r"https?://[^\s\"'<>]+\Z", u) or re.match(r"/(?!/)[^\s\"'<>]*\Z", u)) else ""


def story_slug(text):
    import unicodedata
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def story_inline(text, refs):
    """Escape everything, then allow only **bold**, *italic*, [text](https://... or /path) and [n] source references."""
    import html
    stash = []

    def keep(h):
        stash.append(h)
        return f"\x00{len(stash) - 1}\x00"

    t = html.escape(text, quote=True)

    def link(m):
        href = _safe_href(html.unescape(m.group(2)))
        if not href:
            return m.group(1)
        ext = href.startswith("http")
        return keep(f'<a href="{html.escape(href, quote=True)}"' + (' target="_blank" rel="noopener noreferrer nofollow"' if ext else "") + f">{m.group(1)}</a>")

    t = re.sub(r"\[([^\]\[]+)\]\(([^)\s]+)\)", link, t)

    def ref(m):
        if m.group(1) not in refs:
            raise SystemExit(f"story: source reference [{m.group(1)}] has no entry in sources")
        refs[m.group(1)] += 1
        return keep(f'<sup class="ref"><a href="#src-{m.group(1)}">[{m.group(1)}]</a></sup>')

    t = re.sub(r"\[(\d{1,3})\]", ref, t)
    t = re.sub(r"\*\*(\S(?:.*?\S)?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*(\S(?:[^*]*?\S)?)\*(?![*\w])", r"<em>\1</em>", t)
    return re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], t)


def story_markdown(body, refs, chart_ids=None):
    """Body -> (intro html, [{id, title, html}]). Blocks: ## and ### headings, paragraphs, - lists, 1. lists, > quotes (an optional last
    line '— Name, source' is the attribution). Nothing else is passed through. `## Heading {#anchor}` fixes the anchor.
    With `chart_ids` (argument pages), `{{chart: id}}` on a line of its own places that chart; the build swaps in the figure."""
    sections, cur, seen = [], {"id": "", "title": "", "html": []}, set()
    blocks = [b for b in re.split(r"\n\s*\n", body.replace("\r\n", "\n").strip()) if b.strip()]
    for b in blocks:
        lines = [l.rstrip() for l in b.split("\n")]
        first = lines[0]
        h = re.match(r"(#{2,3})\s+(.*?)(?:\s*\{#([a-z0-9-]+)\})?\s*\Z", first) if len(lines) == 1 else None
        if h:
            if len(h.group(1)) == 2:
                sections.append(cur)
                ident = h.group(3) or story_slug(h.group(2))
                if not ident or ident in seen or ident in ("timeline", "sources") or ident.startswith("src-"):
                    raise SystemExit(f"story: heading {h.group(2)!r} makes a duplicate or empty anchor")
                seen.add(ident)
                cur = {"id": ident, "title": h.group(2), "html": []}
            else:
                ident = h.group(3) or story_slug(h.group(2))
                if not ident or ident in seen or ident in ("timeline", "sources") or ident.startswith("src-"):
                    raise SystemExit(f"story: heading {h.group(2)!r} makes a duplicate or empty anchor")
                seen.add(ident)
                cur["html"].append(f'<h3 id="{ident}">{story_inline(h.group(2), refs)}</h3>')
            continue
        cm = re.fullmatch(r"\{\{chart:\s*([a-z0-9-]+)\s*\}\}", b.strip())
        if cm and chart_ids is not None:
            if cm.group(1) not in chart_ids:
                raise SystemExit(f"story: {{{{chart: {cm.group(1)}}}}} has no entry in charts")
            cur["html"].append(f'<div data-chart="{cm.group(1)}"></div>')
            continue
        if b.strip() == "{{supporters}}":  # the live "who supports it" block; the site fills it from the country's register data
            cur["html"].append('<div data-block="supporters"></div>')
            continue
        if all(re.match(r"[-*]\s+", l) for l in lines):
            cur["html"].append("<ul>" + "".join("<li>" + story_inline(re.sub(r"^[-*]\s+", "", l), refs) + "</li>" for l in lines) + "</ul>")
        elif all(re.match(r"\d+[.)]\s+", l) for l in lines):
            cur["html"].append("<ol>" + "".join("<li>" + story_inline(re.sub(r"^\d+[.)]\s+", "", l), refs) + "</li>" for l in lines) + "</ol>")
        elif first.startswith(">"):
            qs = [re.sub(r"^>\s?", "", l) for l in lines]
            cite = ""
            if len(qs) > 1 and re.match(r"(—|--)\s*\S", qs[-1]):
                cite = re.sub(r"^(—|--)\s*", "", qs.pop())
            cur["html"].append("<blockquote><p>" + story_inline(" ".join(qs), refs) + "</p>" + (f"<footer>{story_inline(cite, refs)}</footer>" if cite else "") + "</blockquote>")
        else:
            if re.match(r"\s*<|#", first):
                raise SystemExit(f"story: unsupported block {first[:40]!r} (no raw HTML; headings are ## or ###)")
            cur["html"].append("<p>" + story_inline(" ".join(l.strip() for l in lines), refs) + "</p>")
    sections.append(cur)
    return "".join(sections[0]["html"]), [dict(id=s["id"], title=s["title"], html="".join(s["html"])) for s in sections[1:]]


def load_story(slug):
    """The story for a country folder as the JSON the site loads, or None. Facts and timeline rows are plain text the site escapes."""
    f = STORIES / f"{slug}.md"
    if not f.exists():
        return None
    fm, body = parse_front_matter(f.read_text(encoding="utf-8"), f.name)
    for k in ("title", "standfirst", "updated"):
        if not fm.get(k):
            raise SystemExit(f"{f.name}: front matter needs {k}")
    if not re.match(r"\d{4}-\d\d-\d\d\Z", fm["updated"]):
        raise SystemExit(f"{f.name}: updated must be YYYY-MM-DD")
    status = fm.get("status", "draft")
    if status not in PAGE_STATUS:
        raise SystemExit(f"{f.name}: status must be one of {PAGE_STATUS}")
    layout = fm.get("layout", "article")
    if layout not in STORY_LAYOUTS:
        raise SystemExit(f"{f.name}: layout must be one of {STORY_LAYOUTS}")
    for key, fields in STORY_LISTS.items():
        for it in fm.get(key, []):
            for need in fields:
                if not it.get(need):
                    raise SystemExit(f"{f.name}: {key} item {it} needs {need}")
    srcs = fm.get("sources", [])
    ids = [s["id"] for s in srcs]
    if len(set(ids)) != len(ids) or not all(re.match(r"\d{1,3}\Z", i) for i in ids):
        raise SystemExit(f"{f.name}: source ids are unique numbers")
    for s in srcs:
        if not s["url"].startswith("https://"):
            raise SystemExit(f"{f.name}: source {s['id']} needs an https url")
    for it in fm.get("facts", []) + fm.get("timeline", []):
        if it.get("source") and it["source"] not in ids:
            raise SystemExit(f"{f.name}: source {it['source']} is not in sources")
    refs = {i: 0 for i in ids}
    intro, sections = story_markdown(body, refs)
    for it in fm.get("facts", []) + fm.get("timeline", []):
        if it.get("source"):
            refs[it["source"]] += 1
    unused = [i for i, n in refs.items() if not n]
    if unused:
        print(f"  WARNING {f.name}: sources never cited: {', '.join(unused)}")
    words = len(re.sub(r"<[^>]+>", " ", intro + " ".join(s["html"] for s in sections)).split())
    print(f"  story {slug}: {words} words, {len(sections)} sections, layout {layout}")
    return dict(title=fm["title"], standfirst=fm["standfirst"], updated=fm["updated"], author=fm.get("author", ""), layout=layout, status=status,
                facts=fm.get("facts", []), timeline=fm.get("timeline", []), sources=srcs, intro=intro, sections=sections, words=words)


# Stories and argument pages carry `status: draft` (the default) until the author marks them final. A draft shows a badge so readers know the page will change.
PAGE_STATUS = ("draft", "final")
DRAFT_NOTE = "Draft. The wording, numbers and structure of this page are still being revised and will change."


def draft_badge(status):
    return f'<p class="draft-note"><span class="draft-pill">Draft</span> <span>{h(DRAFT_NOTE[len("Draft. "):])}</span></p>' if status != "final" else ""


# ---------- arguments: content/arguments/<slug>.md -> /arguments and /arguments/<slug> ----------
# Same markdown dialect and front matter as the stories, without a timeline, plus `kind: argument`, `objection` and `answer`.
# See content/arguments/README.md. The order of the hub, and each page's short title (breadcrumb, previous/next), is this list.
ARGUMENTS_DIR = ROOT / "content" / "arguments"
ARGUMENT_ORDER = [
    ("why-tax-wealth", "Why tax wealth"),
    ("europe-repealed-it", "Europe repealed it"),
    ("they-will-leave", "They will leave"),
    ("you-cannot-value-it", "You cannot value it"),
    ("no-cash", "No cash"),
    ("double-taxation", "Double taxation"),
    ("we-already-tax-property", "We already tax property"),
    ("family-firms", "Family firms"),
    ("it-will-spread", "It will spread"),
    ("not-enough", "Not enough"),
    ("hurts-growth", "Hurts growth"),
    ("unconstitutional", "Unconstitutional"),
    ("nobel-laureates", "Nobel laureates"),
]
ARGUMENT_FIELDS = {"title", "standfirst", "updated", "author", "layout", "facts", "sources", "kind", "objection", "answer", "status", "charts", "card_figure", "card_label"}
CHART_CTX = {}  # what the charts draw from, set in main(): the polls, the world outlines and the wealth tax status
ARGUMENTS_ONLY = False  # --only arguments: a preview build of the section, with the countries its pages link to
ARGUMENT_HUB_INTRO = ("Every wealth tax meets the same objections. Each one is put here the way people raise it, then answered on a page of its own, "
                      "with the figures, the laws and the court rulings behind the answer. Every number carries a source you can open.")


def _front_keys(text):
    """Top-level keys of a front matter block, in order, so unknown ones can be reported (parse_front_matter keeps them but does not list them)."""
    m = re.match(r"﻿?---[ \t]*\r?\n(.*?)\r?\n---", text, re.S)
    return [l.split(":", 1)[0].strip() for l in (m.group(1).splitlines() if m else []) if l[:1] not in " \t#" and ":" in l]


def plain_quote(s):
    """An objection without its own surrounding quotation marks, for display between curly quotes."""
    return s.strip().strip('"“”').strip()


def load_arguments():
    """Every page in content/arguments/ as a dict, in hub order. Errors in any page are collected and then fail the build."""
    files = sorted(ARGUMENTS_DIR.glob("*.md")) if ARGUMENTS_DIR.is_dir() else []
    files = [f for f in files if f.name.lower() not in ("readme.md", "style.md")]
    errors, pages, order = [], {}, {s: i for i, (s, _) in enumerate(ARGUMENT_ORDER)}
    short = dict(ARGUMENT_ORDER)
    for f in files:
        slug = f.stem

        def err(msg, f=f):
            errors.append(f"{f.name}: {msg}")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
            err("the file name must be lower-case letters, digits and hyphens")
        if slug not in order:
            err("not in ARGUMENT_ORDER in scripts/build_site.py (add it there to place it in the hub)")
        try:
            text = f.read_text(encoding="utf-8")
            fm, body = parse_front_matter(text, f.name)
        except SystemExit as e:
            errors.append(str(e))
            continue
        keys = _front_keys(text)
        for k in sorted(set(keys) - ARGUMENT_FIELDS):
            err("unknown front matter field " + repr(k) + (" (arguments have no timeline)" if k == "timeline" else ""))
        for k in sorted({k for k in keys if keys.count(k) > 1}):
            err(f"front matter field {k!r} appears twice")
        for k in ("title", "standfirst", "updated", "objection", "answer", "kind"):
            if not fm.get(k):
                err(f"front matter needs {k}")
        if fm.get("kind") and fm["kind"] != "argument":
            err("kind must be 'argument'")
        if fm.get("status", "draft") not in PAGE_STATUS:
            err(f"status must be one of {PAGE_STATUS}")
        if fm.get("updated") and not re.match(r"\d{4}-\d\d-\d\d\Z", fm["updated"]):
            err("updated must be YYYY-MM-DD")
        if fm.get("layout", "article") not in STORY_LAYOUTS:
            err(f"layout must be one of {STORY_LAYOUTS}")
        srcs = fm.get("sources", [])
        if not srcs:
            err("sources is empty")
        for key in ("facts", "sources"):
            for it in fm.get(key, []):
                for need in STORY_LISTS[key]:
                    if not it.get(need):
                        err(f"{key} item {it} needs {need}")
        ids = [s.get("id", "") for s in srcs]
        if len(set(ids)) != len(ids) or not all(re.match(r"\d{1,3}\Z", i) for i in ids):
            err("source ids are unique numbers")
        for s in srcs:
            if not s.get("url", "").startswith("https://"):
                err(f"source {s.get('id')} needs an https url")
        for it in fm.get("facts", []):
            if it.get("source") and it["source"] not in ids:
                err(f"fact {it.get('label')!r} cites source {it['source']}, which is not in sources")
        charts = fm.get("charts", [])
        for ch in charts:
            for need in STORY_LISTS["charts"]:
                if not ch.get(need):
                    err(f"charts item {ch.get('id', ch)} needs {need}")
            for msg in chartlib.check(ch):
                err(msg)
        cids = [ch.get("id") for ch in charts]
        for dup in sorted({i for i in cids if cids.count(i) > 1}):
            err(f"chart id {dup!r} appears twice")
        if "{{" in re.sub(r"(?m)^\{\{chart:\s*[a-z0-9-]+\s*\}\}\s*$", "", body):
            err("the body has a {{...}} block; arguments have only {{chart: id}}")
        placed = re.findall(r"(?m)^\{\{chart:\s*([a-z0-9-]+)\s*\}\}\s*$", body)
        for i in sorted(set(cids) - set(placed)):
            err(f"chart {i!r} is declared but never placed with {{{{chart: {i}}}}}")
        for i in sorted({i for i in placed if placed.count(i) > 1}):
            err(f"chart {i!r} is placed twice")
        cited = set(re.findall(r"\[(\d{1,3})\](?!\()", body)) | {n for ch in charts for n in re.findall(r"\[(\d{1,3})\](?!\()", ch.get("caption", ""))}
        for n in sorted(cited - set(ids), key=int):
            err(f"the body cites [{n}], which is not in sources")
        try:
            refs = {i: 0 for i in set(ids) | cited}
            intro, sections = story_markdown(body, refs, set(cids))
            for ch in charts:
                ch["caption_html"] = story_inline(ch["caption"], refs)
        except SystemExit as e:
            err(str(e).replace("story: ", ""))
            continue
        used = cited | {it["source"] for it in fm.get("facts", []) if it.get("source")}
        unused = [i for i in ids if i not in used]
        if unused:
            print(f"  WARNING {f.name}: sources never cited: {', '.join(unused)}")
        words = len(re.sub(r"<[^>]+>", " ", intro + " ".join(s["html"] for s in sections)).split())
        pages[slug] = dict(slug=slug, short=short.get(slug, slug), title=fm.get("title", ""), standfirst=fm.get("standfirst", ""), updated=fm.get("updated", ""),
                           author=fm.get("author", ""), layout=fm.get("layout", "article"), status=fm.get("status", "draft"), objection=fm.get("objection", ""), answer=fm.get("answer", ""),
                           facts=fm.get("facts", []), sources=srcs, intro=intro, sections=sections, words=words,
                           charts={ch["id"]: ch for ch in charts}, card_figure=fm.get("card_figure", ""), card_label=fm.get("card_label", ""))
        print(f"  argument {slug}: {words} words, {len(sections)} sections")
    for s in order:
        if s not in pages and files and not any(e.startswith(s + ".md") for e in errors):
            errors.append(f"ARGUMENT_ORDER lists {s!r} but content/arguments/{s}.md does not exist")
    if errors:
        raise SystemExit(f"content/arguments: {len(errors)} error(s)\n  " + "\n  ".join(errors))
    return [pages[s] for s, _ in ARGUMENT_ORDER if s in pages]


def _ref(id_):
    return f'<sup class="ref"><a href="#src-{h(id_)}">[{h(id_)}]</a></sup>' if id_ else ""


def _long_date(d):
    y, m, dd = d.split("-")
    return f"{datetime.date(int(y), int(m), int(dd)).strftime('%B')} {int(dd)}, {y}"  # as the stories show it (en-US)


def argument_body(a, prev, nxt):
    """The article page's <main> content: the story article layout without the country header and tabs, a breadcrumb, and previous/next links."""
    toc = "".join(f'<li><a href="#{h(s["id"])}">{h(s["title"])}</a></li>' for s in a["sections"]) + '<li><a href="#sources">Sources</a></li>'
    facts = ('<dl class="facts">' + "".join(f'<div><dt>{h(f["label"])}</dt><dd>{h(f["value"])}{_ref(f.get("source"))}</dd></div>' for f in a["facts"]) + "</dl>") if a["facts"] else ""
    def charted(t):  # the build swaps each {{chart: id}} placeholder for its figure
        return re.sub(r'<div data-chart="([a-z0-9-]+)"></div>', lambda m: chartlib.render(a["charts"][m.group(1)], CHART_CTX), t)
    secs = "".join(f'<section class="story-sec" id="{h(s["id"])}"><h2><a class="anchor" href="#{h(s["id"])}" aria-label="Link to this section">#</a>{h(s["title"])}</h2>{charted(s["html"])}</section>' for s in a["sections"])
    srcs = ('<section class="story-sec" id="sources"><h2><a class="anchor" href="#sources" aria-label="Link to this section">#</a>Sources</h2><ol class="sources">'
            + "".join(f'<li id="src-{h(r["id"])}"><span class="sn">[{h(r["id"])}]</span> <a href="{h(r["url"])}" target="_blank" rel="noopener noreferrer nofollow">{h(r["title"])} ↗</a></li>' for r in a["sources"])
            + "</ol></section>")

    def pager(x, cls, lab):
        return f'<a class="{cls}" href="/arguments/{h(x["slug"])}"><span>{lab}</span><b>{h(x["short"])}</b></a>' if x else f'<span class="{cls} none"></span>'
    return (f'<div class="wrap fade" data-arg-page="{h(a["slug"])}"><article class="story story-article arg-page"><header class="story-head">'
            f'<nav class="crumbs" aria-label="Breadcrumb"><a href="/arguments">Arguments</a><span>/</span><span>{h(a["short"])}</span></nav>'
            f'{draft_badge(a["status"])}<p class="arg-objection">“{h(plain_quote(a["objection"]))}”</p>'
            f'<h1>{h(a["title"])}</h1><p class="standfirst">{h(a["standfirst"])}</p>'
            f'<p class="byline">{("By <b>" + h(a["author"]) + "</b> · ") if a["author"] else ""}Updated {h(_long_date(a["updated"]))} · {max(1, round(a["words"] / 220))} min read</p></header>'
            f'<div class="story-grid"><nav class="story-nav" aria-label="On this page"><details class="jump" open><summary>Jump to</summary><ol class="toc">{toc}</ol></details></nav>'
            f'<aside class="story-side"><details class="keyfacts" open><summary>Key facts</summary>{facts}</details></aside>'
            f'<div class="story-main"><div class="story-intro">{charted(a["intro"])}</div>{secs}{srcs}'
            f'<nav class="arg-pager" aria-label="More arguments">{pager(prev, "arg-prev", "← Previous")}{pager(nxt, "arg-next", "Next →")}</nav></div></div></article></div>')


def arguments_hub_body(args):
    cards = "".join(
        f'<article class="arg-card{" lead" if i == 0 else ""}"><p class="arg-n">{i + 1:02d} · {h(a["short"])}{" <span class=\"draft-pill\">Draft</span>" if a["status"] != "final" else ""}</p>'
        f'<h2 class="arg-q">“{h(plain_quote(a["objection"]))}”</h2><p class="arg-a">{h(a["answer"])}</p>'
        f'<a class="arg-go" href="/arguments/{h(a["slug"])}">{"Start here: read the answer" if i == 0 else "Read the answer"} →</a></article>' for i, a in enumerate(args))
    return (f'<div class="wrap page-head fade" data-arg-page="hub"><nav class="crumbs" aria-label="Breadcrumb"><span>Arguments</span></nav>'
            f'<div class="kicker" style="margin-top:22px">Arguments</div><h1>The objections, <em>answered.</em></h1><p class="lede">{h(ARGUMENT_HUB_INTRO)}</p>'
            f'<div class="arg-grid">{cards}</div></div>')


def arguments_index(args):
    """data/arguments.json: the hub's list and the search rows. `key` is what a search matches: titles, the objection and answer, section headings, fact labels."""
    return [dict(slug=a["slug"], short=a["short"], title=a["title"], objection=plain_quote(a["objection"]), answer=a["answer"],
                 key=" ".join([a["short"], a["title"], a["objection"], a["answer"], a["standfirst"]] + [s["title"] for s in a["sections"]] + [f["label"] for f in a["facts"]]))
            for a in args]


def referenced_countries():
    """Country folders the argument pages link to as /xx or /xx/..., for --only arguments."""
    out = set()
    for f in ARGUMENTS_DIR.glob("*.md") if ARGUMENTS_DIR.is_dir() else []:
        for m in re.finditer(r"\]\(/([a-z][a-z0-9-]*)(?:[/?#][^)]*)?\)", f.read_text(encoding="utf-8")):
            if (DATA / m.group(1) / "meta.json").exists():
                out.add(m.group(1))
    return out


PAGE_ROUTES = {"/", "/countries", "/parliaments", "/directory", "/resources", "/method", "/about", "/contribute", "/calculator", "/feedback", "/report", "/arguments", "/changelog"}


def check_argument_links(args, full, stories, preview):
    """Every internal link in the argument pages against what the build wrote. Returns (checked, problems, unchecked)."""
    from urllib.parse import urlsplit
    page_ids = {a["slug"]: set(re.findall(r'id="([^"]+)"', a["intro"] + "".join(s["html"] for s in a["sections"]))) | {s["id"] for s in a["sections"]} | {"sources"} for a in args}
    checked, problems, unchecked = 0, [], []
    for a in args:
        body = a["intro"] + "".join(s["html"] for s in a["sections"])
        for href in sorted(set(re.findall(r'href="(/[^"]*)"', body))):
            u = urlsplit(_html.unescape(href))
            path, frag = u.path.rstrip("/") or "/", u.fragment
            parts = path.strip("/").split("/")
            where = f"{a['slug']}: {_html.unescape(href)}"
            checked += 1
            if path in PAGE_ROUTES:
                continue
            if parts[0] == "arguments" and len(parts) == 2:
                if parts[1] not in page_ids:
                    problems.append(f"{where} (no such argument page)")
                elif frag and frag not in page_ids[parts[1]]:
                    problems.append(f"{where} (no section #{frag} on that page)")
                continue
            if parts[0] == "resources" and len(parts) == 2:
                if parts[1] not in RESOURCE_RAW:
                    (unchecked if preview else problems).append(where if preview else f"{where} (no bill page with that slug)")
                continue
            if not (DATA / parts[0] / "meta.json").exists():
                problems.append(f"{where} (no such route or country folder)")
                continue
            if parts[0] not in full:
                unchecked.append(where)  # a country the preview build skipped
                continue
            D = full[parts[0]]
            if len(parts) == 1:
                if frag and parts[0] in stories and frag not in {s["id"] for s in stories[parts[0]]["sections"]} | {"sources", "timeline"}:
                    problems.append(f"{where} (the story has no section #{frag})")
            elif len(parts) == 2 and parts[1] in ("story", "map", "directory", "time", "method", "seats"):
                if parts[1] == "story" and parts[0] not in stories:
                    problems.append(f"{where} (that country has no story)")
                elif parts[1] == "seats" and not D.get("legis"):
                    problems.append(f"{where} (that country has no seats page)")
            elif len(parts) == 2:
                if not any(p[0] == parts[1] for p in D["P"]):
                    problems.append(f"{where} (no such register entry)")
            else:
                problems.append(f"{where} (no such route)")
    return checked, problems, unchecked


def argument_pages(write, cards, args):
    """The hub and one page per argument, with share cards. Returns how many."""
    write("/arguments", "Arguments: the objections to a wealth tax, answered · Wealth Tax Supporters",
          "The objections people raise against a wealth tax, each answered on a page of its own with the figures, laws and court rulings behind it and a source for every number.",
          "arguments", "Arguments: the objections to a wealth tax, answered",
          lambda o: cards.page_card(o, "Arguments", "The objections, answered", "The objections to a wealth tax, each answered with sources.",
                                    [(f"{len(args)}", "objections answered"), (f"{sum(len(a['sources']) for a in args)}", "sources cited")]),
          body=arguments_hub_body(args))
    for i, a in enumerate(args):
        desc = ensure_stop(a["answer"])
        desc = desc if len(desc) <= 300 else desc[:297].rsplit(" ", 1)[0] + "…"
        write(f"/arguments/{a['slug']}", f"{plain_quote(a['objection'])} · Arguments · Wealth Tax Supporters", desc, "arguments/" + a["slug"],
              f"“{plain_quote(a['objection'])}” answered: {a['short']}",
              lambda o, a=a: cards.argument_card(o, a["objection"], a["answer"], figure=(a["card_figure"], a["card_label"]) if a["card_figure"] and a["card_label"] else None),
              body=argument_body(a, args[i - 1] if i else None, args[i + 1] if i + 1 < len(args) else None))
    return len(args) + 1


# ---------- share pages: one small HTML file per page with its own title, description and image ----------
SITE_URL = "https://wealthtaxsupporters.com"
TYPE = {"politician": "Politician", "party": "Party", "government_body": "Council or public body", "academic": "Academic",
        "economist": "Economist", "think_tank": "Think tank", "ngo_campaign": "Campaign group", "union": "Union",
        "union_official": "Union official", "journalist": "Commentator", "media_outlet": "Media outlet",
        "legal_tax_professional": "Legal or tax expert", "wealthy_individual": "Wealthy individual",
        "business_leader": "Business leader", "faith": "Faith leader or body", "cultural_figure": "Cultural figure",
        "campaigner": "Campaigner", "international_body": "International body", "funder": "Funder"}
GRADE = {"A": "Explicit support", "B": "Named support", "C": "Implied support"}
# The same plural labels as TYPES_PL in site/app.js; a page per kind of supporter lives at /directory/<slug>.
TYPE_PLURAL = {"politician": "Politicians", "party": "Parties", "government_body": "Councils and bodies", "academic": "Academics", "economist": "Economists",
               "think_tank": "Think tanks", "ngo_campaign": "Campaign groups", "union": "Unions", "union_official": "Union officials", "journalist": "Commentators",
               "media_outlet": "Media outlets", "legal_tax_professional": "Legal and tax experts", "wealthy_individual": "Wealthy individuals",
               "business_leader": "Business leaders", "faith": "Faith", "cultural_figure": "Cultural figures", "campaigner": "Campaigners",
               "international_body": "International bodies", "funder": "Funders"}


def type_slug(code):
    return re.sub(r"[^a-z]+", "-", TYPE_PLURAL.get(code, code).lower()).strip("-")


def directory_stats(index, full, countries, home_slug):
    """One entry per person: the same Wikidata id on several registers is one person (the directory does the same in the app).
    The entry kept is the one in the person's home country, else the strongest; `designs` is every design they back anywhere."""
    designs = {(c["slug"], p[0]): p[12] for c in countries for p in full[c["slug"]]["P"]}
    by = {}
    for r in index:  # [slug, id, name, type, role, place, grade, statements, qid]
        by.setdefault(r[8] or f"{r[0]}/{r[1]}", []).append(r)
    people = []
    for key, grp in by.items():
        hs = home_slug.get(key, "") if grp[0][8] else ""
        grp.sort(key=lambda r: (r[0] != hs, "ABC".find(r[6]) if r[6] in "ABC" else 3, -int(r[7] or 0)))
        b = grp[0]
        people.append(dict(slug=b[0], id=b[1], name=b[2], type=b[3], role=b[4], place=b[5], grade=b[6], n=sum(int(g[7] or 0) for g in grp),
                           slugs=sorted({g[0] for g in grp}), designs=sorted({d for g in grp for d in designs.get((g[0], g[1]), [])})))
    return dict(people=people, types=dict(collections.Counter(p["type"] for p in people).most_common()),
                designs=dict(collections.Counter(d for p in people for d in p["designs"]).most_common()),
                grades=dict(collections.Counter(p["grade"] for p in people)))
SPOKEN = {"speech", "op_ed", "statement", "interview", "social_post", "testimony", "publication", "editorial", "campaign"}


def the(name):
    return ("the " if name.startswith(("United ", "Netherlands", "Philippines", "Czech")) else "") + name


def _attr(s):
    return (s or "").replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


PRELOAD_SLUGS = set()


def calc_presets():
    """(label, resource slug) for each scheme in the calculator, from CALC_PRESETS in site/app.js."""
    js = (SITE / "app.js").read_text(encoding="utf-8")
    block = js[js.index("const CALC_PRESETS"):]
    block = block[:block.index("\n];")]
    return re.findall(r"label: '([^']+)'.*?src: \['([^']+)'", block, re.S)


def page_html(base, title, desc, path, image, alt, body=None, url_path=None):
    """The site page with this page's meta tags, so link previews show the right title and image."""
    h = base
    if body:  # a page with its own content (a bill) is rendered here; the app keeps it instead of building it again
        h = h.replace('<main id="main" tabindex="-1"></main>', '<main id="main" tabindex="-1">' + body + '</main>', 1)
    m = re.match(r"/([a-z][a-z0-9-]*)(?:/|$)", path)
    if m and m.group(1) in PRELOAD_SLUGS:  # a country page needs its own data file at once
        v = re.search(r'name="data-version" content="(\w+)"', h)
        tag = '<link rel="preload" href="/data/%s.json?v=%s" as="fetch" crossorigin>' % (m.group(1), v.group(1) if v else "")
        h = h.replace("</head>", tag + chr(10) + "</head>", 1)
    h = re.sub(r"<title>.*?</title>", f"<title>{_attr(title)}</title>", h, count=1)
    for prop, val in (("name=\"description\"", desc), ("property=\"og:title\"", title), ("property=\"og:description\"", desc),
                      ("property=\"og:url\"", SITE_URL + (url_path or path)), ("property=\"og:image\"", SITE_URL + image),
                      ("property=\"og:image:alt\"", alt)):
        h = re.sub(r'(<meta %s content=")[^"]*(")' % prop, lambda m: m.group(1) + _attr(val) + m.group(2), h, count=1)
    # the one address search engines should list for this page: no query string, so shareable calculator and filter links do not count as copies
    h = re.sub(r'<link rel="canonical"[^>]*>\s*', "", h)
    h = h.replace("</head>", '<link rel="canonical" href="%s">' % _attr(SITE_URL + (url_path or path)) + chr(10) + "</head>", 1)
    return h


def type_rows(counter):
    """(label, count) for a share card's type bars, biggest first, with the smallest types folded into one row."""
    rows = [(TYPE.get(k, k), n) for k, n in counter.most_common()]
    return rows[:5] + ([("Other types", sum(n for _, n in rows[5:]))] if len(rows) > 6 else rows[5:])


def poll_line(c):
    p = (c.get("polls") or [None])[0]
    if not p:
        return ""
    q = re.sub(r"\s*\(.*?\)", "", p["question"]).strip().rstrip("?.:;")
    if len(q) > 150:
        q = q[:150].rsplit(" ", 1)[0].rstrip(",;: ") + "…"
    return f" Poll: {whole_pct(p['support'])} in support. Asked: “{q}” ({p['pollster']}, {str(p.get('published', ''))[:4]})."


# ---------- resource pages: one page per bill (and, later, report and paper) at /resources/<slug> ----------
import html as _html

DOC_KIND = {"bill": "Bill", "amendment": "Amendment", "motion": "Motion", "petition": "Petition", "question": "Written question",
            "government_proposal": "Government proposal", "consultation": "Consultation", "committee_report": "Committee report",
            "committee_minutes": "Committee minutes", "plenary_minutes": "Plenary minutes", "roll_call": "Roll call",
            "court_ruling": "Court ruling", "audit_or_statistics_report": "Audit or statistics report", "other": "Other document"}
READ_STATUS = {"read": "Read in full", "partial": "Partly read", "skimmed": "Skimmed", "unread": "Not read yet"}
EVIDENCE_KIND = {"vote": "Vote", "bill_sponsorship": "Sponsorship", "motion_signature": "Motion signature", "open_letter": "Open letter",
                 "op_ed": "Op-ed", "policy_adoption": "Policy adopted", "coalition_membership": "Coalition", "social_post": "Social post",
                 "statement": "Statement", "campaign": "Campaign", "manifesto": "Manifesto", "speech": "Speech", "interview": "Interview",
                 "report": "Report", "publication": "Publication", "motion": "Motion", "testimony": "Testimony", "editorial": "Editorial",
                 "funding": "Funding", "other": "Other"}
# (singular, plural) for the "On the record" sentence, one per evidence_type
EVIDENCE_COUNT = {"vote": ("vote", "votes"), "bill_sponsorship": ("sponsorship", "sponsorships"), "motion_signature": ("motion signature", "motion signatures"),
                  "open_letter": ("open letter", "open letters"), "op_ed": ("op-ed", "op-eds"), "policy_adoption": ("policy adoption", "policy adoptions"),
                  "coalition_membership": ("coalition membership", "coalition memberships"), "social_post": ("social post", "social posts"),
                  "statement": ("statement", "statements"), "campaign": ("campaign record", "campaign records"), "manifesto": ("manifesto", "manifestos"),
                  "speech": ("speech", "speeches"), "interview": ("interview", "interviews"), "report": ("report", "reports"),
                  "publication": ("publication", "publications"), "motion": ("motion", "motions"), "testimony": ("testimony", "testimonies"),
                  "editorial": ("editorial", "editorials"), "funding": ("funding record", "funding records"), "other": ("other record", "other records")}
LEVEL_LABEL = {"national": "National", "subnational": "Regional or local", "supranational": "International", "local": "Local", "regional": "Regional"}
RES_KIND_ONE = {"bill": "Bill or law", "report": "Report", "paper": "Paper", "poll": "Poll"}
RES_KIND_MANY = {"bill": "Bills and laws", "report": "Reports and proposals", "paper": "Papers", "poll": "Polls"}
SITE_PATHS = []  # every page path the build wrote, for sitemap.xml


def h(s):
    return _html.escape(str(s), quote=True)


def norm_url(u):
    return re.sub(r"^https?://(www\.)?", "", (u or "").strip().lower()).split("#")[0].rstrip("/")


def alnum(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def ref_tokens(title):
    """Document numbers inside a bill's title and status that other records quote: a Riksdag motion (2013/14:Sk403) or a Dutch Kamerstuk (36 418, nr. 74)."""
    out = {alnum(m.group(0)) for m in re.finditer(r"\b\d{4}/\d{2}:[A-Za-z]*\d+", title)}
    out |= {alnum(m.group(1) + m.group(2)) for m in re.finditer(r"\b(\d{2}\s?\d{3}),\s*nr\.\s*(\d+)", title)}
    return {t for t in out if len(t) >= 6}


def ensure_stop(s):
    s = (s or "").strip()
    return s if not s or s[-1] in ".!?" else s + "."


def doc_links(raw_r, row, docs_by_country):
    """The documents.csv rows that belong to this bill: listed by id in the entry's `documents`, with the same URL as the bill or one of its
    `links`, or carrying the bill's own document number (a motion's committee report quotes it)."""
    urls = {norm_url(row["url"])} | {norm_url(l["url"]) for l in raw_r.get("links", [])}
    toks = ref_tokens(row["title"] + " " + row.get("status", ""))
    found, seen = [], set()

    def add(country, d):
        if (country, d["document_id"]) not in seen:
            seen.add((country, d["document_id"]))
            found.append((country, d))
    for ref in raw_r.get("documents", []):
        c, _, i = str(ref).partition(":")
        d = next((x for x in docs_by_country.get(c, []) if x["document_id"] == i), None)
        if d:
            add(c, d)
    for d in docs_by_country.get(row["country"], []):
        hay = alnum(" ".join((d["ref"], d["title"], d["found"], d["gaps"])))
        if norm_url(d["url"]) in urls or any(t in hay for t in toks):
            add(row["country"], d)
    return found


def resource_body(r, raw_r, people, docs, ev):
    """The page's <main> content for one resource: pre-rendered, so it reads without scripts and search engines see it."""
    country, state = r["country"], r.get("state")
    crumb = (f'<nav class="crumbs" aria-label="Breadcrumb"><a href="/resources">Resources</a><span>/</span>'
             f'<a href="/resources?kind={r["kind"]}">{h(RES_KIND_MANY.get(r["kind"], "Resources"))}</a>'
             + (f'<span>/</span><a href="/resources?country={h(country)}">{h(r["cname"])}</a>' if country != "global" else "") + "</nav>")
    facts = [("Country", r["cname"]), ("Introduced" if r["kind"] == "bill" else "Published", r["published"]),
             ("Level", LEVEL_LABEL.get(r.get("level"), (r.get("level") or "").capitalize())), ("Status", BILL_STATES.get(state, "")),
             ("Sponsors" if r["kind"] == "bill" else "By", r["by"])]
    dl = "".join(f"<div><dt>{h(k)}</dt><dd>{h(v)}</dd></div>" for k, v in facts if v)
    if r.get("status"):
        dl += f'<div><dt>Where it stands</dt><dd>{h(r["status"])}</dd></div>'
    official = [("Official text", r["url"])] + [(l.get("label") or "Official document", l["url"]) for l in raw_r.get("links", [])]
    links = "".join(f'<li><a href="{h(u)}" target="_blank" rel="noopener noreferrer nofollow">{h(lab)} ↗</a></li>' for lab, u in official)
    paras = [p.strip() for p in (raw_r.get("overview") or "").split("\n\n") if p.strip()]
    if paras:
        over = '<section class="bp-sec" id="overview"><h2>Overview</h2>' + "".join(f"<p>{h(p)}</p>" for p in paras) +             '<p class="bp-note">Written from the records and links on this page.</p></section>'
    elif r["kind"] != "bill":  # a paper or report: the summary under the title is its overview
        over = ""
    else:
        over = ('<section class="bp-sec" id="overview"><h2>Overview</h2><p class="bp-todo"><b>Detailed overview not yet written.</b> '
                'Until it is, the summary above and the sourced records below are what the register holds about this bill.</p></section>')
    ppl = ""
    if people:
        ppl = (f'<section class="bp-sec" id="people"><h2>People in the register <span class="bp-n">{len(people):,}</span></h2>'
               f'<p class="bp-note">{"Sponsors and signatories" if r["kind"] == "bill" else "Authors and others"} who are on a register, each with the statement they rest on.</p><ul class="bp-people">'
               + "".join(f'<li><a href="/{h(c)}/{h(i)}">{h(n)}</a></li>' for c, i, n in people) + "</ul></section>")
    evh = ""
    if ev:
        def item(e):
            quote = re.sub(r"\s+", " ", e["quote"]).strip()
            quote = quote if len(quote) <= 260 else quote[:260].rsplit(" ", 1)[0] + "…"
            kind = EVIDENCE_KIND.get(e["type"], e["type"].replace("_", " ").capitalize())
            return (f'<li class="bp-ev"><div class="bp-evh"><a href="/{h(e["c"])}/{h(e["actor"])}">{h(e["name"])}</a>'
                    f'<span class="tag{" signal" if e["grade"] == "A" else ""}">Grade {h(e["grade"])}</span>'
                    f'<span class="bp-m">{h(kind)}{" · " + h(e["date"]) if e["date"] else ""}</span></div>'
                    + (f'<p class="bp-q">“{h(quote)}”</p>' if quote else "")
                    + f'<a class="bp-src" href="{h(e["url"])}" target="_blank" rel="noopener noreferrer nofollow">{h(e["title"] or e["pub"] or "Source")} ↗</a></li>')
        first, rest = ev[:40], ev[40:]
        counts = collections.Counter(e["type"] for e in ev)
        summ = ", ".join(f"{n:,} {EVIDENCE_COUNT.get(t, (t.replace('_', ' '),) * 2)[n != 1]}" for t, n in counts.most_common())
        evh = (f'<section class="bp-sec" id="evidence"><h2>On the record <span class="bp-n">{len(ev):,}</span></h2>'
               f'<p class="bp-note">Statements, votes and sponsorships in the register whose source is this {"bill" if r["kind"] == "bill" else r["kind"]} or one of its documents: {h(summ)}.</p>'
               f'<ul class="bp-list">{"".join(item(e) for e in first)}</ul>'
               + (f'<details class="bp-more"><summary>Show the other {len(rest):,}</summary><ul class="bp-list">{"".join(item(e) for e in rest)}</ul></details>' if rest else "") + "</section>")
    dch = ""
    if docs:
        def ditem(d):
            meta = " · ".join(x for x in (DOC_KIND.get(d["kind"], d["kind"]), d["ref"], d["date"], d["body"]) if x)
            extra = "".join(f"<p><b>{lab}</b> {h(d[k])}</p>" for k, lab in (("found", "Found:"), ("gaps", "Not read:")) if d.get(k))
            ttl = f'<a href="{h(d["url"])}" target="_blank" rel="noopener noreferrer nofollow">{h(d["title"])} ↗</a>' if d["url"].startswith("https://") else h(d["title"])
            return (f'<li class="bp-doc"><div class="bp-evh">{ttl}<span class="tag{" signal" if d["read_status"] == "read" else ""}">{h(READ_STATUS.get(d["read_status"], d["read_status"]))}</span></div>'
                    f'<div class="bp-m">{h(meta)}</div>' + (f'<details class="bp-det"><summary>What the reading found</summary>{extra}</details>' if extra else "") + "</li>")
        dch = (f'<section class="bp-sec" id="documents"><h2>Official documents <span class="bp-n">{len(docs):,}</span></h2>'
               f'<p class="bp-note">From the records tracker for {h(r["cname"])}: {"the bill" if r["kind"] == "bill" else "this " + r["kind"]}, its debates, votes and committee reports, and whether each has been read in full.</p>'
               f'<ul class="bp-list">{"".join(ditem(d) for _, d in docs)}</ul></section>')
    head = (f'<div class="wrap page-head fade bp-head">{crumb}'
            f'<div class="kicker" style="margin-top:22px">{h(RES_KIND_ONE.get(r["kind"], r["kind"]))} · {h(r["cname"])}</div>'
            f'<h1>{h(r["title"])}</h1>'
            + (f'<span class="bp-state bp-{h(state)}">{h(BILL_STATES.get(state, state))}</span>' if state else "")
            + (f'<p class="lede">{h(ensure_stop(r.get("summary")))}</p>' if r.get("summary") else "") + "</div>")
    return (f'<article data-res-page="{h(r["slug"])}">{head}<div class="wrap bp-body"><div class="bp-main">{over}{evh}{dch}{ppl}</div>'
            f'<aside class="bp-side"><dl class="bp-facts">{dl}</dl><div class="kicker">Official links</div><ul class="alinks">{links}</ul>'
            f'<p class="bp-note" style="margin-top:22px">Something wrong or missing? <a href="/report">Report a mistake</a>.</p></aside></div></article>')


def short_title(title):
    """A title for a share card: the whole title if it fits, else the part before the colon; the English words in brackets for another script."""
    t = re.sub(r"\s+", " ", title).strip()
    if any(ord(c) > 0x24F for c in t):
        m = re.search(r"\(([^()]*)\)\s*$", t)
        t = m.group(1) if m else t
    if len(t) > 90:
        t = re.split(r":\s", t, 1)[0]
    return t if len(t) <= 110 else t[:107].rsplit(" ", 1)[0] + "…"


def resource_pages(write, resources, full, cards, countries):
    """One page per resource whose kind is in PAGE_KINDS. Returns how many."""
    docs_by_country = {c["slug"]: rd(DATA / c["slug"] / "documents.csv") for c in countries}
    names, ev_by_url = {}, collections.defaultdict(list)
    for c in countries:
        names.update({(c["slug"], p[0]): p[1] for p in full[c["slug"]]["P"]})
        for e in full[c["slug"]]["E"]:
            ev_by_url[(c["slug"], norm_url(e[7]))].append(e)
    n = 0
    for r in resources:
        if r["kind"] not in PAGE_KINDS or "slug" not in r:
            continue
        raw_r = RESOURCE_RAW[r["slug"]]
        docs = doc_links(raw_r, r, docs_by_country)
        urls = {norm_url(r["url"])} | {norm_url(l["url"]) for l in raw_r.get("links", [])} | {norm_url(d["url"]) for _, d in docs if d["url"]}
        seen, ev = set(), []
        for u in sorted(urls):
            for e in ev_by_url.get((r["country"], u), []):
                if e[11] not in seen:
                    seen.add(e[11])
                    ev.append(dict(actor=e[0], date=e[1], grade=e[2], type=e[3], quote=e[6], url=e[7], title=e[8], pub=e[9], c=r["country"],
                                   name=names.get((r["country"], e[0]), e[0])))
        # evidence the tracker names in a document's `found` text (E00022, E00043-E00044)
        ids = set()
        for _, d in docs:
            for a, b2 in re.findall(r"E(\d{5})(?:\s*-\s*E?(\d{5}))?", d.get("found", "")):
                ids |= {f"E{i:05d}" for i in range(int(a), int(b2 or a) + 1)}
        for e in full[r["country"]]["E"] if r["country"] in full else []:
            if e[11] in ids and e[11] not in seen:
                seen.add(e[11])
                ev.append(dict(actor=e[0], date=e[1], grade=e[2], type=e[3], quote=e[6], url=e[7], title=e[8], pub=e[9], c=r["country"],
                               name=names.get((r["country"], e[0]), e[0])))
        ev.sort(key=lambda e: (e["grade"], e["type"] != "vote", e["date"] or "", e["name"]))
        people = r.get("people", [])
        year = str(r["published"])[:4]
        desc = " ".join(x for x in (ensure_stop(r.get("summary")), f"{BILL_STATES.get(r.get('state')) or RES_KIND_ONE.get(r['kind'], 'Listed')} · {r['cname']}, {year}.") if x)
        desc = desc if len(desc) <= 300 else desc[:297].rsplit(" ", 1)[0] + "…"
        pts = [(BILL_STATES.get(r.get("state"), "") or "Listed", "status"), (year, "introduced")] if r["kind"] == "bill" else [(RES_KIND_ONE.get(r["kind"], "Listed"), "type"), (year, "published")]
        if people:
            pts.append((f"{len(people):,}", "people in the register"))
        if ev:
            pts.append((f"{len(ev):,}", "sourced records"))
        kind1, st = RES_KIND_ONE.get(r["kind"], "Resource"), short_title(r["title"])
        write(f"/resources/{r['slug']}", f"{st} · {r['cname']} · Wealth Tax Supporters", desc, "resources/" + r["slug"],
              f"{st}: {kind1}, {r['cname']}",
              lambda o, r=r, pts=pts, kind1=kind1, st=st: cards.page_card(o, f"{kind1} · {r['cname']}", st, r.get("summary", ""), pts),
              body=resource_body(r, raw_r, people, docs, ev))
        n += 1
    return n


def poll_date(s):
    """2026-02-11 to 2026-02-26 -> 11 to 26 February 2026; a lone YYYY-MM-DD or YYYY-MM -> the date or month."""
    import datetime
    def one(t):
        try:
            d = datetime.date.fromisoformat(t)
            return f"{d.day} {d.strftime('%B %Y')}"
        except ValueError:
            try:
                d = datetime.datetime.strptime(t, "%Y-%m")
                return d.strftime("%B %Y")
            except ValueError:
                return t
    parts = [x.strip() for x in str(s or "").split(" to ")]
    if len(parts) == 2 and re.fullmatch(r"\d{4}-\d{2}-\d{2}", parts[0]) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", parts[1]) and parts[0][:7] == parts[1][:7]:
        return f"{int(parts[0][8:])} to {one(parts[1])}"  # 11 to 26 February 2026
    return " to ".join(one(x) for x in parts) if parts != [""] else ""


def poll_body(r, p, siblings):
    """The page for one poll: the figure, the question as asked, how it was done, and the other polls of the country."""
    fig = whole_pct(p["support"]) if p.get("support") is not None else ""
    crumb = ('<nav class="crumbs" aria-label="Breadcrumb"><a href="/resources">Resources</a><span>/</span><a href="/resources?kind=poll">Polls</a>'
             f'<span>/</span><a href="/resources?country={h(r["country"])}">{h(r["cname"])}</a></nav>')
    facts = [("Country", r["cname"]), ("Who was asked", p.get("scope")), ("Pollster", p.get("pollster")), ("Commissioned by", p.get("commissioned_by")),
             ("Fieldwork", poll_date(p.get("fieldwork"))), ("Sample", p.get("sample")), ("Published", poll_date(p.get("published")))]
    dl = "".join(f"<div><dt>{h(k)}</dt><dd>{h(v)}</dd></div>" for k, v in facts if v)
    asked = f'<p class="pp-q">{h(p["question"])}</p>'
    if p.get("question_original"):
        asked += f'<p class="bp-note">In the original: <i>{h(p["question_original"])}</i></p>'
    note = (f'<section class="bp-sec" id="detail"><h2>In more detail</h2><p>{h(ensure_stop(p["support_text"]))}</p></section>') if p.get("support_text") else ""
    others = ""
    if siblings:
        others = ('<section class="bp-sec" id="others"><h2>Other polls in ' + h(r["cname"]) + '</h2><ul class="bp-list">' + "".join(
            f'<li><a href="/resources/{h(s["slug"])}"><b>{h(s["fig"])}</b> · {h(s["by"].split(" for ")[0])}, {h(str(s["published"])[:4])}</a></li>' for s in siblings) + "</ul></section>")
    head = (f'<div class="wrap page-head fade bp-head">{crumb}<div class="kicker" style="margin-top:22px">Poll · {h(r["cname"])}</div>'
            f'<div class="pp-fig">{h(fig)}<span>in support</span></div>'
            f'<h1>{h(r["title"])}</h1>'
            f'<p class="lede">{h(ensure_stop(r.get("summary")))}</p></div>')
    return (f'<article data-res-page="{h(r["slug"])}">{head}<div class="wrap bp-body"><div class="bp-main">'
            f'<section class="bp-sec" id="asked"><h2>What was asked</h2>{asked}</section>{note}{others}</div>'
            f'<aside class="bp-side"><dl class="bp-facts">{dl}</dl><div class="kicker">The poll</div>'
            f'<ul class="alinks"><li><a href="{h(r["url"])}" target="_blank" rel="noopener noreferrer nofollow">Source of the figure ↗</a></li>'
            f'<li><a href="/{h(r["country"])}">{h(r["cname"])} on the register</a></li></ul>'
            f'<p class="bp-note" style="margin-top:22px">Something wrong or missing? <a href="/report">Report a mistake</a>.</p></aside></div></article>')


def poll_pages(write, resources, cards):
    """One page per poll at /resources/<slug>, and the polls list at /resources/polls (served for /resources?kind=poll by the Worker)."""
    polls = [r for r in resources if r["kind"] == "poll" and r.get("slug") in POLL_RAW]
    by_country = collections.defaultdict(list)
    for r in polls:
        by_country[r["country"]].append(r)
    for r in polls:
        p = POLL_RAW[r["slug"]]
        fig = whole_pct(p["support"]) if p.get("support") is not None else ""
        src = ", ".join(x for x in (p.get("pollster"), str(p.get("published", ""))[:4]) if x)
        q = short_title(r["title"])
        desc = f"{fig} in support of a wealth tax: “{q}” {src}. {r['cname']}." if fig else f"“{q}” {src}. {r['cname']}."
        desc = desc if len(desc) <= 300 else desc[:297].rsplit(" ", 1)[0] + "…"
        write(f"/resources/{r['slug']}", f"{fig} in support of a wealth tax" + f" · {r['cname']} · Wealth Tax Supporters" if fig else f"Poll · {r['cname']} · Wealth Tax Supporters", desc, "resources/" + r["slug"],
              f"{fig} in support, {r['cname']}: {src}",
              lambda o, r=r, p=p, fig=fig, src=src: cards.poll_card(o, r["country"], r["cname"], fig, p["question"], src, p.get("scope") or ""),
              body=poll_body(r, p, [s for s in by_country[r["country"]] if s["slug"] != r["slug"]]))
    best = {}
    for r in polls:
        v = POLL_RAW[r["slug"]].get("support")
        if v is not None and (r["country"] not in best or v > best[r["country"]][2]):
            best[r["country"]] = (r["country"], r["cname"], v)
    rows = sorted(((c, n, int(float(v) + 0.5)) for c, n, v in best.values()), key=lambda t: (-t[2], t[1]))
    write("/resources/polls", f"Polls on a wealth tax: {len(rows)} countries · Wealth Tax Supporters",
          f"{len(polls)} published polls from {len(by_country)} countries on a wealth tax, with the highest result in each country: " + ", ".join(f"{n} {v}%" for _, n, v in rows[:5]) + " and more.",
          "resources/polls", "Polls on a wealth tax: a flag and a percentage for each country",
          lambda o: cards.polls_card(o, rows, "The highest published poll in each country."),
          body=sp.polls_body(polls, POLL_RAW), url_path="/resources?kind=poll")


def share_pages(out, base, countries, full, unique=None, bodies=(), resources=(), stories=None, arguments=(), dirstats=None):
    stories = stories or {}
    PRELOAD_SLUGS.update(c["slug"] for c in countries)
    """Writes per-page HTML (and share images when Pillow is installed). Returns the number of pages."""
    try:
        import share_cards as cards
    except ImportError:
        cards = None
        print("  Pillow not installed: pages get text previews and the default image (pip install pillow)")
    pages = 0
    SITE_PATHS.clear()

    def write(path, title, desc, image_key, alt, draw, body=None, url_path=None):
        nonlocal pages
        SITE_PATHS.append(url_path or path)
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
        dest.write_text(page_html(base, title, desc, path, img, alt, body, url_path), encoding="utf-8")
        pages += 1

    # One person on several countries' registers counts once in the world totals (same Wikidata id); each country keeps its own count.
    tot = dict(supporters=unique if unique is not None else sum(c["supporters"] for c in countries), evidence=sum(c["evidence"] for c in countries), countries=len(countries))
    write("/", "Wealth Tax Supporters: who backs a wealth tax near you?",
          f"{tot['supporters']:,} public figures and organisations across {tot['countries']} countries who have backed a wealth tax on the record. Every name links to its source.",
          "home", "Who backs a wealth tax near you?",
          lambda o: cards.home_card(o, tot, type_rows(collections.Counter(dirstats["types"]))),
          body=sp.home_body(tot, countries))
    write("/method", "How the register is built · Wealth Tax Supporters",
          "What counts as support for a wealth tax, how statements are sourced and graded, and how to report a mistake.",
          "method", "How the register is built", lambda o: cards.method_card(o, [dirstats["grades"].get(g, 0) for g in "ABC"], "Sourced, graded and open: every name links to where they said it."),
          body=sp.method_body([dirstats["grades"].get(g, 0) for g in "ABC"]))
    write("/countries", "Countries · Wealth Tax Supporters",
          f"The {tot['countries']} countries researched so far, with supporters found and seats in the national chambers.",
          "countries", "Country by country", lambda o: cards.countries_card(o, [(c["slug"], c["name"]) for c in sorted(countries, key=lambda c: -c["supporters"])], "Each one researched separately, with its own map, polls and seats."),
          body=sp.countries_body(countries))
    write("/resources", "Resources: polls, papers, reports and bills · Wealth Tax Supporters",
          "Polls, research papers, reports and bills on a wealth tax, from every country in the register and beyond, filterable by place and type.",
          "resources", "Resources on a wealth tax", lambda o: cards.resources_card(
              o, [(lab, sum(1 for r in resources if r["kind"] == k)) for k, lab in (("poll", "Polls"), ("paper", "Papers"), ("report", "Reports"), ("bill", "Bills"))],
              [(lab, n) for k, lab in BILL_STATES.items() if (n := sum(1 for r in resources if r["kind"] == "bill" and r.get("state") == k))],
              "The evidence and the law on a wealth tax."),
          body=sp.resources_body(resources))
    write("/about", "About · Wealth Tax Supporters",
          "An open, sourced register of the public figures and organisations that back a wealth tax on the record: why it exists, how it is made and how to take part.",
          "about", "About Wealth Tax Supporters", lambda o: cards.page_card(o, "About", "A register of who says so", "Open, sourced and made in public.",
                                    [(f"{tot['supporters']:,}", "supporters on the record"), (f"{tot['countries']}", "countries so far"), (f"{tot['evidence']:,}", "sourced statements")]),
          body=sp.about_body(tot, sum(x[1] for c in list(countries) + list(bodies) for x in (c.get("chambers") or []))))
    write("/changelog", "Changelog · Wealth Tax Supporters",
          "What changed in the register each day: supporters and statements added by country, new countries, stories and corrections.",
          "changelog", "Changelog", lambda o: cards.page_card(o, "Changelog", "What changed, day by day", "Supporters, statements and stories added, by country.",
                                    [(f"{tot['supporters']:,}", "supporters on the record"), (f"{tot['countries']}", "countries so far"), (f"{tot['evidence']:,}", "sourced statements")]),
          body=sp.changelog_body(json.loads((DATA / "changelog.json").read_text(encoding="utf-8")) if (DATA / "changelog.json").exists() else []))
    write("/contribute", "Contribute and suggest a supporter · Wealth Tax Supporters",
          "Suggest a public figure or organisation who has backed a wealth tax, help check the entries already here, or start a register for your country.",
          "contribute", "Help build the register", lambda o: cards.page_card(o, "Contribute", "Help build the register", "Suggest a supporter, help check entries, or start a country.",
                                    [("1", "Suggest a supporter"), ("2", "Check an entry's source"), ("3", "Start a country")]),
          body=sp.contribute_body())
    def top_countries(people, n=6):
        c = collections.Counter(p["slug"] for p in people)
        nm = {x["slug"]: x["name"] for x in countries}
        return [(slug, nm.get(slug, slug), k) for slug, k in c.most_common(n)]
    write("/directory", "The global directory · Wealth Tax Supporters",
          f"{tot['supporters']:,} public figures and organisations in {tot['countries']} countries who have backed a wealth tax, filterable by country, type and strength of evidence.",
          "directory", "The global directory",
          lambda o: cards.directory_all_card(o, tot["supporters"], tot["countries"], top_countries(dirstats["people"])),
          body=sp.directory_global_body(countries))
    for code, n_type in dirstats["types"].items():
        if n_type < 25:
            continue
        plural, slug_t = TYPE_PLURAL.get(code, code), type_slug(code)
        ppl = sorted((p for p in dirstats["people"] if p["type"] == code), key=lambda p: ("ABC".find(p["grade"]), -p["n"], p["name"]))
        spread = len({s for p in ppl for s in p["slugs"]})
        write(f"/directory/{slug_t}", f"{plural} who back a wealth tax · Directory · Wealth Tax Supporters",
              f"{n_type:,} {plural.lower()} in {spread} countries who have backed a wealth tax on the record, each with the statement they rest on.",
              f"directory-{slug_t}", f"{plural} who back a wealth tax: {n_type:,} found so far",
              lambda o, plural=plural, n_type=n_type, ppl=ppl, spread=spread: cards.directory_type_card(
                  o, plural, n_type, spread, top_countries(ppl, 5), [p["name"] for p in ppl[:6]]),
              body=sp.directory_type_body(plural, ppl[:300], {x["slug"]: x["name"] for x in countries}))
    write("/feedback", "Feedback and bug reports · Wealth Tax Supporters",
          "Something broken, confusing or missing? Send feedback or report a bug. No account needed.",
          "feedback", "Feedback and bug reports", lambda o: cards.page_card(o, "Feedback", "Tell us what to fix or improve", "Feedback, ideas and bug reports. No account needed.",
                                    [("1", "Report a bug"), ("2", "Suggest an improvement"), ("3", "Flag a mistake")]))

    write("/calculator", "Wealth tax bracket calculator · Wealth Tax Supporters",
          "Try real wealth taxes, in force, ended and proposed, from Spain and Norway to the US and Germany, or set your own brackets. Only the part above each line is taxed.",
          "calculator", "Wealth tax bracket calculator", lambda o: cards.calculator_card(o, [
              # the same bracket tables as CALC_PRESETS in site/app.js, all in euro
              ("Spain, in force", [(3700000, 1.7), (6047998.03, 2.1), (11395996.06, 3.5)], cards.SIGNAL),
              ("Austria, SPÖ", [(1000000, 0.5), (10000000, 1), (50000000, 2)], cards.INK),
              ("France, ISF", [(800000, 0.5), (1300000, 0.7), (2570000, 1), (5000000, 1.25), (10000000, 1.5)], (40, 90, 170)),
              ("Finland, Left", [(1000000, 0.5)], cards.INK3)],
              "Try a real wealth tax on your own numbers",
              "Scales from Spain to the US, in force, ended and proposed. Only the part above each line is taxed. Change the rates and share the result."),
              body=sp.calculator_body(calc_presets()))

    write("/report", "Report a mistake · Wealth Tax Supporters",
          "Something wrong in an entry, or want one about you removed or corrected? Tell us here. No account needed.",
          "report", "Report a mistake", lambda o: cards.page_card(o, "Report", "Spotted a mistake?", "Wrong, broken or out of date? Tell us, with a source if you can.",
                                    [("1", "Say which entry"), ("2", "Say what is wrong"), ("3", "Link a source")]))

    # The Parliaments page and the bodies above the countries (the European Parliament, the UN General Assembly): their own previews,
    # a seats page, and one page per sitting supporter.
    # Chambers, sitting supporters and seats across every country and body with a seat chart.
    legis_all = [b for x in list(countries) + list(bodies) for b in full[x["slug"]].get("legis", [])]
    chambers = (len(legis_all), sum(len(q[3]) for b in legis_all for q in b["parties"]), sum(b["seats"] for b in legis_all))
    write("/parliaments", "Parliaments · Wealth Tax Supporters",
          f"Which seats in the legislatures of {tot['countries']} countries, and in the European Parliament and the UN General Assembly, are held by a sitting supporter of a wealth tax, found so far.",
          "parliaments", "Seats in every parliament",
          lambda o: cards.parliaments_card(o, *chambers, "Who sits today and has backed a wealth tax. Unlit seats mean nothing found, never opposition."),
          body=sp.parliaments_body(countries, bodies))
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
                      lambda o, b=b, legis=legis: cards.seats_card(o, b, legis, "held by a sitting supporter of a wealth tax, found so far. Unlit seats mean nothing found, never opposition.", slug),
                      body=sp.seats_body(b, D, name))
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
                      o, {"name": p[1], "role": role}, name, quote, [], set(), TYPE.get(p[3], p[3]), gradeline, slug, (p[8], GRADE.get(p[8], ""), p[9], span if y0 else "")),
                  body=sp.person_body(slug, name, p, es, TYPE.get(p[3], p[3]), GRADE.get(p[8], "")))

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
        st = stories.get(slug)
        if st:  # a country with a story opens on it: /xx and /xx/story are the story, and the map moves to /xx/map
            map_page = sections.pop("")
            sections = {"story": (st["title"], "Story", st["standfirst"], st["standfirst"]),
                        "map": (f"Map · {name}", "Map · where supporters are", found, map_page[3]), **sections}
        if D.get("legis"):
            sections["seats"] = (f"Seats · {name}", "Seats · who sits in the legislature", found,
                                 f"Which seats in {the(name)}'s legislature are held by supporters of a wealth tax, found so far, by party.")
        for sec, (title, kicker, sub, desc) in sections.items():
            n_sub = c["evidence"] if sec == "time" else c["supporters"]
            cc = dict(c, supporters=n_sub)
            if sec == "seats":
                # A country with chambers at more than one level gets a page and a card for each: /xx/seats is the national one, /xx/seats/regional the next.
                lvl = lambda b: b.get("level") or "national"
                present = [l for l in ("national", "regional", "local", "supranational") if any(lvl(b) == l for b in D["legis"])]
                multi = len(present) > 1
                for lv in (present if multi else [None]):
                    chosen = [b for b in D["legis"] if not multi or lvl(b) == lv]
                    bodies = [dict(name=b["name"], seats=b["seats"], parties=[[q[0], q[1], q[2], len(q[3])] for q in b["parties"]]) for b in chosen]
                    lit = sum(q[3] for b in bodies for q in b["parties"])
                    nseats = sum(b["seats"] for b in bodies)
                    first = lv is None or lv == present[0]
                    label = LEVEL_LABEL.get(lv, "") if multi else ""
                    what = {"national": "national legislature", "regional": "regional parliaments and assemblies", "local": "local councils", "supranational": "international bodies"}.get(lv, "legislature")
                    more = (" Also counted: " + ", ".join(b["name"] for b in bodies[2:4]) + (f" and {len(bodies) - 4} more" if len(bodies) > 4 else "") + ".") if len(bodies) > 2 else ""
                    write(f"/{slug}/seats" + ("" if first else f"/{lv}"),
                          f"{title} · Wealth Tax Supporters" if first else f"{label} seats · {name} · Wealth Tax Supporters",
                          f"{lit:,} of {nseats:,} seats in {the(name)}'s {what if multi else 'legislature'} are held by a sitting supporter of a wealth tax, found so far, shown by party.",
                          slug + ("-seats" if first else f"-seats-{lv}"), f"{label + ' ' if multi else ''}{title}: {lit:,} seats held by supporters found so far".replace("  ", " "),
                          lambda o, cc=cc, bodies=bodies, more=more, label=label, multi=multi: cards.seats_card(
                              o, cc, bodies, "held by a sitting supporter of a wealth tax, found so far. Unlit seats mean nothing found, never opposition." + more, slug,
                              kicker=f"Seats · {label} chambers" if multi else "Seats · who sits in the legislature"),
                          body=sp.seats_body(c, D, the(name), lv))
                continue
            if sec == "directory":
                write(f"/{slug}/directory", f"{title} · Wealth Tax Supporters", desc, slug + "-directory", f"{title}: {c['supporters']:,} found so far",
                      lambda o, cc=cc: cards.directory_card(o, cc["name"], cc["supporters"], "public figures and organisations on the record so far",
                                                            type_rows(collections.Counter(cc.get("types") or {})), [(GRADE[g], cc[g]) for g in "ABC"], slug),
                      body=sp.directory_body(c, D, the(name)))
                continue
            if sec == "time":
                per_year = collections.Counter(e[1][:4] for e in D["E"] if e[1])
                write(f"/{slug}/time", f"{title} · Wealth Tax Supporters", desc, slug + "-time", f"{title}: {c['evidence']:,} statements",
                      lambda o, cc=cc, per_year=per_year, sub=sub: cards.time_card(o, cc, per_year, sub),
                      body=sp.time_body(c, per_year, the(name)))
                continue
            if sec == "method":
                n_res = collections.Counter(r["kind"] for r in resources if r["country"] == slug)
                extra = " · ".join(f"{n_res[k]} {lab if n_res[k] != 1 else lab[:-1]}" for k, lab in (("poll", "polls"), ("bill", "bills"), ("paper", "papers"), ("report", "reports")) if n_res[k])
                write(f"/{slug}/method", f"{title} · Wealth Tax Supporters", desc, slug + "-method", f"{title}: {c['supporters']:,} found so far",
                      lambda o, cc=cc, extra=extra: cards.country_method_card(o, cc, [cc[g] for g in "ABC"], extra),
                      body=sp.method_country_body(c, extra, the(name)))
                continue
            if sec == "story":
                for path in (f"/{slug}", f"/{slug}/story"):
                    write(path, f"{title} · Wealth Tax Supporters", desc, slug + "-story", f"{title}: a country story",
                          lambda o, cc=cc, st=st, units=units: cards.story_card(o, cc, units, st["title"], st["standfirst"]),
                          body=sp.story_body(c, st, the(name)))
                continue
            write(f"/{slug}" + (f"/{sec}" if sec else ""), f"{title} · Wealth Tax Supporters", desc, slug + (f"-{sec}" if sec else ""),
                  f"{title}: {c['supporters']:,} found so far",
                  lambda o, cc=cc, kicker=kicker, sub=sub: cards.country_card(o, cc, units, kicker, sub),
                  body=sp.country_body(c, D, the(name)) if sec in ("", "map") else None)
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
                      units if hl else [], hl, TYPE.get(p[3], p[3]), gradeline, slug, (p[8], GRADE.get(p[8], ""), p[9], span if y0 else "")),
                  body=sp.person_body(slug, name, p, es, TYPE.get(p[3], p[3]), GRADE.get(p[8], "")))
    resource_pages(write, resources, full, cards, countries)
    poll_pages(write, resources, cards)
    if arguments:
        argument_pages(write, cards, arguments)
    return pages


def write_sitemap(out, built, preview):
    """sitemap.xml (every page the build wrote, split at 45,000 URLs) and robots.txt pointing to it. A preview build writes neither."""
    if preview:
        return
    nl, head = chr(10), '<?xml version="1.0" encoding="UTF-8"?>' + chr(10)
    chunks = [SITE_PATHS[i:i + 45000] for i in range(0, len(SITE_PATHS), 45000)] or [[]]
    names = ["sitemap.xml"] if len(chunks) == 1 else [f"sitemap-{i + 1}.xml" for i in range(len(chunks))]
    for name, chunk in zip(names, chunks):
        rows = "".join(f"<url><loc>{SITE_URL}{p}</loc><lastmod>{built}</lastmod></url>" for p in chunk)
        (out / name).write_text(head + '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + rows + "</urlset>" + nl, encoding="utf-8")
    if len(names) > 1:
        idx = "".join(f"<sitemap><loc>{SITE_URL}/{n}</loc><lastmod>{built}</lastmod></sitemap>" for n in names)
        (out / "sitemap.xml").write_text(head + '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + idx + "</sitemapindex>" + nl, encoding="utf-8")
    (out / "robots.txt").write_text(f"User-agent: *{nl}Allow: /{nl}{nl}Sitemap: {SITE_URL}/sitemap.xml{nl}", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    ap.add_argument("--strict-links", action="store_true", help="fail the build when an internal link in an argument page does not resolve (the default only prints them)")
    ap.add_argument("--only", metavar="FOLDER", nargs="+",
                    help="preview build: only these country folders (for example --only co), or 'arguments' for the Arguments section with the countries its pages link to. Fast; skips supranational registers, "
                         "so world totals are partial. Writes to _site_only by default and is never what you deploy.")
    args = ap.parse_args()
    only = set(args.only or [])
    global ARGUMENTS_ONLY
    if "arguments" in only:  # --only arguments: the arguments section with the countries its pages link to (plus any folders named beside it)
        only.discard("arguments")
        ARGUMENTS_ONLY = True
        only |= referenced_countries()
    ONLY.update(only)
    if only:
        missing = sorted(f for f in only if not (DATA / f / "meta.json").exists())
        if missing:
            sys.exit(f"--only: no such country folder under data/: {', '.join(missing)}")
        print(f"PREVIEW BUILD of {', '.join(sorted(only))}{' and the arguments' if ARGUMENTS_ONLY else ''} only: totals are partial, do not deploy this output.")
    out = Path(args.out or ROOT / ("_site_only" if only else "_site"))
    if out.exists():
        shutil.rmtree(out)
    (out / "data").mkdir(parents=True)
    # Every file in site/ except the page and the vendored map source is copied as is.
    assets = [f for f in SITE.iterdir() if f.is_file() and f.name != "index.html"]
    for f in assets:
        shutil.copy(f, out / f.name)
    if (SITE / "fonts").is_dir():  # self-hosted fonts
        shutil.copytree(SITE / "fonts", out / "fonts")
    if (SITE / "vendor" / "flags").is_dir():  # country flags (Wikimedia Commons originals), shown next to country names
        shutil.copytree(SITE / "vendor" / "flags", out / "flags")
    # A content hash in each asset URL makes updates show at once despite caching.
    html = (SITE / "index.html").read_text(encoding="utf-8")
    for f in assets:
        if f.suffix in (".js", ".css", ".svg"):
            h = hashlib.md5(f.read_bytes()).hexdigest()[:8]
            html = html.replace(f'"/{f.name}"', f'"/{f.name}?v={h}"')
    arguments = load_arguments()  # validates every page first: a bad page fails the build before the slow part
    countries, index, places, full, stories = [], [], [], {}, {}
    supras = []
    for folder in sorted(DATA.iterdir()):
        if folder.is_dir() and (folder / "meta.json").exists():
            if only and folder.name not in only:
                continue
            if json.load(open(folder / "meta.json", encoding="utf-8")).get("supranational"):
                supras.append(folder)  # built after the countries: its people live in their registers
                continue
            summary, country, idx, pl = build_country(folder)
            summary["numeric"] = numeric_for(summary["iso2"].split("-")[0])
            story = load_story(folder.name)
            if story:  # the story itself is a separate file, loaded only by the Story tab; the summary says that one exists
                summary["story"] = dict(layout=story["layout"], title=story["title"])
                json.dump(story, open(out / "data" / f"story-{folder.name}.json", "w", encoding="utf-8"), separators=(",", ":"), ensure_ascii=False)
                stories[folder.name] = story
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
    wt_status = {}
    if (DATA / "wealth_tax_status.csv").exists():
        for r in csv.DictReader(open(DATA / "wealth_tax_status.csv", encoding="utf-8")):
            n = numeric_for(r["iso2"])
            if n:
                wt_status[n] = r["status"]
    home_slug = {q: next((c["slug"] for c in countries if c["iso2"].upper() == h), "") for q, h in people_home()[0].items()}
    dirstats = directory_stats(index, full, countries, home_slug)
    world = dict(unique_supporters=unique, types=dirstats["types"], designs=dirstats["designs"], grades=dirstats["grades"], home=home_slug, countries=countries, wt_status=wt_status, bodies=bodies, planned=planned, resources=world_resources, all_countries=sorted(every), built=datetime.date.today().isoformat())
    json.dump(world, open(out / "data" / "world.json", "w", encoding="utf-8"), separators=(",", ":"), ensure_ascii=False)
    if (DATA / "changelog.json").exists():
        shutil.copy(DATA / "changelog.json", out / "data" / "changelog.json")
    json.dump(arguments_index(arguments), open(out / "data" / "arguments.json", "w", encoding="utf-8"), separators=(",", ":"), ensure_ascii=False)
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
    polls_best, poll_stats = chartlib.poll_stats(countries)
    status_rows = list(csv.DictReader(open(DATA / "wealth_tax_status.csv", encoding="utf-8"))) if (DATA / "wealth_tax_status.csv").exists() else []
    CHART_CTX.update(polls_best=polls_best, stats=poll_stats, paths=paths, status_map=chartlib.status_by_numeric(status_rows, numeric_for) if status_rows else {})
    n = share_pages(out, html, countries, full, unique, bodies, world_resources, stories, arguments, dirstats=dirstats)
    if arguments:
        checked, bad, skipped = check_argument_links(arguments, full, stories, bool(only))
        print(f"Argument links: {checked} internal links checked, {len(bad)} problem{'' if len(bad) == 1 else 's'}" + (f", {len(skipped)} not checked (country not in this preview build)" if skipped else ""))
        for b in bad:
            print(f"  BROKEN LINK {b}")
        if bad and args.strict_links:
            sys.exit("argument links: " + str(len(bad)) + " broken")
    write_sitemap(out, world["built"], only)
    print(f"Built {len(countries)} countr{'y' if len(countries) == 1 else 'ies'} and {n} share pages into {out}")


if __name__ == "__main__":
    sys.exit(main())
