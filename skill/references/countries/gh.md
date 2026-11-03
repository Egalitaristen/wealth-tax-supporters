# Ghana (data/gh)

- **Geography:** 16 regions (`GH01`-`GH16`) and 260 Metropolitan, Municipal and District Assemblies (`GH0101`-`GH1609`) from the OCHA COD-AB Ghana layers (CC BY-IGO). The HDX download links answer scripts with an AWS bot challenge (never bypassed); the same unmodified layers are at `https://data.fieldmaps.io/cod/originals/gha.gpkg.zip` (a GeoPackage; read it with `sqlite3` and a small WKB parser, or GDAL). OCHA names the region "Northern East"; it is registered as "North East". Units match by code.
- **Seats:** no adapter and Ghana is not in `seats.py`. Parliament was not read.
- **Wealth tax status:** none in force. The Growth and Sustainability Levy (a company levy), the 2018 high-net-worth income-tax band, the GRA High Net Worth Office and property rates do not count.
- **What exists:** support comes from an economist (Godfred Bokpin) and Ghana-based NGOs on the 2025 pan-African G20 letter; no legislator, party, union or church was found in the first pass.
- **Sources that work:** gna.org.gh, myjoyonline.com, ghanaiantimes.com.gh, graphic.com.gh, citinewsroom.com. ModernGhana returns an empty page to scripts; the Oxfam policy-practice page returned nothing.
- **Watch out:** "tax the rich" and "high-net-worth" in Ghana usually mean income-tax compliance; some speakers call property tax "a form of wealth tax", which is excluded.
