# Bulgaria: flat 10% income tax, no wealth tax, thin support

Seed pass R001 (2026-11-04). The debate is about replacing the flat income tax with a progressive one, which is out of definition. Support found: KNSB and Podkrepa unions (asset-based "данък богатство" proposals, 2017 to 2026) and Socialist MEPs on two European Parliament roll calls (10 May and 12 Dec 2023).

| Level | Units | Notes |
|---|---|---|
| national | Narodno sabranie, 240 seats, 52nd assembly | Open data: `parliament.bg/api/v1/coll-list/bg/2` (groups), `/api/v1/coll-list-ns/bg` (members with group and constituency). Bills and transcripts are a JS app. No adapter in `seats.py`; bodies, seats and positions were written by hand from these endpoints. |
| region | 28 oblasti | Eurostat GISCO NUTS 2024 level 3 codes (BG311 ...). |
| council | 265 obshtini | Eurostat GISCO LAU 2024; codes are NSI municipality codes (`PER32`). |

**Map:** `data/bg/boundaries.json` from GISCO `LAU_RG_01M_2024_4326.geojson` and `NUTS_RG_01M_2024_4326_LEVL_3.geojson` (keep `CNTR_CODE=BG`, add `code` from `GISCO_ID`), `topo_to_boundaries.py --project lonlat --scale 100 --simplify 0.2`, then `merge_boundaries.py`. Licence CC BY 4.0, credit "© European Union, 1995-today; © EuroGeographics".

**Sources:** capital.bg answers 403 to scripts and is not read. europarl.europa.eu answers an empty 202 to scripts; the Wayback copies of the roll-call PDFs read fine and `checkquotes` skips them. Roll-call rows quote the surname as printed in the affirmative list.

**Left out:** BSP progressive income tax bills; Podkrepa's 0.5% tax is graded C because it is aimed at owners of several properties (property-only risk).
