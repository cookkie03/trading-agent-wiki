# Wiki Index — Trading Agent

> Catalogo operativo del vault. Aggiornato dall'agent quando la wiki cresce.

## Overview
- [[overview]] — ingresso principale del progetto

## Build — Spec del progetto
*Tutto ciò che riguarda cosa costruiamo: architettura, moduli, tech stack, decisioni.*

- [[build/system-map]] — architettura completa del sistema (ciclo operativo, layer, flussi)
- [[build/mvp-prototype-design]] — design del prototipo MVP
- [[build/stack]] — tech stack scelto e motivazioni
- [[build/decision-log]] — storico decisioni chiuse + decisioni ancora aperte
- [[build/modules/module-a-exchange-db]] — Modulo A: Exchange + DB (Track 1, Luca)
- [[build/modules/module-c-quant-backtest]] — Modulo C: Quant Agent + Backtesting (Track 2, Luca+Salvatore)
- [[build/modules/module-d-prompt-builder-trader]] — Modulo D: Prompt Builder + LLM Trader (Track 3)
- [[build/modules/risk-analyst]] — Risk Analyst Agent (post-MVP)
- [[build/ideas-log]] — log append-only delle idee di progetto (mai cancellare)

## References — Fonti ingestite
*Materiale grezzo ingestito: call, paper, librerie, articoli.*

- [[references/conversazione-luca-salvatore-2026-04-28-30]] — bundle iniziale conversazioni progettuali
- [[references/videochiamata-luca-salvatore-2026-04-30]] — architettura multi-agente e dashboard
- [[references/videochiamata-luca-salvatore-2026-05-06]] — allineamento architettura cron/prompt-builder
- [[references/videochiamata-luca-salvatore-2026-05-13]] — trend following, value investing, walk-through canvas
- [[paper-trading-agents]] — TradingAgents framework (TauricResearch)
- [[paper-alpha-arena]] — benchmark LLM su trading crypto
- [[references/library-portfolio-optimizer]] — documentazione cvx-portfolio-optimizer
- [[references/architecture-handwritten-notes]] — schemi iniziali di sistema
- [[references/notion-export-investimento-trading]] — export Notion su trading e investimenti
- [[references/onboarding-wiki-workflow]] — metodo di lavoro e uso di Obsidian
- [[references/trading-floor-canvas]] — schema architettura multi-agente
- [[references/external/trading-agents-framework]] — TradingAgents framework (scheda sintetica)
- [[references/tradingagents-code-wiki]] — TradingAgents Code Wiki (documentazione tecnica del codebase: agenti, orchestrazione, data layer, LLM integration)
- [[references/external/cvx-portfolio-optimizer]] — cvx-portfolio-optimizer (scheda sintetica)

## Strategy — Conoscenza di mercato
*Approcci, indicatori, metriche: il dominio di Salvatore. Ogni elemento qui alimenta [[build/modules/module-c-quant-backtest]].*

- [[strategy/index]] — panoramica e principio di linking
- [[strategy/methods/trend-following]] — seguire il trend degli istituzionali
- [[strategy/methods/factor-investing]] — fattori fondamentali e quantitativi (post-MVP)

*(indicators/ e metrics/ si popolano man mano che Salvatore porta materiale)*

## Syntheses — Analisi trasversali
*Sintesi di ricerca, confronti, analisi che attraversano più fonti.*

- [[syntheses/notebooklm-research-2026-05-13]] — ricerca su TradingAgents, MarketSenseAI, Alpha Arena, Simone Rizzo

## Artifacts — Canvas e board
*Schemi visuali, roadmap, board di lavoro.*

- [[artifacts/trading-floor.canvas]] — canvas architettura multi-agente
- [[artifacts/mvp-system-cycle.canvas]] — ciclo operativo completo (MVP + post-MVP)
- [[artifacts/dev-roadmap.canvas]] — roadmap di sviluppo (Track 1/2/3)
- [[artifacts/luca-board]] — board di Luca (focus tecnico: AI, architettura, programmazione)
- [[artifacts/salvatore-board]] — board di Salvatore (focus economico: mercati, strategie)
- [[artifacts/artifact-workbench]] — ponte tra note e artifact
- [[artifacts/kanban-project-status]] — kanban stato progetto

## Meta
- [[_meta/glossario]] — glossario termini del progetto
- [[_meta/taxonomy]] — tassonomia tag e path cartelle
- [[_meta/log]] — log append-only di tutte le operazioni sul vault
- [[_meta/hot-cache]] — contesto sessione corrente
