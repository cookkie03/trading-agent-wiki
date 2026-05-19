---
title: "Modulo A — Exchange + DB"
type: build
tags:
  - build
  - infrastructure
  - software
created: 2026-05-13
updated: 2026-05-13
status: active
priority: high
area: software
related:
  - "[[build/system-map]]"
  - "[[build/stack]]"
  - "[[build/mvp-prototype-design]]"
---

# Modulo A — Exchange + DB

**Track 1 — Luca, sviluppo autonomo, inizia subito.**

Il modulo fondante. Costruisce la pipe vuota: connessione all'exchange, esecuzione ordini paper, DB centrale, logger base. Tutto il resto del sistema dipende da questo.

---

## Cosa fa

- Si connette a **Binance Testnet** (paper trading, zero rischio reale)
- Esegue ordini paper: **limit order + Stop Loss + Take Profit** (sempre obbligatori)
- Alimenta il **DB centrale** con dati di mercato in tempo reale
- Espone un'interfaccia identica per il backend **backtest** (replay dati storici)
- Logga ogni evento nel DB

## Output atteso

> Pipe vuoto funzionante: dati reali che scorrono nel DB, ordini eseguibili, logger attivo.

---

## Schema DB (5 tabelle core)

| Tabella | Contenuto |
|---------|-----------|
| `market_data` | OHLCV, order book, timestamp — dati grezzi da Binance |
| `trades` | Ogni ordine eseguito: entry, SL, TP, esito, P&L |
| `portfolio_state` | Snapshot corrente del portafoglio: posizioni, liquidità, esposizione |
| `module_outputs` | Output JSON di ogni modulo per ogni ciclo |
| `logs` | Log di sistema, errori, chain-of-thought LLM |

---

## Tech

- **CCXT**: connessione Binance. Interfaccia astratta → cambio exchange = cambio config
- **PostgreSQL** (prod) / **SQLite** (dev locale)
- Exchange Module con due backend intercambiabili:
  - `live`: chiama Binance Testnet API
  - `backtest`: replay su dati storici scaricati

---

## Decisioni prese

| Tema | Scelta |
|------|--------|
| Exchange MVP | Binance Testnet |
| Tipo ordini | Limit order + SL + TP (obbligatori, hard constraint) |
| DB | PostgreSQL prod / SQLite dev |
| Interfaccia exchange | Astratta — stesso codice, backend diverso per live/backtest |

## Domande aperte

Nessuna critica. Questo modulo è il più definito — si può iniziare a costruire.

---

## Dipendenze

- **Nessuna dipendenza in ingresso**: Modulo A è il punto di partenza
- **Modulo C dipende da A**: usa il DB di A per i dati storici
- **Modulo D dipende da A**: assembla il prompt dai dati in `module_outputs`

---

*Vedere [[build/mvp-prototype-design]] per il contesto completo del ciclo operativo.*
