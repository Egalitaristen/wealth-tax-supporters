# Refreshing seats after an election

The Seats tab shows a chamber's seats by party, lit where a supporter we have found holds the seat **today**. After an election, a dissolution, a batch of by-elections or a change of government it is out of date until someone reads the new official member list. This is the job.

Each country's refresh is an issue labelled `roadmap`, `seats` and `scheduled` on the project board ([Wealth Tax Supporters roadmap](https://github.com/users/Egalitaristen/projects/3)); the issue says what it waits for. Take one when its date has passed.

## Before you start

1. **Check the new chamber really sits** and the official list is current: a parliament's list can lag the swearing-in, and a dissolved chamber lists only part of its members (Spain's deputies' mandates end at dissolution). If the list is not ready, say so on the issue and stop; do not refresh from a half-updated list.
2. Read the country guide, `skill/references/countries/<iso2>.md`, for the adapter, the source, quirks (a list that only opens in a browser, a name format) and what was done last time.

## Run the refresh

```bash
python skill/scripts/seats.py data/<iso2> --fix-status
```

The adapter rebuilds the chamber's seats and positions from the parliament's own list and prints every supporter whose role, party or status disagrees with it. UK and US: `seats_uk.py data/gb` and `seats_us.py data/us`. Lists that refuse scripts are read once in a browser and passed with `--local` (see the country guide). Never type seat counts or party splits from memory.

Read what it prints before committing. A name-only match, or "not on today's list", can be a spelling difference as well as a real departure: open the person's page on the body's own site.

## Fix what it reports

- **Left the chamber:** `positions.csv` `current=n` with the `end` date; the actor's `role` updated and `status=former_role`. The evidence rows stay.
- **Re-elected or newly seated:** `current=y` with `checked` set to today; `role` and `party` match the list.
- **Changed party:** update `party` on the actor and on the position, and check that the party exists in `seats.csv` (a new party needs a row, a colour and an `order`).
- **Totals:** the `seats` rows add up to the body's `seats`; `as_of` and `source_url` are the new list's. Empty seats are a `Vacant` row.
- **Supporters who no longer hold any office** stay in the register; they simply lose their lit seat.

## Then look for the new intake

A new parliament has new members, and some of them will be supporters nobody has recorded. Run a short research pass on the new intake (manifestos of the parties that gained seats, first speeches, motions and bills tabled in the first weeks, signatories of letters), following the discover and follow-the-leads steps in `skill/SKILL.md` 6.2a and 6.3a. New supporters are added with their own evidence like any other row.

## Finish

1. `wtdb.py validate data/<iso2>` and, for the European Parliament, also `data/eu`.
2. Open a pull request. Report, from the files: seats lit before and after; who left, who joined, who changed party; what the adapter flagged and how you resolved each.
3. Close the issue, and open the issue for the country's next election with its date (the project board's *Waits for* field), so the cycle continues.
