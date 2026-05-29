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

## Schema DB (5 tabelle core)

| Tabella | Contenuto |
|---------|-----------|
| `market_data` | OHLCV, order book, timestamp — dati grezzi dall'exchange |
| `trades` | Ogni ordine eseguito: entry, SL, TP, esito, P&L |
| `portfolio_state` | Snapshot corrente del portafoglio: posizioni, liquidità, esposizione |
| `module_outputs` | Output JSON di ogni modulo per ogni ciclo |
| `logs` | Log di sistema, errori, chain-of-thought LLM |

---

## Design DB esteso (call 2026-05-29)

Nella call del 29/05 il DB è stato ridisegnato in modo più ricco delle 5 tabelle core, ispirato alla dashboard **Streamlit di SFC** (fatta da Edoardo Birondi, "Sbirri"). Obiettivo dichiarato: una **replica custom di Yahoo Finance** specifica per il progetto. Sulla canvas è il blocco **viola**, sempre acceso, interrogato dai tool solo per le info che servono. Vedere [[references/videochiamata-luca-salvatore-2026-05-29]].

Quattro aree logiche:

1. **Rendicontazione portafoglio**
   - **Liquidità corrente / investita** (la base).
   - **Distribuzione portafoglio con più filtri**: geografica, asset class, **settore**, **duration** (bond). Realisticamente una grande tabella (riga = posizione, colonna = caratteristica). Modello mentale a **oggetti** (ogni azione = oggetto con proprietà, anche annidate).
   - **P/L e metriche di performance**.
2. **Dati che si aggiornano di continuo**
   - Prezzi di mercato · calendario economico · news · indicatori macro · **insider trading** (institutional positions) · **tassi di cambio** (importanti: non si opera solo in EUR).
3. **Costituzione / Statuto** — al **centro** (base di rendicontazione e dati live). Vedere [[build/modules/risk-management]].
4. **Log** — includono **states, reports, transactions**. Si salva tutto lo storico.

### Retention / clustering
A lungo termine la memoria cresce troppo → niente troncamento secco: **clusterizzare + riassumere + cancellare progressivamente** tenendo i riassunti. Ipotesi: ~5 anni giornaliero, 5-10 settimanale, 10-30 mensile. Hardware: hard disk esterni (es. 20TB ~500€). Molti dati vecchi sono comunque recuperabili online (Yahoo Finance; Reuters ora a pagamento).

### Extractors (i primi tool degli agenti)
- **Extractors set**: estraggono le info di mercato e le mandano **sia al DB sia agli agenti** (salvate in entrambe le direzioni).
- **Adaptive extractor**: frequenza **adattiva** in base alla vicinanza al target (entro ~30% dal target → alta frequenza/"modalità rischio"; lontano → daily). Serve a risparmiare compute e a rispettare i **rate limit** delle API.
- **Market Alert agent**: riceve dagli adaptive extractor; unico tool = **calendar tool** che scrive eventi nel **calendario economico** (es. data uscita prodotto, trimestrali) → alla corrispondenza data/ora scatta l'**alert** (gli alert sono solo numerici/prezzo).

### Output verso utente (idea)
**Canale Telegram "sala segnali"**: calendario economico, riassunti news, prezzi, trade fatti, variazioni di prezzo importanti (orario/giornaliero). Plaggabile alla dashboard con alert interattivi.

> Le 5 tabelle core qui sotto restano la base SQL minima; il design 2026-05-29 le estende con le aree logiche sopra (da consolidare in schema definitivo).

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

---

## Dipendenze

- **Nessuna dipendenza in ingresso**: è il punto di partenza del sistema
- **[[build/modules/quant-backtesting]]** dipende da questo: legge `market_data` dal DB
- **[[build/modules/llm-agent-system]]** dipende da questo: assembla il prompt dai dati in `module_outputs`

---

*Vedere [[build/mvp-prototype-design]] per il contesto completo del ciclo operativo.*
