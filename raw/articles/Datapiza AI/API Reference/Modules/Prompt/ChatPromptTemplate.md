---
source: https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Prompt/ChatPromptTemplate/
---

[ Skip to content ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#chunkembedder)
[ ![logo](https://docs.datapizza.ai/0.1.0/assets/logo.png) ](https://docs.datapizza.ai/0.1.0/ "Datapizza AI")
Datapizza AI 
0.1.0
  * [0.1.0](https://docs.datapizza.ai/0.1.0/)
  * [0.0.9](https://docs.datapizza.ai/0.0.9/)
  * [0.0.7](https://docs.datapizza.ai/0.0.7/)
  * [0.0.2](https://docs.datapizza.ai/0.0.2/)


ChunkEmbedder 
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
      * ChunkEmbedder  [ ChunkEmbedder  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/) Table of contents 
        * [ ChunkEmbedder  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#datapizza.embedders.ChunkEmbedder)
          * [ __init__  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#datapizza.embedders.ChunkEmbedder.__init__)
          * [ a_embed  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#datapizza.embedders.ChunkEmbedder.a_embed)
          * [ embed  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#datapizza.embedders.ChunkEmbedder.embed)
        * [ Usage  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#usage)
        * [ Features  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#features)
        * [ Examples  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#examples)
          * [ Basic Chunk Embedding  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#basic-chunk-embedding)
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
  * [ ChunkEmbedder  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#datapizza.embedders.ChunkEmbedder)
    * [ __init__  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#datapizza.embedders.ChunkEmbedder.__init__)
    * [ a_embed  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#datapizza.embedders.ChunkEmbedder.a_embed)
    * [ embed  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#datapizza.embedders.ChunkEmbedder.embed)
  * [ Usage  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#usage)
  * [ Features  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#features)
  * [ Examples  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#examples)
    * [ Basic Chunk Embedding  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#basic-chunk-embedding)


  1. [ Home  ](https://docs.datapizza.ai/0.1.0/)
  2. [ API Reference  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/clients/)
  3. [ Embedders  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/)


# ChunkEmbedder
##  datapizza.embedders.ChunkEmbedder
Bases: `PipelineComponent`
ChunkEmbedder is a module that given a list of chunks, it put a list of embeddings in each chunk.
###  __init__

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-0-1)__init__(
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-0-2)    client,
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-0-3)    model_name=None,
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-0-4)    embedding_name=None,
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-0-5)    batch_size=2047,
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-0-6))

```

Initialize the ChunkEmbedder.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `client`  |  `BaseEmbedder`  |  The client to use for embedding.  |  _required_  |  
|  `model_name`  |  `str`  |  The model name to use for embedding. Defaults to None.  |  `None`  |  
|  `embedding_name`  |  `str`  |  The name of the embedding to use. Defaults to None.  |  `None`  |  
|  `batch_size`  |  `int`  |  The batch size to use for embedding. Defaults to 2047.  |  `2047`  |  
###  a_embed `async`

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-0-1)a_embed(nodes)

```

Asynchronously embeds the given list of chunks.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |  `list[Chunk[](https://docs.datapizza.ai/0.1.0/API%20Reference/Type/chunk/#datapizza.type.Chunk "datapizza.type.Chunk


  
      dataclass
  ")]`  |  The list of chunks to embed.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `list[Chunk[](https://docs.datapizza.ai/0.1.0/API%20Reference/Type/chunk/#datapizza.type.Chunk "datapizza.type.Chunk


  
      dataclass
  ")]`  |  list[Chunk]: The list of chunks with embeddings.  |  
###  embed

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-0-1)embed(nodes)

```

Embeds the given list of chunks.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `nodes`  |  `list[Chunk[](https://docs.datapizza.ai/0.1.0/API%20Reference/Type/chunk/#datapizza.type.Chunk "datapizza.type.Chunk


  
      dataclass
  ")]`  |  The list of chunks to embed.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `list[Chunk[](https://docs.datapizza.ai/0.1.0/API%20Reference/Type/chunk/#datapizza.type.Chunk "datapizza.type.Chunk


  
      dataclass
  ")]`  |  list[Chunk]: The list of chunks with embeddings.  |  
## Usage

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-0-1)from datapizza.embedders import ChunkEmbedder
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-0-2)from datapizza.core.clients import Client
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-0-3)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-0-4)# Initialize with any compatible client
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-0-5)client = Client(...)  # Your client instance
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-0-6)embedder = ChunkEmbedder(
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-0-7)    client=client,
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-0-8)    model_name="text-embedding-ada-002",  # Optional model override
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-0-9)    embedding_name="my_embeddings",       # Optional custom embedding name
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-0-10)    batch_size=100                        # Optional batch size for processing
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-0-11))
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-0-12)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-0-13)# Embed chunks - adds embeddings to chunk objects
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-0-14)embedded_chunks = embedder.embed(chunks)

```

## Features
  * Specialized for embedding lists of Chunk objects
  * Batch processing with configurable batch size
  * Adds embeddings directly to Chunk objects
  * Preserves original chunk structure and metadata
  * Async embedding support with `a_embed()`
  * Memory efficient batch processing
  * Works with any compatible LLM client


## Examples
### Basic Chunk Embedding

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-1)import os
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-2)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-3)from datapizza.embedders import ChunkEmbedder
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-4)from datapizza.embedders.openai import OpenAIEmbedder
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-5)from datapizza.type import Chunk
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-6)from dotenv import load_dotenv
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-7)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-8)load_dotenv()
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-9)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-10)# Create client and embedder
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-11)client = OpenAIEmbedder(api_key=os.getenv("OPENAI_API_KEY"))
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-12)embedder = ChunkEmbedder(
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-13)    client=client,
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-14)    model_name="text-embedding-ada-002",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-15)    batch_size=50
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-16))
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-17)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-18)# Create sample chunks
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-19)chunks = [
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-20)    Chunk(id="1", text="First chunk of text", metadata={"source": "doc1"}),
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-21)    Chunk(id="2", text="Second chunk of text", metadata={"source": "doc2"}),
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-22)    Chunk(id="3", text="Third chunk of text", metadata={"source": "doc3"})
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-23)]
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-24)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-25)# Embed chunks (modifies chunks in-place)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-26)embedded_chunks = embedder.embed(chunks)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-27)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-28)# Check embeddings were added
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-29)for i, chunk in enumerate(embedded_chunks):
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-30)    print(f"Chunk {i+1}:")
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-31)    print(f"  Text: {chunk.text[:50]}...")
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-32)    print(f"  Embeddings: {len(chunk.embeddings)}")
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-33)    if chunk.embeddings:
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-34)        print(f"  Embedding name: {chunk.embeddings[0].name}")
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/chunk_embedder/#__codelineno-1-35)        print(f"  Vector size: {len(chunk.embeddings[0].vector)}")

```

Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
