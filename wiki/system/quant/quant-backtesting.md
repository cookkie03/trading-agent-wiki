---
title: Quant Agent + Backtesting
type: build
tags:
  - build
  - strategy
  - software
created: 2026-05-13
updated: 2026-07-13
status: active
priority: high
area: software
related:
  - "[[system/foundation/architecture]]"
  - "[[system/foundation/stack]]"
  - "[[system/foundation/mvp]]"
  - "[[strategy/index]]"
  - "[[strategy/methods/trend-following]]"
  - "[[strategy/methods/factor-investing]]"
  - "[[notebooklm-research-2026-05-13]]"
---

# Quant Agent + Backtesting

Il componente che incorpora la strategia. Contiene tutta la logica quantitativa: quali segnali guardare, come combinarli, come validarli con backtest robusti. Si integra con il DB di [[system/data/data-layer]].

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
Il backtest di strategie deterministiche può diventare anche un **modulo/tool richiamabile dagli agenti**, purché resti separato dalla decisione live.

L'output (hit-rate, rendimento medio, drawdown per configurazione e per agente) alimenta poi: la taratura delle soglie operative + i pesi degli agenti nel learning loop → [[system/quant/learning-feedback-loop]].

**Dati**: già risolti — il DB interno storico (yfinance per dev, Alpha Vantage / Twelve Data per prod). Nessuna API esterna da chiamare durante la simulazione; si legge dal DB.

**Prossimo passo con Salvatore**: definire in dettaglio input (quali regole, quali parametri), output atteso e come leggere i risultati — da fare in chiamata.

---

## Backtesting come validatore continuo delle soglie (input di Luca 2026-06-04)

> Luca: *«il backtesting deve servire come metodo per validare costantemente tutte le soglie, tutti i rapporti definiti a monte (es. [[_meta/glossario#Risk/Reward Ratio (R:R)|R:R]] 1.5), e deve essere continuo e asincrono»*.

Il backtesting **non è un'attività una-tantum** che si fa prima di partire: è un **processo permanente** che gira **in parallelo e in asincrono** rispetto al ciclo operativo, con il compito di **tarare e ri-validare di continuo i parametri "definiti a monte"**. Sono parametri-soglia oggi fissati a mano (default ragionevoli) che il backtest deve confermare o correggere sui dati reali via via che si accumulano:

- **R:R minimo** (default ≥ 1.5) e i coefficienti **`k_stop` / `k_tp` / `k_entry`** in unità di ATR → [[system/investment/state-schemas]];
- periodo dell'**ATR** (default 14) e altri parametri degli indicatori;
- soglie dello **Statuto** (VaR max ~10%, cap settore/area, soglia di approvazione Risk ~60-70%) → [[system/agents/agents]];
- moltiplicatori del **position sizing** per livello di [[_meta/glossario#Conviction Level|conviction]] → [[system/investment/position-sizing]];
- soglie di attivazione degli **alert** (±X%, N deviazioni standard) → [[system/data/data-layer]];
- **pesi degli agenti** (ponderazione dinamica): la hit-rate storica per-agente → pesi nell'aggregazione del PM (input di Luca 2026-06-04) → [[system/quant/learning-feedback-loop]] §4.

**Implicazioni di design**:
- gira come **job asincrono** separato dal ciclo decisionale (non blocca il PM), sul mini-server 24/7;
- **continuo**: ri-esegue man mano che entrano nuovi dati di mercato e nuovi esiti di trade reali;
- **chiude il loop** con il [[system/quant/learning-feedback-loop]]: i risultati possono *proporre* nuovi valori-soglia, applicati con cautela (validazione [[_meta/glossario#Walk-Forward Backtesting|walk-forward]] / out-of-sample per non overfittare → [[strategy/questions-for-salvatore]]);
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

- **VectorBT**: framework Python di backtesting **vettorizzato** (lavora su intere serie storiche con pandas/numpy, molto veloce — testa molte combinazioni di parametri in poco tempo). Usato da MarketSenseAI. Spiegazione nel [[_meta/glossario]].
- **Costi di transazione**: niente più "10bps fisso" → modello **auto-adattivo** che usa le commissioni reali esposte dall'[[_meta/glossario#Adapter / Wrapper (broker)|adapter]] del broker ([[system/execution/execution]]). Finché non esiste il modello reale, conviene almeno definire tutte le tipologie di costo e permettere configurazione via file di config.
- **Dati**: da `market_data` nel DB di [[system/data/data-layer]] (OHLCV stock, timeframe 4h/daily)
- **Metriche obbligatorie**: Sharpe ratio, Sortino ratio, Max Drawdown, Win Rate, Calmar ratio
- **Insidie da evitare**: [[_meta/glossario#Look-Ahead Bias|look-ahead bias]]; **[[_meta/glossario#Overfitting|overfitting]]** e **significatività statistica vs benchmark** → da definire con Salvatore in [[strategy/questions-for-salvatore]].
- **Storico dati**: non abbiamo ancora anni di storico → si raccoglie *mentre* l'alpha gira; il modulo backtesting si aggiunge incrementalmente. Survivorship bias affrontato a sistema maturo.

---

## Decisioni prese

| Tema | Scelta |
|------|--------|
| Framework backtesting | VectorBT (fonte: MarketSenseAI) |
| Costi transazione | Simulare sempre (10bps per trade minimo) |
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

- **Dipende da [[system/data/data-layer]]**: legge `market_data` dal DB
- **[[system/agents/agents]]** dipende da questo: il Prompt Builder include l'output quant nel prompt del Trader

---

## Come contribuisce Salvatore

Salvatore porta il contenuto della strategia in **[[strategy/index]]** — questo modulo lo implementa:
1. Porta in `raw/` indicatori tecnici, strategie, casi reali, paper
2. L'agente ingesta e struttura il materiale in `strategy/methods/`, `strategy/indicators/`, `strategy/metrics/`
3. Quando un metodo è validato, Luca costruisce il tool Python corrispondente qui

*Vedere [[system/foundation/decision-log]] per le decisioni aperte legate a questo modulo.*
