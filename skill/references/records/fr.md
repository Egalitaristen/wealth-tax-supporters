# France: where the official record is and how to read it

Guide to French parliamentary and government records on wealth taxation. For the seat-chart adapter see [references/countries/fr.md](../countries/fr.md); for scope and run notes see `data/fr/area_profile.md`.

## 1. Bills, motions and proposals

- **Assemblée nationale — Dossiers législatifs & textes**: `https://www.assemblee-nationale.fr/dyn/17/dossiers` (17th legislature, July 2024–) and `/dyn/16/dossiers` (16th legislature, 2022–2024). Bill PDFs follow `https://www.assemblee-nationale.fr/dyn/<leg>/textes/l<leg>b<num4>_proposition-loi.pdf` (e.g. `l17b0768_proposition-loi.pdf`) or `/17/pdf/propositions/pion<num4>.pdf`. Amendments follow `https://www.assemblee-nationale.fr/dyn/17/amendements/<dossier>/AN/<num>.pdf`.
- **Sénat — Dossiers législatifs & amendements**: `https://www.senat.fr/dossier-legislatif/<slug>.html` (e.g. `pjlf2026.html`, `pjlf2027.html`). Individual amendments follow `https://www.senat.fr/amendements/<session>/<bill_num>/Amdt_<num>.html` (e.g. `2025-2026/138/Amdt_I-643.html`).
- **Search terms (French)**: `impôt plancher`, `taxe Zucman`, `impôt sur la fortune`, `impôt de solidarité sur la fortune` (ISF), `impôt sur la très grande fortune`, `contribution exceptionnelle sur le patrimoine`, `ultrariches`, `patrimoine net`. Watch out for `IFI` (*impôt sur la fortune immobilière*, real estate only — excluded) and `CDHR` (*contribution différentielle sur les hauts revenus*, income tax — excluded).
- **Sponsors and co-sponsors**: printed on page 1–2 of Assemblée nationale proposition de loi PDFs (`présentée par Mme/M. ... et les membres du groupe ...`) and in the Assemblée open-data XML/JSON (`Dossiers_Legislatifs.json`).

## 2. Debates and votes

- **Assemblée nationale plenary debates**: `https://www.assemblee-nationale.fr/dyn/17/comptes-rendus/seance/`.
- **Assemblée nationale roll calls (scrutins publics)**:
  - Web pages: `https://www.assemblee-nationale.fr/dyn/17/scrutins/<N>` (HTML, directly fetchable). Each parliamentary group has a `<li class="relative-flex">` block starting with `Pour : <count>` containing `<a href="/dyn/deputes/PA...">Mme/M. Name</a>`.
  - Open data: `Scrutins.json` and `AMO30` actor files on `https://data.assemblee-nationale.fr/`.
- **Sénat plenary debates**: `https://www.senat.fr/seances/s<YYYYMM>/s<YYYYMMDD>/s<YYYYMMDD>_mono.html` (single-file HTML for the whole day's sitting, speaker tags `<!--cri:intervenant mat="..." nom="..."-->`).
- **Sénat roll calls (scrutins publics)**: `https://www.senat.fr/scrutin-public/<session_start_year>/scr<session_start_year>-<N>.html` (e.g. `2024/scr2024-322.html` for 12 June 2025; `2025/scr2025-63.html` for 28 Nov 2025). Note: amendments rejected *à main levée* (show of hands), such as the 28 Nov 2025 Zucman fallback amendments (`I-185 rectifié`, `I-1640 rectifié bis`), have no scrutin page.
- **How articles are numbered**: finance bill (`PLF`) wealth-tax amendments are typically tabled *après l'article 2*, *après l'article 3* or *après l'article 4* of Part 1, proposing new articles `885 A` onward of the *Code général des impôts*.

## 3. Members, parties, seats

- **Assemblée nationale**: `data.assemblee-nationale.fr` (active deputies + organs zip, 577 seats, grouped by abbreviation `LFI-NFP`, `SOC`, `EcoS`, `GDR`, `LIOT`, etc.). No Wikidata IDs in open data; matched by name in `skill/scripts/seats.py`.
- **Sénat**: `https://www.senat.fr/data/senateurs/ODSEN_GENERAL.csv` (348 active senators with `État = ACTIF` and group).

## 4. Other official records

- **France Stratégie**: *Comité d'évaluation des réformes de la fiscalité du capital* (`strategie-plan.gouv.fr`), final report Oct 2023 (ISF 2017 scale, IFI revenue, departures).
- **Conseil constitutionnel**: `https://www.conseil-constitutionnel.fr/decision/<year>/<ref>.htm` (e.g. `2026-901 DC` on the 2026 finance law; `2010-44 QPC` on ISF history).
- **DGFiP**: annual ISF statistical series (`impots.gouv.fr` / `data.economie.gouv.fr`).

## 5. Access notes

- `assemblee-nationale.fr`, `senat.fr`, `conseil-constitutionnel.fr`, and `strategie-plan.gouv.fr` all respond cleanly to standard HTTP requests (`urllib`/`requests`) without CAPTCHA or JS rendering.
- `https://www.senat.fr/scrutin-public/2025/` directory listing returns `403 Forbidden`, but individual `scr2025-<N>.html` pages load directly.
- All documents are in French.

## 6. Coverage log

| Date | Run | Documents read (title, number, date) | Result (rows added, votes found) | Not read / open |
|---|---|---|---|---|
| 2026-10-20 | R001 | PPL 768, 246, 2193, 648, 359, 2563, PPR 2164; AN scrutins 878, 881, 3295-3303; Sénat scrutin 322 | Initial register of deputies, senators, cosponsors | Full text of bills beyond page 1-2 |
| 2026-11-01 | R002 | AN bills 768, 246, 2193, 359, 648, 2563; Finance committee report 930; Sénat committee summary | 4 new actors, 37 cosponsor evidence rows | — |
| 2026-11-08 | R007 | France Stratégie 2023 report & avis; CC 2010-44 QPC, 2026-901 DC; PLF 2027 amendments I-471, I-38, I-2566; scrutins 8859-8861 totals | 18 documents tracked in `documents.csv` | Per-member rows for scrutins 8859-8861 |
| 2026-11-14 | R008 | AN scrutins 8859, 8860, 8861 (16 Oct 2026) per-member Pour lists; Sénat sitting 28 Nov 2025 (`s20251128_mono.html`) & scrutin 63/I-643 check | 3 new deputies (`A0393`-`A0395`), 35 `vote` rows (`E00771`-`E00805`); verified Nov 28 2025 Zucman fallback amendments were voted *à main levée* | Remaining partial annexes in France Stratégie 2023; PLF 2027 I-471/I-38/I-2566 full co-signatory lists |

## 7. Known gaps and next steps

- Read the full co-signatory lists of PLF 2027 amendments `I-471` (Bouloux), `I-38` (Sas), `I-2566` (Coquerel) to catch any co-signers who did not vote in scrutins 8859-8861.
- Check Sénat sitting `20251128_mono.html` amendment `I-1640 rectifié bis` (Masset / RDSE) for RDSE co-signatories not yet in the register.
- Read full text of France Stratégie 2023 annexes and Conseil constitutionnel `2010-44 QPC` if needed for historical context.
