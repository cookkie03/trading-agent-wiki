
## 🏦 Broker con API Python — Disponibili in Italia

### ⭐ Interactive Brokers (IBKR) — Il riferimento assoluto

IBKR offre una REST API moderna con accesso alla più ampia gamma di funzionalità: account management, funding, reporting e trading. Include WebSocket streaming per dati real-time, notifiche critiche e market data.

Come di novembre 2025, IBKR gestisce oltre 2.5 milioni di account tramite la sua API robusta, abilitando algo trading su stocks, options, futures e forex.

La piattaforma TWS include 50+ order types e algoritmi, portfolio analysis, modelling, risk management tools e API integration — considerata la Ferrari delle piattaforme trading.

**Disponibile in Italia:** ✅ Sì, pienamente operativo  
**Asset class:** Azioni, ETF, opzioni, futures, forex, bond, crypto  
**Python SDK:** `ib_insync` (community) + API ufficiale  
**Costo API:** Gratuita con account (live o paper)

---

### Alpaca — Il migliore per algo trading puro

Alpaca è stato identificato come il miglior broker per algorithmic trading in Italia nel 2026, grazie alla sua API developer-friendly, basse commissioni e paper trading disponibile globalmente.

Alpaca è un all-in-one: con poche API call puoi recuperare market data e inviare ordini. SDK ufficiali disponibili in Python, JS e altri linguaggi.

**Limiti:** Il live trading richiede KYC ed è disponibile solo in certi paesi — ma il paper trading (demo mode) è disponibile globalmente. Focalizzato su equity US + crypto.

---

### DEGIRO — Attenzione

DEGIRO non ha un'API ufficiale. Quindi per automazione è da escludere.

---

## 📊 Provider di Dati di Mercato + Indicatori — Gratuiti con Python API

Ecco il quadro completo, organizzato per use case:

---

### 1. `yfinance` — Il punto di partenza

La libreria Python non ufficiale di Yahoo Finance. Zero costi, zero API key, installazione in 1 riga.

- Prezzi storici e intraday per azioni, ETF, indici, forex, crypto
- Dati fondamentali (bilancio, P/E, dividendi)
- Facilissima integrazione con `pandas`
- Permette di fetchare dati storici, dividendi e stock splits

**Limite:** non ufficiale, può rompersi con aggiornamenti di Yahoo.

---

### 2. Alpha Vantage — Il più completo sul free tier

Alpha Vantage offre JSON API gratuite per dati storici e real-time di stock market e options, con oltre 50 indicatori tecnici. Supporta intraday, daily, weekly e monthly.

Include anche dati macro US: Real GDP, Treasury yields, Federal Funds Rate, CPI, inflazione, disoccupazione, nonché AI-powered news sentiment analysis, earnings call transcripts e insider trading data.

**Free tier:** 25 richieste/giorno → per uso intensivo serve il piano a pagamento.  
**Python:** libreria ufficiale `alpha_vantage`

---

### 3. Finnhub — Real-time + News + Sentiment

Finnhub fornisce dati finanziari di alta qualità con aggiornamenti real-time del mercato azionario, inclusi prezzi real-time, company info, alternative data come insider trades e sentiment analysis.

Ottimo per: earnings calendars, news per ticker, economic data, crypto.  
**Free tier:** generoso, 60 richieste/minuto  
**Python:** SDK ufficiale disponibile

---

### 4. OpenBB Platform — Il meta-strumento

OpenBB è un open-source data router e toolbox che dà accesso streamlinato a sorgenti multiple (FRED, Yahoo Finance, Alpha Vantage, IMF e altri) sotto una singola API consistente.

In 2026 OpenBB supporta integrazione con Yahoo Finance, Alpha Vantage e FRED, ottimizzata per low-latency con tempi di risposta medi sotto 200ms per la maggior parte delle richieste.

Ideale per aggregare tutto in un unico client Python.

---

### 5. FRED (Federal Reserve Economic Data) — Macro data

Fornito dalla Federal Reserve di St. Louis, completamente gratuito:

- GDP, inflazione, tassi d'interesse, disoccupazione, money supply
- Oltre 800.000 serie storiche
- FRED è una buona fonte per dati macroeconomici inclusi unemployment, GDP, interest rates e money supply
- Python: libreria `fredapi`

---

### 6. Twelve Data — Tecnico + Multi-asset

Twelve Data combina semplicità e versatilità fornendo prezzi intraday, daily e storici su multiple asset class, con supporto built-in per data visualization e integrazione con charting libraries.

**Free tier:** 800 richieste/giorno  
**Python:** SDK ufficiale

---

### 7. Nasdaq Data Link (ex Quandl)

Nasdaq Data Link offre accesso a oltre 250 dataset inclusi equity, opzioni, indici, mutual funds e indicatori economici, tramite REST e streaming API con supporto Python, R, Excel e SQL.

Free tier disponibile con dataset come WIKI EOD Stock Prices.

---

## 🗺️ Riepilogo visivo

|Categoria|Strumento|Asset Class|Gratuito|Python|
|---|---|---|---|---|
|**Broker**|Interactive Brokers|Tutto|✅ API gratis|✅ `ib_insync`|
|**Broker**|Alpaca|US equity + crypto|✅ paper gratis|✅ SDK ufficiale|
|**Prezzi**|yfinance|Tutto|✅|✅|
|**Prezzi + TA**|Alpha Vantage|Tutto|✅ (25/day)|✅|
|**Real-time + news**|Finnhub|Tutto|✅ (60/min)|✅|
|**Aggregatore**|OpenBB|Tutto|✅|✅|
|**Macro**|FRED|Macro|✅|✅ `fredapi`|
|**Multi-asset**|Twelve Data|Tutto|✅ (800/day)|✅|
|**Dataset**|Nasdaq Data Link|Multi|✅ parziale|✅|

---

## 💡 Il mio consiglio per il tuo stack in Italia

Per un trading agent serio su mercati tradizionali, ti consiglio questo stack:

- **Esecuzione:** IBKR (copre tutto, API robusta, disponibile in Italia)
- **Dati prezzi + fondamentali:** `yfinance` per il dev, Alpha Vantage per la produzione
- **Macro + sentiment:** FRED + Finnhub
- **Aggregatore unificato:** OpenBB come layer di astrazione sopra tutto

Vuoi che aggiunga tutto questo alla wiki su Google Drive, o prima preferisci procedere con gli schemi architetturali del trading agent?