---
title: Frontend Module
type: build
tags:
  - frontend-module
  - architecture
  - software
created: 2026-06-23T00:00:00.000Z
updated: 2026-11-12
status: active
confidence: medium
area: software
related:
  - '[[system/foundation/codebase-architecture]]'
  - '[[system/interface/observability-dashboard]]'
  - '[[prior-art/libraries/sfc-portfolio-tracker]]'
  - '[[artifacts/project-board]]'
---

# Frontend Module

> [!important] Promemoria per la UI
> Prima di riprendere la progettazione o l'implementazione della UI del Trading Agent su GitHub, **chiedere a Giuseppe (vedi lista contatti)** un confronto e un aiuto sulla UI.

Il frontend è un modulo sostituibile e disaccoppiato dal core. La decisione MVP corrente è **React + TypeScript + Vite/npm**, con backend Python read-only; la precedente ipotesi Streamlit è superata.

## Boundary

Il frontend legge e visualizza. Non contiene:

- logica di trading;
- calcoli risk/quant;
- chiamate dirette ai vendor;
- submit ordini non mediati da API/servizi espliciti;
- trasformazioni che cambiano lo stato finanziario.

Il frontend puo' contenere:

- componenti UI;
- read models;
- filtri e viste;
- refresh/polling;
- link a log, trace e pagine wiki;
- eventuali controlli futuri solo se passano da contratti applicativi chiari.

## Contratti minimi

La dashboard read-only deve consumare contratti stabili, non repository interni sparsi:

- portfolio snapshot;
- positions;
- cash/liquidity;
- trades e `exit_reason`;
- watchlist/universe;
- benchmark/alpha;
- decision log;
- trigger/events;
- system health;
- last run / daemon status.

Questi contratti possono essere funzioni Python, API locali o query layer, ma devono restare indipendenti dal framework UI.

## MVP corrente

**React + TypeScript + Vite/npm** con backend Python read-only. La UI deve essere un cockpit completo e coerente, non una semplice pagina di metriche: mostrare le capacità effettivamente implementate, gli stati operativi e le fonti, distinguendo sempre dati reali, demo, vuoti, errori e funzionalità non disponibili. La pagina [[system/interface/observability-dashboard]] definisce il dettaglio funzionale.

## UI design & build workflow

La costruzione della UI è un vero workstream del progetto, non un'attività accessoria di styling. Prima di riprendere il frontend, **chiedere a Giuseppe (vedi lista contatti)** un confronto e un aiuto sulla UI del Trading Agent su GitHub.

### Strumenti di riferimento

- **[21st.dev](https://21st.dev/)** — riferimento primario per esplorare componenti, pattern, template e temi React/shadcn, cercare componenti adatti al cockpit e integrarli nel repository. Preferire componenti con codice sorgente installabile e adattarli al design system del progetto; evitare di copiare componenti senza verificarne accessibilità, responsive behavior, dipendenze e coerenza visiva.
  - Skill ufficiali: [21st-dev/skill](https://github.com/21st-dev/skill).
  - Setup skill: `npx @21st-dev/cli install-skill`.
  - CLI: `npx @21st-dev/cli` (login/API key solo se necessario).
- **[Impeccable](https://github.com/pbakaus/impeccable)** — skill di riferimento per progettazione, implementazione e revisione critica della UI. Usarla per shape/plan prima di implementare, poi per critique/audit/polish e verifica di accessibilità, responsive behavior, gerarchia visiva, tipografia, stati e micro-interazioni.
  - Installazione skill: `npx skills add pbakaus/impeccable --skill impeccable`.
  - Licenza del progetto skill: Apache-2.0.

### Sequenza di lavoro UI

1. Raccogliere il confronto con Giuseppe e definire obiettivi, utenti, casi d'uso e direzione visuale.
2. Esaminare la codebase e i contratti read-only esistenti; definire le superfici del cockpit e le priorità informative prima del codice.
3. Usare Impeccable per strutturare la direzione e il piano UX/UI; documentare decisioni e token condivisi.
4. Usare 21st.dev per cercare e selezionare componenti/pattern utili, poi adattarli e integrarli nel progetto React/TypeScript.
5. Costruire il cockpit end-to-end: navigazione, overview, portfolio, watchlist, agent/workflow observability, decision log, trades, system health e stati vuoti/errore/loading, nei limiti dei dati realmente disponibili.
6. Verificare desktop e mobile, accessibilità, interazioni, performance, coerenza e stati edge; usare Impeccable per critique/audit/polish e test automatici/manuali.
7. Registrare componenti riusati, dipendenze aggiunte, scelte visuali e limiti. Il codice finale deve restare nel repository, comprensibile e modificabile, senza dipendere da un servizio remoto per renderizzare componenti già installati.

21st.dev e Impeccable sono strumenti di supporto al design/build, non vincoli architetturali né sostituti dei contratti API, dei test o della verifica del prodotto. La UI resta read-only finché non viene approvata una distinta specifica per eventuali azioni operative.

## Evoluzione futura

Una UI TypeScript futura deve poter riusare gli stessi contratti:

- o tramite API HTTP locale;
- o tramite file/read model esportati;
- o tramite un service layer condiviso.

La scelta tecnica si decide quando la dashboard diventa prodotto, non nel primo harness.
