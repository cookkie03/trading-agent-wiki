---
source: https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/rewriters/
---

[ Skip to content ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#pdfimagesplitter)
[ ![logo](https://docs.datapizza.ai/0.1.0/assets/logo.png) ](https://docs.datapizza.ai/0.1.0/ "Datapizza AI")
Datapizza AI 
0.1.0
  * [0.1.0](https://docs.datapizza.ai/0.1.0/)
  * [0.0.9](https://docs.datapizza.ai/0.0.9/)
  * [0.0.7](https://docs.datapizza.ai/0.0.7/)
  * [0.0.2](https://docs.datapizza.ai/0.0.2/)


PDFImageSplitter 
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
        * PDFImageSplitter  [ PDFImageSplitter  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/) Table of contents 
          * [ PDFImageSplitter  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#datapizza.modules.splitters.PDFImageSplitter)
            * [ __init__  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#datapizza.modules.splitters.PDFImageSplitter.__init__)
            * [ split  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#datapizza.modules.splitters.PDFImageSplitter.split)
          * [ Usage  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#usage)
          * [ Features  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#features)
          * [ Examples  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#examples)
            * [ Basic PDF Content Splitting  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#basic-pdf-content-splitting)
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
  * [ PDFImageSplitter  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#datapizza.modules.splitters.PDFImageSplitter)
    * [ __init__  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#datapizza.modules.splitters.PDFImageSplitter.__init__)
    * [ split  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#datapizza.modules.splitters.PDFImageSplitter.split)
  * [ Usage  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#usage)
  * [ Features  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#features)
  * [ Examples  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#examples)
    * [ Basic PDF Content Splitting  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#basic-pdf-content-splitting)


  1. [ Home  ](https://docs.datapizza.ai/0.1.0/)
  2. [ API Reference  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/clients/)
  3. [ Modules  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/)
  4. [ Splitters  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/recursive_splitter/)


# PDFImageSplitter
##  datapizza.modules.splitters.PDFImageSplitter
Bases: `Splitter`
Splits a PDF document into individual pages, saves each page as an image using fitz, and returns metadata about each page as a Chunk object.
###  __init__

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-0-1)__init__(
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-0-2)    image_format="png",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-0-3)    output_base_dir="output_images",
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-0-4)    dpi=300,
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-0-5))

```

Initializes the Splitter.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `image_format`  |  `Literal['png', 'jpeg']`  |  The format to save the images in ('png' or 'jpeg'). Defaults to 'png'.  |  `'png'`  |  
|  `output_base_dir`  |  `str | Path`  |  The base directory where images for processed PDFs will be saved. A subdirectory will be created for each PDF. Defaults to 'output_images'.  |  `'output_images'`  |  
|  `dpi`  |  `int`  |  Dots Per Inch for rendering the PDF page to an image. Higher values increase resolution and file size. Defaults to 300.  |  `300`  |  
###  split

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-0-1)split(pdf_path)

```

Processes the PDF using fitz: converts pages to images and returns Chunk objects.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `pdf_path`  |  `str | Path`  |  The path to the input PDF file.  |  _required_  |  
Returns:  
| Type  | Description  |  
| --- | --- |  
|  `list[Chunk[](https://docs.datapizza.ai/0.1.0/API%20Reference/Type/chunk/#datapizza.type.Chunk "datapizza.type.Chunk


  
      dataclass
   \(datapizza.type.type.Chunk\)")]`  |  A list of Chunk objects, one for each page of the PDF.  |  
## Usage

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-0-1)from datapizza.modules.splitters import PDFImageSplitter
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-0-2)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-0-3)splitter = PDFImageSplitter()
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-0-4)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-0-5)pdf_chunks = splitter("pdf_path")

```

## Features
  * Specialized handling of PDF document structure
  * Preserves image data and visual elements
  * Maintains spatial layout information
  * Includes page-level metadata and coordinates
  * Handles complex document layouts with mixed content
  * Optimized for PDF content from document intelligence services


## Examples
### Basic PDF Content Splitting

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-1-1)from datapizza.modules.splitters import PDFImageSplitter
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-1-2)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-1-3)# Split while preserving images and layout
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-1-4)pdf_splitter = PDFImageSplitter()
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-1-5)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-1-6)pdf_chunks = pdf_splitter("pdf_path")
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-1-7)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-1-8)# Examine chunks with visual content
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-1-9)for i, chunk in enumerate(pdf_chunks):
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-1-10)    print(f"Chunk {i+1}:")
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-1-11)    print(f"  Content length: {len(chunk.content)}")
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-1-12)    print(f"  Page: {chunk.metadata.get('page_number', 'unknown')}")
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-1-13)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-1-14)    if hasattr(chunk, 'media') and chunk.media:
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-1-15)        print(f"  Media elements: {len(chunk.media)}")
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-1-16)        for media in chunk.media:
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-1-17)            print(f"    Type: {media.media_type}")
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-1-18)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-1-19)    if 'boundingRegions' in chunk.metadata:
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-1-20)        print(f"  Bounding regions: {len(chunk.metadata['boundingRegions'])}")
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-1-21)
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Modules/Splitters/pdf_image_splitter/#__codelineno-1-22)    print("---")

```

Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
