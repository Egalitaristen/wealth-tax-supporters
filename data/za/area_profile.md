# South Africa: area profile

## 1. Scope
- Area: South Africa; country. Depth: seed (national; provinces and municipalities loaded, not swept). Languages: English (the press, Parliament and party statements); isiZulu, Afrikaans and others not searched.
- Started 2026-10-26 (R001) from the African Union run: a Pan-African Parliament delegate (Vuyani Pambo, EFF) and a lead on the EFF pointed here (data/au).

## 2. Wealth tax history and live proposals
- South Africa has estate duty, donations tax, transfer duty, securities transfer tax and capital gains tax, but no annual net wealth tax. The Davis Tax Committee (2014 to 2018) advised against one; SAFTU criticised its shelving ([saftu.org.za/archives/4188] [verify]).
- The ANC adopted "an appropriately structured wealth tax, possibly linked to a land tax" at its 2017 national conference and revived it for a basic income grant at its July 2022 policy conference (Sunday Times, 2022-07-31).
- February to May 2025: the budget speech was postponed over a proposed VAT rise (15% to 17%, later 0.5 points, then reversed). The EFF, SACP, MK Party, COSATU, SAFTU, Black Sash and others called for a wealth tax instead; the Parliamentary Budget Office's second pre-budget brief (12 March 2025) priced a 0.5% wealth tax on the top two quantiles' net wealth as comparable to the VAT rise.
- Government position: Finance Minister Godongwana's written replies (May to June 2025, July 2026) reject a wealth tax: income tax is "the most effective way to tax the wealthy"; capital flight risk (PMG NW3273, IOL 2026-07-07 [verify]). National Treasury says it is studying declared-wealth data (EWN/Business Day, 2025 [verify]).
- November 2025: Patriotic Millionaires and Oxfam SA published a survey of 543 dollar millionaires, 64% of whom said they would pay a 2% wealth tax (Daily Maverick, 2025-11-11). South Africa held the G20 presidency in 2025.

## 3. Legislature and where its records are
- National Assembly and NCOP: written questions and replies are on pmg.org.za (committee-question pages) and parliament.gov.za; Hansard on pmg.org.za. EFF MPs Omphile Maotwe (NW3273, NW4844) and Carl Niehaus ask the Minister about a wealth tax. The Parliamentary Budget Office briefs are at archive.parliament.gov.za.
- Seats: `python skill/scripts/seats.py data/za` reads the Parliamentary Monitoring Group's member API (api.pmg.org.za/member/; 399 current National Assembly members, one seat vacant on 2026-10-26) and lights the seats of Malema, Maotwe, Thambo, Letlape (EFF) and Kubayi (ANC). The Pan-African Parliament delegation is on pap.au.int/mps/south-africa; Vuyani Pambo (EFF) is on it.
- Hansards: pmg.org.za/hansard/<id>/ pages carry the full debate; `pmg.org.za/search/?q=...` finds them (27 hits for "Pambo wealth tax"). A scan of the 21 linked Hansards found no speech of Pambo's mentioning a wealth tax; it did find EFF MP Molebogeng Letlape's member statement of 6 May 2025 (E00028).

## 4. Parties
- EFF (wealth tax and an "apartheid tax" on pre-1994 trusts, 2025 counter-budget); SACP (0.5% wealth tax on the richest 20%); MK Party; GOOD; ANC (2017 conference policy, 2022 revival). Not searched: ActionSA, Patriotic Alliance, Al Jama-ah, Cope, ATM, UDM.

## 5. Government below national level
- 9 provinces, 44 district municipalities, 8 metropolitan municipalities and 205 local municipalities, loaded in geo_units.csv; none swept. Municipal bodies cannot levy a wealth tax; support at this level would be motions or mayors' statements.

## 6. Sources that block scripts
- iol.co.za (some pages), businesstech.co.za, dailyinvestor.com and cliffedekkerhofmeyr.com answer 403. forgood.org.za serves scripts a different page: its two quotes (E00019, E00020) were read in a browser and `checkquotes` reports them as not found. PMG, Parliament's archive, SAFTU, Daily News, The Post and Business Report read fine.

## 7. Runs
R003 (2026-10-26): Hansard, written-question and committee-minutes sweep. PMG's search (api-less, `pmg.org.za/search/?q=...&filter[type]=hansard|minister_question|committee_meeting`, one request per year because paging does not work) was run for "wealth tax", "wealth taxes", "tax the rich", "apartheid tax", "tax on wealth", "wealth taxation", "redress tax" and "tax the super-rich": 148 documents (62 Hansard, 8 written questions, about 80 committee meetings), 284 phrase hits. Each hit was read with its speaker. Added 22 actors (18 people: MPs of the EFF, MK Party, UDM, ACDP and ANC, and Tlou Seopa; 4 organisations: UDM, Amandla.mobi, Women on Farms Project, Budget Justice Coalition) and 31 evidence rows (including extra rows for Maotwe, the MK Party and COSATU). Not added: land or municipal property taxes (Dlamini, Siwisa on luxury land), generic "tax the rich" (Litchfield-Tshabalala, a Pan-African Parliament member), government answers, and speakers whose party PMG does not give for past members (Jafta, Ntshayisa, Qayiso, Abraham, Molefe).
R002 (2026-10-26): National Assembly seats adapter and positions (5 supporters sit); Hansard scan for Vuyani Pambo found nothing of his own; added Molebogeng Letlape.

R001 (2026-10-26)
22 supporters, 27 evidence rows (7 grade A, 15 B). Parties: EFF, SACP, MK Party, ANC, GOOD. People: Malema, Maotwe, Thambo (EFF); Mashilo, Mapaila (SACP); Kubayi (ANC); Herron (GOOD). Unions: COSATU, SAFTU (Vavi, Parks). Institutions: the Parliamentary Budget Office. Think tank and economist: the Institute for Economic Justice and Gilad Isaacs. NGOs: Black Sash, Greenpeace Africa. Campaigner Michael Marchant (op-ed). Two exclusions: Godongwana and National Treasury (opposed).

## 8. Plan (updated after R003)
0. Done in R003: the PMG sweep. Left from it: speakers with no party in PMG's member list (Jafta 2017, Ntshayisa 2019, Qayiso 2022, P N Abraham 2020, Molefe NW6947 Dec 2025, Mahlatsi 2025) and committee-minute speakers whose name the summary omits (35045 Dr Mohamed 2022, 39826, 34424); read each Hansard's attendance list for the party.
1. Hansard sweep (R002 started it): run `pmg.org.za/search/` for "wealth tax", "apartheid tax" and "tax the rich" and read each speaker's own lines (the member-statement and budget-vote debates of Feb to May 2025 are the richest); every EFF, MK Party and SACP-aligned MP who says it is a B or better. Carl Niehaus (EFF MP) asked a question mentioned in the press; find his own line. Pambo: nothing of his own found.
2. Parliament: search PMG for every written question and debate on a wealth tax since 2019 (EFF, MK Party and ActionSA MPs); the Davis Tax Committee; Budget Justice Coalition and Oxfam South Africa (Tlou Seopa's Amandla.mobi quote is borderline, see Business Report 2025-12-03).
3. Other parties' 2024 manifestos; academics (UCT, Wits, Stellenbosch economists), SA Revenue Service and Treasury economists; journalists (Daily Maverick, Business Day columnists); faith groups (SACC); wealthy supporters (Patriotic Millionaires SA).
4. Provinces: sample Gauteng, Western Cape, KwaZulu-Natal and the metros; unlikely to yield beyond the ANC, EFF and MK Party caucuses.
