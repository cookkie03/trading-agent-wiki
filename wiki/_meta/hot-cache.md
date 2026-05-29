# Hot Cache — Trading Agent

> Contesto di sessione recente. Aggiornare a fine sessione. Tenere entro 300 righe.

## Sessione Corrente
- **Data**: 2026-05-29
- **Agent**: Claude Code (Opus)
- **Operazione principale**: **Refactor strutturale completo del wiki**. (1) `build/` → `system/`; (2) `references/` **eliminata**: prior-art esterno → `prior-art/{tradingagents,libraries,papers}/`, le 8 call + handwritten-notes **dissolte** (sostanza già nelle pagine tematiche, grezzi in `raw/archived/`, provenienza ora inline come date), note-audio-salvatore → nuova `strategy/methods/dual-portfolio`, tool-set → `system/data-providers`, onboarding → `_meta/`, trading-floor-canvas → `artifacts/`. (3) **Moduli ricreati sul canvas `architettura.canvas`**: i 4 file legacy (exchange-db/llm-agent-system/risk-management + quant) sostituiti da **`data-layer` · `agents` · `execution` · `quant-backtesting`**. (4) Riscritti tutti i wikilink path-qualified + bare; aggiornati taxonomy, index, overview; `log.md` lasciato come storico.
- **Decisioni di struttura prese con Luca**: dissolvi-del-tutto le call (date inline, no journal); naming inglese; PM = **agente LLM orchestratore** (umano solo override iniziale); decomposizione moduli **per aree del canvas** (4 file).

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
- **Forma di storage per area** (SQL/JSON/time-series) + exchange paper trading equity
- **Ruolo esatto del nodo `mantainer`** nel grafo (nuovo dal canvas)
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
- Verificare in Obsidian che la graph view non abbia orfani inattesi dopo il refactor
- Confermare con Luca il ruolo del nodo **`mantainer`** e completare i moduli se serve
- Decidere **forma di storage per area** + exchange paper trading equity
- Creare pagine metriche (`sharpe-ratio`, `max-drawdown`, `win-rate`) in `strategy/metrics/` solo quando servono
