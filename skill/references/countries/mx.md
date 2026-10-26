# Mexico: geography and map recipe

## Register and boundary source

Use INEGI's [Catálogo Único web service](https://www.inegi.org.mx/servicios/catalogounico.html), not a third-party map with undocumented codes. The catalogue and geometries were fetched on 25 October 2026. The geometry response identifies its source as **INEGI, Marco Geoestadístico, diciembre de 2025**; its population attributes refer to the 2020 census and are not a boundary date.

- `https://gaia.inegi.org.mx/wscatgeo/v2/mgee/`: tabular list of the 32 federal entities, with two-digit `cvegeo` / `cve_ent` codes and `nomgeo` names.
- `https://gaia.inegi.org.mx/wscatgeo/v2/mgem/01` (repeat for the returned entity codes): current municipality/alcaldía catalogue. Preserve the five-digit `cvegeo` as a string, including leading zeros. `cve_ent` identifies its state parent.
- `https://gaia.inegi.org.mx/wscatgeo/v2/geo/mgem/01` (repeat for each entity): municipality GeoJSON; names/codes are `properties.nomgeo` and `properties.cvegeo`.
- `https://gaia.inegi.org.mx/wscatgeo/v2/geo/mgee`: state GeoJSON, with the same name/code properties.

This fetch returned **2,478 municipalities/alcaldías**, all with shapes, and **32 state outlines**. The register has 2,511 rows including the national root. Municipality codes match the shape codes exactly, with no extras, missing shapes or duplicate codes. The 16 Ciudad de México units are `alcaldia`; other local units are `municipality`. State parents use `level=region`, local units `level=council`. Loading a unit does not mean it has been searched: leave its sweep status pending until research actually occurs.

## Licence

INEGI's [Términos de Libre Uso](https://www.inegi.org.mx/inegi/terminos.html) permit copying, publication, adaptation, extraction and commercial exploitation, with attribution and notice of transformations. The map therefore records:

- `licence`: `INEGI Términos de Libre Uso`
- `licence_url`: `https://www.inegi.org.mx/inegi/terminos.html`
- `code_scheme`: `INEGI clave geoestadística: two-digit AGEE and five-digit AGEM`
- `source`: attribution to INEGI's December 2025 Marco Geoestadístico, retrieval date, and an explanation that projection/simplification are this project's transformations, without INEGI endorsement.

This is an explicit open government licence, even if a validator does not recognise its name. Do not substitute GADM or unlicensed personal map repositories.

## Build recipe

Keep downloaded GeoJSON and temporary scripts outside the repository. Fetch the 32 entity lists, 32 municipal geometry collections and state geometry collection; combine the municipal features into one FeatureCollection. Build the register from the tabular catalogue, rather than deriving names or codes from memory.

The saved map uses the existing `topo_to_boundaries.py` geometry/simplification logic with a **shared projection for both tiers**: longitude multiplied by `cos((minimum latitude + maximum latitude)/2)`, latitude negated, both scaled by 100 and rounded to integers, and Douglas–Peucker tolerance 0.65 output units. Compute those extrema across both municipal and state features so their outlines align. Preserve each polygon ring, and encode the resulting paths with the helper's `M`/relative-`l`/`z` format. Put local paths in `units`, state paths in `regions`, and set `match=code`. No inset or geographic shift is applied.

An equivalent way to use the CLI is to concatenate municipal and state features into one GeoJSON, run `topo_to_boundaries.py --project lonlat --scale 100 --simplify 0.65 --name-prop nomgeo --code-prop cvegeo` with the licence/source fields above, then split the output by code length: five-digit codes into `units`, two-digit codes into `regions`. Retain the shared viewBox.

QA on the initial map: all 2,478 local paths and 32 region paths nonempty; exact code match to the register; no duplicate local codes; full-country raster preview inspected for extent and obvious geometry problems. The resulting `boundaries.json` is approximately 989 KiB. Set `meta.json`'s `boundaries` to `boundaries.json`.

## Seats

`python skill/scripts/seats.py data/mx` charts the Cámara de Diputados (500) and the Senado (128) for the LXVI Legislatura. The official lists (`sitl.diputados.gob.mx`, `diputados.gob.mx`, `senado.gob.mx`) time out or answer 403 to scripts, and some of them to a browser on the same network, so the adapter reads the English Wikipedia article "LXVI Legislature of the Mexican Congress", whose lists show each seat's current holder and mark substitutions ("A (until date) B (since date)"). That is a secondary source and the chamber notes say so. When the official lists can be read (or saved from a browser and passed with `--local URL=FILE`), replace the adapter's source and keep the party names. Wikipedia's article titles can be shorter than the name the register uses: add an alias in the adapter (Amalia García is one) and confirm a name-only match.
