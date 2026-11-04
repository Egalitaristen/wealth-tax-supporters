# Slovakia: no wealth-tax bill, a thin economists' case

No net wealth tax and, as far as the first pass found, no bill, party programme or poll for one. Consolidation taxes of 2023-25 (income tax band, bank levy, transaction tax) are not wealth taxes. The register holds an economist's commentary and three MEPs' votes.

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | Národná rada, Government | |
| region | 8 kraje | NUTS 3 code (SK010 ...) in `code` |
| council | 2,927 obce | Statistical Office municipal code (6 digits) in `code`, incl. the military district Záhorie; 2,926 have a map shape |

**Map:** `data/sk/boundaries.json` from Eurostat GISCO LAU 2024 and NUTS 2024 (CC BY 4.0). Same recipe as `hu.md` with the SK sheet of `EU-27-LAU-2024-NUTS-2024.xlsx` (codes need zero-padding to 6 digits).

## Sources

- Works: pravda.sk, sita.sk, teraz.sk, noviny.sk, howtheyvote.eu.
- Blocked (not bypassed): nrsr.sk ("Bot Detection"), eur-lex, europarl.europa.eu.
- The EP roll call prints Hajšel as "Hajsel" (no caron): quote the list's spelling.
- `match_wikidata.py` has no Slovakia entry; QIDs were looked up by hand.

## Seats

No adapter and nrsr.sk blocks scripts, so no Seats tab.

## What counts

- Counts: Schmögnerová's commentary (B), EP FOR votes.
- Left out: Ľuboš Blaha's 2014 remark about taxing the rich and banks; Smer's 2023 bank and income tax talk.
