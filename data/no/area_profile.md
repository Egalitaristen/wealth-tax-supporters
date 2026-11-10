# Area profile — Norway

First written 2026-10-22 (run R001).

## 1. Scope
- Area: Norway; type: country.
- Scope: Seed pass — prominent national supporters across all key layers, plus sampled regional (15 fylker / counties) and local (357 kommuner / municipalities).
- Levels of government in scope: national (Stortinget, regjeringen), regional (15 fylker / fylkeskommuner), and local (357 kommuner / kommunestyrer). Svalbard and Jan Mayen are not municipalities and are out of scope.
- Languages to search in: Norwegian (Bokmål and Nynorsk), English.
- Date of first run: 2026-10-22.

## 2. Wealth tax history and live proposals (2010 onwards)
- Norway is one of the few OECD countries with an **active, continuous annual net wealth tax** (*formuesskatt*), levied partly by the primary municipality (*formuesskatt til primærkommunen*) and partly by the state (*formuesskatt til staten*).
- Under the Solberg coalition government (2013–2021), the wealth tax rate was reduced from 1.1% to 0.85%, and valuation discounts on "working capital" (*arbeidende kapital* — shares and commercial assets) were introduced and increased up to 45% (2021).
- Under the Støre government (Arbeiderpartiet and Senterpartiet, with budget support from SV / Sosialistisk Venstreparti) from autumn 2021 onwards, the wealth tax was strengthened and increased:
  - 2022: Rate increased to 0.95% up to NOK 20m, and a second progressive bracket of 1.1% introduced for fortunes over NOK 20m. Share valuation discount reduced.
  - 2023–2024: Rates set to 1.0% (0.70% municipal + 0.30% state) for net wealth above the threshold (NOK 1.7m) up to NOK 20m, and 1.1% (0.70% municipal + 0.40% state) above NOK 20m. Valuation of shares/commercial property set to 80% (20% discount).
  - 2024–2026: Debates on the exit tax (*utflytterskatt*) following the relocation of several ultra-wealthy Norwegians to Switzerland, municipal attempts in Bø i Vesterålen and Asker to cut the municipal wealth tax rate, and the 2025–2026 government tax commission (*Skattekommisjonen*).
- Positions:
  - **Sosialistisk Venstreparti (SV)**: Demands a higher and more progressive wealth tax (additional bracket at NOK 100m at 1.8%, abolition of valuation discounts on shares, and strict exit tax).
  - **Arbeiderpartiet (Ap)**: Defends the wealth tax as essential for redistribution, against right-wing proposals to abolish it on working capital.
  - **Senterpartiet (Sp)**: Defends keeping the wealth tax and opposes abolition, while advocating higher thresholds and relief for local small/medium businesses.
  - **Rødt**: Demands steep progressive wealth taxation, national luxury tax, and closing loopholes.
  - **Miljøpartiet De Grønne (MDG)**: Supports progressive wealth taxation with high thresholds and higher rates for the ultra-rich.
  - **Opponents (exclusions)**: Høyre (wants to abolish wealth tax on working capital), Fremskrittspartiet (wants complete repeal), NHO.

## 3. Legislatures and where their records are
- **Stortinget (National Parliament):**
  - Open data REST API: `https://data.stortinget.no/` (free public XML/JSON export covering sessions, cases, questions, votes, and member biographies).
  - Web site: `https://www.stortinget.no/`
  - Wealth tax rates and thresholds are set annually in the budget bill *Innstilling fra finanskomiteen om skatter, avgifter og toll* (*Innst. 3 S*).
  - Key debates and votes also occur on representative proposals (*Dokument 8*).

## 4. Parties
- Major Storting parties:
  - `Labour Party` (Arbeiderpartiet, Ap)
  - `Socialist Left Party` (Sosialistisk Venstreparti, SV)
  - `Centre Party` (Senterpartiet, Sp)
  - `Red Party` (Rødt)
  - `Green Party` (Miljøpartiet De Grønne, MDG)
  - Opponents: `Conservative Party` (Høyre), `Progress Party` (Fremskrittspartiet, FrP), `Liberal Party` (Venstre), `Christian Democratic Party` (KrF).

## 5. Government below national level
- **15 fylker (counties):** Oslo (03), Rogaland (11), Møre og Romsdal (15), Nordland (18), Østfold (31), Akershus (32), Buskerud (33), Innlandet (34), Vestfold (39), Telemark (40), Agder (42), Vestland (46), Trøndelag (50), Troms (55), Finnmark (56).
- **357 kommuner (municipalities):** All loaded into `geo_units.csv` with official 4-digit SSB codes.
- Local taxation: Municipalities receive a fixed maximum share of the wealth tax (currently 0.70%), which goes into the municipal equalization system (*inntektsutjevningen*). A few municipalities (notably Bø i Vesterålen in 2020) reduced their local rate, sparking national debate.
- Boundary data: Kartverket (Norwegian Mapping Authority), *Administrative enheter kommuner og fylker* (2024), published under CC BY 4.0 via Geonorge.

## 6. Search terms
| Term | Note |
|---|---|
| formuesskatt, formueskatt | The wealth tax; both spellings used |
| formuesskatten | Definite form ("the wealth tax") |
| milliardærskatt, skatt på de rikeste | Billionaire tax, tax on the richest |
| formuesbeskatning | Wealth taxation |
| utflytterskatt, exit-skatt | Exit tax on unrealized gains / departing fortunes |
| arbeidende kapital | "Working capital" (the political battleground term in Norway) |

## 7. Media
- National dailies: *Klassekampen* (left daily, editorial defender of wealth tax), *Dagsavisen*, *VG*, *Aftenposten*, *Dagens Næringsliv* (business daily), *E24*, *FriFagbevegelse* (labour movement news).
- Broadcasters: *NRK* (public broadcaster), *TV 2*.

## 8. Registers
- Brønnøysundregistrene (`brreg.no`): official business and entity register.
- Stortinget open data: `data.stortinget.no`.
- SSB (Statistisk sentralbyrå): `ssb.no`.

## 9. Known networks
- LO (Landsorganisasjonen i Norge) and member unions (Fagforbundet, Fellesforbundet).
- Think tanks: Tankesmien Manifest, Tankesmien Agenda.
- NGOs & coalitions: Tax Justice Norge, Attac Norge, Kirkens Nødhjelp, Oxfam partners.

## 10. Plan for the next runs
- Order by expected yield:
  1. Storting roll calls on budget votes (Innst. 3 S) and parliamentary motions.
  2. Economists snowballing (Kalle Moene, Gabriel Zucman Norway visits/co-authors, Rolf Aaberge, Annette Alstadsæter).
  3. Regional and local sweep of key municipalities (Oslo, Bergen, Trondheim, Tromsø council groups).
  4. Business/wealthy voices (patriotic millionaires letters, business op-eds).

## Legislative records deep-dive (Run R016, 9 November 2026)

Conducted a comprehensive scan of Storting official parliamentary records from 2010 to 2026 using the official open-data API `data.stortinget.no` and primary PDFs from `stortinget.no`.

### Key Findings & Roll Calls:
1. **Annual budget votes are omnibus block votes:** The annual tax decisions (*Innst. 3 S* and *Innst. 4 L*) bundle wealth tax rates into broad revenue chapters (*rammeområde 21*). These package votes bundle corporate, income, and indirect tax measures together and are discarded under the register QA rules.
2. **Standalone Roll-Call Votes Identified:**
   - **Vote 2354 (29 May 2012)** on *Dokument 8:77 S* / *Innst. 281 S (2011–2012)*: Direct vote on Fremskrittspartiet's motion to abolish the wealth tax on working capital (*arbeidende kapital*). The committee recommendation that the repeal proposal *vedtas ikke* (shall not be adopted) passed 53 to 48. The 53 voting YES (39 Arbeiderpartiet, 7 Senterpartiet, 7 Sosialistisk Venstreparti) defended the wealth tax against repeal. One member, Bendiks H. Arnesen (Ap, Troms), died in November 2024 and was placed in `exclusions.csv` (`reason: deceased`). The remaining 52 members were verified living (`alive_checked=y`) and added with Grade A vote evidence.
   - **Vote 2352 (29 May 2012)**: FrP's direct repeal proposal rejected 79 Mot to 22 For.
   - **Vote 18557 & 18559 (26 April 2022)** on *Dokument 8:110 S* / *Innst. 237 S (2021–2022)*: Proposal to delay and exempt pre-1998 aquaculture concessions (*oppdrettstillatelser*) from the wealth tax base. The Storting rejected postponement 87–14 (Vote 18557) and adopted the committee recommendation rejecting the proposal 86–13 (Vote 18559).
3. **Plenary Speeches Defending the Tax:**
   - **Knut Storberget (A, Hedmark)**: Finance Committee rapporteur on Innst. 280 S and Innst. 281 S, defending the wealth tax as an established redistributive instrument.
   - **Geir-Ketil Hansen (SV, Nordland)**: SV parliamentary spokesperson on Innst. 281 S, defending the red-green tax policy ensuring the wealthiest contribute.
   - **Sigbjørn Johnsen (A, Hedmark)**: Minister of Finance in Stoltenberg II, defending the increasing progressivity and distributional impact of the wealth tax.
   - **Mona Nilsen (A, Nordland)**: Plenary debate speaker on Innst. 237 S (21 April 2022), defending progressive wealth taxation of large fortunes.
   - **Geir Jørgensen (R, Nordland)**: Plenary debate speaker on Innst. 237 S, arguing that multi-million commercial concessions must be taxed under the wealth tax.
4. **Documentation and Resources:**
   - Created country records guide `skill/references/records/no.md`.
   - Logged 13 primary documents in `data/no/documents.csv`.
   - Added 2 qualified bills to `data/resources.json` (*Dokument 8:77 S* and *Dokument 8:110 S*).


Listed on the Resources page after reading each source: the Storting's 2026 tax decision (Vedtak 212), which sets the wealth tax now in force (formuesskatt, an annual net wealth tax; the date of the vote is not on the page), the Skatteutvalget's NOU 2022: 20 (read through the Wayback copy of the ministry's news item of 19 December 2022, because regjeringen.no refuses scripts), and Marius Ring's paper in the Review of Economic Studies. No Norwegian poll on the wealth tax was listed: the only ones found were a 2013 InFact poll for VG known from press coverage and a December 2024 Respons Analyse survey of 400 businesses (on a host with a bad certificate), neither read from the pollster's release.

Leads not yet listed, because the document was not read or was not clearly about the wealth tax:
- NOU 2003: 9 (the Skauge committee) and NOU 2014: 13 (the Scheel committee), both cited in Storting papers on formuesskatt; regjeringen.no refused scripts and no archive copy was read.
- Storting private members' proposals on the wealth tax (for example Dokument 8:72 S (2012–2013) from KrF on working capital, Dokument 8:196 S (2020–2021) from FrP to remove it on business assets): the proposal text and outcome were not read. Dokument 8:97 S and 8:94 S (2025–2026) are about the valuation of homes, not the wealth tax itself.
- Statistics Norway's research project page *Hvordan virker formuesskatten?* (2022) describes a project and states no conclusion; Tankesmien Agenda's 2026 article, Langsikt's 2025 publication and Manifest Analyse's 2024 note are already evidence rows but were not read as reports.
- A DN poll on keeping the wealth tax (the snippet gave neither date nor pollster) and an Aftenposten end-of-campaign poll mentioned by Altinget.
