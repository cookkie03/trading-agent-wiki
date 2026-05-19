---
title: "Modulo C — Quant Agent + Backtesting"
type: build
tags:
  - build
  - strategy
  - software
created: 2026-05-13
updated: 2026-05-13
status: active
priority: high
area: software
related:
  - "[[build/system-map]]"
  - "[[build/stack]]"
  - "[[build/mvp-prototype-design]]"
  - "[[strategy/index]]"
  - "[[strategy/methods/trend-following]]"
  - "[[strategy/methods/factor-investing]]"
  - "[[syntheses/notebooklm-research-2026-05-13]]"
---

# Modulo C — Quant Agent + Backtesting

**Track 2 — Luca + Salvatore, sessioni di progettazione in parallelo con Track 1.**

Il modulo che incorpora la strategia. Contiene tutta la logica quantitativa: quali segnali guardare, come combinarli, come validarli con backtest robusti. Si integra con il DB di Modulo A.

---

## Cosa fa

- Implementa la **strategia quantitativa** scelta (vedi sotto)
- Esegue **backtest robusti** sui dati storici in `market_data` (via VectorBT)
- Calcola indicatori tecnici parametrizzabili (RSI, MACD, Pivot Points, medie mobili...)
- Produce output strutturato nel DB → `module_outputs` (per il Prompt Builder)
- Genera metriche di valutazione per ogni strategia testata

## Output atteso

> Prime metriche su dati reali: Sharpe ratio, win rate, drawdown per la strategia scelta.

---

## Strategia — stato attuale

**Orientamento**: multi-factor (fondamentali + tecnici). Non ancora formalizzato.

| Categoria | Esempi | Stato |
|-----------|--------|-------|
| Indicatori tecnici | RSI, MACD, Pivot Points, medie mobili | Da raccogliere con Salvatore |
| Fattori fondamentali | P/E, revenue trend, macro (tassi, PIL) | Da raccogliere con Salvatore |
| Segnali di sentiment | Fear & Greed, news score | Fase successiva |

**Principio di parametrizzazione**: ogni indicatore è un tool che accetta parametri in input (es. `moving_average(period=N)`), non valori hardcodati. L'agente può sperimentare diversi valori senza toccare il codice.

---

## Tech

- **VectorBT**: framework backtesting. Gestisce costi di transazione (10bps per trade). Stessa logica del codice live.
- **Dati**: da `market_data` nel DB di Modulo A (OHLCV Binance, timeframe 4h/daily)
- **Metriche obbligatorie**: Sharpe ratio, Sortino ratio, Max Drawdown, Win Rate, Calmar ratio
- **Insidie da evitare**: look-ahead bias (non usare dati non ancora disponibili al momento del trade)

---

## Decisioni prese

| Tema | Scelta |
|------|--------|
| Framework backtesting | VectorBT (fonte: MarketSenseAI) |
| Costi transazione | Simulare sempre (10bps per trade minimo) |
| Principio | Tool parametrizzabili, non hardcodati |

## Domande aperte

> Queste domande bloccano o influenzano la progettazione del modulo.

- **Quale strategia quantitativa esatta?** Multi-factor è l'orientamento, ma Salvatore deve portare i fattori concreti. *Da risolvere in sessione con Salvatore.*
- **Frequenza ciclo: 4h vs 24h?** Dipende dai primi backtest — quale timeframe ha più segnale/rumore per swing trading crypto?
- **Modulo TA da includere?** Rischio: TA mal calibrata corrompe l'output. Progettare come modulo opzionale e testare A/B (con/senza).
- **Multi-asset o singolo asset nel backtest iniziale?** MVP singolo asset, ma il codice deve supportare multi-asset per il futuro.
- **Quanti dati storici necessari?** Per avere backtest statisticamente significativi su swing trading crypto.

---

## Dipendenze

- **Dipende da Modulo A**: legge `market_data` dal DB di A
- **Modulo D dipende da C**: il Prompt Builder include l'output di C nel prompt del Trader

---

## Come contribuisce Salvatore

Salvatore porta il contenuto della strategia in **[[strategy/]]** — questo modulo lo implementa:
1. Porta in `raw/` indicatori tecnici, strategie, casi reali, paper
2. L'agente ingesta e struttura il materiale in `strategy/methods/`, `strategy/indicators/`, `strategy/metrics/`
3. Quando un metodo è validato, Luca costruisce il tool Python corrispondente qui

*Vedere [[build/decision-log]] per le decisioni aperte legate a questo modulo.*
