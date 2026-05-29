---
title: "Data Layer — DB centrale + Extraction"
type: build
tags:
  - build
  - infrastructure
  - software
created: 2026-05-13
updated: 2026-05-29
status: active
priority: high
area: software
related:
  - "[[system/architecture]]"
  - "[[system/stack]]"
  - "[[system/data-providers]]"
  - "[[system/modules/agents]]"
  - "[[system/modules/execution]]"
  - "[[system/modules/quant-backtesting]]"
---

# Data Layer — DB centrale + Extraction

Il componente fondante. Costruisce la pipe vuota su cui poggia tutto il resto: il **DB centrale** (unico punto di verità) e il livello di **estrazione** che lo alimenta. Mappa le due aree sinistre di `architettura.canvas` ([[artifacts/trading-floor]] e i canvas in `artifacts/architecture/`): il grande gruppo **DB** e i tool di estrazione (`Extractors set`, `Adaptive extractor`, `Market Alert`, `calendar tool`, `mantainer`).

> L'esecuzione ordini e l'exchange sono trattati in [[system/modules/execution]]. Qui sta solo *come i dati entrano e vivono nel DB*.

---

## Riferimenti di codice (repo esterni)

- **Schema DB context→operation con FK**: [[prior-art/libraries/rizzo-trading-agent]] — `db_utils.py` (schema Postgres completo) collega ogni decisione del bot al contesto esatto (prompt + indicatori + news + sentiment + forecast) → tracciabilità totale e dataset pronto per backtest/eval.
- **Architettura backend a layer**: [[prior-art/libraries/cvx-portfolio-optimizer]] — `api/` (FastAPI: models→repositories→services→routers, middleware, Alembic, docker-compose).
- **Modello transaction-based** (rendicontazione derivata dalle transazioni): [[prior-art/libraries/sfc-portfolio-tracker]] — `fund_manager.py`, `build_nav_history.py`.

---

## DB centrale — il blocco sempre acceso

Unico punto di verità del sistema: tutti i moduli/extractor scrivono qui, gli agenti leggono da qui (solo i campi che servono). Ispirato alla dashboard **Streamlit di SFC**; obiettivo dichiarato: una **replica custom di Yahoo Finance** specifica per il progetto.

Le **5 tabelle core** sono la base SQL minima; il design organizza i dati in **4 aree logiche** (i quattro sotto-gruppi del blocco DB nel canvas):

| Area logica | Contenuto (nodi canvas) | Tabella core |
|-------------|-------------------------|--------------|
| **1. Rendicontazione portafoglio** | Liquidità corrente/investita · distribuzione con più filtri (geo, asset class, **settore**, **duration**) · P/L e metriche di performance. Modello a **oggetti** (riga = posizione, colonna = caratteristica). | `portfolio_state` (esteso) |
| **2. Dati live** (aggiornati di continuo) | Prezzi di mercato · calendario economico · news · indicatori macro · **insider trading** (institutional positions) · **tassi di cambio** | `market_data` (esteso) |
| **3. Costituzione / Statuto** | Regole deterministiche del fondo, al **centro** (base di rendicontazione e dati live) → la logica vive in [[system/modules/agents]] (Statuto del Fondo) | *(nuova)* `charter` / parametri |
| **4. Log** | `log`, `states`, `report`, `transactions` — storico completo | `logs` + `trades` |

> `module_outputs` (5ª core) resta come buffer degli output strutturati per ciclo, confluendo nell'area Log (`states`/`report`).

### Retention / clustering
La memoria cresce troppo → niente troncamento secco: **clusterizzare + riassumere + cancellare progressivamente** tenendo i riassunti. Ipotesi: ~5 anni giornaliero, 5-10 settimanale, 10-30 mensile. Hardware: hard disk esterni (es. 20TB ~500€). Molti dati vecchi sono recuperabili online (Yahoo Finance; Reuters ora a pagamento).

### Forma di storage (domanda aperta — 2026-05-28)
Luca: *"meglio SQL o JSON per i dati? quale forma per quale dato?"* → da decidere per area: relazionale (SQL) per rendicontazione/transazioni strutturate; JSON/documentale per states e output LLM annidati; eventuale time-series store per i dati live. Vedi [[system/decision-log]].

---

## Extraction — come i dati entrano nel DB

Primo set di tool degli agenti. Si agganciano al DB (**DB-first**), non ai vendor direttamente: ogni dato è scritto nel DB prima di essere reso disponibile agli agenti.

| Componente (nodo canvas) | Funzione |
|--------------------------|----------|
| **Extractors set** | Estraggono le info di mercato e le scrivono **sia nel DB sia verso gli agenti**. |
| **Adaptive extractor** | Frequenza **adattiva** in base alla vicinanza al target (entro ~30% dal target → alta frequenza/"modalità rischio"; lontano → daily). Risparmia compute e rispetta i **rate limit** delle API. |
| **Market Alert** | Riceve dagli adaptive extractor; unico tool = **calendar tool** che scrive eventi nel **calendario economico** (es. data uscita prodotto, trimestrali). |
| **calendar tool** | Scrive/legge gli eventi del calendario economico; alla corrispondenza data/ora scatta l'**alert** (solo numerico/prezzo) verso il Portfolio Manager. |
| **mantainer** | Processo di manutenzione (non-LLM) che tiene aggiornati/ricalcolati i **dati technical** e la **rendicontazione portafoglio** nel DB. *(Nodo nuovo del canvas — ruolo esatto da confermare in fase di design del grafo.)* |

**Look-ahead bias — doppia data**: ogni informazione nel DB ha `publication_date` (quando ottenuta/pubblicata) e `reference_date` (data a cui si riferisce). Più preciso del semplice `curr_date` filtering.

**Indicatori calcolati dal DB**: nessun calcolo on-the-fly — gli indicatori si calcolano con formule che richiamano i dati grezzi già nel DB.

---

## Tech

- **PostgreSQL** (prod) / **SQLite** (dev locale)
- Provider dati e broker: vedi [[system/data-providers]]
- Schema DB versionato (Alembic)

---

## Dipendenze

- **Nessuna dipendenza in ingresso**: è il punto di partenza del sistema.
- **[[system/modules/quant-backtesting]]** legge `market_data` dal DB.
- **[[system/modules/agents]]** legge dal DB **solo** i campi che servono (evita context rot).
- **[[system/modules/execution]]** scrive `transactions` qui e legge `portfolio_state`.

---

*Per l'architettura completa vedi [[system/architecture]]. Per le decisioni tecniche [[system/decision-log]].*
