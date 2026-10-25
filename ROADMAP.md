# Roadmap

What is planned, and what waits for a date. The live board is the GitHub project **[Wealth Tax Supporters roadmap](https://github.com/users/Egalitaristen/projects/3)** (status, area, what each item waits for, country). Every item is a public GitHub issue labelled [`roadmap`](https://github.com/Egalitaristen/wealth-tax-supporters/issues?q=is%3Aissue+label%3Aroadmap): comment there, or pick one up (see [CONTRIBUTING.md](CONTRIBUTING.md)).

## Where things stand

The **Seats tab** (a hemicycle per chamber, a dot per seat, lit where a supporter we have found sits today) is live for 20 countries: Belgium, Brazil, Canada, China, France, Germany, India, Indonesia, Japan, Malaysia, the Netherlands, New Zealand, Nigeria, Norway, Poland, Singapore, Spain, Sweden, the United Kingdom and the United States. It reads each parliament's own member list, so a supporter who leaves a chamber loses the seat on the next refresh. How to refresh and what each source is: `skill/SKILL.md` 6.7a and the country guides in `skill/references/countries/`.

An unlit seat means nothing found yet, never opposition.

## Scheduled: waits for a date

These need the autumn 2026 elections to happen and the new parliaments to sit. Milestone: [Autumn 2026 elections](https://github.com/Egalitaristen/wealth-tax-supporters/milestone/1).

| What | When it can be done | Issue |
|---|---|---|
| Refresh the US Congress | After the 3 November 2026 midterms, when the new Congress is sworn in (January 2027) | [#61](https://github.com/Egalitaristen/wealth-tax-supporters/issues/61) |
| Refresh Spain's Congreso | After the 29 November 2026 election: today only 137 of 350 deputies are active because the Cortes were dissolved on 6 October | [#60](https://github.com/Egalitaristen/wealth-tax-supporters/issues/60) |
| Refresh New Zealand's House | After the 7 November 2026 election (official results 27 November): Parliament was dissolved on 1 October | [#78](https://github.com/Egalitaristen/wealth-tax-supporters/issues/78) |
| Check Sweden's Riksdag | November 2026, once the substitutes after the September election settle | [#63](https://github.com/Egalitaristen/wealth-tax-supporters/issues/63) |
| Refresh Brazil's Câmara and Senado | After the new legislature takes office on 1 February 2027 | [#62](https://github.com/Egalitaristen/wealth-tax-supporters/issues/62) |

## Next: regional and local bodies

Supporters in devolved parliaments, state legislatures and councils already have structured positions, but nothing is lit until an official member list is read for each body. Milestone: [Regional and local bodies](https://github.com/Egalitaristen/wealth-tax-supporters/milestone/2).

- [#65](https://github.com/Egalitaristen/wealth-tax-supporters/issues/65) The Senedd and the London Assembly (the Scottish Parliament is done)
- [#66](https://github.com/Egalitaristen/wealth-tax-supporters/issues/66) US state legislatures
- [#67](https://github.com/Egalitaristen/wealth-tax-supporters/issues/67) Councils and city governments
- [#73](https://github.com/Egalitaristen/wealth-tax-supporters/issues/73) The European Parliament (the chart is live with the 14 supporters already on the record; more MEPs to find, and other bodies: the Pan-African Parliament and the UN General Assembly are listed as planned in `data/supranational.json`)

## Data quality

Milestone: [Data quality](https://github.com/Egalitaristen/wealth-tax-supporters/milestone/3).

- [#64](https://github.com/Egalitaristen/wealth-tax-supporters/issues/64) **Verify every lit seat, country by country** (in progress; the refinement queue puts these first)
- [#68](https://github.com/Egalitaristen/wealth-tax-supporters/issues/68) Automate the member lists that only open in a browser (Belgium, India's Rajya Sabha, Malaysia, Indonesia)
- [#69](https://github.com/Egalitaristen/wealth-tax-supporters/issues/69) Nigeria: a current party tally, and the Senate
- [#70](https://github.com/Egalitaristen/wealth-tax-supporters/issues/70) China: a sourced split of the National People's Congress by party
- [#71](https://github.com/Egalitaristen/wealth-tax-supporters/issues/71) Singapore: an official source for each MP's party
- [#72](https://github.com/Egalitaristen/wealth-tax-supporters/issues/72) Japan: English names for the new Diet groups
- [#74](https://github.com/Egalitaristen/wealth-tax-supporters/issues/74) Show how much of each chamber the register has found

## How this list is kept

New ideas and dates go in as issues with the `roadmap` label (and `scheduled` when they wait for a date), and are added to the project with its Area, Waits for and Country fields filled in. When an item is done the issue is closed, its card moves to Done, and this file is updated in the same pull request.
