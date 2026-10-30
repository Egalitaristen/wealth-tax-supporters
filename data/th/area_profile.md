# Area profile — Thailand

First written 2026-10-30 (run R001). Updated 2026-10-30 (run R002) with deep research into macroeconomic institutes, civil service feasibility studies, labor coalitions, and formal exclusions.

## 1. Scope
- Area: Thailand (ราชอาณาจักรไทย / Kingdom of Thailand); unitary constitutional monarchy in Southeast Asia.
- Depth: **Deep / Expanded** (SKILL.md 6.1). Covers national legislative sponsors (Sapha Phuthaen Ratsadon / House of Representatives), political parties, academic economists, think tanks, civil society coalitions, economic media, and formal exclusions.
- Levels of government in scope: National level (Ratthasapha / National Assembly, Khana Ratthamontri / Cabinet). Sub-national levels (76 provinces + Bangkok, and 928 administrative districts / amphoe) are loaded into `geo_units.csv` for geographic localization and mapping; local governments in Thailand (TAOs, PAOs, municipalities) have strictly limited revenue powers and cannot enact wealth taxes.
- Languages to search in: Thai (primary, `th`), English (`en`).
- Date of first run: 2026-10-30 (R001); expansion pass: 2026-10-30 (R002).

## 2. Wealth tax history and live proposals (2010 onwards)
- **Background on Thai Wealth Concentration:** Thailand consistently ranks among the most unequal economies in the world regarding wealth distribution; Credit Suisse Global Wealth Reports indicated that the wealthiest 1% owned over 50% of the total wealth in the country.
- **2012–2015 Initial Fiscal Debates:** During the Yingluck Shinawatra and early military-appointed governments, discussions focused on property taxation. In 2012–2013, Dr. Pan Ananapibut and Dr. Pisit Puapan of the Fiscal Policy Office (Ministry of Finance) publicly examined wealth tax bases (ฐานภาษีความมั่งคั่ง). In 2015, the National Legislative Assembly passed the Inheritance Tax Act (พ.ร.บ. ภาษีการรับมรดก พ.ศ. 2558), but set a high threshold (100 million THB) with low rates (5–10%), generating negligible revenue (under 500M THB/year against an initial 4B THB target).
- **2019–2023 Move Forward Progressive Welfare Platform:** The Move Forward Party (พรรคก้าวไกล) incorporated a dedicated annual net wealth tax into its flagship "Progressive Thai Welfare" (สวัสดิการไทยก้าวหน้า) agenda. Led by economic spokesperson Sirikanya Tansakun and Think Forward Center Director Dr. Decharut Sukkumnoed, the proposal called for a 0.5% annual levy on net assets above 300 million THB, paired with an exit tax (ภาษีขาออก) and aggregate land taxation.
- **October 2023 Draft Wealth Tax Act (ร่าง พ.ร.บ. ภาษีความมั่งคั่ง พ.ศ. ....):** Sirikanya Tansakun and Move Forward MPs formally submitted the bill to the House of Representatives. Under Section 77 of the Constitution, it underwent public consultation via Secretariat of the House of Representatives Survey ID 305 between 2 October and 3 November 2023 (92.86% in favor). However, Prime Minister Srettha Thavisin classified it as a money bill and refused certification ("นายกรัฐมนตรีไม่รับรอง"), stalling it before formal debate.
- **August 2024 Reconstitution as People's Party:** Following the Constitutional Court dissolution of Move Forward Party in August 2024, the reconstituted People's Party (พรรคประชาชน) retained all 143 MPs and reaffirmed the Draft Wealth Tax Act as part of its 8-bill equality legislative package.
- **Civil Society Parallel Campaign:** The We Fair coalition (เครือข่ายรัฐสวัสดิการเพื่อความเท่าเทียมและเป็นธรรม), coordinated academically by Assoc. Prof. Dr. Sustarum Thammaboosadee, drafted a parallel civil society wealth tax bill targeting fortunes over 30 million THB at a 1% rate to directly finance universal old-age pensions (3,000 THB/month).
- **Ministry of Finance Administrative Study:** In 2024, Permanent Secretary of the Ministry of Finance Lavaron Sangsnit acknowledged that inheritance tax has largely failed due to unpredictability and deferrals ("ภาษีจะเกิดขึ้นก็ต่อเมื่อเจ้าของทรัพย์สินเสียชีวิตเท่านั้น"), noting that an annual net wealth tax (Wealth Tax) on asset values represents an active administrative alternative under international OECD automatic data-exchange networks.

## 3. Legislatures and where their records are
- **Sapha Phuthaen Ratsadon (สภาผู้แทนราษฎร / House of Representatives):** Lower chamber, 500 members (400 constituency, 100 party list).
  - Portal: `https://www.parliament.go.th`
  - Section 77 Public Consultation Portal: `https://www.parliament.go.th/section77/` (Searchable by bill name and survey ID; Survey ID 305 contains the Draft Wealth Tax Act).
  - Consultation Outcome Report: `manage/files/file_20240220142504_2_305.pdf`.
- **Wuthisapha (วุฒิสภา / Senate):** Upper chamber, 200 members chosen from 20 professional groups under the 2024 selection system.
  - Portal: `https://www.senate.go.th`

## 4. Parties
- **People's Party (พรรคประชาชน):** 143 seats in the House. Reconstituted from Move Forward in August 2024. Main proponent of net wealth taxation in Thailand.
- **Move Forward Party (พรรคก้าวไกล, 2020–2024):** Won the May 2023 general election with 151 seats. Dissolved August 2024. Submitted Draft Wealth Tax Act.
- **Pheu Thai Party (พรรคเพื่อไทย):** 141 seats. Government coalition leader. Favors consumption stimulation and Negative Income Tax (NIT); explicitly declined wealth tax proposals, citing fears of capital flight.
- **Bhumjaithai Party (พรรคภูมิใจไทย):** 71 seats. Coalition partner. Emphasizes decentralization and business deregulation; neutral to skeptical on asset taxation.
- **Conservative & Military-aligned Parties (Palang Pracharath, United Thai Nation):** Strongly oppose net wealth taxes, defending capital accumulation and foreign investment competitiveness.
- **Fair Party (พรรคเป็นธรรม):** Progressive minor party aligned with People's Party on human rights and social justice.

## 5. Government below national level
- **Structure:** Unitary structure divided into 76 Provinces (*changwat*) and Bangkok Special Administrative Area, subdivided into 928 Districts (*amphoe* / *khet*).
- **Taxation powers:** Local authorities (PAOs, municipalities, TAOs, BMA, Pattaya City) can collect local property taxes (Land and Building Tax, Signboard Tax, Local Development Tax) and receive surcharges on VAT and excise taxes. They possess no statutory jurisdiction to levy taxes on net personal or corporate wealth.
- **Official geographic source:** UN OCHA Common Operational Datasets (COD-AB) for Thailand on HDX (`cod-ab-tha`), CC BY-IGO, derived from the Royal Thai Survey Department. 928 districts form the interactive map boundary.
- **Local decision:** Skip local council sweeps. Local governments lack the legal power to tax wealth, and national policy debate is strictly concentrated in Bangkok / Ratthasapha.

## 6. Search terms
- **Primary Thai Terms (Included):**
  - `"ภาษีความมั่งคั่ง"` (*phasi khwam mang khang*): Wealth tax.
  - `"ภาษีความมั่งคั่งสุทธิ"` (*phasi khwam mang khang sutthi*): Net wealth tax.
  - `"ร่างพระราชบัญญัติภาษีความมั่งคั่ง"`: Draft Wealth Tax Act.
  - `"ภาษีคนรวย"` (*phasi khon ruai*): Tax on the rich (when referring to net worth or wealth).
  - `"ภาษีขาออก"`: Exit tax.
- **Ambiguous & Excluded Terms (Single-Asset Taxes):**
  - `"ภาษีที่ดินและสิ่งปลูกสร้าง"`: Land and Building Tax (real property tax only, enacted 2019).
  - `"ภาษีการรับมรดก"`: Inheritance Tax (transfer on death, enacted 2015).
  - `"ภาษีลาภลอย"`: Windfall tax.
  - `"ภาษีกำไรจากการขายหุ้น"`: Capital Gains Tax on stock transactions alone.

## 7. Media
- **Progressive / In-depth Analytical Outlets:**
  - *The 101 World* (`the101.world`): Regular long-form policy forums and economic analysis covering tax reform and welfare.
  - *Thai PBS Decode* (`thaipbs.or.th/decode`): Public broadcast analytical unit focusing on inequality, labour, and structural reform.
  - *The Matter* (`thematter.co`): Progressive youth and economic commentary, published influential op-eds on billionaire wealth taxes.
  - *Thairath Plus* (`plus.thairath.co.th`): Digital analysis desk of Thairath Media Group, editorializing in favor of wealth redistribution.
  - *ThaiPublica* (`thaipublica.org`): Investigative public policy journalism covering Ministry of Finance fiscal forums and tax policy.
  - *Prachatai* (`prachatai.com`): Independent civil society media outlet (requires desktop headers due to Cloudflare protection).
  - *Isranews Agency* (`isranews.org`): Investigative agency reporting on state budgets, university studies, and pension proposals.
- **Mainstream Newspapers:** *Matichon* (`matichon.co.th`), *Krungthep Turakij* (business daily, `bangkokbiznews.com`), *Bangkok Post*.

## 8. Registers
- **Royal Gazette (ราชกิจจานุเบกษา):** `http://www.ratchakitcha.soc.go.th` (Official publication of enacted statutes, royal decrees, and ministerial regulations).
- **Parliament Section 77 Portal:** `https://www.parliament.go.th/section77/` (Public consultations on all draft bills).
- **Department of Business Development (DBD):** `https://datawarehouse.dbd.go.th` (Corporate registry).
- **National Anti-Corruption Commission (NACC / ป.ป.ช.):** `https://www.nacc.go.th` (Mandatory asset and liability disclosures of MPs and ministers).

## 9. Known networks
- **We Fair (เครือข่ายรัฐสวัสดิการเพื่อความเท่าเทียมและเป็นธรรม):** Welfare state coalition uniting 12+ civil society, labour, and student organisations campaigning for tax-funded social security.
- **Think Forward Center (ศูนย์นโยบายเพื่ออนาคต):** Policy think tank aligned with Move Forward / People's Party, headed by Dr. Decharut Sukkumnoed.
- **Puey Ungphakorn Institute for Economic Research (PIER):** Bank of Thailand-affiliated research institute studying wealth inequality and micro-data.
- **Thai Social Security Watch / Social Security Progressive Movement:** Trade union coalition focusing on pension reform and SSO board governance.

## 10. Documented Exclusions
1. **Dr. Pan Ananapibut** (`X0001`, `out_of_definition`): 2012 presentation titled "ภาษีความมั่งคั่ง" actually proposed a Korean-style property/land and building tax on housing above 5 million THB rather than a net wealth tax on total assets minus debt.
2. **Sommai Phasee** (`X0002`, `out_of_definition`): Finance Minister (2014–2015) who enacted the 2015 Inheritance Tax Act and Land and Building Tax Act; while frequently referred to in media as taxing the wealthy, these are inheritance and real property taxes excluded under Section 2.
3. **Nitirat Sapsomboon** (`X0003`, `out_of_definition`): Coordinator of We Fair Network. In his widely cited 2020 iLaw interview outlining tax funding mechanisms for universal welfare, he proposed capital gains tax (30%), progressive land and building tax, progressive inheritance tax, and cutting BOI privileges, but omitted an annual net wealth tax.
4. **Dr. Somchai Jitsuchon** (`X0004`, `out_of_definition`): Research Director for Inclusive Development at TDRI. While a leading academic voice on inequality and tax reform to finance pensions and child grants, his concrete proposals focus on land and building taxes, windfall taxes, capital gains taxes, and phased VAT increases, rather than an annual net wealth tax.
5. **Lavaron Sangsnit** (`X0005`, `not_advocating`): Permanent Secretary of the Ministry of Finance. Frequently cited in economic media discussing the structural flaws of the inheritance tax and noting that a net wealth tax (Wealth Tax) could be a future policy alternative; his comments represent administrative feasibility review and technical study rather than personal or institutional advocacy.
6. **Pita Limjaroenrat** (`X0006`, `not_advocating`): Former Move Forward Party leader. While campaigning on the party's 2023 Progressive Welfare platform, his public statements focused broadly on welfare spending and economic revitalization; specific legislative drafting and direct defense of the net wealth tax was spearheaded by Sirikanya Tansakun and Think Forward Center, with no distinct standalone net wealth tax quote in his personal capacity.

## 11. Plan for future runs
1. **Parliamentary Progress Tracking:** Monitor parliamentary status of the Draft Wealth Tax Act should the House of Representatives resume consideration or if People's Party reintroduces an updated version in the 2026/2027 legislative sessions.
2. **Civil Service Policy Papers:** Track Fiscal Policy Office (FPO) publications regarding wealth base taxation studies, particularly in relation to OECD Pillar 2 and international automated financial account information exchange (CRS/MCAA).
3. **Senate Committee Monitoring:** Track hearings in the Senate Standing Committee on Finance and Economic Affairs for any formal evaluations of progressive asset or wealth taxation.
