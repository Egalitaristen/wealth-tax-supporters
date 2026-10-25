# Norway: seats

The register's own notes are in `data/no/area_profile.md`. This guide only covers the seat chart for now.

- **Seats:** `python skill/scripts/seats.py data/no` reads the Storting's open data (`data.stortinget.no`, 169 seats, the representatives of the current period; a serving deputy holds the seat of a member on leave). Former members come from the three earlier periods, without end dates. Parties are named as the Storting names them (Arbeiderpartiet, Fremskrittspartiet, Høyre, Sosialistisk Venstreparti, Senterpartiet, Rødt, Miljøpartiet De Grønne, Kristelig Folkeparti, Venstre). Run it again after every election and whenever a member leaves.
