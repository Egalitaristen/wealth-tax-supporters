# Uganda (data/ug)

Seed pass R001 (2026-11-13). Check that URLs still resolve before relying on them.

- **Geography:** 4 regions (`UG1`...`UG4`) and 135 districts (`UG3064`...) from the OCHA COD-AB Uganda layers (valid 2020-08-24, CC BY-IGO 3.0), via the HDX API (`package_show?id=cod-ab-uga`); the geojson zip (37 MB) downloads with a plain GET. Recipe: `topo_to_boundaries.py uga_admin2.geojson --name-prop adm2_name --code-prop adm2_pcode --project lonlat --scale 120 --simplify 0.35`, admin1 as regions, then `merge_boundaries.py`. The layer has 135 districts; Uganda has more today, and the 203 counties of admin 3 are not loaded.
- **Seats:** `bodies.csv` B0001 is the 12th Parliament (529 members) from the Rio Times guide that cites the Electoral Commission's report; the Commission's own table and the Gazette notice (General Notice No. 171 of 2026) were not read. Uganda is not in `seats.py`.
- **Wealth tax status:** none in force. The 2015 URA high-net-worth unit and the Oxfam/SEATINI "taxing the rich" papers are income and property compliance, not a wealth tax. The Fair Tax Monitor reports call property, land and capital gains taxes "wealth taxes" (excluded).
- **What exists:** URA Commissioner General Musinguzi (testimony, June 2020), Oxfam in Uganda and SEATINI (February 2022), Akina Mama wa Afrika (2023 primer). No bill, motion or poll.
- **Sources that work:** chimpreports.com, uganda.oxfam.org, seatiniuganda.org, maketaxfair.net PDFs, bills.parliament.ug PDFs, allafrica.com. **Blocked or refusing scripts:** monitor.co.ug and pmldaily.com (bot check; Wayback copy used for PML), ugandaradionetwork.net (403), akinamamawaafrika.org (SSL handshake failure; Wayback copy used).
- **Watch out:** "high net worth individuals" in Ugandan papers means income-tax compliance; "wealth taxes" in the Fair Tax Monitor means property and capital gains.
