---
name: wealth-tax-supporters
description: Build or extend a sourced database of the people, organisations and institutions in a country, region or supranational area that publicly support actual wealth taxation since 2010. Goal-first: find the most prominent supporters across every layer, with verifiable evidence and honest coverage notes, then plan the next runs. Use when asked to add a country, or to find, update, check or export wealth tax supporters for any area.
---

# Wealth Tax Supporters

Build a comprehensive, verifiable overview of everyone in an area who supports — or appears to support — **actual wealth taxation**: politicians who voted for or sponsored it, academics who argued for it, journalists who advocate it, organisations campaigning for it, councils that passed motions for it, and so on.

This is a database, not a ranking. Every entry rests on dated, sourced, quoted evidence. The work is done in repeatable **runs**; each run reads the current state from disk, works the highest-yield gaps, writes results as it goes, and logs what it did and what to do next, so any assistant in any session can pick up where the last one stopped. **Read section 0 first.**

Files in this skill (use them if present; the rules in this file are sufficient on their own):
- `references/definition-and-grades.md`, `references/data-format.md`, `references/research-run.md`, `references/geography.md`, `references/seats.md`, `references/export-and-pitfalls.md` — sections 2 to 8 of this skill, one file each (see the table at the end of this file)
- `references/source-playbook.md` — layers, bulk-list sources, query templates, search terms in many languages
- `references/area-profile-template.md` — what to establish about an area before searching
- `references/countries/gb.md` — the UK: levels of government, sources and an exhaustive council sweep (a worked example, not the template for every country)
- `references/countries/us.md` — a federal system (states, ballot measures, coalition letters), and what worked there
- `references/countries/se.md` — a unitary state with open parliamentary data, 21 regions and 290 municipalities
- `references/countries/de.md` — a federal state with a suspended wealth tax, Bundestag motions as bulk lists of named sponsors, and an official member register for the alive check
- `references/countries/in.md` — a country with no wealth tax since 2015, where support sits in the Left parties, a campaign (Tax the Top), Oxfam India and a handful of economists; notes on blocked sources and the district map
- `scripts/wtdb.py` — Python helper (stdlib; `openpyxl` only for xlsx export): `init`, `add`, `set`, `validate`, `dedupe`, `merge`, `checkquotes`, `status`, `export`
- `scripts/profiles_wikidata.py` — fills `profiles.csv` (websites, socials, Wikipedia) from Wikidata IDs
- `scripts/topo_to_boundaries.py` — turns a TopoJSON or shapefile of local areas (and their region outlines) into `boundaries.json`, so the country gets a local map on the site
- `scripts/fetch_page.py` — optional headless-browser reader for JavaScript pages and sites that answer 403 to plain clients, including their PDFs (needs `pip install playwright trafilatura`, a Chromium build, and optionally `npm install defuddle jsdom` in `scripts/`). `wtdb.py checkquotes` uses it automatically when a page cannot be read otherwise
- `scripts/adapters/se_meetingplus_scan.py` — optional Sweden adapter: full-text search of MeetingPlus council portals (Stockholm, Huddinge, Danderyd, Region Gotland)
- `scripts/adapters/se_riksdag_scan.py` — optional Sweden adapter: Riksdag scanner: motions, questions, committee reports, plenary debates, votes, member register
- `scripts/adapters/` — per-country source adapters (for example `gb_ocn_scan.py`, a UK council meeting scanner). Adapters are optional and always secondary to the first pass (6.5)

---

## 0. The goal, and how to use this skill

**The goal:** produce a trustworthy, sourced list of the people, organisations and institutions in an area who publicly back an actual wealth tax, so that anyone can see where support comes from and check the evidence behind every name.

**Success looks like:**
1. The **most prominent supporters are found first**: legislators who sponsored or voted for a wealth tax, parties with it in their programme, the big coalitions, unions and NGOs, leading economists, well-known commentators, public wealthy supporters.
2. **Every row is real**: a dated source you opened and a quote that is on the page.
3. **The coverage is honest**: the area profile and `notes` say what was searched, what was blocked and what was left out, so a blank is understood as "not searched" and not as "no support".
4. **The next person can continue**: the run log ends with a plan ordered by expected yield.

**Success is not** finishing every step of a process, covering every tiny unit, or building clever tooling. A first pass that finds 150 well-sourced supporters across all the important layers is worth far more than a half-finished crawler over 300 municipalities.

**How to use this skill:**
- The **rules** (sections 1 to 4: no source no row, the definition, grades, supporters only, public figures only) are firm. The **data format** (section 5) is firm, so that every country merges into one site.
- The **workflow** (section 6) is a default, not a script. Countries differ: some have powerful regions, some have no searchable local records, some have a single dominant campaign. Adapt the plan to the country, and write down what you changed and why in the area profile.
- **Aim at yield.** Before any large piece of work, ask "how many supporters will this find, and how sure am I?" Test with a small sample first. If a sample finds almost nothing, do not scale it up.
- **Look at what already exists** in the repository (the other countries' folders, notes in `skill/references/countries/`, helper scripts) before inventing something new.
- **When something does not work, change approach quickly.** A blocked site, a missing archive or an unsearchable register is a reason to switch source (archive copy, a browser, another outlet, a bulk list) within a few minutes, not a reason to build a tool. Say what you did in the run log.

---

## 1. Ground rules

1. **Apply the definition (section 2) to every piece of evidence.** Support for a mansion tax, capital gains reform or inheritance tax is not support for wealth taxation.
2. **No source, no row.** Every claim is an evidence row with a URL you actually opened and a **verbatim** quote found on that page. Never add an actor or evidence from memory or from a search-result snippet alone.
   - Fetch tools that return a summary can paraphrase. Quote from the raw page text (download it, or use a browser) and run `wtdb.py checkquotes` on the rows you add. It reads PDFs with `pdftotext` and falls back to the headless browser (`fetch_page.py`) for pages that block plain clients.
   - Never compose a sentence of your own and put it in `quote_original`. For list or roster pages where the only text is a name, use the text the page itself prints for that entry: a claim sentence in the page's structured data (JSON-LD), an official bill-status field such as `Rep. Lee, Barbara [D-CA-13]`, or the name and role as listed. Keep quotes short (about 25 words or fewer).
3. **Time window and the living.** Only evidence dated 2010-01-01 or later counts. Individuals are assumed alive unless a death record is found. Check before adding (Wikidata's date of death, or an obituary search when in doubt); anyone found dead goes in `exclusions.csv` (`deceased`), not in `actors.csv`. Record the check by setting `alive_checked=y`; do not narrate it in `notes`. Dissolved organisations may stay, marked `dissolved`.
4. **Supporters only.** Opponents are not recorded as actors. If an existing supporter later retracts or votes against, add evidence with `stance=retracted` (dated, quoted and sourced like any other row). An actor whose latest evidence is a retraction stays in the files but leaves the site.
5. **Public role, public record.** Only people acting in a public capacity (elected officials, officials, published authors, journalists, organisation leaders, people who publicly declared themselves, e.g. signed a published letter). Never record private individuals (ordinary petition signers, private social-media users), and never record home addresses, personal phone numbers or personal emails. Organisation websites and official pages are fine.
6. **The CSV files are the database.** Write each actor and its evidence to disk as soon as you have checked it — never hold a batch in memory to write at the end. The xlsx is a generated export, never edited by hand.
7. **Controlled vocabularies only** (section 5). If nothing fits, use the closest value and say so in `notes`; propose a vocabulary change in the run log rather than inventing a value.
8. **Report counts from the files**, not from memory (`wtdb.py status`, or count the CSV rows).
9. **Search in every official language of the area** (local-language terms are in the source playbook). English-only searching misses most of the local layer.

---

## Where the rest is

The rest of the skill is split into files under `references/`. The section numbers are kept, so every reference to a section number (here, in the country guides, the refine skill and the scripts) still points to the right place.

| Section | Topic | File |
|---|---|---|
| 2 | What counts as wealth taxation | [references/definition-and-grades.md](references/definition-and-grades.md) |
| 3 | Evidence grades | [references/definition-and-grades.md](references/definition-and-grades.md) |
| 4 | Who counts — actor types and inclusion rules | [references/definition-and-grades.md](references/definition-and-grades.md) |
| 5 | Data files | [references/data-format.md](references/data-format.md) |
| 6.1 | Start (brief) | [references/research-run.md](references/research-run.md) |
| 6.2 | Orient (an hour, not a day) | [references/research-run.md](references/research-run.md) |
| 6.3 | The first pass | [references/research-run.md](references/research-run.md) |
| 6.4 | Bulk harvest | [references/research-run.md](references/research-run.md) |
| 6.5 | Regional and local: proportional, sampled, honest | [references/research-run.md](references/research-run.md) |
| 6.6 | Plan the next runs | [references/research-run.md](references/research-run.md) |
| 6.7 | Geography register | [references/geography.md](references/geography.md) |
| 6.7a | Offices, seats and the Seats tab | [references/seats.md](references/seats.md) |
| 6.8 | Later runs | [references/research-run.md](references/research-run.md) |
| 6.9 | QA, and the pull request (end of every run) | [references/research-run.md](references/research-run.md) |
| 6.10 | Parallel work (if the assistant can run subagents) | [references/research-run.md](references/research-run.md) |
| 6.11 | Without code | [references/research-run.md](references/research-run.md) |
| 6.12 | Leads from outside the area | [references/research-run.md](references/research-run.md) |
| 7 | Export | [references/export-and-pitfalls.md](references/export-and-pitfalls.md) |
| 8 | Things that went wrong before (avoid them) | [references/export-and-pitfalls.md](references/export-and-pitfalls.md) |

Read sections 0 and 1 above first, then the files for the job in hand. For a new country: `definition-and-grades.md`, `data-format.md` and `research-run.md` (with `geography.md` and `seats.md` where they apply).
