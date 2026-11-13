# Senegal: sources and geography

Seed pass R001 (2026-11-13). 1 supporter, 1 evidence row. Check that URLs still resolve.

## Levels and geography
| Level | Units | Notes |
|---|---|---|
| national | Assemblée nationale (165, single chamber since the Senate's abolition in 2021) | Tax law is national. |
| region | 14 régions (`SN01`...) | OCHA COD-AB admin 1 |
| county | 46 départements (`SN0101`...) | admin 2 |
| council | 125 arrondissements (`SN010101`...) | admin 3, the lowest tier with an open map and official codes; the ~550 elected communes are not loaded |

**Map:** OCHA / HDX "Senegal - Subnational Administrative Boundaries" (COD-AB, CC BY-IGO 3.0), `sen_admin_boundaries.geojson.zip`, updated 2026-01. Recipe as for Tunisia (`countries/tn.md`): `topo_to_boundaries.py` on `sen_admin3/2/1.geojson` with `--name-prop adm?_name --code-prop adm?_pcode --project lonlat --scale 120 --simplify 0.35`, then `merge_boundaries.py units --regions departments --upper regions`. `geo_units.csv` is built from the same files.

## Seats
`https://www.assemblee.sn/` shows "Législatives 2024, Les Chiffres exacts" by list (130 Pastef, 16 Takku Wallu, ...). The site is an Angular app: plain `curl` returns an empty shell, so read it in a browser. The chart follows the election lists; the site's parliamentary group page shows only Pastef (99 members). No member list with constituencies was read.

## Debate
No wealth tax exists or is proposed. Aminata Touré (Vatican/ICRICT, 13 February 2025) is the only statement found. The ICRICT release (`icrict.com/non-classe/its-time-to-tax-power-icricts-message-at-the-vatican/`) quotes her; `checkquotes` could not read it, so the quote was checked by hand. Search tools return mostly French (taxe Zucman) pages for Senegalese queries; use site searches of Senegalese outlets instead.
