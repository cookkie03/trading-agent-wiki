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

**Fase attuale**: design dell'architettura multi-agente **stock-only** (paper trading equity). Topologia 2026-05-29: analisti → research_state → Risk Analyst (gate bear) → Trade deterministico, con un Portfolio Manager orchestratore e un DB esteso. Stack: LangGraph + OpenRouter/DeepSeek V4 Pro. Si riscrive il grafo partendo dalla base di TradingAgents.

---

## Ingresso rapido

| Vuoi... | Vai a... |
|---------|----------|
| Capire come funziona il sistema | [[build/system-map]] |
| Vedere cosa si sta costruendo ora | [[artifacts/project-board]] |
| Vedere il piano MVP completo | [[build/mvp-prototype-design]] |
| Trovare un termine che non conosci | [[_meta/glossario]] |
| Vedere tutte le decisioni prese | [[build/decision-log]] |
| Trovare una fonte o un paper | [[_meta/index]] |

---

## Struttura della wiki

```
wiki/
├── build/          ← spec software (Luca): architettura, moduli, stack, decisioni
├── strategy/       ← conoscenza di mercato (Salvatore): metodi, indicatori, metriche
├── references/     ← fonti ingestite (call, paper, librerie, articoli)
│   └── external/   ← framework e librerie terze parti
├── syntheses/      ← analisi trasversali multi-fonte
├── artifacts/      ← canvas, roadmap, board di lavoro
└── _meta/          ← navigazione vault (index, log, glossario, taxonomy)
```

---

## Flusso di lavoro

```
raw/           → wiki-ingest →  references/    (fonti)
                             →  syntheses/     (analisi)
                             →  build/         (spec aggiornate)
artifacts/     → boards Luca e Salvatore       (task e decisioni)
```

**Luca**: carica materiale tecnico in `raw/`, aggiorna i moduli in `build/`, aggiorna la board.
**Salvatore**: carica in `raw/` indicatori, strategie, meccanismi di mercato, casi reali. L'agente struttura il materiale in `strategy/`.

---

*Indice completo: [[_meta/index]]*
