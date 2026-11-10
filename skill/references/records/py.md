# Paraguay: where the official record is and how to read it

## 1. Bills, motions and proposals
- **Register of bills:** Sistema de Información Legislativa (SILpy) at `silpy.congreso.gov.py` and the ODS monitoring portal `ods.congreso.gov.py`.
- **Search terms:** `"tasa extraordinaria a las grandes fortunas"`, `"tasa covid"`, `"impuesto a las grandes fortunas"`, `"impuesto al patrimonio"`, `"emergencia educativa"`.
- **Sponsors:** The bill docket (*expediente*) names the initiating senators and accompanying civil society organisations (e.g. Expediente 123524: Hugo Richer, Pedro Santa Cruz, Víctor Ríos, OTEP-SN).

## 2. Debates and votes
- **Plenary and committee records:** *Diario de Sesiones* of the Cámara de Senadores and Cámara de Diputados, available via `senado.gov.py` and `diputados.gov.py`.
- **Roll calls:** The vote on 30 June 2021 in the Cámara de Diputados was by show of hands/majority vote (*rechazo por mayoría/casi unanimidad*); individual electronic roll-call logs are published in the session minutes (*Actas de Sesión*).
- **Proposals rejected:** Both the 2020 Tasa Covid and the 2021 Emergency Education wealth tax bill were rejected and sent to the archive (*al archivo*).

## 3. Members, parties, seats
- **Chamber rosters:**
  - Senado (45 seats): official roster on `senado.gov.py`.
  - Diputados (80 seats): official roster on `diputados.gov.py`.
- Wikidata covers almost all senators and deputies with position held (P39).

## 4. Other official records
- **Contraloría General de la República:** `contraloria.gov.py` (sworn declarations of assets and liabilities of public officials).
- **Dirección Nacional de Ingresos Tributarios (DNIT):** `dnit.gov.py` (official tax statistics, statements opposing wealth tax proposals).

## 5. Access notes
- `ods.congreso.gov.py` is a Vue SPA; `senado.gov.py` restructured its historical news URLs in 2023, but many are preserved on Wayback Machine or reported verbatim in national press (`ultimahora.com`, `abc.com.py`, `lanacion.com.py`).

## 6. Coverage log

| Date | Run | Documents read (title, number, date) | Result (rows added, votes found) | Not read / open |
|---|---|---|---|---|
| 2026-11-10 | R001 | Expediente 123524 (Ley de Emergencia Educativa y tasa a las grandes fortunas, 2021-05-12) | 3 bill sponsors (Richer, Santa Cruz, Ríos), union leaders (Ávalos) | Committee transcripts |
| 2026-11-10 | R001 | Proyecto Tasa Covid (Frente Guasu, 2020-04-20) | 4 senator sponsors (Martínez, Filizzola, Querey, Pereira) | Exact bill text PDF |
| 2026-11-10 | R001 | Sesión extraordinaria Cámara de Diputados (2021-06-30, rechazo impuesto a la riqueza) | 1 speech defending tax (Kattya González); documented rejection | Full per-member voting roll call |

## 7. Known gaps and next steps
- Obtain full PDF transcript of the 30 June 2021 Diputados debate to identify if any other deputy besides Kattya González voted or spoke in favour.
- Check municipal records of Asunción and major Central cities for local declarations.
