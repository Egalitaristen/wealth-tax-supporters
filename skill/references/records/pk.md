# Pakistan: where the official record is and how to read it

Seed pass record notes (R001, November 2026).

## 1. Bills, motions and proposals

- **National Assembly Acts and Bills Register:**
  - URL: `https://na.gov.pk/en/bills.php` (government and private member bills) and `https://na.gov.pk/en/acts-tenure.php` (enacted Acts).
  - Search: Browse by National Assembly tenure (e.g. 14th National Assembly 2013–2018 for Act XXII of 2013, Income Support Levy Act).
  - Act XXII of 2013 (Income Support Levy Act): Enacted on 2013-06-30 as part of the Finance Act 2013. Repealed by Finance Act 2014.
- **Senate of Pakistan Bills:**
  - URL: `https://senate.gov.pk/en/bills.php`
- **Search terms:**
  - English: `wealth tax`, `Income Support Levy`, `Capital Value Tax`, `net wealth`, `Finance Act`.
  - Urdu: `ویلتھ ٹیکس`, `انکم سپورٹ لیوی`, `دولت پر ٹیکس`.
- **Government proposals and consultations:**
  - Ministry of Finance: `https://finance.gov.pk` (Budget speeches, Economic Surveys, Federal Budget in Brief).
  - Federal Board of Revenue: `https://fbr.gov.pk` (FBR Year Books, Statutory Regulatory Orders / SROs).

## 2. Debates and votes

- **Plenary Hansards (National Assembly):**
  - URL: `https://na.gov.pk/en/debates.php`
  - Format: PDF files per sitting, containing verbatim speeches in English and Urdu.
  - Speaker labels: Typically formatted as `Mr. Speaker:`, `Senator Mohammad Ishaq Dar (Minister for Finance):`, `Mr. Asad Umar:`.
- **Plenary Hansards (Senate of Pakistan):**
  - URL: `https://senate.gov.pk/en/debates.php`
  - Note: Senate website direct access may be blocked or rate-limited from outside Pakistan; use web archive mirrors or headless browser.
- **Roll calls:**
  - In Pakistan parliamentary practice, named roll-call division votes are infrequent. Most clauses of Finance Bills are passed by voice vote ("Ayes" vs "Noes"). When a division is demanded by members, the names of members voting Aye and No are printed in the day's verbatim debate minutes.
- **Committees:**
  - Senate Standing Committee on Finance, Revenue and Economic Affairs: Reviews annual Finance Bills and submits recommendations to the National Assembly. Reports are published on the Senate website under Committee Reports (`https://senate.gov.pk/en/committeereports.php`).

## 3. Members, parties, seats

- **National Assembly Members:**
  - Official roster: `https://na.gov.pk/en/all_members.php` (current term) and archived rosters for earlier assemblies.
  - 336 seats: 266 general constituencies, 60 reserved for women, 10 reserved for religious minorities.
- **Senate Members:**
  - Official roster: `https://senate.gov.pk/en/current_members.php`.
  - 96 seats: 23 per province (14 general, 4 technocrats/ulema, 4 women, 1 non-Muslim) and 4 for Islamabad Capital Territory.
- **Wikidata coverage:** High coverage for National Assembly and Senate members, ministers, and prime ministers.

## 4. Other official records

- **Economic Advisory Council (EAC):** Recommends macroeconomic and fiscal policy directly to the Prime Minister and Finance Minister; recommended wealth tax revival in April 2011.
- **Supreme Court of Pakistan:** Rulings on taxation powers between Federation and Provinces under the 18th Amendment (e.g. rulings on Section 7E deemed income tax on immovable property). Case citations published in *All Pakistan Legal Decisions* (PLD) and *Pakistan Tax Decisions* (PTD).

## 5. Access notes

- **Network reachability:** `senate.gov.pk` and `tribune.com.pk` may drop connections or present Cloudflare challenges to automated scripts. Use archived snapshots on `web.archive.org` or respectful user-agent headers.
- **Tools that worked:** `wtdb.py checkquotes`, `wtdb.py validate`, custom redirect interceptor in scratch for tracking canonical news URLs.

## 6. Coverage log

| Date | Run | Documents read (title, number, date) | Result (rows added, votes found) | Not read / open |
|---|---|---|---|---|
| 2026-11-10 | R001 | Income Support Levy Act, 2013 (Act No. XXII of 2013), 2013-06-30 | Enacted 0.5% wealth levy on net movable assets over Rs 1 million; repealed 2014 | Plenary Hansard debate for Finance Act 2013 |
| 2026-11-10 | R001 | Public Support for Wealth and Progressive Taxes in Pakistan (ICTD Policy Brief 17), 2025-06-01 | Survey of 7,500 Pakistani adults finding 42% support for general wealth tax | Full technical econometric working paper |

## 7. Known gaps and next steps

- Detailed inspection of the 14th National Assembly budget debate verbatim transcripts (June 2013 and June 2014) to document opposition and treasury interventions on the Income Support Levy.
- Track FBR working papers on the 2024-2025 movable wealth tax proposal rejected by the IMF.
- Inspect provincial assemblies (Punjab Assembly, Sindh Assembly) for debates on agricultural wealth and urban property taxation.
