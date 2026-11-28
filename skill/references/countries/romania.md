# Romania research guide

INS publishes SIRUTA, the official territorial register. Use the S1 2026 edition at https://data.gov.ro/dataset/721c9059-5f87-4c79-9854-a1d5c18f58d5/resource/dac903f0-32b5-489a-89e7-2c80d96cf68d/download/siruta_s1_2026.csv ; normalized county and UAT files and edition metadata are at https://github.com/romania/siruta (data CC BY 4.0, attributed to INS). Load county SIRUTA entries beneath Romania, UATs beneath their county, and Bucharest sectors beneath Bucharest. Retain SIRUTA codes; exclude component villages, which are not separate general-purpose councils. Current register loaded 42 county-level and 3,187 UAT/sector rows. No local sweeps done.

L299/2025: official Senate register https://www.senat.ro/Legis/Lista.aspx?cod=26923 ; verify text because the threshold combines income and asset values. Parliamentary membership and affiliation can change; refresh from the chambers before asserting current seats. Romanian terms include impozit pe avere, impozit pe averea netă, impozitarea marilor averi, and taxă de solidaritate. Luxury property, income, inheritance and anti-evasion measures alone do not qualify.

No matching polygon map has been prepared. Geo-spatial.org publishes administrative boundary polygons and lines at https://geo-spatial.org/descarcare/date/administrative-boundaries/ ; examine licence and whether a compatible polygon product can be derived before use.
 A mirror reports CC BY-SA 4.0; verify the original licence and compatibility with the repository data licence before importing.

## Seats

Both chambers are charted by `seats.py` (`ro`) from cdep.ro's alphabetical lists of the 2024 legislature (the Chamber of Deputies' site carries both): `structura2015.de?idl=1` for the 330 deputies and `...?idl=1&cam=1&leg=2024` for the 136 senators. Each page lists the sitting members (group, constituency, date joined, none for those who were there from the start) and, below, the members whose mandate ended before the term did, with the date; those give the end dates of former members. 15 November 2026: 330 deputies (PSD 92, AUR 62, PNL 55, USR 40, UDMR 21, minorities 17, UPR 15, SOS RO 13, unaffiliated 15) and 134 senators (2 seats Vacant). senat.ro publishes its list only as a postback grid.
