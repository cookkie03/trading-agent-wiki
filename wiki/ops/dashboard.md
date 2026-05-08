---
title: "Ops Dashboard"
type: ops
tags:
  - ops
  - execution
  - roadmap
created: 2026-04-30
updated: 2026-04-30
status: active
related:
  - "[[ops/ops]]"
  - "[[overview]]"
confidence: high
priority: high
area: ops
---

# Ops Dashboard

Pagina operativa principale del vault.

## Focus attuale

> [!todo]
> Compilare questa sezione all'inizio di ogni sessione o quando cambia il focus del progetto.

- Obiettivo corrente: chiarire architettura iniziale e mercato target
- Outcome desiderato: definire un primo MVP realistico
- Blocco principale: troppe ipotesi aperte su valutazione mercati e grado di autonomia del sistema

## Workstream attivi

- [x] Definire i workstream iniziali del progetto
- [x] Collegare qui le pagine operative reali
- [ ] Chiudere i workstream prioritari

## Prossimi passi

- [ ] Popolare [[ops/current-state]]
- [ ] Popolare [[ops/backlog]]
- [ ] Popolare [[build/system-map]]
- [ ] Eseguire il primo ingest da `raw/`

## Pagine operative chiave

- [[ops/current-state]] — stato reale del progetto
- [[ops/backlog]] — backlog operativo e priorità
- [[kanban-project-status]] — board kanban sullo stato attuale
- [[decisions/decision-log]] — registro decisioni
- [[questions/open-questions]] — domande aperte
- [[build/system-map]] — mappa software iniziale

## Ultime pagine aggiornate

```dataview
TABLE type, status, updated
FROM "wiki"
WHERE type != "overview"
SORT updated DESC
LIMIT 12
```

## Decisioni recenti

```dataview
TABLE decision_status, updated
FROM "wiki/decisions"
SORT updated DESC
LIMIT 10
```

## Domande aperte

```dataview
TABLE status, area, updated
FROM "wiki/questions"
SORT updated DESC
LIMIT 10
```
