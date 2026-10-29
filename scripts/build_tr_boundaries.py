"""Build Turkey's geo_units.csv and boundaries.json.

Source dataset: UN OCHA COD-AB-TUR on HDX (https://data.humdata.org/dataset/cod-ab-tur),
distributed under Creative Commons Attribution for Intergovernmental Organisations (CC BY-IGO).
Standardized TopoJSON and tabular data via ttezer/turkiye-harita-verisi.
"""
import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "brain/scratch/turkey_geo"

def build_geo_units():
    provinces_csv = SRC_DIR / "provinces.csv"
    districts_csv = SRC_DIR / "districts.csv"

    with open(provinces_csv, "r", encoding="utf-8-sig") as f:
        provinces = list(csv.DictReader(f))

    with open(districts_csv, "r", encoding="utf-8-sig") as f:
        districts = list(csv.DictReader(f))

    rows = []
    # 1. Country root
    rows.append({
        "geo_unit_id": "G0001",
        "name": "Turkey",
        "level": "national",
        "unit_type": "country",
        "parent_id": "",
        "website": "https://www.turkiye.gov.tr",
        "sweep_status": "in_progress",
        "swept_run": "R001",
        "swept_date": "2026-10-29",
        "queries_run": "",
        "hits": "",
        "notes": "National seed pass across TBMM, parties, DİSK, KESK, civil society, economists and media.",
        "code": "TR"
    })

    # 2. National legislature
    rows.append({
        "geo_unit_id": "G0002",
        "name": "Grand National Assembly of Turkey",
        "level": "national",
        "unit_type": "legislature",
        "parent_id": "G0001",
        "website": "https://www.tbmm.gov.tr",
        "sweep_status": "in_progress",
        "swept_run": "R001",
        "swept_date": "2026-10-29",
        "queries_run": "",
        "hits": "",
        "notes": "Türkiye Büyük Millet Meclisi (TBMM). 600 seats.",
        "code": ""
    })

    gid = 3
    prov_id_to_gid = {}
    # Sort provinces by plate_code
    provinces.sort(key=lambda p: int(p["plate_code"]))

    for p in provinces:
        unit_id = f"G{gid:04d}"
        prov_id_to_gid[p["id"]] = unit_id
        iso_code = p["iso_3166_2"]  # TR-01 to TR-81
        rows.append({
            "geo_unit_id": unit_id,
            "name": p["name"],
            "level": "region",
            "unit_type": "province",
            "parent_id": "G0001",
            "website": "",
            "sweep_status": "in_progress" if p["name"] in ["İstanbul", "Ankara", "İzmir"] else "pending",
            "swept_run": "R001" if p["name"] in ["İstanbul", "Ankara", "İzmir"] else "",
            "swept_date": "2026-10-29" if p["name"] in ["İstanbul", "Ankara", "İzmir"] else "",
            "queries_run": "",
            "hits": "",
            "notes": f"Province of Turkey ({p['name']}). ISO 3166-2:TR code {iso_code}.",
            "code": iso_code
        })
        gid += 1

    # Districts sorted by parent plate_code and district_local_code
    districts.sort(key=lambda d: (int(d["plate_code"]), d["district_local_code"]))

    for d in districts:
        unit_id = f"G{gid:04d}"
        parent_gid = prov_id_to_gid[d["parent_id"]]
        rows.append({
            "geo_unit_id": unit_id,
            "name": d["name"],
            "level": "council",
            "unit_type": "district",
            "parent_id": parent_gid,
            "website": "",
            "sweep_status": "pending",
            "swept_run": "",
            "swept_date": "",
            "queries_run": "",
            "hits": "",
            "notes": f"District in {d['parent_name']}.",
            "code": d["id"]  # TR-D-XX-YYY
        })
        gid += 1

    fieldnames = [
        "geo_unit_id", "name", "level", "unit_type", "parent_id",
        "website", "sweep_status", "swept_run", "swept_date",
        "queries_run", "hits", "notes", "code"
    ]

    out_path = ROOT / "data/tr/geo_units.csv"
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} geo units to {out_path}")


def prepare_topojson():
    # Enrich districts.topojson and provinces.topojson with names and correct codes
    provinces_csv = SRC_DIR / "provinces.csv"
    districts_csv = SRC_DIR / "districts.csv"

    with open(provinces_csv, "r", encoding="utf-8-sig") as f:
        p_map = {r["id"]: r for r in csv.DictReader(f)}

    with open(districts_csv, "r", encoding="utf-8-sig") as f:
        d_map = {r["id"]: r for r in csv.DictReader(f)}

    # 1. Districts
    with open(SRC_DIR / "districts.topojson", "r", encoding="utf-8") as f:
        d_topo = json.load(f)

    for g in d_topo["objects"]["districts"]["geometries"]:
        gid = g["properties"]["id"]
        if gid in d_map:
            g["properties"]["name"] = d_map[gid]["name"]
            g["properties"]["code"] = gid
            g["id"] = gid

    enriched_d = SRC_DIR / "districts_named.topojson"
    with open(enriched_d, "w", encoding="utf-8") as f:
        json.dump(d_topo, f)

    # 2. Provinces
    with open(SRC_DIR / "provinces.topojson", "r", encoding="utf-8") as f:
        p_topo = json.load(f)

    for g in p_topo["objects"]["provinces"]["geometries"]:
        gid = g["properties"]["id"]
        if gid in p_map:
            g["properties"]["name"] = p_map[gid]["name"]
            iso_code = p_map[gid]["iso_3166_2"]
            g["properties"]["code"] = iso_code
            g["id"] = iso_code

    enriched_p = SRC_DIR / "provinces_named.topojson"
    with open(enriched_p, "w", encoding="utf-8") as f:
        json.dump(p_topo, f)

    print("Enriched TopoJSON files prepared.")


def build_boundaries():
    enriched_d = SRC_DIR / "districts_named.topojson"
    enriched_p = SRC_DIR / "provinces_named.topojson"
    mun_out = SRC_DIR / "mun.json"
    prov_out = SRC_DIR / "prov.json"
    final_out = ROOT / "data/tr/boundaries.json"

    # Step 1: units (districts)
    cmd_mun = [
        sys.executable, str(ROOT / "skill/scripts/topo_to_boundaries.py"),
        str(enriched_d),
        "--object", "districts",
        "--name-prop", "name",
        "--code-prop", "code",
        "--project", "lonlat",
        "--scale", "100",
        "--simplify", "0.5",
        "--licence", "CC-BY-IGO",
        "--licence-url", "https://data.humdata.org/dataset/cod-ab-tur",
        "--code-scheme", "OCHA/HDX COD-AB-TUR district P-codes",
        "--source", "UN OCHA COD-AB-TUR via HDX, CC BY-IGO",
        "--out", str(mun_out)
    ]
    print("Running topo_to_boundaries for districts...")
    subprocess.run(cmd_mun, check=True)

    # Step 2: regions (provinces)
    cmd_prov = [
        sys.executable, str(ROOT / "skill/scripts/topo_to_boundaries.py"),
        str(enriched_p),
        "--object", "provinces",
        "--name-prop", "name",
        "--code-prop", "code",
        "--project", "lonlat",
        "--scale", "100",
        "--simplify", "0.5",
        "--licence", "CC-BY-IGO",
        "--licence-url", "https://data.humdata.org/dataset/cod-ab-tur",
        "--code-scheme", "ISO 3166-2:TR",
        "--source", "UN OCHA COD-AB-TUR via HDX, CC BY-IGO",
        "--out", str(prov_out)
    ]
    print("Running topo_to_boundaries for provinces...")
    subprocess.run(cmd_prov, check=True)

    # Step 3: merge
    cmd_merge = [
        sys.executable, str(ROOT / "skill/scripts/merge_boundaries.py"),
        str(mun_out),
        "--regions", str(prov_out),
        "--out", str(final_out)
    ]
    print("Merging boundaries...")
    subprocess.run(cmd_merge, check=True)
    print(f"Boundaries written to {final_out} ({final_out.stat().st_size} bytes)")


if __name__ == "__main__":
    build_geo_units()
    prepare_topojson()
    build_boundaries()
