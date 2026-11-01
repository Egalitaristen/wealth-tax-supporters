# Saudi Arabia (data/sa)

Worked notes from the Saudi Arabia research passes (`R001` seed pass, `R002` deepening pass, `R003` saturation pass, `R004` exhaustive leads pass, `R005` extended perimeter sweep, 2026-10-31 to 2026-11-01; 1 identified supporter, 22 documented exclusions, 1 opinion poll, 33 logged bilingual queries, 6 tracked leads, 147 governorates loaded).

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | Majlis al-Shura (`G0002`), Council of Ministers | 150 appointed members of the Consultative Assembly (no partisan elections). Fiscal powers strictly centralized. |
| region | 13 Administrative Regions (`G0003`–`G0015`) | Mintaqah administrative regions established under the Regional Law (Royal Decree A/92 of 1992). |
| council | 147 Governorates (`G0016`–`G0162`) | Muhafazat administrative tier. All fiscal powers belong to central government. |

**Map:** `data/sa/boundaries.json` uses open-licence administrative boundaries for Saudi Arabia sourced from geoBoundaries gbOpen:
- Admin 1: `geoBoundaries-SAU-ADM1.geojson` (13 regions; Open Data Commons Open Database License `ODbL-1.0`, `https://opendatacommons.org/licenses/odbl/1-0/`, ISO 3166-2:SA codes `SA-01` to `SA-14`).
- Admin 2: `geoBoundaries-SAU-ADM2.geojson` (147 governorates; `ODbL-1.0` / CC BY-SA 2.0, matched by `shapeID`).
- Boundaries were generated using `topo_to_boundaries.py --project lonlat --scale 100 --simplify 0.4` and merged with `merge_boundaries.py`.

## Identified supporters

1. **A0001: Khalid Abdulla-Janahi** (`business_leader`, `journalist`; Group CEO of DMI Trust, Columnist at *Arab News*).
   - **Grade A** (`op_ed`, 2017-04-25 in *Arab News*): *"Why a wealth tax"*.
     - Verbatim quote: `We should seriously consider introducing a wealth tax for all eligible individuals, whether citizens or residents. This is entirely different from Zakat; we must never confuse the two.`
     - Proposes an annual 1% net wealth tax on individuals holding assets of $5 million or more (`1% on net worth >$5m`) across GCC economies, explicitly separating statutory wealth taxation from religious Zakat obligations to fund quality education and budget stability.
   - **Grade A** (`speech`, 2017-04-11): Top CEO Conference in King Abdullah Economic City (Makkah Region).
     - Verbatim quote: `He proposes an annual 1 percent “wealth tax” on people with $5 million or more in assets — something that would allow governments to funnel more money into education.`
     - Sourced to *Arab News* reporting on the summit proceedings.

2. **A0002: Omar Al-Ubaydli** (`economist`, `journalist`; Bahrain-based economist and columnist).
   - **Grade A** (`op_ed`, 2021-05-02, *Al Arabiya English*): *"Wealth tax: An Islam-friendly way to combat inequality"*.
     - Verbatim quote: `The Saudi tax system’s nascence allows room for experimentation. One trial that merits consideration is a wealth tax: it would combat inequality in an Islam-friendly manner`
     - Recommends a wealth tax for Saudi Arabia, noting that zakat loosely equals a 2.5% wealth tax and that Piketty's figure is about 2%. No rate or threshold is proposed, so the design is `wealth_tax_unspecified`. He is Bahraini, like Janahi, and is in this register because the piece is addressed to Saudi policy.
   - Left out: Saleh Kamel (CNN Arabic, December 2016) said Gulf taxes were late and zakat is a kind of tax, with no wealth tax named (`X0023`).

## Public opinion polls

- **Ipsos / Earth4All G20 Survey (June 2024):**
  - Published 2024-06-24 by Earth4All and the Global Commons Alliance (`https://earth4all.life/global-survey-2024/`).
  - Fieldwork: 2024-03-05 to 2024-04-08; representative sample of 1,000 adults aged 18-75 in Saudi Arabia.
  - Question: *"A wealth tax on wealthy individuals to fund major changes to our economy and lifestyles"* (*فرض ضريبة ثروة على الأفراد الأثرياء لتمويل تغييرات رئيسية في اقتصادنا وأنماط حياتنا*).
  - Result: **54% support** (lowest among surveyed G20 countries alongside Argentina, but still representing a clear majority).

## Excluded taxes and near-misses

1. **Zakat (زكاة):** Administered by ZATCA at 2.5% on commercial assets/capital of Saudi and GCC companies and nationals. Excluded under Section 2 as a religious Sharia institution rather than secular wealth taxation.
2. **White Land Tax (رسوم الأراضي البيضاء):** 2.5% fee on vacant urban land plots under the Ministry of Housing. Excluded under Section 2 as a property/land tax.
3. **The Giving Pledge (Prince Alwaleed bin Talal):** Pledged $32 billion fortune to charity in 2015-2016. Excluded under Section 4 as private philanthropy.
4. **G20 Rio Ministerial Declaration (July 2024):** Agreed by consensus on effective taxation of ultra-high-net-worth individuals, without endorsing a net wealth tax.
5. **Mohammed bin Salman Al Saud (2021 Vision 2030 interview):** Explicitly stated there will be no personal income tax in Saudi Arabia.
6. **Dr. Ihsan Bu-Hulaiga:** Published comparative analysis of California billionaire tax and European wealth taxes, discussing capital flight risks without endorsing a wealth tax.
7. **Dr. Fahad bin Juma'a:** Former Shura Council member and economist who campaigned against the shadow economy, tax and zakat evasion, and advocated electronic payment systems and VAT/excise compliance.
8. **Dr. Said Al-Shaikh:** Former chief economist of NCB and former Shura Council Finance Committee member who advocated White Land fees on vacant urban plots to stimulate real estate development; excluded land tax under Section 2.
9. **Dr. Hamza Al-Salim:** Academic economist who authored comparative studies on Zakat and public taxation and argued in *Al-Jazirah* for progressive income taxation alongside VAT to pay for public services; income tax excluded under Section 2.
10. **Dr. Abdullah Al-Maghlouth:** Member of the Saudi Economic Association and real estate economist who focused on implementing the White Land Tax to reduce urban land speculation; excluded land tax under Section 2.
11. **Barjas Al-Barjas:** Prominent economic analyst who examined VAT, real estate transaction tax, and Zakat contributions to national social welfare, with no proposals for personal wealth taxation.
12. **Dr. Nourah Al-Yousef:** Chair of the Saudi Economic Association and former Shura Council member who focused on energy economics and sovereign non-oil revenue diversification without advocating a net wealth tax.
13. **National Committee of Workers Committees (NCWC):** Saudi national labor representative federation participating in G20 L20 on wages, labor standards, and cost-of-living impacts of VAT, with no proposals for wealth taxation.
14. **Essam Al-Zamil:** Economic analyst who criticized the expansion of VAT and expat levies on middle-class purchasing power, while supporting White Land fees to fight real estate speculation; no wealth tax advocacy.
15. **Dr. Salem Baajajah:** Professor of accounting and co-author of standard university textbook on Saudi Zakat and tax collection systems, focusing on technical ZATCA regulations, withholding taxes, and VAT compliance without proposing a net wealth tax.
16. **Talat Hafez:** Banking expert and former secretary general of the Media and Banking Awareness Committee for Saudi banks who clarified that VAT applies strictly to explicit service fees and not to loans, salaries, or cash withdrawals.
17. **Frank Kane:** Senior business columnist at *Arab News* who moderated the 2017 KAEC Top CEO panel where Janahi proposed a 1% wealth tax and reported on it, but did not personally sponsor or endorse a wealth tax proposal.
18. **Khalid Abu-Ismail & Vladimir Hlasny:** Economists at UN ESCWA in Beirut who authored the 2020 regional technical paper *Wealth Inequality and Closing the Poverty Gap in Arab Countries: The Case for a Solidarity Wealth Tax*, modeling regional redistribution across 14 Arab countries without domestic Saudi policy advocacy (cataloged in global resources).
19. **Mohammed Al-Jadaan:** Saudi Minister of Finance who repeatedly reaffirmed at G20 and WEF Davos that Saudi Arabia has no plans to introduce personal income or wealth taxation, relying on VAT, corporate taxes on foreign entities, and Zakat.
20. **Abdulhamid Al-Amri:** Prominent Saudi real estate economist and columnist who advocated aggressively for expanding and escalating the White Land Tax on vacant urban plots to curb real estate speculation; property levy excluded under Section 2.
21. **Dr. Raja Almarzoqi:** Saudi macroeconomist, GCC General Coordinator for Negotiations, and co-author of *Islamic Macroeconomics* who analyzes Sharia-compliant public finance and non-oil revenue diversification without endorsing secular wealth taxes.
22. **National Assembly Party (NAAS):** Exiled Saudi opposition party founded in 2020; its foundational political manifesto criticizes the imposition of VAT and administrative fees on citizens without democratic accountability, with no wealth tax proposals.
