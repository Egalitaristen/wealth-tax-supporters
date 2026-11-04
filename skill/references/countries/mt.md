# Malta: research guide

Malta has no wealth tax and neither Labour nor the Nationalist Party backs one; the first pass (R001) found the Greens (ADPD) and little else. See `data/mt/area_profile.md` and `runs.csv`.

## Geography and map
68 local councils, codes ISO 3166-2:MT (`MT-01` to `MT-68`), under the country root; no region tier. The map is geoBoundaries gbOpen MLT ADM1 (d-maps.com 2022, public domain), converted with `skill/scripts/topo_to_boundaries.py --project lonlat --code-prop shapeISO`. The source's names are garbled (UTF-8 read as Latin-1) and it gives Mġarr the code of Mellieħa; `boundaries.json` and `geo_units.csv` use the ISO names and MT-31 for Mġarr. A national statistics office layer would be better if an open licence is found. Gozo (14 councils) could become a parent unit.

## Search terms
taxxa fuq il-ġid, taxxa fuq ir-rikkezza, wealth tax, billionaire tax. "Ġid" also appears in asset-declaration stories.

## Sources
- Works: adpd.mt, newsbook.com.mt, thinkmagazine.mt, maltatoday.com.mt, um.edu.mt/library/oar (dissertations).
- Blocks scripts: independent.com.mt (403). Not tried: timesofmalta.com, parliament.mt Hansard.

## Seats
No adapter. No supporter sits in the House today (ADPD has no seat), so there is no Seats tab. If a supporter is elected, write a `malta` adapter in `seats.py` from the parliament.mt member list.

## What counted and what did not
- Counted: ADPD's own budget and tax statements (C), Ralph Cassar's named support for the Greens/EFA wealth tax study (B).
- Left out: Charmaine Portelli (mixed THINK interview), Momentum's economic platform (no wealth tax found).

## A later run should
Open the Malta Independent piece in a browser; read Momentum, Graffitti, GWU and UHM budget submissions; search Hansard and ADPD manifestos 2022 and 2026; check MEPs.
