"""Build Greece's map from Andreadis' Cleisthenes shapefile and the ELSTAT register.

Usage: python scripts/build_gr_boundaries.py path/to/cleisthenes.shp
Requires pyshp and shapely. The source dataset and licence are documented in data/gr/area_profile.md.
"""
import collections
import csv
import json
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

import shapefile
from shapely.geometry import mapping, shape
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[1]
MANUAL = {
    '9025': 'ELSTAT-M0803', '9108': 'ELSTAT-M2405', '9164': 'ELSTAT-M2707',
    '9184': 'ELSTAT-M4706', '9191': 'ELSTAT-M4506', '9193': 'ELSTAT-M4508',
    '9204': 'ELSTAT-M5104', '9211': 'ELSTAT-M5201', '9292': 'ELSTAT-M6702',
    '9170': 'ELSTAT-M4604', '9305': 'ELSTAT-M7101',
}


def normalized(name):
    name = unicodedata.normalize('NFD', name.casefold())
    return ''.join(c for c in name if unicodedata.category(c) != 'Mn' and c.isalnum()).removeprefix('δημοσ')


def main(source):
    with (ROOT / 'data/gr/geo_units.csv').open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    by_id = {r['geo_unit_id']: r for r in rows}
    municipalities = [r for r in rows if r['unit_type'] == 'municipality']
    by_code = {r['code']: r for r in municipalities}
    by_name = collections.defaultdict(list)
    for row in municipalities:
        by_name[normalized(row['name'])].append(row)
    units, areas, regions, used = [], collections.defaultdict(list), collections.defaultdict(list), set()
    for sr in shapefile.Reader(source, encoding='utf_8').iterShapeRecords():
        code, name = sr.record
        if name == 'Άθως':
            continue  # Mount Athos is autonomous, not a municipality.
        candidates = by_name[normalized(name)]
        row = by_code[MANUAL[code]] if code in MANUAL else candidates[0] if len(candidates) == 1 else None
        if not row or row['code'] in used:
            raise ValueError(f'Unmatched or duplicate municipality: {code} {name}')
        used.add(row['code'])
        geometry = shape(sr.shape.__geo_interface__)
        if not geometry.is_valid:
            geometry = geometry.buffer(0)
        units.append({'type': 'Feature', 'properties': {'name': row['name'], 'code': row['code']}, 'geometry': mapping(geometry)})
        area = by_id[row['parent_id']]
        region = by_id[area['parent_id']]
        areas[area['geo_unit_id']].append(geometry)
        regions[region['geo_unit_id']].append(geometry)
    if used != set(by_code):
        raise ValueError(f'Register municipalities missing from map: {set(by_code) - used}')
    def dissolved(groups):
        return [{'type': 'Feature', 'properties': {'name': by_id[k]['name'], 'code': by_id[k]['code']},
                 'geometry': mapping(unary_union(v))} for k, v in groups.items()]
    with tempfile.TemporaryDirectory() as folder:
        temp = Path(folder)
        for name, features in [('units', units), ('areas', dissolved(areas)), ('regions', dissolved(regions))]:
            (temp / f'{name}.geojson').write_text(json.dumps({'type': 'FeatureCollection', 'features': features}, ensure_ascii=False), encoding='utf-8')
            cmd = [sys.executable, str(ROOT / 'skill/scripts/topo_to_boundaries.py'), str(temp / f'{name}.geojson'),
                   '--name-prop', 'name', '--code-prop', 'code', '--scale', '0.002', '--flip-y', '--simplify', '0.15',
                   '--licence', 'CC-BY-4.0', '--licence-url', 'https://creativecommons.org/licenses/by/4.0/', '--out', str(temp / f'{name}.json')]
            if name == 'units':
                cmd += ['--source', 'Municipality boundaries: Ioannis Andreadis, Aristotle University of Thessaloniki, HEAL-Link; derived from geodata.gov.gr (CC BY 3.0). Regions dissolved from municipalities.',
                        '--code-scheme', 'ELSTAT municipality codes, matched by municipality name to 2026 administrative register']
            subprocess.run(cmd, check=True)
        subprocess.run([sys.executable, str(ROOT / 'skill/scripts/merge_boundaries.py'), str(temp / 'units.json'),
                        '--regions', str(temp / 'areas.json'), '--upper', str(temp / 'regions.json'),
                        '--out', str(ROOT / 'data/gr/boundaries.json')], check=True)
    print(f'Matched {len(used)} municipalities, {len(areas)} regional units and {len(regions)} regions.')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(sys.argv[1])
