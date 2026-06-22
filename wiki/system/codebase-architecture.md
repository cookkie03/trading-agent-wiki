---
title: "Codebase Architecture"
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
  - "[[artifacts/project-board]]"
  - "[[system/modules/data-layer]]"
  - "[[system/modules/agents]]"
  - "[[system/modules/execution]]"
---

# Codebase Architecture

Pagina guida per progettare la codebase reale partendo da zero. Il principio fissato da Luca è: **prima si ingegnerizza il tree**, poi si costruiscono i moduli fondamentali con test, poi i layer più specifici e infine i job asincroni o sperimentali.

## Principi

- Il codice attuale della wiki va letto come **design/reference history**, non come baseline implementativa da dare per esistente.
- Gli agenti non devono conoscere broker, vendor o dettagli infrastrutturali: chiedono dati o trade a **interfacce stabili**.
- La prima tranche reale deve essere l'**harness**: broker, vendor wrappers, storage, contracts, test e osservabilità di base.
- I rami di alto livello devono essere **solidi nel tempo** e accomodare sia build minima sia estensioni future.

## Struttura target da chiarire

- `connectors/` o equivalente: adapter verso broker, vendor, frontend esterni.
- `capabilities/` o equivalente: tool deterministici e funzioni che lavorano sui dati standardizzati.
- `database/` o equivalente: schema, models, repositories, migrazioni, servizi di accesso.
- `agents/` o equivalente: prompt, schemas, orchestration, context, evaluation.
- `execution/`: policy di submit, recovery, costs, exits, portfolio state.
- `frontend/`: modulo sostituibile senza cambiare il core applicativo.

## Sequenza di implementazione proposta

1. Definire il tree alto livello e i contratti interni.
2. Costruire harness broker/vendor/storage con test.
3. Implementare strumenti deterministici core e tool wrappers.
4. Solo dopo, progettare grafo, agenti e prompt sopra quei contratti.
5. Infine introdurre job asincroni, monitoring avanzato e componenti sperimentali.

## Link operativi

- Mappa fonti e tool: [[system/data-sources-tool-map]]
- Riorganizzazione documentazione `wiki/system/`: [[system/system-wiki-reorganization]]
- Frontend modulare: [[system/frontend-module]]
