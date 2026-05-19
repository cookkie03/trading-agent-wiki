---
title: "System Map"
type: build
tags:
  - build
  - architecture
created: 2026-04-30
updated: 2026-05-13
status: active
priority: high
area: software
related:
  - "[[build/mvp-prototype-design]]"
  - "[[build/stack]]"
  - "[[build/modules/module-a-exchange-db]]"
  - "[[build/modules/module-c-quant-backtest]]"
  - "[[build/modules/module-d-prompt-builder-trader]]"
  - "[[build/modules/risk-analyst]]"
sources:
  - "[[references/conversazione-luca-salvatore-2026-04-28-30]]"
  - "[[references/videochiamata-luca-salvatore-2026-04-30]]"
  - "[[references/videochiamata-luca-salvatore-2026-05-13]]"
---

# System Map

Architettura completa del `trading-agent`. Il sistema replica e automatizza il workflow di un trader: raccogliere informazioni, analizzare, decidere, eseguire, imparare.

---

## Principi fondanti

**Principio deterministico**: l'LLM fa solo il ragionamento finale. Tutto il resto (calcoli, raccolta dati, esecuzione ordini) è Python puro. Dato lo stesso input, ottieni sempre lo stesso output.

**Modularità**: ogni modulo è un blocco con input e output definiti, scrivibile e leggibile dal DB centrale. Si può sostituire, pesare dinamicamente o disabilitare senza toccare il resto del sistema.

**DB come hub centrale**: tutti i moduli scrivono qui; il Prompt Builder legge da qui. L'unica fonte di verità del sistema.

---

## Ciclo operativo (MVP)

```
Data Ingestion
  │
  ├── TAVOLO (in parallelo):
  │     ├── Analista      → ratio finanziari, validazione news
  │     ├── News Agent    → sentiment elaborato su news
  │     └── Quant Agent   → segnali tecnici e quantitativi (Modulo C)
  │
  ├── Risk Analyst Agent  ← upstream — imposta paletti prima del Trader
  │     └── produce: VaR, esposizione max, range SL/TP, go/no-go
  │
  ├── Prompt Builder      → assembla deterministicamente tutti gli output
  │
  ├── Trader Agent (LLM)  ← decide dentro i paletti del Risk Analyst
  │     └── produce JSON: asset, direzione, entry, SL, TP, leva, reasoning
  │
  ├── Security Module     → hard limits deterministici (statuto del fondo)
  ├── Portfolio Allocator → size finale in base al portafoglio corrente
  ├── Exchange Module     → Binance Testnet (live) | replay storico (backtest)
  └── Logger              → trade, chain-of-thought, metriche nel DB
```

**Frequenza**: ogni 4h o 24h (swing trading). Schedulato come cron job.

---

## Layer 1 — DB Centrale

Unico punto di verità. Tutti i moduli leggono e scrivono qui.

| Tabella | Contenuto |
|---------|-----------|
| `market_data` | OHLCV, order book, timestamp da Binance |
| `module_outputs` | Output JSON di ogni modulo per ogni ciclo |
| `trades` | Ogni ordine: entry, SL, TP, esito, P&L |
| `portfolio_state` | Posizioni correnti, liquidità, esposizione |
| `logs` | Log di sistema, errori, chain-of-thought LLM |

---

## Layer 2 — Moduli di Analisi

Ogni modulo è parametrizzabile — accetta parametri in input, non valori hardcodati.

| Modulo | Funzione | Stato |
|--------|----------|-------|
| **Quant Agent** | Segnali tecnici e quantitativi → [[build/modules/module-c-quant-backtest]] | Track 2 |
| News Agent | Sentiment news, Fear & Greed, whale alerts | Post-MVP |
| Analista | Ratio finanziari, validazione fondamentali | Post-MVP |
| Factor Investigation Agent | Quali fattori includere nel modello; coefficienti empirici | Post-MVP |
| Prediction Agent (DL) | Relazioni non lineari fattori → prezzo | Post-MVP avanzato |

---

## Layer 3 — Decisione

| Componente | Funzione | Tipo |
|------------|----------|------|
| **Risk Analyst** | Paletti dinamici upstream → [[build/modules/risk-analyst]] | Post-MVP |
| **Prompt Builder** | Assembla deterministicamente tutti gli output → [[build/modules/module-d-prompt-builder-trader]] | Track 3 |
| **LLM Trader** | Ragionamento finale → JSON con proposta trade | LLM (DeepSeek) |

---

## Layer 4 — Esecuzione e Controllo

| Componente | Funzione | Tipo |
|------------|----------|------|
| Security Module | Valida proposta contro statuto del fondo (hard limits) | Python deterministico |
| Portfolio Allocator | Calcola size finale in base al portafoglio | Python (post-MVP: cvx-optimizer) |
| **Exchange Module** | Esegue ordini → [[build/modules/module-a-exchange-db]] | CCXT + Binance API |
| Logger | Logga tutto nel DB | Python |

---

## Layer 5 — UI e Apprendimento

| Componente | Funzione | Stato |
|------------|----------|-------|
| Streamlit Dashboard | Sola lettura: equity curve, posizioni, metriche | Post-MVP |
| Telegram Bot | Notifiche trade in tempo reale | Post-MVP |
| RL / Weighting Module | Ponderazione dinamica dei moduli su esiti storici | Post-MVP avanzato |
| Fine-Tuning Module | Riaddestramento LLM su storico del progetto | Post-MVP avanzato |

---

## Protocollo di comunicazione

Tutti i moduli comunicano via DB, non via chiamate dirette:
1. **Moduli → DB**: ogni modulo produce un report JSON in `module_outputs`
2. **DB → Prompt Builder**: il Builder estrae i campi rilevanti e li assembla nel template
3. **Prompt → LLM**: l'agente riceve un prompt denso e strutturato, non chat free-form

Questo evita l'effetto "telefono senza fili" (degradazione informazioni nei prompt lunghi).

---

## Sequenza di sviluppo

| Track | Chi | Moduli |
|-------|-----|--------|
| Track 1 | Luca solo | [[build/modules/module-a-exchange-db]] |
| Track 2 | Luca + Salvatore | [[build/modules/module-c-quant-backtest]] |
| Track 3 | dopo Track 1 | [[build/modules/module-d-prompt-builder-trader]] |
| Post-MVP | tutto il team | Risk Analyst, News Agent, Security Module, Portfolio Allocator |

---

*Per le decisioni tecniche vedere [[build/decision-log]]. Per il piano MVP vedere [[build/mvp-prototype-design]].*
