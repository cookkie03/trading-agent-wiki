---
title: "Modulo D — Prompt Builder + LLM Trader"
type: build
tags:
  - build
  - multi-agent
  - architecture
created: 2026-05-13
updated: 2026-05-21
status: active
priority: medium
area: software
related:
  - "[[build/system-map]]"
  - "[[build/modules/module-a-exchange-db]]"
  - "[[build/modules/module-c-quant-backtest]]"
  - "[[build/modules/risk-analyst]]"
  - "[[references/tradingagents-code-wiki]]"
  - "[[references/external/trading-agents-framework]]"
---

# Modulo D — Prompt Builder + LLM Trader

Track 3 (dopo Modulo A). Il modulo che assembla tutti gli output del sistema e invoca l'LLM per la decisione di trade finale.

---

## Funzione

1. **Prompt Builder**: legge dal DB gli output di tutti i moduli (Quant Agent, News Agent, Risk Analyst, ecc.) e li assembla deterministicamente in un prompt strutturato per l'LLM
2. **LLM Trader**: riceve il prompt, ragiona dentro i paletti definiti dal Risk Analyst, produce un JSON con la proposta di trade

Output JSON obbligatorio: `{ asset, direction, entry, SL, TP, leverage, reasoning }`.

---

## Filosofia degli Agenti

*Emersa dalla lettura del codebase TradingAgents (2026-05-19). Punto di partenza: [[references/tradingagents-code-wiki]]*

### Principio guida: pochi agenti, tanti tool potenti

Il sistema TradingAgents usa molti agenti con ruoli separati (Analysts → Researchers → Risk Debaters → Managers → Trader). La nostra variante mira a **efficientare drasticamente** questa architettura:

- **Analysts** → non sono agenti LLM ma un **layer di moduli deterministici** che forniscono dati già pronti al layer successivo
  - News: gestite con RAG
  - Indicatori tecnici: calcolati automaticamente dal DB con formule
  - Social media sentiment: RAG oppure sintesi con tag multipli (ticker, horizon, data/ora, ecc.)
  - Fondamentali: raccolti e parsati da un modellino locale; metriche bilancio (revenues, EBIT, ecc.) caricate nel DB; eventualmente sintesi LLM-ready allegate
- **Researchers** (Bull/Bear debate) → architettura da valutare criticamente; la divisione in due agenti potrebbe essere inefficiente
- **Risk Management Debaters** → da riesaminare; ipotesi preferita: un agente strategia + un agente rules (portfolio constraints), entrambi orientati a massimizzare profitto analizzando scenari con tool appositi
- **Managers + Trader** → ridurre al minimo; riformulare ispirandosi ai workflow degli investitori istituzionali reali

### Tool-centric design

Ogni agente deve potersi collegare a tool completi e versatili. La selezione e progettazione dei tool è di **fondamentale rilevanza**: dare quanta più completezza di informazioni possibili con quanta meno latenza possibile.

Per ogni tool ereditato dal fork TradingAgents: valutare se tenerlo, potenziarlo o riscriverlo da zero.

Fonti di ispirazione per i tool: sezione "Data Retrieval Tools and Utilities" di [[references/tradingagents-code-wiki]] — Fundamental Data e News/Insider Transactions tools sono buoni punti di partenza.

---

## State Management e Schemas

Obiettivo: **pochi schema molto potenti e dettagliati**, non tanti schema frammentati.

Pattern da TradingAgents da adottare:
- **TypedDict** per gli state di workflow (propagati tra i nodi del grafo)
- **Pydantic** per gli output strutturati degli LLM (con field descriptions come istruzioni)
- **Fallback a free-text** quando structured output non è disponibile o fallisce

Ogni state deve salvare automaticamente le informazioni rilevanti nella memoria del sistema (log).

Buona la gestione degli structured output con fallback in plain text: prevenire interruzioni del pipeline.

---

## Multi-Agent Debate: Mantenerlo o No?

Il debate a 3 agenti per il Risk Management (aggressivo, neutrale, conservativo) ha un vantaggio reale: copertura di angolazioni estreme che un singolo agente potrebbe ignorare (es. extraterritorialità dei ricavi, rischio cambio su mercati esteri).

**Ipotesi**: mantenere il debate se efficientato — ridurre il numero di agenti e affinare i system prompt. Non eliminarlo a priori.

Da investigare: pro e contro della struttura a debate rispetto a un singolo agente multi-prospettiva.

---

## Orchestrazione: LangGraph

Molto probabile che il progetto utilizzi **LangGraph** per i workflow e **LangChain** per gli agenti, partendo come fork di TradingAgents.

Pattern di LangGraph utili da adottare:
- `StateGraph` con nodi = agenti, edges = logica condizionale
- `ConditionalLogic` per routing dinamico in base all'`AgentState`
- `Propagator` per inizializzare lo state con contesto storico
- Checkpointing SQLite per-ticker per resume in caso di crash

---

## Dipendenze

- Legge da: DB centrale (`module_outputs`, `market_data`, `portfolio_state`)
- Produce: proposta trade JSON → Security Module
- Upstream: [[build/modules/risk-analyst]] (paletti), [[build/modules/module-c-quant-backtest]] (segnali quant)
- Downstream: Security Module → Portfolio Allocator → [[build/modules/module-a-exchange-db]]

---

## TODO / Decisioni aperte

- Frequenza di invocazione dell'LLM Trader (vincolo costo token + latenza moduli upstream)
- Valutare architettura debate: quanti agenti, quali prospettive, se mantenerlo
- Definire schema finale AgentState e output JSON del Trader
- Brainstorming: replicare i workflow degli uffici di un investitore istituzionale
