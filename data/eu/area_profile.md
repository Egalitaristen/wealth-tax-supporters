# Area profile — European Union

## 1. Scope
- Area: European Union (`data/eu`); type: supranational
- Depth: Seed (R001, 2026-11-14)
- Levels in scope: EU-level / pan-European organisations (EP political groups, European political parties, trade union confederations, NGOs/coalitions, think tanks, EU-level campaigns), plus sitting MEPs recorded in their own national `data/<iso2>` registers and synced into `data/eu/positions.csv` via `python skill/scripts/seats.py data/eu`.
- Languages searched so far: English (`en`), French (`fr` on `tax-the-rich.eu`).
- Date of first actor run: 2026-11-14 (R001)

## 2. Wealth tax history and live proposals (2010 onwards)
- **Tax the Rich European Citizens' Initiative** (`ECI(2023)000006`): registered 11 July 2023; signature collection 9 October 2023 – 9 October 2024 (357,155 signatures; closed short of 1 million). Called on the Commission to propose a European wealth tax on great fortunes under Article 115 TFEU (`https://www.tax-the-rich.eu/`).
- **EP Subcommittee on Tax Matters (FISC)**: December 2025 public hearing on "Taxation of Ultra-high-net-worth individuals" (with Gabriel Zucman presenting a 2% minimum effective wealth tax on >€100m) and 2026 own-initiative report work on a tax framework for UHNWIs.
- **DG TAXUD Wealth Taxation Study** (April 2026): multi-volume Commission study mapping wealth-related taxes across EU member states.
- **EU Tax Observatory** (June 2024 / March 2025): blueprint for a 2% global/EU minimum effective tax on billionaires (`https://taxobservatory.world/publication/a-blueprint-for-a-coordinated-minimum-effective-taxation-standard-for-ultra-high-net-worth-individuals/`).

## 3. Legislatures and where their records are
- **European Parliament** (`B0001`, 720 seats, elected June 2024): member list and groups via open data API `https://data.europarl.europa.eu/api/v2/meps/show-current`.
- Debate, committee (FISC/ECON), and vote records: `https://www.europarl.europa.eu/`

## 4. Parties and EP Political Groups
- **Greens/EFA** (`greens-efa.eu`): published September 2023 study proposing an EU-wide progressive wealth tax.
- **European Green Party** (`europeangreens.eu`): 2024 EU election manifesto calls for an EU-wide wealth tax.
- **S&D Group** (`socialistsanddemocrats.eu`): February 2025 statement calling for coordinated wealth taxes.
- **Party of European Socialists (PES)** (`pes.eu`): October 2025 Congress resolution backing a European wealth tax initiative and the G20 2% billionaire minimum tax (Zucman tax).
- **Volt Europa** (`volteuropa.org`): adopted policy calling for EU-wide minimum effective rates for wealth taxation and a European Central Financial Wealth Data Register.
- **The Left in the EP** (`left.eu`) & **Party of the European Left** (`european-left.org`): open leads for explicit wealth-tax quotes (2024 manifesto says "tax on the wealthy").

## 5. Government below national level
- Not applicable (`supranational: true`; sub-EU levels belong to national `data/<iso2>` registers).

## 6. Search terms
- English: `"wealth tax" "European Union"`, `"billionaire tax"`, `"Tax the rich" "European Citizens' Initiative"`, `"Zucman tax"`
- French: `"impôt sur les grandes fortunes"`, `"impôt sur la grande fortune"`
- Ambiguous terms to watch: `"tax the super-rich"`, `"tax the wealthy"`, `"super-profits"` (windfall taxes are excluded unless paired with net wealth).

## 7. Known networks and civil society
- **Trade unions**: ETUC (December 2023 Executive Committee resolution), EPSU (open lead, 403 to plain HTTP).
- **NGOs & campaigns**: Oxfam International (EU Office), European Environmental Bureau (EEB), WeMove Europe, SOLIDAR, Eurodad, Global Redistribution Advocates, Tax the Rich ECI.
- **Think tanks**: FEPS (Foundation for European Progressive Studies), EU Tax Observatory.

## 8. Plan for the next runs
1. Check 8 open leads in `data/eu/leads.csv`: EPSU and EESC (blocked 403 to plain HTTP; open with browser), The Left EP, Party of the European Left, European Left Alliance, Tax Me Now, Millionaires for Humanity, DiEM25.
2. Check European Parliament FISC 2025/2026 hearings and own-initiative report for MEP and witness positions (adding MEPs to their national `data/<iso2>` registers and running `seats.py data/eu`).
3. Search in German, Spanish, Italian, and French for pan-European wealth-tax campaigns and academic/commentator voices.

## Resources pass (1 November 2026)

Listed under `global` (the build accepts register folders and `global` only, so the EU and UN pages show no Method-tab list): the 2023 "Tax the rich" citizens' initiative (registered 11 July 2023; collection closed unsuccessful, 357,155 signatures, read on the Commission's register page), the Greens/EFA study of September 2023, the EU Tax Observatory's March 2025 note on minimum taxation in the EU, the FEPS/Renner policy study of March 2021, WIFO's 2022 article on a harmonised EU net wealth tax, and Landais, Saez and Zucman's April 2020 VoxEU column. No Parliament or Commission bill exists; no EU-wide poll on a wealth tax was found.

Leads not listed:
- European Parliament research briefing "Solidarity and wealth tax" (Policy Department for Budgetary Affairs, April 2022, read): covers solidarity levies of many kinds as well as wealth taxes, so it was left out.
- The Commission's study on wealth-related taxes (launched December 2024, per Commissioner Hoekstra as quoted in press) and the December 2025 hearing of Parliament's tax subcommittee (FISC) on taxing ultra-high-net-worth individuals: no document read.
- The EU Tax Observatory note's own figures were not read in full (its page shows no revenue numbers); the 67 and 121 billion euro figures come from Oxfam's press release of 17 March 2025.
