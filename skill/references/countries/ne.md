# Niger: 0 supporters identified; 8 documented exclusions

Worked notes from the Niger seed pass (`R001`, 2026-11-10; 8 documented exclusions, 15 broad queries logged across French, Hausa, and English).

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | Assemblée Nationale du Niger, Gouvernement de la République du Niger | Dissolved National Assembly and transitional executive in Niamey. |
| region | 8 regions: Agadez, Diffa, Dosso, Maradi, Niamey, Tahoua, Tillabéri, Zinder | Admin 1 official P-codes (`NE001`–`NE008`) in `code`. |
| county | 67 départements | Admin 2 official P-codes (`NE001001`–`NE008001`) in `code`. Deconcentrated administrative tier. |
| council | 266 communes | Admin 3 official P-codes (`NE001001001`–`NE008001005`) in `code`. The local municipal tier (communes urbaines and communes rurales) electing local councils. |

**Map:** `data/ne/boundaries.json` uses the official administrative boundaries of Niger from the Direction des Statistiques Démographiques et Sociales / Institut National de la Statistique (INS), distributed via OCHA Common Operational Datasets on HDX (`https://data.humdata.org/dataset/cod-ab-ner`). Licence: `CC-BY-IGO-3.0` (`https://creativecommons.org/licenses/by/3.0/igo/legalcode`). Both `units` (266 communes), `regions` (67 départements) and `regions_upper` (8 regions) come from the same dataset and coordinate system.

## What worked and what to watch

- **Absence of statutory net wealth tax:** Niger has never had an *impôt sur la fortune* (ISF). The *Code Général des Impôts* levies taxes on corporate profits (ISB), individual salaries (IUTS), VAT, registration duties on inheritance, and property taxes (Taxe Foncière Unique - TFU).
- **Ambiguous terms:** In UEMOA / Francophone West Africa, *impôt sur le patrimoine* refers to real estate taxes (*impôt sur le patrimoine foncier* on built and unbuilt property), which are excluded under Section 2. In Niger media (*Le Sahel*), the acronym *ISF* refers to *Internationale Socialiste des Femmes* or the synthetic fertility index (*Indice Synthétique de Fécondité*). *Zakat* in Islamic commentary is sometimes translated as "l'impôt sur la fortune", but is religious charity and not a statutory tax proposal.
- **Resource sovereignty:** Fiscal debates in Niger center on uranium and oil exploitation concessions (Areva/Orano negotiations, Agadem basin pipeline).
- **Fonds de Solidarité pour la Sauvegarde de la Patrie (FSSP):** Established following the July 2023 coup d'état; funded by a 1% compulsory deduction on monthly net salaries, corporate turnover levies on strategic enterprises, and luxury import duties. Turnover and payroll taxes are excluded from the wealth tax definition.
- **Bilateral tax treaty:** In December 2023, Niger and Mali denounced their bilateral double-taxation conventions with France to restore domestic taxing rights over corporate service fees and royalties.
- **Documented exclusions (8 actors in `exclusions.csv`):** UN General Assembly Delegation (UN tax convention vote; `X0001`), Ali Idrissa / ROTAB & PCQVP (extractive transparency and anti-Finance Law 2018; `X0002`), Moussa Tchangari / AEC (anti-austerity and public services; `X0003`), CNSP / FSSP (salary deductions and turnover levies; `X0004`), Government of Niger (bilateral tax treaty denunciation; `X0005`), CDTN / Idrissa Djibrilla (salary tax ITS reduction; `X0006`), PNDS-Tarayya / Bazoum & Issoufou (land tax reforms; `X0007`), and Hama Amadou (deceased former Prime Minister; `X0008`).
