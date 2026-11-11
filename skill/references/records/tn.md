# Tunisia: where the official record is and how to read it

Record notes from R001 and R002 (2026-11-11). Nothing here is a source for a claim in the register.

## 1. Bills, motions and proposals

- **Bill page:** `https://arp.tn/loi/project/4238` is the page of bill 2025/114 (finance bill 2026) and of the law that came from it, with the legislative schedule (office, committee sittings, joint plenary sittings), the final committee report and the Official Gazette reference. Initiator: the Presidency of the Republic. Other bills and laws are under `arp.tn/loi/...` (project and proposal lists).
- **Law:** Law n. 2025-17 of 12 December 2025 (finance law 2026), Official Gazette n. 148, pp. 4231-4331; the wealth tax is **article 88** (pp. 4254-4255). PDF: `https://arp.tn/document/download/115725`. The bill's article 50 became article 88 after the plenary renumbered the articles. Press pages also mention an unrelated "additional article 50" voted on 2 December (customs duties on aluminium panels, per Tuniscope and Echaab, not checked): do not mix them.
- **Bill PDF** (156 pages): `https://arp.tn/document/download/115251` (article 50 not searched yet).
- **Explanatory note** of the tax administration (DGELF), *Note générale n° 13 de 2026*, 11 June 2026: `https://jibaya.tn/wp-content/uploads/2026/06/مذكرة-عامة-عدد-13-لسنة-2026.pdf` (read; garbled glyphs but legible).
- **Predecessor:** decree-law 2022-79 (finance law 2023) article 23, the real estate wealth tax.
- **Search terms:** Arabic *الضريبة على الثروة*, *الأداء على الثروة*, *الفصل 50*, *الفصل 88*, *مشروع قانون المالية لسنة 2026*; French *impôt sur la fortune*, *article 50*, *article 88*, *PLF 2026*.

## 2. Debates and votes

- **Committee minutes** (محضر جلسة, finance and budget committee) are PDFs at `https://arp.tn/ar_SY/document/download/<id>`: 115855 (4 November, Finance Ministry mission), 115857 (11 November, the Finance Minister presents the tax), 115861 (14 November, professional bodies), 115863 (15 November, employers' and other bodies), 115865 (17 November), 115867 (18 November), 115869 (19 November), 115871 (20 November), **115873 (21 November: joint sitting on article 50 with each committee's vote)**, 117050 (24 November), 117054 (25 November). The minutes summarise what speakers said without naming deputies; the joint sitting of 21 November names no member who voted. Ids come from the bill page's schedule; the 22 November minutes were not found (115875 and 115877 are 404).
- **Plenary:** the joint plenary sittings began 28 November, with the first vote on article 50 on 1 December (30 for, 14 abstentions, 69 against, 113 present, per La Presse), the minister's re-tabled article voted on 4 December (72 for, 14 against, 16 abstentions) and the whole law (89 for, 23 against, 12 abstentions). No per-member list and no plenary minutes found on arp.tn. `arp.tn/blog/1/post/<id>` carries a summary of each sitting (for example 2 December: `02-2025-2026-9334`, no wealth tax passage); the debate archive and videos were not searched.
- **Standing order:** article 112 lets the initiator re-table an article, which is how the minister brought article 50 back.
- **Joint sittings:** the finance committees of the ARP and of the CNRD examine the bill together before the plenary; their votes are counted separately, which caused the dispute of 21 to 28 November.

## 3. Members, parties, seats

- **ARP:** `https://arp.tn/deputies` (names, Arabic only, about 156 in the "المباشرون" tab) and `https://arp.tn/blocs` (404). Blocs, not parties, structure the chamber. The page is rendered by a script; the full HTML carries the list.
- **CNRD:** `https://www.cnrd.tn/قائمة-النواب/` (77 rows: name, governorate, region; no party), used for the Seats tab. Committee pages are on the same site.
- Wikidata coverage of 2023 members was not checked.

## 4. Other official records

- Ministry of Finance (`finances.gov.tn`) and DGELF notes (`jibaya.tn` hosts the PDFs). The Court of Audit and the Constitutional Court were not searched.

## 5. Access notes

- Press pages open to a plain client with a browser User-Agent; allAfrica and Al-Araby give 403.
- arp.tn documents download with a browser User-Agent. Read PDFs with `pypdf` when `pdftotext` drops Arabic glyphs; `wtdb.py checkquotes` may report a quote from such a PDF as not found.
- The `arp.tn/ar_SY/...` 404 page lists the real menu paths (`/deputies`, `/blocs`); old paths of the previous site no longer work.

## 6. Coverage log

| Date | Run | Documents read (title, number, date) | Result | Not read / open |
|---|---|---|---|---|
| 2026-11-11 | R001 | Finance committee minutes 11, 14 and 18 November 2025 (115857, 115861, 115867) | Minister's presentation of the tax (E00001); experts' objections (not recorded) | Committee minutes of 19 to 26 November; plenary minutes; JORT text of the law; DGELF note 13/2026 |
| 2026-11-11 | R002 | Minutes 115855, 115859, 115863, 115865, 115869, 115871, 115873 (21 November), 117050, 117054; Law 2025-17 (JORT 148, 115725); DGELF note 13/2026; bill page 4238; arp.tn sitting summary of 2 December | CNRD committee acceptance on 21 November (E00021); article 88 text read; no deputy named in any minute | Joint plenary record and videos of 28 November, 5 and 10 December; committee minutes of 22 November; bill PDF 115251 article 50; the final joint committee report |
