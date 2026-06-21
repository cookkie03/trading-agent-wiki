---
source: https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/node_splitter/
---

[ Skip to content ](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/#model-context-protocol-mcp)
[ ![logo](https://docs.datapizza.ai/0.1.0/assets/logo.png) ](https://docs.datapizza.ai/0.1.0/ "Datapizza AI")
Datapizza AI 
0.1.0
  * [0.1.0](https://docs.datapizza.ai/0.1.0/)
  * [0.0.9](https://docs.datapizza.ai/0.0.9/)
  * [0.0.7](https://docs.datapizza.ai/0.0.7/)
  * [0.0.2](https://docs.datapizza.ai/0.0.2/)


Model Context Protocol (MCP) 
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
      * [ Build your first agent  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/)
      * Model Context Protocol (MCP)  [ Model Context Protocol (MCP)  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/) Table of contents 
        * [ Fetch MCP tools  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/#fetch-mcp-tools)
        * [ Create the agent and run it  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/#create-the-agent-and-run-it)
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
  * [ Fetch MCP tools  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/#fetch-mcp-tools)
  * [ Create the agent and run it  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/#create-the-agent-and-run-it)


  1. [ Home  ](https://docs.datapizza.ai/0.1.0/)
  2. [ Guides  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/quick_start/)
  3. [ Agents  ](https://docs.datapizza.ai/0.1.0/Guides/Agents/agent/)


# Model Context Protocol (MCP)
Model Context Protocol (MCP) is an open-source standard that enables AI applications to connect with external systems like databases, APIs, and tools.
Use MCP (Model Context Protocol) tools inside `datapizza-ai` by wrapping them as regular agent tools. Follow this minimal recipe to get an agent talking to a remote MCP server in just a few steps.
With MCP, you can build AI agents that:
  * **Access your codebase** : Let AI read GitHub repositories, create issues, and manage pull requests
  * **Query your database** : Enable natural language queries against PostgreSQL, MySQL, or any database
  * **Browse the web** : Give AI the ability to search and extract information from websites
  * **Control your tools** : Connect to Slack, Notion, Google Calendar, or any API-based service
  * **Analyze your data** : Let AI work with spreadsheets, documents, and business intelligence tools


## Fetch MCP tools
Here an example of [FastMCP](https://gofastmcp.com/getting-started/welcome) tool provided by FastMCP

```
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/#__codelineno-0-1)from datapizza.tools.mcp_client import MCPClient
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/#__codelineno-0-2)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/#__codelineno-0-3)fastmcp_client = MCPClient(url="https://gofastmcp.com/mcp")
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/#__codelineno-0-4)fastmcp_tools = fastmcp_client.list_tools()

```

## Create the agent and run it

```
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/#__codelineno-1-1)from datapizza.agents import Agent
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/#__codelineno-1-2)from datapizza.clients.openai import OpenAIClient
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/#__codelineno-1-3)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/#__codelineno-1-4)client = OpenAIClient(api_key="OPENAI_API_KEY", model="gpt-4o-mini")
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/#__codelineno-1-5)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/#__codelineno-1-6)agent = Agent(
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/#__codelineno-1-7)    name="mcp_agent",
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/#__codelineno-1-8)    client=client,
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/#__codelineno-1-9)    tools=fastmcp_tools,
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/#__codelineno-1-10))
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/#__codelineno-1-11)
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/#__codelineno-1-12)result = agent.run("How can I use a FastMCP server over HTTP?")
[](https://docs.datapizza.ai/0.1.0/Guides/Agents/mcp/#__codelineno-1-13)print(result.text)

```

That’s it—you now have an agent that discovers tools from the FastMCP server and uses them as part of normal `datapizza-ai` reasoning. Swap in any MCP endpoint or different LLM client to match your project.
Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
