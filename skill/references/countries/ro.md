# Romania research guide

INS publishes SIRUTA, the official territorial register. Use the S1 2026 edition at https://data.gov.ro/dataset/721c9059-5f87-4c79-9854-a1d5c18f58d5/resource/dac903f0-32b5-489a-89e7-2c80d96cf68d/download/siruta_s1_2026.csv ; normalized county and UAT files and edition metadata are at https://github.com/romania/siruta (data CC BY 4.0, attributed to INS). Load county SIRUTA entries beneath Romania, UATs beneath their county, and Bucharest sectors beneath Bucharest. Retain SIRUTA codes; exclude component villages, which are not separate general-purpose councils. Current register loaded 42 county-level and 3,187 UAT/sector rows. No local sweeps done.

L299/2025: official Senate register https://www.senat.ro/Legis/Lista.aspx?cod=26923 ; verify text because the threshold combines income and asset values. Parliamentary membership and affiliation can change; refresh from the chambers before asserting current seats. Romanian terms include impozit pe avere, impozit pe averea netă, impozitarea marilor averi, and taxă de solidaritate. Luxury property, income, inheritance and anti-evasion measures alone do not qualify.

No matching polygon map has been prepared. Geo-spatial.org publishes administrative boundary polygons and lines at https://geo-spatial.org/descarcare/date/administrative-boundaries/ ; examine licence and whether a compatible polygon product can be derived before use.
 A mirror reports CC BY-SA 4.0; verify the original licence and compatibility with the repository data licence before importing.
