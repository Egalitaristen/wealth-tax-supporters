# Renaming country folders and URLs to full names

Folders (`data/fr`), site URLs (`/fr`, `/fr/A0001`) and resource slugs (`/resources/fr-…`) use two-letter codes, except `australia`, which avoids a clash with `au`, the African Union. This plan moves all of them to full English names (`france`, `united-kingdom`, `african-union`). The mapping is `data/countries.csv`; `scripts/country_slugs_audit.py` counts every use (output in `docs/country-slugs-audit.md`).

Ids do not change (`A0001`, `E00001`), so a person reference changes from `fr:A0001` to `france:A0001`. The `iso2` field in each `meta.json` and the ISO codes in `actors.csv`, `leads.csv`, `home_countries.csv` and `wealth_tax_status.csv` stay: they are data about the country, not folder names.

## Decisions to settle first
1. The slug for each row of `data/countries.csv`. Check Turkey or Türkiye, Czechia, Russia, Vietnam, Iran, Georgia, Eswatini-style cases, and `african-union`, `european-union`, `united-nations`. `global` stays.
2. Whether resource slugs move too (`cl-boletin-13555-07` to `chile-boletin-13555-07`). Recommended: yes, with redirects, so a page's name matches its country.
3. D1 (`reports.country`, `suggestions.country`): leave the old values and map on read.

## Preconditions
- No open PR and no agent mid-run on any data folder. Tell Gemini and Codex to pause before the window and hold new briefs until the rename is merged. Every PR branched before the rename would collide.
- Record the baseline from main: row counts per table and folder, the list of every built URL (`_site` file list), `validate` output for each country, `seats.py` totals.

## The rename PR (one commit, scripted, repeatable)
One script, `scripts/rename_countries.py`, reads `data/countries.csv` and does everything; a `--dry-run` prints the full change list and writes nothing. It is run on a fresh branch from main, never edited by hand afterwards.
1. `git mv data/<code> data/<slug>` for all 99 folders (history follows), and `git mv` the files named by code: `content/stories/<code>.md`, `skill/references/countries/<code>.md`, `skill/references/records/<code>.md`. Flags stay keyed by ISO code.
2. Rewrite references with exact patterns, each logged with its count: `folder:id` in `data/resources.json` and any text (`fr:A0001` only where the id pattern matches); `data/<code>/` paths in docs, skill files and scripts; `/<code>/A0001`, `/<code>/seats`, `/<code>` and `/resources/<code>-` links in `content/` and docs; the `country` and `slug` of each resource; `data/featured_skip.txt` (`no:E00027` is keyed by iso2 and stays).
3. Code that hard-codes codes (19 scripts and `site/app.js`, listed in the audit): read the code from `countries.csv` instead of a literal, or change the literal. `site/app.js` already special-cases `australia`; that goes. Shared helper: `wtdb.py` gets `country_folder(code_or_slug)`.
4. Docs and briefs: `skill/SKILL.md`, `refine/SKILL.md`, `skill/references/*`, `README.md`, `docs/developing.md`, issue templates, `CONTRIBUTING.md`. Open issues mention `data/xx`; add the mapping link to the roadmap issue rather than editing 170 issues.

## Redirects (same PR)
- The worker (or `_redirects`) sends every old path to the new one with a 301: `/<code>`, `/<code>/…` (people, seats, directory, share pages and images), `/resources/<oldslug>`. The map is generated from `countries.csv` and the old resource slugs, not typed by hand. Kept permanently.
- Canonical links, the sitemap and share-card URLs use the new paths. After deploy: submit the new sitemap in Search Console and Bing.
- `/au` is the one clash: it redirects to `/african-union`, not Australia; `/australia` is now the Australia page it always was.

## Checks before merge (all must pass)
1. Row counts per table per folder identical to the baseline; no id changed.
2. `wtdb.py validate` 0 errors for all 99 folders; `wtdb.py schema` up to date; `seats.py data/eu` totals unchanged.
3. Full build succeeds; build's own link checks report 0 problems.
4. Old/new site comparison: every file in the old `_site` list exists at its new path (or is redirected); page count equal; people pages equal in content apart from links.
5. Crawl the redirect map: every old URL returns 301 to a URL that returns 200 (run on a preview deploy, then on production).
6. `grep` of the audit script shows no old folder reference left except the iso2 data fields; run the audit again and diff.
7. A sample of 20 stories and arguments opened in the browser, with their links followed.

## Deploy and after
- Merge, deploy once, run the crawl on production, check the Cloudflare analytics paths and the Search Console coverage report the next day.
- Rollback: revert the commit and redeploy the previous worker version; folder history is kept by `git mv`, so a revert is clean.
- Update the stored routines that read Cloudflare paths (they will see new paths), the PR-review checklist, and the briefs given to Gemini and Codex. Lift the pause.
