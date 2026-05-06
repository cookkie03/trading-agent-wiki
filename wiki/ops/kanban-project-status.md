---
title: "Kanban — Stato Progetto"
type: ops
tags:
  - ops
  - execution
  - roadmap
created: 2026-04-30
updated: 2026-04-30
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
---

# Kanban — Stato Progetto

Board operativa costruita sullo stato reale del vault al 2026-04-30.

## Done

- [x] Inizializzare la struttura base del vault
- [x] Ingestire il primo source reale in [[sources/conversazione-luca-salvatore-2026-04-28-30]]
- [x] Formalizzare uno snapshot iniziale in [[ops/current-state]]
- [x] Aprire un backlog operativo in [[ops/backlog]]

## In Progress

- [ ] Fase 1: Progettazione granulare Input/Output per i moduli core (News, TA, Risk)
- [ ] Ricerca e studio progetti esistenti (Alfa Arena, NeuroEspresso, Cornell Paper)
- [ ] Definire l'architettura Multi-Agente in [[build/system-map]]
- [ ] Registrare la decisione sul framing (Dashboard di Augmentazione prima dell'autonomia) in [[decisions/decision-log]]

## Blocked / Decisioni Da Chiudere

- [ ] Scelta mercato iniziale: Crypto vs Equity (Tensione ancora aperta, ma orientata allo scratch build)
- [ ] Definire metriche di portafoglio specifiche (drawdown, rendimento, esposizione) per la dashboard Streamlit

## Later

- [ ] Disegnare la pipeline di logging e auto-miglioramento dei moduli
- [ ] Definire il modulo news / sentiment
- [ ] Definire il modulo portfolio / risk management
- [ ] Creare board separate per research, build e validation quando i workstream saranno piu nitidi

## Note Di Lettura

- Questa board non rappresenta ancora execution software vera e propria.
- Lo stato attuale del progetto e soprattutto di framing, ricerca e decisione architetturale.
- Quando una decisione viene chiusa, spostare il task da `Blocked / Decisioni Da Chiudere` a `Done` o promuovere i task derivati in `In Progress`.
