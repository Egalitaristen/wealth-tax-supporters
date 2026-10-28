# Spain refinement plan

Prepared 28 October 2026 from `refine/SKILL.md`, `skill/references/countries/es.md` and the current `data/es` files. A plan only: no data has been changed and no live source was opened. Counts come from the CSV files and `refine_queue.py`; a queue flag is a prompt to inspect, not proof of an error.

## Baseline

| Measure | Count |
|---|---:|
| Supporters | 136 (88 people, 41 organisations, 7 institutions) |
| Evidence rows | 185 (all `support`, none archived) |
| Best evidence A / B / C | 92 / 41 / 3 |
| Supporters refined | 0 |
| Supporters without a link or website | 22 |
| Persons without a Wikidata ID | 88 of 88 per `wikidata_qid` (the queue flags only 8, so the column may be partly empty: check after `match_wikidata.py`) |
| Positions current / not current | 12 / 51 |
| Latest evidence before 2020 | 1 (Juan Francisco Martín Seco, A0086) |
| Open Spain leads | 3 (L0005 Montero, L0006 Cuerpo, L0007 Albares) |

Queue gaps (124 actors, counts overlap): one statement 101, weak grade 44, coarse place 28, no links 22, office 13, verify seat 12, Wikidata 8, still current 1.

Levels: 117 national, 15 regional, 3 supranational, 1 local. Spain has the Seats tab (Congreso and Senado adapters), so the seat check applies.

## Spain-specific points to handle first

- **Dissolved Cortes.** The Cortes were dissolved on 6 October 2026 (election 29 November). Deputies' mandates ended at dissolution, so `seats.py` shows only about 137 active. A "verify seat" flag now may reflect the dissolution, not an error. Do not mark `current=n` for the whole chamber; record the end of mandate only as the official Congreso data shows it, and plan a seat refresh once the new Cortes meet (`election-refresh.md`, issue #60).
- **Senado** comes from a Wikipedia list because senado.es blocks scripts; read the name-only matches `seats.py` prints (Spanish double surnames, strict matching).
- **Congreso server** returns 403 after about 10,000 requests: fetch single pages, not scans.
- **Names:** register names are in full (for example "Pedro Puy Fraga"), while sources use short or hyphenated forms: search both.
- **Place:** deputies sit at province level (INE two-digit code, `county`); autonomous-community bodies at region level (`ES-xx`); municipalities by five-digit INE code.

## 1. Prepare

- Work on a branch, one pull request, never push to main. This worktree's branch is `claude/spain-refinement-plan-a0f4bb`.
- Read `skill/SKILL.md` sections 1 to 5 and `references/countries/es.md` again before starting.
- Leads: work the three open ones. They are ministers named in international statements (a joint billionaire-levy article, the 2025 Seville initiative, the FfD4 conference). Open each source, apply the definition (a minimum tax on large fortunes and a global billionaire levy are plausible, but check each quote), add the ones that hold up and close each with `leads.py close`. Montero (A0063) and Cuerpo (A0085) are already actors, so these become extra statements for them, not new rows; Albares may be new.
- Automatic pass, whole country:

```bash
python skill/scripts/match_wikidata.py data/es
python skill/scripts/profiles_wikidata.py data/es
python skill/scripts/wtdb.py locate data/es
python skill/scripts/archive_sources.py data/es
python skill/scripts/seats.py data/es
```

- Spot-check several Wikidata matches (description must fit the person; watch common Spanish names). Read the seat mismatches `seats.py` prints against the dissolution note above.
- Regenerate the batch afterwards: `python skill/scripts/refine_queue.py data/es --n 60 --out %TEMP%/es-batch.csv` (outside the repo). The current top 60 is a preview, not a fixed list.

## 2. Batch 1: lit seats (about 60)

The 12 flagged seat-holders come first: Pedro Puy Fraga (A0112, also grade C), Carlos Martín Urriza (A0110), Néstor Rego Candamil (A0008), Enrique Santiago Romero (A0009), Oskar Matute (A0011), Mertxe Aizpurua (A0016), Gabriel Rufián (A0028), Aina Vidal (A0044), Gerardo Pisarello (A0047), Txema Guijarro (A0055), Ione Belarra (A0020), Juan Lobato (A0092).

Most have one statement, probably the 7 June 2022 or 24 November 2022 roll call. For each, in the skill's order:

1. **Links:** Congreso page, party page, public accounts linked from those pages or Wikidata.
2. **Place:** province of election; for Lobato and Puy the place is flagged too.
3. **Statements (max 3):** an own bill, motion, speech or article (BOCG series B, Diario de Sesiones, their party's press pages) to add a second statement of a different kind or year; upgrade C or B to A where possible (Puy, Martín Urriza).
4. **Current stance:** Lobato (PSOE, Madrid) and Puy need a check on whether their position still holds as a wealth tax stance.
5. **Offices:** confirm on congreso.es, taking the dissolution into account, and correct `role`, `status`, positions and `refined`.

Then fill the rest of the 60 from the ranked queue: the economists and the first batch of those with no links (below).

## 3. Batch 2: links, places, grades for the unlinked

- **22 supporters with no link.** Mostly economists (Marina Alcázar, Francisco García-Rodríguez, Luis Molina Temboury, Jorge Fabra Utray, Olga Cantó, Jesús Ruiz-Huerta, Juan Antonio Gimeno Ullastres), the union official Carlos Cruzado, Íñigo Macías, and organisations such as ActionAid España, the Plataforma por la Justicia Fiscal (national and Madrid), the Catalan campaign, Sumar and Más Madrid. Use university and organisation pages and Wikidata.
- **Organisations:** place at the head office or the branch that made the statement (Madrid, Barcelona).
- **Grade B to A** for the organisations and economists: their own reports, manifestos and signed letters rather than press mentions.
- **Juan Francisco Martín Seco (A0086):** the only latest-statement-before-2020 case; search for a recent position, and add a `retracted` row only if a reversal is documented.
- **Former or non-seat politicians with office flags:** Felipe González (A0065), Zapatero (A0066) are grade C: look for a statement of their own, since both are well known and the evidence may be weak. Also Pedro Sánchez (A0062), Montero, Bustinduy (A0064), Cuerpo, Mónica García (A0091), Arcadi España (A0129), Abel Caballero (A0080), Iker Casanova (A0126), Eva López de Arroyabe (A0128): verify the offices against the government, regional or municipal pages.

## 4. Later batches

1. **Single-statement actors (101).** Add a second, differently dated statement for the prominent ones first. Spanish sources that usually yield: BOCG bills, Diario de Sesiones, Senado motions, regional parliaments (Parlament de Catalunya, Juntas Generales, Parlamento de Navarra), party and union press rooms.
2. **Remaining coarse places (28)** and Wikidata IDs for persons.
3. **Positions:** 51 positions are `current=n`; check that the ends are dated and sourced and that no `current=y` is unchecked.
4. **Regional bodies** (15 regional actors): verify each against the regional parliament or government after the autonomous elections.
5. **Seat sweep (section 6 of the refine skill)**, after a refinement pass and once the new Cortes have met. Start with roll calls: the 7 June 2022 and 24 November 2022 Congreso votes and the Senate vote are already harvested, so match them to the current member list first; then sweep names in Sumar, ERC, EH Bildu, BNG, Podemos and the PSOE left, which have logged supporters. Search in Spanish, Catalan, Basque and Galician.
6. **Resources pass:** Spain's polls in `meta.json` and the bills in `data/resources.json`, including the status of any bill in the Congreso database.
7. **New supporters met on the way** go into `harvest.csv` or `leads.csv`, not into this run.

## 5. End of every run

- `wtdb.py validate data/es` and fix all errors.
- `wtdb.py checkquotes data/es --run <run-id>` for the new rows.
- `archive_sources.py data/es --save` in the background; log failures.
- Add a `runs.csv` row with focus `refine: <n> supporters`, zero new actors (except promoted leads) and concrete `notes_next`.
- Compare before and after: links added and supporters still linkless, places made finer, statements added, grades raised, retractions, offices corrected, those not improved and why.
- Open one pull request.

## Order of work

1. Leads and automatic pass (one session).
2. Batch 1 (lit seats), then validation and a pull request.
3. Batch 2 (links and grades), then a pull request.
4. After the 29 November election and the first sitting of the new Cortes: `seats.py` refresh, then the seat sweep.
