# Export, and things that went wrong before

This file holds sections 7, 8 of the skill. `skill/SKILL.md` keeps the section numbers as pointers to this file, so a reference such as "SKILL.md 6.7a" still finds it. Section numbers in the text below refer to the same numbering.

## 7. Export

The xlsx export contains: **Overview** (counts, grade mix, coverage and sweep progress, definitions); **Supporters** (one row per actor: grade, *explicit / named / appears to support*, designs, evidence count, first and latest evidence date, strongest source); **Evidence**; **Local coverage** (each geography unit with sweep status and supporter count); **Links**; **Profiles** (websites and socials); **Harvest lists**; **Run log**; **Former supporters** (latest stance retracted, shown only when there are some). There is no points score. Users filter by grade, type, level, prominence and date.

## 8. Things that went wrong before (avoid them)

- Actions typed outside the vocabulary, so the methodology no longer described the data → always use the controlled values; `validate` enforces them.
- Mansion-tax and council-tax supporters counted as wealth-tax supporters → apply section 2 to every piece of evidence.
- Opponents mixed into the supporter list → supporters only.
- Related tables existed only in the assistant's memory and never reached the file; earlier turns "compressed" in the log → write to disk continuously; log every run.
- Theme-by-theme, name-by-name searching gave few new actors per turn → bulk lists first, then the geography sweep, then snowballing.
- Reporters counted as supporters because they quoted one → journalists need opinion pieces.
- Notes full of "alive on the basis of..." and "no Wikidata match" on hundreds of rows, shown to readers on the site → `alive_checked=y` records the check; `validate` now warns when notes narrate it.
- Paraphrased "quotes": a roster import wrote its own sentence ("Campaign lists X as an endorser…") into 252 rows, because the fetch tool summarises pages → quote the page's own text, and run `checkquotes`.
- One bucket hid a group: all university economists were typed `academic`, so the Economist filter showed four people → type by discipline (`economist` for any economist) and use `other_types` for people who fit two.
- Near-duplicate organisations from different letters and rosters ("Coalition for Human Needs" and "Coalition on Human Needs") → `dedupe` after every large import, then `merge`.
- Party names written several ways ("Labour Party", "Labour", "Welsh Labour"; "Democratic-Farmer-Labor") → one common name per party, branches use the national name.
- Pages that said "tax the wealthy" but not wealth tax were nearly counted → apply section 2 to the speaker's own words.
- Progress reports that ignored higher-level units ("no geography units loaded") → `status` counts the lowest units of whatever depth you loaded.
- Pushing straight to `main` → branch and pull request.
- A run began by writing a crawler for 290 municipalities' protocols before the national legislature, parties and major organisations had been searched, because "every unit, no exceptions" was read as an order → touch every layer once first, sample local units, and build tooling only when a sample shows it pays (6.5).
- Several scoping questions asked one after another before any research → one short message with recommended defaults, then start.
- Brazil's seed pass shipped without a map because IBGE's own pages state no licence, though OCHA republishes the same IBGE shapes with IBGE codes under CC BY-IGO → check HDX and geoBoundaries before giving up on a map (section 5). The same run quoted the roll call's result line on all 136 vote rows, so no row proved its member's vote → quote the member's own entry on the per-member list (6.4).
- Countries were mapped at different depths (US and German maps stopped at states and Länder while the UK and Sweden went down to councils), so maps could not be compared and most local supporters had nowhere to go → load the local tier everywhere (6.7), whether or not you sweep it.
- Maps were built from whatever shapes were easiest to find: Sweden from a GitHub repository whose licence was "to be confirmed", India from a personal compilation with no licence and district codes invented for the project. Both had to be rebuilt → follow the map licence rule (section 5): an open licence and official codes, or no map.
- The UK's exhaustive council sweep was treated as the template for every country. It fits where councils pass motions and publish searchable minutes. Elsewhere, regional or local work should be proportionate to what the sample finds.
- Progress measured by units marked done rather than by supporters found and checked → report supporters, grades and checked rows.
- A review of the eleven country pull requests opened in one weekend removed rows in ten of them, and cut some sharply (Norway 299 to 145, Singapore 81 to 20, Japan 594 to 31). The same few patterns accounted for it → see section 4 ("Each person needs their own evidence") and run `review_scan.py`: a party platform copied onto every candidate and member (Japan, Singapore, Belgium); votes on a whole budget or on inheritance and financial taxes counted as wealth-tax votes, with birth dates in the quote (Norway); bibliography entries, paper titles and biography lines graded A (Norway, Belgium); coalition member lists and working-group members (Norway, Canada, Indonesia); exit-tax-only (China, Netherlands) and land, property and luxury-tax rows labelled partial_wealth (Nigeria); a party row whose cited page never mentioned the tax (Malaysia); a roster's update date used as the statement date (Canada); polls that were not about a wealth tax or could not be verified (Norway, Belgium); scratch scripts and caches committed (several).
- Spain's seed pass stopped the register at the autonomous communities and shipped without a map, and left all 58 deputies of a roll call at "Spain", because 6.3 warned against "loading hundreds of units" and the map step came last → the register and map are now step 4 of 6.1, `validate` fails without a local tier and warns about a missing map and about legislators at the root.
- A journalist went in at grade C for "those with most should contribute more", and a minister for opening a conference on wealth caps → grade C still needs words about wealth; vague fairness language and event programmes are exclusions or nothing.
