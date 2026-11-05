# Style for country stories

Every story goes through the Humanizer skill before it is committed. The skill is installed at `~/.claude/skills/humanizer/SKILL.md` (blader/humanizer v3.1.0, MIT). Read it in full and run it in file mode on the story: change the prose only, keep the front matter, source ids, links, numbers and facts exactly, and re-check every sentence you change against its source id. Match the voice of the About page copy in `site/app.js` (plain sentences of medium length, commas and colons, no dashes in prose).

The skill's patterns most likely to appear in a story, strongest first: not-X-but-Y contrasts, one-line closers, forced triads, dashes as connectors, stacked qualifiers, stock AI words (pivotal, crucial, landscape, underscore, showcase, testament, vibrant, delve), inflated significance, -ing riders (highlighting, reflecting, ensuring), "serves as" for "is", bold as decoration, headings that are not in sentence case, and sentences that describe the page instead of the subject.

## House rules on top of the skill

- Signed Egalitaristen. Front matter `author: Egalitaristen`. The voice is the site's own: plain and confident.
- No hedging. State what the sources show, then what the site argues from it. No "perhaps", "arguably", "may", "might", "seems to", "tends to", "it could be said", "some would say". Where a source itself gives a range or an estimate, give it with its year, in the source's own terms. No hedging boxes and no "the strongest objection that remains": answer a common objection with evidence.
- Source ids on every number. Each figure carries `[n]` pointing to an entry in `sources`, with its year in the text. Use only sources that were opened. Name people and parties and link them to their register entry. Attribute by name, never "experts say".
- Report losses plainly. A vote that went against us is stated once, with its result.
- About 1,500 words of body. Facts, timeline and sources come on top.
- Anchors are stable URLs. Sections are `##` with a fixed anchor, such as `## Cantons undercut each other {#competition}`. Never change an anchor once a link to it exists.
- Live register block. Put `{{supporters}}` on its own line in the section on who backs the tax, below an editorial paragraph. Do not repeat its lists by hand.
- Prose only in the pull-quote attribution. The line starting with a dash after a quote is markup, not prose.
