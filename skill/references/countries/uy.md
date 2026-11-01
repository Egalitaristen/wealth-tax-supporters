# Uruguay (data/uy)

- **Geography:** the 19 departamentos (intendencias) are loaded as the local tier, with OCHA P-codes `UY01` to `UY19` from the [HDX COD-AB Uruguay 2020 gazetteer](https://data.humdata.org/dataset/cod-ab-ury) (CC BY-IGO). The 125 municipios are not loaded: that dataset has no municipios, only 204 second-level areas named "n.a2" and so on. Map: `ury_admbnda_adm1_2020.shp` with `topo_to_boundaries.py --project lonlat --scale 100 --simplify 0.2 --name-prop ADM1_ES --code-prop ADM1_PCODE`, and the ADM0 outline merged as `regions` with `merge_boundaries.py`.
- **Seats:** no adapter. The Senate has 30 senators plus the Vice President (`national_seat_roles` is `^Senator`, so senators need no constituency); the 99 deputies are elected by department. Positions are recorded with `current` blank.
- **Sources that work:** montevideo.com.uy, ambito.com, elobservador.com.uy (the quote is in the page text although the article is for subscribers) and the PIT-CNT site. The Wikipedia page of a legislator gives the department of a past term only.
- **Wikidata:** `match_wikidata.py` has an entry for `UY`.
