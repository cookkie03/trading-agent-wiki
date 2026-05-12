---
title: Backlog
type: ops
tags:
  - ops
  - execution
created: 2026-04-30
updated: 2026-04-30
status: active
related:
  - "[[ops/dashboard]]"
  - "[[kanban-project-status]]"
confidence: high
priority: high
area: ops
sources:
  - "[[references/conversazione-luca-salvatore-2026-04-28-30]]"
  - "[[references/videochiamata-luca-salvatore-2026-04-30]]"
---

# Backlog

Backlog operativo per il progetto `trading-agent`.

## Now

- [x] Ingestire le conversazioni progettuali del 30 aprile
- [x] Aggiornare la mappa del sistema [[build/system-map]] con l'approccio multi-agente
- [x] Registrare le decisioni chiuse in [[decisions/decision-log]]
- [x] Aggiornare le domande aperte con le nuove emerse dalla videochiamata 04-30
- [ ] **Analizzare FinAgent** (Cornell, ~50k stelle GitHub): studiare architettura, paper (38 pag.), e distillare le parti rilevanti nel wiki
- [ ] **Analizzare AlphaArena**: confronto LLM su Bitcoin, capire cosa ha funzionato
- [ ] **Analizzare NeuroEspresso** (Silvio Baratto): approccio multi-agente, repository e documentazione
- [ ] Definire gli artifact necessari: quali mappe mentali e kanban board vogliamo avere

## Next

- [ ] Progettazione I/O granulare per ogni modulo (metodologia input → output → build)
  - Priorità: Prompt Builder, News Module, Factor Quantification, Prediction Module
- [ ] Creare il primo artifact visuale (.canvas) dell'architettura multi-agente aggiornata
- [ ] Valutare il modulo Sentiment degli Analisti: è realizzabile? Raccogliere informazioni su approcci esistenti
- [ ] Backtest comparativi TA vs no-TA (quando ci sarà il primo sistema funzionante)

## Later

- [ ] Implementazione della dashboard Streamlit (basata su SFC Investment Fund — link in `raw/articles/`)
- [ ] Pipeline di logging completa (chain-of-thought + esito trade)
- [ ] Progettazione del modulo RL / Weighting
- [ ] Integrazione Telegram Bot per notifiche
- [ ] Valutare switch a exchange decentralizzato anonimo (post-profitti significativi)
