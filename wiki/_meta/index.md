# Wiki Index — Trading Agent

> Catalogo operativo del vault. Aggiornato dall'agent quando la wiki cresce.

## Overview
- [[overview]] — ingresso principale del progetto

## System — Spec del software
*Tutto ciò che riguarda cosa costruiamo: architettura, moduli, tech stack, decisioni. Dominio Luca.*

- [[system/architecture]] — architettura completa del sistema (topologia, layer, flussi) — allineata ad `architettura.canvas`
- [[system/mvp]] — design del prototipo MVP
- [[system/stack]] — tech stack scelto e motivazioni
- [[system/data-providers]] — broker con API Python in Italia + provider dati (stack raccomandato)
- [[system/decision-log]] — storico decisioni chiuse + decisioni ancora aperte
- [[system/ideas-log]] — log append-only delle idee di progetto (mai cancellare)
- [[system/state-schemas]] — schema di `research_state`/`investment_state` (contratto dati tra agenti) 🛠
- [[system/investment-state-template]] — template-menu completo dell'`investment_state` da definire con Salvatore (potare/modificare) 🔀
- [[system/position-sizing]] — dimensionamento posizioni (relativo, conviction, Kelly) 🛠
- [[system/rating-scoring]] — sistema di rating/scoring (conviction · agenti · asset) 🛠
- [[system/parallelism-design]] — orchestrazione multi-ticker e criteri "info sufficienti" 🛠
- [[system/learning-feedback-loop]] — loop di valutazione/auto-miglioramento (reportistica "cosa va male" · scoring agenti · ponderazione pesi · feedback post-trade) 🛠
- [[system/db-access-performance]] — accesso al DB: quando/da chi è interrogato, tecniche di performance, minimizzazione query, forma fisica (Timescale/JSONB) 🛠
- [[system/tools-inventory]] — inventario dei tool che gli agenti possono chiamare (9 famiglie · live/storico · write-through · vendor) 🛠
- [[system/agent-behaviors]] — comportamento per-agente del desk (Market · Sentiment · Technical · Fondamentali: input · tool · output · ragionamento · stop) 🛠
- [[system/system-prompts]] — metodo di prompt engineering + scheletro a 7 blocchi + tutti e 6 i system prompt (4 desk + PM + Risk, in inglese) 🛠

### Moduli — aree del sistema (da `architettura.canvas`)
- [[system/modules/data-layer]] — DB centrale (4 aree logiche) + Extraction (extractors, adaptive, market alert, calendar tool, mantainer)
- [[system/modules/agents]] — Portfolio Manager orchestratore + Analyst Research + Analyst Technical + Risk Analyst (bear + Statuto)
- [[system/modules/execution]] — Investment State → Trade deterministico → Exchange → transactions
- [[system/modules/quant-backtesting]] — strategia quantitativa, indicatori, backtest VectorBT

## Strategy — Conoscenza di mercato
*Approcci, indicatori, metriche: il dominio di Salvatore. Ogni elemento alimenta [[system/modules/quant-backtesting]].*

- [[strategy/index]] — panoramica e principio di linking
- [[strategy/methods/trend-following]] — seguire il trend degli istituzionali
- [[strategy/methods/factor-investing]] — fattori fondamentali e quantitativi (post-MVP)
- [[strategy/methods/mean-reversion-stat-arb]] — mean reversion e statistical arbitrage / pairs trading
- [[strategy/methods/dual-portfolio]] — idea dual portfolio value + quant (embrionale, Salvatore)
- [[strategy/metrics/benchmark]] — benchmark della gestione attiva (S&P + 60/40 all-world)
- [[strategy/questions-for-salvatore]] — foglio domande aperte per Salvatore (VaR, overfitting, opzioni, fattori) 📈

**Indicatori:**
- [[strategy/indicators/macro-indicators]] — framework indicatori macroeconomici (PIL, inflazione, lavoro, politica monetaria, liquidità, obbligazioni, credito, valute, volatilità, flussi, driver azionari) — 12 categorie, draft Salvatore in corso 📈

*(metrics/ si popola man mano)*

## Prior-art — Sistemi, paper e librerie esterni
*Materiale esterno studiato o forkato. Riferimento durante lo sviluppo.*

### TradingAgents (la base che forkiamo)
- [[prior-art/tradingagents/paper]] — TradingAgents paper + pattern adottati
- [[prior-art/tradingagents/code-wiki]] — Code Wiki del codebase (agenti, orchestrazione, data layer, LLM integration)
- [[prior-art/tradingagents/graph-schema]] — schema del grafo TradingAgents (nodi/edge/state)

### Librerie / progetti riusabili
- [[prior-art/libraries/cvx-portfolio-optimizer]] — cvx-portfolio-optimizer / `portopt` (libreria quant + piattaforma full-stack: FastAPI, Angular, CLI, scheduler, LLM-views via BAML, broker sync)
- [[prior-art/libraries/rizzo-trading-agent]] — Rizzo AI Academy: agente LLM di trading funzionante (GPT JSON strict, multi-sorgente, Postgres) — codice riusabile MIT
- [[prior-art/libraries/sfc-portfolio-tracker]] — SFC: tracker/dashboard fondo in Streamlit (analytics, NAV history, performance/benchmark attribution, PyPortfolioOpt)

### Paper e articoli
- [[prior-art/papers/alpha-arena]] — benchmark LLM su trading
- [[prior-art/papers/brenndoerfer-quant-trading]] — articolo quant trading: alpha, backtesting, metriche (con codice Python)
- [[prior-art/papers/notion-trading-concepts]] — export Notion su trading e investimenti (concetti fondamentali)

## Syntheses — Analisi trasversali
- [[syntheses/notebooklm-research-2026-05-13]] — ricerca su TradingAgents, MarketSenseAI, Alpha Arena, Simone Rizzo

## Artifacts — Canvas e board

**Canvas di design**
- [[architettura.canvas]] — **design corrente del sistema** (topologia 2026-05-29: DB-hub + extraction · PM orchestratore · Analyst Research/Technical · Risk Analyst · Investment State · Trade)
- [[Architettura langchain.canvas]] — schema concettuale LangGraph (agente = system prompt + LLM + tool) — in `artifacts/architecture/`
- [[trading-floor.canvas]] — schema trading floor (versione precedente) — in `artifacts/architecture/`
- [[tradingagents-graph-finance.canvas]] — vista business del sistema TradingAgents

**Doc di supporto canvas**
- [[artifacts/trading-floor]] — descrizione testuale dello schema trading floor

**Board operative**
- [[artifacts/project-board]] — board unica di progetto (tecnico/Luca + mercato/Salvatore + stato progetto)

## Meta
- [[_meta/glossario]] — glossario termini del progetto
- [[_meta/taxonomy]] — tassonomia tag e path cartelle
- [[_meta/onboarding]] — metodo di lavoro e uso di Obsidian
- [[_meta/log]] — log append-only di tutte le operazioni sul vault
- [[_meta/hot-cache]] — contesto sessione corrente
