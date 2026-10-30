# Portugal: research guide

The seed run is in progress. Portuguese search terms include imposto sobre grandes fortunas, imposto sobre a riqueza, and património global; distinguish these from property, income and inheritance taxes.

## Geography and map
The [DGT CAOP 2025 municipality layer](https://www.arcgis.com/home/item.html?id=f02058101f0d4a1987ff15674b90b757), republished by Esri Portugal, states CC BY 4.0 and provides DICO codes. The [district/island layer](https://www.arcgis.com/home/item.html?id=fe2e435c2dd34028a1323c78c7ab18b5) has the same licence. The register contains 308 municipalities grouped under the 29 districts and islands; these groupings are not all elected regional authorities. Azores and Madeira shapes are shifted toward the mainland for display. The 2025 municipality list matches the [government portal’s count](https://portalautarquico.dgal.gov.pt/pt-PT/municipios/).

The ArcGIS FeatureServer endpoints are `https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/CamadaCAOP2025Concelhos/FeatureServer/0/query` and the equivalent `CamadaCAOP2025DistritosIlhas` layer. Query `where=1=1`, `outFields=*`, `f=geojson`, `outSR=4326`, `maxAllowableOffset=0.002`, and `geometryPrecision=4`. Convert with `topo_to_boundaries.py` using municipality properties `Municipio` and `DICO`, region properties `Distrito_Ilha` and `DI`, `--project lonlat --scale 200 --simplify 0.5 --shift '3*:7,5' --shift '4*:17,4'`, CC BY 4.0 and attribution to DGT; combine with `merge_boundaries.py`.

## Research priorities
Trace wealth-tax bills and individual sponsors; follow the open leads; search organisations and economists, then sample regional and local sources. Nothing in the municipality register should be treated as swept.

## Seats
`python skill/scripts/seats_pt.py data/pt` fetches the Parliament’s complete current list of sitting deputies. It validates the list date and count of 230, counts its parliamentary-group labels, and matches supporters by normalized exact name; matched supporters get a checked XVII legislature position and official constituency. It does not infer that unmatched people have permanently left Parliament: they may be temporarily replaced. Refresh after membership changes. `--local <html>` reuses a saved official list for an offline refresh. The page is <https://www.parlamento.pt/DeputadoGP/Paginas/Deputadoslista.aspx>.
