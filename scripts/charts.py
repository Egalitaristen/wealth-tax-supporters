"""Charts for the argument pages, drawn at build time as inline markup: no scripts, no external images, no data files to fetch.

A page declares a chart in its front matter (`charts:`) and places it with a line of its own in the body, `{{chart: id}}`.
See content/arguments/README.md. Three types:

- `bars`: a labelled bar for each row of `data` (`label|value|tone` rows joined by `;`, a row with a label only is a heading).
- `poll-ranking`: the highest poll in every country that has one, from data/<country>/meta.json, with the country's flag.
- `status-map`: the world map coloured by data/wealth_tax_status.csv, drawn from the site's own country outlines.

The bars are a real list (labels and values are text, so a screen reader, a crawler and a phone all get the data); the map is an
SVG with a title and description and the countries listed as text under it. Colours are the site's tokens (`.chart` in site/style.css),
so both themes work. Text in `title`, `desc` and `caption` may use {polls}, {poll_countries} and {above_half}, filled in at build time.
"""
import html
import re

CHART_TYPES = ("bars", "poll-ranking", "status-map")
CHART_REQUIRED = ("id", "type", "title", "desc", "caption")
CHART_OPTIONAL = ("data", "unit", "max", "limit", "tone")
TONES = ("signal", "ink", "gold", "muted")


def h(s):
    return html.escape(str(s), quote=True)


def parse_rows(data):
    """'France, top 0.1%|46|signal; Norway|17.5||15 to 20' -> [(label, value-or-None, tone, shown)]. `shown` is the text printed at the end of the bar
    when it differs from the value (a range is drawn at its middle). A row with a label only is a group heading."""
    rows = []
    for raw in (data or "").split(";"):
        raw = raw.strip()
        if not raw:
            continue
        parts = [p.strip() for p in raw.split("|")]
        if len(parts) == 1:
            rows.append((parts[0], None, "", ""))
            continue
        try:
            float(parts[1])
        except ValueError:
            raise ValueError(f"chart row {raw!r}: the value must be a number")
        tone = parts[2] if len(parts) > 2 else ""
        if tone and tone not in TONES:
            raise ValueError(f"chart row {raw!r}: tone must be one of {', '.join(TONES)}")
        rows.append((parts[0], parts[1], tone, parts[3] if len(parts) > 3 else ""))
    return rows


def check(c):
    """Problems with a chart's front matter entry, as a list of messages."""
    out = []
    cid = c.get("id", "?")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", c.get("id", "")):
        out.append(f"chart id {cid!r} must be lower-case letters, digits and hyphens")
    if c.get("type") not in CHART_TYPES:
        out.append(f"chart {cid}: type must be one of {', '.join(CHART_TYPES)}")
    for k in sorted(set(c) - set(CHART_REQUIRED) - set(CHART_OPTIONAL)):
        out.append(f"chart {cid}: unknown field {k!r}")
    if c.get("type") == "bars":
        try:
            if not [r for r in parse_rows(c.get("data")) if r[1] is not None]:
                out.append(f"chart {cid}: bars need data")
        except ValueError as e:
            out.append(f"chart {cid}: {e}")
    for k in ("max", "limit"):
        if c.get(k) and not re.fullmatch(r"\d+(\.\d+)?", c[k]):
            out.append(f"chart {cid}: {k} must be a number")
    return out


def _fill(s, ctx):
    stats = ctx.get("stats", {})
    return re.sub(r"\{(polls|poll_countries|above_half)\}", lambda m: str(stats.get(m.group(1), m.group(0))), s)


def _bars(c, ctx):
    rows = parse_rows(c.get("data"))
    unit = c.get("unit", "%")
    vals = [float(r[1]) for r in rows if r[1] is not None]
    top = float(c["max"]) if c.get("max") else max(vals)
    default_tone = c.get("tone", "signal")
    items = []
    for label, v, tone, shown in rows:
        if v is None:
            items.append(f'<li class="cb-g">{h(label)}</li>')
            continue
        w = max(0.8, min(100.0, float(v) / top * 100))
        items.append(f'<li class="cb cb-{h(tone or default_tone)}"><span class="cb-l">{h(label)}</span>'
                     f'<span class="cb-t" aria-hidden="true"><i style="width:{w:.1f}%"></i></span><b class="cb-v">{h(shown or v + unit)}</b></li>')
    return '<ul class="cbars">' + "".join(items) + "</ul>"


def _poll_ranking(c, ctx):
    rows = ctx.get("polls_best") or []
    limit = int(float(c["limit"])) if c.get("limit") else len(rows)

    def row(r):
        flag = f'<img class="flag" src="/flags/{h(r["iso2"].lower())}.svg" alt="" width="16" height="12" loading="lazy">' if r.get("iso2") else ""
        return (f'<li class="cb cb-signal"><span class="cb-l">{flag}<a href="/{h(r["slug"])}">{h(r["name"])}</a></span>'
                f'<span class="cb-t" aria-hidden="true"><i style="width:{r["pct"]}%"></i></span><b class="cb-v">{r["pct"]}%</b></li>')
    first, rest = rows[:limit], rows[limit:]
    out = '<ol class="cbars cb-rank">' + "".join(row(r) for r in first) + "</ol>"
    if rest:
        out += (f'<details class="cb-more"><summary>Show the other {len(rest)} countries</summary><ol class="cbars cb-rank" start="{limit + 1}">'
                + "".join(row(r) for r in rest) + "</ol></details>")
    return out


_NUM = re.compile(r"-?\d+(?:\.\d+)?")


def _simplify(pts, tol):
    """Douglas-Peucker on an open polyline."""
    if len(pts) < 3:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        (x1, y1), (x2, y2) = pts[a], pts[b]
        dx, dy = x2 - x1, y2 - y1
        n = (dx * dx + dy * dy) ** 0.5 or 1e-9
        far, fi = 0.0, -1
        for i in range(a + 1, b):
            d = abs(dy * pts[i][0] - dx * pts[i][1] + x2 * y1 - y2 * x1) / n
            if d > far:
                far, fi = d, i
        if far > tol:
            keep[fi] = True
            stack += [(a, fi), (fi, b)]
    return [p for p, k in zip(pts, keep) if k]


def _coarse(d, tol=0.45, min_size=1.4):
    """A country outline from the site's map, simplified for a picture 700 px wide (the site's own is made for zooming)."""
    out, bigger = [], []
    for ring in d.split("M")[1:]:
        pts = [(float(a), float(b)) for a, b in zip(*[iter(_NUM.findall(ring))] * 2)]
        if len(pts) < 3:
            continue
        size = max(max(p[0] for p in pts) - min(p[0] for p in pts), max(p[1] for p in pts) - min(p[1] for p in pts))
        bigger.append((size, pts))
    top = max((s for s, _ in bigger), default=0)
    for size, pts in bigger:
        if size < min_size and size < top:
            continue
        # a ring starts and ends on the same point, so split it at the point farthest from the start first
        m = max(range(len(pts)), key=lambda i: (pts[i][0] - pts[0][0]) ** 2 + (pts[i][1] - pts[0][1]) ** 2)
        s = _simplify(pts[:m + 1], tol) + _simplify(pts[m:], tol)[1:]
        if len(s) >= 3:
            out.append("M" + "L".join(f"{x:.0f} {y:.0f}" for x, y in s) + "Z")
    return "".join(out)


def _status_map(c, ctx):
    paths, status = ctx.get("paths") or {}, ctx.get("status_map") or {}
    land, has, had = [], [], []
    xs, ys = [], []
    for cid, p in paths.items():
        d = _coarse(p["path"])
        if not d:
            continue
        nums = [float(v) for v in _NUM.findall(d)]
        xs += nums[0::2]
        ys += nums[1::2]
        (has if status.get(cid) == "has" else had if status.get(cid) == "had" else land).append(d)
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    box = f"{x0:.0f} {y0:.0f} {x1 - x0:.0f} {y1 - y0:.0f}"
    title_id, desc_id = f'{c["id"]}-t', f'{c["id"]}-d'
    svg = (f'<svg class="cmap" viewBox="{box}" role="img" aria-labelledby="{title_id} {desc_id}" preserveAspectRatio="xMidYMid meet">'
           f'<title id="{title_id}">{h(_fill(c["title"], ctx))}</title><desc id="{desc_id}">{h(_fill(c["desc"], ctx))}</desc>'
           f'<path class="m-land" d="{"".join(land)}"/><path class="m-had" d="{"".join(had)}"/><path class="m-has" d="{"".join(has)}"/></svg>')
    key = (f'<p class="cmap-key"><span><i class="m-has"></i>Has a wealth tax ({len([1 for v in status.values() if v == "has"])})</span>'
           f'<span><i class="m-had"></i>Used to have one ({len([1 for v in status.values() if v == "had"])})</span></p>')

    def names(kind):
        return ", ".join(sorted(h(paths[i]["name"]) for i, v in status.items() if v == kind and i in paths))
    lists = (f'<details class="cb-more"><summary>The countries as a list</summary><p><b>Has a wealth tax:</b> {names("has")}.</p>'
             f'<p><b>Used to have one:</b> {names("had")}.</p></details>')
    return svg + key + lists


def render(c, ctx):
    """The <figure> for one chart. `c` carries caption_html (the caption with its [n] references already linked)."""
    kind = c["type"]
    body = {"bars": _bars, "poll-ranking": _poll_ranking, "status-map": _status_map}[kind](c, ctx)
    title = _fill(c["title"], ctx)
    cap = _fill(c.get("caption_html", h(c["caption"])), ctx)
    # The map carries its title and description inside the SVG; the lists are named by the visible title and described for screen readers.
    desc = "" if kind == "status-map" else f'<p class="sr" id="chart-{h(c["id"])}-d">{h(_fill(c["desc"], ctx))}</p>'
    described = "" if kind == "status-map" else f' aria-describedby="chart-{h(c["id"])}-d"'
    return (f'<figure class="chart chart-{h(kind)}" id="chart-{h(c["id"])}" aria-labelledby="chart-{h(c["id"])}-t"{described}>'
            f'<p class="chart-title" id="chart-{h(c["id"])}-t">{h(title)}</p>{desc}{body}<figcaption>{cap}</figcaption></figure>')


def poll_stats(countries):
    """The highest poll in each country that has one, highest first, from the country summaries (their `polls` are the published ones)."""
    best, total = [], 0
    for c in countries:
        ps = [p for p in c.get("polls", []) if p.get("support") is not None]
        total += len(ps)
        if ps:
            top = max(ps, key=lambda p: float(p["support"]))
            best.append(dict(name=c["name"], slug=c["slug"], iso2=c.get("iso2", ""), pct=int(float(top["support"]) + 0.5)))
    best.sort(key=lambda r: (-r["pct"], r["name"]))
    return best, dict(polls=total, poll_countries=len(best), above_half=sum(1 for r in best if r["pct"] > 50))


# ISO 3166 numeric codes (the map's ids) for the countries in data/wealth_tax_status.csv, so the status map does not depend on pycountry being installed.
ISO_NUMERIC = {"NO": "578", "CH": "756", "ES": "724", "CO": "170", "AR": "032", "BO": "068", "UY": "858", "FR": "250", "SE": "752", "DK": "208", "DE": "276",
               "NL": "528", "AT": "040", "FI": "246", "LU": "442", "IS": "352", "IN": "356", "SR": "740", "GY": "328", "TN": "788", "VE": "862", "PK": "586", "BD": "050"}


def status_by_numeric(rows, numeric_for):
    """{map id: 'has'|'had'} from the rows of data/wealth_tax_status.csv. Fails loudly when a country cannot be placed on the map."""
    out, missing = {}, []
    for r in rows:
        n = numeric_for(r["iso2"]) or ISO_NUMERIC.get(r["iso2"].upper(), "")
        if n:
            out[n] = r["status"]
        else:
            missing.append(r["iso2"])
    if missing or not out:
        raise SystemExit("status map: no map id for " + (", ".join(missing) or "any country") + " (pip install pycountry, or add the code to ISO_NUMERIC in scripts/charts.py)")
    return out
