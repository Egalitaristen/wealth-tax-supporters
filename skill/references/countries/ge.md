# Georgia: no wealth tax, no supporter found

Seed pass R001 (2026-11-13). 0 supporters, 6 exclusions. Folder `data/ge` (the US state would be `us-ga`). No wealth tax exists and none has been tabled; the debates are about a progressive income tax (article 94 of the constitution bars tax rises without a referendum), the property tax and tax relief for offshore assets. Check that URLs still resolve before relying on them.

| Level | Units | Notes |
|---|---|---|
| national | Parliament of Georgia (`B0001`), 150 seats | Seats by list from the CEC count of 26 October 2024 as Interpressnews reported it on 27 October 2024 (89 / 18 / 17 / 14 / 12). The opposition lists boycotted the chamber; later reports say Georgian Dream voted to revoke mandates. parliament.ge was not read, so no member is listed. No adapter in `seats.py`. |
| region | 10 regions (Adjara is an autonomous republic) | OCHA COD-AB admin level 1, codes `GE15`, `GE23`... |
| council | 70 municipalities and self-governing cities, Tbilisi, Abkhazia and the South Ossetia "Provisional Administration" | OCHA admin level 2 (`GE3823`...); Tbilisi (`GE11`), Abkhazia (`GE12`) and the Provisional Administration (`GE48`) exist only at level 1 and are placed directly under the root. |

**Map:** `data/ge/boundaries.json` from OCHA / HDX "Georgia - Subnational Administrative Boundaries" (COD-AB, CC BY-IGO 3.0, valid to 2024-01-31), OCHA P-codes. The GeoJSON files come from `geo_admin_boundaries.geojson.zip` on the dataset page. Recipe: merge `geo_admin2` plus the three level-1 features `GE11`, `GE12`, `GE48` into one unit file (`name`, `code` properties), keep the other ten level-1 features as regions, then

```bash
C="--project lonlat --scale 120 --simplify 0.3 --licence CC-BY-IGO-3.0 --licence-url https://creativecommons.org/licenses/by/3.0/igo/ --code-scheme 'OCHA COD-AB P-codes' --source 'OCHA / HDX Georgia Subnational Administrative Boundaries (COD-AB, CC BY-IGO)'"
python skill/scripts/topo_to_boundaries.py units_in.geojson --name-prop name --code-prop code $C --out units.json
python skill/scripts/topo_to_boundaries.py regs_in.geojson --name-prop name --code-prop code $C --out regs.json
python skill/scripts/merge_boundaries.py units.json --regions regs.json --out data/ge/boundaries.json
```

**Sources that work:** civil.ge, oc-media.org, jam-news.net, interpressnews.ge, jacobin.com and constitutionnet.org answer plain clients. The GTUC site (gtuc.ge) was under maintenance on the manifesto page.

**Quirks:** *ქონების გადასახადი* is the property tax, not a wealth tax. Article 94 is the constitutional tax-rise limit; arguments for lifting it are about progressive income tax. `ge` is Georgia the country; the US state belongs under `us-ga`.
