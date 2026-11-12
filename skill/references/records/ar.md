# Argentina: where the official record is and how to read it

Written on 12 November 2026 (records-guide pass for Argentina). Every route below was tested that day from a Windows machine in Europe with `curl`, `urllib`, `pdftotext`, the Claude in Chrome extension and the app's cloud-side fetcher. Nothing here is a source for a claim in the register; the register's own sources are. Country notes (seats, maps) are in `references/countries/ar.md`.

**What counts.** An annual or one-off tax on the stock of wealth: Ley 27.605 (Aporte Solidario y Extraordinario, 2020), Bienes Personales (Ley 23.966, Título VI), the IMAP bill (2026), Pablo Carro's ten-year contribution (2022, lead D0001). Income, property or windfall taxes do not count.

## 0. The short version

- **The Cámara de Diputados cannot be reached from this machine by any route.** `www.hcdn.gob.ar`, `www.diputados.gob.ar`, `www4.hcdn.gob.ar`, `www3.hcdn.gob.ar`, `rest.hcdn.gob.ar`, `datos.hcdn.gob.ar`, `votaciones.hcdn.gob.ar` and `www.congreso.gob.ar` all resolve in DNS (to 45.230.20.15 / 2801:15:b000:2:45:230:20:15) and then time out at the TCP connection: curl `000` after 15 s, IPv4 and IPv6 alike. The same sites did not load in Chrome (the tab stayed on the browser's own page) and failed in the cloud-side fetcher (`ECONNRESET`). That looks like a network-level block of non-Argentine addresses, not a user-agent or JavaScript wall, so `fetch_page.py` (a headless Chromium on the same network) is expected to fail the same way; it was not run (`trafilatura` is not installed here and nothing suggests it would help). Do not try proxies or "reader" services to get round it (a third-party proxy probe was refused by the session's safety layer and was not run).
- **What works instead:** (a) the Internet Archive for the Chamber's old documents (section 1); (b) the Senate's own site, which carries the Chamber's file number, authors and committee path for every bill that reached the Senate (section 1); (c) Infoleg and AFIP's legal library for laws; (d) news sites for leads only.
- **What does not work:** anything from August 2026 onwards on the Chamber's new `rest.hcdn.gob.ar` site (the IMAP bill). The Internet Archive has no copy. This needs a browser on an Argentine address (a person with a connection in Argentina, or a VPN the maintainer controls), or a later archive snapshot. Until then the IMAP page stays at what the register's one verified quote supports.

## 1. Bills, motions and proposals

| Source | Address | What it holds | Result on 12 Nov 2026 |
|---|---|---|---|
| Chamber bill pages | `https://www.hcdn.gob.ar/proyectos/proyecto.html?exp=4534-D-2020` (also `/diputados/<user>/proyecto.html?exp=`) | status, signers, committee giro | **Blocked** (timeout). Earlier runs read copies from `web.archive.org` (evidence rows cite `web.archive.org/web/20251101200722/...`). |
| Chamber Trámite Parlamentario PDFs | `https://www4.hcdn.gob.ar/dependencias/dsecretaria/Periodo2020/PDF2020/TP2020/4534-D-2020.pdf` (pattern `Periodo{Y}/PDF{Y}/TP{Y}/{NNNN}-{D\|PE\|S}-{Y}.pdf`) | the bill text with fundamentos and the full list of co-signers (`Firma ... Cofirmantes: ...`) | **Blocked directly. Readable through Wayback for many bills**: `https://archive.org/wayback/available?url=<url without scheme>` gives the snapshot timestamp; then `curl -L "http://web.archive.org/web/<timestamp>id_/https://<url>" -o x.pdf` and `pdftotext -layout x.pdf` (text PDFs, Latin-1 accents, no OCR needed). Hit: 4534-D-2020 (snapshot 2025-11-03), 4174-D-2025, 3961-D-2022. Miss: 0747-D-2022 (Carro, 2022). A miss is common; the API answers `{}` and no snapshot exists. |
| Chamber new site | `https://rest.hcdn.gob.ar/web/tramites-parlamentarios/render/adjunto/<id>.pdf`, `/web/proyectos/<n>/adjuntos/<n>` | 2026 documents including the IMAP bill | **Blocked and not archived.** The search engine indexes some of these PDFs (a query for "Impuesto Mínimo a los Altos Patrimonios" returns `.../render/adjunto/6a7cbdaf6c590.pdf`), but opening one fails. A search snippet is not a document read; nothing from it was used. |
| Chamber deputy pages | `https://www.hcdn.gob.ar/diputados/epaulon/listado-proyectos.html` | a deputy's list of bills | Blocked; Wayback has a snapshot from 8 May 2026, which predates the IMAP (August 2026), so it cannot list it. |
| Chamber open data | `https://datos.hcdn.gob.ar` | CSV/API of bills, votes | **Blocked.** Not archived in a useful form. |
| Senate bill search | `https://www.senado.gob.ar/parlamentario/parlamentaria/` | every Senate-origin bill since 1983 and every Chamber bill that reached the Senate | **Works with `curl`** (not with Python `urllib`, which the site answers with a CAPTCHA page; do not try to get past it). See "Senate search recipe" below. |
| Senate bill record | `https://www.senado.gob.ar/parlamentario/comisiones/verExp/49.20/CD/PL` | file number in the Chamber (`Exp. HCD: 4534-D-2020`), authors (`HELLER; KIRCHNER Y OTROS`), orden del día, committee giro, dates of sanction, law number, decree, Boletín Oficial number | **Works.** |
| Infoleg | `https://www.infoleg.gob.ar` (`servicios.infoleg.gob.ar` answers 302) | law texts | Reachable; not used in depth. |
| AFIP legal library | `https://biblioteca.afip.gob.ar/dcp/TOR_C_023966_1997_03_26` | text of Ley 23.966 | Reachable (used for the register's Bienes Personales entry). |
| Boletín Oficial | `https://www.boletinoficial.gob.ar` | laws and decrees as published | **Blocked** (timeout). |
| `argentina.gob.ar/normativa` | | laws | Reachable (HTTP 200). |

**Senate search recipe (curl only).** The search form is a Symfony form with a CSRF token. Two calls with a cookie jar:

1. `curl -s -c cj.txt -b cj.txt -A 'Mozilla/5.0' https://www.senado.gob.ar/parlamentario/parlamentaria/ -o s0.html`, take the value of `busqueda_proyectos[_token]` from `s0.html`.
2. `curl -s -c cj.txt -b cj.txt -A 'Mozilla/5.0' https://www.senado.gob.ar/parlamentario/parlamentaria/avanzada --data-urlencode "busqueda_proyectos[palabra]=<term>" --data-urlencode "busqueda_proyectos[_token]=<token>" -d "busqueda_proyectos[opcion]=Y" -d "busqueda_proyectos[expedienteTipo]=PL" -d "busqueda_proyectos[autor]=" -d "busqueda_proyectos[comision]=" -d "busqueda_proyectos[tipoDocumento]=" -d "busqueda_proyectos[expedienteLugar]=" -d "busqueda_proyectos[expedienteNumeroPos]="`

Results are table rows `<a href="/parlamentario/comisiones/verExp/<n>.<yy>/<origin>/<type>">` with number, type, origin (`S` Senate, `CD` Chamber) and the **extract** (the one-line summary in capitals). The search looks only at the extract (and, for some types, the original text), is an exact word match with no stemming, shows 10 rows per page with a total count (`Cantidad total de registros`), and I found no page parameter: narrow the term instead. Expediente types: `PL` bill, `PC` communication, `PD` declaration, `PR` resolution, `CV` miscellaneous communications, `OV`/`OVD` official papers.

**Search terms** (Spanish). `grandes fortunas`, `fortuna`, `riqueza`, `patrimonio`, `patrimonio neto`, `altos patrimonios`, `impuesto a la riqueza`, `aporte solidario`, `aporte extraordinario`, `bienes personales`, `impuesto al patrimonio`, `superricos`, `millonarios`, `Zucman`. Warnings: `patrimonio` finds mostly cultural heritage bills; `riqueza` finds the forestry law (20.531); `aporte solidario` finds union contributions.

**Sponsors.** The signed list is printed at the end of the bill's Trámite Parlamentario PDF (`Firma <author>`, `Cofirmantes: ...`), not on the Senate record, which gives the first author and "Y OTROS". Names are printed without the deputy's bloc.

**Government proposals.** Not searched. The Executive's budget messages and AFIP statistics were not read.

## 2. Debates and votes

Not read in this pass. Where they are: Chamber transcripts (`Versiones taquigráficas`) and roll calls (`votaciones.hcdn.gob.ar`) are on blocked hosts; the Senate's are at `senado.gob.ar/parlamentario/sesiones/` and `/votaciones/` (reachable with curl, not opened). For Ley 27.605 the Chamber vote was on 17 November 2020 and the Senate's on 4 December 2020 (Senate record, section 1); the register's 179 supporters of that bill come from earlier roll-call harvests.

## 3. Members, parties, seats

`python skill/scripts/seats.py data/ar` reads `diputados.gob.ar/diputados/` and `senado.gob.ar/senadores/listados/listaSenadoRes` (see `countries/ar.md`). The first host is the blocked one: the seat run needs the Senate list only on this machine, and the Chamber list from an Argentine address or an archived copy.

## 4. Other official records

AFIP (Bienes Personales and Aporte Solidario statistics) and the Ministerio de Economía: not read. Court challenges to Ley 27.605 (Corte Suprema, December 2021): not read.

## 5. Access notes

- Test order on a new machine: (1) `curl -m 15 -I https://www.hcdn.gob.ar`; if it times out, go straight to Wayback and the Senate; do not spend more time on the Chamber's hosts. (2) Wayback availability call for the exact PDF URL. (3) Senate search for the bill's extract. (4) News for leads.
- Python `urllib` is served a CAPTCHA by senado.gob.ar; `curl` is not. A CAPTCHA is never to be solved or evaded: if one appears, stop and use another route.
- The cloud-side `WebFetch` tool and Chrome were no better than curl for the Chamber (`ECONNRESET`; error page).
- Secondary sources (flag as secondary, use for leads, never for register quotes): iprofesional.com, cronista.com, ambito.com, economis.com.ar, parlamentario.com and chequeado.com are reachable; they carry no expediente numbers for the 2022 Carro bill.
- Language: Spanish. PDFs are text.

## 6. Coverage log

| Date | Run | Documents read (title, number, date) | Result | Not read / open |
|---|---|---|---|---|
| 2026-11-12 | records-ar | Senate record of 49/20 CD (Aporte Solidario, Exp. HCD 4534-D-2020); Chamber text of 4534-D-2020 via Wayback snapshot 2025-11-03 (all articles, fundamentos and signer list); Senate bill search, 20 terms, type `PL` (and the one `OV/CV` hit set for `fortunas`) | The Senate holds only one wealth-tax bill: the Chamber's 49/20 CD (Ley 27.605). The 2020 Senate `OV/CV` papers (312/20, 76/20) are municipal councils' letters on it. No Senate-origin wealth-tax bill found by extract search (for terms with more than 10 hits, `bienes personales` 80, `patrimonio` 226, `capital` 744, `emergencia` 919, `gravamen` 93, `extraordinario` 54, `solidario` 59, only the first ten rows were read, so this is not proof of absence). Wealth tax in the Chamber: 4534-D-2020 confirmed; signers: Heller (author) and 14 cosigners | The IMAP bill (August 2026) and every other Chamber bill: Chamber hosts unreachable. 0747-D-2022 (Carro) not archived. Senate transcripts and votes. Boletín Oficial text. Chamber bills from 2010 to 2019 (no way to list them) |

## 7. Known gaps and next steps

1. **IMAP bill:** open `https://rest.hcdn.gob.ar/web/proyectos/293708/adjuntos/107190` and the Chamber's bill page from an Argentine address (or via someone there), read the expediente number, signers, giro and the articles, then rebuild the page. Until then the IMAP page says what the one register quote supports.
2. **Chamber search for 2010-2026:** the Chamber's search (`hcdn.gob.ar/proyectos/`) and open data (`datos.hcdn.gob.ar`) are the only complete index; from here nothing replaces them. Candidate bills from the register's leads: Pablo Carro's 2022 "Aporte Solidario Temporario" (lead D0001; the search engine indexes expediente 0747-D-2022 but the PDF could not be opened).
3. Chamber and Senate floor transcripts and roll calls for Ley 27.605 (Senate side reachable).
4. Retry Wayback for 0747-D-2022 and for 2026 documents in a few weeks (the Archive may add them).
