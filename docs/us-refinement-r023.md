# US refinement R023 — 25 October 2026

Refined the first 60 supporters selected by the refinement queue after the automatic pass: 17 senators and 43 representatives. All 60 have `refined=2026-10-25`. This run added no supporters and preserved all existing evidence fields except archive URLs.

## Results

| Measure | Result |
|---|---:|
| Profile links added | 131 (125 manual; 6 from Wikidata) |
| Supporters still without links, whole register | 470 (previously 471) |
| Official actor website fields filled | 60 |
| Current congressional positions verified against chamber sources | 60 |
| Former positions added | 1 (Peter Welch, House, 2007–2023) |
| Substantive role/district corrections | 4 |
| Places made geographically finer | 0 |
| Additional evidence rows | 11 |
| Grade upgrades / retractions | 0 / 0 |
| Evidence rows with archive URLs | 604 (previously 0) |
| Supporters / evidence / profiles / positions after run | 873 / 1,291 / 1,532 / 460 |

The four substantive corrections are Mark Takano (CA-39), Rashida Tlaib (MI-12), Mark DeSaulnier (CA-10), and Peter Welch (Senator for Vermont). Other role edits standardize district formatting. Correcting a district is not counted as adding geographic precision; Welch's location now reflects his statewide Senate seat.

Ten new grade A rows record formal cosponsorship of H.R. 4919, the Oligarch Act of 2023, using each member's own entry and sponsorship date in [official bill-status XML](https://www.govinfo.gov/bulkdata/BILLSTATUS/118/hr/BILLSTATUS-118hr4919.xml). The [bill text](https://www.govinfo.gov/content/pkg/BILLS-118hr4919ih/html/BILLS-118hr4919ih.htm) establishes an annual tax on net wealth with progressive rates of 2%, 4%, 6% and 8%. Added only selected supporters already in the register: Foushee, Raskin, Omar, Schakowsky, Watson Coleman, McGovern, Garcia, Tlaib, DeSaulnier and Lee. The eleventh row is Sanders's [1 April 2026 op-ed](https://www.theguardian.com/commentisfree/2026/apr/01/billionaire-wealth-tax-trump), advocating his 5% annual billionaire wealth tax.

## Sources and automatic pass

- `match_wikidata.py`: no new IDs; six ambiguous matches left blank (Robert Jackson, Kevin Parker, Lisa Davis, P Street, Robert Reich, UltraViolet).
- `profiles_wikidata.py`: seven candidate links for former senator Bob Casey, sourced to Wikidata Q887841. Retained six public profile links; omitted his former Senate website because live availability could not be established. These links do not imply that he remains in office.
- `wtdb.py locate`: no automatic location repairs required.
- `seats_us.py`: 105 supporters currently in Congress, 20 former. Verified the selected 60 using the [House Clerk member list](https://clerk.house.gov/Members/ViewMemberList), [House member XML](https://clerk.house.gov/xml/lists/MemberData.xml), [House website directory](https://www.house.gov/representatives), and [Senate member XML](https://www.senate.gov/general/contact_information/senators_cfm.xml). The House lists 217 Democrats, 221 Republicans, one Independent and two vacancies; the Senate lists 45 Democrats, 53 Republicans and two Independents. Totals agree with the existing charts, so no chart changes were needed.
- Opened all 43 selected House Clerk profiles and House homepages. Added professional account links from those pages after excluding party-wide accounts, sharing buttons, individual posts and embedded media.
- Senate XML was read through Jina Reader after a direct 403. Senator homepages generally returned 403 or an unauthorized page even through that fallback; no new social account was inferred from those responses. Existing Wikidata links remain available, and member websites were verified as links in the official roster.
- Archive lookup covered the first 20 distinct existing URLs: 18 snapshots found, filling 593 rows because many sources are shared. This was a bounded initial archive pass, not a complete sweep of every source. Both new source URLs had snapshots, filling all 11 new rows; 687 rows remain without archive URLs.
- The duplicate scan returned 22 possible pairs; the suggestions concern distinct people, chapters or organisations, so no merges were made.

## Evidence limits and next run

All 60 received an office, link and location review. Existing recent grade A bill sponsorship was retained where a quick own-site search or page review supplied no distinct improvement. Three additional statements per person is a cap, not a target. Forty-nine supporters received no new statement; that is not a finding that they have made no others.

Aisha Wahab remains B: her own campaign page contains a wealth-tax plank but is undated and gives no rate or threshold; an event appearance alone was not treated as an endorsement. Gillibrand's own 2021 release corroborates existing evidence, but searches supplied no newer qualifying statement. No reversal was established in these targeted checks. This was not an exhaustive search of every member's voting record or a complete reconstruction of every state/local office held throughout their careers; current federal offices were the batch priority.

The remaining 45 lit seats lead the regenerated next batch. A0307 and A0330 have Wikidata IDs in their name fields and need identity/name verification. Then follow the queue into missing links and unchecked state/local offices. The five pre-2020 cases remain outside this batch. Temporary batch CSVs and fetched pages are outside the repository.

## Validation

- Database validation: zero errors; two pre-existing warnings (short quote E01065 and missing party for A0268).
- New quote checks: 11 of 11 found; none missing, skipped or too short.
- Site build: passed, including the US directory and profiles. This is a local build; no deployment was performed.
- File comparison: no actors added, none removed; old evidence retained; new evidence limited to the selected batch and at most one new row per person.

## Per-supporter outcomes

Every row below has a verified current congressional position, an official website recorded and the refinement date set. “Blocked” describes direct homepage reading, not roster verification. New-link counts here exclude the six automatic links outside the batch.

| ID | Supporter | Manual links added | New evidence | Outcome / limits |
|---|---|---:|---:|---|
| A0740 | Aisha Wahab | 2 | 0 | Retained B; campaign plank undated |
| A0005 | Kirsten Gillibrand | 0 | 0 | Homepage blocked; official roster verified; No newer qualifying support found |
| A0315 | Valerie Foushee | 7 | 1 | Office and public links verified; existing seat location retained |
| A0316 | Laura Friedman | 5 | 0 | Office and public links verified; existing seat location retained |
| A0323 | Shri Thanedar | 6 | 0 | Office and public links verified; existing seat location retained |
| A0324 | Nydia M. Velázquez | 1 | 0 | Office and public links verified; existing seat location retained |
| A0326 | Chellie Pingree | 3 | 0 | Office and public links verified; existing seat location retained |
| A0327 | Analilia Mejia | 4 | 0 | Office and public links verified; existing seat location retained |
| A0328 | Teresa Leger Fernandez | 6 | 0 | Office and public links verified; existing seat location retained |
| A0329 | Adriano Espaillat | 3 | 0 | Office and public links verified; existing seat location retained |
| A0335 | Ben Ray Luján | 1 | 0 | Homepage blocked; official roster verified |
| A0336 | Angela Alsobrooks | 0 | 0 | Homepage blocked; official roster verified |
| A0338 | Richard Blumenthal | 0 | 0 | Homepage blocked; official roster verified |
| A0340 | Martin Heinrich | 0 | 0 | Homepage blocked; official roster verified |
| A0341 | Patty Murray | 0 | 0 | Homepage blocked; official roster verified |
| A0343 | Chris Coons | 0 | 0 | Homepage blocked; official roster verified |
| A0353 | Zoe Lofgren | 1 | 0 | Office and public links verified; existing seat location retained |
| A0357 | Jamie Raskin | 3 | 1 | Office and public links verified; existing seat location retained |
| A0364 | Val Hoyle | 5 | 0 | Office and public links verified; existing seat location retained |
| A0365 | Emanuel Cleaver | 1 | 0 | Office and public links verified; existing seat location retained |
| A0369 | Marcy Kaptur | 2 | 0 | Office and public links verified; existing seat location retained |
| A0372 | Bill Keating | 3 | 0 | Office and public links verified; existing seat location retained |
| A0373 | Seth Magaziner | 4 | 0 | Office and public links verified; existing seat location retained |
| A0616 | Al Green | 1 | 0 | Office and public links verified; existing seat location retained |
| A0001 | Elizabeth Warren | 0 | 0 | Homepage blocked; official roster verified |
| A0002 | Bernie Sanders | 0 | 1 | Homepage blocked; official roster verified |
| A0003 | Sheldon Whitehouse | 0 | 0 | Homepage blocked; official roster verified |
| A0004 | Jeff Merkley | 0 | 0 | Homepage blocked; official roster verified |
| A0006 | Brian Schatz | 0 | 0 | Homepage blocked; official roster verified |
| A0007 | Ed Markey | 0 | 0 | Homepage blocked; official roster verified |
| A0008 | Mazie Hirono | 0 | 0 | Homepage blocked; official roster verified |
| A0009 | Pramila Jayapal | 2 | 0 | Office and public links verified; existing seat location retained |
| A0010 | Brendan Boyle | 4 | 0 | Office and public links verified; existing seat location retained |
| A0113 | Chris Murphy | 0 | 0 | Homepage blocked; official roster verified |
| A0114 | Judy Chu | 2 | 0 | Office and public links verified; existing seat location retained |
| A0115 | Ro Khanna | 2 | 0 | Office and public links verified; existing seat location retained |
| A0272 | Ilhan Omar | 2 | 1 | Office and public links verified; existing seat location retained |
| A0273 | Alexandria Ocasio-Cortez | 2 | 0 | Office and public links verified; existing seat location retained |
| A0275 | Mark Takano | 3 | 0 | Corrected US Representative (D-CA-39) |
| A0277 | Jan Schakowsky | 2 | 1 | Office and public links verified; existing seat location retained |
| A0278 | Bonnie Watson Coleman | 2 | 1 | Office and public links verified; existing seat location retained |
| A0280 | Ayanna Pressley | 5 | 0 | Office and public links verified; existing seat location retained |
| A0281 | Jim McGovern | 3 | 1 | Office and public links verified; existing seat location retained |
| A0282 | Dwight E. Evans | 1 | 0 | Office and public links verified; existing seat location retained |
| A0283 | Chuy García | 5 | 1 | Office and public links verified; existing seat location retained |
| A0284 | Adam Smith | 1 | 0 | Office and public links verified; existing seat location retained |
| A0285 | Rashida Tlaib | 4 | 1 | Corrected US Representative (D-MI-12) |
| A0288 | Peter Welch | 1 | 0 | Corrected US Senator (D-VT); Homepage blocked; official roster verified |
| A0289 | Steve Cohen | 2 | 0 | Office and public links verified; existing seat location retained |
| A0291 | Grace Meng | 2 | 0 | Office and public links verified; existing seat location retained |
| A0292 | Mark DeSaulnier | 1 | 1 | Corrected US Representative (D-CA-10) |
| A0295 | Don Beyer | 3 | 0 | Office and public links verified; existing seat location retained |
| A0297 | Frank Pallone | 1 | 0 | Office and public links verified; existing seat location retained |
| A0298 | Alex Padilla | 0 | 0 | Homepage blocked; official roster verified |
| A0299 | Danny K. Davis | 2 | 0 | Office and public links verified; existing seat location retained |
| A0300 | Dan Goldman | 3 | 0 | Office and public links verified; existing seat location retained |
| A0301 | Glenn Ivey | 4 | 0 | Office and public links verified; existing seat location retained |
| A0302 | Jonathan Jackson | 2 | 0 | Office and public links verified; existing seat location retained |
| A0303 | Hank Johnson | 2 | 0 | Office and public links verified; existing seat location retained |
| A0304 | Summer Lee | 4 | 1 | Office and public links verified; existing seat location retained |
