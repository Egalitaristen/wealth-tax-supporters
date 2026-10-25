# CN: seats

The register's own notes are in `data/cn/area_profile.md`. This guide only covers the seat chart for now.
- **Seats:** `python skill/scripts/seats.py data/cn` draws the National People's Congress as one block of 2,977 deputies (the 14th NPC, qualifications confirmed by the Standing Committee on 24 February 2023). No official count of deputies by party (CPC, other parties, non-party) was found in the reports, so the chart does not split them; add one to `china()` if a sourced count is published. No deputy is named, so no seat is lit until a supporter who sits is added to `positions.csv`.
