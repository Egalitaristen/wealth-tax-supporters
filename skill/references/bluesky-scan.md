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

One review per author, and the order is: **who, then what, then how strong.**

1. **Who.** Read the profile (name, handle, bio). The register includes politicians, parties, organisations, unions, economists, journalists and other public figures (`definition-and-grades.md` section 4). It does not include private people. If the bio does not make clear that they are a public figure or an organisation of an included kind, stop: they are not a lead. A verified account or a handle on a domain they control (`name.parliament.uk`) is strong evidence of who they are; a bio alone is not. Confirm an office or role from a second source (a party or parliament page, Wikidata) before adding anyone as a supporter. The script's `hints` and `score` only set the reading order.
2. **What.** Read the post itself. The post must support an actual tax on the stock of wealth (section 2). Do not count: news posts that only report or link a story, posts that argue against, sarcasm, a mansion, inheritance or income tax, a generic "tax the rich" or "billionaires should pay their fair share", and posts from media accounts reporting a ballot or a bill without saying what they think.
3. **How strong.** Grade it (section 3): A is a formal act or specifics (a rate, a threshold, a named bill), B is "a wealth tax" by name, C is weaker or ambiguous. Most single posts are B. A journalist who posts a wealth-tax story is not a supporter; one who repeatedly argues for it is.

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
