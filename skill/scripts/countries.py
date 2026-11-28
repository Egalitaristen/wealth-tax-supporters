"""Country folders: look one up by its code (fr, australia) or its full-name slug (france), from data/countries.csv.

Folders are being renamed from codes to full names (docs/country-slugs-plan.md), so no script may read a folder name as a country code.
"""
import csv
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data"
_ROWS = None


def rows():
    global _ROWS
    if _ROWS is None:
        f = DATA / "countries.csv"
        _ROWS = list(csv.DictReader(open(f, encoding="utf-8", newline=""))) if f.exists() else []
    return _ROWS


def row(name):
    """The countries.csv row for a folder code, a slug or a path ending in either; None for a folder the file does not list."""
    n = Path(str(name)).name.lower()
    return next((r for r in rows() if r["folder"] == n), None) or next((r for r in rows() if r["slug"] == n), None)


def code(name):
    """The old folder code (fr, gb, australia), which the seat adapters are keyed by. An unlisted folder gives its first part."""
    r = row(name)
    return r["folder"] if r else Path(str(name)).name.split("-")[0].lower()


def iso(name):
    """The upper-case ISO code, as leads.csv and meta.json write it; EU, UN and AU for the supranational folders."""
    r = row(name)
    return (r["iso2"] or r["folder"].upper()) if r else Path(str(name)).name.split("-")[0].upper()


def folder(name):
    """The name of the folder that exists in data/ for this code or slug (the name itself if neither does)."""
    r = row(name)
    for n in (r["slug"], r["folder"]) if r else ():
        if (DATA / n).is_dir():
            return n
    return Path(str(name)).name


def flag(name):
    """The flag file's code, or '' for a folder with no flag (the African Union, global)."""
    r = row(name)
    return r["flag"] if r else ""


def supranational():
    """Both names of every supranational folder."""
    return {n for r in rows() if r["kind"] == "supranational" for n in (r["folder"], r["slug"])}
