---
title: "Dashboard di osservabilità (read-only)"
type: build
tags:
  - architecture
  - software
  - ux
created: 2026-06-08
updated: 2026-06-08
status: draft
priority: medium
area: software
related:
  - "[[system/universe-watchlist]]"
  - "[[system/modules/data-layer]]"
  - "[[prior-art/libraries/sfc-portfolio-tracker]]"
  - "[[strategy/metrics/benchmark]]"
confidence: medium
---

# Dashboard di osservabilità (read-only)

> Input di Luca (2026-06-08): fatta l'architettura a **daemon** (il sistema gira in background con `start`/`stop`), l'utente deve poterlo **osservare** tramite una dashboard **di sola lettura**, ispirata a **SFC fund** (Streamlit). **Da progettare/implementare in un secondo momento** — qui solo l'impostazione.

## Principio
**Osserva, non controlla.** La dashboard legge dal DB (`~/.tradingagents/trading_agent.db` o Postgres) e non invia mai comandi al sistema: il daemon resta l'unico a operare. Nessun pulsante che muove ordini.

## Cosa mostra (bozza)
- **Portafoglio / rendicontazione**: liquidità, posizioni, distribuzione, P/L, NAV nel tempo (`portfolio_snapshots`).
- **Performance vs benchmark**: rendimento vs SPY (o i benchmark configurati) → **alpha** (`performance.py`).
- **Universo & Watchlist**: dimensione universo riconciliato, watchlist corrente con motivo/score, ingressi/uscite.
- **Decisioni & trade**: ultime tesi (`research_states`/`decision_log`), trade aperti/chiusi con `exit_reason`, opinioni per-agente.
- **Eventi & trigger**: `ticker_events` imminenti, alert, perché il sistema si è svegliato.
- **Stato sistema**: daemon running/stopped (PID), ultimo ciclo, log recenti.

## Riferimento
**SFC portfolio tracker** (Streamlit) → [[prior-art/libraries/sfc-portfolio-tracker]]: analytics, NAV history, attribution, PyPortfolioOpt. Punto di partenza per layout e metriche.

## Note tecniche (future)
- Streamlit app separata che apre il DB in sola lettura (o repliche/materialized view per non contendere il lock con il daemon).
- Si lega a **LangSmith / LangGraph Studio** per il tracing degli agenti (osservabilità del ragionamento), complementare alla dashboard di portafoglio.

## Stato
**Aperto / da fare dopo.** Card in [[artifacts/project-board]]; decisione in [[system/decision-log]].
