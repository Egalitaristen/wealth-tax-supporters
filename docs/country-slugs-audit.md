# Country folder codes: where they are used
99 folders in data/countries.csv; 2002 tracked text files scanned.

## folder:id reference (fr:A0001): 3552
by area: data 3540, skill/scripts 2, data/cy 1, data/cz 1, data/dk 1, data/fi 1, data/gr 1, data/hr 1, data/se 1, data/si 1, scripts 1, skill/references 1
top files: data/resources.json 3537, data/featured_skip.txt 2, skill/scripts/profile_scan.py 2, data/cy/runs.csv 1, data/cz/runs.csv 1, data/dk/runs.csv 1
  e.g. data/cy/runs.csv:5  R004,2026-11-20,Gemini,refine: 4 MEPs (Batch F),EP MEPs,,,,,,,,"EP roll-call MEP refinement (issue #813): Wikidata + EP profile links, finer
  e.g. data/cz/runs.csv:10  R009,2026-11-20,Gemini,refine: 1 MEP (Batch F),EP MEPs,,,,,,,,"EP roll-call MEP refinement (issue #813): Wikidata + EP profile links, finer 
  e.g. data/dk/runs.csv:13  R012,2026-11-20,Gemini,refine: 9 MEPs (Batch F),EP MEPs,,,,,,,,"EP roll-call MEP refinement (issue #813): Wikidata + EP profile links, finer

## data/<folder>/ path: 129
by area: skill/references 90, data/eu 5, scripts 5, docs 4, skill/scripts 4, data/ar 2, data/it 2, data/ma 2, data/ml 2, data/at 1, data/au 1, data/cn 1
top files: skill/references/countries/ru.md 5, docs/developing.md 4, skill/references/data-format.md 4, data/eu/runs.csv 3, scripts/build_gr_boundaries.py 3, skill/references/countries/ie.md 3
  e.g. data/ar/runs.csv:14  R013,2026-11-07,Antigravity,"refine: resources, meta polls, sitting member names normalization","data/resources.json cleanup (deceased legis
  e.g. data/at/area_profile.md:101  - **Primary records & gazette scans:** Downloaded and scanned 23 primary documents from `parlament.gv.at` (motions, plenary transcripts, com
  e.g. data/au/area_profile.md:7  **Run R001 (2026-10-26).** Searched for a PAP member, resolution or AU organ taking a position for an actual wealth tax: web searches in Eng

## site URL /<folder>/A0001 or /<folder>/seats: 256
by area: content/stories 239, content/arguments 6, docs 3, data/fr 2, data 1, data/pl 1, refine 1, site 1, skill/references 1, wrangler.jsonc 1
top files: content/stories/bo.md 22, content/stories/nl.md 19, content/stories/us.md 17, content/stories/pk.md 15, content/stories/fr.md 13, content/stories/ve.md 13
  e.g. content/arguments/README.md:46  `/us/A0675` for a register entry, `/resources/<slug>` for a bill, `/calculator?w=...` for the calculator.
  e.g. content/arguments/double-taxation.md:130  [Emmanuel Saez](/us/A0675) and [Gabriel Zucman](/fr/A0229) wrote the studies behind most of the figures. The OECD's report on net wealth tax
  e.g. content/arguments/why-tax-wealth.md:303  [Gabriel Zucman](/fr/A0229) and [Emmanuel Saez](/us/A0675) wrote studies behind several of the figures on this page. The [directory](/direct

## site URL /<folder> (page): 2
by area: README.md 1, content/stories 1
top files: README.md 1, content/stories/sr.md 1
  e.g. README.md:49  There are also country stories that make the case in one read (start with [Colombia](https://wealthtaxsupporters.com/co)), a directory you c
  e.g. content/stories/sr.md:78  url: https://wealthtaxsupporters.com/sr/directory

## resource slug prefix /resources/<folder>-: 23
by area: content/stories 19, content/arguments 4
top files: content/stories/us.md 6, content/stories/nl.md 4, content/stories/ch.md 2, content/stories/fi.md 2, content/stories/uy.md 2, content/arguments/no-cash.md 1
  e.g. content/arguments/no-cash.md:64  url: https://wealthtaxsupporters.com/resources/us-california-billionaire-tax-act
  e.g. content/arguments/nobel-laureates.md:59  url: https://wealthtaxsupporters.com/resources/us-california-billionaire-tax-act
  e.g. content/arguments/unconstitutional.md:58  url: https://wealthtaxsupporters.com/resources/us-california-billionaire-tax-act

## data/resources.json: `country` field on 387 entries (75 distinct); not a folder: none
   slugs starting with a folder code: 229 of 233

## data/resources_excluded.json: `country` field on 7 entries (5 distinct); not a folder: none
   slugs starting with a folder code: 0 of 0

## CSV columns with folder-like codes (all of data/*.csv at the top level and every data/<folder>/*.csv)
  data/<folder>/actors.csv: column alive_checked (462 rows)
  data/<folder>/actors.csv: column country (4614 rows)
  data/<folder>/evidence.csv: column quote_lang (8045 rows)
  data/<folder>/positions.csv: column party (3 rows)
  data/<folder>/queries.csv: column language (1476 rows)
  data/<folder>/runs.csv: column saturation (6 rows)
  data/home_countries.csv: column home_iso2 (15 rows)
  data/leads.csv: column country (55 rows)
  data/leads.csv: column found_in (55 rows)
  data/wealth_tax_status.csv: column iso2 (24 rows)

## Tracked files named after a folder code (rename with the folders)
  content/stories/: 24 files
  scripts/flags_png/: 96 files
  site/vendor/flags/: 98 files
  skill/references/countries/: 95 files
  skill/references/records/: 29 files

## Quoted two-letter codes in code (hand-check; each is a place that may need the mapping)
  scripts/build_site.py: 25 quoted codes, 3 distinct
  scripts/build_tr_boundaries.py: 8 quoted codes, 1 distinct
  scripts/changelog.py: 2 quoted codes, 1 distinct
  scripts/charts.py: 11 quoted codes, 2 distinct
  scripts/share_cards.py: 13 quoted codes, 3 distinct
  scripts/static_pages.py: 2 quoted codes, 1 distinct
  scripts/suggestions.py: 8 quoted codes, 1 distinct
  site/app.js: 39 quoted codes, 21 distinct
  skill/scripts/gazette_scan.py: 3 quoted codes, 1 distinct
  skill/scripts/link_finder.py: 34 quoted codes, 31 distinct
  skill/scripts/match_wikidata.py: 51 quoted codes, 19 distinct
  skill/scripts/media_scan.py: 9 quoted codes, 1 distinct
  skill/scripts/parliament_links.py: 5 quoted codes, 3 distinct
  skill/scripts/profile_scan.py: 22 quoted codes, 11 distinct
  skill/scripts/seats.py: 75 quoted codes, 44 distinct
  skill/scripts/seats_uk.py: 4 quoted codes, 1 distinct
  skill/scripts/seats_us.py: 3 quoted codes, 1 distinct
  skill/scripts/topo_to_boundaries.py: 5 quoted codes, 1 distinct
  skill/scripts/wtdb.py: 3 quoted codes, 2 distinct

## Other places to check by hand
  wrangler.jsonc: 0 mentions of country/folder
  worker/index.js: 9 mentions of country/folder
  site/_headers: 0 mentions of country/folder
  infra/d1/reports.sql: 3 mentions of country/folder
  infra/d1/suggestions.sql: 1 mentions of country/folder
  infra/d1/schema.sql: 2 mentions of country/folder
  scripts/deploy.py: 0 mentions of country/folder
