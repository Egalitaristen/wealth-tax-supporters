# Petitions on the Resources page: draft spec

Status: draft v6, settled by test run 5 (one predicted verdict change, none unpredicted); small wording and builder fixes applied. Nothing here is built.

## Why

The register shows who supports a wealth tax. A reader who agrees has nowhere to go next. A petition is the smallest action a visitor can take, so the Resources page should link the open ones, filterable by place like the other resources, with a clear "this is open now" signal.

## What counts as a petition

All four rules must hold. The test is on the petition's own text, read in a real browser: its title, its ask, and its stated proposal (the section a page calls "Why this matters", "Our proposal", "Que proposons-nous", "recommendations" and the like). Background text that only describes the problem is not part of the ask. A sentence counts as proposal when it names the tax and either has the decision-maker, "we" or "you" as its subject ("the government should introduce", "we demand", "you can enact") or uses a verb of asking or urging ("introduce", "enact", "pass", "support", "tax", "call on"), even inside a section that also holds background. A revenue estimate ("a 2% wealth tax could raise £24 billion") is background, not an ask; a sentence that only states facts about wealth or tax is background.

1. **It asks for a wealth tax, a billionaire tax or an extreme-wealth tax.** The ask is the title, the petition text and the stated proposal, as defined above. A wealth tax must be one of the stated asks. It passes when the ask does one of these:
   - asks for a tax on a mechanism word: wealth tax, a tax on net wealth, on assets, on fortunes, billionaire tax, millionaire tax, extreme-wealth tax, or the same in the page's language (impôt sur la fortune, impôt sur le patrimoine, Vermögensteuer, patrimoniale and so on). The word must be what is taxed: "the great fortunes must contribute" names the rich and not a tax on them, and does not pass;
   - describes a recurring tax on net assets or wealth above a threshold (for example "2% on assets over £10 million");
   - names a bill or tax that the register treats as a wealth tax. Names that count: Zucman tax (taxe Zucman), Ultra-Millionaire Tax Act, taxe sur les grandes fortunes, impôt sur la fortune (ISF), impuesto a las grandes fortunas, impuesto al patrimonio, Vermögensteuer, patrimoniale, IGF. A Billionaire Minimum Income Tax counts only when the text describes a wealth component. Add to this list when a new name is found.

   It fails when the ask is only "tax the rich", "tax the ultra-rich" or "make them pay their fair share" with no mechanism word and no named bill; when it taxes only income or only corporations; when it asks for a review, a study or a cap instead of a tax (a "cap net worth at £1bn" petition and a "Treasury review of a wealth tax" petition both fail); or when the wealth tax appears only as a funding source or an illustration for another aim ("fund X by taxing the rich"). A petition that asks for a wealth tax together with other asks passes, and the summary says so. A petition that earmarks the tax ("Enact a multi-millionaire wealth tax to fund research") passes when the tax is the thing it asks the decision-maker to enact; it fails when the tax is only a way to pay for something else the petition asks for. If the title names the tax, the funding test is not applied to the body; it applies to the body only when the title does not name the tax. A petition that asks for a referendum on a wealth tax counts as asking for it. The same borderline calls as grade B in `definition-and-grades.md` apply.
2. **A named organisation or official body runs it, or it is on a state-recognised platform.** Accepted:
   - an organisation, party, union or coalition (38 Degrees, 350.org, WeMove Europe, Oxfam, a party, a union);
   - a petition on an organisation's platform that the organisation promotes in its own name, even when a person started it (38 Degrees "Campaigns By You", 350 community petitions run by local groups). "Promotes" means the petition page itself carries the organisation's name as promoter ("Promoted by 38 Degrees", the organisation's logo or campaign number). The organisation's own domain counts as the same signal (an Oxfam petition on an oxfam domain, a Leadnow petition on leadnow.ca). Open platforms (Campact's WeAct, Change.org, openPetition) with no such line fail this bullet, and then need the Change.org/Avaaz bullet or an official's name;
   - an elected official's own petition, with `by` naming them and their office (a member of parliament's Change.org petition);
   - Change.org and Avaaz, when a named organisation runs the petition;
   - a parliament's own petition site (UK Parliament, Scottish Parliament, Bundestag, European Parliament);
   - a state-recognised citizens' initiative or petition platform whose signatures go to a legislature, a state body or the EU (manabalss.lv in Latvia, an Austrian Bürgerinitiative, a European Citizens' Initiative, a French référendum d'initiative partagée). Individual authors are fine here. The limit in "One entry per ask" below applies.

   Not accepted: a private person's petition on a general platform with no organisation behind it.
3. **A visitor can act on it today, or could when it ran.** Sign, send a message to a representative, or join a campaign list. A report about a petition, a press release, a news article, a request to take part in an event, or a letter that only lists signers (we already record those as `open_letter` evidence) is not a petition entry. When the register holds a news article that points to a petition, the petition page is the entry, not the article. A petition that ended stays (see below). A petition that the hosting site refused before it opened for signing (rejected, withdrawn or not admissible, on a parliament site or anywhere else) is not an entry. A petition whose signatures have been handed over to the decision-maker is still open if the page does not say signing has ended.
4. **It collects names for the campaign, not money.** A page whose main ask is a donation is not listed.

A petition that has ended stays in the register with `state: closed`, its end date and its last signature count, and is never deleted. The site shows only open ones by default (see Display).

## Data: `data/resources.json`

A fourth kind, `petition`, next to `paper`, `report` and `bill`. The build's `RESOURCE_KINDS` and the Resources page's `RES_KIND` gain `petition`. It does not get its own page (`PAGE_KINDS` is unchanged): the card links straight out.

Fields, using the existing ones where they fit:

| field | required | meaning |
|---|---|---|
| `country` | yes | a register folder (`gb`) or `global` |
| `kind` | yes | `petition` |
| `title` | yes | the petition's own title, in the page's language |
| `by` | yes | the organisation or body that runs it, in the page's language. A coalition names up to three (the host first), then "and others"; on a coalition's own site, the organisation whose site hosts it comes first. For an elected official, their name and office. For a parliament's site, the parliament's site; the person who started it is never named |
| `published` | no | the date signing opened if the page states it, else the date the petition was created, YYYY-MM-DD or YYYY-MM. Leave it out when the page states no full date. Never take it from a URL slug or a relative time ("1 year ago"). A relative time can still show that a petition is under or over 24 months old (see State) |
| `url` | yes | https link to the page where one signs |
| `summary` | yes | one sentence in English: what it asks, and from whom. Say if the wealth tax is one of several asks, and for a Bundestag-style petition which date `published` is |
| `state` | yes | `open`, `closed` or `unknown` (see State) |
| `ends` | no | YYYY-MM-DD, the end of the signing period, only if the page gives the full date (day, month and year, the year possibly from the page's own dateline). A day and month with no year is not entered; the maintainer can add the year in `note`. For a petition that is still being handled after signing ended, it is still the end of signing |
| `target` | no | the office or body it is addressed to, never the person (the Chancellor, a parliament, a commission) |
| `checked` | yes | YYYY-MM-DD of the last attempt to open and read the entry in a browser. If the attempt failed, `state` is unchanged and `note` says "Not reachable: site, reason, date" |
| `level` | no | `national`, `regional` or `supranational`, following the target, not the organiser: a petition run by a local group to a national parliament is `national`. A petition with `country: global` (addressed to the G20, the UN or a company group) is `supranational` |
| `people` | no | `folder:actor_id` of register entries (people or organisations) that run or front it; verify each id with a `grep -i` over every `data/*/actors.csv` |
| `signatures` | no | an integer: the headline number the page shows when last read (for a rounded figure such as "more than 250,000" use the rounded number and write "about" in `note`), with `signatures_as_of` (YYYY-MM-DD); omitted if the page shows none; `0` is written as `0` and shown as "0 signatures". For a petition with online and paper signatures, the total, and the split in `summary`. Kept while open, then kept as the final count |
| `goal` | no | the target number the page shows ("101,323 of 200,000" gives 200000). Omit if none is shown |
| `signal` | no | YYYY-MM-DD of a dated update or a dated recent-signer entry on the page; the proof of life that an open entry on Avaaz or Change.org needs (see State). `signatures_as_of` with a count counts as a signal too |
| `note` | no | a short line for the maintainer, never shown. Used for: the event a petition is tied to; the other petitions on the same platform with the same ask (see One entry per ask); where the evidence for "addressee gone" comes from; the reason for `open` on an old petition |

Build rules (in `load_resources`, same style as the bill check):

- `petition` needs `state` in `{open, closed, unknown}` and a `checked` date; the build stops without them.
- The build stops on: a `url` that is not https; a `url` that appears twice among petitions; a `country` that is neither a register folder nor `global`; a `people` id that is not in that folder's `actors.csv`; `ends` or `signatures_as_of` or `signal` that is not a full YYYY-MM-DD date; `signatures` or `goal` that is not a whole number. (The checks for bills are the precedent.)
- An open petition hosted on avaaz.org or change.org with neither `signal` nor `signatures_as_of` prints a warning.
- `ends` before the build date, with `state: open`, stops the build with "petition ended". This forces the check to happen (see Staleness).
- `published` more than 24 months before the build date, with `state: open`, prints a warning (it does not stop the build). A petition with no `published` is warned when `checked` is more than 30 days old at build time, and a date in `note` is used for its age if there is one.
- `state: unknown` is hidden from the default view like `closed`.

## State

- `open`: the page shows a working way to act, shows no "closed", "ended" or "victory" notice, no end date in the page has passed, and the cause has not moved on (see `unknown`). An entry on Avaaz or Change.org needs a dated signal to be `open`: a `signal` date, or a count with `signatures_as_of`.
- `closed`: the page says signing has ended, an end date on the page has passed, the platform shows a closed or victory marker, or the petition is tied to a dated event that the page names and the event is over. A petition tied to a vote, a bill or a session is `closed` the day after that event when the page names the day and month. The year may come from the page's own dateline (its publication date), never from outside the page, news or the URL. A relative time on the page ("3 years ago") is a page signal and may be used in State.
- `unknown`: the page reads but does not settle whether acting still means anything, or the page could not be read. "Moved on" needs positive evidence, and means one of: the addressee is no longer in post (the evidence may be another page read in the same run, or the register's own record of the office; write the source in `note`); an event named on the page is past; a bill named on the page is dead or has passed (the finder checks the bill and writes the date of the check in `note`; a check holds for one month; if the bill's status source cannot be reached, record "Not reachable" and leave the state as it is); or the page shows a date or a relative time ("3 years ago") that is more than 24 months old and no later update. A citation or update date on the page counts as a page date; a year that only appears in running text as a data year ("in 2020, billionaires...") does not. A page that shows no date at all is not evidence of age: the monthly check and the 30-day recheck catch a dead page. Hidden by default, listed for the maintainer's next monthly check. An old petition with a working form can be `open` only if the maintainer says why in `note`.

## Display

- A **Petitions** chip on `/resources`, with the open count, next to Papers, Reports and Bills. Default sort: closest end date first, then newest `published` (falling back to `checked` when there is none); entries with no end date follow, in the same order.
- The default view of the chip shows `state: open` only. A filter ("Include closed") shows the rest, labelled "Closed" with the end date, or "no end date stated" when there is none.
- Card layout: the existing card plus a "Sign" button label in place of the arrow, the organisation, the target, "ends 14 Dec 2026" or "no end date stated", "started 3 Mar 2025" ("started Mar 2025" when only the month is known) or "no start date stated", and the signature count with its date ("12,400 signatures on 14 Nov 2026", "101,323 of 200,000" when a goal is known).
- No size filter and no ranking: a small parliament petition under its response threshold is listed like any other. The no-prominence rule applies here too. The only limit is the one on duplicates (see One entry per ask).
- Country pages (second release): a short "Take action" strip listing that country's open petitions, hidden when there are none.
- Wording: the site argues for the tax, so "Take action" fits. Link out only; the site never collects signatures or personal data itself.

## Finding petitions

1. **Evidence we already hold.** About 12 petition pages in the register's campaign rows, plus news articles that point to petitions (38 Degrees, 350.org, WeMove, Oxfam, manabalss.lv, a Bundestag petition, Change.org pages). A one-off pass opens each URL, decides open or closed and writes the entry.
2. **Media scan and link finder.** Add to `media-scan.md`: when an article names a petition, record the petition page as a lead (`leads.py add --kind petition`) before anything else. A petition link inside an article is the most common way we will meet one. If the article names a bill or a vote, record that too.
3. **Search tier.** A Gemini or Codex search run per country for "petition wealth tax" in the country's language(s), on the platforms that host them: 38 Degrees, Avaaz, Change.org, Campact, openPetition, WeMove, Mijn Petitie, and parliament petition sites (UK, Scottish Parliament, Bundestag, European Parliament). Records are leads first; the maintainer approves the entry.
4. **Rule for the finder:**
   - **Read every petition page in a real browser**, not only through a page-summarising fetcher. The test run showed a fetcher reporting "no count" and "no status" on pages where the browser showed both. Look for "X of Y signatures", "verified signatures", a closed or victory banner, and a stated end date before writing "none".
   - Copy the title, the organisation, the start and end date if shown, the target, and the signature count with its date. Never infer a date.
   - If the petition names a bill, record the bill and check its status; if the bill is dead (voted down, lapsed, session ended) set `closed` or `unknown`, with a `note`.
   - Skip petitions the site refused before opening, and duplicates that the one-per-ask rule leaves out; say in the run note that they were skipped.
   - When the source is a news article, match the petition to the article before recording it: the signature count and the date the article gives must fit the petition's page (an article's "80,000 signatures" against a page that shows 53,923 is not the same petition until shown otherwise). If you cannot match them, record the lead with the mismatch noted.
   - A closed petition with no signatures and no media mention that is not a duplicate stays in the register.
   - A page the browser cannot reach (refused, blocked, unsearchable) is recorded in the run note as "Not reachable: site, reason, date". The finder is not required to cover it, and the gap is not read as absence.
   - A site with no usable search of its own (Scottish Parliament, the EP petitions portal, Mijn Petitie) can be searched with a web search restricted to the site (`site:`). The result is a lead, opened and read in a browser before it becomes an entry.
   - Say which platforms and how deep each search went, so a gap is not read as absence. "The run note" in this section is the description of the pull request that carries the finder's run.

## One entry per ask

Some platforms hold many near-identical petitions by different private authors (the Assemblée nationale's platform has ten or more Zucman-tax petitions). A platform is a registrable domain (oxfam.org.uk and oxfamfrance.org are two platforms; act.38degrees.org.uk and you.38degrees.org.uk are one). The register lists one entry per distinct ask per platform and per state: among open duplicates, the one with the most signatures; among closed duplicates, the one with the most signatures. An open petition is never folded into a closed one. The others are named in the kept entry's `note` (title, URL, count) and stay out of the site. A different ask on the same platform is a separate entry. An ask is distinct when it names a different rate, threshold, tax or bill, or has a different target. An adjective ("moderate", "temporary") does not make a distinct ask. A petition that names two taxes (for example the ISF and the Zucman tax) is its own ask. Petitions run by local groups of one organisation on a shared platform with the same text (350 community petitions) are one ask: the kept entry names the groups in `note`. The same author's petitions in different years are separate asks when their targets or the events they are tied to differ.

## Staleness

An open petition that quietly ended is worse than no petition. Layers:

1. **Stated end date.** If the page shows one, put it in `ends`. The build refuses an open petition whose `ends` has passed, so a stale entry blocks the release until someone closes it.
2. **Old and undated.** The build warns on an open petition older than 24 months (see Build rules). The monthly check also looks for the platform's own "closed" or "victory" marker, since Change.org and similar sites keep a Sign button on stale pages.
3. **Closed markers by platform.** The monthly check looks for the platform's own signal, because they differ:

   | Platform | What closed looks like |
   |---|---|
   | Change.org | a "Victory" or "Closed" banner; the Sign button can stay on an old page, so check the page's last update |
   | Avaaz | no marker; the page shows only recent signers, so a dated signal in `note` is required for `open` |
   | 38 Degrees | an update post, or the form replaced by a thank-you page |
   | Parliament sites (UK, Scottish, Bundestag, EP, Assemblée nationale) | the site's own status (Closed, Zeichnungsfrist beendet, Terminée) and an end date |
   | Citizens' initiative platforms | the platform's status text or the legislature's received or handled notice |
   | Organisation action pages (Oxfam, 350, MomsRising) | the form removed or replaced; a campaign tied to a dated event closes with it |

   Add a row when a new platform appears.
4. **Periodic check.** Extend `skill/scripts/check_resources.py` with a petition pass. It already reports dead, moved and blocked links. The petition pass adds, for every `state: open` petition:
   - the link is dead or redirects to a "closed" or "thank you" page: flag it;
   - the entry's `checked` is older than 30 days: flag it as "recheck";
   - `ends` is within 14 days: flag it as "ending soon" (so we can close it on the day);
   - `published` is older than 24 months: flag it as "old".
   It never edits a file. A blocked site is listed for hand-checking, as today. Every open petition needs a touch at least every 30 days; with about 25 open entries that is a monthly half-hour, and it is the maintainer's.
5. **Cadence.** A monthly check, tied to the media scan run. Tracked as a recurring GitHub issue ("Petition recheck") and as a line on the roadmap board. The check is the maintainer's; agents that find a petition set `state` and `checked` once and do not re-judge older entries.

## Out of scope

- Collecting or forwarding signatures, or any form on our own site.
- Pledges, donation pages and event sign-ups (these belong to a possible event tracker, not here).
- Ranking petitions by size or running comparisons between organisations.
- Translating petition text; the title stays in the page's language, and the summary is in English.

## Decisions (settled)

1. **Change.org and Avaaz:** accepted when a named organisation runs the petition; `by` names that organisation.
2. **Parliament petition sites** (UK, Scottish Parliament, Bundestag, European Parliament and others): included, with `target` set to the parliament and `signatures` filled in.
3. **First release:** the Resources chip only. The country "Take action" strips come second.
4. **Signature counts:** shown as of the last read (`signatures` with `signatures_as_of`). A count is never dropped for age. It stays until the petition closes. A closed petition stays in the register with its last count and its end date, and leaves the default view only.

5. **Duplicates (settled 2026-11-18):** one entry per distinct ask per platform, as the "One entry per ask" section defines it. That section is the rule; this line only records the decision.

## Build order

1. Schema and build rules, the Resources chip, the card variant (one PR).
2. One-off pass over the existing campaign URLs, with state and `checked` set (one PR).
3. `check_resources.py` petition pass and the recurring issue and roadmap line (one PR).
4. Link-finder and media-scan instructions, then a first per-country search run.
5. Country "Take action" strips.
