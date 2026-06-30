---
title: "Tech Stack"
type: build
tags:
  - build
  - infrastructure
created: 2026-05-13
updated: 2026-06-20
status: active
area: software
related:
  - "[[system/architecture]]"
  - "[[system/modules/data-layer]]"
---

# Tech Stack

Scelte tecnologiche, orientamenti e snapshot storici del progetto. Ogni voce ha una motivazione o una fonte.

> **Nota editoriale 2026-06-23**: alcune sezioni sotto descrivono una build precedente del repo. Restano utili come **reference design**, ma non vanno lette come inventario affidabile del codice corrente finché la nuova codebase non viene ricostruita.

---

## Linguaggio e runtime

| Componente | Scelta | Motivazione |
|------------|--------|-------------|
| Linguaggio | **Python** | Ecosistema ML/quant maturo, team familiare |
| Architettura | **Monolite modulare** | Sviluppo veloce, debug facile, path evolutivo verso microservizi |
| Schedulazione | **Cron / loop interno** | Swing trading: ciclo ogni 4h o 24h |

## Exchange e connessione

| Componente | Scelta | Motivazione |
|------------|--------|-------------|
| Broker MVP | **Alpaca** (paper) | US equity, developer-first, paper gratuito globale. Stock-only (2026-05-23) |
| Broker prod | **Interactive Brokers (IBKR)** | Copertura ampia (equity int.le, futures, opzioni), API robusta, disponibile in Italia |
| Astrazione broker | **Adapter per broker** | Un wrapper per broker che traduce l'API in interfaccia interna standard → broker intercambiabili come i provider LLM (2026-06-02). Vedi [[system/modules/execution]] |
| Libreria | Alpaca SDK / `ib_insync` · CCXT per futuro multi-asset | SDK ufficiali per equity; CCXT come layer quando si allarga oltre l'equity |
| Tipo ordini | **Limit order + SL + TP** | Obbligatori, hard constraint. Senza SL/TP → drawdown devastanti |
| Costi transazione | **Auto-adattivi dall'adapter** | Commissioni reali esposte dal broker sul momento (no hardcoded) → net performance |

## Database

| Componente | Scelta | Motivazione |
|------------|--------|-------------|
| DB produzione | **PostgreSQL** | Robusto, strutturato, usato da Simone Rizzo (caso simile) |
| DB sviluppo | **SQLite** | Zero setup, stessa interfaccia SQL, sufficiente in locale |
| Schema | 5 tabelle core | `market_data`, `trades`, `portfolio_state`, `module_outputs`, `logs` |

## Backtesting

| Componente | Scelta | Motivazione |
|------------|--------|-------------|
| Framework | **VectorBT** | Usato da MarketSenseAI (paper più rigoroso tra i benchmark). Gestisce costi di transazione. |
| Principio | **Stesso codice del live** | Exchange Module cambia backend (live/backtest), la logica è identica |

## LLM

| Componente | Scelta | Motivazione |
|------------|--------|-------------|
| Router LLM | **OpenRouter** | Intermediario unico verso tutti i provider (Anthropic, Google, Qwen, DeepSeek…). Agilità nel cambiare modello (confermato 2026-05-29) |
| LLM principale | **DeepSeek V4 Pro** | Il più usato su OpenRouter per task finance. Su report NVDA reale (163k in + 20k out token): ~$0,09 vs ~10× di Sonnet 4.6. Open source, eseguibile in locale (vedi 2026-05-29) |
| Output format | **JSON strutturato** | Tutti i framework convergono su questo. Parsing deterministico obbligatorio |
| LLM da monitorare | **Qwen 3 Max** | Vincitore Alpha Arena (+22.88%). Non ancora facilmente accessibile via API |

### Confronto costi modelli ($/milione di token, rilevato 2026-05-29)

| Modello | Input | Output | Costo report NVDA (~183k token) |
|---|---|---|---|
| **DeepSeek V4 Pro** | ~0,40 | ~0,87 | **~$0,09** |
| DeepSeek (provider US) | 1,3 | 2,6 | ~3× DeepSeek base |
| Claude Sonnet 4.6 | 3 | 15 | ~10× DeepSeek |
| GPT-5 (latest) | 5 | 30 | — |
| Claude Opus 4.8 | 10 | 50 | — |

## Storage storico (orientamento 2026-05-29)

| Componente | Scelta | Motivazione |
|------------|--------|-------------|
| Storico long-term | **Hard disk esterni** + clustering/riassunto | Si salva tutto lo storico; oltre una soglia si clusterizza e riassume invece di troncare. Es. 20TB ~500€. Dati vecchi comunque recuperabili online |

## AI Agent Framework

| Componente | Scelta | Motivazione |
|------------|--------|-------------|
| Framework agenti | **Datapizza AI** (`datapizza-ai>=0.1.0`) | Snapshot storico della build precedente. Resta candidato forte, ma la scelta per il nuovo build è da riconfermare. Vedi [[prior-art/libraries/datapizza-ai]] |
| Workflow / grafi | **Datapizza AI Graph** | Snapshot storico della build precedente |
| LLM router | **Datapizza LLM layer** | Supporto multi-provider; da valutare se tenere questa forma anche nella nuova build |
| Debug/Evaluation | *Da definire* | LangSmith rimosso con LangGraph; valutare opzioni Datapizza-native |
| Verifica grafi | *Da definire* | Mermaid LangGraph non più disponibile |

**Contesto storico (2026-06-17)**: una build precedente aveva rimosso LangGraph, LangChain, `llm_clients/`, `structured.py`, `LangSmith` e portato il grafo su Datapizza AI. Questa wiki ora tratta quel passaggio come storia di progetto, non come stato presente garantito.

### Dipendenze principali (snapshot storico 2026-06-20)

```
datapizza-ai>=0.1.0    # Orchestrazione agenti (al posto di LangGraph)
sqlalchemy>=2.0        # ORM / DB
yfinance>=0.2.63       # Dati mercato
stockstats>=0.6.5      # Indicatori tecnici
streamlit>=1.58.0      # Dashboard
plotly>=6.8.0          # Grafici dashboard
ib_async>=2.0          # IBKR adapter
backtrader>=1.9.78     # Backtesting (legacy)
vectorbt>=1.0          # Backtesting (primario, optional)
redis>=6.2.0           # Cache/SSE
typer>=0.21.0          # CLI
rich>=14.0             # Output terminale
```

### Struttura moduli (snapshot storico 2026-06-20)

```
tradingagents/
├── app.py                  # Entry point applicativo
├── cli.py                  # CLI (typer)
├── config.py               # Settings (broker, risk, charter, screening, cycle, data, costs)
├── default_config.py       # Default infrastrutturali (vendors, cache, benchmark)
├── daemon.py               # Daemon background (start/stop/status)
├── benchmark.py            # Benchmark dinamico
├── performance.py          # Metriche performance
├── brain/                  # Datapizza AI graph + agenti
│   ├── datapizza_graph.py  # Grafo agenti (START→desk→PM→Risk→END)
│   ├── datapizza_director.py # Orchestratore (direttore/valutatore/desk)
│   ├── datapizza_llm.py    # LLM wrapper
│   ├── datapizza_tools.py  # Tool binding per agenti
│   ├── prompts.py          # 6 system prompt (desk + PM + Risk)
│   ├── schemas.py          # ResearchState / InvestmentState
│   ├── agent_context.py    # Contesto per-agente
│   ├── context.py          # Context management
│   └── warmup.py           # Warm start (extractor pre-launch)
├── storage/                # DB layer
│   ├── database.py         # Connessione DB
│   ├── models/             # SQLAlchemy models (splittati)
│   │   ├── instrument.py · market.py · portfolio.py
│   │   ├── research.py · trade.py · backtest.py · charter.py
│   └── repository/         # Repository pattern (splittati)
│       ├── instrument.py · market.py · portfolio.py
│       ├── research.py · trades.py · events.py · charter.py
├── domain/                 # Dominio
│   ├── enums.py            # Direction, Conviction, ecc.
│   ├── state.py            # Pydantic state
│   └── risk.py             # Risk engine (ATR, R:R, sizing, guardrail)
├── ingestion/              # Ingresso dati
│   ├── price_ingest.py · news_ingest.py · social_ingest.py
│   ├── fundamentals_ingest.py · macro_ingest.py
│   └── screening.py        # Screening deterministico
├── indicators/             # Indicatori tecnici
│   ├── core.py · db.py
├── broker/                 # Adapter broker
│   ├── base.py · paper.py · alpaca.py · ibkr.py
│   └── commission.py
├── execution/              # Esecuzione trade
│   ├── trade.py · submit.py · exits.py · costs.py
│   ├── portfolio_risk.py · mantainer.py · disinvest.py
│   └── helpers.py
├── orchestration/          # Ciclo di vita
│   ├── cycle.py            # run_cycle / run_forever
│   ├── triggers.py         # Trigger Engine
│   └── datapizza_analyze.py # Analyzer hook per Datapizza
├── dataflows/              # Vendor data fetchers
│   ├── y_finance.py · yfinance_news.py
│   ├── stocktwits.py · reddit.py
│   ├── alpha_vantage_*.py (stock/indicator/news/fundamentals/common)
│   ├── stockstats_utils.py · interface.py · utils.py · config.py
├── tools/                  # Tool per agenti
│   ├── market.py · options.py · portfolio.py
├── universe/               # Universo investibile
│   ├── sources.py · sync.py
├── backtesting/            # Backtesting
│   ├── engine.py · engine_vbt.py · scheduler.py
└── dashboard/              # Streamlit dashboard
    ├── app.py              # App entry
    ├── db_reader.py · metrics.py
    ├── components/         # Sidebar, metrics components
    └── pages/              # Overview, ticker, trades, decisions, watchlist, system
```

## Post-MVP (non decidere ora)

| Componente | Candidato | Quando |
|------------|-----------|--------|
| Portfolio optimizer | cvx-portfolio-optimizer (skfolio) | Dopo che i componenti core girano |
| Fine-tuning | LoRA/QLoRA su modello open-source | Dopo anni di storico |

---
## Commenti recuperati da iCloud (2026-07-01)

> Commenti Obsidian `%%...%%` presenti nella vecchia copia iCloud (`7054827`) e reinseriti senza sovrascrivere il contenuto corrente.

%% diciamo che la predisposizione degli alert e i next check date ci permette di non inserire dei cron statici periodici %%

%% sto anche pensando di realizzare il solo frontend in typescript %%

%% il modulo di back test vorrei che sia disponibile anche come strumenti per l’utente sul frontend per permettergli di fare backest personalizzati fino a se stessi ma persistenti (quindi con meccanismo di salvataggio sul db%%

%% proprio perche datapizza AI è un po acerbo e poco completo, in lido di nuovo la scelta tra langgraph e datapizza AI come da prendere %%

%% struttura completamente da rifare %%

