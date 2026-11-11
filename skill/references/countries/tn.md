# Tunisia: the 2026 wealth tax, sources and geography

Seed pass R001 and second pass R002 (2026-11-11). 16 supporters, 20 evidence rows. Check that URLs still resolve before relying on them.

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | Assemblée des représentants du peuple (`B0001`), Conseil national des régions et des districts (`B0002`), Government (`B0003`) | The ARP legislates; the CNRD gives a consultative opinion on finance bills; the Finance Minister tables the bill. Taxation of wealth is a national power. |
| region | 6 development regions (`TN1` to `TN6`) | OCHA COD-AB admin level 1. |
| county | 24 governorates (`TN11` to `TN83`) | OCHA admin level 2. |
| council | 264 delegations (`TN1151`...) | OCHA admin level 3: the lowest tier with an open map and official codes. The 350 elected municipalities are not loaded. |

**Map:** `data/tn/boundaries.json` is built from OCHA / HDX "Tunisia - Subnational Administrative Boundaries" (COD-AB, licence CC BY-IGO 3.0, `https://creativecommons.org/licenses/by/3.0/igo/`), valid 2022-11-15, codes are the OCHA P-codes. Recipe (run from the repository, with the GeoJSON files from the dataset's `tun_admin_boundaries.geojson.zip` in a scratch folder):

```bash
C="--project lonlat --scale 120 --simplify 0.35 --licence CC-BY-IGO-3.0 --licence-url https://creativecommons.org/licenses/by/3.0/igo/ --code-scheme 'OCHA COD-AB P-codes' --source 'OCHA / HDX Tunisia Subnational Administrative Boundaries (COD-AB, CC BY-IGO)'"
python skill/scripts/topo_to_boundaries.py tun_admin3.geojson --name-prop adm3_name --code-prop adm3_pcode $C --out units.json
python skill/scripts/topo_to_boundaries.py tun_admin2.geojson --name-prop adm2_name --code-prop adm2_pcode $C --out gov.json
python skill/scripts/topo_to_boundaries.py tun_admin1.geojson --name-prop adm1_name --code-prop adm1_pcode $C --out reg.json
python skill/scripts/merge_boundaries.py units.json --regions gov.json --upper reg.json --out data/tn/boundaries.json
```

`geo_units.csv` is built from the same three GeoJSON files (names `adm*_name`, codes `adm*_pcode`; the parent of each unit is the `adm2_pcode` or `adm1_pcode` on the feature). Names are French/English transliterations as OCHA prints them; Arabic names are in `adm*_name1`.

## Seats

**CNRD (77 seats):** drawn from the chamber's own list, `https://www.cnrd.tn/قائمة-النواب/` (WordPress page; one row per member: name, governorate, region, 77 rows on 2026-11-11). The list shows no party, so `seats.csv` has one group. The two members who are supporters (`A0004` Mahdia, `A0005` Le Kef) are placed in their governorate and lit. To refresh: re-read the page, count the rows, update `bodies.csv` `seats` and `as_of`.

**ARP:** not charted. `https://arp.tn/deputies` lists the members by name only (Arabic; about 156 names in the "المباشرون" tab), with no bloc, constituency or party, and `https://arp.tn/blocs` returned 404. Two supporters (`A0006`, `A0007`) were found on that list on 2026-11-11 and carry `current=y`. A Seats tab needs a source with the blocs; Wikidata may have the constituency (P768).

## The wealth tax debate

- **Real estate tax 2023:** 0.5% on real estate worth 3 million dinars or more (decree-law 2022-79 article 23). A tax on one asset class: not counted (`X0011`).
- **2026 tax (article 50 of the bill, article 88 of the law):** annual, 1 January, individuals including minor children; 0.5% on 3 to 5 million dinars of net wealth, 1% above; immovable and movable property in Tunisia (residents: worldwide); main residence and its furniture, professional assets, goodwill in use, cars up to 12 CV and (per the adopted text) bank and financial deposits exempt; return by 30 June. The brief said 5 million dinars; the sources say 3 and 5.
- **Votes:** ARP finance committee rejected the article (10 against, 3 for); plenary rejected it on 1 December 2025; on 4 December 2025 the article, re-tabled by the minister, passed 72 for, 14 against, 16 abstentions; the whole law 89-23-12.
- **Earlier calls (R002):** Elyès Jouini (2014, 2020), an L'Économiste Maghrébin editorial (2020), a Nawaat opinion piece (2020), the 2022 Al Bawsala report. No party, union or deputy proposal for a general wealth tax was found for 2011 to 2021; the 2022 to 2023 debate was about real estate.
- **Designs:** the article is `annual_net_wealth` (net value, after debts tied to the assets); the 2022 Al Bawsala proposal is `wealth_tax_unspecified`.

## Sources that worked and those that did not

- Business News, La Presse, Kapitalis, L'Économiste Maghrébin, Webdo and Mosaïque FM answer plain clients and carry named statements. Business News and Webdo give the clearest deputy and committee-officer names.
- arp.tn committee minutes (`arp.tn/ar_SY/document/download/<id>`) download with a browser User-Agent. They are **Arabic PDFs whose text is garbled by `pdftotext` for some files** but read fine with `pypdf`; `wtdb.py checkquotes` matched the Arabic quote in `E00001`. Read the PDF with `pypdf` to find passages.
- Al Bawsala's report PDFs (`albawsala.com/files/...`) carry presentation-form Arabic glyphs; use the French version, whose text extracts.
- The law is on the bill page `https://arp.tn/loi/project/4238` (stage, schedule, documents, Official Gazette reference); the Official Gazette PDF (`arp.tn/document/download/115725`) is a scan with a text layer that `pypdf` reads; Arabic words there can come out in presentation forms or reversed, so match by normalised text.
- `checkquotes` does not read the garbled committee PDFs reliably (E00021 reported "not found" although the passage is in the PDF): check such rows by hand with `pypdf`.
- allAfrica and Al-Araby returned 403 to scripts; the same stories are usually on La Presse or Business News.
- Spellings vary: Michket / Mechkat / Mechket Salama / Slama Khaldi; Chkoundali / Chkandali; Bouzaïene / Bouzeyene / Bouzian. Search several.

## Quirks

- The Conseil national des régions et des districts (CNRD) is a second chamber whose opinion on finance bills is consultative; its finance committee sits jointly with the ARP's. Do not read its vote as law.
- The press often calls the 2023 tax "impôt sur la fortune immobilière" and the 2026 tax "impôt sur la fortune": check which one a source means.
- Opponents named in the brief or the press (Maher Ktari, Ridha Chkoundali, UTICA) are in `exclusions.csv`; Tarek Mahdi was not found.
