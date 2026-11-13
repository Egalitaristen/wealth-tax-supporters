# Sri Lanka: a wealth tax abolished in 1992, listed in the IMF programme, not enacted

Notes from the seed pass (R001, 13 November 2026). Check that URLs still resolve before relying on them.

## Levels and the geography register

| Level | Units | Notes |
|---|---|---|
| national | Government, Parliament (`G0002`, 225 members) | Taxes set by the national Parliament |
| region | 9 provinces | OCHA P-codes `LK1` to `LK9` |
| council | 25 districts | The map tier, P-codes `LK11` to `LK92`. The 331 divisional secretariats (admin 3) and local authorities are not loaded |

**Map:** `data/lk/boundaries.json` is the OCHA COD-AB Sri Lanka dataset (Survey Department boundaries) from data.humdata.org (`cod-ab-lka`), CC BY-IGO 3.0. Recipe:

```bash
# unzip lka_admin_boundaries.geojson.zip from the HDX resource list
python skill/scripts/topo_to_boundaries.py lka_admin2.geojson --name-prop adm2_name --code-prop adm2_pcode --project lonlat --scale 60 --simplify 1.0 --licence CC-BY-IGO-3.0 --licence-url https://creativecommons.org/licenses/by/3.0/igo/ --code-scheme "OCHA P-codes (Survey Department of Sri Lanka)" --source "OCHA/HDX COD-AB Sri Lanka (Survey Department boundaries)" --out units.json
# same for lka_admin1.geojson with adm1_name / adm1_pcode, then copy its units into "regions"
```

## Wealth tax debate context

- 1958 wealth tax, abolished 1992/93 (1990 Tax Commission).
- 2022 IMF staff-level agreement and 2023 programme list a wealth tax; the June 2024 "wealth tax" was an imputed rental income tax on property (not recorded as evidence). The NPP government has not proposed one.
- Support comes from international bodies (IMF, World Bank, HRW, Crisis Group) and think tanks (IPS, Arutha). Advocata opposes. No union, party or sitting MP statement found in English.

## What worked and what to watch

- **Daily FT** (ft.lk) renders in JavaScript: plain scripts get only the page title. Use the browser, and read the byline: many columns carry only an email address.
- Daily Mirror, Sunday Times, The Morning, News 1st, HRW and Sangam.org answer plain scripts with a browser User-Agent. crisisgroup.org answered 403/404; the report is reprinted on sangam.org and ft.lk.
- **Seats:** parliament.lk `members-of-parliament/mp-listing?page=N` (about 29 pages of 8 members, party and district printed for each); count the "Political Party" field. Wikipedia's party counts matched it.
- "Wealth tax" in Sri Lankan press often means the property or imputed rental tax: check the design before grading.

## Terms

wealth tax, super-rich tax, wealth transfer tax, property and wealth tax; Sinhala වත්කම් බද්ද (not yet searched). Out of definition: property tax, mansion tax, imputed rental income tax, gift and inheritance tax, windfall tax.
