# Before you open the pull request

Run this list on your own work before the pull request. Every item comes from a row that a review removed or regraded in earlier country PRs; a reviewer will run the same checks, so a row that fails one of them is cheaper to fix now. Section numbers refer to `skill/SKILL.md`.

## 1. Whose register is it?

The register holds supporters **of this area**.

- A statement addressed to several countries, or to another country, is not evidence for this one (a regional paper's authors, a report about "the region"). Leave it out, or record the organisation only if it acted in or towards this area.
- A person who lives and works elsewhere belongs in their home register, even when they speak to your country's audience (a UK commentator interviewed on an Australian programme). Log a lead for their home area (6.12); do not add them here.
- A folder name that collides with an ISO code of an existing body gets the country's full lowercase name (`australia`, because `au` is the African Union). Say so in `meta.json` `notes`.

## 2. Is it a wealth tax? (section 2)

- Apply the definition to the speaker's own words, not to the topic of the page.
- A tax a source calls a "wealth tax" that is really an income or profit surcharge (a temporary levy on high net income, a "wealth tax" on capital gains) is out of definition: an exclusion row, or at most grade B with the doubt written in `grading_note`.
- A passing mention in a list of measures ("wealth and luxury taxation") is not a position. Grade C only if the speaker's own words are about wealth, otherwise an exclusion.

## 3. Is the quote the person's own, and does it state a position? (sections 1 and 3)

- The quote is the person's words, or the page's own entry for them (a roster line, an official vote entry). A journalist's narration of what someone announced is grade B at best, and only if the person is clearly the source.
- For a speech, open the transcript and check **who is speaking** at that point (a debate page can hold several speakers). A shared debate page cited for one senator's words proves nothing for the others.
- A paper abstract that says the proposals are "considered", "discussed" or "modelled" describes the paper, not the author's view. Grade C, or leave it out, unless the text recommends or proposes the tax.
- Co-authors count only where the text recommends the tax and names them as authors; a bibliography, an acknowledgement or a conference programme does not.
- Roster and endorsement lists are grade B (section 3).

## 4. Is the person a public figure? (section 1, rule 5)

- Students, trainees and anyone known only through one paper or one signature are private individuals: an exclusions row (`private_individual`), not an actor.
- People assumed alive, checked (`alive_checked=y`); anyone found dead goes to exclusions (`deceased`).
- No birth dates, genders from official records, home towns or contact details in `quote_original`, `notes` or `location`.

## 5. Each person has their own evidence (section 4)

A party platform, coalition statement or roster is evidence about that body only. Candidates, members and signatories need their own vote, bill, motion, speech, article or signed letter. Votes on a whole budget or report, on inheritance, property or transaction taxes, and requests to study a tax do not count.

## 6. Every quote is on its source

1. `python skill/scripts/wtdb.py checkquotes data/<slug> --run <run>`: fix or remove every row it cannot find.
2. For rows it skips (blocked sites, PDFs, pages that need a browser), open the page in a browser and find the quote. Say in the area profile how many you checked by hand.
3. A page behind a bot check (a "just a moment" or "verify you are human" screen) is not read around: use an archive copy of the page, and record the archive link in `archive_url`.
4. Spot-check at least 10% of the run's rows (minimum 5) for grade and meaning, not only wording.

## 7. Grades, dates and designs (sections 2 and 3)

- Grade each row on its own, with one line in `grading_note` saying why.
- The date is the date of the act or statement, not the date of a later article about it or the day a roster was updated.
- `wt_design` and `design_detail` say what was actually called for.

## 8. Politicians, positions and seats (6.7a)

- Every politician has a `positions.csv` row (body, party, seat, start).
- `current=y` only for people found on the body's own official list, with the date in `checked`.
- Seat counts come from the body's official list, never from memory.

## 9. Leads, queries and near-misses (6.3a)

- Every lead you opened is closed with a status, or left open with a note on what was tried. The PR description gives the number of open leads and the most promising few.
- `queries.csv` holds the broad searches of the discover step, in each language used.
- Candidates you checked and rejected are in `exclusions.csv`, so nobody re-checks them.

## 10. Tools and files

```bash
python skill/scripts/wtdb.py validate data/<slug>
python skill/scripts/wtdb.py dedupe data/<slug>
python skill/scripts/review_scan.py data/<slug> --names
```

Read what `review_scan.py` lists and fix or remove the rows. Besides the evidence checks it flags actors described as students or trainees, quotes that narrate the person in the third person, quotes that describe a proposal without recommending a tax, income surcharges typed as a wealth tax, multi-country statements, and people who are both an actor and an exclusion. `validate` warns about the last of these and about a folder name that is not the ISO code. Do not commit scratch scripts, caches or downloaded files: put the recipe for a country's geography or map in `skill/references/countries/<iso2>.md` instead. A missing map is not a blocker for a first pass: record which sources you checked in `meta.json` `notes` and open a follow-up issue for it.

## 11. Data hygiene

- **Controlled vocabularies only** (section 5); `validate` enforces them.
- **Type people by what they do**: an economist is `economist` even at a university, with `other_types` for a second role; a journalist needs opinion pieces (a reporter who quoted someone is not a supporter).
- **One name per party**, branches under the national party's name; run `dedupe` after every large import (rosters produce near-duplicates such as "Coalition for Human Needs" and "Coalition on Human Needs"), then `merge`.
- **`notes` are shown to readers**: identity caveats and sources only. Never "alive", "no Wikidata match" or "checked X, nothing found" (that is `alive_checked` and the run log).
- **A roll call is quoted from the member's own entry** on the official per-member list, never from the shared result line.
- **Write to disk as you go**, log every run in `runs.csv`, and report counts from the files (`wtdb.py status`), not from memory. Measure progress in supporters found and checked, not in units marked done.
- **Maps**: an open licence and the official codes, or no map. The register goes down to the local tier either way (6.7).
- **Sample before you scale**: no crawler for local units before the layers are touched and a sample shows it pays (6.5).
- **Work on a branch** and open a pull request; never push to `main`.

## 12. The pull request

Describe, from the files and not from memory: new supporters and evidence by type and level and grade; what was left out and why; what was checked by script and what by hand; the open leads; the languages searched; the map licence if there is a map; and the plan for the next run.
