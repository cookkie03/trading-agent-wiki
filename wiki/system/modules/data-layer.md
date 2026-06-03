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

### Forma di storage (decisione 2026-06-02)
**Principalmente time-series**, ma con DB e **architetture a oggetti internamente** (Luca: *"qualcosa di time-series, ma con db e architetture anche ad oggetti internamente al db"*). Lettura per area:
- **Dati live / prezzi / macro** → time-series (cuore del sistema);
- **Rendicontazione** → modello a oggetti (riga = posizione, colonne = caratteristiche);
- **States e output LLM annidati** → forma documentale/JSON (forma fine ancora da assegnare).

Resta aperta solo la **forma fine per i singoli stati annidati**. Vedi [[system/decision-log]] e [[system/state-schemas]].

---

## Extraction — come i dati entrano nel DB

Primo set di tool degli agenti. Si agganciano al DB (**DB-first**), non ai vendor direttamente: ogni dato è scritto nel DB prima di essere reso disponibile agli agenti.

| Componente (nodo canvas) | Funzione |
|--------------------------|----------|
| **Extractors set** | Estraggono le info di mercato e le scrivono **sia nel DB sia verso gli agenti**. |
| **Adaptive extractor** | Frequenza **adattiva** in base alla vicinanza al target (entro ~30% dal target → alta frequenza/"modalità rischio"; lontano → daily). Risparmia compute e rispetta i **rate limit** delle API. |
| **Market Alert** | Riceve dagli adaptive extractor; unico tool = **calendar tool** che scrive eventi nel **calendario economico** (es. data uscita prodotto, trimestrali). |
| **calendar tool** | Scrive/legge gli eventi del calendario economico; alla corrispondenza data/ora scatta l'**alert** (solo numerico/prezzo) verso il Portfolio Manager. |
| **mantainer** | Processo di manutenzione (non-LLM, blocco verde/technical sul canvas) che **trasforma i dati `technical`/`transactions` in `rendicontazione`** (portfolio accounting) e la tiene aggiornata nel DB. *Ruolo confermato in call 2026-06-02*: «un mantainer che trasforma i technical in rendicontazione». È il ponte deterministico transazioni → metriche di portafoglio. |

**Look-ahead bias — doppia data**: ogni informazione nel DB ha `publication_date` (quando ottenuta/pubblicata) e `reference_date` (data a cui si riferisce). Più preciso del semplice `curr_date` filtering.

**Indicatori calcolati dal DB**: nessun calcolo on-the-fly — gli indicatori si calcolano con formule che richiamano i dati grezzi già nel DB.

### Queue system + check presenza (decisione 2026-06-02)
Gli extractor si chiamano **solo se l'informazione non è già nel DB**. Flusso:
1. **Check preventivo nel DB**: se il dato c'è → si legge da lì, fine (nessuna richiesta esterna).
2. Se manca → la richiesta entra in una **coda (queue)**; **un extractor per vendor** consuma la sua coda e **autogestisce i rate limit** di estrazione.
3. Il check avviene *prima* di accodare, per non riempire la coda di richieste inutili.

Si estraggono dai vendor **solo le osservazioni grezze**; le metriche derivate (P/E, ratio, ecc.) si **calcolano internamente** dai dati grezzi già nel DB (vedi [[system/modules/quant-backtesting]]).

---

## Operatività & resilienza

- **Deploy**: il sistema gira sul **Minisforum (mini-server) di Luca, acceso 24/7 in casa** (decisione 2026-06-02).
- **Secrets**: chiavi API (OpenRouter, broker, data vendor) in **`.env` locale** per ora.
- **Graceful shutdown & recovery** *(aperto)*: serve un meccanismo di **inizializzazione** e di **ripresa dal punto precedente** in caso di crash a metà ciclo (ordine inviato non loggato, state parzialmente compilato). Il checkpointing SQLite di LangGraph è la base, ma la strategia di recovery è da definire. → [[system/decision-log]].
- **Orario di mercato / weekend**: gli extractor e gli alert devono conoscere le ore di mercato e i festivi (da definire).

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
