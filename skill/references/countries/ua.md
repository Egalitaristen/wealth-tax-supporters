# Ukraine


## Map

The local tier is the 1,769 hromadas of the KATOTTG codifier, with the 139 districts and 27 regions above them. Shapes: OCHA Common Operational Datasets for Ukraine, HDX `cod-ab-ukr` (CC BY-IGO 3.0), which draw Ukraine as it was before 2014, with the Autonomous Republic of Crimea (297 hromadas) and Sevastopol; its `adm3_pcode` values equal the register's `code`. Recipe (shapefile bundle `ukr_admin_boundaries.shp.zip`; export each layer to GeoJSON with pyshp's `__geo_interface__`, which is already in WGS84):

```
L="--licence CC-BY-IGO-3.0 --licence-url https://creativecommons.org/licenses/by/3.0/igo/legalcode --project lonlat --scale 80"
python skill/scripts/topo_to_boundaries.py ukr_admin3.geojson --code-prop adm3_pcode --name-prop adm3_name --simplify 0.8 $L --code-scheme "KATOTTG hromada codes as used by OCHA COD-AB P-codes" --source "..." --out units.json
python skill/scripts/topo_to_boundaries.py ukr_admin2.geojson --code-prop adm2_pcode --name-prop adm2_name --simplify 1 $L --code-scheme "OCHA COD-AB P-codes" --out dist.json
python skill/scripts/topo_to_boundaries.py ukr_admin1.geojson --code-prop adm1_pcode --name-prop adm1_name --simplify 1.2 $L --code-scheme "OCHA COD-AB P-codes" --out obl.json
python skill/scripts/merge_boundaries.py units.json --regions dist.json --upper obl.json --out data/ua/boundaries.json
```
