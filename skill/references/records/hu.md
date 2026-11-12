# Hungary: where the official record is and how to read it

Written in run R003 (2026-11-12). Country guide for maps, seats and shortcuts: `skill/references/countries/hu.md`. This file answers one question: **where is everything the Országgyűlés and the Government have put on record about the wealth tax (*vagyonadó*), and how do I get all of it?** Nothing here is a source for a claim in the register; the register's own sources are.

**Short answer.** Everything official sits on `parlament.hu`, and `parlament.hu` answers every script and every browser pane with an image CAPTCHA. It is not bypassed. Two routes work: a person opens the page or the PDF in an ordinary browser and saves it (then the file is read locally with `pdftotext`), and the Wayback Machine's `id_` copies of bills that were archived as real PDFs. Nothing else tried reaches the bill text.

## 1. Bills, motions and proposals

- **Register of bills.** `https://www.parlament.hu/web/guest/iromanyok-lekerdezese` (iromány search) and `https://www.parlament.hu/folyamatban-levo-torvenyjavaslatok` (pending bills). Both are behind the CAPTCHA, so the search could not be run from this machine: **no search for other wealth-tax bills since 2010 has been done on the official register.** Open it by hand (see section 5).
- **Document paths (static, predictable).** `https://www.parlament.hu/irom<term>/<number, 5 digits>/<number>.pdf`. The cycle number is not the parliamentary term: `irom38` = 2006-10 (T/9818, 2009), `irom42` = 2022-26 (T/5575, T/12722), `irom43` = 2026- (T/930). Other files of the same bill sit beside it with a suffix: `00930-0001.pdf`, `...-0002.pdf` (committee decisions, amendments, reports). Numbers restart each cycle.
- **Prefixes.** `T/` = bill (törvényjavaslat); `H/` = resolution proposal (határozati javaslat); `J/` = report; `B/` = report to the Assembly. `T/930/2` style suffixes are follow-up documents of the same bill.
- **Search terms (Hungarian).** `vagyonadó`, `vagyonadóról`, `szolidaritási vagyonadó`, `milliárdosok vagyonadója`, `luxusadó`, `gazdagok adója`, `szolidaritási hozzájárulás`, `válságadó`, `vagyonarányos közteherviselés`. Look-alikes to leave out: `vagyonadó` in the old sense of a levy on dwellings, boats and aircraft (T/9818, 2009), `építményadó`, `telekadó`, `kommunális adó` (local property taxes), `illeték` (duties), `különadó` on sectors (windfall).
- **Sponsors.** The cover page of the PDF names the submitter. A government bill carries "Benyújtó" (submitter, here a minister) and "Előadó" (presenter). A private member's bill lists the MPs as "Benyújtó" on the cover and by name at the end of the text. Quote the member's own entry.
- **Government proposals and consultations.** The consultation draft was published for comment on 6 Oct 2026 and closed on 14 Oct 2026 (Index, Telex, Hvg report this; the draft's own address was not found on `kormany.hu` and was not read).

## 2. Debates and votes

- **Plenary diary (*Országgyűlési napló*).** Per sitting on `parlament.hu` (section "Napló"). Also reached through `konyvtar.parlament.hu/documents/10181/...` (the parliamentary library hosts diary PDFs). Both: CAPTCHA.
- **Roll calls (*szavazás*).** Named votes are published per vote on `parlament.hu` ("Szavazások"). Not reachable.
- **Order of business.** Press agenda articles (Telex, Világgazdaság, Újpesti Hírmondó, Adózóna) name the day of the general debate. For T/930 they put it on 3 Nov 2026 and say committee reports and the amendment vote come in the week of 23 Nov 2026. These are secondary and not read in the parliament's record.
- **Numbering.** The bill is amended in the Legislative Committee (*Törvényalkotási Bizottság*); the summary of amendments appears as a further document of the same T/ number. The final text is the Magyar Közlöny.

## 3. Members, parties, seats

- Official list `https://www.parlament.hu/kepviselok` (CAPTCHA). The register uses hu.wikipedia and the MTI report of the inaugural sitting instead (see `data/hu/bodies.csv`).
- Open data: `https://www.parlament.hu/open-data` and `/documents/static/opendata/` both return the CAPTCHA page. `data.parlament.hu` does not resolve (no DNS).

## 4. Other official records

- **Enacted law:** `njt.hu` (connection reset from this machine, 2026-11-12) and `magyarkozlony.hu` (front page opens; a keyword-search address returned 404, search not explored). The justification of a bill passed into law is printed in the Magyar Közlöny's *Indokolások Tára* (the T/930 text says so itself).
- **Tax authority (NAV):** will host the mass real-estate valuation model that § 22 of T/930 describes; nothing read.
- **Constitutional Court, State Audit Office:** not searched.

## 5. Access notes (tested 2026-11-12)

| Route | Result |
|---|---|
| `parlament.hu` bill PDF, bill page, iromány search, open-data page, home page; Python urllib, default and Chrome user agents | CAPTCHA page (HTTP 200, 33,022 bytes, "CAPTCHA ellenőrzés … 5 attempts"), same for every path |
| Same in the Claude desktop built-in browser | Same CAPTCHA |
| `konyvtar.parlament.hu` diary PDF | Same CAPTCHA |
| Wayback `archive.org/wayback/available` for `irom43/00930/00930.pdf` | Two captures (2026-10-29, 2026-10-31); both are the CAPTCHA page, not the bill |
| Wayback `web/<ts>id_/https://www.parlament.hu/irom38/09818/09818.pdf` | Real PDF (327 kB). **Works for bills Wayback archived with a real PDF.** `irom42/12722/12722.pdf` (capture 2025-12-14) also returned a real PDF; the plain `/web/<ts>/` form returns a wrapper page |
| Wayback capture index (CDX) | Timed out or "temporarily offline" on 2026-11-12; 429 on rapid repeats; wait and retry |
| `adozona.hu/jogtar/<id>_T_930_szamu_torvenyjavaslat_indokolassal` (a reprint of the bill) | HTTP 403 bot wall; not bypassed |
| `njt.hu` | Connection reset |
| `data.parlament.hu` | No DNS |
| Telex, Index, Hvg, Infostart, law-firm blogs | Open; secondary |
| **A person saves the PDF in an ordinary browser, then `pdftotext -enc UTF-8 -layout file.pdf out.txt`** | **Works.** The T/930 PDF (351 kB, text layer, UTF-8) was read this way |

How to read the record when the CAPTCHA is the only blocker: a person opens `https://www.parlament.hu/irom<cycle>/<nnnnn>/<nnnnn>.pdf` (and the bill's page, the diary of the sitting and the vote list) in a normal browser, types the CAPTCHA and saves the files; the researcher then reads the saved files. For `checkquotes`: it cannot fetch parlament.hu, so check quotes against the saved text (`grep` on the flattened text) and say so in `grading_note`.

PDFs have a text layer (not scans). Command-line `pdftotext` mis-prints Hungarian characters on a Windows console; write with `-enc UTF-8` to a file.

## 6. Coverage log

| Date | Run | Documents read (title, number, date) | Result | Not read / open |
|---|---|---|---|---|
| 2026-11-12 | R003 | T/930 *A vagyonadóról*, government bill, submitted 2026-10-27 21:27 (cover, 39 §, Annex 1-2, general and detailed justification), saved by hand | Page rebuilt; 1 actor (Ruff), 3 evidence rows E00026-E00028; `documents.csv` M0001 | Bill page (committee, TAB amendments), diary and vote list of the 3 Nov 2026 debate, the consultation draft |
| 2026-11-12 | R003 | T/9818 *A vagyonadóról* (2009, Wayback `id_` PDF, cover and first page only) | Not added: 2009, before the register's 2010 start, and a tax on dwellings, boats and aircraft | rest of the text |
| 2026-11-04 | R002 | T/5575 and T/12722 (Wayback `id_` copies) | Bills and Párbeszéd sponsors in the register | |

## 7. Known gaps and next steps

1. Run the iromány search by hand for the terms in section 1, 2010 to date, and save every hit (bills, resolutions `H/`, amendments); only then can "no other wealth-tax bill since 2010" be said. Press and search engines found none besides T/5575, T/12722 and T/930.
2. T/930: bill page and follow-up documents (committee decisions, the Legislative Committee's amendments summary, the final text), the diary of 3 Nov 2026 with the speakers, and the final-vote list (adds MPs who voted for it, grade A).
3. The consultation draft of 6 Oct 2026 (where on `kormany.hu`).
