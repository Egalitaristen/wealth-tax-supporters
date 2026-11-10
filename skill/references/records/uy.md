# Uruguay: where the official record is and how to read it

Written in run R004 (2026-11-09) by reading the official records of the Parlamento del Uruguay (Cámara de Senadores, Cámara de Representantes, Asamblea General) and IMPO from 2010 to November 2026. Every URL and method below was tested on that date; failures and access quirks are documented.

## 1. Bills, motions and proposals

**Official parliamentary portal:** `https://parlamento.gub.uy`
- Advanced search: `https://parlamento.gub.uy/documentosyleyes/busquedaAvanzada` (GET form submitting to `/documentosyleyes/busqueda-documentos`).
- Document listing: `https://parlamento.gub.uy/documentosyleyes/busqueda-documentos?Searchtext={TERM}&Searchcuerpos[0]=All&vista_origen=avanzada`
- Category checkboxes:
  - `Chkasuntosparlamento=1` (Asuntos del Parlamento: bill files and legislative initiatives)
  - `Chkdistri=1` (Distribuidos de Comisiones: committee prints, bill texts, and reports)
  - `Chkdiariosesiones=1` (Diarios de Sesiones: verbatim plenary records)
  - `Chkvtcomisiones=1` (Versiones Taquigráficas de Comisiones: committee debate transcripts)
  - `Chkleyes=1` (Promulgated laws)
- Direct bill file page (Ficha Asunto): `https://parlamento.gub.uy/documentosyleyes/ficha-asunto/{AsuntoID}` (e.g. Asunto 156712).

**Local terms (use all):**
- `impuesto al patrimonio` (the primary legal term in Uruguay, Título 14 del Texto Ordenado)
- `sobretasa del impuesto al patrimonio` / `sobretasa al patrimonio`
- `impuesto a los más ricos` / `impuesto al 1% más rico`
- `impuesto a las grandes fortunas`
- `impuesto a la riqueza`
- `impuesto a los millonarios`

**Key bills post-2010:**
- **Carpeta 804/2022 (Asunto 156712, Distribuido 1227/2022 and Distribuido 79/2025):** *Fondo Nacional de Vivienda. Se crea una sobretasa sobre el Impuesto al Patrimonio.*
  - **Sponsors:** Senators Oscar Andrade, Daniel Caggiani, Charles Carrera, Daniel Olesker, Uruguay Russi, Alejandro Sánchez (Frente Amplio).
  - **Text:** Article 1: *"Créase una sobretasa de un 25% (veinticinco por ciento) sobre el Impuesto al Patrimonio, cuya recaudación será destinada al Fondo Nacional de Vivienda."*
  - **History:** Entered Senate on 17 October 2022 (Diario de Sesiones No. 33 of 18 October 2022); referred to Comisión de Vivienda y Ordenamiento Territorial. Lapsed at the end of the XLIX Legislature (February 2025) and archived. Reintroduced on 11 March 2025 when Senator Daniel Caggiani requested its desarchivo, approved 27 to 2 by the Senate plenary (Diario de Sesiones No. 5 of 11 March 2025, p. 36; Distribuido 79/2025). Currently pending in committee.
- **Carpeta 1168/2013 (Distribuido 2007/2013, Ley 19.088):** Government bill sent by President José Mujica and Economy Minister Fernando Lorenzo to adjust Impuesto al Patrimonio on rural land and agricultural assets above 12,000,000 UI, following the Supreme Court invalidation of the ICIR. Promulgated as Ley 19.088 on 14 June 2013.

## 2. Debates and votes

- **Plenary records (Diarios de Sesiones):**
  - Published in PDF and HTML at `https://parlamento.gub.uy/documentosyleyes/documentos/diarios-de-sesion/{id}/IMG` (PDF) and `/SSN` (HTML).
  - Speaker labels in Diarios de Sesiones follow standard conventions: `SEÑOR SENADOR [SURNAME]`, `SEÑORA PRESIDENTA`, `SEÑOR SECRETARIO`.
  - Introduction of Carpeta 804/2022: Cámara de Senadores, 3er Período Ordinario, Sesión 33 (18 October 2022), Diario Nro. 33, item 5: *"Varios señores senadores presentan un proyecto de ley por el que se crea una tasa del 25 % sobre el impuesto al patrimonio, cuya recaudación será destinada al Fondo Nacional de Vivienda y Urbanización."*
  - Desarchivo vote: Cámara de Senadores, 1er Período Ordinario, Sesión 4 (11 March 2025), Diario Nro. 5, p. 36: vote on desarchivo of Carpeta 804/2022 requested by Sen. Daniel Caggiani; approved 27 en 29.
- **Committee records (Versiones Taquigráficas):**
  - Full verbatim records of Senate and House committee sessions are recorded and published as PDFs at `https://parlamento.gub.uy/documentosyleyes/documentos/versiones-taquigraficas/{cuerpo}/{legislatura}/{distribuido}/{anexo}`.
  - Hearing of 14 November 2023 (VT 1872/0, XLIX Legislatura): Comisión de Vivienda y Ordenamiento Territorial received Minister Raúl Lozano to discuss Carpeta 804/2022; Senator Oscar Andrade defended the 25% surcharge on Impuesto al Patrimonio.
  - Hearing of 9 September 2025 (VT 444/2025, L Legislatura): Comisión de Vivienda y Ordenamiento Territorial received a delegation from the Facultad de Arquitectura, Diseño y Urbanismo (UDELAR), including architects Lucía Anzalone and Andrés Cabrera, who presented testimony endorsing the 25% wealth-tax surcharge (Distribuido 79/2025) to provide permanent financing for the housing fund.
- **Roll calls and voting rules:**
  - Most votes in the Uruguayan Senate and Chamber of Representatives are conducted by show of hands ("por la afirmativa, sírvanse manifestar"), where the secretariat announces only the totals (e.g. "27 en 29. Afirmativa").
  - Roll-call votes (*votación nominal*) occur upon formal request supported by the required number of members, or on constitutional/disciplinary matters. When a roll call occurs, names are recorded under *afirmativa* or *negativa*.
  - Desarchivo votes and general committee referrals are plenary votes, but under the project QA rules, block procedural or omnibus budget votes are discarded; only explicit bill sponsorships, article-specific votes, or member speeches/testimony count.

## 3. Members, parties, seats

- **Official member list:** `https://parlamento.gub.uy/sobreelparlamento/legisladores` and individual member profiles at `/camarasycomisiones/legisladores/{id}`.
- **Chambers:**
  - Cámara de Senadores: 30 senators elected proportionally in a single nationwide district, plus the Vice President of the Republic (who presides).
  - Cámara de Representantes: 99 deputies elected across the 19 departamentos (at least two per departamento).
- **Parties (L Legislatura 2025–2030):** Frente Amplio (governing coalition, comprising Movimiento de Participación Popular [MPP], Partido Comunista [PCU/Lista 1001], Partido Socialista [PS], Convocatoria Seregnista Progresistas / Asamblea Uruguay, Casa Grande, Vertiente Artiguista), Partido Nacional, Partido Colorado, Cabildo Abierto, Partido Independiente, Identidad Soberana.

## 4. Other official records

- **IMPO (Dirección Nacional de Impresiones y Publicaciones Oficiales):** `https://www.impo.com.uy`
  - Publishes the *Diario Oficial* and official compilations of law (Texto Ordenado).
  - Impuesto al Patrimonio: Título 14 del Texto Ordenado 2023 (`https://impo.com.uy/bases/todgi2023/101-2024/4_T14`).
  - Ministry of Economy and Finance (MEF) decrees setting the non-taxable minimum threshold (*mínimo no imponible*), updated annually every December.
- **Party and civil society primary records:**
  - Frente Amplio: *Bases Programáticas 2025 - 2030* (`https://www.frenteamplio.uy/wp-content/uploads/Bases-Programaticas-2025-2030.pdf`), p. 29 on strengthening progressive taxation on net wealth, gran capital, and large fortunes.
  - PIT-CNT: Consultative commission report on the personal net wealth tax surcharge (*Propuesta de creación de una sobretasa del Impuesto al Patrimonio de las Personas Físicas (IPPF)*, November 2025, `https://www.pitcnt.uy/sites/default/files/2025-11/IPPF.pdf`).

## 5. Access notes

- **CloudFront anti-bot protection:** Plain Python `urllib` requests without browser headers receive HTTP 403 Forbidden. Requests MUST specify standard browser headers (`User-Agent`, `Accept`, `Accept-Language`).
- **Temporary PDF links (`/temporales/<uuid>.PDF`):** When viewing a document (Distribuido, Diario de Sesiones, or Versión Taquigráfica), the Drupal frontend generates a dynamic temporary PDF located on `https://infolegislativa.parlamento.gub.uy/temporales/<uuid>.PDF` and embeds it in an `iframe id="documento"`. Plain links to older `/temporales/` URLs return HTTP 404 after the server session expires. To fetch any PDF programmatically:
  1. Request the canonical permalink on `parlamento.gub.uy` (e.g. `/documentos-comision/senadores/50/79/0`).
  2. Parse the HTML to extract the `src` attribute of `iframe id="documento"`.
  3. Immediately fetch and save that temporary URL to disk.
- **Tools that worked:** `python skill/scripts/gazette_scan.py` works on downloaded PDFs in `data/uy/primary_docs/`.

## 6. Coverage log

| Date | Run | Documents read (title, number, date) | Result (rows added, votes found) | Not read / open |
|---|---|---|---|---|
| 2026-11-08 | R003 | Texto Ordenado 2023 Título 14 Impuesto al Patrimonio (Decreto 101/024); Decreto MEF 1765 (31 Dec 2024); Ley 20.531 Rendición de Cuentas; PIT-CNT IPPF.pdf; De Rosa and Vilá letter; FES Minuta Uruguay | Primary tax framework and commission authors added | Senate bill number and primary parliamentary documents not yet located |
| 2026-11-09 | R004 | Carpeta 804/2022 (Distribuido 1227/2022 & Distribuido 79/2025); Diario de Sesiones No. 33 (18-10-2022); Diario de Sesiones No. 5 (11-03-2025); Versión Taquigráfica 1872/0 (14-11-2023); Versión Taquigráfica 444/2025 (09-09-2025); Distribuido 2007/2013 (Carpeta 1168/2013, Ley 19.088); Bases Programáticas Frente Amplio 2025-2030 (p. 29); El Popular interviews & speeches (Moreira, De Rosa, Giometti) | Upgraded 6 bill sponsors to primary parliamentary record (Asunto 156712); added Constanza Moreira (speech), Bruno Giometti (article), Lucía Anzalone & Andrés Cabrera (testimony), Andrade committee speech, De Rosa interview; verified Frente Amplio programme p. 29; qualified bill added to resources.json | Committee debate in Chamber of Deputies on 2013 rural patrimony reform |

## 7. Known gaps and next steps

- Monitor committee progress of Carpeta 804/2022 (Distribuido 79/2025) in the Senate Comisión de Vivienda y Ordenamiento Territorial.
- Check future legislative entry of the PIT-CNT personal wealth tax surcharge proposal once formal legislation is filed in the 2025–2030 legislative period.
- Sample Montevideo Junta Departamental for municipal motions on wealth tax or local contributions.
