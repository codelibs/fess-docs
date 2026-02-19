==========================
LLM Integration Overview
==========================

Overview
========

|Fess| 15.5 supports AI mode (RAG: Retrieval-Augmented Generation) functionality powered by Large Language Models (LLM).
This feature allows users to retrieve information through conversational AI assistance based on search results.

Supported Providers
===================

|Fess| supports the following LLM providers.

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Provider
     - Configuration Value
     - Description
   * - Ollama
     - ``ollama``
     - An open-source LLM server that runs in local environments. Supports models like Llama, Mistral, and Gemma. Default setting.
   * - OpenAI
     - ``openai``
     - OpenAI's cloud API. Enables use of models like GPT-4.
   * - Google Gemini
     - ``gemini``
     - Google's cloud API. Enables use of Gemini models.

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

To enable LLM functionality, add the following settings to ``app/WEB-INF/conf/fess_config.properties``.

Enabling AI Mode
----------------

::

    # Enable AI mode functionality
    rag.chat.enabled=true

Selecting LLM Provider
----------------------

::

    # Specify LLM provider (ollama, openai, gemini)
    rag.llm.type=ollama

For detailed configuration of each provider, please refer to the following documentation.

- :doc:`llm-ollama` - Ollama Configuration
- :doc:`llm-openai` - OpenAI Configuration
- :doc:`llm-gemini` - Google Gemini Configuration

Common Settings
===============

Configuration items used across all LLM providers.

Generation Parameters
---------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``rag.chat.max.tokens``
     - Maximum number of tokens to generate
     - ``4096``
   * - ``rag.chat.temperature``
     - Generation randomness (0.0-1.0). Lower values produce more deterministic responses
     - ``0.7``

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
   * - ``rag.chat.context.max.chars``
     - Maximum number of characters in context
     - ``4000``
   * - ``rag.chat.content.fields``
     - Fields to retrieve from documents
     - ``title,url,content,...``

System Prompt
-------------

::

    rag.chat.system.prompt=You are an AI assistant for Fess search engine. Answer questions based on the search results provided. Always cite your sources using [1], [2], etc.

This prompt defines the basic behavior of the LLM. You can customize it as needed.

Availability Check
------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``rag.llm.availability.check.interval``
     - Interval (in seconds) to check LLM availability. Set to 0 to disable
     - ``60``

This setting allows |Fess| to periodically verify the connection status with the LLM provider.

Session Management
==================

Configuration for chat session management.

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

Rate Limiting
=============

Rate limiting settings to prevent API overload.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``rag.chat.rate.limit.enabled``
     - Enable rate limiting
     - ``true``
   * - ``rag.chat.rate.limit.requests.per.minute``
     - Maximum requests per minute
     - ``10``

Evaluation Settings
===================

Settings for search result evaluation.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``rag.chat.evaluation.max.relevant.docs``
     - Maximum number of relevant documents to select in the evaluation phase
     - ``3``

Next Steps
==========

- :doc:`llm-ollama` - Detailed Ollama Configuration
- :doc:`llm-openai` - Detailed OpenAI Configuration
- :doc:`llm-gemini` - Detailed Google Gemini Configuration
- :doc:`rag-chat` - Detailed AI Mode Configuration
