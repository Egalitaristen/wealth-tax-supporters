# Geography register

This file holds section 6.7 of the skill. `skill/SKILL.md` keeps the section numbers as pointers to this file, so a reference such as "SKILL.md 6.7a" still finds it. Section numbers in the text below refer to the same numbering.

### 6.7 Geography register
A tree of the places you will report on, in `geo_units.csv`, with a country root and `parent_id` set (section 5).

**Every country uses the same depth: the register and the map go down to the lowest tier of general-purpose local government, with the regions or states above it as parents.** That keeps countries comparable and lets a visitor find supporters near them. Today:

| Country | Regions (parents) | Local tier (map units) |
|---|---|---|
| United Kingdom | nations and English regions, counties | 361 local authority districts (GSS codes) |
| Sweden | 21 län | 290 kommuner (kommunkod) |
| Germany | 16 Länder, 401 Kreise and kreisfreie Städte | 10,939 Gemeinden and unincorporated areas (AGS, BKG VG250) |
| India | 36 states and union territories (ISO 3166-2:IN) | 734 districts (LGD codes; Survey of India shapes) |
| United States | 50 states and DC | 3,143 counties and equivalents (FIPS) |
| Brazil | 26 states and the Federal District (IBGE codes) | 5,571 municípios (IBGE codes) |
| France | 13 regions (ISO 3166-2:FR), 101 départements | 34,920 communes (INSEE, COG 2025) |
| Netherlands | 12 provinces (CBS PV codes) | 342 gemeenten (CBS GM codes, PDOK Gebiedsindelingen 2026, CC BY 4.0) |
| Spain | 17 autonomous communities and 2 autonomous cities (ISO 3166-2:ES), 52 provinces (INE) | 8,132 municipios (INE) |

For a new country, pick the tier that elects a council and runs local services (municipalities, districts or counties), not wards or parishes. Take that tier even when it runs to tens of thousands of units (France's 35,000 communes): an official list loads in one command, a generalised shape file (a few MB) draws fine, and the site needs no change. Supporters still sit at whatever level the evidence shows (a deputy in the département, a mayor in the commune); areas below a level with supporters get a faint tint graded by how many are known there. Give the regions a different code system from the units when the official ones overlap (INE numbers both Spanish provinces and communities from 01): use ISO 3166-2 for the regions, since `validate` rejects duplicate codes. Fetch the **official current list** with codes (a statistics office, mapping agency or interior ministry), not memory, and build `boundaries.json` from the same agency's shapes where possible, so codes match. **Check the licence before you download anything** (map licence rule, section 5): an unlicensed map has to be thrown away later, and so does the work built on it.

Loading the local tier is not a promise to sweep it: sweeping stays proportionate to what the sample finds (6.5), and unswept units stay `pending`. Place each actor at the finest unit the source shows (a mayor in the city's unit, a state legislator in the state). Finer places you meet are not lost: put them in `location` as place text after the last unit (`United States > California > Ventura County > Camarillo`). On the map, areas with their own supporters are shaded, and areas whose region only has supporters at region level get a light tint. Seats are places, not institutions: an MP belongs to the constituency, a US representative to the district. Roll calls rarely print the constituency, so look it up in bulk: Wikidata records it as the qualifier *electoral district* (P768) on the member's *position held* (P39) statement, one SPARQL query for the whole list. `validate` warns about legislators left at the country root. For a map, also build `boundaries.json` (see `scripts/topo_to_boundaries.py`).
