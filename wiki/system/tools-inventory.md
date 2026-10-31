---
title: "Tools Inventory — i tool che gli agenti possono chiamare"
type: synthesis
tags:
  - multi-agent
  - architecture
  - infrastructure
created: 2026-06-06
updated: 2026-06-06
status: active
related:
  - "[[system/modules/agents]]"
  - "[[system/modules/data-layer]]"
  - "[[system/data-providers]]"
  - "[[system/state-schemas]]"
  - "[[prior-art/tradingagents/code-wiki]]"
confidence: medium
area: software
---

# Tools Inventory — i tool che gli agenti possono chiamare

> 🟢 **Implementato (alpha v0, 2026-06-07)** — pacchetti `tradingagents/ingestion/` (A prezzi · C fondamentali · D news+social · E macro) e `tradingagents/tools/` (`get_realtime_quote` **real-time-first + write-through**, `get_open_positions_risk` = heat, `volume_spike`, `get_options_chain`+`select_contract`). B indicatori = `indicators/`; G portafoglio = `inject_portfolio_state`; I guardrail = `domain/risk.check_guardrails`. *Resta rifinitura*: il **tool-calling LLM-driven** (l'agente che emette le call da sé) — oggi i tool sono reali e usati dal brain, con la regola real-time-first applicata, ma invocati deterministicamente.

> **Stato: impianto approvato da Luca (2026-06-06).** Le 9 famiglie e le due regole trasversali sono confermate; 2 nodi risolti (portfolio auto+richiamabile · `compute_indicator` parametrico), restano aperti solo i vendor (live MVP + opzioni), da fissare a implementazione. Inventario di *cosa* gli agenti possono invocare durante il ragionamento. È il pezzo che rende concreta l'**autonomia informativa real-time first + write-through** decisa il 2026-06-05 ([[system/modules/agents]]). Il livello gemello è il **comportamento per-agente** (come ogni desk usa questi tool) → ancora aperto in [[system/modules/agents]].

## Come si legge un tool — le 5 etichette

Ogni tool è definito da cinque attributi:

1. **Cosa** — estrae un dato o calcola un valore.
2. **Live / Storico** — determina la **precedenza** (decisione 2026-06-05):
   - **Live / decision-critical** (prezzo, ultima news, quote opzioni) → l'agente prova **prima il tool real-time**, poi copia in DB.
   - **Storico / immutabile** (barre passate, bilanci depositati) → **check-presenza DB-first** ([[system/modules/data-layer]]); inutile ri-scaricare ciò che non cambia.
3. **Write-through?** — il dato live torna all'agente **e** ne scrive una copia nel DB → il DB resta **centro unico**.
4. **Agente/i** — chi lo usa (Market · Sentiment · Technical · Fondamentali · PM · Risk).
5. **Vendor** — fonte primaria / secondaria, dal mapping in [[system/data-providers]].

### Due regole trasversali (proposte come vincolanti)
- **Parametrici, mai hardcoded**: `get_ohlcv_history(ticker, start, end, interval)`, non "ultimi 30 giorni" (già nello stack, [[system/data-providers]]).
- **Adaptive extractor come rete**: ogni tool live passa per i guardrail di frequenza/rate-limit dell'adaptive extractor ([[system/modules/data-layer]]).

### Eredità dal fork TradingAgents
Molti tool esistono già come `dataflows` di TradingAgents (sezione "Data Retrieval Tools and Utilities", [[prior-art/tradingagents/code-wiki]]) e vanno **tenuti / potenziati / riscritti**. In tabella: **grassetto** = ereditabile quasi diretto; *normale* = da costruire ex-novo per il progetto.

---

## Inventario per famiglie

### A — Prezzi & quote
| Tool                                                                | Live/Storico       | Write-through   | Agente        | Vendor                              |
| ------------------------------------------------------------------- | ------------------ | --------------- | ------------- | ----------------------------------- |
| `get_realtime_quote(ticker)` — prezzo/bid/ask corrente              | **live**           | ✅               | Technical, PM | Finnhub · Alpaca                    |
| **`get_ohlcv_history(ticker, start, end, interval)`** — barre OHLCV | storico (DB-first) | n/a (già in DB) | Technical     | yfinance (dev) · Twelve Data (prod) |

### B — Indicatori tecnici (calcolo parametrico, on-demand)
| Tool | Live/Storico | Write-through | Agente | Vendor |
|------|--------------|---------------|--------|--------|
| **`compute_indicator(ticker, indicator, params)`** — ATR(14), RSI, MACD, SMA/EMA, Bollinger, 52w high/low, drawdown | calcolo su OHLCV dal DB | risultato cacheabile/precalcolabile | Technical | interno |
| `volume_spike(ticker, window, z_threshold)` — z-score volumi anomali | calcolo su DB | — | Technical | interno (idea board) |

> L'ATR usato dal sizing/`entry_price` arriva da qui ([[system/position-sizing]]). Indicatori "caldi" possono essere **pre-calcolati** in materialized view ([[system/db-access-performance]]); il tool resta per richieste parametriche fuori dal set pre-calcolato.

### C — Fondamentali
| Tool                                                                          | Live/Storico                           | Write-through | Agente       | Vendor                   |
| ----------------------------------------------------------------------------- | -------------------------------------- | ------------- | ------------ | ------------------------ |
| **`get_financials(ticker, statement, period)`** — balance / income / cashflow | storico (DB-first, `publication_date`) | n/a           | Fondamentali | Alpha Vantage · yfinance |
| `get_ratios(ticker)` — P/E (trailing vs current), P/B, ROE, margini           | semi-storico                           | —             | Fondamentali | Alpha Vantage · yfinance |
| **`get_earnings(ticker)`** — storico + prossimi earnings                      | semi-live                              | ✅ (prossimo)  | Fondamentali | Finnhub · AV             |

### D — News & sentiment
> **Divisione per tipo di informazione** (Luca 2026-06-06): **Market** usa le news come *catalizzatori* macro/settore; **Sentiment** copre il *mood/posizionamento* attingendo a **quante più fonti possibili** — vendor di notizie **+ social/forum** (Reddit, StockTwits, X) **+ piattaforme di sentiment dedicate**. L'elenco dei tool/fonti sentiment è un **sotto-lavoro aperto** (vedi sotto), legato all'aperto *"indicatori di sentiment"* con Salvatore.

| Tool | Live/Storico | Write-through | Agente | Vendor |
|------|--------------|---------------|--------|--------|
| **`get_news(ticker, since)`** — news recenti (come catalizzatori) | **live** | ✅ | Market | Finnhub |
| `get_news_sentiment(ticker)` — tono/sentiment delle news | **live** | ✅ | Sentiment | Finnhub · AV |
| `get_social_sentiment(ticker, platform)` — **aggregatore social/forum**: Reddit, StockTwits, X/Twitter | **live** | ✅ | Sentiment | *da definire (multi-vendor)* |
| **`get_insider_transactions(ticker)`** — insider trades | semi-live | ✅ | Sentiment, Fondamentali | Finnhub |

> **Sotto-lavoro aperto — fonti di sentiment**: enumerare e validare le piattaforme/API da cui pescare sentiment (Reddit/PRAW, StockTwits, X, news-sentiment, eventuali servizi dedicati) e come aggregarle in `get_social_sentiment`. L'obiettivo di Luca è la **massima copertura di fonti**. Si interseca con la definizione degli *indicatori di sentiment* con Salvatore → [[strategy/questions-for-salvatore]].

### E — Macro
| Tool | Live/Storico | Write-through | Agente | Vendor |
|------|--------------|---------------|--------|--------|
| `get_macro_series(series_id, start, end)` — GDP, CPI, fed funds, disoccupazione, yields | storico (DB-first) | n/a | Market | FRED |

> Mappa sugli indicatori macro che Salvatore sta definendo → [[strategy/indicators/macro-indicators]].

### F — Calendario
| Tool | Live/Storico | Write-through | Agente | Vendor |
|------|--------------|---------------|--------|--------|
| `get_calendar(type, window)` — earnings + calendario economico | semi-live | ✅ | Market, PM (alimenta i trigger di alert) | Finnhub |

### G — Portafoglio & conto (interni, area rendicontazione del DB)
| Tool | Live/Storico | Write-through | Agente | Vendor |
|------|--------------|---------------|--------|--------|
| **`inject_portfolio_state()`** — foto portafoglio: cassa, posizioni, distribuzione, P/L · **OBBLIGATORIO** · auto a ogni ciclo + richiamabile | DB rendicontazione | lettura | PM, Risk | interno |
| `get_open_positions_risk()` — **portfolio heat** corrente (somma rischi aperti) per sizing/Risk | DB rendicontazione | lettura | PM, Risk | interno |

> `inject_portfolio_state` è il tool deciso da Luca 2026-06-04 ([[system/modules/agents]]); `get_open_positions_risk` serve al cap di portfolio heat del [[system/position-sizing]].

### H — Opzioni (leva)
| Tool | Live/Storico | Write-through | Agente | Vendor |
|------|--------------|---------------|--------|--------|
| `get_options_chain(ticker, expiry, type)` — quote Call/Put per la leva | **live** | ✅ | Risk, PM | IBKR · Tradier |

> Attivo solo in fase `Strong Buy`/`Strong Sell` validata ([[system/modules/agents]] §Leva). Fuori MVP (Alpaca non copre opzioni reali).

### I — Guardrail Statuto (NON sono tool LLM)
I controlli dello Statuto (max % per area, VaR di portafoglio, diversificazione, riserva 10% cash) **non** sono tool che l'agente chiama: sono **check Python deterministici** nel gate del Risk Analyst ([[system/modules/agents]] §Guardrail). Elencati qui solo per completezza, per evitare di trasformarli per errore in tool LLM.

---

## Nodi risolti / aperti

**Risolti (Luca 2026-06-06):**
1. ✅ **`inject_portfolio_state` = automatico a ogni ciclo + richiamabile**: la foto del portafoglio è iniettata nel contesto all'avvio di ogni ciclo (così nessun agente decide "al buio"), ma resta un tool che l'agente può **ri-chiamare** se vuole la foto aggiornata durante il ragionamento. Coerente col real-time first.
2. ✅ **`compute_indicator` = un tool unico parametrico**: `compute_indicator(ticker, indicator, params)`, l'indicatore si sceglie via parametro. Più scalabile e meno superficie da mantenere; i nomi degli indicatori disponibili vanno elencati nel system prompt / docstring del tool.

**Ancora aperti:**
3. **Vendor dei dati live** (famiglie A/D/F — news, quote, calendario): da fissare **quando si implementa il data-layer**. Candidato naturale Finnhub (60 req/min free, copre news+sentiment+insider+earnings+real-time con una sola integrazione), ma non lo blocchiamo ora. Lo storico resta yfinance/FRED.
4. **Vendor opzioni** (famiglia H): IBKR (già broker prod) vs Tradier — da decidere quando si entra nelle opzioni (post-MVP).

## Prossimo passo collegato
Una volta fissato l'inventario, il livello successivo è il **comportamento per-agente**: per ciascun desk, *quali* di questi tool usa, in che ordine, con quale criterio di stop → [[system/modules/agents]] (TODO aperto).
