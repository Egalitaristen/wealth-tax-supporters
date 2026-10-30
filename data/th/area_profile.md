# Area profile — Thailand

First written 2026-10-30 (run R001). Seed pass across all core layers (legislature, political parties, academic economists, think tanks, trade unions/civil society campaigns, economic commentators/media).

## 1. Scope
- Area: Thailand (ราชอาณาจักรไทย / Kingdom of Thailand); unitary constitutional monarchy in Southeast Asia.
- Depth: **Seed** (SKILL.md 6.1). Covers national legislative sponsors (Sapha Phuthaen Ratsadon / House of Representatives), political parties, academic economists, think tanks, civil society coalitions, and economic media.
- Levels of government in scope: National level (Ratthasapha / National Assembly, Khana Ratthamontri / Cabinet). Sub-national levels (76 provinces + Bangkok, and 928 administrative districts / amphoe) are loaded into `geo_units.csv` for geographic localization and mapping; local governments in Thailand (TAOs, PAOs, municipalities) have strictly limited revenue powers and cannot enact wealth taxes.
- Languages to search in: Thai (primary, `th`), English (`en`).
- Date of first run: 2026-10-30.

## 2. Wealth tax history and live proposals (2010 onwards)
- **Background on Thai Wealth Concentration:** Thailand consistently ranks among the most unequal economies in the world regarding wealth distribution; Credit Suisse Global Wealth Reports indicated that the wealthiest 1% owned over 50% of the total wealth in the country.
- **2012–2015 Initial Fiscal Debates:** During the Yingluck Shinawatra and early military-appointed governments, discussions focused on property taxation. In 2013, Dr. Pisit Puapan of the Fiscal Policy Office (Ministry of Finance) publicly advocated shifting towards a wealth tax base (ฐานภาษีความมั่งคั่ง) to tackle structural inequality. In 2015, the National Legislative Assembly passed the Inheritance Tax Act (พ.ร.บ. ภาษีการรับมรดก พ.ศ. 2558), but set a high threshold (100 million THB) with low rates (5–10%), generating negligible revenue.
- **2019–2023 Move Forward Progressive Welfare Platform:** The Move Forward Party (พรรคก้าวไกล) incorporated a dedicated annual net wealth tax into its flagship "Progressive Thai Welfare" (สวัสดิการไทยก้าวหน้า) agenda. Led by economic spokesperson Sirikanya Tansakun and Think Forward Center Director Dr. Decharut Sukkumnoed, the proposal called for a 0.5% annual levy on net assets above 300 million THB, paired with an exit tax (ภาษีขาออก) and aggregate land taxation.
- **October 2023 Draft Wealth Tax Act (ร่าง พ.ร.บ. ภาษีความมั่งคั่ง พ.ศ. ....):** Sirikanya Tansakun and Move Forward MPs formally submitted the bill to the House of Representatives. Under Section 77 of the Constitution, it underwent public consultation via Secretariat of the House of Representatives Survey ID 305 between 2 October and 3 November 2023 (92.86% in favor). However, Prime Minister Srettha Thavisin classified it as a money bill and refused certification ("นายกรัฐมนตรีไม่รับรอง"), stalling it before formal debate.
- **August 2024 Reconstitution as People's Party:** Following the Constitutional Court dissolution of Move Forward Party in August 2024, the reconstituted People's Party (พรรคประชาชน) retained all 143 MPs and reaffirmed the Draft Wealth Tax Act as part of its 8-bill equality legislative package.
- **Civil Society Parallel Campaign:** The We Fair coalition (เครือข่ายรัฐสวัสดิการเพื่อความเท่าเทียมและเป็นธรรม), coordinated academically by Assoc. Prof. Dr. Sustarum Thammaboosadee, drafted a parallel civil society wealth tax bill targeting fortunes over 30 million THB at a 1% rate to directly finance universal old-age pensions (3,000 THB/month).

## 3. Legislatures and where their records are
- **Sapha Phuthaen Ratsadon (สภาผู้แทนราษฎร / House of Representatives):** Lower chamber, 500 members (400 constituency, 100 party list).
  - Portal: `https://www.parliament.go.th`
  - Section 77 Public Consultation Portal: `https://www.parliament.go.th/section77/` (Searchable by bill name and survey ID; Survey ID 305 contains the Draft Wealth Tax Act).
  - Hansard & Session Records: `https://www.parliament.go.th/ewtadmin/ewt/parliament_parcy/ewt_news.php?nid=79998`
- **Wuthisapha (วุฒิสภา / Senate):** Upper chamber, 200 members chosen from 20 professional groups under the 2024 selection system.
  - Portal: `https://www.senate.go.th`

## 4. Parties
- **People's Party (พรรคประชาชน):** 143 seats in the House. Reconstituted from Move Forward in August 2024. Main proponent of net wealth taxation in Thailand.
- **Move Forward Party (พรรคก้าวไกล, 2020–2024):** Won the May 2023 general election with 151 seats. Dissolved August 2024. Submitted Draft Wealth Tax Act.
- **Pheu Thai Party (พรรคเพื่อไทย):** 141 seats. Government coalition leader. Has favored consumption-stimulating policies (e.g., Digital Wallet) rather than structural net wealth taxes; government leadership withheld money-bill endorsement.
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
- **Mainstream Newspapers:** *Matichon* (`matichon.co.th`), *Krungthep Turakij* (business daily), *Bangkok Post*.

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

## 10. Plan for the next runs
- **Immediate Follow-ups (Run R002):**
  1. Expand co-sponsors on the Draft Wealth Tax Act: Examine the remaining Move Forward MPs who co-signed Sirikanya Tansakun's bill text in House Survey ID 305.
  2. Map member organisations of the We Fair network (labour unions, slum networks, rural federations) that formally endorsed the civil society wealth tax bill.
  3. Review academic publications from Chulalongkorn University and Thammasat University Faculty of Economics on capital gains and net wealth taxation.
  4. Monitor Senate Standing Committee on Finance and Economic Affairs for any inquiries into wealth base expansion.
