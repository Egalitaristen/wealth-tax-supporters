# Turkey (Türkiye): Wealth Tax Landscape and Reference

Turkey enacted the controversial *Varlık Vergisi* in 1942 (Law No. 4305), an emergency WWII capital levy with discriminatory application that was repealed in 1944. Modern wealth tax proposals are deliberately distinguished as an annual, progressive net wealth tax (*artan oranlı servet vergisi*). Proponents cluster in left, socialist, and pro-Kurdish political parties (DEM Parti, TİP, EMEP, TÖP), progressive trade union confederations (DİSK, KESK), and independent academic economists. In March 2024, billionaire industrialist İbrahim Erdemoğlu (Erdemoğlu Holding / SASA) publicly urged a mandatory 1% wealth tax on assets over 6m TL for earthquake recovery and urban transformation. An Earth4All / Ipsos G20 public opinion survey in June 2024 revealed 78% public support in Turkey for a wealth tax on the rich—the second highest in the G20.

## Levels and the Geography Register

| Level (`level`) | Units | Notes |
|---|---|---|
| `national` | Grand National Assembly of Turkey (TBMM), Presidency, Ministries | TBMM has 600 seats. Official seat distribution published at `https://www.tbmm.gov.tr/sandalyedagilimi`. |
| `regional` | 81 provinces (*iller*) | Coded TR-01 to TR-81 using standard Turkish traffic/administrative codes (ISO 3166-2:TR). 30 provinces are organized as Metropolitan Municipalities (*Büyükşehir Belediyeleri*). |
| `local` | 973 districts (*ilçeler*) | The map tier. Coded `TR-D-{province}-{district}`. Municipalities have zero statutory or constitutional power to levy broad wealth taxes under Article 73 of the Constitution. |

## Map and Boundaries

`data/tr/boundaries.json` contains:
- 973 district polygons (local tier).
- 81 province region boundary lines (regional tier).
- ViewBox and projection: EPSG:4326 projected with scale factor 300 to match repository standards.
- Source: UN OCHA COD-AB-TUR dataset via Humanitarian Data Exchange (HDX) / `ttezer/turkiye-harita-verisi`, licensed under Creative Commons Attribution for Intergovernmental Organisations (CC BY-IGO).

To rebuild the boundaries file:
```bash
python scripts/build_tr_boundaries.py
```
The script downloads/reads the TopoJSON, matches all 973 districts and 81 provinces to `data/tr/geo_units.csv`, projects and simplifies geometry using `skill/scripts/topo_to_boundaries.py` and `skill/scripts/merge_boundaries.py`, and writes `data/tr/boundaries.json`.

## Chamber and Seats

The Grand National Assembly of Turkey (*Türkiye Büyük Millet Meclisi* - TBMM) is the unicameral national legislature:
- **Total seats:** 600.
- **28th Term distribution (as of October 2026):**
  - Adalet ve Kalkınma Partisi (AK Parti): 266
  - Cumhuriyet Halk Partisi (CHP): 128
  - Halkların Eşitlik ve Demokrasi Partisi (DEM Parti): 57
  - Milliyetçi Hareket Partisi (MHP): 47
  - İYİ Parti: 30
  - Saadet Partisi: 20
  - Bağımsız Milletvekili (Independents): 7
  - Hür Dava Partisi (HÜDA PAR): 4
  - Yeniden Refah Partisi (YRP): 4
  - Demokrat Parti (DP): 3
  - Türkiye İşçi Partisi (TİP): 3
  - Emek Partisi (EMEP): 2
  - Demokrasi ve Atılım Partisi (DEVA Partisi): 1
  - Demokratik Bölgeler Partisi (DBP): 1
  - Demokratik Sol Parti (DSP): 1
  - Gelecek Partisi: 1
  - Vacant seats: 8
  - Total: 600
- Official records:
  - Seat distribution: [TBMM Sandalye Dağılımı](https://www.tbmm.gov.tr/sandalyedagilimi)
  - Plenary debates: [TBMM Tutanak Dergisi](https://www.tbmm.gov.tr/Tutanaklar/TutanakMetinleri)
  - Legislative proposals: [TBMM Kanun Teklifleri](https://www.tbmm.gov.tr/Denetim/Kanun-Teklifleri)

## Research Quirks and Constitutional Context

1. **Constitutional Primacy of National Taxation (Article 73):** Under Article 73 of the Constitution of the Republic of Turkey (*"Vergi, resim, harç ve benzeri mali yükümlülükler kanunla konulur, değiştirilir veya kaldırılır"*), all taxation powers are reserved to the TBMM by statute. Municipal councils (*belediye meclisleri*) cannot introduce general wealth or net wealth taxes. Local initiatives and petitions invariably demand legislative action from the national parliament rather than local municipal ordinances.
2. **Historical Terminology Sensitivity:** When searching Turkish sources, `Varlık Vergisi` refers specifically to the 1942 WWII discriminatory capital levy. Modern wealth tax advocacy uses `servet vergisi` or `artan oranlı servet vergisi` (progressive wealth tax).
3. **Excluded Taxes:**
   - `Değerli Konut Vergisi` (Law No. 7194): A luxury housing tax on residential properties exceeding specified valuation thresholds. Excluded as a narrow immovable real-estate tax.
   - `Emlak Vergisi` (Law No. 1319): Standard municipal real estate tax. Excluded.
   - `Veraset ve İntikal Vergisi` (Law No. 7338): Inheritance and transfer tax. Excluded unless integrated into an annual comprehensive net wealth tax proposal.

## Key Proponent Clusters

- **Political Parties:** DEM Parti (manifesto), TİP (party congress resolution), EMEP (party campaign and leadership), SOL Parti (crisis solution program).
- **Trade Unions:** Peak confederations DİSK and KESK; major sectoral affiliates Birleşik Metal-İş (United Metalworkers) and Eğitim Sen (Education and Science Workers).
- **Parliamentarians (TBMM):** Perihan Koca (bill sponsor), Garo Paylan (budget commission speeches), Sevda Karaca (plenary address).
- **Academic Economists:** Korkut Boratav, Erinç Yeldan, Aziz Konukman, Mustafa Durmuş, Oğuz Oyan, Hayri Kozanoğlu.
- **Industry & Business:** İbrahim Erdemoğlu (billionaire chairman of Erdemoğlu Holding / SASA).
- **Civil Society & NGOs:** KEDV (Kadın Emeğini Değerlendirme Vakfı / Oxfam Türkiye).
