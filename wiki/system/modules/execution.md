---
title: "Execution — Investment State, Trade, Exchange"
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
  - "[[system/modules/agents]]"
  - "[[system/modules/data-layer]]"
  - "[[system/data-providers]]"
---

# Execution — Investment State, Trade, Exchange

La coda deterministica del sistema: dal `research_state` approvato all'ordine eseguito sull'exchange. Mappa i nodi `Investment State`, `Trade` e l'uscita verso `transactions` di `architettura.canvas`. **Niente LLM qui**: tutto è Python puro.

```
research_state (approvato dal Risk Analyst)
   → Investment State (gate di completezza)
      → Trade (funzione Python deterministica)
         → Exchange (paper) → transactions (DB)
```

---

## Riferimenti di codice (repo esterni)

- **Esecuzione ordini + stop-loss**: [[prior-art/libraries/rizzo-trading-agent]] — `hyperliquid_trader.py` (validazione input → size dal balance → market order + SL trigger `reduce_only`); `utils.py` per la reconciliation degli SL esterni via diff di snapshot; `_place_stop_loss` / `check_stop_loss`.
- **Broker sync**: [[prior-art/libraries/cvx-portfolio-optimizer]] — `services/broker_sync_service.py` + `trading212/`.
- **Modello transaction-based** (posizioni derivate dalle transazioni): [[prior-art/libraries/sfc-portfolio-tracker]] — `fund_manager.py`.

---

## Investment State — gate di completezza

Nessun trade finché l'`investment_state` non è **completo** (forza il passaggio per tutti i desk analisti + gate Risk). Si **resetta automaticamente** quando il blocco Trade rileva la transazione: *state pieno → estrae trade → reset*. Schema in [[system/modules/agents]] (TypedDict/Pydantic).

---

## Trade — funzione Python deterministica (NON agent)

La conversione `research_state → transazione` **non richiede un LLM**: una funzione estrae i campi della proposta (asset, direzione, entry, SL, TP, sizing, convinzione) ed esegue. La scelta del **miglior prezzo tra broker** è deterministica.

> **Nota (riconciliazione 2026-05-29)**: il precedente "LLM Trader che produce un JSON `{asset, direction, entry, SL, TP, leverage, reasoning}`" è **superato**. Quei campi sono ora campi dello `research_state` compilato dagli analisti e validato dal Risk Analyst. Vedi *Trader = funzione Python deterministica* in [[system/decision-log]].

- **Ordini**: limit order + **Stop Loss + Take Profit** sempre obbligatori (hard constraint).
- **Leva via opzioni**: se lo state porta un segnale `Strong` validato, la funzione traduce il segnale in acquisto di opzioni **Call** (`Strong Buy`) o **Put** (`Strong Sell`). Logica di validazione in [[system/modules/agents]].

---

## Exchange (paper trading)

- Si connette all'**exchange** tramite **interfaccia astratta** (paper trading, zero rischio reale): cambio exchange = cambio config.
- Espone un'interfaccia identica per il backend **backtest** ([[system/modules/quant-backtesting]]): stessa logica del codice live, replay su dati storici.
- Logga ogni evento in `transactions` (area Log del DB → [[system/modules/data-layer]]).

> **Nota scope (2026-05-23)**: progetto **stock-only** (non crypto). L'exchange per la fase demo/paper non è ancora scelto (Alpaca, Interactive Brokers o altri). CCXT è il candidato come layer di astrazione, ma potrebbe non coprire tutti gli exchange equity → valutare librerie dedicate (es. `alpaca-trade-api`). Provider in [[system/data-providers]].

---

## Decisioni prese

| Tema | Scelta |
|------|--------|
| Trade | Funzione Python deterministica, non agente (2026-05-29) |
| Tipo ordini | Limit order + SL + TP (obbligatori) |
| Interfaccia exchange | Astratta — stesso codice, backend live/backtest |
| Leva | Solo via opzioni Call/Put su segnali `Strong` validati |

## Domande aperte

- **Exchange per paper trading stock**: Alpaca (API gratuite US equity) vs Interactive Brokers (copertura ampia, setup complesso) vs altri.
- **CCXT per equity**: verificare la copertura o usare libreria dedicata.
- **Meccanismo di disinvestimento ottimale**: come scegliere deterministicamente quale asset vendere per liberare liquidità senza intaccare il 10% cash (logica Statuto in [[system/modules/agents]]).

---

## Dipendenze

- Legge da: `portfolio_state` + lo `research_state` approvato → [[system/modules/agents]]
- Scrive in: `transactions` → [[system/modules/data-layer]]
- Upstream: gate Risk Analyst ([[system/modules/agents]]); Downstream: aggiornamento rendicontazione nel DB

---

*Per l'architettura completa vedi [[system/architecture]].*
