# Area profile — Niger

Save as `data/ne/area_profile.md`. Seed pass and wider discovery pass completed 2026-11-10 (`R001`, `R002`).

## 1. Scope
- Area: Niger; type: country (ISO 3166-1 alpha-2: `NE`)
- Depth: Seed pass (`R001`) and wider discovery pass (`R002`)
- Levels of government in scope: National (transitional authorities, Conseil National pour la Sauvegarde de la Patrie - CNSP, dissolved Assemblée Nationale), regional (8 regions: Agadez, Diffa, Dosso, Maradi, Niamey, Tahoua, Tillabéri, Zinder), departmental (67 départements), and local (266 communes loaded from official mapping data into `geo_units.csv`).
- Languages searched: French (`fr`), Hausa (`ha`), English (`en`)
- Dates of runs: 2026-11-10 (`R001`, `R002`)

## 2. Wealth tax history and live proposals (2010 onwards)
- **Absence of statutory net wealth tax:** Niger has never had an annual tax on the stock of net wealth (*impôt sur la fortune* or *impôt de solidarité sur la fortune*). The tax system administered by the Direction Générale des Impôts (DGI) is governed by the General Tax Code (*Code Général des Impôts*) and relies primarily on indirect consumption taxes (TVA at 19%), corporate profit taxes (ISB / BIC at 30%), and personal income taxes on salaries (Impôt Unique sur les Traitements et Salaires - IUTS).
- **Resource sovereignty and mining fiscal disputes:** Fiscal politics in Niger historically center on the extractive sector, particularly uranium exploitation in the Agadez region (Arlit, Imouraren) and oil production (Agadem basin, Niger-Benin pipeline). Civil society (ROTAB, PCQVP) and governments have engaged in prolonged negotiations with French multinational Areva/Orano over mining royalties, tax exemptions, and customs duties.
- **2018 anti-Finance Law movement:** In late 2017 and 2018, the adoption of the 2018 Finance Law (Loi n° 2017-82) triggered massive public protests organized by civil society coalitions led by Ali Idrissa (ROTAB) and Moussa Tchangari (AEC). The protests opposed regressive fiscal measures, including housing taxes, utility levies, and an expanded synthetic tax, arguing they burdened the poor while foreign mining corporations enjoyed exemptions. No net wealth tax was proposed.
- **Post-coup transitional fiscal policy and the FSSP (2023–present):** Following the July 2023 coup d'état that deposed President Mohamed Bazoum, the military administration led by General Abdourahamane Tiani (CNSP) created the *Fonds de Solidarité pour la Sauvegarde de la Patrie* (FSSP) via Ordonnance n° 2023-13. The fund is financed through a 1% mandatory monthly levy on net salaries, 1–2% corporate turnover levies on strategic enterprises, and luxury import duties. Under Section 2, turnover taxes and payroll deductions are excluded from the wealth tax definition.
- **Bilateral tax treaty termination:** On 5 December 2023, the transitional governments of Niger and Mali jointly denounced their 1965/1972 bilateral double-taxation conventions with France, which terminated in 2024 to restore domestic taxing rights over technical assistance fees and royalties.
- **International and UN processes:** On 22 December 2023, Niger voted in favor of UN General Assembly Resolution 78/230 on international tax cooperation. No domestic politician, economist, or civil society leader from Niger has been identified as a signatory to international wealth tax appeals (e.g. G20 billionaire-tax letters, Patriotic Millionaires, Proud to Pay More).
- **Regional AES dynamics:** While neighbouring Alliance des États du Sahel (AES) partner Burkina Faso engaged the African Tax Administration Forum (ATAF) to study wealth tax options (logged as external lead `L0042`), Niger's transitional administration and DGI have focused on extractive audits, state property inventory (DGPE), and confederal customs levies (0.5% import levy).

## 3. Identified supporters
- No named domestic supporter of an actual wealth tax has been identified to date across national, regional, or local layers.

## 4. Legislatures and where their records are
- **Assemblée Nationale du Niger (`https://www.assemblee.ne`):** The unicameral legislature (171 deputies elected in 2020–2021, previously presided over by Seini Oumarou) was dissolved following the coup d'état of 26 July 2023. Legislative power is currently exercised by executive decree/ordonnance of the CNSP. Historical parliamentary sessions and debates were reported via the official press agency (*Agence Nigérienne de Presse* - ANP) and the national daily (*Le Sahel*). No bill or motion proposing an *impôt sur la fortune* was introduced between 2010 and 2023.
- **Future consultative bodies:** National consultations (*Assises Nationales*) have been planned to determine the transitional charter and future legislative assemblies.

## 5. Parties
- Major political parties and their fiscal stances:
  - **PNDS-Tarayya (Parti Nigérien pour la Démocratie et le Socialisme):** Ruling party from 2011 to 2023 under Presidents Mahamadou Issoufou and Mohamed Bazoum; member of the Socialist International. Emphasized agrarian development, public school infrastructure, and hydrocarbon industrialisation; introduced the Taxe Foncière Unique (TFU) on real property but no net wealth tax.
  - **MODEN/FA Lumana Africa:** Led by former Prime Minister Hama Amadou (deceased October 2024); main opposition platform; focused on governance, anti-corruption, and institutional reforms without wealth tax proposals.
  - **MNSD-Nassara:** Led by Seini Oumarou (former President of the National Assembly); centrist agrarian platform.
  - **MPN Kiishin Kassa:** Led by Ibrahim Yacouba; populist governance platform.
  - **CDS-Rahama:** Historic party of former President Mahamane Ousmane; liberal-democratic orientation.

## 6. Government below national level
- **Structure:** Niger has 8 administrative regions (Admin 1: Agadez, Diffa, Dosso, Maradi, Niamey, Tahoua, Tillabéri, Zinder), subdivided into 67 départements (Admin 2) and 266 communes (Admin 3: communes urbaines and communes rurales).
- **Taxation powers:** Under territorial decentralisation (Loi N° 2001-023), regions and communes levy local development taxes (taxe de voirie, patentes locales, taxe régionale de développement). They possess no statutory power to institute a net wealth tax.
- **Official source:** Sourced from the official administrative boundaries published by the Direction des Statistiques Démographiques et Sociales / Institut National de la Statistique (INS) via OCHA Common Operational Datasets (COD-AB) on HDX under CC BY-IGO 3.0 (`data/ne/boundaries.json`).

## 7. Search terms
- French: `impôt sur la fortune`, `ISF`, `taxe sur les grandes fortunes`, `impôt sur le patrimoine`, `taxe Zucman`, `justice fiscale`, `imposition des riches`.
- Hausa: `harajin dukiya` (wealth tax), `haraji a kan masu kudi` (tax on the rich), `harajin masu arziki`.
- Ambiguous terms to watch:
  - *Impôt sur le patrimoine* in WAEMU / UEMOA member states refers to real estate taxes (*Taxe Foncière Unique* - TFU on built and unbuilt property), which are excluded under Section 2.
  - In Niger press (*Le Sahel*), the acronym *ISF* refers to *Internationale Socialiste des Femmes* or *Indice Synthétique de Fécondité* (total fertility rate).
  - *Zakat* in Islamic jurisprudence is sometimes translated as "l'impôt sur la fortune" in religious commentary, but is religious charity rather than statutory tax legislation.

## 8. Media
- National public and independent media:
  - *Le Sahel* (`https://lesahel.org`, national public daily)
  - *Agence Nigérienne de Presse* (ANP, `https://www.anp.ne`)
  - *Aniamey.com* (`https://www.aniamey.com`)
  - *Air Info Agadez* (`https://airinfoagadez.com`)
  - *Les Échos du Niger* (`https://lesechosduniger.com`)
  - *Niger Inter* (`https://nigerinter.com`)
  - *Groupe Labari* (private television and radio founded by Ali Idrissa)

## 9. Registers
- Direction Générale des Impôts (DGI): `https://dgi.gouv.ne`
- Institut National de la Statistique du Niger (INS): `https://www.stat-niger.org`
- Présidence de la République du Niger: `https://www.presidence.ne`

## 10. Key organizations and excluded actors
- 10 documented exclusions in `exclusions.csv`:
  - **Délégation du Niger à l'ONU:** Voted Yes on UN General Assembly Resolution 78/230 on international tax cooperation without wealth tax endorsement (`X0001`).
  - **Ali Idrissa (ROTAB / PCQVP):** Anti-Finance Law 2018 mobilization and extractive transparency without net wealth tax (`X0002`).
  - **Moussa Tchangari (AEC):** Civil society critiques of fiscal austerity and indirect consumer taxes (`X0003`).
  - **CNSP / Gouvernement de Transition (FSSP):** 1% salary deductions and turnover contributions for national security fund (`X0004`).
  - **Gouvernement du Niger (Convention fiscale):** Denunciation of 1965/1972 bilateral tax treaty with France (`X0005`).
  - **CDTN / Idrissa Djibrilla:** Trade union advocacy for salary tax (ITS) cuts and mobile money tax opposition (`X0006`).
  - **PNDS-Tarayya:** Land property tax modernizations without net wealth tax (`X0007`).
  - **Hama Amadou (MODEN/FA Lumana):** Former Prime Minister and opposition leader; deceased October 2024 (`X0008`).
  - **Association Islamique du Niger (AIN) / Conseil Islamique du Niger:** Religious guidance on Zakat (2.5% religious charity above Nisab) rather than statutory wealth taxation (`X0009`).
  - **Conseil Économique, Social et Culturel (CESOC):** Advisory body focusing on tax compliance (civisme fiscal) and electronic certified invoicing (`X0010`).

## 11. Plan for the next runs
- **Run 3:**
  1. Monitor transitional political consultations (*Assises Nationales*) and any newly convened transitional consultative or legislative bodies for fiscal and wealth-related proposals.
  2. Track AES (Alliance des États du Sahel) fiscal harmonization committees and communiqués.
  3. Review future Finance Ordinances and potential tax reforms promulgated by the CNSP administration.

---

### Sources
1. Direction Générale des Impôts du Niger, *Code Général des Impôts*, `https://dgi.gouv.ne`.
2. Assemblée Nationale du Niger, *Loi n° 2017-82 du 13 décembre 2017 portant loi de finances pour l'année budgétaire 2018*, `https://www.anp.ne`.
3. Les Échos du Niger, "Fiscalité et solidarité nationale : les nouveaux prélèvements du FSSP au Niger", 2025, `https://lesechosduniger.com`.
4. Sénat français, "Dénonciation de la convention fiscale bilatérale franco-nigérienne", Question écrite n° 09923, 2024, `https://www.senat.fr/questions/base/2024/qSEQ240109923.html`.
5. United Nations Digital Library, "Resolution 78/230: Promotion of inclusive and effective international tax cooperation at the United Nations", Voting record, 22 December 2023, `https://digitallibrary.un.org/record/4031649`.
6. ANP, "La CDTN alerte sur l'impact social de la loi de finances et appelle à la révision de l'ITS", `https://www.anp.ne`.
7. Niger Inter, "Interview croisée de Moussa Tchangari et Inoussa Saouna sur la loi de finances 2018", 27 October 2017, `https://nigerinter.com`.
8. Le Monde, "Au Niger, mort de l'ancien premier ministre Hama Amadou", 24 October 2024, `https://www.lemonde.fr/afrique/article/2024/10/24/au-niger-mort-de-l-ancien-premier-ministre-hama-amadou_6359051_3212.html`.
9. Le Sahel, "Comprendre la Zakat : Troisième pilier de l'Islam et justice sociale", `https://lesahel.org`.
10. L'Événement Niger, "CESOC : Dialogue public-privé sur les réformes fiscales et le civisme", `https://levenementniger.com`.
