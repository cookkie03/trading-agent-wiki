# Wiki Index — Trading Agent

> Catalogo operativo del vault. La struttura `system/` è stata riordinata il 2026-07-13; il repository vive fuori dal vault e il suo stato non viene dedotto da queste pagine.

## Overview

- [[overview]] — ingresso principale del progetto

## System — Spec software (dominio Luca)

### Foundation

- [[system/foundation/architecture]] — mappa di design del sistema
- [[system/foundation/mvp]] — scope MVP USD-only
- [[system/foundation/stack]] — stack e framework scelti
- [[system/foundation/implementation-status]] — convenzione tra spec wiki e repository esterno
- [[system/foundation/decision-log]] — decisioni chiuse e aperte
- [[system/foundation/ideas-log]] — idee storiche di progetto
- [[system/foundation/wiki-reorganization]] — riordino editoriale completato

### Data e tools

- [[system/data/data-layer]] — DB, retention e data layer
- [[system/data/data-providers]] — panoramica storica di broker/provider
- [[system/data/data-vendors]] — policy OpenBB-first e copertura multi-vendor
- [[system/data/data-sources-tool-map]] — provider → wrapper → capability
- [[system/data/db-access-performance]] — accesso DB e ottimizzazioni
- [[system/tools/tools-inventory]] — capacità/tool disponibili agli agenti

### Agenti, orchestrazione e investimento

- [[system/agents/agents]] — ruoli e topologia agentica
- [[system/agents/agent-behaviors]] — input, tool, output, ragionamento e stop per ruolo
- [[system/agents/system-prompts]] — prompt engineering e prompt v0
- [[system/agents/agent-memory]] — memoria intra/inter-task e ricerca RAG+grafi
- [[system/orchestration/parallelism-design]] — funnel e isolamento per ticker
- [[system/orchestration/trigger-engine]] — alert, checkpoint e health check
- [[system/orchestration/universe-watchlist]] — universo, watchlist e benchmark Post-MVP
- [[system/investment/state-schemas]] — schema annidato `research_state` / `investment_state`
- [[system/investment/investment-state-template]] — template da validare con Salvatore
- [[system/investment/position-sizing]] — position sizing
- [[system/investment/rating-scoring]] — rating/scoring e drift Post-MVP
- [[system/investment/cost-accounting]] — accounting audit e scope Post-MVP
- [[system/execution/execution]] — execution deterministica e recovery
- [[system/quant/quant-backtesting]] — backtesting e indicatori
- [[system/quant/learning-feedback-loop]] — logging e learning Post-MVP
- [[system/interface/frontend-module]] — confine del frontend sostituibile
- [[system/interface/observability-dashboard]] — requisito dashboard read-only

### Reference design

- [[system/_reference/canvas-code-mapping]] — mapping storico canvas/repository
- [[system/_reference/fork-gap-analysis]] — analisi storica del fork

## Strategy — Conoscenza di mercato (dominio Salvatore)

- [[strategy/index]] — metodi, scelta strategia MVP e metriche
- [[strategy/methods/trend-following]] — trend following
- [[strategy/methods/factor-investing]] — factor investing e tesi corporate bond
- [[strategy/methods/mean-reversion-stat-arb]] — mean reversion/stat arb
- [[strategy/methods/dual-portfolio]] — dual portfolio
- [[strategy/metrics/benchmark]] — benchmark (Post-MVP)
- [[strategy/indicators/macro-indicators]] — indicatori macro
- [[strategy/questions-for-salvatore]] — decisioni e domande di mercato

## Prior-art

- [[prior-art/tradingagents/paper]] · [[prior-art/tradingagents/code-wiki]] · [[prior-art/tradingagents/graph-schema]] — TradingAgents come reference
- [[prior-art/libraries/datapizza-ai]] — reference storica, non framework corrente
- [[prior-art/libraries/cvx-portfolio-optimizer]] — ottimizzazione quant/Post-MVP
- [[prior-art/libraries/rizzo-trading-agent]] · [[prior-art/libraries/sfc-portfolio-tracker]] — reference mirate
- [[prior-art/papers/alpha-arena]] · [[prior-art/papers/brenndoerfer-quant-trading]] · [[prior-art/papers/kronos-foundation-model]] · [[prior-art/papers/notion-trading-concepts]]

## Artifacts

- [[artifacts/project-board]] — board unica di progetto
- [[artifacts/tool-catalog.base]] — vista delle spec tool/vendor
- [[architettura.canvas]] — canvas di design
- [[artifacts/trading-floor]] — canvas trading floor storico

## Meta

- [[_meta/glossario]] — glossario
- [[_meta/taxonomy]] — ruoli, path e tag canonici
- [[_meta/comment-resolution-2026-07-13]] — ledger della rilettura/commenti
- [[_meta/log]] — log append-only
- [[_meta/hot-cache]] — contesto operativo corrente
