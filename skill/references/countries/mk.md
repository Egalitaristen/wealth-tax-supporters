# North Macedonia research guide

Geography: OCHA/HDX COD-AB North Macedonia 2025 (https://data.humdata.org/dataset/cod-ab-mkd, CC BY-IGO): 8 planning regions, 80 opštini. Four Skopje municipalities share ADM2 P-code MK00809, so the register uses the dataset's PCODEX (MK0080901 ...) as unit code. Map: `--name-prop ADM2_EN --code-prop PCODEX --scale 140 --simplify 0.4 --project lonlat`.

Terms: данок на богатство (wealth), данок на луксуз (богатство) (SDSM/Levica wording; ambiguous with luxury-goods tax), данок на имот (property: excluded), солидарен данок (windfall: excluded). Sources: northmacedonia.rferl.org (works), okno.mk, civilmedia.mk, lokalno.mk; levica.mk answers 403 to scripts (not bypassed). Found: Levica (A, 2020 programme read at https://levica.mk/wp-content/uploads/2020/06/Levica-programa-A4-final-za-net-12.06.2020-1.pdf, which downloads fine with pypdf though pdftotext garbles it; 2024 numbers via RFE/RL), Apasiev (C, 2016), SDSM (C). sobranie.mk member pages are Angular; Wayback was rate-limited.

## Seats

The Sobranie (120 seats) is charted by `seats.py` (`mk`) from the Assembly's own list of members, https://www.sobranie.mk/mps-en.nspx (120 on 15 November 2026; VMRO-DPMNE 57, SDSM 13, DUI 10, BESA 10, Levica 6, others). The list is an Angular page that loads its rows with a "Show more" button, so it is read once in a browser and passed with `--local`:

1. Open the page, wait for it to load, and click the `[ng-click="loadMore()"]` button until 120 member links (`a[href*="mps-details"]`) are on the page.
2. For each link take the first text line (name), the second (party; empty or "Независни пратеници" means independent) and the `param=` GUID from the href.
3. Save rows `[name, party, GUID]` as JSON and run: `python skill/scripts/seats.py data/mk --fix-status --local "https://www.sobranie.mk/mps-en.nspx=<saved file>"`.

The list gives parties, not parliamentary groups, so the seat chart is by party. Names are Latin on the English page; the register keeps the Cyrillic name with the Latin one in brackets.
