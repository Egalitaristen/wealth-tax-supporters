# Bluesky scan

A scan of public Bluesky posts for supporters the other scans miss. Posting is far easier than being interviewed or writing an article, so this finds people and organisations that never reach the press. It is a source of leads and of extra evidence, not a register by itself.

## Running it

```
python skill/scripts/bluesky_scan.py open  --since 2026-11-02 --out bsky_open.jsonl      # phrases and hashtags in every language
python skill/scripts/bluesky_scan.py known --country gb --since 2026-01-01              # the same phrases, only from accounts already in a register
python skill/scripts/bluesky_scan.py show  bsky_open.jsonl --min-score 2 --new-only      # read it, best candidates first
```

`open` is the main mode. `known` is lower priority: people already in the register will mostly turn up in `open` too, and each match is extra evidence for them. The query lists are in `references/bluesky-queries.json`; add a language or a phrase there.

The script only collects. It never writes to the register. It skips authors who set the `!no-unauthenticated` label, which means they asked not to be shown to logged-out viewers.

## Reviewing what it collects

Read every author in full. Keywords, scores and follower counts only set the reading order; they never exclude anyone. For each author read the whole bio, the pinned post, every matching post (with the post it answers), the alt text of images and the title of any linked article. An image-only post carries its message in the alt text.

Then decide in this order: **who, what, how strong.**

### Who counts

An author goes on the list only if all four hold:

1. **A real identity.** A real name, or an organisation or established brand whose public work is the account. Anonymous and throwaway handles never count, however large their audience. A first name with a slogan ("Malena-PRO-CHOICE") is not a name. A name with no way of confirming it is a lead at most.
2. **A stated role or body of public work.** The bio or pinned post says what they are: a politician, party, union, think tank or campaign group; an economist or academic; a journalist or commentator who publishes; a writer, artist or creator with published work; an activist or campaigner with a public cause. A political opinion is not a role. A big audience is not a role, and neither is a small one a reason to leave someone out. Influencers and creators who publish commentary count as journalists (opinion, video, podcast) or cultural figures or campaigners; credentials are not required.
3. **A second source for the role.** Academics, economists, officials, party and organisation staff and journalists must be confirmed on their institution's or publication's own page, in Wikidata or in the register. A writer, artist or activist can be confirmed by their published work (a book, comic, site, campaign). If the role cannot be confirmed, record a lead with the note "role unconfirmed" and do not add a supporter. A self-declared role in a bio is a reason to look, not a confirmation. If the only evidence a person exists is the account itself, they are not identified.
4. **Their own statement** (next section).

Not on the list: private people, however clearly they support a wealth tax; news outlets, aggregators and bots; reporters who report; accounts that reply with a one-line joke or only repost; accounts of people who oppose it.

### Their own statement

- It must be in their own words. A repost, a headline, a quoted post or a link with no comment is not a statement.
- It must refer to a tax on the stock of wealth (section 2): "wealth tax", "billionaire tax" on net worth, "taxe Zucman", "Vermögenssteuer", "impuesto a las grandes fortunas" and equivalents. Not "tax the rich", "fair share", mansion, inheritance, income or capital-gains taxes, or closing a loophole.
- A cap on wealth counts: a 100% tax above a threshold is a rate and a threshold.
- Grade it (section 3). **A**: a rate or a threshold, a named bill or proposal. **B**: a wealth tax or billionaire tax by name, supported. **C**: support only implied, for example regret that a wealth-tax measure failed. A single post caps at C or B; several posts over time, in their own words, support B or A.
- Check the whole account before deciding: search the author's posts back to 2024 for the same phrases (`searchPosts` with `author=`), because one reply can understate a long record.
- A post that reports a ballot result or a vote count is not evidence of that result. A partial count is not a result either. Check the official source before repeating one.

## What to do with a hit

- Already in the register (the scan marks name and handle matches): add the post as a new statement for that person if it is new evidence.
- Not in the register, and a public figure or organisation of an included kind with a statement graded A, B or C: add a **lead** (`leads.py add`) with the post URL, and a later run on that country turns it into a supporter. Do not add a supporter from a social post alone unless the run has confirmed who they are.
- Anything else: skip it. Record nothing about private people.

## Evidence rules specific to posts

- Quote the post as written in the original language, with an English translation in `quote_en`; the URL is `https://bsky.app/profile/<handle>/post/<id>`.
- Archive the post (`archive_sources.py`) when you use it. Posts get deleted.
- Use the post's own date. Bluesky opened to the public in 2024, so posts are recent evidence.
- Public posts and the public profile only. No direct messages, no follower lists, no personal details.
- A post that mentions a ballot result or a vote count is not evidence of that result: check the official source before repeating one.
