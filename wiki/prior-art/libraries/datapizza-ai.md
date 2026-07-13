---
title: "Datapizza AI Framework"
type: source
tags:
  - source
  - multi-agent
  - architecture
  - infrastructure
created: 2026-06-15
updated: 2026-06-20
status: active
priority: high
area: software
related:
  - "[[system/agents/agents]]"
  - "[[system/foundation/architecture]]"
  - "[[system/foundation/stack]]"
---

# Datapizza AI Framework

> ✅ **Migrazione completata (2026-06-17)** — `datapizza-ai>=0.1.0` è ora il framework di orchestrazione principale di `trading-agent/`. Sostituisce completamente LangGraph + LangChain. Branch `feat/datapizza-migration` → merge in `feat/refactor-pipeline`.

## Link alla documentazione

- **Documentazione ufficiale**: [docs.datapizza.ai](https://docs.datapizza.ai/0.1.0/)
- **GitHub**: [github.com/datapizza-labs/datapizza-ai](https://github.com/datapizza-labs/datapizza-ai)
- **PyPI**: [pypi.org/project/datapizza-ai/](https://pypi.org/project/datapizza-ai/)

## Overview

`datapizza-ai` è un framework Python (3.10-3.12) per costruire agenti Gen AI con orchestrazione chiara e visibilità end-to-end. Fornisce:

- **Clienti multi-provider**: OpenAI, Google VertexAI, Ollama, OpenRouter, DeepSeek, ecc.
- **Agent API**: combinano `name` + `system_prompt` + `client` + tools/memory/hooks/structured output/handoffs
- **Pipeline RAG + tools** senza boilerplate multi-classe
- **Agent loop** con tracing/logging di ogni chiamata LLM/tool
- **MCP support**: Model Context Protocol per tool esterni
- **Multi-agent patterns**: agents-as-tools, handoffs
- **Structured output** integrato

## Implementazione nel progetto

### File chiave

| File | Ruolo |
|------|-------|
| `brain/datapizza_graph.py` | Definizione del grafo agenti (START→desk→PM→Risk→END) |
| `brain/datapizza_director.py` | Orchestratore: direttore/valutatore/desk hierarchy |
| `brain/datapizza_llm.py` | Wrapper LLM (multi-provider via Datapizza clients) |
| `brain/datapizza_tools.py` | Tool binding per agenti (market, portfolio, options) |
| `orchestration/datapizza_analyze.py` | Analyzer hook: innesta il grafo nel `run_cycle` |

### Architettura agenti (post-migrazione)

```
START
  → Analyst Research (Market + Sentiment)
  → Analyst Technical (Technical + Fondamentali)
  → PM (aggrega agent_opinions → direction/conviction)
  → Risk (gate bear + guardrail deterministici)
  → (loop "nel dubbio chiedi", capped)
  → END
```

### Mappatura LangGraph → Datapizza (effettiva)

| Concetto LangGraph | Equivalente Datapizza | Stato |
|---------------------|-----------------------|-------|
| `StateGraph` | `Agent` + pipeline config | ✅ Implementato |
| `add_node` | Tool registration su `Agent` | ✅ Implementato |
| `add_edge` / conditional | Multi-agent pattern (handoffs) | ✅ Implementato |
| `State` (TypedDict) | `StructuredOutput` / agent memory | ✅ Implementato |
| `tool.bind` | `tools=[...]` su Agent dispatch | ✅ Implementato |
| `invoke` / `astream_events` | `agent.invoke()` / streaming | ✅ Implementato |
| `checkpointer` | Agent memory | ⚠️ Parziale |
| Interrupt / Human-in-the-loop | Hooks (da validare) | ⚠️ Da validare |
| `START` / `END` | Pipeline config | ✅ Implementato |

## Rimosso con la migrazione

- `tradingagents/brain/llm.py` (vecchio LangGraph LLM wrapper)
- `tradingagents/brain/tooling.py` (vecchio build_desk_tools)
- `tradingagents/llm_clients/` (intero modulo)
- `tradingagents/structured.py` (LangChain leftover)
- Dipendenze: `langchain`, `langchain-core`, `langgraph`, `langsmith`

## Vedi anche

- [[system/agents/agents]] — dettaglio agenti e tool-calling
- [[system/foundation/architecture]] — architettura completa
- [[system/foundation/stack]] — tech stack e dipendenze
