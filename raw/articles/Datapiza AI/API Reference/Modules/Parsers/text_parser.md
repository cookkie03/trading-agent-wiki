---
source: https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Parsers/text_parser/
---

[ Skip to content ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#togetherreranker)
[ ![logo](https://docs.datapizza.ai/0.1.0/assets/logo.png) ](https://docs.datapizza.ai/0.1.0/ "Datapizza AI")
Datapizza AI 
0.1.0
  * [0.1.0](https://docs.datapizza.ai/0.1.0/)
  * [0.0.9](https://docs.datapizza.ai/0.0.9/)
  * [0.0.7](https://docs.datapizza.ai/0.0.7/)
  * [0.0.2](https://docs.datapizza.ai/0.0.2/)


TogetherReranker 
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
        * [ CohereReranker  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/)
        * TogetherReranker  [ TogetherReranker  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/) Table of contents 
          * [ Installation  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#installation)
          * [ TogetherReranker  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#datapizza.modules.rerankers.together.TogetherReranker)
            * [ __init__  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#datapizza.modules.rerankers.together.TogetherReranker.__init__)
            * [ rerank  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#datapizza.modules.rerankers.together.TogetherReranker.rerank)
          * [ Usage  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#usage)
          * [ Features  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#features)
          * [ Available Models  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#available-models)
          * [ Examples  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#examples)
            * [ Basic Usage  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#basic-usage)
      * Prompt  Prompt 
        * [ ChatPromptTemplate  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Prompt/ChatPromptTemplate/)
    * Tools  Tools 
      * [ MCPClient  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Tools/mcp/)
      * [ DuckDuckGo  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Tools/duckduckgo/)
      * [ FileSystem  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Tools/filesystem/)
      * [ SQLDatabase  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Tools/SQLDatabase/)
      * [ WebFetch  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Tools/web_fetch/)


Table of contents 
  * [ Installation  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#installation)
  * [ TogetherReranker  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#datapizza.modules.rerankers.together.TogetherReranker)
    * [ __init__  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#datapizza.modules.rerankers.together.TogetherReranker.__init__)
    * [ rerank  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#datapizza.modules.rerankers.together.TogetherReranker.rerank)
  * [ Usage  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#usage)
  * [ Features  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#features)
  * [ Available Models  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#available-models)
  * [ Examples  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#examples)
    * [ Basic Usage  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#basic-usage)


  1. [ Home  ](https://docs.datapizza.ai/0.1.0/)
  2. [ API Reference  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/clients/)
  3. [ Modules  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/)
  4. [ Rerankers  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/cohere_reranker/)


# TogetherReranker
A reranker that uses Together AI's API for document reranking with various model options.
## Installation

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-0-1)pip install datapizza-ai-rerankers-together

```

##  datapizza.modules.rerankers.together.TogetherReranker
Bases: `Reranker`
A reranker that uses the Together API to rerank documents.
###  __init__

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-0-1)__init__(api_key, model, top_n=10, threshold=None)

```

Initialize the TogetherReranker.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `api_key`  |  `str`  |  Together API key  |  _required_  |  
|  `model`  |  `str`  |  Model name to use for reranking  |  _required_  |  
|  `top_n`  |  `int`  |  Number of top documents to return  |  `10`  |  
|  `threshold`  |  `Optional[float]`  |  Minimum relevance score threshold. If None, no filtering is applied.  |  `None`  |  
###  rerank

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-0-1)rerank(query, documents)

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
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-1-1)from datapizza.modules.rerankers.together import TogetherReranker
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-1-2)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-1-3)reranker = TogetherReranker(
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-1-4)    api_key="your-together-api-key",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-1-5)    model="sentence-transformers/msmarco-bert-base-dot-v5",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-1-6)    top_n=15,
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-1-7)    threshold=0.3
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-1-8))
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-1-9)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-1-10)# Rerank documents
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-1-11)query = "How to implement neural networks?"
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-1-12)reranked_results = reranker.rerank(query, document_chunks)

```

## Features
  * Access to multiple reranking model options
  * Flexible model selection for different use cases
  * Score-based filtering with configurable thresholds
  * Support for various domain-specific models
  * Integration with Together AI's model ecosystem
  * Automatic model initialization and management


## Available Models
Common reranking models available through Together AI:
  * `sentence-transformers/msmarco-bert-base-dot-v5`
  * `sentence-transformers/all-MiniLM-L6-v2`
  * `sentence-transformers/all-mpnet-base-v2`
  * Custom fine-tuned models for specific domains


## Examples
### Basic Usage

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-1)import uuid
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-2)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-3)from datapizza.modules.rerankers.together import TogetherReranker
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-4)from datapizza.type import Chunk
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-5)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-6)# Initialize with specific model
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-7)reranker = TogetherReranker(
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-8)    api_key="TOGETHER_API_KEY",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-9)    model="Salesforce/Llama-Rank-V1",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-10)    top_n=10,
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-11)    threshold=0.4
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-12))
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-13)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-14)# Sample chunks
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-15)chunks = [
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-16)    Chunk(id=str(uuid.uuid4()), text="Neural networks are computational models inspired by biological brains..."),
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-17)    Chunk(id=str(uuid.uuid4()), text="Deep learning uses multiple layers to learn complex patterns..."),
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-18)    Chunk(id=str(uuid.uuid4()), text="Backpropagation is the algorithm used to train neural networks..."),
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-19)    Chunk(id=str(uuid.uuid4()), text="The weather is sunny today with mild temperatures..."),
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-20)    Chunk(id=str(uuid.uuid4()), text="Convolutional neural networks excel at image recognition tasks...")
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-21)]
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-22)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-23)query = "How do neural networks learn?"
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-24)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-25)# Rerank based on relevance
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-26)reranked_results = reranker.rerank(query, chunks)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-27)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-28)# Display results
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-29)for i, chunk in enumerate(reranked_results):
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-30)    score = chunk.metadata.get('relevance_score', 'N/A')
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Rerankers/together_reranker/#__codelineno-2-31)    print(f"Rank {i+1} (Score: {score}): {chunk.text[:70]}...")

```

Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
