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
author: Egalitaristen
layout: article          # article (A) or profile (B)
facts:
  - label: Wealth tax since
    value: 1840s
    source: 3            # a source id, optional
timeline:
  - year: 1840
    text: What happened.
    source: 2
related:
  - label: Switzerland's supporters
    href: /ch/directory  # site-relative or http(s)
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
  `## How it works {#how}` to fix the anchor so later wording changes never break links. `timeline`, `keep-exploring`, `sources` and `src-*` are reserved.
  Text before the first `##` is the introduction.
- `### Subheading`, paragraphs, `- ` lists, `1. ` lists, `**bold**`, `*italic*`.
- `[text](https://...)` or `[text](/ch/directory)`: only http(s) and site-relative links survive.
- `[3]` is a numbered source reference, linked to the entry with `id: 3` in `sources`.
- `> text` is a pull quote. A last line `> — Name, source` is its attribution.
- No raw HTML, images or tables.

Stable URLs: `/<folder>#<anchor>` and `/<folder>/story#<anchor>`.

## Layouts

`layout: article` is a calm long-form column with a Key facts box. `layout: profile` is implemented by `renderStoryProfile` in `site/app.js`
(until it is built it falls back to the article layout). Both read the same schema.
