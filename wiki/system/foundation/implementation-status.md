---
title: "Implementation Status Policy"
type: build
tags:
  - architecture
  - roadmap
  - infrastructure
created: 2026-07-13
updated: 2026-07-13
status: active
related:
  - "[[system/foundation/architecture]]"
  - "[[system/_reference/fork-gap-analysis]]"
  - "[[system/_reference/canvas-code-mapping]]"
  - "[[artifacts/project-board]]"
confidence: high
area: software
---

# Implementation Status Policy

Il repository del progetto vive fuori da questo vault. La wiki è la spec condivisa, il registro delle decisioni e il backlog: non è una fonte affidabile per attestare processi attivi, branch, test, URL o moduli effettivamente presenti nel repository.

## Convenzioni

- Una pagina di design descrive un requisito o una decisione valida.
- Un riferimento a codice precedente è marcato **reference design / storico**.
- `Implementato`, `✅`, test verdi e dettagli di deployment compaiono solo con una verifica esterna datata e un link/record che la renda controllabile.
- La board contiene **specifiche da consegnare al coding agent**, non comandi o attività eseguite sul repository.
- Quando il codice esterno verrà verificato, si aggiorna una sola pagina di stato con data, evidenza e impatto sulle spec; non si duplicano claim in ogni pagina.

## Effetto sulla wiki

Le decisioni architetturali restano attive: monolite modulare, dati e tool con confini espliciti, output strutturati, guardrail deterministici, frontend sostituibile. I dettagli di branch o snapshot vengono consultati soltanto nelle pagine di [[system/_reference/fork-gap-analysis|reference design]] e [[system/_reference/canvas-code-mapping|mappatura storica]].
