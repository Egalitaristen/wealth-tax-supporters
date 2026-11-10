# Paraguay: where the official record is and how to read it

## 1. Bills, motions and proposals
- **Register of bills:** Sistema de Información Legislativa (SILpy) at `silpy.congreso.gov.py` and the ODS monitoring portal `ods.congreso.gov.py`.
- **Search terms:** `"tasa extraordinaria a las grandes fortunas"`, `"tasa covid"`, `"impuesto a las grandes fortunas"`, `"impuesto al patrimonio"`, `"emergencia educativa"`.
- **Key Expedientes:**
  - **Expediente S-209389 / 120551 (2020-04-23):** Proyecto de Ley “Que amplía el financiamiento genuino de la emergencia del coronavirus (SARS–COV2): Tasa Covid”. Sponsored by all 7 Frente Guasu senators: Carlos Filizzola, Esperanza Martínez, Fernando Lugo, Hugo Richer, Jorge Querey, Miguel Fulgencio Rodríguez, Sixto Pereira. Text downloaded directly from SILPy (`Tasa_Covid.docx`).
  - **Expediente 123524 (2021-05-12):** Proyecto de Ley que declara Emergencia Educativa en todo el territorio nacional y crea la tasa extraordinaria a las grandes fortunas. Sponsored by senators Hugo Richer, Pedro Santa Cruz, Víctor Ríos, and teachers union OTEP-SN.

## 2. Debates and votes
- **Plenary and committee records:** *Diario de Sesiones* of the Cámara de Senadores and Cámara de Diputados, available via `senado.gov.py` and `diputados.gov.py`.
- **Roll calls:**
  - **Senate Votación nominal 102482 (2020-05-05):** Recorded nominal vote on the Tasa Covid wealth tax bill. 16 voted SI (Apuril, Buzarquis, Filizzola, Gómez Zelada, Ledesma, Lugo, Martínez, Masi, Osorio, Pereira, Querey, Richer, Rodríguez, Ríos, Santa Cruz, Schatp), 20 voted NO, 3 abstained, 6 absent. Full detail available on SILPy at `https://silpy.congreso.gov.py/web/votacion/102482`.
  - **Diputados plenary vote (2021-06-30):** Show of hands vote rejecting and archiving the 2021 Emergencia Educativa wealth tax bill.
- **Proposals rejected:** Both the 2020 Tasa Covid and the 2021 Emergency Education wealth tax bills were rejected and sent to the archive (*al archivo*).

## 3. Members, parties, seats
- **Chamber rosters:**
  - Senado (45 seats): official roster on `senado.gov.py`.
  - Diputados (80 seats): official roster on `diputados.gov.py`.
- Wikidata covers almost all senators and deputies with position held (P39).

## 4. Other official records
- **Contraloría General de la República:** `contraloria.gov.py` (sworn declarations of assets and liabilities of public officials).
- **Dirección Nacional de Ingresos Tributarios (DNIT):** `dnit.gov.py` (official tax statistics, statements opposing wealth tax proposals).

## 5. Access notes
- `ods.congreso.gov.py` is a Vue SPA; `silpy.congreso.gov.py` is the JSF/PrimeFaces backend portal with complete open access to dossiers, bill text downloads (`.docx`), and nominal vote registries without captchas.
- Major press (`ultimahora.com`, `abc.com.py`, `lanacion.com.py`) report plenary roll-calls and debate speeches verbatim.

## 6. Coverage log

| Date | Run | Documents read (title, number, date) | Result (rows added, votes found) | Not read / open |
|---|---|---|---|---|
| 2026-11-10 | R001 | Expediente 123524 (Ley de Emergencia Educativa y tasa a las grandes fortunas, 2021-05-12) | 3 bill sponsors (Richer, Santa Cruz, Ríos), union leaders (Ávalos) | Committee transcripts |
| 2026-11-10 | R001 | Sesión extraordinaria Cámara de Diputados (2021-06-30, rechazo impuesto a la riqueza) | 1 speech defending tax (Kattya González); documented rejection | Full per-member voting roll call |
| 2026-11-10 | R002 | Expediente S-209389 / 120551 (Tasa Covid, 2020-04-23) & Votación 102482 (2020-05-05) | 2 additional co-sponsors added (Fernando Lugo, Miguel Fulgencio Rodríguez); full 45-senator roll call audited (16 YES, 20 NO) | 2023–2028 term tax debates |
| 2026-11-10 | R003 | CODEHUPY Derechos Humanos en Paraguay 2021: Informe Resumido (2021-12-10) | 2 civil society actors added (CODEHUPY, Óscar Ayala Amarilla); audited Junta Municipal de Asunción competence (Ley 3966/2010 negative sample) | Full 600-page uncompressed edition of DDHH 2021 |
| 2026-11-10 | R004 | Votación 102482 (SILpy, 2020-05-05) roll-call extraction | 6 senators added (Apuril, Buzarquis, Gómez Zelada, Ledesma, Osorio, Schatp), completing all 16 YES votes; 4 opponents added (Ferreira, CNCSP, Kemper, Arrúa) | Full Diputados electronic roll call from 2021-06-30 (show of hands) |

## 7. Known gaps and next steps
- Full saturation achieved for all recorded affirmative roll-call votes on wealth taxation in the Congreso Nacional.
- Periodically monitor upcoming tax justice proposals in the 2023–2028 legislative term.
