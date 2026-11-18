# Media scan

A periodic scan of media sources for supporters, statements and sources the other scans miss. Press pages of organisations that campaign for a wealth tax list the interviews, op-eds and reports their members appear in; reading them finds people who say it in their own words (a source of new supporters and of extra evidence for people already in the register). It is a source of leads and evidence, not a register by itself, in the same way as the Bluesky scan (`bluesky-scan.md`).

## The pieces

- `data/media_sources.json`: the registered sources. Each has an `id`, a `name`, a `url`, a `country`, a `language`, a `format` (`html` for a news page or feed; `squarespace` for a Squarespace blog or media page, read as `?format=json` with its own paging and dates; `wp-json` for a WordPress REST list, with an optional `where` filter) and a `note` saying what the source is and who asked for it.
- A source with `"people": true` (a roster such as the group's "meet the millionaires" pages) lists people, not articles: each item is a person's page, titled with their name and role. Being on the roster is not a statement; read the page, then search for the person's own words about a wealth tax, and add them only when you find them (grades as below). Staff of the group, a partner outlet's reporters and executives are `skipped` or `reviewed`.
- `data/media_seen.csv`: every article ever seen, with its source, link, title, publication date, the date it was first seen and a status: `new`, `reviewed` (read, nothing to add), `used` (a statement or lead came from it) or `skipped` (not relevant). The scan only adds rows, so each run reports what appeared since the last one. Commit it with the run's pull request.
- `skill/scripts/media_scan.py`: `sources`, `scan`, `list`, `read`, `mark`. It reads politely: it identifies itself, honours `robots.txt`, waits between requests and never works around a block. It only collects; it never writes to a register.

## Running it

```
python skill/scripts/media_scan.py scan                      # read every source (first two pages), record what is new
python skill/scripts/media_scan.py scan --source pm-uk --pages 20     # a first full read of one source
python skill/scripts/media_scan.py list --status new --source pm-ca   # what to review, oldest first
python skill/scripts/media_scan.py read M0344                 # title, date and text of one article
python skill/scripts/media_scan.py mark M0344 M0345 --status reviewed --note "no member quoted"
```

Run `scan` about monthly (a source that publishes daily, weekly), review what is new, and open one pull request per run.

## Reviewing an article

Read the whole article, not the headline. Then decide in this order: **who, what, how strong**, with the same rules as the Bluesky scan (`bluesky-scan.md`, "Who counts" and "Their own statement") and the grades of `definition-and-grades.md`:

1. **Who.** A real, named public figure or organisation (for example a politician, party, union, think tank, campaign group, economist, academic, journalist, writer, artist, activist, business leader or wealthy person speaking publicly; a role that fits no actor type is recorded as `other`, never skipped). Not private people, not the outlet, not the reporter who reports. A group that organises the page (the group whose press page it is) is usually in the register already.
2. **What.** Their own words, or an act: a direct quote, an interview answer, a signed letter, an op-ed they wrote. It must refer to a tax on the stock of wealth ("wealth tax", "billionaire tax" on net worth, a rate or a threshold on wealth), not "tax the rich", income, capital-gains or inheritance taxes alone. "Taxing extreme wealth" without naming a tax, a rate or a threshold is support only implied: grade C (the register's rule for C), and a reviewer may still remove it. A reporter's paraphrase without a quote is at most a lead. Membership of a group that supports a wealth tax is not a statement; the group's own letter or statement names its signatories, and signing is the act.
3. **How strong.** A: a rate, a threshold, a named bill or proposal. B: a wealth tax or billionaire tax by name, supported. C: support only implied.

Things this scan meets often:

- A first-party post of a campaign group ("letter to the Prime Minister", "reactive statement") lists signatories or quoted members: each named signatory is a statement by an act (a letter) or a quote.
- An interview or podcast by a member: the member's own answer. Note the timestamp or the passage; transcripts are usually absent, so quote only what you can read or hear, in the original language with an English translation in `quote_en`.
- A poll published by the group is a poll of the country (`meta.json` `polls`, see `data-format.md`) only if it asks about a tax on wealth: read the poll's own questions, not the press release. A report or paper goes in `data/resources.json`. Neither is a statement by a person.
- A petition the group runs or backs (a page where a visitor can sign, asking for a wealth tax by name) is not a statement by a person. Record the petition page as a lead (`leads.py add --country XX --kind petition --name "<petition title>" --url <the page where one signs> --from M0001`) and read it as `docs/petitions-spec.md` says: the ask, the organisation that runs it, the dates the page states, the signature count and its date. A petition that is listed on the site goes in `data/resources.json` as kind `petition`.
- A quote reproduced in the group's own press release is the speaker's statement; give the group as `publisher`, use `evidence_type` `statement` (or `open_letter` for a signed letter) and grade it on the words, not on the release being the group's own.
- Board members, patrons and funders are not members of the organisation they serve: a board member needs their own statement.
- An article about a person who is not quoted is no evidence.

## What to do with a hit

- **Already in the register:** add the quote as new evidence for that person if it is new, with the article as `source_url`, the outlet as `publisher`, the article's own date, and `archive_sources.py` run on it (articles move behind paywalls and disappear).
- **Not in the register, identified, with a statement graded A, B or C:** add them as a supporter of their country (the person's, which for a country's press page is usually the page's own country, see `country` in `media_sources.json`), following the next section. A person whose role cannot be confirmed is a lead (`leads.py add --country <the person's country, else the source's> --from data/<that country>` with the note "role unconfirmed").
- **A new source worth watching** (a podcast, a newsletter, an outlet that keeps covering the topic): add it to `data/media_sources.json` with a note.
- Then `mark` every article you read: `used` when it produced anything new (a supporter, evidence for someone already in the register, or a lead; put the ids in `--note`), `reviewed` when everyone and everything in it is already in the register or it had nothing to add, `skipped` when it was off topic.

## Adding a source

1. Find the listing: a news or press page, an RSS or Atom feed, or the site's JSON (a Squarespace page answers `?format=json`; a WordPress site answers `/wp-json/wp/v2/<type>`; try `/feed` too).
2. Check its `robots.txt` allows our user agent for the path. If it does not, do not add it; ask the organisation for a feed instead.
3. Add the entry to `data/media_sources.json`, run `scan --source <id> --dry-run --pages 20` to see what it would record, then without `--dry-run`.

Sources worth adding next: the press pages of Oxfam, Tax Justice Network and other organisations that campaign on the topic; the news pages of parties and unions in the register; per-language news search feeds.

## Cost and manners

A scan of a few sources is a few requests each. Do not lower the delay. The first full read of a source records its whole archive as `new`; work through it oldest or newest first in runs of about 25 articles, not all at once.

## A review run by an agent (about 25 articles, ending in a pull request)

The same steps as above, for an agent with web access and a shell. One run is one source, newest articles (by publication date) first, about 25 articles, one pull request. The agent never merges and never deploys; a reviewer reads the pull request and removes anything wrong before it goes in.

**Setup.** From a clean checkout of `main` (`git checkout main && git pull`, then `git checkout -b media/pm-uk-01`; use the source id and the run number; an agent that already has its own worktree branch just makes sure it is up to date with `origin/main`):

```bash
python skill/scripts/media_scan.py list --status new --source pm-uk --newest --limit 25
```

**What to read first, and only this.** `bluesky-scan.md` ("Who counts", "Their own statement"), `definition-and-grades.md` (grades), the evidence and actor field rules in `data-format.md`, and in `research-run.md` only 6.3 (how a supporter and an evidence row are written) and 6.9 (QA and the pull request). Ignore the rest: initialising an area, geography, discovery, bulk harvests and seats are for whole-country runs. Follow `pre-pr-checklist.md` for what a pull request must contain, with the changes this procedure lists.

**For each article.** `python skill/scripts/media_scan.py read M0001` (set `PYTHONIOENCODING=utf-8` on Windows; the script also does it itself) prints the title, the date, the links inside the article and its text; an outlet that blocks our reader may still open in a browser. Decide who, what and how strong as above, then:

- **Check who is already in:** `grep -i "<surname>" data/*/actors.csv` (and the person's `wikidata_qid`); `wtdb.py dedupe data/<iso2>` afterwards finds pairs. A person is never added twice.
- **A new quote for someone in the register:** `wtdb.py add data/<iso2> evidence '{...}'`. `quote_original` is the exact words (with `quote_en` when not English); `source_url` is the article, `publisher` the outlet (or the group when the quote is reproduced in its release), `date` the article's own date, `run_id` this run's id. Not more than the sentences that carry the statement.
- **A new supporter:** `wtdb.py add data/<iso2> actors '{...}'` with the required fields of `data-format.md` (copy `geo_unit_id`, `level`, `prominence` from a similar existing row of that country), a second source for the role (the organisation's or outlet's own page, Wikidata with `wikidata_qid`), and the evidence row. When the person is a politician, run `seats.py data/<iso2> --fix-status` afterwards.
- **A lead:** `leads.py add ...` as above.
- **Archive:** `python skill/scripts/archive_sources.py data/<iso2> --ids E00905,E00906` with the evidence ids this run added (lookups only: no `--save`). When there is no snapshot, leave `archive_url` empty.
- **Mark the article:** `media_scan.py mark M0001 --status used --note "gb A0220 E00906"`.

**The run.** Take the next run id (the last in `data/<iso2>/runs.csv` plus one; the same id for every country this run touches is fine) and append a row to each touched country's `runs.csv` the way 6.9 step 5 says, with the media source as the source and the counts. Commit when the last article is marked.

**Before the pull request.** `python skill/scripts/wtdb.py validate data` reports 0 errors (the warnings already there are not yours to clear; add none), `python skill/scripts/wtdb.py checkquotes data/<iso2> --run <your run id>` passes for each country touched, and `git status` shows only `data/<iso2>/{actors,evidence,runs,leads}.csv`, `data/leads.csv` and `data/media_seen.csv` changed.

The pull request lists, per article: the article id and title, the outcome (used, reviewed or skipped) and, for each used one, who said what with its grade, and which were added as new supporters, as new evidence for existing ones, or as leads. Anything you were unsure about goes at the end with how you decided it.

What the reviewer checks: every new quote against the article (words, speaker, date), the identity of every new person, that a reporter's paraphrase, a roster line or a group's membership was not counted as a statement, that the grade matches the words (an implied-only statement is C), and that no private person was added.
