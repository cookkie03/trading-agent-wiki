---
title: "Codebase Architecture"
type: build
tags:
  - architecture
  - software
  - roadmap
created: 2026-06-23
updated: 2026-06-23
status: active
confidence: medium
area: software
related:
  - "[[artifacts/project-board]]"
  - "[[system/architecture]]"
  - "[[system/modules/data-layer]]"
  - "[[system/modules/agents]]"
  - "[[system/modules/execution]]"
  - "[[system/modules/quant-backtesting]]"
  - "[[system/data-sources-tool-map]]"
---

# Codebase Architecture

Pagina guida per progettare la **nuova codebase reale**. Nasce da un cambio di stato deciso da Luca: il progetto va costruito in modo leggibile da zero, con codice che Luca possa seguire mentre cresce. Le implementazioni e i branch storici restano reference design, non baseline da assumere.

## Principio operativo

La sequenza corretta non parte dagli agenti. Parte dai contratti e dall'harness:

1. **Tree e confini dei package**
2. **Harness broker + data vendor + DB + test**
3. **Capability/tool deterministici**
4. **State, prompt e orchestration agentica**
5. **Job asincroni, dashboard, esperimenti**

Questa sequenza tiene insieme tre decisioni gia' presenti nella wiki: DB come hub centrale, principio deterministico e broker/vendor sostituibili via adapter.

## Boundary dei package

| Package / area | Responsabilita' | Dipendenze ammesse | Non deve contenere |
|---|---|---|---|
| `connectors/` | Adapter verso broker e data vendor: Alpaca, IBKR, yfinance, FRED, Finnhub, OpenBB, ecc. | SDK esterni, config, logging tecnico | Prompt, logica agentica, scoring di strategia |
| `database/` | Schema, migrazioni, repository, transazioni, dedup, retention | SQL/ORM, config DB | Chiamate vendor dirette, ragionamento LLM |
| `capabilities/` | Calcoli deterministici su dati normalizzati: indicatori, risk metrics, backtest helpers, transforms | `database/`, librerie quant | Chiamate API raw non wrappate, prompt |
| `tools/` | Interfacce stabili offerte agli agenti o al PM: quote, macro, sentiment, portfolio state, backtest query | `capabilities/`, `database/`, `connectors/` | Dettagli vendor visibili agli agenti |
| `agents/` | Prompt, schemas, context, routing, policy di richiamo tool, PM/desk/Risk | `tools/`, schemas condivisi | Calcoli numerici a mano, SDK broker/vendor |
| `execution/` | Trade deterministico, submit, recovery, costi, exit management, broker intent log | `database/`, `connectors/brokers`, risk capabilities | LLM decision-making |
| `frontend/` | UI read-only o controllata tramite contratti espliciti | API/query layer, read models | Business logic critica |
| `orchestration/` | Cycle runner, trigger engine, job scheduling, daemon | tutti i package tramite interfacce | Logica di dominio nascosta |

I nomi sono orientativi. La decisione da prendere non e' il nome esatto, ma il confine: **gli agenti non devono sapere quale broker o vendor sta dietro una richiesta**.

## Slice 1: harness minimo

Il primo pezzo di codice utile deve dimostrare che l'infrastruttura regge senza agenti:

- config unica per ambiente, broker, vendor, DB e costi;
- database iniziale con migrazioni e repository;
- adapter broker paper e contratto broker;
- almeno un data connector storico (`yfinance`) e uno macro (`FRED`) o mock equivalente;
- dedup/check-presenza per scritture DB;
- test offline con fake connector e fake broker;
- un test end-to-end: fetch dati -> DB -> capability calcola indicatore -> proposta trade finta -> execution paper.

Questo slice rende possibile costruire gli agenti sopra fondamenta osservabili, invece di usarli per coprire buchi infrastrutturali.

## Slice 2: capability e tool layer

Dopo l'harness, si costruisce il layer che rende gli agenti utili:

- `compute_indicator(ticker, indicator, params)` per ATR, RSI, MACD, medie, 52w, drawdown;
- `get_portfolio_state()` e `get_open_positions_risk()` dal DB;
- `get_macro_series(series_id, start, end)` da FRED/DB;
- `get_news` e `get_news_sentiment` dietro wrapper vendor;
- `get_calendar` per earnings e macro events;
- `run_backtest(strategy_id, params, window)` come capability separata dal live trading.

Questo layer deve collegarsi a [[system/tools-inventory]] e [[system/data-sources-tool-map]]: la mappa provider decide da dove arrivano i dati, l'inventory decide quali tool espone il sistema.

## Slice 3: agenti e state

Solo quando tool e dati sono stabili si passa a:

- prompt in file dedicati/versionabili;
- schema `research_state` / `investment_state` chiarito e testato;
- PM con policy "nel dubbio chiedi";
- desk Market/Sentiment/Technical/Fondamentali;
- Risk Analyst come desk/gate da decidere con Luca e Salvatore;
- orchestration event-driven tramite trigger engine.

Gli output agentici devono essere verificabili: ogni numero importante viene da tool deterministici, ogni decisione lascia trace nel DB.

## Decisioni aperte da chiudere prima di codice vero

- Framework agentico: Datapizza AI come candidato/reference o scelta confermata per il nuovo build? → [[system/stack]]
- Schema definitivo dello state e rapporto `research_state` / `investment_state` → [[system/state-schemas]]
- Risk Analyst: desk pari agli altri o gate finale? → [[system/agent-behaviors]]
- Primo set strategy da codificare: trend following, mean reversion, factor/value, dual portfolio → [[strategy/index]]
- Livello minimo di frontend nel primo harness: nessuno, CLI, o dashboard read-only → [[system/frontend-module]]

## Collegamenti operativi

- Board: [[artifacts/project-board]]
- Mappa fonti/tool: [[system/data-sources-tool-map]]
- Data layer: [[system/modules/data-layer]]
- Execution: [[system/modules/execution]]
- Quant/backtesting: [[system/modules/quant-backtesting]]
- Agents: [[system/modules/agents]]
