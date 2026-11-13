# Zimbabwe (data/zw)

Seed pass R001 (2026-11-13). Check that URLs still resolve before relying on them.

- **Geography:** 10 provinces (`ZW10`...`ZW19`) and 91 districts (`ZW1601`...) from the OCHA COD-AB Zimbabwe layers (valid 2018-09-11, CC BY-IGO 3.0), via the HDX API (`package_show?id=cod-ab-zwe`); the geojson zip (43 MB) downloads with a plain GET. Recipe: `topo_to_boundaries.py zwe_admin2.geojson --name-prop adm2_name --code-prop adm2_pcode --project lonlat --scale 120 --simplify 0.35`, admin1 as regions, then `merge_boundaries.py`.
- **Seats:** `bodies.csv` B0001 is the National Assembly (280) with the 194 ZANU-PF and 86 CCC of CITE's report on the 18 June 2026 vote; parlzim.gov.zw answers scripts with a bot check, so its Hansard and member list were not read. Zimbabwe is not in `seats.py`.
- **Wealth tax status:** the Finance Act 2023 (No. 13) "wealth tax" on dwellings above US$250,000 (proposed at US$100,000) is a property tax and is excluded (X0001); collection has been suspended. Supporters of the government's design are not recorded.
- **What exists:** Fight Inequality Alliance Zimbabwe and three of its spokespeople (2021 to 2025), Oxfam Southern Africa (January 2022), MP Mathew Nyashanu (December 2022). No bill, motion or poll.
- **Sources that work:** 263chat.com, bulawayo24.com, thenewshawks.com, midweekwatch.com, newsday.co.zw (ledes), cite.org.zw, afriwise.com. **Blocked or empty:** parlzim.gov.zw, pindula.co.zw, fightinequality.org, theindependent.co.zw (JavaScript).
- **Watch out:** in Zimbabwean coverage "wealth tax" almost always means the 2024 property charge; read the speaker's words for a tax on net wealth. Nyashanu's name is printed Mathew (Electoral Commission) and Matthew (NewsDay); the Wikidata item Q100524761 for "Mathew Nyashanu" is a researcher and was not used.
