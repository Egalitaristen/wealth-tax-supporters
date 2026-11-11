# Bangladesh: surcharge, not a wealth tax; a 2026 plan dropped

Notes from the seed pass (R001, 11 November 2026). Check that URLs still resolve before relying on them.

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | Government of Bangladesh, Jatiya Sangsad (`G0002`) | Taxes are set by the national Finance Act; the NBR administers them |
| region | 8 divisions (Barishal, Chattogram, Dhaka, Khulna, Mymensingh, Rajshahi, Rangpur, Sylhet) | OCHA P-codes `BD10` to `BD60`, parent `G0001` |
| council | 64 districts (zila) | The map tier. OCHA P-codes `BD1004` to `BD6094`. The 495 upazilas (OCHA admin 3) are not loaded |

**Map:** `data/bd/boundaries.json` uses the OCHA COD-AB Bangladesh boundaries (Bangladesh Bureau of Statistics shapes, version 3 valid on 2023-05-21), dataset `cod-ab-bgd` on data.humdata.org. Licence: CC BY-IGO 3.0 (`creativecommons.org/licenses/by/3.0/igo/`), as stated by the HDX API (`package_show?id=cod-ab-bgd`). Recipe:

```bash
# download the GeoJSON zip from the HDX resource list, unzip bgd_admin1.geojson and bgd_admin2.geojson
python skill/scripts/topo_to_boundaries.py bgd_admin2.geojson --name-prop adm2_name --code-prop adm2_pcode --project lonlat --scale 60 --simplify 1.0 --licence CC-BY-IGO-3.0 --licence-url https://creativecommons.org/licenses/by/3.0/igo/ --code-scheme "OCHA P-codes (BBS)" --source "OCHA/HDX COD-AB Bangladesh (BBS boundaries)" --out units.json
# same for bgd_admin1.geojson with adm1_name / adm1_pcode, then copy its units into "regions" of units.json
```

Both files come out with the same `viewBox`, so the outlines fall on the district borders.

## Wealth tax debate context

- The Wealth Tax Act, 1963 was repealed in 1999; a surcharge on income tax payable for wealthy taxpayers has applied since FY2011-12 (10% to 35% for net wealth above Tk 4 crore).
- May 2026: the NBR drafted a direct tax of 0.25% to 1% on declared net wealth above Tk 4 crore to replace the surcharge (about Tk 5,000 crore). Economists welcomed it; the government dropped it before the 11 June 2026 budget.
- Opponents: Masud Khan (Daily Star, 20 May 2026), Muhith, Mirza Azizul Islam, Sajjad Zohir (2011), Mamun Rashid (2023). Recorded in `exclusions.csv`, not as actors.

## What worked and what to watch

- **Where the supporters are.** Economists and think tanks (CPD above all, then BIDS, PRI, SANEM), one government task force, and press columns. The CPD website republishes press articles with its own headline; the original date is the date of the statement (see E00002 and E00016).
- **No party layer.** BNP, Jamaat and NCP 2026 manifestos held tax cuts and tax-net pledges only. No MP statement on a wealth tax was found; try Bengali budget-debate reports.
- **Surcharge or wealth tax?** Almost every article says "wealth tax" for the surcharge. Record only statements for a direct tax on net wealth, or those that name "wealth tax" as a reform; mark the ambiguous ones C (Raihan, Parvez) and the 2019 budget proposal B with the doubt in `grading_note`.
- **Inheritance and property tax** are frequent companions in the same article (CPD 2023, Task Force); they do not count on their own.
- **Fetching.** `urllib` with a browser `User-Agent` works for the Daily Star, TBS, Prothom Alo English, CPD, bdnews24 and FE. Dhaka Tribune and Bangla Tribune answer 403.
- **Dates.** Take `datePublished` or `article:published_time`; the Daily Star prints "Published :" in the text.
- **Mismatched search summaries.** A search summary credited Zahid Hussain with a wealth and inheritance tax suggestion that, in the article, belongs to Rizwanul Islam. Always read the article.

## Terms

wealth tax / ওয়েলথ ট্যাক্স / সম্পদ কর, wealth surcharge / সম্পদ সারচার্জ, net wealth / নিট সম্পদ, high-net-worth individuals (HNWI). Out of definition: inheritance tax, property or holding tax, land development tax, capital gains tax, black-money whitening.
