---
title: "Exchange + DB"
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
  - "[[build/system-map]]"
  - "[[build/stack]]"
  - "[[build/mvp-prototype-design]]"
  - "[[build/modules/llm-agent-system]]"
  - "[[references/videochiamata-luca-salvatore-2026-05-29]]"
---

# Exchange + DB

Il componente fondante. Costruisce la pipe vuota: connessione all'exchange, esecuzione ordini paper, DB centrale, logger base. Tutto il resto del sistema dipende da questo.

---

## Riferimenti di codice (repo esterni)

- **Schema DB context→operation con FK**: [[references/external/rizzo-trading-agent]] — `db_utils.py` (schema Postgres completo) collega ogni decisione del bot al contesto esatto (prompt + indicatori + news + sentiment + forecast) → tracciabilità totale e dataset pronto per backtest/eval.
- **Esecuzione ordini**: [[references/external/rizzo-trading-agent]] — `hyperliquid_trader.py` (validazione input → size dal balance → market order + SL trigger `reduce_only`); `utils.py` per la reconciliation degli SL esterni via diff di snapshot.
- **Architettura backend a layer + broker sync**: [[references/external/cvx-portfolio-optimizer]] — `api/` (FastAPI: models→repositories→services→routers, middleware, Alembic, docker-compose) e `services/broker_sync_service.py` + `trading212/`.
- **Modello transaction-based** (posizioni derivate dalle transazioni): [[references/external/sfc-portfolio-tracker]] — `fund_manager.py`.

---

## Cosa fa

- Si connette all'**exchange** (paper trading, zero rischio reale) tramite interfaccia astratta
- Esegue ordini paper: **limit order + Stop Loss + Take Profit** (sempre obbligatori)
- Alimenta il **DB centrale** con dati di mercato in tempo reale
- Espone un'interfaccia identica per il backend **backtest** (replay dati storici)
- Logga ogni evento nel DB

> **Nota scope (2026-05-23)**: il progetto è ora stock-only (non crypto). L'exchange per la fase demo/paper non è ancora scelto (Alpaca, Interactive Brokers o altri). CCXT rimane il layer di astrazione ma potrebbe non coprire tutti gli exchange equity.

## Output atteso

> Pipe vuoto funzionante: dati reali che scorrono nel DB, ordini eseguibili, logger attivo.

---

## Schema DB (definitivo, consolidato 2026-05-29)

Il DB è il blocco **viola** della canvas `agents.canvas`: sempre acceso, interrogato dai tool solo per le info che servono. Ispirato alla dashboard **Streamlit di SFC** (Edoardo Birondi, "Sbirri"); obiettivo dichiarato: una **replica custom di Yahoo Finance** specifica per il progetto ([[references/videochiamata-luca-salvatore-2026-05-29]]).

Le **5 tabelle core** sono la base SQL minima; il design 29/05 le organizza in **4 aree logiche**. Mapping unico:

| Area logica | Tabelle / contenuto | Tabella core |
|-------------|---------------------|--------------|
| **1. Rendicontazione portafoglio** | Liquidità corrente/investita; distribuzione con più filtri (geo, asset class, **settore**, **duration**); P/L e metriche di performance. Modello a **oggetti** (ogni posizione = oggetto con proprietà annidate; riga = posizione, colonna = caratteristica). | `portfolio_state` (esteso) |
| **2. Dati live** (aggiornati di continuo) | Prezzi di mercato · calendario economico · news · indicatori macro · **insider trading** (institutional positions) · **tassi di cambio** (non si opera solo in EUR) | `market_data` (esteso) |
| **3. Costituzione / Statuto** | Regole deterministiche del fondo, al **centro** (base di rendicontazione e dati live) → [[build/modules/risk-management]] | *(nuova)* `charter` / parametri |
| **4. Log** | `states`, `reports`, `transactions` — si salva tutto lo storico | `logs` + `trades` |

> `module_outputs` (5ª core) resta come buffer degli output strutturati per ciclo, confluendo nell'area Log (`states`/`reports`).

### Retention / clustering
A lungo termine la memoria cresce troppo → niente troncamento secco: **clusterizzare + riassumere + cancellare progressivamente** tenendo i riassunti. Ipotesi: ~5 anni giornaliero, 5-10 settimanale, 10-30 mensile. Hardware: hard disk esterni (es. 20TB ~500€). Molti dati vecchi sono comunque recuperabili online (Yahoo Finance; Reuters ora a pagamento).

### Forma di storage (domanda aperta — daily note 2026-05-28)
Luca: *"meglio SQL o JSON per i dati? quale forma di storage è meglio per quale dato? ci sono altre forme che non sto considerando?"* → da decidere per area: relazionale (SQL) per rendicontazione/transazioni strutturate; JSON/documentale per states e output LLM annidati; eventuali time-series store per i dati live. Vedi Domande aperte.

### Extractors (i primi tool degli agenti)
- **Extractors set**: estraggono le info di mercato e le mandano **sia al DB sia agli agenti** (salvate in entrambe le direzioni).
- **Adaptive extractor**: frequenza **adattiva** in base alla vicinanza al target (entro ~30% dal target → alta frequenza/"modalità rischio"; lontano → daily). Serve a risparmiare compute e a rispettare i **rate limit** delle API.
- **Market Alert agent**: riceve dagli adaptive extractor; unico tool = **calendar tool** che scrive eventi nel **calendario economico** (es. data uscita prodotto, trimestrali) → alla corrispondenza data/ora scatta l'**alert** (gli alert sono solo numerici/prezzo).

### Output verso utente (idea)
**Canale Telegram "sala segnali"**: calendario economico, riassunti news, prezzi, trade fatti, variazioni di prezzo importanti (orario/giornaliero). Plaggabile alla dashboard con alert interattivi.

---

## Tech

- **CCXT** (o equivalente): interfaccia astratta → cambio exchange = cambio config
- **PostgreSQL** (prod) / **SQLite** (dev locale)
- Exchange Module con due backend intercambiabili:
  - `live`: chiama Binance Testnet API
  - `backtest`: replay su dati storici scaricati

---

## Decisioni prese

| Tema | Scelta |
|------|--------|
| Exchange MVP | Da scegliere — stock exchange con paper trading API (Alpaca, IB, ecc.) |
| Tipo ordini | Limit order + SL + TP (obbligatori, hard constraint) |
| DB | PostgreSQL prod / SQLite dev |
| Interfaccia exchange | Astratta — stesso codice, backend diverso per live/backtest |

## Domande aperte

- **Exchange per paper trading stock**: quale scegliere? Alpaca ha API gratuite per US equity; Interactive Brokers ha copertura più ampia ma setup più complesso. Da decidere.
- **CCXT per equity**: verificare se CCXT supporta l'exchange scelto o se serve una libreria dedicata (es. alpaca-trade-api).
- **Forma di storage per area (daily note 2026-05-28)**: SQL relazionale vs JSON/documentale vs time-series — quale per quale dato? Possibili forme non ancora considerate? Da decidere insieme allo schema definitivo.

---

## Dipendenze

- **Nessuna dipendenza in ingresso**: è il punto di partenza del sistema
- **[[build/modules/quant-backtesting]]** dipende da questo: legge `market_data` dal DB
- **[[build/modules/llm-agent-system]]** dipende da questo: assembla il prompt dai dati in `module_outputs`

---

*Vedere [[build/mvp-prototype-design]] per il contesto completo del ciclo operativo.*
