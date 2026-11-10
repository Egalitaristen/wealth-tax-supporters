# Area profile — Paraguay

## 1. Scope
- Area: Paraguay; type: country (ISO 3166-1 alpha-2: PY, alpha-3: PRY)
- Depth: Seed and legislative deep dive (prominent supporters in every layer at national level; comprehensive roll-call and bill-sponsorship extraction; geography loaded down to local tier; plan for next runs)
- Levels of government in scope: National (Congreso Nacional: Cámara de Senadores and Cámara de Diputados; Corte Suprema de Justicia; Executive); regional (17 departamentos and Capital District Asunción) and local (263 distritos / municipios in `geo_units.csv` and `boundaries.json`). Regional and local levels were sampled and not individually swept as subnational units lack tax powers.
- Languages to search in: Spanish (`es`), Guaraní (`gn`)
- Runs completed: R001 (2026-11-10, seed pass), R002 (2026-11-10, legislative roll-call and sponsor deep dive), R003 (2026-11-10, civil society coalitions, CODEHUPY, think tanks, and local tier competence audit), R004 (2026-11-10, complete roll-call extraction for Senate Tasa Covid bill with all 16 affirmative votes, business federation exclusions, and faith sector review)

## 2. Wealth tax history and live proposals (2010 onwards)
- **Existing tax background:** Paraguay has never enacted a recurrent general net wealth tax or inheritance tax. The tax system relies predominantly on consumption taxes (IVA ~50% of tax revenue) and flat 10% rates (the "10-10-10" model: IRE, IRP, IVA). Real estate is subject to municipal property tax (*impuesto inmobiliario*), which is low and distinct from net wealth.
- **2020 — "Tasa Covid" on large fortunes (Expediente S-209389 / 120551):** On 23 April 2020, during the COVID-19 emergency, the left-wing coalition Frente Guasu (senators Carlos Filizzola, Esperanza Martínez, Fernando Lugo, Hugo Richer, Jorge Querey, Miguel Fulgencio Rodríguez, and Sixto Pereira) presented a bill creating a temporary annual 1% to 2% levy on net fortunes exceeding 30,000 minimum wages (approx. USD 10 million, affecting roughly 90 economic groups or families) to fund emergency healthcare and social support without increasing public debt ([SILPy Expediente 120551](https://silpy.congreso.gov.py/expediente/120551), [Última Hora](https://www.ultimahora.com/frente-guasu-critica-que-haya-consenso-senado-no-tratar-nuevos-impuestos-n2881651)). On 5 May 2020, the Cámara de Senadores voted on the bill in a nominal roll call ([Votación 102482](https://silpy.congreso.gov.py/web/votacion/102482)), which was rejected and archived (16 votes in favour, 20 against, 3 abstentions, 6 absent).
- **2021 — "Tasa extraordinaria a las grandes fortunas" (Emergencia Educativa, Expediente 123524):** In May 2021, teachers union OTEP-SN alongside senators Hugo Richer (FG), Pedro Santa Cruz (PDP), and Víctor Ríos (PLRA) presented a bill declaring an educational emergency for 3 years, funded by an extraordinary wealth tax of 1% to 5% on net assets exceeding 30,000 minimum wages (approx. USD 10 million) to raise USD 400 million for public schools ([ABC Color](https://www.abc.com.py/nacionales/2021/05/12/presentan-proyecto-de-ley-que-declara-emergencia-educativa-y-crea-tasa-extraordinaria-a-las-grandes-fortunas/), [Última Hora](https://www.ultimahora.com/presentan-ley-emergencia-educativa-n2940644)). On 30 June 2021, the Cámara de Diputados voted to reject and archive the initiative ([Última Hora](https://www.ultimahora.com/impuesto-las-grandes-fortunas-fue-rechazado-diputados-n2948629), [La Nación](https://www.lanacion.com.py/politica/2021/06/30/diputados-mandan-al-archivo-propuesta-de-crear-impuesto-a-la-riqueza/)), with deputy Kattya González (PEN) vigorously defending the proposal.
- **2024–2025 — Regional and Mercosur debate:** Parlasur adopted Declaración 10/2025 supporting international tax cooperation towards a global minimum tax on large fortunes ([Parlasur](https://sapl.parlamentomercosur.org/media/sapl/public/normajuridica/2025/769/declaracion_102025.pdf)).

## 3. Legislatures and where their records are
- **Congreso Nacional de Paraguay:** Bicameral legislature.
  - **Cámara de Senadores:** 45 senators elected in a single nationwide constituency. Records at [senado.gov.py](https://www.senado.gov.py).
  - **Cámara de Diputados:** 80 deputies elected by department. Records at [diputados.gov.py](https://www.diputados.gov.py).
  - **Sistema de Información Legislativa (SILpy):** [silpy.congreso.gov.py](https://silpy.congreso.gov.py) / [ods.congreso.gov.py](https://ods.congreso.gov.py). Both core wealth tax bills have complete technical files and vote registries:
    - 2020 Tasa Covid: [Expediente 120551](https://silpy.congreso.gov.py/expediente/120551), [Votación 102482](https://silpy.congreso.gov.py/web/votacion/102482).
    - 2021 Emergencia Educativa: [Expediente 123524](https://ods.congreso.gov.py/expedientes/123524).
  - Plenary minutes and debates are published in daily session records (*Diario de Sesiones*).

## 4. Parties
- **Frente Guasu (FG):** Coalition of left-wing parties (Tekojoja, País Solidario, Convergencia Popular Socialista, Participación Ciudadana). Primary champion of wealth taxation in Paraguay since 2010; all 7 senators co-sponsored the 2020 Tasa Covid bill.
- **Partido Democrático Progresista (PDP):** Centre-left opposition party. Supported wealth taxation (Pedro Santa Cruz co-sponsored the 2021 bill; Desirée Masi advocated wealth taxes in Senate debate).
- **Partido Encuentro Nacional (PEN):** Centre-left / social-democratic party. Represented by Kattya González who defended the wealth tax in the 2021 plenary debate.
- **Partido Liberal Radical Auténtico (PLRA):** Main opposition party; factionally divided. Progressive wing (Víctor Ríos) co-sponsored the wealth tax; conservative llanista faction (Blas Llano, Hermelinda Alvarenga) opposed it.
- **Asociación Nacional Republicana (ANR / Partido Colorado):** Ruling conservative party; officially and firmly opposes wealth taxation (party leadership, President Mario Abdo, and key senators Silvio Ovelar, Enrique Bacchetta, and Juan Carlos Galaverna actively opposed).
- **Partido Patria Querida (PPQ):** Conservative/liberal party; opposes wealth taxation (Stephan Rasmussen and Fidel Zavala voted against and spoke against in plenary).

## 5. Government below national level
- **Structure:** 17 departamentos + 1 Distrito Capital (Asunción) at the regional level. Below departments: 263 distritos (municipios) governed by *intendencias* and *juntas municipales*.
- **Taxation powers:** Subnational levels cannot introduce income or net wealth taxes (Art. 170 and 179 of the National Constitution). Municipalities levy local real estate property taxes (*impuesto inmobiliario*) and municipal fees (*patentes* and *tasas*) strictly delimited by Ley Orgánica Municipal N° 3966/2010. All calls for net wealth taxation are addressed exclusively to the national Congreso.
- **Official geography sources:** DGEEC / Instituto Nacional de Estadística (INE) via OCHA HDX COD-AB Paraguay (CC BY-IGO). The register covers all 18 regions and 263 distritos.
- **Local decision:** National actions sampled; local municipal records in Asunción and Central departments were sampled during 2020–2021. Municipal responses were strictly restricted to fee waivers (*exoneración de recargos*), patent extensions, and emergency soup kitchens (*ollas populares*). Local units were not swept individually as subnational councils lack tax competency and no local wealth tax motions have been identified to date (SKILL.md 6.5).

## 6. Search terms
- Spanish: `"impuesto a la riqueza"`, `"impuesto a las grandes fortunas"`, `"impuesto al patrimonio"`, `"tasa extraordinaria a las grandes fortunas"`, `"tasa covid"`, `"aporte solidario"`, `"emergencia educativa"`, `"justicia fiscal"`
- Guaraní: `"mba'ereta rehegua impuesto"` / `"viru rehegua"` (used in informal indigenous and campesino statements, but official legislative bills and major press publish exclusively in Spanish).
- Ambiguous terms to watch: `"impuesto inmobiliario"` (property tax, excluded), `"impuesto a la renta personal"` (income tax, excluded), `"impuesto a la soja"` (commodity export tax, excluded).

## 7. Media
- National dailies with active editorial and opinion sections:
  - **Última Hora** ([ultimahora.com](https://www.ultimahora.com)): extensive objective reporting on wealth tax bills and full op-eds.
  - **ABC Color** ([abc.com.py](https://www.abc.com.py)): leading national daily; detailed legislative coverage, bill sponsorships, and business reaction.
  - **La Nación** ([lanacion.com.py](https://www.lanacion.com.py)): conservative daily, tracks congressional voting and business statements.
  - **Revista PLUS** ([revistaplus.com.py](https://www.revistaplus.com.py)): financial and economic news.
  - **LatFem** ([latfem.org](https://latfem.org)): published op-ed by Paraguayan economist Verónica Serafini on wealth tax and gender equity.

## 8. Registers
- Dirección Nacional de Ingresos Tributarios (DNIT / former SET): [dnit.gov.py](https://www.dnit.gov.py)
- Contraloría General de la República (asset declarations of public officials): [contraloria.gov.py](https://www.contraloria.gov.py)

## 9. Known networks
- **CODEHUPY (Coordinadora de Derechos Humanos del Paraguay):** Leading national human rights coalition of 35 civil society and popular organisations; publishes annual national human rights reports and officially advocates progressive wealth taxation to fund basic social rights. Led by Executive Secretary Óscar Ayala Amarilla (2018–2022).
- **OTEP-SN (Organización de Trabajadores de la Educación del Paraguay - Sindicato Nacional):** Core union proponent of the 2021 wealth tax bill.
- **Decidamos (Campaña por la Expresión Ciudadana):** Prominent Paraguayan tax justice NGO, national affiliate of Latindadd.
- **Latindadd (Red Latinoamericana por Justicia Económica y Social):** Regional network active in Paraguay.
- **CADEP (Centro de Análisis y Difusión de la Economía Paraguaya):** Economic research center where progressive tax economists (e.g. Verónica Serafini) publish.

## 10. Saturation and maintenance
- **Status:** Full saturation achieved at the national level. All 16 affirmative votes on the 2020 Tasa Covid wealth tax roll call (Votación 102482) are verified and registered in the database, along with all 2021 Emergencia Educativa bill sponsors, union leaders, tax justice NGOs (Decidamos, CODEHUPY), and prominent progressive economists.
- **Maintenance / Next:**
  - Periodically monitor the 2023–2028 Congreso Nacional for newly introduced wealth tax or fiscal justice bills in the SILpy portal.
  - Track upcoming publications and tax justice campaigns by Latindadd, Decidamos, and CODEHUPY in Asunción.
