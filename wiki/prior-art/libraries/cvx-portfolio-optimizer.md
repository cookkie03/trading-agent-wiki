---
title: "Portfolio Optimizer (cvx-portfolio-optimizer)"
type: source
tags:
  - quant
  - software
  - optimization
raw_source_path: "raw/articles/optimizer/ + https://github.com/SilvioBaratto/optimizer"
created: 2026-05-12
updated: 2026-05-29
status: active
confidence: high
related:
  - "[[system/modules/agents]]"
  - "[[system/modules/agents]]"
  - "[[system/architecture]]"
  - "[[prior-art/libraries/rizzo-trading-agent]]"
  - "[[prior-art/libraries/sfc-portfolio-tracker]]"
---

# Portfolio Optimizer ([cvx-portfolio-optimizer](https://github.com/cvxgrp/cvxportfolio) )

Libreria Python per la costruzione e l'ottimizzazione di portafogli quantitativi, basata su `skfolio` e `scikit-learn`.

Resta un riferimento da **studiare e sfruttare**, non solo da archiviare come prior-art.

## Architettura e Design

- **Frozen-config + Factory Pattern**: le configurazioni sono dataclass immutabili e serializzabili; le factory creano gli stimatori. Permette di loggare e storicizzare ogni configurazione di trade/ottimizzazione in modo pulito.
- **Pipeline scikit-learn**: ogni componente (preprocessing, selezione, ottimizzazione) è un trasformatore sklearn. L'intera catena è validabile e tunabile come un singolo oggetto.
- **Data Flow**: `prices → returns → [preprocess → pre-select → optimize] → backtest → weights`

## Caratteristiche principali

- **Pipeline-driven**: orchestrazione end-to-end da prezzi a pesi validati
- **Preprocessing**: validazione dati, outlier treatment, imputation
- **Pre-selection**: filtri per varianza, correlazione, dominanza, scadenza
- **Moments**: 5 stimatori di rendimento atteso e 11 di covarianza; supporta HMM per regimi di mercato
- **Views — [[_meta/glossario#Black-Litterman|Black-Litterman]] & [[_meta/glossario#Entropy Pooling|Entropy Pooling]]**: integra le views (previsioni LLM) nell'ottimizzazione matematica
- **Optimization**: oltre 10 modelli (Mean-Risk, Risk Budgeting, HRP, HERC, NCO, robust ellipsoidal)
- **Validation**: [[_meta/glossario#Walk-Forward Backtesting|Walk-Forward]], Combinatorial Purged CV ([[_meta/glossario#CPCV (Combinatorial Purged Cross-Validation)|CPCV]])
- **Regime detection (HMM)**: adatta il modello di rischio al regime di mercato
- **Scoring**: 19 metriche di performance ([[_meta/glossario#Sharpe Ratio|Sharpe]], [[_meta/glossario#Sortino Ratio|Sortino]], Calmar, ecc.)
- **Factors**: 17 fattori in 9 gruppi per la selezione degli asset

## Ruolo nel progetto

Motore di calcolo candidato per il **Portfolio Allocator** (post-MVP). Implementa deterministicamente:
- Traduzione delle views LLM in pesi portfolio (via Black-Litterman / Entropy Pooling)
- Ribilanciamento con [[_meta/glossario#Rebalancing Gate|Rebalancing Gate]]
- Hard limits (statuto del fondo)
- Il design "Config + Factory" è compatibile con il layer DB: la configurazione del portafoglio può essere salvata nel DB e riletta deterministicamente
- Le "Views" sono il punto di contatto ideale tra LLM e Quant: l'LLM produce un'opinione e la libreria la integra matematicamente

---

## ★ Il repo non è solo una libreria: è una piattaforma full-stack (ingest 2026-05-29 dal codice)

L'analisi del **repository GitHub** (https://github.com/SilvioBaratto/optimizer, pacchetto PyPI `portopt`, BSD-3) rivela che la pagina precedente — basata solo sui docs — copriva **solo la libreria**. Il repo è in realtà una **piattaforma completa** con backend API, frontend, CLI, scheduler, DB e **integrazione LLM strutturata**. È il riferimento architetturale più maturo e completo che abbiamo, molto vicino al sistema che vogliamo costruire.

### Stack del progetto
- **Libreria** `optimizer/` (Python, sklearn API): moduli `preprocessing`, `pre_selection`, `moments`, `views`, `optimization`, `validation`, `scoring`, `factors`, `rebalancing`, `synthetic`, `universe`, `tuning`, `fx`, `pipeline`, `exceptions`. Dipende da `skfolio`, `scikit-learn`, `numpy`, `pandas`, `scipy`, `hmmlearn`, `arch` (+ opzionale `torch`/`pyro-ppl` per DMM).
- **Backend** `api/` — **FastAPI** con architettura a layer pulita: `models` (SQLAlchemy) · `repositories` · `services` · `schemas` · `api/v1` (router) · `middleware` (auth, logging, **rate_limiting**, security, metrics) · **Alembic** per le migrazioni · `baml_client`/`baml_src` (LLM). Postgres come DB.
- **Frontend** `frontend/` — **Angular** (nginx, Dockerfile) — dashboard live (`optimizer.silviobaratto.com`).
- **CLI** `cli/` — entrypoint `optimizer` (auth, client, portfolio, universe, macro, yfinance, db, data_assembly, direct_fetch, display).
- **Scheduler** `scheduler/` — script shell (`fetch.sh`, `refetch_all.sh`, `smoke.sh`) per fetch dati programmato.
- **Deploy**: `docker-compose.yml` orchestra Postgres 16 + Adminer + FastAPI + (Ollama su host per LLM locale). Healthcheck su tutti i servizi.

### ★ Integrazione LLM via BAML — il pattern "LLM genera views → ottimizzazione matematica"
La cartella `api/baml_src/` definisce **funzioni LLM tipizzate** con [BAML](https://boundaryml.com) (output strutturato garantito, client configurabile — incl. **Ollama locale**). È **esattamente il ponte LLM↔Quant** che cerchiamo, implementato in modo production-grade:

| Funzione BAML                            | Scopo                                                                                                                          |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **`GenerateViews`**                      | da dati multi-fattore per asset → **views Black-Litterman** (direction ±1, magnitude bps, confidence→Idzorek alpha, reasoning) |
| `ExpertView`                             | view di un "esperto" su singolo asset                                                                                          |
| `ScoreNewsSentiment`                     | scoring del sentiment da news                                                                                                  |
| `SummarizeCountryNews`                   | sintesi news per paese                                                                                                         |
| `ClassifyMacroRegime`                    | classifica il regime macro                                                                                                     |
| `SelectCovRegime`                        | seleziona il regime di covarianza (HMM)                                                                                        |
| `CalibrateDelta` / `CalibrateRiskBudget` | calibrazione parametri di ottimizzazione                                                                                       |
| `AdaptFactorWeights`                     | adatta i pesi dei fattori                                                                                                      |
| `DesignStressScenarios`                  | genera scenari di stress                                                                                                       |

Queste funzioni sono candidate sia per **replica interna** sia per eventuale riuso diretto, se il package si dimostra abbastanza maturo.

Pattern chiave (in `GenerateViews.baml`): l'LLM riceve **fattori quantitativi per asset** (P/E, P/B, momentum 12-1m, RSI, ROE, debt/equity, growth, distanza da 52w high/low, consenso analisti) e produce views con **confidence calibrata mappata su Idzorek alpha** → fed deterministicamente nel modello Black-Litterman. **Da studiare e adattare**: è il modo "giusto" di far produrre all'LLM opinioni che la matematica integra, anziché lasciare all'LLM la decisione finale di trade (allineato al nostro principio deterministico, [[system/modules/agents]]).

### Servizi backend riutilizzabili come riferimento (`api/app/services/`)
`view_generation`, `entropy_pooling_service`, `opinion_pooling`, `optimization_service`, `backtest_service`, `rebalancing_service`, `risk_analytics_service`, `risk_budget_service`, `factor_*_service`, `macro_regime_service`, `macro_news_summary`, `sentiment`, `stress_scenarios`, `synthetic_service`, `tuning_service`, `universe_screening_service`, `validation_service`, `reference_index_seeder`, `report_service`, `scheduler`, **`broker_sync_service`** + **`trading212/`** (sincronizzazione broker), `yfinance_data_service`, `notifications`. I router `api/v1/` espongono ognuno di questi (`optimize`, `views`, `opinion_pooling`, `risk`, `factors`, `rebalance`, `backtest`, `tune`, `synthetic`, `stress_scenarios`, `macro_regime`, `attribution`, `dashboard`, `jobs`, `trading212`, ...).

### Cosa estrarre / a cui ispirarsi per il nostro progetto
1. **Architettura backend FastAPI a layer** (models→repositories→services→routers + middleware + Alembic) = blueprint diretto per il nostro backend e il DB centrale ([[system/modules/data-layer]]).
2. **BAML per le funzioni LLM** (output strutturato + Ollama/cloud intercambiabili) = alternativa o complemento al nostro "JSON obbligatorio su [[_meta/glossario#DeepSeek|DeepSeek]]"; `GenerateViews` è il template del ponte LLM→Black-Litterman ([[system/modules/agents]]).
3. **`broker_sync_service` + `trading212`** = riferimento per il modulo Exchange (anche se equity europeo).
4. **Background jobs + scheduler + Alembic + docker-compose** = infrastruttura operativa già risolta.
5. La **libreria `optimizer/`** resta il motore quant candidato (vedi sopra) — ora sappiamo che esiste anche tutto il "contorno" applicativo a cui guardare.
6. **Confronto con gli altri due riferimenti**: [[prior-art/libraries/rizzo-trading-agent]] dà il ciclo agente LLM→esecuzione end-to-end (semplice, crypto); questo optimizer dà il motore quant + LLM-views production-grade; [[prior-art/libraries/sfc-portfolio-tracker]] dà analytics/dashboard/reporting. Insieme coprono tutto lo spettro del nostro sistema.

---
## Commenti recuperati da iCloud (2026-07-01)

> Commenti Obsidian `%%...%%` presenti nella vecchia copia iCloud (`7054827`) e reinseriti senza sovrascrivere il contenuto corrente.

%% per esempio, devo ricordarmi e segnarmi come task di studiare questa libreria o perlomeno di imparare ad utilizzarla e sfruttarla per questo progetto%%

%% TASK: documentazione](https://silviobaratto.github.io/optimizer/) su cui fare crawl e inserire dentro raw/articles%%

%%molto interessante%%

%% molto interessante %%

%% queste funzioni possono essere molto utili, si potrebbero o replicare per avere tanta maneggevoleza e grado di personalizzazione oppure utilizzarle nel codice perosnale come pacchetto incluso se già professional-grade%%

%%aggiungi Idzorek alpha al [[glossario]]%%

%% anche quest'ultimo concetto è molto importante e rappresentativo, quindi vale la pena valorizzarlo come concetto chiave%%

