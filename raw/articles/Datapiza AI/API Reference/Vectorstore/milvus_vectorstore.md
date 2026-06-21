---
source: https://docs.datapizza.ai/0.1.0/API%20Reference/Vectorstore/milvus_vectorstore/
---

[ Skip to content ](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#multimodality)
[ ![logo](https://docs.datapizza.ai/0.1.0/assets/logo.png) ](https://docs.datapizza.ai/0.1.0/ "Datapizza AI")
Datapizza AI 
0.1.0
  * [0.1.0](https://docs.datapizza.ai/0.1.0/)
  * [0.0.9](https://docs.datapizza.ai/0.0.9/)
  * [0.0.7](https://docs.datapizza.ai/0.0.7/)
  * [0.0.2](https://docs.datapizza.ai/0.0.2/)


Multimodality 
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
      * Multimodality  [ Multimodality  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/) Table of contents 
        * [ Supported Media Types  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#supported-media-types)
        * [ Basic Image Input  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#basic-image-input)
          * [ Single Image from File  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#single-image-from-file)
          * [ Image from URL  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#image-from-url)
          * [ Image from Base64  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#image-from-base64)
        * [ Multiple Images  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#multiple-images)
        * [ Working with PDFs  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#working-with-pdfs)
        * [ Working with Audio  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#working-with-audio)
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
  * [ Supported Media Types  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#supported-media-types)
  * [ Basic Image Input  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#basic-image-input)
    * [ Single Image from File  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#single-image-from-file)
    * [ Image from URL  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#image-from-url)
    * [ Image from Base64  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#image-from-base64)
  * [ Multiple Images  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#multiple-images)
  * [ Working with PDFs  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#working-with-pdfs)
  * [ Working with Audio  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#working-with-audio)


  1. [ Home  ](https://docs.datapizza.ai/0.1.0/)
  2. [ Guides  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/quick_start/)
  3. [ Clients  ](https://docs.datapizza.ai/0.1.0/Guides/Clients/quick_start/)


# Multimodality
The clients supports various media types including images and PDFs, allowing you to create rich multimodal applications.
## Supported Media Types  
| Media Type  | Supported Formats  | Source Types  |  
| --- | --- | --- |  
| Images  | PNG, JPEG, GIF, WebP  | File path, URL, base64  |  
| PDFs  | PDF documents  | File path, base64  |  
## Basic Image Input
### Single Image from File

```
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-1)from datapizza.clients.openai import OpenAIClient
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-2)from datapizza.type import Media, MediaBlock, TextBlock
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-3)
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-4)client = OpenAIClient(
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-5)    api_key="your-api-key",
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-6)    model="gpt-4o"  # Vision models required for images
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-7))
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-8)
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-9)# Create image media object
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-10)image = Media(
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-11)    media_type="image",
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-12)    source_type="path",
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-13)    source="image.png", # Use the correct path
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-14)    extension="png"
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-15))
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-16)
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-17)# Create media block
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-18)media_block = MediaBlock(media=image)
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-19)text_block = TextBlock(content="What do you see in this image?")
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-20)
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-21)# Send multimodal input
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-22)response = client.invoke(
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-23)    input=[text_block, media_block],
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-24)    max_tokens=200
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-25))
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-26)
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-0-27)print(response.text)

```

### Image from URL

```
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-1-1)# Image from URL
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-1-2)image_url = Media(
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-1-3)    media_type="image",
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-1-4)    source_type="url",
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-1-5)    source="https://example.com/image.png",
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-1-6)    extension="png"
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-1-7))
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-1-8)
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-1-9)response = client.invoke(
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-1-10)    input=[
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-1-11)        TextBlock(content="Describe this image"),
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-1-12)        MediaBlock(media=image_url)
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-1-13)    ]
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-1-14))
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-1-15)print(response.text)

```

### Image from Base64

```
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-2-1)import base64
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-2-2)
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-2-3)# Read and encode image
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-2-4)with open("image.jpg", "rb") as image_file:
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-2-5)    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-2-6)
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-2-7)image_b64 = Media(
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-2-8)    media_type="image",
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-2-9)    source_type="base64",
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-2-10)    source=base64_image,
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-2-11)    extension="png"
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-2-12))
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-2-13)
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-2-14)response = client.invoke(
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-2-15)    input=[
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-2-16)        TextBlock(content="Analyze this image"),
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-2-17)        MediaBlock(media=image_b64)
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-2-18)    ]
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-2-19))
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-2-20)print(response.text)

```

## Multiple Images
Compare or analyze multiple images in a single request:

```
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-1)# Multiple images for comparison
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-2)image1 = Media(
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-3)    media_type="image",
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-4)    source_type="path",
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-5)    source="before.png",
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-6)    extension="png"
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-7))
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-8)
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-9)image2 = Media(
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-10)    media_type="image",
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-11)    source_type="path",
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-12)    source="after.png",
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-13)    extension="png"
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-14))
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-15)
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-16)response = client.invoke(
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-17)    input=[
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-18)        TextBlock(content="Compare these two images and describe the differences"),
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-19)        MediaBlock(media=image1),
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-20)        MediaBlock(media=image2)
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-21)    ],
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-22)    max_tokens=300
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-23))
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-24)
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-3-25)print(response.text)

```

## Working with PDFs

```
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-4-1)# PDF from file path
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-4-2)pdf_doc = Media(
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-4-3)    media_type="pdf",
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-4-4)    source_type="path",
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-4-5)    source="document.pdf",
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-4-6)    extension="pdf"
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-4-7))
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-4-8)
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-4-9)response = client.invoke(
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-4-10)    input=[
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-4-11)        TextBlock(content="Summarize the key points from this document"),
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-4-12)        MediaBlock(media=pdf_doc)
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-4-13)    ],
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-4-14)    max_tokens=500
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-4-15))
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-4-16)
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-4-17)print(response.text)

```

## Working with Audio
Google handle audio inline

```
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-5-1)pip install datapizza-ai-clients-google

```


```
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-6-1)from datapizza.clients.google import GoogleClient
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-6-2)from datapizza.type import Media, MediaBlock, TextBlock
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-6-3)
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-6-4)client = GoogleClient(
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-6-5)    api_key="YOUR_API_KEY",
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-6-6)    model="gemini-2.0-flash-exp"
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-6-7))
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-6-8)# PDF from file path
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-6-9)media = Media(
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-6-10)    media_type="audio",
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-6-11)    source_type="path",
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-6-12)    source="sample.mp3",
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-6-13)    extension="mp3"
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-6-14))
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-6-15)
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-6-16)response = client.invoke(
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-6-17)    input=[
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-6-18)        TextBlock(content="Summarize the key points from this audio file"),
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-6-19)        MediaBlock(media=media)
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-6-20)    ],
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-6-21))
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-6-22)
[](https://docs.datapizza.ai/0.1.0/Guides/Clients/multimodality/#__codelineno-6-23)print(response.text)

```

Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
