---
source: https://docs.datapizza.ai/0.1.0/API%20Reference/Tools/filesystem/
---

[ Skip to content ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#ingestion-pipeline)
[ ![logo](https://docs.datapizza.ai/0.1.0/assets/logo.png) ](https://docs.datapizza.ai/0.1.0/ "Datapizza AI")
Datapizza AI 
0.1.0
  * [0.1.0](https://docs.datapizza.ai/0.1.0/)
  * [0.0.9](https://docs.datapizza.ai/0.0.9/)
  * [0.0.7](https://docs.datapizza.ai/0.0.7/)
  * [0.0.2](https://docs.datapizza.ai/0.0.2/)


Ingestion Pipeline 
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
      * Ingestion Pipeline  [ Ingestion Pipeline  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/) Table of contents 
        * [ Core Concepts  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#core-concepts)
        * [ Available Components  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#available-components)
        * [ Configuration Methods  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#configuration-methods)
          * [ 1. Programmatic Configuration  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#1-programmatic-configuration)
          * [ 2. YAML Configuration  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#2-yaml-configuration)
            * [ Example YAML Configuration (config.yaml)  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#example-yaml-configuration-configyaml)
        * [ Pipeline Execution (run method)  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#pipeline-execution-run-method)
          * [ Async Execution (a_run method)  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#async-execution-a_run-method)
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
  * [ Core Concepts  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#core-concepts)
  * [ Available Components  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#available-components)
  * [ Configuration Methods  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#configuration-methods)
    * [ 1. Programmatic Configuration  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#1-programmatic-configuration)
    * [ 2. YAML Configuration  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#2-yaml-configuration)
      * [ Example YAML Configuration (config.yaml)  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#example-yaml-configuration-configyaml)
  * [ Pipeline Execution (run method)  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#pipeline-execution-run-method)
    * [ Async Execution (a_run method)  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#async-execution-a_run-method)


  1. [ Home  ](https://docs.datapizza.ai/0.1.0/)
  2. [ Guides  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/quick_start/)
  3. [ Pipeline  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/)


# Ingestion Pipeline
The `IngestionPipeline` provides a streamlined way to process documents, transform them into nodes (chunks of text with metadata), generate embeddings, and optionally store them in a vector database. It allows chaining various components like parsers, captioners, splitters, and embedders to create a customizable document processing workflow.
## Core Concepts
  * **Components** : These are the processing steps in the pipeline, typically inheriting from `datapizza.core.models.PipelineComponent`. Each component implements a `_run` method to perform a specific task like parsing a document, splitting text, or generating embeddings. Components are executed sequentially via their `__call__` method in the order they are provided.
  * **Vector Store** : An optional component responsible for storing the final nodes and their embeddings.
  * **Nodes** : The fundamental unit of data passed between components. A node usually represents a chunk of text (e.g., a paragraph, a table summary) along with its associated metadata and embeddings.


## Available Components
The pipeline typically supports components for:
  1. [**Parsers**](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Parsers/): Convert raw documents (PDF, DOCX, etc.) into structured `Node` objects (e.g., `AzureParser`, `UnstructuredParser`).
  2. [**Captioners**](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/captioners/): Enhance nodes representing images or tables with textual descriptions using models like LLMs (e.g., `LLMCaptioner`).
  3. [**Splitters**](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/): Divide nodes into smaller chunks based on their content (e.g., `NodeSplitter`, `PdfImageSplitter`).
  4. [**Embedders**](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/openai_embedder/): Create chunk embeddings for semantic search and similarity matching (e.g., `NodeEmbedder`, `ClientEmbedder`).
     * [`ChunkEmbedder`](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/): Batch processing for efficient embedding of multiple nodes.
  5. [**Vector Stores**](https://docs.datapizza.ai/0.1.0/API%20Reference/Vectorstore/qdrant_vectorstore/): Store and retrieve embeddings efficiently using vector databases (e.g., `QdrantVectorstore`).


Refer to the specific documentation for each component type (e.g., in `datapizza.parsers`, `datapizza.embedders`) for details on their specific parameters and usage. Remember that pipeline components typically inherit from `PipelineComponent` and implement the `_run` method.
## Configuration Methods
There are two main ways to configure and use the `IngestionPipeline`:
### 1. Programmatic Configuration
Define and configure the pipeline directly within your Python code. This offers maximum flexibility.

```
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-1)from datapizza.clients.openai import OpenAIClient
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-2)from datapizza.core.vectorstore import VectorConfig
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-3)from datapizza.embedders import ChunkEmbedder
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-4)from datapizza.modules.parsers.docling import DoclingParser
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-5)from datapizza.modules.splitters import NodeSplitter
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-6)from datapizza.pipeline.pipeline import IngestionPipeline
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-7)from datapizza.vectorstores.qdrant import QdrantVectorstore
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-8)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-9)vector_store = QdrantVectorstore(
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-10)    location=":memory:" # or set host and port
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-11))
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-12)vector_store.create_collection(collection_name="datapizza", vector_config=[VectorConfig(dimensions=1536, name="vector_name")])
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-13)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-14)pipeline = IngestionPipeline(
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-15)    modules=[
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-16)        DoclingParser(),
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-17)        NodeSplitter(max_char=2000),
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-18)        ChunkEmbedder(client=OpenAIClient(api_key="OPENAI_API_KEY", model="text-embedding-3-small"), model_name="text-embedding-3-small", embedding_name="small"),
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-19)    ],
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-20)    vector_store=vector_store,
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-21)    collection_name="datapizza",
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-22))
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-23)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-24)pipeline.run(file_path="sample.pdf")
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-25)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-0-26)print(vector_store.search(query_vector= [0.0]*1536, collection_name="datapizza", k=4))

```

### 2. YAML Configuration
Define the entire pipeline structure, components, and their parameters in a YAML file. This is useful for managing configurations separately from code.

```
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-1-1)from datapizza.pipeline.pipeline import IngestionPipeline
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-1-2)import os
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-1-3)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-1-4)# Load pipeline from YAML
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-1-5)pipeline = IngestionPipeline().from_yaml("path/to/your/config.yaml")
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-1-6)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-1-7)# Run the pipeline (Ensure necessary ENV VARS for the YAML config are set)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-1-8)pipeline.run(file_path="path/to/your/document.pdf")

```

#### Example YAML Configuration (`config.yaml`)

```
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-1)constants:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-2)  EMBEDDING_MODEL: "text-embedding-3-small"
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-3)  CHUNK_SIZE: 1000
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-4)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-5)elements:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-6)  my_custom_splitter:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-7)    type: TextSplitter
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-8)    module: datapizza.modules.splitters
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-9)    params:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-10)      max_char: 1500
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-11)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-12)ingestion_pipeline:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-13)  clients:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-14)    openai_embedder:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-15)      provider: openai
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-16)      model: "${EMBEDDING_MODEL}"
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-17)      api_key: "${OPENAI_API_KEY}"
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-18)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-19)  modules:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-20)    - name: parser
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-21)      type: DoclingParser
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-22)      module: datapizza.modules.parsers.docling
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-23)    - name: splitter
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-24)      type: NodeSplitter
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-25)      module: datapizza.modules.splitters
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-26)      params:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-27)        max_char: ${CHUNK_SIZE}
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-28)    - name: embedder
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-29)      type: ChunkEmbedder
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-30)      module: datapizza.embedders
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-31)      params:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-32)        client: openai_embedder
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-33)    - name: custom_processor
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-34)      type: MyCustomProcessor
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-35)      module: my_project.processors
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-36)      params:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-37)        splitter: "${my_custom_splitter}"
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-38)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-39)  vector_store:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-40)    type: QdrantVectorstore
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-41)    module: datapizza.vectorstores.qdrant
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-42)    params:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-43)      host: "localhost"
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-44)      port: 6333
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-45)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-2-46)  collection_name: "my_documents"

```

**Key points for YAML configuration:**
  * **Constants** : Define string values under `constants` that can be referenced using `${CONST_NAME}` syntax.
  * **Environment Variables** : Use `${VAR_NAME}` syntax within strings to securely load secrets or configuration from environment variables. Ensure these variables are set in your execution environment.
  * **Elements** : Define reusable component instances under `elements`. Each element requires `type` (class name) and `module` (Python path). Optional `params` are passed to the constructor. Reference them in module `params` using `"${element_name}"` syntax. Unlike constants (simple string substitution), elements are fully instantiated Python objects.
  * ~~**Clients** ~~ (Obsoleted, use Elements instead): Define shared clients (like `OpenAIClient`) under the `clients` key and reference them by name within module `params`. Clients are specifically for LLM/API clients created via `ClientFactory`.
  * **Modules** : List components under `modules`. Each requires `type` (class name) and `module` (Python path to the class). `params` are passed to the component's constructor (`__init__`). Components should generally inherit from `PipelineComponent`.
  * **Vector Store** : Configure the optional vector store similarly to modules.
  * **Collection Name** : Must be provided if a `vector_store` is configured.


## Pipeline Execution (`run` method)

```
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-3-1)pipeline.run(file_path=f, metadata={"name": f, "type": "md"})

```

### Async Execution (`a_run` method)
IngestionPipeline support async run _NB:_ Every modules should implement `_a_run` method to run the async pipeline.

```
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/#__codelineno-4-1)await pipeline.a_run(file_path=f, metadata={"name": f, "type": "md"})

```

Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
