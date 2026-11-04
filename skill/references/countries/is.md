# Iceland research guide

## Geography and map
8 regions (landsvæði, ISO 3166-2:IS-1 to IS-8) and 61 municipalities (sveitarfélög). Names and codes come from Statistics Iceland's PxWeb tables (`px.hagstofa.is/pxis/api/v1/is/Ibuar/mannfjoldi/2_byggdir/sveitarfelog/`: MAN02005 for the division of 1 January 2026, MAN10001 for the latest quarter, where Borgarbyggð and Skorradalshreppur are one municipality, code 3609). The region is the first digit of the municipality number (0 and 1 are the capital region). Shapes: National Land Survey of Iceland (LMÍ) IS 50V, layer `IS_50V:mork_sveitarf_flakar` from `https://gis.lmi.is/geoserver/IS_50V/wfs` (GetFeature, outputFormat application/json, srsName EPSG:4326), CC BY 4.0. The layer still labels the merged municipality `Borgarbyggð` with the old code 3506; it is remapped to 3609. Shapes were merged by code and simplified with shapely `coverage_simplify` (0.004 degrees); region outlines are the union of the simplified municipalities; then `topo_to_boundaries.py --project lonlat --scale 1500` and `merge_boundaries.py --code-prefix IS-`.

## Sources
- althingi.is (bills, speeches, votes) returns 403 to scripts; use Wayback copies or a browser. The minister's answer 154/2266 was read through Wayback.
- Heimildin pages carry soft hyphens, so `checkquotes` cannot match them.
- Search terms: auðlegðarskattur (the 2010-2014 tax), eignarskattur (the older one), stóreignaskattur.
- Supporters on the record: Sósíalistaflokkurinn, Vinstri græn, ASÍ. No Alþingi member of a supporting party sits today.
