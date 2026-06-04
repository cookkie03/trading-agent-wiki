---
title: "Trading Agent — Overview"
type: overview
tags:
  - overview
  - strategy
created: 2026-04-30
updated: 2026-05-29
status: active
related: []
confidence: high
---

# Trading Agent

Wiki operativa del progetto `trading-agent`. Raccoglie fonti, documenta il software, traccia le decisioni e mantiene visibile lo stato del progetto. Consultabile da agenti AI e da umani.

---

## Cos'è il progetto

Un sistema multi-agente che replica e automatizza il workflow di un trader professionale: raccogliere informazioni, analizzare segnali quantitativi, decidere con un LLM, eseguire ordini deterministicamente.

**Fase attuale**: design dell'architettura multi-agente **stock-only** ([[_meta/glossario#Paper Trading / Testnet|paper trading]] equity). Topologia 2026-05-29: analisti → research_state → Risk Analyst (gate bear) → Trade deterministico, con un Portfolio Manager orchestratore e un DB esteso. Stack: LangGraph + OpenRouter/DeepSeek V4 Pro. Si riscrive il grafo partendo dalla base di TradingAgents.

---

## Ingresso rapido

| Vuoi... | Vai a... |
|---------|----------|
| Capire come funziona il sistema | [[system/architecture]] |
| Vedere cosa si sta costruendo ora | [[artifacts/project-board]] |
| Vedere il piano MVP completo | [[system/mvp]] |
| Trovare un termine che non conosci | [[_meta/glossario]] |
| Vedere tutte le decisioni prese | [[system/decision-log]] |
| Trovare una fonte o un paper | [[_meta/index]] |

---

## Struttura della wiki

```
wiki/
├── system/         ← spec software (Luca): architettura, moduli, stack, decisioni, MVP
│   └── modules/    ← data-layer · agents · execution · quant-backtesting
├── strategy/       ← conoscenza di mercato (Salvatore): metodi, indicatori, metriche
├── prior-art/      ← sistemi/paper/librerie esterni studiati e forkati
│   ├── tradingagents/ · libraries/ · papers/
├── syntheses/      ← analisi trasversali multi-fonte
├── artifacts/      ← canvas, board di lavoro
└── _meta/          ← navigazione vault (index, log, glossario, taxonomy, onboarding)
```

---

## Flusso di lavoro

```
raw/           → wiki-ingest →  prior-art/     (sistemi/paper esterni)
                             →  syntheses/     (analisi)
                             →  system/        (spec software aggiornate)
                             →  strategy/      (conoscenza di mercato)
artifacts/     → project-board                 (task e decisioni)
```

I record grezzi delle call restano in `raw/archived/`; la loro sostanza è dissolta nelle pagine tematiche (decisioni datate in `system/decision-log`).

**Luca**: carica materiale tecnico in `raw/`, aggiorna i moduli in `system/modules/`, aggiorna la board.
**Salvatore**: carica in `raw/` indicatori, strategie, meccanismi di mercato, casi reali. L'agente struttura il materiale in `strategy/`.

---

*Indice completo: [[_meta/index]]*
