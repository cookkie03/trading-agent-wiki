---
title: "Frontend Module"
type: build
tags:
  - architecture
  - software
  - roadmap
created: 2026-06-23
updated: 2026-07-13
status: active
confidence: medium
area: software
related:
  - "[[system/foundation/codebase-architecture]]"
  - "[[system/interface/observability-dashboard]]"
  - "[[prior-art/libraries/sfc-portfolio-tracker]]"
  - "[[artifacts/project-board]]"
---

# Frontend Module

Vincolo architetturale emerso dalle daily notes: il frontend deve essere **un modulo sostituibile**. Streamlit puo' essere la prima UI, ma il core non deve dipendere da Streamlit; in futuro deve essere possibile passare a TypeScript cambiando il modulo frontend e i suoi adapter.

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

## Prima versione

Prima versione consigliata: **Streamlit read-only stile SFC**.

Motivo: e' veloce per osservabilita', usa Python e si integra bene col DB. La pagina [[system/interface/observability-dashboard]] resta il dettaglio funzionale; questa pagina definisce solo il confine architetturale.

## Evoluzione futura

Una UI TypeScript futura deve poter riusare gli stessi contratti:

- o tramite API HTTP locale;
- o tramite file/read model esportati;
- o tramite un service layer condiviso.

La scelta tecnica si decide quando la dashboard diventa prodotto, non nel primo harness.
