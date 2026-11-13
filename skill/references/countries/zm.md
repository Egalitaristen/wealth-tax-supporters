# Zambia (data/zm)

Seed pass R001 (2026-11-13). Check that URLs still resolve before relying on them.

- **Geography:** 10 provinces (`ZM101`...) and 116 districts (`ZM101001`...) from the OCHA COD-AB Zambia layers (v02, valid 2023-06-29, CC BY-IGO 3.0), via the HDX API (`package_show?id=cod-ab-zmb`). The geojson zip is 123 MB (it holds settlement levels); only `zmb_admin1.geojson` and `zmb_admin2.geojson` are used. Recipe as for Namibia: `topo_to_boundaries.py zmb_admin2.geojson --name-prop adm2_name --code-prop adm2_pcode --project lonlat --scale 120 --simplify 0.35`, admin1 as regions, then `merge_boundaries.py`.
- **Seats:** none. The 13 August 2026 election result was still being settled in October 2026 (dispute over the 40 proportional seats), and no official member list was read.
- **Wealth tax status:** none in force; property transfer tax (on transfers) and rental income tax only, no estate duty, no capital gains tax.
- **What exists:** ActionAid Zambia (2020 statement, tax advisor interview), CUTS Lusaka's 2020 Fair Tax Monitor (funded by Oxfam Zambia), CAN Zambia (2025 pan-African letter), Socialist Party president Fred M'membe (September 2026 policy manifesto, as reported). The June 2022 ActionAid/CTPD report designs a net wealth tax but recommends enforcing existing asset taxes instead (excluded).
- **Sources that work:** lusakatimes.com, diggers.news, zambiamonitor.com, zambia.actionaid.org PDFs, maketaxfair.net PDFs, afrobarometer.org. **Blocked:** fightinequality.org and core.ac.uk (403 to scripts).
- **Watch out:** the Afrobarometer item on taxing the rich at higher rates is not a wealth tax poll; land holdings tax and property transfer tax are excluded.
