==============================================
AI Search (RAG) and LLM Integration Overview
==============================================

Overview
========

|Fess| supports AI search mode (RAG: Retrieval-Augmented Generation) functionality powered by Large Language Models (LLM).
This feature allows users to retrieve information through conversational AI assistance based on search results, answering natural-language questions directly from your enterprise search index with cited sources.

LLM integration is provided as ``fess-llm-*`` plugins. Install the plugin corresponding to the LLM provider you wish to use.

AI search mode retrieves documents through the standard |Fess| search pipeline (rank fusion), not a separate vector index — by default this is keyword (BM25) search. Because it reuses that pipeline, if you install and configure the Semantic Search plugin, its semantic (vector) searcher participates in rank fusion for all searches, including the retrieval step of AI search mode; no AI-search-specific configuration is required. See :doc:`rank-fusion`.

Supported Providers
===================

|Fess| supports the following LLM providers.

.. list-table::
   :header-rows: 1
   :widths: 20 20 30 30

   * - Provider
     - Configuration Value
     - Plugin
     - Description
   * - Ollama
     - ``ollama``
     - ``fess-llm-ollama``
     - An open-source LLM server that runs in local environments. Supports models such as Llama, Mistral, and Gemma. Default setting.
   * - OpenAI
     - ``openai``
     - ``fess-llm-openai``
     - OpenAI's cloud API. Enables use of models such as GPT-4.
   * - Google Gemini
     - ``gemini``
     - ``fess-llm-gemini``
     - Google's cloud API. Enables use of Gemini models.

Provider Comparison
--------------------

.. list-table::
   :header-rows: 1

   * - Provider (``rag.llm.name``)
     - Default model
     - Endpoint
     - Authentication
     - Data location
   * - Ollama (``ollama``)
     - ``gemma4:e4b``
     - ``http://localhost:11434``
     - None (local)
     - Local / self-hosted — questions and documents stay on your host
   * - OpenAI (``openai``)
     - ``gpt-5-mini``
     - ``https://api.openai.com/v1``
     - ``Authorization: Bearer`` (``rag.llm.openai.api.key``)
     - Cloud — the question and retrieved documents are sent to OpenAI
   * - Google Gemini (``gemini``)
     - ``gemini-3.1-flash-lite-preview``
     - ``https://generativelanguage.googleapis.com/v1beta``
     - ``x-goog-api-key`` (``rag.llm.gemini.api.key``)
     - Cloud — the question and retrieved documents are sent to Google

.. note::

   If ``rag.llm.name`` is not set, only the Ollama client is active by default; install and select the provider you want with ``rag.llm.name``.

Plugin Installation
===================

LLM functionality is provided as plugins. You must place the JAR file of the ``fess-llm-{provider}`` plugin corresponding to your provider in the plugin directory.

For example, to use the OpenAI provider, download ``fess-llm-openai-15.7.0.jar`` and place it in the following directory.

::

    app/WEB-INF/plugin/

After placement, restart |Fess| to load the plugin.

Architecture
============

The AI search mode feature operates with the following flow.

1. **User Input**: User enters a question in the chat interface
2. **Intent Analysis (intent)**: LLM analyzes the user's question and extracts search keywords
3. **Search Execution (search)**: |Fess| search engine retrieves relevant documents
4. **Result Evaluation (evaluate)**: LLM evaluates the relevance of search results and selects the most suitable documents
5. **Query Regeneration (when needed)**: If no search results are found, or if no relevant documents are identified during evaluation, the LLM regenerates the query and retries the search
6. **Content Fetching (fetch)**: Retrieves the body text of the selected documents
7. **Answer Generation (answer)**: LLM generates a response based on the retrieved documents (Markdown rendering supported)
8. **Source Citation**: The response includes links to the referenced source documents

.. note::

   The internal processing consists of five phases — ``intent``, ``search``, ``evaluate``, ``fetch``, and ``answer`` — and the progress of each phase is reported to the client via streaming (SSE).

Basic Configuration
===================

LLM functionality is configured in the following two locations.

Administration Screen General Settings / system.properties
----------------------------------------------------------

Configure in the administration screen general settings or in ``system.properties``. Used for selecting the LLM provider.

::

    # Specify LLM provider (ollama, openai, gemini)
    rag.llm.name=ollama

fess_config.properties
----------------------

Configure in ``app/WEB-INF/conf/fess_config.properties``. In addition to enabling AI search mode and configuring session and history-related settings, provider-specific settings such as the connection URL, API key, and generation parameters are also specified in this file.

::

    # Enable AI search mode functionality
    rag.chat.enabled=true

    # Example of provider-specific settings (for OpenAI)
    rag.llm.openai.api.key=sk-...
    rag.llm.openai.answer.temperature=0.7

For detailed configuration of each provider, please refer to the following documentation.

- :doc:`llm-ollama` - Ollama configuration
- :doc:`llm-openai` - OpenAI configuration
- :doc:`llm-gemini` - Google Gemini configuration

Common Settings
===============

Configuration items used across all LLM providers. These are configured in ``fess_config.properties``.

Context Settings
----------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``rag.chat.context.max.documents``
     - Maximum number of documents to include in context
     - ``5``
   * - ``rag.chat.content.fields``
     - Fields to retrieve from documents
     - ``title,url,content,doc_id,content_title,content_description``

.. note::

   The maximum number of characters in context (``context.max.chars``) has been changed to a per-provider and per-prompt-type setting. Configure it as ``rag.llm.{provider}.{promptType}.context.max.chars`` in ``fess_config.properties``.

System Prompt
-------------

System prompts are managed in the DI XML files of each plugin rather than in properties files.

The system prompt is defined in the ``fess_llm++.xml`` file bundled inside the JAR of each ``fess-llm-*`` plugin. Because this file is a classpath resource bundled within the plugin JAR, customizing a prompt requires editing the DI XML file inside the JAR.

Availability Check
------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``rag.llm.{provider}.availability.check.interval``
     - Interval (in seconds) at which LLM availability is checked. Set to 0 to disable.
     - ``60``

This setting is configured in ``fess_config.properties``. |Fess| periodically verifies the connection status with the LLM provider.

Session Management
==================

Settings for chat sessions. These are configured in ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``rag.chat.session.timeout.minutes``
     - Session timeout duration (in minutes)
     - ``30``
   * - ``rag.chat.session.max.size``
     - Maximum number of sessions
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - Maximum number of messages to retain in conversation history
     - ``30``

Concurrency Control
===================

Settings for controlling the number of concurrent requests to the LLM. Configure in ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``rag.llm.{provider}.max.concurrent.requests``
     - Maximum number of concurrent requests to the provider
     - ``5``
   * - ``rag.llm.{provider}.concurrency.wait.timeout``
     - Maximum time (in milliseconds) to wait for an available slot when the concurrency limit is reached. If no slot becomes available within this time, a rate-limit error is returned.
     - ``30000``

For example, to configure the concurrency for the OpenAI provider:

::

    rag.llm.openai.max.concurrent.requests=10

Evaluation Settings
===================

Settings for search result evaluation. Configure in ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``rag.llm.{provider}.chat.evaluation.max.relevant.docs``
     - Maximum number of relevant documents to select in the evaluation phase
     - ``3``

Per-Prompt-Type Settings
========================

Generation parameters can be configured per prompt type, allowing fine-grained tuning for each use case. Configure in ``fess_config.properties``.

Prompt Type List
----------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Prompt Type
     - Configuration Value
     - Description
   * - Intent Analysis
     - ``intent``
     - Analyzes the user's question and extracts search keywords
   * - Evaluation
     - ``evaluation``
     - Evaluates the relevance of search results
   * - Unclear Question
     - ``unclear``
     - Generates a response when the question is unclear
   * - No Results
     - ``noresults``
     - Generates a response when no search results are found
   * - Document Not Found
     - ``docnotfound``
     - Generates a response when the corresponding document does not exist
   * - Answer Generation
     - ``answer``
     - Generates an answer based on search results
   * - Summary
     - ``summary``
     - Generates a summary of documents
   * - FAQ
     - ``faq``
     - Generates FAQ-style answers
   * - Direct Answer
     - ``direct``
     - Generates a direct answer without going through search
   * - Query Regeneration
     - ``queryregeneration``
     - Regenerates the query when no search results are found

Configuration Pattern
---------------------

Per-prompt-type settings are specified using the following pattern.

::

    rag.llm.{provider}.{promptType}.temperature
    rag.llm.{provider}.{promptType}.max.tokens
    rag.llm.{provider}.{promptType}.context.max.chars

Configuration examples (for the OpenAI provider):

::

    # Set answer generation temperature lower
    rag.llm.openai.answer.temperature=0.5
    # Maximum tokens for answer generation
    rag.llm.openai.answer.max.tokens=4096
    # Intent analysis requires only short responses, so set lower
    rag.llm.openai.intent.max.tokens=256
    # Maximum context characters for summary
    rag.llm.openai.summary.context.max.chars=8000

.. note::

   ``temperature``, ``max.tokens``, and ``context.max.chars`` are available across all providers. In addition, each provider supports provider-specific parameters such as ``thinking.budget``, ``top.p``, and ``reasoning.effort``. Refer to the documentation for each provider for details.

Next Steps
==========

- :doc:`llm-ollama` - Detailed Ollama configuration
- :doc:`llm-openai` - Detailed OpenAI configuration
- :doc:`llm-gemini` - Detailed Google Gemini configuration
- :doc:`rag-chat` - Detailed AI search mode configuration
- :doc:`rank-fusion` - Rank Fusion settings (hybrid search result merging)
