# Algeria (`dz`) — Country Reference Guide

## Geography & Map Layers

- **Hierarchy (`geo_units.csv`)**:
  - `G0001`: `Algeria` (`national`, `DZ`)
  - `G0002`: `Assemblée Populaire Nationale` (`chamber`, `APN`) — lower house of Parliament (407 seats)
  - `G0003`: `Conseil de la Nation` (`chamber`, `CN`) — upper house of Parliament (174 seats)
  - `G0004`–`G0051`: **48 Wilayas** (`region`, `DZ-01` Adrar through `DZ-48` Relizane, parent `G0001`)
  - `G0052`–`G1592`: **1,541 Communes** (*baladiyahs*, `council`, 6-digit OCHA/ONS p-codes `001001` through `048038`, parent `G0004`–`G0051`)
- **Boundary polygons (`boundaries.json`)**:
  - Source: UN OCHA / Humanitarian Data Exchange (HDX) Common Operational Dataset — Administrative Boundaries (`COD-AB`) for Algeria (compiled by INCT / ONS), licensed under **`CC-BY-IGO-3.0`**.
  - Contains `1,540` commune polygons under `units` (`level: "council"`) and `48` wilaya outlines under `regions`. Note: `G0211` (*Beni Maouche*, `006010`, in Béjaïa) is a valid commune row in `geo_units.csv` that is merged into its neighboring polygon in the upstream OCHA shapefile (`wtdb.py validate` permits up to 10% unmapped council rows).
  - Note on post-2019 wilayas: Law No. 19-12 of December 2019 elevated 10 southern administrative districts (*wilayas déléguées*) to full wilayas (`DZ-49` Timimoun through `DZ-58` El Meniaa); when assigning `geo_unit_id` for actors in those southern communes, match by the commune name (`level = council`), which remains unchanged under its historical parent wilaya in `geo_units.csv`.

## Statutory Wealth Tax Framework

Algeria has had a statutory net wealth tax in **Articles 274–282 of the *Code des impôts directs et taxes assimilées* (CIDTA)** since the **1993 Finance Law**, reformed repeatedly:

1. **1993–2019 (*Impôt sur le patrimoine* / الضريبة على الأملاك)**:
   - Enacted in the 1993 Finance Law on individual net real estate and luxury movable assets. By 2015–2019, the threshold stood at **100M DZD** (10 billion centimes), but the tax remained largely uncollected ("ink on paper") due to the lack of a digitized cadastre and widespread informal cash holdings (*أصحاب الشكارة*).
2. **2017 (*Projet de loi de finances pour 2018*, Article 12)**:
   - Prime Minister **Ahmed Ouyahia** and Finance Minister **Abderrahmane Raouya** proposed renaming the tax *Impôt sur la fortune* (ISF) with a **50M DZD** (5 billion centimes) threshold and progressive rates of **1% to 3.5%**.
   - Deleted by the FLN–RND majority on the APN Finance Committee (chaired by **Toufik Torche**) on 17 November 2017 after lobbying by the **Forum des Chefs d'Entreprises (FCE)** (**Ali Haddad**), over fierce objections from the **Parti des Travailleurs (PT)**, **MSP**, **FFS**, and **Ennahda–Adala–Bina**.
3. **2020 Supplementary Finance Law (*Loi de finances complémentaire pour 2020*, Articles 26–32)**:
   - Enacted the revamped ***Impôt sur la fortune (ISF)*** (الضريبة على الثروة) on net worldwide assets of Algerian residents (and Algerian-situs assets of non-residents) exceeding **100M DZD** (10 billion centimes) at progressive rates of **0.15% (100–150M), 0.25% (150–250M), 0.35% (250–350M), 0.50% (350–450M), and 1.00% (>450M DZD)**, splitting proceeds **70% to the State budget** and **30% to the local-government solidarity fund (CSGCL)**.
4. **2021–2023 Digitization & *CAD-Fisc* Enforcement**:
   - Presidential directives (**Abdelmadjid Tebboune**, Oct 2021 & Oct 2022) and ministerial instructions (**Laaziz Faid**, May & Aug 2023) established the **DGDN–DGI cadastral data-sharing protocol (*CAD-Fisc*)** to cross-check land registries and enforce the ISF.
5. **2026 Finance Law (*Projet de loi de finances pour 2026*, Article 25)**:
   - Lowered the ISF liability threshold from **100M DZD (10 billion centimes) to 80M DZD (8 billion centimes)** with a revised progressive bracket schedule of **0.20% (80–120M), 0.30% (120–200M), 0.40% (200–300M), 0.50% (300–400M), and 1.00% (>400M DZD)**, annual filing by 31 March, and **10%–25% late-filing penalties**.

## Currency & Number Conventions

- Currency is the **Algerian dinar (`DZD`, د.ج / DA)**.
- **Centimes trap**: In Algerian Arabic and French media and parliamentary debates, large sums are routinely stated in **centimes** (*سنتيم* / *centimes*, where `1 DZD = 100 centimes`):
  - `1 milliard de centimes` (1 مليار سنتيم) = **10,000,000 DZD** (10 million DZD)
  - `5 milliards de centimes` (5 ملايير سنتيم) = **50,000,000 DZD** (50 million DZD — the 2017 PLF 2018 threshold)
  - `8 milliards de centimes` (8 ملايير سنتيم / sometimes loosely written `8 مليار دج` in headlines) = **80,000,000 DZD** (80 million DZD — the 2026 PLF threshold)
  - `10 milliards de centimes` (10 ملايير سنتيم) = **100,000,000 DZD** (100 million DZD — the 2020 LFC threshold)
- Always normalize thresholds in `design_detail` and `notes` to **million DZD** (putting the centimes equivalent in parentheses when quoted in the source).

## Source Accessibility & Geo-Blocking Notes

- **DZSecurity geo-blocking**: Official `.dz` government and state-agency domains (`aps.dz`, `mfdgi.gov.dz`, `mf.gov.dz`, `joradp.dz`, `apn.dz`, `conseil-constitutionnel.dz`, `elmoudjahid.com`) are behind the **DZSecurity** firewall and return connection timeouts or 403 blocks to non-Algerian IPs.
- **Cloudflare / dead domains**: `elwatan-dz.com` serves a Cloudflare challenge to automated fetchers; `liberte-algerie.com` ceased publication in April 2022.
- **Recommended open domains for `source_url`** (verified compatible with `wtdb.py checkquotes`):
  - French: `tsa-algerie.com`, `algerie-eco.com`, `radioalgerie.dz` / `news.radioalgerie.dz` (republishes full APS dispatches verbatim and is open globally), `lnr-dz.com`, `jeune-independant.net`, `dknews-dz.com`, `algeriepatriotique.com`.
  - Arabic: `echoroukonline.com`, `elkhabar.com`, `el-massa.com`, `elhiwar.dz`, `almostathmir.dz`, `independentarabia.com`, `asharq.com`, `aawsat.com`.
  - Note on `echoroukonline.com`: Very long Arabic slugs are truncated by WordPress at 200 UTF-8 percent-encoded characters; always copy the exact `<link rel="canonical">` URL when citing Echorouk Online.
