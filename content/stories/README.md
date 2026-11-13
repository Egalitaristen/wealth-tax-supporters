# Country stories

One file per country, named after its `data/` folder: `content/stories/ch.md`. A country with a story opens on it:
`/ch` and `/ch/story` show the Story tab, the map moves to `/ch/map`. A country without a file is unchanged.
The build (`scripts/build_site.py`) turns each file into `data/story-<folder>.json`, a share card (`/og/<folder>-story.png`) and
static HTML for `/<folder>` and `/<folder>/story`.

## Front matter

```
---
title: Switzerland has taxed wealth for 150 years
standfirst: One or two sentences, shown under the headline and on the share card.
updated: 2026-11-05
layout: article          # the only template
status: draft            # draft (default) shows a Draft badge; final removes it
facts:
  - label: Wealth tax since
    value: 1840s
    source: 3            # a source id, optional
timeline:
  - year: 1840
    text: What happened.
    source: 2
sources:
  - id: 1
    title: Federal Tax Administration, Steuerbelastung in der Schweiz 2024
    url: https://www.estv.admin.ch/...
---
```

One value per line, quotes optional. `source` ids are numbers; every id used in the body or in a fact or timeline row must exist in `sources`.

## Body

Markdown, restricted on purpose (the build escapes everything and allows only this):

- `## Heading` starts a section. Its anchor is the slugified heading (`## How it works` is `#how-it-works`); write
  `## How it works {#how}` to fix the anchor so later wording changes never break links. `timeline`, `sources` and `src-*` are reserved.
  Text before the first `##` is the introduction.
- `### Subheading`, paragraphs, `- ` lists, `1. ` lists, `**bold**`, `*italic*`.
- `[text](https://...)` or `[text](/ch/directory)`: only http(s) and site-relative links survive.
- `[3]` is a numbered source reference, linked to the entry with `id: 3` in `sources`.
- `> text` is a pull quote. A last line `> — Name, source` is its attribution.
- `{{supporters}}` on a line of its own draws the live "Who supports it" block: parties, politicians, economists and unions from the country's register, with counts, one line of role per entry, links to each entry and to the directory. Use it once, in the section on who backs the tax, below an editorial paragraph.
- No raw HTML, images or tables.

Stable URLs: `/<folder>#<anchor>` and `/<folder>/story#<anchor>`.

## Writing

Read `STYLE.md` before writing or editing a story; it points to the Humanizer skill, lists the house rules and sets out what we learned from the first stories (start from the register's data and primary sources, a law that has not passed is not a law, polls as whole percentages, dates go stale).

### Before you write a story

1. Read the country's files: `data/<cc>/meta.json` (polls, notes), `actors.csv` and `evidence.csv` (who backs it, with sources), `documents.csv`, `bodies.csv` and `seats.csv`, the records guide `skill/references/records/<cc>.md` if there is one, and the country's row in `data/wealth_tax_status.csv`.
2. Read its bills and reports in `data/resources.json`; link a bill as `/resources/<slug>` and a poll as `/resources/<country>-poll-<pollster>-<year>`.
3. Open the primary sources and check every number against them. Put each in `sources` with its `https` url.
4. Decide what the country's status is, as the law stands today: has a tax in force (gold), had one (silver), or neither. A bill that has not passed is a bill. Do not change `data/wealth_tax_status.csv` in a story pull request unless the law is enacted and published, and then say so in the description.
5. Write, run the Humanizer pass, build with `python scripts/build_site.py --strict-links`, look at the page in the preview, and open the pull request as a draft with the list of anything you could not verify.

A new country's story may follow a thin register; write what is verified, and open an issue "<Country>: grow the register" with the leads left.

## Layouts

`layout: article` is the story template: the section list on the left (a "Jump to" control on phones), the text in the middle, Key facts on the right (under the standfirst on phones).

## Checking a story quickly

`python scripts/build_site.py --only co` builds just that country into `_site_only/` in a few seconds, with the story, its sources and the `/co` and `/co/story` pages. Totals on the home page are partial in that build, so never deploy it. A full build (no flag) is what CI and deploy use.
