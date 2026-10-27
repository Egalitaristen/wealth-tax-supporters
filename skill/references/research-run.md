# Research run workflow

This file holds sections 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.8, 6.9, 6.10, 6.11, 6.12 of the skill. `skill/SKILL.md` keeps the section numbers as pointers to this file, so a reference such as "SKILL.md 6.7a" still finds it. Section numbers in the text below refer to the same numbering.

### 6.1 Start (brief)
1. Read this file, the area's folder if it exists (`area_profile.md`, the last three `runs.csv` rows, `wtdb.py status`), and the notes for the nearest country in `skill/references/countries/`. For a new country, also list the suggestions people have already sent for it from the site (`python scripts/suggestions.py`): the form accepts any country, so they wait there until a register starts, and they go into the first pass's leads. Also read the leads earlier runs found for it while researching elsewhere (`python skill/scripts/leads.py list --country <iso2>`; 6.12).
2. Settle three things with the user, in **one short message**, each with a recommended default: **which area**, **scope** (national only; plus regional; plus local) and **depth** (see the ladder below). If the user has already told you, do not ask again. If they do not answer, use the defaults and say so.
3. In this repository, work on a branch and open one pull request per run. Never push to `main`.
4. `wtdb.py init data/<iso2> --area "<Name>"`, then **load the geography register down to the local tier** (6.7): an official list with codes, usually a few turns. It is part of every seed pass, not a later run, and `validate` fails while the register stops at regions. Then look for an open-licence map of the same units (section 5); a missing map is a warning, not a blocker: record the sources you checked in `meta.json` `notes` and open a follow-up issue for it. Then go straight to 6.2. State your plan in a few lines and begin; do not wait for approval of the plan.

**Depth ladder** (pick one, and say which in `meta.json` `notes`):

| Depth | What it delivers | Local and regional |
|---|---|---|
| **Seed** (default for a new country) | The prominent supporters in every layer at the national level, with a plan for the next runs | Regional legislatures and the largest cities, sampled |
| **Standard** | Seed, plus every harvest list and layer pass until new finds dry up | Regional bodies in full; local bodies where the sample showed they matter |
| **Exhaustive** | Standard, plus every local unit | Every unit in scope, as in the UK run |

### 6.2 Orient (a few turns, not a long session)
Fill in `area_profile.md` from `references/area-profile-template.md`, briefly: the history of wealth taxes in the area since 2010; live bills, ballot measures and campaigns; which parties, unions, NGOs and economists have taken positions; which languages and search terms to use; where the legislature publishes votes, bills and motions; whether local bodies pass motions and publish records you can search; which sources block you. Every factual line gets a source. Mark anything from a search summary only as `[verify]`.

This step decides the plan. Spend your effort where the evidence says support lives.

### 6.2a Discover: ask the open web first (3 to 5 turns)
Before searching any layer, find out what the country's wealth-tax debate looks like from the outside. The layers in 6.3 search the places where support is expected; this step finds where it actually is, including actors and layers you would not have listed. Skipping it is how a run ends up with the legislature and nothing else.

1. **Broad searches, in every official language.** The tax by name (the playbook has the terms for each language) combined with: proposal, campaign, petition, open letter, referendum, "calls for", "supports", "demands", economists, union, church, poll, and the country's name. Use general web and news search, not searches restricted to one site, and read the first two or three pages of results for each query.
2. **Broad sources about the country.** The encyclopaedia article on the country's wealth tax or tax debate, tax-justice and inequality organisations' country pages (Oxfam, Tax Justice Network and its national branches, the EU Tax Observatory, the World Inequality Lab), and news timelines of the last proposal. They give names, dates and documents; they are never the source of a row.
3. **Polls and international campaigns.** Polls on a wealth tax (they name who commissioned them, often a supporter), and the country's signatories and coverage of international letters and campaigns (Patriotic Millionaires, Millionaires for Humanity, the G20 billionaire-tax track, the Zucman tax).
4. **Write down what you learn.** In `area_profile.md`: a dated timeline of the debate since 2010 and the search terms that worked. Then **every name, organisation, document, event or list you meet is a lead**: `python skill/scripts/wtdb.py add data/<iso2> leads '{"kind":"document","name":"...","source_url":"https://...","why":"...","found_run":"R001","status":"open"}'`, with the link where you saw it and one line on why it matters. Add someone straight to `actors.csv` only if you have already opened the source and hold the quote; the point of this step is breadth.
5. **Log the queries** in `queries.csv` (`language`, `query`, `channel`, `results_opened`, `leads_added`): one row per query worth knowing, so the next run sees what was tried and a reviewer sees how broad the search was.

Stop after 3 to 5 turns, or earlier when new queries mostly return leads you already hold. If broad searches find almost no named supporters, say so in the area profile: that is a finding about the country (support is thin or sits in one campaign) and shapes the plan.

### 6.3 The first pass
Touch **every layer once, highest yield first**, before going deep in any one, starting from the leads of 6.2a. A typical order (adapt it):
1. **Legislature:** sponsors and cosponsors of wealth-tax bills, roll-call votes, motions, amendments, committee evidence.
2. **Parties:** programmes and manifestos since 2010, congress motions, party youth wings.
3. **Coalitions, NGOs, unions, think tanks:** campaign coalitions and their member lists, union congress motions, tax-justice groups, think-tank reports.
4. **Economists and academics:** open letters, commission and report authors, op-eds.
5. **Commentators and media:** opinion columns, editorials, podcasters and video commentators with a public profile.
6. **Wealthy individuals, business, faith, culture, funders:** public declarations and letters.
7. **Regional and local:** regional parliaments and governments, then a sample of local units (6.5).

For bulk lists (letters, rosters, coalition pages, bill cosponsor data) queue them in `harvest.csv` and process them whole; they produce many actors with uniform evidence (6.4). Use search in the area's languages (the playbook has terms). Check the definition against what each list or person actually calls for.

**End the first pass when every layer has been touched and the biggest lists are in.** Then validate, run the quote check, open the pull request, and write the run plan (6.6). The whole seed pass is about ten turns. If you find yourself building a crawler or sweeping hundreds of units one by one, stop and check the plan against the goal.

### 6.3a Follow the leads
Leads are how the register grows beyond the first obvious names. Work them through the whole run, not only at the end.

- **Work the queue.** After each layer in 6.3, and again before the pull request, take every open lead (`wtdb.py status` lists them): open its source, apply sections 2 to 4, and close it with `wtdb.py set data/<iso2> leads D0001 status=used closed_run=R001`: `used` (rows were added), `rejected` (fails the definition or is not a public figure; add an `exclusions.csv` row when the name could come up again) or `duplicate`.
- **Every source you open is a source of more leads.** Look for: co-signers and co-authors; people quoted or thanked; the organisation behind a campaign and its member list or board; who a speaker cites, answers or shares a platform with; coalition partners; who covered the event (commentators, outlets with editorials); the next document in the chain (bill, committee evidence, debate, vote). Add each as a lead with its link and why. Add it straight to the register only when you already hold the quote.
- **Prefer leads that are lists or documents** (they give many names) to single names. Queue a list as a harvest (6.4) and say so in the lead's `note`.
- **A lead you cannot check** (a blocked site, a document you cannot find): leave it open, write what you tried in `note`, and name it in the pull request so the next run starts there. Never delete a lead; closing needs a status.
- Leads about **another country** go in `data/leads.csv` (6.12), not here.
- **Stop** when the open queue is empty, or what is left is blocked or low yield. Do not stop with unchecked leads that point at lists or documents.

### 6.4 Bulk harvest
Lists produce many actors at once with uniform, strong evidence. Queue each in `harvest.csv`, then process it entry by entry:
- roll-call votes on wealth-tax bills or amendments, and bill co-sponsors
- signatories of parliamentary or council motions
- open letters with published signatory lists (economists, millionaires, faith leaders, organisations)
- coalition and campaign member lists
- authors of wealth-tax reports and commissions; witnesses and written evidence
- union and party conference motions (mover, seconder, supporting bodies)

Rosters can be large (a ballot campaign's endorsement page listed about 250 names). Parse the page's structured data instead of retyping names, check each name against the database (name variants such as "Coalition for Human Needs" and "Coalition on Human Needs" are the same body: `merge`), and keep the list's own entry text as the quote. For a roll call, that is the member's own line: the `source_url` is the official per-member list (an open-data API endpoint is fine, such as the Câmara's `/votacoes/<id>/votos`) and `quote_original` is the name exactly as that list prints it, with the vote, party and seat in `grading_note`. Never quote the result line ("Yes: 136; No: 262") for every member: it is the same on every row and proves nobody's vote. Wikipedia and other secondary lists are good for finding names, never as the source; re-read each name at its own cited page.

For each person or organisation on a list: check for duplicates, check the definition applies to what the list actually calls for, check they are not dead (or, for an organisation, that it still exists), then add the actor and an evidence row whose `harvest_id` points to the list. Mark the list `done` with `actors_added`.

### 6.5 Regional and local: proportional, sampled, honest
Local support is real in some countries (UK councils pass motions) and nearly absent or unsearchable in others. Decide from evidence, not from a checklist.

1. **Load the geography register to the depth you intend to use** (6.7), not deeper.
2. **Sample first.** Pick 5 to 10 units: the largest cities, and units run by the parties most likely to support a wealth tax. Search each (site-restricted web search, the unit's own records search, local news, party and union branches). Count the supporters found and the time spent.
3. **Decide from the sample.** If most sampled units yield something, continue region by region. If few do, stop sweeping units one by one and look for the aggregators instead: a party's list of its councillors who signed a letter, a union branch network, a campaign's local groups, a national motion template that councils copied.
4. **Be honest in the register.** `sweep_status=done` means the unit was actually read. Units you chose not to search are `skipped` with a reason in `notes`. A unit you only sampled stays `in_progress`. Never mark a unit done to make progress look complete.
5. **Prefer search to scraping.** A site-restricted web search ("site:example.se förmögenhetsskatt motion") over a municipality's own pages is usually enough. Build a crawler only when **all** of these hold: a sample shows the documents really contain hits; many units (about 30 or more) share one platform; and you have told the user what it will cost. Keep it in `skill/scripts/adapters/<iso2>_*.py` with a docstring, treat its hits as **leads** (confirm each in the source), and never let it replace the first pass.
6. Failed motions still identify the proposer and seconder as supporters. Councils that **passed** a motion are `government_body` actors.

### 6.6 Plan the next runs
At the end of the first pass, write the plan into the last `runs.csv` row (`notes_next`) and the area profile (section 10): the layers and lists still to do, ordered by **expected yield per turn**, with what you expect from each and what is blocked. Include the regional and local decision from 6.5 and, if it is "continue", the order of regions. The user reads this to choose what to run next.

### 6.8 Later runs
Improving the supporters already found (links, finer places, more statements, a check that support is still current) is a separate workflow: `refine/SKILL.md`.

Each run reads the folder (`status`, `notes_next`), picks the top of the plan, works it, and writes a new plan. A good run is one harvest list, or one region, plus one layer pass. Priority order when the plan is silent:
0. open leads in this area's own `leads.csv` (6.3a), and the leads other runs logged for this country (`leads.py list --country <iso2>`; 6.12): check each against its source, add it to the register, then `leads.py close` it as used, rejected or duplicate
1. suggestions sent from the site for this country (`python scripts/suggestions.py export new.csv`; check each against its source, then `mark` it added, duplicate or rejected)
2. queued harvest lists
3. thin cells in the coverage grid (actor type × level)
4. upgrades of C- and B-graded actors (look for a vote, a signed letter, a specified design; leave the old evidence in place)
5. snowballing: follow co-authors, co-signatories, coalition members, their organisation and party outwards
6. regional and local units, as decided in 6.5
7. retractions: for prominent supporters, check whether they have since retracted

**Stopping.** A layer is saturated when about nine in ten of the candidates you find are already in the database (or excluded) for two passes in a row **and no open lead from that layer is left** (6.3a). The database is "complete for now" when the plan is empty or the remaining items are low yield; after that, runs are update sweeps (new evidence since the last run). Completeness is never a precondition for publishing: a partial database with honest coverage notes is the normal state.

### 6.9 QA, and the pull request (end of every run)
1. `validate` → fix every error. Warnings: fix or justify in `notes`.
2. `dedupe` → merge true duplicates with `merge`.
2a. Every new politician has a `positions.csv` row (6.7a). Where the country has a Seats tab, refresh it (UK: `seats_uk.py`) and fix every actor it reports.
3. **Quote check:** `checkquotes --run <this run>`. Fix or remove every row it reports as not found. Rows it skips (PDFs, blocked pages) need a manual look: open the page, find the quote. The checker reads the page's declared charset (so Chinese and Japanese pages work), falls back to `pypdf` when `pdftotext` is missing, and counts CJK quotes by characters. A quote too short to compare (a single-word roster name) is listed as "too short to check" rather than as missing. Then spot-check at least 10% of the run's rows (minimum 5) by hand for grade and meaning, not just wording. There is no separate verification mark: a row is in the database because its quote was found on its source, and readers report mistakes from the site.
3a. **Leads and queries (6.3a):** every lead opened this run is closed with a status or left open with a note on what was tried; `queries.csv` holds the broad searches of 6.2a. The pull request description gives the number of open leads, the most promising few, and the languages searched. Then run through `references/pre-pr-checklist.md`.
3b. **Review scan:** `python skill/scripts/review_scan.py data/<iso2>` (add `--names` for roster and author lists). It lists groups of people who share one quote, quotes with no wealth or tax wording, citations, exit-tax-only and property-type rows, research-date dates, personal data and the polls. Read what it lists and fix or remove the rows; a reviewer will run the same scan. Also check each poll's figures at its source: it must ask about a wealth tax (not "should the rich pay more"), and say who paid for it.
4. `match_wikidata.py` and `profiles_wikidata.py` for new actors. Do not commit scratch scripts or caches: put the recipe for a country's geography or map in `skill/references/countries/<iso2>.md` instead. The pull request description names the map licence. Check that `boundaries.json` exists (6.7); `validate` warns when it does not.
5. Append the run row to `runs.csv`, including `saturation` and `notes_next` (the plan).
6. Open or update the pull request and report to the user: new actors and evidence by type and level, what was left out and why, the plan for the next runs, and numbers from `status`, not from memory.

### 6.10 Parallel work (if the assistant can run subagents)
Split by layer or by region, never so that two workers write the same file. Each worker writes `staging_<worker>.jsonl` files (actors and evidence with temporary IDs) and returns them; the coordinator deduplicates against the database, adds with `wtdb.py add`, runs `validate`, and has a separate worker do the spot-check. Do not use parallel workers to do a large sweep that the sampling step (6.5) has not justified.

### 6.11 Without code
Follow the same steps by hand: keep the CSVs in exactly the format above, check the `validate` rules yourself (required fields, allowed values, dates from 2010, a URL and a quote on every evidence row, no actor without evidence, no duplicates), and deliver the CSVs or a spreadsheet built from them.

### 6.12 Leads from outside the area
Leads about the area you are researching go in its own `leads.csv` (6.3a). This section is for the other kind.

While you research one area you will meet supporters of another: a UN run finds a UAE minister, the Mexico run finds a Cuban economist, a Swedish article quotes a Danish union. Do **not** add them to this area's register (it holds one area only) and do **not** let them go. Log each as a lead:

```
python skill/scripts/leads.py add --country AE --name "Name" --url <where you saw the statement> --role "..." --note "what they said" --from data/<this area>
```

- One lead per person or organisation, with the link to the statement and a line of what they said. Public figures and organisations only, never personal data. Use the country's ISO code (a region as `US-CA`; `UN`, `EU` or `AU` for a body with no country).
- Leads sit in `data/leads.csv`, committed with the run's pull request. A lead is a pointer, not evidence: the run that picks it up checks it against its source and applies sections 2 to 4 like any other candidate.
- The run that starts or refines that country reads its leads first (6.1, 6.8, `refine/SKILL.md`), then closes each one: `leads.py close L0007 --status used --run R003` (or `rejected`, or `duplicate`). `leads.py summary` shows which areas have open leads.
- Mention the leads you logged in the run's report so the user sees where they went.
