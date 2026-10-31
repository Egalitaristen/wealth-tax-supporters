# Saudi Arabia (data/sa)

Worked notes from the Saudi Arabia research pass (`R001` seed pass, 2026-10-31; 1 identified supporter, 6 documented exclusions, 1 opinion poll, 7 logged bilingual queries, 147 governorates loaded).

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
