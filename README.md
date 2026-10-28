# Wealth Tax Supporters

An open, sourced register of who publicly backs an actual wealth tax, built country by country: 28 countries and three international bodies so far. Each country is a folder of CSV files, and every entry rests on a dated source and a quote that is on the page. The site built from them is deployed to Cloudflare at [wealthtaxsupporters.com](https://wealthtaxsupporters.com).

> **The data is AI-generated and may be wrong.** Every entry links to a source, and many rows have not yet been checked by a person. If you spot a mistake or want an entry removed, use the **Report** link on the site, or [open an issue](../../issues/new?template=data-report.yml).

## Why this exists

The aim is to make it easy for people who share the view that wealth should be taxed to find each other, wherever they are. The place to start is the public record: the politicians, parties, organisations, economists and commentators who have said so, each with a source. Seat charts for each parliament show which seats are held today by someone on the register. A community layer for ordinary supporters is planned, but not built. See [docs/community.md](docs/community.md).

## What is here

| Path | What it holds |
|---|---|
| `data/<iso2>/` | One database per country or region, for example `data/gb/`. Plain CSV files plus a `meta.json`. |
| `skill/` | The research skill for people and for AI coding assistants. `SKILL.md` holds the goal and the ground rules; `references/` holds the definition and grades, the data format (its column lists are generated from `wtdb.py`), the research run (discover, layers, follow the leads), geography, seats, the pre-pull-request checklist, the election-refresh guide, the source playbook and one guide per country. Helper scripts: `wtdb.py` (init, add, validate, checkquotes, status), `review_scan.py`, `leads.py`, `seats.py` and its adapters, `seat_sweep.py` (sitting members still to search), `match_wikidata.py`, `profiles_wikidata.py`, `topo_to_boundaries.py`. |
| `refine/` | The refinement workflow (`SKILL.md`) for supporters already in a register: links, finer places, more statements, and a check that support is still current. Uses the scripts in `skill/scripts/` (`refine_queue.py`, `archive_sources.py`). |
| `site/` | The static front end: one page and one script, no framework. Home with search and a zoomable world map, country pages (area map, seat charts, directory, timeline, method), a page per supporter, a global directory, the parliaments and resources pages, method and contribute pages. Maps zoom with the mouse wheel or by pinching. |
| `scripts/build_site.py` | Turns `data/` into the site data, a search index and CSV downloads. Standard library plus `pycountry`. |
| `scripts/share_cards.py`, `scripts/fonts/` | Link-preview images for every page (home, directory, each country page including its seats and directory pages, each supporter), drawn with Pillow; the seats card shows the chambers as seat charts. The build also writes a small HTML file per page with its own title, description and image, so previews on Discord and social media match the page. |
| `scripts/serve.py` | Serves the built site locally the way Cloudflare does (unknown paths fall back to `index.html`). |
| `scripts/deploy.py`, `wrangler.jsonc` | Build and deploy the site to Cloudflare from a local checkout. |
| `docs/`, `infra/` | The community plan, and the Cloudflare setup and draft database schema. The suggestions database is deployed; the community schema is a draft. |

Twenty-eight countries so far, all built with AI assistants and all work in progress. The site shows the live counts; each folder's `area_profile.md` says what was searched and what was not.

| Country | Folder | Map (local tier) | What it rests on |
|---|---|---|---|
| Australia | `data/australia/` | 548 local government areas | The Greens' billionaire-tax plan and their senators' speeches, Oxfam Australia, the Australia Institute and its authors, ANU researchers, socialist parties, a manufacturing union, campaigners (the folder is `australia` because `au` is the African Union) |
| Belgium | `data/be/` | 581 municipalities | Wealth-tax bills of the PTB-PVDA, PS and Groen and their cosponsors, party manifestos, unions |
| Brazil | `data/br/` | 5,570 municípios | Every wealth-tax bill in the Câmara since 2010 with its authors, the 30 October 2024 roll call, the G20 billionaire-tax track, the "Tem Um Elefante Na Sala" coalition |
| Canada | `data/ca/` | 4,886 census subdivisions | The 2020 NDP motion for a 1% tax on wealth above CAD 20m, convention resolutions, a Quebec manifesto, Patriotic Millionaires Canada, unions |
| China | `data/cn/` | 361 prefectures | A few economists and scholars who propose a wealth or minimum wealth tax, and Oxfam Hong Kong |
| Egypt | `data/eg/` | No map yet | Economists, politicians and business figures who argue for a wealth tax in Egypt, and a few organisations |
| Finland | `data/fi/` | 308 municipalities | MPs who signed the 2012 wealth-tax bill (LA 55/2012 vp) and a 2022 budget motion, plus other public figures and organisations |
| France | `data/fr/` | 34,790 communes | Assemblée and Sénat roll calls on the "taxe Zucman" and earlier ISF bills, the Le Monde appeal, economists, NGOs, unions |
| Germany | `data/de/` | 10,939 Gemeinden | Bundestag sponsors since 2010, party programmes, the alliance "Vermögen besteuern jetzt", unions, economists |
| India | `data/in/` | 731 districts (provisional) | The 2024 World Inequality Lab proposal, the Left parties, the central trade unions, Oxfam India, the Tax the Top campaign |
| Indonesia | `data/id/` | 514 districts and cities | CELIOS, PRAKARSA and the FPBI alliance white paper, politicians who proposed a wealth tax, a student league, economists |
| Ireland | `data/ie/` | 31 local authorities | Labour, the Social Democrats, People Before Profit, Sinn Féin and the Greens and their TDs, Oxfam Ireland, the Irish Congress of Trade Unions, economists |
| Italy | `data/it/` | 7,896 comuni | The May 2024 Manifesto of 134 economists from 50 universities, the May 2026 popular initiative bill "1% Equo", the 2020 Orfini–Fratoianni and 2024–2026 AVS budget amendments and fiscal package, Fondazione Demo's Zucman-tax dossier, CGIL, Oxfam Italia, Sbilanciamoci!, Forum Disuguaglianze e Diversità, Carlo De Benedetti and a regional/local sample |
| Japan | `data/jp/` | 1,749 municipalities | Diet speeches naming the tax, the Communist, Social Democratic and Reiwa party policies, a citizens' coalition and scholars |
| Malaysia | `data/my/` | 144 districts | MPs and parliamentary questions, PSM, economists, civil society |
| Mexico | `data/mx/` | 2,478 municipios and alcaldías | Initiatives for a tax on net wealth above MXN 100m and their deputies, Oxfam México, Fundar, the Alianza contra la Desigualdad, economists and campaigners |
| Netherlands | `data/nl/` | 342 gemeenten | The Box 3 wealth-tax bill and its cosponsors, motions, party manifestos, Zucman's testimony, the Davos letters |
| New Zealand | `data/nz/` | 67 territorial authorities | Parties, individual politicians, tax-justice campaigns, unions, economists, commentators, faith and business |
| Nigeria | `data/ng/` | 774 local government areas | The Oxfam-led 2024 report and its authors, Oxfam's 2026 call for a 1% tax, a Lagos wealth-tax conference, op-eds |
| Norway | `data/no/` | 357 kommuner | Parties, unions, think tanks, economists and commentators who defend the formuesskatt in their own words |
| Poland | `data/pl/` | 2,479 gminas | Razem and the Greens, OPZZ, economists and commentators, MEP votes; 251 manifesto signatories are flagged as implied support |
| Singapore | `data/sg/` | 55 planning areas | The Workers', Progress Singapore and Red Dot United party platforms, MPs' motions, economists and NGOs |
| South Africa | `data/za/` | 213 metropolitan and local municipalities | The EFF, the South African Communist Party, COSATU and other unions, MPs, the Institute for Economic Justice, Black Sash |
| Spain | `data/es/` | 8,125 municipios | The 7 June 2022 Congreso roll call, Ley 38/2022, Sumar, ministers, Oxfam Intermón, Gestha, the big unions |
| Sweden | `data/se/` | 290 kommuner | Riksdag members of the left parties, unions, economists; the regional and local sweep is still to do |
| Ukraine | `data/ua/` | 1,769 hromadas | Economists and policy authors (the GROWFORD Institute and academic papers) and a parliamentary speech; thin so far |
| United Kingdom | `data/gb/` | 361 council districts | Councils, MPs, unions, economists and the "Proud to Pay" millionaires' letter |
| United States | `data/us/` | 3,141 counties | State legislators and Congress, cities and counties, unions, economists, wealthy signers |

Every country's register goes down to its lowest tier of local government, and the map shows the same tier where an open source with official codes exists, so maps are comparable; see `skill/SKILL.md` 6.7. A missing map is a follow-up issue, not a blocker. Supporters need their own evidence: a party's platform is recorded on the party, not on each of its members (`skill/references/definition-and-grades.md`, section 4).

Three bodies above the countries have a register of their own for chambers and seats only: the European Parliament (`data/eu/`, 720 seats), the United Nations General Assembly (`data/un/`, one dot per government) and the African Union's Pan-African Parliament (`data/au/`). A supporter who sits in one is recorded in their own country's register.

## What counts

- **Supporters only.** Opponents and sceptics are not recorded as actors.
- **An actual wealth tax:** a recurring tax on net wealth, a one-off levy, or a minimum tax on billionaires. Income, property and capital gains reforms alone do not count.
- **Dated, linked source** and a short quote for every entry. Grades: **A** explicit (a formal act or a stated design), **B** named, **C** implied.
- **Public figures and organisations only.** Petition signers and other private individuals are never recorded.
- People are assumed alive unless a death record is found; anyone found dead is removed.
- **Seats:** a seat on a parliament's chart is lit only for someone found on the chamber's own official list today. An unlit seat means nothing found, never opposition.

## How the research works

The goal is a trustworthy register of who publicly backs an actual wealth tax, with the evidence behind every name. A research run starts by asking the open web broadly, in every official language of the country, who has argued for a wealth tax and when, and turns what it finds into a queue of leads. It then touches every layer once, going after the most prominent supporters first (legislature, parties, coalitions and unions, economists, commentators, wealthy and business, regional), and follows the leads (co-signers, people quoted, coalition partners, the next document in the chain) until the queue is empty or low yield. Local sweeps are sampled first and expanded only where they pay. Coverage is reported honestly, so a blank means "not searched", and a run ends with a checklist and a plan for the next one. After an election the seat charts are refreshed from the parliament's new official list. The details are in [`skill/SKILL.md`](skill/SKILL.md); read its sections 0 and 1 first.

## Add your country

1. Fork this repository.
2. Read [CONTRIBUTING.md](CONTRIBUTING.md) and `skill/SKILL.md` (sections 0 and 1, then the files under `skill/references/` that it points to).
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

## Roadmap

Planned and scheduled work is public: the [roadmap project](https://github.com/users/Egalitaristen/projects/3) is the live board, [ROADMAP.md](ROADMAP.md) explains it, and the items are the issues labelled [`roadmap`](../../issues?q=is%3Aissue+label%3Aroadmap). Each country has an issue for refreshing its seats after its next election, with the date it waits for.

## Licences

- Code: [MIT](LICENSE).
- Data in `data/`: [CC BY 4.0](DATA_LICENSE.md). Quotes are short extracts from cited sources and stay under their owners' copyright.

## Corrections and removals

Use the Report links on the site, or open a [data report](../../issues/new?template=data-report.yml). Reports are public issues, so do not paste private information into them.
