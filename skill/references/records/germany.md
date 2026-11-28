# Germany: official wealth-tax records

## Bundestag bills and motions

- The [Bundestag open-data page](https://www.bundestag.de/services/opendata) links the DIP API, XML and JSON parliamentary documents, member biographies and roll-call spreadsheets. Search in German for `Vermögensteuer`, `Vermögenssteuer`, `Vermögensabgabe`, `Millionärsteuer` and `Milliardärsteuer`; review context because inheritance and property tax alone do not qualify.
- Parliamentary papers are available as text PDFs at `https://dserver.bundestag.de/btd/<term>/<three-digit-block>/<term><four-digit-number>.pdf`; for example [19/94](https://dserver.bundestag.de/btd/19/000/1900094.pdf), [20/4307](https://dserver.bundestag.de/btd/20/043/2004307.pdf), and [21/4029](https://dserver.bundestag.de/btd/21/040/2104029.pdf). Their first page names individual sponsors and the group; demands are in section II. A group motion does not automatically establish support of unnamed members.

## Debates and votes

- [2022 official debate summary](https://www.bundestag.de/dokumente/textarchiv/2022/kw45-de-vermoegensabgabe-920034): motion 20/4307 rejected 36–649; [2026 summary](https://www.bundestag.de/dokumente/textarchiv/2026/kw10-de-vermoegensteuer-1150522) describes the first reading and committee referral of 21/4029. These are summaries, not complete verbatim records.
- The Bundestag [2013 roll call](https://www.bundestag.de/resource/blob/194544/20130627_4_vermoegensabgabe.pdf) lists each member by party and vote column: bill 17/10770 rejected, 66 yes, 318 no and 195 abstentions. PDF text extraction can lose column alignment: check the original layout. The open-data page links original XML, JSON and spreadsheet material; speaker transcripts and votes should be checked against the official records.

## Members and state records

- The Bundestag open-data page links its biographical register (XML) including historic members. The [Thuringian members list](https://www.thueringer-landtag.de/abgeordnete/abgeordnete-fraktionen-sitzordnung/) provides party and member pages; [Brandenburg](https://www.landtag.brandenburg.de/de/abgeordnete_im_ueberblick/25777) provides the current list and biographies.
- Brandenburg's [2021 decision record](https://www.landtag.brandenburg.de/de/meldungen/der_44._sitzung_des_landtages_brandenburg_am_donnerstag_dem_20._mai_2021/13923) reports rejection of 7/3405. The [2026 session metadata](https://www.parlamentsdokumentation.brandenburg.de/portal/sitzung.tt.html?search=NODE%3D651873%2A&wp=8) links the agenda, documents and [decision PDF](https://www.parlamentsdokumentation.brandenburg.de/starweb/LBB/ELVIS/parladoku/w8/beschlpr/protokolle/37.pdf); TOP 16 records rejection of 8/3319 and lists speakers. Decisions alone do not establish a named vote.
- [Thuringian October agenda](https://www.thueringer-landtag.de/uploads/tx_tltcalendar/invitations/Pe8056-6.pdf) references motion 8/3730 and committee report 8/4476. The group source linked to Parldok, which returned 403 here; the provisional 25 June protocol returned 410. Recheck the full final documents before interpreting any compromise.

## Coverage and gaps

| Date | Run | Documents checked | Findings and limits |
|---|---|---|---|
| 2026-11-14 | R046–R047 | Brandenburg 7/3405 and 8/3319; Hande speech extract | Group motions and statements recorded; 2026 outcome was not then known. |
| 2026-11-14 | R048 | Bundestag 19/94 and 20/4307; Brandenburg BePr 7/44 and BePr 8/37; 2013 roll-call result | Both Brandenburg motions rejected; 2022 Bundestag motion rejected. Decision items read, not complete debate transcripts; 2013 named vote requires layout-aware review. |

`data/germany/documents.csv` contains additional earlier readings; do not interpret absent documents as a negative search result. Continue the unread or partial core records, remaining Bundestag terms, state legislatures and Bundesrat; check 21/4029 and 21/8267 final outcomes at DIP. No municipality-wide sweep was conducted.
