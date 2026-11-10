# Paraguay (data/py)

- **Geography:** 18 regions (17 departamentos plus Distrito Capital Asunción, codes `PY00` to `PY17`) and 263 distritos / municipios (codes `PY0000` to `PY1704`) from the OCHA / HDX COD-AB Paraguay dataset (DGEEC / INE, CC BY-IGO). Run `topo_to_boundaries.py` on `pry_admin2.geojson` (`--project lonlat --scale 100 --simplify 0.2 --name-prop adm2_name --code-prop adm2_pcode`) for units, and on `pry_admin1.geojson` for regions, then merge with `merge_boundaries.py`.
- **Seats:** No automated API adapter. The Senado has 45 senators elected in a single nationwide constituency (`national_seat_roles` is `^Senador` in `meta.json`, so senators need no subnational constituency); the Cámara de Diputados has 80 deputies elected by department. Positions are recorded with `current` checked against official terms.
- **Sources that work:** `ultimahora.com`, `abc.com.py`, `lanacion.com.py`, `decidamos.org.py`, `latfem.org`, `revistaplus.com.py`, and `ods.congreso.gov.py`.
- **Wikidata:** `match_wikidata.py` has an entry for `PY` (`Q733`, languages `es`, `gn`, `en`).
