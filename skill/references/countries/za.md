# South Africa: no annual wealth tax; support sits in the EFF, SACP, MK Party, COSATU, SAFTU and the Parliamentary Budget Office

Worked notes from the seed pass (`R001`, 2026-10-26; 22 supporters, 27 evidence rows). The peak of the debate was the February to May 2025 budget fight, when a proposed VAT rise was countered with calls for a wealth tax.

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | National Assembly, National Council of Provinces, National Government | |
| region | 9 provinces | OCHA COD-AB P-codes (`ZA1`..`ZA9`) in `code` |
| county | 44 district municipalities | `ZA244` style codes; drawn as the bolder-line outlines under the provinces |
| council | 205 local municipalities and 8 metropolitan municipalities | The map tier: 213 shapes with 6-character P-codes (`ZA5263`); metros hang directly under their province |

**Map:** `data/za/boundaries.json` is the Municipal Demarcation Board's 2020 boundaries as republished by OCHA (HDX `cod-ab-zaf`, licence CC BY-IGO 3.0). Built from `zaf_admin3/2/1.geojson` in `zaf_admin_boundaries.geojson.zip`:

```bash
L="--licence CC-BY-IGO-3.0 --licence-url https://creativecommons.org/licenses/by/3.0/igo/legalcode --project lonlat --scale 80"
python skill/scripts/topo_to_boundaries.py zaf_admin3.geojson --code-prop adm3_pcode --name-prop adm3_name --simplify 0.8 $L --code-scheme "Municipal Demarcation Board / OCHA COD-AB P-codes" --source "Municipal Demarcation Board of South Africa, via OCHA Common Operational Datasets (HDX cod-ab-zaf), CC BY-IGO" --out units.json
python skill/scripts/topo_to_boundaries.py zaf_admin2.geojson --code-prop adm2_pcode --name-prop adm2_name --simplify 1 $L --code-scheme "OCHA COD-AB P-codes" --out dist.json
python skill/scripts/topo_to_boundaries.py zaf_admin1.geojson --code-prop adm1_pcode --name-prop adm1_name --simplify 1.2 $L --code-scheme "OCHA COD-AB P-codes" --out prov.json
python skill/scripts/merge_boundaries.py units.json --regions dist.json --upper prov.json --out data/za/boundaries.json
```

The 2020 file has 213 local units (205 locals + 8 metros) and 44 districts; the districts file also lists the 8 metros as `adm2`, so the register hangs the metros under their province and draws the metro outlines in the districts layer.

## What worked

- **Parliament's own question pages.** `pmg.org.za/committee-question/<id>/` gives the asker, date and wording of each written question and the Minister's reply: EFF's Omphile Maotwe (NW3273, NW4844). Search PMG for further askers.
- **Parliamentary Budget Office briefs** at `archive.parliament.gov.za/bitstreams/<id>/download` (PDF; `pdftotext` works). The second pre-budget brief of 12 March 2025 prices a 0.5% wealth tax.
- **Independent Media sites** (Daily News, The Post, Business Report, Cape Argus) read fine and carry the party statements of 2025; IOL and BusinessTech often answer 403 to scripts.
- **Trade union statements** are on `saftu.org.za/archives/<id>` and are dated by the budget they answer.

## Watch

- "Wealth tax" in the South African press often means estate duty, transfer duty or capital gains tax. Read the sentence: the Treasury's reply lists them as the existing "wealth taxes".
- The EFF's proposals mix an annual levy on luxury land (a property tax, left out) with a once-off levy on trust assets (included as `one_off_levy`) and an annual levy on inherited wealth above R10 million (not recorded: no source read).
- `forgood.org.za` serves a different page to scripts, so `checkquotes` cannot verify its quotes; read them in a browser.
