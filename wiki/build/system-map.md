---
title: "System Map"
type: build
tags:
  - build
  - architecture
created: 2026-04-30
updated: 2026-04-30
status: draft
related:
  - "[[build/build]]"
  - "[[concepts/modular-trading-agent-architecture]]"
  - "[[artifacts/artifacts]]"
confidence: high
priority: high
area: software
sources:
  - "[[sources/conversazione-luca-salvatore-2026-04-28-30]]"
  - "[[sources/videochiamata-luca-salvatore-2026-04-30]]"
---

# System Map

Mappa dell'architettura software del `trading-agent`. Il sistema è progettato per essere un ecosistema modulare che supporta inizialmente un workflow di **augmentazione** per il trader.

## Componenti Architetturali

### 1. Data & Persistence Layer (The DB)
- **Market State**: Prezzi, volumi, order book.
- **News/Sentiment Store**: Feed di notizie pre-elaborate.
- **Factor Study Hub**: Database dei fattori quantificati.
- **Trade History & Reasoning Log**: Memoria storica di ogni trade e della relativa "Chain of Thought" dell'agente.
- **Portfolio & Risks**: Stato corrente delle posizioni, drawdown, margini.

### 2. Research & Intelligence (Multi-Agent Team)
- **News Analyst**: Agente focalizzato sull'interpretazione delle notizie.
- **Technical Analyst**: Agente focalizzato su pattern grafici e soglie psicologiche.
- **Economist Agent**: Analisi di paper e modelli macroeconomici per estrarre nuovi fattori.
- **Optimizer / RL Module**: Sistema di ponderazione dinamica dei vari input.

### 3. Execution & Control
- **Trader Agent**: Orchestratore che sintetizza gli input e propone i trade.
- **Risk Manager**: Filtro finale che valida le proposte contro vincoli di rischio e regole di protezione (es. Trailing Stop).
- **Execution Manager**: Interfaccia con i broker/exchange per l'esecuzione degli ordini.

### 4. UI & Monitoring Layer
- **Streamlit Dashboard**: Visualizzazione avanzata delle metriche di portafoglio (ispirata a SFC Investment Fund).
- **Telegram Interface**: Bot per notifiche e controllo remoto rapido.

## Flussi Principali

1. **Ingest & Enrich**: I dati grezzi entrano nel DB, i moduli di intelligence estraggono segnali.
2. **Consultation**: Il Trader Agent interroga i vari specialisti (News, TA, Economist).
3. **Drafting**: Viene creata una proposta di operazione completa di parametri (SL, TP, Leva).
4. **Validation**: Il Risk Manager approva o rigetta la proposta.
5. **Learning**: L'esito del trade viene loggato e analizzato dal modulo di Fine-Tuning per migliorare le performance future.

## Roadmap di Implementazione
- **Fase 1 (Dashboard)**: Visualizzazione dati e analisi manuale supportata da agenti.
- **Fase 2 (Augmentation)**: Proposte di trade generate dall'agente per l'approvazione umana.
- **Fase 3 (Autonomy)**: Esecuzione automatica con supervisione e kill-switch.
