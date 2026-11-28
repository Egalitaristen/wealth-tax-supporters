#!/usr/bin/env python3
"""Add outlying territories to a country map: their register units in geo_units.csv and their outlines as insets.

Run once per country (it refuses to add a unit that is already there). Download the shape files first; each source
and licence is written into boundaries.json, which the country's Method page prints.

  python scripts/add_territory_insets.py us counties-10m.json tw-names.json
      us-atlas@3 counties-10m.json (https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json); names and codes of the
      county equivalents from TIGERweb State_County layer 1, queried with outFields=GEOID,NAME,STATE, f=json
  python scripts/add_territory_insets.py fr FOLDER
      FOLDER holds communes-, departements- and regions-1000m.geojson.gz from
      https://etalab-datasets.geo.data.gouv.fr/contours-administratifs/2025/geojson/
  python scripts/add_territory_insets.py gb
      site/vendor/countries-50m.json (Natural Earth 1:50m via world-atlas), already in the repository

Each inset keeps the shapes' proportions (equirectangular at its own latitude) and is scaled to fill its box, so
insets are not at the scale of the main map or of each other. The Isle of Man is drawn where it is.
"""
import argparse, csv, gzip, json, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skill" / "scripts"))
from topo_to_boundaries import decode, ring_points, simplify  # noqa: E402


def topo_shapes(path, obj):
    """{id: (name, rings of (lon, lat))} from a TopoJSON object."""
    topo = json.load(open(path, encoding="utf-8"))
    arcs, out = decode(topo), {}
    for g in topo["objects"][obj]["geometries"]:
        polys = g.get("arcs") or []
        polys = polys if g["type"] == "MultiPolygon" else [polys]
        out[str(g.get("id", ""))] = ((g.get("properties") or {}).get("name", ""),
                                     [ring_points(arcs, r) for p in polys for r in p])
    return out


def geojson_shapes(path):
    out = {}
    for f in json.load(gzip.open(path, "rt", encoding="utf-8"))["features"]:
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        out[f["properties"]["code"]] = (f["properties"]["nom"], [[(p[0], p[1]) for p in r] for poly in polys for r in poly])
    return out


def fitter(rings, box):
    """lon/lat -> canvas, so that all these rings fill the box (x, y, w, h), centred, proportions kept."""
    lons = [p[0] for r in rings for p in r]
    lats = [p[1] for r in rings for p in r]
    k = math.cos(math.radians((min(lats) + max(lats)) / 2))
    x0, x1, y0, y1 = min(lons) * k, max(lons) * k, -max(lats), -min(lats)
    s = min(box[2] / (x1 - x0), box[3] / (y1 - y0))
    ox = box[0] + (box[2] - (x1 - x0) * s) / 2 - x0 * s
    oy = box[1] + (box[3] - (y1 - y0) * s) / 2 - y0 * s
    return lambda p: (ox + p[0] * k * s, oy - p[1] * s)


def shrink(box, f):
    return (box[0] + box[2] * (1 - f) / 2, box[1] + box[3] * (1 - f) / 2, box[2] * f, box[3] * f)


def national_grid(p):
    """lon/lat -> British National Grid metres with y pointing down. No datum shift: about 100 m, invisible here."""
    a, b, f0 = 6377563.396, 6356256.909, 0.9996012717
    lat, lon, lat0, lon0 = math.radians(p[1]), math.radians(p[0]), math.radians(49), math.radians(-2)
    e2, n = 1 - (b * b) / (a * a), (a - b) / (a + b)
    s, c, t = math.sin(lat), math.cos(lat), math.tan(lat)
    nu = a * f0 / math.sqrt(1 - e2 * s * s)
    rho = a * f0 * (1 - e2) / (1 - e2 * s * s) ** 1.5
    eta2 = nu / rho - 1
    d, q = lat - lat0, lat + lat0
    m = b * f0 * ((1 + n + 1.25 * n * n + 1.25 * n ** 3) * d - (3 * n + 3 * n * n + 2.625 * n ** 3) * math.sin(d) * math.cos(q)
                  + (1.875 * n * n + 1.875 * n ** 3) * math.sin(2 * d) * math.cos(2 * q) - (35 / 24) * n ** 3 * math.sin(3 * d) * math.cos(3 * q))
    dl = lon - lon0
    north = (m - 100000 + nu / 2 * s * c * dl ** 2 + nu / 24 * s * c ** 3 * (5 - t * t + 9 * eta2) * dl ** 4)
    east = (400000 + nu * c * dl + nu / 6 * c ** 3 * (nu / rho - t * t) * dl ** 3
            + nu / 120 * c ** 5 * (5 - 18 * t * t + t ** 4 + 14 * eta2 - 58 * t * t * eta2) * dl ** 5)
    return east, -north


class Canvas:
    def __init__(self, bounds, tolerance):
        self.b, self.tol, self.markers, self.pts = bounds, tolerance, [], []

    def path(self, name, rings, xy):
        d, projected = "", [[xy(p) for p in r] for r in rings]
        for ring in projected:
            pts = []
            for p in simplify(ring, self.tol):
                p = (round(p[0]), round(p[1]))
                if not pts or p != pts[-1]:
                    pts.append(p)
            if len(pts) >= 3:
                d += f"M{pts[0][0]} {pts[0][1]}l" + " ".join(f"{x - px} {y - py}" for (px, py), (x, y) in zip(pts, pts[1:])) + "z"
                self.pts += pts
        if not d:  # an atoll too small to survive rounding: a small diamond, so the unit can still be seen and clicked
            ring = max(projected, key=len)
            x, y = round(sum(p[0] for p in ring) / len(ring)), round(sum(p[1] for p in ring) / len(ring))
            r = max(2, round(self.tol * 3))
            d = f"M{x - r} {y}l{r} {-r} {r} {r} {-r} {r}z"
            self.pts += [(x - r, y - r), (x + r, y + r)]
            self.markers.append(name)
        return d

    def add(self, key, name, code, rings, xy):
        if any(u["code"] == code for u in self.b.get(key, [])):
            sys.exit(f"{key} already has a shape with code {code}")
        self.b.setdefault(key, []).append({"name": name, "code": code, "path": self.path(name, rings, xy)})

    def widen(self, margin):
        """Grow the viewBox to take in everything added."""
        x, y, w, h = self.b["viewBox"]
        xs, ys = [p[0] for p in self.pts], [p[1] for p in self.pts]
        x0, y0 = min(x, min(xs) - margin), min(y, min(ys) - margin)
        x1, y1 = max(x + w, max(xs) + margin), max(y + h, max(ys) + margin)
        self.b["viewBox"] = [x0, y0, x1 - x0, y1 - y0]


class Register:
    def __init__(self, folder):
        self.path = ROOT / "data" / folder / "geo_units.csv"
        raw = self.path.read_bytes().decode("utf-8")
        self.nl = "\r\n" if "\r\n" in raw else "\n"
        self.rows = list(csv.DictReader(raw.splitlines()))
        self.fields = raw.splitlines()[0].split(",")
        self.width = len(self.rows[0]["geo_unit_id"]) - 1
        self.last = max(int(r["geo_unit_id"][1:]) for r in self.rows)
        self.new = []

    def add(self, name, level, unit_type, parent, code="", notes=""):
        if code and any(r["code"] == code for r in self.rows + self.new):
            sys.exit(f"geo_units.csv already has code {code}")
        self.last += 1
        uid = f"G{self.last:0{max(4, self.width)}d}"
        row = dict.fromkeys(self.fields, "")
        row.update(geo_unit_id=uid, name=name, level=level, unit_type=unit_type, parent_id=parent, sweep_status="pending", code=code, notes=notes)
        self.new.append(row)
        return uid

    def save(self):
        raw = self.path.read_bytes()
        with open(self.path, "a", encoding="utf-8", newline="") as f:
            if not raw.endswith(b"\n"):
                f.write(self.nl)
            csv.DictWriter(f, self.fields, lineterminator=self.nl).writerows(self.new)


def finish(folder, canvas, register, margin):
    canvas.widen(margin)
    p = ROOT / "data" / folder / "boundaries.json"
    p.write_text(json.dumps(canvas.b, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    register.save()
    print(f"{folder}: {len(register.new)} units added to geo_units.csv; viewBox {canvas.b['viewBox']}; "
          f"{len(canvas.markers)} drawn as markers{': ' + ', '.join(canvas.markers) if canvas.markers else ''}")


def load(folder):
    return json.load(open(ROOT / "data" / folder / "boundaries.json", encoding="utf-8"))


def us(counties_file, names_file):
    counties, states = topo_shapes(counties_file, "counties"), topo_shapes(counties_file, "states")
    names = {f["attributes"]["GEOID"]: f["attributes"]["NAME"] for f in json.load(open(names_file, encoding="utf-8"))["features"]}
    c, reg = Canvas(load("united-states"), 0.8), Register("united-states")
    root = next(r["geo_unit_id"] for r in reg.rows if r["name"] == "United States" and r["level"] == "national")
    # A row under the main map: the Pacific territories on the left below Hawaii, the Caribbean on the right below Florida.
    groups = [((-150, 2490, 330, 330), ["66"]), ((330, 2490, 330, 330), ["69"]), ((820, 2490, 560, 330), ["60"]),
              ((2650, 2490, 900, 330), ["72", "78"])]
    territory = {"60": "American Samoa", "66": "Guam", "69": "Northern Mariana Islands", "72": "Puerto Rico", "78": "U.S. Virgin Islands"}
    kinds = {"60": "district", "66": "territory", "69": "municipality", "72": "municipio", "78": "island"}
    regions = {s: reg.add(territory[s], "region", "territory", root) for s in sorted(territory)}
    for box, fips in groups:
        xy = fitter([r for s in fips for r in states[s][1]], box)
        for s in fips:
            c.add("regions", territory[s], s, states[s][1], xy)
            for code in sorted(k for k in names if k[:2] == s):
                shape = counties.get(code)
                note = "" if shape else "No outline in the us-atlas file, so not on the map."
                reg.add(names[code], "county", "atoll" if code in ("60030", "60040") else kinds[s], regions[s], code, note)
                if shape:
                    c.add("units", shape[0], code, shape[1], xy)
    c.b["source"] += (" Puerto Rico and the island territories: US Census Bureau cartographic boundaries 2017 via us-atlas@3 "
                      "(public domain), each in its own inset below the map, not to a common scale.")
    finish("united-states", c, reg, 20)


def fr(folder):
    folder = Path(folder)
    communes, deps, regs = (geojson_shapes(folder / f"{n}-1000m.geojson.gz") for n in ("communes", "departements", "regions"))
    c, reg = Canvas(load("france"), 1.0), Register("france")
    root = next(r["geo_unit_id"] for r in reg.rows if r["level"] == "national" and r["unit_type"] == "country")
    # Two columns west of the metropolitan map (the legend covers the bottom of the frame, so not below it);
    # French Polynesia is spread over an ocean and gets a double box.
    cell = lambda col, row, span=1: (-2140 + col * 500, -15310 + row * 486, 440 + (span - 1) * 500, 420)
    overseas = {"971": cell(0, 0), "972": cell(1, 0), "973": cell(0, 1), "974": cell(1, 1), "976": cell(0, 2), "975": cell(1, 2),
                "977": cell(0, 3), "978": cell(1, 3), "986": cell(0, 4), "988": cell(1, 4), "987": cell(0, 5, 2)}
    region_of = {"971": "01", "972": "02", "973": "03", "974": "04", "976": "06"}  # INSEE region codes of the overseas departments
    collectivities = {"975": "FR-PM", "977": "FR-BL", "978": "FR-MF", "986": "FR-WF", "987": "FR-PF", "988": "FR-NC"}
    for dep, box in overseas.items():
        mine = sorted(k for k in communes if k.startswith(dep))
        if dep in ("977", "978"):  # tiny islands: at full box size the 1000 m generalisation shows as straight edges
            box = shrink(box, 0.45)
        xy = fitter([r for k in mine for r in communes[k][1]], box)
        c.add("regions", deps[dep][0], dep, deps[dep][1], xy)
        if dep in region_of:
            code = region_of[dep]
            c.add("regions_upper", regs[code][0], code, regs[code][1], xy)
        else:
            parent = reg.add(deps[dep][0], "region", "overseas collectivity", root, collectivities[dep])
            for k in mine:
                reg.add(communes[k][0], "council", "circonscription territoriale" if dep == "986" else "commune", parent, k)
        for k in mine:
            c.add("units", communes[k][0], k, communes[k][1], xy)
    c.b["source"] = ("Commune, département and region outlines: Etalab contours administratifs 2025 (1000 m). Metropolitan France, "
                     "derived from IGN Admin Express, under the Licence Ouverte 2.0. Overseas departments and collectivities (insets "
                     "west of the map, not to a common scale), from IGN Admin Express, OpenStreetMap (© OpenStreetMap contributors) "
                     "and the French Polynesian and New Caledonian authorities' data; data.gouv.fr publishes the dataset under the "
                     "ODbL 1.0 (https://opendatacommons.org/licenses/odbl/1-0/).")
    c.b["licence"] = "Licence-Ouverte-2.0 (metropolitan) and ODbL-1.0 (overseas)"
    c.b["licence_url"] = "https://www.data.gouv.fr/datasets/contours-administratifs"
    finish("france", c, reg, 20)


def gb():
    world = topo_shapes(ROOT / "site" / "vendor" / "countries-50m.json", "countries")
    c, reg = Canvas(load("united-kingdom"), 250), Register("united-kingdom")
    root = next(r["geo_unit_id"] for r in reg.rows if r["level"] == "national" and not r["parent_id"])
    group = reg.add("Crown dependencies and overseas territories", "region", "territories_group", root,
                    notes="Not represented at Westminster; the Crown dependencies set their own taxes.")
    # (ISO 3166-1 numeric in the world file, ISO alpha-2 code used in the register, name, kind)
    territories = [("833", "IM", "Isle of Man", "crown_dependency"), ("831", "GG", "Guernsey", "crown_dependency"),
                   ("832", "JE", "Jersey", "crown_dependency"), ("660", "AI", "Anguilla", "overseas_territory"),
                   ("060", "BM", "Bermuda", "overseas_territory"), ("086", "IO", "British Indian Ocean Territory", "overseas_territory"),
                   ("092", "VG", "British Virgin Islands", "overseas_territory"), ("136", "KY", "Cayman Islands", "overseas_territory"),
                   ("238", "FK", "Falkland Islands", "overseas_territory"), ("292", "GI", "Gibraltar", "overseas_territory"),
                   ("500", "MS", "Montserrat", "overseas_territory"), ("612", "PN", "Pitcairn Islands", "overseas_territory"),
                   ("654", "SH", "Saint Helena, Ascension and Tristan da Cunha", "overseas_territory"),
                   ("239", "GS", "South Georgia and the South Sandwich Islands", "overseas_territory"),
                   ("796", "TC", "Turks and Caicos Islands", "overseas_territory")]
    for num, code, name, kind in territories:
        note = "" if num in world else "No outline in the Natural Earth 1:50m file, so not on the map."
        reg.add(name, "council", kind, group, code, note)
    # Insets in two columns east of Great Britain; the Channel Islands share one box.
    boxes = [["GG", "JE"], ["BM"], ["AI"], ["VG"], ["MS"], ["TC"], ["KY"], ["FK"], ["GS"], ["SH"], ["IO"], ["PN"]]
    num_of = {code: num for num, code, _, _ in territories}
    name_of = {code: name for _, code, name, _ in territories}
    c.add("units", name_of["IM"], "IM", world[num_of["IM"]][1], national_grid)
    for i, codes in enumerate(boxes):
        box = (700000 + (i % 2) * 220000, -1200000 + (i // 2) * 160000, 170000, 125000)  # clear of the legend at the bottom
        if codes[0] in ("AI", "BM", "VG", "MS", "IO", "PN"):  # a few points each at 1:50m: drawn smaller
            box = shrink(box, 0.5)
        xy = fitter([r for k in codes for r in world[num_of[k]][1]], box)
        for k in codes:
            c.add("units", name_of[k], k, world[num_of[k]][1], xy)
    c.b["source"] += (" Isle of Man, Channel Islands and overseas territories: Natural Earth 1:50m via the world-atlas package "
                      "(public domain), all but the Isle of Man in insets east of Great Britain, not to a common scale.")
    c.b["code_scheme"] += "; ISO 3166-1 alpha-2 for the Crown dependencies and overseas territories"
    finish("united-kingdom", c, reg, 5000)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("country", choices=["us", "fr", "gb"])
    ap.add_argument("files", nargs="*")
    a = ap.parse_args()
    {"us": us, "fr": fr, "gb": gb}[a.country](*a.files)
