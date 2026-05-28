---
title: "Exchange + DB"
type: build
tags:
  - build
  - infrastructure
  - software
created: 2026-05-13
updated: 2026-05-27
status: active
priority: high
area: software
related:
  - "[[build/system-map]]"
  - "[[build/stack]]"
  - "[[build/mvp-prototype-design]]"
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
