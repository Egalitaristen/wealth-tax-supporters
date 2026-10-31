# Area profile — Austria (AT)

*Last updated: 2026-10-31 (Seed Pass)*

## 1. Scope
- **Area:** Austria (Republic of Austria / *Republik Österreich*); ISO 3166-1 alpha-2: `AT`.
- **Depth:** Seed pass (National tier + 9 Federal States / *Bundesländer* + initial municipal anchors Vienna and Graz).
- **Levels of government in scope:**
  - National: Nationalrat (183 seats), Bundesrat (61 seats), Federal Government (*Bundesregierung*).
  - Regional: 9 Federal States (*Bundesländer*: Burgenland, Kärnten, Niederösterreich, Oberösterreich, Salzburg, Steiermark, Tirol, Vorarlberg, Wien).
  - Local: 2,093 Municipalities (*Gemeinden*, with official 5-digit *Gemeindekennziffer* / GKZ codes).
- **Languages:** German (*Deutsch*).
- **Date of first run:** 2026-10-31 (Run `R001`).

---

## 2. Wealth tax history and live proposals (2010 onwards)
- **Historical context:** Austria historically levied an annual net wealth tax (*Vermögensteuer* under the *Vermögensteuergesetz 1954*), which was abolished under Finance Minister Ferdinand Lacina (SPÖ) in 1993 (effective 1 January 1994) in exchange for the introduction of capital gains withholding tax (*KESt*). Inheritance and gift tax (*Erbschafts- und Schenkungssteuer*) lapsed on 31 July 2008 following a 2007 Constitutional Court (*VfGH*) ruling.
- **Active proposals & models:**
  - **SPÖ Model (Babler Model):** Progressive net wealth tax starting at €1,000,000 net assets.
    - Slices: 0.5% (€1m–€10m), 1.0% (€10m–€50m), 2.0% (>€50m).
    - Allowances: Owner-occupied primary residence (*Eigenheim*) exempt up to €1,500,000.
    - Yield: Estimated by Momentum Institut at €5.0 billion annually. Targets the top 1–2% of households while relieving income taxes on labor.
  - **ÖGB / AK Joint Model:** Progressive net wealth tax starting at €1m with rates between 0.5% and 1.5%.
  - **Gewerkschaft GPA Model:** 0.5% (>€1m), 1.0% (>€10m), 1.5% (>€100m).
  - **Attac Österreich Model:** Corona-Lastenausgleich / Vermögensabgabe starting at €5m progressive up to 10% on billion-euro fortunes.
  - **KPÖ Model:** Progressive wealth tax starting at €1m protecting primary residences to relieve municipalities.
- **Key Exclusions (Ground Rule 1):**
  - **Die Grünen (Werner Kogler):** Campaign under the slogan *"Superreiche fair besteuern"*, but their legislative demands and party platform are strictly limited to an inheritance tax on large estates (*Millionenerbschaften* from €1m), rejecting or omitting an annual net wealth tax. Excluded per Ground Rule 1 under `out_of_definition`.

---

## 3. Legislatures and where their records are
- **Chamber:** Nationalrat (183 seats, XXVIII. GP elected 29 September 2024).
- **Portal:** [Austrian Parliament Portal](https://www.parlament.gv.at) (License: CC BY 4.0).
- **Data APIs:**
  - Sitting MPs & Filters: Open JSON POST API `https://www.parlament.gv.at/Filter/api/json/post?jsMode=EVAL&FBEZ=WFW_002&...`
  - Item Details: Append `?json=TRUE` to any bill, motion, or person URL (e.g. `https://www.parlament.gv.at/gegenstand/XXVII/UEA/1077?json=TRUE`).
  - Plenary debates (*Stenographische Protokolle*): Full text and downloadable PDFs at `https://www.parlament.gv.at/dokument/...`.

---

## 4. Parties & parliamentary alignment
- **FPÖ (57 seats):** Strongly opposes any wealth or inheritance tax; labels proposals as "standortfeindlich" and expropriation.
- **ÖVP (51 seats):** Strongly opposes; strict veto on "Substanzsteuern".
- **SPÖ (41 seats):** Main political champion of annual net wealth tax under party leader Andreas Babler.
- **NEOS (17 seats):** Opposes; advocates income and corporate tax cuts instead.
- **Grüne (16 seats):** Advocates inheritance tax (*Erbschaftssteuer*) on fortunes >€1m, but not an annual recurring wealth tax (Ground Rule 1 exclusion).
- **KPÖ (non-parliamentary federally; state/local representation):** Strongly supports annual wealth tax from €1m.

---

## 5. Government below national level
- **Federal Structure:** 9 Federal States (*Bundesländer*). Each has an elected state parliament (*Landtag*).
- **Municipal Tier:** 2,093 Municipalities (*Gemeinden*).
- **Fiscal powers:** Austrian fiscal federalism (*Finanzausgleich*) concentrates direct tax powers at the federal level. Municipalities rely on *Kommunalsteuer* (payroll tax), *Grundsteuer* (property tax based on outdated *Einheitswerte*), and federal tax shares (*Ertragsanteile*).
- **Local dynamics:** Because municipalities have experienced structural deficit crunches, left/progressive city councillors (e.g. KPÖ Graz, SPÖ Vienna/Linz) regularly table local council motions urging the Federal Government to reintroduce wealth taxation to fund local services.

---

## 6. Search terms
- Primary German terms: `Vermögensteuer`, `Vermögenssteuer`, `Millionärssteuer`, `Millionärsabgabe`, `Vermögensabgabe`, `Superreiche besteuern`.
- Ambiguous terms to check carefully: `Erbschaftssteuer`, `Erbschaftsteuer`, `Schenkungssteuer` (excluded under Ground Rule 1 unless coupled with annual net wealth tax); `Grundsteuer` (property tax).

---

## 7. Media & primary repositories
- **News agencies & press releases:** [APA-OTS](https://www.ots.at) (official open PR clearinghouse, extensive verbatim quotes from all political and civil society actors).
- **Newspapers & media:** *Der Standard*, *Die Presse*, *Kurier*, *ORF*, *Profil*, *Trend*, *Kontrast.at* (SPÖ parliamentary club publication), *Arbeit & Wirtschaft* (AK/ÖGB publication).

---

## 8. Known networks & key civil society organisations
- **Trade unions:** ÖGB (*Österreichischer Gewerkschaftsbund*), Gewerkschaft GPA, Gewerkschaft Bau-Holz (GBH), PRO-GE.
- **Chambers:** *Arbeiterkammer* (AK / Federal Chamber of Labour).
- **Think tanks:** *Momentum Institut* (lead research institute producing distribution and revenue models).
- **NGOs & Campaigns:** *Attac Österreich*, *taxmenow* (German-speaking wealthy advocates initiative active in Austria), *Guter Rat für Rückverteilung*.

---

## 9. Plan for the next runs
- **Standard Pass (R002):**
  1. Expand Nationalrat coverage: sweep all SPÖ MPs on the Finance & Budget Committee (*Finanzausschuss*).
  2. Landtag resolution motions: sweep Vienna (*Gemeinderat / Landtag Wien*), Graz, and Linz city council debates.
  3. Austrian MEPs in the European Parliament: verify cross-border support for EU-wide wealth tax initiatives (e.g. European Citizens' Initiative *Tax the Rich*).
  4. Follow up on cross-country leads `D0001` (Ernest Fuhrmann) and check *taxmenow* Austrian network members.
