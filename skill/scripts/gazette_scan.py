#!/usr/bin/env python3
"""Read legislative records that are published as PDFs (gazettes, plenary minutes, committee reports).

Why this exists: a bill-tracker page often says little, and press snippets say less, yet the official
gazettes hold the named roll calls and the speeches. Colombia's Ley 2277 (2022) looked like "block votes only"
until the plenary minutes were read in full: they hold a named vote on deleting the wealth-tax article and
speeches defending it. Read the documents; do not conclude from snippets.

Usage
  python gazette_scan.py DIR                     # DIR holds the PDFs (or the .txt files made from them)
  python gazette_scan.py DIR --term patrimonio   # the word(s) that mark the wealth tax in that language
  python gazette_scan.py DIR --term "Vermögen|Vermögensteuer" --article 31

What it does
  1. Extracts text from every PDF once (DIR/<name>.txt, keeps the line breaks, which hold the structure).
  2. Prints one line per document: its header, size and how often the term occurs.
  3. Lists every named vote ("Votación nominal", "roll call", "Namensabstimmung" ... see VOTE_HEADS) with the
     article numbers in its title, the printed result and the number of names printed under each side.
     Votes whose title names the wealth-tax article, or deletes/amends it, are the ones to use.
  4. Prints each passage with the term, with the nearest preceding speaker label.
  5. Writes the printed name lists of the votes selected with --article to DIR/votes_<article>.json,
     one name per line exactly as printed (a roll call is quoted from the member's own entry).

It prints; it does not edit the register. Parties, seats and Wikidata ids still come from the official
member list. Check the extracted names against the PDF before using them.
"""
import argparse, json, os, re, sys
from pathlib import Path

VOTE_HEADS = r"(Votaci[oó]n nominal|Votaci[oó]n ordinaria|Roll[- ]?call|Namentliche Abstimmung|Namensabstimmung|Appel nominal|Scrutin public|Votação nominal|Votazione nominale)"
SIDE_HEADS = {"yes": r"^\s*Por el S[ií]\b|^\s*(Yes|Ja|Pour|Sim|Favorevoli)\s*$", "no": r"^\s*Por el No\b|^\s*(No|Nein|Contre|Não|Contrari)\s*$"}
SPEAKER = re.compile(r"(Palabras d[eo]l?[^\n:.]{3,80}|(?:hace uso de la palabra|interviene|Intervenci[oó]n d[eo]l?)[^\n:]{3,90}|Dirección de Presidencia, [^\n:]{3,60}|[A-ZÁÉÍÓÚÑ][\wáéíóúñ]+(?: [\wáéíóúñ]+){1,4}):")


def extract(d: Path):
    texts = {}
    for p in sorted(d.iterdir()):
        if p.suffix.lower() == ".pdf":
            t = p.with_suffix(".txt")
            if not t.exists():
                try:
                    from pypdf import PdfReader
                except ImportError:
                    sys.exit("pypdf is needed to read PDFs: pip install pypdf")
                r = PdfReader(str(p))
                pages = []
                for pg in r.pages:
                    try:
                        pages.append(pg.extract_text() or "")
                    except Exception:
                        pages.append("")
                t.write_text("\n\f".join(pages), encoding="utf-8")
            texts[p.stem] = t.read_text(encoding="utf-8")
        elif p.suffix.lower() == ".txt" and p.with_suffix(".pdf").exists() is False:
            texts[p.stem] = p.read_text(encoding="utf-8")
    return texts


def flat(s):
    return re.sub(r"\s+", " ", s).strip()


SKIP = re.compile(r"^(Gaceta|Página|Votaci|Honorables|Proyecto|Por el|Martes|Viernes|Lunes|Miércoles|Jueves|Sábado|Domingo|\d+\.? ?[IVX]+\.? ?\d{4})", re.I)
NAME = re.compile(r"^[A-ZÁÉÍÓÚÑ][\wáéíóúñü.\-' ]+$")
PROSE_START = re.compile(r"^(La|El|Con|Los|Las|Sobre|Negada|Secretar|En consecuencia)\b")


def names_block(block):
    """Names printed one per line. Stops at the first line of running prose once the list has started."""
    out = []
    for line in block.split("\n"):
        line = line.strip().replace("\x0c", "")
        if not line or SKIP.match(line):
            continue
        if NAME.match(line) and 2 <= len(line.split()) <= 6 and not PROSE_START.match(line):
            out.append(line)
        elif out and len(line.split()) >= 3:
            break
    return out


def votes(text):
    """Yield (offset, title, result_line, yes_names, no_names) for each named vote that prints its lists."""
    heads = [m.start() for m in re.finditer(VOTE_HEADS, text)]
    for i, a in enumerate(heads):
        b = heads[i + 1] if i + 1 < len(heads) else min(len(text), a + 40000)
        seg = text[a:b]
        title = flat(seg[:420])
        if not re.search(SIDE_HEADS["yes"], seg, re.M | re.I) and not re.search(SIDE_HEADS["no"], seg, re.M | re.I):
            continue
        yi = re.search(SIDE_HEADS["yes"], seg, re.M | re.I)
        ni = re.search(SIDE_HEADS["no"], seg, re.M | re.I)
        end = len(seg)
        yes, no = [], []
        if yi and ni and yi.start() < ni.start():
            yes = names_block(seg[yi.end():ni.start()])
            tail = re.search(r"En consecuencia|ha sido (aprobad|negad)|Votaci[oó]n nominal|Gaceta del Congreso \d+ \w+, \d+", seg[ni.end():])
            no = names_block(seg[ni.end():ni.end() + (tail.start() if tail else 6000)])
        elif ni and yi and ni.start() < yi.start():
            no = names_block(seg[ni.end():yi.start()])
            tail = re.search(r"En consecuencia|ha sido (aprobad|negad)|Votaci[oó]n nominal", seg[yi.end():])
            yes = names_block(seg[yi.end():yi.end() + (tail.start() if tail else 6000)])
        elif yi:
            yes = names_block(seg[yi.end():end])
        elif ni:
            no = names_block(seg[ni.end():end])
        before = text[max(0, a - 1500):a]
        res = re.findall(r"Por el S[ií]:?\s*\d+\s*Por el No:?\s*\d+\s*TOTAL:?\s*\d+", before, re.I)
        yield a, title, (flat(res[-1]) if res else ""), yes, no


def merged(vs):
    """A list that runs over a page break repeats its heading: join entries that share a title."""
    out = {}
    for off, title, res, yes, no in vs:
        k = title[:230]
        if k in out:
            o = out[k]
            o[3].extend(x for x in yes if x not in o[3])
            o[4].extend(x for x in no if x not in o[4])
            o[2] = o[2] or res
        else:
            out[k] = [off, title, res, list(yes), list(no)]
    return [tuple(v) for v in out.values()]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir")
    ap.add_argument("--term", default="patrimonio|wealth tax|Vermögen")
    ap.add_argument("--article", help="article number: print and save name lists of votes whose title names it")
    ap.add_argument("--context", type=int, default=450)
    ap.add_argument("--max-hits", type=int, default=25, help="per document")
    a = ap.parse_args()
    d = Path(a.dir)
    texts = extract(d)
    term = re.compile(a.term, re.I)
    print(f"{len(texts)} documents in {d}")
    for k, t in texts.items():
        print(f"== {k}: {len(t):,} chars, {len(term.findall(t))} hits of /{a.term}/ | {flat(t[:160])[:110]}")
    saved = {}
    for k, t in texts.items():
        vs = merged(votes(t))
        if not vs:
            continue
        print(f"\n##### named votes in {k}: {len(vs)}")
        for off, title, res, yes, no in vs:
            mark = ""
            if a.article and re.search(rf"\b(art[ií]culos?|art\.?)[^.]{{0,200}}\b{re.escape(a.article)}\b", title, re.I):
                mark = "  <== article " + a.article
                saved[f"{k}@{off}"] = dict(title=title, result=res, yes=yes, no=no)
            print(f"[{off}] {res or '-'} | names yes={len(yes)} no={len(no)} | {title[:200]}{mark}")
    if a.article and saved:
        out = d / f"votes_{a.article}.json"
        out.write_text(json.dumps(saved, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\nsaved {len(saved)} vote(s) naming article {a.article} to {out}")
    print("\n##### passages")
    for k, t in texts.items():
        last = -10 ** 9
        n = 0
        for m in term.finditer(t):
            if m.start() - last < a.context * 3:
                continue
            last = m.start()
            n += 1
            if n > a.max_hits:
                print(f"  ... more hits in {k}; raise --max-hits")
                break
            before = t[max(0, m.start() - 4000):m.start()]
            sp = [x.group(1) for x in SPEAKER.finditer(before)]
            who = flat(sp[-1])[:90] if sp else "?"
            print(f"[{k} @{m.start()}] {who}\n    {flat(t[max(0, m.start() - a.context // 2):m.end() + a.context])}\n")


if __name__ == "__main__":
    main()
