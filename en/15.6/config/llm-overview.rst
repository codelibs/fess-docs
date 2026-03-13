==========================
LLM Integration Overview
==========================

Overview
========

|Fess| 15.6 supports AI mode (RAG: Retrieval-Augmented Generation) functionality powered by Large Language Models (LLM).
This feature allows users to retrieve information through conversational AI assistance based on search results.

In |Fess| 15.6, LLM integration is provided as ``fess-llm-*`` plugins. Install the plugin corresponding to the LLM provider you wish to use.

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
     - An open-source LLM server that runs in local environments. Supports models like Llama, Mistral, and Gemma. Default setting.
   * - OpenAI
     - ``openai``
     - ``fess-llm-openai``
     - OpenAI's cloud API. Enables use of models like GPT-4.
   * - Google Gemini
     - ``gemini``
     - ``fess-llm-gemini``
     - Google's cloud API. Enables use of Gemini models.

Plugin Installation
===================

In |Fess| 15.6, LLM functionality is separated as plugins. You must place the JAR file of the ``fess-llm-{provider}`` plugin corresponding to your provider in the plugin directory.

For example, to use the OpenAI provider, download ``fess-llm-openai-15.6.0.jar`` and place it in the following directory.

::

    app/WEB-INF/plugin/

After placement, restart |Fess| to load the plugin.

Architecture
============

The AI mode feature operates with the following flow.

1. **User Input**: User enters a question in the chat interface
2. **Intent Analysis**: LLM analyzes the user's question and extracts search keywords
3. **Search Execution**: |Fess| search engine retrieves relevant documents
4. **Result Evaluation**: LLM evaluates the relevance of search results and selects optimal documents
5. **Response Generation**: LLM generates a response based on the selected documents
6. **Source Citation**: The response includes links to referenced source documents

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

Configure in ``app/WEB-INF/conf/fess_config.properties``. These settings are loaded at startup and are used to enable AI mode, configure session and history-related settings, and set provider-specific parameters such as connection URL, API key, and generation parameters.

::

    # Enable AI mode functionality
    rag.chat.enabled=true

    # Example of provider-specific settings (for OpenAI)
    rag.llm.openai.api.key=sk-...
    rag.llm.openai.answer.temperature=0.7

For detailed configuration of each provider, please refer to the following documentation.

- :doc:`llm-ollama` - Ollama Configuration
- :doc:`llm-openai` - OpenAI Configuration
- :doc:`llm-gemini` - Google Gemini Configuration

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
     - ``title,url,content,...``

.. note::

   The maximum number of characters in context (``context.max.chars``) has been changed to a per-provider and per-prompt-type setting. Configure it as ``rag.llm.{provider}.{promptType}.context.max.chars`` in ``fess_config.properties``.

System Prompt
-------------

In |Fess| 15.6, system prompts are managed in the DI XML files of each plugin rather than in properties files.

System prompts are defined in the ``fess_llm++.xml`` file included in each ``fess-llm-*`` plugin. To customize prompts, edit the DI XML file in the plugin directory.

Availability Check
------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``rag.llm.{provider}.availability.check.interval``
     - Interval (in seconds) to check LLM availability. Set to 0 to disable
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
     - ``20``

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

In |Fess| 15.6, generation parameters can be configured per prompt type. This allows fine-grained adjustments based on the intended use. Configure in ``fess_config.properties``.

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

Configuration Pattern
---------------------

Per-prompt-type settings are specified using the following pattern.

::

    rag.llm.{provider}.{promptType}.temperature
    rag.llm.{provider}.{promptType}.max.tokens
    rag.llm.{provider}.{promptType}.context.max.chars

Configuration Examples (for OpenAI provider):

::

    # Set answer generation temperature lower
    rag.llm.openai.answer.temperature=0.5
    # Maximum tokens for answer generation
    rag.llm.openai.answer.max.tokens=4096
    # Intent analysis requires only short responses, so set lower
    rag.llm.openai.intent.max.tokens=256
    # Maximum context characters for summary
    rag.llm.openai.summary.context.max.chars=8000

Next Steps
==========

- :doc:`llm-ollama` - Detailed Ollama Configuration
- :doc:`llm-openai` - Detailed OpenAI Configuration
- :doc:`llm-gemini` - Detailed Google Gemini Configuration
- :doc:`rag-chat` - Detailed AI Mode Configuration
- :doc:`rank-fusion` - Rank Fusion Settings (Hybrid Search Result Merging)
