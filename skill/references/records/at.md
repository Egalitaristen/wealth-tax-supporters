# Austria: where the official record is and how to read it

Written in run R007 (2026-11-09, official legislative records workflow pass). This file answers one question: **where is everything the Austrian Parliament (Nationalrat and Bundesrat) and the Federal Government have put on record about wealth taxation, and how do I get all of it?** Nothing here is a source for a claim in the register; the register's own sources are.

Wealth-tax context: the net wealth tax (*Vermögensteuergesetz 1954*) was repealed with effect from 1 January 1994 (via the *Steuerreformgesetz 1993*, BGBl. Nr. 818/1993, passed in the XVIII. GP). Since 1994, Austria has had no recurrent net wealth tax. Between 2007 and 2008, the Constitutional Court (VfGH) struck down the inheritance and gift tax (Erbschafts- und Schenkungssteuer) due to unequal valuation of real estate. Since 2010, proposals for introducing a recurrent wealth tax (*Vermögenssteuer*, *Millionärssteuer*, *Millionärsabgabe*) have regularly reached the Nationalrat, principally via:
1. Opposition motions for a resolution (*selbständige und unselbständige Entschließungsanträge*, `A(E)` and `UEA`).
2. Citizens' initiatives (*Bürgerinitiativen*, `BI`), notably the 2009–2010 KPÖ-sponsored initiative *Reichensteuer jetzt!* (15/BI).
3. Parliamentary questions and question time debates (*Mündliche und Dringliche Anfragen*, `M` and `J`).
4. General tax reform bills (e.g. *Steuerreformgesetz 2015/2016*, 684 d.B. XXV. GP), where wealth tax proposals were debated in plenary but not enacted.

---

## 1. Bills, motions and proposals

- **Register of parliamentary items:** The Austrian Parliament operates an open web portal and open JSON API at `parlament.gv.at`:
  - **Portal:** `https://www.parlament.gv.at/recherchieren/gegenstaende`
  - **Direct JSON search API (Items / Gegenstände):** `POST https://www.parlament.gv.at/Filter/api/filter/data/101?js=eval&showAll=true&export=true&search=<encoded_term>`
  - **Item details API:** `https://www.parlament.gv.at/gegenstand/{GP}/{ITYP}/{INR}?json=TRUE` (e.g., `https://www.parlament.gv.at/gegenstand/XXVII/UEA/1077?json=TRUE`)
- **Document types that matter:**
  - `UEA`: *Unselbständiger Entschließungsantrag* (motion for a resolution attached to an ongoing debate; e.g. 1077/UEA XXVII. GP).
  - `A`: *Selbständiger Entschließungsantrag* / *Antrag* (independent motion, cited as `NNN/A` or `NNN/A(E)`).
  - `BI`: *Bürgerinitiative* (citizens' initiative submitted with at least 500 signatures; e.g. 15/BI XXIV. GP).
  - `I` / `d.B.`: *Drucksache der Beilagen* (government bills / *Regierungsvorlagen* and committee reports / *Ausschussberichte*).
  - `J` / `AB`: Written questions (*Anfragen*) and ministerial answers (*Anfragebeantwortungen*).
  - `M`: Oral questions during plenary question time (*Mündliche Anfragen*; e.g. 114/M XXVII. GP).
- **Search terms (Austrian German):**
  - Core wealth tax terms: `Vermögenssteuer`, `Vermögensteuer`, `Millionärssteuer`, `Millionärsabgabe`, `Vermögensabgabe`, `Reichensteuer`.
  - Note spelling: In Austrian parliamentary records, the spelling with Fugen-s (*Vermögenssteuer*) is far more common than without (*Vermögensteuer*), although both appear.
  - Excluded look-alikes (Ground Rule 1):
    - `Erbschaftssteuer`, `Erbschaftsteuer`, `Schenkungssteuer`, `Erbschafts- und Schenkungssteuer`, `Millionenerbschaften` (inheritance and gift taxes; e.g. motions 1041/UEA, 748/A(E), 210/UEA, 1119/A(E) are strictly inheritance tax motions).
    - `Immobiliensteuer`, `Grunderwerbsteuer`, `Grundsteuer` (real estate / transfer taxes).
    - `Bankenabgabe`, `Finanztransaktionssteuer` (financial transaction or sector levies).
    - `Übergewinnsteuer`, `Zufallsgewinnsteuer` (excess profits taxes).
- **Sponsors and signatories:**
  - In `UEA` and `A` documents, the lead sponsor is named in the document title (`der Abgeordneten Julia Elisabeth Herr, Kolleginnen und Kollegen`).
  - The scanned PDF (`fnameorig_*.pdf`) contains the physical signature list of MPs at the end of the motion.
  - For `BI` documents, the primary petitioner and contact person is named on the front page (e.g., Claudia Klimt-Weithaler for 15/BI).

---

## 2. Debates and votes

- **Plenary transcripts (*Stenographische Protokolle*):**
  - **Portal:** `https://www.parlament.gv.at/recherchieren/plenarsitzungen`
  - **Direct JSON search API (Plenary sittings):** `POST https://www.parlament.gv.at/Filter/api/filter/data/211?js=eval&showAll=true&export=true&search=<encoded_term>`
  - **URL structure:** `https://www.parlament.gv.at/dokument/{GP}/NRSITZ/{SITZNR}/fnameorig_{FILEID}.html` (and `.pdf`).
  - **Speaker labels:** Speeches in the *Stenographisches Protokoll* are clearly tagged by speaker role, time, and name:
    - E.g.: `Abgeordnete Mag. Selma Yildirim (SPÖ): ...`
    - E.g.: `Abgeordnete Sabine Schatz (SPÖ): ...`
    - E.g.: `Abgeordnete Nurten Yılmaz (SPÖ): ...`
    - Oral questions in Fragestunde: `114/M „Werden Sie in Österreich endlich einen gerechten Beitrag der Multimillionäre und Milliardäre durch die Einführung einer Millionärssteuer sicherstellen?“`
- **Voting mechanism in the Nationalrat (Critical Finding):**
  - Under the Rules of Procedure of the Austrian National Council (*Geschäftsordnungsgesetz des Nationalrates*, GOG-NR, § 66):
    - Routine votes and resolution motions (*Entschließungsanträge*) are decided by **show of hands or standing up** (*Zeichen mit der Hand* / *Aufstehen*).
    - In the official stenographic minutes, only the aggregate party positions are recorded:
      - E.g., for 1077/UEA: *"Der Antrag ist abgelehnt. Dafür: SPÖ, dagegen: ÖVP, FPÖ, GRÜNE, NEOS."*
    - **No per-member division list exists for show-of-hands votes.**
    - A roll-call vote (*Namentliche Abstimmung*) requires a written petition signed by at least 20 Members of the National Council prior to the vote (§ 66 Abs. 3 GOG-NR).
    - When a roll-call vote is conducted, the complete member-by-member alphabetical roll call is printed in the stenographic protocol (with `Ja`, `Nein`, `Abwesend`).
    - **Post-2010 Roll Calls Check:** A comprehensive scan of all tax-reform plenary sessions post-2010 (notably the *Steuerreformgesetz 2015/2016*, 83. Sitzung XXV. GP on 7 July 2015) shows that the roll calls requested by opposition parties were strictly confined to specific income tax brackets (*Art. 1 Z 4, 10, 40* and *Z 19*) and family allowances. **Zero roll-call votes were held on a wealth-tax bill or amendment post-2010 in Austria.**
    - Ground Rule 2: Because party block totals cannot be attributed to individual members, **Grade A voting evidence from roll-call votes is non-existent in post-2010 Austria**. Grade A legislative evidence is instead provided by individual speeches (`evidence_type=speech`) and formally tabled motions (`evidence_type=motion`).

---

## 3. Members, parties, seats

- **Member register:**
  - National Council (Nationalrat) sitting members and historic terms are hosted at `https://www.parlament.gv.at/recherchieren/personen/nationalrat`.
  - Individual profile URL structure: `https://www.parlament.gv.at/person/{PID}`
  - Identifiers: The Austrian Parliament assigns an internal person ID (`PID`, formerly `PAD_intern`). Examples:
    - Julia Herr: `PID 5639`
    - Kai Jan Krainer: `PID 14842`
    - Selma Yildirim: `PID 2339`
    - Sabine Schatz: `PID 2337`
    - Nurten Yılmaz: `PID 83117`
    - Markus Marterbauer: `PID 31021` (Finance Minister since 2025)
  - Wikidata: High-quality coverage exists for all Austrian Nationalrat members (e.g. `Q42303254` for Selma Yildirim, `Q42853141` for Sabine Schatz, `Q1679312` for Nurten Yılmaz).
- **Subnational chambers (Landtage):**
  - 9 provincial parliaments (*Landtage*): Wien, Niederösterreich, Oberösterreich, Steiermark, Tirol, Salzburg, Kärnten, Burgenland, Vorarlberg.
  - While wealth taxation is a federal competency (*Bundeskompetenz* under the B-VG), provincial politicians (such as KPÖ in Graz/Steiermark and SPÖ Wien) frequently pass resolutions or publish model proposals addressed to the federal government.

---

## 4. Other official records

- **Federal Law Gazette (*Bundesgesetzblatt*, BGBl.):**
  - Hosted on the Legal Information System of the Republic (*Rechtsinformationssystem des Bundes*, RIS) at `https://www.ris.bka.gv.at`.
  - Historical laws (1945–2003) and current gazette issues (BGBl. I, II, III).
  - BGBl. Nr. 818/1993: Enacted the repeal of the *Vermögensteuergesetz 1954* as part of the *Steuerreformgesetz 1993*.
- **Constitutional Court (*Verfassungsgerichtshof*, VfGH):**
  - Searchable via RIS (*Judikatur der Höchstgerichte*).
  - Landmark decisions on wealth/capital taxation:
    - VfGH G 54/06 (repeal of inheritance tax on equal protection grounds due to unitary property valuations).
    - VfGH G 23/07 (gift tax).
- **Austrian National Bank (OeNB) and Austrian Institute of Economic Research (WIFO):**
  - Household Finance and Consumption Survey (HFCS) studies: primary empirical basis used by Austrian economists (Marterbauer, Schnetzer, Kapeller) and parliamentary parties to model wealth distribution and wealth-tax yield.
- **Federal Ministry of Finance (*Bundesministerium für Finanzen*, BMF):**
  - Pre-draft consultations (*Begutachtungsentwürfe*) and tax statistics.

---

## 5. Access notes

- **API & Portal behavior:**
  - `parlament.gv.at` uses a modern web frontend with backend REST JSON filters (`Filter/api/filter/data/101` for items, `data/211` for meetings).
  - The JSON API supports `export=true`, `showAll=true`, and `js=eval` parameters.
  - Queries with German umlauts must be properly percent-encoded (`Verm%C3%B6genssteuer`).
  - Scanned PDFs: Older documents (prior to ~2015) or physical motion originals (`fnameorig_*.pdf`) are scanned images; OCR text is available in the Stenographisches Protokoll transcripts.
  - Character encoding: Windows default codepages (cp1252) break on Turkish characters in Austrian MP names (e.g., `Nurten Yılmaz` and `Selma Yıldırım`). Scripts must set UTF-8 stdout encoding (`sys.stdout.reconfigure(encoding='utf-8')`).
- **QA Tooling:**
  - `python skill/scripts/gazette_scan.py` works on local plenary and motion PDFs / text files.
  - `python skill/scripts/wtdb.py checkquotes` verifies verbatim speech text against published protocols.

---

## 6. Coverage log

| Date | Run | Documents read (title, number, date) | Result (rows added, votes found) | Not read / open |
|---|---|---|---|---|
| 2026-11-09 | R007 | 23 primary documents downloaded to `data/at/primary_docs/`: 1077/UEA (2023-06-14), 219. Sitzung XXVII. GP (2023-06-14), 15/BI (2009-11-06), 589 d.B. XXIV. GP (2010-01-21), 460/UEA (2010-08-25), 75. Sitzung XXIV. GP (2010-08-25), 99/UEA (2020-04-22), 24. Sitzung XXVII. GP (2020-04-22), 1041/UEA (2023-05-12), 211. Sitzung XXVII. GP (2023-05-12), 1265/UEA (2024-09-18), 276. Sitzung XXVII. GP (2024-09-18), 115. Sitzung XXVII. GP (2021-07-07), 117. Sitzung XXVII. GP (2021-07-08), 684 d.B. XXV. GP (2015-06-16), 750 d.B. XXV. GP (2015-07-02), 83. Sitzung XXV. GP (2015-07-07), 145/UEA (2014-05-21), 234/UEA (2014-09-02), 693/A(E), 748/A(E), 210/UEA, 1119/A(E). | 4 new actors (A0039 Selma Yildirim, A0040 Sabine Schatz, A0041 Nurten Yılmaz, A0042 Peter Windischhofer); 4 new evidence rows (E00039, E00040, E00041, E00042); corrected E00003 date to 2023-06-14; 2 bills added to `data/resources.json`; closed leads L0018 and L0019; confirmed 0 roll-call votes post-2010. | Plenary sittings prior to 2010 (XXIV. GP back to XVIII. GP 1993); Landtag minutes in Vienna and Graz. |

---

## 7. Known gaps and next steps

- **XVIII. GP Plenary Records (1993):** Download and scan the plenary session debating the *Steuerreformgesetz 1993* (November/December 1993) to capture the historic debate surrounding the formal suspension/repeal of the *Vermögensteuergesetz 1954*.
- **Subnational Landtag records:** Search municipal/state records in Vienna (*Wiener Landtag / Gemeinderat*) and Styria (*Landtag Steiermark*) for formal state-level resolutions demanding federal wealth tax enactments.
