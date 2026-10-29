# Area profile — Mali

Save as `data/ml/area_profile.md`. First pass completed 2026-10-29.

## 1. Scope
- Area: Mali; type: country (ISO2: `ML`)
- Depth: Seed (first run R001)
- Levels of government in scope: National (transition authorities, executive, legislature), regional (19 regions and the capital district of Bamako), and local (160 cercles loaded from official mapping data into `geo_units.csv`).
- Languages searched: French (`fr`), English (`en`)
- Date of first run: 2026-10-29

## 2. Wealth tax history and live proposals (2010 onwards)
- **No general net wealth tax (ISF):** Mali has never enacted a general annual tax on net wealth or net worth. The domestic tax system administered by the Direction Générale des Impôts (DGI) is based on the General Tax Code (*Code Général des Impôts*) and relies predominantly on indirect consumption taxes (TVA at 18%), direct taxes on business profits (IBIC/IS at 30%), and personal income taxes on salaries (ITS) [1].
- **Focus on resource sovereignty and mining tax reform:** The national debate regarding the taxation of large accumulations of wealth centers almost entirely on natural resources (particularly gold, the nation's chief export). Under the transition government (2020–present), the state adopted the 2023 Mining Code to increase state and local participation up to 35% and aggressively audited multinational mining operators (such as Barrick Gold and B2Gold), recovering hundreds of billions of CFA francs in tax arrears and renegotiating royalty agreements [2].
- **Bilateral tax treaties:** In December 2023, Mali and Niger jointly denounced their 1972 bilateral double-taxation convention with France, which officially terminated in March 2024 to restore domestic taxing rights over cross-border capital flows and service payments [3].
- **High economic informality:** Because roughly 80% of economic activity takes place in the informal sector, economic and fiscal policy focuses on broadening the formal tax base, reducing discretionary corporate exemptions, and digitizing revenue collection rather than introducing complex individual net wealth taxes.

## 3. Legislatures and where their records are
- **Conseil National de la Transition (CNT):** Following the dissolution of the elected National Assembly in August 2020, legislative powers have been exercised by the Conseil National de la Transition (147 members presided over by Colonel Malick Diaw; `https://cnt.ml`). Plenary sessions and committee hearings are reported through the national press (*L'Essor*) and broadcast via ORTM. No bill, motion, or amendment proposing a net wealth tax has been introduced in the CNT.
- **Future bicameral parliament:** The new Constitution approved by referendum in June 2023 and promulgated in July 2023 establishes an Assemblée Nationale and a Sénat, which will be constituted following transition elections.

## 4. Parties
- Major political parties include:
  - **Solidarité Africaine pour la Démocratie et l'Indépendance (SADI):** Left-wing party led by Oumar Mariko; rhetoric focuses on rural peasants against urban political elites and multinational mining exploitation, but platform does not include a net wealth tax.
  - **Yéléma:** Led by former Prime Minister and certified accountant Moussa Mara; prioritizes fiscal transparency, regular personal asset declarations, and elimination of tax exemptions.
  - **Union pour la République et la Démocratie (URD)**, **ADEMA-PASJ**, **Rassemblement pour le Mali (RPM)**, and coalition platforms like **M5-RFP**.
  - None of these parties' programmes include an annual net wealth tax.

## 5. Government below national level
- **Structure:** 19 administrative regions plus the District de Bamako (Admin 1), divided into 160 cercles / communes urbaines (Admin 2).
- **Taxation powers:** Local collectivités territoriales (cercles and communes) collect local development and market fees (taxe de développement régional et local - TDRL, taxe de voirie, patentes locales). They have no statutory authority to levy taxes on net wealth or capital.
- **Official source:** The 160 cercles and 20 regions are sourced directly from the official administrative boundaries published by the Institut Géographique du Mali (IGM) via the OCHA Common Operational Datasets (COD-AB) under CC BY-IGO 3.0 (`data/ml/boundaries.json`).

## 6. Search terms
- French: `impôt sur la fortune`, `ISF`, `taxe sur les grandes fortunes`, `impôt sur le patrimoine`, `taxe Zucman`, `justice fiscale`, `imposition des riches`.
- Ambiguous phrases:
  - *Impôt sur le patrimoine* in WAEMU / UEMOA member states refers to real estate and property taxes (*impôt sur le patrimoine foncier* on built and unbuilt property), which are excluded under Section 2.
  - In religious commentary, *zakat* is occasionally referred to colloquially as "l'impôt sur la fortune", but is a religious pillar rather than statutory tax policy.

## 7. Media
- Major national news portals and print media:
  - *L'Essor* (`https://lessor.ml`, national public daily)
  - *Maliweb.net* (`https://www.maliweb.net`)
  - *Malijet.com* (`https://malijet.com`)
  - *Bamada.net* (`https://bamada.net`)
  - *Le Républicain*, *L'Indépendant*, *Le Combat*

## 8. Registers
- Direction Générale des Impôts (DGI): `https://dgi.gouv.ml`
- Extractive Industries Transparency Initiative (ITIE-Mali): `https://itie.ml`
- Primature de la République du Mali: `https://www.primature.ml`

## 9. Known networks
- **Coalition Malienne Publiez Ce Que Vous Payez (PCQVP Mali):** National chapter of Publish What You Pay, focusing on mining revenue disclosure and natural resource accountability.
- **Coalition des Alternatives Africaines Dette et Développement (CAD-Mali):** Campaigns on debt cancellation, fair taxation, and ending regressive consumption taxes.
- **Trade union confederations:** Union Nationale des Travailleurs du Mali (UNTM) and Confédération Syndicale des Travailleurs du Mali (CSTM), with their joint research arm CARES-Mali; focus on personal income tax on wages (ITS) and basic goods affordability.
- **Oxfam au Mali:** Active in humanitarian relief, climate resilience, and domestic resource mobilization advocacy.

## 10. Plan for the next runs
- **Expected yield:** Low. Research across parliamentary, party, union, civil society, and academic layers confirms that no domestic wealth tax proposal exists in Mali.
- **Future monitoring:**
  1. Monitor multilateral negotiations on the UN Framework Convention on International Tax Cooperation (Africa Group) and the Alliance of Sahel States (AES) for any coordinated initiatives targeting high-net-worth wealth.
  2. Screen academic publications from the Faculté des Sciences Économiques et de Gestion (FSEG, Université de Bamako) and the Centre d'Études et de Renforcement des Capacités d'Analyse (CERA) for any theoretical or policy papers addressing capital stock taxation.
  3. Track any future public endorsements by Malian civil society coalitions (PCQVP, CAD-Mali) if international billionaire tax campaigns expand into francophone West Africa.

---

### Sources
1. Direction Générale des Impôts (DGI), *Code Général des Impôts du Mali*, `https://dgi.gouv.ml`.
2. Sika Finance, "Mali : Le gouvernement recouvre des centaines de milliards d'arriérés d'impôts miniers", `https://sikafinance.com/marches/mali-le-gouvernement-recouvre-des-centaines-de-milliards-darrieres-dimpots-miniers_44521`.
3. Ministère de l'Économie et des Finances, "Dénonciation de la convention fiscale bilatérale franco-malienne", `https://www.impots.gouv.fr`.
