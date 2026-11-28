# Area profile — Panama

Seed pass of 2026-11-03 (run R001). Every line has a source; lines marked `[verify]` come from a search summary only.

## 1. Scope
- Area: Panama; type: country
- Depth: Seed, national level only. No regional or local sweep.
- Register: the 13 first-level areas (10 provincias and 3 comarcas indígenas with provincial status) and the 76 distritos (municipios) as the local tier. The 594 corregimientos are not loaded.
- Languages searched: Spanish and English.
- Map: [OCHA / HDX COD-AB Panama](https://data.humdata.org/dataset/cod-ab-pan) (valid 2021-10-20, from the Instituto Nacional de Estadística y Censo), CC BY-IGO; codes are the OCHA P-codes (province `PA01` to `PA13`, district `PA0101` and so on).

## 2. Wealth tax history and live proposals (2010 onwards)
- **Headline finding: no Panamanian deputy, party, union, church body or business figure was found on the record for an actual wealth tax; the only Panamanian voice is one economist-columnist (grade B).** Forty-seven searches in Spanish and English over five passes (see `queries.csv`) returned only Argentine, Chilean, Spanish and Colombian material, or other Panamanian tax stories. This says what web search reaches, not that nobody has ever proposed one: the Assembly's bill search could not be opened (asamblea.gob.pa timed out, the Legispan root answers 403 to scripts, not bypassed), so bills were searched only through Legispan PDFs and news that search engines index.
- **No net-wealth tax is in force.** Panama has a property tax (impuesto de inmuebles, Ley 66 of 2017) and no tax on total net wealth; a law-firm guide says so ([Morgan & Morgan](https://morimor.com/es/private-wealth-2023-panama/)) `[verify: search summary only]`. The property tax is out of definition and is not listed as a resource.
- **2025 social-security reform.** Ley 462 of 18 March 2025 changed contributions, pensions and governance of the Caja de Seguro Social; President Mulino said it raised no taxes ([MEF](https://www.mef.gob.pa/2025/03/presidente-mulino-sanciona-nueva-ley-de-la-css/)). No wealth-tax proposal was found in that debate.
- **2026 tax reform.** Ley 526 (Proyecto 641, approved 70 to 0 in the third debate, in force from fiscal 2027) sets a 15% tax on multinational entities without economic substance, to leave the EU list of non-cooperative jurisdictions ([Lac Group](https://www.lacgrp.com/ley-526-sustancia-economica-panama-2026/)). A corporate tax, out of definition.
- **Income-tax bill.** An independent deputy, José Antonio Pérez Barboni, filed an anteproyecto in 2025 that raises the exempt income threshold and sets higher bands for high incomes ([La Estrella](https://www.laestrella.com.pa/panama/politica/diputados-buscan-cortar-privilegios-fiscales-a-los-partidos-JD16730933)). An income tax, so he is an exclusion.
- **International.** Oxfam's regional report of March 2025 recommends a 2.5% to 5% tax on net wealth above USD 5 million for Central America and studies Panama among the six countries; it is the only qualifying item and gives Panama no figure of its own ([report](https://lac.oxfam.org/wp-content/uploads/2025/03/Informe-Mas-recursos-para-mas-derechos-Oxfam.pdf), [EFE via Infobae](https://www.infobae.com/america/agencias/2025/03/27/oxfam-propone-impuesto-a-grandes-fortunas-para-reducir-desigualdad-en-centroamerica/)).
- **CSS reform debate (Ley 462 of 2025, earlier Bill 163 of 2024).** SUNTRACS, CONUSI and Frenadeso opposed the reform and its retirement-age and contribution changes; deputies of Realizando Metas and the mixed bench proposed higher taxes on banking services ([Panamá América](https://www.panamaamerica.com.pa/sociedad/reformas-la-css-abundantes-propuestas-poca-evolucion-1243808)). The Universidad de Panamá's official proposal rests on cutting evasion, fund returns and formalisation ([La Universidad](https://launiversidad.up.ac.pa/node/4281)). None asks for a tax on wealth. One student representative said in a university interview that the reform should include taxes on grandes fortunas ([La Universidad, 14 Jan 2025](https://launiversidad.up.ac.pa/node/4357)); a student is not recorded (exclusion).
- **International letters and tax-justice networks.** The Latindadd 2021 paper and the 2020 summary on wealth taxes in Latin America name Panama only in a country list; no Panamanian signer of the G20 billionaire-tax, Millionaires for Humanity or Club de Madrid letters was found.
- **Opinion writing (R004).** Eduardo L. Lamphrey R., an economist writing in La Estrella, proposes taxing the largest assets ("si se gravara el 5% de los mayores activos a la tasa del 5%") as the way to reverse concentration ([column, 9 Oct 2023](https://www.laestrella.com.pa/opinion/columnistas/distribuir-equitativamente-riquezas-KELE499535)). Recorded at grade B: no wealth tax is named and the figure is a global one. His later column on growth and development argues the rich pay less tax than the middle class and calls for regulating the distribution of wealth, with no tax proposal.
- **Regional bodies.** Press reports list Panama among the countries of the Plataforma Tributaria de América Latina y el Caribe, whose May 2024 declaration backed Brazil's G20 billionaire-tax proposal ([El Destape](https://www.eldestapeweb.com/internacionales/america-latina/impuesto-a-los-super-ricos-fuerte-apoyo-en-america-latina-a-la-propuesta-de-brasil-20245719540)); the platform's own communiqué does not list who signed, so it is an exclusion and an open lead, not a row. No Panamanian organisation was found among the Red de Justicia Fiscal's or the platform's civil-society members.
- **Polls:** no Panamanian poll on taxing the rich or wealth (CIEPS, Ipsos, Dichter & Neira searched).
- **Opposition (not recorded):** a Panamá América columnist opposed a billionaire tax in 2019 ([column](https://www.panamaamerica.com.pa/opinion/cierto-zuckerberg-pero-eres-incoherente-1146827)); the government's 2026 reform targets companies only.

## 3. Legislature
- **Bill scan (R003):** Fundación Espacio Cívico mirrors the Assembly's register and serves it through its own public JSON ([Buscador de Leyes](https://espaciocivico.org/proyectos)). I read all 834 bills filed since 2 July 2024 (2024: 218, 2025: 345, 2026: 271 up to August) and scanned the titles for patrimonio, riqueza, fortunas, millonarios, solidario and any tax wording. **None proposes a wealth tax.** The tax bills are the 2026 economic-substance law, the 2025 income-tax anteproyecto of Pérez Barboni, Código Fiscal and ITBMS changes, short-stay lodging and budgets. The 2019-2024 term is not in the mirror and was not checked. The site rate-limited the first, faster attempt (HTTP 429); the second ran with pauses.
- Asamblea Nacional (71 deputies, single chamber): bills and minutes on [asamblea.gob.pa](https://www.asamblea.gob.pa) and the Legispan store (`s3-legispan.asamblea.gob.pa`); the minutes are PDFs. The Legispan bill search was not run. The member list was not read, so no seat chart and no positions.
- Parties and blocs seen in coverage: Vamos (Janine Prado heads the bench), Movimiento Otro Camino (MOCA), independents (Pérez Barboni), PRD, Panameñista. None was found with a wealth-tax programme or bill.

## 4. Parties
- Programmes since 2010 were not read. Searches for a wealth-tax plank in the Frente Amplio por la Democracia, Movimiento Otro Camino or Partido Panameñista found nothing.

## 5. Government below national level
- 10 provincias, 3 comarcas indígenas with provincial status, 76 distritos with an alcalde and a concejo municipal. They have no power over a wealth tax. Not sampled.

## 6. Search terms
- impuesto a la riqueza; impuesto al patrimonio; impuesto a las grandes fortunas; impuesto a los millonarios; impuesto a los súper ricos; gravar las grandes fortunas. Watch for the property tax (impuesto de inmuebles), tax exemptions (exoneraciones), the Ley 526 substance tax and the OECD global minimum tax, all out of definition.

## 7. Media
- La Prensa (prensa.com), La Estrella de Panamá, Panamá América, TVN, Telemetro, Metro Libre, Crítica, Eco TV. Opinion sections not systematically read.

## 9. Known networks
- Unions and popular fronts: CONATO, CONUSI, Frenadeso, SUNTRACS, the Asociación de Educadores Veragüenses, Alianza Pueblo Unido por la Vida. Demands found for the Alianza (profit margins, evasion, education budget) are not wealth taxes ([SELVIHP](https://selvihp.org/alianza-pueblo-unido-por-la-vida/)). Their own sites were not read.
- Tax-justice networks: Oxfam, Latindadd, Plataforma Tributaria LAC, ICRICT.
- Church: Archbishop José Domingo Ulloa speaks on corruption and inequality; no statement on taxing wealth was found.

## 10. Plan for the next runs
1. Search the Asamblea Nacional bill register (Legispan) in a browser for anteproyectos with patrimonio, riqueza or fortunas since 2019. Highest yield; web search cannot reach it.
2. Read the own sites and pliegos of CONUSI, Frenadeso, CONATO, SUNTRACS and the teachers' associations.
3. Identify Panamanian partners of Latindadd and the Plataforma Tributaria LAC.
4. The El Socialista Centroamericano piece (the site answers 403; try an archive copy).
5. Watch the 2027 budget and any follow-up to Ley 526.

## 11. Directions tried and their yield
| Direction | Yield |
|---|---|
| Web search on deputies, parties, unions, church, economists (R001) | nothing |
| Legispan PDFs and news via search, asamblea.gob.pa directly (R002) | site blocked or timed out; nothing |
| CSS-reform debate 2024-25, Universidad de Panamá (R002) | opposition to Ley 163, no wealth tax; one student remark, excluded |
| International letters, Latindadd and tax-justice papers (R002) | Panama only in a country list |
| Press archives by outlet, deputies' X posts, Parlatino (R003) | nothing; search returns other countries |
| Marco Gandásegui h. and CELA (R003) | columns on tax cuts for the rich, not a wealth tax |
| Espacio Cívico bill mirror, 834 bills since July 2024 (R003) | clean negative for the current Assembly |
| Oxfam Central America report (R001) | a regional supporter |
| Opinion columns, tax-justice networks, polls and papers (R004) | one columnist (Lamphrey, grade B); no poll; Panama only named as a platform country |
| Register, leads, UN and EU files (R005) | no Panamanian actor or lead anywhere else |
| Wikidata list of 99 living Panamanian economists, academics and politicians, ten checked (R005) | none calls for a wealth tax: Gordón (regressive-tax critique), Jované, Bernal, Méndez, Arrocha, Mirones, Lombana, Vásquez, Silva, Navarro |
| Other La Estrella columnists, CLACSO, CELAG and Oxfam LAC partners (R005) | evasion and progressive-tax columns only; no Panamanian signer or partner |

## 12. Searched, nothing found
- Wealth-tax statements by: Asamblea deputies (Prado, Cedeño, Richards, Vega, Pérez Barboni), President Mulino, the Universidad de Panamá, the Catholic Church, Alianza Pueblo Unido por la Vida, CONATO, CONUSI, Frenadeso, SUNTRACS. No Panamanian signatory of an international letter (G20 billionaire tax) was found.
- The one evidence row was checked by script (quote found in the report PDF). It has no archive copy: the Wayback upload was not run.
