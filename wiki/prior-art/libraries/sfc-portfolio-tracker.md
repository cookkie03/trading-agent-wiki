---
title: "SFC Portfolio Tracker (Sbirrondi)"
type: source
tags:
  - quant
  - software
  - backtesting
  - infrastructure
raw_source_path: "https://github.com/Sbirrondi/sfc-portfolio-tracker"
created: 2026-05-29
updated: 2026-05-29
status: active
confidence: high
priority: medium
area: software
related:
  - "[[system/quant/quant-backtesting]]"
  - "[[system/data/data-layer]]"
  - "[[prior-art/libraries/cvx-portfolio-optimizer]]"
  - "[[system/data/data-providers]]"
  - "[[system/foundation/architecture]]"
---

# SFC Portfolio Tracker (Sbirrondi)

Tracker/dashboard di un **fondo reale in EUR** ("SFC fund") costruito in **Streamlit** + Plotly. A differenza di [[prior-art/libraries/rizzo-trading-agent]] (esecuzione automatica) e [[prior-art/libraries/cvx-portfolio-optimizer]] (ottimizzazione), questo è il **riferimento per il lato analytics / dashboard / performance reporting / NAV tracking** del nostro sistema. Tutto su **equity, ETF e bond** (il nostro dominio MVP), niente crypto.

- **Repo**: https://github.com/Sbirrondi/sfc-portfolio-tracker
- **Stack**: `streamlit`, `yfinance`, `pandas`, `numpy`, `plotly`, `quantstats`, `pyportfolioopt`, `scipy`, `streamlit-lightweight-charts`, `beautifulsoup4`, `openpyxl`
- **Persistenza**: file su disco (`data/`: CSV + JSON) sincronizzati su GitHub via API (`github_sync.py`) — niente database
- **Modello dati**: il fondo è **transaction-based** — le posizioni sono *derivate* dalle transazioni (single source of truth)
- **App principale**: `app.py` (~4000 righe Streamlit, multi-pagina)

> Niente README nel repo: la conoscenza è nelle docstring dei moduli (riportate sotto) e nei test (`tests/`).

---

## Modello dati (`data/`)

`fund_transactions.csv` (verità) → da cui si calcolano `fund_positions.csv`, `fund_cash.json`, `fund_nav_history.csv`, `fund_asset_allocation.csv`. Più `isin_map.json` (ISIN→ticker), `overrides.json` / `position_overrides.json` (metadati manuali), `fund_info.json`. **Pattern da adottare**: derivare lo stato dalle transazioni invece di salvarlo direttamente → ricostruibilità e audit totali (concettualmente vicino al nostro DB event-sourced, [[system/data/data-layer]]).

---

## Moduli e codice da cui estrarre / ispirarsi

### `analytics.py` — Metriche di performance e rischio (★ da estrarre)
Modulo puro pandas/numpy, **direttamente riusabile** nel nostro **Quant/Backtesting** ([[system/quant/quant-backtesting]]). Funzioni:
- `detect_frequency(prices)` — deduce daily/weekly/monthly e i `periods_per_year`
- `calculate_returns`, `cumulative_returns`, `total_return`
- `annualized_return`, `annualized_volatility`
- `sharpe_ratio`, `sortino_ratio` (risk_free configurabile)
- `max_drawdown`, `drawdown_series`, `calmar_ratio`
- `var_historical`, `cvar` (confidence configurabile)
- `calculate_alpha_beta(returns, benchmark)` — regressione vs benchmark
- `rolling_metrics`, `monthly_returns_table`, `performance_report`

### `analytics_plus.py` — Analisi avanzata (★ QuantStats + PyPortfolioOpt)
Integra **QuantStats** e **PyPortfolioOpt** (lazy import per non rompere se mancano). Sovrapponibile alle funzioni di [[prior-art/libraries/cvx-portfolio-optimizer]], ma con un'API molto più semplice — utile come **alternativa leggera** o per la dashboard:
- `advanced_risk_metrics(returns, benchmark)` — [[_meta/glossario#VaR (Value at Risk)|VaR]], [[_meta/glossario#CVaR (Conditional Value at Risk)|CVaR]], Calmar, Information Ratio, ecc.
- `rolling_statistics(returns, window)` — Sharpe/Sortino/Vol/Beta rolling
- `drawdown_details(returns)` — tabella dei [[_meta/glossario#Drawdown|drawdown]]
- `montecarlo_simulation(returns, n_sims=500, n_days=252)` — proiezione Monte Carlo
- `optimize_max_sharpe`, `optimize_min_volatility`, `optimize_hrp` — ottimizzazione pesi (PyPortfolioOpt)
- `efficient_frontier_curve(prices, n_points)` — frontiera efficiente
- `risk_contribution(positions, isin_map)` — contributo al rischio per posizione
- `correlation_matrix(prices)`
- `generate_html_report(...)` — **report HTML** (QuantStats tearsheet) generabile on-demand

### `data_fetcher.py` — Recupero dati di mercato (★ multi-sorgente, da studiare)
Gestione dati con **cache in memoria**. Rilevante per il confronto provider in [[system/data/data-providers]]:
- `get_ticker_info`, `get_historical_prices`, `get_current_prices` — via **yfinance**
- `get_benchmark_prices(benchmark_key, ...)` — serie del benchmark
- `get_fx_rate` / `get_fx_history` — conversione valutaria (fondo in EUR)
- `_classify_asset(info, ticker)` — classifica equity/ETF/bond/...
- **Fallback prezzi bond/ISIN europei** (non coperti bene da yfinance): `_fetch_tradingview_prices` (tradingview-screener), `_fetch_euronext_price`, `get_bond_price_from_borsa_italiana` (scraping). Pattern utile per asset europei dove yfinance è lacunoso.

### `fund_manager.py` — Motore centrale del fondo (★ single source of truth, 905 righe)
"Motore centrale del portafoglio, single source of truth". Gestisce transazioni→posizioni→NAV:
- `add_transaction`, `update_transaction`, `delete_transaction`
- `compute_positions_from_transactions()` — ricostruisce le posizioni dalle transazioni
- `compute_cash_from_transactions()`, `calculate_nav(positions, cash)`
- `update_position_prices`, `enrich_positions` (con overrides/metadati)
- `snapshot_nav`, `load_nav_history`, `update_fund_info`
- `get_portfolio_summary()` — riepilogo completo
- `recalculate_all()` — ricalcolo end-to-end; `migrate_positions_to_transactions()`
- `pause_sync`/`resume_sync` — sospende il sync GitHub durante batch

### `build_nav_history.py` — Storico NAV giornaliero (★ logica preziosa per backtest)
"Costruisce lo storico NAV giornaliero da transazioni + prezzi storici di mercato". Ricostruisce **giorno per giorno dall'inception**: posizioni e cash storici (`build_daily_positions_and_cash`), download prezzi storici (yfinance) e **FX rate storici**, bond senza ticker usano l'ultimo prezzo noto. `fill_missing_nav_days()` riempie i buchi. **Pattern direttamente trasferibile** al nostro backtesting: dato uno storico di operazioni, ricostruisci la curva di equity giornaliera per calcolare le metriche.

### `performance_contribution.py` — Performance attribution
Attribuzione della performance per posizione/gruppo su un periodo: `compute_period_contributions`, `summarize_contributions(group_col)`, `contribution_waterfall_items` (grafico waterfall), `period_bounds(nav_history, period)`, `benchmark_period_comparison`. Convenzione FX: importi in valuta locale divisi per `fx_rate` → EUR. **Spunto** per spiegare *da dove* viene il rendimento del fondo (utile per la valutazione dell'agente).

### `benchmark_contribution.py` + `benchmark_lookthrough.py` — Look-through del benchmark
Il benchmark (VNGA60, un fondo di ETF) viene **scomposto nei suoi ETF sottostanti** per confronto a parità di esposizione. `benchmark_lookthrough.py` fa scraping di StockAnalysis per le holding dell'ETF (con fallback su pesi noti), `compare_group_exposures` confronta fondo vs benchmark per gruppo. Tecnica avanzata di analisi relativa — *nice to have*, non MVP.

### `xray_utils.py` — Esposizione (X-Ray)
Normalizza il campo `sector` (che mescola settori reali, temi ETF, regioni, tipi di emittente bond, commodity) in bucket utili: `infer_xray_sector`, `add_xray_sector`, `build_exposure_table`, `build_country_exposure`. Utile per dashboard di esposizione settoriale/geografica.

### `github_sync.py` — Persistenza via GitHub API
`push_file`/`sync_data_file`/`sync_all_data` committano i CSV/JSON nel repo via GitHub Contents API (gestisce lo SHA per update). **Persistenza serverless** senza DB — interessante per un deploy semplice, ma per noi è probabilmente superato dal Postgres centrale. `get_sync_status()` per lo stato.

### `app.py` — Dashboard Streamlit
~4000 righe, multi-pagina (testata da `tests/test_app_navigation.py`). **Riferimento UI/UX** per la nostra eventuale dashboard di monitoraggio del fondo (NAV, posizioni, performance, esposizione, attribution). Mostra come orchestrare tutti i moduli sopra in un'interfaccia.

---

## ★ Tutti i valori calcolati dalla dashboard (pagina per pagina)

> Inventario completo di **ogni metrica/valore calcolato e mostrato** in `app.py` (11 pagine). Serve come **catalogo di KPI** da replicare nella nostra dashboard di monitoraggio del fondo. Formati: `€` = importo, `%` = percentuale.

### Quantità di base (calcolate al caricamento, valide su tutte le pagine)
Per ogni posizione: `avg_cost`, `current_price`, `quantity`, `invested_capital`, `current_value`, `pnl = current_value − invested_capital`, `pnl_pct = pnl / invested_capital`, `price_effect` (€), `fx_effect` (€), `realized_pnl`, `unrealized_pnl`, `dividends_received`, `weight`. Aggregati fondo: `total_value = Σ current_value`, `total_invested = Σ invested_capital`, `total_pnl = total_value − total_invested`, `total_pnl_pct`, `liquidita` (cash), **`nav_total = total_value + liquidita`**.

### 1. 🏠 Dashboard
- **Sidebar**: NAV, performance since inception `(nav_total − initial_nav)/initial_nav` (initial_nav default 10M), n° posizioni, cash, inception date, last update, stato sync GitHub.
- **4 KPI card**: NAV Corrente (+ % since inception); Total Return € `= unrealized + realized + dividends` (con breakdown Unrealizzato / Realizzato+Dividendi); **Alpha vs Benchmark** `= inception_perf − bench_perf` (bench_perf `= benchmark[-1]/benchmark[0] − 1`); Cash & Positions (`cash_pct = liquidita/nav_total`, n° posizioni attive).
- **Grafico NAV vs Benchmark** ribasato a 100, selettore periodo YTD/1M/3M/6M/1Y/Dall'Inizio → 3 metriche: SFC Fund %, Benchmark %, **Alpha** (differenza).
- **Performance Overview (tabella)**: per YTD, 1M, 3M, 6M, 1Y, Since Inception → Fondo %, Benchmark %, Alpha (= Fondo − Bench).
- **Asset Allocation (donut)**: peso % per macro_class `= current_value/nav_total` + Liquidità.
- **P&L Breakdown & Risk**: Non Realizzato €, Realizzato+Div €, Investito Totale €, Controvalore € · **Volatilità Annualizzata**, **[[_meta/glossario#Sharpe Ratio|Sharpe]] Ratio** (rf 2%), **Max Drawdown**, split Equity %/Fixed Income % (su NAV) — calcolati dalla serie NAV.
- **Top & Bottom Performers**: posizioni ordinate per `pnl_pct`.
- **Top 10 Holdings (tabella)**: nome, classe, valuta, costo, prezzo, investito, valore, P&L, P&L %, **peso `= current_value/nav_total`**.

### 2. 📋 Posizioni
- **5 KPI**: NAV Totale, n° Posizioni, P&L Totale €, P&L %, Liquidità €.
- **Per classe** (Equity / Fixed Income / Alternative): Valore classe `= Σ current_value`, **Peso su NAV** `= class_value/nav_total`, P&L Classe `= class_value − class_invested`, P&L % `= class_pnl/class_invested`.
- **Tabella posizioni**: isin, nome, settore, valuta, prezzo carico, prezzo attuale, investito €, controvalore €, P&L €, P&L %, **Effetto Prezzo €**, **Effetto Cambio €**, **peso sulla classe** `= current_value/class_value`.
- **Tabella completa**: **peso sul portafoglio** `= current_value/nav_total`.

### 3. 📈 Performance — `performance_report()` (frequenza auto-rilevata)
Calcola e mostra (tutte le metriche del report):
- **Total Return**, **Annualized Return**, **Annualized Volatility**, **Sharpe Ratio**, **[[_meta/glossario#Sortino Ratio|Sortino]] Ratio**, **Max Drawdown**, **Calmar Ratio**, **VaR (95%)**, **CVaR (95%)**, **Best/Worst Day|Week|Month** (in base alla frequenza), **Positive Days/Weeks/Months %**, **Observations** (n°), **Data Frequency**.
- Se c'è benchmark: **Alpha (ann.)**, **Beta**, **R²**, **Tracking Error**, **Information Ratio**, **Correlation**, **Benchmark Return**, **Benchmark Ann. Return**, **Benchmark Volatility**.
- Inoltre: curva cumulata ribasata, **serie drawdown** (`drawdown_series`), **heatmap rendimenti mensili** (`monthly_returns_table`), barre P&L per posizione (top 10 / bottom 5).

### 4. 📊 Analytics Avanzate — `advanced_risk_metrics()` (QuantStats)
Metriche raggruppate (tutte mostrate come st.metric):
- **Performance**: CAGR, Sharpe, Sortino, Calmar, **Omega**.
- **Rischio**: Volatilità Ann., Max Drawdown, VaR 95%, CVaR 95%, **Recovery Factor**, **Ulcer Index**.
- **Distribuzione**: **Skew**, **Kurtosis**, **Tail Ratio**.
- **Win/Loss**: **[[_meta/glossario#Win Rate|Win Rate]]**, Best Day, Worst Day, **Profit Factor**, **Payoff Ratio**, **[[_meta/glossario#Kelly Criterion|Kelly Criterion]]**.
- **vs Benchmark**: Information Ratio, **Treynor Ratio**, Alpha, Beta.
- **Rolling stats** (`rolling_statistics`, finestra 21/42/63/126/252 gg): **Rolling Sharpe**, **Rolling Sortino**, **Rolling Volatility**.
- **Drawdown analysis** (`drawdown_details`): serie drawdown + tabella Top 10 periodi di drawdown (inizio, fine, durata, profondità).
- **Report HTML** QuantStats scaricabile + performance di periodo (SFC %, Benchmark %, Scostamento).

### 5. 🏆 Contribuzione Performance — `performance_contribution.py`
- **Header KPI**: NAV Iniziale €, NAV Finale €, **Performance Periodo** (`fund_return_pp`, in punti percentuali), **Residuo Riconciliazione** (`residual_pp`).
- **Contributi al periodo** per posizione e per **Macro Classe** (in pp, `compute_period_contributions` + `summarize_contributions`); waterfall.
- **Confronto Benchmark**: Fondo %, Benchmark %, **Active Return** (pp), **Extra Performance** €.
- **Look-through VNGA60** (`benchmark_contribution.py`): Benchmark Reale %, **Ricostruito Sottostanti** %, Residuo, Active Return Fondo; **Top/Bottom Driver VNGA60**; contributo per gruppo (fondo vs benchmark); dettaglio sottostanti.

### 6. 🏛️ Analisi Fixed Income (calcoli bond proprietari)
- **5 KPI**: Valore FI €, Peso su NAV %, n° Posizioni, P&L €, P&L %.
- **Per obbligazione**: cedola %, scadenza, **anni a scadenza**, prezzo, **YTM approssimato** `= (cedola + (100 − prezzo)/anni) / ((100 + prezzo)/2)`, **Macaulay Duration** (formula chiusa), **Modified Duration** `= Macaulay/(1+y)`, **Reddito Annuo €** `= qty·100·cedola%`, controvalore, peso FI.
- **Metriche aggregate** (medie ponderate sul valore): **Duration Media (mod.)**, **YTM Medio**, **Cedola Media**, **Reddito Annuo Stimato €** (somma).
- **Sensitivity ai tassi**: ΔValore stimato per variazioni tasso da −1.00% a +1.00% (via duration).
- **Distribuzione per rating**; **Calendario cedole & scadenze**: Cedole Attese (12m) €, Scadenze (12m) €, n° Cedole da Registrare.

### 7. 🎯 Ottimizzazione PTF — `analytics_plus.py` (PyPortfolioOpt)
- **3 portafogli ottimali** — Max Sharpe / Min Volatility / HRP — ciascuno con: **Expected Return**, **Volatilità**, **Sharpe Ratio**, e dizionario **pesi**.
- **Confronto pesi** Attuale % vs Max Sharpe % vs Min Vol % vs HRP % (peso attuale `= current_value/eq_total`).
- **Frontiera Efficiente** (30 punti: coppie rischio/rendimento).
- **Contributo al Rischio per posizione** (`risk_contribution`): peso %, **% contributo al rischio**, **risk/weight ratio**.
- **Matrice di Correlazione** (`correlation_matrix`) + coppie a più alta correlazione.

### 8. 🔬 X-Ray Esposizioni
- **4 KPI**: Posizioni Totali, **Posizioni Effettive** `= 1/HHI`, **Top 5 Concentrazione** `= Σ top-5 pesi`, **HHI Index** `= Σ wᵢ²` (Herfindahl-Hirschman).
- **Tabelle esposizione** (`build_exposure_table`) per Settore, Geografia (Paese), Valuta, Macro Classe, Tipo Asset: per gruppo → peso %, valore €, n° strumenti. Choropleth geografica (totale / Equity / Fixed Income). Top 20 posizioni con peso.

### 9. 💹 Multipli & Fondamentali (live da yfinance)
- **Multipli medi ponderati equity** (peso `= current_value/total_eq_value`, filtro 0<x<500): **P/E Trailing**, **P/E Forward**, **Price/Book**, **EV/EBITDA**, **Dividend Yield**, **Beta**.
- **Dettaglio per posizione**: trailing_pe, forward_pe, price_to_book, ev_to_ebitda, **profit_margin**, **ROE**, dividend_yield, beta.
- **Contributo al P&L per settore**: P&L sommato per settore (`groupby sector`).

### 10. 📝 Operazioni & Import / 11. ⚙️ Gestione Info Strumenti
Pagine di **gestione (CRUD)**, protette da password: inserimento/modifica/eliminazione transazioni, aggiornamento prezzi, prezzi manuali bond, modifica `fund_info`, mapping ISIN→ticker. Non producono metriche calcolate (input dati).

### Sintesi: catalogo KPI riutilizzabile
Performance/rischio: **Total/Annualized Return, Volatility, Sharpe, Sortino, Calmar, Omega, Max Drawdown, Recovery Factor, Ulcer Index, VaR/CVaR 95%, Skew, Kurtosis, Tail Ratio, Win Rate, Profit Factor, Payoff Ratio, Kelly, CAGR**. Relativi a benchmark: **Alpha, Beta, R², Tracking Error, Information Ratio, Treynor Ratio, Correlation, Active Return**. Portafoglio: **HHI, posizioni effettive, top-5 concentrazione, pesi, contributo al rischio, contributo alla performance, frontiera efficiente, correlazioni**. Fixed income: **YTM, Macaulay/Modified Duration, cedola media, reddito annuo, sensitivity ai tassi**. Fondamentali: **P/E trail/fwd, P/B, EV/EBITDA, dividend yield, ROE, profit margin, beta**. → Tutti calcolabili con `analytics.py` + `analytics_plus.py` (vedi sopra), riusabili nel nostro Quant/Backtesting.

---

## Takeaway per il progetto

1. **`analytics.py` è quasi copia-incollabile** nel Quant/Backtesting: tutte le metriche standard (Sharpe, Sortino, Calmar, max DD, VaR, CVaR, alpha/beta) in pandas puro.
2. **`build_nav_history.py`** = template per ricostruire la curva di equity giornaliera da uno storico di operazioni → base del backtesting e della valutazione.
3. **Modello transaction-based** (posizioni derivate dalle transazioni) = pattern robusto per il DB centrale e l'audit.
4. **`data_fetcher.py`** documenta il fallback multi-provider per **asset europei** (Euronext, Borsa Italiana) dove yfinance è lacunoso — rilevante avendo scelto equity (vedi [[system/data/data-providers]]).
5. **QuantStats + PyPortfolioOpt** (`analytics_plus.py`) = alternativa leggera/complementare a [[prior-art/libraries/cvx-portfolio-optimizer]] per metriche e ottimizzazione, più i **report HTML** pronti.
6. **Performance attribution** e **NAV/dashboard** sono il lato "reporting" che a Rizzo e all'optimizer manca: completa il quadro per la valutazione del fondo.
7. **Limite**: niente esecuzione/automazione e niente DB (persistenza su file+GitHub). È un tracker/dashboard, non un agente — utile per analytics e UI, non per il ciclo di trading.
