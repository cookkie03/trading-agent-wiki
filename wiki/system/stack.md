---
title: "Tech Stack"
type: build
tags:
  - build
  - infrastructure
created: 2026-05-13
updated: 2026-05-29
status: active
area: software
related:
  - "[[system/architecture]]"
  - "[[system/modules/data-layer]]"
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
| Framework agenti | **LangChain** | Confermato 2026-05-23. Ecosistema maturo, ben mantenuto, usato anche da TradingAgents (base del fork) |
| Workflow / grafi | **LangGraph** | StateGraph con nodi = agenti, edges = logica condizionale, checkpointing SQLite per-ticker |
| Debug agenti | **LangSmith** | Piattaforma di tracing e debugging integrata nell'ecosistema LangChain |
| Evaluation | **LangSmith CLI** | Evaluation automatica degli agenti nel terminale (VS Code) |
| Verifica grafi | **Mermaid (LangGraph built-in)** | LangGraph genera diagrammi Mermaid dei grafi — usare per verificare struttura con coding agent |

### Struttura repo (orientamento 2026-05-23)

- Un subfolder per ogni componente/agente del sistema
- Un subfolder dedicato alle **liste di tool** disponibili per gli agenti

## Post-MVP (non decidere ora)

| Componente | Candidato | Quando |
|------------|-----------|--------|
| Portfolio optimizer | cvx-portfolio-optimizer (skfolio) | Dopo che i componenti core girano |
| Fine-tuning | LoRA/QLoRA su modello open-source | Dopo anni di storico |
