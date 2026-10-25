# US refinement plan

Prepared 25 October 2026 from `refine/SKILL.md`, research skill sections 1–5, the US country reference, and the current CSV files. This is a plan for existing supporters, not a research run for new names. No live sources have been verified for this plan.

## Baseline

| Measure | Current count |
|---|---:|
| Supporters | 873 |
| Evidence rows | 1,280 |
| Profile links | 1,401 |
| Supporters marked refined | 0 |
| Supporters without any profile link or website | 471 |
| Best evidence A / B / C | 557 / 316 / 0 |
| Supporters with one support statement | 646 |
| Latest support evidence before 2020 | 5 |
| People without Wikidata IDs | 243 |
| Positions marked current / former / unchecked | 105 / 20 / 334 |
| Evidence rows without archive URLs | 1,280 |

The queue identifies 844 actors with gaps, including 381 place gaps, 105 seat-verification flags and 15 politicians without positions. Counts overlap. A queue flag is a prompt to inspect, not proof that the record is wrong. All 125 checked positions carry 25 October 2026, but refinement still requires checking the official body page for each selected officeholder.

## 1. Prepare the first run

- Preserve existing local changes; use a `codex/` branch and one pull request per completed run. Never push to main.
- Keep the batch CSV outside the repository. A provisional 60-person batch has been generated at `%TEMP%/us-refine-batch-2026-10-25.csv`.
- Run the whole-country automatic pass: `match_wikidata.py`, spot-check several identity matches, then `profiles_wikidata.py`, `wtdb.py locate`, `archive_sources.py`, and `seats_us.py`, each against `data/us`.
- Review automatic changes, especially identities, office mismatches and source provenance. The US seat helper uses congress-legislators; direct chamber verification remains required. Confirm seat totals and party splits from official chamber lists.
- Regenerate the 60-person queue after the automatic pass. It may change as gaps are filled or offices corrected. Do not treat the provisional names as a fixed assignment.

## 2. First batch: visible seats

The provisional first 60 are all politicians flagged for seat verification. They begin with Aisha Wahab (A0740), Kirsten Gillibrand (A0005), Valerie Foushee (A0315), Laura Friedman (A0316), and Shri Thanedar (A0323). Other selected supporters include Elizabeth Warren, Bernie Sanders, Pramila Jayapal, Ro Khanna, Ilhan Omar and Alexandria Ocasio-Cortez. These are database queue entries, not newly verified claims about current office.

For every selected supporter, follow this sequence:

1. **Links:** add the official website, chamber/party profile and public professional social accounts linked by those pages or Wikidata. Record the discovery source and checked date; use HTTPS. Never infer accounts from a matching name.
2. **Place:** use state and congressional district for federal representatives, state for senators, and the appropriate seat for state legislators. Districts cross county boundaries; do not assign a representative to an arbitrary county. Use finer public-role locations for other actors, with `location_source`; town precision is the limit for people.
3. **Evidence:** prioritize an actor's own statement or formal act that upgrades B to A, then recent evidence, then a different year or kind. Add at most three new statements per supporter; zero is acceptable. Verify each quote on the source itself. Generic “tax the rich,” income surtaxes and realised capital-gains reforms do not qualify.
4. **Current stance:** investigate evidence predating 2020 and any sign of a reversal. Add a dated, sourced `stance=retracted` row if a reversal is established. Preserve earlier evidence; record uncertainty in the run log.
5. **Offices:** open the body's official page and verify party, seat and present membership. Review every held or former office recorded for the person, add missing position rows, and correct role/status. Set `current=y` only after official verification; use `current=n` and a sourced end date for departed members. Leave unverified offices unchecked.
6. **Finish:** resolve genuine duplicates and set `refined` to the actual completion date, including when no enrichment was found. Log blockers outside reader-facing actor notes.

Spend minutes per person. Change source quickly when blocked; do not let one inaccessible page stall the batch.

## 3. Subsequent batches

Each run is one regenerated batch of approximately 60 supporters, skipping those refined within 180 days.

1. **Remaining visible seats:** the baseline has 105 flagged actors, so roughly 45 remain after the provisional first batch, subject to refresh and verification changes. Fill the rest of the next batch from the ranked queue.
2. **Links and unchecked offices:** follow the queue into the 471 linkless supporters, 334 unchecked position rows and 15 missing-office cases. Prioritize prominent supporters; verify state and local offices against their own legislatures or councils.
3. **Evidence and location depth:** upgrade the 316 grade B supporters using their own statements or formal acts. Locate organisations at the headquarters or branch responsible for the statement and people using public biographies. Campaign endorsement rosters remain B unless stronger evidence is found.
4. **Older and remaining records:** ensure the five pre-2020 cases receive a current-stance search, and address remaining single-statement and identity gaps as the queue reaches them. Do not pursue three statements merely to fill a quota.

For US evidence, favor official congressional bill-status records, legislators' releases, state bill pages, signed coalition letters and the supporter's own policy pages. Treat earlier run notes about ballot measures and candidates as leads requiring fresh verification. New supporters encountered belong in the run log or harvest queue, not this refinement batch. Do not expand into a county sweep.

## 4. Completion criteria for every run

- Validate `data/us` and fix every error.
- Check every new quote with `wtdb.py checkquotes data/us --run <run-id>`; resolve failures by verifying the source or removing unsupported new rows.
- Request archives for new sources with `archive_sources.py data/us --save`; log failures without implying a snapshot exists.
- Add a run row with focus `refine: <n> supporters`, zero new actors, and concrete next-batch priorities. Use the next available run ID at execution time.
- Compare before/after files to report links added and supporters still linkless, locations improved, new statements, actors upgraded, retractions, offices corrected, and supporters not improved with reasons.
- Review the final changes and open one pull request. The run is complete when every selected supporter has a recorded outcome, required checks pass, and unresolved source limitations are documented.

## Planning limits

The automatic pass has not been executed and no supporter data has been changed. The queue CSV is provisional and outside the repository as required by the skill. Baseline figures describe local files, not independently verified present-day political facts.
