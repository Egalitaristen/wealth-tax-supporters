# Export, and things that went wrong before

This file holds sections 7, 8 of the skill. `skill/SKILL.md` keeps the section numbers as pointers to this file, so a reference such as "SKILL.md 6.7a" still finds it. Section numbers in the text below refer to the same numbering.

## 7. Export

The xlsx export contains: **Overview** (counts, grade mix, coverage and sweep progress, definitions); **Supporters** (one row per actor: grade, *explicit / named / appears to support*, designs, evidence count, first and latest evidence date, strongest source); **Evidence**; **Local coverage** (each geography unit with sweep status and supporter count); **Links**; **Profiles** (websites and socials); **Harvest lists**; **Run log**; **Former supporters** (latest stance retracted, shown only when there are some). There is no points score. Users filter by grade, type, level, prominence and date.

## 8. Things that went wrong before (avoid them)

The list of past mistakes is now the checklist in [`pre-pr-checklist.md`](pre-pr-checklist.md): each item there comes from a row, a map or a run that a review had to fix, and the checks name the tool that finds it. Run it before every pull request.

Why it exists: the first reviews of eleven country pull requests removed rows in ten of them, and cut some sharply (Norway 299 to 145, Singapore 81 to 20, Japan 594 to 31), mostly for the same few patterns: a party platform copied onto every candidate, votes on a whole budget counted as wealth-tax votes, bibliography entries graded as support, coalition member lists, exit-tax-only and property-tax rows, a roster's update date used as the statement date, polls that were not about a wealth tax, and scratch scripts committed.
