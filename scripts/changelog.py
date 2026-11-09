#!/usr/bin/env python3
"""Build data/changelog.json: what changed in the register on each day, with numbers by country.

The numbers come from git, not from pull-request text. Every commit on the main branch (squash merges, so each
commit is one change) is diffed against its parent: supporters are actor ids added to or removed from a country's
actors.csv, statements are evidence ids added to or removed from its evidence.csv. A commit is counted once, on the
day it landed, so a day can never be counted twice.

The words come from data/changelog_notes.json: {"2026-11-09": {"summary": "...", "items": [{"kind": "added|improved|corrected", "text": "..."}]}}.
A day without notes still gets its numbers.

Usage: python scripts/changelog.py          (rewrites data/changelog.json; needs the full git history)
"""
import csv, io, json, subprocess, sys, collections
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def git(*args, check=True):
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode:
        raise SystemExit(r.stderr)
    return r.stdout


def ids_in(rev, path, col):
    out = git("show", f"{rev}:{path}", check=False)
    if not out:
        return set()
    return {row[col] for row in csv.DictReader(io.StringIO(out)) if row.get(col)}


def country_names():
    names = {}
    for meta in DATA.glob("*/meta.json"):
        try:
            names[meta.parent.name] = json.load(open(meta, encoding="utf-8")).get("name", meta.parent.name.upper())
        except Exception:
            pass
    return names


def main():
    commits = git("log", "--first-parent", "--reverse", "--format=%H|%cI").split()
    days = collections.OrderedDict()
    for line in commits:
        sha, when = line.split("|")
        day = when[:10]
        d = days.setdefault(day, dict(countries=collections.defaultdict(lambda: dict(s=0, sr=0, e=0, er=0)), stories=[], arguments=[], new_countries=[]))
        is_root = subprocess.run(["git", "rev-parse", "--verify", "-q", sha + "^"], cwd=ROOT, capture_output=True).returncode != 0
        parent = sha + "^"
        paths = ["--", "data/*/actors.csv", "data/*/evidence.csv", "content/stories", "content/arguments"]
        if is_root:  # nothing before it: every file counts as added
            diff = git("diff-tree", "--root", "-r", "--name-status", "--no-renames", "--format=", sha, *paths, check=False)
        else:
            diff = git("diff", "--name-status", "--no-renames", parent, sha, *paths, check=False)
        for row in diff.strip().split("\n"):
            if not row:
                continue
            status, path = row.split("\t")
            parts = path.split("/")
            if parts[0] == "content":
                name = parts[-1][:-3]
                if status == "A" and name not in ("STYLE", "README"):
                    (d["stories"] if parts[1] == "stories" else d["arguments"]).append(name)
                continue
            iso, kind = parts[1], parts[2]
            col, k_add, k_rem = ("actor_id", "s", "sr") if kind == "actors.csv" else ("evidence_id", "e", "er")
            before, after = ids_in(parent, path, col), ids_in(sha, path, col)
            c = d["countries"][iso]
            c[k_add] += len(after - before)
            c[k_rem] += len(before - after)
            if kind == "actors.csv" and status == "A" and after:
                d["new_countries"].append(iso)
    notes_path = DATA / "changelog_notes.json"
    notes = json.load(open(notes_path, encoding="utf-8")) if notes_path.exists() else {}
    names = country_names()
    out = []
    for day in sorted(days, reverse=True):
        d = days[day]
        rows = []
        for iso, c in sorted(d["countries"].items(), key=lambda kv: -(kv[1]["s"] + kv[1]["e"])):
            if any(c.values()):
                rows.append([iso, names.get(iso, iso.upper()), c["s"], c["sr"], c["e"], c["er"]])
        entry = dict(date=day, countries=rows,
                     new_countries=[names.get(i, i.upper()) for i in dict.fromkeys(d["new_countries"])],
                     stories=list(dict.fromkeys(d["stories"])), arguments=list(dict.fromkeys(d["arguments"])))
        entry.update(notes.get(day, {}))
        out.append(entry)
    json.dump(out, open(DATA / "changelog.json", "w", encoding="utf-8"), separators=(",", ":"), ensure_ascii=False)
    print(f"{len(out)} days, {sum(r[2] for e in out for r in e['countries'])} supporters added, {sum(r[4] for e in out for r in e['countries'])} statements added")


if __name__ == "__main__":
    main()
