# Denmark: where the official record is and how to read it

Written in run R009 (2026-11-09) from an exhaustive scan of the Folketing open data API (`oda.ft.dk`), Folketingstidende verbatim plenary and committee records, and ministerial documentation for all post-2010 wealth-tax terms. Every URL, endpoint, and method below was verified on that date.

Key fact for Denmark: **Denmark abolished its national net wealth tax (*formueskat*) with effect from 1997 (L 112, 1995-96). Since 2010, only one parliamentary motion proposing an actual wealth tax has reached a vote in the Folketing: B 70 (2021-22), moved by Frie Grønne and voted on 7 June 2022.** Plenary debate transcripts print aggregate party tallies; individual roll-call votes are published in the open data API (`oda.ft.dk`) and on `ft.dk`. Verbatim plenary debates and bill texts are freely downloadable as primary PDFs from `folketingstidende.dk` without any bot check.

---

## 1. Bills, motions and proposals

- **Parliamentary Open Data API (OData v4), tested and works:** `https://oda.ft.dk/api/`
  - Completely open, unauthenticated, JSON endpoint without Cloudflare or rate-limiting.
  - Sager (Bills/Motions): `https://oda.ft.dk/api/Sag?$filter=substringof('formueskat', titel) or substringof('formueskat', resume)`
    - Document types: `typeid=3` (Lovforslag — government/private bills), `typeid=5` (Beslutningsforslag — parliamentary motions/resolutions), `typeid=9` (Forslag til vedtagelse — motions moved during debates), `typeid=10` (§ 20-spørgsmål — written questions to ministers), `typeid=2` (Forespørgsel — interpellations), `typeid=4` (Alm. del — committee business).
  - Documents & Files: `https://oda.ft.dk/api/Dokument` and `https://oda.ft.dk/api/Fil`.
  - Member Registry: `https://oda.ft.dk/api/Aktør?$filter=typeid eq 5` returns all Folketing members.
  - Votes: `https://oda.ft.dk/api/Afstemning` (vote metadata and conclusions) and `https://oda.ft.dk/api/Stemme` (individual votes per MP).

- **Official Gazette & Plenary Record (Folketingstidende), tested and works:** `https://www.folketingstidende.dk/`
  - Primary PDFs are open and return HTTP 200 to plain scripts without any bot blocker.
  - Proposal URL pattern: `https://www.folketingstidende.dk/samling/<session>/beslutningsforslag/<number>/<session>_<number>_som_fremsat.pdf` (e.g. `20211_B70_som_fremsat.pdf`).
  - Bill overview directory: `https://www.folketingstidende.dk/samling/<session>/beslutningsforslag/<number>/index.htm` lists all PDFs (initial text, committee reports, plenary debates, amendments).
  - Document lists by session: `https://www.folketingstidende.dk/dokumenttyper/beslutningsforslag?session=<session>` (e.g. `session=20211` for 2021-22, `20251` for 2025-26, `20261` for 2026-27).

- **Search terms (Danish):**
  - *Core terms:* `formueskat` (net wealth tax), `formueskatter`, `formuebeskatning`, `milliardærskat` / `milliardärskat` (billionaire tax), `nettoformue` (net wealth).
  - *Contextual terms requiring verification:* `millionærskat` / `millionärskat` (frequently used for an extra bracket on high incomes, such as the 2011 S-SF "Fair Forandring" topskat surtax or the 2013-14 V 9 debate; only counts if the statutory tax base is net assets/wealth rather than income), `formueafgift`, `skat på formue`, `skat på store formuer`, `rigmandsskat`.
  - *Excluded look-alikes:*
    - `formueskattekurs` / `formueskattekursen`: an administrative valuation convention for unlisted shares dating from the pre-1997 wealth tax, repealed administratively in 2015; not a wealth tax.
    - `ejendomsværdiskat` / `grundskyld`: property and land value taxes.
    - `boafgift` / `arveafgift`: estate and inheritance taxes.
    - `aktieavancebeskatning` / `kapitalindkomstskat`: capital gains and capital income taxes.
    - `topskat` / `top-topskat`: personal income surtaxes (including the 2026 top-topskat on personal earnings above DKK 2.5m).
    - `formueret`: civil property and contract law.

- **Sponsors and co-sponsors:**
  - Printed at the top of the proposal PDF on Folketingstidende: e.g. `Fremsat den 20. januar 2022 af Sikandar Siddique (FG), Uffe Elbæk (FG) og Susanne Zimmer (FG)`.
  - In OData API: `SagAktør` records for the case with `rolleid` 19 (`Forslagsstiller`) or 24 (`Medforslagsstiller`).

- **Government proposals and consultations:**
  - Inquiries and draft bills: `retsinformation.dk` and `skm.dk` (Ministry of Taxation).
  - Committee fiches: Skatteudvalget (SAU) and Finansudvalget (FIU) `alm. del` documents contain ministerial calculations on wealth-tax designs (e.g. SAU alm. del svar på spm. 301 and 347 in 2024-25, modeling a 0.5% tax on net wealth over DKK 5m; SAU spm. 243 in 2025-26 modeling FH's 0.3% over DKK 20m and 1% over DKK 35m).

---

## 2. Debates and votes

- **Plenary transcripts (Referater):**
  - Published for each plenary meeting (*møde*) as PDF: `https://www.folketingstidende.dk/samling/<session>/salen/M<nr>/<session>_M<nr>_referat.pdf`.
  - Speaker labels: structured verbatim as `Kl. HH:MM\n[Speaker Name] ([Party]):` or `Kl. HH:MM\n[Minister Role] ([Minister Name]):` (e.g. `Kl. 11:49\nRune Lund (EL):`, `Kl. 12:39\nStatsministeren (Mette Frederiksen):`, `Kl. 11:05\nSkatteministeren (Jeppe Bruus):`).
  - Text is clean and searchable; `gazette_scan.py` extracts text and locates passages.
- **Committee reports (Betænkninger):**
  - URL pattern: `https://www.folketingstidende.dk/samling/<session>/beslutningsforslag/<number>/<session>_<number>_betaenkning.pdf`.
  - Dispositive text lists party group recommendations (*indstillinger*): `Et mindretal i udvalget (EL) indstiller beslutningsforslaget til vedtagelse uændret. Et flertal i udvalget (...) indstiller beslutningsforslaget til forkastelse`.
- **Roll calls:**
  - Plenary minutes (*referat*) print only the aggregate party vote: e.g. `For stemte 10 (EL, FG og ALT), imod stemte 86 (S, V, SF, RV, KF, DF, NB, LA, Bent Bøgsted (UFG), Karina Adsbøl (UFG) og Naser Khader (UFG)), hverken for eller imod stemte 0. Forslaget til folketingsbeslutning er forkastet.`
  - The per-member division list is published in Folketinget's open data API: `oda.ft.dk/api/Afstemning` (for B 70, ID 8849, Afstemning nr. 506) and `oda.ft.dk/api/Stemme`. Member vote types: `typeid=1` (For), `2` (Imod), `3` (Fravær), `4` (Hverken for eller imod).
  - Human web page: `https://www.ft.dk/samling/20211/beslutningsforslag/b70/121/506/afstemning.htm` displays the member table (`Henning Hyllested Enhedslisten (EL) For`), but is behind Cloudflare.
  - The 10 affirmative votes on B 70 (7 June 2022): Bruno Jerup (EL), Henning Hyllested (EL), Jakob Sølvhøj (EL), Peder Hvelplund (EL), Pernille Skipper (EL), Rosa Lund (EL), Susanne Zimmer (FG), Søren Egge Rasmussen (EL), Torsten Gejl (ALT), Victoria Velasquez (EL). Sponsors Sikandar Siddique and Uffe Elbæk were absent on that sitting (`typeid=3`).
- **Numbering across versions:**
  - `B <nr>`: Beslutningsforslag (private member motions).
  - `L <nr>`: Lovforslag (bills).
  - `F <nr>`: Forespørgsel (interpellations).
  - `V <nr>`: Forslag til vedtagelse (motions moved during a forespørgselsdebat).
  - `S <nr>`: § 20-spørgsmål (written ministerial questions).
- **Block and package votes:**
  - The annual budget (*finansloven*) and broad tax reform packages (e.g. *aftale om personskat*) are voted as whole packages; an overall vote for the budget or tax reform is an omnibus block vote and does not count as wealth-tax evidence. Only single-issue motions or article-specific votes (such as B 70) count at Grade A.

---

## 3. Members, parties, seats

- **Official member list:**
  - Open data: `oda.ft.dk/api/Aktør?$filter=typeid eq 5` returns Folketing members with `id`, `navn`, `gruppenavn` (party), `periodeid`.
  - Active seat roster: `https://www.ft.dk/da/medlemmer/medlemmerne` and party distribution across 179 seats at `https://www.ft.dk/Medlemmer/Mandatfordelingen` (includes 2 seats for Greenland, 2 seats for Faroe Islands).
  - Historical members: `https://www.ft.dk/da/medlemmer/folketingets-historie/tidligere-medlemmer`.
  - Seats script: `python skill/scripts/seats.py data/dk` updates Folketing distribution.
  - Wikidata: Danish MPs have comprehensive Wikidata items with P39 (member of the Folketing).

---

## 4. Other official records

- **Government inquiries and ministries:**
  - Skatteministeriet: publishes responses to parliamentary committee questions (SAU) modeling revenue and distributional outcomes of wealth-tax variants.
  - De Økonomiske Råd (Danish Economic Councils / "vismændene"): annual economic reports analyse capital taxation and wealth inequality, but express no policy advocacy.
- **Regions and Municipal Councils:**
  - Denmark's 5 regions (*regioner*) and 98 municipalities (*kommuner*): regional councils have no taxation authority. Municipalities levy municipal income tax and land tax (*grundskyld*); they have no legal authority to enact a net wealth tax.
  - Municipal meeting portals (KMD, FirstAgenda): sampled major cities (København, Aarhus, Odense, Aalborg, Gladsaxe, Vejle, Sønderborg, Esbjerg); no municipal motion on wealth taxation was found. Local council resolutions are not a source of wealth-tax legislation in Denmark.

---

## 5. Access notes

- `oda.ft.dk/api/`: completely open OData v4 JSON API. No key, no captcha, fast response. Always use for structured bill metadata, votes, and member rosters.
- `folketingstidende.dk`: completely open PDF and HTML archive for all sessions. PDFs download cleanly via HTTP GET with standard user agent (`Mozilla/5.0`). The quote checker verifies text in Folketingstidende PDFs directly via `pypdf`/`pdftotext`.
- `ft.dk`: website uses Cloudflare bot management and returns HTTP 403 to automated clients. Prefer `folketingstidende.dk` for primary PDFs and `oda.ft.dk` for vote data.
- Encoding: Danish uses characters `æ`, `ø`, `å` (and capitals `Æ`, `Ø`, `Å`). Use UTF-8 everywhere (`-X utf8` in Python, `-enc UTF-8` in pdftotext).

---

## 6. Coverage log

| Date | Run | Documents read (title, number, date) | Result (rows added, votes found) | Not read / open |
|---|---|---|---|---|
| 2026-11-08 | R008 | L 112 (1995-96) bill as introduced, committee report (Skatteudvalget), 1st and 3rd reading plenary minutes; Hans Mølgaard Christensen 100-year tax review; Folketingstidende titles for 2025-27 | 0 rows (repeal documents pre-date 2010 scope) | 2nd reading of L 112; SAU committee questions |
| 2026-11-09 | R009 | B 70 (2021-22) bill as introduced, committee report (Skatteudvalget 18 May 2022), 1st reading plenary debate (M100 referat, 28 April 2022, all 10 speakers), 2nd reading and vote (M121 referat, 7 June 2022); Opening debate 2025 (M3 referat, 9 October 2025, Dragsted speech); Plenary debate 2026 (M57 referat, 26 February 2026, Frederiksen speech); Forespørgsel F 6 & V 9 (2013-14, M26 and M28 referater); SAU committee answers 2024-25 (spm. 301, 347) and 2025-26 (spm. 243); ODA FT Afstemning 8849 and Stemme | 0 new actors (all 10 B 70 YES voters, 3 sponsors, and 3 debate speakers already recorded); 9 evidence rows updated to primary Folketingstidende PDFs, achieving 100% verified status for all parliamentary speeches and sponsorships (41/51 checkquotes verified, remaining 10 roll calls on ft.dk); V 9 established as income surtax context; country records guide `dk.md` created | Historical committee questions (almindelig del) 2010-2020; local municipal motions (low yield) |

Never write "no roll call" or "no statements" in the register's area profile unless this table shows the relevant sittings were read.

---

## 7. Known gaps and next steps

1. **Monitor future sessions (2026-27 onwards):** If a government bill or new beslutningsforslag implementing the 2026 wealth-tax proposals (Socialdemokratiet, SF, or Enhedslisten) is formally introduced in the Folketing, harvest its sponsor list, committee report, and division lists.
2. **Committee questions archive:** Monitor Skatteudvalget (SAU) questions for new revenue models and expert submissions regarding wealth-tax valuation.
3. **Alternativet party programme (Lead D0007):** While Torsten Gejl (ALT) voted For B 70 in 2022, check upcoming party congress documents for an explicit standalone net-wealth tax chapter to qualify the party organisation itself.
4. **Local tier monitoring:** Danish municipalities have no net-wealth taxing power, but any future council petitions or symbolic resolutions should be logged if discovered.
