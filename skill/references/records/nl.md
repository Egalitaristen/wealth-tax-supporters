# Netherlands: where the official record is and how to read it

Written in run R030 (2026-11-08) by reading the Tweede Kamer and Eerste Kamer record for wealth-tax terms from 2006 to November 2026. Every URL and method below was tested on that date; failures are stated.

Key fact for the Netherlands: **almost every vote on a wealth-tax motion is by show of hands** ("Met handopsteken"). The open data lists the vote per fractie (party group), never per member. So a vote makes nobody an individual supporter. The individual evidence is: the signatories of a motion or amendment (open data and the printed document), speeches in Handelingen and committee reports, and the rare named vote (hoofdelijke stemming), printed in Handelingen.

## 1. Bills, motions and proposals

**Local terms** (use all): `miljonairsbelasting`, `miljonairstaks` (colloquial), `miljardairsbelasting`, `vermogensbelasting`, `vermogensheffing`, `belasting op vermogen`, `vermogensplafond`, `solidariteitsheffing`, `extreem rijken`, `superrijken`, `Zucman` (Zucmanbelasting), `minimumbelasting` + `vermogen`. Read context every time: `vermogensbelasting`, `vermogenstaks`, `vermogensrendementsheffing` and `vermogensaanwasbelasting` almost always mean **box 3** (a tax on a deemed or actual return on savings and investments). That is not a wealth tax under the definition. A tax on net wealth (miljonairsbelasting, "1% boven 1 miljoen", a levy on the asset base) is. A solidarity levy on incomes or companies, a vermogenswinstbelasting (capital gains), an inheritance tax and an "effective tax rate for the richest" are out.

**Tweede Kamer open data (OData v4), tested and works:** `https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/`
- `Document?$filter=contains(Onderwerp,'miljonairsbelasting') and (Soort eq 'Motie' or Soort eq 'Amendement')&$select=Id,DocumentNummer,Soort,Onderwerp,Datum` finds motions and amendments by subject line. Subjects are short; a motion whose subject does not contain the term is missed, so also use the full-text route below.
- Signatories: `Document?$filter=DocumentNummer eq '2024D13520'&$expand=DocumentActor` gives `ActorNaam`, `ActorFractie`, `Relatie` ("Eerste ondertekenaar", "Mede ondertekenaar") and `Persoon_Id`. This is the sponsor list and a formal act (grade A for a wealth-tax motion or amendment).
- Text of any document: `Document(<Id>)/resource` returns the PDF (use `pdftotext -layout`).
- Votes: `Document?...&$expand=Zaak($expand=Besluit($expand=Stemming))`. `Besluit.StemmingsSoort` is `Met handopsteken` (Stemming rows per fractie only, `Persoon_Id` null) or a named vote (rows with `Persoon_Id`). Always check which.
- Queries with many `contains(...)` terms on `Document` can take minutes without a `Soort` filter; filter on `Soort` and `Datum`. A query on the unfiltered `vermogen` term returns about 250 irrelevant motions.
- `Persoon` gives names and the Tweede Kamer's `Id` for members; `Activiteit`, `Verslag` exist but were not needed.

**Full-text search of all official publications (best route for speeches), tested and works:** SRU at `https://repository.overheid.nl/sru?query=<CQL>&operation=searchRetrieve&x-connection=officielepublicaties&maximumRecords=100&startRecord=N` (XML). Example query: `cql.textAndIndexes=miljonairsbelasting`; add `and dt.creator="Eerste Kamer der Staten-Generaal"` to restrict to the Senate; `w.publicatienaam=Handelingen` restricts to plenary reports. Each record carries `dcterms:identifier`, `title`, `date` and `gzd:preferredUrl`. Page with `startRecord`; the server returns at most 2000 usable results per query, so use specific terms (a query on `vermogensbelasting` alone returns 9,000 mostly box 3 documents). The text of a hit is at `https://zoek.officielebekendmakingen.nl/<identifier>.html` (HTML, 200 for all 460 documents fetched). The older URL `repository.overheid.nl/frbr/sru/` returns 404; the web search form `zoek.officielebekendmakingen.nl/resultaten?...` works but is HTML only.

**Tweede Kamer website:** `https://www.tweedekamer.nl/zoeken?qry=...` returns 200 (HTML, JavaScript results); `kamerstukken/detail?did=<DocumentNummer>&id=<ZaakNummer>` is the stable human page for a document with its vote summary.

**Bills** (wetsvoorstellen) on a wealth tax: only one initiative exists, **36 173 (Wet vermogensbelasting 2024, Nijboer c.s., 2022)**, a progressive levy on the box 3 asset base, still pending. Government bills do not propose a net wealth tax.

**Sponsors:** printed under the motion text (the last lines list the signatories in order) and in `DocumentActor`. For bill 36 173 the sponsors and later defenders are in the letters 36 173 nr. 1, 4, 5 and 6.

**Government proposals and consultations:** Ministerie van Financiën letters in Kamerstuk 32 140 (Herziening Belastingstelsel) and 25 087 (Internationaal fiscaal beleid), e.g. 32 140 nr. 71 (Bouwstenen 2020, includes a millionaire-tax fiche), 25 087 nr. 342 (follow-up to the 30-member debate on an extra tax for the extremely rich), 32 140 nr. 290 (letter of March 2026 on a 2% minimum tax for very wealthy persons). Commissions: the Studiecommissie Belastingstelsel (2019/2020, Bouwstenen) and the IBO Vermogensverdeling (2022). Internet consultations on tax bills run at `internetconsultatie.nl`; none specific to a wealth tax was found.

## 2. Debates and votes

- **Handelingen** (verbatim plenary reports) are `h-tk-<year>-<n>-<item>` and `h-ek-...` on officielebekendmakingen.nl; they appear within about a week as corrected texts. Speaker labels look like `De heer Dijk (SP):`, `Mevrouw Marijnissen (SP):`. HTML, searchable, no PDF needed.
- **Committee reports** (verslag commissiedebat / wetgevingsoverleg / algemeen overleg) are Kamerstukken, `kst-<dossier>-<n>`; they appear several weeks after the debate, so the newest debates are missing. Speaker labels as in Handelingen.
- **Written questions** (Kamervragen) are `kv-tk-...` (question) and `ah-tk-...` (Aanhangsel Handelingen, with answer). Questions on the wealth tax mostly cite news about box 3.
- **Roll calls:** only a few. A named vote is announced in Handelingen "Stemmingen" and lists members under voor/tegen. Example: 23 April 2024, motion Dijk/Maatoug on an EU exit tax (`h-tk-20232024-68-33`), 72 names; its rows were added in R003 and removed in the R006 review because the motion only asks to develop an exit tax, so it is not wealth-tax evidence. Check `StemmingsSoort` in the open data for every other motion; in R030 every wealth-tax motion and amendment checked (about 30) was a show-of-hands vote.
- **Block and package votes:** the Belastingplan is voted as a whole; amendments (amendementen) and motions are voted separately. Amendments to introduce a millionaire tax in the Belastingplan are article-specific; the final bill vote is not.
- **Where the Belastingplan debates sit:** the Tweede Kamer holds a wetgevingsoverleg (WGO) in October and a plenary debate in November (e.g. `h-tk-20222023-19-25`, `-20-10` for 2022); the Eerste Kamer holds a plenary debate in December. The Algemene Politieke Beschouwingen and Algemene Financiële Beschouwingen (September/October in the Tweede Kamer, November in the Eerste Kamer) are where party leaders mention the tax most.

## 3. Members, parties, seats

- Tweede Kamer: `Persoon` (OData) and `https://www.tweedekamer.nl/kamerleden_en_commissies/alle_kamerleden`; former members have `Functie` "Oud Kamerlid". `python skill/scripts/seats.py data/nl` reads the open data.
- Eerste Kamer: `https://www.eerstekamer.nl/alle_leden` (initials and surname, group; for example "R.O. Martens MSc (PRO)"); person pages `/persoon/<slug>`; past members `/oud_leden`. The first name is often not printed.
- The Tweede Kamer fractie names change (GroenLinks and PvdA formed GroenLinks-PvdA in 2023, shown as "PRO" in 2026 documents); record the party name at the date of the act.
- Wikidata covers Tweede Kamer members well; verify by label.

## 4. Other official records

- **Eerste Kamer** search at `eerstekamer.nl/zoeken?q=` is a **keyword (trefwoord) index only**: a search for `miljonairsbelasting` returns "no results". Use the SRU query with the Senate as creator instead. The Senate has no wealth-tax bill, but Senate groups speak in the Belastingplan and Algemene Financiële Beschouwingen debates (SP's Van Apeldoorn most).
- **Raad van State, CPB, Algemene Rekenkamer** reports: not searched for positions; CPB scenarios of a millionaire tax are cited in motion explanations.
- **Courts:** Hoge Raad 24 December 2021 (box 3) is about the deemed return; not a wealth-tax position.
- **European Parliament:** Dutch MEPs (R003) via the EP record; not part of this guide.
- **Provincial states and municipal councils:** raadsinformatie runs on iBabs, Notubiz and others; `https://openraadsinformatie.nl/` aggregates many municipalities (API not queried in R030). Two web searches (municipal and provincial motions on a millionaire tax) returned only national hits. Local branches of SP, GroenLinks and PvdA run "miljonairsbelasting" campaigns (R004 leads); a council motion would be the evidence, not the campaign.
- **Belastingdienst / Rijksoverheid consultations:** no consultation on a wealth tax exists (the box 3 consultations are about the deemed-return reform).

## 5. Access notes

- officielebekendmakingen.nl HTML: reliable with a normal browser User-Agent. SRU: reliable, XML, no key.
- `gegevensmagazijn.tweedekamer.nl` OData: reliable; page size 250, follow `@odata.nextLink`.
- `tweedekamer.nl` search and `eerstekamer.nl` pages work with a browser User-Agent but are JavaScript-heavy; prefer the open data and SRU.
- `repository.overheid.nl/frbr/sru/` (404), Wikidata API after many calls in a row (429): wait.
- Tools: `scripts/gazette_scan.py` is for PDF gazettes; Dutch Handelingen are HTML, so a short script over SRU results plus the passage reader is enough (R030 cached 460 documents and printed the passages with a speaker label).

## 6. Coverage log

| Date | Run | Documents read | Result | Not read / open |
|---|---|---|---|---|
| 2026-11-08 | R030 | 244 documents tracked in documents.csv: 31 read in full (motions and amendments with signatories and vote type, the 30-member debate, the 2024 roll call); 130 partial (Handelingen and committee reports in which a strong term occurs: keyword passages with speaker label reviewed, not line by line); 83 skimmed (written questions, letters, agendas: hits only); bill 36 173 partial | 12 evidence rows, 5 new actors; every wealth-tax motion checked was a show-of-hands vote except the 23 April 2024 exit-tax named vote (rows removed in R006) | Handelingen/committee reports that use only box 3 words; debates after about September 2026; Eerste Kamer committee reports; provinces; municipalities; documents before 2006 |

Never write "no roll call" or "no statements" for the Netherlands without this table: the 23 April 2024 exit-tax vote is the only named vote found, and it is outside the definition; every motion in `documents.csv` with a fractie-only vote says so.

## 7. Known gaps and next steps

1. Re-run the SRU queries every quarter for new Handelingen and committee reports (the newest are missing from the archive for weeks).
2. Open Raadsinformatie full-text search for `miljonairsbelasting` and `vermogensbelasting` across municipalities; provincial states of the 12 provinces (they elect the Eerste Kamer in 2027).
3. Read the line-by-line text of the 30-member debate of 4 April 2024 and of the Wet werkelijk rendement box 3 debates in 2026 (Tweede Kamer and Eerste Kamer 30 June 2026) for supporters who speak for a simple wealth tax as the alternative.
4. Earlier SP, GroenLinks and PvdA sponsors of amendments before 2014 (keyword hits in 2006-2013 were only checked in titles and hits).
