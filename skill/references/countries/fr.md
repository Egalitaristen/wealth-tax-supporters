# France: seats

The register's own notes are in `data/fr/area_profile.md`. This guide only covers the seat chart for now.

- **Seats:** `python skill/scripts/seats.py data/fr` reads the Assemblée nationale's open data (`data.assemblee-nationale.fr`, the zip of active deputies and their organs: 577 seats, groups by their abbreviation such as RN, LFI-NFP, SOC, EcoS) and the Sénat's (`data.senat.fr/data/senateurs/ODSEN_GENERAL.csv`, senators with état ACTIF: 348 seats, by group). Supporters are matched by name (the open data has no Wikidata IDs); no end dates for former members.
