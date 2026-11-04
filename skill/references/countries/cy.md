# Cyprus: research guide

Cyprus has no wealth tax; the only live push is AKEL's, and its bills target high-value property and companies, which the definition excludes. The first pass (R001) recorded AKEL, PEO and one AKEL MP. See `data/cy/area_profile.md`.

## Geography and map
Six districts, ISO 3166-2:CY (`CY-01` Nicosia to `CY-06` Kyrenia), as the local tier. The map is geoBoundaries gbOpen CYP ADM1 (OpenStreetMap, ODbL 1.0). Municipalities (30) and communities (about 350) are not loaded: the Eurostat GISCO LAU file (`LAU_RG_01M_2024_4326.geojson`, about 150 MB for all of Europe) has official LAU codes, but each community needs a district parent first.

## Search terms
Greek: φόρος πλούτου, φορολόγηση του πλούτου, φόρος στους υπερπλούσιους. "Φόρος ακίνητης περιουσίας" (property tax) and "έκτακτη αμυντική εισφορά" do not count.

## Sources
- Works: akel.org.cy, peo.org.cy, dialogos.com.cy (AKEL's outlet; reports speeches in indirect speech), cyprus-mail.com, fastforward.com.cy.
- Blocks scripts: parliament.cy (403), nomoplatform.cy (403).

## Seats
No adapter and no readable member list, so no Seats tab. Damianou's position has `current` blank. A `cyprus` adapter in `seats.py` would need the parliament.cy list read in a browser and passed with `--local`.

## What counted and what did not
- Counted: AKEL memorandum (B), PEO statement (B), Damianou (B).
- Left out: AKEL's December 2025 property and company bills; Stefanou, Christofides and Loukaides on their own words.

## A later run should
Read the AKEL bill texts and vote at parliament.cy; AKEL 2026 manifesto; Greens and EDEK programmes; Economics Research Centre report; SEK; polls.
