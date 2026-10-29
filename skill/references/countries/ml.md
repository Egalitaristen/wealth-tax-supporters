# Mali: 2 Grade A supporters identified across international and domestic presidential platforms

Worked notes from the Mali research passes (`R001` seed pass, `R002` wider discovery pass, 2026-10-29; 2 supporters, 8 documented exclusions, 16 broad queries logged).

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | Conseil National de la Transition (CNT), Gouvernement du Mali | Transitional legislative and executive organs in Bamako. |
| region | 19 regions and the District de Bamako | Official Institut Géographique du Mali (IGM) / OCHA COD-AB P-codes (`ML01`–`ML20`) in `code`. |
| council | 160 Cercles and urban communes | The local map tier, with official IGM / OCHA COD-AB P-codes (`ML0101`–`ML2006`) in `code`. Under the decentralized territorial administration, cercles and communes levy local development taxes (TDRL) and cannot enact a net wealth tax. |

**Map:** `data/ml/boundaries.json` uses the official administrative boundaries of Mali (Admin 1 regions + Bamako and Admin 2 cercles) from the Institut Géographique du Mali (IGM), distributed via the OCHA Common Operational Datasets on HDX (`https://data.humdata.org/dataset/cod-ab-mli`, package metadata at `https://data.humdata.org/api/3/action/package_show?id=cod-ab-mli`). Licence: `CC-BY-IGO-3.0` (`https://creativecommons.org/licenses/by/3.0/igo/legalcode`). Both `units` (160 cercles) and `regions` (20 regions) come from the same geodatabase / GeoJSON dataset, so region outlines fall cleanly on cercle borders.

## Identified supporters

1. **A0001: Moussa Mara** (`politician`, former Prime Minister of Mali 2014–2015, certified accountant, leader of Yéléma; Wikidata: `Q3326215`).
   - **Grade A** (`open_letter`, 2023-09-05).
   - Named signatory on the international open letter calling on G20 Heads of State to enact wealth taxes on extreme wealth (*G20 Leaders must tax extreme wealth*, hosted at `taxextremewealth.com/signatures`).
   - Verbatim quote: `Moussa Mara Former Prime Minister of Mali (ML)`

2. **A0002: Clément Dembélé** (`politician` / `academic`, 2018 presidential candidate, university professor, president of the Plateforme contre la corruption et le chômage - PCC; Wikidata: `Q96048074`).
   - **Grade A** (`interview`, 2018-01-17).
   - Explicit presidential campaign platform proposal to establish an Impôt de Solidarité sur la Fortune (ISF) in Mali targeting mining assets, high-value real estate, and financial bank deposits.
   - Published in *Bamada.net* / *Malijet*.
   - Verbatim quote: `Je mettrai en place l’ISF qui est l’Impôt de Solidarité sur la Fortune et qui sera basé sur la réalisation minière, immobilière et sur la déclaration des revenus dans les banques avec un petit prélèvement.`

## What worked and what to watch

- **Absence of general statutory net wealth tax:** Mali does not currently have an *impôt sur la fortune* (ISF) in its General Tax Code (*Code Général des Impôts*).
- **Resource sovereignty:** The national fiscal debate focuses on the mining sector (chiefly gold), where the government audited foreign multinationals (e.g. Barrick Gold), adopted the 2023 Mining Code to increase state and local participation up to 35%, and recovered substantial tax arrears.
- **Double taxation treaty termination:** In December 2023, Mali terminated its 1972 bilateral tax convention with France (effective March 2024), citing unequal terms that drained domestic revenues.
- **Ambiguous terms:** In UEMOA / Francophone West Africa, *impôt sur le patrimoine* almost always designates property tax (*impôt sur le patrimoine foncier* on built and unbuilt real estate), which is excluded under Section 2. *Zakat* in religious contexts is occasionally translated as "l'impôt sur la fortune" in Islamic jurisprudence, but is religious charity and not a statutory tax proposal.
- **Documented exclusions (8 actors in `exclusions.csv`):** Oumar Mariko (SADI, anti-mining rhetoric without wealth stock tax), Transitional Government (mining audits and treaty denunciation), PCQVP Mali (mining transparency), CAD-Mali (anti-debt and VAT equity), UNTM & CSTM (salary income tax ITS and living costs), Étienne Fakaba Sissoko (macroeconomics and public finance), Aminata Dramane Traoré (anti-imperialism), and the UN General Assembly Delegation (UN tax convention vote).
