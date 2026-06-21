---
source: https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/recursive_splitter/
---

[ Skip to content ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#dagpipeline)
[ ![logo](https://docs.datapizza.ai/0.1.0/assets/logo.png) ](https://docs.datapizza.ai/0.1.0/ "Datapizza AI")
Datapizza AI 
0.1.0
  * [0.1.0](https://docs.datapizza.ai/0.1.0/)
  * [0.0.9](https://docs.datapizza.ai/0.0.9/)
  * [0.0.7](https://docs.datapizza.ai/0.0.7/)
  * [0.0.2](https://docs.datapizza.ai/0.0.2/)


DagPipeline 
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
      * DagPipeline  [ DagPipeline  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/) Table of contents 
        * [ Core Concepts  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#core-concepts)
          * [ Modules  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#modules)
          * [ Connections  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#connections)
        * [ Running the Pipeline  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#running-the-pipeline)
          * [ Async run  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#async-run)
        * [ Configuration via YAML  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#configuration-via-yaml)
          * [ Example YAML (dag_config.yaml)  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#example-yaml-dag_configyaml)
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
  * [ Core Concepts  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#core-concepts)
    * [ Modules  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#modules)
    * [ Connections  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#connections)
  * [ Running the Pipeline  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#running-the-pipeline)
    * [ Async run  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#async-run)
  * [ Configuration via YAML  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#configuration-via-yaml)
    * [ Example YAML (dag_config.yaml)  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#example-yaml-dag_configyaml)


  1. [ Home  ](https://docs.datapizza.ai/0.1.0/)
  2. [ Guides  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/quick_start/)
  3. [ Pipeline  ](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/ingestion_pipeline/)


# DagPipeline
The `DagPipeline` class allows you to define and execute a series of processing steps (modules) organized as a Directed Acyclic Graph (DAG). Modules typically inherit from `datapizza.core.models.PipelineComponent` or are simple callables. This enables complex workflows where the output of one module can be selectively used as input for others.
## Core Concepts
### Modules
Modules are the building blocks of the pipeline. They are typically instances of classes inheriting from `datapizza.core.models.PipelineComponent` (which requires implementing a `run` and `a_run` method), `datapizza.core.models.ChainableProducer` (which exposes an `as_module_component` method returning a `PipelineComponent`), or simply Python callables.

```
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-0-1)from datapizza.core.models import PipelineComponent
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-0-2)from datapizza.pipeline import DagPipeline
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-0-3)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-0-4)class MyProcessingStep(PipelineComponent):
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-0-5)    # Inheriting from PipelineComponent provides the __call__ wrapper for logging
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-0-6)    def _run(self, input_data: str) -> str:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-0-7)        return something
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-0-8)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-0-9)    async _a_run(self, something: str) -> str:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-0-10)        return await do_stuff()

```

### Connections
Connections define the flow of data between modules. You specify which module's output connects to which module's input.
  * **`from_node_name`**: The name of the source module.
  * **`to_node_name`**: The name of the target module.
  * **`source_key`**(Optional): If the source module's`process` method (or callable) returns a dictionary, this key specifies which value from the dictionary should be passed. If `None`, the entire output of the source module is passed.
  * **`target_key`**: This key specifies the argument name in the target module's`process` method (or callable) that should receive the data. If `None`, and the source output is _not_ a dictionary, the data is passed as the first non-`self` argument to the target's `_run` method/callable. If `None` and the source output _is_ a dictionary, its key-value pairs are merged into the target's input keyword arguments.



```
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-1)from datapizza.clients.openai import OpenAIClient
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-2)from datapizza.core.models import PipelineComponent
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-3)from datapizza.core.vectorstore import VectorConfig
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-4)from datapizza.embedders.openai import OpenAIEmbedder
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-5)from datapizza.modules.prompt import ChatPromptTemplate
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-6)from datapizza.modules.rewriters import ToolRewriter
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-7)from datapizza.pipeline import DagPipeline
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-8)from datapizza.vectorstores.qdrant import QdrantVectorstore
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-9)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-10)client = OpenAIClient(api_key="OPENAI_API_KEY", model="gpt-4o-mini")
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-11)vector_store = QdrantVectorstore(location=":memory:")
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-12)vector_store.create_collection(collection_name="my_documents", vector_config=[VectorConfig(dimensions=1536, name="vector_name")])
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-13)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-14)pipeline = DagPipeline()
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-15)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-16)pipeline.add_module("rewriter", ToolRewriter(client=client, system_prompt="rewrite the query to perform a better search in a vector database"))
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-17)pipeline.add_module("embedder", OpenAIEmbedder(api_key="OPENAI_API_KEY", model_name="text-embedding-3-small"))
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-18)pipeline.add_module("vector_store", vector_store)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-19)pipeline.add_module("prompt_template", ChatPromptTemplate(user_prompt_template = "this is a user prompt: {{ user_prompt }}", retrieval_prompt_template = "{% for chunk in chunks %} Relevant chunk: {{ chunk.text }} \n\n {% endfor %}"))
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-20)pipeline.add_module("llm", OpenAIClient(model = "gpt-4o-mini", api_key = "OPENAI_API_KEY"))
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-21)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-22)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-23)pipeline.connect("rewriter", "embedder", target_key="text")
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-24)pipeline.connect("embedder", "vector_store", target_key="query_vector")
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-25)pipeline.connect("vector_store", "prompt_template", target_key="chunks")
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-1-26)pipeline.connect("prompt_template", "llm", target_key="memory")

```

## Running the Pipeline
The `run` method executes the pipeline based on the defined connections. It requires an initial `data` dictionary which provides the missing input arguments for the nodes that require them.
The keys of this dictionary should match the names of the modules requiring initial input, and the values should be dictionaries mapping argument names to values for their respective `process` methods (or callables).

```
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-2-1)user_input = "tell me something about this document"
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-2-2)res = pipeline.run(
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-2-3)    {
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-2-4)        "rewriter": {"user_prompt": user_input},
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-2-5)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-2-6)        # Embedder doesn't require any input because it's provided by the rewriter
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-2-7)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-2-8)        "prompt_template": {"user_prompt": user_input},  # Prompt template requires user_prompt
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-2-9)        "vector_store": {
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-2-10)            "collection_name": "my_documents",
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-2-11)            "k": 10,
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-2-12)        },
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-2-13)        "llm": {
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-2-14)            "input": user_input,
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-2-15)            "system_prompt": "You are a helpful assistant. try to answer user questions given the context",
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-2-16)        },
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-2-17)    }
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-2-18))
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-2-19)result = res.get("llm").text
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-2-20)print(result)

```

The pipeline automatically determines the execution order based on dependencies. It executes modules by calling their `run` method only when all their prerequisites (connected `from_node_name` modules) have completed successfully.
### Async run
Pipeline support async run with `a_run` With async run, the pipeline will call a_run of modules.
This only works if you are using a remote qdrant server. The in-memory qdrant function does not work with asynchronous execution. 

```
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-3-1)res = await pipeline.a_run(
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-3-2)    {
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-3-3)        "rewriter": {"user_prompt": user_input},
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-3-4)        "prompt_template": {"user_prompt": user_input},
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-3-5)        "vector_store": {
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-3-6)            "collection_name": "datapizza",
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-3-7)            "k": 10,
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-3-8)        },
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-3-9)        "llm": {
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-3-10)            "input": user_input,
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-3-11)            "system_prompt": "You are a helpful assistant. try to answer user questions given the context",
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-3-12)        },
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-3-13)    }
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-3-14))

```

## Configuration via YAML
Pipelines can be defined entirely using a YAML configuration file, which is loaded using the `from_yaml` method. This is useful for separating pipeline structure from code.
The YAML structure includes sections for `clients` (like LLM providers), `modules`, and `connections`.

```
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-4-1)from datapizza.pipeline import DagPipeline
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-4-2)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-4-3)pipeline = DagPipeline().from_yaml("dag_pipeline.yaml")
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-4-4)user_input = "tell me something about this document"
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-4-5)res = pipeline.run(
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-4-6)    {
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-4-7)        "rewriter": {"user_prompt": user_input},
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-4-8)        "prompt_template": {"user_prompt": user_input},
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-4-9)        "vector_store": {"collection_name": "my_documents","k": 10,},
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-4-10)        "llm": {"input": user_input,"system_prompt": "You are a helpful assistant. try to answer user questions given the context",},
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-4-11)    }
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-4-12))
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-4-13)result = res.get("llm").text
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-4-14)print(result)

```

### Example YAML (`dag_config.yaml`)

```
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-1)dag_pipeline:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-2)  clients:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-3)    openai_client:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-4)      provider: openai
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-5)      model: "gpt-4o-mini"
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-6)      api_key: ${OPENAI_API_KEY}
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-7)    google_client:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-8)      provider: google
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-9)      model: "gemini-2.0"
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-10)      api_key: ${GOOGLE_API_KEY}
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-11)    openai_embedder:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-12)      provider: openai
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-13)      model: "text-embedding-3-small"
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-14)      api_key: ${OPENAI_API_KEY}
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-15)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-16)  modules:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-17)    - name: rewriter
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-18)      type: ToolRewriter
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-19)      module: datapizza.modules.rewriters
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-20)      params:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-21)        client: openai_client
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-22)        system_prompt: "rewrite the query to perform a better search in a vector database"
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-23)    - name: embedder
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-24)      type: ClientEmbedder
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-25)      module: datapizza.embedders
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-26)      params:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-27)        client: openai_embedder
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-28)    - name: vector_store
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-29)      type: QdrantVectorstore
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-30)      module: datapizza.vectorstores.qdrant
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-31)      params:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-32)        host: localhost
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-33)    - name: prompt_template
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-34)      type: ChatPromptTemplate
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-35)      module: datapizza.modules.prompt
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-36)      params:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-37)        user_prompt_template: "this is a user prompt: {{ user_prompt }}"
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-38)        retrieval_prompt_template: "{% for chunk in chunks %} Relevant chunk: {{ chunk.text }} \n\n {% endfor %}"
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-39)    - name: llm
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-40)      type: OpenAIClient
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-41)      module: datapizza.clients.openai
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-42)      params:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-43)        model: "gpt-4o-mini"
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-44)        api_key: ${OPENAI_API_KEY}
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-45)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-46)  connections:
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-47)
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-48)    - from: rewriter
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-49)      to: embedder
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-50)      target_key: text
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-51)    - from: embedder
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-52)      to: vector_store
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-53)      target_key: query_vector
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-54)    - from: vector_store
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-55)      to: prompt_template
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-56)      target_key: chunks
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-57)    - from: prompt_template
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-58)      to: llm
[](https://docs.datapizza.ai/0.1.0/Guides/Pipeline/retrieval_pipeline/#__codelineno-5-59)      target_key: memory

```

**Key points for YAML configuration:**
  * **Environment Variables** : Use `${VAR_NAME}` syntax to load sensitive information like API keys from environment variables.
  * **Clients** : Define clients once and reference them by name in module `params`.
  * **Module Loading** : Specify the `module` path and `type` (class name) for dynamic loading. The class should generally be a `PipelineComponent`.
  * **Parameters** : `params` are passed directly to the module's constructor.
  * **Connections** : Define data flow similarly to the programmatic `connect` method.


Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
