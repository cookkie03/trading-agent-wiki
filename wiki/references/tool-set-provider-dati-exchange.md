---
title: "Tool Set, Provider Dati, Exchange"
type: source
tags:
  - source
  - infrastructure
  - market-structure
raw_source_path: "raw/archived/notes/Tool Set, Provider dati, Exchange.md"
created: 2026-05-22
updated: 2026-05-22
confidence: high
status: active
related:
  - "[[build/modules/module-a-exchange-db]]"
  - "[[build/stack]]"
  - "[[build/system-map]]"
---

# Tool Set, Provider Dati, Exchange

Panoramica dei broker con API Python disponibili in Italia e dei provider di dati di mercato gratuiti, con raccomandazioni per lo stack del trading agent. Fonte: note raw compilate (probabile output di ricerca AI su Claude/ChatGPT).

---

## Broker con API Python — Disponibili in Italia

### Interactive Brokers (IBKR) — Il riferimento assoluto

IBKR offre una REST API moderna con accesso alla più ampia gamma di funzionalità: account management, funding, reporting e trading. Include WebSocket streaming per dati real-time, notifiche critiche e market data.

A novembre 2025 IBKR gestisce oltre 2.5 milioni di account tramite la sua API robusta, abilitando algo trading su stocks, options, futures e forex.

La piattaforma TWS include 50+ order types e algoritmi, portfolio analysis, modelling, risk management tools e API integration — considerata la "Ferrari delle piattaforme trading".

- **Disponibile in Italia**: sì, pienamente operativo
- **Asset class**: Azioni, ETF, opzioni, futures, forex, bond, crypto
- **Python SDK**: `ib_insync` (community) + API ufficiale
- **Costo API**: gratuita con account (live o paper)

---

### Alpaca — Il migliore per algo trading puro

Alpaca è identificato come il miglior broker per algorithmic trading in Italia nel 2026, grazie alla sua API developer-friendly, basse commissioni e paper trading disponibile globalmente.

All-in-one: con poche API call si recuperano market data e si inviano ordini. SDK ufficiali disponibili in Python, JS e altri linguaggi.

- **Limiti**: il live trading richiede KYC ed è disponibile solo in certi paesi. Il paper trading (demo mode) è disponibile globalmente. Focalizzato su equity US + crypto.
- **Rilevanza per il progetto**: ottimo per phase testing, ma non su Binance/crypto

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

| Categoria | Strumento | Asset Class | Gratuito | Python |
|---|---|---|---|---|
| **Broker** | Interactive Brokers | Tutto | API gratis | `ib_insync` |
| **Broker** | Alpaca | US equity + crypto | paper gratis | SDK ufficiale |
| **Prezzi** | yfinance | Tutto | sì | sì |
| **Prezzi + TA** | Alpha Vantage | Tutto | 25/day | sì |
| **Real-time + news** | Finnhub | Tutto | 60/min | sì |
| **Aggregatore** | OpenBB | Tutto | sì | sì |
| **Macro** | FRED | Macro | sì | `fredapi` |
| **Multi-asset** | Twelve Data | Tutto | 800/day | sì |
| **Dataset** | Nasdaq Data Link | Multi | parziale | sì |

---

## Stack raccomandato per il Trading Agent (mercati tradizionali)

- **Esecuzione**: IBKR (copre tutto, API robusta, disponibile in Italia)
- **Dati prezzi + fondamentali**: `yfinance` per il dev, Alpha Vantage per la produzione
- **Macro + sentiment**: FRED + Finnhub
- **Aggregatore unificato**: OpenBB come layer di astrazione sopra tutto

> Nota: per il prototipo attuale su Binance/crypto, lo stack principale è Binance API (order book pubblico, dati storici, paper trading testnet). I provider sopra sono rilevanti per la fase successiva o per eventuali espansioni su equity.

---

## Relazione con il Modulo A

Il [[build/modules/module-a-exchange-db]] dovrà implementare i connector verso i provider scelti. La filosofia è: ogni provider diventa un modulo Python parametrizzabile che legge dall'API e scrive nel DB centrale. I tool non devono avere valori hardcodati (es. non "scarica ultimi 30 giorni" ma "scarica dal parametro `start_date` al parametro `end_date`").
