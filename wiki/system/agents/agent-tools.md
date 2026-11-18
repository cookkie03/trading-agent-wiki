---
title: Agent Tools — bozza MVP dei tool per agente
type: synthesis
tags:
  - agent-behaviors
  - tools
  - multi-agent
created: 2026-11-18T00:00:00.000Z
updated: 2026-11-18T00:00:00.000Z
status: active
confidence: medium
area: software
related:
  - '[[system/agents/agent-behaviors]]'
  - '[[system/tools/tools-inventory]]'
  - '[[system/investment/state-schemas]]'
  - '[[prior-art/libraries/openalice]]'
---

# Agent Tools — bozza MVP dei tool per agente

> **Decisione Luca 2026-11-18 (Q28):** tabella dei tool approvata, con parametri. È una bozza utilizzabile, non lo schema definitivo: i nomi e i tipi diventano schemi Pydantic nello spec.

Principi:

- Nessun agente ha un tool che invia ordini al broker. L'ordine nasce solo da `decide(accept)` del PM, passa per Bozza → Risk Gate → coda di approvazione umana → broker (codice).
- I tool di dati sono deterministici e in sola lettura; i numeri arrivano da qui, mai dall'LLM.
- Gli agenti non sanno se il broker è paper o live (Q36): nessun tool espone quell'informazione.
- Market Analyst: lavora a orari fissi (pre-market ed eventi macro), aggiorna una visione di mercato per settore nello state, che ogni ciclo riceve in automatico per il settore del ticker (Q47). Può scrivere al PM: il messaggio vale come Alert sui ticker toccati, un ciclo per ticker (Q48).
- Nessun parametro `as_of` (Q41): il trading è in tempo reale, ogni dato ricevuto vale per quello che è.
- Ogni chiamata (tool, LLM, subagent) salva su DB token, costo, latenza ed esito; queste metriche non tornano agli agenti (Q42).

## Tool comuni a tutti gli agenti

| Tool | Parametri | Ritorno |
|------|-----------|---------|
| `send_message` | `to: AgentId`, `chat: ChatRef` (ticker o tema), `text: str` | id messaggio; conta sul Budget del ciclo |
| `fill_state` | `ticker: str`, `text: str` | scrive solo la sezione testuale dell'agente chiamante |
| `suggest_state` | `ticker: str`, `field: StateField`, `value`, `reason: str` | valore accettato o errore di validazione (campo non suo, fuori limiti) |
| `read_state` | `ticker: str`, `sections: list[str] \| None` | state corrente del ticker (Analysis degli altri, bozza, decisioni) |
| `call_subagent` | `task: str`, `tools: list[ToolName]` (sottoinsieme read-only dei propri), `max_steps: int = 10` | testo del risultato; conta sul budget |
| `read_portfolio` | — | cassa, equity, posizioni, ordini aperti (iniettato anche nel contesto) |

Campi di `suggest_state` per agente (limiti deterministici nel codice):

- ogni Analyst: `suggested_direction ∈ {buy, sell, hold}`, `suggested_conviction ∈ [0, 1]`;
- Risk Analyst: `k_entry`, `risk_fraction`;
- Technical Analyst: `k_stop`, `k_tp`.

## Market Analyst (fuori dai cicli, Q32)

Lavora per conto suo sulle chat di tema (macro, settori), con il suo calendario; risponde alle richieste degli altri agenti.

| Tool | Parametri |
|------|-----------|
| `get_macro_series` | `series_id: str` (FRED via OpenBB), `start: date`, `end: date \| None`, `frequency: str \| None` |
| `get_news` | `topic: str \| None`, `tickers: list[str] \| None`, `since: datetime`, `limit: int = 20` |
| `get_economic_calendar` | `start: date`, `end: date`, `country: str = "US"`, `min_importance: int = 2` |
| `get_sector_performance` | `period: Literal["1d","1w","1m","3m","ytd"]` |

## Sentiment Analyst

| Tool | Parametri |
|------|-----------|
| `get_news` | `tickers: [ticker]`, `since: datetime`, `limit: int = 20` (il tono lo giudica l'agente) |
| `get_analyst_ratings` | `ticker: str`, `since: date` → consenso, upgrade/downgrade, target price |
| `get_insider_transactions` | `ticker: str`, `since: date` |

Fonti social: post-MVP.

## Technical Analyst

| Tool | Parametri |
|------|-----------|
| `get_quote` | `ticker: str` → ultimo prezzo, bid/ask, volume |
| `get_ohlcv` | `ticker: str`, `interval: Literal["1d","1h"] = "1d"`, `lookback: int = 200` |
| `compute_indicator` | `ticker: str`, `name: Literal["sma","ema","rsi","macd","atr","pivots"]`, `params: dict` (es. `{"window": 14}`), `interval = "1d"` |

## Fundamental Analyst

| Tool | Parametri |
|------|-----------|
| `get_financials` | `ticker: str`, `statement: Literal["income","balance","cashflow"]`, `period: Literal["annual","quarter"] = "quarter"`, `limit: int = 4` |
| `get_ratios` | `ticker: str` → P/E, EV/EBITDA, margini, debito/equity |
| `get_earnings` | `ticker: str` → prossima data, ultime sorprese EPS/ricavi |

## Risk Analyst

| Tool | Parametri |
|------|-----------|
| `get_portfolio_risk` | `ticker: str \| None` → esposizione per titolo/settore, concentrazione, rischio aperto totale, correlazione con le posizioni |
| `get_order_draft` | `ticker: str` → bozza corrente (entry, SL, TP, size, R:R) e coefficienti |
| `compute_indicator` | come Technical (ATR, volatilità) |

## Portfolio Manager

| Tool | Parametri |
|------|-----------|
| `decide` | `ticker: str`, `action: Literal["accept","defer"]`, `rationale: str` (richiede un `schedule_task` sul ticker nello stesso ciclo) |
| `read_watchlist` | — |
| `update_watchlist` | `op: Literal["add","remove"]`, `ticker: str`, `reason: str` (Q30) |
| `get_order_draft` | come Risk |

`schedule_task` (Q56) sostituisce la `next_check_date`: è il Controllo programmato, limitato tra un minimo e un massimo configurabili in giorni di borsa (Q33). Il bracket order scade al Controllo programmato.

## Tool di programmazione (PM e Market Analyst)

| Tool | Parametri |
|------|-----------|
| `schedule_task` | `when: datetime` (limitato tra min e max), `chat: ChatRef` (ticker per il PM, tema per il Market), `note: str` (cosa verificare) → sostituisce l'eventuale controllo già programmato sulla stessa chat |

Alla scadenza il Trigger engine genera un Alert per il PM (ticker) o riattiva il Market Analyst (tema).
