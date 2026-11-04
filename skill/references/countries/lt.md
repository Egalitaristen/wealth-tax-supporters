# Lithuania: no net-wealth tax, thin register

A first-pass guide (seed, 2026-11-04). Lithuania has a property tax (the 2021 'turto mokestis' on high-value real estate, replaced by a new law from 2026) and no net-wealth tax, so the register is thin: four former and sitting MEPs who voted for the 2023 EU wealth-tax amendment.

## Geography

10 apskritys (ISO 3166-2 LT-xx, equal to NUTS 3) over 60 savivaldybės. Both from Eurostat GISCO (LAU 2024 and NUTS 2024 level 3 GeoJSON, e.g. `distribution/v2/lau/geojson/LAU_RG_01M_2024_4326.geojson`, CC BY 4.0), filtered by `CNTR_CODE`; each municipality is placed in its county by a shapely `representative_point` test. Shapes: `topo_to_boundaries.py --project lonlat --scale 100 --simplify 0.2` for units and regions, then `merge_boundaries.py`.

## Sources that worked and blocked

- europarl.europa.eu roll-call PDFs refuse scripts; the Wayback copy (`web.archive.org/web/<ts>id_/<url>`) works.
- ERR (err.ee, news.err.ee) pages read with plain curl; the date is in `article:published_time`.
- Search engines return mostly property-tax and income-tax material; check every hit against the definition.

## Exclusions to remember

See `data/lt/exclusions.csv` and `data/lt/leads.csv`: progressive income tax, inheritance tax, property tax and (Estonia) company asset tax are out of definition.
