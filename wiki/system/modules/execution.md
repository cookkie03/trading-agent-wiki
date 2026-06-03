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

### Disinvestimento automatico
Una parte del disinvestimento è **deterministica e automatica**: TP, SL e **trailing stop loss** armati sull'ordine chiudono la posizione senza intervento dell'agente. È il livello 1 del disinvestimento; il livello 2 (valutazione periodica rating-based di cosa vendere per far spazio) vive in [[system/rating-scoring]]. Distinto dal **cash-out** (estrazione profitti verso IBAN, vedi Statuto in [[system/modules/agents]]).

**Logging del meccanismo di uscita**: ogni chiusura registra in `transactions` il campo **`exit_reason`** (`take_profit`/`stop_loss`/`trailing_stop`/`rating_based`/`manual_override`/`option_expiry`). È il prerequisito per il feedback post-trade segmentato per tipo di uscita → [[system/rating-scoring]] §4.

---

## Exchange (paper trading) — broker intercambiabili

**Design deciso (2026-06-02)**: un **file-adapter (wrapper) per ogni broker** che traduce le API del servizio in un'**interfaccia interna standardizzata** e leggibile dal programma. Il broker si cambia esattamente come in TradingAgents si cambia il provider LLM (Luca: *«io devo poter cambiare facilmente il broker del progetto»*).

```
        ┌─ alpaca_adapter.py ─┐
core  ──┤  ibkr_adapter.py    ├── interfaccia interna standard (place_order, get_positions, get_fees…)
        └─ ..._adapter.py    ─┘
```

- **MVP**: **Alpaca** (paper US equity, developer-first, gratuito).
- **Produzione**: **IBKR** — la transizione deve essere **facile**, i due broker **intercambiabili** (stesso contratto I/O, cambia solo l'adapter attivo).
- Espone un'interfaccia identica per il backend **backtest** ([[system/modules/quant-backtesting]]): stessa logica del codice live, replay su dati storici.
- Logga ogni evento in `transactions` (area Log del DB → [[system/modules/data-layer]]).
- CCXT resta candidato come layer per il futuro multi-asset, ma per l'equity gli SDK ufficiali (Alpaca/`ib_insync`) sono più adatti. Provider in [[system/data-providers]].

### Transaction cost auto-adattivo (decisione 2026-06-02)
Niente costo hardcodato. L'adapter del broker **espone le commissioni reali applicate sul momento**, in funzione di broker, tipo di asset, size e quant'altro. Il costo (più il costo token del ciclo) è sottratto dal profitto atteso per ottenere la **net performance**. Così il backtest e il live usano lo stesso modello di costo, sempre aggiornato. Vedi [[system/modules/quant-backtesting]].

---

## Decisioni prese

| Tema | Scelta |
|------|--------|
| Trade | Funzione Python deterministica, non agente (2026-05-29) |
| Tipo ordini | Limit order + SL + TP (obbligatori) |
| Interfaccia exchange | Astratta — stesso codice, backend live/backtest |
| Leva | Solo via opzioni Call/Put su segnali `Strong` validati |

## Domande aperte

- ~~**Exchange per paper trading**~~ → **CHIUSO**: Alpaca per MVP, IBKR per prod, adapter intercambiabili (vedi sopra).
- **`entry_price` del limit order**: come si calcola (pivot / % sotto prezzo / range 52w)? Da strutturare bene → [[system/state-schemas]].
- **Position sizing**: formula da definire (relativo al portafoglio, scalato per conviction) → [[system/position-sizing]].
- **Meccanismo di disinvestimento ottimale**: quale asset vendere per liberare liquidità senza intaccare il 10% cash → [[system/rating-scoring]] + logica Statuto in [[system/modules/agents]].
- **Sizing opzioni**: diverso dall'equity spot, fuori MVP → [[strategy/questions-for-salvatore]].

---

## Dipendenze

- Legge da: `portfolio_state` + lo `research_state` approvato → [[system/modules/agents]]
- Scrive in: `transactions` → [[system/modules/data-layer]]
- Upstream: gate Risk Analyst ([[system/modules/agents]]); Downstream: aggiornamento rendicontazione nel DB

---

*Per l'architettura completa vedi [[system/architecture]].*
