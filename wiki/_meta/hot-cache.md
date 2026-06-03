# Hot Cache — Trading Agent

> Contesto di sessione recente. Aggiornare a fine sessione. Tenere entro 300 righe.

## Sessione Corrente
- **Data**: 2026-06-03
- **Agent**: Claude Code (Opus)
- **Operazione principale**: **Review pre-sviluppo + risposta alle lacune**. Luca ha risposto a un'analisi delle cose ancora da decidere/capire. Create **5 nuove pagine** (`system/state-schemas`, `system/position-sizing`, `system/rating-scoring`, `system/parallelism-design`, `strategy/questions-for-salvatore`); aggiornati decision-log, data-layer, execution, agents, quant-backtesting, stack, glossario, ideas-log, index. **Board ridisegnata come centrale operativa** (owner + riferimento pagina su ogni card). Nuova sezione in **CLAUDE.md** che formalizza la board come hub + convenzione owner/riferimenti.
- **Prossimi due passi concordati**: 1) strutturare lo schema dello state ([[system/state-schemas]]); 2) definire la formula di position sizing ([[system/position-sizing]]).
- **Luca ha rivisto e commentato l'intera analisi delle lacune** (tutti i punti B + C). Input aggiuntivi 2026-06-03: **subgraph come pattern granulare** per collegare parti diverse del sistema ([[system/parallelism-design]]); **disinvestimento a 2 livelli** (automatico via TP/trailing stop + valutato rating-based) ([[system/rating-scoring]], [[system/modules/execution]]).

### Sessione precedente (2026-05-29)
- **Refactor strutturale completo del wiki**: `build/`→`system/`, `references/` eliminata, moduli ricreati su `architettura.canvas` (`data-layer`/`agents`/`execution`/`quant-backtesting`). Decisioni: dissolvi le call (date inline); naming inglese; PM = agente LLM orchestratore.

## Stato attuale del progetto
- Fase: **Design → sviluppo in preparazione**
- **Architettura**: monolite modulare, principio deterministico (Statuto rigido Python upstream)
- **Prototipo**: paper trading autonomo su exchange equity (da scegliere) + backtesting continuativo
- **Orizzonte trade**: swing trading (4h/daily / checkpoint AI flessibili)
- **Scope**: **Stock-only** (equity pura) — poi multi-asset: commodities, BTC only, derivati futures/opzioni
- **Framework**: LangChain + LangGraph (fork da TradingAgents TauricResearch)
- **Debug/Evaluation**: LangSmith + LangSmith CLI
- **LLM**: OpenRouter + DeepSeek V4 Pro, output JSON obbligatorio
- **Backtesting**: VectorBT (decisione chiusa)

## Struttura wiki (post-refactor 2026-05-29)
```
wiki/
├── _meta/          ← navigazione (index, log, hot-cache, taxonomy, glossario, onboarding)
├── overview.md     ← entry point
├── system/         ← spec software (dominio Luca)
│   ├── architecture.md · mvp.md · stack.md · data-providers.md
│   ├── decision-log.md · ideas-log.md
│   └── modules/    ← data-layer · agents · execution · quant-backtesting
├── strategy/       ← conoscenza di mercato (dominio Salvatore)
│   ├── index.md
│   ├── methods/    ← trend-following · factor-investing · mean-reversion-stat-arb · dual-portfolio
│   ├── indicators/ ← da popolare
│   └── metrics/    ← benchmark
├── prior-art/      ← esterni studiati/forkati
│   ├── tradingagents/ ← paper · code-wiki · graph-schema
│   ├── libraries/  ← cvx-portfolio-optimizer · rizzo-trading-agent · sfc-portfolio-tracker
│   └── papers/     ← alpha-arena · brenndoerfer-quant-trading · notion-trading-concepts
├── syntheses/      ← analisi trasversali
└── artifacts/      ← architettura.canvas (corrente) + architecture/ (canvas) + project-board
```

## Moduli (allineati ad `architettura.canvas`)
- **data-layer** — DB centrale (4 aree: rendicontazione, dati live, costituzione, log) + Extraction (extractors set, adaptive extractor, market alert, calendar tool, **mantainer**)
- **agents** — PM orchestratore + Analyst Research (Market+Sentiment) + Analyst Technical (Technical+Fondamentali) + Risk Analyst (bear + Statuto + guardrail + token cost + leva opzioni)
- **execution** — Investment State (gate completezza) → Trade (Python deterministico) → Exchange (paper) → transactions
- **quant-backtesting** — strategia quant + VectorBT (offline, non nel canvas)

## Decisioni chiuse importanti (recenti)
- **Broker intercambiabili via adapter** — Alpaca MVP → IBKR prod (2026-06-02)
- **Storage principalmente time-series + oggetti** (2026-06-02)
- **Extractor DB-first con queue + check presenza** (2026-06-02)
- **Transaction cost auto-adattivo** (no hardcoded) (2026-06-02)
- **Conviction level assegnato dal PM** (2026-06-02)
- **`mantainer` = technical → rendicontazione** (confermato 2026-06-02)
- **Deploy su mini-server di casa 24/7 + .env locale** (2026-06-02)
- **Approccio incrementale (alpha-first)** (2026-06-02)
- **Portfolio / mid-term confermato, NO day trading** (2026-05-29)
- **OpenRouter + DeepSeek V4 Pro** come provider/modello principale (2026-05-29)
- **Trader = funzione Python deterministica (NON agent)** (2026-05-29)
- **PM = agente LLM orchestratore** (umano solo override iniziale) (2026-05-29)
- **2 desk analisti**: Analyst Research + Analyst Technical (chiude "2 vs 4") (2026-05-29, da canvas)
- **Head of Analyst eliminato; Risk Analyst = gate bear unico** (2026-05-29)
- **Guardrail deterministici da Statuto-schema** (2026-05-29)
- **Avvio con portafoglio già investito** + universo investibile come lista (2026-05-29)
- **Benchmark: S&P 500 + 60/40 all-world** (2026-05-29)
- **Investment State come gate di completezza pre-trade** (2026-05-29)
- **Riscrivere il grafo tenendo base TradingAgents** (2026-05-29)
- **Statuto & 10% cash · Leva via Opzioni · Token cost = commissioni · Business Model Piero** (2026-05-27)

## Decisioni ancora aperte (priorità)
> Lista completa e navigabile in [[artifacts/project-board]] (sezione 🟠) e [[system/decision-log]].
- **Schema state** + **formula position sizing** (i due prossimi passi)
- **`entry_price` limit order** · **parallelismo multi-ticker** · **criteri info-sufficienti**
- **VaR / overfitting / test benchmark / rating asset / opzioni** → [[strategy/questions-for-salvatore]]
- **Indicatori di sentiment**: da inventare — con Salvatore
- **Desk di monitoring/evaluation**: design dell'agente che sorveglia le posizioni
- **Strategia del fondo**: da formalizzare con Salvatore (multi-factor)
- **Frequenza ciclo**: 4h vs 24h (dipende da backtest)
- **Regole specifiche dello Statuto** + **algoritmo di disinvestimento ottimale** (in corso)
- **Dynamic Temporal Checkpoints**: feedback loop temporale gestito dall'AI

## Pending ingest
- **File market driver di Salvatore** (4 macro-categorie) — atteso in `raw/` come TXT → `strategy/indicators/`
- **Documento indicatori di valuation** (Salvatore) — atteso, poi TXT + ingest
- `raw/articles/AlphaArena/` + `optimizer/` + `TradingAgents*` — in raw per consultazione (pagine prior-art già esistenti)
- `raw/daily-notes/model.md` = template vuoto (resta)

## Da fare prossima sessione
- Iniziare a **strutturare lo schema dello state** con Luca → [[system/state-schemas]]
- Poi **formula di position sizing** → [[system/position-sizing]]
- Verificare in Obsidian che la graph view non abbia orfani inattesi
- Creare pagine metriche (`sharpe-ratio`, `max-drawdown`, `win-rate`) in `strategy/metrics/` solo quando servono
