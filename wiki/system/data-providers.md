---
title: "Tool Set, Provider Dati, Exchange"
type: source
tags:
  - source
  - infrastructure
  - market-structure
raw_source_path: "raw/archived/notes/Tool Set, Provider dati, Exchange.md"
created: 2026-05-22
updated: 2026-05-29
confidence: high
status: active
related:
  - "[[system/modules/data-layer]]"
  - "[[system/stack]]"
  - "[[system/architecture]]"
---

# Tool Set, Provider Dati, Exchange

Panoramica dei broker con API Python disponibili in Italia e dei provider di dati di mercato gratuiti, con raccomandazioni per lo stack del trading agent. Fonte: note raw compilate (probabile output di ricerca AI su Claude/ChatGPT).

> **Distinzione fondamentale**: il broker serve principalmente per **eseguire ordini** (e per il [[_meta/glossario#Paper Trading / Testnet|paper trading]] dell'MVP). La **popolazione del DB** (prezzi storici, fondamentali, news, macro, sentiment) avviene tramite data vendor separati. Le due cose si sovrappongono solo parzialmente — IBKR ad esempio può fornire entrambe, ma non è detto sia la scelta ottimale per ogni tipo di dato.

---

## Broker — Solo per l'esecuzione ordini

### Specifiche richieste dal progetto

| Categoria | Requisito | Motivazione |
|-----------|-----------|-------------|
| **API** | REST + WebSocket | REST per ordini, WebSocket per feed real-time (adaptive extractor) |
| **API** | Paper trading sandbox = specchio del live | Il codice non deve cambiare passando a live |
| **API** | Python SDK ufficiale o CCXT-compatible | Stack Python; interfaccia astratta = cambio broker = cambio config |
| **API** | Rate limit adeguati | Adaptive extractor: alta freq vicino al target, daily altrove |
| **API** | Tipi ordine: limit, SL, TP | Hard constraint architetturale |
| **Asset** | Equity US (S&P 500) — MVP | Benchmark primario |
| **Asset** | Equity internazionale | Secondo benchmark 60/40 all-world |
| **Asset** | Multi-currency (USD, EUR minimo) | Portafoglio non solo EUR |
| **Asset** | Roadmap: commodities, BTC, futures, opzioni | Espansione post-MVP |
| **Safety** | Broker regolamentato (MiFID II / ESMA o SEC+FINRA) | Requisito legale e fiduciario |
| **Safety** | Fondi segregati + protezione depositi | Rischio controparte |
| **Safety** | Uptime SLA documentato | Sistema autonomo, downtime = trade mancati |
| **Costi** | Commissioni basse o zero per equity | Drag minimo sul rendimento |
| **Costi** | Paper trading gratuito | Dev + testing indefinito prima del live |
| **Dev** | Documentazione API di qualità, API stabile | Velocità di sviluppo, no breaking change imprevisti |

> Il broker **non** è il fornitore principale di dati storici o fondamentali — quelli vengono dai data vendor sotto.

---

### Interactive Brokers (IBKR) — Il riferimento assoluto

IBKR offre una REST API moderna con accesso alla più ampia gamma di funzionalità: account management, funding, reporting e trading. Include WebSocket streaming per dati real-time, notifiche critiche e market data.

A novembre 2025 IBKR gestisce oltre 2.5 milioni di account tramite la sua API robusta, abilitando algo trading su stocks, options, futures e forex.

La piattaforma TWS include 50+ order types e algoritmi, portfolio analysis, modelling, risk management tools e API integration — considerata la "Ferrari delle piattaforme trading".

- **Disponibile in Italia**: sì, pienamente operativo
- **Asset class**: Azioni, ETF, opzioni, futures, forex, bond, crypto
- **Python SDK**: `ib_insync` (community) + API ufficiale
- **Costo API**: gratuita con account (live o paper)

---

### Alpaca — Il migliore per algo trading puro (MVP candidate)

Alpaca è identificato come il miglior broker per algorithmic trading in Italia nel 2026, grazie alla sua API developer-friendly, basse commissioni e paper trading disponibile globalmente.

All-in-one: con poche API call si recuperano market data e si inviano ordini. SDK ufficiali disponibili in Python, JS e altri linguaggi.

- **Limiti**: il live trading richiede KYC ed è disponibile solo in certi paesi. Il paper trading (demo mode) è disponibile globalmente. Focalizzato su equity US + crypto.
- **Rilevanza per il progetto**: candidato ideale per la fase MVP/paper trading — API developer-first, zero friction, paper trading perfetto. Limite: US equity only, niente opzioni reali. Per produzione con copertura internazionale → IBKR.

---

### DEGIRO — Da escludere

DEGIRO non ha un'API ufficiale. Per automazione è da escludere.

---

## Provider di Dati di Mercato + Indicatori — Gratuiti con Python API

### 1. `yfinance` — Il punto di partenza

La libreria Python non ufficiale di Yahoo Finance. Zero costi, zero API key, installazione in 1 riga.

- Prezzi storici e intraday per azioni, ETF, indici, forex, crypto
- Dati fondamentali (bilancio, P/E, dividendi)
- Facilissima integrazione con `pandas`
- Permette di fetchare dati storici, dividendi e stock splits
- **Limite**: non ufficiale, può rompersi con aggiornamenti di Yahoo
- **Uso nel progetto**: sviluppo e prototipazione; sostituire con fonti più stabili in produzione

---

### 2. Alpha Vantage — Il più completo sul free tier

Alpha Vantage offre JSON API gratuite per dati storici e real-time di stock market e options, con oltre 50 indicatori tecnici. Supporta intraday, daily, weekly e monthly.

Include anche dati macro US: Real GDP, Treasury yields, Federal Funds Rate, CPI, inflazione, disoccupazione, nonché AI-powered news sentiment analysis, earnings call transcripts e insider trading data.

- **Free tier**: 25 richieste/giorno → per uso intensivo serve piano a pagamento
- **Python**: libreria ufficiale `alpha_vantage`

---

### 3. Finnhub — Real-time + News + Sentiment

Finnhub fornisce dati finanziari di alta qualità con aggiornamenti real-time del mercato azionario, inclusi prezzi real-time, company info, alternative data come insider trades e sentiment analysis.

- Ottimo per: earnings calendars, news per ticker, economic data, crypto
- **Free tier**: generoso, 60 richieste/minuto
- **Python**: SDK ufficiale disponibile

---

### 4. OpenBB Platform — Il meta-strumento (aggregatore)

OpenBB è un open-source data router e toolbox che dà accesso streamlinato a sorgenti multiple (FRED, Yahoo Finance, Alpha Vantage, IMF e altri) sotto una singola API consistente.

Nel 2026 OpenBB supporta integrazione con Yahoo Finance, Alpha Vantage e FRED, ottimizzata per low-latency con tempi di risposta medi sotto 200ms per la maggior parte delle richieste.

- Ideale per aggregare tutto in un unico client Python
- Layer di astrazione sopra tutti i provider

---

### 5. FRED (Federal Reserve Economic Data) — Macro data

Fornito dalla Federal Reserve di St. Louis, completamente gratuito:

- GDP, inflazione, tassi d'interesse, disoccupazione, money supply
- Oltre 800.000 serie storiche
- Buona fonte per dati macroeconomici inclusi unemployment, GDP, interest rates e money supply
- **Python**: libreria `fredapi`

---

### 6. Twelve Data — Tecnico + Multi-asset

Twelve Data combina semplicità e versatilità fornendo prezzi intraday, daily e storici su multiple asset class, con supporto built-in per data visualization e integrazione con charting libraries.

- **Free tier**: 800 richieste/giorno
- **Python**: SDK ufficiale

---

### 7. Nasdaq Data Link (ex Quandl)

Nasdaq Data Link offre accesso a oltre 250 dataset inclusi equity, opzioni, indici, mutual funds e indicatori economici, tramite REST e streaming API con supporto Python, R, Excel e SQL.

Free tier disponibile con dataset come WIKI EOD Stock Prices.

---

## Riepilogo

| Ruolo | Strumento | Asset Class | Gratuito | Python |
|-------|-----------|-------------|----------|--------|
| **Broker (esecuzione)** | Interactive Brokers | Tutto | API gratis | `ib_insync` |
| **Broker (MVP paper)** | Alpaca | US equity + crypto | paper gratis | SDK ufficiale |
| **Prezzi storici** | yfinance | Tutto | sì | sì |
| **Prezzi + TA + fondamentali** | Alpha Vantage | Tutto | 25/day free | sì |
| **Real-time + news + sentiment** | Finnhub | Tutto | 60/min free | sì |
| **Aggregatore** | OpenBB | Tutto | sì | sì |
| **Macro** | FRED | Macro | sì | `fredapi` |
| **Multi-asset prezzi** | Twelve Data | Tutto | 800/day free | sì |
| **Dataset storici** | Nasdaq Data Link | Multi | parziale | sì |

---

## Stack raccomandato per il Trading Agent

### Esecuzione ordini (broker)
- **MVP / paper trading**: Alpaca — API developer-first, zero commission, US stocks only, paper trading identico al live
- **Produzione**: IBKR — copre tutto (equity internazionale, futures, opzioni), API robusta, disponibile in Italia

### Copy trading / monetizzazione
- **Darwinex** — progettata per algo trader: collega Python → MT5 → Darwinex → DARWIN (prodotto finanziario verificato FCA). Compenso: 20% performance fee. Integrazione diretta con IBKR. Da attivare dopo il paper trading. → [[system/ideas-log]]

### Popolazione DB (data vendor, separati dal broker)
- **Prezzi OHLCV storici + fondamentali**: `yfinance` per il dev → Alpha Vantage o Twelve Data per la produzione
- **News + sentiment + insider trading**: Finnhub (60 req/min free, ottimo per il Market Alert Agent)
- **Macro (GDP, tassi, inflazione)**: FRED — gratuito, 800k+ serie storiche
- **Aggregatore unificato**: OpenBB come layer di astrazione sopra tutti i provider (unica API, sostituire sorgenti senza riscrivere i connector)

---

## Relazione con il Modulo Exchange + DB

Il [[system/modules/data-layer]] dovrà implementare i connector verso i provider scelti. La filosofia è: ogni provider diventa un modulo Python parametrizzabile che legge dall'API e scrive nel DB centrale. I tool non devono avere valori hardcodati (es. non "scarica ultimi 30 giorni" ma "scarica dal parametro `start_date` al parametro `end_date`").

### Mapping provider → area DB

| Area DB | Fonte principale | Fonte secondaria |
|---------|-----------------|-----------------|
| `market_data` — prezzi | yfinance (dev) / Twelve Data (prod) | Alpha Vantage |
| `market_data` — fondamentali | Alpha Vantage | yfinance |
| `market_data` — news + sentiment | Finnhub | Alpha Vantage news |
| `market_data` — macro | FRED | Alpha Vantage macro |
| `market_data` — insider trading | Finnhub | Alpha Vantage |
| `market_data` — calendario economico | Finnhub (earnings calendar) | — |
| `market_data` — tassi di cambio | Alpha Vantage / Twelve Data | — |
| Esecuzione ordini | Alpaca (MVP) → IBKR (prod) | — |

---
## Commenti recuperati da iCloud (2026-07-01)

> Commenti Obsidian `%%...%%` presenti nella vecchia copia iCloud (`7054827`) e reinseriti senza sovrascrivere il contenuto corrente.

%%super interessante, implementarlo come primo layer di informazioni e configurarlo per massimo wide di estrazione dati, poi integrare con dati del broker (alpaca/ibkr) e poi fonti esterne%%

%%stack di data vendor e popolazione del db da rivalutare alla luce della preferenza per openbb%%

%%da rivalutare, soprattutto alla luce della preferenza per openbb, per altro se possiamo scaricare anche dal broker, forse preferirei, quindi per esempio per i prezzi usare dati real time in flusso continuo web socket usando alpaca/ibkr%%

