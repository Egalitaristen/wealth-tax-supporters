# Australia: where the official record is and how to read it

Written in run R015 (2026-11-15). This file answers one question: **where is everything the Parliament of Australia (Senate and House of Representatives) and the Federal Government have put on record about wealth taxation, and how do I get all of it?** Nothing here is a source for a claim in the register; the register's own sources are.

Wealth-tax context: Australia has no federal recurrent net wealth tax. Proposals for a net wealth tax or billionaires' wealth tax have reached the federal Parliament primarily via Australian Greens urgency motions, private members' motions, Question Time questions, and budget/supply debates (notably the Greens' 6% billionaire tax in 2021–2022 and their PBO-costed 10% annual net wealth tax on billionaires announced in February 2025).

## 1. Bills, motions and proposals

- **Register of bills (Parliament of Australia):** `https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation` (blocks plain HTTP clients with 403 / bot checks; use a browser or search engines).
- **Parliamentary Budget Office (PBO):** `https://www.pbo.gov.au/` publishes costings of election commitments and minor-party proposals (including the Greens' billionaires tax).
- **Search terms (English):** `wealth tax`, `net wealth tax`, `billionaires tax`, `billionaire tax`, `tax billionaires`, `tax the 1%`.
- **Excluded look-alikes (Ground Rule 1):**
  - Capital gains tax (CGT) discount reform, negative gearing, and land tax / council rates (property-only or income/realised-gain taxes).
  - Division 296 / `$3 million superannuation` tax (applies to superannuation earnings, not general net wealth).
  - Petroleum Resource Rent Tax (PRRT) and corporate super-profits taxes.
  - Inheritance / estate taxes alone.

## 2. Debates and votes

- **OpenAustralia scraped XML (recommended for automated reading):**
  - **Senate debates:** `https://data.openaustralia.org.au/scrapedxml/senate_debates/YYYY-MM-DD.xml`
  - **House of Representatives debates:** `https://data.openaustralia.org.au/scrapedxml/representatives_debates/YYYY-MM-DD.xml`
  - Both directories are openly accessible without bot checks and updated within days of sittings. Each `<speech>` element carries `speakername`, `speakerid`, and `id` (e.g. `uk.org.publicwhip/lords/2025-02-11.119.6`).
- **OpenAustralia web UI & They Vote For You:**
  - `https://www.openaustralia.org.au/` and `https://theyvoteforyou.org.au/` return 403 / browser challenges to plain scripts; use Wayback Machine copies (`https://web.archive.org/web/2025id_/https://theyvoteforyou.org.au/...`) or a browser when needed.
- **Roll calls / divisions:**
  - Senate and House divisions are recorded in Hansard (`aph.gov.au`, blocked to scripts) and mirrored with per-member votes on `theyvoteforyou.org.au`.

## 3. Members, parties, seats

- **OpenAustralia member XMLs (openly accessible, updated regularly):**
  - `https://data.openaustralia.org.au/members/senators.xml` (includes `fromdate`, `todate`, `towhy`, `party`, `division`, `id`)
  - `https://data.openaustralia.org.au/members/representatives.xml`
  - `https://data.openaustralia.org.au/members/people.xml`
  - `https://data.openaustralia.org.au/members/websites.xml` (includes `aph_url` with `MPID=...` and `mp_website`)
- Note: `aph.gov.au/Senators_and_Members/Members` returns 403 to plain `curl`, so `seats.py data/australia` fails unless run against a mirror or browser. Use `data.openaustralia.org.au/members/` to verify sitting senators, MPs, party switches, and retirements.

## 4. Access notes

- `aph.gov.au`, `www.openaustralia.org.au`, `theyvoteforyou.org.au`, and `australiainstitute.org.au` block plain HTTP scripts (403 / Cloudflare challenge).
- `data.openaustralia.org.au` (raw XMLs for debates and members) is open to plain HTTP requests and is the fastest, cleanest way to read federal Hansard and verify seats.

## 5. Coverage log

| Date | Run | Documents read (title, number, date) | Result (rows added, votes found) | Not read / open |
|---|---|---|---|---|
| 2026-11-01 | R014 | Senate division 2025-02-11/2 (They Vote For You Wayback) | 12 ayes (6 existing, 7 new/updated rows) | House debates |
| 2026-11-15 | R015 | All 85 Senate XMLs & 104 House XMLs (2025–2026) scanned via `data.openaustralia.org.au`; key sittings read in full (`2025-02-10` House, `2025-02-11`, `2025-08-25`, `2026-06-22`, `2026-06-24`, `2026-08-17`, `2026-10-12` Senate) | Added Max Chandler-Mather, second statements for McKim, Shoebridge, Faruqi, Waters | Pre-2025 House/Senate XMLs (2010–2024) |
| 2026-11-15 | R016 | All 250 Senate XMLs & 296 House XMLs (2020–2024) scanned via `data.openaustralia.org.au`; 8 key sittings logged in `documents.csv` (`M0009`–`M0016`) | Added Janet Rice (Grade A 6% billionaires tax) and Stephen Bates (Grade B), plus 5 Hansard speeches for Bandt (Grade A), Allman-Payne, Cox, Whish-Wilson, Chandler-Mather | Pre-2020 House/Senate XMLs (2010–2019) |
| 2026-11-15 | R017 | All 1,115 Senate & House XMLs (2010–2019) scanned via `data.openaustralia.org.au` (114 keyword matches reviewed) | Confirmed 0 missed 2010–2019 federal net-wealth-tax supporters (federal Greens billionaires' wealth tax push began in 2021) | State/territory parliaments |

## 6. Known gaps and next steps

- Check state/territory parliaments (NSW, Victoria, Queensland, SA, WA, Tasmania, ACT, NT) for wealth-tax motions or speeches.
