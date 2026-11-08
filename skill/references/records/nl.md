# Netherlands: where the official record is and how to read it

Written in run R030 (2026-11-08) by reading the Tweede Kamer and Eerste Kamer record for wealth-tax terms from 2006 to November 2026. Every URL and method below was tested on that date; failures are stated.

Key fact for the Netherlands: **almost every vote on a wealth-tax motion is by show of hands** ("Met handopsteken"). The open data and Handelingen record the vote per fractie (party group), never per member. Individual evidence is: the signatories of a motion or amendment (open data and the printed document), speeches in Handelingen and committee reports, the rare named vote (hoofdelijke stemming), and, by project decision (R030b), the **fraction vote applied to the fraction's members** on a motion that is itself about an actual wealth tax (section 2b).

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

## 2b. Fraction votes applied to the fraction's members (R030b)

Project decision (relayed 2026-11-08): when a fraction voted *voor* on a motion or amendment that is **specifically about an actual wealth tax** (an annual or one-off net-wealth levy, introduced or called for; not a shift of tax from labour to capital, a solidarity levy on income or windfalls, a box 3 deemed-return change, an exit tax, or a request to study), every member of that fraction seated on the vote date gets a grade A `vote` row. This departs from the general rule in `definition-and-grades.md` (quote the member's own entry in a per-member list), so every such row says so in `grading_note` ("Fraction vote applied to the fraction's members") and the quote is the fraction line printed in the vote result, not a personal entry. A member who voted differently or was absent is left out; on a show of hands neither is recorded, so only absence can be read (below).

How it is done (repeatable):
1. **Vote result.** Open data: `Document?$filter=DocumentNummer eq '2019D39162'&$expand=Zaak($expand=Besluit($expand=Stemming))`. The Besluit with `StemmingsSoort` `Met handopsteken` has one `Stemming` per fractie (`ActorFractie`, `Soort` Voor/Tegen, `FractieGrootte`, `Fractie_Id`). `Besluit(<id>)?$expand=Agendapunt($expand=Activiteit)` gives the vote date (the vote is some days after the motion is filed; a vote after midnight is dated by the sitting).
2. **Printed fraction line (the quote).** The Handelingen item "Stemmingen moties ..." (find it with SRU `w.publicatienaam=Handelingen and dt.date=<vote date>`). After "In stemming komt de motie-X (dossier, nr. N)" the chair says "Ik constateer dat de (aanwezige) leden van de fracties van ... voor deze motie hebben gestemd en de leden van de overige fracties ertegen". Quote that clause. Older items say "aanwezige leden" (present members).
3. **Seat list.** `FractieZetelPersoon?$filter=FractieZetel/Fractie_Id eq <id> and Van le <date>&$expand=Persoon`; keep rows with `Van <= date <= TotEnMet` (or `TotEnMet` empty), comparing the **local calendar date**: `TotEnMet` is the last day in office at 00:00 local time, so a time-of-day filter drops the members who leave that day. Check the count against `FractieGrootte`: for all seven votes applied here they matched exactly. A member is listed once per seat, so de-duplicate on `Persoon_Id` (a fractievoorzitter appears twice).
4. **Absence.** Open data has no attendance. The first Handelingen item of the sitting (`h-tk-<year>-<n>-1`, "Presentie en opening") prints "Aanwezig zijn N leden der Kamer, te weten: ...". Match each seated member by surname (with first name for duplicates) and drop those not listed (2019-10-08: seven PVV/SP/GroenLinks members; the four other votes with absentees lost one each). This is a floor: someone present at the opening may have left before the vote, and the record cannot show it.
5. **Party and dates.** Record the fraction at the vote date; GroenLinks and PvdA members are filed under `GroenLinks-PvdA` with the original fraction named in `notes`; Group Kuzu/Öztürk under `DENK`. Death dates are in `Persoon.Overlijdensdatum`: a deceased member goes to `exclusions.csv` (Sazias, X0019).

**Applied (seven votes, 268 rows, 117 members):** amendment-Bashir 13 Nov 2014 (SP, GroenLinks); motion-Roemer 17 Sep 2015 (SP, Group Kuzu/Öztürk, GroenLinks); motion-Leijten 29 May 2018 (SP, PvdA, GroenLinks, DENK); motion-Alkaya c.s. 8 Oct 2019 (SP, PvdA, GroenLinks, vKA, PvdD, DENK, 50PLUS, PVV); motion-Dijk 14 Feb 2024 (SP, GL-PvdA, PvdD, DENK, Volt, D66); motion-Dijk/Maatoug 9 Apr 2024 (same list); motion-Dijk 19 Sep 2024 (SP, GL-PvdA, PvdD, DENK).

**Not applied, awaiting a decision (documents.csv `gaps` says so):** motion Van den Hul/Asscher 6 Mar 2019 (31 288 nr. 706, "progressievere vermogensbelasting", the box 3 label; PvdD, GroenLinks, PVV, SP, PvdA, DENK for); the two adopted motions of 25 Oct 2023 (36 418 nr. 74 Alkaya and nr. 76 Van der Lee) and motion 25 087 nr. 330 of 4 Apr 2024, which ask the government to lobby internationally for a global billionaire tax / progress on it and passed with 13 fractions including VVD, CDA and PVV (about 150 members). Not wealth-tax motions by the test above: nr. 331 (exit tax), 21 501-07 nr. 1144 and 1676, 36 471 nr. 82 and 36 602 nr. 115, and all study motions. Motions for 2006-2013: the Document list for `Motie`/`Amendement` before 2014 holds none on a net-wealth levy (only the 2011 Plasterk income levy, the 2011 Bashir capital gains tax and box 3 motions).

**Eerste Kamer:** the Senate prints the same clause ("Voor stemmen de leden van de fracties van ..."), but none of the 80 Handelingen with a strong term (2010 to June 2026) contains a motion for a wealth tax put to a vote: the Senate motions on the topic are study or priority requests (Van Rooijen c.s., December 2024), box 3 motions, or a motion Martens GroenLinks-PvdA voted against on 12 Dec 2023 (stemverklaring: the motion was too vague, the fraction wants a wealth tax). Seat lists for the Senate are not in the open data; use `eerstekamer.nl/oud_leden` with dates if a motion turns up.

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
| 2026-11-08 | R030b | Follow-up to R030: 7 vote items in Handelingen (the printed fraction line on each wealth-tax motion or amendment) and the 7 opening attendance lists; Tweede Kamer open data seat lists on each vote date; 80 Eerste Kamer Handelingen with a strong term scanned for motions | 268 grade A fraction-vote rows for 117 members (85 new actors), 1 exclusion (deceased); Eerste Kamer: no qualifying motion | Four motions with an ambiguous or lobbying text not applied (section 2b); absence read from the opening list only; Eerste Kamer seat lists |

Never write "no roll call" or "no statements" for the Netherlands without this table: the 23 April 2024 exit-tax vote is the only named vote found, and it is outside the definition; every motion in `documents.csv` with a fractie-only vote says so. Fraction votes on seven wealth-tax motions are applied to the fraction members (section 2b).

## 7. Known gaps and next steps

1. Re-run the SRU queries every quarter for new Handelingen and committee reports (the newest are missing from the archive for weeks).
2. Open Raadsinformatie full-text search for `miljonairsbelasting` and `vermogensbelasting` across municipalities; provincial states of the 12 provinces (they elect the Eerste Kamer in 2027).
3. Read the line-by-line text of the 30-member debate of 4 April 2024 and of the Wet werkelijk rendement box 3 debates in 2026 (Tweede Kamer and Eerste Kamer 30 June 2026) for supporters who speak for a simple wealth tax as the alternative.
4. Earlier SP, GroenLinks and PvdA sponsors of amendments before 2014 (keyword hits in 2006-2013 were only checked in titles and hits).
