# Slovenia: research guide

First pass 4 November 2026. Terms: davek na bogastvo, davek na premoženje (often real estate), premoženjski davek, obdavčitev najbogatejših. Sources that worked: rtvslo.si, n1info.si, siol.net, zsss.si PDFs, greenpeace.org/slovenia. dz-rs.si is a JavaScript portal (no seat adapter yet).

## Geography and map
212 občine (LAU codes, e.g. `001`) under the 12 NUTS 3 statistical regions (`SI031`…). Built from Eurostat GISCO `LAU_RG_01M_2024_4326.geojson` and `NUTS_RG_01M_2024_4326_LEVL_3.geojson` (filtered to SI). Parent region by point-in-polygon of a representative point of each municipality. `topo_to_boundaries.py --project lonlat --scale 200 --simplify 0.1 --name-prop LAU_NAME --code-prop GISCO_ID --strip-prefix SI_` (regions: `--name-prop NAME_LATN --code-prop NUTS_ID`), then `merge_boundaries.py`. Licence: CC-BY-4.0 with credit to EuroGeographics, as for Czechia.

## Seats

The Državni zbor (90 seats) is charted by `seats.py` (`si`) from the Assembly's open data file `https://fotogalerija.dz-rs.si/datoteke/opendata/SIF.XML` (listed on dz-rs.si/wps/portal/Home/ostalo/OpenData): the persons who are deputies today and their deputy group (Svoboda 29, SDS 28, NSi-SLS-Fokus 9, SD 6, Demokrati 6, Levica 5, Resni.ca 5, minorities 2 on 15 November 2026). Only names, group and voting district are read; the file has no start dates. Substitutes of ministers count as deputies there.
