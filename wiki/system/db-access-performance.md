---
title: "DB — Accesso, performance e minimizzazione delle query"
type: build
tags:
  - build
  - infrastructure
  - software
created: 2026-06-04
updated: 2026-06-04
status: active
priority: high
area: software
related:
  - "[[system/modules/data-layer]]"
  - "[[system/modules/agents]]"
  - "[[system/modules/execution]]"
  - "[[system/modules/quant-backtesting]]"
  - "[[system/state-schemas]]"
  - "[[system/decision-log]]"
---

# DB — Accesso, performance e minimizzazione delle query

> Approfondimento sul **come** il DB centrale viene letto/scritto e su come renderlo veloce e poco interrogato. Il *cosa* contiene (aree logiche, extraction, retention) sta in [[system/modules/data-layer]]; qui sta l'ingegneria di accesso.

---

## 1. Stato attuale (sintesi)

Il DB è **deciso a livello di design, non ancora implementato** (fase pre-sviluppo). Punti fermi:

- **Motore**: PostgreSQL (prod) / SQLite (dev), schema versionato con Alembic.
- **DB-first**: unico punto di verità; tutti scrivono lì, gli agenti leggono **solo i campi che servono** (anti context-rot).
- **4 aree logiche** / 5 tabelle core: `portfolio_state`, `market_data`, `charter` (Statuto), `logs`+`trades`, `module_outputs`.
- **Forma mista**: time-series (prevalente) + oggetti (rendicontazione) + documentale JSONB (state annidati).
- **Doppia data** (`publication_date` / `reference_date`) anti look-ahead-bias.
- **Queue + check-presenza** sugli extractor; indicatori **pre-calcolati**, mai on-the-fly.

---

## 2. Quando viene interpellato

### In scrittura
| Chi | Quando | Tabella |
|-----|--------|---------|
| **Extractors set** | quando il check-presenza fallisce → la coda scrive i grezzi | `market_data` |
| **`mantainer`** | trasforma `transactions` → accounting di portafoglio | `portfolio_state` |
| **Execution / Trade** | a ogni ordine eseguito | `trades` / `transactions` |
| **LangGraph checkpointer** | a ogni step del grafo salva lo `state` | checkpoint store |
| **Backtesting validatore** | scrive i risultati di ri-validazione delle soglie | `module_outputs` / report |

### In lettura
| Chi | Cosa legge |
|-----|-----------|
| **Agenti del desk** | solo i campi necessari per il loro task |
| **Backtesting** | `market_data` storico (serie temporali) |
| **Execution** | `portfolio_state` (per sizing) + `charter` (Statuto) |
| **Calendar / Alert** | eventi schedulati, prezzo vs target |
| **PM** | snapshot di portafoglio + context all'inizio del ciclo |

---

## 3. Come è gestito e da chi

- **Owner**: modulo [[system/modules/data-layer]] (🛠 Luca).
- **Pattern a layer** (ispirato a [[prior-art/libraries/cvx-portfolio-optimizer]]): `models → repositories → services → routers`. Gli agenti **non** scrivono SQL: passano dai service/repository, che incapsulano le query. Un punto solo da ottimizzare.
- **Un file gateway per modulo** (decisione 2026-05-19): l'accesso al DB è centralizzato, non sparso.

---

## 4. Velocizzare lettura e scrittura

### Scrittura
- **Batch insert / `COPY`**: gli extractor scrivono a blocchi, non riga per riga.
- **Connection pooling** (pool SQLAlchemy / pgbouncer): niente handshake a ogni operazione.
- **Partitioning temporale** (o hypertable Timescale): le scritture cadono sempre sull'ultima partizione → indici piccoli e caldi.
- **Scritture asincrone / fire-and-forget** per i log non critici (la pipeline non aspetta il commit del log).

### Lettura
- **Indici mirati**: `(ticker, reference_date)` per i dati di mercato; PK/FK per gli oggetti.
- **BRIN index** sulle colonne data delle serie temporali: leggerissimo e velocissimo su dati ordinati nel tempo (ideale per `market_data`).
- **GIN index** sui campi-chiave dentro le colonne **JSONB** (filtri sugli state senza scartabellare il blob).
- **Materialized views** per rendicontazione e metriche di performance: calcolate una volta, lette molte; refresh su trigger del `mantainer`.
- **Indicatori pre-calcolati** salvati nel DB (già nel design): nessun calcolo a ogni lettura.

---

## 5. Interrogare il DB il meno possibile

Principio: **una lettura per ciclo, non N**. Leve (dalla più al meno già decisa):

1. **Check-presenza prima di estrarre** *(già deciso)*: se il dato è nel DB, zero richieste esterne e zero accodamenti inutili.
2. **Snapshot di ciclo in memoria** *(= tool di iniezione del portafoglio)*: all'avvio del ciclo del PM si carica **una volta** `portfolio_state` + context, lo si mette nello `state` del grafo LangGraph e **tutti i nodi leggono da lì**, non dal DB. Vedi [[system/modules/agents]].
3. **Periodical synthesis** *(già prevista)*: stato sintetico precompilato → gli agenti non ricostruiscono il quadro dal DB ogni volta.
4. **Read-through cache** per i dati "caldi" letti spessissimo e che cambiano poco: prezzo corrente, **Statuto/`charter`** (cambia raramente). In-process per l'MVP, eventualmente **Redis** se il carico cresce → *decisione aperta*.
5. **Evitare N+1**: una query che porta tutto il necessario per tutti i ticker del ciclo, non una query per ticker.
6. **Compute-once-store**: ogni metrica derivata (P/E, ratio, indicatori) si calcola una volta dai grezzi e si persiste; le letture successive sono semplici `SELECT`.

---

## 6. Che forma avrebbe il DB

**Deciso (2026-06-04): PostgreSQL + estensione TimescaleDB** — un solo motore che copre i tre regimi di dati, niente secondo database.

| Regime | Contenuto | Forma fisica |
|--------|-----------|--------------|
| **Time-series** | `market_data`, prezzi, macro, tassi | **Hypertable** Timescale (compressione + query temporali rapide) |
| **Relazionale / oggetti** | `portfolio_state`, `trades`, `charter` | Tabelle classiche (riga = posizione/oggetto) |
| **Documentale** | `states`, `module_outputs`, report | Colonna **JSONB** con campi-chiave estratti come colonne indicizzate (GIN) |
| **Checkpoint grafo** | stato LangGraph per recovery | SQLite (dev) / tabella Postgres (prod) |

Perché Timescale: è il "matrimonio" naturale tra l'orientamento *«principalmente time-series, ma con oggetti e JSON internamente»* (decisione 2026-06-02) e Postgres già scelto — resta tutto relazionale + JSONB nello stesso posto, senza un DB documentale separato (coerente con l'orientamento JSONB della [[system/state-schemas]]).

---

## Decisioni chiuse di questa pagina
- ✅ **Motore = PostgreSQL + TimescaleDB** (2026-06-04): hypertable time-series + relazionale/oggetti + JSONB in un solo motore.
- ✅ **Cache = in-process per l'MVP** (2026-06-04): read-through in-process per i dati caldi finché il sistema è un singolo processo. **Redis** resta **idea futura**, da introdurre solo quando/se il sistema si spezza in più processi che devono condividere la cache — solo allora vale il costo di un server Redis + invalidazione separati.

## Decisioni ancora aperte
- 🛠 **Graceful shutdown & recovery**: già aperta in [[system/modules/data-layer]] — la strategia di ripresa dal checkpoint resta da definire.

---

*Vedi [[system/modules/data-layer]] per le aree del DB e l'extraction, [[system/decision-log]] per lo storico decisioni.*

---
## Commenti recuperati da iCloud (2026-07-01)

> Commenti Obsidian `%%...%%` presenti nella vecchia copia iCloud (`7054827`) e reinseriti senza sovrascrivere il contenuto corrente.

%%langgraph è stato dismesso, salviamo structured output%%

%%???%%

%% valutare bene cosa fare subito in v alpha e cosa in post mvp o comunque in futuro come ottimizzazioni%%

