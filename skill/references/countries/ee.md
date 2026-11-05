# Estonia: no net-wealth tax, thin register

Updated after runs R001–R004 (2026-11-05). Estonia has a land tax and no net-wealth tax. The register holds 11 supporters (7 grade A, 3 grade B, 1 grade C): three MEPs on European Parliament roll-call votes (Toom, Kaljurand, Mikser), two political party platforms (Eesti Vasakliit, Erakond Eestimaa Rohelised), a prominent business leader/banker (Indrek Neivelt), academics and economists (Peet Kask, Rainer Kattel, Toomas Peterson, Kerly Randlane), and one implied statement (Lauri Läänemets).

## Geography

5 NUTS 3 regions over 79 omavalitsused (vald and linn), from Eurostat GISCO LAU 2024 and NUTS 2024 (CC BY 4.0), built as for Lithuania. The 15 maakonnad (ISO 3166-2 EE-xx) are not loaded because GISCO does not say which county a municipality is in; Statistics Estonia's list would add them.

## Seats

Riigikogu (101 seats) from `https://api.riigikogu.ee/api/plenary-members?lang=et` (open, no key): each member's active `FRAKTSIOON` gives the party split (typed into `seats.csv` by hand, since `seats.py` has no Estonian adapter) and `uuid` is the `member_ref`. An adapter would be a small addition to `skill/scripts/seats.py`.

## Sources that worked and blocked

- europarl.europa.eu roll-call PDFs refuse scripts; the Wayback copy (`web.archive.org/web/<ts>id_/<url>`) works.
- ERR (err.ee, news.err.ee) pages read with plain curl; the date is in `article:published_time`.
- Postimees (majandus.postimees.ee), Müürileht (muurileht.ee), and party platforms (vasakliit.ee, rohelised.ee) read with plain python / curl.
- Search engines return mostly property-tax and income-tax material; check every hit against the definition.

## Exclusions to remember

See `data/ee/exclusions.csv` and `data/ee/leads.csv`: progressive income tax, inheritance tax, property/land tax, real-estate taxes (kinnisvaramaks), and company asset tax (ettevõtete varamaks) are out of definition. Also excluded: analytical scenario modeling without policy advocacy (Arenguseire Keskus / Piirits; Eesti Pank / Meriküll & Rõõm), youth wing proposals limited to progressive income tax (Monticelli / Noorsotsid), and cultural reviews of Piketty without personal policy endorsement (Liivik, Kõusaar).
