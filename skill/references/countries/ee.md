# Estonia: no net-wealth tax, thin register

A first-pass guide (seed, 2026-11-04). Estonia has a land tax and no net-wealth tax; SDE talks about asset taxes and a company asset tax. The register holds two domestic statements and one MEP vote.

## Geography

5 NUTS 3 regions over 79 omavalitsused (vald and linn), from Eurostat GISCO LAU 2024 and NUTS 2024 (CC BY 4.0), built as for Lithuania. The 15 maakonnad (ISO 3166-2 EE-xx) are not loaded because GISCO does not say which county a municipality is in; Statistics Estonia's list would add them.

## Seats

Riigikogu (101 seats) from `https://api.riigikogu.ee/api/plenary-members?lang=et` (open, no key): each member's active `FRAKTSIOON` gives the party split (typed into `seats.csv` by hand, since `seats.py` has no Estonian adapter) and `uuid` is the `member_ref`. An adapter would be a small addition to `skill/scripts/seats.py`.

## Sources that worked and blocked

- europarl.europa.eu roll-call PDFs refuse scripts; the Wayback copy (`web.archive.org/web/<ts>id_/<url>`) works.
- ERR (err.ee, news.err.ee) pages read with plain curl; the date is in `article:published_time`.
- Search engines return mostly property-tax and income-tax material; check every hit against the definition.

## Exclusions to remember

See `data/ee/exclusions.csv` and `data/ee/leads.csv`: progressive income tax, inheritance tax, property tax and (Estonia) company asset tax are out of definition.
