# Area profile — Switzerland

Written 2026-10-31 (run R001, seed pass). Lines marked `[verify]` come from a search summary only and were not read at the source.

## 1. Scope
- Area: Switzerland (country; federal state of 26 cantons).
- Depth: Seed. National layer (the Federal Assembly, parties, economists, a wealthy supporter) plus cantonal initiatives found through the discover step. Cantonal parliaments, cantonal party sections and the 2,110 municipalities were **not** swept: the register loads them (so the map and later runs work) and leaves every unit `pending`.
- Levels of government in scope: national, regional (cantons). Local (municipalities) loaded, not searched.
- Languages searched: German, French, English, Italian (see `queries.csv`).
- Date of first run: 2026-10-31.

## 2. Wealth tax history and live proposals (2010 onwards)
- **A wealth tax already exists in every canton** (and in the communes); the federal level has none. So the live question is mostly whether to raise it, defend it, or add a federal one, not whether to introduce it. Support for "keeping and raising the existing tax" fits `defend_existing` and `annual_net_wealth` in this register.
- **Federal motions in the National Council** (official texts and per-member votes from the Swiss Parliament's open data, `ws.parlament.ch`):
  - 20.3174, Denis de la Reussille (PdA/Greens group): Covid-19 solidarity tax on wealth over CHF 3 million. Rejected 22 Sep 2021, 65 yes, 118 no.
  - 20.3335, Stefania Prezioso Batou: temporary federal wealth tax of 1% on wealth over CHF 2 million for three years. Rejected 15 Mar 2022, 66 yes, 127 no.
  - 20.3203, Social Democratic group: temporary solidarity levy on wealth over CHF 1 billion for a Covid-19 fund. Rejected 15 Mar 2022, 66 yes, 126 no.
  - 23.3361, Stefania Prezioso Batou (Ensemble à Gauche): change Art. 128 of the Constitution to introduce a direct tax on the wealth of natural persons. Rejected 13 Mar 2024, 60 yes, 132 no.
  - 24.3761, Barbara Schaffner (Green Liberals): asks the Federal Council to examine federal wealth-tax models. A request to study, so not recorded as support (see `exclusions.csv`).
- **Cantonal initiatives:**
  - Zurich, "Faire Finanzierung der Corona-Hilfen" (AL, SP, Greens, Juso, Junge Grüne, CSP, GBKZ, Travail.Suisse): temporary 20% surcharge on the top wealth-tax bracket for three years; withdrawn by its committee in August 2023 before a vote (AL statement, 11 Aug 2023).
  - Schaffhausen: Corona solidarity surcharge of 0.3 per mille on taxable wealth over CHF 2 million for five years, launched by the SP with AL and Greens; rejected 15 May 2022 with almost 69% against (SRF).
  - Geneva IN 185, "Pour une contribution temporaire de solidarité sur les grandes fortunes": 2.5 per mille on the part of a fortune above CHF 3 million for ten years (official initiative text; the 4.5 to 5 per mille in its own memorandum includes the centimes additionnels). Put to the vote on 18 June 2023 and rejected [verify the margin; one source says 59.5%]. In the Grand Conseil debate of 1 Sept 2022 (official minutes) Jean Batou (EAG), Pierre Eckert (Greens) and Sylvain Thévoz (SP) spoke for it, and the Conseil d'Etat's majority proposed a counter-proposal keeping the contribution for five years; the initiative went to the tax commission.
  - Neuchâtel, POP initiative "Pour une fiscalité plus équitable": higher wealth-tax rate from CHF 500,000. Rejected at the ballot on 15 May 2022 [verify; the cantonal voter pamphlet marks it NON].
  - St. Gallen: initiative to replace the flat wealth-tax rate by a progressive scale [verify; seen only in a search summary].
- **Outside the definition (not recorded):** the Juso initiative "For a future" (50% federal inheritance and gift tax above CHF 50 million) was rejected on 30 Nov 2025 by about 78% [verify]; the 99%-Initiative (capital income) was rejected in 2021. Both are inheritance or capital-income taxes.
- **After the Juso vote:** the billionaire Alfred Gantner (Partners Group) called for a progressive wealth tax on the very rich (1% above CHF 200 million, rising with wealth), 1 Dec 2025 (vol.at, zentralplus). In February 2026 Marius Brülhart (Lausanne) argued for a federal wealth tax instead of higher VAT or payroll levies to finance the 13th AHV pension and defence (SRF, 23 Feb 2026).

## 3. Legislatures and where their records are
- **Federal Assembly** (National Council 200, Council of States 46). Open-data API `https://ws.parlament.ch/odata.svc/` (OData, JSON with `Accept: application/json`): `Business` (motions, with `SubmittedText`), `Vote` and `Voting` (every member's vote on a recorded vote), `MemberCouncil` (party, canton, dates, date of death). Curia Vista pages are JavaScript and cannot be read by the quote checker; the API URLs can. Use `$filter` and a `$select` made only of real field names (an invalid `$select` answers 400).
- Cantonal parliaments: not yet read. Zurich (`parlzhcdws.cmicloud.ch`), Geneva (`ge.ch/grandconseil`, minutes and initiative texts as PDF), Neuchâtel (`ne.ch/autorites/GC`) and St. Gallen (`ratsinfo.sg.ch`) publish motions and reports.

## 4. Parties
- Left of centre, with positions on wealth taxation: Social Democratic Party (SP/PS), Greens (GPS/Verts), Swiss Party of Labour (PdA/POP), Alternative Liste (AL), solidaritéS/Ensemble à Gauche. In the 2021 to 2024 votes on the motions above, only SP and Greens members (and one AL/Zug Green) voted yes; no member of another group did.
- Green Liberals: a federal wealth-tax study request (24.3761) and a reported proposal for a federal wealth tax with a CHF 5 million exemption [verify], so a possible further layer.
- Right and centre parties oppose; opponents are not recorded.

## 5. Government below national level
- 26 cantons (regions in the register, ISO 3166-2 codes), 2,110 municipalities (council tier, BFS numbers, state of 1 Oct 2026), loaded from the BFS Historised Municipality Directory (`agvchapp.bfs.admin.ch/api/communes/snapshot?date=01-10-2026&format=csv`; the file is Windows-1252). Districts (Bezirke) are not loaded: they are not general-purpose local government and several cantons have none.
- What each level taxes: cantons set the wealth tax rate and base (communes levy it as a multiple); the Confederation has no wealth tax, so federal actors call for a new constitutional basis (Art. 128).
- Map: swisstopo swissBOUNDARIES3D 2026-01 (free use, source reference required; see `meta.json`).
- **Local decision:** not sampled in this run. Municipal councils mostly have no say over the wealth tax; the aggregators (cantonal parties and unions) are the better source, so a sweep unit by unit is not recommended.

## 6. Search terms
- German: Vermögenssteuer · Vermögensabgabe · Solidaritätsabgabe auf Vermögen · Millionärssteuer · Reichensteuer. Watch for: *Erbschaftssteuer* (inheritance tax, outside the definition) and *Vermögenssteuer* meaning the existing cantonal tax.
- French: impôt sur la fortune · contribution de solidarité sur les grandes fortunes · taxe Zucman. Italian: imposta sulla sostanza (the Swiss term) · imposta patrimoniale. Watch for *impôt sur les successions*.
- Roll-call motions are found by title through the API (`substringof('Vermögenssteuer',Title)`; also `Solidaritätsabgabe`, `Millionäre`, `Superreiche`).

## 7. Media
- SRF, NZZ, Tages-Anzeiger, Blick (blocks plain fetches with 403), swissinfo.ch, Le Temps, RSI, zentralplus, vol.at. Bloomberg Tax covered the Juso vote.

## 8. Registers
- Lobbying and donations: Swiss Parliament interest bindings (not used in this run). Commercial register (zefix.ch) not used.

## 9. Known networks
- Tax-justice side: SP/Juso, Greens, AL, unions (SGB/USS, Travail.Suisse, Unia, cantonal union federations such as GBKZ), Oxfam Switzerland, Alliance Sud, Public Eye (all unchecked).
- The Juso campaign for the inheritance tax brought out many figures (Juso leaders, SP, Greens) who may also back a wealth tax.

## 10. Plan for the next runs
Ordered by expected yield per turn:
1. **Council of States and earlier National Council votes** (2010 to 2019): query `Business` for earlier SP and Green motions and initiatives that asked for a wealth tax or a levy on large fortunes, and take the Ja votes (same method as H0001 to H0003). Expect a few dozen additional names, many new.
2. ~~Seats tab~~ done in this run with the `ch` adapter in `seats.py`; rerun it after each addition.
3. **Cantonal parliaments with initiatives:** Geneva IN 185 (committee, parties, the Grand Conseil debate and vote), Neuchâtel POP initiative, St. Gallen initiative, Aargau 2016 "Millionärssteuer", Basel-Stadt, Bern, Vaud, Ticino. Read each cantonal source first (see leads).
4. **Organisations:** SGB/USS, Unia, Travail.Suisse's own publications, Oxfam Switzerland, Alliance Sud, Public Eye, Greens Switzerland (the party as an actor), Juso.
5. **Economists and academics:** Isabel Martínez, Reto Föllmi (has a wealth-tax alternative in the SRF piece, not support), the authors of the 2025/26 "Wealth and Inheritance" study, signatories of any open letter.
6. **Wealthy and business supporters:** Swiss signatories of Millionaires for Humanity, Patriotic Millionaires and similar letters; follow-ups to Gantner's interview.
7. **Polls:** a poll on a wealth tax (not an inheritance tax) for `meta.json`; none was checked.
- Decisions that changed the default: districts left out of the register; municipal sweep skipped (see section 5).
