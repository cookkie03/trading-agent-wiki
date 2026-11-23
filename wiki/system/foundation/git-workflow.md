---
title: Convenzione Git e Workspace
type: build
tags:
  - git
  - workflow
  - software
created: 2026-10-31
updated: 2026-11-23
status: active
related:
  - '[[system/foundation/decision-log]]'
  - '[[system/foundation/implementation-status]]'
area: software
---

# Convenzione Git e Workspace

La decisione del 2026-11-22 sostituisce il lavoro diretto su `main` deciso il 2026-10-31. La procedura operativa vive in `AGENTS.md` e `docs/git-workflow.md` del repository del codice.

## Decisione

Il lavoro sul codice passa da issue → branch → PR → CI; Luca mantiene il merge manuale (l'agente unisce solo quando Luca lo chiede per quella PR). Per il cockpit si usa una branch per pagina, `<pagina>-frontend` (es. `settings-frontend`), con backend e frontend della pagina (decisione del 2026-11-23). La CI verifica test offline e build senza credenziali del broker. La release SemVer è un passaggio separato, avviato manualmente da `main`: produce un tag e note, non un deploy.

La wiki conserva le decisioni e il contesto, mentre GitHub Issues tiene traccia del lavoro sul codice. Nessuna integrazione Linear o migrazione del vault è stata decisa.

## Stato

Workflow `ci.yml` e `release.yml` su `main` dal 2026-11-23 (commit `db765d6`). Prima release non ancora pubblicata.
