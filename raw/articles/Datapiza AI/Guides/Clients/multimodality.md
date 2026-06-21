---
source: https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/
---

[ Skip to content ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#coherereranker)
[ ![logo](https://docs.datapizza.ai/0.1.0/assets/logo.png) ](https://docs.datapizza.ai/0.1.0/ "Datapizza AI")
Datapizza AI 
0.1.0
  * [0.1.0](https://docs.datapizza.ai/0.1.0/)
  * [0.0.9](https://docs.datapizza.ai/0.0.9/)
  * [0.0.7](https://docs.datapizza.ai/0.0.7/)
  * [0.0.2](https://docs.datapizza.ai/0.0.2/)


CohereReranker 
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
        * CohereReranker  [ CohereReranker  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/) Table of contents 
          * [ Installation  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#installation)
          * [ CohereReranker  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#datapizza.modules.rerankers.cohere.CohereReranker)
            * [ __init__  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#datapizza.modules.rerankers.cohere.CohereReranker.__init__)
            * [ a_rerank  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#datapizza.modules.rerankers.cohere.CohereReranker.a_rerank)
            * [ rerank  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#datapizza.modules.rerankers.cohere.CohereReranker.rerank)
          * [ Usage  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#usage)
          * [ Features  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#features)
          * [ Examples  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#examples)
            * [ Basic Usage  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#basic-usage)
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
  * [ Installation  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#installation)
  * [ CohereReranker  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#datapizza.modules.rerankers.cohere.CohereReranker)
    * [ __init__  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#datapizza.modules.rerankers.cohere.CohereReranker.__init__)
    * [ a_rerank  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#datapizza.modules.rerankers.cohere.CohereReranker.a_rerank)
    * [ rerank  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#datapizza.modules.rerankers.cohere.CohereReranker.rerank)
  * [ Usage  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#usage)
  * [ Features  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#features)
  * [ Examples  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#examples)
    * [ Basic Usage  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#basic-usage)


  1. [ Home  ](https://docs.datapizza.ai/0.1.0/)
  2. [ API Reference  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/clients/)
  3. [ Modules  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/)
  4. [ Rerankers  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/)


# CohereReranker
A reranker that uses Cohere's reranking API to score and reorder documents based on query relevance.
## Installation

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-0-1)pip install datapizza-ai-rerankers-cohere

```

##  datapizza.modules.rerankers.cohere.CohereReranker
Bases: `Reranker`
A reranker that uses the Cohere API to rerank documents.
###  __init__

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-0-1)__init__(
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-0-2)    api_key,
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-0-3)    endpoint,
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-0-4)    top_n=10,
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-0-5)    threshold=None,
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-0-6)    model="model",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-0-7))

```

Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_key`  |  `str`  |  The API key for the Cohere API.  |  _required_  |  
|  `endpoint`  |  `str`  |  The endpoint for the Cohere API.  |  _required_  |  
|  `top_n`  |  `int`  |  The number of documents to return.  |  `10`  |  
|  `threshold`  |  `float | None`  |  The threshold for the reranker.  |  `None`  |  
###  a_rerank `async`

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-0-1)a_rerank(query, documents)

```

Rerank documents based on query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  `str`  |  The query to rerank documents by.  |  _required_  |  
|  `documents`  |  `list[Chunk[](https://docs.datapizza.ai/0.1.0/API%20Reference/Type/chunk/#datapizza.type.Chunk "datapizza.type.Chunk


  
      dataclass
  ")]`  |  The documents to rerank.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `list[Chunk[](https://docs.datapizza.ai/0.1.0/API%20Reference/Type/chunk/#datapizza.type.Chunk "datapizza.type.Chunk


  
      dataclass
  ")]`  |  The reranked documents.  |  
###  rerank

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-0-1)rerank(query, documents)

```

Rerank documents based on query.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `query`  |  `str`  |  The query to rerank documents by.  |  _required_  |  
|  `documents`  |  `list[Chunk[](https://docs.datapizza.ai/0.1.0/API%20Reference/Type/chunk/#datapizza.type.Chunk "datapizza.type.Chunk


  
      dataclass
  ")]`  |  The documents to rerank.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `list[Chunk[](https://docs.datapizza.ai/0.1.0/API%20Reference/Type/chunk/#datapizza.type.Chunk "datapizza.type.Chunk


  
      dataclass
  ")]`  |  The reranked documents.  |  
## Usage

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-1-1)from datapizza.modules.rerankers.cohere import CohereReranker
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-1-2)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-1-3)reranker = CohereReranker(
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-1-4)    api_key="your-cohere-api-key",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-1-5)    endpoint="https://api.cohere.ai/v1",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-1-6)    top_n=10,
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-1-7)    threshold=0.5,
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-1-8)    model="rerank-v3.5",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-1-9))
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-1-10)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-1-11)# Rerank chunks based on query
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-1-12)query = "What are the benefits of machine learning?"
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-1-13)reranked_chunks = reranker.rerank(query, chunks)

```

## Features
  * High-quality semantic reranking using Cohere's models
  * Configurable result count and score thresholds
  * Support for both sync and async processing
  * Automatic relevance scoring for retrieved content
  * Integration with Cohere's latest reranking models
  * Flexible endpoint configuration for different Cohere services


## Examples
### Basic Usage

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-1)import uuid
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-2)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-3)from datapizza.modules.rerankers.cohere import CohereReranker
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-4)from datapizza.type import Chunk
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-5)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-6)# Initialize reranker
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-7)reranker = CohereReranker(
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-8)    api_key="COHERE_API_KEY",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-9)    endpoint="https://api.cohere.ai/v1",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-10)    top_n=5,
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-11)    threshold=0.6,
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-12)    model="rerank-v3.5",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-13))
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-14)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-15)# Sample retrieved chunks
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-16)chunks = [
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-17)    Chunk(id=str(uuid.uuid4()), text="Machine learning enables computers to learn from data..."),
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-18)    Chunk(id=str(uuid.uuid4()), text="Deep learning is a subset of machine learning..."),
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-19)    Chunk(id=str(uuid.uuid4()), text="Neural networks consist of interconnected nodes..."),
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-20)    Chunk(id=str(uuid.uuid4()), text="Supervised learning uses labeled training data..."),
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-21)    Chunk(id=str(uuid.uuid4()), text="The weather forecast shows rain tomorrow...")
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-22)]
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-23)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-24)query = "What is deep learning and how does it work?"
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-25)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-26)# Rerank based on relevance to query
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-27)reranked_chunks = reranker.rerank(query, chunks)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-28)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-29)# Display results with scores
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-30)for i, chunk in enumerate(reranked_chunks):
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-31)    score = chunk.metadata.get('relevance_score', 'N/A')
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/#__codelineno-2-32)    print(f"Rank {i+1} (Score: {score}): {chunk.text[:80]}...")

```

Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
