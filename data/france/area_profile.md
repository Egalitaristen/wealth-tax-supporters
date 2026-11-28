# Area profile — France

First written 2026-10-20 (run R001). Seed pass; national level.

## 1. Scope
France (unitary). Depth: Seed. Languages: French, English. Register: regions and départements (the lowest tier mapped; communes not loaded).

## 2. History and live proposals
- ISF abolished and replaced by the real-estate IFI on 1 Jan 2018. Left bills since 2022 (PS 648, Ecologists 359, LFI 2563, Communist 2193/246).
- "Taxe Zucman": 2% floor on net wealth above EUR 100m. Adopted by the Assemblée 20 Feb 2025 (116-39, scrutin 881); rejected by the Sénat 12 June 2025 (129-188, scrutin 322); rejected in the 2026 budget on 31 Oct 2025 (172-228, scrutin 3300).
- Polls: Ifop for the PS (Sept 2025) 86% in favour; Elabe (Sept 2025) 74%.

## 3. Sources
Assemblée open data (Scrutins.json, AMO30 actors, Dossiers législatifs), assemblee-nationale.fr/dyn/17/scrutins/N, Sénat scrutin pages and ODSEN_GENERAL, Wikidata (P4123, P1808).

## 4. Map
Commune, département and region outlines from Etalab contours administratifs 2025 (1000 m), INSEE codes: metropolitan France under the Licence Ouverte 2.0.

**Overseas (28 November 2026, issue #222).** The five overseas departments and six inhabited collectivities (975, 977, 978, 986, 987, 988) are drawn as insets west of the metropolitan map, from the 2025 files of the same dataset, which data.gouv.fr publishes under the ODbL; the collectivities' communes come from OpenStreetMap and the French Polynesian and New Caledonian authorities. Each collectivity is a region-level unit (code ISO 3166-2) with its communes below it (Wallis-et-Futuna: three circonscriptions), all `pending`: none has been swept. The French Southern and Antarctic Lands (984) and Clipperton (989) have no permanent population and are not units. Fangatau and Pukapuka are too small to survive rounding and are drawn as small diamonds. Rebuild: `scripts/add_territory_insets.py fr`.

## 10. Plan for the next runs (by expected yield)
1. Remaining thin actor types: `funder`, `media_outlet`, `business_leader`, and `wealthy_individual`. (R009: 31 *premiers signataires* of `H0011` + Bruno Palier, Emmanuel Saez, Marine Tondelier. R010: 6 economists. R011: 12 Sep 2024 Sherpa / Libération open letter. R012: UNSA, FSU, Institut Rousseau, Institut La Boétie. R013: AES coalition unions/NGOs. R014: Pascal Demurger [MAIF / Impact France] + 6 NGOs/faith orgs from the 13 Jun 2026 G7 Evian appeal. R015: 14 `union_official`s, `Jeunesse Ouvrière Chrétienne (JOC)`, `GreenFaith`, 8 NGOs/unions from the 16 Sep 2024 open letter, and 48 mayors from the 10 Jun 2025 *Le Nouvel Observateur* open letter. R016: 6 `academic`s, `journalist` David Dufresne, `business_leader` Bertrand Faivre, 3 `cultural_figure`s, 4 `campaigner`s, Noël Mamère, and Grand Est regional councillor Lou Noirclère.)
2. `H0013` MEP petition list (March 2023; `callforfairtaxation.com` no longer resolves and CDX timed out — `gabriel-zucman.eu/taxation-mondiale/` lists the 10 *premiers signataires*, including Aurore Lalucq and Lucas Chancel already in `data/france`).
3. PLF 2027 amendments `I-471`, `I-38`, `I-2566` harvested in R009 (4 new deputies, 138 fresh 2026 `motion_signature` rows); check Sénat `I-1640 rectifié bis` co-signers if published on `senat.fr`.
4. Regional & local: Jœuf (30 Oct 2025), Strasbourg (29 Sep 2025), Conseil départemental de Loire-Atlantique (13 Oct 2025), Bourgogne-Franche-Comté regional council (16 Oct 2025), Vénissieux (8 Dec 2025), plus local councillors in Villeurbanne and Saint-Pierre-des-Corps, and 48 mayors (Lyon, Strasbourg, Nantes, Lille, Bordeaux, Grenoble, Rouen, Besançon, Tours, Poitiers, Clermont-Ferrand, Villeurbanne, etc., 10 Jun 2025); no official council `vœu` found on `paris.fr`, `lyon.fr`, `marseille.fr`, or `montreuil.fr`.
5. Opinion columns and editorials.

## Resources pass (1 November 2026)

Listed on the Resources page after reading each text: the Assemblée nationale bills no. 246, 2193, 359, 648 and 2563 (first pages, articles and exposés des motifs), the commission des finances report no. 930 and the Senate finance committee's summary of 4 June 2025; and, in `meta.json`, the Elabe/BFMTV poll of 4 to 5 November 2025 (read from the PDF; the question asks whether the deputies were wrong to reject the tax) and the Ifop release for the Parti socialiste, now linked to Ifop's own page. The status of the 16th-legislature bills is inferred (see the PR): their pages show no stage after referral and the legislature ended with the dissolution of June 2024.

Leads not yet listed:
- Conseil d'analyse économique, Focus no. 118 (July 2025) on capital taxation and tax exile: studies the 2013 and 2017 reforms (wealth-tax and flat-tax changes) and does not cost a net wealth tax, so left out; read it in full before deciding.
- Conseil des prélèvements obligatoires and Cour des comptes reports on the taxation of wealth: whole-reform reports; no text on a net wealth tax read.
- Conseil constitutionnel: a search for a decision on the 2025/2026 Zucman amendments found none (the amendments were rejected in committee on 20 October and in the chamber on 31 October 2025, per press reports not read in full), and the Conseil d'État opinion quoted in the debate was not read.
- Other Ifop, Ipsos, Odoxa and Harris polls on the Zucman tax: not found with a question wording and fieldwork dates.

## Taxes in force that are outside the definition
- **Impôt sur la fortune immobilière (IFI):** in force since 2018, it taxes real estate only (net property above EUR 1.3 million), so it is a property tax outside the definition. A call to bring back a tax on all net wealth (the old ISF) is inside it. `[verify: stated from general knowledge, not read from the law for this note]`

## Review corrections (2026-11-07)

- Regraded E00762 (Dossus), E00763 (Kanner) and E00764 (Gontard) from A to B: the cited sentences show a group initiative, the Prime Minister's stance and a general tax-justice line, not their own tax design; the articles around them show they back the Zucman tax.
