---
title: Strategy — Indice
type: overview
tags:
  - trading-approach
  - backtesting
  - strategy
  - market-structure
created: 2026-05-14T00:00:00.000Z
updated: 2026-07-13T00:00:00.000Z
status: active
area: strategy
related:
  - '[[system/quant/quant-backtesting]]'
  - '[[system/foundation/decision-log]]'
---

# Strategy

Tutto ciò che riguarda **cosa fa tradare il sistema**: approcci, indicatori, metriche di valutazione, meccanismi di mercato.

Questa sezione è il dominio di Salvatore. Ogni elemento qui dentro è distillato da materiale grezzo portato in `raw/` e poi ingestato. Quando un metodo o un indicatore diventa parte della spec del Modulo C, il file qui rimane come riferimento concettuale e il modulo linka qui.

---

## Principio di linking

Ogni file in `strategy/` dovrebbe linkare:
- i **metodi** che lo usano (es. `rsi.md` → `trend-following.md`)
- le **metriche** con cui si valuta (es. `trend-following.md` → `sharpe-ratio.md`)
- il **modulo software** che lo implementa (es. `trend-following.md` → `[[system/quant/quant-backtesting]]`)

---

## Methods — Approcci di trading

Ogni metodo descrive una strategia o un approccio: come funziona, quando funziona, cosa richiede.

- [[strategy/methods/trend-following]] — seguire il trend degli istituzionali (approccio attuale Salvatore)
- [[strategy/methods/factor-investing]] — investire basandosi su fattori fondamentali e quantitativi
- [[strategy/methods/mean-reversion-stat-arb]] — mean reversion e statistical arbitrage / pairs trading (candidata per Modulo C, da Salvatore)

## Decisione strategica MVP — 2026-11-01

L'MVP adotta **trend following su barre hourly, long-only, azioni USA, USD-only, con swing trading**. La scelta è confermata da Luca; non implica che il modello software venga costruito solo per questa strategia.

La wiki conserva più metodi perché devono poter diventare strategie componibili, non perché vadano tutti implementati insieme. Il primo protocollo di backtest e le prime capability quantitative vengono quindi definiti sul trend following, mantenendo un contratto di stato riusabile per strategie future.

- **In scope MVP:** una strategia trend following su barre hourly, segnali deterministici, sizing e risk gate verificabili, backtest con costi/slippage e benchmark statico.
- **Fuori scope iniziale:** short, pairs trading, multi-leg, FX, opzioni, ML/deep learning e composizione di più strategie.
- **Vincolo di design:** lo state non deve codificare `SMA20` o una singola formula nei campi strutturali; indicatori e parametri appartengono alla definizione/versione della strategia e alla provenance del segnale.

*Aggiungere un file per ogni nuovo approccio studiato, anche se poi si decide di non usarlo.*

---

## Indicators — Indicatori tecnici e quantitativi

Un file per ogni indicatore: cosa misura, come si interpreta, quali parametri ha.

Questa sezione va popolata in modo più sistematico. Oltre agli indicatori tecnici, servirà una pagina definitiva sulle **metriche** e una tassonomia più pulita dei metodi che vogliamo poi portare a codice.

---

## Metrics — Metriche di valutazione

Un file per ogni metrica: come si calcola, cosa misura, quando è utile.

- [[strategy/metrics/benchmark]] — il benchmark come riferimento della gestione attiva (S&P + 60/40 all-world)

*(Da popolare — le principali sono già nel [[_meta/glossario]])*

---

## Come contribuisce Salvatore

1. Carica in `raw/` tutto quello che trova: articoli, note, audio, casi reali
2. L'agente ingesta e crea/aggiorna file qui
3. Salvatore può anche modificare direttamente i file esistenti
4. Luca traduce i metodi validati in tool Python in [[system/quant/quant-backtesting]]

