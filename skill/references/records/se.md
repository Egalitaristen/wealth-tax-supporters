# Sweden: where the official record is and how to read it

Written in run R026 (2026-11-08) and deepened in run R027 (2026-11-09, official legislative records deep-dive for Sweden). Country guide for maps, seats and local portals: `skill/references/countries/se.md` (and `data/se/area_profile.md`). This file answers one question: **where is everything the Riksdag and government have put on record about wealth taxation (*förmögenhetsskatt* / *miljardärsskatt*), and how do I get all of it?** Nothing here is a source for a claim in the register; the register's own sources are.

### Institutional and Legislative Context

1. **Abolition in 2007:** Sweden abolished its national net wealth tax (*statlig förmögenhetsskatt*, governed by *lagen (1997:323) om statlig förmögenhetsskatt*) effective from 1 January 2007 through government proposition 2007/08:26 (*Slopad förmögenhetsskatt m.m.*), approved by the Riksdag in December 2007 on recommendation of the Committee on Taxation (*Skatteutskottets betänkande 2007/08:SkU15*).
2. **Post-2010 Parliamentary Dynamics:** Since 2010, the question of reinstating or reforming wealth taxation has never reached the Riksdag as a government bill (*regeringsproposition*). Instead, wealth taxation has reached the chamber via:
   - **Private member motions (*enskilda motioner*):** Individual MPs submitting proposals during the annual general private members' motions period (*allmänna motionstiden*), e.g. Motion 2009/10:Sk342 (Sachet, S), 2013/14:Sk403 and 2016/17:2632 (Lillemets & Mutt, MP), and 2020/21:1885 (Järrebring m.fl., S).
   - **Party and committee motions (*parti- och kommittémotioner*):** Comprehensive economic and tax policy alternatives submitted by the Left Party (*Vänsterpartiet*, V) and the Green Party (*Miljöpartiet*, MP), including dedicated chapters proposing annual wealth taxes (*förmögenhetsskatt*) and billionaire taxes (*miljardärsskatt*).
   - **Spring fiscal bill counter-motions (*vårmotioner*):** Alternative proposals to the government's spring fiscal policy bill (*prop. 100, den ekonomiska vårpropositionen*), e.g. Motion 2025/26:4108 (V) and 2025/26:4118 (MP).
   - **Official Government Inquiries (*Statens offentliga utredningar*, SOU):** Most notably the Equality Commission (*Jämlikhetskommissionen*), SOU 2020:46 *En gemensam angelägenhet*, part 2, which formally recommended reintroducing an annual net wealth tax.
3. **Absence of Standalone Roll-Call Votes:** In the Riksdag, motions proposing a wealth tax are handled by *Skatteutskottet* (SkU) or *Finansutskottet* (FiU). Standalone motion points are routinely rejected by acclamation (*acklamation*), meaning no electronic roll-call division is recorded. When division votes do occur on tax policy, wealth-tax motions are either bundled into omnibus decision points containing numerous unrelated motions (e.g. 2013/14:SkU17 punkt 1) or voted as part of overall budget framework reservations (*rambeslut* in FiU1 and FiU20). Under standard QA rules, omnibus block votes are discarded.

---

## 1. Bills, motions and proposals

- **Riksdag Open Data REST API (tested and fully functional):** `https://data.riksdagen.se/`
  - Unauthenticated JSON and XML API covering bills, motions, committee reports, parliamentary questions, and plenary debates.
  - **Document list endpoint:**
    `https://data.riksdagen.se/dokumentlista/?sok={term}&doktyp={type}&from={YYYY-MM-DD}&tom={YYYY-MM-DD}&sz=200&p={page}&utformat=json`
    - Parameter `@sidor` in the response indicates total pages.
    - Important document types (`doktyp`): `mot` (motions), `bet` (committee reports), `ip` (interpellations), `fr` (written questions), `frs` (oral questions), `prop` (government bills), `sou` (government inquiries), `dir` (inquiry directives), `ds` (ministry reports), `prot` (plenary protocols).
  - **Document metadata and signatories endpoint:**
    `https://data.riksdagen.se/dokumentstatus/{dok_id}.json`
    - Contains `dokumentstatus.dokintressent.intressent[]` listing each signer's `namn`, `partibet`, and `roll` (`undertecknare`).
  - **Full-text endpoints:**
    - Raw text: `https://data.riksdagen.se/dokument/{dok_id}.text` (XML containing the unescaped plain text).
    - Web view for citing and quote-checking: `https://data.riksdagen.se/dokument/{dok_id}.html`.
- **Search terms (Swedish):**
  - *Core wealth tax terms:* `förmögenhetsskatt`, `förmögenhetsskatten`, `förmögenhetsskatter`, `förmögenhetsbeskattning`, `miljardärsskatt`, `miljardärsskatten`, `miljardärskatt`, `skatt på förmögenheter`, `skatt på stora förmögenheter`, `skatt på superrika`, `Zucmanskatt`.
  - *Excluded look-alikes:*
    - `förmögenhetsregister`, `förmögenhetsdeklaration`, `förmögenhetsstatistik`: asset registry and statistical data collection (e.g. SOU 2022:51), not a tax.
    - `arvs- och gåvoskatt`: inheritance and gift taxes abolished in 2004 (excluded).
    - `fastighetsskatt` / `fastighetsavgift`: real property tax / municipal property fee (excluded).
    - `kapitalskatt`: income taxes on dividends, interest, or capital gains (excluded).
    - `solidaritetsskatt`: in Swedish parliamentary usage refers to personal income surtaxes, not net wealth taxation.
- **Qualified Post-2010 Wealth Tax Bills & Motions:**
  1. **Motion 2011/12:Sk291** (*GZ02Sk291*, 2011-09-29): *Översyn av det svenska skattesystemet* by Lars Ohly and Left Party group MPs (E00001–E00008). Proposes an inquiry into reinstating a reformed net wealth tax.
  2. **Motion 2011/12:Fi17** (*GZ02Fi17*, 2012-04-28): Left Party spring budget motion by Jonas Sjöstedt m.fl. (E00009–E00014) proposing a wealth tax model.
  3. **Motion 2013/14:Sk201** (*H102Sk201*, 2013-09-19): *Översyn av det svenska skattesystemet* by Jacob Johnson and Left Party group MPs (E00196–E00201). Proposes reinstating wealth taxation.
  4. **Motion 2013/14:Sk403** (*H102Sk403*, 2013-10-03): *Arvsskatt och förmögenhetsskatt* by Annika Lillemets and Valter Mutt (MP) (E00043–E00044). Calls for an inquiry to prepare reintroducing the wealth tax.
  5. **Motion 2013/14:Fi254** (*H102Fi254*, 2013-10-03): Left Party budget alternative by Jonas Sjöstedt m.fl. (E00202–E00207).
  6. **Motion 2016/17:2632** (*H4022632*, 2016-10-05): *Arvs- och förmögenhetsskatt* by Annika Lillemets and Valter Mutt (MP) (E00045–E00046). Urges reintroducing a progressive wealth tax.
  7. **Motion 2017/18:2962** (*H5022962*, 2017-10-05): *Solidarisk ekonomi* by Valter Mutt, Carl Schlyter, and Annika Lillemets (MP) (E00047–E00049).
  8. **Motion 2018/19:3093** (*H6023093*, 2019-04-29): Left Party spring budget motion by Jonas Sjöstedt m.fl. (E00208–E00215).
  9. **Motion 2019/20:2915** (*H7022915*, 2019-10-03): *En plan för jämlikhet och grön omställning* by Jonas Sjöstedt and Left Party group MPs (E00015–E00023). Specifies an annual wealth tax of 1% above SEK 5M and 2% above SEK 10M.
  10. **Motion 2019/20:3601** (*H7023601*, 2020-04-29): Left Party spring budget motion by Jonas Sjöstedt m.fl. (E00050).
  11. **Motion 2020/21:1885** (*H8021885*, 2020-10-02): *Jämlik skattepolitik* by Joakim Järrebring and Social Democratic MPs (E00052). Argues for wealth taxation in broad tax reform.
  12. **Motion 2020/21:3170** (*H8023170*, 2020-10-06): *Vägen ut ur krisen – en plan för jämlikhet och grön omställning* by Jonas Sjöstedt m.fl. (V) (E00216–E00223).
  13. **Motion 2020/21:4031** (*H8024031*, 2021-04-29): Left Party spring budget motion by Nooshi Dadgostar m.fl. (E00051).
  14. **Motion 2021/22:3278** (*H9023278*, 2021-10-04): *Röd politik för en grön omställning* by Nooshi Dadgostar and Left Party MPs (E00024–E00032). Proposes an annual wealth tax on high net fortunes.
  15. **Motion 2025/26:4108** (*HD024108*, 2026-04-28): Left Party spring budget motion by Nooshi Dadgostar m.fl. (E00033–E00042). Proposes an inquiry into a billionaire tax (*miljardärsskatt*).
  16. **Motion 2025/26:4118** (*HD024118*, 2026-04-29): Green Party spring budget motion by Daniel Helldén and 18 other MP members (E00059–E00077). Proposes an annual tax on billionaires to fund green investments.
  17. **SOU 2020:46 (del 2)** (*H8B346d2*, 2020-08-24): *En gemensam angelägenhet*, report of the Equality Commission (*Jämlikhetskommissionen*, chair Per Molander) recommending the reintroduction of an annual net wealth tax.

---

## 2. Debates and votes

- **Plenary Debate Protocols (*Kammarens protokoll*, `prot`):**
  - Daily proceedings are published in full verbatim stenographic text at:
    `https://data.riksdagen.se/dokument/{id}.html` (e.g. `HD09135.html` for 2025/26 sitting 135).
  - **Speaker attribution syntax:** Speeches are demarcated by bold numbered headings:
    `Anf. {N} {FIRSTNAME} {LASTNAME} ({PARTY})` (e.g. `Anf. 67 ILONA SZATMÁRI WALDAU (V):`, `Anf. 120 JONAS SJÖSTEDT (V) replik:`).
  - Speeches can be accurately located and mapped using `skill/scripts/adapters/se_riksdag_scan.py speeches`.
  - **Verified Chamber Speeches Defending Wealth/Billionaire Taxation:**
    - 2012-13 sitting 81 (*H00981*): Jacob Johnson (V) (E00088)
    - 2013-14 sitting 82 (*H10982*): Annika Lillemets (MP) (E00084)
    - 2015-16 sitting 13 (*H30913*): Jonas Sjöstedt (V) (E00224)
    - 2015-16 sitting 103 (*H309103*): Daniel Sestrajcic (V) (E00225)
    - 2016-17 sitting 5 (*H4095*): Ulla Andersson (V) (E00078)
    - 2016-17 sitting 52 (*H40952*): Jonas Sjöstedt (V) (E00079)
    - 2016-17 sitting 88 (*H40988*): Daniel Sestrajcic (V) (E00080)
    - 2017-18 sitting 39 (*H50939*): Momodou Jallow (V) (E00226)
    - 2017-18 sitting 98 (*H50998*): Ulla Andersson (V) (E00228)
    - 2017-18 sitting 136 (*H509136*): Annika Lillemets (MP) (E00085)
    - 2018-19 sitting 72 (*H60972*): Jens Holm (V) (E00081)
    - 2019-20 sitting 140 (*H709140*): Amineh Kakabaveh (independent / former V) (E00086)
    - 2021-22 sitting 33 (*H90933*): Tony Haddou (V) (E00087)
    - 2021-22 sitting 38 (*H90938*): Jessica Wetterling (V) (E00227)
    - 2025-26 sitting 57 (*HD0957*): Nooshi Dadgostar (V) (E00082)
    - 2025-26 sitting 135 (*HD09135*): Ilona Szatmári Waldau (V) (E00083)

- **Electronic Roll-Call Voting Records (*Voteringlista*):**
  - Per-member division records are queried via:
    `https://data.riksdagen.se/voteringlista/?rm={session}&bet={report}&punkt={number}&utformat=json`
  - Per-member ballot values: `Ja`, `Nej`, `Avstår`, `Frånvarande`.
  - **Why No Standalone Wealth Tax Roll-Call Exists:**
    - Reports 2016/17:SkU23 punkt 8 and 2017/18:SkU9 punkt 10 (the Green Party's standalone proposals for inheritance and wealth taxation) were decided by acclamation (*acklamation*). The API returns `no vote data`.
    - Report 2013/14:SkU17 punkt 1 bundled 14 distinct motions together under "Företagande och investeringar, allmänna frågor", preventing attribution of any vote specifically to the wealth tax.
    - Budget resolutions in *Finansutskottet* (*FiU1* autumn budget and *FiU20* spring budget) are voted as entire budget package reservations (*rambeslut*), which are omnibus votes discarded by QA rules.

---

## 3. Members, parties, seats

- **Riksdag Member Register (*Personlista*):**
  - Complete historical register: `https://data.riksdagen.se/personlista/?utformat=json&rdlstatus=samtliga`
  - Filters: `fnamn` (first name), `enamn` (last name).
  - Key fields: `intressent_id`, `tilltalsnamn`, `efternamn`, `parti`, `valkrets`, `status` (`Tidigare riksdagsledamot`, `Avliden  YYYY-MM-DD`), `fodd_ar`.
  - Alive-check protocol: Check `status` field. Any member marked `Avliden` must be moved to `exclusions.csv` (`deceased`).
- **Wikidata Integration:**
  - Swedish MPs have high-quality Wikidata coverage with birth/death dates and parliamentary terms.

---

## 4. Other official records

- **Government Inquiries (*Statens offentliga utredningar*, SOU):**
  - Queryable via `doktyp=sou`.
  - SOU 2020:46 *En gemensam angelägenhet* (Equality Commission) represents the primary official post-2010 inquiry advocating for a net wealth tax.
  - SOU 2022:51 *En ny statistik över hushållens tillgångar och skulder* analyzes data gaps resulting from wealth tax abolition, but restricts its scope to statistical methodology rather than tax design.
- **Regional and Municipal Council Portals:**
  - Swedish municipalities and regions do not levy net wealth taxes (statutory tax power rests with the state).
  - MeetingPlus portals (Stockholm, Huddinge, Danderyd, Region Gotland) can be searched using `skill/scripts/adapters/se_meetingplus_scan.py`.

---

## 5. Access notes

- **Networking & IPv6:** On Windows systems, queries to `data.riksdagen.se` may suffer connection resets if routed via IPv6 (`2001:6b0:48::101`). Scripts (`se_riksdag_scan.py`, `wtdb.py`) enforce IPv4 resolution to guarantee instant, reliable access.
- **Word Splitting & Soft Hyphens:** Riksdag documents converted from Word via Aspose frequently embed soft hyphens (`&#xad;`, `\xad`) inside HTML tags (e.g. `miljardärs</span><span>&#xad;</span><span>skatt`). `wtdb.py` automatically normalizes these patterns during quote verification.
- **Encoding:** Swedish primary texts must be handled in UTF-8 (`python -X utf8` on Windows).

---

## 6. Coverage log

| Date | Run | Documents read (title, number, date) | Result (rows added, votes found) | Not read / open |
|---|---|---|---|---|
| 2026-11-08 | R026 | Full text of Riksdag documents returned for wealth-tax terms from 2006/07 to 2026/27: 175 motions, 180 interpellations, 25 written questions, 30 oral questions, 210 committee reports, 31 opinions, 129 bills, 64 SOU, 393 chamber protocols. 385 documents catalogued in `documents.csv`. | 34 evidence rows from 4 motion signature blocks and 6 speeches, 1 commission report (E00196–E00230); 0 standalone votes found (acclamation or omnibus bundles). | Budget motions read at tax sections; municipal portals outside MeetingPlus. |
| 2026-11-09 | R027 | Deep legislative records pass: comprehensive verification of 196 chamber protocols (2010–2026), full cataloguing of all 17 qualified post-2010 wealth-tax bills/motions and SOU reports, added Motion 2025/26:4118 (M0386) to `documents.csv`, expanded `data/resources.json` with 8 new qualified bills and SOU 2020:46, resolved Aspose soft-hyphen quote issues on 10 Left Party signatories (E00033–E00042), updated records guide. | 11 qualified resources in `data/resources.json`, M0386 logged in `documents.csv`, 10 quotes perfected and verified, all QA checks passing. | Autumn 2026/27 sittings post-October; municipal motion registers of Göteborg and Malmö. |

---

## 7. Known gaps and next steps

- **Autumn 2026/27 Sittings:** Continuously monitor the Riksdag API for general motions period filings following government formation.
- **Municipal Council Motion Books:** Malmö and Göteborg publish open PDF motion registries; individual motions addressing national tax policy could be systematically swept in future municipal refinement passes.
