---
title: "Agent Behaviors — comportamento per-agente del desk"
type: synthesis
tags:
  - multi-agent
  - architecture
created: 2026-06-06
updated: 2026-07-13
status: active
related:
  - "[[system/agents/agents]]"
  - "[[system/tools/tools-inventory]]"
  - "[[system/investment/state-schemas]]"
  - "[[system/quant/quant-backtesting]]"
confidence: medium
area: software
---

# Agent Behaviors — comportamento per-agente del desk

> **Stato:** specifica di lavoro. Market/Sentiment/Technical/Fondamentali hanno cinque dimensioni esplicite; il Risk Analyst ha una sezione equivalente. Restano decisioni condivise il suo posizionamento esatto e l'elenco delle fonti sentiment. Prima il comportamento, poi il prompt che lo realizza.

## Le 5 dimensioni di ogni agente

Ogni agente è definito da: **Input** (cosa riceve) · **Tool** (quali tool dell'inventario usa) · **Output** (quali campi dello state scrive) · **Ragionamento** (lo stile/angolo) · **Stop** (quando ha finito il suo lavoro). I riferimenti tool (A/B/C…) sono le famiglie di [[system/tools/tools-inventory]].

---

## Desk Analyst Research

### Market — contesto macro & settoriale (top-down)
- **Input**: `ticker`, settore, `portfolio_context`, `current_price`.
- **Tool**: E `get_macro_series` · F `get_calendar` · D `get_news` (solo come **catalizzatori** macro/settore) · A `get_realtime_quote`.
- **Output**: `market_view` — regime macro (crescita/inflazione/tassi), forza del settore, eventi imminenti dal calendario economico. Riga in `agent_opinions` (contributo primario: **la direzione di contesto**).
- **Ragionamento**: **top-down** (macro → settore → titolo). Domanda guida: *il contesto è a favore o contro la direzione che si sta valutando?*
- **Stop**: coperti regime macro + posizione del settore + eventi/dati macro imminenti rilevanti.

### Sentiment — sentiment multi-fonte & posizionamento
- **Input**: `ticker`, news recenti, **stream social/forum** dal last check.
- **Tool**: D `get_news_sentiment` (tono delle news) · D `get_social_sentiment` (Reddit, StockTwits, X/Twitter — **aggregatore multi-piattaforma**) · D `get_insider_transactions`. → l'obiettivo (Luca 2026-06-06) è **raccogliere quante più fonti di sentiment possibili**, non solo i vendor di notizie. L'elenco completo delle fonti/tool è un sotto-lavoro aperto, vedi [[system/tools/tools-inventory]] famiglia D.
- **Output**: `sentiment_view` — sentiment aggregato cross-fonte (news + social + insider), divergenze, anomalie di posizionamento. Riga in `agent_opinions`.
- **Ragionamento**: aggrega il **"mood" da più piattaforme** e lo **confronta col prezzo** — il consenso è già prezzato? C'è divergenza prezzo/notizie/social da sfruttare? (lega all'idea "tradare prima della folla" → [[system/foundation/ideas-log]]).
- **Stop**: coperte le fonti rilevanti dal last check (news + social + insider).

---

## Desk Analyst Technical

### Technical — price action, momentum, volatilità
- **Input**: `ticker`, OHLCV storico.
- **Tool**: A `get_ohlcv_history` · B `compute_indicator` (ATR, RSI, MACD, SMA/EMA, Bollinger, 52w high/low, drawdown) · B `volume_spike`.
- **Output**: `technical_view` — trend, momentum, supporti/resistenze, picchi di volume. **Fornisce l'ATR** che alimenta `entry_price`/`stop_loss`/`take_profit` ([[system/investment/state-schemas]]) e il volatility-adjustment del [[system/investment/position-sizing]]. Riga in `agent_opinions` (contributo primario: **i livelli di entry/stop/target**).
- **Ragionamento**: trend-following + livelli tecnici; **quantifica la volatilità** (è il fornitore dei numeri ATR per tutto il resto della pipeline).
- **Stop**: coperti trend + momentum + volatilità (ATR) + livelli chiave.

Per ogni output tecnico vanno definiti tool deterministici dedicati, così da velocizzare i calcoli e ridurre al minimo numeri “inventati” dall'LLM.

### Fondamentali (financials) — salute & valuation (bottom-up)
- **Input**: `ticker`.
- **Tool**: C `get_financials` (balance/income/cashflow) · C `get_ratios` (P/E trailing vs current, P/B, ROE, margini) · C `get_earnings`.
- **Output**: `fundamental_view` — salute del bilancio, valuation, crescita, **prossimi earnings come rischio-evento** (gap). Riga in `agent_opinions`.
- **Ragionamento**: **bottom-up** sul valore intrinseco; flag esplicito se ci sono earnings imminenti (rischio gap che cambia il profilo di rischio del trade).
- **Stop**: coperti bilancio + ratio + calendario earnings del titolo.

---

## Risk Analyst — gate bear, sizing e guardrail

> **Decisione ancora da chiudere con Luca e Salvatore:** questa sezione descrive il comportamento minimo comune. Il Risk può essere desk pari, gate finale oppure operare a due livelli (titolo e portafoglio); la scelta modifica il routing, non i suoi strumenti o vincoli.

- **Input**: `agent_opinions`, livelli tecnici, contesto portafoglio, regole dello Statuto.
- **Tool**: G `inject_portfolio_state` · G `get_open_positions_risk` · H `get_options_chain` quando la leva è ammessa · I guardrail deterministici lato risk engine.
- **Output**: `risk_view` / `risk_gate` — approvazione o rifiuto motivato, limiti di sizing, violazioni di guardrail, richieste di approfondimento.
- **Ragionamento**: prende il lato **antitesi bear** della proposta e verifica se l'idea resta valida quando la si passa attraverso vincoli di rischio, concentrazione, costi, drawdown, leva e coerenza col portafoglio.
- **Stop**: la proposta è approvata, respinta o rimandata al PM con un elenco chiaro di informazioni mancanti o vincoli rotti.

---

## Comportamenti trasversali (uguali per tutti e 4)

1. **Opinione per-agente — tutti contribuiscono, ognuno la sua parte** (Luca 2026-06-06): ognuno lascia in `agent_opinions` la sua `suggested_direction` + `suggested_conviction` + razionale breve. Ogni agente ha un **contributo primario** legato alla sua specialità (Market → direzione di contesto; Technical → livelli entry/stop/target; Sentiment → mood/posizionamento; Fondamentali → valore/rischio-evento), ma **tutti possono esprimersi su tutto** (nessuno è zittito su una dimensione fuori dalla sua specialità). Il **PM aggrega e decide** la `direction`/`conviction` finale (deciso 2026-06-04, [[system/investment/state-schemas]]).
2. **Real-time first + autonomia**: per il dato vivo l'agente prova **prima il tool real-time** e può **richiamarlo più volte** per verificare/essere sicuro (decisione 2026-06-05, [[system/agents/agents]]).
3. **Ruolo di validatore**: ognuno garantisce **completezza · correttezza · esaustività fonti** della *propria* sezione durante la ricerca; il PM compie l'ultima verifica di insieme ([[system/investment/state-schemas]]).
4. **Contributo a `key_factors`**: ogni agente deposita i fattori che ha calcolato (con come sono stati letti) → [[system/quant/quant-backtesting]].
5. **Solo reasoning, niente calcoli a mano**: i numeri (indicatori, ratio, ATR) vengono **dai tool deterministici**, non "a occhio" dall'LLM (filosofia agenti, [[system/agents/agents]]).

---

## Snodi — decisi da Luca (2026-06-06)

1. ✅ **Spartizione news/sentiment per tipo di informazione**: **Market** tratta le notizie come *catalizzatori* macro/settore (taglio tassi, dato occupazione); **Sentiment** copre il *mood/posizionamento* attingendo a **più fonti possibili** — non solo vendor di notizie ma **social e piattaforme di sentiment** (Reddit, StockTwits, X…). La divisione è per **tipo di informazione**, non per "chi tocca il tool news". → genera un **sotto-lavoro aperto**: enumerare le fonti/tool di sentiment (famiglia D di [[system/tools/tools-inventory]]); lega all'aperto *"indicatori di sentiment da inventare"* con Salvatore.
2. ✅ **Tutti contribuiscono alla direzione, ognuno la sua parte**: ogni agente propone secondo la sua specialità (contributo primario) ma **può esprimersi su tutto**; il PM aggrega. Vedi trasversale #1 sopra.
3. ✅ **Stop = auto-stop + il PM può richiamare**: ogni agente si ferma su una checklist di copertura (default), ma il PM può sempre richiamarlo se ha ancora dubbi (*"nel dubbio chiedi sempre"*). I due meccanismi convivono.

## Lavoro aperto generato
- **Enumerare le fonti/tool di sentiment** (Reddit, StockTwits, X, news sentiment, eventuali API dedicate) → da aggiungere alla famiglia D di [[system/tools/tools-inventory]]; si interseca con *"indicatori di sentiment"* da definire con Salvatore ([[strategy/questions-for-salvatore]]).

## Prossimo passo collegato
Una volta fissato il comportamento, si scrive il **system prompt** di ciascun agente che lo realizza (Prompt Builder) → [[system/agents/agents]] (decisione aperta).

