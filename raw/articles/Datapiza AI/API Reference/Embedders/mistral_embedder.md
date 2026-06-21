---
source: https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/
---

[ Skip to content ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#mistralembedder)
[ ![logo](https://docs.datapizza.ai/0.1.0/assets/logo.png) ](https://docs.datapizza.ai/0.1.0/ "Datapizza AI")
Datapizza AI 
0.1.0
  * [0.1.0](https://docs.datapizza.ai/0.1.0/)
  * [0.0.9](https://docs.datapizza.ai/0.0.9/)
  * [0.0.7](https://docs.datapizza.ai/0.0.7/)
  * [0.0.2](https://docs.datapizza.ai/0.0.2/)


MistralEmbedder 
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
      * MistralEmbedder  [ MistralEmbedder  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/) Table of contents 
        * [ Usage  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#usage)
          * [ Async Embedding  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#async-embedding)
        * [ Ingestion  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#ingestion)
          * [ The full error  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#the-full-error)
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
  * [ Usage  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#usage)
    * [ Async Embedding  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#async-embedding)
  * [ Ingestion  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#ingestion)
    * [ The full error  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#the-full-error)


  1. [ Home  ](https://docs.datapizza.ai/0.1.0/)
  2. [ API Reference  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/clients/)
  3. [ Embedders  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/)


# MistralEmbedder

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-0-1)pip install datapizza-ai-embedders-mistral

```

## Usage

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-1-1)from datapizza.embedders.mistral import MistralEmbedder
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-1-2)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-1-3)embedder = MistralEmbedder(
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-1-4)    api_key=os.getenv("MISTRAL_API_KEY"),
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-1-5)    model_name="mistral-embed",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-1-6))
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-1-7)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-1-8)embedding = mistral_embedder.embed(text)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-1-9)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-1-10)# Embed multiple texts
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-1-11)embeddings = embedder.embed(
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-1-12)    ["Hello world", "Another text"],
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-1-13))

```

### Async Embedding

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-2-1)import asyncio
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-2-2)from datapizza.embedders.mistral import MistralEmbedder
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-2-3)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-2-4)async def embed_async():
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-2-5)    embedder = MistralEmbedder(
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-2-6)        api_key=os.getenv("MISTRAL_API_KEY"),
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-2-7)        model_name="mistral-embed",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-2-8)    )
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-2-9)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-2-10)    text = "Async embedding example"
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-2-11)    embedding = await embedder.a_embed(text)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-2-12)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-2-13)    return embedding
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-2-14)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-2-15)# Run async function
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-2-16)embedding = asyncio.run(embed_async())

```

## Ingestion
Set the batch size to a conservative value (eg: 150) to avoid the error `Too many inputs in request`:

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-3-1)                ingestion_pipeline = IngestionPipeline(
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-3-2)                    modules=[
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-3-3)                        # some modules
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-3-4)                        ChunkEmbedder(
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-3-5)                            client=MistralEmbedder(
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-3-6)                                api_key="some_key",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-3-7)                                model_name="mistral-embed",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-3-8)                            ),
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-3-9)                            batch_size=150  # Mistral API limit (conservative)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-3-10)                        ),
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-3-11)                    ],
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-3-12)                )

```

### The full error

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-4-1){
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-4-2)  "object": "error",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-4-3)  "message": "Too many inputs in request, split into more batches.",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-4-4)  "type": "invalid_request_prompt",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-4-5)  "param": null,
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-4-6)  "code": "3210"
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/mistral_embedder/#__codelineno-4-7)}

```

Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
