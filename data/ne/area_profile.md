# Area profile — Niger

Save as `data/ne/area_profile.md`. Seed pass and follow-up discovery passes completed 2026-11-10 (`R001`, `R002`, `R003`, `R004`).

## 1. Scope
- Area: Niger; type: country (ISO 3166-1 alpha-2: `NE`)
- Depth: Seed pass (`R001`), wider discovery pass (`R002`), international/local sweep (`R003`), and civil society / economic debate deep dive (`R004`).
- Levels of government in scope: National (transitional authorities, Conseil National pour la Sauvegarde de la Patrie - CNSP, dissolved Assemblée Nationale), regional (8 regions: Agadez, Diffa, Dosso, Maradi, Niamey, Tahoua, Tillabéri, Zinder), departmental (67 départements), and local (266 communes loaded from official mapping data into `geo_units.csv`).
- Languages searched: French (`fr`), Hausa (`ha`), English (`en`)
- Dates of runs: 2026-11-10 (`R001`, `R002`, `R003`, `R004`)

## 2. Wealth tax history and live proposals (2010 onwards)
- **Absence of statutory net wealth tax:** Niger has never had an annual statutory tax on the stock of net wealth (*impôt sur la fortune* or *impôt de solidarité sur la fortune*). The tax system administered by the Direction Générale des Impôts (DGI) is governed by the General Tax Code (*Code Général des Impôts*) and relies primarily on indirect consumption taxes (TVA at 19%), corporate profit taxes (ISB / BIC at 30%), and personal income taxes on salaries (Impôt Unique sur les Traitements et Salaires - IUTS).
- **Civil society and the 2018 anti-Finance Law mobilization:** In late 2017 and 2018, the adoption of the 2018 Finance Law (Loi n° 2017-82) triggered massive public protests organized by civil society coalitions led by Ali Idrissa (ROTAB), Moussa Tchangari (Alternative Espaces Citoyens - AEC), Nouhou Arzika (MPCR), and Maïkoul Zodi (Tournons la Page Niger). The protests focused on abolishing regressive consumer and household levies (housing tax / *taxe d'habitation*, utility surcharges, and expanded informal sector taxes) while denouncing corporate tax exemptions granted to foreign telecoms and uranium miners (Areva/Orano). The coalition demanded fiscal fairness and state budget reductions, but did not propose a net wealth tax.
- **Academic and economic proposal on family net wealth:** During the broader national debate on tax reform in October 2017, prominent Nigerien development economist and former diplomat **Mamadou Kiari Liman-Tinguiri** published an op-ed in *Niger Inter* ("Débat/Niger : Faut-il réformer le système fiscal ?"). Explicitly citing Thomas Piketty (*Le Capital au XXIe siècle*), he proposed an *impôt direct universel* levied progressively on family net wealth (*patrimoine familial*), specifically targeting assets above the median with higher brackets on the top decile (the wealthiest 10%). This represents an explicit Grade A proposal for an annual net wealth tax in Niger.
- **Post-coup transitional fiscal policy and the FSSP (2023–present):** Following the July 2023 coup d'état that deposed President Mohamed Bazoum, the military administration led by General Abdourahamane Tiani (CNSP) created the *Fonds de Solidarité pour la Sauvegarde de la Patrie* (FSSP) via Ordonnance n° 2023-13. The fund is financed through a 1% mandatory monthly levy on net salaries, 1–2% corporate turnover levies on strategic enterprises, and luxury import duties. Under Section 2 of the skill rules, turnover taxes and payroll deductions are excluded from the wealth tax definition.
- **Bilateral tax treaty termination:** On 5 December 2023, the transitional governments of Niger and Mali jointly denounced their 1965/1972 bilateral double-taxation conventions with France, which terminated in 2024 to restore domestic taxing rights over technical assistance fees and royalties.
- **International and UN processes:** On 22 December 2023, Niger voted in favor of UN General Assembly Resolution 78/230 on international tax cooperation. Former Prime Minister Ibrahim Assane Mayaki co-chaired the UN FACTI Panel (2020–2021) on illicit financial flows and financial integrity, but the panel's final report advocated beneficial ownership registries and corporate tax minimums rather than an annual net wealth tax.
- **Regional AES dynamics:** While neighbouring Alliance des États du Sahel (AES) partner Burkina Faso engaged the African Tax Administration Forum (ATAF) to study wealth tax options (logged as external lead `L0042` in `data/leads.csv`), Niger's transitional administration and DGI have focused on extractive audits, state property inventory (DGPE), and confederal customs levies (0.5% import levy).

## 3. Identified supporters
- **Mamadou Kiari Liman-Tinguiri** (`A0001`): Development economist, President of WASDI (West African Strategic Development Institute), former UN official (UNDP, UNICEF), and former Niger Ambassador to the United States (2021–2023). In an op-ed titled "Débat/Niger : Faut-il réformer le système fiscal ?" in *Niger Inter* (19 October 2017), he explicitly proposed a progressive direct universal tax on family net wealth (*patrimoine familial*), taxing wealth above the median with a higher bracket for the top 10%, citing Thomas Piketty's work on capital and wealth taxation (Grade A, `E00001`).

## 4. Legislatures and where their records are
- **Assemblée Nationale du Niger (`https://www.assemblee.ne`):** The unicameral legislature (171 deputies elected in 2020–2021, previously presided over by Seini Oumarou) was dissolved following the coup d'état of 26 July 2023. Legislative power is currently exercised by executive decree/ordonnance of the CNSP. Historical parliamentary sessions and debates were reported via the official press agency (*Agence Nigérienne de Presse* - ANP) and the Journal Officiel.
- **Transition Consultative Bodies:** A national dialogue process (*Assises Nationales*) is planned to establish transitional guidelines and potential consultative or legislative councils.

## 5. Political parties and groupings
- **PNDS-Tarayya (Parti Nigérien pour la Démocratie et le Socialisme):** Ruling party under Presidents Mahamadou Issoufou (2011–2021) and Mohamed Bazoum (2021–2023). Programs focused on rural infrastructure, the "Renaissance" program, and broadening the tax base via cadastral modernization, but without wealth tax proposals.
- **MODEN/FA Lumana Africa:** Main historical opposition party led by former Prime Minister Hama Amadou (deceased October 2024).
- **MNSD-Nassara:** Former ruling party led by Seini Oumarou.
- **MPR-Jamhuriya / CPR-Inganci / RDR-Tchanji:** Other notable national political formations. All legislative activities are currently suspended.

## 6. Administrative divisions
- **National (`national`):** Country root (`G0001`), Assembly (`G0002`), Government (`G0003`).
- **Regions (`region`):** 8 administrative regions: Agadez (`G0004`), Diffa (`G0005`), Dosso (`G0006`), Maradi (`G0007`), Niamey (`G0008`), Tahoua (`G0009`), Tillabéri (`G0010`), Zinder (`G0011`).
- **Départements (`county`):** 67 deconcentrated administrative divisions (`G0012`–`G0078`).
- **Communes (`council`):** 266 decentralized municipal units (communes urbaines and communes rurales, `G0079`–`G0344`).

## 7. Tax terms and glossary
- *Impôt sur la fortune (ISF):* Wealth tax. Never enacted in Niger.
- *Impôt direct universel sur le patrimoine familial:* Proposed universal progressive direct tax on family net wealth above median assets (Kiari Liman-Tinguiri, 2017).
- *Impôt sur le patrimoine foncier / Taxe Foncière Unique (TFU):* Property tax on real estate (land and buildings). Excluded under Section 2.
- *Impôt Unique sur les Traitements et Salaires (IUTS / ITS):* Progressive income tax on employment earnings.
- *Impôt sur les Bénéfices Industriels et Commerciaux (BIC / ISB):* Corporate profit tax (standard rate 30%).
- *FSSP (Fonds de Solidarité pour la Sauvegarde de la Patrie):* Transitional solidarity levy (1% payroll deduction, turnover contributions). Excluded under Section 2.
- *Zakat:* Islamic religious duty (2.5% on qualifying wealth above Nisab). Often colloquially described as "l'impôt sur la fortune" in religious commentary, but is religious charity rather than statutory tax legislation.

## 8. Media
- National public and independent media:
  - *Le Sahel* (`https://lesahel.org`, national public daily)
  - *Agence Nigérienne de Presse* (ANP, `https://www.anp.ne`)
  - *ActuNiger* (`https://actuniger.com`)
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
- 16 documented exclusions in `exclusions.csv`:
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
  - **Ibrahim Assane Mayaki (UN FACTI Panel):** Co-chair of UN FACTI Panel; report focused on beneficial ownership transparency, tax havens, and corporate tax minimums (`X0011`).
  - **Oumarou Moumouni Dogari (Ville de Niamey):** Former Mayor of Niamey; municipal street maintenance taxes (*taxes de voirie*) and local market fees (`X0012`).
  - **Nouhou Arzika (MPCR):** Led anti-2018 budget demonstrations; focused on cost of living, opposition to regressive consumption taxes and telecom exemptions (`X0013`).
  - **Maïkoul Zodi (Tournons la Page Niger / ROTAB):** Mobilized against the 2018 budget regressive taxes; focused on multinational tax exemptions and basic social services (`X0014`).
  - **Moustapha Kadi Oumani (CODDAE):** Civil society consumer rights advocate; focused on civic tax duty and mining/energy revenues (`X0015`).
  - **Adamou Louché Ibrahim (Analyste Économique):** Economic analyst writing for Niger Inter; published analyses on the budget, public spending quality, and universal basic income; no wealth tax proposal (`X0016`).

## 11. Plan for the next runs
- **Run 5:**
  1. Periodic monitoring of transitional political consultations (*Assises Nationales*) and any newly convened transitional consultative or legislative bodies for fiscal proposals.
  2. Track AES (Alliance des États du Sahel) fiscal harmonization committees and communiqués.
  3. Review future Finance Ordinances and potential tax reforms promulgated by the CNSP administration.

---

### Sources
1. Direction Générale des Impôts du Niger, *Code Général des Impôts*, `https://dgi.gouv.ne`.
2. Assemblée Nationale du Niger, *Loi n° 2017-82 du 13 décembre 2017 portant loi de finances pour l'année budgétaire 2018*, `https://www.anp.ne`.
3. Kiari Liman-Tinguiri, "Débat/Niger : Faut-il réformer le système fiscal ?", *Niger Inter*, 19 October 2017, `https://nigerinter.com/2017/10/19/debatniger-faut-il-reformer-le-systeme-fiscal/`.
4. Les Échos du Niger, "Fiscalité et solidarité nationale : les nouveaux prélèvements du FSSP au Niger", 2025, `https://lesechosduniger.com`.
5. Sénat français, "Dénonciation de la convention fiscale bilatérale franco-nigérienne", Question écrite n° 09923, 2024, `https://www.senat.fr/questions/base/2024/qSEQ240109923.html`.
6. United Nations Digital Library, "Resolution 78/230: Promotion of inclusive and effective international tax cooperation at the United Nations", Voting record, 22 December 2023, `https://digitallibrary.un.org/record/4031649`.
7. ANP, "La CDTN alerte sur l'impact social de la loi de finances et appelle à la révision de l'ITS", `https://www.anp.ne`.
8. Niger Inter, "Interview croisée de Moussa Tchangari et Inoussa Saouna sur la loi de finances 2018", 27 October 2017, `https://nigerinter.com`.
9. Le Monde, "Au Niger, mort de l'ancien premier ministre Hama Amadou", 24 October 2024, `https://www.lemonde.fr/afrique/article/2024/10/24/au-niger-mort-de-l-ancien-premier-ministre-hama-amadou_6359051_3212.html`.
10. Le Sahel, "Comprendre la Zakat : Troisième pilier de l'Islam et justice sociale", `https://lesahel.org`.
11. L'Événement Niger, "CESOC : Dialogue public-privé sur les réformes fiscales et le civisme", `https://levenementniger.com`.
12. UN FACTI Panel, *Financial Integrity for Sustainable Development*, February 2021, `https://factipanel.org`.
13. Anadolu Agency, "Niger: arrestation d'un acteur de la société civile opposé à la loi de finances", `https://www.aa.com.tr`.
14. Secours Catholique, "Niger : la loi de finances 2018 alourdit la pression fiscale sur les plus pauvres", `https://www.secours-catholique.org`.
