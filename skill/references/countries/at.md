# Austria: a federal republic with an abolished wealth tax

A worked example of a federal republic where the net wealth tax was abolished in 1993, leaving high taxes on labor and near-zero taxes on net wealth. The debate is polarized around the SPÖ/ÖGB model championed by Andreas Babler and trade unions against the conservative ÖVP and far-right FPÖ.

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | Nationalrat (183 seats), Bundesrat (61 seats), Bundesregierung | The tax was federal law (*Vermögensteuergesetz 1954*), abolished effective 1 Jan 1994. Direct tax legislation is federal. |
| supranational | Austrian MEPs | Tracked in supranational EU register. |
| region | 9 *Bundesländer* (each with an elected *Landtag*) | ISO 3166-2 `AT-1` through `AT-9`. |
| council | 2,093 *Gemeinden* | Official 5-digit *Gemeindekennziffer* (GKZ) in `code`. The map tier rendered from Eurostat GISCO LAU 2024. |

## The boundary map

`data/at/boundaries.json` contains:
- 2,093 *Gemeinden* from Eurostat GISCO LAU 2024 (projected in lonlat with `--scale 100 --simplify 0.2`, CC-BY-4.0).
- 9 *Bundesländer* from Eurostat GISCO NUTS 2024 (NUTS 2).
- Validated via `wtdb.py validate` with `"boundaries": "boundaries.json"` declared in `meta.json`.

## The legislative seats adapter

The native `austria()` adapter in `skill/scripts/seats.py` queries the official open data JSON API of the Austrian Parliament:
- Endpoint: `https://www.parlament.gv.at/Filter/api/json/post?jsMode=EVAL&FBEZ=WFW_002&listeId=undefined&showAll=true&export=true`
- Body: `{"STEP": ["1000"], "NRBR": ["NR"], "GP": ["AKT"], "R_WF": ["FR"], "R_PBW": ["WK"], "M": ["M"], "W": ["W"]}`
- Returns all 183 sitting MPs of the 28th legislative period (elected 29 September 2024).
- Parties: FPÖ (57), ÖVP (51), SPÖ (41), NEOS (17), Grüne (16), Ohne Klub (1).
- Supporter position matching: maps sitting MPs (such as Julia Herr, Kai Jan Krainer, Barbara Teiber, Dr. Christoph Matznetter) to their person profiles on `parlament.gv.at`.

## Core political landscape & models

1. **SPÖ (Babler Model):**
   - Threshold: €1,000,000 net assets.
   - Slices: 0.5% (€1m–€10m), 1.0% (€10m–€50m), 2.0% (>€50m).
   - Allowance: Primary home (*Eigenheim*) exempt up to €1,500,000.
   - Yield: ~€5 billion/year, dedicated to reducing labor taxes and funding healthcare/education.
2. **Social Partnership (*Sozialpartnerschaft*):**
   - **ÖGB & Arbeiterkammer (AK):** Strong joint advocacy for 0.5%–1.5% wealth tax from €1m.
   - **Gewerkschaft GPA:** Active campaigns by Chairwoman Barbara Teiber.
3. **Left & Civil Society:**
   - **KPÖ:** Advocates progressive wealth taxation to fund municipal infrastructure.
   - **Attac Österreich & Momentum Institut:** Lead empirical modeling and grassroots advocacy.
   - **Wealthy Advocates:** Marlene Engelhorn (*taxmenow*, *Guter Rat für Rückverteilung*).

## Crucial Exclusions (Ground Rule 1)

- **Die Grünen (Werner Kogler):**
  - Campaign under *"Superreiche fair besteuern"*, but specifically limit their demand to an inheritance tax (*Erbschaftssteuer*) on *Millionenerbschaften* (>€1m).
  - Under Ground Rule 1, inheritance and gift tax alone is excluded unless accompanied by an annual net wealth tax. Classified as `out_of_definition`.

## Source repositories

- **Austrian Parliament:** `https://www.parlament.gv.at` (plenary protocols, motions, bills). Supports appending `?json=TRUE` to detail URLs.
- **APA-OTS:** `https://www.ots.at` (verbatim press declarations from political parties, unions, and NGOs). Note: newer pages store article text in JSON script tags; `wtdb._fetch_for_check` parses this text cleanly.
- **Official portals:** `spoe.at`, `oegb.at`, `arbeiterkammer.at`, `gpa.at`, `attac.at`, `momentum-institut.at`, `kpoe.at`.
