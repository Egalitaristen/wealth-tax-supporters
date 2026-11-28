# Slovakia: no wealth-tax bill, a thin economists' case

No net wealth tax and, as far as the searches found, no national bill or qualifying poll. Consolidation taxes of 2023-25 (income tax band, bank levy, transaction tax) are not wealth taxes. The register includes an economist's commentary, three MEPs' votes, a union report suggesting consideration of a net-wealth tax, and two ambiguous positions on wealth taxation.

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | Národná rada, Government | |
| region | 8 kraje | NUTS 3 code (SK010 ...) in `code` |
| council | 2,927 obce | Statistical Office municipal code (6 digits) in `code`, incl. the military district Záhorie; 2,926 have a map shape |

**Map:** `data/slovakia/boundaries.json` from Eurostat GISCO LAU 2024 and NUTS 2024 (CC BY 4.0). Same recipe as `hu.md` with the SK sheet of `EU-27-LAU-2024-NUTS-2024.xlsx` (codes need zero-padding to 6 digits).

## Sources

- Works: pravda.sk, sita.sk, teraz.sk, noviny.sk, howtheyvote.eu.
- FEPS documents a 2024 Slovak campaign for the EU Tax the Rich initiative with Proforum and Friedrich-Ebert-Stiftung, including events in Bratislava, Košice and Banská Bystrica. Teologické fórum also asked readers to sign; date its undated appeal to 2024 using the forum's dated 10 September 2024 article. Event appearances alone do not establish speakers' positions.
- The 17 June 2025 European civil-society letter on EU own resources is hosted by the European Environmental Bureau; it names Climate Coalition Slovakia and coordinator Dana Mareková and explicitly supports a progressive wealth tax. Zuzana Fialová discusses the same proposal in her own July 2025 Pravda interview; distinguish this sociologist from the actress of the same name.
- Blocked (not bypassed): nrsr.sk ("Bot Detection"), eur-lex, europarl.europa.eu.
- The EP roll call prints Hajšel as "Hajsel" (no caron): quote the list's spelling.
- HowTheyVote's 2 April 2025 amendment 82 page exposes the complete Slovak roll call through its country filter and Show all button even when its downloadable API and the Parliament site are blocked. Five Slovak MEPs voted for the rejected 3% minimum wealth-tax proposal; see H0002. The displayed names were checked manually.
- `match_wikidata.py` has no Slovakia entry; QIDs were looked up by hand.

## Seats

The Národná rada (150 seats) is charted by `seats.py` (`sk`) from the National Council's own alphabetical list of deputies and the club pages, https://www.nrsr.sk/web/Default.aspx?sid=poslanci/zoznam_abc (Smer 41, PS 33, Hlas 24, KDH 12, Slovensko 12, SaS 11, non-attached 9, SNS 8 on 15 November 2026). nrsr.sk answers scripts with a bot check (not bypassed), so the lists are read once in a browser and passed with `--local`:

1. Open the alphabetical list in Chrome: every deputy is a link with `PoslanecID=` ("Surname, Given").
2. Fetch the seven club pages (`...sid=poslanci/kluby/klub&ID=55` and the others on `...kluby/zoznam`) and `...kluby/nezavisli`, and give each deputy the club whose page links them.
3. Save rows `[name, id, club label]` as JSON and run: `python skill/scripts/seats.py data/slovakia --fix-status --local "https://www.nrsr.sk/web/Default.aspx?sid=poslanci/zoznam_abc=<saved file>"`.

No politician in the Slovak register sits in the Council today (they are MEPs).

## What counts

- Counts: Schmögnerová's commentary (B), EP FOR votes, the KOZ report's tentative net-wealth proposal (B), the EU initiative's Slovak campaign partners (A), and explicitly flagged ambiguous Dobrá voľba and Tomáš Profant positions (C).
- Left out: Ľuboš Blaha's 2014 remark about taxing the rich and banks; Smer's 2023 bank and income tax talk.
