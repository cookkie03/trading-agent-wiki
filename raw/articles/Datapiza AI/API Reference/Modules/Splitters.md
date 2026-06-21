---
source: https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/
---

[ Skip to content ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/#splitters)
[ ![logo](https://docs.datapizza.ai/0.1.0/assets/logo.png) ](https://docs.datapizza.ai/0.1.0/ "Datapizza AI")
Datapizza AI 
0.1.0
  * [0.1.0](https://docs.datapizza.ai/0.1.0/)
  * [0.0.9](https://docs.datapizza.ai/0.0.9/)
  * [0.0.7](https://docs.datapizza.ai/0.0.7/)
  * [0.0.2](https://docs.datapizza.ai/0.0.2/)


Splitters 
Initializing search 
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
  * [ Installation  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/#installation)
  * [ Available Splitters  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/#available-splitters)
    * [ Core Splitters (Included by Default)  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/#core-splitters-included-by-default)
  * [ Common Features  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/#common-features)
  * [ Usage Patterns  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/#usage-patterns)
    * [ Basic Text Splitting  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/#basic-text-splitting)
    * [ Document Processing Pipeline  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/#document-processing-pipeline)
    * [ Choosing the Right Splitter  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/#choosing-the-right-splitter)


  1. [ Home  ](https://docs.datapizza.ai/0.1.0/)
  2. [ API Reference  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/clients/)
  3. [ Modules  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/)
  4. [ Splitters  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/recursive_splitter/)


# Splitters
Splitters are pipeline components that divide large text content into smaller, manageable chunks. They help optimize content for processing, storage, and retrieval in AI applications by creating appropriately sized segments while preserving context and meaning.
## Installation
All splitters are included with `datapizza-ai-core` and require no additional installation.
## Available Splitters
### Core Splitters (Included by Default)
  * [RecursiveSplitter](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/recursive_splitter/) - Recursively divides text using multiple splitting strategies
  * [TextSplitter](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/text_splitter/) - Basic text splitter for general-purpose chunking
  * [NodeSplitter](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/node_splitter/) - Splitter for Node objects preserving hierarchical structure
  * [PDFImageSplitter](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/) - Specialized splitter for PDF content with images


## Common Features
  * Multiple splitting strategies for different content types
  * Configurable chunk sizes and overlap
  * Context preservation through overlapping
  * Support for structured content (nodes, PDFs, etc.)
  * Metadata preservation during splitting
  * Spatial layout awareness for document content


## Usage Patterns
### Basic Text Splitting

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/#__codelineno-0-1)from datapizza.modules.splitters import RecursiveSplitter
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/#__codelineno-0-2)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/#__codelineno-0-3)splitter = RecursiveSplitter(chunk_size=1000, chunk_overlap=200)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/#__codelineno-0-4)chunks = splitter(long_text_content)

```

### Document Processing Pipeline

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/#__codelineno-1-1)from datapizza.modules.parsers import TextParser
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/#__codelineno-1-2)from datapizza.modules.splitters import NodeSplitter
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/#__codelineno-1-3)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/#__codelineno-1-4)parser = TextParser()
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/#__codelineno-1-5)splitter = NodeSplitter(max_char = 4000)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/#__codelineno-1-6)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/#__codelineno-1-7)document = parser.parse(text_content)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/#__codelineno-1-8)structured_chunks = splitter(document)

```

### Choosing the Right Splitter
  * **RecursiveSplitter** : Best for general text content, articles, and most use cases
  * **TextSplitter** : Simple splitting for basic text without complex requirements
  * **NodeSplitter** : When working with structured Node objects from parsers
  * **PDFImageSplitter** : Specifically for PDF content with images and complex layouts
  * **BBoxMerger** : Utility for processing documents with spatial layout information


Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
