# Norway: where the official record is and how to read it

Written in run R016 (2026-11-09, official legislative records deep-dive for Norway). Country guide for maps, seats and local portals: `skill/references/countries/no.md` (and `data/no/area_profile.md`). This file answers one question: **where is everything the Storting and government have put on record about wealth taxation (*formuesskatt*), and how do I get all of it?** Nothing here is a source for a claim in the register; the register's own sources are.

Norway has maintained a continuous statutory net wealth tax (*formuesskatt*) governed by Chapter 4 of the Tax Act of 1999 (*skatteloven*, lov 26. mars 1999 nr. 14, §§ 4-1 flg.). The tax comprises both a municipal wealth tax share (*kommunal formuesskatt*) and a state wealth tax (*statlig formuesskatt*), whose rates and thresholds are determined annually by the Storting through the annual tax resolution (*Stortingets skattevedtak*, *Innst. 3 S*).

The official record consists of:
1. **Government proposals and budget bills:** *Prop. 1 LS* (Skatter og avgifter) and *Prop. 1 S* (Statsbudsjettet) from Finansdepartementet.
2. **Private member motions:** *Dokument 8* proposals (*representantforslag*) submitted by opposition parties to repeal, restrict, or delay wealth taxation.
3. **Standing committee recommendations:** *Innstilling S* (especially *Finanskomiteen* recommendations on budget frames and motions) and *Innstilling L* (statutory legislative amendments to *skatteloven*).
4. **Plenary debates and referater:** Stenographic records of debates in the Storting chamber (*referater*, published daily in PDF and on Stortinget.no).
5. **Electronic roll-call voting records:** Division lists (*voteringsutskrifter*) recorded through the parliamentary voting system and exposed via the open REST API `data.stortinget.no`.
6. **Official inquiries and reports:** NOU reports (e.g. NOU 2014:13 Scheel-utvalget, NOU 2022:20 Torvik-utvalget), ministry consultative papers (*høringsnotater*), and statistics from Skatteetaten and SSB.

---

## 1. Bills, motions and proposals

- **Register of cases and bills:** Stortinget open data API `https://data.stortinget.no/eksport/saker?sesjonid={session}&format=json` (covers all parliamentary sessions from 2000 onwards; no authentication required). Individual case tracking URL: `https://data.stortinget.no/eksport/sak?sakid={id}&format=json` and public web page: `https://www.stortinget.no/no/Saker-og-publikasjoner/Saker/Sak/?p={id}`.
- **Document numbering conventions:**
  - `Dokument 8:NN S (YYYY–YYYY)`: Private member motions (*representantforslag*). Examples:
    - *Dokument 8:77 S (2011–2012)*: Fremskrittspartiet motion to abolish wealth tax on working capital (*opphevelse av formuesskatt på arbeidende kapital*).
    - *Dokument 8:76 S (2011–2012)*: FrP motion to abolish wealth tax on non-working capital.
    - *Dokument 8:47 S (2011–2012)*: Opposition motion (Høyre, KrF, Venstre) demanding an independent study on wealth tax effects.
    - *Dokument 8:10 S (2018–2019)*: Rødt motion on inequality and wealth/inheritance taxation.
    - *Dokument 8:110 S (2021–2022)*: FrP motion to delay and reassess wealth taxation of aquaculture concessions (*havbrukskonsesjoner / oppdrettstillatelser*).
  - `Prop. 1 LS (YYYY–YYYY)`: Annual government tax and customs proposition (*Skatter, avgifter og toll*).
  - `Innst. 3 S (YYYY–YYYY)`: Annual Finance Committee recommendation on budget revenue frames (*rammeområde 21*) and the statutory tax decision (*skattevedtaket*).
  - `Innst. 4 L (YYYY–YYYY)`: Annual Finance Committee recommendation on amendments to the Tax Act (*skatteloven*).
- **Search terms (Norwegian):**
  - Core terms: `formuesskatt`, `formueskatt`, `formuesbeskatning`, `skatt på formue`, `arbeidende kapital`, `bunnfradrag`, `verdsettelsesrabatt`, `aksjerabatt`, `havbrukskonsesjoner`.
  - Excluded look-alikes: `eiendomsskatt` (municipal property tax on real estate), `arveavgift` (inheritance tax abolished in 2014), `trinnskatt` (progressive personal income bracket tax), `formuesregister` (wealth register registry without a tax).
- **Sponsors and co-sponsors:** Listed on the front page of every *Dokument 8* PDF and exposed in the Storting API under `forslag_levert_av_representant` and `forslag_levert_av_parti_liste`.
- **Government proposals and consultations:** Finansdepartementet publishes budget propositions on `https://www.regjeringen.no/no/tema/okonomi-og-budsjett/statsbudsjettet/` and consultative drafts on `https://www.regjeringen.no/no/sok/id86008/?term=formuesskatt&type=horing`. Note that regjeringen.no can intermittently return 403 or captcha to automated scrapers; use Stortinget.no / data.stortinget.no which provides permanent open access.

---

## 2. Debates and votes

- **Plenary transcripts (*Referater*):**
  - Daily proceedings are published in full stenographic text at:
    - Pre-2020: `https://www.stortinget.no/globalassets/pdf/referater/stortinget/{session}/s{YYMMDD}.pdf` (or `s{YYMMDD}-ny.pdf`).
    - Post-2020: `https://www.stortinget.no/globalassets/pdf/referater/stortinget/{session}/refs-{session_short}-{MM}-{DD}.pdf`.
  - Also available via HTML pages at `https://www.stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/{session}/{YYMMDD}/` (note: HTML pages are rendered via client-side React hydration; the direct PDF files are static, full-text searchable, and ideal for `gazette_scan.py`).
  - **Speaker labels:** Formatted in bold text with timestamp, party affiliation, and representative name:
    - Committee rapporteur: `Knut Storberget (A) [19:09:15]:`
    - Party spokesperson: `Geir-Ketil Hansen (SV) [19:34:41]:`
    - Government minister: `Statsråd Sigbjørn Johnsen [20:06:49]:`
    - Opposition speaker: `Christian Tybring-Gjedde (FrP) [19:15:30]:`
    - Debate on aquaculture: `Mona Nilsen (A) [16:16:01]:`, `Geir Jørgensen (R) [16:25:46]:`.
- **Roll-Call Votes (*Voteringer*):**
  - Every counted vote in the Storting chamber is recorded electronically.
  - Votes for any specific case (*sak*) are listed via:
    `https://data.stortinget.no/eksport/voteringer?sakid={sakid}&format=json`
  - Verbatim text of the proposal being voted on:
    `https://data.stortinget.no/eksport/voteringsforslag?voteringid={voteringid}&format=json`
  - Per-member division list (*voteringsresultat*):
    `https://data.stortinget.no/eksport/voteringsresultat?voteringid={voteringid}&format=json`
    - `votering = 2`: **For** (Yes)
    - `votering = 3`: **Mot** (No)
    - `votering = 1`: **Ikke tilstede** (Absent)
- **Distinguishing Article-Specific Votes from Block Votes:**
  - **Omnibus / Budget block votes (Discard):** Annual fiscal budget recommendations (*Innst. 3 S*, *rammeområde 21*) bundle hundreds of revenue lines, tax rates, VAT provisions, and customs duties together into aggregate package votes, or oppose them through unified opposition alternative budgets. Under standard register QA rules, overall budget block votes are discarded.
  - **Standalone Wealth-Tax Votes (Retain - Grade A):**
    - **Vote 2354 (29 May 2012)** on *Dokument 8:77 S / Innst. 281 S (2011–2012)*:
      - Motion: *Komiteens tilråding* that the proposal to abolish the wealth tax on working capital (*opphevelse av formuesskatt på arbeidende kapital*) *vedtas ikke* (shall NOT be adopted).
      - Adopted 53 to 48.
      - 53 YES voters (Grade A vote support): 39 Arbeiderpartiet (A), 7 Senterpartiet (Sp), 7 Sosialistisk Venstreparti (SV).
    - **Vote 2352 (29 May 2012)** on *Dokument 8:77 S / Innst. 281 S (2011–2012)*:
      - Motion: FrP proposal nr. 1 to abolish wealth tax on working capital from 1 Jan 2013.
      - Rejected 79 Mot to 22 For.
    - **Vote 2349 & 2351 (29 May 2012)** on *Dokument 8:76 S / Innst. 280 S (2011–2012)*:
      - Motion: Proposal to abolish wealth tax outside working capital.
      - Vote 2349 rejected 77 Mot to 23 For. Vote 2351 (komiteens tilråding) adopted 59 For to 42 Mot.
    - **Vote 18557 & 18559 (26 April 2022)** on *Dokument 8:110 S / Innst. 237 S (2021–2022)*:
      - Motion: FrP and Høyre proposal to postpone and exempt pre-1998 aquaculture concessions from wealth tax valuation.
      - Vote 18557 (FrP postponement): Rejected 87 Mot to 14 For.
      - Vote 18559 (Komiteens tilråding - bifalles ikke): Adopted 86 For to 13 Mot.

---

## 3. Members, parties, seats

- **Storting Member Register API:**
  - `https://data.stortinget.no/eksport/representanter?stortingperiodeid={session}&format=json` lists all representatives and deputy representatives (*vararepresentanter*) for any 4-year parliamentary period (e.g. `2009-2013`, `2013-2017`, `2017-2021`, `2021-2025`).
  - Individual profile: `https://data.stortinget.no/eksport/person?personid={perid}&format=json` provides full biographical data, date of birth, date of death (`doedsdato`), committee assignments, and electoral county (*fylke*).
  - Living status check: `doedsdato` is `None` for living members. If `doedsdato` contains a timestamp, the member is deceased and must be placed in `data/no/exclusions.csv` (`reason: deceased`).
- **Wikidata coverage:**
  - Stortinget representative identifiers are mapped 1-to-1 on Wikidata using property **P3072** (*Storting person ID*).
  - A SPARQL query matching `?item wdt:P3072 "{perid}"` resolves 100% of Storting representatives to their Wikidata QID in a single batch query.

---

## 4. Other official records

- **NOU Commission Reports (Norges offentlige utredninger):**
  - *NOU 2014: 13 Kapitalbeskatning i en global økonomi* (Scheel-utvalget): Evaluated the wealth tax, recommending a lower rate (0.75%), higher basic threshold, and removing valuation discounts.
  - *NOU 2022: 20 Et helhetlig skattesystem* (Torvik-utvalget): Extensive 450-page review of Norwegian tax policy. Recommended broadening the wealth tax base to all assets at 100% market value while substantially raising thresholds and lowering rates.
- **Municipal Wealth Tax Share (*Kommunal formuesskatt*):**
  - Section 2-2 of the annual tax decision sets the maximum municipal wealth tax rate (typically 0.70% historically, reduced to 0.35% in recent fiscal years).
  - Municipalities are authorized to set a lower rate, but virtually all 356 Norwegian municipalities levy the maximum rate to preserve local tax revenues, with rare exceptions (e.g. Bø i Vesterålen lowering the municipal rate to 0.20% in 2020).
- **Tax Administration (Skatteetaten):**
  - Publishes official tax statistics (*skattestatistikk for personer*), annual wealth tax revenue yields, and binding advance rulings (*bindende forhåndsuttalelser*).

---

## 5. Access notes

- **API & Portal Stability:** `data.stortinget.no` is completely open, exceptionally well-structured, fast, and does not require API keys or session cookies.
- **Tools that worked:**
  - `skill/scripts/gazette_scan.py` with `--term "formuesskatt|formueskatt"` successfully indexed and searched all downloaded primary PDFs.
  - Direct REST JSON endpoints for cases, votes, vote proposals, and division lists.
  - Single batch SPARQL query against Wikidata property P3072 for representative QIDs.
  - `skill/scripts/wtdb.py validate`, `dedupe`, `checkquotes`.

---

## 6. Coverage log

| Date | Run | Documents read (title, number, date) | Result (rows added, votes found) | Not read / open |
|---|---|---|---|---|
| 2026-11-09 | R016 | Storting parliamentary records deep-dive (2010–2026): Dok 8:77 S, Innst. 281 S, Dok 8:76 S, Innst. 280 S, Plenary Referat s120529 (29 May 2012); Dok 8:47 S, Innst. 215 S (April 2012); Dok 8:10 S, Innst. 144 S (2018–2019); Dok 8:110 S, Innst. 237 S, Plenary Referater refs-202122-04-21 & refs-202122-04-26 (April 2022); targeted scan of 238 wealth-tax vote proposals across 15 sessions in `data.stortinget.no`. | Identified standalone roll-call Vote 2354 (Innst. 281 S, 53 Yes votes to reject repeal of wealth tax on working capital) and Vote 18557/18559 (Innst. 237 S). Added 5 speeches defending wealth tax (Knut Storberget, Geir-Ketil Hansen, Sigbjørn Johnsen, Mona Nilsen, Geir Jørgensen), verified 52 living MPs from Vote 2354 with alive checks, added deceased member Bendiks H. Arnesen to `exclusions.csv`, logged 13 primary docs in `documents.csv`, added 2 qualified bills to `data/resources.json`. | Municipal council wealth-tax debates (e.g. Bø i Vesterålen local rate reductions); committee hearing submissions (*skriftlige høringsinnspill*) on NOU 2022:20. |

---

## 7. Known gaps and next steps

- **Municipal wealth-tax resolutions:** Local council debates in municipalities that discussed lowering the municipal wealth tax rate (notably Bø i Vesterålen in 2020) or defending the municipal tax yield against state rate reductions.
- **Parliamentary question hour (*Muntlig spørretime* and *Skriftlige spørsmål*):** Routine written questions (*dokument 15*) from opposition MPs to the Minister of Finance regarding wealth-tax yields, valuation discounts, and relocation of high-net-worth individuals to Switzerland.
- **Future fiscal year sessions (2025–2026+):** Follow up on the upcoming White Paper (*stortingsmelding*) following up on NOU 2022:20 (Torvik-utvalget) and potential cross-party tax compromise discussions.
