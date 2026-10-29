# Mali: no domestic net wealth tax; fiscal debate focused on mining resource sovereignty, corporate exemptions, and French bilateral treaty termination

Worked notes from the Mali seed pass (`R001`, 2026-10-29; 0 supporters, 9 documented exclusions, 12 broad queries logged).

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | Conseil National de la Transition (CNT), Gouvernement du Mali | Transitional legislative and executive organs in Bamako. |
| region | 19 regions and the District de Bamako | Official Institut Géographique du Mali (IGM) / OCHA COD-AB P-codes (`ML01`–`ML20`) in `code`. |
| council | 160 Cercles and urban communes | The local map tier, with official IGM / OCHA COD-AB P-codes (`ML0101`–`ML2006`) in `code`. Under the decentralized territorial administration, cercles and communes levy local development taxes (TDRL) and cannot enact a net wealth tax. |

**Map:** `data/ml/boundaries.json` uses the official administrative boundaries of Mali (Admin 1 regions + Bamako and Admin 2 cercles) from the Institut Géographique du Mali (IGM), distributed via the OCHA Common Operational Datasets on HDX (`https://data.humdata.org/dataset/cod-ab-mli`, package metadata at `https://data.humdata.org/api/3/action/package_show?id=cod-ab-mli`). Licence: `CC-BY-IGO-3.0` (`https://creativecommons.org/licenses/by/3.0/igo/legalcode`). Both `units` (160 cercles) and `regions` (20 regions) come from the same geodatabase / GeoJSON dataset, so region outlines fall cleanly on cercle borders. Built with:

```bash
python skill/scripts/topo_to_boundaries.py .cache/mli_admin2.geojson \
  --project lonlat --scale 100 --simplify 0.5 --name-prop adm2_name --code-prop adm2_pcode \
  --licence "CC-BY-IGO-3.0" --licence-url "https://creativecommons.org/licenses/by/3.0/igo/legalcode" \
  --source "Mali Institut Geographique (IGM) via OCHA HDX" --code-scheme "IGM-PCODE" --out .cache/units.json

python skill/scripts/topo_to_boundaries.py .cache/mli_admin1.geojson \
  --project lonlat --scale 100 --simplify 0.5 --name-prop adm1_name --code-prop adm1_pcode \
  --licence "CC-BY-IGO-3.0" --licence-url "https://creativecommons.org/licenses/by/3.0/igo/legalcode" \
  --source "Mali Institut Geographique (IGM) via OCHA HDX" --code-scheme "IGM-PCODE" --out .cache/regions.json

python skill/scripts/merge_boundaries.py .cache/units.json --regions .cache/regions.json --out data/ml/boundaries.json
```

## What worked and what to watch

- **Absence of net wealth tax (ISF):** Mali has no general tax on net wealth (*impôt sur la fortune*), nor has any legislation for one been proposed in the transition legislature (CNT) or the previous National Assembly.
- **Resource sovereignty:** The national fiscal debate focuses on the mining sector (chiefly gold), where the government audited foreign multinationals (e.g. Barrick Gold), adopted the 2023 Mining Code to increase state and local participation up to 35%, and recovered substantial tax arrears.
- **Double taxation treaty termination:** In December 2023, Mali terminated its 1972 bilateral tax convention with France (effective March 2024), citing unequal terms that drained domestic revenues.
- **Ambiguous terms:** In UEMOA / Francophone West Africa, *impôt sur le patrimoine* almost always designates property tax (*impôt sur le patrimoine foncier* on built and unbuilt real estate), which is excluded under Section 2. *Zakat* in religious contexts is occasionally translated as "l'impôt sur la fortune" in Islamic jurisprudence, but is religious charity and not a statutory tax proposal.
- **Screened candidates:** Key screened figures include former Prime Minister Moussa Mara (declares personal assets, advocates expanding the tax base and curbing corporate exemptions), SADI leader Oumar Mariko (anti-imperialist rhetoric against mining multinationals), CAD-Mali and PCQVP Mali (mining transparency and debt cancellation campaigns), and trade unions UNTM/CSTM (focus on personal income tax on salaries and living costs). All are documented in `exclusions.csv` (`out_of_definition`).
