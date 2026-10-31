---
title: Convenzione Git e Workspace
type: build
tags:
  - git
  - workflow
  - software
created: 2026-10-31
updated: 2026-10-31
status: active
related:
  - '[[system/foundation/decision-log]]'
  - '[[system/foundation/implementation-status]]'
area: software
---

# Convenzione Git e Workspace

Decisione condivisa da Luca il 2026-10-31. Le regole operative dettagliate vivono in `docs/git-workflow.md` nel repository del codice; questa pagina conserva la decisione e il motivo.

## Regole

- Il lavoro ordinario si svolge su `main`, così Luca può monitorare il codice da VS Code.
- Si apre un worktree separato solo su richiesta di Luca o per modifiche radicali, sperimentali o ancora incerte.
- Ogni lavoro completato viene pushato su GitHub.
- Il merge su `main` lo esegue Luca.
- Quando il lavoro usa un branch separato, l'agente apre autonomamente la Pull Request dopo il push e non esegue il merge.
- Decisioni e avanzamenti rilevanti vengono sincronizzati con la documentazione del repository e con questa wiki.

## Motivazione

La regola privilegia la visibilità diretta del lavoro durante lo sviluppo quotidiano e riserva l'isolamento ai casi in cui riduce davvero il rischio o facilita una sperimentazione. La separazione delle responsabilità mantiene il merge sotto il controllo di Luca, senza rinunciare a push e PR automatici.
