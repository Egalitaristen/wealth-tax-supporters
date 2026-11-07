# Source playbook

Layers, the sources that work for each, and query templates. Replace `{TERM}` with each search term for the area's languages (table at the end), `{AREA}` with the area name, `{UNIT}` with a geography unit name, and `{DOMAIN}` with a site's domain. Use quotation marks around exact phrases. Always open the page itself; a search snippet is not evidence.

**Where to start in a new country.** Do the first pass in this order, touching every layer once before going deep in any: legislature (bills, votes, motions) → parties → coalitions, NGOs, unions, think tanks → economists and academics → commentators and media → wealthy, business, faith, culture, funders → regional and local (sampled). Bulk lists first within each layer. See SKILL.md 6.3.

Named organisations below are **candidates to check**, not assumed supporters: each must meet the definition with its own evidence.

---

## Bulk lists first (harvest)

These produce many actors at once. Queue every one you find in `harvest.csv`.

| List | Where to find it | Query ideas |
|---|---|---|
| Roll-call votes on wealth-tax bills or amendments | Parliament vote records; vote trackers (e.g. HowTheyVote.eu for the European Parliament) | `{TERM} amendment vote {AREA}`, `{TERM} bill division` |
| Bill sponsors and co-sponsors | Parliament bill pages | `{TERM} bill cosponsors`, `"{TERM}" private member's bill` |
| Signatories of parliamentary or council motions | Motion registers (e.g. UK early day motions) | `"{TERM}" motion signatures` |
| Open letters | Campaign sites, newspapers that published them | `open letter "{TERM}" signatories`, `economists letter "{TERM}"`, `millionaires letter "tax us"` |
| Coalition and campaign members | "Our members" or "supporters" pages of coalitions | `"{TERM}" coalition members`, `campaign "{TERM}" "supported by"` |
| Report and commission authors | Report title pages, commission websites | `"{TERM}" commission report authors {AREA}` |
| Evidence to commissions and committees | Committee written-evidence pages | `"{TERM}" written evidence committee` |
| Conference motions | Union and party conference agendas and reports | `congress motion "{TERM}"`, `conference composite "{TERM}"` |

International lists worth checking for every area (for actors from that area): the Patriotic Millionaires and Millionaires for Humanity letters to world leaders; the "Proud to Pay More" letters; economists' letters supporting the G20 billionaire minimum tax; the European Citizens' Initiative "Tax the Rich" (organisers and partner organisations); Tax Justice Network and Global Alliance for Tax Justice member lists; Oxfam national affiliates.

---

## Layers

### L1 Legislatures (national, devolved, regional, supranational)
- Debate records (Hansard-type): search for each term; record speakers who argued for it.
- Written and oral questions calling for it.
- Votes, bills, motions: see bulk lists.
- Committee reports and witnesses.
- Queries: `site:{PARLIAMENT_DOMAIN} "{TERM}"`, `"{TERM}" MP speech {AREA}`, `"{TERM}" senator OR deputy {AREA}`

### L2 Parties
- Manifestos since 2010 (national and regional elections); the Manifesto Project corpus helps for older ones.
- Conference motions, policy documents, youth-wing and council-group positions.
- Queries: `"{TERM}" manifesto {YEAR}`, `party conference "{TERM}" motion passed`, `"young" party "{TERM}"`

### L3 Executive and government bodies
- Government programmes and coalition agreements; ministers' statements; tax commissions and their recommendations.
- Queries: `coalition agreement "{TERM}"`, `minister "{TERM}" {AREA}`, `tax commission recommends "{TERM}"`

### L4 Sub-national and local (sample first; see the local sweep pack below and SKILL.md 6.5)
- Regional parliaments and governments behave like national ones: bills, votes, motions. Start there.
- Local bodies vary. Test 5 to 10 units (largest cities, units run by the most sympathetic parties) before deciding to sweep more.
- Aggregators beat unit-by-unit searching: a party's list of councillors who signed a letter, union branch networks, a campaign's local groups, a motion template that councils copied.

### L5 Academia and economists
- Scholarly search (OpenAlex, Google Scholar, SSRN, RePEc) for papers recommending a wealth tax for the area; then check the author's own conclusion.
- Authors of books and policy reports; university research centres on inequality or tax.
- Economists' open letters (bulk).
- Queries: `"{TERM}" {AREA} working paper recommend`, `"case for a wealth tax" {AREA}`, `economist op-ed "{TERM}"`

### L6 Think tanks
- Publications pages; "our proposals" pages; responses to budgets.
- Queries: `think tank "{TERM}" {AREA} report`, `site:{DOMAIN} "{TERM}"`

### L7 Civil society: NGOs, campaigns, coalitions, charities
- National branches of tax-justice, anti-poverty, climate and development NGOs; campaign coalitions; charities speaking on inequality.
- Queries: `campaign "{TERM}" {AREA}`, `"tax the super-rich" campaign {AREA}`, `climate "{TERM}" campaign {AREA}`

### L8 Unions
- Confederation congress motions; each major union's policy pages and leaders' speeches; trades councils (local).
- Queries: `union "{TERM}" {AREA}`, `general secretary "{TERM}"`, `trades council "{TERM}"`

### L9 Media (opinion only)
- Opinion and comment sections of national and regional outlets; columnists' archives; editorials ("Our view", "The Guardian view on…" style); podcasts and video commentators with a public profile.
- Queries: `site:{OUTLET_DOMAIN}/commentisfree "{TERM}"`, `opinion "{TERM}" {AREA}`, `editorial "{TERM}"`, `column "why we need a wealth tax"`

### L10 Legal and tax professionals
- Professional tax journals and blogs; submissions to commissions; law-firm and chambers commentary; former tax-authority officials writing in favour; professional bodies' consultation responses.
- Queries: `tax barrister OR "tax lawyer" "{TERM}" in favour`, `former tax official "{TERM}"`, `accountant "{TERM}" design {AREA}`

### L11 Wealthy individuals and business
- Members and signatories of Patriotic Millionaires, Millionaires for Humanity, taxmenow (German-speaking countries), Proud to Pay More; business leaders' statements; business associations.
- Queries: `millionaire "tax me" {AREA}`, `billionaire supports "{TERM}"`, `CEO "{TERM}" {AREA}`

### L12 Faith, culture and other public figures
- Statements by church and faith bodies; artists', athletes' and writers' letters and statements.
- Queries: `bishop OR church "{TERM}"`, `actor OR musician "{TERM}" {AREA}`

### L13 Funders
- Grant databases (360Giving in the UK; Candid in the US; foundation annual reports elsewhere) for grants to wealth-tax work; funders listed on reports.
- Queries: `grant "wealth tax" foundation`, `"funded by" "{TERM}" report`

### L14 International and supranational
- UN tax convention process; IMF, OECD, World Bank and G20 documents; European Parliament and Commission; EU Tax Observatory; ICRICT.
- Include in an area's database only when the actor acted in or towards that area.

### L15 Polling and petitions
- Use only to find **organisations or public figures** who commissioned a poll or launched a petition. Never record private signatories.

---

## Official gazettes and plenary records (PDF)

Bill-tracker pages, press snippets and search results under-report what a legislature has on record. Colombia's Ley 2277 (2022) first read as "block votes only, no individual statements". Reading all 24 gazettes linked from the Congreso Visible bill page showed a named roll call in the Senate plenary on deleting the wealth-tax article (18 for deleting, 68 against, 66 names printed) and speeches defending the tax. Do this whenever a country's bill has a page that links its gazettes, minutes or committee reports:

1. **Download every document the bill page lists** (ponencias, committee and plenary minutes, conciliation reports, the final text). Do not stop at the summary or the timeline.
2. **Extract text once, keep the line breaks** (`scripts/gazette_scan.py DIR`). A roll call is one name per line in the raw text; collapsing whitespace destroys it.
3. **Find the wealth-tax article number in each text version.** Numbering shifts between the government bill, the ponencias and the final law. The presiding officer or the ponente usually says it aloud ("Artículo 31, impuesto al patrimonio"). Then search the vote headings for that number: `gazette_scan.py DIR --term "impuesto al patrimonio" --article 31`.
4. **Proposals to delete or amend the wealth-tax article are article-specific votes**, even when the final vote is a block of many articles. A "No" on deleting it is a vote to keep the tax (grade A, `evidence_type=vote`, quote the member's own printed entry). A "Sí" from someone already in the register is a retraction (SKILL.md 4).
5. **Block votes, whole-package votes and ponencia signatures stay out** unless the wealth tax is the only thing in the block.
6. **Speeches**: minutes mark speakers ("Palabras del honorable Senador X", "Intervención del Representante X"). Read the passages that mention the tax, quote the member's own words, skip speakers who only describe the rates or who oppose it.
7. **Record what you read.** `area_profile.md` lists the documents read (gazette numbers and dates). Never write "only block votes found" or "no individual statements" unless every minute of the relevant sittings was read; say which ones were not.
8. If the PDFs cannot be read as text (scans), say so in the profile and open them with the browser or computer use before concluding.

**Per-country records guide.** Each country gets `references/records/<folder>.md` (template: `records/_template.md`): where its bills, debates, roll calls and member lists are, how to get all of them, what was read when, and what is still open. Read it before researching a country; if it is missing, write it as the first step of the run. Track each bill, debate, vote list and report in the country's `documents.csv` (`read_status`, who read it, how, what it produced, what is left); `scripts/records_status.py` shows the state of every country.

## Local sweep pack (for sampled units, and for every unit only at Exhaustive depth)

1. `"{TERM}" "{UNIT}" council motion`
2. `"{TERM}" "{UNIT}" councillor`
3. `site:{COUNCIL_DOMAIN} "{TERM}"` (and the council's own minutes search, if it has one)
4. `"{UNIT}" council "tax the super-rich" OR "tax the rich" motion` (finds C-grade and leads to minutes)
5. `"{UNIT}" trades council OR "union branch" "{TERM}"`
6. `"{UNIT}" Green OR Labour OR Socialist (or the area's relevant parties) group "{TERM}"`
7. Local newspaper sites for the unit: `site:{LOCAL_NEWS_DOMAIN} "{TERM}"`

Record the number of queries run and hits on the unit. Failed motions still identify the proposer and seconder as supporters. Use search first; write a crawler only when a sample shows documents contain hits and about 30 or more units share one platform (SKILL.md 6.5).

---

## Search terms by language

Use all applicable terms, plus the area's own name for any specific proposal (bill names, initiative numbers, "taxe Zucman").

| Language | Terms |
|---|---|
| English | wealth tax · net wealth tax · wealth levy · billionaire tax · billionaire minimum tax · tax on extreme wealth · tax the super-rich · "1% wealth tax" / "2% wealth tax" |
| Swedish | förmögenhetsskatt · skatt på förmögenhet · miljardärsskatt |
| Norwegian | formuesskatt · formueskatt |
| Danish | formueskat · milliardærskat |
| Finnish | varallisuusvero |
| German | Vermögensteuer · Vermögenssteuer · Vermögensabgabe · Milliardärssteuer · Reichensteuer (check: often means income tax) |
| French | impôt sur la fortune · ISF · taxe Zucman · impôt plancher · taxe sur les milliardaires · impôt sur les grandes fortunes |
| Spanish | impuesto sobre el patrimonio · impuesto a las grandes fortunas · impuesto de solidaridad · impuesto a los milmillonarios |
| Catalan | impost sobre el patrimoni |
| Italian | patrimoniale · imposta patrimoniale · tassa sui miliardari (check: *patrimoniale* can mean property taxes) |
| Portuguese | imposto sobre grandes fortunas · IGF · taxação dos super-ricos · imposto sobre a riqueza |
| Dutch | vermogensbelasting · miljonairsbelasting · miljardairsbelasting (check: may refer to the savings box) |
| Polish | podatek majątkowy · podatek od bogactwa |
| Welsh | treth cyfoeth |
| Irish | cáin rachmais |

If the area uses a language not listed, build the term list in the area profile first, from the area's own news coverage of wealth taxes.
