---
source: https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/
---

[ Skip to content ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#functional-pipeline)
[ ![logo](https://docs.datapizza.ai/0.1.0/assets/logo.png) ](https://docs.datapizza.ai/0.1.0/ "Datapizza AI")
Datapizza AI 
0.1.0
  * [0.1.0](https://docs.datapizza.ai/0.1.0/)
  * [0.0.9](https://docs.datapizza.ai/0.0.9/)
  * [0.0.7](https://docs.datapizza.ai/0.0.7/)
  * [0.0.2](https://docs.datapizza.ai/0.0.2/)


Functional Pipeline 
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
      * Functional Pipeline  [ Functional Pipeline  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/) Table of contents 
        * [ Core Components  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#core-components)
          * [ Dependency  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#dependency)
          * [ FunctionalPipeline  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#functionalpipeline)
        * [ Building Pipelines  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#building-pipelines)
          * [ Sequential Execution  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#sequential-execution)
          * [ Branching  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#branching)
          * [ Foreach Loop  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#foreach-loop)
        * [ Executing Pipelines  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#executing-pipelines)
        * [ YAML Configuration  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#yaml-configuration)
        * [ Real-world Examples  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#real-world-examples)
          * [ Question Answering Pipeline  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#question-answering-pipeline)
          * [ Branch and loop usage example  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#branch-and-loop-usage-example)
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
  * [ Core Components  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#core-components)
    * [ Dependency  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#dependency)
    * [ FunctionalPipeline  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#functionalpipeline)
  * [ Building Pipelines  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#building-pipelines)
    * [ Sequential Execution  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#sequential-execution)
    * [ Branching  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#branching)
    * [ Foreach Loop  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#foreach-loop)
  * [ Executing Pipelines  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#executing-pipelines)
  * [ YAML Configuration  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#yaml-configuration)
  * [ Real-world Examples  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#real-world-examples)
    * [ Question Answering Pipeline  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#question-answering-pipeline)
    * [ Branch and loop usage example  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#branch-and-loop-usage-example)


  1. [ Home  ](https://docs.datapizza.ai/0.1.0/)
  2. [ Guides  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/quick_start/)
  3. [ Pipeline  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/)


# Functional Pipeline
> **_WARNING:_** This module is in beta. Signatures and interfaces may change in future releases.
The `FunctionalPipeline` module provides a flexible way to build data processing pipelines with complex dependency graphs. It allows you to define reusable processing nodes and connect them in various patterns including sequential execution, branching, parallel execution, and foreach loops.
## Core Components
### Dependency
Defines how data flows between [Nodes](https://docs.datapizza.ai/0.1.0/API%20Reference/Type/node/):

```
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-0-1)@dataclass
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-0-2)class Dependency:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-0-3)    node_name: str
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-0-4)    input_key: str | None = None
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-0-5)    target_key: str | None = None

```

  * `node_name`: The name of the node to get data from
  * `input_key`: Optional key for extracting a specific part of the node's output
  * `target_key`: The key under which to store the data in the receiving node's input


### FunctionalPipeline
The main class for building and executing pipelines:

```
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-1-1)class FunctionalPipeline:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-1-2)    def __init__(self):
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-1-3)        self.nodes = []

```

## Building Pipelines
### Sequential Execution

```
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-2-1)pipeline = FunctionalPipeline()
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-2-2)pipeline.run("load_data", DataLoader(), kwargs={"filepath": "data.csv"})
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-2-3)pipeline.then("transform", Transformer(), target_key="data")
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-2-4)pipeline.then("save", Saver(), target_key="transformed_data")

```

### Branching

```
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-3-1)pipeline.branch(
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-3-2)    condition=is_valid_data,
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-3-3)    if_true=valid_data_pipeline,
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-3-4)    if_false=invalid_data_pipeline,
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-3-5)    dependencies=[Dependency(node_name="validate", target_key="validation_result")]
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-3-6))

```

### Foreach Loop

```
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-4-1)pipeline.foreach(
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-4-2)    name="process_items",
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-4-3)    do=item_processing_pipeline,
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-4-4)    dependencies=[Dependency(node_name="get_items")]
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-4-5))

```

## Executing Pipelines

```
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-5-1)result = pipeline.execute(
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-5-2)    initial_data={"load_data": {"filepath": "override.csv"}},
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-5-3)    context={"existing_data": {...}}
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-5-4))

```

## YAML Configuration
You can define pipelines in YAML and load them at runtime: This is useful for separating pipeline structure from code

```
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-6-1)modules:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-6-2)  - name: data_loader
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-6-3)    module: my_package.loaders
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-6-4)    type: CSVLoader
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-6-5)    params:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-6-6)      encoding: "utf-8"
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-6-7)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-6-8)  - name: transformer
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-6-9)    module: my_package.transformers
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-6-10)    type: StandardTransformer
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-6-11)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-6-12)pipeline:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-6-13)  - type: run
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-6-14)    name: load_data
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-6-15)    node: data_loader
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-6-16)    kwargs:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-6-17)      filepath: "data.csv"
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-6-18)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-6-19)  - type: then
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-6-20)    name: transform
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-6-21)    node: transformer
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-6-22)    target_key: data

```

Load the pipeline:

```
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-7-1)pipeline = FunctionalPipeline.from_yaml("pipeline_config.yaml")
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-7-2)result = pipeline.execute()

```

## Real-world Examples
### Question Answering Pipeline
Here's an example of a question answering pipeline that uses embeddings to retrieve relevant information and an LLM to generate a response:
Define the components: 

```
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-1)from datapizza.clients.google import GoogleClient
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-2)from datapizza.clients.openai import OpenAIClient
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-3)from datapizza.core.vectorstore import VectorConfig
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-4)from datapizza.embedders.openai import OpenAIEmbedder
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-5)from datapizza.modules.prompt import ChatPromptTemplate
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-6)from datapizza.modules.rewriters import ToolRewriter
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-7)from datapizza.pipeline import Dependency, FunctionalPipeline
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-8)from datapizza.vectorstores.qdrant import QdrantVectorstore
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-9)from dotenv import load_dotenv
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-10)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-11)load_dotenv()
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-12)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-13)rewriter = ToolRewriter(
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-14)    client=OpenAIClient(
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-15)        model="gpt-4o",
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-16)        api_key=os.getenv("OPENAI_API_KEY"),
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-17)        system_prompt="Use only 1 time the tool to answer the user prompt.",
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-18)    )
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-19))
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-20)embedder = OpenAIEmbedder(
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-21)    api_key=os.getenv("OPENAI_API_KEY"), model_name="text-embedding-3-small"
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-22))
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-23)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-24)vector_store = QdrantVectorstore(host="localhost", port=6333)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-25)vector_store.create_collection(collection_name="my_documents", vector_config=[VectorConfig(dimensions=1536, name="vector_name")])
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-26)vector_store = vector_store.as_module_component() # required to use the vectorstore in the pipeline
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-27)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-28)prompt_template = ChatPromptTemplate(
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-29)    user_prompt_template="this is a user prompt: {{ user_prompt }}",
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-30)    retrieval_prompt_template="{% for chunk in chunks %} Relevant chunk: {{ chunk.text }} \n\n {% endfor %}",
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-31))
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-32)generator = GoogleClient(
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-33)    api_key=os.getenv("GOOGLE_API_KEY"),
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-34)    system_prompt="You are a senior Software Engineer. You are given a user prompt and you need to answer it given the context of the chunks.",
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-8-35)).as_module_component()

```

And now create and execute the pipeline

```
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-9-1)pipeline = (FunctionalPipeline()
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-9-2)    .run(name="rewriter", node=rewriter, kwargs={"user_prompt": "tell me something about this document"})
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-9-3)    .then(name="embedder", node=embedder, target_key="text")
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-9-4)    .then(name="vector_store", node=vector_store, target_key="query_vector",
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-9-5)          kwargs={"collection_name": "my_documents", "k": 4})
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-9-6)    .then(name="prompt_template", node=prompt_template, target_key="chunks" , kwargs={"user_prompt": "tell me something about this document"})
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-9-7)    .then(name="generator", node=generator, target_key="memory", kwargs={"input": "tell me something about this document"})
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-9-8)    .get("generator")
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-9-9))
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-9-10)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-9-11)result = pipeline.execute()
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-9-12)print(result)

```

When using `.then()`, the `target_key` parameter specifies the input parameter name for the current node's `run()` method that will receive the output from the previous node. In other words, `target_key` defines how the previous node's output gets mapped into the current node's `run()` method parameters.
This pipeline:
  1. [Rewrites/processes](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/rewriters/) the user query
  2. [Creates embeddings](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/) from the processed query
  3. Retrieves relevant chunks from a [vector database](https://docs.datapizza.ai/0.1.0/API%20Reference/Vectorstore/qdrant_vectorstore/)
  4. [Creates a prompt template](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Prompt/ChatPromptTemplate/) with the retrieved context
  5. Generates a response using an LLM
  6. Returns the generated response


### Branch and loop usage example

```
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-1)from datapizza.core.models import PipelineComponent
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-2)from datapizza.pipeline import Dependency, FunctionalPipeline
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-3)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-4)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-5)class Scraper(PipelineComponent):
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-6)    def _run(self, number_of_links: int = 1):
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-7)        return ["example.com"] * number_of_links
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-8)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-9)class UpperComponent(PipelineComponent):
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-10)    def _run(self, item):
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-11)        return item.upper()
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-12)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-13)class SendNotification(PipelineComponent):
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-14)    def _run(self ):
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-15)        return "No Url found, Notification sent"
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-16)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-17)send_notification = FunctionalPipeline().run(name="send_notification", node=SendNotification())
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-18)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-19)upper_elements = FunctionalPipeline().foreach(
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-20)    name="loop_links",
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-21)    dependencies=[Dependency(node_name="get_link")],
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-22)    do=UpperComponent(),
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-23))
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-24)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-25)pipeline = (
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-26)    FunctionalPipeline()
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-27)    .run(name="get_link", node=Scraper())
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-28)    .branch(
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-29)        condition=lambda pipeline_context: len(pipeline_context.get("get_link")) > 0,
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-30)        dependencies=[Dependency(node_name="get_link")],
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-31)        if_true=upper_elements,
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-32)        if_false=send_notification,
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-33)    )
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-34))
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-35)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-36)results = pipeline.execute(initial_data={"get_link": {"number_of_links": 0}}) # put 1 to test the other branch
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/functional_pipeline/#__codelineno-10-37)print(results)

```

Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
