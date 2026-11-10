"""Share images (1200x630 PNG) for link previews on Discord, social media and chat apps.

Used by build_site.py when Pillow is installed (pip install pillow). Fonts are in scripts/fonts (SIL OFL).
Images are cached in .cache/cards by a hash of their content, so a rebuild only draws what changed.
"""
import hashlib, json, re, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FONTS = HERE / "fonts"
FLAGS = HERE / "flags_png"  # made from site/vendor/flags by make_flag_pngs.py (Pillow cannot read SVG)
CACHE = HERE.parent / ".cache" / "cards"
VERSION = "12"  # bump to redraw every card after a design change

W, H, S = 1200, 630, 2  # drawn at 2x, then scaled down for smooth edges
PAPER, PAPER2, INK, INK2, INK3, RULE = (243, 239, 230), (233, 227, 214), (23, 21, 15), (74, 70, 61), (124, 118, 106), (214, 207, 191)
SIGNAL, LAND, NIGHT = (217, 67, 30), (207, 199, 181), (18, 17, 14)
FOOT = 74

# The logo mark on its 64-unit grid (see site/index.html).
MARK_BODY = "M4 58 L4 57 C30 57 42 56.5 47 53 C52 49.5 54 42 54 30 C54.27 27.3 54.61 24.6 55.03 21.94 L60 21.94 L60 58 Z"
MARK_TIP = "M55.03 17.94 C56.15 10.75 57.81 3.84 60 -2 L60 17.94 Z"
MARK_DEP = "M4 54.5 L43.92 54.5 C37.66 56.65 25.71 57 4 57 Z"


def _font(name, size, weight=None):
    f = ImageFont.truetype(str(FONTS / name), int(size * S))
    if weight:
        try:
            f.set_variation_by_axes([weight])
        except Exception:  # not a variable font, or no axis support: keep the default weight
            pass
    return f


SERIF = lambda s: _font("InstrumentSerif-Regular.ttf", s)
ITALIC = lambda s: _font("InstrumentSerif-Italic.ttf", s)
SANS = lambda s, w=400: _font("Geist.ttf", s, w)


def _bez(p0, p1, p2, p3, n=24):
    return [((1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t * t * p2[0] + t ** 3 * p3[0],
             (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t * t * p2[1] + t ** 3 * p3[1])
            for t in (i / n for i in range(1, n + 1))]


def _rings(d):
    """M/L/l/C/Z path data (absolute, or relative lines) to a list of point rings."""
    toks = re.findall(r"[MLlCZz]|-?\d+(?:\.\d+)?", d)
    rings, cur, i, pt, cmd = [], [], 0, None, None
    num = lambda k: float(toks[k])
    while i < len(toks):
        if toks[i] in "MLlCZz":
            cmd = toks[i]; i += 1
            if cmd in "Zz":
                if len(cur) > 2: rings.append(cur)
                cur = []
            continue
        if cmd == "M":
            if len(cur) > 2: rings.append(cur)
            pt = (num(i), num(i + 1)); i += 2; cur = [pt]; cmd = "L"
        elif cmd == "L":
            pt = (num(i), num(i + 1)); i += 2; cur.append(pt)
        elif cmd == "l":
            pt = (pt[0] + num(i), pt[1] + num(i + 1)); i += 2; cur.append(pt)
        elif cmd == "C":
            a = [(num(i + k), num(i + k + 1)) for k in (0, 2, 4)]; i += 6
            cur += _bez(pt, *a); pt = a[2]
        else:
            i += 1
    if len(cur) > 2: rings.append(cur)
    return rings


def _mark(dr, x, y, size, ink, signal):
    k = size / 64 * S
    tr = lambda ring: [((x * S) + px * k, (y * S) + (py + 4) * k) for px, py in ring]
    for d, col in ((MARK_BODY, ink), (MARK_TIP, signal), (MARK_DEP, signal)):
        for r in _rings(d):
            dr.polygon(tr(r), fill=col)


def _wrap(dr, text, font, width, lines, tail=""):
    """Wrap text into at most `lines` lines; if it is cut, the last line ends in an ellipsis. `tail` (a closing quote, say) always ends the last line."""
    words, out, cur = text.split(), [], ""
    if words:
        words[-1] += tail
    for w in words:
        t = (cur + " " + w).strip()
        if dr.textlength(t, font=font) <= width * S:
            cur = t
        else:
            if cur: out.append(cur)
            cur = w
            if len(out) == lines: break
    if cur and len(out) < lines: out.append(cur)
    if len(out) == lines and " ".join(out) != " ".join(words):
        last = out[-1]
        while last and dr.textlength(last.rstrip(",;:.") + "…" + tail, font=font) > width * S:
            last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
        out[-1] = last.rstrip(",;:.") + "…" + tail
    return out


def _lines(dr, text, font, width):
    """All the lines text makes at this width (no cut)."""
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if dr.textlength(t, font=font) <= width * S or not cur:
            cur = t
        else:
            out.append(cur)
            cur = w
    return out + ([cur] if cur else [])


def _title(dr, text, width, max_lines=2, start=112, smallest=60):
    """A serif title in as many as max_lines lines, as large as fits. Returns (lines, size)."""
    size = start
    while True:
        f = SERIF(size)
        ls = _lines(dr, text, f, width)
        if (len(ls) <= max_lines and all(dr.textlength(l, font=f) <= width * S for l in ls)) or size <= smallest:
            if len(ls) > max_lines:
                ls = ls[:max_lines]
                while ls[-1] and dr.textlength(ls[-1] + "…", font=f) > width * S:
                    ls[-1] = ls[-1][:-1]
                ls[-1] = ls[-1].rstrip() + "…"
            return ls, size
        size -= 4


def _put_title(dr, lines, size, x, y, fill=INK, pitch=0.96):
    """Draw title lines; returns the y below them."""
    f = SERIF(size)
    for ln in lines:
        dr.text((x * S, y * S), ln, font=f, fill=fill)
        y += int(size * pitch)
    return y


def _fit(dr, text, maker, width, start, smallest):
    size = start
    while size > smallest and dr.textlength(text, font=maker(size)) > width * S:
        size -= 4
    return maker(size), size


def _canvas(bg=PAPER):
    img = Image.new("RGB", (W * S, H * S), bg)
    return img, ImageDraw.Draw(img)


def _footer(dr, dark=False):
    """The branded strip along the bottom of every card."""
    top = H - FOOT
    dr.rectangle((0, top * S, W * S, H * S), fill=INK if not dark else (35, 33, 28))
    _mark(dr, 44, top + 13, 46, PAPER, SIGNAL)
    dr.text((104 * S, (top + 18) * S), "Wealth Tax", font=SERIF(34), fill=PAPER)
    x = 104 * S + dr.textlength("Wealth Tax ", font=SERIF(34))
    dr.text((x, (top + 18) * S), "Supporters", font=ITALIC(34), fill=SIGNAL)
    url = "wealthtaxsupporters.com"
    f = SANS(22, 500)
    dr.text(((W - 44) * S - dr.textlength(url, font=f), (top + 26) * S), url, font=f, fill=(200, 193, 180))


_FLAG_CACHE = {}


def flag_file(slug):
    """The flag PNG for a register slug, by the same rule as the site (australia is au; au and global have none)."""
    code = "au" if slug == "australia" else "" if slug in ("au", "global") or not re.fullmatch(r"[a-z]{2}", slug or "") else slug
    p = FLAGS / f"{code}.png"
    return p if code and p.exists() else None


def _flag(img, slug, x, y, w, h, center=False):
    """Paste a country's flag, contained in the box (x, y, w, h) and centred vertically, with a hairline border. Returns the width drawn, 0 if none."""
    p = flag_file(slug)
    if not p:
        return 0
    f = _FLAG_CACHE.get(p) or _FLAG_CACHE.setdefault(p, Image.open(p).convert("RGBA"))
    k = min(w * S / f.width, h * S / f.height)
    size = (max(1, round(f.width * k)), max(1, round(f.height * k)))
    f = f.resize(size, Image.LANCZOS)
    px = round(x * S + ((w * S - size[0]) / 2 if center else 0))
    py = round(y * S + (h * S - size[1]) / 2)
    img.paste(f, (px, py), f)
    ImageDraw.Draw(img).rectangle((px, py, px + size[0] - 1, py + size[1] - 1), outline=RULE, width=S)
    return size[0] / S


def _kicker(img, dr, text, slug=None):
    """The small caps line at the top left, led by the country's flag when there is one."""
    x = 60
    if slug:
        w = _flag(img, slug, 60, 50, 44, 30)
        x += w + 14 if w else 0
    dr.text((x * S, 54 * S), text.upper(), font=SANS(20, 500), fill=INK3)


def _panel(dr, x=740):
    dr.rectangle((x * S, 40 * S, 1160 * S, 516 * S), fill=PAPER2)


def _area_map(dr, box, units, highlight=None):
    """Draw a country's area map into box=(x, y, w, h): units are (path, t) with t in 0..1 for shading."""
    bx, by, bw, bh = box
    rings = [(_rings(p), t) for p, t in units]
    xs = [x for rs, _ in rings for r in rs for x, _ in r]
    ys = [y for rs, _ in rings for r in rs for _, y in r]
    if not xs:
        return
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    k = min(bw / (x1 - x0), bh / (y1 - y0))
    ox, oy = bx + (bw - (x1 - x0) * k) / 2, by + (bh - (y1 - y0) * k) / 2
    tr = lambda r: [((ox + (x - x0) * k) * S, (oy + (y - y0) * k) * S) for x, y in r]
    for i, (rs, t) in enumerate(rings):
        if highlight is not None:
            col = SIGNAL if i in highlight else LAND
        elif t > 0:
            col = tuple(round(LAND[c] + (SIGNAL[c] - LAND[c]) * t) for c in range(3))
        else:
            col = LAND
        for r in rs:
            if len(r) > 2:
                dr.polygon(tr(r), fill=col, outline=PAPER if (x1 - x0) * k < 2000 else None)


def _save(img, out):
    img = img.resize((W, H), Image.LANCZOS).quantize(colors=64, method=Image.Quantize.MEDIANCUT)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)


def cached(out, key, draw):
    """Copy a cached image if its inputs are unchanged, otherwise draw and cache it."""
    h = hashlib.md5((VERSION + json.dumps(key, sort_keys=True, ensure_ascii=False)).encode()).hexdigest()
    c = CACHE / f"{h}.png"
    if not c.exists():
        draw(c)
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(c, out)
    return c.exists()


# ---------- cards ----------
def home_card(out, totals, types):
    def draw(path):
        img, dr = _canvas()
        dr.text((60 * S, 54 * S), "AN OPEN, SOURCED REGISTER", font=SANS(20, 500), fill=INK3)
        f = SERIF(118)
        dr.text((56 * S, 96 * S), "Who backs a", font=f, fill=INK)
        dr.text((56 * S, 206 * S), "wealth tax", font=f, fill=INK)
        dr.text((56 * S, 316 * S), "near you?", font=ITALIC(118), fill=SIGNAL)
        # the numbers and who they are, right column
        x = 790
        dr.line((x * S, 60 * S, x * S, 490 * S), fill=RULE, width=2 * S)
        dr.text(((x + 36) * S, 56 * S), f"{totals['supporters']:,}", font=SERIF(84), fill=INK)
        for i, ln in enumerate(_wrap(dr, f"public figures and organisations in {totals['countries']} countries", SANS(21), 330, 2)):
            dr.text(((x + 40) * S, (150 + i * 28) * S), ln, font=SANS(21), fill=INK2)
        dr.text(((x + 40) * S, 222 * S), "WHO THEY ARE", font=SANS(16, 500), fill=INK3)
        top = types[:6]
        mx = max([n for _, n in top] or [1])
        for i, (lab, n) in enumerate(top):
            by = 252 + i * 38
            dr.text(((x + 40) * S, by * S), lab, font=SANS(19), fill=INK)
            cnt = f"{n:,}"
            dr.text((1150 * S - dr.textlength(cnt, font=SANS(19, 500)), by * S), cnt, font=SANS(19, 500), fill=INK)
            dr.rectangle(((x + 40) * S, (by + 27) * S, (x + 40 + max(6, int(320 * n / mx))) * S, (by + 31) * S), fill=SIGNAL)
        _footer(dr)
        _save(img, path)
    return cached(out, ["home", totals, types], draw)


def _poll(dr, poll, x, y, width):
    """The poll figure, who asked and the question as asked, in a block about 130 high."""
    dr.rectangle((x * S, y * S, (x + 6) * S, (y + 128) * S), fill=SIGNAL)
    fig = poll.get("support_text") or f"{poll['support']}%"
    ff, _ = _fit(dr, fig, SERIF, min(330, width - 250), 76, 40)
    dr.text(((x + 26) * S, (y - 6) * S), fig, font=ff, fill=SIGNAL)
    fx = x + 26 + dr.textlength(fig, font=ff) / S + 20
    src = ", ".join(v for v in [poll.get("pollster"), str(poll.get("published", ""))[:4]] if v)
    dr.text((fx * S, (y + 18) * S), "SUPPORT", font=SANS(15, 500), fill=INK3)
    dr.text((fx * S, (y + 38) * S), _wrap(dr, src, SANS(18), x + width - fx, 1)[0], font=SANS(18), fill=INK2)
    q = re.sub(r"\s*\(.*?\)", "", poll["question"]).strip().rstrip("?.:;")
    for i, ln in enumerate(_wrap(dr, "Asked: “" + q, SANS(21), width - 26, 2, tail="”")):
        dr.text(((x + 26) * S, (y + 78 + i * 27) * S), ln, font=SANS(21), fill=INK)


def _header(img, dr, kicker, name, slug, width=660):
    """Kicker with flag and the name in as large a serif as fits in two lines. Returns the y below the name."""
    _kicker(img, dr, kicker, slug)
    lines, size = _title(dr, name, width, 2, 104, 60)
    return _put_title(dr, lines, size, 56, 84 + (0 if len(lines) == 1 else -4)) + 24


def country_card(out, c, units, kicker, sub):
    """c: country summary from build_site; units: [(path, t)] map units; kicker/sub: page specific lines."""
    poll = (c.get("polls") or [None])[0]

    def draw(path):
        img, dr = _canvas()
        y = _header(img, dr, kicker, c["name"], c.get("slug"))
        dr.text((60 * S, y * S), f"{c['supporters']:,}", font=SERIF(64), fill=SIGNAL)
        nx = 60 * S + dr.textlength(f"{c['supporters']:,}", font=SERIF(64)) + 16 * S
        for i, ln in enumerate(_wrap(dr, sub, SANS(24), 650 - (nx / S - 60), 2)):
            dr.text((nx, (y + 8 + i * 30) * S), ln, font=SANS(24), fill=INK2)
        if poll:
            _poll(dr, poll, 60, 396, 650)
        if units:
            _panel(dr)
            _area_map(dr, (760, 60, 380, 436), units)
        _footer(dr)
        _save(img, path)
    return cached(out, ["country", c["name"], c.get("slug"), c["supporters"], c["evidence"], kicker, sub, poll, len(units), [round(t, 2) for _, t in units]], draw)


def person_card(out, p, country, quote, units, highlight, typelabel, gradeline, slug=None, badge=None):
    """badge: (grade letter, grade name, statement count, years) for the panel shown when there is no map."""
    def draw(path):
        img, dr = _canvas()
        right = 760
        _kicker(img, dr, f"{typelabel} · {country}", slug)
        lines, size = _title(dr, p["name"], right - 80, 2, 96, 44)
        y = _put_title(dr, lines, size, 56, 84) + 28
        for ln in _wrap(dr, p["role"], SANS(23), right - 80, 2):
            dr.text((60 * S, y * S), ln, font=SANS(23), fill=INK2); y += 30
        if quote:
            y += 26
            room = (H - FOOT - 70) - y
            qs = 46 if len(quote) < 140 else 40
            qf, lh = ITALIC(qs), int(qs * 1.18)
            lines = _wrap(dr, "“" + quote, qf, right - 110, max(1, room // lh), tail="”")
            dr.rectangle((60 * S, (y + 6) * S, 65 * S, (y + len(lines) * lh) * S), fill=SIGNAL)
            for ln in lines:
                dr.text((84 * S, y * S), ln, font=qf, fill=INK); y += lh
        dr.text((60 * S, (H - FOOT - 50) * S), gradeline, font=SANS(20, 500), fill=SIGNAL)
        if units:
            _panel(dr, 800)
            _area_map(dr, (816, 56, 328, 444), units, highlight=highlight)
        elif badge:
            _panel(dr, 800)
            letter, label, n, span = badge
            cx = 980
            dr.text((cx * S, 70 * S), letter, font=SERIF(250), fill=SIGNAL, anchor="mt")
            dr.text((cx * S, 330 * S), label, font=SANS(24, 500), fill=INK, anchor="mt")
            dr.text((cx * S, 366 * S), f"{n} statement{'s' if n != 1 else ''}" + (f" · {span}" if span else ""), font=SANS(19), fill=INK2, anchor="mt")
            fw = _flag(img, slug, 920, 420, 120, 72, center=True) if slug else 0
            if not fw:
                _mark(dr, cx - 28, 424, 56, INK, SIGNAL)
        _footer(dr)
        _save(img, path)
    return cached(out, ["person", p, country, quote, typelabel, gradeline, len(units), sorted(highlight or []), slug, badge], draw)


def _rows(dr, items, x, y, w, pitch, numw=160):
    """Rows in a panel: a big serif figure, then a label. items: (figure, label)."""
    for i, (num, lab) in enumerate(items):
        ry = y + i * pitch
        if i:
            dr.line((x * S, (ry - 16) * S, (x + w) * S, (ry - 16) * S), fill=RULE, width=2)
        nf, _ = _fit(dr, num, SERIF, numw - 20, 64, 36)
        dr.text((x * S, ry * S), num, font=nf, fill=SIGNAL)
        for j, ln in enumerate(_wrap(dr, lab, SANS(23, 500), w - numw, 2)):
            dr.text(((x + numw) * S, (ry + 14 + j * 28) * S), ln, font=SANS(23, 500), fill=INK)


def _blurb(dr, kicker, title, line, width=620, line_count=4):
    """The left side of a text page: kicker, title and a line under it."""
    dr.text((60 * S, 54 * S), kicker.upper(), font=SANS(20, 500), fill=INK3)
    lines, size = _title(dr, title, width, 3, 112, 68)
    y = _put_title(dr, lines, size, 56, 92) + 36
    for ln in _wrap(dr, line, SANS(27), width, line_count):
        dr.text((60 * S, y * S), ln, font=SANS(27), fill=INK2); y += 37
    return y


def page_card(out, kicker, title, line, points=()):
    """A text page: title and line on the left, up to four (figure, label) points in the panel at the right (the logo mark without them)."""
    def draw(path):
        img, dr = _canvas()
        _blurb(dr, kicker, title, line)
        _panel(dr)
        if points:
            n = min(4, len(points))
            pitch = 440 // n
            _rows(dr, points[:n], 776, 64 + (pitch - 72) // 2, 350, pitch)
        else:
            _mark(dr, 800, 130, 340, INK, SIGNAL)
        _footer(dr)
        _save(img, path)
    return cached(out, ["page", kicker, title, line, [list(q) for q in points]], draw)


def argument_card(out, objection, answer, number=0):
    """An argument page: the objection in quotes as the headline, the one-line answer under it, and a small 'answered with sources' foot."""
    def draw(path):
        img, dr = _canvas()
        _kicker(img, dr, "Argument · the objection")
        lines, size = _title(dr, "“" + objection.strip().strip("“”\"") + "”", 1060, 3, 84, 50)
        y = _put_title(dr, lines, size, 56, 92) + 26
        dr.line((60 * S, y * S, 160 * S, y * S), fill=SIGNAL, width=4 * S)
        y += 24
        dr.text((60 * S, y * S), "THE ANSWER", font=SANS(17, 500), fill=SIGNAL)
        y += 32
        for ln in _wrap(dr, answer, SANS(27), 1060, 4):
            dr.text((60 * S, y * S), ln, font=SANS(27), fill=INK2); y += 37
        _footer(dr)
        _save(img, path)
    return cached(out, ["argument", objection, answer], draw)


GRADES = (("A", "Explicit support", "A formal act or specific proposal"),
          ("B", "Named support", "Said to back a wealth tax, by name"),
          ("C", "Implied support", "Read from context"))


def _grades(dr, counts, x=772, y=96, pitch=134):
    """The A/B/C evidence grades with a count each, in the panel."""
    mx = max(list(counts) + [1])
    for i, ((g, lab, meaning), n) in enumerate(zip(GRADES, counts)):
        gy = y + i * pitch
        dr.rectangle((x * S, gy * S, (x + 76) * S, (gy + 76) * S), fill=(SIGNAL, INK2, INK3)[i])
        dr.text(((x + 38) * S, (gy + 40) * S), g, font=SERIF(60), fill=PAPER, anchor="mm")
        dr.text(((x + 100) * S, (gy - 4) * S), lab, font=SANS(24, 500), fill=INK)
        dr.text(((x + 100) * S, (gy + 28) * S), meaning, font=SANS(16), fill=INK2)
        cnt = f"{n:,}"
        cf = SANS(18, 500)
        dr.text(((x + 100) * S, (gy + 52) * S), cnt, font=cf, fill=INK)
        bx = x + 100 + dr.textlength(cnt, font=cf) / S + 12
        dr.rectangle((bx * S, (gy + 62) * S, (bx + max(4, int(170 * n / mx))) * S, (gy + 67) * S), fill=SIGNAL)


def method_card(out, grades, line):
    """The site's Method page: the three evidence grades with how many supporters rest on each. grades: counts for A, B, C."""
    def draw(path):
        img, dr = _canvas()
        _blurb(dr, "Method", "How the register is built", line)
        _panel(dr)
        dr.text((772 * S, 62 * S), "SUPPORTERS, BY THEIR BEST EVIDENCE", font=SANS(15, 500), fill=INK3)
        _grades(dr, list(grades))
        _footer(dr)
        _save(img, path)
    return cached(out, ["method", list(grades), line], draw)


# ---------- seats and directory cards ----------
def _hemicycle(n):
    """Dot positions for n seats in a half ring, the same layout as the site's seat chart (hemicycle() in site/app.js)."""
    import math
    r0, rows = 0.32, 1
    cap = lambda R: sum(math.floor(math.pi * (r0 + (i + .5) * (1 - r0) / R) / ((1 - r0) / R)) for i in range(R))
    while cap(rows) < n:
        rows += 1
    dr = (1 - r0) / rows
    rad = lambda i: r0 + (i + .5) * dr
    tot = sum(rad(i) for i in range(rows))
    raw = [n * rad(i) / tot for i in range(rows)]
    per = [math.floor(v) for v in raw]
    left = n - sum(per)
    for _, i in sorted(((v - math.floor(v), i) for i, v in enumerate(raw)), reverse=True):
        if left > 0:
            per[i] += 1
            left -= 1
    pts = []
    for i, k in enumerate(per):
        for j in range(k):
            a = math.pi / 2 if k == 1 else math.pi * (1 - j / (k - 1))
            pts.append((a, rad(i), math.cos(a) * rad(i), -math.sin(a) * rad(i)))
    pts.sort(key=lambda p: (-p[0], p[1]))
    return pts, dr * 0.43


def _seat_rgb(hexc):
    h = (hexc or "").lstrip("#")
    if not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        return (138, 134, 128)
    r, g, b = int(h[:2], 16), int(h[2:4], 16), int(h[4:], 16)
    return (138, 134, 128) if (r * .299 + g * .587 + b * .114) / 255 > 0.88 else (r, g, b)


def _hemi(dr, cx, cy, radius, body):
    """One chamber as a hemicycle: a seat per dot in party blocks, solid where a supporter sits, faded elsewhere."""
    pts, dot = _hemicycle(body["seats"])
    at = 0
    for party, n, colour, lit in body["parties"]:
        own, rgb = pts[at:at + n], _seat_rgb(colour)
        at += n
        faded = tuple(int(c * .32 + p * .68) for c, p in zip(rgb, PAPER2))
        on = {int((k + .5) * n / lit) for k in range(lit)} if lit else set()
        for i, (_, _, x, y) in enumerate(own):
            px, py, r = (cx + x * radius) * S, (cy + y * radius) * S, dot * radius * S
            dr.ellipse((px - r, py - r, px + r, py + r), fill=rgb if i in on else faded)


def _chamber_label(dr, cx, y, body, width, start, smallest):
    lab = f"{body['name']} · {sum(q[3] for q in body['parties'])} of {body['seats']:,}"
    lf, _ = _fit(dr, lab, lambda s: SANS(s, 500), width, start, smallest)
    dr.text((cx * S - dr.textlength(lab, font=lf) / 2, y * S), lab, font=lf, fill=INK2)


def seats_card(out, c, bodies, sub, slug=None):
    """bodies: [{name, seats, parties: [[party, seats, colour, number lit]]}]; the first two are drawn."""
    shown = bodies[:2]
    lit_all = sum(q[3] for b in bodies for q in b["parties"])
    seats_all = sum(b["seats"] for b in bodies)

    def draw(path):
        img, dr = _canvas()
        _kicker(img, dr, "Seats · who sits in the legislature", slug)
        nf, size = _fit(dr, c["name"], SERIF, 640, 112, 64)
        dr.text((56 * S, 86 * S), c["name"], font=nf, fill=INK)
        y = 86 + size + 18
        dr.text((60 * S, y * S), f"{lit_all:,}", font=SERIF(84), fill=SIGNAL)
        dr.text((60 * S, (y + 92) * S), f"of {seats_all:,} seats", font=SANS(30, 500), fill=INK)
        for i, ln in enumerate(_wrap(dr, sub, SANS(24), 620, 3)):
            dr.text((60 * S, (y + 142 + i * 31) * S), ln, font=SANS(24), fill=INK2)
        _panel(dr)
        if len(shown) == 1:
            _hemi(dr, 950, 400, 190, shown[0])
            _chamber_label(dr, 950, 438, shown[0], 380, 22, 15)
        else:
            for k, b in enumerate(shown):
                oy = 60 + k * 226
                _chamber_label(dr, 950, oy, b, 390, 20, 14)
                _hemi(dr, 950, oy + 196, 160, b)
        _footer(dr)
        _save(img, path)
    return cached(out, ["seats", c["name"], slug, sub, [[b["name"], b["seats"], [[q[0], q[1], q[2], q[3]] for q in b["parties"]]] for b in shown], lit_all, seats_all], draw)


def directory_card(out, name, total, line, types, grades, slug=None):
    """name: the page's subject; types: [(label, count)] biggest first; grades: [(label, count)]."""
    top = types[:6]
    mx = max([n for _, n in top] or [1])

    def draw(path):
        img, dr = _canvas()
        _kicker(img, dr, "Directory · every name with its source", slug)
        nf, size = _fit(dr, name, SERIF, 640, 112, 64)
        dr.text((56 * S, 86 * S), name, font=nf, fill=INK)
        y = 86 + size + 18
        dr.text((60 * S, y * S), f"{total:,}", font=SERIF(84), fill=SIGNAL)
        for i, ln in enumerate(_wrap(dr, line, SANS(26), 620, 2)):
            dr.text((60 * S, (y + 96 + i * 33) * S), ln, font=SANS(26), fill=INK2)
        gx = 60
        for lab, n in grades:
            t = f"{n:,} {lab.lower()}"
            dr.text((gx * S, 448 * S), t, font=SANS(20, 500), fill=INK3)
            gx += int(dr.textlength(t, font=SANS(20, 500)) / S) + 28
        dr.line((740 * S, 70 * S, 740 * S, 470 * S), fill=RULE, width=2 * S)
        dr.text((780 * S, 62 * S), "WHO THEY ARE", font=SANS(18, 500), fill=INK3)
        for i, (lab, n) in enumerate(top):
            by = 108 + i * 63
            dr.text((780 * S, by * S), lab, font=SANS(22), fill=INK)
            cnt = f"{n:,}"
            dr.text((1140 * S - dr.textlength(cnt, font=SANS(22, 500)), by * S), cnt, font=SANS(22, 500), fill=INK)
            dr.rectangle((780 * S, (by + 33) * S, (780 + max(6, int(360 * n / mx))) * S, (by + 39) * S), fill=SIGNAL)
        _footer(dr)
        _save(img, path)
    return cached(out, ["directory", name, slug, total, line, top, grades], draw)


# ---------- cards with their own picture ----------
def country_method_card(out, c, grades, extra):
    """A country's method page: the poll it rests on at the left, the evidence grades at the right. grades: counts for A, B, C; extra: a line of other counts."""
    poll = (c.get("polls") or [None])[0]

    def draw(path):
        img, dr = _canvas()
        y = _header(img, dr, "Method · polls, bills, sources and downloads", c["name"], c.get("slug"))
        dr.text((60 * S, y * S), f"{c['supporters']:,}", font=SERIF(64), fill=SIGNAL)
        nx = 60 * S + dr.textlength(f"{c['supporters']:,}", font=SERIF(64)) + 16 * S
        for i, ln in enumerate(_wrap(dr, "public figures and organisations, each with a source", SANS(24), 650 - (nx / S - 60), 2)):
            dr.text((nx, (y + 8 + i * 30) * S), ln, font=SANS(24), fill=INK2)
        if poll:
            _poll(dr, poll, 60, 396, 650)
        _panel(dr)
        dr.text((772 * S, 62 * S), "SUPPORTERS, BY THEIR BEST EVIDENCE", font=SANS(15, 500), fill=INK3)
        _grades(dr, list(grades), y=96, pitch=124)
        if extra:
            dr.line((772 * S, 468 * S, 1128 * S, 468 * S), fill=RULE, width=2)
            dr.text((772 * S, 480 * S), _wrap(dr, extra, SANS(18, 500), 356, 1)[0], font=SANS(18, 500), fill=INK2)
        _footer(dr)
        _save(img, path)
    return cached(out, ["cmethod", c["name"], c.get("slug"), c["supporters"], poll, list(grades), extra], draw)


def time_card(out, c, years, sub):
    """A country's 'over time' page: sourced statements per year as bars. years: {year: count}."""
    ys = sorted(int(y) for y in years if str(y).isdigit())
    counts = {int(y): n for y, n in years.items() if str(y).isdigit()}

    def draw(path):
        img, dr = _canvas()
        _kicker(img, dr, "Over time · statements per year", c.get("slug"))
        lines, size = _title(dr, c["name"], 640, 1, 96, 56)
        y = _put_title(dr, lines, size, 56, 84)
        for i, ln in enumerate(_wrap(dr, sub, SANS(24), 640, 1)):
            dr.text((60 * S, (y + 24) * S), ln, font=SANS(24), fill=INK2)
        num = f"{c['evidence']:,}"
        dr.text((1140 * S, 70 * S), num, font=SERIF(104), fill=SIGNAL, anchor="rt")
        dr.text((1140 * S, 178 * S), "sourced statements", font=SANS(22, 500), fill=INK2, anchor="rt")
        if ys:
            y0, y1 = ys[0], ys[-1]
            span = list(range(y0, y1 + 1))
            top, base, x0, x1 = 276, 494, 60, 1140
            slot = min((x1 - x0) / len(span), 110)
            bw = slot * 0.68
            gx = x0 + ((x1 - x0) - slot * len(span)) / 2
            mx = max(counts.values())
            peak = max(span, key=lambda v: counts.get(v, 0))
            step = next(s for s in (1, 2, 5, 10, 20) if slot * s >= 52)
            labelled = {v for v in span if v % step == 0}
            labelled |= {e for e in (y0, y1) if all(abs(e - v) * slot >= 52 for v in labelled)}
            dr.line((x0 * S, base * S, x1 * S, base * S), fill=INK3, width=2)
            for i, yr in enumerate(span):
                n = counts.get(yr, 0)
                bx = gx + i * slot + (slot - bw) / 2
                hh = (base - top - 26) * n / mx
                if n:
                    dr.rectangle((bx * S, (base - hh) * S, (bx + bw) * S, base * S), fill=SIGNAL if yr == peak else (232, 148, 118))
                    if slot >= 30 or yr == peak:
                        dr.text(((bx + bw / 2) * S, (base - hh - 6) * S), str(n), font=SANS(16 if slot < 40 else 19, 500), fill=INK if yr == peak else INK2, anchor="ms")
                if yr in labelled:
                    dr.text(((bx + bw / 2) * S, (base + 10) * S), str(yr), font=SANS(16), fill=INK3, anchor="mt")
        _footer(dr)
        _save(img, path)
    return cached(out, ["time", c["name"], c.get("slug"), c["evidence"], sub, sorted(counts.items())], draw)


def countries_card(out, countries, line):
    """The Countries page: every country's flag in a grid. countries: [(slug, name)]."""
    flags = [(s, n) for s, n in countries if flag_file(s)]

    def draw(path):
        img, dr = _canvas()
        dr.text((60 * S, 54 * S), "COUNTRIES", font=SANS(20, 500), fill=INK3)
        dr.text((56 * S, 84 * S), "Country by country", font=SERIF(100), fill=INK)
        dr.text((1140 * S, 70 * S), str(len(countries)), font=SERIF(104), fill=SIGNAL, anchor="rt")
        dr.text((1140 * S, 178 * S), "countries so far", font=SANS(22, 500), fill=INK2, anchor="rt")
        dr.text((60 * S, 204 * S), line, font=SANS(25), fill=INK2)
        n = max(1, len(flags))
        gx, gy, gw, gh = 60, 262, 1080, 276
        for cols in range(8, 40):
            rows = -(-n // cols)
            cw = gw / cols
            fw = min(cw - 14, 80)
            fh = fw * 2 / 3
            if rows * (fh + 14) <= gh:
                break
        for i, (slug, _) in enumerate(flags):
            r, k = divmod(i, cols)
            _flag(img, slug, gx + k * cw, gy + r * (fh + 14), fw, fh, center=False)
        _footer(dr)
        _save(img, path)
    return cached(out, ["countries", [s for s, _ in flags], line], draw)


def resources_card(out, kinds, bill_states, line):
    """The Resources page: how many polls, papers, reports and bills, and where the bills stand. kinds: [(label, count)]; bill_states: [(label, count)]."""
    def draw(path):
        img, dr = _canvas()
        _blurb(dr, "Resources", "Polls, papers, reports and bills", line, line_count=1)
        total = sum(n for _, n in bill_states)
        if total:
            by = 424
            dr.text((60 * S, by * S), f"{total} BILLS BY STATE", font=SANS(16, 500), fill=INK3)
            cols = [SIGNAL, (232, 148, 118), INK2, INK3, LAND]
            x = 60
            for (lab, n), col in zip(bill_states, cols):
                w = 620 * n / total
                dr.rectangle((x * S, (by + 28) * S, (x + w - 2) * S, (by + 46) * S), fill=col)
                x += w
            lx, ly = 60, by + 66
            for (lab, n), col in zip(bill_states, cols):
                t = f"{n} {lab.lower()}"
                tw = dr.textlength(t, font=SANS(18)) / S + 38
                if lx + tw > 680:
                    lx, ly = 60, ly + 28
                dr.rectangle((lx * S, (ly + 5) * S, (lx + 14) * S, (ly + 19) * S), fill=col)
                dr.text(((lx + 22) * S, ly * S), t, font=SANS(18), fill=INK2)
                lx += tw
        _panel(dr)
        mx = max([n for _, n in kinds] + [1])
        for i, (lab, n) in enumerate(kinds):
            ry = 72 + i * 110
            if i:
                dr.line((776 * S, (ry - 18) * S, 1126 * S, (ry - 18) * S), fill=RULE, width=2)
            dr.text((776 * S, ry * S), f"{n:,}", font=SERIF(68), fill=SIGNAL)
            dr.text((930 * S, (ry + 10) * S), lab, font=SANS(24, 500), fill=INK)
            dr.rectangle((930 * S, (ry + 52) * S, (930 + max(6, int(196 * n / mx))) * S, (ry + 57) * S), fill=SIGNAL)
        _footer(dr)
        _save(img, path)
    return cached(out, ["resources", kinds, bill_states, line], draw)


def parliaments_card(out, n_chambers, lit, seats, line):
    """The Parliaments page: one big hemicycle with the share of seats held by a supporter, found so far, lit."""
    def draw(path):
        img, dr = _canvas()
        _blurb(dr, "Parliaments", "Seats in every parliament", line)
        dr.text((60 * S, 418 * S), f"{lit:,}", font=SERIF(76), fill=SIGNAL)
        nx = 60 + dr.textlength(f"{lit:,}", font=SERIF(76)) / S + 18
        dr.text((nx * S, 424 * S), f"of {seats:,} seats in {n_chambers} chambers", font=SANS(23, 500), fill=INK)
        dr.text((nx * S, 456 * S), "held by a sitting supporter, found so far", font=SANS(19), fill=INK2)
        _panel(dr)
        pts, dot = _hemicycle(420)
        on_n = max(1, round(420 * lit / seats)) if seats else 0
        on = {int((k + .5) * 420 / on_n) for k in range(on_n)} if on_n else set()
        radius, cx, cy = 175, 950, 330
        for i, (_, _, x, y) in enumerate(pts):
            px, py, r = (cx + x * radius) * S, (cy + y * radius) * S, dot * radius * S
            dr.ellipse((px - r, py - r, px + r, py + r), fill=SIGNAL if i in on else (205, 198, 183))
        dr.text((cx * S, 366 * S), f"{lit / seats:.1%}" if seats else "", font=SERIF(60), fill=INK, anchor="mt")
        dr.text((cx * S, 436 * S), "of all seats, shown as 420 dots", font=SANS(17), fill=INK3, anchor="mt")
        _footer(dr)
        _save(img, path)
    return cached(out, ["parliaments", n_chambers, lit, seats, line], draw)


def story_card(out, c, units, title, standfirst):
    """A country's story: the flag and 'Story' kicker, the headline, the standfirst, and the country's map when there is one."""
    def draw(path):
        img, dr = _canvas()
        _kicker(img, dr, f"Story · {c['name']}", c.get("slug"))
        lines, size = _title(dr, title, 640 if units else 1000, 3, 76, 48)
        y = _put_title(dr, lines, size, 56, 92) + 28
        for ln in _wrap(dr, standfirst, SANS(24), 640 if units else 1000, 4):
            dr.text((60 * S, y * S), ln, font=SANS(24), fill=INK2); y += 33
        dr.text((60 * S, 504 * S), "BY EGALITARISTEN", font=SANS(17, 500), fill=INK3)
        if units:
            _panel(dr)
            _area_map(dr, (760, 60, 380, 436), units)
        _footer(dr)
        _save(img, path)
    return cached(out, ["story", c["name"], c.get("slug"), title, standfirst, len(units)], draw)


# ---------- calculator card ----------
def _bracket_tax(rows, w):
    """Marginal brackets: rows are (threshold, rate in percent); the same sum as calcTax() in site/app.js."""
    t = 0.0
    for i, (lo, rate) in enumerate(rows):
        hi = rows[i + 1][0] if i + 1 < len(rows) else float("inf")
        if w > lo:
            t += (min(w, hi) - lo) * rate / 100
    return t


def calculator_card(out, curves, title, line, unit="€"):
    """The calculator page: real schemes drawn as the share of wealth they take, by wealth on a log scale.
    curves: (label, rows, colour) with rows as (threshold, percent), all in one currency."""
    import math
    def draw(path):
        img, dr = _canvas()
        _blurb(dr, "Calculator", title, line)
        _panel(dr)
        dr.text((772 * S, 62 * S), f"SHARE OF WEALTH TAKEN EACH YEAR, {unit}1M TO {unit}10BN", font=SANS(15, 500), fill=INK3)
        x0, x1, y0, y1 = 800, 1030, 130, 456  # chart box; the labels sit to the right of x1
        top = 4.0
        sx = lambda w: x0 + (x1 - x0) * (math.log10(w) - 6) / 4
        sy = lambda r: y1 - (y1 - y0) * r / top
        for r in range(0, 5):
            dr.line((x0 * S, sy(r) * S, x1 * S, sy(r) * S), fill=RULE, width=S)
            dr.text(((x0 - 10) * S, sy(r) * S), f"{r}%", font=SANS(15), fill=INK3, anchor="rm")
        for e, lab in ((6, "1M"), (7, "10M"), (8, "100M"), (9, "1bn"), (10, "10bn")):
            gx = sx(10 ** e)
            dr.line((gx * S, y1 * S, gx * S, (y1 + 6) * S), fill=INK3, width=S)
            dr.text((gx * S, (y1 + 10) * S), lab, font=SANS(15), fill=INK3, anchor="ma")
        ends = []
        for lab, rows, col in curves:
            pts = []
            for k in range(0, 161):
                w = 10 ** (6 + 4 * k / 160)
                pts.append((sx(w) * S, sy(min(top, 100 * _bracket_tax(rows, w) / w)) * S))
            dr.line(pts, fill=col, width=4 * S, joint="curve")
            ends.append([lab, col, pts[-1][1] / S])
        ends.sort(key=lambda e: e[2])
        for i in range(1, len(ends)):  # keep the end labels apart
            ends[i][2] = max(ends[i][2], ends[i - 1][2] + 24)
        for lab, col, y in ends:
            dr.text(((x1 + 12) * S, y * S), lab, font=SANS(17, 500), fill=col, anchor="lm")
        _footer(dr)
        _save(img, path)
    return cached(out, ["calc", title, line, unit, [[l, [list(r) for r in rows], list(c)] for l, rows, c in curves]], draw)
