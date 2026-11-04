# Hungary: a wealth tax passing from opposition bills to government policy

No net wealth tax exists. Párbeszéd tabled bills in 2023 and 2025; the Tisza party that won the April 2026 election pledged a 1% tax on wealth above HUF 1bn (1.5% above HUF 100bn in the October 2026 draft, from 1 January 2027). Check every URL still works before relying on it.

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | Országgyűlés, Government | |
| supranational | Hungarian MEPs | recorded in this register, seats in `data/eu` |
| region | 20 counties (vármegye, incl. Budapest) | NUTS 3 code (HU110 ...) in `code` |
| council | 3,155 settlements (település) | KSH settlement code (5 digits) in `code`; parent = county by the Eurostat LAU-NUTS table |

**Map:** `data/hu/boundaries.json` from Eurostat GISCO LAU 2024 and NUTS 2024 (CC BY 4.0, credit "© European Union, 1995-today"). Recipe: download `lau/geojson/LAU_RG_01M_2024_4326.geojson`, `nuts/geojson/NUTS_RG_01M_2024_4326_LEVL_3.geojson` and Eurostat's correspondence workbook `EU-27-LAU-2024-NUTS-2024.xlsx` (sheet HU: NUTS 3, LAU code, name); join on `GISCO_ID = HU_<code>`; `topo_to_boundaries.py --project lonlat --scale 100 --simplify 0.2` for units and regions, then `merge_boundaries.py`.

## Sources

- Works: 444.hu, telex.hu, index.hu, vg.hu, penzcentrum.hu, property-forum.eu; Wayback `id_` copies of parlament.hu PDFs (`web.archive.org/web/2025id_/https://www.parlament.hu/irom42/12722/12722.pdf`; the plain `/web/2025/` form returns a wrapper page that `checkquotes` cannot read); howtheyvote.eu for EP votes.
- Blocked (not bypassed): parlament.hu (CAPTCHA), eur-lex, europarl.europa.eu; adozona.hu returned a bot page.
- Bill cover pages print "Benyújtó" (submitter): quote the member's own entry.
- `match_wikidata.py` has no Hungary entry; QIDs were looked up by hand.

## Seats

No adapter: parlament.hu blocks scripts, so there is no Seats tab and Párbeszéd MPs' positions have `current` blank. Add an adapter in `seats.py` when a readable official list exists. EP: all four Hungarian members who voted FOR in 2023 have left the Parliament (checked against the open data portal's current list).

## What counts

- Counts: bill submitters, party and government announcements with rate and threshold, EP roll-call FOR votes.
- Left out: the 2020 levy on receipts of state money; business federations' comments on the draft design; Klára Dobrev (no vote).
