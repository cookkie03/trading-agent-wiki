---
title: "Agent Behaviors — comportamento per-agente del desk"
type: synthesis
tags:
  - multi-agent
  - architecture
created: 2026-06-06
updated: 2026-06-06
status: draft
related:
  - "[[system/modules/agents]]"
  - "[[system/tools-inventory]]"
  - "[[system/state-schemas]]"
  - "[[system/modules/quant-backtesting]]"
confidence: medium
area: software
---

# Agent Behaviors — comportamento per-agente del desk

> **Stato: PROPOSTA (draft) — in attesa di reazione di Luca.** È il livello **appena sotto i system prompt**: *cosa fa esattamente* ognuno dei 4 agenti del desk. Si appoggia sui tool definiti in [[system/tools-inventory]] e sui campi dello state in [[system/state-schemas]]. Prima il comportamento, poi il prompt che lo realizza.

## Le 5 dimensioni di ogni agente

Ogni agente è definito da: **Input** (cosa riceve) · **Tool** (quali tool dell'inventario usa) · **Output** (quali campi dello state scrive) · **Ragionamento** (lo stile/angolo) · **Stop** (quando ha finito il suo lavoro). I riferimenti tool (A/B/C…) sono le famiglie di [[system/tools-inventory]].

---

## Desk Analyst Research

### Market — contesto macro & settoriale (top-down)
- **Input**: `ticker`, settore, `portfolio_context`, `current_price`.
- **Tool**: E `get_macro_series` · F `get_calendar` · D `get_news` (solo come **catalizzatori** macro/settore) · A `get_realtime_quote`.
- **Output**: `market_view` — regime macro (crescita/inflazione/tassi), forza del settore, eventi imminenti dal calendario economico. Riga in `agent_opinions`.
- **Ragionamento**: **top-down** (macro → settore → titolo). Domanda guida: *il contesto è a favore o contro la direzione che si sta valutando?*
- **Stop**: coperti regime macro + posizione del settore + eventi/dati macro imminenti rilevanti.

### Sentiment — news flow & posizionamento
- **Input**: `ticker`, news recenti dal last check.
- **Tool**: D `get_news` (come **tono**) · D `get_sentiment` · D `get_insider_transactions`.
- **Output**: `sentiment_view` — tono delle news, sentiment aggregato, insider buying/selling, anomalie. Riga in `agent_opinions`.
- **Ragionamento**: legge il **"mood"** e lo **confronta col prezzo** — il consenso è già prezzato? C'è divergenza prezzo/notizie da sfruttare? (lega all'idea "tradare prima della folla" → [[system/ideas-log]]).
- **Stop**: coperte le news rilevanti dal last check + sentiment + insider recenti.

---

## Desk Analyst Technical

### Technical — price action, momentum, volatilità
- **Input**: `ticker`, OHLCV storico.
- **Tool**: A `get_ohlcv_history` · B `compute_indicator` (ATR, RSI, MACD, SMA/EMA, Bollinger, 52w high/low, drawdown) · B `volume_spike`.
- **Output**: `technical_view` — trend, momentum, supporti/resistenze, picchi di volume. **Fornisce l'ATR** che alimenta `entry_price`/`stop_loss`/`take_profit` ([[system/state-schemas]]) e il volatility-adjustment del [[system/position-sizing]]. Riga in `agent_opinions`.
- **Ragionamento**: trend-following + livelli tecnici; **quantifica la volatilità** (è il fornitore dei numeri ATR per tutto il resto della pipeline).
- **Stop**: coperti trend + momentum + volatilità (ATR) + livelli chiave.

### Fondamentali (financials) — salute & valuation (bottom-up)
- **Input**: `ticker`.
- **Tool**: C `get_financials` (balance/income/cashflow) · C `get_ratios` (P/E trailing vs current, P/B, ROE, margini) · C `get_earnings`.
- **Output**: `fundamental_view` — salute del bilancio, valuation, crescita, **prossimi earnings come rischio-evento** (gap). Riga in `agent_opinions`.
- **Ragionamento**: **bottom-up** sul valore intrinseco; flag esplicito se ci sono earnings imminenti (rischio gap che cambia il profilo di rischio del trade).
- **Stop**: coperti bilancio + ratio + calendario earnings del titolo.

---

## Comportamenti trasversali (uguali per tutti e 4)

1. **Opinione per-agente**: ognuno lascia in `agent_opinions` la sua `suggested_direction` + `suggested_conviction` + razionale breve. Il **PM aggrega e decide** la `direction`/`conviction` finale (deciso 2026-06-04, [[system/state-schemas]]).
2. **Real-time first + autonomia**: per il dato vivo l'agente prova **prima il tool real-time** e può **richiamarlo più volte** per verificare/essere sicuro (decisione 2026-06-05, [[system/modules/agents]]).
3. **Ruolo di validatore**: ognuno garantisce **completezza · correttezza · esaustività fonti** della *propria* sezione prima del sealing (opzione validazione collettiva, [[system/state-schemas]]).
4. **Contributo a `key_factors`**: ogni agente deposita i fattori che ha calcolato (con come sono stati letti) → [[system/modules/quant-backtesting]].
5. **Solo reasoning, niente calcoli a mano**: i numeri (indicatori, ratio, ATR) vengono **dai tool deterministici**, non "a occhio" dall'LLM (filosofia agenti, [[system/modules/agents]]).

---

## Snodi aperti (in attesa di Luca)

1. **Proprietà delle news Market vs Sentiment**: entrambi usano `get_news`. Proposta: **Market** legge le news come *catalizzatori* macro/settore (un taglio sui tassi, un dato sull'occupazione); **Sentiment** le legge come *tono/posizionamento* (il mercato è euforico o in panico su questo titolo?). Stesso tool, lente diversa — da confermare.
2. **Chi propone una direzione**: tutti e 4 lasciano `suggested_direction` + `suggested_conviction`, oppure solo i ruoli "direzionali" (Technical + Sentiment) mentre Market e Fondamentali restano *contesto/qualificazione*? (proposta: tutti e 4 propongono, è più ricco per il PM e più informativo per il backtest hit-rate per-agente).
3. **Criterio di stop**: ogni agente si **auto-ferma** su una checklist di copertura, oppure è il **PM** che continua a interrogarlo finché non ha "info sufficienti" (istruzione *"nel dubbio chiedi sempre"*)? (proposta: auto-stop per-agente come *default*, ma il PM può sempre richiamarlo → i due meccanismi convivono).

## Prossimo passo collegato
Una volta fissato il comportamento, si scrive il **system prompt** di ciascun agente che lo realizza (Prompt Builder) → [[system/modules/agents]] (decisione aperta).
