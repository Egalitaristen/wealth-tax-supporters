# Thailand: wealth tax debate, sources and layers

Notes from seed pass (R001, October 2026), deep research (R002), comparative party/academic research (R003), consolidation pass (R004), and supporters expansion pass (R005). Check that URLs still resolve before relying on them.

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | National Assembly of Thailand (Ratthasapha / รัฐสภา): House of Representatives (Sapha Phuthaen Ratsadon / สภาผู้แทนราษฎร, 500 seats), Senate (Wuthisapha / วุฒิสภา, 200 seats), Cabinet (Khana Ratthamontri / คณะรัฐมนตรี) | Direct and indirect taxation is exclusively a national legislative power under the 2017 Constitution. Money bills require Prime Ministerial endorsement. |
| region | 76 Provinces (*changwat* / จังหวัด) + Bangkok Special Administrative Area (*Krung Thep Maha Nakhon*) = 77 administrative regions | Codes: ISO 3166-2:TH / UN OCHA P-codes (`TH10` to `TH96`), parent `G0001`. |
| local | 928 administrative districts (*amphoe* / อำเภอ; in Bangkok *khet* / เขต) | The map tier. Codes: official Royal Thai Survey Department / UN OCHA P-codes (`TH1001` to `TH9613`), parented to their respective provinces. |

**Map:** `data/th/boundaries.json` is generated from the Royal Thai Survey Department / UN OCHA Common Operational Datasets (COD-AB) for Thailand republished under **CC BY-IGO** on HDX (`cod-ab-tha`). Contains 928 administrative districts simplified (scale 100, tolerance 0.8) and merged with `merge_boundaries.py` (332 KB).

## Wealth tax debate context

Thailand has one of the highest levels of wealth concentration in Southeast Asia, with Credit Suisse Global Wealth Reports repeatedly finding that the wealthiest 1% own around 50% of national wealth. The wealth tax debate centres around financing universal cradle-to-grave welfare (รัฐสวัสดิการถ้วนหน้า) and basic pensions.

- **Primary legislative champion:** The Move Forward Party (พรรคก้าวไกล), succeeded by the People's Party (พรรคประชาชน) in August 2024 following Constitutional Court dissolution.
- **Draft Wealth Tax Act (ร่างพระราชบัญญัติภาษีความมั่งคั่ง พ.ศ. ....):** Submitted by Sirikanya Tansakun and Move Forward MPs in October 2023. Underwent formal Section 77 constitutional public consultation (Survey ID 305) from 2 October to 3 November 2023 (92.86% in favour among participants).
- **Twin Legislative Bills Distinction:**
  - **Survey ID 305 (Draft Wealth Tax Act):** Broad-based net wealth tax on total net worth exceeding 300M THB at a 0.5% ceiling rate (Included).
  - **Survey ID 310 (Draft Aggregated Land Tax Act / ร่าง พ.ร.บ. ภาษีที่ดินรวมแปลง พ.ศ. ....):** Championed by MP Woraphop Viriyaroj; real property tax on holdings $\ge 50$ rai and $> 20$ million THB to prevent land hoarding (Excluded as single-asset tax).
- **Bill design:** 
  - Net wealth tax base: total global and domestic assets minus debt liabilities as of 1 January annually.
  - Threshold: to be set by Royal Decree, with a statutory minimum of 300 million THB (Move Forward proposed 300M THB).
  - Ceiling rate: Section 18 establishes a maximum statutory rate of 0.5%.
  - Anti-avoidance: Exit tax (ภาษีขาออก) for individuals attempting to renounce Thai nationality, OECD Common Reporting Standard (CRS / MCAA) data exchange.
- **Current status:** Classified as a money bill (ร่าง พ.ร.บ. เกี่ยวด้วยการเงิน) under Section 134 of the 2017 Constitution. The Prime Minister (Pheu Thai coalition) refused certification ("นายกรัฐมนตรีไม่รับรอง"), preventing it from entering second reading. The People's Party retained the bill in its 8-bill equality package upon founding in August 2024.
- **Civil society parallel bill:** The We Fair coalition (เครือข่ายรัฐสวัสดิการเพื่อความเท่าเทียมและเป็นธรรม) led by Dr. Sustarum Thammaboosadee drafted a parallel bill proposing a 1% wealth tax on assets over 30 million THB to directly fund universal public pensions of 3,000 THB/month.
- **Comparative Party Landscape:**
  - **People's Party / Move Forward:** Sole proponent of net wealth taxation in parliament.
  - **Pheu Thai Party:** Opposed net wealth taxation; focuses on Negative Income Tax (NIT), growth stimulation, and Digital Wallet cash transfers.
  - **Democrat Party:** Low-wage income tax exemptions and pre-IPO capital gains tax; no net wealth tax.
  - **Bhumjaithai Party:** Hometown tax (ภาษีบ้านเกิดเมืองนอน) and SME relief; no net wealth tax.
  - **Conservative Parties (Palang Pracharath, United Thai Nation):** Strongly oppose net wealth taxation.

## Key terminology

- **Included terms:**
  - ภาษีความมั่งคั่ง (*phasi khwam mang khang*): Wealth tax.
  - ภาษีความมั่งคั่งสุทธิ (*phasi khwam mang khang sutthi*): Net wealth tax.
  - ภาษีคนรวย (*phasi khon ruai*): Tax on the rich (when referring to asset or net worth taxation).
  - ภาษีขาออก (*phasi kha ok*): Exit tax on wealth departure / renunciation of nationality.
- **Excluded terms (single-asset taxes or separate mechanisms):**
  - ภาษีที่ดินและสิ่งปลูกสร้าง (*phasi thi din lae sing pluk sang*): Land and Building Tax (real property only, enacted 2019).
  - ภาษีที่ดินรวมแปลง (*phasi thi din ruam plaeng*): Aggregated Land Tax across parcels (Survey ID 310).
  - ภาษีการรับมรดก (*phasi kan rap moradok*): Inheritance Tax (enacted 2015, threshold 100M THB).
  - ภาษีลาภลอย (*phasi lap loi*): Windfall profit tax (infrastructure value capture or refinery margin capture).
  - Capital Gains Tax alone (ภาษีส่วนเพิ่มของทุน), unless bundled into a net wealth tax proposal.

## What worked and what to watch

- **Parliament of Thailand Section 77 Portal (`parliament.go.th/section77`):** Authoritative repository of bills undergoing public consultation. Reports status, text PDFs, and executive summaries (Survey ID 305 for Draft Wealth Tax Act, Survey ID 310 for Draft Aggregated Land Tax Act).
- **Cloudflare blocks:** `prachatai.com` and `pridi.or.th` enforce Cloudflare Managed Challenges and block standard automated HTTP requests; desktop user agents or headless browser needed if querying them directly.
- **High-yield media:** `matichon.co.th`, `isranews.org`, `the101.world`, `thematter.co`, `plus.thairath.co.th`, `thaipublica.org`, and `ngthai.com` resolve cleanly with standard headers.
- **Think tanks:** Think Forward Center (ศูนย์นโยบายเพื่ออนาคต), Puey Ungphakorn Institute for Economic Research (PIER), and Thailand Development Research Institute (TDRI).
