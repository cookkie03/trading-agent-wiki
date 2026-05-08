---
title: "Kanban — Stato Progetto"
type: ops
tags:
  - ops
  - execution
  - roadmap
created: 2026-04-30
updated: 2026-05-06
status: active
related:
  - "[[ops/dashboard]]"
  - "[[ops/current-state]]"
  - "[[ops/backlog]]"
  - "[[build/system-map]]"
  - "[[decisions/decision-log]]"
  - "[[questions/open-questions]]"
confidence: high
priority: high
area: ops
kanban-plugin: board
sources:
  - "[[sources/conversazione-luca-salvatore-2026-04-28-30]]"
  - "[[sources/notion-export-investimento-trading]]"
  - "[[sources/trading-floor-canvas]]"
---

# Kanban — Stato Progetto

Board operativa per tracciare i progressi dello sviluppo del Trading Agent e della Wiki.

## To Do (Backlog)

- [ ] Definire la struttura Input/Output del modulo **News Research Agent**
- [ ] Definire la struttura Input/Output del modulo **Risk Analyst Agent**
- [ ] Definire la struttura Input/Output del modulo **Analista (Ratio/Grafici)**
- [ ] Iniziare la ricerca sui progetti citati: Alfa Arena, NeuroEspresso, Cornell Paper
- [ ] Definire metriche di portafoglio specifiche (drawdown, rendimento, esposizione) per la dashboard Streamlit
- [ ] Registrare ufficialmente la decisione "Dashboard di Augmentazione" in [[decisions/decision-log]]

## In Progress

- [ ] Progettazione granulare dei moduli e delle interazioni (basandosi sul Trading Floor Canvas)

## Blocked / Decisioni Da Chiudere

- [ ] Scelta mercato iniziale: Crypto vs Equity (Tensione aperta: Equity ha metriche forti, Crypto ha API facili. Decisione bloccante per l'implementazione pratica del data ingestion)

## Done

- [x] Ingestire l'export Notion su Investimenti e Trading (Teoria, TA, DeFi, Risk Management)
- [x] Consolidare l'architettura Multi-Agente in un `Trading Floor Canvas` e nella wiki
- [x] Ingestire i transcript della videochiamata del 30 aprile
- [x] Inizializzare repository Git ed eseguire il primo commit
- [x] Inizializzare la struttura base del vault
- [x] Formalizzare uno snapshot iniziale in [[ops/current-state]]

## Note Di Lettura

- Sposta i task man mano che il progetto evolve.
- Usa le doppie parentesi `[[nome pagina]]` per linkare task alle note della wiki.
