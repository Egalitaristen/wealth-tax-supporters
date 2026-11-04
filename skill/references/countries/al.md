# Albania research guide

Geography: OCHA/HDX COD-AB Albania 2019 (https://data.humdata.org/dataset/cod-ab-alb, CC BY-IGO): ADM1 = 12 qarks, ADM2 = 61 bashkia, loaded with P-codes (AL01, AL0101). The dataset labels AL1101 "Bashkia Kamez" in English but "Kavajë" in Albanian; the register says Kamëz. Map: `topo_to_boundaries.py <adm2 shp> --project lonlat --name-prop ADM2_EN --code-prop ADM2_PCODE --scale 120 --simplify 0.4`, regions from ADM1, merged with `merge_boundaries.py`.

Terms: "taksa e pasurisë" and "tatimi mbi pasurinë e paluajtshme" are the immovable-property tax: excluded. "Tatim progresiv" is the income-tax scale. Sources that worked: levizjabashke.al, reporter.al, euronews.al. Found: Lëvizja Bashkë (C), economist Majlind Lazimi (A, Balkanweb 2020). Balkanweb and gazetasi.al read fine; parlament.al and the Sobranie sites need a browser. Bashkë programme PDF still to be located.
