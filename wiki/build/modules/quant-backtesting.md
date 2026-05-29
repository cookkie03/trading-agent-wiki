---
title: "Quant Agent + Backtesting"
type: build
tags:
  - build
  - strategy
  - software
created: 2026-05-13
updated: 2026-05-29
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
  - "[[references/videochiamata-luca-salvatore-2026-05-29]]"
---

# Quant Agent + Backtesting

Il componente che incorpora la strategia. Contiene tutta la logica quantitativa: quali segnali guardare, come combinarli, come validarli con backtest robusti. Si integra con il DB di [[build/modules/exchange-db]].

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

### Posizione di Salvatore su TA, fondamentali e sentiment (2026-05-29)
*Vedere [[references/videochiamata-luca-salvatore-2026-05-29]].*
- **Analisi tecnica usata bene** (non "candele alla guru di Dubai"): minimi/massimi a **52 settimane**, range del prezzo e suoi sforamenti, **drawdown**, **volumi**, capire cosa è successo nel giorno di uno sforamento. Serve ad avere "il quadro" (come una dashboard vs dati grezzi), non a fare trading da grafico. Posizione **ibrida col sentiment**.
- **Sentiment**: non ha indicatori propri standard (al massimo indici di paura) → **da inventare/definire**. Legge tweet/posizioni delle persone.
- **Fondamentali**: non sono "pochi". Es. esistono **5 tipi di P/E** (normale/current, **trailing**, **forward**); Salvatore usa il confronto **trailing vs current** (capire se il calo è dovuto al prezzo o agli EPS). Dare un **tool** per calcolarli e lasciar combinare all'agente.
- **Factor investing / regressioni / strumenti statistici**: utili ma "un'altra parte della finanza", competenze non ancora possedute → per ora fuori scope MVP.

---

## Tech

- **VectorBT**: framework backtesting. Gestisce costi di transazione (10bps per trade). Stessa logica del codice live.
- **Dati**: da `market_data` nel DB di [[build/modules/exchange-db]] (OHLCV stock, timeframe 4h/daily)
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
- **Frequenza ciclo: 4h vs 24h?** Dipende dai primi backtest — quale timeframe ha più segnale/rumore per swing trading equity?
- **Modulo TA da includere?** Rischio: TA mal calibrata corrompe l'output. Progettare come modulo opzionale e testare A/B (con/senza).
- **Multi-asset o singolo asset nel backtest iniziale?** MVP singolo asset, ma il codice deve supportare multi-asset per il futuro.
- **Quanti dati storici necessari?** Per avere backtest statisticamente significativi su swing trading equity.

---

## Dipendenze

- **Dipende da [[build/modules/exchange-db]]**: legge `market_data` dal DB
- **[[build/modules/llm-agent-system]]** dipende da questo: il Prompt Builder include l'output quant nel prompt del Trader

---

## Come contribuisce Salvatore

Salvatore porta il contenuto della strategia in **[[strategy/]]** — questo modulo lo implementa:
1. Porta in `raw/` indicatori tecnici, strategie, casi reali, paper
2. L'agente ingesta e struttura il materiale in `strategy/methods/`, `strategy/indicators/`, `strategy/metrics/`
3. Quando un metodo è validato, Luca costruisce il tool Python corrispondente qui

*Vedere [[build/decision-log]] per le decisioni aperte legate a questo modulo.*
