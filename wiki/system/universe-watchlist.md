---
title: "Universo investibile, Watchlist dinamica, Gerarchia agenti"
type: build
tags:
  - architecture
  - multi-agent
  - software
created: 2026-06-08
updated: 2026-06-08
status: active
priority: high
area: software
related:
  - "[[system/modules/agents]]"
  - "[[system/parallelism-design]]"
  - "[[strategy/metrics/benchmark]]"
  - "[[system/modules/data-layer]]"
  - "[[system/canvas-code-mapping]]"
confidence: high
---

# Universo investibile, Watchlist dinamica, Gerarchia agenti

> Cambio di paradigma deciso con Luca + Salvatore (2026-06-08): il sistema è **autonomo anche nella scelta degli asset** e ha un **benchmark da battere**. Implementato nel branch `feat/universe-watchlist`.

## Modello a tre insiemi concentrici

```
UNIVERSO   = tutti i tradable del broker, conosciuti + riconciliati periodicamente   (catalogo, righe economiche)
   ⊇  WATCHLIST = sottoinsieme DINAMICO sotto analisi, gestito dagli agent             (working set, analisi costosa)
        ⊇  PORTFOLIO = asset posseduti                                                  (gestione uscite)
BENCHMARK  = S&P 500 via SPY — il numero da battere, tracciato a parte (dinamico, mai fisso)
```

L'efficienza: ingestione/deep-dive costosi solo su **watchlist + portfolio + triggerati**; il resto dell'universo è catalogo a costo ~0. Una news/alert su un asset fuori watchlist può farlo **entrare** (dinamicità).

## Universo + riconciliazione (codice: `tradingagents/universe/`)
- `broker.list_assets()` enumera i tradable (Alpaca `/v2/assets`; IBKR non li elenca → fallback al seed S&P500; PaperBroker lista statica/seed).
- `sync_universe()` fa upsert dei tradable, **marca inattivi** quelli che il broker non offre più (riconciliazione continua "conosciuto vs reale"), tagga i costituenti S&P500 dal **seed** (`tradingagents/data/sp500.csv`, ampliabile).
- Cadenza configurabile (`[universe] reconcile_every_cycles`).

## Watchlist dinamica (membership ibrida)
- **Seed** iniziale = S&P500 ∩ broker-tradable (`[watchlist] seed`).
- **Entra**: candidati deterministici (screening/alert/news); quando un alert o una news cita un ticker non in watchlist, **entra** (`_admit_watchlist`). Il PM cura (estendibile a giudizio LLM).
- Scheda ticker (`ticker_card`) = hub DB-first: screening, ultima valutazione, membership, date. Le **date** stanno in `ticker_events` e alimentano in automatico i trigger (il sistema si auto-schedula).

## Benchmark dinamico (codice: `benchmark.py`, `performance.py`)
- Simboli **solo da config** (`[benchmark] symbols=["SPY"]`, lista, cambiabile). Mai hardcoded.
- `performance_vs_benchmarks()` → rendimento portafoglio vs ciascun benchmark = **alpha**.

## Gerarchia agenti (tre livelli) — codice: `brain/director.py` + `brain/graph.py`
```
DIRETTORE (Portfolio Manager, uno) — decide cosa analizzare, gestisce watchlist,
   fa fan-out parallelo, decisione di portafoglio + Statuto di portafoglio
      ▼
VALUTATORE (uno per titolo, in parallelo) = brain per-ticker (analyze_symbol)
   coordina i desk → tesi del titolo
      ▼
DESK: Market · Sentiment · Technical · Fondamentali
+ RISK ANALYST = ruolo DISTINTO su DUE livelli:
   - singolo titolo: bear + Statuto del titolo (dentro l'Evaluator)
   - portafoglio: `admit_within_statute` (riserva 10% cassa, VaR totale, settore)
     + giudizio finale del Risk sull'intero book (estendibile)
```
Il Risk Analyst **non è stato sostituito**: resta la figura distinta decisa con Salvatore, estesa al livello di portafoglio.

## Parallelismo
`analyze_batch` fa fan-out dei Valutatori su un **thread pool** limitato (`[cycle] max_parallel`), ogni worker con la propria sessione DB; l'esecuzione ordini resta seriale. Vincolo: con SQLite + modelli free rate-limited il parallelismo effettivo è modesto; Postgres + modelli a pagamento lo scalano. (I subgraph LangGraph per-ticker restano la struttura; i thread danno la concorrenza reale sulle chiamate LLM bloccanti.)

## Riferimento da studiare
**"hermes agent"** (full Python) — segnalato da Luca come riferimento per principi di autonomia/dinamicità/versatilità degli agent generalisti. Da verificare e approfondire (non assunto).
