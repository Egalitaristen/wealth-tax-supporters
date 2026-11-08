# Norway: net wealth tax (formuesskatt), sourced fact sheet for the Arguments pages

Prepared 2026-11-08. Feeds the pages "the rich will leave", "you can't value it", "it doesn't raise enough" and "it hurts growth". Research only: no `data/` or `content/` changes.

## 0. How to read this sheet

- Every entry has: **Claim** (plain words), **Figure** (exact, with year), **Quote / table cell** (Norwegian original, then English translation), **URL**, **Opened** (date), **How opened**, and a **Status**.
- All entries were opened on **2026-11-08** unless a different date is shown.
- **How opened** uses these codes:
  - **API-full**: SSB StatBank table pulled in full through the official `data.ssb.no` API (the figures are the table cells; the URL given is the public StatBank page for the same table).
  - **PDF-full**: the PDF was downloaded and converted to text locally, and the quoted passages were read in that text.
  - **Page-extract**: a web page was fetched through a text-extraction tool that returns excerpts. Quotes are as returned by the tool and are short; I did not read the page end to end. Treat these as "opened, excerpted".
  - **Search-only**: seen only in a search-result snippet. Never used as the sole basis of a "verified" entry.
- **Blocked source.** `regjeringen.no` serves an automated-access wall (HTTP 403 for scripts, a "security verification" page in a browser). I did not try to get past it. Everything that exists only on regjeringen.no (the Tax Commission report NOU 2026:9, Prop. 1 LS, the ministry's tax-rate pages) is therefore in section 9 (could not verify), except where the Storting (`stortinget.no`) or Skatteetaten (`skatteetaten.no`) republishes the same fact.
- No Wikipedia numbers. No AI-chat-tool content. Media articles are used only as the "claim" side of the media-versus-statistics comparison, never as the evidence for a number; where a media figure is also an official figure, the official document is cited.
- Two kinds of "year" matter and are easy to confuse. SSB's table year (e.g. "2024") is the **income year** (wealth at 31 December 2024, tax assessed in 2025). Political and press years refer to when someone moved or when a budget was passed.
- "NOK" = Norwegian kroner. "mill." = million, "mrd." = billion (10^9). 1 BNOK = NOK 1,000 million.

### Sources opened in full (full text read, or the full table pulled)

| Source | Type | Code |
|---|---|---|
| SSB table 08815 (taxable wealth, debt and wealth tax; 1999-2024) | Official statistics | API-full |
| SSB table 08231 (wealth tax by size-of-tax bracket; 1999-2024) | Official statistics | API-full |
| SSB table 10799 (annual income and capital accounts by sector) | Official statistics (national accounts) | API-full |
| SSB table 05395 (migration to and from abroad; 1958-2025) | Official statistics | API-full |
| Finance Ministry answer to written question no. 1236 (Farahmand), 28 Feb 2025, Table 1 (Skattedirektoratet data) | Official, Storting document | PDF-full |
| Storting research service note 2024150, "Endringer i formuesskatten fra 2000 til 2024", 15 May 2024 | Official, Storting | PDF-full |
| Ring (2026), NBER Working Paper 35854, "Taxing Entrepreneurial Wealth: Evidence from Norway, 2021-2025" | Working paper (not peer reviewed) | PDF-full (text extracted from the whole PDF; abstract, introduction, revenue section and references read) |
| Civita note no. 26/2025, "Store formuer flytter ut av Norge" | Think-tank analysis of SSB register data | PDF-full |

### Sources opened as excerpts (Page-extract)

Skatteetaten tax-rate page (2025 and 2026 versions); Skatteetaten page on deferral of wealth tax on business wealth; Skatteklagenemnda decision SKNS1-2024-117; Skatteetaten press release of 19 Oct 2023 on foreign wealth; Innst. 172 S (2023-2024) with Riksrevisjonen's Document 3:3 (2023-2024); Minister of Finance answer to written question 15:1899 (2024-2025) from Tina Bru; Nettavisen 9 Jan 2024; NRK 16 May 2026; E24 3 Oct 2022; Fortune/Bloomberg 19 Apr 2024; abstracts of Iacono and Smedsvik (CESifo WP 11335), Bjorneby, Markussen and Roed (Economica 2023), Brulhart et al. (AEJ: Economic Policy 2022), Jakobsen et al. (QJE 2020), Fagereng et al. (Econometrica 2020), Ring (REStud 2025).

---

## 1. Newest data, read past the headlines

**N1. How many pay, and how much it raises (income year 2024, latest published).**
- Claim: In income year 2024, 719,007 taxpayers paid wealth tax, and the total was NOK 31,784 million.
- Figure: 2024: 719,007 persons; NOK 31,784 million; average NOK 44,200 per payer.
- Table cells (SSB 08815, row "Formuesskatt", variable "Skattepliktige med beløp" / "Beløp for skattepliktige (mill. kr)" / "Gjennomsnitt for skattepliktige med beløp (kr)"): `2024 | 719007 | 31784 | 44200`.
- Translation: "Taxpayers with an amount", "Amount for taxpayers (NOK million)", "Average for taxpayers with an amount (NOK)".
- Series from the same table: 2019: 560,020 / 16,599 / 29,600; 2020: 596,616 / 17,236 / 28,900; 2021: 667,022 / 18,454 / 27,700; 2022: 647,591 / 26,320 / 40,600; 2023: 671,646 / 29,399 / 43,800; 2024: 719,007 / 31,784 / 44,200 (persons / NOK million / NOK).
- URL: https://www.ssb.no/statbank/table/08815 (API: https://data.ssb.no/api/v0/no/table/08815)
- Opened: 2026-11-08. API-full. Status: **verified**. (The StatBank page shows the series ends at 2024; the search listing gave "1999 - 2024".)

**N2. Revenue grew 72% from 2021 to 2024 while the number of payers grew 8%.** (my arithmetic on N1)
- Figure: 31,784 / 18,454 = 1.722, i.e. +72.2%. Payers: 719,007 / 667,022 = 1.078, i.e. +7.8%. Average payment per payer: NOK 27,700 to NOK 44,200 (+59.6%). All nominal, not inflation-adjusted.
- Source: SSB 08815, as N1. Status: **verified** (arithmetic from verified cells).

**N3. Who pays: about 15% of adults, and nearly half of those pay under NOK 10,000.**
- Claim: In 2024, among 4,541,587 residents aged 17 and over, 3,840,105 had no wealth tax. So 701,482 residents (15.4% of adults) paid. 313,434 of them (44.7%) paid under NOK 10,000.
- Table cells (SSB 08231, "Bosatte 17 år og eldre", 2024): "I alt" 4,541,587; "Uten formuesskatt" 3,840,105; "Positiv formuesskatt under 9 999 kr" 313,434; "10 000 - 24 999 kr" 178,023; "25 000 - 49 999 kr" 105,635; "50 000 - 74 999 kr" 39,531; "75 000 - 99 999 kr" 19,186; "100 000 - 149 999 kr" 17,922; "150 000 - 199 999 kr" 8,207; "200 000 - 249 999 kr" 4,607; "250 000 - 299 999 kr" 2,904; "300 000 - 349 999 kr" 2,002; "350 000 - 499 999 kr" 3,435; "500 000 - 999 999 kr" 3,758; "1 000 000 kr og over" 2,838.
- Translation: "Residents 17 years and over"; "Total"; "Without wealth tax"; "Positive wealth tax under NOK 9,999"; and so on.
- Derived: 45,673 residents paid NOK 100,000 or more (my sum of the last eight bands; 34,979 in 2022). 2,838 paid NOK 1 million or more (2,572 in 2022; +10.3%). Average taxable net wealth of the NOK-1-million-plus band: NOK 296,832,700 (2024) and NOK 302,458,800 (2022).
- Why it matters: the number of residents paying NOK 1 million or more went **up** after the 2022 increase, even with the departures discussed below.
- URL: https://www.ssb.no/statbank/table/08231
- Opened: 2026-11-08. API-full. Status: **verified**. Note: N1 counts 719,007 "taxpayers with an amount" (all taxpayers, including non-residents); N3 counts residents only, so the two totals differ by design.

**N4. Wealth tax as a share of GDP and of taxes (2024).**
- Claim: NOK 31,784 million is 0.59% of Norway's GDP in 2024 and about 1.5% of general-government tax and contribution receipts.
- Figures (SSB 10799, sector "Sum innenlandske sektorer", current prices, NOK million, 2024): "= BRUTTONASJONALPRODUKT, markedsverdi" 5,382,441. Government sector ("Offentlig forvaltning") receipts, 2024: "+ Skatt på inntekt og formue" 1,079,576; "+ Merverdi- og investeringsavgift" 386,600; "+ Produktskatter" 96,510; "+ Næringsskatter" 41,609; "+ Toll" 3,511; "+ Arbeidstakers trygde- og pensjonspremier" 197,155; "+ Arbeidsgivers trygde- og pensjonspremier" 295,410.
- Translation: "= Gross national product, market value"; "+ Tax on income and wealth"; "+ VAT and investment tax"; "+ Product taxes"; "+ Business taxes"; "+ Customs"; "+ Employees' social security and pension contributions"; "+ Employers' ...".
- Derived by me: 31,784 / 5,382,441 = **0.59%** of GDP. Sum of the seven government lines = NOK 2,100,371 million; 31,784 / 2,100,371 = **1.5%**. Against the single line "tax on income and wealth" only: 2.9%.
- Caveats: (a) this GDP includes oil and gas and shipping, so the share of "mainland" GDP is higher; I did not pull mainland GDP, so no mainland figure is given. (b) The "income and wealth tax" line includes petroleum taxes (the 2022 value of NOK 1,552 bn reflects the energy-price spike), so the 1.5% and 2.9% shares are lower than they would be for a mainland-only denominator. (c) These ratios are my computation from two SSB tables, not an SSB-published ratio. State the denominator whenever used.
- URL: https://www.ssb.no/statbank/table/10799
- Opened: 2026-11-08. API-full. Status: **verified (arithmetic)**; needs the caveats when used.

**N5. Rates and thresholds, 2022 to 2026.**
- Claim: The headline rate on wealth above the allowance has been around 1% since 2023, with 1.1% on the top slice. The allowance rose from NOK 1.7m (2022-2024) to NOK 1.76m (2025) and NOK 1.9m (2026).
- 2022 (Storting research note): "Trinn 1 i formuesskatten ble økt til 0,95 prosent. Det ble innført et nytt trinn 2 i formuesskatten med en sats på 0,4 prosent. Innslagspunktet for trinn 2 ble satt til 20 millioner kroner." / "Bunnfradraget i formuesskatten ble økt til 1 700 000 kroner for enslige og til 3 400 000 kroner for ektepar." (Step 1 raised to 0.95%; a new step 2, 0.4 percentage points extra, kicks in at NOK 20m; allowance NOK 1.7m for singles, 3.4m for couples.)
- 2023 (same note): "Satsen i formuesskattens trinn 1 ble økt til 1 prosent." / "Bunnfradraget i formuesskatten ble nominelt videreført fra 2022 til 2023." (Step 1 rate raised to 1%; allowance carried over nominally.) The top rate stayed 1.1% above NOK 20m: Ring (NBER 35854, p.2) writes "The top statutory tax rate increased from 0.85% to 1.1%".
- 2024 (same note): "Formuesskatten ble i 2024 skjerpet ved at bunnfradrag mv. ble nominelt videreført fra 2023." (Tightened in 2024 because the allowance etc. was carried over nominally.) No rate change is recorded for 2024, so NOK 1.7m and 1.0%/1.1% hold. I did not find the 2024 rate table itself, so state 2024 as "unchanged from 2023" only.
- 2025 (Skatteetaten rate page, 2025 tables): state: "0 - 1 760 000 kroner 0,0 %"; "1 760 001 kroner - 20 700 000 kroner 0,475 %"; "20 700 001 kroner og over 0,575 %". Municipality: "1 760 001 kroner og over 0,525 %". Combined: 1.0% (0.475 + 0.525) up to NOK 20.7m, 1.1% (0.575 + 0.525) above.
- 2026 (Skatteetaten rate page): state: "1 900 001 kroner - 21 500 000 kroner 0,65 %"; "21 500 001 kroner og over 0,75 %". Municipality: "1 900 001 kroner og over 0,35 %". Combined: 1.0% up to NOK 21.5m, 1.1% above. Allowance: "0 – 1 900 000 kroner 0,0 %". Thresholds are for single taxpayers; for spouses "the thresholds are twice the amounts shown".
- URLs: https://stortinget.no/globalassets/pdf/utredningsseksjonen/utredningsnotater/2024/endringer-i-formueskatten-fra-2000-til-2024-2024150.pdf (PDF-full); https://www.skatteetaten.no/satser/formuesskatt/ and `?year=2025` variant (Page-extract; the page's rate tables carried no year label in the extracted text, but the 2025 variant's discount table is headed "Verdsettings-rabatt i 2025", and the figures match the 2025 and 2026 budget decisions reported by Stortinget; see N6).
- Opened: 2026-11-08. Status: **verified** for 2022, 2023 and (rates unchanged) 2024 from the Storting note; **verified** for 2025 and 2026 from Skatteetaten, with the year-label caveat noted. The Storting resolution for 2026 allowance of NOK 1.9m was also seen in a search snippet of Innst. 3 S (2025-2026) (Search-only, corroborating).

**N6. Valuation discounts (verdsettingsrabatt) 2021 to 2026.** (this is what "wealth tax value" means in practice)
- 2025 Skatteetaten table "Verdsettingsrabatt 2025": "Primærbolig 75 pst."; "Primærbolig med boligverdi over 10 mill. kroner 30 pst."; "Sekundærbolig (og tilordnet gjeld) 0 pst."; "Aksjer (inkl. næringseiendom) og tilordnet gjeld 20 pst."; "Driftsmidler (og tilordnet gjeld) 30 pst." For 2026 the same page shows: Primary home 75 pst.; over NOK 14 million 30 pst.; secondary home 0 pst.; shares 20 pst.
- Translation: Primary home: valued at 25% of its assessed value after a 75% discount; for the part of a primary home's value above NOK 10m (2025) / NOK 14m (2026) the discount is 30%; secondary home: no discount; shares including commercial property (with attached debt): 20% discount; operating assets: 30% discount.
- History (Storting note): 2021 "Verdsettelsesrabatten for aksjer og driftsmidler og tilordnet gjeld ble økt til 45 prosent"; 2022 "reduced to 25 percent" for shares; 2023 "Verdsettelsesrabatten for aksjer (inkludert næringseiendom) og tilordnet gjeld ble redusert til 20 prosent" with an estimated revenue effect of NOK 1,175 million; secondary home discount "avviklet" (abolished) in 2023, estimated +NOK 265 million; operating assets discount raised to 30% in 2023 (-NOK 25 million). The Storting note puts the 2023 package at an increase of NOK 3,085 million (the PDF text prints this figure as "3 0859"; read it as 3,085 with a footnote marker, not 30,859; check against the original PDF before citing the sum).
- Ring (NBER 35854, p.2): "Directly before the reform, each $1 of book equity in private firms entered taxable wealth at a discounted value of $0.55. After the reform, $1 of book equity increased taxable wealth by $0.80." The effective top marginal rate on business wealth went from 0.47% to 0.88%.
- Opened: 2026-11-08. Status: **verified** (Storting note PDF-full; Skatteetaten Page-extract).

**N7. Taxable net wealth, the tax base (income year 2024).**
- Figure: SSB 08815 "Skattepliktig nettoformue" 2024: 4,805,655 persons with an amount; NOK 3,692,444 million; average NOK 768,400. 2022: NOK 3,223,450 million. Gross wealth 2024: NOK 8,291,803 million; debt (Gjeld) 2023: NOK 4,428,951 million (2024 debt cell not read).
- Opened: 2026-11-08. API-full. Status: **verified**.

---

## 2. Emigration of wealthy Norwegians since 2022: what official data say

**E1. Total emigration from Norway did not change course.**
- Figure (SSB 05395, both sexes, "Utvandring"): 2020: 26,744; 2021: 34,297; 2022: 32,536; 2023: 34,011; 2024: 31,968; 2025: 32,919.
- Why it matters: any claim of a general "exodus" of Norwegians is not in the totals. The question is only about the very top of the wealth distribution (E2 onwards).
- URL: https://www.ssb.no/statbank/table/05395 . Opened: 2026-11-08. API-full. Status: **verified**.

**E2. The Finance Ministry's own count of super-rich who moved (2022 and 2023).**
- Claim: 48 persons with net wealth over NOK 100 million moved in 2022 and 34 in 2023 (to 19 Dec 2023); 82 in total, with taxable wealth of about NOK 34.8bn (2022 movers, wealth in 2021) and NOK 10.9bn (2023 movers, wealth in 2022).
- Quote (Nettavisen's report of Finance Minister Vedum's written answer to Alfred Jens Bjørlo, 9 Jan 2024): "34 styrtrike personer (med nettoformue over 100 millioner) flyttet fra Norge i 2023"; "I 2022 var det 48 styrtrike personer som flyttet ut av Norge." (34 ultra-rich persons (net wealth over NOK 100m) moved from Norway in 2023; in 2022 there were 48 ultra-rich persons who moved out.)
- Caveats stated by the ministry, as reported: the overview covers people with net wealth over NOK 100m in at least one year in 2013-2022, or on Kapital's list of the 400 richest (2019-2022), in total 3,391 people; the wealth figure is the year before the person was registered as moved; the figures "må tolkes med varsomhet" and were not "hentet ut for statistikkformål, og er dermed ikke kvalitetssikret" (must be interpreted with caution; not extracted for statistical purposes and therefore not quality-assured).
- URL: https://www.nettavisen.no/okonomi/vedums-nye-exit-tall-82-megarike-utflyttere-pa-to-ar/s/5-95-1565612 . Opened: 2026-11-08. Page-extract.
- Status: **verified as what the ministry said** (via the press report; the original ministry answer on regjeringen.no is blocked, see section 9). 82 people is 0.012% of the 701,482 residents who paid wealth tax in 2024 (N3) and 3,391 is the size of the ministry's reference group; 82 / 3,391 = 2.4%.

**E3. Skattedirektoratet's exit-tax table for 2021-2023 movers (the best primary data on wealth that left).**
- Claim: People who were assessed exit tax after moving abroad in 2021, 2022 and 2023 held the following taxable net wealth, paid the following tax in the year before they left, and had the following unrealised share gains.
- Table 1 (Finance Ministry answer to written question 1236, 28 Feb 2025, signed Jens Stoltenberg; NOK million; source "Skattedirektoratet og Finansdepartementet"):
  - Latent gain assessed for 2021: 7,621. Taxable net wealth the year before moving: 1,735; net income 170; tax paid to the state 20; to municipalities 31.
  - Latent gain assessed for 2022: 134,405. Year before moving: net wealth 36,059; net income 2,237; tax to the state 241; to municipalities 564. In the year of moving: net wealth 2,829; net income 1,988; tax to the state 161; municipalities 227.
  - Latent gain assessed for 2023: 42,099. Year before: net wealth 16,425; net income 870; state tax 159; municipal 229. In the year of moving: 3,984; 1,138; 122; 181.
- Quote: "Det presiseres videre at tallene ikke er innhentet for statistikkformål, og at de må tolkes med varsomhet." (It is further stressed that the figures were not collected for statistical purposes and must be interpreted with caution.) And: "Utflyttede personer kan fortsatt betale skatt til Norge." (Persons who have moved out can still pay tax to Norway.)
- Reading it: the set is "people for whom exit tax was assessed", not "all wealthy emigrants". The 2022 cohort is dominated by a few very large cases (taxable net wealth NOK 36.1bn in the year before moving, against total taxable net wealth of NOK 3,223bn for all of Norway in 2022, i.e. 1.1%). Their combined state plus municipal tax paid in the year before departure (income and wealth tax together) was NOK 805 million, against NOK 26,320 million wealth tax collected from all payers in 2022 (N1); the two numbers are not the same tax, so do not divide them as if they were.
- The unfavourable side: the latent gain for 2022 alone, NOK 134.4bn, is the base on which exit tax is assessed (at the capital-gains rate; see L4 for deferral). That base left the ordinary tax net.
- URL: https://www.stortinget.no/globalassets/pdf/dokumentserien/2024-2025/dok15-202425-1236-vedlegg.pdf . Opened: 2026-11-08. PDF-full. Status: **verified**.

**E4. Switzerland count (NRK, May 2026), and what it does and does not say.**
- Claim: NRK counted 163 business owners who moved to Switzerland since 2020; before leaving they paid a combined NOK 343 million in wealth tax, 2% of all wealth tax collected in 2019.
- Quote (NRK, published 16 May 2026): "Kartlegginga vår viser at 163 bedriftseigarar har flytta til Sveits sidan 2020." (Our survey shows 163 business owners have moved to Switzerland since 2020.) "utgjorde 2 prosent av all formuesskatt staten Noreg fekk inn i 2019" (made up 2 percent of all wealth tax the state of Norway received in 2019.) Also: "Me kan ikkje fastslå kva Noreg totalt fram til i dag har tapt." (We cannot determine what Norway has lost in total up to today.)
- Method caveats stated by NRK: owners from the beneficial-owner register (94% of companies registered), moving dates from the population register, wealth and tax "from Skatteetaten's tax lists"; the wealth tax is estimated from net wealth on the tax lists; latest year available is 2024. Movers who left before 2024 still paid about NOK 310 million in other Norwegian taxes in 2024 (250 million in 2019), because their companies are Norwegian.
- Check against SSB: 343 / 16,599 (2019 total, N1) = 2.07%, so the "2%" is right on a 2019 base. On the 2024 base of NOK 31,784 million (N1), 343 million is 1.1%. NOK 343 million is a stock of past tax paid by 163 people over several years' departures, not an annual loss.
- URL: https://www.nrk.no/norge/skatteflyktningane_-sa-mange-har-flytta-til-sveits-og-dette-betalte-dei-i-formuesskatt-1.17853968 . Opened: 2026-11-08. Page-extract. Status: **verified as NRK's claim and method**; NRK is a journalistic estimate, not official statistics.

**E5. Peer-style estimate: how many left because of the reform, and what it cost in revenue (Ring 2026).**
- Claim: At most about 100 people left because of the 2021-2024 reforms, almost all in 2022-2023, concentrated in the top 0.1% of taxable wealth. Reform-driven emigration cut the 2021-2024 growth in wealth-tax revenue from 75.1% to 71.5%.
- Quotes (Ring, NBER WP 35854, abstract, Oct 2026): "While I document clear effects on migration, these responses are concentrated among the top 0.1% of the wealth distribution and mostly confined to 2022 and 2023. My results indicate that at most 100 individuals left due to the reforms." "I estimate that absent any outmigration, wealth tax revenues would have increased by 75% from 2021 to 2024. Reform-driven outmigration lowers the revenue gain to 71.5%."
- From the body (p.3): "My estimates suggest that about 1.78% of the top 0.1%, or about 0.24% of the top 1% migrated due to the reform. This amounts to 74-98 individuals." "I estimate a total wealth-tax revenue loss of about 0.65 BNOK, or about 2% of counterfactual revenues." (p.14-15: counterfactual 2024 revenue NOK 31.97 BNOK, loss 2.05%; netting off wealth tax that emigrants still pay for up to three years, the excess loss is 0.49 BNOK.) "This excess outmigration lasted to the fall of 2023, after which migration rates returned to pre-reform levels."
- Unfavourable details (use them): "I also consider individual shareholders in Norwegian firms. I find excess outmigration of 2.19% among the top-1% of business owners, but no response among the remaining 99%." Blandhol (2025) is cited (Ring fn. 11) as finding that those who left in 2022 "accounted for about 2.25% of 2021 wealth tax revenues". "[T]he closing of the five-year loophole may also have accelerated wealth-tax-motivated migration." The paper's own conclusion is limited to "short-run economic costs".
- Status of the paper: NBER states "They have not been peer-reviewed". The author is at UT Austin/Yale (data: shareholder register 2003-2025, public tax lists, Kapital's top-400, Orbis).
- URL: https://www.nber.org/papers/w35854 . Opened: 2026-11-08. PDF-full. Status: **verified** as the paper's content; **working paper, not peer reviewed**.

**E6. Think-tank count from SSB register data (Civita note 26/2025): the unfavourable reading.**
- Claim: Emigration of people with net wealth over NOK 50 million rose from 17 a year on average under the Solberg government (2014-2021) to 77 a year under the Støre government (2022-2023); over NOK 10 million, from 122 to 258 a year; below NOK 10 million, stable at 26,000-27,000 a year.
- Quotes: "Det mest slående funnet var at det i gjennomsnitt flyttet ut 17 personer med formue over 50 millioner kroner per år under Solberg-regjeringen, mens tallet under Støre-regjeringen har økt til 77 personer." (The most striking finding was that on average 17 persons with wealth above NOK 50 million moved out per year under the Solberg government, while the figure under the Støre government has risen to 77.) "Analysen foretar ikke en kausalanalyse" (The analysis does not make a causal analysis.) Also: "Om lag 268 000 personer hadde formue under 10 millioner kroner (99,45 prosent). Om lag 1 190 ... mellom 10 og 50 millioner ... og 290 emigrerte personer hadde over 50 millioner kroner" (about 268,000 of ~269,000 emigrants 2014-2023 had under NOK 10m; about 1,190 had 10-50m; 290 had over 50m.) And: in 2022, net emigration (after subtracting immigration) of 106 persons with business wealth above NOK 10m, 57 of them above NOK 50m; but "netto innflytting ... av 20 personer med formue over 10 millioner kroner, men som ikke eide aksjer personlig" (net immigration of 20 people with over NOK 10m who did not own shares personally).
- Source quality: written by Civita (a think tank that campaigns against ownership taxes), using SSB register data compiled by Prof. Amir Sasson (BI) and processed by NyAnalyse. It is the strongest unfavourable analysis I found; its wealth is "beregnet" (estimated, highest net wealth in the five years before moving, 2023 kroner), not the same definition as the ministry's list (E2). Its numbers are counts of **persons** and say nothing about euro-for-euro revenue.
- URL: https://civita.no/content/uploads/2025/07/Notat_26_2025_Store-formuer-flytter-ut-av-Norge.pdf . Opened: 2026-11-08. PDF-full. Status: **verified as Civita's content; use only with attribution and the causality caveat**.
- Compared with Ring (E5): Civita's "77 a year over NOK 50m" (2022-2023) is a gross count of all emigrants in that group, not the reform-induced excess (Ring: 74-98 individuals in total, in the top 0.1%).

**E7. E24's 2022 count.**
- Claim: 64 of about 2,700 people who had over NOK 100m taxable wealth at some time in 2010-2020 had emigrated and were still abroad by September 2022; 2.4% of the group; about 7% of the group's wealth; typical emigrant took about NOK 166m.
- Quote (E24, 3 Oct 2022, updated 5 Oct 2022): "Utflytterne utgjør 2,4 prosent av alle som har vært rike i denne perioden"; "De 64 er de som er utvandret pr. i dag." (The emigrants make up 2.4 percent of all who were rich in this period; the 64 are those who have emigrated as of today.) "Veksttakten har gått kraftig opp de siste par årene." (The pace has risen sharply in the past couple of years.)
- URL: https://e24.no/naeringsliv/i/ab7lWa/rike-nordmenn-to-prosent-har-forlatt-norge-paa-12-aar . Opened: 2026-11-08. Page-extract. Status: **verified as E24's claim; a 2022 snapshot, superseded by E2/E3/E5**.

**E8. Exit-tax tightening (the policy response).**
- Claim: Tax no longer lapses 5 years after emigration (29 Nov 2022); from 20 Mar 2024 the exit tax must be paid within 12 years (immediately, in instalments over 12 years, or deferred with interest). The Ministry's booked yield is "about NOK 100 million in 2026", on "a very uncertain basis", rising to about NOK 1,200 million after 12 years.
- Source: answer by Jens Stoltenberg (Minister of Finance) to written question 15:1899 (2024-2025) from Tina Bru (H), answered 24 Apr 2025. The page-extract reproduces the dates and amounts above; the question asks for "provenyet i 2026 av de ulike endringene i utflyttingsskatten som er gjennomført siden 2021" (the 2026 revenue effect of the various changes to the exit tax made since 2021).
- URL: https://www.stortinget.no/no/Saker-og-publikasjoner/Sporsmal/Skriftlige-sporsmal-og-svar/Skriftlig-sporsmal/?qnid=104342 . Opened: 2026-11-08. Page-extract. Status: **verified**.

---

## 3. Media claim versus statistics

| # | Widely reported claim (where I found it) | What the original actually says | What the official figure says | The difference, in numbers |
|---|---|---|---|---|
| M1 | "Eighty-two rich Norwegians with a combined net wealth of about 46 billion kroner" left in 2022-2023, "more than 70" to Switzerland (Fortune, repost of Bloomberg, 19 Apr 2024) | Attributes the 82 and NOK 46bn to the Finance Ministry; the "more than 70 to Switzerland" to Dagens Næringsliv (Jan 2024). | Ministry (via Nettavisen, E2): 48 + 34 persons; taxable wealth about NOK 34.8bn + NOK 10.9bn = 45.7bn; "må tolkes med varsomhet ... ikke kvalitetssikret". Total taxable net wealth in 2022: NOK 3,223bn (N7). | The article's number is right as a ministry number. In context: 82 persons; their year-before wealth is 1.4% of Norway's 2022 taxable net wealth (45.7 / 3,223); revenue effect per Ring is -2.05% of 2024 wealth tax (E5). Not mentioned in the article: the ministry's own warning that the data were not quality-assured. (Original article: https://fortune.com/europe/2024/04/19/wealthy-norwegians-flee-to-switzerland-to-evade-high-wealth-taxes-bankers-following-dnb-abg-sundal-collier/ , Page-extract.) |
| M2 | "The government increased the wealth tax burden by 55%, adjusted for inflation", and ownership-tax receipts of NOK 65bn in 2023 against NOK 38bn in 2021 (same Fortune/Bloomberg article, both attributed there to Civita) | Both numbers are attributed to Civita, "a privately funded think tank". | SSB 08815: wealth tax NOK 18,454m (2021), NOK 29,399m (2023), NOK 31,784m (2024). | Wealth tax alone rose +59% 2021-2023 and +72% 2021-2024, nominal (N2). The NOK 65bn is Civita's sum of wealth tax plus dividend and capital-income taxes on owners; I could not reproduce it from an official source (section 9). |
| M3 | "Norway's Exodus of Billionaires" (Financial Times, 2023, Free Lunch column, as cited by Ring) and "scores of billionaires had, not so quietly, migrated to Switzerland" (Ring's summary of FT 2023, Bloomberg 2024, Guardian 2025) | FT: paywalled; I did not open it. Guardian: my fetch tool is blocked there. The titles and the characterisation are in Ring's introduction (p.2). | Ring's own estimate: at most about 100 persons; 74-98 individuals, 1.78% of the top 0.1% (E5). Ministry: 82 persons over NOK 100m in 2022-2023 (E2). | "Exodus" in the sense of a mass departure: not in the numbers. Dozens, concentrated in 2022 and the first months of 2023, not a continuing flow. |
| M4 | "163 business owners moved to Switzerland since 2020" and "NOK 343 million in wealth tax" (NRK, 16 May 2026) | As quoted in E4. | Total wealth tax 2019: NOK 16,599m; 2024: NOK 31,784m (N1). | 343 / 16,599 = 2.1% (2019 base); 343 / 31,784 = 1.1% (2024 base). NRK itself says the total loss cannot be determined. The same persons still paid about NOK 310 million in other Norwegian taxes in 2024. |
| M5 | "About 2% of the wealthy have left in 12 years", and "growth is sharply up" (E24, Oct 2022) | E7. | Ministry list (E2): 3,391 persons; moved in 2022 and 2023: 82. | 2.4% over 2010-2022 on E24's own definition; the ministry's later counts are 82 persons in two years. Same order of magnitude; the E24 piece is older and a different group. |
| M6 | "Record emigration of Norwegians after the government change" (Civita note 20/2025 title; I opened note 26/2025, its companion) | "Rekordhøy utflytting av nordmenn etter regjeringsskiftet i 2021" is the title of note 20/2025 as shown in search results; I did not open note 20 itself. Note 26 uses the same data. | SSB 05395 (E1): total emigration 34,297 (2021), 32,536 (2022), 34,011 (2023), 31,968 (2024), 32,919 (2025). | In **total** there is no record year in 2022-2025 (2021 was highest at 34,297). The Civita claim is about people with over NOK 10m or 50m: 17 to 77 a year over NOK 50m, and that is a rise in tiny numbers (E6). |
| M7 | Officials' latest count 2024 and 2025 | I could not open it: NOU 2026:9 is on regjeringen.no (blocked). A search-engine snippet of the Tax Commission's consultation note showed a table with 16 persons (2024) and 17 persons (2025), with year-before wealth tax of NOK 57m and NOK 55m. | Not verified. | Do not use. See section 9. |

---

## 4. Valuation and filing in practice

**V1. The tax return is pre-filled, and the value of unlisted shares comes from the company, not the owner.**
- Claim: For unlisted companies the company itself calculates the wealth-tax value of its shares and attaches the calculation to its tax return; the owner then uses that figure in the personal return.
- Quote (Skatteklagenemnda decision SKNS1-2024-117, 11 Dec 2024, published by Skatteetaten 26 Mar 2025): "Formuesverdien av aksjer i ikke-børsnoterte selskaper skal fastsettes av selskapet når selskapets skattegrunnlag fastsettes." "Aksjeselskapet har plikt til å beregne aksjenes formuesverdi og beregningen skal vedlegges selskapets skattemelding" (The wealth value of shares in unlisted companies shall be determined by the company when its tax base is determined. The company is obliged to calculate the shares' wealth value and the calculation shall be attached to the company's tax return.) and "aksjonæren fastsetter grunnlaget for formuesskatt i sin skattemelding".
- URL: https://www.skatteetaten.no/en/rettskilder/type/vedtak/skatteklagenemnda/skattemessig-formuesverdi-pa-aksjer/ . Opened: 2026-11-08. Page-extract. Status: **verified**.
- Related, from a search snippet only: the 2025 value of unlisted shares is 80% of the share's portion of the company's tax-based wealth value on 1 January (consistent with the 20% discount in N6). Search-only; the 20% rate itself is verified in N6.

**V2. Bank, funds and listed shares are reported by third parties; the owner does not type them in.**
- Claim: Banks and similar institutions report balances and holdings to Skatteetaten (third-party reporting), which is why SSB's table 08815 can break wealth into bank deposits, funds, shares and so on from register data. I did not open the Skatteetaten page that lists exactly what is pre-filled (the pages that came up were older or on income), so I make this claim only through SSB: table 08815 has the components "Bankinnskudd" (bank deposits), "Verdipapirfond, aksjedel" (mutual funds, equity part), "Aksjesparekonto (2017-)" and "Aksjer og verdipapirer (2019-)" (shares and securities) as separate rows, i.e. the data exist in the tax register at the level of the individual.
- URL: https://www.ssb.no/statbank/table/08815 . Opened: 2026-11-08. API-full. Status: **partly verified** (existence of register data; the precise pre-fill rules for each asset type are in section 9).

**V3. How many people simply approve the pre-filled return: could not verify a current figure.**
- What I found: a 2022 Skatteetaten press-release snippet (Search-only) reading "2,1 millioner leverte uten endringer - 58 % av de som har levert" (2.1 million submitted without changes, 58% of those who have submitted); a note in a Skatteetaten page that a person with no changes "trenger ikke å levere skattemeldingen" (need not submit the return). A 2018-19 figure (about 70% using "leveringsfritak") also appeared in a search snippet. I did not open the originals, and none of these is about wealth taxpayers specifically. **Do not use any of them.** See section 9.

**V4. The real compliance problem Skatteetaten and the Auditor General identify is foreign assets, not domestic ones.**
- Claim: Riksrevisjonen found a large number of taxpayers fail to report foreign wealth and income; the Tax Administration estimates the revenue loss at about NOK 7 billion a year; the control level has been too low.
- Quotes (Innst. 172 S (2023-2024), 16 Jan 2024, on Document 3:3 (2023-2024)): "Et stort antall skattepliktige unnlater å rapportere utenlandsformuer og -inntekter i skattemeldingen." (A large number of taxpayers fail to report foreign wealth and income in the tax return.) "Skatteetaten har anslått provenytapet til ca. sju milliarder kroner årlig." (The Tax Administration has estimated the revenue loss at about seven billion kroner a year.) "Skatteetatens kontrollnivå har vært for lavt." (The Tax Administration's control level has been too low.) "For inntektsåret 2021 mottok Norge over én million oppgaver." (For income year 2021 Norway received over one million reports [under CRS, FATCA etc.].) "Komiteen slutter seg til Riksrevisjonens konklusjoner."
- Skatteetaten press release, 19 Oct 2023: "utgjør 7,1 milliarder kroner årlig" (amounts to NOK 7.1 billion per year); "Vi har sett at vi har hatt for få kontroller på dette området" (We have seen that we have had too few controls in this area); the estimate "is based on an EU Commission analysis and a comparison with Sweden and Denmark"; the Administration says it has added "flere titalls årsverk".
- Important limit: the NOK 7bn covers **hidden foreign income and wealth in all taxes**, not wealth tax alone. Do not present it as "wealth-tax evasion".
- URLs: https://stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2023-2024/inns-202324-172s/?all=true ; https://www.skatteetaten.no/en/press/nyhetsrommet/skatteetaten-har-okt-kontrollen-av-verdier-i-utlandet/ . Opened: 2026-11-08. Page-extract. Status: **verified**.

**V5. Evidence on what happens when there is no third-party reporting (Switzerland).**
- Claim: In Swiss cantons, where financial wealth is self-reported, a 1 percentage-point cut in a canton's wealth-tax rate raised reported taxable wealth by at least 43% after six years. About a quarter was taxpayers moving and about a fifth rising house prices; the rest, with little savings response, was read by the authors as evasion.
- Quote (Brülhart, Gruber, Krapf and Schmidheiny, AEJ: Economic Policy 14(4), 2022, pp.111-150, abstract): "a 1 percentage point drop in a canton's wealth tax rate raises reported taxable wealth by at least 43 percent"; "suggesting sizable evasion responses in this setting with no third-party reporting of financial wealth".
- Use for Norway: the evasion channel the Swiss paper identifies is the one Norway's third-party reporting closes for domestic bank and securities holdings. It does not close it for foreign assets (V4) or for private-company values (V1).
- URL: https://www.aeaweb.org/articles?id=10.1257/pol.20200258 . Opened: 2026-11-08. Page-extract (abstract). Status: **verified** (abstract only; magnitude details not read).

---

## 5. Liquidity: deferral, dividends, and the debate

**L1. A permanent deferral scheme for wealth tax on business wealth exists from income year 2026.**
- Claim: Private individuals can defer payment of the part of wealth tax that is attributed to business wealth, for up to three years, if the amount is NOK 30,000 or more; interest is the central-bank policy rate plus 5 percentage points. The earliest income year to apply for is 2026.
- Quotes (Skatteetaten, "Utsett betaling av formuesskatt beregnet på virksomhetsformue"): "Du kan utsette betaling av formuesskatt beregnet på virksomhetsformue hvis du er privatperson"; "beløpet du skal utsette er 30 000 kroner eller mer"; "i opptil tre år"; "Renten er satt sammen av styringsrenten til Norges Bank, med et påslag på 5 prosentpoeng."; "Det tidligste året du kan søke for er 2026." (You can defer payment of wealth tax calculated on business wealth if you are a private individual; the amount to be deferred is NOK 30,000 or more; for up to three years; the interest is the Norges Bank policy rate with a surcharge of 5 percentage points; the earliest year you can apply for is 2026.) "Virksomhetsformue" lists: shares, share-savings account, shares in companies with participant taxation, operating assets and commercial property in sole proprietorships.
- Not stated on the page as extracted: any requirement of collateral. Status of the rate level: a search snippet showed "9 prosent fra 1. januar 2026 og 9,25 prosent fra 1. juli 2026" (Search-only: do not quote).
- URL: https://www.skatteetaten.no/person/skatt/skattekort/utsett-virksomhetsformue/ . Opened: 2026-11-08. Page-extract. Status: **verified** (scheme and terms); rate level could not verify.
- Earlier schemes: a temporary one existed for 2016-2017 and 2020 (Search-only: Skattebetalingsloven § 15-3 page). Not verified in detail.

**L2. The dividend-tax side of the liquidity argument.**
- Claim: The reform raised the dividend tax from 32% to almost 38% by 2023, which hits owners who must take dividends to pay the wealth tax. (Ring, NBER 35854, p.2, "the dividend tax rate increased from 32% to almost 38% by 2023, which exacerbated the effect of the reform on business owners who rely on dividend distributions to pay their wealth tax".) PDF-full. Status: **verified** as the paper's statement; the statutory rate history itself is not in an official source I opened.

**L3. Did owners strip their firms of capital to pay the tax? The best evidence says no, in the short run.**
- Quote: "Across settings, I find no evidence that Norwegian-owned firms pay out more dividends or invest less after the reforms, nor is there any evidence that the reform induced more bankruptcies." (Ring, NBER 35854, abstract). The author allocates owners' wealth tax to firms and finds it rose by about 1.6 percentage points of revenue from 2020 to 2024 (p.4). He "can reject reductions in the investment rate larger than 1.2 percentage points" (p.5). Limits he states: the results are "short-run"; the sample is firms with data in Orbis and the shareholder register; the comparison group is foreign-owned and other exempt owners.
- Status: **verified**; working paper, not peer reviewed.

**L4. What cuts the other way on liquidity.**
- The Finance Ministry's own exit-tax numbers (E3, E8) show that the owners who left in 2022 and 2023 had large unrealised gains (NOK 134.4bn and NOK 42.1bn) on which exit tax is assessed but deferred: that is the "no cash, big tax bill" problem which the exit-tax rule (12-year payment) and the 2026 deferral scheme (L1) both address.
- Civita (E6) argues that persons with over NOK 10m who moved had 58-93% of their wealth in limited-company shares ("mellom 58 og 93 prosent av sin formue i eierskap i aksjeselskaper"). That is the group for which a wealth tax is paid out of dividends or sales. The Ring result in L3 is the counter-evidence, and Ring's own text notes this "theoretically ambiguous" effect (p.4: investment falls only if the elasticity of intertemporal substitution exceeds about 0.66).
- Status: **verified** as statements in the cited sources; the political debate itself (who argues what) I did not survey beyond these.

---

## 6. Investment, entrepreneurship and growth: empirical studies, favourable and unfavourable

Each study is rated for **direction** (does it help or hurt the case for a wealth tax) and for **how well I verified it**.

**S1. Ring (2026), "Taxing Entrepreneurial Wealth: Evidence from Norway, 2021-2025", NBER WP 35854.** Direction: mostly favourable. Findings: E5, L2, L3; plus: "I find no evidence of significant outmigration or reduced inflows of startup founders or inventors" (abstract); in a calibrated model the reforms reduce investment only if the elasticity of intertemporal substitution exceeds about 0.66, and "[t]he implied change in the investment rate ranges from -2.8 to +3.5 percentage points for values of the EIS between 0.2 and 6" (p.4). Caution: short horizon (2021-2025 data); working paper, not peer reviewed; the abstract speaks of "short-run economic costs". PDF-full. **Verified.**

**S2. Ring (2025), "Wealth Taxation and Household Saving: Evidence from Assessment Discontinuities in Norway", Review of Economic Studies 92(5), pp.3375-3402.** Direction: favourable for the "growth" objection. Finding (abstract): "wealth taxation causes households to save more"; "Each additional NOK of wealth tax increases annual net financial saving by 3.76" and the increase is "primarily financed by increases in labour earnings". Page-extract of an abstract listing (EconPapers/university listing); I did not read the paper. **Verified as abstract only.** URL: https://econpapers.repec.org/RePEc:oup:restud:v:92:y:2025:i:5:p:3375-3402 (listing seen in search; not opened in full).

**S3. Bjørneby, Markussen and Røed (2023), "An imperfect wealth tax and employment in closely held firms", Economica 90(358), pp.557-583.** Direction: favourable on jobs, with an unfavourable mechanism. Abstract (EconPapers): "Our results indicate a positive causal relationship between the level of a household's wealth tax and subsequent employment growth in the taxpayers' closely held firms." The unfavourable part, in the same abstract: "intangible assets held by non-traded firms are in practice tax-exempt, giving firm owners an incentive to allocate wealth into their businesses". Data: Norwegian register data and tax reforms 2007-2017 (before the 2022 increase; the effect of a much higher rate is not tested). URL: https://econpapers.repec.org/RePEc:bla:econom:v:90:y:2023:i:358:p:557-583 . Page-extract (abstract). **Verified as abstract only.**

**S4. Iacono and Smedsvik (2024), "Behavioral Responses to Wealth Taxation: Evidence from a Norwegian Reform", CESifo WP 11335.** Direction: **unfavourable to local wealth taxes; neutral nationally.** Quotes (ifo/CESifo abstract): "We document a significant 60% increase in average taxable wealth" in the treated municipality (Bø), after the municipal rate was cut from 0.85% to 0.35% in 2021; "The elasticity of taxable wealth increases to 68.7% when focusing exclusively on wealth taxpayers"; "Migration effects of the reform dominate", the main response being internal mobility of wealthy taxpayers; the results "do not suggest a large-scale exodus at the national level". Note: the extracted abstract describes "a 1 percentage point drop" but the rate change (0.85% to 0.35%) is 0.5 points; magnitudes need checking in the PDF. Lesson for the page: a single municipality that cuts its rate attracts wealthy residents from other Norwegian municipalities, which is an argument for a uniform, national tax, not an argument about leaving the country. URL: https://www.ifo.de/en/cesifo/publications/2024/working-paper/behavioral-responses-wealth-taxation-evidence-norwegian-reform . Page-extract. **Verified as abstract only.**

**S5. Brülhart, Gruber, Krapf and Schmidheiny (2022), AEJ: Economic Policy 14(4), pp.111-150 (Switzerland).** Direction: **unfavourable** if the tax relies on self-reporting; shows large sensitivity of reported wealth to the rate. Quotes: see V5. Not Norway: Switzerland has cantonal wealth taxes, no third-party reporting of financial wealth. **Verified as abstract only.**

**S6. Jakobsen, Jakobsen, Kleven and Zucman (2020), "Wealth Taxation and Wealth Accumulation: Theory and Evidence from Denmark", QJE 135(1), pp.329-388.** Direction: **unfavourable.** Quotes (abstract): "We find clear reduced-form effects of wealth taxes in the short and medium run ... with larger effects on the very wealthy than on the moderately wealthy"; "the long-run elasticity of taxable wealth with respect to the net-of-tax return is sizable at the top of the distribution". Denmark, not Norway, and a tax that was later abolished. The extract did not give the numerical elasticities. URL: https://collaborate.princeton.edu/en/publications/wealth-taxation-and-wealth-accumulation-theory-and-evidence-from-/ . Page-extract. **Verified as abstract only.**

**S7. Fagereng, Guiso, Malacrino and Pistaferri (2020), "Heterogeneity and Persistence in Returns to Wealth", Econometrica 88(1), pp.115-170 (Norwegian administrative data).** Direction: **cuts both ways, and is the paper opponents will cite.** From the abstract listing (EconPapers/CESifo): returns are heterogeneous across persons, persist over time, and rise with wealth: "increases the return by 18 percentage points (and 10 percentage points if looking at net-of-tax returns)" moving from the 10th to the 90th wealth percentile; a standard deviation of 22.1% on net worth. Implication to answer accurately: a flat wealth tax is a higher tax on the returns of high-return owners, which is the basis of the "it taxes entrepreneurs hardest" objection; the same persistence is also what wealth-tax supporters use to argue that high-return wealth compounds across generations. Search listing only for the numbers above (the Econometrica page was in search results, not opened). **Verified only as quoted by listings; do not use the 22.1% or 18 pp numbers without opening the paper.**

**S8. Civita (2025), notes 20/2025, 26/2025, 28/2025.** Direction: **unfavourable.** See E6. Note 28/2025 ("Utflytting av store verdier etter regjeringsskiftet i 2021"): search snippet only, reporting that people with over NOK 50m who moved paid on average NOK 7.4 million in personal tax the year before: **not verified, do not use**.

---

## 7. Safe to write (headline facts, all verified in this sheet)

1. In income year 2024, 719,007 taxpayers paid Norwegian wealth tax, in total NOK 31,784 million (SSB table 08815). [N1]
2. Revenue rose from NOK 18,454 million in 2021 to NOK 31,784 million in 2024, +72% in kroner, while the number of payers grew 8%. [N2]
3. About 15% of Norwegian adults pay (701,482 of 4,541,587 in 2024), and 45% of those pay under NOK 10,000. Only 2,838 pay NOK 1 million or more. [N3]
4. The number of residents paying NOK 1 million or more went up from 2,572 (2022) to 2,838 (2024), after the 2022 increase. [N3]
5. The wealth tax was 0.59% of GDP in 2024 and about 1.5% of the general government's tax and contribution receipts (state the denominators and that GDP includes oil). [N4]
6. The rate for wealth above the allowance is 1.0% (1.1% above about NOK 21.5m in 2026); the allowance is NOK 1.9m in 2026 (NOK 1.76m in 2025, NOK 1.7m in 2022-2024). [N5]
7. Shares are discounted 20% for wealth-tax purposes, primary homes 75% (30% on the most valuable part), secondary homes 0% (2025-2026). [N6]
8. Total emigration from Norway was 34,297 (2021), 32,536 (2022), 34,011 (2023), 31,968 (2024) and 32,919 (2025): no break in the total. [E1]
9. The Finance Ministry counted 48 people with over NOK 100 million of net wealth moving in 2022 and 34 in 2023 (to 19 Dec 2023), with the caveat that the numbers are "not quality-assured". [E2]
10. A working paper by Marius Ring (NBER, October 2026, not yet peer reviewed) estimates at most about 100 people (74-98) left because of the 2021-2024 reforms, almost all in 2022-2023, and that this cost about 2% of wealth-tax revenue: revenue still rose 71.5% rather than 75%. [E5]
11. The same paper finds no evidence of more dividends, less investment or more bankruptcies in firms owned by wealth-tax payers, and no extra emigration of startup founders or inventors. [L3, S1]
12. NRK counted 163 business owners moving to Switzerland since 2020; the NOK 343 million in wealth tax they had paid was 2% of 2019's wealth tax (1.1% of 2024's). [E4, M4]
13. Riksrevisjonen and Skatteetaten: hidden foreign income and wealth costs NOK 7 billion a year (all taxes), and controls had been too few. This is a general compliance problem, not a feature of the wealth tax. [V4]
14. From income year 2026 owners of business wealth can defer the wealth tax attributed to it for up to three years at the policy rate plus 5 percentage points. [L1]

## 8. Do not use

1. **"X% of the rich left" from E24 (2.4%) as current.** It is a 2022 snapshot with another definition. [E7]
2. **Civita numbers (17 to 77 a year over NOK 50m; "record emigration") without saying who Civita is and that the analysis is not causal.** Also never present them as SSB's own publication. [E6]
3. **"At most 100 left" as "only 100 left".** The paper's wording is "at most", and it adds the 2.19% extra outmigration among the top 1% of business owners. [E5]
4. **The NRK NOK 343 million as an annual loss.** It is a stock of past taxes paid by 163 people, on a 2019 base. [E4]
5. **The Finance Ministry's 82 as "statistics".** The ministry says they were not extracted for statistical purposes. [E2]
6. **Tax-return approval shares (58%, ~70%).** Not verified, not about wealth taxpayers. [V3]
7. **"NOK 7 billion of wealth-tax evasion".** The figure is hidden foreign income and wealth in total. [V4]
8. **Any 2025 or 2026 wealth-tax revenue figure.** SSB's table ends at 2024; budget estimates and Civita estimates were not verified. [section 9]
9. **The 16 (2024) and 17 (2025) departures.** Not opened in the original. [M7, section 9]
10. **Wealth-tax revenue "share of mainland GDP".** I did not pull mainland GDP. [N4]
11. **The Fortune/Bloomberg "55% burden" and "NOK 65bn" ownership-tax numbers** as facts: Civita's numbers, not official. [M2]
12. **Swiss, Danish and Bø results as predictions for a national Norwegian tax or for other countries** without the caveat about third-party reporting and about municipal competition. [S4, S5, S6]
13. **Fagereng's 18 pp and 22.1% figures** until the paper is opened. [S7]
14. **Anything attributed to an AI chat tool.** None is used in this sheet.

---

## 9. Could not verify (and what would settle it)

| Item | What I have | What is missing |
|---|---|---|
| Officials' departure counts for 2024 (16) and 2025 (17), plus year-before wealth tax of NOK 57m and NOK 55m | A search-engine summary of Table 3.2 in the Tax Commission's consultation note (NOU 2026:9, delivered 24 June 2026, section 3.7.3) | The original table. regjeringen.no is behind a bot wall. Needs a person to open https://www.regjeringen.no/no/dokumenter/nou-2026-9/id3167167/ and copy Table 3.2 and its notes. |
| Wealth-tax revenue and payers for income year 2025 and 2026 | SSB table 08815 stops at 2024; Civita estimates (not opened in detail: about NOK 35bn and 690,000 payers for 2026 in its note 48/2025) | Prop. 1 LS (2026-2027) or SSB's 2025 release. |
| Share of taxpayers (and of wealth taxpayers) who approve the pre-filled return unchanged | Old and unopened snippets (V3) | Skatteetaten's annual "Skattemeldingen i tall" or Årsrapport; ask Skatteetaten directly. |
| Exactly which wealth items are pre-filled in the personal return | SSB table components (V2); the company-delivers-share-value rule (V1) | Skatteetaten's page on "Formue" in the return. |
| Current deferral-rate level (9%, 9.25%) | Search snippet | Skatteetaten's "Renter ved utsatt betaling" rate page. |
| The government's own memo or white paper on the 2026 changes (primary-home model, allowance of NOK 1.9m "provenynøytral") | Search snippets of Prop. 1 LS (2025-2026) quoting that the changes were revenue-neutral | Prop. 1 LS (2025-2026) chapter on wealth tax; regjeringen.no blocked. |
| Original FT 2023 "Norway's Exodus of Billionaires" and Guardian 7 Sep 2025 | Titles from Ring's reference list (FT, p.36) and Ring's characterisation; the Guardian fetch was blocked | The articles themselves. |
| Civita's "ownership taxes NOK 65bn (2023) vs NOK 38bn (2021)" | Fortune/Bloomberg citing Civita | The Civita note and its sources (probably Finance Ministry tables). |
| Norges Bank view | Not found; I did not find a Norges Bank analysis of the wealth tax | If the argument page wants Norges Bank, a targeted search of its Monetary Policy Report or staff memos is needed. |
| Tax-expert reports (NOU 2022:20; Tax Commission 2026) on valuation | Not opened | regjeringen.no is blocked; Stortinget may republish. |
| Fagereng, Ring (REStud 2025), Bjørneby et al., Brülhart et al., Jakobsen et al. in full | Abstracts only | Papers' full text. |
| Berzins, Bøhren, Stacescu on shareholder illiquidity and firm behaviour (BI) | A slide deck seen in search results only | The paper; possibly the best study of liquidity effects on firms. |
| Blandhol (2025), Princeton job-market paper on emigration | Cited in Ring (fn. 11) as "about 2.25% of 2021 wealth tax revenues" | The paper. |
| Market-value versus assessed-value gap for primary homes and shares | Discount tables only (N6) | SSB or Skatteetaten data comparing assessed and market values. |

## 10. Method note and reproduction

- SSB tables can be reproduced by POSTing a JSON query to `https://data.ssb.no/api/v0/no/table/<number>`. Table 08815, variable code `Formue2` = `18` ("Formuesskatt") and `15` ("Skattepliktig nettoformue"); `ContentsCode` = `LignetPersoner`, `LignerKr`, `LiknetGjsnitt`. Table 08231, variable `FormuesSkatt1` = `01`..`15`. Table 10799, sector `100000`/`h130000`, transactions `i3000M_`, `i335_`, `i30210`, `i30220`, `i3027_`, `i30250`, `i33401`, `i3342_`. Table 05395, `Utvandring`.
- A few cells in the SSB tables are shown to the nearest unit; sums above are mine.
- The Farahmand answer and the Storting note were converted with `pdftotext -layout`; special characters in the printed numbers (e.g. "3 0859") were read from that text and should be checked against the original PDF if a number from them is reused.
