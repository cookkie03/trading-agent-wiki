---
source: https://docs.datapizza.ai/0.1.0/API%20Reference/Embedders/google_embedder/
---

[ Skip to content ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#response)
[ ![logo](https://docs.datapizza.ai/0.1.0/assets/logo.png) ](https://docs.datapizza.ai/0.1.0/ "Datapizza AI")
Datapizza AI 
0.1.0
  * [0.1.0](https://docs.datapizza.ai/0.1.0/)
  * [0.0.9](https://docs.datapizza.ai/0.0.9/)
  * [0.0.7](https://docs.datapizza.ai/0.0.7/)
  * [0.0.2](https://docs.datapizza.ai/0.0.2/)


Response 
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
      * Response  [ Response  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/) Table of contents 
        * [ ClientResponse  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#datapizza.core.clients.ClientResponse)
          * [ first_text  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#datapizza.core.clients.ClientResponse.first_text)
          * [ function_calls  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#datapizza.core.clients.ClientResponse.function_calls)
          * [ structured_data  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#datapizza.core.clients.ClientResponse.structured_data)
          * [ text  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#datapizza.core.clients.ClientResponse.text)
          * [ thoughts  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#datapizza.core.clients.ClientResponse.thoughts)
          * [ is_pure_function_call  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#datapizza.core.clients.ClientResponse.is_pure_function_call)
          * [ is_pure_text  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#datapizza.core.clients.ClientResponse.is_pure_text)
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
  * [ ClientResponse  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#datapizza.core.clients.ClientResponse)
    * [ first_text  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#datapizza.core.clients.ClientResponse.first_text)
    * [ function_calls  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#datapizza.core.clients.ClientResponse.function_calls)
    * [ structured_data  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#datapizza.core.clients.ClientResponse.structured_data)
    * [ text  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#datapizza.core.clients.ClientResponse.text)
    * [ thoughts  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#datapizza.core.clients.ClientResponse.thoughts)
    * [ is_pure_function_call  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#datapizza.core.clients.ClientResponse.is_pure_function_call)
    * [ is_pure_text  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#datapizza.core.clients.ClientResponse.is_pure_text)


  1. [ Home  ](https://docs.datapizza.ai/0.1.0/)
  2. [ API Reference  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/clients/)
  3. [ Clients  ](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/clients/)


# Response
##  datapizza.core.clients.ClientResponse
A class for storing the response from a client. Contains a list of blocks that can be text, function calls, or structured data, maintaining the order in which they were generated.
Parameters:  
| Name  | Type  | Description  | Default  |  
| --- | --- | --- | --- |  
|  `content`  |  `List[Block[](https://docs.datapizza.ai/0.1.0/API%20Reference/Type/block/#datapizza.type.Block "datapizza.type.Block")]`  |  A list of blocks.  |  _required_  |  
|  `delta`  |  `str`  |  The delta of the response. Used for streaming responses.  |  `None`  |  
|  `usage`  |  `TokenUsage`  |  Aggregated token usage.  |  `None`  |  
|  `stop_reason`  |  `str`  |  Stop reason.  |  `None`  |  
###  first_text `property`

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#__codelineno-0-1)first_text

```

Returns the content of the first TextBlock or None
###  function_calls `property`

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#__codelineno-0-1)function_calls

```

Returns all function calls in order
###  structured_data `property`

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#__codelineno-0-1)structured_data

```

Returns all structured data in order
###  text `property`

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#__codelineno-0-1)text

```

Returns concatenated text from all TextBlocks in order
###  thoughts `property`

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#__codelineno-0-1)thoughts

```

Returns all thoughts in order
###  is_pure_function_call

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#__codelineno-0-1)is_pure_function_call()

```

Returns True if response contains only FunctionCallBlocks
###  is_pure_text

```
[](https://docs.datapizza.ai/0.1.0/API%20Reference/Clients/models/#__codelineno-0-1)is_pure_text()

```

Returns True if response contains only TextBlocks
Made with [ Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)
