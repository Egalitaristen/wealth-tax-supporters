---
name: wealth-tax-supporters-refine-country
description: Refinement run for the Wealth Tax Supporters register: improve EVERY supporter already in one country's register, wealthy individuals and business leaders included. For each supporter, in order: add their official website and public social accounts, place them as precisely as public sources allow, add up to three more sourced statements (stronger grades and recent ones first), and check that their support is still current. Also covers the seat sweep: searching the name of every sitting member of a country's parliament, party by party, for support not yet logged. Use when asked to refine, enrich, deepen, update, clean up or improve an existing country, to add links, locations or more sources for its supporters, or to sweep its parliament for missed supporters. To find new supporters or add a country use `wealth-tax-supporters-research-country` instead.
---

# Refine a country's supporters

The research skill (`skill/SKILL.md`, named `wealth-tax-supporters-research-country`) finds supporters. This skill makes each entry better: easier to reach, better placed, better sourced and still true. It works on supporters who are already in `data/<iso2>/`; it does not look for new ones (that is a research run), with one exception: the seat sweep in section 6, where the parliament's own member list is what supplies the names.

**The rules of `skill/SKILL.md` apply unchanged**: what counts as a wealth tax (section 2), the grades (3), who may be recorded (1 and 4), the file formats and controlled values (5). Read sections 1 to 5 before the first run. This file only adds the refinement workflow.

## 1. Start

1. Pick the country. If the user did not name one, take the country whose supporters were refined longest ago (or never: the `refined` column in `actors.csv` is empty), say which, and start.
2. Work on a branch and open one pull request per run. Never push to `main`.
3. Make the batch: `python skill/scripts/refine_queue.py data/<iso2> --n 60 --out refine_batch.csv`. It ranks supporters by their gaps (no links first, then a coarse place, weak grades, a single statement, old evidence, no Wikidata ID), puts prominent ones first and skips anyone refined in the last 180 days. Keep the batch file outside the repository. A run is one batch; 30 to 80 supporters is a good size.

**Leads.** Before you start, read the leads other runs logged for this country (`python skill/scripts/leads.py list --country <iso2>`; `refine_queue.py` prints how many there are), and this country's own open leads (`leads.csv` in its folder, `skill/SKILL.md` 6.3a). Check each against its source, add the ones that hold up (they are new supporters: `skill/SKILL.md` sections 2 to 4 apply) and `leads.py close` every one as used, rejected or duplicate. And when this run meets a supporter of **another** country, log a lead instead of adding them here (`skill/SKILL.md` 6.12), then name them in the run's report.

## 2. The automatic pass (whole country, a few commands)

Run these first; they fill what open data already knows, so the manual work starts from the real gaps:

```bash
python skill/scripts/match_wikidata.py data/<iso2>       # Wikidata IDs where the match is unambiguous
python skill/scripts/profiles_wikidata.py data/<iso2>    # websites and accounts that Wikidata lists
python skill/scripts/wtdb.py locate data/<iso2>          # geo_unit_id and location in step
python skill/scripts/archive_sources.py data/<iso2>      # archive_url from existing Wayback snapshots
python skill/scripts/seats_uk.py data/gb                 # UK only: who sits in the Commons and Lords today; lists roles and statuses that disagree
python skill/scripts/seats_us.py data/us                 # US only: who sits in the Senate and House today; same
python skill/scripts/seats.py data/<iso2>                # any country in the ADAPTERS table at the bottom of seats.py: the same for those parliaments (--fix-status marks former members)
```

Spot-check a handful of what `match_wikidata.py` filled (the description should fit the person) before going on.

## 3. Each supporter, in this order

Work through the batch one supporter at a time and write to the files as you go (`wtdb.py add`, `wtdb.py set`). Spend a few tool calls on each, not a long search: take what the sources readily give and move on. The exception is a supporter you cannot yet identify (see 3.1, *Identify first*): give each of those 15 to 20 calls.

### 3.1 Links (most important)
A visitor who finds a supporter should be able to reach them. Add to `profiles.csv`:
- their **official website** (their own, their office's or their organisation's page about them);
- the **public social accounts they run in their public role**: X, Bluesky, Mastodon, Instagram, Facebook, YouTube, TikTok, LinkedIn, Substack;
- their **parliament or party page**, and **Wikipedia**.

Find accounts where the person or organisation links them: the header or footer of their website, their parliament or party profile, their organisation's page. A name search on a platform is not a source: the account must be linked from a page they control or one that lists them officially (Wikidata or a parliament counts). `source` is the page where you found the link and `checked` the date. Only https links. Skip private accounts.

**Identify first.** Some supporters are on the register with little more than a name and a province, typically signers of a public letter (the Patriotic Millionaires letters list "Name (ON)" and nothing else). A link is only worth adding once you know which person it is, so for these the work is identifying them, and it takes more than a few calls. Try, in this order:
1. the campaign's own pages: signer lists with bios, member pages and press releases (for Patriotic Millionaires, `millionairesforhumanity.org/the-millionaires/`, `patrioticmillionaires.org` and the national site);
2. press that names members (national papers, local and trade press, the campaign's interviews);
3. official registers where the country has them (a lobbyist registry, a company or charity register, a parliament's witness lists);
4. the name with the province and a typical role (founder, CEO, investor, philanthropist, doctor, lawyer), company and foundation pages, university pages, and LinkedIn.

A LinkedIn profile is acceptable when it clearly matches: same province, a role that fits, and ideally a mention of the campaign, the tax or tax fairness. A common name with nothing that ties a page to the signer is not a match: do not guess, and write down what you tried and which candidates you rejected, so the next run does not start again. Give each of these supporters 15 to 20 calls; the "few calls" rule is for people who are already identified.

**Nobody is left out of refinement.** Every supporter in the batch gets this step, wealthy individuals, business leaders and signatories of a list included: they backed the tax in public, and a reader should be able to reach their public pages like anyone else's (their company or foundation page, a press profile, Wikipedia, Wikidata, the accounts they run publicly). Rank, wealth and the lack of a formal role are not reasons to skip. If a search finds nothing public, say so in the run log with what you tried; do not skip silently. The limits are on what is recorded, not on whom: accounts run in a public role only, and no private accounts, home addresses or anything that locates a home (3.2).

### 3.2 Place
Put each supporter in the finest place a public source shows, and record that source in `location_source`:
- a legislator: the seat (constituency, district, state), as in `skill/SKILL.md` 6.7 (no `location_source` needed);
- an organisation: the city of its head office, or of the branch that made the statement;
- a person: where public sources say they are based or from. A news profile, their own biography, their university or employer page all count, as does Wikidata. Town level at most: never a street, an address or anything a reader could use to find their home.

Write the place as a path that resolves to a register unit (`wtdb.py locate` updates `geo_unit_id`); anything finer than the register goes after it as place text. If sources disagree, use the one closest to their public role and say so in the run log.

### 3.3 Statements (at most three new ones per supporter per run)
In this order of value:
1. **A stronger grade**: their own words or a formal act (a vote, a sponsored bill, a signed letter, a policy) for a supporter who is only at B or C;
2. **A recent statement**, if their latest is more than a few years old;
3. **A different kind or year**, to show the support is consistent.

Their own channels first (website, press releases, speeches, parliamentary records, their own posts and op-eds), then interviews and reporting. Apply section 2 of `skill/SKILL.md` to every statement: words about taxing wealth, not just "tax the rich". Quote verbatim, translate in `quote_en`, grade each row on its own, and leave the existing rows as they are. Three is a cap, not a target.

### 3.4 Still a supporter?
If their latest statement is from before 2020, or anything suggests a change of mind (a new party, a government role, a vote against), search for their recent position. If they now oppose a wealth tax, add a row with `stance=retracted`, quoting where they said so. The site leaves out anyone whose latest evidence is a retraction, and the files keep the history. If it is unclear, keep them and note it in the run log, not in `notes`.

### 3.5 Offices (politicians), and lit seats first
`refine_queue.py` puts everyone who holds a **lit seat** on the Seats tab at the top ("verify seat"). For each: open the chamber's own page for them, confirm they hold the seat today and the party shown, and fix `role`, `party`, `status` and the position if they do not. A party change is easy to miss (the Rajya Sabha's Sukhendu Sekhar Ray left Trinamool for the BJP in July 2026 and was re-elected on its ticket). Set `refined` when done so the next pass skips them.

### 3.5a Offices (all politicians)
Every politician needs a row in `positions.csv` for each office they hold or held (`skill/SKILL.md` section 5 and 6.7a): the body, the party, the seat, `start`, and `end` when they left. Check each against the body's own official list (a parliament's member list or API, a council's page) and set `current=y` with `checked=<today>`; for someone no longer on it set `current=n` and the `end` date, and update the actor's `role` and `status=former_role` to match. A person who left a chamber loses the seat on the Seats tab at once, which is the point: outdated tags go away on update. Where a country has a seat refresher (`seats_uk.py` for the UK), run it first and work through what it reports. Never leave `current=y` on a position you did not check, and never touch their evidence rows.

### 3.6 Facts and finish
Update `role`, `party` and `status` (`former_role` when they no longer hold the role the evidence came from) when a source shows a change. Merge any duplicate you notice (`wtdb.py dedupe`, then `merge`). Then set the date: `python skill/scripts/wtdb.py set data/<iso2> actors <ID> refined=<YYYY-MM-DD>`. Set it also when you found nothing to add, so the queue moves on.

## 4. End of the run

1. `wtdb.py validate data/<iso2>`: fix every error.
2. `wtdb.py checkquotes data/<iso2> --run <run>`: every new quote must be on its page; fix or remove what is not.
3. `archive_sources.py data/<iso2> --save` for the new sources (slow: run it in the background).
4. Add a row to `runs.csv` with `focus` = `refine: <n> supporters`, and in `notes_next` what the next batch should look at.
5. Open the pull request. Report from the files, not memory:
   - links added, and supporters who still have none;
   - places made finer;
   - statements added and grades raised;
   - retractions;
   - supporters you could not improve, and why.

## 5. Things to avoid

- **Guessed links.** An account with the right name but no link from the person's own pages may belong to someone else. Leave it out.
- **Home towns that reveal homes.** Town level at most, and only from a public source about their public life.
- **A supporter who sits as an MEP.** After you change an MEP's role, status or party, run `python skill/scripts/seats.py data/eu` (and `wtdb.py validate data/eu`) so the European Parliament chart on `/eu/seats` follows. Add other MEPs you find to their own country's register, not to `data/eu`.
- **Stale seats.** A role that still says "MP for X (at signing, 2021)" for someone who has since left, or `current=y` on an office nobody checked. Re-check offices on every pass.
- **A supporter who has died** leaves the register: add an `exclusions.csv` row (reason `deceased`, with the source of the news) and keep their original actor, profile and evidence rows in `docs/refinement/history/<iso2>-<ID>.json`, so nothing is lost. Never leave a deceased person marked active.
- **Rewriting history.** Never edit or delete an existing evidence row because a newer one exists; add the new one. Remove a row only when its quote is not on its page.
- **Notes that narrate the work.** ("Checked X, nothing found.") That goes in the run log; `notes` are shown to readers.
- **New supporters.** Someone you meet who is not in the register is a lead for a research run: list them in the run log or `harvest.csv` instead of adding them here.

## 6. Seat sweep: look for support among the sitting members

The member list of a parliament is a complete list of candidates, which a research run does not have. A sweep takes each sitting member who is not in the register and searches their name for a wealth-tax statement or vote, so politicians who back the tax quietly (a speech, a co-signed bill, one line in an interview) are found. Do it for countries with a Seats tab (an adapter in `seats.py`), after a refinement pass or when asked.

1. **Make the batch.** `python skill/scripts/seat_sweep.py data/<iso2> --n 40 --out sweep_batch.csv` reads the chambers' own lists, leaves out everyone already an actor, in `exclusions.csv` or swept before, and orders the parties by how much support is already logged in them (supporters who sit for the party today, then their share of its seats). Start at the top: parties with logged supporters are where more are most likely. `--party NAME` limits it to one party. Keep the batch file outside the repository.
2. **Roll calls first.** A name-by-name web search is a slow way to find votes: the first trial (Argentina, 20 names of the party with most logged supporters) found one supporter, from a news article about their own statement. A recorded vote on the named wealth tax lists every member at once, so before sweeping names look for the country's roll calls, bill co-sponsor lists and signed motions on a wealth tax, queue them in `harvest.csv` (`skill/SKILL.md` 6.4) and match them to the member list; the names left over are the sweep.
3. **Search each name**, a few tool calls at most, in the country's language: the name together with the local words for a wealth tax (the terms in `queries.csv` from the discover step), and the name with the parliament's record where it can be searched (bills they sponsored, motions they signed, speeches). Take what the sources readily give and move on.
4. **What counts** is the same as everywhere (`skill/SKILL.md` sections 2 to 4). A member needs **their own** evidence: a vote on the wealth tax itself, a bill or motion they sponsored or signed, their own speech, article or post, an interview in which they say it. Their party's platform, a coalition statement or being on the same list as a supporter is not evidence for them; it is a reason to look. Quote verbatim and grade each row.
5. **Add the supporters you find** as in a research run (`wtdb.py add`), with their `positions.csv` row; then run `python skill/scripts/seats.py data/<iso2>` so the seat lights up, and read what it prints. Someone who turns out to oppose a wealth tax is not recorded (supporters only); a near-miss that could come up again goes in `exclusions.csv` with the reason.
6. **Log every name you searched**, found or not, as a row in `queries.csv`: `channel=seat_sweep`, `query` the name and the term used, `results_opened`, `leads_added`. The next sweep skips them, so a run that finds nothing still moves the queue on. Never write "checked, nothing found" in an actor's `notes`.
7. **Stop a party** when about thirty names in a row bring nothing, and say so in `notes_next`; go on to the next party. A sweep that finds nothing for a party is a result, and it is not evidence that the members oppose the tax.
8. **End the run** as in section 4. In `runs.csv` use `focus` = `seat sweep: <party>, <n> names`, and report from the files: names searched, supporters added by party and grade, and the parties still to sweep.

## Resources pass (polls, papers, reports and bills)

The Resources page lists polls (each country's `meta.json` `polls`) and papers, reports and bills (`data/resources.json`; format in `skill/SKILL.md` section 5). Treat them like evidence: a run on resources opens each item at its source and checks that the link works, the title, authors and date are right, that it is about an actual wealth tax, that a bill's `status` is what the parliament's own page shows today (bills lapse and pass), and that a poll's figure matches the pollster's report and its question names a wealth tax. Fix or remove what fails. When a country is refined, also look for what is missing: its bills in the parliament's database, its official or independent reports, its published polls. Never state a status you have not seen. Open items are on the roadmap (the Resources and parliaments milestone).
