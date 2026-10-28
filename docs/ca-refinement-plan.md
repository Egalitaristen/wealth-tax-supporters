# Canada refinement plan

Prepared 28 October 2026 from `refine/SKILL.md`, `skill/references/countries/ca.md` and the current `data/ca` files. A plan only: no data has been changed and no live source was opened. Counts come from the CSV files and `refine_queue.py`; a queue flag is a prompt to inspect, not proof of an error.

## Baseline

| Measure | Count |
|---|---:|
| Supporters | 287 (259 active, 28 `former_role`) |
| Evidence rows | 302 (grade A 270, B 32, no C) |
| Supporters refined | 0 |
| Levels | 132 national, 111 regional, 44 local |
| Latest-evidence years | 2025: 141, 2026: 34, 2020 to 2023: 117, before 2020: 4 |
| Links (`links.csv`) | empty |
| Open Canada leads | 0 (no `leads.csv`; `leads.py list --country ca` returns none) |
| Seats tab | House (343) and Senate (105), `seats.csv` already filled |

Queue gaps (284 actors, counts overlap): one statement 273, no links 219, coarse place 196, no Wikidata ID 94, weak grade 27, office 15, verify seat 8, still current 4.

The shape of the register decides the work. About 80 organisations and 60 or so "wealthy individuals" come from two bulk sources (the Quebec manifesto sample and the Millionaires/Patriotic Millionaires letter). They score low in the queue (about 11) and are single-statement signatories with no public role; the skill says to skip links for those. The real work is the few dozen prominent people and organisations.

## Canada-specific points to handle first

- **Commons site blocks scripts** (403, even curl). `seats.py` needs the member XML saved in a browser and passed with `--local "https://www.ourcommons.ca/Members/en/search/xml=<file>"`. Vote pages cannot be read by `checkquotes`: check by hand against Hansard.
- **Seats**: the House list does not include former members; those not listed get `current=n` with no end date, so dates must be found by hand. The Senate comes from the senators page JSON (needs the `X-Requested-With: XMLHttpRequest` header).
- **Seven top-ranked people are lit seats**: Don Davies (A0010), Leah Gazan (A0013), Gord Johns (A0017), Jenny Kwan (A0019), Heather McPherson (A0025), Kim Pate (A0235, Senate), Rosa Galvez (A0236, Senate), plus Elizabeth May (A0024). Confirm each holds the seat and party today. Check whether the NDP's 2025 seat loss and leadership change affected any of them.
- **Quebec**: search in French (`impôt sur la fortune`, `taxe sur les grandes fortunes`, `impôt sur le patrimoine`). Sources include the Assemblée nationale's Journal des débats and the Québec solidaire press room.
- **Place**: MPs at riding level (register unit is the CSD/region, riding in place text); provincial bodies at province; local actors by seven-digit CSDUID. Town level at most for private people. The "wealthy individuals" are already at province level and can stay there.
- **Encoding**: some place strings show a broken dash (`Courtenay?Alberni`) in the queue output; check the CSV is UTF-8 and the text is intact before editing.

## 1. Prepare

- Branch `claude/refine-skill-canada-plan-090128`, one pull request, never push to main.
- Reread `skill/SKILL.md` sections 1 to 5 and the Canada guide.
- Leads: none logged, so skip. Log leads for supporters of other countries met on the way (`skill/SKILL.md` 6.12).
- Automatic pass, whole country:

```bash
python skill/scripts/match_wikidata.py data/ca
python skill/scripts/profiles_wikidata.py data/ca
python skill/scripts/wtdb.py locate data/ca
python skill/scripts/archive_sources.py data/ca
python skill/scripts/seats.py data/ca --local "https://www.ourcommons.ca/Members/en/search/xml=<saved file>"
```

- Spot-check Wikidata matches (common names, and the many "wealthy individual" names that may match unrelated people; accept only when the description fits).
- Batch file outside the repo: `python skill/scripts/refine_queue.py data/ca --n 60 --out %TEMP%/ca-batch.csv`.

## 2. Batch 1: lit seats and prominent people (about 60)

1. **The eight lit seats** listed above: confirm seat, party and status on ourcommons.ca / sencanada.ca, add `positions.csv` rows if missing, set `refined`. Each has one statement (probably the 2020 NDP motion vote): add a second of a different kind or year, such as a bill, a 2025 platform or leadership statement, an op-ed or a Hansard speech. Pate and Galvez may have Senate bills or speeches.
2. **Other politicians with office flags (15)**, including Rob Ashton (A0323), Tony McQuail (A0324), Tanille Johnston (A0322) and Dimitri Lascaris (A0327): verify offices (candidate, councillor, MLA, party role) against the legislature, council or party page. Mark `former_role` where they left.
3. **Prominent non-seat people** (all with no links): Andrew Jackson (A0098), Alex Hemingway (A0037), David Macdonald (A0045), Dennis Howlett (A0228), Alex Cosh (A0229). Economists and policy researchers: find CCPA or university pages, ORCID, Wikidata; look for a recent report authored by them for a grade A statement.
4. **Campaigners with no place** (Muneeb Javaid, Chris Kruszewski, Jared A. Walker, Katrina Miller, John Anderson): place from their organisation page.
5. Fill the rest of the 60 from the queue order.

## 3. Batch 2: organisations, unions, parties

- The 219 supporters with no link are mostly signatories. Prioritise organisations with an official site: the NDP, Green Party, Québec solidaire, the Canadian Labour Congress and affiliated unions, CCPA, Canadians for Tax Fairness, Oxfam Canada, Patriotic Millionaires Canada, Millionaires for Humanity, and riding associations that submitted convention resolutions.
- For organisations: place at head office or the branch that made the statement; upgrade to a grade-A act (their own report, resolution or signed letter).
- Retraction check (4 flagged "still current?"): the four whose latest evidence is before 2020 and the 28 `former_role` entries; search for a recent position. Add `stance=retracted` only where a reversal is documented.
- Quebec manifesto: the register holds 80 of 1,443 organisational signatories (H0009). Adding the rest is a research run, not a refinement; record it in `notes_next`.

## 4. Later batches

1. Remaining single-statement actors (273): prominent ones first, second statement of a different kind or year.
2. Remaining coarse places (196) and the 94 missing Wikidata IDs.
3. Positions: 33 rows; check every `current=y` against the body's official list and date the ends.
4. Provincial and municipal actors (111 regional, 44 local): check against provincial legislatures and council pages after recent elections.
5. **Seat sweep** (refine skill section 6): after the refinement pass. Roll calls first: the 2020 NDP motion vote and Quebec division 477 (9 Yeas, 22 May 2025) are harvested; look for later federal motions and bills. Then sweep names in the NDP, Greens, Bloc Québécois, then Liberal progressives and the Senate groups (Progressive Senate Group, Independent Senators Group). Search in English and French; log each name in `queries.csv`.
6. Resources pass: Canada's polls in `meta.json` and bills in `data/resources.json` (confirm statuses at parl.ca).
7. New supporters met on the way go to `harvest.csv`, not into this run.

## 5. End of every run

- `wtdb.py validate data/ca`, then `wtdb.py checkquotes data/ca --run <run-id>` (House vote quotes need a manual check).
- `archive_sources.py data/ca --save` in the background.
- Add a `runs.csv` row, focus `refine: <n> supporters`, zero new actors, concrete `notes_next`.
- Report before and after: links added and supporters still linkless, finer places, statements added, grades raised, retractions, offices corrected, those not improved and why.
- Open one pull request.

## Order of work

1. Automatic pass and batch 1 (lit seats and prominent people), validation, pull request.
2. Batch 2 (organisations and unions), pull request.
3. Later batches and the seat sweep.
