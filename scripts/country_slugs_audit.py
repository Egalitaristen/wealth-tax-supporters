"""Audit every place the country folder code (fr, gb, australia ...) is used, before the folders are renamed to full names.

Read-only. Reads data/countries.csv (folder, slug, name, iso2, kind) and prints, per kind of reference, how many there are and where:
  - folder:id references (fr:A0001) in any tracked text file
  - data/<folder>/ paths in text
  - site URLs: /<folder>, /<folder>/A0001, /resources/<folder>-slug and full wealthtaxsupporters.com links
  - the `country` field of data/resources*.json and resource slug prefixes
  - CSV columns that hold a folder code
  - quoted two-letter codes in scripts (hand-check: these decide which tools need a mapping)
Run: python scripts/country_slugs_audit.py [--examples N] [--write docs/country-slugs-audit.md]
"""
import argparse, collections, csv, json, os, re, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("--examples", type=int, default=3)
ap.add_argument("--write", default="")
args = ap.parse_args()

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
C = list(csv.DictReader(open("data/countries.csv", encoding="utf-8", newline="")))
folders = [r["folder"] for r in C]
alt = "|".join(sorted(folders, key=len, reverse=True))
TEXT = (".py", ".js", ".md", ".json", ".csv", ".txt", ".html", ".css", ".toml", ".jsonc", ".sql", ".yml", ".yaml", ".sh", ".mjs")
files = [f for f in subprocess.run(["git", "ls-files"], capture_output=True, text=True, encoding="utf-8").stdout.split("\n")
         if f and f.endswith(TEXT) and not f.startswith(("_site/", "site/vendor/")) and f != "scripts/country_slugs_audit.py" and f != "data/countries.csv"]

PAT = {
    "folder:id reference (fr:A0001)": re.compile(rf"(?<![\w/.-])({alt}):[AEHROBLMXGDQ]\d{{3,5}}\b"),
    "data/<folder>/ path": re.compile(rf"data/({alt})/"),
    "site URL /<folder>/A0001 or /<folder>/seats": re.compile(rf"(?:wealthtaxsupporters\.com)?/({alt})/(?:A\d{{4}}|seats|[a-z-]+\.html)"),
    "site URL /<folder> (page)": re.compile(rf"wealthtaxsupporters\.com/({alt})(?=[\"')\s/#?.]|$)"),
    "resource slug prefix /resources/<folder>-": re.compile(rf"/resources/({alt})-"),
}
found = {k: collections.Counter() for k in PAT}
examples = {k: [] for k in PAT}
by_file = {k: collections.Counter() for k in PAT}
for f in files:
    try:
        text = open(f, encoding="utf-8").read()
    except Exception:
        continue
    for k, p in PAT.items():
        n = 0
        for m in p.finditer(text):
            n += 1
            found[k][m.group(1)] += 1
            if len(examples[k]) < args.examples * 4 and (not examples[k] or examples[k][-1][0] != f):
                line = text[:m.start()].count("\n") + 1
                examples[k].append((f, line, text.splitlines()[line - 1].strip()[:140]))
        if n:
            by_file[k][f] += n

out = []
def p(s=""):
    out.append(s)

p("# Country folder codes: where they are used")
p(f"{len(folders)} folders in data/countries.csv; {len(files)} tracked text files scanned.\n")
for k in PAT:
    tot = sum(found[k].values())
    p(f"## {k}: {tot}")
    areas = collections.Counter()
    for f, n in by_file[k].items():
        areas[f.split("/")[0] + ("/" + f.split("/")[1] if f.startswith(("data/", "skill/", "content/", "docs/")) and f.count("/") > 1 else "")] += n
    p("by area: " + ", ".join(f"{a} {n}" for a, n in areas.most_common(12)))
    p("top files: " + ", ".join(f"{f} {n}" for f, n in by_file[k].most_common(6)))
    for f, line, t in examples[k][:args.examples]:
        p(f"  e.g. {f}:{line}  {t}")
    p()

# resources and exclusions: the country field
for name in ("data/resources.json", "data/resources_excluded.json"):
    if not os.path.exists(name):
        continue
    d = json.load(open(name, encoding="utf-8"))
    c = collections.Counter(x.get("country") for x in d if isinstance(x, dict))
    bad = sorted(k for k in c if k not in folders and k != "global")
    p(f"## {name}: `country` field on {sum(c.values())} entries ({len(c)} distinct); not a folder: {bad or 'none'}")
    slugs = [x.get("slug", "") for x in d if isinstance(x, dict)]
    pre = sum(1 for s in slugs if s and re.match(rf"({alt})-", s))
    p(f"   slugs starting with a folder code: {pre} of {sum(1 for s in slugs if s)}\n")

# CSV columns that hold a folder or code
p("## CSV columns with folder-like codes (all of data/*.csv at the top level and every data/<folder>/*.csv)")
seen = collections.Counter()
codeset = set(folders) | {f.upper() for f in folders}
tops = [f for f in files if f.endswith(".csv") and f.count("/") in (1, 2)]
for f in tops:
    try:
        rows = list(csv.DictReader(open(f, encoding="utf-8", newline="")))
    except Exception:
        continue
    if not rows:
        continue
    for col in [c for c in rows[0].keys() if c]:
        vals = [r[col] for r in rows if isinstance(r.get(col), str) and r.get(col)]
        if vals and sum(1 for v in vals if v in codeset) >= max(1, len(vals) // 2):
            seen[(f if f.count("/") == 1 else "data/<folder>/" + f.split("/")[-1], col)] += len(vals)
for (f, col), n in sorted(seen.items()):
    p(f"  {f}: column {col} ({n} rows)")
p()


# files and folders named by a code (they need renaming too)
p("## Tracked files named after a folder code (rename with the folders)")
allf = subprocess.run(["git", "ls-files"], capture_output=True, text=True, encoding="utf-8").stdout.split(chr(10))
named = collections.Counter()
for f in allf:
    stem = os.path.splitext(os.path.basename(f))[0]
    if f and stem in folders and not f.startswith("data/" + stem + "/") and f != "data/countries.csv":
        named[os.path.dirname(f)] += 1
for d, n in sorted(named.items()):
    p(f"  {d}/: {n} files")
p()
# quoted codes in scripts and the site
p("## Quoted two-letter codes in code (hand-check; each is a place that may need the mapping)")
q = re.compile(rf"""['"]({'|'.join(f for f in folders if len(f) == 2)})['"]""")
for f in files:
    if f.endswith((".py", ".js", ".mjs")):
        t = open(f, encoding="utf-8").read()
        hits = q.findall(t)
        if hits:
            p(f"  {f}: {len(hits)} quoted codes, {len(set(hits))} distinct")
p()
p("## Other places to check by hand")
for f in ("wrangler.jsonc", "worker/index.js", "site/_headers", "infra/d1/reports.sql", "infra/d1/suggestions.sql", "infra/d1/schema.sql", "scripts/deploy.py"):
    if os.path.exists(f):
        t = open(f, encoding="utf-8").read()
        p(f"  {f}: {len(re.findall(r'country|folder', t))} mentions of country/folder")
text = "\n".join(out)
print(text)
if args.write:
    open(args.write, "w", encoding="utf-8", newline="\n").write(text + "\n")
