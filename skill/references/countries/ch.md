# Switzerland: a wealth tax that exists in every canton, and a federal debate about adding one

Notes from the seed pass (R001, October 2026). Check that URLs still work before relying on them.

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | Federal Assembly: National Council (200), Council of States (46); Federal Council | There is no federal wealth tax; federal motions ask for a new constitutional basis (Art. 128) |
| region | 26 cantons, `code` = ISO 3166-2 (`CH-ZH`), names in English (Zurich, Lucerne, Geneva, Graubünden) | Cantons and communes levy the wealth tax, so cantonal initiatives and parliaments matter |
| council | 2,110 municipalities, `code` = BFS municipality number, parented to the canton | The map tier. Districts (Bezirke) are skipped: not general-purpose government and absent in several cantons. BFS canton numbers (1 to 26) collide with municipality numbers, which is why cantons use ISO codes |

**Register source:** the BFS Historised Municipality Directory, `https://www.agvchapp.bfs.admin.ch/api/communes/snapshot?date=01-10-2026&format=csv` (Windows-1252; `Level` 1 cantons, 2 districts, 3 municipalities). Municipalities merge every year; take a new snapshot before an update and compare with the shapes (the 2026-01 shapes matched all 2,110 numbers).

**Map:** `data/ch/boundaries.json` uses swisstopo swissBOUNDARIES3D, release `2026-01` (`https://data.geo.admin.ch/ch.swisstopo.swissboundaries3d/swissboundaries3d_2026-01/swissboundaries3d_2026-01_2056_5728.shp.zip`, 36 MB). Licence: swisstopo's OGD terms (free use, processing and commercial use allowed, source reference "Bundesamt für Landestopografie swisstopo" mandatory); `validate` warns that it does not know this licence name. The `swiss-maps` TopoJSON on GitHub is **not** usable: its data comes from BFS GEOSTAT under a non-commercial licence. Build: from `TLM_HOHEITSGEBIET` keep `OBJEKTART=Gemeindegebiet`, `ICC=CH` and `BFS_NUMMER<9000` (the 9xxx numbers are lakes); the shapefile is PolygonZ, so write a plain 2D copy first (pyshp, drop the Z), then `topo_to_boundaries.py com.shp --name-prop NAME --code-prop BFS --scale 0.002 --flip-y --simplify 0.4`. Cantons come the same way from `TLM_KANTONSGEBIET` with codes `CH-<ISO>` (`KANTONSNUM` mapped to the ISO letters), and `merge_boundaries.py mun.json --regions kt.json`. Result: 2,110 units, 26 regions, 520 KB.

## Sources that work

- **Swiss Parliament open data** (`https://ws.parlament.ch/odata.svc/`): the best source in the country. Send `Accept: application/json` and use `$filter`; `$select` only with real field names (a wrong name returns 400). `Business` has the motion text (`SubmittedText`), `Vote` lists a business's recorded votes with `IdSession`, and `Voting` has every member's `Decision` (1 Ja, 2 Nein, others abstain or absent) for an `IdVote`; `MemberCouncil` gives party, canton, council, join and leave dates and `DateOfDeath`. Responses are paged: add `$top` (200 is enough for a chamber). The per-vote `Voting` URL and the `Business(ID=...,Language='DE')` URL are readable by `wtdb.py checkquotes`; Curia Vista pages are not (JavaScript).
- **SRF** and **zentralplus** answer plain clients. **Blick** answers 403 to a plain client. **al-zh.ch** gzips its pages even when not asked (`wtdb.py checkquotes` now decompresses them).
- Cantonal official sites: Geneva's Grand Conseil texts are PDFs (`ge.ch/grandconseil/data/texte/IN00185.pdf`; the file is text with Windows-1252 accents, so `pdftotext` output needs `errors='ignore'` or cp1252). A Neuchâtel PDF with a space in its path (`D_Init_ FiscPlusEquitable.pdf`) came back as a corrupt file.

## Wealth tax debate in short

See `data/ch/area_profile.md` section 2. Two things to keep in mind when searching: the headline fights of 2025 (the Juso inheritance-tax initiative) are **outside** the definition, and "Vermögenssteuer" often means the cantonal tax that already exists, so support for keeping it or raising it is `defend_existing` or `annual_net_wealth`. Federal motions by the left (20.3174, 20.3203, 23.3361) gave 83 yes-voting members in three votes; only SP and Green members voted yes.

## Terms

German: Vermögenssteuer · Vermögensabgabe · Solidaritätsabgabe · Millionärssteuer · Reichensteuer (check). French: impôt sur la fortune · contribution de solidarité sur les grandes fortunes. Italian: imposta sulla sostanza · imposta patrimoniale. Not in the definition: Erbschaftssteuer / impôt sur les successions, Pauschalbesteuerung (lump-sum taxation of wealthy foreigners), 99%-Initiative (capital income).

## Seats

`python skill/scripts/seats.py data/ch` (adapter `ch`) reads `MemberCouncil` with `Active eq true` from the Parliament's OData service: 200 National Council and 46 Council of States members with party and canton, giving both chambers a Seats tab. The Greens' count includes the Alternative-die Grünen member from Zug. Run it again after each election (October 2027), by-election and run that adds politicians. Federal Councillors (`Council` 99) are not charted.
