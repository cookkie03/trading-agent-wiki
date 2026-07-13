---
title: "Dashboard di osservabilità"
type: build
tags:
  - architecture
  - software
  - ux
  - streamlit
  - nas
  - deploy
created: 2026-06-08
updated: 2026-07-13
status: active
priority: high
area: software
related:
  - "[[system/orchestration/universe-watchlist]]"
  - "[[system/data/data-layer]]"
  - "[[prior-art/libraries/sfc-portfolio-tracker]]"
confidence: high
---

# Dashboard di osservabilità (read-only)

Pagina di **spec**, non di stato del repository esterno. L'obiettivo è rendere osservabile il sistema senza inserire logica di investimento nel frontend; vedi anche [[system/interface/frontend-module]].

## Boundary

La dashboard legge read model o contratti applicativi espliciti. Non chiama vendor direttamente, non esegue ordini e non calcola regole di rischio/strategia.

## Informazioni da esporre

1. portfolio snapshot, liquidità e posizioni;
2. watchlist, ticker e ultimo stato di analisi;
3. decisioni, opinioni, trigger e motivazioni;
4. trade, `exit_reason` e metriche di esito;
5. health del sistema e staleness dei dati;
6. benchmark/alpha solo quando il benchmark sarà introdotto Post-MVP.

## Evoluzione

Una prima UI può usare Streamlit come reference SFC; una UI TypeScript futura deve riusare gli stessi contratti di lettura. Dettagli di deploy, URL, daemon e database appartengono al repository/infrastruttura esterni e non vengono mantenuti qui come stato corrente.
