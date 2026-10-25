# Japan: a wealth tax proposed by the left, argued by a citizens' coalition

A twelfth worked example. Japan has no net-wealth tax. The Japanese Communist Party proposes an annual tax of 0.5 to 3% on net assets above 500 million yen, the SDP and Reiwa Shinsengumi answered a 2025 tax-justice questionnaire in favour, and a citizens' coalition (公正な税制を求める市民連絡会) with scholars and lawyers published *Introduction to the Wealth Tax* in September 2025. Check every URL still works before relying on it.

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | National Diet (House of Representatives, House of Councillors), government | Diet records are on `kokkai.ndl.go.jp`. The pages are JavaScript, so `wtdb.py checkquotes` reads them through the Diet's open API (`/api/speech?issueID=…`), which is built in |
| region | 47 prefectures | Two-digit JIS X 0401 code |
| council | 1,749 municipalities | The map tier, with the five-digit JIS X 0402 code |

**Map:** `data/jp/boundaries.json` uses the Geospatial Information Authority of Japan's *Global Map Japan* (2016), as packaged by the npm package `jpn-atlas` (BSD-3-Clause is the package's own licence; the data are GSI's, under terms compatible with CC BY 4.0, credit "国土地理院"). The 2016 vintage means municipal mergers since then are not reflected.

## What counts, and what was removed in review

- **Counts:** a Diet or assembly speech that names a wealth tax, a party's own policy document (the party row), a coalition's co-representatives (grade B: a roster), and scholars and lawyers who write for a wealth tax.
- **Does not count:** a candidate or assembly member listed on a party roster page, or carrying the party's manifesto sentence, with nothing of their own. The first draft had about 560 such rows (Communist Party candidates and assembly members, SDP and Reiwa candidates); they were removed, and the three party rows stay.
- **Seats:** `python skill/scripts/seats.py data/jp` reads the **House of Representatives** (465; ten pages `shugiin.go.jp/internet/itdb_annai.nsf/html/statics/syu/<1-10>giin.htm`, Shift-JIS, one row per member with name, reading, group, constituency and terms) and the **House of Councillors** (248; the page of the latest Diet session, `sangiin.go.jp/japanese/joho1/kousei/giin/<session>/giin.htm`: the script tries session numbers upward from 222). Names are in kanji, so a supporter is matched on the kanji in brackets after the Latin name in the register (`Akira Koike (小池晃)`): give every Japanese politician their kanji. Groups: LDP, CDP, Ishin, DPP, Komeito, JCP, Reiwa, Sanseito are named in English; other groups (中道, みらい, 志士, 民主) stay as the House writes them until someone checks their English names.
