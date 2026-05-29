---
title: "Rizzo Trading Agent (Rizzo AI Academy)"
type: source
tags:
  - multi-agent
  - execution
  - quant
  - software
  - architecture
raw_source_path: "https://github.com/Rizzo-AI-Academy/rizzo-trading-agent"
created: 2026-05-29
updated: 2026-05-29
status: active
confidence: high
priority: high
area: software
related:
  - "[[system/modules/agents]]"
  - "[[system/modules/data-layer]]"
  - "[[system/modules/quant-backtesting]]"
  - "[[system/modules/agents]]"
  - "[[prior-art/papers/alpha-arena]]"
  - "[[syntheses/notebooklm-research-2026-05-13]]"
---

# Rizzo Trading Agent (Rizzo AI Academy)

Agente di trading LLM **open source funzionante** sviluppato da Rizzo AI Academy (Simone Rizzo), dichiaratamente ispirato ad [[prior-art/papers/alpha-arena|Alpha Arena]] (nof1.ai). È **il riferimento più vicino al nostro MVP**: un singolo file `main.py` orchestra un ciclo completo "raccolta dati multi-sorgente → prompt strutturato → decisione LLM JSON → esecuzione su exchange → logging su Postgres".

- **Repo**: https://github.com/Rizzo-AI-Academy/rizzo-trading-agent
- **Video presentazione**: https://www.youtube.com/watch?v=Vrl2Ar_SvSo
- **Licenza**: MIT (codice riutilizzabile liberamente)
- **Asset**: crypto perpetuals (BTC, ETH, SOL) su **Hyperliquid** (testnet/mainnet)
- **LLM**: OpenAI `gpt-5.1` con **Structured Output (JSON Schema strict)**
- **Deploy**: Railway (`railway.json`), Postgres come DB (`psycopg2`)
- **Stack**: `ccxt`, `pandas`, `numpy`, `ta`, `tradingview-screener`, `prophet`, `yfinance`, `hyperliquid-python-sdk`, `eth-account`, `openai`, `plotly`, `python-dotenv`

> ⚠️ Differenza di dominio: loro fanno **crypto perp con leva 1-10x su timeframe 15m**, noi facciamo **equity swing 4h/daily, deterministico**. Il valore qui è **architetturale e di codice**, non di strategia. Diversi pattern (whale alert, funding rate) sono crypto-specifici e non si applicano all'equity.

---

## Architettura del ciclo (`main.py`)

Pipeline lineare a ogni esecuzione (pensata per girare su cron/scheduler):

```
1. HyperLiquidTrader(secret_key, account_address, testnet)   # connessione exchange
2. indicators_txt, indicators_json = analyze_multiple_tickers(['BTC','ETH','SOL'])
3. news_txt       = fetch_latest_news()
4. sentiment_txt  = get_sentiment()        # Fear & Greed Index
5. forecasts_txt  = get_crypto_forecasts() # Prophet
   (whale_alerts  = format_whale_alerts_to_string()  -- disattivato)
6. account_status = bot.get_account_status()
7. stop_losses    = check_stop_loss(account_status)   # diff posizioni vs snapshot precedente
8. snapshot_id    = db_utils.log_account_status(account_status)
9. system_prompt  = open('system_prompt.txt').format(portfolio_data, msg_info)
10. out           = previsione_trading_agent(system_prompt)   # LLM → JSON
11. bot.execute_signal(out)                                   # esecuzione ordine
12. db_utils.log_bot_operation(out, system_prompt, indicators, news, sentiment, forecasts)
    + log_account_status(nuovo stato)
    (eccezione globale → db_utils.log_error con contesto completo)
```

**Pattern chiave riusabile**: il contesto multi-sorgente è assemblato in un'unica stringa con **tag XML** (`<indicatori>`, `<news>`, `<sentiment>`, `<forecast>`) e iniettato in `system_prompt.txt` via `.format()`. È esattamente il nostro **Prompt Builder** ([[system/modules/agents]]) — qui implementato nel modo più semplice possibile.

---

## Moduli e codice da cui estrarre / ispirarsi

### `trading_agent.py` — LLM decision (★ da estrarre)
Cuore della decisione. Usa la **OpenAI Responses API** con `text.format` di tipo `json_schema` **strict** → l'LLM è **obbligato** a restituire un oggetto valido. Schema dell'operazione di trade:

| Campo | Tipo | Vincoli |
|-------|------|---------|
| `operation` | enum | `open` / `close` / `hold` |
| `symbol` | enum | `BTC` / `ETH` / `SOL` |
| `direction` | enum | `long` / `short` |
| `target_portion_of_balance` | number | 0.0–1.0 (frazione di balance da allocare/chiudere) |
| `leverage` | number | 1–10 |
| `stop_loss_percent` | number | 1–3 |
| `reason` | string | 1–300 char |

Usa anche `reasoning={"effort":"medium","summary":"auto"}` e `include=["reasoning.encrypted_content", ...]`. **Da riusare**: lo schema JSON strict è il modello esatto del nostro contratto "decisione LLM → ordine deterministico". Adattare gli enum a equity e rimuovere `leverage` (o sostituirlo con opzioni Call/Put, vedi [[system/decision-log]]).

### `indicators.py` — Analisi tecnica (★ da estrarre, classe `CryptoTechnicalAnalysisHL`)
Calcolo indicatori con la libreria `ta` su candele dell'exchange. Da riusare per il **Quant Agent** ([[system/modules/quant-backtesting]]) — i metodi sono indipendenti dalla sorgente dati:
- `calculate_ema(data, period)` — `ta.trend.EMAIndicator`
- `calculate_macd(data)` — `ta.trend.MACD` → (macd, signal, diff)
- `calculate_rsi(data, period)` — `ta.momentum.RSIIndicator` (usa RSI 7 e 14)
- `calculate_atr(high, low, close, period)` — `ta.volatility.AverageTrueRange`
- `calculate_pivot_points(high, low, close)` — pivot classici PP/S1/S2/R1/R2 dal giorno precedente
- `get_complete_analysis(ticker)` — assembla: prezzo corrente, EMA20, MACD, RSI7/14, volume bid/ask da orderbook L2, pivot daily, contesto "longer term" (EMA20 vs EMA50, ATR3 vs ATR14, volume current vs average), serie intraday (ultime 10 candele) di mid prices/EMA/MACD/RSI
- `format_output(data)` — serializza tutto in stringa con tag `<TICKER_data>` per il prompt LLM
- mini-cache su `meta_and_asset_ctxs` (TTL 2s) per funding/OI/mark price
- `analyze_multiple_tickers(tickers)` → ritorna `(stringa_per_prompt, lista_json_per_DB)`

Pattern utile: **doppio output** (testo human-readable per l'LLM + JSON strutturato per il DB). `INTERVAL_TO_MS` mappa timeframe→millisecondi.

### `forecaster.py` — Forecasting Prophet (classe `HyperliquidForecaster`)
Usa **Facebook Prophet** per prevedere il prezzo a +1 step su 15m e 1h. Fetcha candele, costruisce DataFrame `ds`/`y`, `Prophet(daily_seasonality=True, weekly_seasonality=True)`, `predict` → restituisce `yhat`, `yhat_lower`, `yhat_upper` e variazione % attesa. **Spunto** per un modulo di forecasting statistico complementare all'LLM (da valutare per swing daily/4h: Prophet o alternative).

### `sentiment.py` — Fear & Greed Index
Chiama l'API CoinMarketCap `v3/fear-and-greed/historical` (header `X-CMC_PRO_API_KEY`, `limit=1`). Crypto-specifico, ma il **pattern "indice di sentiment di mercato come feature nel prompt"** è generalizzabile (per equity: VIX, put/call ratio, AAII sentiment).

### `news_feed.py` — News via RSS (★ pattern leggero da riusare)
`fetch_latest_news(max_chars=4000)` parsa l'**RSS feed** di CoinJournal con `xml.etree.ElementTree`, pulisce HTML (`_strip_html_tags`), normalizza date in UTC, e tronca al limite di caratteri. **Zero costi/API key**: pattern utile per un News Agent equity (basta cambiare il feed RSS — es. feed finanziari). Gestisce il troncamento intelligente per non sforare il budget di token.

### `whalealert.py` — Whale Alert (crypto-only)
Scraping di `whale-alert.io/data.json` per movimenti significativi on-chain. **Non applicabile all'equity** (disattivato anche nel loro `main.py`), ma documenta il pattern "segnale di flusso ordini grandi → feature".

### `hyperliquid_trader.py` — Esecuzione ordini (★ logica preziosa, classe `HyperLiquidTrader`)
Gestione completa dell'esecuzione su exchange. Anche se l'exchange è diverso, la **logica di esecuzione è il template del nostro modulo Exchange** ([[system/modules/data-layer]]):
- `_validate_order_input()` — valida i campi obbligatori del segnale JSON prima di eseguire
- `_round_price()` / `_round_size()` — **arrotondamento per tick-size / szDecimals** letti dai metadata dell'exchange (`meta()["universe"]`); evita reject per troppi decimali
- `set_leverage_for_symbol()` — imposta leva cross/isolated
- `execute_signal(order_json)` — dispatch su `hold`/`close`/`open`; per `open`: imposta leva → legge balance (`marginSummary.accountValue`) → calcola nozionale `balance * portion * leverage` → size grezza / mark price → arrotonda a min_size → `market_open` con slippage 1% → piazza **stop-loss** automatico
- `_place_stop_loss()` — ordine **Trigger Market con `reduce_only=True`** (chiude solo, non apre): per long SL sotto, per short SL sopra
- `get_account_status()` — normalizza posizioni: symbol, side, size, entry_price, mark_price, **pnl_usd**, leverage → struttura `{balance_usd, open_positions[]}`
- `debug_symbol_limits()` — stampa min size, decimali, max leverage per asset

**Da riusare**: il pattern "segnale JSON validato → calcolo size dal balance → ordine market + SL trigger reduce_only" è direttamente trasferibile a un broker equity (Alpaca/IBKR), sostituendo le chiamate SDK.

### `utils.py` — Rilevamento stop-loss esterno (★ pattern intelligente)
`check_stop_loss(account_status)`: confronta lo snapshot precedente (`account_status_old.json`) con quello attuale; se un simbolo è **sparito** dalle posizioni aperte → lo SL è scattato lato exchange → registra un'operazione `close` con `reason: "Stop loss"` e logga il PnL. **Pattern di reconciliation**: deduce le chiusure avvenute fuori dal controllo dell'agente confrontando gli stati. Utile per il nostro DB centrale che deve restare allineato all'exchange.

### `db_utils.py` — Logging su Postgres (★ schema da studiare per il nostro DB)
883 righe. `DATABASE_URL` env, `psycopg2`, `init_db()` crea tutto lo schema. **Schema relazionale completo** che è un'ottima base per il nostro **DB centrale** ([[system/modules/data-layer]]):

| Tabella | Scopo |
|---------|-------|
| `account_snapshots` | balance_usd + raw_payload JSONB, timestamp |
| `open_positions` | FK→snapshot; symbol, side, size, entry/mark price, pnl_usd, leverage, stop_loss_percent |
| `ai_contexts` | il system_prompt completo inviato all'LLM |
| `indicators_contexts` | FK→context; **tutti** gli indicatori per ticker (price, ema, macd, rsi, pivot, OI, funding, serie intraday in JSONB) |
| `news_contexts` | FK→context; news_text |
| `sentiment_contexts` | FK→context; value, classification, timestamp |
| `forecasts_contexts` | FK→context; ticker, timeframe, prediction, bounds, change_pct |
| `bot_operations` | FK→context; operation, symbol, direction, portion, leverage, raw_payload |
| `errors` | error_type, message, traceback, context JSONB, source |

**Principio chiave riusabile**: ogni decisione del bot (`bot_operations`) è collegata via FK al **contesto esatto** (`ai_contexts` + indicatori + news + sentiment + forecast) che l'ha generata. → **piena tracciabilità/audit e dataset pronto per backtesting/evaluation**. Allineato al nostro principio "tutto passa dal DB" e al debug via LangSmith. Funzioni: `log_account_status`, `log_bot_operation`, `log_error`, `get_latest_account_snapshot`, `get_recent_bot_operations`. Helper di normalizzazione JSON (`_normalize_for_json`, `_to_plain_number`).

### `system_prompt.txt` — Prompt del trader (★ da studiare)
Definisce il ruolo ("cryptocurrency trading AI"), inietta `Portfolio Data` e `<context_info>`, e impone **regole esplicite**:
- Una sola posizione per coin (long XOR short)
- Verifica posizioni correnti prima di aprire
- Può chiudere solo posizioni esistenti
- Leva alta (>5x) solo se molto confidente
- **"Pay a lot of attention to the fees, don't open/close frequently"** (controllo costi via prompt)
- **"Be very careful when you see that in the previous 15 minutes you have taken the stop loss on a position"** (memoria dello SL recente come guardia anti-overtrading)

`formatted_system_prompt.txt` è un esempio reale renderizzato (utile come riferimento del formato finale). Nota: molte di queste regole nel nostro design sono **deterministiche a monte (Statuto Python)** anziché affidate al prompt — vedi [[system/modules/agents]].

---

## Takeaway per il progetto

1. **Lo scheletro end-to-end del nostro MVP esiste già qui** e si può clonare adattandolo: raccolta feature → prompt builder con tag XML → LLM JSON strict → esecuzione validata → logging completo su Postgres.
2. **Structured Output JSON Schema strict** (OpenAI) è il meccanismo per garantire output parsabile dall'LLM — equivalente al nostro vincolo "output JSON obbligatorio" (noi su DeepSeek, vedi [[system/stack]]).
3. **Schema DB context→operation con FK** = tracciabilità totale e dataset di training/eval già strutturato.
4. **Esecuzione**: validazione input → size dal balance → market order + SL trigger `reduce_only` è il template del modulo Exchange.
5. **Reconciliation degli stop-loss esterni** via diff di snapshot è un pattern da adottare.
6. **News via RSS** = News Agent a costo zero (cambiare feed per l'equity).
7. **Limiti**: leva, whale alert, funding rate, Fear&Greed sono crypto-specifici; la nostra strategia (deterministica, equity, swing) diverge. Riusare il **codice infrastrutturale**, non la strategia.
