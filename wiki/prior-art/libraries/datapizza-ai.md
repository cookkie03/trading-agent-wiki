---
title: "Datapizza AI Framework"
type: source
tags:
  - source
  - multi-agent
  - architecture
  - infrastructure
created: 2026-06-15
updated: 2026-06-15
status: draft
priority: high
area: software
related:
  - "[[system/modules/agents]]"
  - "[[system/architecture]]"
---

# Datapizza AI Framework

> **Proof of Concept** in corso su branch `feat/datapizza-migration` su `trading-agent/`.
> Migrazione da LangGraph a Datapizza AI per il layer di orchestrazione degli agenti.

## Link alla documentazione

- **Documentazione ufficiale**: [[https://docs.datapizza.ai/0.1.0/]]
- **GitHub**: [[https://github.com/datapizza-labs/datapizza-ai]]
- **PyPI**: [[https://pypi.org/project/datapizza-ai/]]

## Overview

`datapizza-ai` è un framework Python (3.10-3.12) per costruire agenti Gen AI con orchestrazione chiara e visibilità end-to-end. Fornisce:

- **Clienti multi-provider**: OpenAI, Google VertexAI, Ollama, ecc.
- **Agent API**: combinano `name` + `system_prompt` + `client` + tools/memory/hooks/structured output/handoffs
- **Pipeline RAG + tools** senza boilerplate multi-classe
- **Agent loop** con tracing/logging di ogni chiamata LLM/tool
- **MCP support**: Model Context Protocol per tool esterni
- **Multi-agent patterns**: agents-as-tools, handoffs
- **Structured output** integrato

## Guide chiave (struzione sidebar docs)

### Clients
- Quick Start — setup OpenAIClient, invoke/memory/tokens
- Multimodality, Streaming, Structured Responses, Tools
- Chatbot example, Ollama local

### Agents
- Build your first agent — `Agent(name, system_prompt, client)` + tools/memory/hooks
- Tool use control, Memory streaming
- Structured output, Multi-agent (agents-as-tools, handoffs)
- Agent loop observation, Plan-before-acting, Async run

### RAG
- Retrieval-Augmented Generation con tool integrati

### Pipeline
- Orchestrazione workflow multi-step

### Monitoring
- Tracing/logging di chiamate

## API Base (dalla documentazione)

```python
from datapizza.agents import Agent
from datapizza.clients.openai import OpenAIClient

agent = Agent(
    name="assistant",
    system_prompt="You are a helpful assistant.",
    client=OpenAIClient(api_key="YOUR_API_KEY", model="gpt-4o-mini"),
)

response = agent.invoke("What is the capital of France?")
print(response.text)
```

### Con tools

```python
from datapizza.agents import Agent
from datapizza.clients.openai import OpenAIClient

def get_weather(city: str) -> str:
    """Get the weather for a city."""
    return f"The weather in {city} is sunny"

agent = Agent(
    name="weather_assistant",
    system_prompt="You are a weather assistant.",
    client=OpenAIClient(api_key="YOUR_API_KEY"),
    tools=[get_weather],
)
```

## Mappatura LangGraph → Datapizza (ipotetica)

| Concetto LangGraph | Equivalente Datapizza |
|---------------------|-----------------------|
| `StateGraph` | `Agent` + pipeline config |
| `add_node` | Tool registration su `Agent` |
| `add_edge` / conditional | Multi-agent pattern (handoffs / agents-as-tools) |
| `State` (TypedDict) | `StructuredOutput` / agent memory |
| `tool.bind` | `tools=[...]` su Agent dispatch |
| `invoke` / `astream_events` | `agent.invoke()` / streaming guide |
| `checkpointer` | Agent memory / checkpoint da aggiungere |
| Interrupt / Human-in-the-loop | Da validare (hooks? custom?) |
| ` START` / `END` | Configurazione pipeline |

## Decisione

Valutare come sostituto di LangGraph per:
1. Semplificazione dell'orchestrazione (meno boilerplate)
2. Supporto nativo per agenti multipli con handoffs
3. Structured output integrato
4. Osservabilità migliore (tracing/logging)

**Proseguimento**: implementare un PoC di `brain/analyst_research` e `brain/pm` come Datapizza agents sulla branch `feat/datapizza-migration`.
