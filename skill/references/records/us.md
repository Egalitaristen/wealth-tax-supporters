# United States: where the official record is and how to read it

Written in run R038 (8 November 2026, the records pilot). Every method below was tested from a Windows machine with plain `urllib`/`curl` unless it says otherwise. Nothing here is a source for a claim in the register; the register's own sources are. Country notes (maps, seats, state sources for the first sweeps) are in `references/countries/us.md`.

**What counts.** The register counts an annual or one-off tax on net wealth. Income-type designs do not count, even when the sponsor calls them a billionaires tax: the Billionaire Minimum Income Tax, the Billionaires Income Tax (mark-to-market), minimum taxes on realised income, capital-gains realisation rules (ROBINHOOD Act), estate and gift taxes ("Taxing Dynastic Wealth"). Earlier runs recorded the mark-to-market bills as `unrealised_gains`; the pilot brief says they do not count, so those rows are flagged in the area profile for a decision.

## 1. Bills, motions and proposals

**Federal bills: the sure way.**

| Method | Works? | Notes |
|---|---|---|
| GovInfo search API `POST https://api.govinfo.gov/search?api_key=DEMO_KEY` with a JSON body `{"query": "collection:(BILLS) AND title:(\"wealth tax\") ...", "pageSize":100, "offsetMark":"*"}` | Yes | Returns bill versions with `packageId` (`BILLS-119hr2912ih`). **DEMO_KEY allows about 10 calls an hour**, then answers 429. A personal key from api.data.gov removes that limit. Page with the returned `offsetMark`. |
| Bill text `https://www.govinfo.gov/content/pkg/BILLS-119hr2912ih/html/BILLS-119hr2912ih.htm` | Yes | Not rate limited. Read the operative section (`IMPOSITION OF ... TAX`) to apply the definition; the title can mislead (Health Over Wealth, Sovereign Wealth Fund bills are unrelated). |
| Bill status XML `https://www.govinfo.gov/bulkdata/BILLSTATUS/{congress}/{hr|s|hres}/BILLSTATUS-{congress}{type}{number}.xml` | Yes | `sponsors/item/fullName` and `cosponsors/item/fullName` print as `Rep. Lee, Summer L. [D-PA-12]`; `sponsorshipDate`, `isOriginalCosponsor`, `sponsorshipWithdrawnDate` (skip withdrawn ones). A clean grade A quote. `fullName` can carry accents (`García`): keep them. |
| congress.gov bill pages and search | **No (403)** | Bot protection. Needs a browser; not tried here. |
| congress.gov API `api.congress.gov/v3` | **Timed out** from this machine, with DEMO_KEY | Not usable here; needs a key and a working route. |
| Congressional Record "Public Bills and Resolutions" listing (one per introduction day) | Yes | Gives the sponsor and first cosponsors and the bill's one-line title, quickest way to find a bill introduced in a given week. |

**Search terms** (English; no other language is official federally): `wealth tax`, `net worth tax`, `Ultra-Millionaire Tax`, `tax on net wealth`, `extreme wealth`, `pandemic wealth tax`, `billionaires tax`, `Billionaires Income Tax` (find it, then exclude), `Make Billionaires Pay`, `Oligarch Act`. "Billionaire Minimum Income Tax" is not a wealth tax: apply the definition, do not search for it as one. Bills with a name that sounds like a wealth tax but is not: Donald J. Trump Wealth Tax Act (H.R. 2143, 8316: protest bills), Strengthen Social Security by Taxing Dynastic Wealth Act (estate tax), ROBINHOOD Act (capital-gains rule), Babies over Billionaires (mark-to-market income tax).

**Bills found (all documents are in `data/us/documents.csv`):** Ultra-Millionaire Tax Act 2021, 2024, 2026; Make Billionaires Pay Their Fair Share Act 2026; Oligarch Act 2023 and 2025; Make Billionaires Pay Act 2020 (one-time tax on the rise in billionaires' wealth); H.Res. 1028 (2026), which names a wealth tax among measures.

**State bills.** Reachable by scripts: Washington (`lawfilesext.leg.wa.gov` bill text, `app.leg.wa.gov/billsummary`, `wslwebservices.leg.wa.gov` SOAP/XML), Maryland (`mgaleg.maryland.gov` details page and PDFs), Minnesota (`revisor.mn.gov/bills/bill.php?b=House&f=HF4616&ssn=0&y=2026`, authors as links to `house.mn.gov/members/profile/ID`), Hawaii (`capitol.hawaii.gov/session/measure_indiv.aspx`), Vermont (`legislature.vermont.gov`), Connecticut (`cga.ct.gov`), Colorado (`leg.colorado.gov/bills`), New York (`legislation.nysenate.gov/pdf/bills/YEAR/S165`; the Assembly pages at `nyassembly.gov/leg/?bn=A03632&term=2025...`), Illinois bill-status XML (`my.ilga.gov/ftp/legislation/104/BillStatus/XML/...`, worked in an earlier run), California ballot measure documents (`vig.cdn.sos.ca.gov/2026/general/pdf/prop40-title-summ-analysis.pdf`, `lao.ca.gov/BallotAnalysis`). Blocked or failed: `leginfo.legislature.ca.gov` (403), `legiscan.com` (403), `nysenate.gov` HTML pages (403), the NY Senate API (401, key needed), `malegislature.gov`, `webserver.rilegislature.gov` and `ilga.gov` (connection timed out here, though the Rhode Island and Illinois files were readable in earlier runs), NCSL (403). Hawaii bills reached through fastdemocracy.com in an earlier run.

State search terms: `wealth tax`, `net worth tax`, `tax on extreme wealth`, `billionaire tax`, `financial intangible assets` (Washington's design), `wealth asset tax` (Hawaii), `mark-to-market` (New York, Illinois, Vermont: income-tax design, see above).

**Sponsors and cosponsors.** Federal: bill status XML (above). State: the bill page's sponsor line or `Authors` list; compare the list with the register (the run compared Minnesota HF 4616: 17 authors, 16 in the register).

**Government proposals and consultations.** The President's budgets proposed a minimum income tax on billionaires (not a wealth tax). JCT (`jct.gov`) and CBO (`cbo.gov`) answer 403 to scripts: revenue estimates have to come from a browser or from Penn Wharton and Saez-Zucman letters already in the Resources page.

## 2. Debates and votes

**Hearings and reports.** GovInfo collections `CHRG` (hearings), `CRPT` (reports), `CPRT` (committee prints, JCT). Search with the same POST call and `collection:(CHRG OR CRPT OR CPRT) AND ("wealth tax" OR ...)`; the full transcript is at `https://www.govinfo.gov/content/pkg/CHRG-117shrg48668/html/CHRG-117shrg48668.htm` (also `/pdf/...pdf`). The text is monospaced with speaker labels like `Senator Warren.`, `Dr. Disney.`, `Chairman Sanders.` followed by the speech. **Beware:** after the oral part, submitted statements and "Questions for the record" are printed with the last speaker's label; a hit there belongs to the witness or letter-writer named in the heading, not to the labelled senator. The wealth-tax hearings so far found: Senate Finance subcommittee on Fiscal Responsibility and Economic Growth, 27 April 2021 (Warren chair; the main one); Senate Budget Committee, 17 and 25 March 2021 and 18 April 2023. `senate.gov` and committee sites (`finance.senate.gov`, `budget.senate.gov`) answer 403 to scripts, so use GovInfo. House committee pages at `docs.house.gov/Committee/Calendar` answer scripts but were not swept.

**Floor debate.** Congressional Record by granule: `https://www.govinfo.gov/content/pkg/CREC-2026-03-19/html/CREC-2026-03-19-pt1-PgS1314.htm` (HTML, one speaker label per speech: `Mr. SANDERS.`). Find granules with the search API (`collection:(CREC)`). **The GovInfo search is incomplete for this topic:** 138 granules came back for 2010-2026, among them only two relevant speeches, while Sanders and Warren spoke about the wealth tax on the floor many times in 2019-2021. The complete list needs a Congress.gov Congressional Record search in a browser (open lead D0002). The `.../pdf/...pdf` versions are real text PDFs and work with `gazette_scan.py`; the HTML is easier to read.

**Roll calls.** House: `https://clerk.house.gov/evs/{year}/roll{NNN}.xml` works for scripts (per-member `<recorded-vote>` with name-id). Senate: `senate.gov/legislative/LIS/roll_call_votes/vote{congress}{session}/vote_{congress}_{session}_{NNNNN}.xml` and the vote menus return **403**; do not try to get around that. Substitute: Voteview (`https://voteview.com/static/data/out/rollcalls/S119_rollcalls.csv`, `H117_...`, and per-member `.../votes/S117_votes.csv`), which carries a short description (`vote_desc`, `dtl_desc`) and the member votes by ICPSR id. Scan the descriptions for `wealth|billionaire|net worth|ultra-?millionaire`: in the 112th to 119th Congress no vote is specific to a wealth tax. The closest are vote-a-rama amendments on "tax cuts for the ultra-rich" (S119 rolls 62, 63, 71) and "the wealthy pay their fair share" (S117 roll 319); their text was not read. The register therefore has **no vote rows for the US**, and that is a finding about the record, not a gap in the scan, with the caveat that vote-a-rama amendment texts are unread.

**Article numbering and block votes.** Not applicable: federal wealth-tax bills were never marked up or reported. A wealth tax appeared in no reconciliation bill; a vote on a reconciliation bill or budget resolution is a package vote and does not count.

## 3. Members, parties, seats

`python skill/scripts/seats_us.py data/us` rebuilds Congress seats and positions from the congress-legislators project (needs GitHub access; it ran in R038). Bill status gives the bioguide id (`S000033`) of each sponsor. State legislators: each legislature's member list; positions for them are bootstrapped from the role text and stay unchecked.

## 4. Other official records

- Ballot measures: the California Secretary of State voter guide (title, summary, Legislative Analyst, arguments), `vig.cdn.sos.ca.gov`. The Oregon initiative IP 70 and state ballot-measure files are in the area profile.
- Court rulings on the constitutionality of a federal wealth tax are not in the register; the Gamage testimony of 2021 argues the constitutional case.
- JCT and CBO: blocked to scripts (403); open in a browser.

## 5. Access notes

- Works for scripts: `api.govinfo.gov` (DEMO_KEY, ~10 calls an hour), `www.govinfo.gov/content/pkg/...` and `/bulkdata/` (no limit), `clerk.house.gov`, `voteview.com`, `docs.house.gov`, state sites listed above.
- Blocked or unusable here: `congress.gov` (403), `api.congress.gov` (timeout), `senate.gov` roll-call XML (403), `finance.senate.gov` and `budget.senate.gov` (403), `jct.gov` (403), `cbo.gov` (403), `leginfo.legislature.ca.gov` (403), `legiscan.com` (403), `nysenate.gov` pages (403). Those need a browser (`scripts/fetch_page.py` or Claude in Chrome) and were **not** opened in R038.
- Wikidata/Wikipedia are not used as sources.
- The GovInfo PDFs of hearings are real text; no OCR was needed.
- Tools: `scripts/gazette_scan.py` suits the Congressional Record PDFs only when a roll-call list is printed inside (rare in the US, since roll calls are separate documents); R038 used a short speaker-label scan of the HTML instead.

## 6. Coverage log

| Date | Run | Documents read | Result | Not read / open |
|---|---|---|---|---|
| 2026-11-08 | R038 | BILLSTATUS and text of 8 federal wealth-tax bills and 5 near-miss bills; 75 hearings/reports (GovInfo search) scanned, every hearing with three or more mentions read by speaker; 138 Congressional Record granules scanned; 8 voteview CSVs (112th-119th) scanned; Prop 40 SOS summary; Minnesota HF 4616 | 61 evidence rows (53 A, 8 B): 9 testimony/speech rows, 52 sponsor/cosponsor rows; 2 new actors; 3 exclusions; 0 vote rows | Congress.gov search of the Congressional Record; text of vote-a-rama amendments; House committee hearings; state hearings and floor debate; Massachusetts, Connecticut, Illinois, Colorado bill lists; JCT/CBO; the pre-2019 federal record beyond the title search |

Never write "no roll call" or "no statements" in the area profile unless this table shows the relevant sittings were read; here it shows they were not.

## 7. Known gaps and next steps

1. Congress.gov Congressional Record full-text search in a browser for `wealth tax`, 2019-2026, then download the granules from GovInfo and read the speakers (Sanders, Warren, Jayapal, Khanna, Whitehouse, Merkley, Markey).
2. Read the text of the vote-a-rama amendments (Senate budget resolutions: 2021 SCONRES14, 2025 SCONRES7 and HCONRES14) and compare the roll calls on those that propose a wealth tax or delete a Republican tax cut for the wealthy by naming one.
3. State hearings: Washington (House Finance hearing on HB 1473, 2023), Maryland HB 1238 (5 March 2026, Ways and Means), Hawaii SB 313 and SB 925 (Judiciary and Ways and Means), Minnesota HF 4616. Video only; testimony PDFs are sometimes posted.
4. Massachusetts, Connecticut, Illinois, Colorado, Oregon, Rhode Island: confirm bill lists when the sites answer.
5. A decision on the mark-to-market bills (NY, IL, VT and the federal Billionaires Income Tax): rows recorded as `unrealised_gains` in earlier runs.
6. Get a free api.data.gov key before repeating GovInfo searches.
