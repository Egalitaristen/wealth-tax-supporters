# Italy: where the official record is and how to read it

One file per country, keeping track of where the Italian Parliament (Camera dei deputati and Senato della Repubblica), government, and regional/local assemblies put wealth-tax bills, amendments, debates, and votes on record.

## 1. Bills, motions and proposals

- **Camera dei deputati — Linked Open Data SPARQL (`https://dati.camera.it/sparql`)**: Covers bills (`ocd:atto`), plenary votes (`ocd:votazione`), per-member vote expressions, and deputies across legislatures. Returns JSON via `?query=...&format=json`. Note: `atti` titles often use `"grandi patrimoni"`, `"imposta patrimoniale"`, or `"patrimonio netto"`, while many budget-law wealth-tax proposals are tabled as *emendamenti* or *ordini del giorno* to the annual *Legge di Bilancio* rather than standalone bills.
- **Camera dei deputati — Bill dossiers (`https://www.camera.it/leg<LEG>/126?tab=1&leg=<LEG>&idDocumento=<NUM>`)**: Works for Legislature 18 (`A.C. 2790` Budget Law 2021) and Legislature 19. Older Legislature 16 bills (e.g. `A.C. 4678` Cambursano 2011) resolve via `http://www.camera.it/uri-res/N2Ls?urn:camera-it:parlamento:scheda.progetto.legge:camera;16.legislatura;<NUM>`.
- **Senato della Repubblica — Linked Open Data SPARQL (`https://dati.senato.it/sparql`)**: Covers Senate bills (`osr:Ddl`) and senators (`osr:Senatore`). The web portal `senato.it` and `aic.camera.it` sit behind Radware Captcha protection and block plain HTTP clients.
- **Popular initiative bills (*proposte di legge di iniziativa popolare*)**: Filed at the Corte di Cassazione under art. 71 Cost.; digital signatures are collected on `firmereferendum.giustizia.it`. Example: *1% Equo* ("Imposta grandi patrimoni", filed 7 May 2026), text openly downloadable at `https://unpercentoequo.it/proposta-di-legge-imposta-grandi-patrimoni.pdf`.
- **Search terms (Italian / German)**: `"grandi patrimoni"`, `"imposta patrimoniale"`, `"imposta sui grandi patrimoni"`, `"tassa sui super ricchi"`, `"tassa sui miliardari"`, `"contributo di solidarietà"`, `"Vermögenssteuer"`. Beware false positives: *"patrimoniale"* in bill titles often refers to criminal *frode patrimoniale*, *misure di prevenzione patrimoniali* (anti-mafia), or *patrimonializzazione delle imprese*.

## 2. Debates and votes

- **Plenary stenographic reports (Camera)**: Openly downloadable as text-searchable PDFs at `https://documenti.camera.it/leg<LEG>/resoconti/assemblea/html/sed<SED4>/stenografico.pdf` (e.g. `sed0446` for 27 December 2020). Speaker labels are uppercase `FIRSTNAME SURNAME (GROUP).`
- **Plenary *Allegato A* (full text and signatories of voted *ordini del giorno* and amendments)**: Openly accessible via `https://documenti.camera.it/apps/commonServices/getDocumento.ashx?idLegislatura=<LEG>&sezione=assemblea&tipoDoc=documenti_seduta&idSeduta=<SED4>&nomefile=allegato_a`.
- **Roll-call votes (Camera)**: Query `dati.camera.it/sparql` for `ocd:votazione` and per-member `ocd:rif_votazione` / `dc:type` (`"Favorevole"`, `"Contrario"`, `"Astensione"`). Always cross-check single unexpected `Favorevole` votes from opposing parties (e.g. FI/Lega) against speeches or later statements to rule out accidental button presses.
- **Committee stage**: Budget-law wealth-tax amendments (2020 Orfini–Fratoianni, 2024 Grimaldi, 2025 Magni) are examined in the 5th Committee (*Commissione Bilancio*) and are frequently ruled inadmissible or withdrawn before plenary electronic roll calls.

## 3. Members, parties, seats

- `python skill/scripts/seats.py data/it` fetches Camera dei deputati (`camera.it/deputati/elenco?leg=19&lettera=X`, SURNAME Name) and Senato (`dati.senato.it/sparql`, `osr:` namespace).
- `dati.camera.it/sparql` also provides full historical member lists for earlier legislatures (`ocd:rif_leg`).

## 4. Other official records

- **Autonomous Province of Bolzano (Südtiroler Landtag)**: Motions (*Voti* / *Begehrensanträge*) are published as open PDFs on `api-idap.landtag-bz.org/doc/IDAP_<id>.pdf` (e.g. `IDAP_773272.pdf` for Voto n. 39/25 *"Tax the Rich"*).

## 5. Access notes

- **Open to plain HTTP**: `dati.camera.it/sparql`, `dati.senato.it/sparql`, `camera.it/leg18/126`, `documenti.camera.it` (PDFs & `getDocumento.ashx`), `api-idap.landtag-bz.org/doc/`, `unpercentoequo.it/proposta-di-legge-imposta-grandi-patrimoni.pdf`.
- **Blocked / JS-only**: `senato.it`, `aic.camera.it` (Radware Captcha), `unpercentoequo.it` homepage (403 to plain HTTP / JS SPA), `oxfamitalia.org` (403 to plain HTTP).

## 6. Coverage log

| Date | Run | Documents read (title, number, date) | Result (rows added, votes found) | Not read / open |
|---|---|---|---|---|
| 2026-11-14 | R003 | `M0001` Proposta di legge di iniziativa popolare "Imposta grandi patrimoni" (1% Equo, 2026-05-07); `M0003` OdG 9/2790-bis-AR/69 Allegato A (2020-12-27); `M0004` Camera Seduta 446 stenografico (2020-12-27); `M0005` Camera roll call `vs18_446_008` (2020-12-27); `M0006` Bolzano Voto n. 39/25 PDF (2025-08-27) | 19 `Favorevole` votes + 10 signatories on `9/2790-bis-AR/69` + Fassina speech; 1% Equo bill text verified | `M0007` A.C. 4678 full text PDF; Bolzano Voto n. 39/25 roll-call stenographic PDF; Leg 19 2024–2025 Budget Committee amendment texts |

## 7. Known gaps and next steps

- Locate full text PDF of `A.C. 4678` (2011 Cambursano bill) to verify net-wealth-tax design before adding its 28 signatories.
- Locate Bolzano Landtag stenographic report for 19 Sep 2025 (`Voto n. 39/25`) for the 10 *Yes* voters.
- Check Leg 19 Budget Law 2025 & 2026 Committee minutes for AVS amendments (Grimaldi 2024, Magni 2025).
