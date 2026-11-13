# Lebanon: the crisis-era wealth tax debate

Seed pass R001 (2026-11-13). 9 supporters, 10 evidence rows (grade A 4 actors, B 1, C 4). No wealth tax exists. The register rests on one bill (Taymour Joumblatt, 14 April 2021), one party programme (Lebanese Communist Party, 2022) and economists' papers written after the 2019 financial collapse. Check that URLs still resolve before relying on them.

| Level | Units | Notes |
|---|---|---|
| national | Parliament (`B0001`), 128 seats, half Christian and half Muslim | Seats by alliance from the 15 May 2022 election results, tabulated on Wikipedia from the Interior Ministry figures. Parliament extended its own term in March 2026 (two years). `lp.gov.lb` (the Parliament's site) was not read, so no member is marked sitting. |
| region | 8 governorates | OCHA COD-AB admin level 1, codes `LB1`...`LB8` (Akkar is `LB7`, Baalbek-Hermel `LB8`). |
| county | 26 districts (qada) | OCHA admin level 2, codes `LB11`...`LB63`. The 1,600 cadastral localities (admin level 3, with a "Conflict" placeholder) were not loaded. |

**Map:** `data/lb/boundaries.json` from OCHA / HDX "Lebanon - Subnational Administrative Boundaries" (COD-AB, CC BY-IGO 3.0, valid 2024-11-13 to 2025-10-30), OCHA P-codes. From `lbn_admin_boundaries.geojson.zip`, using `lbn_admin2.geojson` (units) and `lbn_admin1.geojson` (regions):

```bash
C="--project lonlat --scale 150 --simplify 0.3 --licence CC-BY-IGO-3.0 --licence-url https://creativecommons.org/licenses/by/3.0/igo/ --code-scheme 'OCHA COD-AB P-codes' --source 'OCHA / HDX Lebanon Subnational Administrative Boundaries (COD-AB, CC BY-IGO)'"
python skill/scripts/topo_to_boundaries.py lbn_admin2.geojson --name-prop adm2_name --code-prop adm2_pcode $C --out units.json
python skill/scripts/topo_to_boundaries.py lbn_admin1.geojson --name-prop adm1_name --code-prop adm1_pcode $C --out regs.json
python skill/scripts/merge_boundaries.py units.json --regions regs.json --out data/lb/boundaries.json
```

**The debate:** bill of 14 April 2021 (0.5% to 7% in eight brackets on wealth of USD 1 million and up; owner-occupied homes and some other assets exempt); LCP programme 2022 (2% above USD 1 million); Carnegie (Assouad 2019 and 2021), FES (Dibeh 2020), Arab Reform Initiative (2021) and ESCWA (2020) papers. Out of definition: the Sayrafa windfall tax, the financial gap law's levy on pre-crisis transfers, taxes on bank profits, bail-in of shareholders and depositors.

**Sources that work:** legal-agenda.com, lebanon24.com, carnegieendowment.org (use the `?lang=en` URL for the 2019 piece), arab-reform.net, lebanon.fes.de, digitallibrary.un.org. Al-Akhbar and unescwa.org returned bot checks to plain clients; al-nidaa.com refused connections and was read from the Wayback copy; old.lcps-lebanon.org has an expired certificate.

**Quirks:** the family name appears as Joumblatt, Jumblatt and Jumblat; Taymour and Walid are father and son. The LCP is *al-Hizb al-Shuyu'i al-Lubnani*. "Solidarity tax" (*dariba al-tadamun*) in the 2021 budget debate is a lead, not read.
