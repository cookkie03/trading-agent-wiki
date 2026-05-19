---
title: "Tech Stack"
type: build
tags:
  - build
  - infrastructure
created: 2026-05-13
updated: 2026-05-13
status: active
area: software
related:
  - "[[build/system-map]]"
  - "[[build/modules/module-a-exchange-db]]"
---

# Tech Stack

Scelte tecnologiche confermate per il progetto. Ogni voce ha una motivazione o una fonte.

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
| Exchange MVP | **Binance Testnet** | Paper trading, zero rischio, API complete, dati storici |
| Libreria exchange | **CCXT** | Supporta 100+ exchange con stessa interfaccia — cambio exchange = cambio config |
| Tipo ordini | **Limit order + SL + TP** | Obbligatori, hard constraint. Senza SL/TP → drawdown devastanti |

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
| LLM principale | **DeepSeek** | Alpha Arena: 2° posto (+4.76%), 1/30 del costo di GPT-5. Miglior costo/perf disponibile |
| Output format | **JSON strutturato** | Tutti i framework convergono su questo. Parsing deterministico obbligatorio |
| LLM da monitorare | **Qwen 3 Max** | Vincitore Alpha Arena (+22.88%). Non ancora facilmente accessibile via API |

## Post-MVP (non decidere ora)

| Componente | Candidato | Quando |
|------------|-----------|--------|
| Portfolio optimizer | cvx-portfolio-optimizer (skfolio) | Dopo che A+C+D girano |
| Framework multi-agente | da valutare (LangGraph, AutoGen, custom) | Dopo MVP funzionante |
| Fine-tuning | LoRA/QLoRA su modello open-source | Dopo anni di storico |
