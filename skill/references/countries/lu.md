# Luxembourg research guide

## Geography and map
12 cantons (LAU1 codes, written `LU-01` to `LU-12` here) and 100 communes (LAU2 codes). Source: Administration du cadastre et de la topographie, "Limites administratives du Grand-Duché de Luxembourg" on data.public.lu (CC0), file `limadmin.geojson` (layers `communes` and `cantons`, updated 2026-10-05) and the commune list `commune-canton-district-circonscription-arrondissements.csv`. Communes were merged by code and simplified with shapely `coverage_simplify` (0.0003 degrees); canton outlines are the union of the simplified communes; then `topo_to_boundaries.py --project lonlat --scale 6000` and `merge_boundaries.py --code-prefix LU-`.

## Sources
- chd.lu has a register of motions (`/de/motion_resolution/<id>`), questions and dossiers; deposit documents are often scanned images (read with OCR). Motion pages print vote totals, not member votes.
- The personal impôt sur la fortune ended with 2006; what remains (companies only) is out of the definition.
- Party positions in 2023: the Tageblatt comparison (orbilu.uni.lu 10993/57950) and Paperjam's "How the parties feel about tax reform". The KPL programme is a text PDF on kommunisten.lu.
- `seats.py` has no Luxembourg adapter yet.
