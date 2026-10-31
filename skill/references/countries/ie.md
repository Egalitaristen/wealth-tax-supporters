# Ireland: Oireachtas records, a 31-authority map and the parties that back a net wealth tax

Ireland has no net wealth tax today (the Parliamentary Budget Office's 2024 overview says so), so support comes from opposition parties, trade unions, think tanks and a long run of independent TDs and senators. Search terms: `wealth tax`, `net wealth tax`, `wealth levy`, `tax on super wealth`, and the Irish `cáin rachmais`. Capital gains tax, capital acquisitions (inheritance) tax, property tax and "tax the rich" on their own do not count (`skill/SKILL.md` section 2). The register's story is in `data/ie/area_profile.md` and the run log in `data/ie/runs.csv` (R001 to R008); read both before a new run.

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | Houses of the Oireachtas: Dáil Éireann (174 seats) and Seanad Éireann (60) | Dáil constituencies and the Seanad panels are place text, not map units. |
| council | 31 statutory local authorities | The map tier. `geo_units.csv` uses Tailte Éireann's `BDY_ID` as `code` (for example `15001` for Carlow County Council). |

Sampling of the local authorities (Dublin City, Cork City, Galway City, Limerick, South Dublin) has not started, and nothing in the local tier should be read as swept.

## Map

`data/ie/boundaries.json` comes from Tailte Éireann's *Local Authorities, National Statutory Boundaries, Ungeneralised, 2026* ([data.gov.ie](https://data.gov.ie/dataset/local-authorities-national-statutory-boundaries-ungeneralised-20261)), licence CC BY 4.0, generalised and projected for display. Units are matched by the 5-digit `BDY_ID` (`--code-prop BDY_ID`), the code scheme is "Tailte Éireann BDY_ID (local authority boundary ID, 2026)", and the source line says the shapes were generalised here and are not Tailte Éireann's work or endorsement. Rebuild with `skill/scripts/topo_to_boundaries.py` (shapefile or TopoJSON in, `--licence CC-BY-4.0`, `--licence-url https://creativecommons.org/licenses/by/4.0/`).

## Where the records are, and what blocks scripts

- **Debates and bills:** the website `oireachtas.ie` shows a human-verification wall to scripts, so a debate page often returns no text. The same records are published as open data at `data.oireachtas.ie` (for example `debateRecord/seanad/2023-12-12/debate/mul@/main.pdf`) and through the API at `api.oireachtas.ie`. Prefer those, and quote only what the file shows.
- **Members:** `api.oireachtas.ie/v1/members?house_no=34&chamber=dail` (and `seanad`) gives each member's party, constituency or panel and dates.
- **Parties and bodies:** Labour, the Social Democrats, People Before Profit–Solidarity, Sinn Féin and the Green Party publish their positions on their own sites; Oxfam Ireland, the Irish Congress of Trade Unions (ICTU), NERI and TASC publish their papers as PDFs.

## Seats

`python skill/scripts/seats.py data/ie` (adapter `ireland`) reads both houses from the Oireachtas members API and sets each supporter's current or former status. Run it with `--fix-status` after a general election or a by-election, read what it prints, and check the supporters it lists: a name-only match may be a spelling difference (`Seán` and `Sean`, `Ó` and `O`). The register has position rows for every listed politician; 12 of them were current when it was last run.

## What counted and what did not

- **Counted:** a named net-wealth-tax design (Social Democrats' 0.5% above €1m, 1% above €2m and 2% above €5m; Labour's targeted tax; People Before Profit's progressive rates; the Green Party's tax on assets over €10m; ICTU's tax above €1m), formal motions and amendments with thresholds, a one-off 1% solidarity levy, signed opinion pieces, NERI's and Oxfam Ireland's costed proposals.
- **Left out:** Financial Justice Ireland and Social Justice Ireland (educational or conditional, not a clear endorsement), the 2011 Siobhán O'Donoghue campaign article (kept as a lead: the accessible page gives only the month), proposals for capital acquisitions (inheritance) tax or property tax alone.
- **Same name, different person:** Stephen Kinsella in the Irish register is the University of Limerick economist, not the UK campaigner of the same name.

## What a later run should do

1. Seek named union-affiliate leaders and signed opinion or academic pieces, using primary pages and not search snippets.
2. Continue the Oireachtas records beyond the independent and Civil Engagement groups, keeping only people whose own words or formal motions back an actual wealth tax.
3. Give each TD a constituency from the members API instead of the country root.
4. Sample the five largest authorities' council records before deciding on a wider local sweep.
5. Add Wikidata ids (only 1 of 46 actors has one; see issue #128).
