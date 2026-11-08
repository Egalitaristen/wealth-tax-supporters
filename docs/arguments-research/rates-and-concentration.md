# Fact sheet: tax rates at the top, composition of top wealth, concentration, and how a wealth tax differs from other taxes

Feeds the Arguments pages "Why tax wealth?", "Double taxation", "We already tax property, gains and inheritance" and "It doesn't raise enough".

**Date opened (all entries):** 2026-11-08 unless a different date is given.
**Scope rule:** primary datasets and primary papers only. No Wikipedia numbers, no AI-tool content. Search-engine snippets were used only to find documents; no number below rests on a snippet.

## 0. How to read this sheet

- Every entry has: **Claim** (plain words), **Figure** (value, year, unit), **Source text** (quote or table cell; quotes are kept short), **URL**, **Opened**.
- **Status:** `V` = verified in the primary document I opened. `V*` = verified, with a caveat that changes how it may be used (caveat stated in the entry).
- Entries are numbered 1 to 46 across sections A to E. Section G lists results that are unfavourable to a wealth tax or contradict a common claim. Section H lists what I could not verify. Sections I and J are the "safe to write" and "do not use" lists.

### Sources opened in full or in substance (what I actually read)

| Short name | Document | How much I read |
|---|---|---|
| BSYZ 2025 | Balkir, Saez, Yagan, Zucman, *How Much Tax Do US Billionaires Pay? Evidence from Administrative Data*, NBER WP 34170, Aug 2025 | Abstract, introduction, sections 2 to 3.4, Tables 1 and 2. Not the appendices. Working paper, not peer reviewed (stated on its cover). |
| RSZ 2026 | Ring, Seim, Zucman, *Personal Holding Companies, Tax Progressivity, and Inequality*, NBER WP 35534, Jul 2026 | Abstract, introduction, section 5 (effective rates, wealth tax as backstop). Working paper, not peer reviewed (stated on its cover). |
| IPP n°92 | Bach, Bozio, Guillouzouic, Malgouyres, *Quels impôts les milliardaires paient-ils ?*, Note IPP n°92, cover dated June 2023, file name "version actualisée" (uploaded May 2025) | Whole note (525 lines of text extracted). 2016 tax data. |
| Yagan 2023 | Yagan, *What Is the Average Federal Individual Income Tax Rate on the Wealthiest Americans?*, Oxford Review of Economic Policy, Apr 2023 | Abstract and introduction. |
| CEA 2021 | Leiserson and Yagan, same title, White House CEA blog, 23 Sep 2021 | Opening section (abstract and method paragraphs). |
| SYZ 2021 | Saez, Yagan, Zucman, *Capital Gains Withholding*, Jan 2021 | Abstract and section 1 (1.3 on unrealised gains). It is a policy-proposal paper. |
| Fed DFA | Federal Reserve, Distributional Financial Accounts, bulk file `dfa.zip` (files dated 15 Sep 2026), plus the FRED series page WFRBSTP1300 (last updated 2026-09-18) | Calculated from the Fed's own CSVs (`dfa-networth-shares.csv`, `dfa-networth-levels-detail.csv`, `dfa-data-definitions.txt`). All sums and ratios below are my arithmetic on those files. |
| WID | World Inequality Database bulk file `wid_all_data.zip` (903 MB), variable `shweal992j` (net personal wealth, adults, equal split), percentiles p90p100, p99p100, p99.9p100 | Read the eight country files directly. |
| SSB | Statistics Norway StatBank table 10318 (via the SSB API) | Pulled the table directly. |
| ESTV 2022 | Swiss Federal Tax Administration, *Die Verteilung der steuerbaren Vermögen in der Schweiz im Jahr 2022*, 29 Oct 2025 | Whole 10-page note. |
| DIW 1717 | Bach, Thiemann, Zucco, *Looking for the Missing Rich*, DIW Discussion Paper 1717 (Jan 2018) | Abstract and conclusions. |
| Bundesbank 2025 | Bundesbank Monthly Report, April 2025, results of the 2023 household wealth survey (PHF) | Read via a page-extraction tool, not as a PDF. Quotes below are as returned by the tool; recheck against the PDF before publishing. |
| OECD 2018 | OECD, *The Role and Design of Net Wealth Taxes in the OECD*, OECD Tax Policy Studies, 12 Apr 2018 | Executive summary, chapter 1 (printed pp. 16 to 18), chapter 2 composition and inequality pages, chapter 5 conclusions (printed p. 99). Not every chapter. |
| Mirrlees | Mirrlees et al., *Tax by Design* (IFS, 2011), chapter 15 "Taxes on Wealth Transfers" | Opening pages of the chapter (printed pp. 347 to 348). |

---

## A. Effective total tax rates: the very rich versus everyone else

### United States

**1. The top 400 pay a lower total tax rate than the average American, on the authors' benchmark.** `V*`
- Figure: total effective tax rate (all taxes, all levels of government, as % of economic income): top 0.0002% (about the top 400) **23.8%**, 2018 to 2020 average; top 0.00005% (about the top 100) **22.0%**; all US population **30.2%**; top labour-income earners **45%**.
- Source text (abstract): "averaged 24% in 2018–2020 compared with 30% for the full population and 45% for top labor income earners." Table 2, Panel A, "Total effective tax rate (% of economic income)": 30.2% / 23.8% / 22.0% / 26.6% (all / top 400 / top 100 / next 300).
- Caveats: the authors match the Forbes 400 list to IRS returns. "Economic income" is basic-price national income (labour plus capital income, with company profits allocated to owners). Corporate tax is fully allocated to shareholders; the authors say other methods (CBO's) "would lead to lower top-end tax rates". Working paper.
- URL: https://gabriel-zucman.eu/files/BSYZ2025NBER.pdf (also https://www.nber.org/papers/w34170). Opened 2026-11-08.

**2. For the top 400, the individual income tax is only about 11% of economic income; the corporate tax carries about 9 points.** `V`
- Figure: individual income and payroll taxes 11.0% of economic income (all population 20.5%); worldwide corporate tax about 8.9 points; business property taxes about 3.4 points (top 400, 2018 to 2020).
- Source text: "Out of the top 400's effective tax rate of 23.8%, about 9 points comes from the corporate tax." "[B]usiness property taxes … contribute 3.4 points." Table 2 individual income and payroll row: 20.5% / 11.0% / 8.0% / 15.6%.
- Why it matters: any claim that billionaires pay "nothing" is wrong. They pay corporate tax through the companies they own. The gap is in the personal income tax.
- URL: as entry 1. Opened 2026-11-08.

**3. The reason is a narrow personal income tax base: taxable income is a small share of economic income.** `V`
- Figure: for the top 100, taxable individual income is "one-third of economic income compared with two-thirds for the overall population and nearly 100% for top labor income earners." For the top 400 the ratio is 40% (section 3.4, Figure 3a) against 70% for the whole population.
- Mechanism in the paper: private C-corporations owned by the top 400 distribute "less than 10% of their profits in dividends"; passthrough business income is "negative for the top 400 as a whole" despite positive book income.
- URL: as entry 1. Opened 2026-11-08.

**4. Taxes paid were small relative to wealth.** `V`
- Figure: total taxes paid by the top 400 were **1.3% of their wealth** in 2018 to 2020 (2.7% in 2010 to 2013, 2.0% in 2014 to 2017). Of the 1.3%, 0.7 points are corporate and business property taxes and individual income taxes (federal, state, local) are 0.6% of wealth.
- Source text: "Total taxes paid by the top 400 amounted to 2.7% of their wealth in 2010–13, down to 2.0% in 2014–17, and 1.3% in 2018–2020."
- URL: as entry 1. Opened 2026-11-08.

**5. Taxable income covered only about a third of the rise in top-400 wealth over 2010 to 2019.** `V`
- Source text: "taxable individual income only accounts for about one-third of the 2010–2019 rise in their wealth."
- URL: as entry 1. Opened 2026-11-08.

**6. Estate and gift taxes add very little.** `V`
- Figure: top-400 decedents paid **0.8% of wealth** in estate tax when married and **7%** when single. Gross estates were about 39% of the Forbes wealth estimate at death (single decedents).
- Source text (abstract): "Top-400 decedents paid 0.8% of their wealth in estate tax when married and 7% when single." Section 3.2: "The value of their gross estate is 39% of the Forbes estimate of their wealth."
- URL: as entry 1. Opened 2026-11-08.

**7. The top-400 rate fell after the 2017 tax law.** `V`
- Figure: about 30% in 2010 to 2017, 24% in 2018 to 2020. Source text: "The top-400 effective tax rate fell from 30% in 2010–2017 to 24% in 2018–2020." (abstract).
- URL: as entry 1. Opened 2026-11-08.

**8. The federal individual income tax paid by the 400 richest was about 8 to 10% of their income including unrealised gains.** `V*`
- Figure: CEA/OMB 2021: **8.2%** for 2010 to 2018, sensitivity range 6 to 12%. Yagan 2023 (peer-reviewed volume): **9.6%** nominal, **12.0%** real (inflation-adjusted); sensitivity ranges 6.7 to 14.6% (nominal) and 8.4 to 17.9% (real).
- Source text (CEA): "we estimate an average Federal individual income tax rate of 8.2 percent for the period 2010-2018." Yagan abstract: "9.6 percent in nominal terms and 12.0% in real (inflation-adjusted) terms."
- Caveats: this is the federal individual income tax only, divided by "Haig-Simons income" (change in wealth plus taxes). It excludes corporate tax, state tax and payroll tax, so it is not a total tax rate. The author notes his estimate "may be overestimates by construction" because the denominator also leaves out some items. The 2021 piece was by Greg Leiserson (CEA) and Danny Yagan (OMB). It is **not** a paper by Balkir. The brief's "Balkir/Treasury 2021" label is a misattribution; use "White House Council of Economic Advisers and OMB, 2021".
- URLs: https://bidenwhitehouse.archives.gov/cea/written-materials/2021/09/23/what-is-the-average-federal-individual-income-tax-rate-on-the-wealthiest-americans/ ; https://eml.berkeley.edu/~yagan/Top400TaxOxREP.pdf . Opened 2026-11-08.

**9. On a wealth-growth basis (Haig-Simons), the top 400 total rate over 2010 to 2019 was about the same as the population's.** `V` (this one cuts against the simple "billionaires pay less" line; see G1)
- Figure: top 400 **21.2%**, whole population **21.5%** (taxes cumulated 2010 to 2019 divided by change in wealth plus taxes plus consumption).
- Source text: "The top 400 Haig-Simons total effective tax rate is 21.2% over 2010–19, similar to the Haig-Simons tax rate for the entire population (21.5%)." Table 2 Panel B: 21.5% / 21.2% / 19.4% / 24.6%.
- URL: as entry 1. Opened 2026-11-08.

### France

**10. In 2016 the effective direct tax rate rose with income up to the top 0.1% and then fell for the very richest.** `V`
- Figure: **46%** for the top 0.1% of tax households; **26%** for the top 0.0002% (the note's "milliardaires"). Income tax falls to "environ 2 %" of economic income in the top 0.001%.
- Source text (summary page): "passant de 46 % pour les 0,1 % les plus riches, à 26 % pour les 0,0002 % les plus riches". "L'impôt sur les sociétés est le seul impôt atteignant des taux substantiels pour les « milliardaires »."
- Definition: "revenu économique" = tax income plus non-contributory social contributions plus retained profits of companies the household controls (stakes of 10% or more). Pension and unemployment contributions are excluded from the tax numerator (box 3). Direct taxes only (income tax, ISF, CSG/CRDS, CEHR, non-contributory social contributions, corporate tax with an estimate for foreign tax). Data are for 2016 and do not include later reforms; the note says so itself.
- URL: https://www.ipp.eu/wp-content/uploads/2025/05/92_Note_IPP_Billionaires-version-actualisee.pdf (page https://www.ipp.eu/publication/note-ipp-n92-quels-impots-les-milliardaires-paient-ils/). Opened 2026-11-08.

**11. For French billionaires the ISF and the income tax were a negligible part of their total income.** `V`
- Source text: "Pour les « milliardaires », l'impôt sur le revenu ou l'ISF ne représentent qu'une fraction négligeable de leurs revenus globaux, alors que l'impôt sur les sociétés est le principal impôt acquitté."
- URL: as entry 10. Opened 2026-11-08.

**12. The ISF cap: the IPP note says the Constitutional Council forced the ISF to be capped by reference to personal income, so that, in the note's words, it could not correct the fall in rates at the top.** `V*`
- Source text: "le Conseil Constitutionnel, particulièrement dans sa décision 2012-662, a contraint l'ISF à être plafonné à un certain pourcentage du revenu personnel", and "il a déjà été montré que l'ISF n'a pu corriger la régressivité que nous documentons (Bach et al., 2021)".
- Caveat: this is the IPP's description. The France Stratégie committee reports themselves (which contain the cap finding the brief asked for) could not be opened; see H1.
- URL: as entry 10. Opened 2026-11-08.

**13. The note's counterfactual: if billionaires' economic income were taxed at the personal-income scale, their rate would be 59%, not 26%.** `V*`
- Source text: "le taux effectif global d'imposition du revenu économique passerait de 26 % à 59 %" "si le barème des impôts personnels leur était appliqué" and no behavioural response. This is a model counterfactual with no behavioural response. Do not present it as revenue.
- URL: as entry 10. Opened 2026-11-08.

**14. The authors say the same pattern is probably common across European countries.** `V`
- Source text (summary): "Cette régressivité au sommet de la distribution est probablement commune à l'ensemble des pays européens".
- URL: as entry 10. Opened 2026-11-08.

### Norway and Sweden

**15. In Norway and Sweden effective rates fall from about 50% for the upper middle class to 15 to 20% at the top.** `V*`
- Figure: "about 50%" to "about 15%–20%", top 0.0005% (about the population of US-dollar billionaires), 2018 to 2020. Section 5.1: "50%–55% on average for individuals in P95-99 to about 15%–20% in the top 0.0005%." In Sweden the top 0.01% rate "was halved between 2000 and 2020, from 30% to 15%".
- Mechanism: about half of the income of the top 0.1% is retained in personal holding companies; holding companies "shield around half of dividend distributions from individual income taxation".
- Caveat: working paper (NBER WP 35534, July 2026), not peer reviewed.
- URL: https://gabriel-zucman.eu/files/RSZ2026.pdf (also https://www.nber.org/papers/w35534). Opened 2026-11-08.

**16. Norway's wealth tax absorbs very little of top income, because private-company shares are valued far below market.** `V` (important design lesson, and unfavourable to the way Norway's tax works today; see G4)
- Figure: the wealth tax "absorbs barely 1% of income at the top of the distribution in Norway" (2018 to 2020). Shares in private businesses "enter the wealth tax base for only a tenth of their market value."
- The paper also reports that Sweden exempted unlisted shares before it abolished the wealth tax in 2007, and says a wealth tax "based on such market values would serve as an effective backstop to the income tax" (section 1, authors' conclusion, not a measured outcome).
- URL: as entry 15. Opened 2026-11-08.

**17. Europe versus the US.** `V`
- Source text (BSYZ introduction): "the top-end effective rates we obtain in the United States are higher than in Europe." Netherlands "less then [sic] 20%" for the top 0.0001% (Bruil et al.); France 26% for the top 0.0002% in 2016 (Bach et al.).
- URL: as entry 1. Opened 2026-11-08.

### Switzerland and Germany

**18. Not found.** I did not find an official ESTV or DIW/Bundesbank estimate of the total effective tax rate of the richest households. Do not write a Swiss or German "effective rate at the top" number. See H3 and H4.

### A minimum-wage worker's total burden

**19. Not found from a primary source.** The only population-wide figure I verified is the all-US-population total effective rate of **30.2%** of economic income (BSYZ Table 2, 2018 to 2020; entry 1), which includes sales and property taxes and payroll taxes. I could not open CBO's distribution tables (blocked to my tools) or OECD *Taxing Wages* country tables. There is no verified rate for a minimum-wage worker. See H2.

---

## B. Composition of top wealth

### United States (Federal Reserve DFA)

All DFA numbers in this section are my calculations from the Fed's CSV files (quarterly, in millions of dollars) for **2026 Q2**, the latest quarter in the file I downloaded. They are household balance-sheet data with the Fed's own top-tail adjustment; the Fed revises them.

**20. Top 0.1% of US households by net worth: where the money is.** `V*`
- Figure (share of the group's total assets, 2026 Q2; group total assets $28.17 trillion, net worth $27.87 trillion, 136,779 households):
  - corporate equities and mutual fund shares: **57.3%**
  - equity in unincorporated businesses ("Miscellaneous other equity" in the detail file): **17.0%**
  - owner-occupied real estate: **7.0%**
  - deposits 5.1%, money-market funds 3.5%, debt securities 3.9%, consumer durables 2.6%, pensions 1.7%, life insurance and annuities 1.0%, other 0.9%.
- Liabilities were only about 1.1% of assets.
- Definitions (Fed file `dfa-data-definitions.txt`): "Real estate: Owner-occupied real estate including vacant land and mobile homes at market value". "Unincorporated Business: Proprietors' equity in noncorporate business (Includes non-publicly traded businesses and real estate owned by households for renting out to others)".
- **Caveat that changes the wording on real estate:** the DFA "real estate" line is owner-occupied housing only. Rented-out property sits inside unincorporated business equity. So "7% real estate" understates real estate. Safe wording: "owner-occupied homes are about 7% of the assets of the top 0.1%". Do not write "real estate is only 7% of billionaire wealth". The DFA also does not split listed from unlisted corporate stock, so I cannot give a listed versus unlisted split from this source.
- Same data, other years: equities and mutual funds 43.5% (2016 Q2) and 36.2% (2006 Q2); owner-occupied real estate 8.5% (2016 Q2) and 10.3% (2006 Q2); unincorporated business 24.6% (2016 Q2) and 26.8% (2006 Q2).
- URL: https://www.federalreserve.gov/releases/z1/dataviz/dfa/distribute/table/ (data: https://www.federalreserve.gov/releases/z1/dataviz/download/zips/dfa.zip). Opened 2026-11-08.

**21. The top 0.1% hold a much larger share of business equity than of housing.** `V`
- Figure (2026 Q2): the top 0.1% hold **28.5%** of all household "unincorporated business" equity and **3.9%** of all owner-occupied real estate (the shares file `dfa-networth-shares.csv` gives 28.5 and 3.9, matching my sums from the levels file).
- URL: as entry 20. Opened 2026-11-08.

**22. Unrealised gains are a large part of top wealth (Treasury estate data).** `V*`
- Figure: in the 2010 estate-tax data, **about 44%** of estates above $20 million was unrealised capital gains. Within those gains: 30% publicly traded stock, 36% private stock, 15% other business assets, 14% real estate (only 2% from a main residence), 3% art and collectibles, 2% other. SYZ add: "81% is in business shares" and "only 32% is in assets with markets".
- Source text: "about 44% of top estates (in excess of $20m) are in unrealized capital gains (Table 2, p. 10)" citing US Treasury (2014).
- Caveats: I read this in the SYZ paper, not in the Treasury 2014 document it cites (which I have not opened). SYZ is an advocacy-adjacent proposal paper by wealth-tax supporters. The figure is for 2010 estates.
- URL: https://gabriel-zucman.eu/files/SYZ2021.pdf . Opened 2026-11-08.

**23. Survey of Consumer Finances (SCF) based estimate for the very richest.** `V*`
- Figure: for households above $50 million, capital gains are **50% of wealth** (54% above $100 million); about 90% of the gains are in business shares and 25% in publicly traded stock; real estate about 10%. Aggregate unrealised gains: $33.5 trillion in 2020 (160% of GDP), of which households above $50 million hold **$8 trillion**; more than half of all gains belong to the top 1%.
- Source text: "capital gains are 50% of wealth." "[U]nrealized capital gains of the super wealthy currently stand at $8 trillion." Residences "are only 2% of the unrealized capital gains of the rich."
- Caveat: SYZ aged the 2019 SCF to 2020 and combined it with the Forbes list. It is the authors' estimate, not a published Fed table. The Fed's own SCF gains tables were not opened (H6).
- URL: https://gabriel-zucman.eu/files/SYZ2021.pdf . Opened 2026-11-08.

**24. Forbes-based concentration of the very top (a media list, use sparingly).** `V*`
- Figure: Forbes 400 wealth was 0.9% of US household wealth in 1982 and 4.1% in 2025; in GDP terms 2% (1982) to 20% (2025).
- Source text: BSYZ introduction. The Forbes list is not an official dataset; the paper uses it because it is the only list of named individuals.
- URL: as entry 1. Opened 2026-11-08.

### Germany and Norway

**25. Germany: top fortunes are mostly business and real assets, and surveys miss them.** `V*`
- DIW 1717: the survey (HFCS) top-1% share of 24% rises to **31%** (wave 1, 2008 to 2011) and **33%** (wave 2, 2011 to 2015) after adding rich-list fortunes and a Pareto fit. Top 0.1% "hikes up from 4 to 16 percent in the first wave" (the sentence is cut off in my extract, so the second-wave figure was not read).
- On composition, the paper says low interest rates raise "the market valuation of investments such as real estate, businesses, and corporate shares. As the latter dominate top wealth strata". I did not find a percentage composition table for the German top in DIW 1717.
- Bundesbank 2025 (2023 PHF survey): top 10% hold 54% of net wealth in the survey (55% in 2017, 56% in 2021) and "more than 60%" in the distributional wealth accounts that add the rich list; Gini 72.4% (2021: 72.8%); median net wealth about €103,200; "The majority of these households' wealth is also directly attributable to their business ownership" (for the richest group). The Bundesbank warns very wealthy households are "not sufficiently represented" in the sample.
- URLs: https://www.diw.de/documents/publikationen/73/diw_01.c.575768.de/dp1717.pdf ; https://publikationen.bundesbank.de/publikationen-en/reports-studies/monthly-reports/household-wealth-and-finances-in-germany-results-of-the-2023-household-wealth-survey-954660 . Opened 2026-11-08.
- Not found: Bach et al.'s DIW composition of the largest German fortunes (the MPIfG paper on Germany's largest private fortunes appeared in search results but I did not open it).

**26. Norway: shares in private businesses are the main asset at the top.** `V*`
- Source text (RSZ 2026, section 5): "most of the wealth at the top of the distribution corresponds to shares in private businesses" (Figure A7, not opened). I did not open an SSB table giving the asset mix of the richest Norwegians.
- URL: as entry 15. Opened 2026-11-08.

### The "buy, borrow, die" mechanism

**27. The mechanism in primary-source wording: gains are taxed late, at low rates, or never.** `V`
- CEA 2021: "if a wealthy investor never sells stock that has increased in value, those investment gains are wiped out for income tax purposes when those assets are passed on to their heirs under a provision known as stepped-up basis." Yagan 2023: unrealised gains "avoid income tax until sale or gift … and never face income tax if bequeathed at death."
- Preferred rates: dividends and stock sales are taxed at a maximum 20% (23.8% with the net investment income tax) against 37% (40.8%) for ordinary income (CEA 2021).
- URLs: as entry 8. Opened 2026-11-08.

**28. Borrowing: I could not verify any primary-source number on how much of the richest households' spending is funded by loans against shares.** See H5.

---

## C. Concentration of wealth

### Share of net wealth held by the top 10%, 1% and 0.1% (WID, adults, equal split; per cent)

Source: World Inequality Database bulk file, variable `shweal992j`, the cited year columns; downloaded and read 2026-11-08. URL: https://wid.world/bulk_download/wid_all_data.zip (data portal https://wid.world/data/).

| Country | Group | 1990 | 2000 | 2010 | 2020 | 2024 |
|---|---|---|---|---|---|---|
| **United States** | Top 10% | 65.1 | 68.7 | 73.0 | 71.0 | 69.5 |
| | Top 1% | 29.0 | 32.3 | 34.6 | 35.1 | 34.8 |
| | Top 0.1% | 12.6 | 15.9 | 17.4 | 18.1 | 18.4 |
| **Norway** | Top 10% | 50.5 | 51.2 | 51.2 | 52.5 | 52.7 |
| | Top 1% | 23.5 | 24.2 | 24.2 | 23.2 | 23.5 |
| | Top 0.1% | 15.1 | 15.7 | 15.7 | 12.0 | 12.3 |
| **Switzerland** | Top 10% | 55.5 | 59.5 | 59.7 | 62.2 | 62.8 |
| | Top 1% | 24.1 | 29.0 | 28.8 | 30.4 | 31.5 |
| | Top 0.1% | 11.1 | 15.4 | 14.4 | 15.2 | 16.4 |
| **Sweden** | Top 10% | 60.4 | 63.9 | 66.1 | 67.7 | 68.2 |
| | Top 1% | 24.0 | 26.1 | 27.1 | 26.1 | 27.5 |
| | Top 0.1% | 12.4 | 12.5 | 14.1 | 12.2 | 13.9 |
| **Germany** | Top 10% | 50.9 | 57.4 | 59.1 | 58.3 | 58.5 |
| | Top 1% | 21.9 | 26.7 | 27.3 | 27.5 | 27.9 |
| | Top 0.1% | 11.6 | 13.0 | 14.5 | 13.0 | 13.4 |
| **France** | Top 10% | 50.5 | 60.5 | 58.3 | 58.9 | 59.9 |
| | Top 1% | 17.7 | 29.8 | 24.6 | 26.0 | 27.7 |
| | Top 0.1% | 7.2 | 14.2 | 10.4 | 11.4 | 13.3 |
| **Uruguay** | Top 10% | 77.8 | 77.8 | 76.7 | 75.9 | 76.7 |
| | Top 1% | 39.7 | 39.7 | 36.9 | 39.4 | 40.5 |
| | Top 0.1% | 18.6 | 18.6 | 16.9 | 17.5 | 18.3 |
| **Colombia** | Top 10% | 72.5 | 72.5 | 71.9 | 72.2 | 71.9 |
| | Top 1% | 39.9 | 40.0 | 39.2 | 39.6 | 39.2 |
| | Top 0.1% | 21.5 | 21.6 | 21.0 | 21.2 | 21.0 |

**29. The table above.** `V*`
- Caveats:
  - **Uruguay and Colombia:** the values are identical from 1980 to about 2000 (for example Uruguay top 1%: 39.8 / 39.7 / 39.7 in 1980 / 1990 / 2000), which points to carried-forward or interpolated values. I did not open the WID metadata to confirm. Treat the level in recent years as the usable number and do not write a "trend" for these two countries from this file.
  - WID is a modelled series that combines surveys, tax data and rich lists; it is not the national statistics office figure. Where an official figure exists it can differ a lot (entries 31 and 32).
  - Sweden's bottom 50% is on net negative wealth in WID (`p0p50` is -10.9% in 2024), because of household debt.
  - Germany's 1990 values predate or straddle reunification, so avoid comparing 1990 with later years there.
- Opened 2026-11-08.

**30. United States, Federal Reserve DFA, share of household net worth.** `V`
- Figure: top 0.1% **8.6%** (1989 Q3) → 11.2% (2000 Q1) → 12.4% (2016 Q1) → **15.0%** (2026 Q2; 14.5% in 2026 Q1). Top 1% 22.8% → 27.9% → 30.4% → **32.5%** (2026 Q2). Top 10% 60.8% → 63.8% → 69.7% → 68.9%. Bottom 50% 3.5% → 3.2% → 1.2% → 2.3%.
- The FRED page for series WFRBSTP1300 shows the same top-0.1% values: 8.6 (1989-07-01), 14.5 (2026-01-01), 15.0 (2026-04-01); "Last updated: 2026-09-18".
- Top 1% = "TopPt1" plus "RemainingTop1" categories in the Fed's file; top 10% adds "Next9". My sums.
- Note the DFA (32.5% top 1% in 2026 Q2) and WID (34.8% in 2024) differ by about two points. Choose one source per page and name it.
- URLs: https://www.federalreserve.gov/releases/z1/dataviz/dfa/distribute/table/ ; https://fred.stlouisfed.org/data/WFRBSTP1300 . Opened 2026-11-08.

**31. Switzerland, official tax-data figure: the top 1% hold 45.8% of taxable net wealth (2022).** `V*`
- Figure: top-1% share **45.8%** (2022), 45.9% (2021), 44.8% (2020); Gini 0.823 (2022). In several cantons it is above 60% (Nidwalden, Schwyz, Zug, Basel-Stadt, Obwalden) and 67.3% in Geneva.
- Source text: "Im Jahr 2022 lag der gesamtschweizerische Top-1 % Vermögensanteil bei 45,8 %".
- Caveats: ESTV works from cantonal tax declarations in 11 wealth classes and estimates the top share with a Pareto method. It covers taxable wealth, so it does not include pension-fund assets and uses tax valuations. It is far above the WID figure for the top 1% (31.5% for 2024). Do not put the two side by side without saying why they differ.
- Also in the note (footnote 3): wealth taxes contributed "knapp 4 Prozent" of total tax revenue in Switzerland in 2018 per OECD data, "gut 1 Prozent" in Norway and "etwa 0,5 Prozent" in Spain.
- URL: https://www.estv2.admin.ch/stp/berichte/stp-berichte-2022-vermoegen.pdf . Opened 2026-11-08.

**32. Norway, official figures from Statistics Norway.** `V*`
- Figure (share of total net wealth, SSB table 10318, households): top 10% **51.0%** (2010), 50.6% (2015), 53.7% (2020), **51.9%** (2024). Top 1% **20.1%**, 19.8%, 23.8%, **21.7%**. Top 0.1% **9.8%**, 9.4%, 12.3%, **10.3%**. Decile 1 holds negative wealth (-5.7% in 2010, -2.7% in 2024).
- Caveat: the SSB series is a register-based "estimated net wealth". I did not verify exactly how SSB values private businesses and housing, so do not compare it with WID without a note. WID shows the top 1% at 23.5% for 2024.
- URL: https://data.ssb.no/api/v0/en/table/10318 (StatBank table 10318). Opened 2026-11-08.

**33. Germany: concentration is higher than surveys show.** See entry 25 (DIW 1717: top 1% 24% in the survey, 31 to 33% with the rich list; Bundesbank top 10% 54% in the survey, more than 60% with the rich list).

**34. Sweden and the Equality Commission.** Not found. I did not open the Equality Commission's (Jämlikhetskommissionen) report or a Statistics Sweden top-1% table. WID (table above) is the only Swedish concentration source here. See H4.

### How fast top fortunes have grown: United States, DFA, nominal dollars

**35. Over 20 and 10 years the top 0.1% grew faster than total household wealth and than GDP.** `V*`
- Calculation (all from Fed DFA files and FRED nominal GDP, 2006 Q2, 2016 Q2, 2026 Q2):

| | 2006 Q2 | 2016 Q2 | 2026 Q2 | ×, 20 years | ×, 10 years |
|---|---|---|---|---|---|
| Net worth of top 0.1% ($ trillion) | 6.76 | 10.85 | 27.87 | **4.12** | **2.57** |
| Net worth of all households ($ trillion) | 61.79 | 86.45 | 185.65 | 3.00 | 2.15 |
| Net worth of bottom 50% ($ trillion) | 1.49 | 1.04 | 4.28 | 2.87 | 4.11 |
| Nominal GDP ($ trillion) | 13.75 | 18.71 | 32.56 | 2.37 | 1.74 |
| Top-0.1% net worth as % of GDP | 49% | 58% | 86% | | |
| Average net worth per household, top 0.1% ($ million) | 58.9 | 86.2 | 203.7 | 3.46 | 2.36 |
| Average net worth per household, bottom 50% ($ thousand) | 26.0 | 16.6 | 63.3 | 2.44 | 3.82 |

- Source: DFA `dfa-networth-levels-detail.csv` ("Net worth", "Household count") and FRED GDP (https://fred.stlouisfed.org/data/GDP: 13,753.4 / 18,711.7 / 32,563.0 billion dollars, seasonally adjusted annual rate, last updated 2026-10-29). Ratios are mine.
- **Do not claim** that the top fortunes grew faster than the bottom over the last 10 years in percentage terms: the bottom 50% grew faster from a very small base (×4.11 against ×2.57). The honest claim is about dollars and about the 20-year span (see G6).
- I did not calculate a median-wealth series (the DFA gives only group totals). "Bottom 50% average" is a proxy, not a median.
- No equivalent calculation was done for Norway, Switzerland, Sweden, Germany, France, Uruguay or Colombia.
- Opened 2026-11-08.

---

## D. How a wealth tax differs from other taxes (base, timing, avoidability)

**36. What a net wealth tax is (base).** `V`
- OECD 2018 (printed p. 16): net wealth taxes are "recurrent taxes on individual net wealth stocks". They "include national and subnational recurrent taxes on a wide range of movable and immovable property, net of debt". They are "distinct from other taxes on capital, including taxes on capital income and taxes on wealth transfers", and, "compared to recurrent taxes on immovable property, they are taxes on a broad range of property and debts are deductible".
- URL: https://www.oecd.org/content/dam/oecd/en/publications/reports/2018/04/the-role-and-design-of-net-wealth-taxes-in-the-oecd_g1g89919/9789264290303-en.pdf . Opened 2026-11-08.

**37. Timing and base versus an income or capital gains tax.** `V`
- OECD 2018 (printed p. 99): "a net wealth tax is equivalent to a proportional tax on a presumptive return, meaning that the tax is levied irrespective of the actual returns earned on savings", and "a wealth tax is in theory levied on an accrual basis while income taxes are typically levied upon realisation". It "can potentially be more comprehensive than a capital income tax, covering both income and non-income generating assets."
- OECD 2018 (printed p. 56): taxing capital gains on accrual "prevents the deferral of realised capital gains and lock-in effects" and enhances fairness, but involves practical problems.
- Income and gains taxes on realisation: the CEA 2021 text (entry 27) shows the gain never enters the tax base if the asset is held to death.
- Same URL as entry 36. Opened 2026-11-08.

**38. Versus property tax and inheritance tax.** `V`
- Property tax: a recurrent tax on immovable property only; the OECD contrasts it with the net wealth tax, which covers "a broad range of property" with debts deductible (printed p. 16, entry 36). In the US data (entry 20), owner-occupied housing is 7.0% of the top 0.1%'s assets, so a tax on homes alone reaches little of top wealth (rented-out property is counted under business equity and would also be missed by a residence-only tax; I did not quantify that).
- Inheritance: OECD executive summary: "there is a strong case for an accompanying inheritance tax on efficiency, equity and administrative grounds." The Fed/Treasury evidence on how little estate tax the top pay is at entry 6 (0.8% of wealth when married, 7% when single).
- URL: as entry 36. Opened 2026-11-08.

**39. Avoidability: where wealth taxes leak.** `V*`
- OECD 2018 (printed p. 17): reasons for repeal were efficiency costs and "risks of capital flight", "narrow tax bases as well as tax avoidance and evasion" and administrative cost.
- France: IPP n°92 and the Constitutional Council cap (entry 12). Norway and Sweden: RSZ 2026 (entry 16): low valuation of private businesses, Swedish exemption of unlisted shares.
- OECD printed p. 18: Switzerland collected "considerably higher revenues" from its wealth taxes thanks to "comparatively low exemption thresholds and broader tax bases"; Norway's revenues were low "in part because of the very favourable valuation rules that apply to primary residences".
- URL: as entry 36. Opened 2026-11-08.

**40. The Mirrlees Review argued against an annual wealth tax in the UK.** `V` (an opposing source; see G3)
- Source text (*Tax by Design*, ch. 15, printed pp. 347 to 348): "Levying a tax on the stock of wealth is not appealing." The Review says a wealth tax "is equivalent to taxing the normal return to savings but exempting excess returns", with a worked example: a 20% tax on a 5% return equals a 1% tax on the stock. "[P]ractical experience has not been encouraging" in "France, Greece, Norway, and Switzerland".
- URL: https://ifs.org.uk/sites/default/files/output_url_files/taxbydesign.pdf . Opened 2026-11-08.

**41. IMF, and a consumption tax comparison.** Not found. I did not open an IMF document or a primary source comparing a wealth tax with a consumption tax. See H7.

---

## E. The OECD tally of countries with net wealth taxes

**42. 1990: twelve. 2017: four.** `V`
- Figure: **12** OECD countries levied individual net wealth taxes in 1990; **4** in 2017.
- Source text, executive summary (PDF page 13, printed p. 11): "While 12 countries had net wealth taxes in 1990, there were only four OECD countries that still levied recurrent taxes on individuals' net wealth in 2017." Chapter 1 (PDF page 18, printed p. 16): "The number of OECD countries levying individual net wealth taxes dropped from 12 in 1990 to 4 in 2017 (Figure 1.1)." Figure 1.1 source: "OECD Net Wealth Tax Questionnaire".
- The four in 2017: "France, Norway, Spain and Switzerland were the only OECD countries that levied net wealth taxes."
- Repeals listed in the report: Austria (1994), Denmark (1997), Germany (1997), the Netherlands (2001), Finland, Iceland and Luxembourg (all 2006), Sweden (2007). Spain used a 100% credit in 2008 and reinstated the tax in 2011; Iceland reinstated it 2010 to 2014. That list (8 repealed plus the 4 left) adds up to 12; the report gives the number 12, and the list of twelve is my inference from it.
- Date caveat: this is the situation in 2017, as published in 2018. The report is not a current count. France replaced the ISF with a real-estate-only tax (IFI) in 2018, so "France" in the 2017 list is no longer a general net wealth tax. I have not verified any later OECD count.
- Report page: https://www.oecd.org/en/publications/the-role-and-design-of-net-wealth-taxes-in-the-oecd_9789264290303-en.html ; PDF as entry 36. Opened 2026-11-08.

**43. Revenue was low.** `V`
- Figure (2016): net wealth tax revenue ranged from **0.2% of GDP in Spain to 1.0% of GDP in Switzerland**, and from **0.5% of total tax revenue in France to 3.7% in Switzerland**.
- Source text (printed p. 18): "In 2016, tax revenues from individual net wealth taxes ranged from 0.2% of GDP in Spain to 1.0% of GDP in Switzerland. As a share of total tax revenues, they ranged from 0.5% in France to 3.7% in Switzerland (Figure 1.3)."
- Caveat: the bar labels of Figure 1.3 did not extract cleanly from the PDF. Use the sentence, not the figure labels. The ESTV 2022 note (entry 31) gives a 2018 OECD-based figure of "knapp 4 Prozent" for Switzerland.
- Same URL as entry 36. Opened 2026-11-08.

**44. The OECD's overall judgement (opposing, and it must be answered fairly).** `V` (see G3)
- Source text (executive summary): "from both an efficiency and equity perspective, there are limited arguments for having a net wealth tax in addition to broad-based personal capital income taxes and well-designed inheritance and gift taxes." But also: "there are stronger arguments for having a net wealth tax in the absence of broad-based personal capital income taxes and taxes on wealth transfers", and the report finds "a strong case for addressing wealth inequality through the tax system".
- Same URL as entry 36. Opened 2026-11-08.

**45. OECD on how unequal wealth is.** `V`
- Source text (printed p. 31): "the bottom 40% own only 3% of total household wealth"; "the top 10% of the wealth distribution hold half of total household wealth and the wealthiest 1% own almost a fifth" (18 OECD countries, from OECD 2015, so data are older than 2018).
- Same URL as entry 36. Opened 2026-11-08.

**46. OECD on tax-rate trends.** `V`
- Figure: the OECD-average top statutory personal income tax rate fell from **65.7% in 1981** to **50.6% in 1990**, **41.4% in 2008**, and **43.3% in 2016**; the average statutory corporate rate fell from 47% (1981) to 24% (2017); the average tax on dividends from 75% to 42%.
- Source: printed p. 17, Figure 1.2. Same URL as entry 36. Opened 2026-11-08.

---

## G. Results unfavourable to a wealth tax, or that contradict a common claim made for it

1. **"Billionaires pay a lower tax rate than ordinary people" depends on the measure.** On total tax relative to economic income in 2018 to 2020, yes (23.8% against 30.2%, entry 1). But in 2010 to 2017 the top-400 rate was about 30%, "similar to the US population average" (entry 7), and on a wealth-growth (Haig-Simons) basis the 2010 to 2019 rate was 21.2% against 21.5% (entry 9). Write the claim with the years and the measure.
2. **"Billionaires pay about 8%" is a federal individual income tax rate only** (entry 8). It leaves out corporate tax (about 9 points for the top 400, entry 2). Using it as a "total tax rate" is wrong and easy to rebut.
3. **The OECD and the Mirrlees Review both argue against an annual wealth tax where broad capital income taxes and inheritance tax already exist** (entries 40, 44). The OECD finds wealth taxes "more distortive and less equitable" than capital income taxes. A fair page should say this and then argue the other half: the OECD also says the case is stronger when capital is lightly taxed, and the US/French/Nordic data (entries 1, 10, 15) show capital at the very top is lightly taxed.
4. **Existing wealth taxes did a poor job at the top.** Norway's wealth tax absorbs "barely 1%" of top income because private businesses are valued at about a tenth of market value (entry 16); the French ISF was capped by income (entries 11, 12) and its holders paid little ISF relative to income (entry 11). The honest argument is for a better designed tax, not "the ISF/Norwegian tax worked".
5. **Revenue was low where wealth taxes existed** (0.2 to 1.0% of GDP, entry 43). For "it doesn't raise enough", note that Switzerland, with the broadest base and lowest exemption, raised the most (about 1% of GDP, nearly 4% of tax revenue).
6. **The bottom 50% of US households gained faster in percentage terms over the last 10 years** (×4.11 against ×2.57, entry 35), from a very low base. Use dollars, the 20-year span, or the top 0.1% share of GDP, not a percentage-growth league table over 10 years.
7. **Concentration is not rising everywhere.** Norway's top 1% share in WID is flat (23.5% in 1990, 23.5% in 2024), and its top 0.1% fell from 17.2% (2005) to 12.3% (2024); SSB's top 1% share is 20.1% (2010) and 21.7% (2024). Germany's Bundesbank Gini slipped from 72.8% to 72.4% between 2021 and 2023. Do not write "wealth concentration is rising in every country". Do not credit Norway's wealth tax for the Norwegian pattern (no causal evidence was read).
8. **Switzerland has the highest official top-1% share among the European countries covered (45.8%, entry 31) and the broadest wealth tax.** Do not claim wealth taxes by themselves reduce concentration.
9. **Top US effective rates are higher than European ones** (entry 17): "top-end effective rates … in the United States are higher than in Europe." For a European audience this supports the case; for a US audience it complicates "the rich pay less".
10. **A model gap, not a measured loss:** the 59% counterfactual (entry 13) assumes no behavioural response.

## H. Could not verify (do not use until checked)

1. **France Stratégie committee reports on the ISF cap.** The 2023 final report (4th report) is on the site of the successor body (strategie-plan.gouv.fr); my download returned a web page, not the PDF, and the English summary page listed topics only. I did not read the cap finding. A search snippet claimed the cap "aurait coûté de l'ordre de 2 milliards d'euros" and that its effect was negligible below the top decile; I did not confirm either. Next step: open the report PDF from the committee's page.
2. **A minimum-wage worker's total burden (income, payroll, consumption, property tax).** I could not read CBO's *Distribution of Household Income in 2021* (CBO's site refused my tool; I did not work around it), nor OECD *Taxing Wages*. Next step: open CBO publication 60341 in a normal browser, or OECD *Taxing Wages* country tables, and compute for the statutory minimum wage.
3. **ESTV/Swiss effective tax rate of the richest.** Nothing found.
4. **Sweden official concentration figure and the Equality Commission's wealth numbers; Swedish effective tax rate by wealth rank beyond RSZ 2026.** Not opened.
5. **Primary evidence on how much of the richest households' spending is financed by borrowing against shares ("borrow").** Not found. One search result suggested academic work finds the very rich do not borrow much, so "buy, borrow, die" may be better described as "buy, hold, die". That is a secondary snippet and I did not open it. Check before using "borrow" language.
6. **JCT, Treasury Green Book and Federal Reserve SCF tables on unrealised gains.** I read the Treasury 2010 estate data only through SYZ 2021 (entry 22) and did not open the Treasury 2014 document ("Step-Up Basis 2014", home.treasury.gov). The Senate Finance Committee 2021 hearing record on this subject: I could not find it, and I did not find any hearing record in the search results (the results were news coverage of Senator Wyden's October 2021 proposal). Do not cite a hearing.
7. **IMF on wealth taxes** and any consumption-tax comparison: not opened.
8. **JCT estimate of the top 400's total rate.** A search summary mentioned a JCT figure of "34%" for the top 400 and another of "26%" for the top 0.4% of families. I did not find either in a JCT document. Do not use.
9. **Colombia and Uruguay: national statistics.** Only WID was read, and WID shows signs of interpolation (entry 29). No DANE/DIAN or Uruguayan DGI wealth statistics opened.
10. **Cato's critique of the billionaire-rate estimates** (a blog post claiming the population rate falls from 30% to 25% on their adjustments): seen in search results only; not opened. If Cato's critique is likely to be raised, read it before publishing a comparison.
11. **Bach et al. (2025) on the effective wealth tax rate of ultra-high-net-worth households in France** (cited in RSZ 2026 as showing a very low effective rate): the paper itself was not opened.
12. **Current OECD count (after 2017).** Not checked.
13. **Bundesbank quotes** (entry 25) came through a page-extraction tool; recheck the exact wording in the PDF.

## I. Safe to write (headline facts)

Each is verified in a primary document above, with the wording limits shown.

1. "In 2018 to 2020 the 400 richest Americans paid total taxes equal to about 24% of their economic income, against 30% for the whole population (Balkir, Saez, Yagan and Zucman, NBER working paper, August 2025)." Say it is a working paper. (Entry 1)
2. "Their personal income tax was only about 11% of economic income; about nine points of their rate came from the corporate tax." (Entry 2)
3. "In 2018 to 2020 the top 400 paid taxes equal to 1.3% of their wealth." (Entry 4)
4. "Taxable income covered only about a third of the rise in their wealth in 2010 to 2019." (Entry 5)
5. "In France in 2016 the effective direct tax rate was 46% for the top 0.1% of households but 26% for the top 0.0002%, because company profits retained in holding structures are taxed at the corporate rate, not the income tax scale (IPP, June 2023)." (Entry 10)
6. "In Sweden and Norway effective tax rates fall from about 50% for the upper middle class to 15 to 20% for the top 0.0005% (Ring, Seim, Zucman, 2026, working paper)." (Entry 15)
7. "The top 0.1% of US households hold 15.0% of net worth (Federal Reserve, 2026 Q2), up from 8.6% in 1989." (Entry 30)
8. "The top 1% hold 32.5% and the bottom 50% hold 2.3% (Federal Reserve, 2026 Q2)." (Entry 30)
9. "The net worth of the top 0.1% of US households grew about 4.1 times between 2006 and 2026 and about 2.6 times over the last ten years; nominal GDP grew 2.4 and 1.7 times. Their combined wealth equals about 86% of GDP, against 49% in 2006." (Entry 35, my calculation from Fed and FRED files; say "calculated from")
10. "Owner-occupied homes make up about 7% of the assets of the top 0.1% of US households; corporate shares and mutual funds are 57% and business equity 17% (Federal Reserve, 2026 Q2)." Use exactly this wording about homes (entry 20).
11. "About 44% of the value of estates above $20 million in 2010 was unrealised capital gains (US Treasury estate data as reported by Saez, Yagan, Zucman)." (Entry 22)
12. "The OECD counted 12 countries with net wealth taxes in 1990 and four in 2017: France, Norway, Spain and Switzerland (OECD, 2018, executive summary and chapter 1, printed p. 16)." (Entry 42)
13. "In 2016, OECD countries' net wealth taxes raised between 0.2% (Spain) and 1.0% (Switzerland) of GDP." (Entry 43)
14. "The Swiss tax administration reports that the richest 1% of taxpayers held 45.8% of taxable net wealth in 2022." (Entry 31)
15. "Statistics Norway: the top 1% of households held 21.7% of net wealth in 2024 and the top 0.1% 10.3%." (Entry 32)
16. "A net wealth tax is equivalent to a tax on a presumed return and is levied whatever the actual return; an income or gains tax is typically levied only on realisation (OECD, 2018)." (Entry 37) Pair it with the OECD's own conclusion on when the case is strongest (entry 44).
17. "When a wealthy investor never sells, the gain is wiped out for income tax purposes at death through the stepped-up basis (White House CEA, 2021)." (Entry 27)

## J. Do not use

- "Billionaires pay about 8% tax" as a **total** rate (entry 8, G2). It is a federal individual income tax rate.
- "Balkir/Treasury 2021": the 2021 study is Leiserson and Yagan (CEA/OMB). Balkir co-wrote the 2024 to 2025 administrative-data work.
- "Real estate is only 7% of billionaire wealth" (entry 20 caveat): the 7% is owner-occupied housing in the top 0.1%; rental property is counted under business equity. Also the group is the top 0.1% of households, not billionaires.
- A listed versus unlisted equity split for the US top: the DFA does not give one, and I found none elsewhere.
- Any Swiss "top 1% = 45.8%" next to WID's "31.5%" without an explanation of method (entry 31).
- Any Uruguay or Colombia concentration trend from WID (entry 29).
- Any minimum-wage worker rate, any JCT percentage, any Senate Finance 2021 hearing citation, any France Stratégie ISF-cap number (H1, H2, H6, H8).
- Commercial or press sites that came up in searches and that I did not rely on: richify.ai (an ESTV re-publisher whose 45.8% happens to match ESTV but is not a source), Credit Suisse wealth reports, news summaries of the NBER paper, blog posts.
- The 59% French counterfactual as a projection of revenue (entry 13).
- "Concentration is rising everywhere" or "wealth taxes reduce concentration" (G7, G8).
- The "12 in 1990, 4 now" line with "now" meaning 2026: the OECD figure is for 2017.
