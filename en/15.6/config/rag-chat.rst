==========================
AI Mode Configuration
==========================

Overview
========

AI mode (RAG: Retrieval-Augmented Generation) extends |Fess| search results with LLM (Large Language Model) capabilities,
providing information through conversational interaction. Users can ask questions in natural language and receive
detailed answers based on search results.

In |Fess| 15.6, LLM functionality has been separated as ``fess-llm-*`` plugins.
Core settings and LLM provider-specific settings are configured in ``fess_config.properties``, while
the LLM provider selection (``rag.llm.name``) is configured in ``system.properties`` or from the administration screen.

How AI Mode Works
=================

AI mode operates through the following multi-stage flow.

1. **Intent Analysis Phase**: Analyzes the user's question and extracts optimal keywords for search
2. **Search Phase**: Uses |Fess| search engine to find documents with the extracted keywords
3. **Evaluation Phase**: Evaluates relevance of search results and selects the most appropriate documents
4. **Generation Phase**: LLM generates a response based on the selected documents
5. **Output Phase**: Returns the response and source information to the user

This flow enables higher quality responses that understand context better than simple keyword searches.

Basic Configuration
===================

AI mode configuration is divided into core settings and provider settings.

Core Settings (fess_config.properties)
---------------------------------------

Basic settings for enabling AI mode functionality.
Configure in ``app/WEB-INF/conf/fess_config.properties``.

::

    # Enable AI mode functionality
    rag.chat.enabled=true

LLM Provider Selection (system.properties / Administration Screen)
-------------------------------------------------------------------

The LLM provider is selected from the administration screen or in ``system.properties``. Only ``rag.llm.name`` is configured here.

**Configuring from the administration screen**:

Select the LLM provider to use from the settings screen at Administration > System > General.

**Configuring in system.properties**:

::

    # Select LLM provider (ollama, openai, gemini)
    rag.llm.name=ollama

For detailed LLM provider configuration, refer to:

- :doc:`llm-ollama` - Ollama Configuration
- :doc:`llm-openai` - OpenAI Configuration
- :doc:`llm-gemini` - Google Gemini Configuration

Core Settings List
==================

List of core settings that can be configured in ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``rag.chat.enabled``
     - Enable AI mode functionality
     - ``false``
   * - ``rag.chat.context.max.documents``
     - Maximum number of documents to include in context
     - ``5``
   * - ``rag.chat.session.timeout.minutes``
     - Session timeout duration (in minutes)
     - ``30``
   * - ``rag.chat.session.max.size``
     - Maximum number of concurrent sessions
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - Maximum number of messages to retain in conversation history
     - ``20``
   * - ``rag.chat.intent.history.max.messages``
     - Maximum number of conversation history messages used for intent analysis
     - ``4``
   * - ``rag.chat.content.fields``
     - Fields to retrieve from documents
     - ``title,url,content,doc_id,content_title,content_description``
   * - ``rag.chat.message.max.length``
     - Maximum number of characters in user messages
     - ``4000``
   * - ``rag.chat.highlight.fragment.size``
     - Fragment size for highlight display
     - ``500``
   * - ``rag.chat.highlight.number.of.fragments``
     - Number of fragments for highlight display
     - ``3``
   * - ``rag.chat.history.assistant.content``
     - Type of content to include in assistant history
     - ``source_titles``
   * - ``rag.chat.history.assistant.max.chars``
     - Maximum number of characters in assistant history
     - ``500``
   * - ``rag.chat.history.assistant.summary.max.chars``
     - Maximum number of characters for assistant history summary
     - ``500``
   * - ``rag.chat.history.max.chars``
     - Maximum number of characters in conversation history
     - ``2000``

Generation Parameters
=====================

In |Fess| 15.6, generation parameters (maximum tokens, temperature, etc.) are configured
per provider and per prompt type. These settings are managed as part of each ``fess-llm-*``
plugin's configuration rather than as core settings.

For details, refer to each provider's documentation:

- :doc:`llm-ollama` - Ollama generation parameter settings
- :doc:`llm-openai` - OpenAI generation parameter settings
- :doc:`llm-gemini` - Google Gemini generation parameter settings

Context Settings
================

Settings for the context passed from search results to the LLM.

Core Settings
-------------

The following settings are configured in ``fess_config.properties``.

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

Provider-Specific Settings
--------------------------

The following settings are configured per provider in ``fess_config.properties``.

- ``rag.llm.{provider}.{promptType}.context.max.chars`` - Maximum number of context characters
- ``rag.llm.{provider}.chat.evaluation.max.relevant.docs`` - Maximum number of relevant documents to select in the evaluation phase

``{provider}`` is replaced with the provider name such as ``ollama``, ``openai``, or ``gemini``.
``{promptType}`` is replaced with the prompt type such as ``chat``, ``intent_analysis``, or ``evaluation``.

For details, refer to each provider's documentation.

Content Fields
--------------

Fields that can be specified in ``rag.chat.content.fields``:

- ``title`` - Document title
- ``url`` - Document URL
- ``content`` - Document body
- ``doc_id`` - Document ID
- ``content_title`` - Content title
- ``content_description`` - Content description

System Prompt
=============

In |Fess| 15.6, system prompts are defined in the DI XML (``fess_llm++.xml``) of each ``fess-llm-*``
plugin rather than in properties files.

Customizing Prompts
-------------------

To customize system prompts, override the ``fess_llm++.xml`` from the plugin JAR.

1. Retrieve ``fess_llm++.xml`` from the plugin JAR file you are using
2. Make the necessary changes
3. Place it in the appropriate location under ``app/WEB-INF/`` to override

Different system prompts are defined for each prompt type (intent analysis, evaluation, generation),
optimized for their respective purposes.

For details, refer to each provider's documentation:

- :doc:`llm-ollama` - Ollama prompt settings
- :doc:`llm-openai` - OpenAI prompt settings
- :doc:`llm-gemini` - Google Gemini prompt settings

Session Management
==================

Settings for chat session management.

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
     - Maximum number of concurrent sessions
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - Maximum number of messages to retain in conversation history
     - ``20``

Session Behavior
----------------

- When a user starts a new chat, a new session is created
- Conversation history is saved in the session, enabling context-aware dialogue
- Sessions are automatically deleted after the timeout period
- When conversation history exceeds the maximum message count, older messages are deleted first

Concurrency Control
===================

The number of concurrent requests to the LLM is controlled per provider in ``fess_config.properties``.

::

    # Maximum concurrent requests per provider
    rag.llm.ollama.max.concurrent.requests=5
    rag.llm.openai.max.concurrent.requests=10
    rag.llm.gemini.max.concurrent.requests=10

Concurrency Control Considerations
------------------------------------

- Configure with the LLM provider's rate limits in mind
- In high-load environments, it is recommended to set lower values
- When the concurrency limit is reached, requests are queued and processed sequentially

API Usage
=========

AI mode functionality is available through REST APIs.

Non-Streaming API
-----------------

Endpoint: ``POST /api/v1/chat``

Parameters:

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Required
     - Description
   * - ``message``
     - Yes
     - User's message
   * - ``sessionId``
     - No
     - Session ID (when continuing a conversation)
   * - ``clear``
     - No
     - Set to ``true`` to clear the session

Request Example:

::

    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "message=How do I install Fess?"

Response Example:

::

    {
      "status": "ok",
      "sessionId": "abc123",
      "content": "To install Fess...",
      "sources": [
        {"title": "Installation Guide", "url": "https://..."}
      ]
    }

Streaming API
-------------

Endpoint: ``POST /api/v1/chat/stream``

Streams responses in Server-Sent Events (SSE) format.

Parameters:

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Required
     - Description
   * - ``message``
     - Yes
     - User's message
   * - ``sessionId``
     - No
     - Session ID (when continuing a conversation)

Request Example:

::

    curl -X POST "http://localhost:8080/api/v1/chat/stream" \
         -d "message=What are the features of Fess?" \
         -H "Accept: text/event-stream"

SSE Events:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Event
     - Description
   * - ``session``
     - Session information (sessionId)
   * - ``phase``
     - Processing phase start/completion (intent_analysis, search, evaluation, generation)
   * - ``chunk``
     - Generated text fragments
   * - ``sources``
     - Reference document information
   * - ``done``
     - Processing complete (sessionId, htmlContent)
   * - ``error``
     - Error information

For detailed API documentation, see :doc:`../api/api-chat`.

Web Interface
=============

In the |Fess| web interface, AI mode functionality is available from the search screen.

Starting a Chat
---------------

1. Access the |Fess| search screen
2. Click the chat icon
3. The chat panel will be displayed

Using the Chat
--------------

1. Enter your question in the text box
2. Click the send button or press Enter
3. The AI assistant's response will be displayed
4. Responses include links to reference sources

Continuing a Conversation
-------------------------

- You can continue conversations within the same chat session
- Responses will consider the context of previous questions
- Click "New Chat" to reset the session

Troubleshooting
===============

AI Mode Won't Enable
--------------------

**Check the following**:

1. Is ``rag.chat.enabled=true`` configured?
2. Is the LLM provider correctly configured with ``rag.llm.name``?
3. Is the corresponding ``fess-llm-*`` plugin installed?
4. Is the connection to the LLM provider possible?

Low Response Quality
--------------------

**Improvements**:

1. Use a higher-performance LLM model
2. Increase ``rag.chat.context.max.documents``
3. Customize system prompts in the DI XML
4. Adjust provider-specific temperature settings (refer to each ``fess-llm-*`` plugin's documentation)

Slow Responses
--------------

**Improvements**:

1. Use a faster LLM model (e.g., Gemini Flash)
2. Decrease provider-specific max.tokens settings (refer to each ``fess-llm-*`` plugin's documentation)
3. Decrease ``rag.chat.context.max.documents``

Session Not Maintained
----------------------

**Check the following**:

1. Is sessionId being sent correctly from the client?
2. Check the ``rag.chat.session.timeout.minutes`` setting
3. Check session storage capacity

Debug Settings
--------------

When investigating issues, adjust log levels to output detailed logs.

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm" level="DEBUG"/>
    <Logger name="org.codelibs.fess.api.chat" level="DEBUG"/>
    <Logger name="org.codelibs.fess.chat" level="DEBUG"/>

References
==========

- :doc:`llm-overview` - LLM Integration Overview
- :doc:`llm-ollama` - Ollama Configuration
- :doc:`llm-openai` - OpenAI Configuration
- :doc:`llm-gemini` - Google Gemini Configuration
- :doc:`../api/api-chat` - Chat API Reference
- :doc:`../user/chat-search` - End User Chat Search Guide
