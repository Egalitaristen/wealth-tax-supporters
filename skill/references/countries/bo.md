# Bolivia (data/bo)

- **Geography:** 9 departamentos, 112 provincias and 339 municipios from the OCHA / HDX COD-AB Bolivia GeoJSON (GeoBolivia, valid 2024-09-16, CC BY-IGO); codes are the OCHA P-codes (`BO` plus the INE codes). Run `topo_to_boundaries.py` three times (`bol_admin3.geojson` with `adm3_name` and `adm3_pcode`, then `bol_admin2.geojson` and `bol_admin1.geojson`; `--project lonlat --scale 100 --simplify 0.2`) and merge with `merge_boundaries.py units.json --regions prov.json --upper dep.json`.
- **Seats:** no adapter. The Chamber of Deputies and the Senate member lists were not read, so no seat chart and no positions.
- **Sources that work:** eju.tv, correodelsur.com, lanacion.com.py, the Oxfam en Bolivia site and impuestos.gob.bo. Lexivox carries Ley 1357; the Gaceta Oficial was not read.
- **Wikidata:** `match_wikidata.py` has an entry for `BO`.
