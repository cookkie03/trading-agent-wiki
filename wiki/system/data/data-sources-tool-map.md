---
title: "Data Sources & Tool Map"
type: build
tags:
  - infrastructure
  - software
  - architecture
created: 2026-06-23
updated: 2026-07-13
status: active
confidence: medium
area: software
related:
  - "[[system/tools/tools-inventory]]"
  - "[[system/data/data-providers]]"
  - "[[system/data/data-layer]]"
  - "[[system/agents/agents]]"
  - "[[system/execution/execution]]"
  - "[[system/quant/quant-backtesting]]"
  - "[[artifacts/project-board]]"
---

# Data Sources & Tool Map

Questa pagina collega tre livelli che prima erano separati:

- **provider/vendor**: chi fornisce dati o broker API;
- **wrapper/connector**: come il codice normalizza quella fonte;
- **tool/capability**: cosa vede l'agente o il modulo deterministico.

La regola architetturale e': **vendor e broker stanno sotto wrapper, gli agenti vedono solo tool stabili**.

## Mappa provider -> wrapper -> tool

| Dominio | Fonte primaria | Wrapper interno | Tool/capability esposta | Area DB |
|---|---|---|---|---|
| Broker MVP | Alpaca paper | broker adapter | `submit_order`, `get_positions`, `get_cash`, reconciliation | rendicontazione/log |
| Broker prod | IBKR | broker adapter | ordini, posizioni, opzioni, account summary | rendicontazione/log |
| Prezzi storici dev | yfinance | market data connector | `get_ohlcv_history` | market_data |
| Prezzi prod/multi-asset | Twelve Data / Alpha Vantage | market data connector | `get_ohlcv_history`, quote fallback | market_data |
| Quote live | Finnhub / Alpaca / IBKR | live quote connector | `get_realtime_quote` con write-through | market_data |
| Macro | FRED | macro connector | `get_macro_series` | market_data |
| Fondamentali | Alpha Vantage / yfinance | fundamentals connector | `get_financials`, `get_ratios`, `get_earnings` | market_data |
| News/catalizzatori | Finnhub | news connector | `get_news` | market_data |
| Sentiment | Finnhub / StockTwits / Reddit / X | sentiment connectors | `get_news_sentiment`, `get_social_sentiment` | market_data/log |
| Calendario | Finnhub / FRED calendar sources | calendar connector | `get_calendar`, trigger events | market_data/trigger |
| Opzioni | IBKR / Tradier | options connector | `get_options_chain`, `select_contract` | market_data/execution |
| Aggregatore | OpenBB | meta-provider wrapper | fonte unificata o fallback router | dipende dal dato |

Questa tabella non decide ancora i provider definitivi: definisce il **posto** in cui ogni provider entra nel sistema.

## Policy per ogni fonte

Ogni fonte deve avere una scheda minima:

- dati coperti;
- granularita' e freshness;
- rate limit e costo;
- stabilita' API;
- chiave dedup;
- mapping al DB;
- fallback possibile;
- se il dato e' storico DB-first o live real-time-first;
- test offline con fake response.

Senza questa scheda, la fonte resta research, non dipendenza di codice.

## Relazione con `tools-inventory`

[[system/tools/tools-inventory]] descrive i tool dal punto di vista degli agenti. Questa pagina descrive cosa c'e' sotto quei tool.

Esempio:

- agente Technical chiama `compute_indicator`;
- `compute_indicator` legge OHLCV normalizzati dal DB;
- gli OHLCV arrivano da `yfinance` in dev o Twelve Data/Alpha Vantage in prod;
- l'agente non vede mai la differenza.

Questo evita duplicazioni, vendor lock-in e logica sparsa nei prompt.

## Backlog di ricerca

- **OpenBB**: da studiare come meta-provider o SDK di ricerca, non come dipendenza automatica.
- **FinRL**: da valutare per moduli sperimentali RL/quant research, fuori dal core iniziale.
- **Kronos**: da studiare come modello/fonte prior-art per time-series e linguaggio dei mercati.
- **optimizer**: reference per BAML views, FastAPI layer, scheduler, broker sync e portfolio optimization.
- **SFC**: reference per dashboard e analytics read-only.

## Primo deliverable pratico

Prima del codice agentico, produrre una tabella completa provider/tool con:

- famiglia tool di [[system/tools/tools-inventory]];
- provider candidato;
- wrapper da scrivere;
- DB tables toccate;
- test minimo;
- rischio principale.

Questa tabella diventa input diretto per il primo slice di [[system/foundation/codebase-architecture]].
