# Russia

Read `data/ru/area_profile.md` and the most recent run log first. Russian `налог на богатство` (wealth tax), `налог на сверхбогатство` (super-wealth tax), and `солидарный налог на состояние` (solidarity wealth tax) are the primary terms. The phrase `налог на роскошь` (luxury tax) is widely used by both CPRF and A Just Russia – For Truth to refer to general taxes on luxury asset holdings and extreme fortunes; distinguish this from statutory vehicle transport tax luxury multipliers or progressive personal income tax (НДФЛ) brackets, which fall outside the wealth tax definition. A luxury tax on listed goods (yachts, jets, supercars, expensive property) is out too: count a speaker only when their own words name wealth or fortunes (`богатство`, `состояние`).

## Official document access

State Duma bill tracking and plenary transcripts are published on the State Duma legislative portal (СОЗД):
- Portal: `https://sozd.duma.gov.ru`
- Deputies directory (8th convocation): `http://duma.gov.ru/duma/deputies/8/`

Plenary transcripts record individual statements and faction positions on tax bills. Russian news agencies (TASS, RIA Novosti, Interfax) and official party websites (kprf.ru, spravedlivo.ru) frequently publish verbatim transcripts of legislative bill submissions and press conferences. Some Russian government and party portals implement anti-bot filtering against plain HTTP clients; when direct fetching fails, verify quotes using browser sessions or regional subdomains (e.g. `56.kprf.ru` or `moskva.spravedlivo.ru`).

## Parliamentary seats and parties

The State Duma has 450 seats elected every five years. The 8th convocation (elected September 2021) consists of:
- **United Russia** (`United Russia`, colour `#0054A5`): 324 seats
- **Communist Party of the Russian Federation** (`Communist Party of the Russian Federation`, colour `#D71A21`): 57 seats — sponsors a 1%–4% luxury-asset tax (not counted: it taxes listed luxury goods, not net wealth)
- **A Just Russia – For Truth** (`A Just Russia - For Truth`, colour `#F5B803`): 27 seats — advocates annual solidarity wealth tax modelled on the French ISF
- **Liberal Democratic Party of Russia** (`Liberal Democratic Party of Russia`, colour `#003399`): 21 seats
- **New People** (`New People`, colour `#00A896`): 13 seats
- **Other / Independent** (`Other`, colour `#888888`): 8 seats

`bodies.csv` registers the State Duma (`B0001`, national chamber, 450 seats). Sitting deputies supporting wealth taxation are linked via `positions.csv` with their official State Duma deputy ID (`member_ref`).

## Geography and map recipe

Boundary shapes are sourced from [geoBoundaries](https://www.geoboundaries.org/) under the Open Data Commons Open Database License (ODbL 1.0):
- **ADM1 (Federal Subjects)**: 83 regions (`geoBoundaries-RUS-ADM1.geojson`).
- **ADM2 (Raions and Urban Okrugs)**: 2,327 municipal districts (`geoBoundaries-RUS-ADM2.geojson`).

### Spatial Join & Hierarchy
Because ADM2 features contain boundary shapes but lack ADM1 parent IDs, perform a spatial containment join using Shapely (`STRtree`) against the ADM1 polygons to assign 100% of municipal units to their parent federal subject:
1. Load ADM1 polygons as index shapes.
2. Query each ADM2 polygon's representative point against the spatial tree. If disjoint due to boundary simplification or coastal slivers, resolve by maximum intersection area.
3. Assign the matched ADM1 `geo_unit_id` as `parent_id` in `data/ru/geo_units.csv`.

### Boundary Map Generation
Generate `boundaries.json` using `topo_to_boundaries.py`:
```bash
python skill/scripts/topo_to_boundaries.py \
  --units scratch/rus_adm2.geojson \
  --regions scratch/rus_adm1.geojson \
  --unit-code shapeID \
  --region-code shapeID \
  --licence ODbL-1.0 \
  --licence-url "https://opendatacommons.org/licenses/odbl/1-0/" \
  --simplify 0.05 \
  --out data/ru/boundaries.json
```
The resulting `data/ru/boundaries.json` (576 KB, 2,304 simplified paths) aligns cleanly with the 2,414 units in `data/ru/geo_units.csv` with 0 missing-map errors or warnings.
