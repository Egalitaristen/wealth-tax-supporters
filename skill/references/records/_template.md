# {Country}: where the official record is and how to read it

One file per country, `skill/references/records/<folder>.md`, written by whoever first reads that country's legislature in depth and kept up to date by every later run. It answers one question: **where is everything the parliament and government have put on record about wealth taxation, and how do I get all of it?** Country guides under `references/countries/` cover maps, seats and shortcuts; this file covers the record.

Rules for writing it: test every URL and method before listing it. Say what failed (403, captcha, JS-only app, scanned PDFs). Give the exact search terms in the local language. Keep it short enough to follow as a checklist. Nothing here is a source for a claim in the register; the register's own sources are.

## 1. Bills, motions and proposals

- **Register of bills** (name, URL, what it covers, from which year). How to list every bill, motion, amendment, petition and parliamentary question that mentions the tax: search URL pattern, filters, export, API.
- **Search terms** in each language (wealth tax, net wealth tax, fortune tax, millionaire tax, solidarity tax on large fortunes, one-off levy, plus the local tax name and the term for the article/section).
- **Sponsors and co-sponsors**: where the signed list is printed (bill page, annex, gazette) and its format.
- **Government proposals and consultations**: ministry of finance pages, impact assessments, expert commissions.

## 2. Debates and votes

- **Plenary and committee records**: URL pattern, format (HTML, PDF, scanned), whether they are searchable, how long after a sitting they appear, what the speaker labels look like (`Palabras del Senador X`, `Hon. Member for Y`).
- **Roll calls**: where named votes are published (per-member list, open data, PDF annex), their format, and how to read the result line. Note if only totals are published.
- **How articles are numbered across versions** (government bill, committee text, final law) and how to find the wealth-tax article in each.
- **Block and package votes**: how this legislature groups articles, and where amendments to delete or change the wealth-tax article are voted separately (those are article-specific; block votes are not).

## 3. Members, parties, seats

- Official member list per term (URL, format, party and seat data) and the identifier used by the legislature. Open-data or API endpoints, and Wikidata coverage.
- Where historic members (earlier terms) are listed.

## 4. Other official records

- Budget committee and audit office reports, central-bank or statistics office material, court rulings (constitutional challenges name the parties and their arguments), tax-administration statistics and consultations, local councils and regional parliaments.

## 5. Access notes

- What needs a browser, what blocks scripts, what the Wayback copy or a mirror gives. If a PDF is a scan, say so. Language of documents.
- Tools that worked: `scripts/gazette_scan.py` (PDF gazettes and minutes), `scripts/fetch_page.py`, an adapter under `scripts/adapters/`.

## 6. Coverage log

| Date | Run | Documents read (title, number, date) | Result (rows added, votes found) | Not read / open |
|---|---|---|---|---|

Never write "no roll call" or "no statements" in the register's area profile unless this table shows the relevant sittings were read.

## 7. Known gaps and next steps

- Terms, chambers, committees, regions or years not yet read; the order to read them in.
