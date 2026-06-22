---
title: "System Wiki Reorganization"
type: build
tags:
  - architecture
  - roadmap
  - software
created: 2026-06-23
updated: 2026-06-23
status: active
confidence: medium
area: ops
related:
  - "[[artifacts/project-board]]"
  - "[[system/codebase-architecture]]"
  - "[[system/decision-log]]"
---

# System Wiki Reorganization

Pagina di lavoro per ripulire `wiki/system/` senza perdere informazione.

## Obiettivo

Rendere `wiki/system/` leggibile e ordinata per un umano che deve progettare o implementare il codice oggi, distinguendo bene:

- **design attuale**;
- **contesto storico**;
- **backlog operativo**;
- **idee future**.

## Problemi rilevati

- Molte pagine mischiano design, storia di branch e stato operativo corrente.
- In più punti compaiono claim `🟢 Implementato` o `✅` che non rappresentano il codice attuale.
- Alcuni task erano rimasti solo in commenti `%%...%%` o nelle daily notes.

## Policy editoriale adottata

- I claim di implementazione non vengono cancellati brutalmente: diventano **contesto storico** o **reference design**.
- Le pagine operative devono parlare al presente solo quando descrivono decisioni ancora valide.
- I task escono dai commenti e finiscono in board o in pagine dedicate.
- Le informazioni scartate non si eliminano: si archiviano, si assorbono in pagine migliori o si spostano nei log.

## Candidati a sottosezioni future

- `system/agents/`
- `system/data/`
- `system/execution/`
- `system/frontend/`
- `system/orchestration/`
- `system/quant/`

## Deliverable di questo ingest

- board semplificata e riallineata;
- pagine hub nuove per codebase, fonti/tool, frontend e reorg;
- prime correzioni sulle pagine che falsavano di più lo stato del progetto.
