# Niger: 1 supporter identified; 20 documented exclusions

Worked notes from the Niger seed pass and follow-up passes (`R001`, `R002`, `R003`, `R004`, `R005`, 2026-11-10; 1 supporter, 20 documented exclusions, 42 broad queries logged across French, Hausa, and English).

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | Assemblée Nationale du Niger, Gouvernement de la République du Niger | Dissolved National Assembly and transitional executive in Niamey. |
| region | 8 regions: Agadez, Diffa, Dosso, Maradi, Niamey, Tahoua, Tillabéri, Zinder | Admin 1 official P-codes (`NE001`–`NE008`) in `code`. |
| county | 67 départements | Admin 2 official P-codes (`NE001001`–`NE008001`) in `code`. Deconcentrated administrative tier. |
| council | 266 communes | Admin 3 official P-codes (`NE001001001`–`NE008001005`) in `code`. The local municipal tier (communes urbaines and communes rurales) electing local councils. |

**Map:** `data/ne/boundaries.json` uses the official administrative boundaries of Niger from the Direction des Statistiques Démographiques et Sociales / Institut National de la Statistique (INS), distributed via OCHA Common Operational Datasets on HDX (`https://data.humdata.org/dataset/cod-ab-ner`). Licence: `CC-BY-IGO-3.0` (`https://creativecommons.org/licenses/by/3.0/igo/legalcode`). Both `units` (266 communes), `regions` (67 départements) and `regions_upper` (8 regions) come from the same dataset and coordinate system.

## What worked and what to watch

- **Supporter discovered:** Development economist and former diplomat **Mamadou Kiari Liman-Tinguiri** (`A0001`, Q18169961) explicitly proposed an *impôt direct universel* progressively taxing family net wealth (*patrimoine familial*) above the median with higher rates for the top decile, drawing on Thomas Piketty's capital taxation (*Niger Inter*, 19 October 2017; Grade A, `E00001`).
- **Absence of statutory net wealth tax:** Niger has never had an *impôt sur la fortune* (ISF). The *Code Général des Impôts* levies taxes on corporate profits (ISB), individual salaries (IUTS), VAT, registration duties on inheritance, and property taxes (Taxe Foncière Unique - TFU).
- **Ambiguous terms:** In UEMOA / Francophone West Africa, *impôt sur le patrimoine* refers to real estate taxes (*impôt sur le patrimoine foncier* on built and unbuilt property), which are excluded under Section 2. In Niger media (*Le Sahel*, *ActuNiger*), the acronym *ISF* refers to *Internationale Socialiste des Femmes* or the synthetic fertility index (*Indice Synthétique de Fécondité*). *Zakat* in Islamic commentary is sometimes translated as "l'impôt sur la fortune", but is religious charity and not a statutory tax proposal.
- **Resource sovereignty and civil society campaigns:** Fiscal debates in Niger center on uranium and oil exploitation concessions (Areva/Orano negotiations, Agadem basin pipeline). Protests against the 2018 budget led by civil society coalitions (ROTAB, Alternative Espaces Citoyens, MPCR, Tournons la Page Niger) targeted regressive indirect taxes (housing tax, utilities) and corporate exemptions rather than demanding an annual net wealth tax.
- **Fonds de Solidarité pour la Sauvegarde de la Patrie (FSSP):** Established following the July 2023 coup d'état; funded by a 1% compulsory deduction on monthly net salaries, corporate turnover levies on strategic enterprises, and luxury import duties. Turnover and payroll taxes are excluded from the wealth tax definition.
- **Bilateral tax treaty:** In December 2023, Niger and Mali denounced their bilateral double-taxation conventions with France to restore domestic taxing rights over corporate service fees and royalties.
- **Regional AES leads:** Neighboring Burkina Faso engaged ATAF to study wealth tax feasibility; logged as external lead `L0042` in `data/leads.csv`.
- **Documented exclusions (20 actors in `exclusions.csv`):**
  1. UN General Assembly Delegation (UN tax convention vote; `X0001`)
  2. Ali Idrissa / ROTAB & PCQVP (extractive transparency and anti-Finance Law 2018; `X0002`)
  3. Moussa Tchangari / AEC (anti-austerity and public services; `X0003`)
  4. CNSP / FSSP (salary deductions and turnover levies; `X0004`)
  5. Government of Niger (bilateral tax treaty denunciation; `X0005`)
  6. CDTN / Idrissa Djibrilla (salary tax ITS reduction; `X0006`)
  7. PNDS-Tarayya / Bazoum & Issoufou (land tax reforms; `X0007`)
  8. Hama Amadou (deceased former Prime Minister; `X0008`)
  9. Association Islamique du Niger / Conseil Islamique (religious zakat vs secular taxes; `X0009`)
  10. CESOC (tax compliance and certified invoicing; `X0010`)
  11. Ibrahim Assane Mayaki / FACTI Panel (illicit financial flows and corporate minimum taxes; `X0011`)
  12. Oumarou Moumouni Dogari / Ville de Niamey (municipal waste and market fees; `X0012`)
  13. Nouhou Arzika / MPCR (cost-of-living and anti-2018 budget; `X0013`)
  14. Maïkoul Zodi / Tournons la Page Niger (fiscal justice, multinational tax exemptions; `X0014`)
  15. Moustapha Kadi Oumani / CODDAE (civic tax duty and energy royalties; `X0015`)
  16. Adamou Louché Ibrahim / Analyste Économique (universal basic income, public spending quality; `X0016`)
  17. Hassoumi Massoudou / Former Minister of Finance (ruled out wealth taxes in 2018 budget; `X0017`)
  18. Dr. Ahmat Jidoud / Former Minister of Finance (digitalisation and property tax reforms; `X0018`)
  19. Ali Mahaman Lamine Zeine / Transitional Prime Minister & Finance Minister (sanctions resilience and basic goods tax relief; `X0019`)
  20. Haute Autorité du Waqf / HAW (Islamic charitable endowments and tax exemptions; `X0020`).
