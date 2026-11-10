# Area profile — Sweden

First written 2026-10-19 (run R001). Lines marked *(to source)* were not yet checked against a page and must be sourced or removed in R002.

## 1. Scope
- Area: Sweden; type: country.
- Levels of government in scope: national (Riksdag, government), European Parliament (Swedish MEPs), regional (21 län / regions, regionfullmäktige) and local (290 kommuner, kommunfullmäktige). Below municipal level (kommundelsnämnder, church parishes) is out of scope.
- Languages to search in: Swedish (main), English. Minority languages (Sami, Finnish, Meänkieli, Romani, Yiddish) only for the Sami parliament and a few northern municipalities, and only if a hit suggests it.
- Date of first run: 2026-10-19.

## 2. Wealth tax history and live proposals (2010 onwards)
- The national wealth tax (*förmögenhetsskatt*) was abolished with effect from 1 January 2007, and the wealth declaration went with it. Sources: Riksdag motion [2017/18:2962](https://data.riksdagen.se/dokument/H5022962.html) ("avskaffad i Sverige sedan den 1 januari 2007"); motion [2021/22:2597](https://data.riksdagen.se/dokument/H9022597.html) (the declaration disappeared). Inheritance and gift tax went in 2004–05 and the state property tax in 2008 *(to source)*.
- Since 2010 the question has been raised in the Riksdag mainly through motions, not bills. A search of the Riksdag open data for motions from 2010-01-01 containing *förmögenhetsskatt* or *miljardärsskatt* gives 82 motions (query and list in `harvest.csv` H0001). Most are by opponents or only mention the abolished tax.
- Supporters in the Riksdag since 2010: Vänsterpartiet (annual calls for a study from 2011, a costed design from 2019), Miljöpartiet (motions 2013, 2016, 2017, and in 2026 a "miljardärsskatt"), the independent MP Amineh Kakabaveh (2020, 2021). The Social Democrats have been cautious: a 2020 motion by one MP asks for a review of "en ny förmögenhetsskatt"; the party leader rejected a billionaire tax in 2026 *(to source; not recorded: opponents are out of scope)*.
- Live proposals 2026: V wants an inquiry into a "särskild miljardärsskatt"; MP wants a billionaire tax on a Zucman model (2% on wealth over 100 million euro) ([TV4, 2026-05-18](https://www.tv4.se/artikel/45KWAtSv8KaMNZnITwLqXf/mp-och-v-kraever-miljardaerskatt-men-sagas-av-expert)). Oxfam Sverige proposes a wealth tax of 2%, 3% and 5% in three brackets ([Oxfam Sverige, Feb 2026](https://oxfam.se/wp-content/uploads/2026/02/Vart-Ojamlika-Sverige-Utsatthet-och-Extrem-Formogenhet.pdf)).
- Government and election: the Tidö government (M, KD, L with SD support) opposed new wealth taxes: M and SD motions praise the abolition and Moderate MPs attack the "miljardärsskatt" in the chamber (e.g. Lotta Björklund, 2026-10-15, [protocol 2026/27:8](https://data.riksdagen.se/dokument/HE098.html)). The general election was held on 13 September 2026. According to [Swedish Wikipedia's article on the election](https://sv.wikipedia.org/wiki/Riksdagsvalet_i_Sverige_2026) (secondary source, read 2026-10-19), the red-green side won: S 28.0% (99 seats), V 8.4% (30), C 7.0% (25), MP 6.1% (22) against M 19.9% (70), SD 17.5% (62), KD 6.2% (22), L 5.3% (19). Kristersson resigned on 17 September; as of 13 October 2026 the government formation had stalled (S, V and MP all demand to be in government; C refuses V). The outcome decides whether the V and MP billionaire-tax inquiry demands reach negotiations. R003 should re-check.
- S position: the Social Democrats have rejected a wealth tax in the chamber throughout (see `exclusions.csv` X0008). The line is "skatten på kapital behöver öka" without a wealth tax. One S MP, Joakim Järrebring, asked in a 2020 motion for a review of "en ny förmögenhetsskatt" (grade C). In 2010 the S-MP-V election motion proposed only a study of taxing the wealthy more.
- MP position: MP's economic spokesperson said on 2011-04-13 that the party would not pursue a wealth tax (X0007). MP MPs Lillemets and Mutt nevertheless moved to reintroduce it in 2013, 2016 and 2017, and the party's spring 2026 motion (section 6.5) asks for "en ny skatt för miljardärer" on a Zucman model.
- V position: V has asked for a wealth tax in every year of the window, first as a study (2011-2013), then with a costed design in budget motions 2019-2021 (SEK 6m threshold, 1-5%), and in 2026 as an inquiry into a billionaire tax. V's chamber speeches 2016-2017 also say "Vi vill återinföra förmögenhetsskatten".
- Reports and commissions: Katalys no. 75 "Beskatta kapitalet!" (Per Sundgren, 2019) *(to open and source)*. Konjunkturinstitutet's comparison of Swedish taxes for SNS (2019) is cited by V motions; it does not argue for a tax.
- Main moments: the 2010 election (S/MP/V joint "study a tax on the wealthy" line), the 2012–13 V budget motions, the Januari agreement 2019, the 2026 election campaign and Zucman's visit to Stockholm University (Realtid, 2026-04-01).

## 3. Legislatures and where their records are
- **Riksdag.** Motions, bills, votes and debates are in the open data API: `https://data.riksdagen.se/dokumentlista/?sok=<term>&doktyp=mot&from=2010-01-01&utformat=json`. Full text: `https://data.riksdagen.se/dokument/<dok_id>.text` (XML with the text inside; unescape it). Signatories: `https://data.riksdagen.se/dokumentstatus/<dok_id>.json`, `dokintressent`. Votes: `https://data.riksdagen.se/voteringlista/`. Search works well; the API returns every motion containing the term.
- **European Parliament.** Swedish MEPs' motions and votes via the European Parliament's open data portal *(to source)*.
- **Regionfullmäktige and kommunfullmäktige.** Minutes (protokoll) and motions are published on each municipality's or region's own site, often on the platforms Platsen, Ciceron/Open ePlatform, Meetings+ or "Insyn" *(to source and map in R003)*.

## 4. Parties
- Riksdag parties 2022–2026: V, S, MP, C, L, KD, M, SD. Party names to use in the `party` column (English common name): `Left Party`, `Social Democrats`, `Green Party`, `Centre Party`, `Liberals`, `Christian Democrats`, `Moderates`, `Sweden Democrats`, `Independent`.
- Manifestos since 2010 (V, MP, S, C) *(to collect in R002)*.

## 5. Government below national level
- 21 län, each with a regionfullmäktige (health care and regional development) and a state county administrative board (länsstyrelse); 290 kommuner, each with a kommunfullmäktige. Official list: SCB's region code list, loaded in `geo_units.csv` (21 + 290 units + 3 national/supranational). Source for the list: SCB table BE0101A (variable *Region*, retrieved 2026-10-19 via `api.scb.se`).
- Taxation: municipalities and regions levy only a proportional income tax and cannot introduce a wealth tax *(to source)*. Local actors therefore call on the Riksdag or government, and many local motions will be statements to the state, not decisions.
- Boundaries for the municipality map: [okfse/sweden-geojson](https://github.com/okfse/sweden-geojson) (municipalities, derived by that project from Valmyndigheten's boundaries via Opendatasoft), simplified further here.
- Municipal minutes: see section 3.

## 6. Search terms
| Term | Note |
|---|---|
| förmögenhetsskatt | The wealth tax; also used for the abolished 1947–2006 tax |
| miljardärsskatt, miljardärskatt, skatt på miljardärer | Billionaire taxes; both spellings occur |
| förmögenhetsbeskattning, skatt på förmögenhet, skatt på stora förmögenheter | |
| superrika, extrem förmögenhet, "betala på sin förmögenhet" | Context only; check the person's own words |
| exitskatt, utflyttningsskatt | Exit tax |
| förmögenhetsregister, förmögenhetsdeklaration | A register or declaration is **not** a tax on its own; record as `out_of_definition` unless a tax is also proposed |
| arvsskatt, gåvoskatt, fastighetsskatt, kapitalskatter | **Excluded** taxes, check that a wealth tax is also named |
| Zucmanskatt, Zucman | Billionaire minimum tax (2% above 100 million euro) |
- Ambiguous: *kapitalskatt*, *skatt på kapital* (income from capital); *fastighetsavgift* (municipal property fee); *värnskatt* (income tax surtax, abolished 2020).

## 7. Media
- National: Dagens Nyheter, Svenska Dagbladet, Aftonbladet, Expressen, Dagens Industri, Dagens Arbete, Dagens ETC, Arbetet, Flamman, Syre, Realtid, Affärsvärlden, Dagens PS, Ordfront, Tidningen Kontakt; SVT, Sveriges Radio, TV4. Regional press: local editions of NTM, Mittmedia/Bonnier, Gota Media *(to map in R003)*.
- Opinion-column writers and economists known to write on tax: to be collected in R002.

## 8. Registers
- Lobbying: none in Sweden *(to source)*. Charities: Bolagsverket and Svensk Insamlingskontroll *(to source)*. Party funding: Kammarkollegiet's party-support register *(to source)*.

## 9. Known networks
- Oxfam Sverige (recorded), Arena Idé (recorded, with Elinor Odeberg), SSU and S-studenter (recorded as youth wings, against the party line), LO (press report only), Tankesmedjan Katalys (neutral in its 2019 report; excluded for now), Tankesmedjan Tiden (opposes a new wealth tax in its 2020 report), Fair Finance, Attac Sverige, Diakonia, Forum Syd/Concord Sverige, Kristna Fredsrörelsen, trade unions (LO and its unions, TCO, Saco), Tax Justice Network and Patriotic Millionaires contacts, "Skattejusterarna". All to be checked in R002/R003.

## 10. Notes for future runs
- Pre-2010 motions (e.g. 2009/10:Sk342 by Ameer Sachet) are before the time window; the API's `from=2010-01-01` filter excludes 2009/10 motions submitted in autumn 2009.
- The Riksdag free-text search matches whole words only; also search stems and compounds (*förmögenhetsbeskattning*, *förmögenhetsskatten*, *miljardärer*, *superrika*).
- Wikidata's API rate-limits this environment's address hard; `Special:EntityData/<QID>.json` still worked, and the QID can be read from an article page's `wgWikibaseItemId`. The Riksdag person register (`data.riksdagen.se/personlista/`) flags deceased members as `Avliden`, which serves as the death check for MPs.
- Motions are quoted from `data.riksdagen.se/dokument/<id>.html`. The page splits some words with a soft hyphen, so choose quote spans that avoid a hyphenated word.

## 11. Run plan

Status after R001 (2026-10-19): 35 actors, 58 evidence rows, all `verified=n`. National Riksdag motions read; all 314 geography units pending except the Riksdag (in progress). Order follows the skill's priorities: bulk lists, then geography, then thin layers, then upgrades.

| Run | Focus | Targets and method | Done when |
|---|---|---|---|
| **R002** (done 2026-10-19, part 1) | National politics | Built `skill/scripts/adapters/se_riksdag_scan.py`. Reran the motion search, read interpellations, questions, committee reports and 196 plenary protocols; added the 2026 MP motion, 11 chamber speeches and 19 actors. Still open: H0002 roll calls (reservations in SkU reports), the 2026/27 motions, EP, and party documents (vansterpartiet.se blocks curl; use a browser) | Riksdag unit `done`; party rows backed by their own documents |
| **R003** (done 2026-10-19, part 1) | Civil society and unions | Added Arena Idé, SSU, S-studenter, LO (press report), Elfva Barrio, a second Oxfam source, and Odeberg's own words; Tankesmedjan Tiden, Katalys and an old LO report went to exclusions. Web search returned nothing for Attac, Diakonia, Fair Finance, ForumCiv, Kristna fredsrörelsen, Greenpeace, Ung Vänster, Grön Ungdom, TCO, Saco or any union congress: those need their own sites read with a browser | Every network in section 9 checked on its own site |
| **R003b** (done 2026-10-19) | Organisation and party sites | Read mp.se (MP billionaire-tax page, Helldén's Almedalen speech), ungvanster.se, gronungdom.se, feministerna.se, socialisterna.org. Added Ung Vänster, Grön Ungdom, Feministiskt initiativ and upgraded MP to grade A. **Blocked**: vansterpartiet.se (403 for all clients) and attac.se, fairfinance.se, kristnafredsrorelsen.se, rattvisepartiet.se (no connection); no results for the union and NGO sites searched | V manifesto 2026 and K26 motion answer obtained by a person with a browser |
| **R004** (done 2026-10-19, part 1) | Economists, academics, journalists, public figures | Added Kolsrud, Landais, Zucman's DN Debatt piece (via EFN), Arena Idé's own proposal (0.3% over SEK 10m) with its authors Odeberg and Österlund, Lisa Pelling, Tankesmedjan Tiden (2017 support, 2020 retraction) and five columnists in Arbetet, Arbetarbladet, Piteå-Tidningen and Arbetsvärlden. Johansson-Stenman, Östros and the opposing economists and business leaders are in exclusions. DN, SvD, Aftonbladet and Expressen cannot be searched (crawler-blocked); use allowed_domains for the other outlets | Coverage grid has no empty row for a type that has evidence |
| **R005** (part 1, 2026-10-19) | Local sweep: Stockholm region | Built `skill/scripts/adapters/se_meetingplus_scan.py`. Full-text protocol search is available in Stockholm, Huddinge, Danderyd and Region Gotland (MeetingPlus) and Nacka (own search): those 5 municipalities are `done` (3 actors found, all in Stockholm: V group, Lindblom, Mohammed, reservation 2020). The other 39 municipalities and 3 regions are pending: their sites are page-search or PDF folders, and web search cannot prove absence | All 44 units `done` |
| **R006** (sample, 2026-10-19) | Local: Västra Götaland, sampled | Surveyed all 49 municipal sites. Full-text search exists only in Göteborg (2023 on): 0 qualifying hits. Downloaded and read protocol PDFs of Trollhättan (70, 0 hits); Borås and Skövde crawls were stopped. Web searches on Göteborg, Region VG, Borås, Trollhättan and Skövde found nothing. **Sample yield: zero**, so no crawler is justified | Stop unit-by-unit sweeping |
| **R007** (part 1 done 2026-10-19: Reformisterna, Annie Ross, Moska Hassas, Seim, Ring, 11 local V/MP voices from three local-paper debate articles; unions, faith, climate NGOs, pensioners: nothing found) | Aggregators and remaining first-pass gaps | Local support, where it exists, shows up through lists, not unit-by-unit searches: Vänsterpartiet and Miljöpartiet lists of local groups and councillors who signed or moved the party's wealth-tax proposals, V congress motions (K26) and their movers from named districts, MP and S congress motions, regionfullmäktige motions in Stockholm, Skåne and Västra Götaland (largest regions), local V groups' own sites and local ledare via allowed_domains. Plus open first-pass items: H0002 roll calls and reservations, 2026/27 motions, EP, Oxfam 2023/2025 reports, Patriotic Millionaires, DN page 2, SvD/Aftonbladet author pages, faith voices, Wikidata IDs | Every layer touched; yield per hour reported |
| **R008** (sample done 2026-10-19) | Sample of 10 large municipalities | Web search in local papers and party pages for Malmö, Uppsala, Umeå, Örebro, Eskilstuna, Västerås, Lund, Helsingborg, Göteborg, Jönköping: zero finds. **Decision: stop municipal sweeps** (skill 6.5). The remaining units stay `pending` | Sample decision written here |
| **R009** (part 1, 2026-10-19: DN topic page and search scan, Piketty and Sjöstedt rows; leads listed in runs.csv) | QA and the remaining first-pass gaps | Second-person verification of all rows; Wikidata IDs; DN page 2, SvD and Aftonbladet author pages; union and Swedish economists; H0002 roll calls; 2026/27 motions; S congress motion book; EP | No `verified=n` in A-grade rows |
| **R011** | QA and upgrades | Run `validate`, `dedupe`, `checkquotes` on all rows; a second person (or a separate agent that did not write the rows) opens sources and sets `verified`; upgrade C and B actors; check retractions; resolve the municipality-map licence; add MP constituencies to `location` once a constituency layer exists; update `meta.json` status | No `verified=n` rows left in A-grade evidence; saturation reported |

Tooling: adapters `se_riksdag_scan.py` and `se_meetingplus_scan.py` exist. Do not build further municipal crawlers unless a sample shows hits (skill 6.5).

Update sweeps after completion: re-run H0001 each autumn (budget motions, October) and each spring (spring bill motions, April-May).


## Resources pass (1 November 2026)

Listed on the Resources page after reading each source: three private motions to the Riksdag that are about the wealth tax itself, read on data.riksdagen.se together with the Riksdag's recorded outcome (all rejected): 2009/10:Sk342 (Ameer Sachet, S), 2013/14:Sk403 and 2016/17:2632 (Lillemets and Mutt, MP). The Verian poll for Oxfam Sverige was already in `meta.json`.

Not listed: the Vänsterpartiet budget and spring motions (2019/20:2915, 2021/22:3278, 2025/26:4108 and others) and the MP and S motions on capital taxes; they mention a wealth tax inside a whole tax-policy programme, with no separate proposal on it. The Riksdag's motion search (data.riksdagen.se, query förmögenhetsskatt) was read through 2005 and no other dedicated wealth-tax motion since 2016/17 turned up.

Leads not yet listed:
- Arena Idé, "Skatt på kapital – Skatteöversyn delrapport 3" (March 2026, Odeberg and Österlund): proposes a wealth tax of 0.3% on net wealth above SEK 10 million (at least SEK 23 billion a year) but as one of several capital-tax measures in a 100 billion package, so left out as a whole-reform report; the earlier delrapporter and the Tankesmedjan Tiden reports of 2017 and 2020 are of the same kind.
- Verian poll for Oxfam Sverige (June 2026): done in the second pass; the poll in `meta.json` now links Oxfam's own news item of 11 June 2026, with fieldwork 26 to 28 May 2026 and the sample description. The exact question wording is not in Oxfam's release.
- Oxfam Sverige's report "Vårt ojämlika Sverige" (February 2026): the PDF is over 10 MB and was not read.
- Åsa Hansson, "Förmögenhetsskatten som symbol", Ratio Working Paper 39 (2002): read the abstract only; the month of publication is not shown.
- Press-only polls on a Swedish wealth tax (a Dagens PS item of 23 September 2025 on a poll for Zucman's proposal turned out to be about France) were not found with a pollster's release.

### Research runs R012–R025 (2026-11-06)

New entries draw on Swedish Social Democratic congress motions, local official records, climate advocacy, Oxfam authors and party programmes. The quote checker could not access these sources from this environment; the underlying article and motion texts were inspected through browser-readable pages, including the congress PDF. Local motions were attributed to adopting associations or named authors, not automatically to forwarding or national party organisations. The 2021 motion book remains in progress (H0007); several signers need identity and public-role checks. IF Metall's 2025 motion on a wealth register does not itself endorse a wealth tax.

## Review corrections (2026-11-07)

- Removed three motion authors who hold no public office (Lennart Hallengren, Håkan Andersson, Jennie Östlund; exclusions X0019-X0021, private_individual): party organiser, district officer and delegate, and unelected candidate. The other motion authors hold or held municipal or council offices and stay.

## Records pass (R026, 2026-11-08)

Guide: `skill/references/records/se.md`. Documents tracked in `documents.csv`: 385 (119 read, 266 partial, 0 skimmed, 0 unread); the register's 3 Resources-page motions are among them. By kind: 113 motions (32 core), 51 interpellations and questions, 82 committee reports and opinions, 134 chamber protocols with a Left or Green Party speaker, 1 bill, 2 inquiries, 2 vote records. "Read" means a motion short enough that the whole text was scanned; "partial" means every passage with the term and the signature block or speaker label were read, not the whole document (budget motions, committee reports, protocols).

What the record shows (2006/07 to 2026-11-08):
- **Motions.** The API returns 175 motions for the wealth-tax terms (the 82 of H0001 were from 2010 and a narrower search). The motions from 2010 to 2026 that call for or prepare a wealth tax are the Left Party's budget and spring motions of 2011 to 2013 (study of a tax "to be introduced" 2014/2015), 2013 (Sk201 and Fi254: "Vänsterpartiet menar att det bör finnas en förmögenhetsskatt"), 2019 spring (3093), 2019 and 2020 budget (2915, 3170: a design with SEK 6 m threshold), 2021 (3278), 2026 (4108); the Green Party's 2013, 2016, 2017 and 2026 motions; Kakabaveh 2020 and 2021; one S motion 2020. The Left Party's 2022 to 2025 budget motions describe the missing tax and ask for an inquiry into *egendomsskatter* (property and estate taxes): a study request, not recorded. M, FP, KD, C, L and SD motions (133 not tracked individually) mention the tax only to praise the abolition or warn against its return.
- **Signatories.** The 2013 motions Sk201 and Fi254 and the 2019 to 2020 motions 3093 and 3170 had signatories not yet in the register: 28 signature rows (grade A, quoted from the member's printed entry), 5 new former members of the Riksdag (Torbjörn Björlund, Josefin Brink, Rossana Dinamarca, Christina Höj Larsen, Wiwi-Anne Johansson). The R001 note that the 2013 to 2018 V budget motions "mention the tax without a clear call" was wrong for 2013. Siv Holma (co-signer of Fi254) is deceased (exclusion X0022); Lena Olsson signed only a study request (X0023).
- **Debates.** The 393 protocols that contain a term were attributed to speakers: V (105 hits), MP (23), S (70, all rejecting or describing), M and the other parties (opponents). New supporting speeches: Sjöstedt 2015, Sestrajcic 2016, Wetterling 2021, Ulla Andersson 2018, Momodou Jallow 2017 (new actor) and a särskilt yttrande by Jacob Johnson 2014. Speeches whose only content is a description of the abolished tax, or that describe a study, were not recorded.
- **Votes.** None qualifies. 2016/17:SkU23 punkt 8 and 2017/18:SkU9 punkt 10 (the Green Party's wealth-tax proposal) were decided by acclamation; 2013/14:SkU17 punkt 1 is a bundle of 14 motions (named vote: S and V abstained, MP voted with the committee, so MP's vote is not a retraction); budget and spring-statement reports are block votes. No supporter retracted by vote.
- **Inquiries.** The Equality Commission (SOU 2020:46, part 2, "Skatter") calls reintroducing a wealth tax desirable and assesses it should be studied within a larger reform: recorded as a government body (E00230, grade B).
- **Local.** MeetingPlus portals (Stockholm, Huddinge, Danderyd, Gotland) re-searched with the stems; web search for Göteborg, Malmö, Uppsala, Region Skåne, Västra Götaland and Region Stockholm found no wealth-tax motion. Absence is not proven; see leads D0003.

Not read: whole budget motions and protocols page by page; the Left Party's congress motion book and 2026 manifesto beyond R003; the Riksdag's 2026/27 term after 2026-11-04; the European Parliament; municipal portals other than the four named.

## Records deep-dive pass (R027, 2026-11-09)

Official records deep-dive executed per `skill/SKILL.md` legislative records workflow.
- **Records guide:** Expanded and finalized `skill/references/records/se.md` detailing all open data API endpoints, parliamentary motion lifecycle, handling by Skatteutskottet (SkU) and Finansutskottet (FiU), acclamation vs roll call rules, plenary protocol structure, personlista, and SOU inquiries.
- **Riksdag Debates:** Scanned all 196 chamber protocols from 2010 to 2026 matching wealth-tax terms (`förmögenhetsskatt`, `miljardärsskatt`). Verified all 18 verbatim speech entries defending the tax (from Jacob Johnson, Annika Lillemets, Jonas Sjöstedt, Daniel Sestrajcic, Ulla Andersson, Momodou Jallow, Jens Holm, Amineh Kakabaveh, Tony Haddou, Jessica Wetterling, Nooshi Dadgostar, and Ilona Szatmári Waldau).
- **Bills and Resources:** Added 8 post-2010 qualified bills and SOU 2020:46 to `data/resources.json` (increasing total Sweden resources from 3 to 11) and corrected character encodings on existing items. Logged Motion 2025/26:4118 (M0386) in `data/se/documents.csv`.
- **Quote normalization:** Resolved Aspose soft-hyphen HTML word-splitting (`miljardärs</span><span>&#xad;</span><span>skatt`) in `skill/scripts/wtdb.py` and updated quotes for 10 Left Party signatories (E00033–E00042) to include the full tax phrase, successfully passing `checkquotes`.
- **Networking:** Enforced IPv4 socket preference in `se_riksdag_scan.py` and `wtdb.py` to prevent Windows IPv6 connection resets on `data.riksdagen.se`.
- **QA:** Ran `wtdb.py validate`, `wtdb.py dedupe`, `wtdb.py checkquotes`, and `review_scan.py`; 0 validation errors, 0 duplicates, all targeted quotes pass.
