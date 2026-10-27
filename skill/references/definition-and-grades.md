# What counts, the grades and who counts

This file holds sections 2, 3, 4 of the skill. `skill/SKILL.md` keeps the section numbers as pointers to this file, so a reference such as "SKILL.md 6.7a" still finds it. Section numbers in the text below refer to the same numbering.

## 2. What counts as wealth taxation

A tax on the **stock of wealth** (net assets) of the wealthy, rather than on income, transactions or a single type of property.

**Included** — the `wt_design` values:

| wt_design | Meaning | Examples |
|---|---|---|
| `annual_net_wealth` | Recurring annual tax on net wealth above a threshold | 2% on assets over £10m; Spain's patrimonio; Norway's formuesskatt |
| `one_off_levy` | One-time levy on net wealth | California's one-time 5% billionaire tax ballot measure; post-crisis wealth levies |
| `billionaire_minimum` | Minimum tax set as a % of wealth for the ultra-rich | Zucman's 2% minimum tax on billionaires; the G20 2024 billionaire-tax discussion; France's "taxe Zucman" |
| `unrealised_gains` | Annual taxation of unrealised gains for the very wealthy (mark-to-market) | US billionaire minimum income tax on unrealised gains |
| `exit_tax` | Tax on wealth or unrealised gains when the wealthy emigrate | Exit-tax proposals tied to a wealth tax |
| `partial_wealth` | Recurring tax on net holdings of a broad asset class (e.g. financial assets), not a single property | — |
| `defend_existing` | Opposing abolition, or supporting keeping or raising an existing wealth tax | Defending a national wealth tax against repeal |
| `wealth_tax_unspecified` | Calls for "a wealth tax" without saying which design | "We need a wealth tax" |

**Excluded** (never qualifies on its own): mansion or high-value property taxes; council tax or property tax reform; land value tax; capital gains tax changes on realisation; inheritance, estate or gift taxes; income or dividend tax rises; windfall taxes; corporate taxes; financial transaction taxes; closing loopholes or tax-avoidance measures; generic "tax the rich" or "fair share" with no reference to the stock of wealth.

**Ambiguous phrases.** "Tax wealth like work" or "tax wealth not work" often means aligning capital gains with income tax (common UK usage). Treat it as grade C at most, and only when nothing in the speaker's own platform shows they mean capital gains. If it clearly means capital gains or dividends, it does not qualify. Watch local terms that also cover excluded taxes (e.g. Italian *patrimoniale* can mean property taxes; Dutch *vermogensbelasting* often refers to the savings box) and read the context.

**Not enough on their own:** "tax the wealthy", "tax billionaires more", "make the rich pay their fair share", and support for bills that change income or capital-gains tax (a millionaires' surtax, a minimum income tax on realised income). Count them only when the person's own words or the named bill refer to wealth, net worth or unrealised gains, as in the table above. Record the near-misses in `exclusions.csv` (`out_of_definition` or `insufficient_evidence`) so nobody re-checks them.

**Wealth caps.** A cap on individual wealth (the limitarian position, for example The Wealth Cap Project) counts as a 100% levy above a threshold. Record it under the closest design (usually `wealth_tax_unspecified`) and say "wealth cap" in `design_detail`.

Someone who supports both an included design and an excluded one qualifies on the included evidence; record only that evidence.

## 3. Evidence grades

| Grade | Label | Rule |
|---|---|---|
| **A** | Explicit | Endorses an included design **with specifics** (rate, threshold, named bill or proposal), **or** a formal act: voted for, sponsored or co-sponsored, signed a motion or letter that calls for an included design, organisational policy adoption, authored a publication recommending one, gave supportive testimony. |
| **B** | Named | Supports "a wealth tax", "wealth levy", "billionaire tax" or an equivalent local term by name, without specifics. |
| **C** | Implied | Language that probably means wealth taxation but is ambiguous ("make the super-rich pay on their wealth"). Included and flagged as *appears to support*; a target for upgrade. C still needs words about wealth: "those with most should contribute more" is not C, it is an exclusion (section 2). Neither is a name on an event programme or a speaking slot without the words spoken. |

**Roster and endorsement lists.** When a campaign's own page lists someone as an endorser, that is a claim by the campaign, not a statement by the endorser. Grade it **B** and say so in `grading_note`; upgrade to A when you find the endorser's own statement, vote or signature. Sponsors and cosponsors in official bill data are a formal act (A).

An actor's grade is the best grade among its support evidence. Grade each piece of evidence on its own, and write one line in `grading_note` explaining why.

## 4. Who counts — actor types and inclusion rules

`kind` is `person`, `organisation` or `institution` (a public body: a council, parliament, government or commission).

| actor_type | kind | Include when… |
|---|---|---|
| `politician` | person | Elected official or candidate at any level (supranational to local), or a minister, with qualifying evidence: vote, sponsorship, signed motion, speech or statement. Record level and geography. |
| `party` | organisation | Party, party branch, council group or youth wing; evidence from a manifesto, policy document or conference motion. |
| `government_body` | institution | A council, parliament, government or commission that **passed** a motion or adopted a position, or a commission that recommended it. A failed motion goes on the proposer, not the body. |
| `academic` | person | Scholar outside economics (law, politics, public health, sociology and so on) who wrote in favour (paper, book, report, op-ed, testimony). Merely researching wealth taxes does not count. |
| `economist` | person | Any economist, whether at a university, central bank, international organisation, bank, think tank or consultancy, arguing in favour. Use this for economists in academia too, so that one filter finds them all. |
| `think_tank` | organisation | Published a recommendation, or campaigns for it. |
| `ngo_campaign` | organisation | NGO, charity, campaign group or coalition campaigning for or endorsing it. |
| `union` | organisation | Union, union confederation or trades council with a policy, motion or campaign. |
| `union_official` | person | Union leader or official speaking for it. |
| `journalist` | person | Writes **opinion** pieces (columns, op-eds, essays, podcasts, video commentary) arguing for it. Reporters writing straight news do not count. |
| `media_outlet` | organisation | An editorial (the outlet's own stated view) argues for it. |
| `legal_tax_professional` | person / organisation | Tax lawyer, accountant, valuer, former tax-authority official or professional body that publishes in favour or gives supportive evidence. |
| `wealthy_individual` | person | A wealthy person who has **publicly** declared support (signed letter, member of a public group such as Patriotic Millionaires, statement). |
| `business_leader` | person / organisation | A business figure or business association publicly in favour. |
| `faith` | person / organisation | Faith leader or faith organisation. |
| `cultural_figure` | person | Artist, writer, athlete or celebrity with a public statement. |
| `campaigner` | person | Individual activist or NGO leader with a public profile (spokesperson, founder, author, charity chief executive). |
| `international_body` | institution / organisation | International or supranational body, or intergovernmental group (UN, IMF, OECD, G20 track, EU institutions, EU Tax Observatory). |
| `funder` | organisation | Foundation that **funds wealth-tax advocacy or research specifically**; evidence is a grant record or a programme page. |

**Each person needs their own evidence.** A party's manifesto, a coalition's statement or a roster page is evidence about the party, coalition or list, not about every candidate, member or signatory who appears on it. Record the party (or coalition) once, and add an individual only with something of their own: their vote on the wealth tax itself, a bill or motion they sponsored or signed, their own speech, article or statement, or a signed letter that names the tax. These do **not** make a person a supporter: standing for a party; holding a seat for it; being listed on its roster or ticket; being quoted next to the party's position; being a co-author of a study that measures a tax without recommending it; being named in a bibliography; being on a board, in a coalition's member list or working group; a vote on a whole budget or report that includes the tax among much else; a vote on an inheritance, property or financial-transaction tax; a request to study an exit tax, unless the same text calls for a wealth tax. Where a member's vote is the evidence, quote the member's own entry in the official per-member list (name, as printed there), never the shared result line or a block of neighbouring names, and never personal data such as a birth date.

International actors (Zucman, Oxfam International) are included in a country database only when they acted **in or towards that area** (testimony to its parliament, a campaign there). Give them their Wikidata ID so databases can be merged later.
