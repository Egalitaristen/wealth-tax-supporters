# Style for arguments

Arguments follow `content/stories/STYLE.md` without change: the Humanizer skill pass, the site's own voice, no hedging, a `[n]` source
on every number, losses reported plainly, stable `{#anchors}`. Two things differ:

- Length. An argument is one objection, answered in about 700 to 1,200 words of body, not 1,500. The pillar page, `why-tax-wealth`, has no length target: it is as long as the case needs, with anchored sections, a short opening that gives the whole case, and the surprising fact first in each section.
- The `objection` is written the way a person would say it, in their words, and the `answer` is a claim the page then proves with sources.

## Voice rules (9 November 2026, from the author's review of the first drafts)

These override anything above that softens them. They apply to every story and every argument page.

1. **English only.** No quotations in Swedish, German, French, Spanish, Norwegian, Danish or any other language in the text. Translate or paraphrase into plain English. We tell a story; we don't cite exact wording in the original language.
2. **No hedging and no points handed to the other side.** The page argues in favour of wealth taxation. A finding that favours the opponents is stated accurately if it matters, and answered in the same paragraph: does it outweigh what giving up the tax cost, can closing loopholes or an exit tax fix it, what use is a rich resident who stays and pays nothing, and what is wrong with the premise? No "a fair point", "the strongest objection", "the argument had something to it".
3. **A public voice, not a short academic paper.** Write for a curious general reader who wants to dig a little deeper and learn facts they probably don't know: plain words, short sentences, concrete detail, the surprising fact first, terms explained. No author lists in the prose ("X, Y, Z and W find"), no "working paper", "modelled", "peer reviewed" or "in the register's wording" in the sentences; those details belong in the numbered source list. Name a researcher only when the name helps a lay reader, and at most once.
4. Numbers stay exact, rounded as before, each with its `[n]` source. Pages carry `status: draft` until the author says final.

## What we learned writing the arguments (13 November 2026)

The stories file has the general lessons (`content/stories/STYLE.md`, section 'What we learned'): start from the register's data and primary sources, open every source, a law that has not passed is not a law, polls are whole percentages, dates go stale, run the Humanizer pass. These are the ones that apply to arguments in particular.

**Answer the objection with the mechanism, not a symptom.** The first version of `why-tax-wealth` opened on the share of income the richest pay in tax. That is a symptom, and it left the reader asking why a tax on wealth is needed at all. The rewrite opens on wealth: where it is held, how fast it grows, why the growth is never counted as income (shares nobody sells, companies that pay no dividends, holding companies), and what reaches the bank account (loans against shares, which are not income). Test every page: if the reader stops after three paragraphs, can they say why the answer is right?

**One concrete case beats three general claims.** Use the figure and the year for a real case from a source you opened (the 25 richest Americans' wealth up $401 billion in 2014 to 2018, 3.4% paid in federal income tax), then the general number behind it (billionaires pay about 0.3% of their wealth a year). Name individuals only where the source names them and the figure is public, and state the fact without comment.

**Derived numbers are computed from sourced ones.** A ratio ('more than five times as fast') or a sum is written only after you have calculated it from the numbers on the page, in the units you print. Say which period each figure covers. A chart is a way to show the page's own numbers; it never adds a new one.

**Objections are answered in one paragraph and linked to their page.** The pillar page answers each common objection in short and links to its own page. The objection pages link back to the pillar page's stable anchors: `#concentration`, `#growth`, `#unrealised`, `#bank`, `#lower-rate`, `#taxes`, `#difference`, `#minimum`, `#revenue`, `#power`, `#objections`, `#polls`, `#where`, `#who`, `#act`. Never rename one. The link check (`--strict-links`) fails on an anchor that does not exist.

**The share card.** `card_figure` is the single number that carries the page's lead (for the pillar page, 0.3%: the tax billionaires pay each year as a share of their wealth), and `card_label` says what it is in one sentence. The `answer` must fit four lines on the card: about 170 characters. Look at the PNG (`_site/og/arguments/<slug>.png`) after a build; a cut-off sentence is a bug.

**Charts.** Declare the chart in the front matter, place it once with `{{chart: id}}`, give it a `desc` for screen readers and a caption that names its source with `[n]`. Check it in light, dark and at phone width in the preview before you open the pull request.
