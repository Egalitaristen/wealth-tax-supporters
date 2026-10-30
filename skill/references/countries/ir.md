# Iran (data/ir)

## Geography and map boundaries

`data/ir/boundaries.json` is generated from the authoritative United Nations Office for the Coordination of Humanitarian Affairs (UN OCHA) Common Operational Dataset on Administrative Boundaries (COD-AB) for the Islamic Republic of Iran:
- **Source:** UN OCHA / Humanitarian Data Exchange (HDX), `irn_admin_boundaries.geojson.zip` and `irn_admin_boundaries.xlsx`.
- **License:** Creative Commons Attribution for Intergovernmental Organisations (CC BY-IGO / CC-BY-3.0-IGO).
- **Administrative Tiers:**
  - `regions` (ADM1): 31 Provinces (*ostān*), e.g. Tehran, Isfahan, Fars, East Azerbaijan, Razavi Khorasan.
  - `units` (ADM2): 429 Counties (*shahrestān*).
- **Projection & Conversion:** Cleaned, reprojected, simplified, and transformed into the standard repository TopoJSON topology format via `skill/scripts/topo_to_boundaries.py` with bounding box `[44.0327, 25.0782, 63.3167, 39.782]`.
- **Geo Units Register:** `data/ir/geo_units.csv` contains 462 rows (G0001 country root `Iran`, G0002 national chamber `Islamic Consultative Assembly`, G0003–G0033 31 provinces, and G0034–G0462 429 counties).

## Network and domain access notes

Domestic `.ir` government domains (including the Majlis Research Center `rc.majlis.ir` and certain state agencies) employ domestic IP whitelisting or drop external SSL handshakes from non-Iranian IP addresses. Research on Iranian parliamentary records and economic policy should rely on open national news agencies and academic portals:
- *ILNA* (`ilna.ir`) — Open, no bot blocks.
- *Tabnak* (`tabnak.ir`) — Open, comprehensive parliamentary and economic coverage.
- *Donya-e-Eqtesad* (`donya-e-eqtesad.com`) — Open, Iran's primary economic daily.
- *Quarterly Journal of Applied Economics Studies, Iran* (`aes.basu.ac.ir`) — Bu-Ali Sina University, open academic publication of empirical tax studies.
- *Fararu* (`fararu.com`) & *Tejarat News* (`tejaratnews.com`) — Open economic commentary and analysis.

## Wealth tax debate context

1. **Direct Taxes Reform (2012–2013):** The Majlis Economic Commission under Arsalan Fathi-Pour drafted an aggregate net wealth tax on movable and immovable assets exceeding 2 billion tomans at a rate of 0.2%, zero-rated for productive enterprise.
2. **Exclusion of Single-Asset Luxury Taxes:** Note that Band 'Ayn' Note 6 of recent annual budget laws levies annual property tax on luxury houses and luxury vehicles. Under Section 2 of `SKILL.md`, single-asset excise taxes (real estate alone or vehicles alone) are excluded unless part of a comprehensive net wealth tax.
3. **Piketty Wealth Tax Framework:** Peer-reviewed academic studies (e.g. Saadatmehr & Bazgir 2023 in *Applied Economics Studies*) have empirically verified that net wealth taxation significantly reduces the Gini coefficient in Iran and advocated broad-based wealth taxation following Thomas Piketty's theory.
