# Serbia: no wealth tax, thin support

Seed pass R001 (2026-11-13). 5 supporters, 5 evidence rows, none above grade B. No wealth tax exists or has been tabled; the debate is about the income tax on high earners (*porez na bogate*), the property tax and inheritance tax, which are out of definition. Folder `data/rs` (Suriname is `sr`).

| Level | Units | Notes |
|---|---|---|
| national | Narodna skupština, 250 seats | Seats from the final results of the 25 October 2026 election (Radio Free Europe, 5 to 6 Nov 2026). `rik.parlament.gov.rs` results are a script-driven portal and return nothing to plain clients. No adapter in `seats.py`; bodies and seats were written by hand. No members listed until the new convocation confirms mandates. |
| region | 4 statistical regions (NUTS 2) and 25 districts (NUTS 3) | Eurostat GISCO NUTS 2024; codes `RS11`, `RS110`... Names are English forms of the Serbian names (GISCO gives Cyrillic). |
| council | 168 municipalities and city municipalities | Eurostat GISCO LAU 2024; code `RS_<Statistical Office number>`. Belgrade (17) and Niš (5) appear as city municipalities; the file has fewer than the 174 local governments. Kosovo excluded. |

**Map:** `data/rs/boundaries.json` from `LAU_RG_01M_2024_4326.geojson` and `NUTS_RG_01M_2024_4326_LEVL_3` / `LEVL_2` (keep `CNTR_CODE=RS`; code from `GISCO_ID` or `NUTS_ID`; the district parent of a unit is the NUTS 3 polygon that holds its `representative_point`), `topo_to_boundaries.py --project lonlat --scale 100 --simplify 0.2`, then `merge_boundaries.py units.json --regions districts.json --upper regions.json`. Licence CC BY 4.0, credit "© European Union, 1995-today; © EuroGeographics".

**Sources that work:** Danas, N1, Vreme, Biznis.rs, 021.rs, RFE, nedavimobeograd.rs and zelenolevifront.rs answer plain clients. The ZLF programme PDF loses č, š and ž in `pdftotext`; quote from the HTML page. Naslovi.net carries Beta wire texts (its canonical URL has the date). `parlament.gov.rs` lists bills as PDFs per convocation.

**Quirks:** *porez na imovinu* is the municipal property tax; *porez na bogate* is an income tax. The Student List is a list of independents, not a party. Tamara Milenković Kerković left Dveri in 2024.
