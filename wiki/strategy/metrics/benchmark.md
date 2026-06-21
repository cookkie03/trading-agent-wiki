---
title: "Benchmark"
type: synthesis
tags:
  - strategy
  - market-structure
created: 2026-05-29
updated: 2026-05-29
status: active
area: strategy
confidence: medium
related:
  - "[[strategy/index]]"
  - "[[system/modules/agents]]"
---

# Benchmark

Una gestione **attiva** ha **sempre un benchmark**: un indice di riferimento, "un numero da superare" (principio del fondo attivo, ricordato da Salvatore da "Trezzi"). Senza benchmark non c'è un target misurabile né senso nell'investire attivamente (altrimenti meglio comprare un ETF passivo).

> 🟢 **Implementato (2026-06-08)** — benchmark **dinamico** (`tradingagents/benchmark.py` + `performance.py`): simboli **solo da config** (`[benchmark] symbols`, lista cambiabile; default **SPY**), mai hardcoded; si calcola l'**alpha** (rendimento portafoglio − benchmark). L'**universo investibile** è ora di prima classe (catalogo broker riconciliato) con la **watchlist dinamica** come working set → [[system/universe-watchlist]].

## Scelta per il progetto (2026-05-29)
- **S&P 500** — US, pubbliche, trasparenti, in inglese, info facilmente raggiungibili.
- **60/40 Vanguard all-world
- Con la **riserva del 10% di liquidità**, il portafoglio sarà ~**50/40 ÷ 55/35** + 10% cash → un po' meno investito del benchmark, ma puntando a una **selezione attiva** migliore.

## Idea: selezione attiva dei titoli S&P
Ridurre l'universo investibile ai **titoli del benchmark** (e.g. i titoli dell'S&P500), prendere il **percentile migliore** e battere l'indice. Considerato "l'unico modo realistico per battere il benchmark": universo piccolo, dati trasparenti, niente mercati emerging poco trasparenti.

## Dati di riferimento (al 2026-05-29)
- S&P 500: **+29%** sugli ultimi 12 mesi, **+10% YTD**.
- Per battere l'S&P sul periodo serve **>30%**; target "soddisfacente" minimo: battere il benchmark (~10%).

> Il benchmark dà anche **paletti** di asset allocation (es. il 60/40 classico come linea da seguire).
