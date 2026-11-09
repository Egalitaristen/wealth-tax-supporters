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
author: Egalitaristen
layout: article                     # the only template
status: draft                       # draft (default) shows a Draft badge; final removes it
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
(default Egalitaristen), `layout`, `facts`.

## Body

The story dialect (`content/stories/README.md`): `## Heading {#anchor}` sections, `### `, paragraphs, lists, `**bold**`, `*italic*`,
`[text](url)`, `[3]` source references, `> quote`. Arguments do not use `{{supporters}}`.

Links between pages: `/arguments/<slug>` (add `#anchor` to point at a section), `/us` and `/us/story#anchor` for countries,
`/us/A0675` for a register entry, `/resources/<slug>` for a bill, `/calculator?w=...` for the calculator.

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
