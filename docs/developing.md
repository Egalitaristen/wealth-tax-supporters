# Developing and contributing data

The technical guide that used to be the README: how the repository is laid out, how to add a country and how to build the site locally. The short version for readers is in the [README](../README.md).

## What is here

| Path | What it holds |
|---|---|
| `data/<iso2>/` | One database per country or region, for example `data/gb/`. Plain CSV files plus a `meta.json`. |
| `skill/` | The research skill for people and for AI coding assistants. `SKILL.md` holds the goal and the ground rules; `references/` holds the definition and grades, the data format (its column lists are generated from `wtdb.py`), the research run (discover, layers, follow the leads), geography, seats, the pre-pull-request checklist, the election-refresh guide, the source playbook and one guide per country. Helper scripts: `wtdb.py` (init, add, validate, checkquotes, status), `review_scan.py`, `leads.py`, `seats.py` and its adapters, `seat_sweep.py` (sitting members still to search), `match_wikidata.py`, `profiles_wikidata.py`, `topo_to_boundaries.py`. |
| `refine/` | The refinement workflow (`SKILL.md`) for supporters already in a register: links, finer places, more statements, and a check that support is still current. Uses the scripts in `skill/scripts/` (`refine_queue.py`, `archive_sources.py`). |
| `site/` | The static front end: one page and one script, no framework. Home with search and a zoomable world map, country pages (area map, seat charts, directory, timeline, method), a page per supporter, a global directory, the parliaments and resources pages, method and contribute pages. Maps zoom with the mouse wheel or by pinching. |
| `scripts/build_site.py` | Turns `data/` into the site data, a search index and CSV downloads. Standard library plus `pycountry`. |
| `scripts/share_cards.py`, `scripts/fonts/` | Link-preview images for every page (home, directory, each country page including its seats and directory pages, each supporter), drawn with Pillow; the seats card shows the chambers as seat charts, the over-time card the statements per year, and country, person, seats and directory cards carry the country's flag (small PNGs in `scripts/flags_png/`, made from `site/vendor/flags` by `scripts/make_flag_pngs.py`, which needs Chrome or Edge and is only re-run when a flag changes). The build also writes a small HTML file per page with its own title, description and image, so previews on Discord and social media match the page. |
| `scripts/serve.py` | Serves the built site locally the way Cloudflare does (unknown paths fall back to `index.html`). |
| `scripts/deploy.py`, `wrangler.jsonc` | Build and deploy the site to Cloudflare from a local checkout. |
| `docs/`, `infra/` | The community plan, and the Cloudflare setup and draft database schema. The suggestions database is deployed; the community schema is a draft. |

The site's [countries page](https://wealthtaxsupporters.com/countries) shows the live list of countries with their counts; each `data/<iso2>/area_profile.md` says what was searched and what was not.

Every country's register goes down to its lowest tier of local government, and the map shows the same tier where an open source with official codes exists, so maps are comparable; see `skill/SKILL.md` 6.7. A missing map is a follow-up issue, not a blocker. Supporters need their own evidence: a party's platform is recorded on the party, not on each of its members (`skill/references/definition-and-grades.md`, section 4).

Three bodies above the countries have a register of their own for chambers and seats only: the European Parliament (`data/eu/`, 720 seats), the United Nations General Assembly (`data/un/`, one dot per government) and the African Union's Pan-African Parliament (`data/au/`). A supporter who sits in one is recorded in their own country's register.

## How the research works

The goal is a trustworthy register of who publicly backs an actual wealth tax, with the evidence behind every name. A research run starts by asking the open web broadly, in every official language of the country, who has argued for a wealth tax and when, and turns what it finds into a queue of leads. It then touches every layer once, going after the most prominent supporters first (legislature, parties, coalitions and unions, economists, commentators, wealthy and business, regional), and follows the leads (co-signers, people quoted, coalition partners, the next document in the chain) until the queue is empty or low yield. Local sweeps are sampled first and expanded only where they pay. Coverage is reported honestly, so a blank means "not searched", and a run ends with a checklist and a plan for the next one. After an election the seat charts are refreshed from the parliament's new official list. The details are in [`skill/SKILL.md`](../skill/SKILL.md); read its sections 0 and 1 first.

## Add your country

1. Fork this repository.
2. Read [CONTRIBUTING.md](../CONTRIBUTING.md) and `skill/SKILL.md` (sections 0 and 1, then the files under `skill/references/` that it points to).
3. Create `data/<iso2>/` (the lowercase ISO code; if another folder already holds the code, the country's lowercase name, as with `australia`):
   ```bash
   python skill/scripts/wtdb.py init data/de --area "Germany"
   ```
4. Do the research, by hand or with an AI assistant. Tell the assistant the country, the scope (national, plus regional, plus local) and the depth (a first-pass seed is the default). It should start with the biggest supporters, not with tooling. Work on a branch, never on `main`.
5. Check your work:
   ```bash
   python skill/scripts/wtdb.py validate data/de
   python skill/scripts/wtdb.py checkquotes data/de --run R001     # quotes really are on the pages
   python skill/scripts/review_scan.py data/de                    # the evidence problems reviews keep finding
   python skill/scripts/profiles_wikidata.py data/de               # websites and socials from Wikidata
   ```
6. For a local map, build a boundary file from an open source with official codes (see `skill/scripts/topo_to_boundaries.py`) and name it in `meta.json`. If none turns up, ship without a map and open a follow-up issue.
7. Run through `skill/references/pre-pr-checklist.md`, then open a pull request. Every quote must be found on its source (`wtdb.py checkquotes`); readers report mistakes from the site.

## Build the site locally

```bash
pip install pycountry pillow          # Pillow is optional: without it pages share the default image
python scripts/build_site.py          # writes _site/
python scripts/serve.py               # http://localhost:8000
```

The site uses clean URLs (`/gb` with its map, `/gb/directory`, `/gb/time`, `/gb/seats`, `/gb/method`, a profile at `/gb/A0001`; `/countries`, `/parliaments` for every seat chart including the European Parliament at `/eu/seats`, `/resources` for polls, papers, reports and bills, `/method` and `/about`), so it needs a host that falls back to `index.html` for unknown paths. The Cloudflare deployment does this (`not_found_handling` in `wrangler.jsonc`), and `scripts/serve.py` does the same locally.

The maintainer deploys from a local checkout with `python scripts/deploy.py` (after a one-time `npx wrangler login`). Merging to `main` does not deploy by itself. Filtered views are shareable: `/gb/directory?place=United Kingdom > Wales&type=economist`.
