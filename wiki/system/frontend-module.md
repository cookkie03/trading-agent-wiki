---
title: "Frontend Module"
type: build
tags:
  - architecture
  - software
  - roadmap
created: 2026-06-23
updated: 2026-06-23
status: active
confidence: medium
area: software
related:
  - "[[system/codebase-architecture]]"
  - "[[system/observability-dashboard]]"
  - "[[artifacts/project-board]]"
---

# Frontend Module

Vincolo architetturale emerso dalle daily notes: il frontend deve essere **un modulo a sé, intercambiabile**, così da poter passare in futuro da Streamlit a un frontend TypeScript senza toccare il core del sistema.

## Requisiti

- Il core applicativo non deve dipendere da un framework UI specifico.
- Il frontend legge stato, metriche, portfolio, log e decisioni tramite contratti stabili.
- Streamlit può essere il primo adapter UI, non il vincolo definitivo.
- Una futura UI TypeScript deve poter sostituire il modulo frontend con cambi minimi fuori dal suo boundary.

## Conseguenze per la codebase

- Separare chiaramente `frontend/` dal resto della business logic.
- Esporre interfacce di lettura semplici per dashboard e observability.
- Evitare di nascondere logica critica dentro componenti Streamlit.

## Collegamenti

- Pianificazione codebase: [[system/codebase-architecture]]
- Dashboard osservabilità: [[system/observability-dashboard]]
