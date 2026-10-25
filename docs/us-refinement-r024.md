# US refinement R024 — 25 October 2026

Refined the remaining 45 supporters flagged for visible-seat verification: eight senators and 37 representatives. Together with R023, all 105 supporters currently lighting federal seats have a completed refinement pass dated 25 October 2026. This is one 45-person batch, within the skill's 30–80 range, chosen to finish the visible federal seats before moving into the more varied link and state/local-office queue.

## Results

| Measure | Result |
|---|---:|
| Supporters refined in this run | 45 |
| Public profile links added | 118 |
| Official actor website fields filled | 45 |
| Names repaired | 2 |
| Substantive current-office corrections | 1 |
| Former office rows added | 1 |
| Places made geographically finer | 0 |
| New evidence rows | 9 (7 A, 2 B) |
| Actor grade upgrades / retractions | 0 / 0 |
| Supporters still without links | 470 |
| Supporters / evidence / profiles / positions after run | 873 / 1,300 / 1,650 / 461 |

A0307 is **Delia C. Ramirez**, not “Q58416610”; A0330 is **Maxine Dexter**, not “Q96777172”. The official House names were matched through Bioguide IDs R000617 and D000635, respectively, also present in the corresponding Wikidata claims. Their current seats are IL-03 and OR-03. Existing IDs and all evidence were preserved.

Adam Schiff's actor entry now says **US Senator (D-CA)** instead of representative for CA-30, and his map location reflects his statewide seat. His former House service, 3 January 2001 to 8 December 2024, was added as `current=n` from the [official House biography](https://history.house.gov/People/Listing/S/SCHIFF%2C-Adam-%28S001150%29/). The biography covers his House service across multiple districts, so that historical position is recorded at California level without inventing a single district for the whole period.

New links comprise 37 official House pages, 17 websites not already present as equivalent profile URLs, 17 Facebook, 13 Instagram, 13 YouTube, 10 X, nine Bluesky, one LinkedIn and one TikTok link. All 45 actor website fields were filled from the chamber directories, including websites already present in profiles. Rejected sharing controls, embedded posts, House Democrats accounts, an empty YouTube placeholder and a retweeted account belonging to another representative.

## Evidence added

- Six A rows: Nadler, Huffman, Dean, Frost, Casar and Ramirez formally cosponsored H.R. 4919, the Oligarch Act of 2023. Used each member's own name and sponsorship date from [official bill-status XML](https://www.govinfo.gov/bulkdata/BILLSTATUS/118/hr/BILLSTATUS-118hr4919.xml). The bill's annual tax on net wealth was already verified in R023; this run fetched the roster again and added only previously absent evidence for selected supporters.
- Schiff, August 2026, B: directly calls for a federal wealth tax in [an interview excerpt published by his office](https://www.schiff.senate.gov/news/press-releases/icymi-sen-schiff-says-trump-owns-status-quo-while-democrats-are-focused-on-affordability-at-politico-california-summit/). The office published the excerpt on 19 August; the row uses month precision because the original interview day was not independently confirmed. No rate or threshold in that statement, so existing A sponsorship evidence remains the basis of his best grade.
- Moulton, 12 December 2025, B: [his own affordability-agenda release](https://sethmoulton.com/moulton-rolls-out-affordability-agenda-amid-rising-costs/) explicitly proposes a national wealth tax on mega-millionaires. No rate or precise threshold in the release. This supplies newer support than his previous 2023 evidence. Earlier criticism of wealth taxes does not establish a current reversal in light of his later proposal.
- Fetterman, 30 September 2025, A: [his own release and statement](https://www.fetterman.senate.gov/fetterman-colleagues-reintroduce-the-billionaires-income-tax-act/) support the named Billionaires Income Tax Act, an included unrealised-gains design. This supplements the existing formal sponsorship record with his own public statement.

Thirty-six selected supporters received no new evidence. Existing recent qualifying evidence was retained where targeted own-site searches and page reviews provided no distinct addition. No statement was inferred from party membership, generic tax language or an event appearance. The 2025 Gomez income-bracket amendment surfaced in search but was not added as wealth-tax evidence. No retraction was established in this targeted review.

## Source checks and limits

Reused the same-day whole-country Wikidata identity/profile work from R023 rather than repeating unchanged or ambiguous matches. Freshly retrieved the [House Clerk roster](https://clerk.house.gov/Members/ViewMemberList), [House XML](https://clerk.house.gov/xml/lists/MemberData.xml), [House website directory](https://www.house.gov/representatives), and [Senate XML](https://www.senate.gov/general/contact_information/senators_cfm.xml). Opened every selected House member's Clerk profile and official website. Senate homepages returned 403; their membership, party, state and official website were verified from the Senate's own roster, retrieved through Jina Reader.

Ran `seats_us.py --dry-run`: it still reports 105 current supporters and 20 former. The refresh was not allowed to rewrite the files because that would replace R023's directly verified source URLs and drop its added historical House position. This run manually updates only the 45 selected current positions and adds Schiff's former House position. The charts' totals and party splits did not change. The run focuses on current congressional offices and the discovered stale House role; it does not claim an exhaustive reconstruction of every member's lifetime state/local career.

Quote verification: the standard checker found all six XML quotes; the three prose pages were blocked to its HTTP client and were reported as skipped, not as passes. Verified the Moulton and Fetterman quotes against freshly retrieved raw Jina text carrying their original source URLs. Verified Schiff's exact sentence on the official page in the web reader. All nine new quotations have therefore been checked; three required alternative readers.

Archive outcome: all four source URLs have snapshots, now recorded on all nine new rows. The register has 613 evidence rows with archive URLs and 687 without.

## Validation and continuation

- Database validation: zero errors, with the same two pre-existing warnings (short E01065 quote and missing party for A0268).
- Full local site build: passed. No deployment.
- Duplicate scan: 22 suggested pairs concern distinct people or organisations/chapters; no merge was made.
- File comparison: no actors added or removed; only the selected 45 actor records changed; existing evidence retained, with archive URLs the only permitted updates to old rows. At most one new evidence row per selected person.
- The regenerated queue has no remaining visible-seat verification flags. Next: Roxanne Brown, Porter McConnel, older wealthy signers where public-role eligibility permits enrichment, Abdul El-Sayed, then the ranked California state/local office gaps. There remain 334 unchecked position rows and five pre-2020 support cases outside these federal batches.
- PR is based on `codex/refine-us-r023` because that run's PR was still open when work began. No merge or deployment was performed. Temporary batch files and fetched pages remain outside the repository.

## Per-supporter outcomes

All rows below have a checked current office, party and seat; an official actor website; and `refined=2026-10-25`. Link counts are additions in profiles, not the number of existing links re-read.

| ID | Supporter | Links added | New evidence | Outcome / limits |
|---|---|---:|---:|---|
| A0305 | Jerrold Nadler | 2 | 1 | Office and linked professional accounts verified |
| A0307 | Delia C. Ramirez | 4 | 1 | Replaced QID-only name using matched official roster ID |
| A0308 | Adam Schiff | 1 | 1 | Corrected Senate role and statewide location; retained former House office; Homepage blocked; Senate roster verified |
| A0309 | Jill N. Tokuda | 4 | 0 | No distinct new qualifying evidence added |
| A0311 | Maxine Waters | 1 | 0 | No distinct new qualifying evidence added |
| A0312 | Chris Deluzio | 4 | 0 | No distinct new qualifying evidence added |
| A0313 | Yassamin Ansari | 7 | 0 | No distinct new qualifying evidence added |
| A0314 | Madeleine Dean | 6 | 1 | Office and linked professional accounts verified |
| A0317 | Maxwell Frost | 4 | 1 | Office and linked professional accounts verified |
| A0318 | Adelita Grijalva | 5 | 0 | No distinct new qualifying evidence added |
| A0319 | Robin Kelly | 1 | 0 | No distinct new qualifying evidence added |
| A0320 | Linda Sánchez | 2 | 0 | No distinct new qualifying evidence added |
| A0321 | Lateefah Simon | 5 | 0 | No distinct new qualifying evidence added |
| A0322 | Melanie Stansbury | 1 | 0 | No distinct new qualifying evidence added |
| A0325 | Greg Casar | 4 | 1 | Office and linked professional accounts verified |
| A0330 | Maxine Dexter | 2 | 0 | Replaced QID-only name using matched official roster ID; No distinct new qualifying evidence added |
| A0331 | Tammy Duckworth | 0 | 0 | Homepage blocked; Senate roster verified; No distinct new qualifying evidence added |
| A0332 | Tina Smith | 0 | 0 | Homepage blocked; Senate roster verified; No distinct new qualifying evidence added |
| A0333 | Chris Van Hollen | 0 | 0 | Homepage blocked; Senate roster verified; No distinct new qualifying evidence added |
| A0334 | Ron Wyden | 0 | 0 | Homepage blocked; Senate roster verified; No distinct new qualifying evidence added |
| A0337 | Tammy Baldwin | 0 | 0 | Homepage blocked; Senate roster verified; No distinct new qualifying evidence added |
| A0339 | John Fetterman | 0 | 1 | Homepage blocked; Senate roster verified |
| A0342 | Jack Reed | 0 | 0 | Homepage blocked; Senate roster verified; No distinct new qualifying evidence added |
| A0344 | Rosa DeLauro | 1 | 0 | No distinct new qualifying evidence added |
| A0345 | Betty McCollum | 2 | 0 | No distinct new qualifying evidence added |
| A0346 | John Garamendi | 3 | 0 | No distinct new qualifying evidence added |
| A0347 | Kevin Mullin | 8 | 0 | No distinct new qualifying evidence added |
| A0348 | Greg Landsman | 4 | 0 | No distinct new qualifying evidence added |
| A0349 | Mary Gay Scanlon | 4 | 0 | No distinct new qualifying evidence added |
| A0350 | Yvette Clarke | 6 | 0 | No distinct new qualifying evidence added |
| A0351 | Jared Huffman | 2 | 1 | Office and linked professional accounts verified |
| A0352 | Donald Norcross | 2 | 0 | No distinct new qualifying evidence added |
| A0354 | Nikki Budzinski | 4 | 0 | No distinct new qualifying evidence added |
| A0355 | John B. Larson | 1 | 0 | No distinct new qualifying evidence added |
| A0356 | Nanette Barragán | 3 | 0 | No distinct new qualifying evidence added |
| A0358 | Jimmy Gomez | 5 | 0 | No distinct new qualifying evidence added |
| A0359 | Mark Pocan | 1 | 0 | No distinct new qualifying evidence added |
| A0360 | Bill Foster | 1 | 0 | No distinct new qualifying evidence added |
| A0361 | Seth Moulton | 1 | 1 | Office and linked professional accounts verified |
| A0363 | Nikema Williams | 6 | 0 | No distinct new qualifying evidence added |
| A0366 | André Carson | 1 | 0 | No distinct new qualifying evidence added |
| A0367 | Troy Carter | 4 | 0 | No distinct new qualifying evidence added |
| A0368 | Lori Trahan | 2 | 0 | No distinct new qualifying evidence added |
| A0370 | Ted Lieu | 2 | 0 | No distinct new qualifying evidence added |
| A0371 | Dina Titus | 2 | 0 | No distinct new qualifying evidence added |
