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

> 🟢 **Trade deterministico implementato (alpha v0, 2026-06-06)** — `tradingagents/execution/trade.py` (branch `feat/trade-execution`): `can_trade` (gate: approvato·completo·azionabile·prezzato) → `build_trade` (state → `OrderProposal` via risk engine + ATR levels) → `persist_trade` (con `client_order_id` idempotente) → `inject_portfolio_state` (tool G) → `propose_and_record` end-to-end. 5 test integrazione.

%%qui manca una parte relativa all'errore, cioè, se can_trade non va perché research_state non è completo, bisogna avvisare un agent, tendenzialmente il pm, dicendogli che il trade è saltato perché non sono stati interpellati tutti gli agent, in questo modo si può procedere con le conversazioni tra agent e procedere no? idem una notifica al pm che gli manda la conferma di trade
in generale pensare sempre ai meccanismi di error handling%%

> 🟢 **Broker adapter implementato (alpha v0, 2026-06-06)** — pacchetto `tradingagents/broker/` (branch `feat/broker-adapter`): interfaccia `Broker` intercambiabile + `PaperBroker` (simulatore in-process, fill istantanei, **idempotente su `client_order_id`**, traccia cassa/posizioni) + `AlpacaBroker` (REST paper via `requests`, integration). In `execution/submit.py`: `submit_trade`, `execute_thesis` (size+record+submit), `reconcile_open_trades` (**broker = source of truth → graceful recovery**). 5 test unit + 1 integration Alpaca gated. **Manca ancora**: IBKR adapter (prod), esecuzione bracket completa, gestione fill parziali. Vedi [[system/fork-gap-analysis]] (M4).

```
research_state (approvato dal Risk Analyst)
   → Investment State (gate di completezza)
      → Trade (funzione Python deterministica)
         → Exchange (paper) → transactions (DB)
```

%%errore, research_state è lo State, Investment State corrisponde ad research_state, che coincide come ruolo nel file [[architettura.canvas]]%%

---

## Riferimenti di codice (repo esterni)

- **Esecuzione ordini + stop-loss**: [[prior-art/libraries/rizzo-trading-agent]] — `hyperliquid_trader.py` (validazione input → size dal balance → market order + SL trigger `reduce_only`); `utils.py` per la reconciliation degli SL esterni via diff di snapshot; `_place_stop_loss` / `check_stop_loss`.
- **Broker sync**: [[prior-art/libraries/cvx-portfolio-optimizer]] — `services/broker_sync_service.py` + `trading212/`.
- **Modello transaction-based** (posizioni derivate dalle transazioni): [[prior-art/libraries/sfc-portfolio-tracker]] — `fund_manager.py`.

---

## Investment State — gate di completezza

Nessun trade finché l'`investment_state` non è **completo** (forza il passaggio per tutti i desk analisti + gate Risk). Si **resetta automaticamente** quando il blocco Trade rileva la transazione: *state pieno → estrae trade → reset*. Schema in [[system/modules/agents]] (TypedDict/Pydantic).

> **Validazione collettiva (opzione, 2026-06-04)**: oltre al gate deterministico di completezza e al gate bear del Risk, si valuta un sign-off di **tutti gli agenti** che garantiscono completezza · correttezza · esaustività delle fonti dello state; se uno segnala una lacuna → `send_back` prima del sealing. Dettaglio in [[system/state-schemas]].

%%questa parte di sign off è valida ma va fatta bene ed efficiente, quindi questo signoff va fatto per esempio quando il pm manda il reasearch_state, in quel caso si apre un nnuovo thread per ogni agent, specifico, con tutta la conversazione passata o un "compact" della conversazione per sign off%%

---

## Trade — funzione Python deterministica (NON agent)

La conversione `research_state → transazione` **non richiede un LLM**: una funzione estrae i campi della proposta (asset, direzione, entry, SL, TP, sizing, convinzione) ed esegue. La scelta del **miglior prezzo tra broker** è deterministica.

> **Nota (riconciliazione 2026-05-29)**: il precedente "LLM Trader che produce un JSON `{asset, direction, entry, SL, TP, leverage, reasoning}`" è **superato**. Quei campi sono ora campi dello `research_state` compilato dagli analisti e validato dal Risk Analyst. Vedi *Trader = funzione Python deterministica* in [[system/decision-log]].

- **Ordini**: [[_meta/glossario#Limit Order|limit order]] + **Stop Loss + Take Profit** sempre obbligatori (hard constraint).
- **Leva via opzioni**: se lo state porta un segnale `Strong` validato, la funzione traduce il segnale in acquisto di opzioni **Call** (`Strong Buy`) o **Put** (`Strong Sell`). Logica di validazione in [[system/modules/agents]].

### Disinvestimento automatico
Una parte del disinvestimento è **deterministica e automatica**: TP, SL e **[[_meta/glossario#Trailing Stop Loss|trailing stop loss]]** armati sull'ordine chiudono la posizione senza intervento dell'agente. È il livello 1 del disinvestimento; il livello 2 (valutazione periodica rating-based di cosa vendere per far spazio) vive in [[system/rating-scoring]]. Distinto dal **cash-out** (estrazione profitti verso IBAN, vedi Statuto in [[system/modules/agents]]).

**Logging del meccanismo di uscita**: ogni chiusura registra in `transactions` il campo **`exit_reason`** (`take_profit`/`stop_loss`/`trailing_stop`/`rating_based`/`manual_override`/`option_expiry`). È il prerequisito per il feedback post-trade segmentato per tipo di uscita → [[system/rating-scoring]] §4.

%% devo ancora leggere le informazioni sulla memoria degli agenti, ma sicuramente questa exit Reason potrebbe essere qualcosa di iniettato automaticamente nel momento in cui si analizzano ticker in cui siamo già stati investiti idealmente%%

---

## Exchange (paper trading) — broker intercambiabili

**Design deciso (2026-06-02)**: un **file-adapter ([[_meta/glossario#Adapter / Wrapper (broker)|wrapper]]) per ogni broker** che traduce le API del servizio in un'**interfaccia interna standardizzata** e leggibile dal programma. Il broker si cambia esattamente come in TradingAgents si cambia il provider LLM (Luca: *«io devo poter cambiare facilmente il broker del progetto»*).
%%così come abbiamo pensato ai wrapper per gli exchange/broer, dobbiamo pensare ai wrapper anche per i tool e l'estrazione dati da vendor diversi, per aumentare la scalabilità ed evitare duplicazioni, stndardizzando le informaizoni e i loro formati, unificando i dati di vendor diversi con i wrapper%% 

```
        ┌─ alpaca_adapter.py ─┐
core  ──┤  ibkr_adapter.py    ├── interfaccia interna standard (place_order, get_positions, get_fees…)
        └─ ..._adapter.py    ─┘
```
%%i wrapper chiaramente dovranno essere extra llm/agents, gli agenti non si dovranno mai preoccupare del broker o del data vendor o niente, gli agents devono fare solamente la richiesta del dato o l'immissione del trade, nient'altro, al resto deve pensarci l'infrastruttura%%
- **MVP**: **Alpaca** (paper US equity, developer-first, gratuito).
- **Produzione**: **IBKR** — la transizione deve essere **facile**, i due broker **intercambiabili** (stesso contratto I/O, cambia solo l'adapter attivo).
- Espone un'interfaccia identica per il backend **backtest** ([[system/modules/quant-backtesting]]): stessa logica del codice live, replay su dati storici.
- Logga ogni evento in `transactions` (area Log del DB → [[system/modules/data-layer]]).
- [[_meta/glossario#CCXT|CCXT]] resta candidato come layer per il futuro multi-asset, ma per l'equity gli SDK ufficiali (Alpaca/`ib_insync`) sono più adatti. Provider in [[system/data-providers]].

### Transaction cost auto-adattivo (decisione 2026-06-02, %%sperimentale, da implementare post alpha version%%)
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

- ~~**Exchange per [[_meta/glossario#Paper Trading / Testnet|paper trading]]**~~ → **CHIUSO**: Alpaca per MVP, IBKR per prod, adapter intercambiabili (vedi sopra).
- **`entry_price` del limit order**: come si calcola (pivot / % sotto prezzo / range 52w)? Da strutturare bene → [[system/state-schemas]].
- **Position sizing**: formula da definire (relativo al portafoglio, scalato per [[_meta/glossario#Conviction Level|conviction]]) → [[system/position-sizing]].
- **Meccanismo di disinvestimento ottimale**: quale asset vendere per liberare liquidità senza intaccare il 10% cash → [[system/rating-scoring]] + logica Statuto in [[system/modules/agents]].
- **Sizing opzioni**: diverso dall'equity spot, fuori MVP → [[strategy/questions-for-salvatore]].

---

## Dipendenze

- Legge da: `portfolio_state` + lo `research_state` approvato → [[system/modules/agents]]
- Scrive in: `transactions` → [[system/modules/data-layer]]
- Upstream: gate Risk Analyst ([[system/modules/agents]]); Downstream: aggiornamento rendicontazione nel DB

---

*Per l'architettura completa vedi [[system/architecture]].*
