---
source: https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/client_factory/
---

[ Skip to content ](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#tracing)
[ ![logo](https://docs.datapizza.ai/0.1.0/assets/logo.png) ](https://docs.datapizza.ai/0.1.0/ "Datapizza AI")
Datapizza AI 
0.1.0
  * [0.1.0](https://docs.datapizza.ai/0.1.0/)
  * [0.0.9](https://docs.datapizza.ai/0.0.9/)
  * [0.0.7](https://docs.datapizza.ai/0.0.7/)
  * [0.0.2](https://docs.datapizza.ai/0.0.2/)


Tracing 
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
      * Tracing  [ Tracing  ](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/) Table of contents 
        * [ Features  ](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#features)
        * [ Quick Start  ](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#quick-start)
        * [ Clients trace input/output/memory  ](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#clients-trace-inputoutputmemory)
        * [ Manual Span Creation  ](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#manual-span-creation)
        * [ Adding External Exporters  ](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#adding-external-exporters)
          * [ Create the resource  ](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#create-the-resource)
          * [ Zipkin Integration  ](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#zipkin-integration)
          * [ OTLP (OpenTelemetry Protocol)  ](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#otlp-opentelemetry-protocol)
        * [ Performance Considerations  ](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#performance-considerations)
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
  * [ Features  ](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#features)
  * [ Quick Start  ](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#quick-start)
  * [ Clients trace input/output/memory  ](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#clients-trace-inputoutputmemory)
  * [ Manual Span Creation  ](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#manual-span-creation)
  * [ Adding External Exporters  ](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#adding-external-exporters)
    * [ Create the resource  ](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#create-the-resource)
    * [ Zipkin Integration  ](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#zipkin-integration)
    * [ OTLP (OpenTelemetry Protocol)  ](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#otlp-opentelemetry-protocol)
  * [ Performance Considerations  ](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#performance-considerations)


  1. [ Home  ](https://docs.datapizza.ai/0.1.0/)
  2. [ Guides  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/quick_start/)
  3. [ Monitoring  ](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/)


# Tracing
The tracing module provides an easy-to-use interface for collecting and displaying OpenTelemetry traces with rich console output. It's designed to help developers monitor performance and understand the execution flow of their applications.
## Features
  * **In-memory trace collection** - Stores spans in memory for fast access
  * **Context-aware tracking** - Only collects spans for explicitly tracked operations
  * **Thread-safe operations** - Safe for use in multi-threaded applications
  * **OpenTelemetry integration** - Works with standard OpenTelemetry instrumentation


## Quick Start
The simplest way to use tracing is with the `tracer` context manager:

```
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-0-1)from datapizza.tracing import ContextTracing
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-0-2)
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-0-3)
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-0-4)# Basic tracing
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-0-5)with ContextTracing().trace("trace_name"):
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-0-6)    # Your code here
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-0-7)    result = some_datapizza_operations()
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-0-8)
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-0-9)# Output will show:
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-0-10)# ╭─ Trace Summary of my_operation ────────────────────────────────── ╮
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-0-11)# │ Total Spans: 3                                                    │
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-0-12)# │ Duration: 2.45s                                                   │
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-0-13)# │ ┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-0-14)# │ ┃ Model       ┃ Prompt Tokens ┃ Completion Tokens ┃ Cached Tokens ┃
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-0-15)# │ ┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-0-16)# │ │ gpt-4o-mini │ 31            │ 27                │ 0             │
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-0-17)# │ └─────────────┴───────────────┴───────────────────┴───────────────┘
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-0-18)# ╰───────────────────────────────────────────────────────────────────╯

```

## Clients trace input/output/memory
If you want to log the input/output and the memory passed to client invoke you should set the env variable
`DATAPIZZA_TRACE_CLIENT_IO=TRUE`
default is `FALSE`
## Manual Span Creation
For more granular control, create spans manually:

```
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-1-1)from opentelemetry import trace
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-1-2)from datapizza.tracing import ContextTracing
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-1-3)
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-1-4)tracer = trace.get_tracer(__name__)
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-1-5)
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-1-6)with ContextTracing().trace("trace_name"):
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-1-7)    with tracer.start_as_current_span("database_query"):
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-1-8)        # Database operation
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-1-9)        data = fetch_from_database()
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-1-10)
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-1-11)    with tracer.start_as_current_span("data_validation"):
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-1-12)        # Validation logic
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-1-13)        validate_data(data)
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-1-14)
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-1-15)    with tracer.start_as_current_span("business_logic"):
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-1-16)        # Core business logic
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-1-17)        result = process_business_rules(data)

```

## Adding External Exporters
The tracing module uses in-memory storage by default, but you can easily add external exporters to send traces to other systems.
### Create the resource
First of all you should set the trace provider

```
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-2-1)from opentelemetry.sdk.resources import Resource
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-2-2)from opentelemetry.sdk.trace import TracerProvider
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-2-3)from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-2-4)from opentelemetry.semconv.resource import ResourceAttributes
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-2-5)
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-2-6)resource = Resource.create(
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-2-7)   {
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-2-8)       ResourceAttributes.SERVICE_NAME: "your_service_name",
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-2-9)   }
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-2-10))
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-2-11)trace.set_tracer_provider(TracerProvider(resource=resource))

```

### Zipkin Integration
Export traces to Zipkin for visualization and analysis:
`pip install opentelemetry-exporter-zipkin`
After setting the trace provider you can add the exporters

```
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-3-1)from opentelemetry import trace
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-3-2)from opentelemetry.exporter.zipkin.json import ZipkinExporter
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-3-3)from opentelemetry.sdk.trace.export import SimpleSpanProcessor
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-3-4)from opentelemetry.sdk.resources import Resource
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-3-5)from opentelemetry.semconv.resource import ResourceAttributes
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-3-6)
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-3-7)zipkin_url = "http://localhost:9411/api/v2/spans"
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-3-8)
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-3-9)zipkin_exporter = ZipkinExporter(
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-3-10)    endpoint=zipkin_url,
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-3-11))
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-3-12)
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-3-13)tracer_provider = trace.get_tracer_provider()
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-3-14)
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-3-15)span_processor = SimpleSpanProcessor(zipkin_exporter)
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-3-16)trace.get_tracer_provider().add_span_processor(span_processor)
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-3-17)
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-3-18)# Now all traces will be sent to both in-memory storage and Zipkin

```

### OTLP (OpenTelemetry Protocol)
Export to any OTLP-compatible backend (Grafana, Datadog, etc.):

```
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-4-1)from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-4-2)from opentelemetry.sdk.trace.export import BatchSpanProcessor
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-4-3)
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-4-4)from opentelemetry.sdk.resources import Resource
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-4-5)from opentelemetry.semconv.resource import ResourceAttributes
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-4-6)
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-4-7)otlp_exporter = OTLPSpanExporter(
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-4-8)    endpoint="http://localhost:4317",
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-4-9)    headers={"authorization": "Bearer your-token"}
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-4-10))
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-4-11)
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-4-12)span_processor = BatchSpanProcessor(otlp_exporter)
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-4-13)trace.get_tracer_provider().add_span_processor(span_processor)

```

## Performance Considerations
  * Use `BatchSpanProcessor` for external exporters in production
  * Set reasonable limits on span attributes and events
  * Monitor memory usage with many active traces



```
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-5-1)# Production configuration
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-5-2)from opentelemetry.sdk.trace.export import BatchSpanProcessor
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-5-3)
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-5-4)# Batch spans for better performance
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-5-5)batch_processor = BatchSpanProcessor(
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-5-6)    exporter,
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-5-7)    max_queue_size=2048,
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-5-8)    schedule_delay_millis=5000,
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-5-9)    max_export_batch_size=512,
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-5-10))
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-5-11)
[](https://docs.datapizza.ai/0.1.0/Guides/Monitoring/tracing/#__codelineno-5-12)trace.get_tracer_provider().add_span_processor(batch_processor)

```

Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
