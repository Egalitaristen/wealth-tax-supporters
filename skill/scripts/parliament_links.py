#!/usr/bin/env python3
"""Add the website and social accounts that a parliament's own open data lists for its members.

Usage: python skill/scripts/parliament_links.py fr|br|ch [--dry-run]

The seat adapters (seats.py) store each member's id in positions.csv `member_ref`. Some parliaments publish, per member, the accounts the member
gave them, so these are the member's own and need no name check:
  fr  Assemblée nationale open data (deputies): "Site internet", Twitter, Facebook, Instagram and Linkedin addresses.
  br  Câmara dos Deputados API: urlWebsite and redeSocial.
  ch  Parlament.ch web service (PersonCommunication): Homepage, Facebook, Twitter, Instagram, LinkedIn.
(The Tweede Kamer's open data holds no website or account, and the other adapters were not checked.)

A link is added to profiles.csv (source names the parliament's data, checked today) unless the supporter already has a row for that platform or that
address. Every supporter with a member id gets a profile_checks.csv row (method parliament_page). Standard library only.
"""
import argparse, io, json, os, re, sys, time, urllib.request, zipfile
from datetime import date
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wtdb  # noqa: E402
import countries  # noqa: E402
import profile_scan as ps  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
UA = {"User-Agent": "WealthTaxSupportersBot/1.0 (+https://wealthtaxsupporters.com/about; reads a parliament's open data)"}
FR_ZIP = "https://data.assemblee-nationale.fr/static/openData/repository/17/amo/deputes_actifs_mandats_actifs_organes/AMO10_deputes_actifs_mandats_actifs_organes.json.zip"
FR_TYPES = {"Twitter": "x", "Facebook": "facebook", "Instagram": "instagram", "Linkedin": "linkedin", "Site internet": "website"}


def get(url, accept="application/json"):
    time.sleep(0.3)
    req = urllib.request.Request(url, headers={**UA, "Accept": accept})
    return urllib.request.urlopen(req, timeout=120).read()


def norm(platform, value):
    """A platform and an address from what the parliament wrote (a handle, a bare address or a full link)."""
    v = (value or "").strip()
    if not v:
        return None
    if " " in v and not v.startswith("http"):  # a display name, not an account
        return None
    if platform == "linkedin" and re.match(r"^/?(in|company)/", v):
        v = "https://www.linkedin.com/" + v.lstrip("/")
    if platform == "x" and not v.startswith("http"):
        v = "https://x.com/" + v.lstrip("@")
    if platform in ("facebook", "instagram", "linkedin") and not v.startswith("http"):
        v = {"facebook": "https://www.facebook.com/", "instagram": "https://www.instagram.com/", "linkedin": "https://www.linkedin.com/in/"}[platform] + v.lstrip("@")
    if platform == "website":
        if not v.startswith("http"):
            v = "https://" + v
        host = v.split("//", 1)[1].split("/", 1)[0].lower()
        if "." not in host or any(s in host for s in ("facebook.", "twitter.", "x.com", "instagram.", "youtube.", "linkedin.", "tiktok.")):
            return None
        return "website", v.replace("http://", "https://", 1)
    c = ps.classify(v)
    return (c[0], c[1]) if c and c[0] == platform else None


def france():
    z = zipfile.ZipFile(io.BytesIO(get(FR_ZIP)))
    out = {}
    for n in z.namelist():
        if "acteur/PA" not in n:
            continue
        a = json.loads(z.read(n))["acteur"]
        ad = (a.get("adresses") or {}).get("adresse") or []
        if isinstance(ad, dict):
            ad = [ad]
        links = []
        for x in ad:
            plat = FR_TYPES.get(x.get("typeLibelle"))
            if plat:
                r = norm(plat, x.get("valElec"))
                if r:
                    links.append(r)
        out[a["uid"]["#text"] if isinstance(a["uid"], dict) else a["uid"]] = links
    return out, "Assemblée nationale open data"


def brazil(refs):
    out = {}
    for ref in refs:
        try:
            d = json.loads(get(f"https://dadosabertos.camara.leg.br/api/v2/deputados/{ref}"))["dados"]
        except Exception:
            continue
        links = []
        if d.get("urlWebsite"):
            r = norm("website", d["urlWebsite"])
            if r:
                links.append(r)
        for u in d.get("redeSocial") or []:
            c = ps.classify(u)
            if c:
                links.append((c[0], c[1]))
        out[str(ref)] = links
    return out, "Câmara dos Deputados API"


CH_TYPES = {"homepage": "website", "website": "website", "facebook": "facebook", "twitter": "x", "x": "x", "instagram": "instagram", "linkedin": "linkedin"}


def switzerland(refs):
    out = {}
    for ref in refs:
        try:
            d = json.loads(get(f"https://ws.parlament.ch/odata.svc/PersonCommunication?$filter=PersonNumber%20eq%20{ref}%20and%20Language%20eq%20'DE'&$format=json"))["d"]
        except Exception:
            continue
        links = []
        for x in (d if isinstance(d, list) else d.get("results", [])):
            plat = CH_TYPES.get((x.get("CommunicationTypeText") or "").strip().lower())
            if plat:
                r = norm(plat, x.get("Address"))
                if r:
                    links.append(r)
        out[str(ref)] = links
    return out, "Parlament.ch web service"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("country", type=countries.code, choices=["fr", "br", "ch"], help="code or folder name")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    d = str(ROOT / "data" / countries.folder(a.country))
    positions = wtdb.load(d, "positions")
    ref_of = {}
    for p in positions:
        if p.get("member_ref"):
            ref_of.setdefault(p["actor_id"], p["member_ref"])
    data, label = france() if a.country == "fr" else brazil(sorted(set(ref_of.values()))) if a.country == "br" else switzerland(sorted(set(ref_of.values())))
    profiles, checks = wtdb.load(d, "profiles"), wtdb.load(d, "profile_checks")
    key = lambda u: re.sub(r"[^a-z0-9]", "", u.lower().split("//")[-1].replace("www.", "").replace("twitter.com", "x.com"))
    have = {(p["actor_id"], p["platform"]) for p in profiles}
    urls = {(p["actor_id"], key(p["url"])) for p in profiles}
    today = date.today().isoformat()
    added = gained = 0
    for aid, ref in ref_of.items():
        if ref not in data:
            continue
        new = []
        for plat, u in data[ref]:
            if (aid, plat) in have or (aid, key(u)) in urls:
                continue
            have.add((aid, plat)); urls.add((aid, key(u)))
            new.append(dict(actor_id=aid, platform=plat, url=u, source=f"{label} ({ref})", checked=today))
        added += len(new); gained += bool(new)
        if not a.dry_run:
            for n in new:
                profiles.append(dict(profile_id=wtdb.next_id(profiles, "profiles"), **n))
            checks.append(dict(check_id=wtdb.next_id(checks, "profile_checks"), actor_id=aid, method="parliament_page", url=f"{label} ({ref})", checked=today,
                               result="found" if new else "none", found=";".join(n["platform"] for n in new), note=""))
    print(f"{a.country}: {len(ref_of)} members with an id, {gained} gained links, {added} links added")
    if not a.dry_run:
        wtdb.save(d, "profiles", profiles)
        wtdb.save(d, "profile_checks", checks)


if __name__ == "__main__":
    sys.exit(main())
