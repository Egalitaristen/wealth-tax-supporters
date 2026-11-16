# Finding websites for supporters (a search run)

About 2,400 supporters in the register still have no website on file, so their social accounts were never collected. This file is the whole procedure for one search run by an agent with web search and a shell. A run covers about 300 supporters and ends in one pull request that a reviewer checks. The agent never merges and never deploys.

Read `pre-pr-checklist.md` once for the repository's general rules. Nothing else in the register is changed by a search run: only `data/*/profiles.csv` and `data/*/profile_checks.csv`, and only through the scripts below.

## Setup

```bash
git checkout main && git pull
git checkout -b links/YYYY-MM-DD-NN
python skill/scripts/link_finder.py todo --out ../links-work/batches --size 30 --limit 300
```

`todo` lists supporters that have no website or official page, are not wealthy-individual-only, and were not searched in the last year, so a second run never repeats a first. It writes `batch001.json` and so on to a folder outside the repository (`../links-work`), 30 supporters per file: `country`, `country_name`, `actor_id`, `name`, `kind`, `type`, `role`, `affiliation`, `party`.

## For each batch

Find each supporter's own website with web search, then write `../links-work/results/resultNNN.json` (same number as the batch): a JSON list with one object per entry, in the same order:

```json
{"country": "<copy>", "actor_id": "<copy>", "url": "https://... or \"\"", "kind": "website or profile",
 "title": "<the exact page title or main heading you read, or \"\">", "note": "<one line: where you found it and how you confirmed identity>"}
```

**What counts**

- `website`: the person's own site (personal, campaign, researcher or author homepage). Give the homepage address.
- `profile`: only when there is no own site but an official institutional page about that person exists (a parliament or assembly member page, a university staff page, a party page for the person, a city council page).
- Neither found: an empty `url`. An empty answer is a good answer; a wrong address is worse than none. Most answers will be empty: in a trial on 100 people about 1 in 10 politicians had a personal site, most of the rest only a parliament page, and people outside politics were found less often.

**How to search** (up to about six searches per entry; stop at the first confirmed own site)

1. Search the exact name in quotes with role, party, affiliation and country. Search again in the person's own language ("site officiel", "sitio web oficial", "offizielle Website", "sito ufficiale", "hemsida", "persoonlijke website", "strona internetowa").
2. Open what the results point to. A personal or campaign site is often linked from the person's parliament page, party page, university page, Wikipedia page (any language) or a social media bio. Read the website, homepage, links and contact fields and the page footer.
3. Confirm identity on the page you opened: its title or main heading carries the exact name, and the role, party, affiliation, city or country agrees with the entry. If two people share the name and you cannot tell which is meant, return an empty url.
4. Search every entry at least twice before returning an empty url. If a search is rate-limited, wait about 20 seconds and retry once.

**Never return**

- Social media accounts (X/Twitter, Facebook, Instagram, YouTube, TikTok, LinkedIn, Bluesky, Mastodon, Threads). They are collected later from the site.
- Wikipedia, Wikidata, Google Scholar, ORCID, RePEc, directories, aggregators, "who's who" or election guide sites.
- News articles, interviews, or an employer's or think tank's page that merely mentions the person.
- The site of a namesake (another country or profession) or of a parent party or union.
- An address you did not actually see in a search result or on a page you opened. Never guess or construct an address.

Do not log in, solve captchas or work around bot protection. If a page refuses you, return the address only when the search results alone make the identity clear (and say so in `note`), otherwise leave it empty.

## After all the batches of the run

```bash
python skill/scripts/link_finder.py ingest --file ../links-work/results
python skill/scripts/profile_scan.py --sample 500 --due --seed 1 --report ../links-work/scan.tsv
python skill/scripts/wtdb.py validate data
```

- `ingest` re-checks every address itself and writes only what passes: no social, wiki or election-guide pages, and a website only if the page's own title, headings or address carry the person's name (a profile page must carry the name in its text). Rejected and empty answers are logged in `profile_checks.csv` so they are not searched again for a year. Nothing is taken on the agent's word alone.
- `profile_scan.py` reads the new websites and adds the social accounts they link to, with a name check for people.
- `validate` must report 0 errors.

## The pull request

Commit only `data/*/profiles.csv` and `data/*/profile_checks.csv` (check with `git status`: nothing else should be changed). Open one PR titled `Links: search run NN (about 300 supporters)` with:

- supporters searched, websites found, official pages found, answers rejected by `ingest`, empty answers;
- the accounts the scan added, by platform;
- anything you were unsure about and how you decided it;
- the command lines you ran.

Do not merge and do not deploy. A reviewer reads the PR, spot-checks the new rows against the web and removes any that are wrong before it goes in.

## What the reviewer looks at

Every person account must carry the person's name in its handle (the scan enforces this; unnamed handles are only logged). A sample of the new websites is opened to confirm they are that person's own site; an organisation's accounts are checked for the parent body's or a leader's accounts being taken for the group's. Wrong rows are removed by hand and the cause is fixed in `link_finder.py` or `profile_scan.py`.
