# Arguments

One file per objection to a wealth tax, named by its URL: `content/arguments/they-will-leave.md` is `/arguments/they-will-leave`.
The hub is `/arguments`. The build (`scripts/build_site.py`) turns each file into static HTML (with its own title, description and
share card at `/og/arguments/<slug>.png`), a row in `data/arguments.json` (the hub and the site search) and a sitemap entry.

## Front matter

Same dialect as the country stories (`content/stories/README.md`), with three extra fields and no timeline:

```
---
title: The headline, a claim the page proves
kind: argument                      # always "argument"
objection: "The rich will just leave."   # the objection as people say it, shown in quotes on the hub and the card
answer: One or two sentences. Shown under the objection on the hub and on the share card.
standfirst: One or two sentences under the headline.
updated: 2026-11-08
layout: article                     # the only template
status: draft                       # draft (default) shows a Draft badge; final removes it
card_figure: 26%                    # optional: a big number for the share card, with card_label under it (both or neither)
card_label: What the label says.
charts:                             # optional: charts the body places with {{chart: id}} (see Charts below)
  - id: effective-rates
    type: bars
facts:
  - label: Wealth tax since
    value: 1840s
    source: 3                       # a source id, optional
sources:
  - id: 1
    title: Federal Tax Administration, Steuerbelastung in der Schweiz 2024
    url: https://www.estv.admin.ch/...
---
```

Required: `title`, `kind`, `objection`, `answer`, `standfirst`, `updated`, at least one source with an `https` url. Optional: `author`
(left out: pages carry no byline), `layout`, `facts`, `charts`, `card_figure` and `card_label`.

## Body

The story dialect (`content/stories/README.md`): `## Heading {#anchor}` sections, `### `, paragraphs, lists, `**bold**`, `*italic*`,
`[text](url)`, `[3]` source references, `> quote`. Arguments do not use `{{supporters}}`; their one block is `{{chart: id}}` (below).

Links between pages: `/arguments/<slug>` (add `#anchor` to point at a section), `/us` and `/us/story#anchor` for countries,
`/us/A0675` for a register entry, `/resources/<slug>` for a bill, `/calculator?w=...` for the calculator.

## Charts

A chart is drawn by the build as inline markup: no scripts, no external images, no files to fetch. It uses the site's colour tokens, so it works in
light and dark, and it is plain text underneath (a screen reader, a crawler and a phone all get the labels and values). Declare it under `charts:`
in the front matter and put `{{chart: id}}` on a line of its own where it belongs in the body. Every declared chart must be placed once, and the
build fails on an unknown id, an unknown field, or a `[n]` in a caption with no matching source. A caption names its source with the `[n]` reference.

Fields: `id` (letters, digits, hyphens), `type`, `title` (shown above the chart), `desc` (read out by screen readers, not shown), `caption` (shown
below, with `[n]` references), and for some types `data`, `unit`, `max`, `limit`, `tone`. In `title`, `desc` and `caption`, `{polls}`, `{poll_countries}`
and `{above_half}` are filled in at build time with the register's poll counts.

- `type: bars`: a labelled bar for each row of `data`. Rows are joined by `;`, and each is `label|value`, `label|value|tone` or `label|value|tone|shown`.
  A row with only a label is a heading for the rows under it. `tone` is `signal` (the site's red-orange, the default), `ink`, `gold` or `muted`; `shown`
  is the text printed at the bar's end when it differs from the number (a range such as `15% to 20%` is drawn at its middle). `unit` (default `%`) is added
  to a value, and `max` sets what a full bar means (default: the largest value).
- `type: poll-ranking`: the highest poll in each country that has one, from `data/<country>/meta.json`, with the flag, ranked. `limit: 12` shows the
  first 12 and folds the rest under "Show the other n countries".
- `type: status-map`: the world map, coloured from `data/wealth_tax_status.csv` (gold: has a wealth tax, silver: used to have one, as on the site's own map), with the countries
  listed as text under it. It is drawn from the same outlines as the site's map, simplified.

The code is `scripts/charts.py`, the placeholder swap is `argument_body` in `scripts/build_site.py`, and the styles are the `.chart` block in `site/style.css`.
Use only numbers that are in the page's `sources`; a chart is a way to show those numbers, not a place to add new ones.

## Order and short titles

The hub order, and each page's short title (breadcrumb, previous/next links, card label), is the list `ARGUMENT_ORDER` in
`scripts/build_site.py`. `why-tax-wealth` is first and the lead card. A new page is added to that list, otherwise the build fails.

## What the build checks

It fails on: a missing required field; an unknown front matter field (a `timeline` included); a duplicate slug or source id; a `[n]`
in the body or a fact `source` with no entry in `sources`; a source without an `https` url; a file that is not in `ARGUMENT_ORDER`
(or an entry with no file). It prints, without failing, sources that are never cited and **internal links that do not resolve**: every
`/arguments/...`, country, register entry (`/us/A0675`), section anchor and `/resources/<slug>` link in the body is checked against
what the build wrote. `--strict-links` turns the link report into a failure.

## Writing

`STYLE.md` points to the house rules in `content/stories/STYLE.md`; they apply to arguments unchanged.

## Checking a page quickly

`python scripts/build_site.py --only arguments` builds the section, with the countries its pages link to, into `_site_only/` (use
`--only arguments co` to add another country). Totals are partial there, so never deploy it. A full build (no flag) is what CI and deploy use.
