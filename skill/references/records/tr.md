# Turkey: where the official record is and how to read it

Written 2026-11-12 (run: records-tr access pass). Country guide: `skill/references/countries/tr.md`. Nothing here is a source for a claim in the register; the register's own sources are.

**The one fact that unlocks everything: use the host `tbmm.gov.tr` WITHOUT `www`.** `https://www.tbmm.gov.tr/...` answers `308` to `http://tbmm.gov.tr:80/...`, which stalls or fails for many clients. `https://tbmm.gov.tr/...` returns the pages with a plain `curl` or `requests` (any browser-like User-Agent, no browser needed). `www2.tbmm.gov.tr` (old `d28/2/2-<n>.pdf` pattern) does not connect at all (tested 2026-11-12). Term numbers: 28th term = from 2023; bills by MPs carry the prefix `2/`, government bills `1/`, research motions `10/`.

## 1. Bills, motions and proposals

- **Bill search, current (28th) term**: form `https://tbmm.gov.tr/yasama/kanun-teklifleri`; data endpoint `GET https://tbmm.gov.tr/Yasama/Kanun-Teklifleri-Sonuc-Sayfa` with DataTables parameters (`draw, start, length, columns[i][...]`) plus `DonemYasamaYili`, `TaksimNo=0`, `TeklifSicil`, `IlkImzaSahibi=false`, `SonDurumu`, `MetinArama=<term>`. The three GUID fields must be the zero GUID `00000000-0000-0000-0000-000000000000`, not empty (empty returns 0 rows silently). Returns JSON with the proposer line, title, summary, status and links to the text PDF and the detail page. `length` up to 500 works.
- **Past terms (20 to 27)**: same, at `/yasama/Gecmis-Kanun-Teklifleri` and `/Yasama/Gecmis-Kanun-Teklifleri-Sonuc-Sayfa`, `DonemYasamaYili` = the term GUID listed on the form (27th `f72877c2-f508-037b-e050-007f01005610`, 26th `...f51d...`, 25th `...f509...`, 24th `...f50a...`, 23rd `...f50b...`; zero GUID = all past terms, 21,830 records).
- **`MetinArama` searches the title and summary only**, not the bill text (`IcerikArama` is ignored in the current term). A wealth-tax article inside a general tax bill is invisible to it: download the PDFs (`cdn.tbmm.gov.tr/KKBSPublicFile/D<term>/Y<year>/T2/WebOnergeMetni/<guid>.pdf`) and search the text.
- **Detail page**: `https://tbmm.gov.tr/Yasama/KanunTeklifi/<guid>` (link "Diğer Bilgiler") lists term/year, number, date, title, summary, **Son Durumu** (status), committee table (type, name, entry/exit dates, action), and the **signers table** (name, party, constituency, first signer flagged).
- **Incoming papers**: `https://tbmm.gov.tr/Gundem/GelenKagitDetay/<guid>` (works; HTML).
- **Research motions and general debate motions**: `/denetim/meclis-arastirma-onergeleri`, `/denetim/genel-gorusme-onergeleri` (past terms: `/Denetim/meclis-arastirma-onergeleri-gecmis-donem` and `...genel-gorusme-onergeleri-gecmis-donem`). Flow: GET the form for the CSRF token, POST the form (`AranacakKelime`, GUID fields), read the embedded `data:` object and the CSRF header from the result page, then POST form-encoded DataTables parameters (with `columns[i][name]`) to `/Denetim/MeclisArastirmaOnergesiTable` or `/Denetim/GenelGorusmeOnergesiTable` with header `X-CSRF-TOKEN-TBMM-WEB-Mvc-Prod`. For past terms omit `YasamaYiliId` and send `GecmisDonemId`, or the server answers with the current term.
- **Search terms**: `servet vergisi`, `servet`, `varlık vergisi` (the 1942 levy: Garo Paylan's apology bills 2/4717 and research motions 10/2093, 10/5062 are about that, not a wealth tax), `zenginlik`, `artan oranlı`, `temel gelir`, `servet beyanı`. Look-alikes to exclude: `gelir ve servet üzerinden alınan vergilerde çifte vergilendirme` (double-tax treaties; dozens of hits), `değerli konut`, `emlak vergisi`, `veraset`.

## 2. Debates and votes

- **Plenary full-text search**: form `/Tutanaklar/TutanakSorgu`; data `GET /Tutanaklar/Tutanaklar-Sonuc-Sayfa` (params `YasamaDonemi=<term number>`, `YasamaYili`, `Kelime`, DataTables columns `donemVeYasamaYili, birlesimNo, tarih, sayfa, onizleme`). Each hit gives term/year, sitting number, date, page and a snippet with a link `Tutanak?Id=<guid>&BaslangicSayfa=<p>`. That page embeds the minutes PDF (`cdn.tbmm.gov.tr/TbmmWeb/Tutanak/<term>/<year>/<sitting>/Tam/<guid>.pdf`, also `.html`/`.docx`, and a printed version). Snippets do not name the speaker: open the PDF page.
- Committee minutes: `/Tutanaklar/KomisyonTutanaklari`; committee reports: `/yasama/komisyon-raporlari` (form POST `/Yasama/KomisyonRaporlari-Sonuc`). Not read in this pass.
- Roll calls: not located in this pass.

## 3. Members, parties, seats

- `https://tbmm.gov.tr/milletvekili/liste`, `/sandalyedagilimi`, `/milletvekili/milletvekiligi-sona-erenler` (reachable). Members appear by name with the party at signing time.

## 4. Other official records

- `https://www.mevzuat.gov.tr/` and `https://www.resmigazete.gov.tr/` return 200 to curl (enacted law; not needed for pending bills). `www5.tbmm.gov.tr/develop/owa/kanunlar_erisim.Giris` (law and decision system) returns 200. `acikerisim.tbmm.gov.tr` returns 200 (library). `data.tbmm.gov.tr` does not resolve. Wayback has no copy of the 2/2613 detail page.

## 5. Access notes

- Bill text PDFs from 2019 onward that carry a text layer are often **mangled** (2/2613: Turkish letters ı, ş, ğ lost); older and many newer ones are **scans with no text layer** (875 of 1,355 tax-related MP-bill PDFs in the 23rd to 28th terms). OCR with Tesseract `-l tur --psm 6` at 200 to 300 dpi (render with PyMuPDF; `pdftoppm` is not installed here) reads them cleanly. Check numbers against the page image: OCR read "3,3" where the page says "3,5".
- `playwright`/`trafilatura` were not installed and were not needed. The in-app browser works too and is the easiest way to see which AJAX URL a form uses (read the network log after submitting).
- Python on this machine: run helper scripts from files with `</dev/null`; use `python -X utf8`.

## 6. Coverage log

| Date | Run | Documents read | Result | Not read / open |
|---|---|---|---|---|
| 2026-11-12 | records-tr | Detail page of bill 2/2613 (28/3, 16.10.2024); bill text PDF (4 pages, OCR plus page image) | Sole signer: Perihan Koca Doğan (DEM Parti, Mersin), first signer. Referred 17.10.2024: Plan and Budget Committee (lead), Health, Family, Labour and Social Affairs Committee (secondary). Status "KOMİSYONDA". Rates 2 / 3.5 / 5 / 7.5 / 10 % from TL 40m / 100m / 250m / 500m / 750m; Basic Income Guarantee Fund | Committee agenda/minutes |
| 2026-11-12 | records-tr | Title/summary search for `servet`, `varlık`, `zengin`, `servet vergisi` etc. in current and past terms 20 to 28 | In the wealth-tax sense only 2/2613 matches in the summaries | Bills whose summary lacks these words |
| 2026-11-12 | records-tr | PDF text of the 1,355 MP bills (terms 23 to 28) with `vergi` in the summary: text-layer grep; OCR of the 874 image-only ones (all done) | Text hits: 2/2613; 2/2708 (28/3, Öznur Bartın, labour-law omnibus: says wealth taxation "remains at very low levels", not a wealth-tax proposal as read from garbled text); 2/4717 (1942 levy apology); OCR hits only in treaty 2/2935 and income-tax bill 2/1556 (passing mentions); 2/2708 read in full by OCR: no wealth-tax article | Bills whose summary lacks `vergi` |
| 2026-11-12 | records-tr | Research and general-debate motion search, current and past terms | No motion proposes a wealth tax; 10/419 (28/2, Yeşiller ve Sol Gelecek Partisi) asks for an inquiry into income and wealth inequality | Texts of 10/4923, 10/5019 (tax-burden inquiries, 28/5) |
| 2026-11-12 | records-tr | Plenary search `servet vergisi`: 39 hits 28th term, 24 27th, 9 26th, 4 24th; `varlık vergisi` 5/10/10/13/6 | Snippets show many MPs calling for a wealth tax (2023 to 2026) | Speakers not identified, no minutes opened, no evidence rows written |

## 7. Known gaps and next steps

1. Done: OCR grep found no other wealth-tax bill (2/2613 only). Extend to bills whose summary lacks `vergi`.
2. Done: 2/2613 entry rebuilt (PR commit 6c78a54).
3. Open the plenary pages found by the search, name the speakers, and add evidence rows (speech) for MPs who call for the tax.
4. Read committee agendas for Plan and Budget on 2/2613.
