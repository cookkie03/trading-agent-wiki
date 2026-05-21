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
- [[references/external/paper-trading-agents]] — TradingAgents paper + pattern adottati nel progetto — *anche come bare link `[[paper-trading-agents]]`*
- [[references/external/paper-alpha-arena]] — benchmark LLM su trading crypto — *anche come bare link `[[paper-alpha-arena]]`*
- [[references/architecture-handwritten-notes]] — schemi iniziali di sistema
- [[references/notion-export-investimento-trading]] — export Notion su trading e investimenti
- [[references/onboarding-wiki-workflow]] — metodo di lavoro e uso di Obsidian
- [[references/trading-floor-canvas]] — schema architettura multi-agente
- [[references/tradingagents-code-wiki]] — TradingAgents Code Wiki (documentazione tecnica del codebase: agenti, orchestrazione, data layer, LLM integration)
- [[references/external/cvx-portfolio-optimizer]] — cvx-portfolio-optimizer (documentazione completa, merge con library-portfolio-optimizer)
- [[references/tool-set-provider-dati-exchange]] — broker con API Python disponibili in Italia + provider dati gratuiti (stack raccomandato)
- [[references/note-audio-salvatore-quant-strategy]] — note audio Salvatore su strategie quant: dual portfolio value+quant, mean reversion/stat arb
- [[references/quantitative-trading-strategies-brenndoerfer]] — articolo Brenndoerfer su quant trading: alpha, backtesting, metriche performance (con codice Python)

## Strategy — Conoscenza di mercato
*Approcci, indicatori, metriche: il dominio di Salvatore. Ogni elemento qui alimenta [[build/modules/module-c-quant-backtest]].*

- [[strategy/index]] — panoramica e principio di linking
- [[strategy/methods/trend-following]] — seguire il trend degli istituzionali
- [[strategy/methods/factor-investing]] — fattori fondamentali e quantitativi (post-MVP)
- [[strategy/methods/mean-reversion-stat-arb]] — mean reversion e statistical arbitrage / pairs trading (candidata Modulo C)

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
- [[artifacts/idea architettura.canvas]] — canvas architettura (artifact di lavoro)

## Meta
- [[_meta/glossario]] — glossario termini del progetto
- [[_meta/taxonomy]] — tassonomia tag e path cartelle
- [[_meta/log]] — log append-only di tutte le operazioni sul vault
- [[_meta/hot-cache]] — contesto sessione corrente
