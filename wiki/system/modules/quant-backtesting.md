---
title: "Quant Agent + Backtesting"
type: build
tags:
  - build
  - strategy
  - software
created: 2026-05-13
updated: 2026-06-11
status: active
priority: high
area: software
related:
  - "[[system/architecture]]"
  - "[[system/stack]]"
  - "[[system/mvp]]"
  - "[[strategy/index]]"
  - "[[strategy/methods/trend-following]]"
  - "[[strategy/methods/factor-investing]]"
  - "[[syntheses/notebooklm-research-2026-05-13]]"
---

# Quant Agent + Backtesting

Il componente che incorpora la strategia. Contiene tutta la logica quantitativa: quali segnali guardare, come combinarli, come validarli con backtest robusti. Si integra con il DB di [[system/modules/data-layer]].

---

## Riferimenti di codice (repo esterni)

- **Indicatori tecnici (lib `ta`)**: [[prior-art/libraries/rizzo-trading-agent]] — `indicators.py` (EMA, MACD, RSI 7/14, [[_meta/glossario#ATR (Average True Range)|ATR]], [[_meta/glossario#Pivot Points|pivot points]], doppio output testo+JSON per prompt e DB).
- **Metriche performance/rischio (pandas puro, quasi copia-incollabili)**: [[prior-art/libraries/sfc-portfolio-tracker]] — `analytics.py` ([[_meta/glossario#Sharpe Ratio|Sharpe]], [[_meta/glossario#Sortino Ratio|Sortino]], Calmar, max DD, [[_meta/glossario#VaR (Value at Risk)|VaR]], [[_meta/glossario#CVaR (Conditional Value at Risk)|CVaR]], alpha/beta) e `analytics_plus.py` (QuantStats + PyPortfolioOpt: efficient frontier, Monte Carlo, risk contribution). Catalogo KPI completo nella pagina del tracker.
- **Ricostruzione curva equity giornaliera per backtest**: [[prior-art/libraries/sfc-portfolio-tracker]] — `build_nav_history.py`.
- **Motore quant completo (sklearn API)**: [[prior-art/libraries/cvx-portfolio-optimizer]] — libreria `optimizer/` (moments, optimization, validation Walk-Forward/CPCV, scoring, factors).

---

## Cosa fa

- Implementa la **strategia quantitativa** scelta (vedi sotto)
- Esegue **backtest robusti** sui dati storici in `market_data` (via [[_meta/glossario#VectorBT|VectorBT]])
- Calcola indicatori tecnici parametrizzabili (RSI, MACD, Pivot Points, medie mobili...)
- Produce output strutturato nel DB → `module_outputs` (per il Prompt Builder)
- Genera metriche di valutazione per ogni strategia testata

## Output atteso

> Prime metriche su dati reali: Sharpe ratio, [[_meta/glossario#Win Rate|win rate]], [[_meta/glossario#Drawdown|drawdown]] per la strategia scelta.

---

## Cos'è il backtesting nel nostro sistema

Il backtesting è la risposta alla domanda: *"se avessimo applicato questa strategia dal 2004 al 2025, com'è andata?"*

Si costruiscono **script Python con regole deterministiche** di entrata/uscita (es. "entra se succede X, esci se succede Y"), li si fa girare su serie storiche del DB interno (yfinance / Alpha Vantage) — con VectorBT come motore (vettorizzato, veloce, molte combinazioni in parallelo). Si fanno girare molte simulazioni in stile Monte Carlo per ottenere la distribuzione dei rendimenti. L'AI **non gira durante la simulazione** — il processo è puramente Python deterministico.

L'output (hit-rate, rendimento medio, drawdown per configurazione e per agente) alimenta poi: la taratura delle soglie operative + i pesi degli agenti nel learning loop → [[system/learning-feedback-loop]].

**Dati**: già risolti — il DB interno storico (yfinance per dev, Alpha Vantage / Twelve Data per prod). Nessuna API esterna da chiamare durante la simulazione; si legge dal DB.

**Prossimo passo con Salvatore**: definire in dettaglio input (quali regole, quali parametri), output atteso e come leggere i risultati — da fare in chiamata.

---

## Backtesting come validatore continuo delle soglie (input di Luca 2026-06-04)

> Luca: *«il backtesting deve servire come metodo per validare costantemente tutte le soglie, tutti i rapporti definiti a monte (es. [[_meta/glossario#Risk/Reward Ratio (R:R)|R:R]] 1.5), e deve essere continuo e asincrono»*.

Il backtesting **non è un'attività una-tantum** che si fa prima di partire: è un **processo permanente** che gira **in parallelo e in asincrono** rispetto al ciclo operativo, con il compito di **tarare e ri-validare di continuo i parametri "definiti a monte"**. Sono parametri-soglia oggi fissati a mano (default ragionevoli) che il backtest deve confermare o correggere sui dati reali via via che si accumulano:

- **R:R minimo** (default ≥ 1.5) e i coefficienti **`k_stop` / `k_tp` / `k_entry`** in unità di ATR → [[system/state-schemas]];
- periodo dell'**ATR** (default 14) e altri parametri degli indicatori;
- soglie dello **Statuto** (VaR max ~10%, cap settore/area, soglia di approvazione Risk ~60-70%) → [[system/modules/agents]];
- moltiplicatori del **position sizing** per livello di [[_meta/glossario#Conviction Level|conviction]] → [[system/position-sizing]];
- soglie di attivazione degli **alert** (±X%, N deviazioni standard) → [[system/modules/data-layer]];
- **pesi degli agenti** (ponderazione dinamica): la hit-rate storica per-agente → pesi nell'aggregazione del PM (input di Luca 2026-06-04) → [[system/learning-feedback-loop]] §4.

**Implicazioni di design**:
- gira come **job asincrono** separato dal ciclo decisionale (non blocca il PM), sul mini-server 24/7;
- **continuo**: ri-esegue man mano che entrano nuovi dati di mercato e nuovi esiti di trade reali;
- **chiude il loop** con il [[system/learning-feedback-loop]]: i risultati possono *proporre* nuovi valori-soglia, applicati con cautela (validazione [[_meta/glossario#Walk-Forward Backtesting|walk-forward]] / out-of-sample per non overfittare → [[strategy/questions-for-salvatore]]);
- ogni parametro tarabile va quindi tenuto come **configurazione esterna**, non hardcodato, così il backtest può scriverne di aggiornati.

---

## Strategia — stato attuale

**Orientamento**: multi-factor (fondamentali + tecnici). Non ancora formalizzato.

| Categoria | Esempi | Stato |
|-----------|--------|-------|
| Indicatori tecnici | RSI, MACD, Pivot Points, medie mobili | Da raccogliere con Salvatore |
| Fattori fondamentali | P/E, revenue trend, macro (tassi, PIL) | Da raccogliere con Salvatore |
| Segnali di sentiment | Fear & Greed, news score | Fase successiva |

**Principio di parametrizzazione**: ogni indicatore è un tool che accetta parametri in input (es. `moving_average(period=N)`), non valori hardcodati. L'agente può sperimentare diversi valori senza toccare il codice.

**Principio di calcolo interno (2026-06-02)**: dai vendor si estraggono **solo le osservazioni grezze**; tutte le metriche calcolabili (P/E e i suoi 5 tipi, ratio, metriche derivate) si **calcolano internamente** dai dati grezzi già nel DB e si riscrivono nel DB. Questo centralizza accesso in lettura/scrittura e riduce le chiamate esterne. Luca: *«i dati calcolabili si calcolano internamente senza richieste, da lì si calcolano anche le metriche derivate, estraendo dai vendor solo le osservazioni»*.

**Fattori come "vocabolario" per l'agente**: i fattori devono poter essere **calcolati in grande quantità**; sarà l'agente AI a saperli usare/combinare/valutare. Compito di Luca: dargli gli **strumenti** (tool di calcolo), non la logica d'uso. Salvatore prepara il vocabolario di metriche (market driver + indicatori di valuation) → [[strategy/questions-for-salvatore]]. Approccio **incrementale**: prima un set base funzionante, poi si aggiungono fattori.

### Posizione di Salvatore su TA, fondamentali e sentiment (2026-05-29)
*Fonte: call del 2026-05-29.*
- **Analisi tecnica usata bene** (non "candele alla guru di Dubai"): minimi/massimi a **52 settimane**, range del prezzo e suoi sforamenti, **drawdown**, **volumi**, capire cosa è successo nel giorno di uno sforamento. Serve ad avere "il quadro" (come una dashboard vs dati grezzi), non a fare trading da grafico. Posizione **ibrida col sentiment**.
- **Sentiment**: non ha indicatori propri standard (al massimo indici di paura) → **da inventare/definire**. Legge tweet/posizioni delle persone.
- **Fondamentali**: non sono "pochi". Es. esistono **5 tipi di P/E** (normale/current, **trailing**, **forward**); Salvatore usa il confronto **trailing vs current** (capire se il calo è dovuto al prezzo o agli EPS). Dare un **tool** per calcolarli e lasciar combinare all'agente.
- **Factor investing / regressioni / strumenti statistici**: utili ma "un'altra parte della finanza", competenze non ancora possedute → per ora fuori scope MVP.

---

## Tech

> 🌿 **Stato (2026-06-11)**: l'evoluzione descritta in questa sezione (VectorBT default, sweep 3-D, walk-forward, **job notturno schedulato**) vive sul branch **`feat/vectorbt-backtest`**, non ancora su `main`. Su `main` il backend VectorBT è stato *revertato* (resta solo il motore `custom`): main è pulito da VectorBT in attesa del merge del branch. Vedi [[system/decision-log]] 2026-06-11.

### Due backend affiancati (stesso contratto `BacktestResult`)
Implementati in `tradingagents/backtesting/`, selezionabili via `config.toml [backtest] engine`:

- **`vectorbt`** (default sul branch) — `engine_vbt.py`: motore **vettorizzato** (richiede l'extra `backtest`: `uv sync --extra backtest`). Stessa logica ATR (`k_entry`/`k_stop`/`k_tp`) e **stesso sizing risk-based** (`position_size`) del custom, ma simulato con `vbt.Portfolio.from_signals` (stop/target nativi `sl_stop`/`tp_stop`, `fees` supportate). Calcola anche **Sharpe/Sortino/Calmar/profit_factor**. Serve per **velocità, sweep e walk-forward**.
- **`custom`** — `engine.py`: motore **event-driven** scritto a mano, scorre le barre intra-bar (`low`/`high`), riusa **le stesse** `indicators.core.atr` + `domain.risk.position_size`. È la **verità 1:1 col live** e resta come riferimento/riconciliazione. Long-only, una posizione alla volta, nessun costo.

> ⚠️ **Insidia nota (riconciliazione)**: VectorBT applica gli stop a livello di **barra** (vettorizzato), il custom **intra-barra** su `low`/`high`. I due **concordano sul segno e l'ordine di grandezza** (verificato con sizing allineato: stesso n. trade e hit-rate, rendimenti vicini), ma **non sono bit-identici**. Prima di tarare soglie in produzione con VectorBT, riconciliare sempre su un caso noto col motore custom.

### VectorBT al massimo: sweep 3-D + walk-forward
- **`sweep(bars, k_stop_grid, k_tp_grid, atr_period_grid, rank_by)`** — grid-search su **3 dimensioni** (`k_stop` × `k_tp` × `atr_period`), default 5×4×3 = 60 combinazioni per simbolo. Scarta le combo con R:R < 1, ordina per `rank_by` (default **`sharpe`**, più robusto del return puro; alternative: sortino/calmar/total_return/profit_factor). È il "validatore continuo delle soglie" del [[system/decision-log]] 2026-06-04.
- **`walk_forward(bars, …, n_splits)`** — validazione **out-of-sample** (anti-overfitting): per ogni fold tara i parametri in-sample e li misura out-of-sample; restituisce `oos_mean_sharpe`/`oos_mean_return` e i **`robust_params`** (combo più frequente tra i fold). Affronta la richiesta di walk-forward / significatività di [[strategy/questions-for-salvatore]].

### Job notturno schedulato (il backtest cablato nel sistema)
- **`backtesting/scheduler.py`**: `run_nightly_backtest` gira lo sweep + walk-forward su **ogni simbolo della watchlist** (fallback: universo), **persiste** i risultati nel DB e — se `apply_robust` — scrive le soglie **mediane** (conservativo) nel `charter`.
- **Timing**: `seconds_until_hour(hour)` + `nightly_loop` dormono fino all'ora configurata (default **02:00**, mercati chiusi) e ripetono ogni notte; un errore in una run viene loggato e **non uccide mai** lo scheduler.
- **Persistenza**: tabella **`backtest_results`** (`BacktestResultRow`) con best-params + metriche (Sharpe/Sortino/Calmar) + esito walk-forward (`oos_mean_sharpe`, `robust_params`) + payload (top-5 sweep + fold). La leggerà la dashboard di osservabilità / il learning loop; **non** alimenta il ciclo live direttamente.
- **CLI**: `python -m tradingagents.cli backtest` (one-shot), `--nightly` (loop notturno), `--apply-robust` (scrive le soglie nel charter).
- **Daemon**: `cli start` lancia un **secondo processo detached** per il job notturno (PID/log separati in `~/.tradingagents/backtest.{pid,log}`); `stop`/`status` gestiscono entrambi i processi. Configurabile via `[backtest] nightly_enabled` / `nightly_hour`.

### Resto del tech
- **Costi di transazione**: niente più "10bps fisso" → modello **auto-adattivo** che usa le commissioni reali esposte dall'[[_meta/glossario#Adapter / Wrapper (broker)|adapter]] del broker ([[system/modules/execution]]). Il backend vectorbt accetta `fees` per simularli; il custom oggi li ignora.
- **Dati**: da `price_bars` nel DB di [[system/modules/data-layer]] (OHLCV stock, timeframe 4h/daily), via `indicators.db.recent_bars` (default `lookback=750` barre per simbolo).
- **Metriche**: il custom calcola hit-rate, return, max drawdown; il backend vectorbt espone anche **Sharpe/Sortino/Calmar/profit factor** (popolati in `BacktestResult`).
- **Insidie da evitare**: [[_meta/glossario#Look-Ahead Bias|look-ahead bias]]; **[[_meta/glossario#Overfitting|overfitting]]** (mitigato dal walk-forward) e **significatività statistica vs benchmark** → da definire con Salvatore in [[strategy/questions-for-salvatore]].
- **Storico dati**: non abbiamo ancora anni di storico → si raccoglie *mentre* l'alpha gira; il modulo backtesting si aggiunge incrementalmente. Survivorship bias affrontato a sistema maturo.

> **Integrazione nel sistema**: il backtest **non è un tool degli agenti** e **non gira nel ciclo di trading** (l'AI non gira durante la simulazione — decisione 2026-06-04). È un **job offline/asincrono notturno** che legge il DB storico, tara le soglie (`k_stop`/`k_tp`/ATR/sizing) e alimenta il [[system/learning-feedback-loop]]. Gli agenti ne consumano *indirettamente* l'output (le soglie tarate in `config.toml`/`charter`), non lo invocano mai. ✅ **Aggancio runtime fatto** (branch): scheduler notturno nel daemon.

---

## Decisioni prese

| Tema | Scelta |
|------|--------|
| Framework backtesting | **Due backend** (2026-06-10): `custom` event-driven 1:1 col live (default) + `vectorbt` vettorizzato per sweep/metriche. VectorBT fonte: MarketSenseAI |
| Costi transazione | Simulare sempre (`fees` nel backend vectorbt; auto-adattivo dal broker a sistema maturo) |
| Principio | Tool parametrizzabili, non hardcodati |

## Domande aperte

> Queste domande bloccano o influenzano la progettazione del modulo.

- **Quale strategia quantitativa esatta?** Multi-factor è l'orientamento, ma Salvatore deve portare i fattori concreti → [[strategy/questions-for-salvatore]].
- **VaR, overfitting, test statistici sul benchmark** → tutti da definire con Salvatore in [[strategy/questions-for-salvatore]].
- **Frequenza ciclo: 4h vs 24h?** Dipende dai primi backtest — quale timeframe ha più segnale/rumore per [[_meta/glossario#Swing Trading|swing trading]] equity?
- **Modulo TA da includere?** Rischio: TA mal calibrata corrompe l'output. Progettare come modulo opzionale e testare A/B (con/senza).
- **Multi-asset o singolo asset nel backtest iniziale?** MVP singolo asset, ma il codice deve supportare multi-asset per il futuro.

---

## Dipendenze

- **Dipende da [[system/modules/data-layer]]**: legge `market_data` dal DB
- **[[system/modules/agents]]** dipende da questo: il Prompt Builder include l'output quant nel prompt del Trader

---

## Come contribuisce Salvatore

Salvatore porta il contenuto della strategia in **[[strategy/index]]** — questo modulo lo implementa:
1. Porta in `raw/` indicatori tecnici, strategie, casi reali, paper
2. L'agente ingesta e struttura il materiale in `strategy/methods/`, `strategy/indicators/`, `strategy/metrics/`
3. Quando un metodo è validato, Luca costruisce il tool Python corrispondente qui

*Vedere [[system/decision-log]] per le decisioni aperte legate a questo modulo.*
