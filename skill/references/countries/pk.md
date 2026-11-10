# Pakistan: wealth tax debate, sources and layers

Notes from seed pass (R001, November 2026). Check that URLs still resolve before relying on them.

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | Majlis-e-Shoora (Parliament of Pakistan): National Assembly (`B0001`, 336 seats) and Senate (`B0002`, 96 seats) | Legislative authority over broad direct wealth taxation resides exclusively at the federal level under the Constitution of Pakistan (Federal Legislative List, Entry 50: taxes on capital value of assets, not including immovable property). |
| region | 7 provincial/territorial units: Punjab, Sindh, Khyber Pakhtunkhwa, Balochistan, Islamabad Capital Territory, Azad Jammu and Kashmir, Gilgit-Baltistan | Official OCHA COD-AB codes (`PK1` to `PK7`), parent `G0001`. Provinces hold devolved power over agricultural income tax and immovable property taxation following the 18th Constitutional Amendment (2010), but cannot levy a general net wealth tax. |
| council | 160 administrative districts (*zila*) | The local administrative tier. Official OCHA COD-AB P-codes (`PK101` to `PK729`), parented to their respective provinces/territories. Districts have negligible independent revenue powers. |

**Map:** Pakistan's subnational boundaries are provided in `data/pk/boundaries.json`, compiled from OCHA / HDX Pakistan Administrative Boundaries (COD-AB, CC BY-IGO 3.0). It covers 160 administrative districts and 7 regional boundaries with official OCHA P-codes matching `geo_units.csv`.

## Wealth tax debate context

Pakistan has a rich statutory history with wealth taxation, moving between comprehensive legislation, temporary levies, and elite resistance:

- **The Wealth Tax Act, 1963:** Enacted in 1963, this law provided for an annual progressive tax on individuals' net wealth (movable and immovable property). It was repealed via the *Finance Act, 2003* under General Pervez Musharraf's administration.
- **The Income Support Levy Act, 2013:**
  - Enacted by Finance Minister Ishaq Dar (`A0001`) under the PML-N administration in June 2013 as part of the *Finance Act, 2013*.
  - Imposed a 0.5% wealth levy on individuals whose declared net movable assets exceeded Rs 1 million.
  - The proceeds were statutorily designated for the Income Support Fund to assist low-income households.
  - Due to fierce opposition from wealthy filers and business chambers, the government repealed the levy the following year via the *Finance Act, 2014*.
- **The PTI Commitments (2018–2019):**
  - Upon taking office in August 2018, incoming Finance Minister Asad Umar (`A0002`) announced plans to Bloomberg and Radio Pakistan to introduce a wealth tax to cover revenue lost from tax cuts on productive sectors.
  - In April 2019, Umar confirmed draft proposals for wealth tax and inheritance tax before standing committee discussions, though these were derailed during subsequent macroeconomic crises and leadership turnover.
- **Section 7E Deemed Income Tax (Finance Act 2022):**
  - Levied a 1% deemed income tax on the fair market value of vacant or unutilized immovable property over Rs 25 million.
  - Struck down as ultra vires by the Supreme Court in 2026. Excluded from the core register as property taxation.
- **FBR 2024–2025 Budget Deliberations:**
  - The Federal Board of Revenue proposed reviving wealth taxes on movable assets and gold in 2024 budget preparation.
  - The IMF explicitly rejected the wealth tax proposal during loan negotiations, directing Pakistan to focus strictly on income taxation and sales tax.
- **Public Opinion Research (2024–2025):**
  - A nationwide representative survey of 7,500 Pakistani adults conducted in 2024 by researchers from the International Centre for Tax and Development (ICTD) and LUMS (Dr. Umair Javed, Dr. Max Gallien, Dr. Vanessa van den Boogaard) found 42% support for a general wealth tax.
  - Support jumped above 70% when revenues were transparently earmarked for the poor and progressive exemptions shielded middle-class assets.

## Key terminology

- **Included terms:**
  - `wealth tax` / `net wealth tax`
  - `Income Support Levy` (2013 movable net wealth tax)
  - `ویلتھ ٹیکس` (wealth tax in Urdu)
  - `دولت پر ٹیکس` (tax on wealth)
  - `امیروں پر ٹیکس` (tax on the rich)
- **Excluded terms (single-asset taxes or separate tax categories):**
  - `Capital Value Tax` / `CVT`: Single-asset transaction levy on property transfers or vehicle purchases.
  - `Section 7E` / `Deemed income tax`: Vacant land/property tax.
  - `Property tax` / `Urban immovable property tax (UIPT)`: Provincial property taxes on buildings and plots.
  - `Agricultural Income Tax` (`زرعی انکم ٹیکس`): Income tax on crop harvest and farm profits, levied under provincial statutes.

## What worked and what to watch

- **Legislative records:** The National Assembly (`na.gov.pk`) maintains bills and acts in searchable format. Hansards for earlier sessions are available in PDF format.
- **Network blocks:** `senate.gov.pk` and `tribune.com.pk` may drop connections or present Cloudflare challenges to automated scrapers. Use web archives (`web.archive.org`) or browser fetch.
- **Verbatim quotes:** Always verify quotes against the exact page text. Automated quote checks require exact substring matches.
