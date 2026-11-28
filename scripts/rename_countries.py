"""Plan the rename of country folders and URLs from codes (fr, gb, australia) to full names (docs/country-slugs-plan.md).

DRY RUN ONLY: it reads data/countries.csv and the tracked files, and writes nothing in the repository.
It lists the moves, applies every text rewrite in memory, counts them per rule and area, checks for collisions and
for references the rules would leave behind, and builds the redirect map.

    python scripts/rename_countries.py                      # summary
    python scripts/rename_countries.py --report out.md      # full report: every move, sample diffs, redirect map
    python scripts/rename_countries.py --verify             # rewrite a temporary copy and run the register validation on it
"""
import argparse, collections, csv, io, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NL = chr(10)
ap = argparse.ArgumentParser()
ap.add_argument("--report", default="")
ap.add_argument("--verify", action="store_true")
ap.add_argument("--samples", type=int, default=4)
ap.add_argument("--copy", default="", help="write a renamed copy of the repository to this folder (outside the repository), to build and compare")
args = ap.parse_args()

C = list(csv.DictReader(open(ROOT / "data" / "countries.csv", encoding="utf-8", newline="")))
SLUG = {r["folder"]: r["slug"] for r in C}
CHANGING = {f: s for f, s in SLUG.items() if f != s}
ALT = "|".join(sorted(CHANGING, key=len, reverse=True))
TEXT = (".py", ".js", ".md", ".json", ".csv", ".txt", ".html", ".css", ".toml", ".jsonc", ".sql", ".yml", ".yaml", ".sh", ".mjs")
# never rewritten: the mapping and its tools, generated files, and the file keyed by ISO code
SKIP = {"data/countries.csv", "data/featured_skip.txt", "data/changelog.json", "docs/country-slugs-audit.md", "docs/country-slugs-plan.md",
        "scripts/country_slugs_audit.py", "scripts/rename_countries.py", "skill/scripts/countries.py"}
NAMED_DIRS = ("content/stories", "skill/references/countries", "skill/references/records")
PROSE = ("content/", "docs/", "refine/", "skill/", "README.md", "CONTRIBUTING.md", "ROADMAP.md")


def tracked():
    out = subprocess.run(["git", "ls-files"], capture_output=True, text=True, encoding="utf-8", cwd=ROOT, check=True).stdout
    return [f for f in out.split(NL) if f]


# ---------------------------------------------------------------- moves
def moves(files):
    out = []
    for old, new in sorted(CHANGING.items()):
        if any(f.startswith(f"data/{old}/") for f in files):
            out.append((f"data/{old}", f"data/{new}"))
        for d in NAMED_DIRS:
            for f in files:
                if os.path.dirname(f) == d and os.path.splitext(os.path.basename(f))[0] == old:
                    out.append((f, f"{d}/{new}{os.path.splitext(f)[1]}"))
    return out


# ---------------------------------------------------------------- text rules
def m(g):
    return CHANGING[g]


RULES = [
    # name, applies(path), pattern, replacement
    ("folder:id (fr:A0001)", lambda f: True,
     re.compile(rf"(?<![\w/.:-])({ALT}):([AEHROBLMXGDQ]\d{{3,5}})\b"), lambda x: f"{m(x[1])}:{x[2]}"),
    ("folder-id in supranational seats (fr-A0001)", lambda f: f.startswith("data/"),
     re.compile(rf"(?<![\w/.:-])({ALT})-(A\d{{4}})\b"), lambda x: f"{m(x[1])}-{x[2]}"),
    ("data/<folder> path", lambda f: True,
     re.compile(rf"(?<![\w-])data/({ALT})(?![\w-])"), lambda x: f"data/{m(x[1])}"),
    ("markdown link ](/<folder>…)", lambda f: f.startswith(PROSE),
     re.compile(rf"\]\(/({ALT})(?=[/)?#])"), lambda x: f"](/{m(x[1])}"),
    ("full site link wealthtaxsupporters.com/<folder>", lambda f: True,
     re.compile(rf"(wealthtaxsupporters\.com)/({ALT})(?=[\"')\]\s/?#.,]|$)", re.M), lambda x: f"{x[1]}/{m(x[2])}"),
    ("inline path /<folder>/A0001", lambda f: f.startswith(PROSE),
     re.compile(rf"(?<=[`\"' ])/({ALT})/(A\d{{4}}|seats|directory)\b"), lambda x: f"/{m(x[1])}/{x[2]}"),
    ("resource link /resources/<folder>-…", lambda f: True,
     re.compile(rf"/resources/({ALT})-(?=[a-z0-9])"), lambda x: f"/resources/{m(x[1])}-"),
]


def rewrite_resources(text, log):
    """resources.json keeps one entry per line: change only the country and slug values on the lines that need it."""
    out = []
    for line in text.split(NL):
        new = re.sub(rf'("country": ?")({ALT})(")', lambda x: x[1] + m(x[2]) + x[3], line)
        if new != line:
            log["resources `country` value"] += 1
        new2 = re.sub(rf'("slug": ?")({ALT})-', lambda x: x[1] + m(x[2]) + "-", new)
        if new2 != new:
            log["resources slug prefix"] += 1
        out.append(new2)
    return NL.join(out)


def resource_slugs():
    """Old resource slug -> new, for every stored slug that starts with a country code."""
    out = {}
    for x in json.loads((ROOT / "data" / "resources.json").read_text(encoding="utf-8")):
        s = x.get("slug") or ""
        head = s.split("-")[0]
        if head in CHANGING:
            out[s] = CHANGING[head] + s[len(head):]
    return out


RES = resource_slugs()
RES_PAT = re.compile(r"(?:(?<=/resources/)|(?<![\w/-]))(" + "|".join(sorted(map(re.escape, RES), key=len, reverse=True)) + r")(?![\w-])")
SLUG_FILES = ("site/", "scripts/", "worker/", "content/", "refine/", "skill/", "data/")


def rewrite(path, text):
    log = collections.Counter()
    if path.startswith(SLUG_FILES) and path not in ("data/resources.json",):  # a slug named on its own, as in the calculator's presets
        text, n = RES_PAT.subn(lambda x: RES[x[1]], text)
        if n:
            log["resource slug named in text or code"] += n
    if path in ("data/resources.json", "data/resources_excluded.json"):
        text = rewrite_resources(text, log)
    if path == "data/media_sources.json":
        text, n = re.subn(rf'("country": ?")({ALT})(")', lambda x: x[1] + m(x[2]) + x[3], text)
        if n:
            log["media source `country` value"] += n
    for name, applies, pat, rep in RULES:
        if applies(path):
            text, n = pat.subn(rep, text)
            if n:
                log[name] += n
    return text, log


def new_path(path, mv):
    for a, b in mv:
        if path == a or path.startswith(a + "/"):
            return b + path[len(a):]
    return path


def area(f):
    p = f.split("/")
    return "/".join(p[:2]) if p[0] in ("skill", "content", "docs") and len(p) > 2 else p[0]


files = tracked()
mv = moves(files)
text_files = [f for f in files if f.endswith(TEXT) and not f.startswith(("_site/", "site/vendor/")) and f not in SKIP]
changed, counts, areas, samples = {}, collections.Counter(), collections.Counter(), collections.defaultdict(list)
for f in text_files:
    raw = (ROOT / f).read_bytes().decode("utf-8", "replace")
    new, log = rewrite(f, raw)
    if new != raw:
        changed[f] = new
        counts.update(log)
        areas[area(f)] += sum(log.values())
        for a, b in zip(raw.split(NL), new.split(NL)):
            if a != b:
                key = next(iter(log))
                if len(samples[key]) < args.samples:
                    i = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), 0)
                    samples[key].append((f, a[max(0, i - 40):i + 50].strip(), b[max(0, i - 40):i + 60].strip()))
                break

# ---------------------------------------------------------------- checks
problems, warnings = [], []
RESERVED = {"resources", "arguments", "directory", "calculator", "about", "api", "flags", "fonts", "vendor", "global", "changelog", "search", "seats",
            "methodology", "stories", "petitions", "suggest", "report", "assets"}
if clash := sorted(set(SLUG.values()) & RESERVED):
    problems.append(f"slugs that collide with site pages: {clash}")
if len(set(SLUG.values())) != len(SLUG):
    problems.append("duplicate slugs in countries.csv")
folders = {f.split("/")[1] for f in files if f.startswith("data/") and f.count("/") >= 2}
if missing := sorted(folders - set(SLUG)):
    problems.append(f"data folders not in countries.csv: {missing}")
for a, b in mv:
    if (ROOT / b).exists():
        problems.append(f"target already exists: {b}")
if set(CHANGING.values()) & set(CHANGING):
    problems.append(f"a new name equals an old code: {sorted(set(CHANGING.values()) & set(CHANGING))}")

res = json.loads((ROOT / "data" / "resources.json").read_text(encoding="utf-8"))
new_res = json.loads(changed.get("data/resources.json", (ROOT / "data" / "resources.json").read_text(encoding="utf-8")))
if len(res) != len(new_res):
    problems.append("resources.json changes the number of entries")
slug_map = {o["slug"]: n["slug"] for o, n in zip(res, new_res) if o.get("slug") and o["slug"] != n["slug"]}
news = [x["slug"] for x in new_res if x.get("slug")]
if dup := [s for s, c in collections.Counter(news).items() if c > 1]:
    problems.append(f"duplicate resource slugs after rename: {dup[:5]}")
if noslug := [x["title"][:60] for x in res if x["kind"] in ("bill", "report", "paper") and not x.get("slug")]:
    warnings.append(f"{len(noslug)} bill/report/paper entries have no `slug`; the build derives one from the country, so their URL changes too: {noslug[:4]}")
bad_people = [p for x in new_res for p in x.get("people", []) if p.split(":")[0] not in set(SLUG.values())]
if bad_people:
    problems.append(f"people refs that would not resolve: {bad_people[:5]}")

# anything that still looks like an old reference after rewriting
LEFT = {"old folder:id left": re.compile(rf"(?<![\w/.:-])({ALT}):A\d{{4}}\b"),
        "old data/<folder> left": re.compile(rf"(?<![\w-])data/({ALT})(?![\w-])"),
        "old /<folder>/A0001 left": re.compile(rf"(?<![\w])/({ALT})/A\d{{4}}\b"),
        "old <folder>-A0001 left": re.compile(rf"(?<![\w/.:-])({ALT})-A\d{{4}}\b")}
left = collections.defaultdict(list)
for f in text_files:
    t = changed.get(f) or (ROOT / f).read_bytes().decode("utf-8", "replace")
    for k, p in LEFT.items():
        for x in p.finditer(t):
            left[k].append(f"{f}:{t[:x.start()].count(NL) + 1} {t[max(0, x.start() - 30):x.end() + 10].strip()!r}")

# code that assumes the folder name is a code: must be edited by hand before the rename
MANUAL = [
    ("folder name used as ISO code", re.compile(r"(slug|Path\(a\.dir\)[^\n]*name|\.name)(\.split\(\"-\"\)\[0\])?(\.resolve\(\)\.name)?\.upper\(\)|name\.split\(\"-\"\)\[0\]|slug\.split\(\"-\"\)\[0\]|resolve\(\)\.name\.upper\(\)")),
    ("two-letter assumption", re.compile(r"\[a-z\]\{2\}|== ?\"australia\"|=== ?'australia'")),
    ("folder-name rule", re.compile(r"slug == iso|slug\.startswith\(iso")),
    ("supranational folders named in code", re.compile(r"\(\"eu\", ?\"un\", ?\"au\"\)|'au' \|\| slug")),
    ("literal data path built from a code", re.compile(r"DATA ?/ ?\"[a-z]{2}\"|data[\"'], ?[\"'](" + ALT + r")[\"']")),
    ("git history read by folder path", re.compile(r"data/\*/actors\.csv")),
]
manual = collections.defaultdict(list)
for f in text_files:
    if f.endswith((".py", ".js", ".mjs")) and not f.startswith("data/"):
        for i, line in enumerate((ROOT / f).read_text(encoding="utf-8", errors="replace").split(NL), 1):
            for k, p in MANUAL:
                if p.search(line):
                    manual[k].append(f"{f}:{i}  {line.strip()[:130]}")

redirects = [(f"/{a}", f"/{b}") for a, b in sorted(CHANGING.items())] + [(f"/resources/{a}", f"/resources/{b}") for a, b in sorted(slug_map.items())]

# ---------------------------------------------------------------- report
R = []
R.append("# Rename dry run (nothing written)")
R.append(f"- folders and files to move: {len(mv)} ({sum(1 for a, _ in mv if a.startswith('data/'))} data folders, {sum(1 for a, _ in mv if not a.startswith('data/'))} files)")
R.append(f"- files whose text changes: {len(changed)}; replacements: {sum(counts.values())}")
R.append(f"- redirects needed: {len(redirects)} path prefixes ({len(CHANGING)} countries, {len(slug_map)} resource pages)")
R.append("")
R.append("## Replacements by rule")
R += [f"- {k}: {n}" for k, n in counts.most_common()]
R.append("")
R.append("## Replacements by area")
R.append(", ".join(f"{a} {n}" for a, n in areas.most_common()))
R.append("")
R.append("## Blocking problems")
R += [f"- {p}" for p in problems] or ["- none"]
R.append("")
R.append("## Warnings")
R += [f"- {w}" for w in warnings] or ["- none"]
R.append("")
R.append("## Old references the rules leave behind (check by hand)")
R += [f"- {k}: {len(v)}, e.g. " + "; ".join(v[:5]) for k, v in left.items()] or ["- none"]
R.append("")
R.append("## Code to edit by hand before the rename")
for k, v in manual.items():
    R.append(f"### {k} ({len(v)})")
    R += [f"- {x}" for x in v]
short = NL.join(R)
print(short)
if args.report:
    R.append("")
    R.append("## Sample changes")
    for k, v in samples.items():
        R.append(f"### {k}")
        for f, a, b in v:
            R.append(f"- {f}\n    - `{a}`\n    + `{b}`")
    R.append("")
    R.append("## Moves")
    R += [f"- {a} -> {b}" for a, b in mv]
    R.append("")
    R.append("## Redirect map")
    R += [f"- {a} -> {b}" for a, b in redirects]
    Path(args.report).write_text(NL.join(R) + NL, encoding="utf-8", newline=NL)
    print(f"\nfull report: {args.report}")

if args.copy:
    dest = Path(args.copy).resolve()
    if dest == ROOT or ROOT in dest.parents:
        sys.exit("--copy must be outside the repository")
    for f in files:
        dst = dest / new_path(f, mv)
        dst.parent.mkdir(parents=True, exist_ok=True)
        if f in changed:
            dst.write_bytes(changed[f].encode("utf-8"))
        else:
            shutil.copy2(ROOT / f, dst)
    print(f"renamed copy written to {dest}")

if args.verify:
    # apply to a throwaway copy and run the register's own checks there
    tmp = Path(tempfile.mkdtemp(prefix="slugs-"))
    for f in files:
        if f.startswith(("data/", "skill/")):
            dst = tmp / new_path(f, mv)
            dst.parent.mkdir(parents=True, exist_ok=True)
            if f in changed:
                dst.write_bytes(changed[f].encode("utf-8"))
            else:
                shutil.copy2(ROOT / f, dst)
    def rows(base):
        out = collections.Counter()
        for p in (base / "data").glob("*/*.csv"):
            out[(p.parent.name, p.name)] = sum(1 for _ in csv.reader(open(p, encoding="utf-8", newline="")))
        return out
    before, after = rows(ROOT), rows(tmp)
    diff = {k for k, n in before.items() if after.get((SLUG.get(k[0], k[0]), k[1])) != n}
    print(f"\nverify: {len(before)} tables before, {len(after)} after, row counts differ in {len(diff)}")
    errs = collections.Counter()
    for d in sorted((tmp / "data").iterdir()):
        if d.is_dir():
            p = subprocess.run([sys.executable, str(tmp / "skill" / "scripts" / "wtdb.py"), "validate", str(d)], capture_output=True, text=True, encoding="utf-8", cwd=tmp)
            for line in (p.stdout + p.stderr).split(NL):
                if line.startswith(("ERROR", "Traceback")):
                    errs[re.sub(r"'[^']*'", "'…'", line)[:150]] += 1
    print(f"verify: validation errors in the renamed copy: {sum(errs.values())}")
    for k, n in errs.most_common(8):
        print(f"  {n} x {k}")
    shutil.rmtree(tmp, ignore_errors=True)
