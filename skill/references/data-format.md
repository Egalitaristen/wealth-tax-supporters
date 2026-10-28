# Data files

This file holds section 5 of the skill. `skill/SKILL.md` keeps the section numbers as pointers to this file, so a reference such as "SKILL.md 6.7a" still finds it. Section numbers in the text below refer to the same numbering.

## 5. Data files

In this repository, `<area-slug>` is the lowercase ISO 3166-1 alpha-2 code (`gb`, `de`) or `<iso2>-<region>` (`us-ca`). Where the code is already taken by a body above the countries (`au` is the African Union), use the country's lowercase name (`australia`) and say so in `meta.json` `notes`; set `iso2` to the real code. Each folder also needs a `meta.json` (`name`, `iso2`, `lead`, `status`, `boundaries`, `notes`; `init` creates it). Put the scope you chose (levels covered, anything left out) in `notes` and in section 1 of `area_profile.md`. Everything lives in `data/<area-slug>/` (e.g. `data/gb/`, `data/us-california/`). A body above the countries, such as the European Parliament, is not a register of its own: `data/eu/` holds only its chamber, seats and positions (`meta.json` has `"supranational": true`), and a supporter who sits there is recorded in their own country's register (6.7a). `wtdb.py validate data/eu` checks it that way. The column lists, ID formats, required fields and allowed values between the `<!-- schema:... -->` markers are generated from `skill/scripts/wtdb.py` (`python skill/scripts/wtdb.py schema --write`); never edit them by hand, change `wtdb.py` and regenerate. The text around them says what each column means. Create it with `python skill/scripts/wtdb.py init data/<slug> --area "<Area name>"`, or by hand with exactly these headers. IDs are prefix + zero-padded number (A0001, E00001, G0001, L0001, H0001, X0001, R001).

**actors.csv** — one row per actor
<!-- schema:actors -->
`actor_id, name, kind, actor_type, other_types, role, affiliation, party, affiliation_actor_id, country, level, location, geo_unit_id, location_source, wikidata_qid, website, status, alive_checked, prominence, notes, added_run, updated, refined`
- IDs look like `A0001`. Required: `name`, `kind`, `actor_type`, `country`, `level`, `status`, `alive_checked`.
- `kind` is one of: institution · organisation · person.
- `actor_type` is one of: academic · business_leader · campaigner · cultural_figure · economist · faith · funder · government_body · international_body · journalist · legal_tax_professional · media_outlet · ngo_campaign · party · politician · think_tank · union · union_official · wealthy_individual.
- `level` is one of: local · national · regional · supranational.
- `status` is one of: active · dissolved · former_role.
- `alive_checked` is one of: na · y.
- `prominence` is one of: international · local · national · regional (or blank).
<!-- /schema:actors -->
- `other_types`: extra `actor_type` values separated by `;`, for people who fit more than one (for example `journalist` primary with `economist` here). `actor_type` is the main role; the site and the coverage grid count a person under every type they hold.
- `party`: for politicians, the party's common name in English (for example `Labour`, `Green Party`, `Democratic Party`; `Independent` if none). Use one name per party so the site can filter on it; a regional or state branch uses the national party's name (the Minnesota DFL is `Democratic Party`). Blank for non-politicians, and for local officials in non-partisan offices when the party is not known. `validate` warns about a missing party above local level.
- `level`: supranational · national · regional · local (the level of government or society they act at)
- `location`: where they are based or whom they represent, written as a path from the country down, separated by ` > `: `United States > California > Camarillo`, `United Kingdom > London > Hackney`, `United Kingdom > Yorkshire and The Humber > Leeds East`. The first part is the country root unit in `geo_units.csv`. Each next part that matches a register unit under the previous one is resolved to that unit; anything after that is plain place text (a city, district or constituency the register does not list yet). Give the finest place you can prove. If you only know the state, stop at the state; if you only know the country (a national union, a nationwide campaign), write just the country. Never guess a finer place. A national-level actor sits at the country; a legislator sits at the place they represent (the district, constituency, state or region), not at the institution (that goes in `role`). The site counts an actor for every unit on the path, so a city actor counts for their state and the country.
- `geo_unit_id`: the register unit the actor is placed in, the deepest unit `location` resolves to. It is the stable key (names change: Araba became Álava, and Connecticut's counties became planning regions). `wtdb.py add` fills it from `location`; `wtdb.py locate` fills any that are empty and, after a unit is renamed or moved, rewrites the unit part of `location` from the register and keeps the place text after it. `validate` fails when the two disagree.
- `location_source`: the page that shows the place, when it is not obvious from the evidence (a news profile saying where they are from, their organisation's address, a university page). A legislator's seat needs none. Never a home address.
- `refined`: the date of the last refinement pass on this actor (the `refine` skill), so the next pass can skip them.
- `status`: active · former_role · dissolved
- `alive_checked`: y · na (organisations and institutions). `y` means you looked for a death record and found none.
- `notes`: only what a reader needs: an identity caveat (a common name, a role taken from a list), where the party or role came from, or context the evidence rows do not show. **Never** write that the person is alive, that Wikidata has no match, or that no death record was found; `alive_checked` already says it, and the site shows the notes to readers. Leave `notes` empty when there is nothing to add.
- `prominence`: international · national · regional · local (how widely they are known on this issue)

**evidence.csv** — one row per piece of evidence (an actor can have many)
<!-- schema:evidence -->
`evidence_id, actor_id, date, stance, grade, evidence_type, wt_design, design_detail, quote_original, quote_lang, quote_en, source_url, source_title, publisher, archive_url, accessed, harvest_id, grading_note, run_id`
- IDs look like `E00001`. Required: `actor_id`, `date`, `stance`, `grade`, `evidence_type`, `wt_design`, `quote_original`, `quote_lang`, `source_url`, `grading_note`.
- `stance` is one of: retracted · support.
- `grade` is one of: A · B · C.
- `evidence_type` is one of: bill_sponsorship · campaign · coalition_membership · editorial · funding · interview · manifesto · motion · motion_signature · op_ed · open_letter · other · policy_adoption · publication · report · social_post · speech · statement · testimony · vote.
- `wt_design` is one of: annual_net_wealth · billionaire_minimum · defend_existing · exit_tax · one_off_levy · partial_wealth · unrealised_gains · wealth_tax_unspecified.
<!-- /schema:evidence -->
- `date`: YYYY-MM-DD (or YYYY-MM / YYYY if that is all that is known); the date of the act or statement, not of a later article about it
- `stance`: support · retracted
- `grade`: A · B · C
- `evidence_type`: vote · bill_sponsorship · motion · motion_signature · open_letter · publication · report · op_ed · editorial · speech · statement · interview · social_post · manifesto · policy_adoption · campaign · coalition_membership · testimony · funding · other
- `wt_design`: values in section 2
- `design_detail`: rate, threshold, bill name or number (e.g. "2% over £10m")
- `quote_original`: verbatim from the source page; `quote_lang`: ISO code; `quote_en`: translation if not English
- `archive_url`: a Wayback Machine copy of the source (`skill/scripts/archive_sources.py` fills it), so the quote stays checkable when the page moves or goes behind a paywall

**geo_units.csv** — the tree of places you report on, and the checklist for regional and local sweeps (6.5, 6.7)
<!-- schema:geo_units -->
`geo_unit_id, name, level, unit_type, parent_id, website, sweep_status, swept_run, swept_date, queries_run, hits, notes, code`
- IDs look like `G0001`. Required: `name`, `level`, `sweep_status`.
- `level` is one of: combined_authority · council · county · devolved · national · region · sub_council · supranational.
- `sweep_status` is one of: done · in_progress · pending · skipped.
<!-- /schema:geo_units -->
- The register is a **tree**. The top row is the **country root** (`unit_type=country`, `level=national`, no parent), named as the first part of every `location`. Regions, states and nations are its children (`parent_id`), and councils, counties or cities sit below those. Institutions such as the legislature or the executive are also children of the root, but actors are not placed on them (see `location`).
- Unit names must be unique among siblings. Write the plain name (`California`), not `California (state legislature)`; put descriptions in `unit_type` and `notes`. Where a city and a district share a name, use the usual local form to tell them apart (`München` and `Landkreis München`).
- `code`: the official code of the unit (ONS GSS code, US county FIPS, German AGS, Swedish kommunkod). Give every local unit one: map shapes are matched by code, because names repeat (thirty US counties are called Washington County).
- `level`: supranational · national · devolved · region · county · combined_authority · council · sub_council. In a federal country, states are `region`. Load the register down to the local tier (6.7) even where you do not sweep it; a unit with children is a parent, and `status` counts the lowest units.
- `sweep_status`: pending · in_progress · done · skipped

**bodies.csv, seats.csv, positions.csv** — the offices politicians hold, and the seat charts (optional; see 6.7a)
`bodies`:
<!-- schema:bodies -->
`body_id, name, level, kind, seats, as_of, source_url, seat_view, notes`
- IDs look like `B0001`. Required: `name`, `level`, `kind`.
- `level` is one of: local · national · regional · supranational.
- `kind` is one of: chamber · council · other.
- `seat_view` is one of: y (or blank).
<!-- /schema:bodies -->
`seats`:
<!-- schema:seats -->
`seat_id, body_id, party, seats, colour, order`
- IDs look like `S0001`. Required: `body_id`, `party`, `seats`.
<!-- /schema:seats -->
`positions`:
<!-- schema:positions -->
`position_id, actor_id, body_id, role, party, geo_unit_id, start, end, current, member_ref, checked, source_url`
- IDs look like `O00001`. Required: `actor_id`, `body_id`.
- `current` is one of: n · y (or blank).
<!-- /schema:positions -->
- `bodies`: one row per chamber, council or similar (`kind`: chamber · council · other; `level` as for actors). `seat_view=y` gives the body a chart on the country's **Seats** tab and needs `seats`, `as_of` and `source_url`: take the total and the split from the body's own official list, never from memory.
- `seats`: how a `seat_view` body's seats split between parties (the same party names as `actors.party` and `positions.party`; a `Vacant` row for empty seats). `order` runs left to right across the chamber; `colour` is the party's hex colour without `#`. The rows add up to the body's `seats`.
- `positions`: one row per office a politician holds or held, with `start` and `end` dates (YYYY-MM-DD, YYYY-MM or YYYY). `current` is `y` (found on the body's own list on the `checked` date; no `end`), `n` (no longer holds it; `end` says when) or blank (not checked against an official list). `member_ref` is the body's own ID for the member. Only `current=y` lights a seat.

**Polls** (optional, `meta.json` `polls`): published opinion polls on a wealth tax in the country, so a visitor can see that the register is the visible tip of wider support. One object per poll: `support` (percent), optional `support_text` ("About 8 in 10") and `oppose` (kept in the data, not shown on the site), `scope` (who was asked), `question` (the design asked about, in English), optional `question_original`, `pollster`, `commissioned_by`, `fieldwork`, `sample`, `published` (YYYY-MM-DD or YYYY-MM) and an https `url`. Use the pollster's own release or tables where they exist. Include polls that show low support as well as high, and put the most recent poll on a tax on the very rich first: the site shows the first one in the country header.

**Papers, reports and bills** (optional, `data/resources.json`, one list for every country): research and legislation about an actual wealth tax, shown with the polls on the site's Resources page (`/resources`, filterable by kind, place and year). One object each: `country` (a register folder such as `fr`, or `global`), `kind` (`paper` for academic work, `report` for think-tank, commission or official reports and proposals, `bill` for bills, motions and laws), `title`, `by` (authors, sponsors or body), `published` (YYYY-MM-DD, or YYYY-MM), an https `url` to the original, a one-sentence `summary`, and for bills a `status` and `level`. Read the document itself before listing it (it must be about a wealth tax, not income or inheritance tax alone), and state a bill's status only as far as you have seen it. The build stops on a missing field or an unknown country. Polls stay in `meta.json` and appear on the page automatically.

**boundaries.json** (in the country folder, named in `meta.json`) draws the local map on the site: `{"viewBox": [x, y, w, h], "source", "licence", "licence_url", "code_scheme", "units": [{"name", "code", "path"}], "regions": [{"name", "code", "path"}]}`.

**Map licence rule (hard):** the shapes must come from a source that states an open licence (public domain, CC0, CC BY, ODbL, or an open government licence such as OGL or dl-de/by), and the unit codes must be the official ones. In order of preference, look for:
1. the national statistics office or mapping agency, which also publishes the codes;
2. a well-known open republication of those official shapes (us-atlas for the US Census; DataMeet for the Survey of India);
3. OCHA's Common Operational Datasets on HDX (`data.humdata.org/dataset/cod-ab-<iso3>`): the national agency's boundaries, usually under CC BY-IGO, with P-codes built from the official codes (Brazil's `BR1100015` is IBGE `1100015`; `topo_to_boundaries.py --strip-prefix BR`). The HDX API (`/api/3/action/package_show?id=cod-ab-<iso3>`) states the licence.
4. geoBoundaries gbOpen, after checking the licence of that country's entry (`geoboundaries.org/api/current/gbOpen/<ISO3>/ADM2/` gives `boundaryLicense`).

When the national agency states no licence on its own site, look at 3 and 4 before giving up: they often republish the same official shapes under an open licence.

A personal GitHub repository or blog with no licence file, a "free to use" note, a non-commercial licence (GADM is CC BY-NC, so not usable), or any shapes whose origin you cannot name are **not** used, however convenient. Never invent codes, not even "state code plus a running number". If no open source with official codes turns up, ship the country without a map: the site works without one. Say so in `meta.json` notes, with the sources you checked, and open a follow-up issue for the map. Write `licence`, `licence_url` (https) and `code_scheme` into the file. `topo_to_boundaries.py` requires them, `wtdb.py validate` fails without them and warns about licences it does not know, and the PR description must name the licence. (India's first map broke this rule and had to be replaced.) `units` are the local tier (6.7) and are matched to `geo_units.csv` by `code` when the register has codes, otherwise by name. `regions` are the outlines of the level above (English regions and UK nations, län, Länder, states, départements, provinces), drawn as lines over the map; every country has them. Where there are two levels above the units, put the higher one in `regions_upper` (régions over départements, communities over provinces), drawn bolder; `scripts/merge_boundaries.py` combines the files. Take units and regions from the same agency and coordinate system so the lines fall on the unit borders (deriving region borders from simplified units does not work: neighbours rarely share vertices). Make both with `scripts/topo_to_boundaries.py` from a TopoJSON, GeoJSON or shapefile (`--simplify` keeps the file small, `--where` drops water areas, `--encoding` reads Latin-1 shapefiles). `source` names where the shapes come from and their licence; the site prints it on the country's Method page as the credit most licences require. `wtdb.py validate` warns about shapes that match no unit.

**links.csv** — relationships, used for snowballing
<!-- schema:links -->
`link_id, from_actor_id, to_actor_id, link_type, evidence_id, source_url, note`
- IDs look like `L0001`. Required: `from_actor_id`, `to_actor_id`, `link_type`.
- `link_type` is one of: co_author · co_signatory · coalition_partner · founded · funds · leads · member_of · party_of · works_for.
<!-- /schema:links -->
- `link_type`: member_of · works_for · leads · co_author · co_signatory · funds · founded · coalition_partner · party_of

**profiles.csv** — official or professional links for an actor, one row per link
<!-- schema:profiles -->
`profile_id, actor_id, platform, url, source, checked`
- IDs look like `P00001`. Required: `actor_id`, `platform`, `url`.
- `platform` is one of: bluesky · facebook · instagram · linkedin · mastodon · official_page · substack · tiktok · website · wikipedia · x · youtube.
<!-- /schema:profiles -->
- `platform`: website · official_page · x · bluesky · mastodon · instagram · facebook · youtube · tiktok · linkedin · substack · wikipedia
- Only pages the person or their organisation publishes (their own site, party or parliament page, professional social accounts), or that Wikidata or a parliament lists for them. No personal accounts, email addresses or phone numbers, and nothing guessed from a name search. `url` must be https. `source` says where the link came from and `checked` is the date you read that source. Skip private individuals and people who are only known as wealthy signers.

**harvest.csv** — bulk lists to process (see 6.4)
<!-- schema:harvest -->
`harvest_id, title, list_type, url, date, est_size, status, actors_added, notes`
- IDs look like `H0001`. Required: `title`, `list_type`, `status`.
- `list_type` is one of: coalition_members · commission_evidence · conference_motion · cosponsors · motion_signatories · open_letter · other · report_authors · roll_call.
- `status` is one of: done · failed · in_progress · queued.
<!-- /schema:harvest -->
- `list_type`: roll_call · cosponsors · motion_signatories · open_letter · coalition_members · report_authors · commission_evidence · conference_motion · other
- `status`: queued · in_progress · done · failed

**leads.csv** — things to chase in this area (see 6.2a and 6.3a)
<!-- schema:leads -->
`lead_id, kind, name, source_url, why, found_run, status, closed_run, note`
- IDs look like `D0001`. Required: `kind`, `name`, `source_url`, `status`.
- `kind` is one of: document · event · list · organisation · person.
- `status` is one of: duplicate · open · rejected · used.
<!-- /schema:leads -->
- IDs are `D0001`. `kind`: person · organisation · document · event · list. `status`: open · used · rejected · duplicate. `source_url` is the link where you saw it; `why` is one line on why it matters; `found_run` and `closed_run` are run IDs; `note` says what was tried when a lead is left open. Leads about other areas go in `data/leads.csv` (6.12).

**queries.csv** — the searches worth knowing, mainly the broad ones of 6.2a
<!-- schema:queries -->
`query_id, run_id, date, language, query, channel, results_opened, leads_added, note`
- IDs look like `Q0001`. Required: `query`.
<!-- /schema:queries -->
- IDs are `Q0001`. `language` is an ISO code; `channel` is free text (web, news, archive, a site or database).

**exclusions.csv** — candidates checked and rejected, so they are not checked again
<!-- schema:exclusions -->
`exclusion_id, name, reason, detail, source_url, run_id`
- IDs look like `X0001`. Required: `name`, `reason`.
- `reason` is one of: deceased · duplicate · insufficient_evidence · opposes · out_of_definition · pre_2010_only · private_individual.
<!-- /schema:exclusions -->
- `reason`: out_of_definition · pre_2010_only · deceased · private_individual · opposes · insufficient_evidence · duplicate

**runs.csv** — one row per run
<!-- schema:runs -->
`run_id, date, assistant, focus, targets, queries_run, sources_opened, candidates_seen, new_actors, new_evidence, grade_upgrades, saturation, notes_next`
- IDs look like `R001`. Required: `date`, `focus`.
<!-- /schema:runs -->

**area_profile.md** — the area profile (section 6.2).

Helper commands (when Python is available):
```
python skill/scripts/wtdb.py add data/gb actors '{"name":"…","kind":"person",…}'   # assigns ID; prints it
python skill/scripts/wtdb.py add data/gb evidence @new_evidence.jsonl               # one JSON object per line
python skill/scripts/wtdb.py set data/gb geo_units G0042 sweep_status=done hits=2 queries_run=6
python skill/scripts/wtdb.py add data/gb leads '{"kind":"list","name":"...","source_url":"https://...","why":"...","found_run":"R001","status":"open"}'   # a lead in this area (6.3a)
python skill/scripts/wtdb.py set data/gb leads D0001 status=used closed_run=R001        # close it
python skill/scripts/wtdb.py validate data/gb     # errors must be fixed before a run ends
python skill/scripts/wtdb.py locate data/gb       # fill geo_unit_id; repair locations after a unit is renamed
python skill/scripts/match_wikidata.py data/gb  # fill wikidata_qid where the match is unambiguous; spot-check it
python skill/scripts/wtdb.py dedupe data/gb       # likely duplicate actors
python skill/scripts/wtdb.py merge data/gb A0012 A0345   # merge a duplicate (second) into the first: moves evidence, links, profiles
python skill/scripts/wtdb.py checkquotes data/gb --run R004   # fetch sources and check the quotes are on the pages
python skill/scripts/profiles_wikidata.py data/gb  # websites, socials and Wikipedia from Wikidata IDs
python skill/scripts/topo_to_boundaries.py counties-albers-10m.json --object counties --code-prop id --scale 4 --simplify 0.8 --out data/us/boundaries.json
python skill/scripts/seats_uk.py data/gb          # UK only: Commons and Lords seats and sitting members from the Parliament API
python skill/scripts/seats.py data/gb --adapter scottish_parliament   # the Scottish Parliament (129 MSPs) from data.parliament.scot; --adapter picks a chamber set other than the country's own
python skill/scripts/seats_us.py data/us          # US only: Senate and House seats and sitting members (congress-legislators, CC0)
python skill/scripts/seats.py data/se             # any country in the ADAPTERS table at the bottom of seats.py: the chamber's seats and sitting members from the parliament's open data; --fix-status marks those who left as former
python skill/scripts/seats.py data/eu             # the European Parliament (720 MEPs, by political group) from data.europarl.europa.eu; matches supporters in every country register by the MEP's own country. data/eu has only meta.json (supranational: true), bodies, seats and positions (actor ids are <folder>-<id>); a supporter who is an MEP stays an actor in their own country, whose role you keep current by hand
python skill/scripts/wtdb.py status data/gb       # counts, coverage grid, sweep progress, suggested next targets
python skill/scripts/wtdb.py export data/gb       # writes data/gb/<slug>_wealth_tax_supporters.xlsx
```
Writing CSVs directly is fine too, but quote fields properly (quotes often contain commas), and run `validate` afterwards.
