# Czechia: a unitary republic with high labor taxation and zero net wealth tax

A worked example of a Central European unitary republic with heavy reliance on labor and indirect taxes and an almost negligible property/wealth tax contribution (<1.5% of tax revenue). The wealth tax debate is championed primarily by the extra-parliamentary center-left (SOCDEM) and greens (Strana zelených), academic tax researchers (Tax Justice Network / Charles University), trade union confederation (ČMKOS), progressive Pirates in the European Parliament, and isolated wealth managers.

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | Poslanecká sněmovna (200 seats), Senát (81 seats), Vláda ČR | Direct tax legislation is exclusively national. Subnational units have no legislative tax autonomy beyond setting property tax multipliers. |
| supranational | Czech MEPs (21 seats) | Tracked in the supranational European Parliament register. |
| region | 14 *Kraje* (Higher territorial self-governing units) | ISO 3166-2 `CZ-10` through `CZ-80` (NUTS 3). |
| council | 6,258 *Obce* (Municipalities) | Official 6-digit ČSÚ municipal codes in `code`. The map tier rendered from Eurostat GISCO LAU 2024. |

## The boundary map

`data/cz/boundaries.json` contains:
- 6,258 *Obce* from Eurostat GISCO LAU 2024 (projected in lonlat with `--scale 100 --simplify 0.2`, CC-BY-4.0).
- 14 *Kraje* from Eurostat GISCO NUTS 2024 (NUTS 3).
- Validated via `wtdb.py validate` with `"boundaries": "boundaries.json"` declared in `meta.json`.

## The legislative seats adapter

The native `czechia()` adapter in `skill/scripts/seats.py` queries the official open register of the Chamber of Deputies (*Poslanecká sněmovna*):
- Endpoint: `https://www.psp.cz/sqw/snem.sqw?P1=0&P2=0`
- Encoded in `windows-1250`.
- Returns all 200 sitting MPs of the 9th legislative period.
- Parliamentary clubs (as of October 2026): ANO 2011 (80), ODS (27), STAN (22), Piráti (18), KDU-ČSL (16), SPD (15), Motoristé sobě (13), TOP 09 (9).
- Supporter position matching: maps sitting MPs to `psp.cz` detail pages (`detail.sqw?id=...`). Sitting MP Gabriela Svárovská (`id=7049`, co-chair of Strana zelených) matches 1 seat in Poslanecká sněmovna.

## Core political landscape & models

1. **Strana zelených / Palanský Model (2024–2026):**
   - Threshold: 111,000,000 CZK (~€4.4 million) net wealth.
   - Rate: 3.5% annually; progressive alternatives modeled from 33m and 68m CZK.
   - Yield: ~58 billion CZK (~€2.3 billion) annually from ~4,200 wealthy individuals.
   - Authored by economist Dr. Miroslav Palanský (Tax Justice Network / Charles University); championed by Johanna Nejedlová, Michal Berg, and party co-chairs Matěj Pomahač and Gabriela Svárovská (sitting MP in Poslanecká sněmovna).
2. **SOCDEM (formerly ČSSD) Model (2021 & 2023):**
   - Threshold: 100,000,000 CZK (~€4 million) net wealth.
   - Rate: 1.0% annually.
   - Championed in the 2021 manifesto by former Labour Minister Jana Maláčová and articulated in 2023 by former Prime Minister Vladimír Špidla.
3. **Budoucnost & Levice (Progressive Parties):**
   - Extra-parliamentary progressive movement *Budoucnost* and democratic socialist party *Levice* explicitly incorporate wealth taxation into their platforms to shift the fiscal burden away from labor.
4. **Trade Unions (ČMKOS):**
   - Led by Josef Středula; continuous advocacy for increasing taxes on capital and accumulated wealth (*zdanění majetku a kapitálu*) to fund public services and infrastructure.
5. **European Parliament Roll Calls:**
   - Pirate Party MEPs (Markéta Gregorová, Marcel Kolaja, Mikuláš Peksa) voted FOR European wealth tax amendments on EU own resources in May 2023 (vote 155121) and December 2023 (vote 162327).
6. **Business Commentators:**
   - Mikuláš Splítek (portfolio manager at Erste Asset Management) published a prominent 2025 column in *Hospodářské noviny* calling for progressive wealth taxation to prevent runaway compound wealth inequality.

## Crucial Exclusions (Ground Rule 1)

- **Jakub Michálek & Zdeněk Hřib (Piráti):**
  - Advocated taxing capital gains on share sales exceeding 40 million CZK, vacant apartment property taxes (*daň z prázdného bytu*), and windfall corporate taxes, but expressly not an annual net wealth tax. Classified as `out_of_definition`.
- **KSČM & Kateřina Konečná (Stačilo!):**
  - Propose progressive corporate/income taxes, sectoral bank taxes, and taxing vacant apartments, but no recurring tax on total net personal wealth. Classified as `out_of_definition`.
- **Petr Janský (Charles University / Centrum veřejných financí):**
  - Author of *Chytřejší daně* / 17 recommendations for tax reform. In policy analysis, uses *majetkové daně* to refer exclusively to the real estate property tax (*daň z nemovitých věcí*) and inheritance/wealth transfer taxes, not an annual net wealth tax. Classified as `out_of_definition`.
- **Danuše Nerudová (MEP, STAN) & Filip Pertold (CERGE-EI / IDEA):**
  - Nerudová's advocacy focuses on bringing Czech real estate property taxes closer to OECD averages. Pertold explicitly cautions against net wealth taxes due to mobile capital flight, arguing instead for personal income tax bracket progression. Both classified as `out_of_definition`.
- **Tomáš Tožička (Tax Justice Network Czechia / Social Watch):**
  - Focuses on tax transparency, corporate anti-haven rules, and financial transaction taxes, rather than domestic net wealth taxation. Classified as `out_of_definition`.
- **Vít Samek (former Vice-President of ČMKOS):**
  - Prominently advocated taxing accumulated wealth and capital on television panels, but passed away in January 2025. Classified as `deceased` under Ground Rule 2 (living figures only).
