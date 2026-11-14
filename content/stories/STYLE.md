# Style for country stories

Every story goes through the Humanizer skill before it is committed. The skill is installed at `~/.claude/skills/humanizer/SKILL.md` (blader/humanizer v3.1.0, MIT). Read it in full and run it in file mode on the story: change the prose only, keep the front matter, source ids, links, numbers and facts exactly, and re-check every sentence you change against its source id. Match the voice of the About page copy in `site/app.js` (plain sentences of medium length, commas and colons, no dashes in prose).

The skill's patterns most likely to appear in a story, strongest first: not-X-but-Y contrasts, one-line closers, forced triads, dashes as connectors, stacked qualifiers, stock AI words (pivotal, crucial, landscape, underscore, showcase, testament, vibrant, delve), inflated significance, -ing riders (highlighting, reflecting, ensuring), "serves as" for "is", bold as decoration, headings that are not in sentence case, and sentences that describe the page instead of the subject.

## House rules on top of the skill

- No byline. Leave `author` out of the front matter. The voice is the site's own: plain and confident.
- No hedging. State what the sources show, then what the site argues from it. No "perhaps", "arguably", "may", "might", "seems to", "tends to", "it could be said", "some would say". Where a source itself gives a range or an estimate, give it with its year, in the source's own terms. No hedging boxes and no "the strongest objection that remains": answer a common objection with evidence.
- Source ids on every number. Each figure carries `[n]` pointing to an entry in `sources`, with its year in the text. Use only sources that were opened. Name people and parties and link them to their register entry. Attribute by name, never "experts say".
- Report losses plainly. A vote that went against us is stated once, with its result.
- No length target: the story is as long as the case needs, and a longer page earns its length with anchored sections, a short opening and the surprising fact first in each section. Facts, timeline and sources come on top.
- Anchors are stable URLs. Sections are `##` with a fixed anchor, such as `## Cantons undercut each other {#competition}`. Never change an anchor once a link to it exists.
- Live register block. Put `{{supporters}}` on its own line in the section on who backs the tax, below an editorial paragraph. Do not repeat its lists by hand.
- Prose only in the pull-quote attribution. The line starting with a dash after a quote is markup, not prose.

## Voice rules (9 November 2026, from the author's review of the first drafts)

These override anything above that softens them. They apply to every story and every argument page.

1. **English only.** No quotations in Swedish, German, French, Spanish, Norwegian, Danish or any other language in the text. Translate or paraphrase into plain English. We tell a story; we don't cite exact wording in the original language.
2. **No hedging and no points handed to the other side.** The page argues in favour of wealth taxation. A finding that favours the opponents is stated accurately if it matters, and answered in the same paragraph: does it outweigh what giving up the tax cost, can closing loopholes or an exit tax fix it, what use is a rich resident who stays and pays nothing, and what is wrong with the premise? No "a fair point", "the strongest objection", "the argument had something to it".
3. **A public voice, not a short academic paper.** Write for a curious general reader who wants to dig a little deeper and learn facts they probably don't know: plain words, short sentences, concrete detail, the surprising fact first, terms explained. No author lists in the prose ("X, Y, Z and W find"), no "working paper", "modelled", "peer reviewed" or "in the register's wording" in the sentences; those details belong in the numbered source list. Name a researcher only when the name helps a lay reader, and at most once.
4. Numbers stay exact, rounded as before, each with its `[n]` source. Pages carry `status: draft` until the author says final.

## What we learned writing the first stories and arguments (13 November 2026)

These come from the stories for 30-odd countries and from the rewrite of the pillar argument. Follow them for every new page.

**Say why the tax is needed before you say what happened.** A story or argument that opens on a statistic the reader cannot interpret (a ratio, a rank) misses the point. The first three paragraphs must let a reader who stops there say what the tax is for, in plain words, with one concrete number. Show the mechanism as a chain of plain steps and name each step. Wealth, not income, is the subject: where it is, how fast it grows, why that growth is never counted as income, and how the owners spend it (loans against shares are not income).

**Start from what the register holds, then go to primary sources.** Before writing, read the country's `data/<cc>/` files, its bills and reports in `data/resources.json`, its polls in `meta.json` and its row in `data/wealth_tax_status.csv`. Then open the primary sources (the law in the gazette, the parliament's record, the statistics office) and check each number against the page. Never write a number from a search snippet, a summary or memory. If a source cannot be read (a PDF that is only an image, a site that blocks scripts, a paywall), do not use its numbers; say in the pull request what could not be read.

**A law that has not passed is not a law.** A country gets the gold border and the words "has a wealth tax" only when the law is enacted and published. A bill that passed one chamber, or a government proposal, is described as exactly that, with its date and next step. Check the parliament's record on the day you write, because news stories run ahead of it. The same goes for ballot results: say the result once, with its date and whether it is certified.

**Polls are whole percentages.** A poll result is written as a whole number ("83%"), never "about two in three" or "82.9%". The detail (how the result split, who paid for the poll, the exact question) lives on the poll's own page, `/resources/<slug>`, and the text may link to it. Say whose poll it is and when it was taken. When a country has several, the page says "the highest poll" or names the one it means.

**Dates and counts go stale.** Say "as of 13 November 2026" next to a count that can change. Where a chart or a placeholder can fill the number at build time (`{polls}`, `{poll_countries}`), use it instead of typing it. Do not hard-code how many countries or supporters the register has in a sentence that will be read in a year.

**Run the Humanizer pass.** It is not optional, and it is easy to skip when a build is waiting. Read the finished page aloud once: short sentences, the surprising fact first, no sentence that describes the page instead of the subject. Check arithmetic in the units you print (3.4% is 3.4 cents on every dollar, not on the hundred dollars).

**People.** Name a person only when a public, sourced fact about them matters and the name helps the reader. Give the figure and the year, link the register entry, and do not characterise them. No invented quotes, studies or endorsements. A thin register is fine: write what is verified and list the leads you did not finish in an issue titled "<Country>: grow the register".

**Delivery.** A page stays `status: draft` until the author says it is final. The pull request lists what changed, every source added, and anything you could not verify and left out. Pages are written in English; quotes from other languages are translated or paraphrased. A session never merges; the maintainer reviews and merges.

## Refined rules for stories (14 November 2026)

What we learned writing the argument pages, applied to every country story. A story is revised against these, one country at a time, after its records work (issue labels `stories` and `records`).

1. **Open on why the tax matters or what it did, with one concrete figure.** The first three paragraphs let a reader who stops there say what happened in this country and why it matters. Start from the surprising fact, not a ratio or a rank.
2. **One concrete case beats three general claims.** Use the figure and the year for a real case from a source you opened. Derived numbers (a ratio, a share, a sum) are computed from sourced ones, in the units you print, and say which period they cover.
3. **Dates, counts and status are current and exact.** Check the parliament's record, the gazette and the register on the day you write. A bill is a bill. A vote or an election result is stated once, with its date and whether it is certified.
4. **Argue for the tax, plainly.** No hedging, no points handed to the other side, English only, a public voice. Names of researchers and phrases such as "working paper" stay in the source list.
5. **Link to the arguments.** Where the story answers an objection, link the argument page (`/arguments/<slug>`) and, for the mechanism, the pillar anchors (`/arguments/why-tax-wealth#unrealised`, `#bank`, `#minimum`, `#revenue`). The link check fails on an anchor that does not exist.
6. **Two section shapes**, by kind of country. A country with a tax in force: the surprising fact, what the tax is and how it works, what it raises, the leaks and their fix, the objections with the figure, the politics now, who backs it. A country that dropped it: what the tax was, why it went, what the repeal cost, what has been tried since, who backs a return, what a new tax would need. Keep every existing anchor.
7. **A share card figure and one or more charts.** `card_figure` is the single number that carries the story's lead; the label says what it is in one sentence. Charts (bars only) show the story's own sourced numbers: revenue by year, the threshold, a poll, the cost of a repeal. A chart never adds a new number. Look at the card (`_site/og/<folder>-story.png`) and the chart in light, dark and at phone width before opening the pull request.
8. **Trim.** A run of country-by-country or year-by-year figures becomes a chart or is cut to the two that matter. Read it aloud once. The page stays `status: draft`, and the Humanizer pass is not optional.
