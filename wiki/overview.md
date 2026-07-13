---
title: "Trading Agent — Overview"
type: overview
tags:
  - overview
  - strategy
created: 2026-04-30
updated: 2026-07-13
status: active
related: []
confidence: high
---

# Trading Agent

Wiki operativa del progetto `trading-agent`. Raccoglie fonti, documenta il software, traccia le decisioni e mantiene visibile lo stato del progetto. Consultabile da agenti AI e da umani.

---

## Cos'è il progetto

Un sistema multi-agente che replica e automatizza il workflow di un trader professionale: raccogliere informazioni, analizzare segnali quantitativi, decidere con un LLM, eseguire ordini deterministicamente.

**Fase attuale**: specificazione ordinata dell'architettura multi-agente **stock-only / USD-only** per paper trading equity. La wiki definisce requisiti, decisioni e priorità; il repository è esterno e il suo stato non viene attestato qui. Framework documentato: LangGraph + LangSmith; topologia e confini restano in revisione con Luca e Salvatore.

---

## Ingresso rapido

| Vuoi... | Vai a... |
|---------|----------|
| Capire come funziona il sistema | [[system/foundation/architecture]] |
| Vedere cosa si sta costruendo ora | [[artifacts/project-board]] |
| Vedere il piano MVP completo | [[system/foundation/mvp]] |
| Trovare un termine che non conosci | [[_meta/glossario]] |
| Vedere tutte le decisioni prese | [[system/foundation/decision-log]] |
| Trovare una fonte o un paper | [[_meta/index]] |

---

## Struttura della wiki

```
wiki/
├── system/         ← spec software (Luca)
│   ├── foundation/ · data/ · tools/ · agents/ · orchestration/
│   ├── investment/ · execution/ · quant/ · interface/
│   └── _reference/ ← snapshot e pattern storici
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

I record grezzi delle call restano in `raw/archived/`; la loro sostanza è dissolta nelle pagine tematiche (decisioni datate in `system/foundation/decision-log`).

**Luca**: carica materiale tecnico in `raw/`, aggiorna le pagine del dominio pertinente in `system/`, aggiorna la board.
**Salvatore**: carica in `raw/` indicatori, strategie, meccanismi di mercato, casi reali. L'agente struttura il materiale in `strategy/`.

---

*Indice completo: [[_meta/index]]*
