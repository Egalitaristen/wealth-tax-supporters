# Tunisia: the 2026 wealth tax, sources and geography

Seed pass R001 and second pass R002 (2026-11-11). 16 supporters, 20 evidence rows. Check that URLs still resolve before relying on them.

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | Assemblée des représentants du peuple (`B0001`), Conseil national des régions et des districts (`B0002`), Government (`B0003`) | The ARP legislates; the CNRD gives a consultative opinion on finance bills; the Finance Minister tables the bill. Taxation of wealth is a national power. |
| region | 6 development regions (`TN1` to `TN6`) | OCHA COD-AB admin level 1. |
| county | 24 governorates (`TN11` to `TN83`) | OCHA admin level 2. |
| council | 264 delegations (`TN1151`...) | OCHA admin level 3: the lowest tier with an open map and official codes. The 350 elected municipalities are not loaded. |

**Map:** `data/tunisia/boundaries.json` is built from OCHA / HDX "Tunisia - Subnational Administrative Boundaries" (COD-AB, licence CC BY-IGO 3.0, `https://creativecommons.org/licenses/by/3.0/igo/`), valid 2022-11-15, codes are the OCHA P-codes. Recipe (run from the repository, with the GeoJSON files from the dataset's `tun_admin_boundaries.geojson.zip` in a scratch folder):

```bash
C="--project lonlat --scale 120 --simplify 0.35 --licence CC-BY-IGO-3.0 --licence-url https://creativecommons.org/licenses/by/3.0/igo/ --code-scheme 'OCHA COD-AB P-codes' --source 'OCHA / HDX Tunisia Subnational Administrative Boundaries (COD-AB, CC BY-IGO)'"
python skill/scripts/topo_to_boundaries.py tun_admin3.geojson --name-prop adm3_name --code-prop adm3_pcode $C --out units.json
python skill/scripts/topo_to_boundaries.py tun_admin2.geojson --name-prop adm2_name --code-prop adm2_pcode $C --out gov.json
python skill/scripts/topo_to_boundaries.py tun_admin1.geojson --name-prop adm1_name --code-prop adm1_pcode $C --out reg.json
python skill/scripts/merge_boundaries.py units.json --regions gov.json --upper reg.json --out data/tunisia/boundaries.json
```

`geo_units.csv` is built from the same three GeoJSON files (names `adm*_name`, codes `adm*_pcode`; the parent of each unit is the `adm2_pcode` or `adm1_pcode` on the feature). Names are French/English transliterations as OCHA prints them; Arabic names are in `adm*_name1`.

## Seats

**CNRD (77 seats):** drawn from the chamber's own list, `https://www.cnrd.tn/قائمة-النواب/` (WordPress page; one row per member: name, governorate, region, 77 rows on 2026-11-11). The list shows no party, so seats are grouped by development region (see below). The two members who are supporters (`A0004` Mahdia, `A0005` Le Kef) are placed in their governorate and lit. To refresh: re-read the page, count the rows, update `bodies.csv` `seats` and `as_of`.

(Superseded on 15 November 2026: the ARP is now charted too, see below.)

## Seat refresh (15 November 2026)

**ARP (161 seats):** `https://www.arp.tn/parlementaire/groupes` lists each sitting member with the bloc (Arabic), role in the bloc and constituency, 12 rows per page and 13 pages (the pager is client side, so the list is read in a browser). In the page console click through the pager collecting `table.sortable tbody tr` cells (`[name, bloc, role, constituency, member link]`, 153 rows), save as JSON and run:

```bash
python skill/scripts/seats.py data/tunisia --local "https://www.arp.tn/parlementaire/groupes=arp.json"
```

153 members are named (blocs: 29 non-affiliated incl. one with no bloc shown, Al-Amana wal-Amal 25, Voice of the Republic 25, Free 23, Pour que le peuple triomphe 18, Independent National 18, National Sovereign Line 15); the other 8 seats show as Vacant. The Assembly publishes blocs, not parties. Names are Arabic only: write them in brackets after the Latin name (`Ali Zaghdoud (علي زغدود)`).

**CNRD (77 seats):** `https://www.cnrd.tn/قائمة-النواب/` answers a script (a TablePress table: name, governorate, development region); the refresh reads it directly and groups seats by development region because the list gives no party. Run `python skill/scripts/seats.py data/tunisia --fix-status` with the ARP file as above (the default adapter does both chambers).
