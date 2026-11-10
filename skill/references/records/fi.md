# Finland: where the official record is and how to read it

Written in run R004 (2026-11-09) from an exhaustive scan of the Finnish Parliament (Eduskunta / Riksdagen) open data REST API (`avoindata.eduskunta.fi`), primary legislative documents (PDF and XML), verbatim plenary debates (*täysistunnon pöytäkirjat*, PTK), and committee documents (*Valtiovarainvaliokunta*, VaVM) for all post-2010 wealth-tax terms. Every URL, endpoint, and method below was verified on that date.

Key fact for Finland: **Finland abolished its national wealth tax (*varallisuusvero* / *förmögenhetsskatt*) effective from 1 January 2006 (Government proposal HE 144/2005 vp, adopted 13 December 2005 by 134 votes to 45; Parliament's reply EV 218/2005 vp). Since 2010, six parliamentary initiatives or budget motions proposing an actual net wealth tax have been introduced: LA 63/2010 vp, TAA 107/2010 vp, TAA 166/2010 vp, TAA 422/2010 vp, LA 55/2012 vp, LA 62/2014 vp, and TPA 25/2022 vp.** None resulted in a separate plenary division vote on adopting a wealth tax: committee recommendations to reject were adopted without roll call (e.g. LA 55/2012 vp in PTK 113/2012 vp), or the bills lapsed at the dissolution of the electoral term (*rauennut*). Plenary debates feature direct speeches defending the wealth and millionaire tax by party leaders and MPs. Primary PDFs and open data endpoints are unauthenticated and freely downloadable.

---

## 1. Bills, motions and proposals

- **Parliamentary Open Data REST API, tested and works:** `https://avoindata.eduskunta.fi/api/v1/`
  - Unauthenticated JSON API providing tabular access to parliamentary documents, votes, members, and speeches.
  - Document query endpoints:
    - Text search across document titles and contents: `https://avoindata.eduskunta.fi/api/v1/vaski/text?filter=<term>&perPage=100&page=0`
    - Parliament identifier lookup: `https://avoindata.eduskunta.fi/api/v1/vaski/eduskuntatunnus?filter=<id>`
    - Raw XML repository: `https://avoindata.eduskunta.fi/api/v1/tables/VaskiData/rows?columnName=Eduskuntatunnus&columnValue=<id>`
  - Document types in Finland:
    - `HE` / `RP`: *Hallituksen esitys* / *Regeringens proposition* (Government proposals/bills).
    - `LA` / `LM`: *Lakialoite* / *Lagmotion* (Private member legislative bills).
    - `TPA` / `ÅM`: *Toimenpidealoite* / *Åtgärdsmotion* (Parliamentary motion for executive action).
    - `TAA` / `BM`: *Talousarvioaloite* / *Budgetmotion* (Budget motions submitted during the September budget debate).
    - `VaVM` / `FiUB`: *Valtiovarainvaliokunnan mietintö* / *Finansutskottets betänkande* (Finance Committee report).
    - `EV` / `RSv`: *Eduskunnan vastaus* / *Riksdagens svar* (Parliament's reply adopting a bill).
    - `PTK` / `PR`: *Pöytäkirja* / *Protokoll* (Plenary sitting verbatim minutes and transcripts).

- **Official PDF & Matter Portal, tested and works:** `https://www.eduskunta.fi/`
  - Primary document direct PDF URL pattern:
    - `https://www.eduskunta.fi/pdf/<Type>+<Number>/<Year>` (e.g. `https://www.eduskunta.fi/pdf/LA+55/2012`, `https://www.eduskunta.fi/pdf/TAA+422/2010`). Returns clean HTTP 200 without bot mitigation.
  - Primary S3 storage endpoint for newer digital plenary records and motions:
    - `https://s3-eu-west-1.amazonaws.com/eduskunta-avoindata-documents-prod/vaski%2F<DocId>.pdf` (e.g. `PTK-116+2025-vp.pdf`, `TPA-25+2022-vp.pdf`). Completely public, no rate-limiting.
  - SvelteKit matter status endpoint:
    - `https://www.eduskunta.fi/asiat-ja-aanestykset/valtiopaivaasiat/<MatterId>/__data.json` returns structured lifecycle milestones (*vireilletulo*, *lähetekeskustelu*, *valiokuntakäsittely*, *ensimmäinen käsittely*, *toinen käsittely*, and resolution status *hylätty* / *rauennut*).

- **Search terms (Finnish & Swedish):**
  - *Core terms (Finnish):* `varallisuusvero` (net wealth tax), `varallisuusveron palauttaminen` (restoration of wealth tax), `varallisuusverolaki` (wealth tax act), `miljonäärivero` (millionaire tax), `suurten omaisuuksien vero` (tax on large fortunes), `puolustusvero` (wealth-based defense levy).
  - *Core terms (Swedish):* `förmögenhetsskatt` (net wealth tax), `miljonärsskatt` (millionaire tax), `miljardärsskatt` (billionaire tax), `förmögenhetsbeskattning` (wealth taxation).
  - *Contextual terms requiring verification:* `solidaarisuusvero` (used in Finland for the 2013+ temporary highest income-tax bracket on earnings over EUR 100,000 / EUR 85,800; not a wealth tax unless targeted at net assets), `pääomavero` (capital income tax on dividends/gains).
  - *Excluded look-alikes:*
    - `kiinteistövero` / `fastighetsskatt`: real property tax (excluded).
    - `perintö- ja lahjavero` / `arvs- och gåvoskatt`: inheritance and gift taxes (excluded).
    - `arvonnousuvero` (exit tax on unrealised capital gains when moving abroad; excluded unless paired with an annual net-wealth base).
    - Double taxation treaties (*tulo- ja varallisuusveroja koskeva kaksinkertaisen verotuksen välttäminen*, e.g. HE 159/2026 vp): bilateral DTAs incorporating OECD model conventions; not national wealth tax legislation.

- **Sponsors and co-sponsors:**
  - In primary PDFs: printed prominently on page 1 (e.g. `TAA 422/2010 vp — Esa Lahtela /sd ym.`, signature list: `Esa Lahtela /sd`, `Marjaana Koskinen /sd`; `LA 55/2012 vp — Kaj Turunen /ps ym.`, signature list of 39 MPs at the end).
  - In VaskiData XML: actors are recorded in `<met:Toimija>` elements with `muuTunnus` (MP ID) and name fields.

- **Government proposals and consultations:**
  - Ministry of Finance (*Valtiovarainministeriö*, VM): `vm.fi`.
  - Committee expert hearings (*asiantuntijalausunnot*): available via `vaski/text?filter=Asiantuntijalausunto` or `EDK-...-AK-...` PDF links.

---

## 2. Debates and votes

- **Plenary transcripts (Pöytäkirjat / PTK):**
  - Published for each sitting as downloadable PDF and online: `https://www.eduskunta.fi/pdf/PTK+<Nr>/<Year>` and via open data S3 bucket `PTK-<Nr>+<Year>-vp.pdf`.
  - Speaker format:
    - Structured with exact timestamps and party labels: e.g. `14.35 Minja Koskela vas (esittelypuheenvuoro):`, `15.02 Minja Koskela vas (vastauspuheenvuoro):`, `15.48 Jessi Jokelainen vas:`, `17.54 Minja Koskela vas:`.
    - Easily scanned with `gazette_scan.py` preserving line breaks. Verbatim speech statements defending the wealth tax qualify at Grade A (`evidence_type=speech`).
- **Committee reports (Mietinnöt / VaVM):**
  - Finance Committee (*Valtiovarainvaliokunta*): `https://www.eduskunta.fi/pdf/VaVM+<Nr>/<Year>`.
  - Signed dissents and reservations (*vastalause* / *lauselma*): printed at the end of the report with named signatories. E.g. VaVM 53/2010 vp (reservation 2 signed by Mikko Kuoppa, Minna Sirnö, Matti Kauppila); VaVM 25/2014 vp (reservation 2 signed by Kari Uotila).
- **Roll calls and voting database:**
  - Vote table: `https://avoindata.eduskunta.fi/api/v1/tables/SaliDBAanestys/rows?columnName=IstuntoVPVuosi&columnValue=<Year>`
    - Columns: `AanestysId`, `IstuntoNumero`, `AanestysNumero`, `AanestysOtsikko`, `AanestysTulosJaa`, `AanestysTulosEi`, `AanestysTulosTyhjia`, `AanestysTulosPoissa`, `AanestysPoytakirja`, `AanestysValtiopaivaasia`.
  - Individual MP roll call votes: `https://avoindata.eduskunta.fi/api/v1/tables/SaliDBAanestysEdustaja/rows?columnName=AanestysId&columnValue=<Id>`
    - Columns: `EdustajaHenkiloNumero`, `EdustajaEtunimi`, `EdustajaSukunimi`, `EdustajaRyhmaLyhenne`, `EdustajaAanestys` (`Jaa`, `Ei`, `Tyhjää`, `Poissa`).
  - Plenary voting reality:
    - All 2010–2026 plenary votes in `SaliDBAanestys` were scanned: zero named roll calls were held specifically on enacting or amending a wealth-tax article.
    - Private member bills (`LA 55/2012 vp`, `LA 63/2010 vp`, `LA 62/2014 vp`, `TPA 25/2022 vp`) either lapsed or were rejected following negative committee reports without a recorded roll call division.
- **Block and package votes:**
  - General budget votes (e.g. final vote on the *valtion talousarvio*) and omnibus tax law votes are block votes and do not constitute Grade A evidence. Only single-issue motions, signed committee reservations, and verbatim debate speeches qualify.

---

## 3. Members, parties, seats

- **Official member register:**
  - Table: `https://avoindata.eduskunta.fi/api/v1/tables/MemberOfParliament/rows`
    - Contains `personId`, `firstname`, `lastname`, `party`, and XML biography chunks (`XmlDataFi`, `XmlDataSv`).
  - Active seating chart: `https://avoindata.eduskunta.fi/api/v1/tables/SeatingOfParliament/rows`
  - Current seats in Eduskunta: 200 seats, elected from 13 constituencies.
  - Wikidata coverage: Finnish MPs have complete Wikidata coverage (P39: member of the Parliament of Finland), with dates of death (P570) tracked.

---

## 4. Other official records

- **Valtion taloudellinen tutkimuskeskus (VATT) & Palkansaajien tutkimuslaitos (LABORE):**
  - Research papers evaluating capital taxation and wealth distribution.
- **Finnish Tax Administration (Verohallinto):**
  - Historical wealth-tax statistics published up to tax year 2005.
- **Municipal councils (Kunnanvaltuustot):**
  - Municipalities in Finland levy municipal income tax (*kunnallisvero*) and property tax (*kiinteistövero*). Municipalities have no statutory authority to levy net wealth taxes. A sample across the five largest cities (Helsinki, Espoo, Tampere, Turku, Oulu) confirmed no municipal wealth-tax motion exists.

---

## 5. Access notes

- `avoindata.eduskunta.fi`: fully functional REST API. Requires standard User-Agent header (`Mozilla/5.0`); default empty urllib user agent returns 403.
- `eduskunta.fi/pdf/<Doc>`: open and fast direct PDF downloads.
- `s3-eu-west-1.amazonaws.com/eduskunta-avoindata-documents-prod/`: open AWS S3 storage for plenary transcripts and motions.
- Windows encoding: Finnish uses characters `ä`, `ö`, `å`. Always invoke Python with `-X utf8` (`python -X utf8 ...`) to prevent `cp1252` encoding exceptions on stdout.

---

## 6. Coverage log

| Date | Run | Documents read (title, number, date) | Result (rows added, votes found) | Not read / open |
|---|---|---|---|---|
| 2026-10-27 | R001 | LA 55/2012 vp, TPA 25/2022 vp | 50 MP cosponsors/signatories added; 1 deceased excluded | Older initiatives |
| 2026-10-27 | R002 | VaVM 53/2010 vp, VaVM 25/2014 vp | 4 signed reservation authors added | LA 63/2010, TAA 422/2010 co-signers |
| 2026-11-01 | R003 | LA 81/2006, LA 84/2009, LA 63/2010, LA 62/2014 | 2 living signers added; pre-2010 signers linked | TAA 422/2010 co-signers |
| 2026-11-09 | R004 | TAA 422/2010 vp, TAA 166/2010 vp, TAA 107/2010 vp, LA 63/2010 vp, LA 62/2014 vp, PTK 116/2025 vp, PTK 69/2026 vp, PTK 65/2024 vp, PTK 49/2026 vp, PTK 69/2023 vp, PTK 112/2012 vp, PTK 113/2012 vp | 4 new supporters added (Esa Lahtela, Marjaana Koskinen, Matti Kangas, Jessi Jokelainen); 10 new evidence rows (including 2 plenary speeches); TAA 422/2010 gap solved; 4 resources added to `resources.json` | None in post-2010 legislative records |

---

## 7. Known gaps and next steps

- Post-2010 national legislative initiatives and plenary debates are exhaustively checked.
- Finnish MEPs' individual statements on EU-wide or international wealth-tax initiatives (e.g. Merja Kyllönen).
- Academic and think-tank reports (LABORE, SOSTE, Kalevi Sorsa säätiö).
- Swedish-language and Åland political coverage.
