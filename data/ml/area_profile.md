# Area profile — Mali

Save as `data/ml/area_profile.md`. Seed and wider research passes completed 2026-10-29 (`R001`, `R002`).

## 1. Scope
- Area: Mali; type: country (ISO2: `ML`)
- Depth: Seed and wider discovery pass (`R001`, `R002`)
- Levels of government in scope: National (transition authorities, executive, legislature), regional (19 regions and the capital district of Bamako), and local (160 cercles loaded from official mapping data into `geo_units.csv`).
- Languages searched: French (`fr`), English (`en`), Bambara (`bm`)
- Dates of runs: 2026-10-29 (`R001`, `R002`)

## 2. Wealth tax history and live proposals (2010 onwards)
- **Domestic tax landscape:** Mali has never had a statutory annual net wealth tax. The national tax system administered by the Direction Générale des Impôts (DGI) is codified in the General Tax Code (*Code Général des Impôts*) and relies predominantly on indirect consumption taxes (TVA at 18%), direct taxes on business profits (IBIC/IS at 30%), and personal income taxes on salaries (ITS) [1].
- **2018 presidential election proposal (Clément Dembélé):** During the 2018 presidential campaign, Professeur Clément Mahamadou Dembélé (university professor, 2018 presidential candidate, and president of the Plateforme contre la corruption et le chômage - PCC) explicitly proposed the introduction of an Impôt de Solidarité sur la Fortune (ISF) in Mali. In an interview published on 17 January 2018, Dembélé outlined his solidarity policy: *"Je mettrai en place l’ISF qui est l’Impôt de Solidarité sur la Fortune et qui sera basé sur la réalisation minière, immobilière et sur la déclaration des revenus dans les banques avec un petit prélèvement."* [2].
- **International G20 wealth tax letter (Moussa Mara):** In September 2023, former Prime Minister Moussa Mara (Prime Minister 2014–2015, certified accountant, and leader of the Yéléma party) joined an international coalition of politicians, millionaires, and economists in signing the open letter to G20 Heads of State calling for an international agreement on wealth taxes on extreme wealth (*G20 Leaders must tax extreme wealth*, hosted at `taxextremewealth.com`) [3].
- **Focus on resource sovereignty and mining tax reform:** Under the transitional military government (Colonel Assimi Goïta, 2020–present), fiscal debates regarding large wealth and capital center on natural resources (particularly gold). The government adopted the 2023 Mining Code to increase state and local equity participation up to 35%, aggressively audited multinational gold producers (e.g. Barrick Gold, B2Gold), and recovered hundreds of billions of CFA francs in tax arrears [4].
- **Bilateral tax treaties:** In December 2023, Mali and Niger jointly denounced their 1972 bilateral double-taxation convention with France, which officially terminated in March 2024 to restore domestic taxing rights over cross-border capital flows and service payments [5].

## 3. Identified supporters
- **A0001: Moussa Mara** (`politician`, former Prime Minister of Mali 2014–2015, chartered accountant, leader of Yéléma; Wikidata: `Q3326215`). Grade B (`open_letter`, 2023-09-05; the letter's own signature list, so a roster claim). Named Malian signatory on the international open letter calling on G20 Heads of State to enact wealth taxes on extreme wealth (`taxextremewealth.com/signatures`).
- **A0002: Clément Dembélé** (`politician` / `academic`, 2018 presidential candidate, university professor, president of the PCC; Wikidata: `Q96048074`). Grade A (`interview`, 2018-01-17). Explicit campaign platform proposal to establish an Impôt de Solidarité sur la Fortune (ISF) in Mali targeting mining assets, real estate, and financial bank holdings (`bamada.net`).

## 4. Legislatures and where their records are
- **Conseil National de la Transition (CNT):** Following the dissolution of the elected National Assembly in August 2020, legislative powers have been exercised by the Conseil National de la Transition (147 members presided over by Colonel Malick Diaw; `https://cnt.ml`). Plenary sessions and committee hearings are reported through the national press (*L'Essor*) and broadcast via ORTM. No bill, motion, or amendment proposing a net wealth tax has been introduced in the CNT.
- **Future bicameral parliament:** The new Constitution approved by referendum in June 2023 and promulgated in July 2023 establishes an Assemblée Nationale and a Sénat, which will be constituted following transition elections.

## 5. Parties
- Major political parties and platforms:
  - **Yéléma:** Led by former Prime Minister Moussa Mara; prioritizes fiscal transparency, regular personal asset declarations, and elimination of tax exemptions.
  - **Convergence patriotique pour le changement (CPM / Mali Ko):** Supported Clément Dembélé's 2018 presidential bid and ISF proposal.
  - **Solidarité Africaine pour la Démocratie et l'Indépendance (SADI):** Left-wing party led by Oumar Mariko; rhetoric focuses on rural peasants against urban political elites and multinational mining exploitation, but platform does not include a net wealth tax.
  - **Union pour la République et la Démocratie (URD)**, **ADEMA-PASJ**, **Rassemblement pour le Mali (RPM)**, and coalition platforms like **M5-RFP**.

## 6. Government below national level
- **Structure:** 19 administrative regions plus the District de Bamako (Admin 1), divided into 160 cercles / communes urbaines (Admin 2).
- **Taxation powers:** Local collectivités territoriales (cercles and communes) collect local development and market fees (taxe de développement régional et local - TDRL, taxe de voirie, patentes locales). They have no statutory authority to levy taxes on net wealth or capital.
- **Official source:** Sourced directly from the official administrative boundaries published by the Institut Géographique du Mali (IGM) via the OCHA Common Operational Datasets (COD-AB) under CC BY-IGO 3.0 (`data/ml/boundaries.json`).

## 7. Search terms
- French: `impôt sur la fortune`, `ISF`, `taxe sur les grandes fortunes`, `impôt sur le patrimoine`, `taxe Zucman`, `justice fiscale`, `imposition des riches`.
- Ambiguous phrases:
  - *Impôt sur le patrimoine* in WAEMU / UEMOA member states refers to real estate and property taxes (*impôt sur le patrimoine foncier* on built and unbuilt property), which are excluded under Section 2.
  - In religious commentary, *zakat* is occasionally referred to colloquially as "l'impôt sur la fortune", but is a religious pillar rather than statutory tax policy.
  - Bambara terms: *nisɔngɔ* (poll/capitation tax), *foroba nafolo* (public treasury/wealth).

## 8. Media
- Major national news portals and print media:
  - *L'Essor* (`https://lessor.ml`, national public daily)
  - *Maliweb.net* (`https://www.maliweb.net`)
  - *Malijet.com* (`https://malijet.com`)
  - *Bamada.net* (`https://bamada.net`)
  - *Le Républicain*, *L'Indépendant*, *Le Combat*

## 9. Registers
- Direction Générale des Impôts (DGI): `https://dgi.gouv.ml`
- Extractive Industries Transparency Initiative (ITIE-Mali): `https://itie.ml`
- Primature de la République du Mali: `https://www.primature.ml`

## 10. Key organizations and excluded actors
- 8 documented exclusions in `exclusions.csv`:
  - **Oumar Mariko (SADI):** Focuses on nationalization and anti-imperialism; no net wealth tax proposed (`X0001`).
  - **Gouvernement du Mali (Transition):** Mining code audits and bilateral tax treaty denunciation (`X0002`).
  - **PCQVP Mali:** Extractive transparency and EITI reporting (`X0003`).
  - **CAD-Mali:** Anti-debt and illicit financial flows advocacy (`X0004`).
  - **UNTM & CSTM:** Salary tax (ITS) reduction and basic goods purchasing power (`X0005`).
  - **Étienne Fakaba Sissoko:** Macroeconomic commentary on public finance (`X0006`).
  - **Aminata Dramane Traoré:** Structural adjustment and anti-imperialist critiques (`X0007`).
  - **Délégation du Mali à l'ONU:** Voted for UN tax convention resolution without wealth tax endorsement (`X0008`).

---

### Sources
1. Direction Générale des Impôts (DGI), *Code Général des Impôts du Mali*, `https://dgi.gouv.ml`.
2. Bamada.net, "Professeur Clément Mahamadou Dembélé, candidat a la présidentielle de 2018 : « Je veux incarner l’espoir des Maliens »", 17 January 2018, `https://bamada.net/professeur-clement-mahamadou-dembele-candidat-a-la-presidentielle-de-2018-je-veux-incarner-lespoir-des-maliens`.
3. Tax Extreme Wealth, "G20 Leaders must tax extreme wealth — Signatures", 5 September 2023, `https://taxextremewealth.com/signatures`.
4. Sika Finance, "Mali : Le gouvernement recouvre des centaines de milliards d'arriérés d'impôts miniers", `https://sikafinance.com/marches/mali-le-gouvernement-recouvre-des-centaines-de-milliards-darrieres-dimpots-miniers_44521`.
5. Ministère de l'Économie et des Finances, "Dénonciation de la convention fiscale bilatérale franco-malienne", `https://www.impots.gouv.fr`.

## Audit — R003
- Both quotes were found on their pages. Moussa Mara is regraded A to B because the only evidence is the campaign's signature list. A further search in French (opposition parties, unions, economists, Oxfam and tax-justice networks, Mara's own statements) found no other Malian supporter of a wealth tax; the signature list names only one Malian. Mara was sentenced in October 2025, so recent statements may be hard to find.
