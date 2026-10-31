# Malawi: wealth tax debate, sources and layers

Notes from seed pass (R001, October 2026). Check that URLs still resolve before relying on them.

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | National Assembly of Malawi (unicameral, 193 seats, expanding to 229 in 2025). | Exclusive constitutional power over direct and indirect taxation. No wealth tax bill has been enacted or tabled. |
| region | 3 Regions: Northern (`MW1`), Central (`MW2`), Southern (`MW3`) | Parented to Malawi (`G0001`). Administrative level. |
| local | 32 Local Government Authorities: 28 District Councils and 4 City Councils (Lilongwe City `MW210`, Blantyre City `MW315`, Mzuzu City `MW107`, Zomba City `MW314`) | The local map tier. Codes: official UN OCHA P-codes (`MW101` to `MW315`), parented to their respective regions. |

**Map:** `data/mw/boundaries.json` is generated from the National Statistics Office of Malawi via the UN OCHA Common Operational Datasets (COD-AB) for Malawi on HDX (`cod-ab-mwi`), republished under **CC BY-IGO**. Contains 32 local councils (projected `lonlat`, scale 100, tolerance 0.5) merged with 3 region outlines (50 KB).

## Wealth tax debate context

Malawi has severe income and wealth inequality, with the top 10% owning 61% of total wealth and the wealthiest 1% earning as much income as the bottom 50% combined (CRI Index Malawi Profile 2025). Crushing debt service consumes domestic revenue, prompting prominent economists and civil society coalitions to advocate for progressive wealth taxation.

- **Key policy proposal (July 2025):** At the launch of the *Commitment to Reducing Inequality (CRI) Index Malawi Country Profile 2025* in Lilongwe, Dr. Bertha Bangara-Chikadza (President of the Economics Association of Malawi - ECAMA) presented a 5-point fiscal reform agenda centered on introducing a moderate wealth tax (the Oxfam profile estimates it could raise $70 million, 0.7% of GDP, / K779 billion annually; the Nation article misreads the 0.7% as a rate to fund essential healthcare for 890,000 citizens).
- **Solidarity wealth levy:** Agnes Nyirongo (Economic Governance Officer at the Centre for Social Concern - CfSC) proposed a solidarity wealth levy on the richest 1% to 5% of individuals framed as a national development contribution.
- **Trade union pushback (January 2026):** The Malawi Congress of Trade Unions (MCTU) rejected government proposals to tax retirement pensions and death benefits, demanding that Treasury shift revenue measures to wealth, high-income earners, tax evasion, and illicit financial flows.
- **Legislative landscape:** The National Assembly has passed progressive income tax amendments (including a 40% top PAYE bracket on monthly earnings over K10 million) and corporate turnover minimums (MAT), but no political party (MCP, DPP, UTM) has introduced a standalone net wealth tax bill.

## Key terminology

- **Included terms:**
  - Wealth tax / Tax on wealth
  - Moderate wealth tax / Solidarity wealth levy
  - *Msonkho wa chuma* / *Msonkho pa chuma*: Chichewa for tax on wealth/riches.
  - *Msonkho wa olemera*: Tax on the rich.
- **Excluded terms (single-asset taxes or separate mechanisms):**
  - *Msonkho wa malipiro* / PAYE (personal income tax, including the top 40% band).
  - Estate Duty Act (inheritance tax on deceased estates).
  - Minimum Alternative Tax (MAT) on gross turnover (corporate revenue).
  - Capital gains tax on listed shares (realization).
  - Mobile money transfer levy (transaction tax).
  - City rates / Ground rates (local property rates).

## What worked and what to watch

- **The Nation (`mwnation.com`):** Most detailed and consistent coverage of fiscal reform debates, pre-budget submissions, and civil society launches in Malawi.
- **Times Group (`times.mw`):** Reliable coverage of parliamentary affairs, inequality indices, and MEJN statements.
- **Oxfam Southern Africa / Open Repository:** Authoritative host for the CRI Country Profile reports.
- **Local councils:** Under the Local Government Act, district and city councils have no authority over wealth or income taxes. Unit-by-unit sweeping yields zero results; follow national aggregators and civil society networks instead.
