# Philippines: where the official record is and how to read it

Written in run R009 (2026-11-12). Country guide for maps and seats: `skill/references/countries/ph.md`. This file answers one question: **where is everything the House and Senate have put on record about wealth taxation, and how do I get all of it?** Nothing here is a source for a claim in the register; the register's own sources are.

## 1. Bills, motions and proposals

**House of Representatives: filed texts (works from a script).** `https://docs.congress.hrep.online/legisdocs/basic_<congress>/HB<5-digit number>.pdf`, for example `basic_20/HB04304.pdf` (20th Congress) and `basic_18/HB10253.pdf`. Plain `curl` with an ordinary browser user agent returns 200 and the PDF (tested 2026-11-12 for HB 4304, 8123, 8860, 9274 and 10253); `pdftotext -layout` reads them (text PDFs, not scans). The folder and the site root answer 403 (it is a bucket), so you cannot list; you need the number from the search below. A PDF is the bill as filed: it has the date and time stamp, the "Introduced by" line, the explanatory note and the articles. It does not hold committee referral, later co-authors or status.

**House: bill search and bill tracking (needs a real browser).** `https://www.congress.gov.ph/legislative-documents` (menu: Legislation > Legislative Documents > House Bills & Resolutions). `curl` gets a Cloudflare challenge (403). In the user's real Chrome (Claude in Chrome) the challenge clears by itself after a few seconds; from there:
- Search: POST form to `/legislative-documents` with `title` (substring of the title, English) and `congress` (`all`, `20`, `19` ... `8`) plus the page's `_token`. Each card gives number, title, date filed, principal authors, date read, primary referral and status ("Pending with the Committee on WAYS AND MEANS since 2026-03-03"). Run it from the page with `fetch` and parse the HTML; one query returns all hits (no paging seen up to 586 hits).
- History: `GET https://www.congress.gov.ph/bill/history?billno=HB04304&congress=20` returns an HTML fragment with the full title, principal authors, **co-authors with the date of the journal entry** (surname and initials only) and the first-reading referral. This is the page to cite for referral and co-authors.
- Members: `/house-members` (324 cards, official id such as `J078`), `/house-members/view/<id>` (district or party-list, authored and co-authored bills; no party for district members).
- Throttling: after about 170 requests in a few minutes the site answered 403 for roughly ten minutes. Keep to a few dozen requests and pause.
- Also listed in the menu and not yet read: House Journals, Order of Business, Committee Reports, Committee Meetings, Congressional Records.

**Senate.** `https://senate.gov.ph/legislative-documents/bills` (new site; `www.senate.gov.ph` loads in Chrome, curl gets 403). The old hosts `web.senate.gov.ph/lis/...` returned Cloudflare 523 (origin down) and `legacy.senate.gov.ph` returned a maintenance page on 2026-11-12. The page is a JavaScript app over a JSON endpoint: `GET /lis/documents_v2?document_type=bills|resolutions&congress=20th+Congress&search=<term>` (the `congress` value must read like `19th Congress`; `20th` alone is ignored; `search` matches the short title). It is slow (20 to 60 seconds) and began to return an HTML error after a few hundred calls. Run it from the page with `fetch` in a background loop and poll.

**Search terms (title match).** English: wealth, billionaire, super-rich, ultra, solidarity, net worth, affluent. Filipino terms were not tried. Beware: "wealth" also hits "Commonwealth Act", "National Wealth" (the 40 percent local share of natural-resource revenue, not a wealth tax), "ill-gotten wealth" and sovereign wealth fund bills; "ultra" hits "ultrasonic".

**Not reachable or not useful.** `congress.gov.ph/legisdocs/...` (403 to curl); `officialgazette.gov.ph` (403 to curl, not tried in Chrome); Wayback has no snapshots of the House PDFs or the search page (`archive.org/wayback/available` empty on 2026-11-12); `skill/scripts/fetch_page.py` could not be tried (playwright is not installed on this machine). Other user agents were not tried on purpose (no crawler impersonation).

## 2. Debates and votes

Not read. House Journal, Order of Business and committee hearing records for Ways and Means were not opened. The four bills below had no committee action beyond referral on the House search page on 2026-11-12.

## 3. Members, parties, seats

House: `/house-members` (official id, name, district or party-list). Party for district members comes from outside the House site (Wikipedia's list of current members, used only for party names). Senate: the Senate site lists senators and the Senate Bills filter has an author list.

## 4. Numbering quirks

`HB` = House Bill; the Senate uses `SBN-<n>` and lists House bills as `HBN-<n>`. House numbers restart each Congress (the 20th Congress runs July 2025 to 2028; 18th July 2019 to 2022): HB 10253 (18th) and HB 8123 (20th) are the same bill refiled. Bills are listed by filing date; "date read" is first reading, when the Speaker refers them to a committee. Wealth-tax bills go to the Committee on Ways and Means. Co-authors are added later by journal entry and appear only on the history page.

## 5. Wealth-tax bills found (House, all Congresses back to the 8th searched by title)

| Bill | Congress | Filed | Principal authors | Referral and status on 2026-11-12 |
|---|---|---|---|---|
| HB 10253 Super-Rich Tax | 18th | 2021-09-20 | Gaite, Zarate, Cullamat, Castro, Brosas, Elago | Ways and Means since 2021-09-22 |
| HB 4304 Solidarity Contribution | 20th | 2025-09-03 | Cendaña, Diokno, Ismula, Bag-ao; 25 co-authors 2026-05-26 to 2026-11-09 | Ways and Means since 2025-09-08 |
| HB 8123 Billionaire Wealth Tax | 20th | 2026-02-26 | Tinio, Elago, Co | Ways and Means since 2026-03-03 |
| HB 8860 PATAS Act (income tax relief, solidarity wealth tax, windfall tax) | 20th | 2026-04-14 | Mendoza | Ways and Means since 2026-05-04 |
| HB 9274 Ultra-Wealth Tax | 20th | 2026-05-18 | De Lima | Ways and Means since 2026-05-20 |

No House bill from the 8th to 17th Congresses and no 19th Congress bill matched; no Senate bill matched (searches in section 1; the Senate sweep was cut short by throttling).

## 6. Coverage log

| Date | Run | Documents read | Result | Not read / open |
|---|---|---|---|---|
| 2026-11-12 | R009 | HB 4304, 8123, 8860, 9274 (20th) and HB 10253 (18th), filed texts, full text; House history pages of the same five; House members list | Five bills identified; referral and status found; 25 HB 4304 co-authors printed on the history page | Resource pages for HB 4304, 8123, 9274, 10253 rewritten and HB 8860 added; 24 co-author supporters (A0051-A0074, E00053-E00076) added from the history page; `checkquotes` skipped them (the page needs a browser) so the quotes were taken from the page text in Chrome |

## 7. Known gaps and next steps

- Finish the Senate sweep (terms with `tax`, Filipino terms, resolutions); the endpoint throttled after about 130 searches.
- Read the House Journal and Ways and Means hearing records for the five bills.
- HB 4304 co-author "Yap (G.)" is ambiguous between three members and is not in the register; `Gonzales (A.)` was read as Alexandria Gonzales and `Gonzales (A. M.)` as Alyssa Michaela Gonzales.
- Party names of the co-authors come from Wikipedia's list of current members, not from the House site.
