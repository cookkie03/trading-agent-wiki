---
source: https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/
---

[ Skip to content ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#build-your-first-agent)
[ ![logo](https://docs.datapizza.ai/0.1.0/assets/logo.png) ](https://docs.datapizza.ai/0.1.0/ "Datapizza AI")
Datapizza AI 
0.1.0
  * [0.1.0](https://docs.datapizza.ai/0.1.0/)
  * [0.0.9](https://docs.datapizza.ai/0.0.9/)
  * [0.0.7](https://docs.datapizza.ai/0.0.7/)
  * [0.0.2](https://docs.datapizza.ai/0.0.2/)


Build your first agent 
Type to start searching
[ datapizza-labs/datapizza-ai  ](https://github.com/datapizza-labs/datapizza-ai "Go to repository")
  * [ Home ](https://docs.datapizza.ai/0.1.0/)
  * [ Guides ](https://docs.datapizza.ai/0.1.0/Guides/Clients/quick_start/)
  * [ API Reference ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/clients/)


[ ![logo](https://docs.datapizza.ai/0.1.0/assets/logo.png) ](https://docs.datapizza.ai/0.1.0/ "Datapizza AI") Datapizza AI 
[ datapizza-labs/datapizza-ai  ](https://github.com/datapizza-labs/datapizza-ai "Go to repository")
  * [ Home  ](https://docs.datapizza.ai/0.1.0/)
  * Guides  Guides 
    * Clients  Clients 
      * [ Quick Start  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/quick_start/)
      * [ Multimodality  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/)
      * [ Structured Responses  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/structured_responses/)
      * [ Streaming  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/streaming/)
      * [ Tools  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/tools/)
      * [ Real example: Chatbot  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/chatbot/)
      * [ Running with Ollama  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/local_model/)
    * Agents  Agents 
      * Build your first agent  [ Build your first agent  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/) Table of contents 
        * [ Create your first agent  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#create-your-first-agent)
        * [ Run your first agent  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#run-your-first-agent)
        * [ Give your agent tools  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#give-your-agent-tools)
          * [ Control tool use  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#control-tool-use)
        * [ Add memory to your agent  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#add-memory-to-your-agent)
        * [ Stream responses  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#stream-responses)
        * [ Return structured data  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#return-structured-data)
        * [ Choose a multi-agent pattern  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#choose-a-multi-agent-pattern)
          * [ Agents as tools  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#agents-as-tools)
          * [ Handoffs  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#handoffs)
        * [ Observe the agent loop  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#observe-the-agent-loop)
        * [ Plan before acting  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#plan-before-acting)
        * [ Async run  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#async-run)
        * [ Next steps  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#next-steps)
      * [ Model Context Protocol (MCP)  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/)
    * RAG  RAG 
      * [ Build a RAG  ](https://docs.datapizza.ai/0.1.0/Guides/RAG/rag/)
    * Pipeline  Pipeline 
      * [ Ingestion Pipeline  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/)
      * [ DagPipeline  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/)
      * [ Functional Pipeline  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/)
    * Monitoring  Monitoring 
      * [ Tracing  ](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/)
      * [ Log level  ](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/log/)
  * API Reference  API Reference 
    * Clients  Clients 
      * [ Clients  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/clients/)
      * [ Client Factory  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/client_factory/)
      * [ Response  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/)
      * [ Cache  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/cache/)
      * Avaiable Clients  Avaiable Clients 
        * [ Openai  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/Avaiable_Clients/openai/)
        * [ Google  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/Avaiable_Clients/google/)
        * [ Anthropic  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/Avaiable_Clients/anthropic/)
        * [ Azure Openai  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/Avaiable_Clients/AzureOpenai/)
        * [ Mistral  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/Avaiable_Clients/mistral/)
        * [ Openai like  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/Avaiable_Clients/openai-like/)
        * [ IBM WatsonX  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/Avaiable_Clients/watsonx/)
    * Agents  Agents 
      * [ Agent  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Agents/agent/)
    * Embedders  Embedders 
      * [ ChunkEmbedder  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/)
      * [ CohereEmbedder  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/)
      * [ FastEmbedder  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/fast_embedder/)
      * [ GoogleEmbedder  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/google_embedder/)
      * [ MistralEmbedder  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/)
      * [ OllamaEmbedder  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/ollama_embedder/)
      * [ OpenAIEmbedder  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/openai_embedder/)
    * Vectorstore  Vectorstore 
      * [ Milvus  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Vectorstore/milvus_vectorstore/)
      * [ Qdrant  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Vectorstore/qdrant_vectorstore/)
    * [ Memory  ](https://docs.datapizza.ai/0.1.0/API%20Reference/memory/)
    * Type  Type 
      * [ Blocks  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Type/block/)
      * [ Chunk  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Type/chunk/)
      * [ Media  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Type/media/)
      * [ Node  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Type/node/)
      * [ Tool  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Type/tool/)
    * Pipelines  Pipelines 
      * [ Dag  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Pipelines/dag/)
      * [ Functional  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Pipelines/functional/)
      * [ Ingestion  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Pipelines/ingestion/)
    * Modules  Modules 
      * [ Modules  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/)
      * Parsers  Parsers 
        * [ TextParser  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Parsers/text_parser/)
        * [ DoclingParser  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Parsers/docling_parser/)
        * [ AzureParser  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Parsers/azure_parser/)
      * [ Treebuilder  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/treebuilder/)
      * [ Captioners  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/captioners/)
      * Splitters  Splitters 
        * [ RecursiveSplitter  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/recursive_splitter/)
        * [ TextSplitter  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/text_splitter/)
        * [ NodeSplitter  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/node_splitter/)
        * [ PDFImageSplitter  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/)
      * [ Metatagger  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/metatagger/)
      * [ Rewriters  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/rewriters/)
      * Rerankers  Rerankers 
        * [ CohereReranker  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/)
        * [ TogetherReranker  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/)
      * Prompt  Prompt 
        * [ ChatPromptTemplate  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Prompt/ChatPromptTemplate/)
    * Tools  Tools 
      * [ MCPClient  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Tools/mcp/)
      * [ DuckDuckGo  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Tools/duckduckgo/)
      * [ FileSystem  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Tools/filesystem/)
      * [ SQLDatabase  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Tools/SQLDatabase/)
      * [ WebFetch  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Tools/web_fetch/)


Table of contents 
  * [ Create your first agent  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#create-your-first-agent)
  * [ Run your first agent  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#run-your-first-agent)
  * [ Give your agent tools  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#give-your-agent-tools)
    * [ Control tool use  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#control-tool-use)
  * [ Add memory to your agent  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#add-memory-to-your-agent)
  * [ Stream responses  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#stream-responses)
  * [ Return structured data  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#return-structured-data)
  * [ Choose a multi-agent pattern  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#choose-a-multi-agent-pattern)
    * [ Agents as tools  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#agents-as-tools)
    * [ Handoffs  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#handoffs)
  * [ Observe the agent loop  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#observe-the-agent-loop)
  * [ Plan before acting  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#plan-before-acting)
  * [ Async run  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#async-run)
  * [ Next steps  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#next-steps)


  1. [ Home  ](https://docs.datapizza.ai/0.1.0/)
  2. [ Guides  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/quick_start/)
  3. [ Agents  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/)


# Build your first agent
Agents are the core building block in Datapizza AI.
An `Agent` combines:
  * a `name`
  * a `system_prompt`
  * a `client`
  * optional tools, memory, hooks, structured output, and handoffs


Use this page to get an agent running quickly, then add the capabilities you need.
## Create your first agent
Start with the smallest useful setup.

```
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-0-1)from datapizza.agents import Agent
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-0-2)from datapizza.clients.openai import OpenAIClient
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-0-3)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-0-4)agent = Agent(
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-0-5)    name="assistant",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-0-6)    system_prompt="You are a helpful assistant.",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-0-7)    client=OpenAIClient(api_key="YOUR_API_KEY", model="gpt-4o-mini"),
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-0-8))

```

The only required pieces are:
  * `name`: a human-readable name for the agent
  * `system_prompt`: the instructions the model follows
  * `client`: the model provider implementation


## Run your first agent
Call `run(...)` and read the final answer from `result.text`.

```
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-1-1)result = agent.run("Write a one-line welcome message for a new user.")
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-1-2)print(result.text)

```

`run(...)` returns a `StepResult`, not a plain string.
The most useful properties are:
  * `result.text`: the final text answer
  * `result.tools_used`: tools called in that step
  * `result.structured_data`: parsed structured output when `output_cls` is set
  * `result.usage`: token usage aggregated for the run


## Give your agent tools
Tools let the agent fetch data or perform actions.

```
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-2-1)from datapizza.agents import Agent
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-2-2)from datapizza.clients.openai import OpenAIClient
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-2-3)from datapizza.tools import tool
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-2-4)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-2-5)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-2-6)@tool
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-2-7)def get_weather(location: str, when: str) -> str:
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-2-8)    """Return weather information for a location and time."""
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-2-9)    return "25 C"
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-2-10)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-2-11)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-2-12)agent = Agent(
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-2-13)    name="weather_agent",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-2-14)    system_prompt="You help users with weather questions.",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-2-15)    client=OpenAIClient(api_key="YOUR_API_KEY", model="gpt-4o-mini"),
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-2-16)    tools=[get_weather],
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-2-17))
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-2-18)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-2-19)result = agent.run("What's the weather tomorrow in Milan?")
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-2-20)print(result.text)

```

### Control tool use
At run time, you can control how the model uses tools with `tool_choice`.

```
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-3-1)result = agent.run(
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-3-2)    "What's the weather in Milan?",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-3-3)    tool_choice="required_first",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-3-4))

```

Supported values:
  * `"auto"`: the model decides whether to use a tool
  * `"required"`: the model must use a tool every step
  * `"none"`: the model must not use tools
  * `"required_first"`: the first step must use a tool, later steps go back to `auto`
  * `list[str]`: restrict tool use to a named subset


## Add memory to your agent
You can pass a custom `Memory` object. This is useful when you want to start one specific run from custom history without changing the agent's default memory.

```
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-4-1)from datapizza.memory import Memory
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-4-2)from datapizza.type import ROLE, TextBlock
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-4-3)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-4-4)memory = Memory()
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-4-5)memory.add_turn(TextBlock(content="The user's name is Federico."), role=ROLE.USER)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-4-6)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-4-7)result = agent.run("What is the user's name?", memory=memory)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-4-8)print(result.text)

```

## Stream responses
Use `stream_invoke(...)` when you want to observe the run as it happens.
It yields:
  * `ClientResponse` chunks when client streaming is enabled
  * `StepResult` objects for completed agent steps
  * `Plan` objects when planning is enabled



```
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-5-1)from datapizza.agents import Agent, StepResult
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-5-2)from datapizza.clients.openai import OpenAIClient
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-5-3)from datapizza.core.clients import ClientResponse
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-5-4)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-5-5)agent = Agent(
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-5-6)    name="assistant",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-5-7)    system_prompt="You are a helpful assistant.",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-5-8)    client=OpenAIClient(api_key="YOUR_API_KEY", model="gpt-4o-mini"),
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-5-9)    stream=True,
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-5-10))
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-5-11)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-5-12)for event in agent.stream_invoke("Tell me a short joke."):
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-5-13)    if isinstance(event, ClientResponse):
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-5-14)        print(event.delta, end="", flush=True)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-5-15)    elif isinstance(event, StepResult):
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-5-16)        print("\nfinal step:", event.text)

```

Async streaming works the same way with `a_stream_invoke(...)`.

```
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-6-1)import asyncio
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-6-2)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-6-3)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-6-4)async def main():
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-6-5)    agent = Agent(
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-6-6)        name="assistant",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-6-7)        system_prompt="You are a helpful assistant.",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-6-8)        client=OpenAIClient(api_key="YOUR_API_KEY", model="gpt-4o-mini"),
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-6-9)        stream=True,
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-6-10)    )
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-6-11)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-6-12)    async for event in agent.a_stream_invoke("Tell me a short joke."):
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-6-13)        print(event)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-6-14)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-6-15)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-6-16)asyncio.run(main())

```

## Return structured data
If you want typed output instead of plain text, set `output_cls`.

```
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-7-1)from pydantic import BaseModel
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-7-2)from datapizza.agents import Agent
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-7-3)from datapizza.clients.openai import OpenAIClient
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-7-4)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-7-5)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-7-6)class Person(BaseModel):
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-7-7)    name: str
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-7-8)    age: int
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-7-9)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-7-10)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-7-11)agent = Agent(
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-7-12)    name="person_extractor",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-7-13)    system_prompt="Extract a person from the input.",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-7-14)    client=OpenAIClient(api_key="YOUR_API_KEY", model="gpt-4.1-mini"),
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-7-15)    output_cls=Person,
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-7-16))
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-7-17)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-7-18)result = agent.run('{"name": "Alice", "age": 30}')
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-7-19)person = result.structured_data[0]
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-7-20)print(person.name)

```

When `output_cls` is set:
  * the agent asks the client for structured output on each model turn
  * the parsed objects are available in `result.structured_data`
  * `result.text` may be empty


If the selected client does not support structured output, Datapizza raises a clear `ValueError`.
## Choose a multi-agent pattern
Before adding more agents, decide who should own the final answer.
  * `can_call(...)` / `as_tool()`: one orchestrator stays in control and calls specialists as tools
  * `handoffs`: control transfers to another agent, which continues the run


Use `can_call(...)` when you want a manager pattern. Use `handoffs` when you want a specialist to take over.
### Agents as tools
In this pattern, the main agent keeps control of the conversation.

```
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-1)from datapizza.agents import Agent
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-2)from datapizza.clients.openai import OpenAIClient
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-3)from datapizza.tools import tool
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-4)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-5)client = OpenAIClient(api_key="YOUR_API_KEY", model="gpt-4.1")
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-6)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-7)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-8)@tool
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-9)def get_weather(city: str) -> str:
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-10)    return f"The weather in {city} is sunny."
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-11)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-12)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-13)weather_agent = Agent(
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-14)    name="weather_expert",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-15)    description="Answers weather questions.",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-16)    system_prompt="You are a weather expert.",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-17)    client=client,
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-18)    tools=[get_weather],
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-19))
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-20)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-21)planner_agent = Agent(
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-22)    name="planner",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-23)    system_prompt="You are a travel planner. Use specialist tools when useful.",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-24)    client=client,
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-25))
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-26)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-27)planner_agent.can_call(weather_agent)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-28)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-29)result = planner_agent.run("Can I go hiking in Milan tomorrow?")
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-8-30)print(result.text)

```

You can also convert an agent manually with `as_tool()`.

```
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-9-1)tool = weather_agent.as_tool()

```

If delegating should end the orchestrator run immediately, use `end=True`.

```
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-10-1)terminal_tool = weather_agent.as_tool(end=True)

```

When Datapizza builds a tool from an agent, the tool description is chosen in this order:
  1. `description` passed to `Agent(...)`
  2. the agent class docstring
  3. the agent name


### Handoffs
In this pattern, one agent transfers control to another.

```
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-11-1)from datapizza.agents import Agent
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-11-2)from datapizza.clients.openai import OpenAIClient
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-11-3)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-11-4)client = OpenAIClient(api_key="YOUR_API_KEY", model="gpt-4.1")
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-11-5)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-11-6)refund_agent = Agent(
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-11-7)    name="refund_specialist",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-11-8)    system_prompt="Handle refund requests clearly and safely.",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-11-9)    client=client,
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-11-10))
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-11-11)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-11-12)triage_agent = Agent(
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-11-13)    name="triage",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-11-14)    system_prompt="Route the user to the right specialist.",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-11-15)    client=client,
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-11-16)    handoffs=[refund_agent],
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-11-17))
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-11-18)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-11-19)result = triage_agent.run("I was charged twice. I need a refund.")
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-11-20)print(result.text)

```

You can also register handoffs later:

```
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-12-1)triage_agent.can_handoff(refund_agent)

```

For most users, `agent.run(...)` is enough. Datapizza creates an `AgentRunner` internally.
If you need richer orchestration metadata, use `AgentRunner` directly.

```
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-13-1)from datapizza.agents import AgentRunner
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-13-2)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-13-3)runner = AgentRunner()
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-13-4)result = runner.run(triage_agent, "I was charged twice.")
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-13-5)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-13-6)print(result.final_step.text)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-13-7)print(result.final_agent.name)

```

`AgentRunner.run(...)` returns an `AgentRunnerResult` with these fields:
  * `final_step`: the final `StepResult`
  * `final_agent`: the agent that produced the final answer
  * `handoff_count`: how many handoffs happened during the run
  * `visited_agents`: the sequence of agents visited during the run
  * `memory`: the shared `Memory` used for the run
  * `usage`: aggregated `TokenUsage` for the whole run


## Observe the agent loop
Use hooks when you want to log or inspect each step.

```
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-14-1)from datapizza.agents import Agent, AgentHooks, StepContext, StepResult
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-14-2)from datapizza.clients.openai import OpenAIClient
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-14-3)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-14-4)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-14-5)class DebugHooks(AgentHooks):
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-14-6)    def before_step(self, context: StepContext) -> None:
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-14-7)        print(f"starting step {context.step_index}")
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-14-8)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-14-9)    def after_step(self, context: StepContext, result: StepResult) -> None:
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-14-10)        print(f"finished step {context.step_index}: {result.text}")
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-14-11)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-14-12)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-14-13)agent = Agent(
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-14-14)    name="assistant",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-14-15)    system_prompt="You are a helpful assistant.",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-14-16)    client=OpenAIClient(api_key="YOUR_API_KEY", model="gpt-4o-mini"),
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-14-17)    hooks=DebugHooks(),
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-14-18))

```

`before_step(...)` runs at the start of each loop iteration. `after_step(...)` runs after the step result is produced.
## Plan before acting
If you want the agent to periodically create a plan before continuing, set `planning_interval`.

```
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-15-1)agent = Agent(
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-15-2)    name="planner_agent",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-15-3)    system_prompt="You solve tasks carefully.",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-15-4)    client=OpenAIClient(api_key="YOUR_API_KEY", model="gpt-4.1"),
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-15-5)    planning_interval=3,
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-15-6))

```

When planning is enabled, the agent generates a structured `Plan` at regular intervals and then continues execution.
## Async run
If your application is async, use `a_run(...)`.

```
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-16-1)import asyncio
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-16-2)from datapizza.agents import Agent
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-16-3)from datapizza.clients.openai import OpenAIClient
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-16-4)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-16-5)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-16-6)async def main():
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-16-7)    agent = Agent(
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-16-8)        name="assistant",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-16-9)        system_prompt="You are a helpful assistant.",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-16-10)        client=OpenAIClient(api_key="YOUR_API_KEY", model="gpt-4o-mini"),
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-16-11)    )
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-16-12)    result = await agent.a_run("Summarize this text in one sentence.")
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-16-13)    print(result.text)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-16-14)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-16-15)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/#__codelineno-16-16)asyncio.run(main())

```

## Next steps
If you want to...
  * add capabilities to your agent, read the tools guide
  * build manager-style or handoff-based systems, read the multi-agent guides
  * stream events in more detail, use `stream_invoke(...)` / `a_stream_invoke(...)`
  * inspect orchestration metadata, use `AgentRunner`


Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
