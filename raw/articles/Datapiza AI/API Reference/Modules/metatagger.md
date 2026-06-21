---
source: https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/metatagger/
---

[ Skip to content ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#cohereembedder)
[ ![logo](https://docs.datapizza.ai/0.1.0/assets/logo.png) ](https://docs.datapizza.ai/0.1.0/ "Datapizza AI")
Datapizza AI 
0.1.0
  * [0.1.0](https://docs.datapizza.ai/0.1.0/)
  * [0.0.9](https://docs.datapizza.ai/0.0.9/)
  * [0.0.7](https://docs.datapizza.ai/0.0.7/)
  * [0.0.2](https://docs.datapizza.ai/0.0.2/)


CohereEmbedder 
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
      * CohereEmbedder  [ CohereEmbedder  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/) Table of contents 
        * [ CohereEmbedder  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#datapizza.embedders.cohere.CohereEmbedder)
        * [ Usage  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#usage)
        * [ Features  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#features)
        * [ Examples  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#examples)
          * [ Basic Text Embedding  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#basic-text-embedding)
          * [ Search Query Embedding  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#search-query-embedding)
          * [ Batch Text Embedding  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#batch-text-embedding)
          * [ Async Embedding  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#async-embedding)
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
  * [ CohereEmbedder  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#datapizza.embedders.cohere.CohereEmbedder)
  * [ Usage  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#usage)
  * [ Features  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#features)
  * [ Examples  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#examples)
    * [ Basic Text Embedding  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#basic-text-embedding)
    * [ Search Query Embedding  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#search-query-embedding)
    * [ Batch Text Embedding  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#batch-text-embedding)
    * [ Async Embedding  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#async-embedding)


  1. [ Home  ](https://docs.datapizza.ai/0.1.0/)
  2. [ API Reference  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/clients/)
  3. [ Embedders  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/)


# CohereEmbedder

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-0-1)pip install datapizza-ai-embedders-cohere

```

##  datapizza.embedders.cohere.CohereEmbedder
Bases: `BaseEmbedder`
## Usage

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-1-1)from datapizza.embedders.cohere import CohereEmbedder
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-1-2)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-1-3)embedder = CohereEmbedder(
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-1-4)    api_key="your-cohere-api-key",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-1-5)    base_url="https://api.cohere.ai/v1",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-1-6)    input_type="search_document"  # or "search_query"
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-1-7))
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-1-8)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-1-9)# Embed a single text
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-1-10)embedding = embedder.embed("Hello world", model_name="embed-english-v3.0")
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-1-11)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-1-12)# Embed multiple texts
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-1-13)embeddings = embedder.embed(
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-1-14)    ["Hello world", "Another text"],
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-1-15)    model_name="embed-english-v3.0"
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-1-16))

```

## Features
  * Supports Cohere's embedding models
  * Configurable input type for search documents or queries
  * Handles both single text and batch text embedding
  * Async embedding support with `a_embed()`
  * Custom endpoint support for compatible APIs
  * Uses Cohere's ClientV2 for optimal performance


## Examples
### Basic Text Embedding

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-2-1)from datapizza.embedders.cohere import CohereEmbedder
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-2-2)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-2-3)embedder = CohereEmbedder(
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-2-4)    api_key="your-cohere-api-key",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-2-5)    base_url="https://api.cohere.ai/v1",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-2-6)    input_type="search_document"
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-2-7))
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-2-8)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-2-9)# Single text embedding
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-2-10)text = "This is a sample document for embedding."
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-2-11)embedding = embedder.embed(text, model_name="embed-english-v3.0")
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-2-12)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-2-13)print(f"Embedding dimensions: {len(embedding)}")
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-2-14)print(f"First 5 values: {embedding[:5]}")

```

### Search Query Embedding

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-3-1)from datapizza.embedders.cohere import CohereEmbedder
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-3-2)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-3-3)# Configure for search queries
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-3-4)embedder = CohereEmbedder(
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-3-5)    api_key="your-cohere-api-key",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-3-6)    base_url="https://api.cohere.ai/v1",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-3-7)    input_type="search_query"
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-3-8))
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-3-9)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-3-10)query = "What is machine learning?"
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-3-11)embedding = embedder.embed(query, model_name="embed-english-v3.0")
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-3-12)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-3-13)print(f"Query embedding size: {len(embedding)}")

```

### Batch Text Embedding

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-4-1)from datapizza.embedders.cohere import CohereEmbedder
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-4-2)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-4-3)embedder = CohereEmbedder(
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-4-4)    api_key="your-cohere-api-key",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-4-5)    base_url="https://api.cohere.ai/v1"
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-4-6))
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-4-7)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-4-8)texts = [
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-4-9)    "First document to embed",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-4-10)    "Second document to embed",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-4-11)    "Third document to embed"
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-4-12)]
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-4-13)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-4-14)embeddings = embedder.embed(texts, model_name="embed-english-v3.0")
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-4-15)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-4-16)for i, emb in enumerate(embeddings):
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-4-17)    print(f"Document {i+1} embedding size: {len(emb)}")

```

### Async Embedding

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-5-1)import asyncio
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-5-2)from datapizza.embedders.cohere import CohereEmbedder
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-5-3)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-5-4)async def embed_async():
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-5-5)    embedder = CohereEmbedder(
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-5-6)        api_key="your-cohere-api-key",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-5-7)        base_url="https://api.cohere.ai/v1"
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-5-8)    )
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-5-9)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-5-10)    text = "Async embedding example"
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-5-11)    embedding = await embedder.a_embed(text, model_name="embed-english-v3.0")
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-5-12)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-5-13)    return embedding
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-5-14)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-5-15)# Run async function
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/cohere_embedder/#__codelineno-5-16)embedding = asyncio.run(embed_async())

```

Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
