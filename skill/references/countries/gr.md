# Greece geography and map

The 2026 ELSTAT administrative register supplies the 13 regions, 74 regional units and 332 municipalities in `data/gr/geo_units.csv`. Its codes overlap across administrative tiers, so the register prefixes them R, U and M. Mount Athos is autonomous and is excluded from the municipality layer.

The municipality polygons come from Ioannis Andreadis, Aristotle University of Thessaloniki, [Cleisthenes administrative boundaries](https://doi.org/10.26255/heal.5fh6-7qxu), licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), based on geodata.gov.gr data licensed CC BY 3.0. The source incorporates the 2019 municipal splits.

To reproduce `data/gr/boundaries.json`, download and extract the Cleisthenes shapefile and run `python scripts/build_gr_boundaries.py <path-to-cleisthenes.shp>`. This requires pyshp and shapely. The script normalizes Greek names to join the shapefile with the ELSTAT register, applies 11 reviewed mappings where names differ or are ambiguous, and asserts that every municipality matches exactly once. It dissolves municipality polygons to regional units and regions, then runs the repository boundary conversion and merge tools. Attribution and licensing are embedded in the output. Check a new register against the shapefile before regenerating; the shape dataset is not a substitute for subsequent administrative changes.
