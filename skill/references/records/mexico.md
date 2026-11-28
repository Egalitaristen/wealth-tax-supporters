# Mexico: where the official record is and how to read it

Written in run R020 (2026-11-12). Every route below was tested on that date from one Windows machine in Europe (a residential connection). Mexico's parliament publishes a lot, but its own sites mostly cannot be opened from outside Mexico by scripts or by an ordinary browser here, so **the reliable route is the Wayback Machine's raw copy of the Gaceta Parlamentaria**. Mexico has no national wealth tax. The Congress of the Union has two chambers (Cámara de Diputados, Senado de la República); the legislatures are numbered LXI (2009-12) to LXVI (2024-27).

## 1. Bills, motions and proposals

- **Gaceta Parlamentaria of the Cámara de Diputados**, `https://gaceta.diputados.gob.mx/`. Holds every initiative, with the full text. **Direct access failed** (connection times out after 20 s, from `curl` and from Chrome, 12 Nov 2026). **Works through Wayback**, with the `id_` flag (raw bytes, no toolbar): `https://web.archive.org/web/2026id_/https://gaceta.diputados.gob.mx/<path>`. Add `--compressed` to `curl`. Not every file was archived (a 404 means this one was not captured; try another form of the same document: the day's `.html` page, the `.pdf`, a numbered part such as `-II-4`).
  - Day page: `/Gaceta/66/2026/mar/20260303-II-4.html` (legislature 66, year, month abbreviation, date, annex `-I`, `-II-1` ... ). Each page lists at the top the titles of that annex and holds the full text of every initiative in it, with `#Iniciativa3` anchors. Text is HTML, in UTF-8, and a Gaceta page is cleanly searchable.
  - PDF of the same annex: `/PDF/66/2026/mar/20260303-II-4.pdf` (text PDFs; `pymupdf` reads them). The `-I` annex holds the communications and the summary of the day, the initiatives are in the `-II-n` annexes.
- **Index of initiatives per period, the best entry point.** `/Gaceta/Iniciativas/<legislature>/gp<legislature>_a<year><period>.html`, for example `/Gaceta/Iniciativas/66/gp66_a2segundo.html` (second ordinary period of the second year). One block per initiative: title, `Presentada por ... (party); y suscrita por ...`, `Turnada a la Comisión de ...`, any `Prórroga`, `Dictamen` or `Aprobada` line, and the Gaceta number it appeared in. Encoded **windows-1252**: decode with `cp1252` or accents break. Pages are large (0.4 to 1.2 MB) and one request per 10 seconds or slower is needed: Wayback answers 429, then refuses connections, after about 30 quick requests. `a1primero` returned 200 for legislatures 61 to 66; the `_a3primero` of the 66th exists. Search the text for `riqueza`, `fortuna`, `patrimonio`, `multimillonari`, `Impuesto sobre la Renta`.
- **Sistema de Información Legislativa (SIL)**, `https://sil.gobernacion.gob.mx/`. The Interior Ministry's tracking system for every initiative since 1997 (stage, turn, votes). `curl` fails the TLS check ("unable to get local issuer certificate"; the server does not send its intermediate certificate); a client that skips certificate checks was not used. In Chrome `/portal` loads but the search page `/Busquedas/Basica/BusquedaBasica.php` rendered blank. Not read in this run. Not archived by Wayback (`available` API returned no snapshot).
- **Senado de la República**: `https://www.senado.gob.mx/` and `comunicacionsocial.senado.gob.mx` answer **403 with an Incapsula bot wall** to scripts; `infosen.senado.gob.mx/sgsp/gaceta/<leg>/<year>/<date>-<n>/assets/documentos/<file>.pdf` (where the Senate's own initiatives are filed as PDFs) is behind the same wall; `gaceta.senado.gob.mx` does not connect. Wayback has the page `www.senado.gob.mx/66/gaceta_del_senado` (a menu, no list of initiatives) but a given initiative document is a matter of luck. A web search sometimes returns an `infosen` PDF URL: try it with `https://web.archive.org/web/2id_/` in front.
- **Sponsor group pages** work directly: `https://www.ptdiputados.org.mx/iniciativa.php?id=406` (PT) lists each initiative with a link to the Gaceta page. Other groups' pages were not tested.
- **Search terms (Spanish)**: `impuesto a las grandes fortunas`, `impuesto a las grandes riquezas`, `impuesto a la riqueza`, `impuesto sobre el patrimonio`, `impuesto al patrimonio neto`, `contribución a las grandes fortunas`, `impuesto a los multimillonarios`. Look-alikes to exclude: `impuesto a las herencias` (inheritance), `impuesto predial` and `impuesto a la propiedad` (property), `impuesto a bienes de lujo` (luxury goods), `sobretasa del ISR` or `tasa máxima` (income).
- **Sponsors and co-signers**: the index prints `Presentada por ... ; y suscrita por integrantes del Grupo Parlamentario de ...` (a whole group signs, names not listed) or `y suscrita por los diputados ...` in the initiative text; the last page of the initiative has the signatures (`(rúbrica)`).
- **Government proposals**: the annual package (Paquetes Económicos, Ley de Ingresos, Miscelánea Fiscal) from the Treasury (`hacienda.gob.mx`, `ppef.hacienda.gob.mx`) is voted as a block and does not count as wealth-tax evidence.

## 2. Debates and votes

- **Diario de los Debates**: `cronica.diputados.gob.mx/PDF/<leg>/<year>/<month>/<yymmdd>-<n>.pdf` (a web search returns these). Not opened here.
- **Committee turn and report**: the index above gives the turn and, once there is one, the `Dictamen`; the Comisión de Hacienda y Crédito Público publishes its own agenda and minutes (`diputados.gob.mx/LeyesBiblio/..` and the committee pages): not read.
- **Roll calls**: the Cámara publishes nominal votes at `sitl.diputados.gob.mx`; not reachable in this run. Wealth-tax initiatives have not reached a floor vote in the cases read so far.

## 3. Members, parties, seats

- `sitl.diputados.gob.mx`, `diputados.gob.mx` and `senado.gob.mx` rosters time out or answer 403 to scripts; the seats adapter reads the English Wikipedia article for the legislature (see `references/countries/mx.md`).

## 4. Other official records

- INEGI (geostatistics, open licence), SAT statistics (`sat.gob.mx`, not tested), Supreme Court rulings (`scjn.gob.mx`, not tested).

## 5. Access notes (summary of what was tried, 12 Nov 2026)

| Route | Result |
|---|---|
| `gaceta.diputados.gob.mx` direct (curl, Chrome) | Times out |
| `web.archive.org/web/2026id_/https://gaceta.diputados.gob.mx/...` (curl, with `--compressed`) | Works: day pages, PDFs and period indices; some files not archived; 429 under fast sweeps |
| `sil.gobernacion.gob.mx` curl | TLS error (no intermediate certificate) |
| `sil.gobernacion.gob.mx` Chrome | Portal loads, search page blank; not read |
| `senado.gob.mx`, `comunicacionsocial.senado.gob.mx`, `infosen.senado.gob.mx` | 403, Incapsula |
| `gaceta.senado.gob.mx` | No connection |
| Wayback of Senate pages | `senado.gob.mx/66/gaceta_del_senado` 200 (menu only); home page 403; documents hit and miss |
| `ptdiputados.org.mx` | Works with curl |
| Web search | Indexes Gaceta pages and PDFs, useful to find a document before fetching it via Wayback |
| `fetch_page.py` (Playwright) | Not tried: no Chromium installed on this machine |

Never write a number or name from a press report: Mexican press summaries of wealth-tax initiatives differ on the articles and on whether debts are deducted. Read the Gaceta text.

## 6. Coverage log

| Date | Run | Documents read (title, number, date) | Result (rows added, votes found) | Not read / open |
|---|---|---|---|---|
| 2026-11-12 | R020 | Gaceta 6987-II-4 of 3 March 2026, initiative 3 (PT, Sánchez González, impuesto a las grandes riquezas), full text; Gaceta index of initiatives `gp66_a2segundo` (copy of 14 Oct 2026) for turn and status | PT bill page rebuilt from the text; evidence E00008 re-sourced to the Gaceta; document M0001 | Diario de los Debates 3 March 2026; committee agendas; SIL record; Senate Gaceta |

## 7. Known gaps and next steps

- Scan the period indices for legislatures 61 to 66 (`a1primero` to `a3segundo`) for wealth-tax titles, then open each hit's Gaceta page. Record in section 6 which indices were scanned.
- Senate: Sen. Amalia García Medina (MC), 22 April 2026, initiative on inheritances and large fortunes (a law-firm note describes a tax on net wealth above 100 million pesos): the Senate's own text was not reachable; find it through an `infosen` PDF URL via Wayback.
- Dip. Alfonso Ramírez Cuéllar (Morena), February 2021: press says he proposed a tax on large fortunes; find the initiative in the 64th legislature's index.
- Try SIL from a browser that can render it, or with the intermediate certificate installed properly.
