# Vietnam: wealth tax debate, sources and layers

Notes from seed pass (R001, November 2026). Check that URLs still resolve before relying on them.

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | Quốc hội Việt Nam (500 seats), Chính phủ Việt Nam | Direct and indirect taxation is exclusively a national legislative power under the 2013 Constitution and State Budget Law. |
| region | 63 provincial units: 58 provinces (*tỉnh*) + 5 centrally-governed cities (*thành phố trực thuộc trung ương*: Hà Nội, TP. Hồ Chí Minh, Hải Phòng, Đà Nẵng, Cần Thơ) | Official 2-digit GSO codes (`01` to `96`), parent `G0001`. Provinces have no independent tax-raising authority. |
| council | 705 district-level administrative units (*quận*, *huyện*, *thị xã*, *thành phố thuộc tỉnh*) | The local tier. Official 3-digit GSO codes (`001` to `973`), parented to their respective provinces. |

**Map:** No open-licence local boundary file with official GSO codes is currently available. While UN OCHA HDX publishes `cod-ab-vnm` (provinces, CC BY-IGO) and geoBoundaries publishes an ADM2 layer under CC BY-IGO, geoBoundaries ADM2 lacks official GSO codes (using synthetic IDs and unaccented names) and has slight vintage discrepancies with the official 705 GSO districts. Per SKILL.md 5 and 6.7, shipping without an unlicensed/uncoded map is preferred; a follow-up issue is opened for `boundaries.json`.

## Wealth tax debate context

Vietnam has experienced rapid economic expansion and wealth creation over the last two decades, resulting in high concentrations of private assets, particularly in urban real estate.

- **Absence of net wealth tax:** Vietnam currently has no annual tax on net wealth (*thuế tài sản ròng*) or minimum billionaire tax (*thuế tỷ phú*). The tax system relies on VAT, corporate income tax, personal income tax, and specific land-use fees.
- **The 2018 Draft Law on Property Tax (*Dự án Luật Thuế tài sản*):**
  - Formulated by the Ministry of Finance (*Bộ Tài chính*) in April 2018.
  - Proposed an annual tax of 0.3%–0.4% on housing with an assessed construction value over 700 million or 1 billion VND, non-agricultural land, cars over 1.5 billion VND, aircraft, and yachts.
  - Faced fierce public and expert backlash regarding the low threshold, lack of market valuation data, and concerns over double taxation on middle-income households.
  - The government subsequently shelved the proposal; it was never introduced to the National Assembly plenary.
  - *Status in register:* Excluded under Section 2 as a gross property/single-asset tax reform (`out_of_definition`).
- **Second-home and land speculation debates:**
  - Party Central Committee Resolution 18-NQ/TW (2022) directed the formulation of higher tax rates for individuals possessing multiple houses or leaving land idle (*thuế nhà đất thứ hai*, *thuế đất bỏ hoang*).
  - Prominent economists and former officials (e.g. GS. Đặng Hùng Võ, TS. Vũ Đình Ánh, TS. Đinh Trọng Thịnh) regularly advocate for property tax reform to curb real estate speculation. These proposals are excluded under Section 2 as single-asset property taxes.
- **Civil society advocacy:**
  - **Oxfam tại Việt Nam (Oxfam in Vietnam):** The leading active domestic advocate for net wealth taxation. Publishes national Vietnamese translations of global inequality reports (*Survival of the Richest*, 2023; *Takers Not Makers*, 2025) explicitly calling for up to 5% progressive annual net wealth taxes on multi-millionaires and billionaires to address extreme wealth concentration and finance public services.
  - **Liên minh Công bằng Thuế Việt Nam (VATJ):** A coalition of CSOs and economic research bodies (including VEPR) working on corporate tax incentives, tax transparency, and fiscal fairness, without an explicit wealth tax platform to date.

## Key terminology

- **Included terms:**
  - `thuế tài sản ròng`: Net wealth tax.
  - `thuế người siêu giàu` / `thuế giới siêu giàu`: Tax on the super-rich.
  - `thuế tỷ phú` / `thuế tỉ phú`: Billionaire tax.
  - `thuế tài sản`: Property/wealth tax (verify that the tax base covers broad net assets rather than real estate alone).
- **Excluded terms (single-asset taxes or separate tax categories):**
  - `thuế bất động sản`: Real estate tax.
  - `thuế nhà đất`: Housing and land tax.
  - `thuế sử dụng đất phi nông nghiệp`: Non-agricultural land use tax.
  - `thuế thừa kế`: Inheritance tax.
  - `thuế thu nhập cá nhân`: Personal income tax.
  - `thuế tiêu thụ đặc biệt`: Special consumption tax (luxury excise).

## What worked and what to watch

- **Legislative records:** The National Assembly portal (`quochoi.vn`) and its digital library (`thuvienso.quochoi.vn`) provide legislative texts and session agendas. Roll-call votes on wealth tax bills do not exist in Vietnam.
- **Sub-national taxing constraints:** Local People's Councils (*Hội đồng nhân dân*) at provincial and district levels cannot enact local taxes. Sweeping local councils individually is unproductive; advocacy is strictly focused at the national level.
- **Official GSO administrative units:** General Statistics Office of Vietnam (GSO) maintains standard codes for 63 provinces (2-digit, `01` to `96`) and 705 district-level units (3-digit, `001` to `973`). Sibling name collisions (e.g. Huyện Kỳ Anh vs. Thị xã Kỳ Anh in Hà Tĩnh) are disambiguated using official administrative prefixes (`name_with_type`).
