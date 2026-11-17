# Media scan

A periodic scan of media sources for supporters, statements and sources the other scans miss. Press pages of organisations that campaign for a wealth tax list the interviews, op-eds and reports their members appear in; reading them finds people who say it in their own words (a source of new supporters and of extra evidence for people already in the register). It is a source of leads and evidence, not a register by itself, in the same way as the Bluesky scan (`bluesky-scan.md`).

## The pieces

- `data/media_sources.json`: the registered sources. Each has an `id`, a `name`, a `url`, a `country`, a `language`, a `format` (`html` for a news page or feed; `squarespace` for a Squarespace blog or media page, read as `?format=json` with its own paging and dates; `wp-json` for a WordPress REST list, with an optional `where` filter) and a `note` saying what the source is and who asked for it.
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

1. **Who.** A real, named public figure or organisation of an included kind (politician, party, union, think tank, campaign group, economist, academic, journalist, writer, artist, activist, business leader or wealthy person speaking publicly). Not private people, not the outlet, not the reporter who reports. A group that organises the page (the group whose press page it is) is usually in the register already.
2. **What.** Their own words, or an act: a direct quote, an interview answer, a signed letter, an op-ed they wrote. It must refer to a tax on the stock of wealth ("wealth tax", "billionaire tax" on net worth, "tax on extreme wealth" with a rate or a threshold), not "tax the rich", income, capital-gains or inheritance taxes alone. A reporter's paraphrase without a quote is at most a lead. Membership of a group that supports a wealth tax is not a statement; the group's own letter or statement names its signatories, and signing is the act.
3. **How strong.** A: a rate, a threshold, a named bill or proposal. B: a wealth tax or billionaire tax by name, supported. C: support only implied.

Things this scan meets often:

- A first-party post of a campaign group ("letter to the Prime Minister", "reactive statement") lists signatories or quoted members: each named signatory is a statement by an act (a letter) or a quote.
- An interview or podcast by a member: the member's own answer. Note the timestamp or the passage; transcripts are usually absent, so quote only what you can read or hear, in the original language with an English translation in `quote_en`.
- A poll or report published by the group is a document (`resources.json` and `documents`), not a statement by a person.
- Board members, patrons and funders are not members of the organisation they serve: a board member needs their own statement.
- An article about a person who is not quoted is no evidence.

## What to do with a hit

- **Already in the register:** add the quote as new evidence for that person if it is new, with the article as `source_url`, the outlet as `publisher`, the article's own date, and `archive_sources.py` run on it (articles move behind paywalls and disappear).
- **Not in the register, identified, with a statement graded A, B or C:** add them as a supporter of that country following `research-run.md`, or, when the country is not the one being worked on, add a **lead** (`leads.py add`) with the article link. A person whose role cannot be confirmed is a lead with the note "role unconfirmed".
- **A new source worth watching** (a podcast, a newsletter, an outlet that keeps covering the topic): add it to `data/media_sources.json` with a note.
- Then `mark` every article you read: `used` when a supporter, statement or lead came from it (put the supporter's id or lead id in `--note`), `reviewed` when it had nothing to add, `skipped` when it was off topic.

## Adding a source

1. Find the listing: a news or press page, an RSS or Atom feed, or the site's JSON (a Squarespace page answers `?format=json`; a WordPress site answers `/wp-json/wp/v2/<type>`; try `/feed` too).
2. Check its `robots.txt` allows our user agent for the path. If it does not, do not add it; ask the organisation for a feed instead.
3. Add the entry to `data/media_sources.json`, run `scan --source <id> --dry-run --pages 20` to see what it would record, then without `--dry-run`.

Sources worth adding next: the press pages of Oxfam, Tax Justice Network and other organisations that campaign on the topic; the news pages of parties and unions in the register; per-language news search feeds.

## Cost and manners

A scan of a few sources is a few requests each. Do not lower the delay. The first full read of a source records its whole archive as `new`; work through it oldest or newest first in runs of about 25 articles, not all at once.
