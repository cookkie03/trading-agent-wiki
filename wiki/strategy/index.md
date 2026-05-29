---
title: "Strategy — Indice"
type: overview
tags:
  - strategy
  - market-structure
created: 2026-05-14
updated: 2026-05-29
status: active
area: strategy
related:
  - "[[build/modules/quant-backtesting]]"
  - "[[build/decision-log]]"
---

# Strategy

Tutto ciò che riguarda **cosa fa tradare il sistema**: approcci, indicatori, metriche di valutazione, meccanismi di mercato.

Questa sezione è il dominio di Salvatore. Ogni elemento qui dentro è distillato da materiale grezzo portato in `raw/` e poi ingestato. Quando un metodo o un indicatore diventa parte della spec del Modulo C, il file qui rimane come riferimento concettuale e il modulo linka qui.

---

## Principio di linking

Ogni file in `strategy/` dovrebbe linkare:
- i **metodi** che lo usano (es. `rsi.md` → `trend-following.md`)
- le **metriche** con cui si valuta (es. `trend-following.md` → `sharpe-ratio.md`)
- il **modulo software** che lo implementa (es. `trend-following.md` → `[[build/modules/quant-backtesting]]`)

---

## Methods — Approcci di trading

Ogni metodo descrive una strategia o un approccio: come funziona, quando funziona, cosa richiede.

- [[strategy/methods/trend-following]] — seguire il trend degli istituzionali (approccio attuale Salvatore)
- [[strategy/methods/factor-investing]] — investire basandosi su fattori fondamentali e quantitativi
- [[strategy/methods/mean-reversion-stat-arb]] — mean reversion e statistical arbitrage / pairs trading (candidata per Modulo C, da Salvatore)

*Aggiungere un file per ogni nuovo approccio studiato, anche se poi si decide di non usarlo.*

---

## Indicators — Indicatori tecnici e quantitativi

Un file per ogni indicatore: cosa misura, come si interpreta, quali parametri ha.

*(Da popolare — Salvatore porta gli indicatori che usa)*

> **In arrivo (2026-05-29)**: Salvatore convertirà in TXT/Obsidian il suo file **market driver** (4 macro-categorie, da arricchire) e preparerà un documento sugli **indicatori di valuation** delle stock. Vedere [[references/videochiamata-luca-salvatore-2026-05-29]].

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
4. Luca traduce i metodi validati in tool Python in `build/modules/quant-backtesting`
