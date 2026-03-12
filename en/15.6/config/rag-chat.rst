==========================
AI Mode Configuration
==========================

Overview
========

AI mode (RAG: Retrieval-Augmented Generation) extends |Fess| search results with LLM (Large Language Model) capabilities,
providing information through conversational interaction. Users can ask questions in natural language and receive
detailed answers based on search results.

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

Basic settings for enabling AI mode functionality.

``app/WEB-INF/conf/fess_config.properties``:

::

    # Enable AI mode functionality
    rag.chat.enabled=true

    # Select LLM provider (ollama, openai, gemini)
    rag.llm.type=ollama

For detailed LLM provider configuration, refer to:

- :doc:`llm-ollama` - Ollama Configuration
- :doc:`llm-openai` - OpenAI Configuration
- :doc:`llm-gemini` - Google Gemini Configuration

Generation Parameters
=====================

Parameters that control LLM generation behavior.

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
     - Generation randomness (0.0-1.0)
     - ``0.7``

Temperature Setting
-------------------

- **0.0**: Deterministic responses (always the same response for the same input)
- **0.3-0.5**: Consistent responses (appropriate for fact-based questions)
- **0.7**: Balanced responses (default)
- **1.0**: Creative responses (appropriate for brainstorming, etc.)

Context Settings
================

Settings for the context passed from search results to the LLM.

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
   * - ``rag.chat.evaluation.max.relevant.docs``
     - Maximum number of relevant documents to select in evaluation phase
     - ``3``

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

The system prompt defines the basic behavior of the LLM.

Default Setting
---------------

::

    rag.chat.system.prompt=You are an AI assistant for Fess search engine. Answer questions based on the search results provided. Always cite your sources using [1], [2], etc.

Customization Examples
----------------------

For prioritizing Japanese responses:

::

    rag.chat.system.prompt=You are an AI assistant for the Fess search engine. Please answer questions based on the provided search results. Respond in Japanese and always cite your sources using [1], [2], etc.

For specialized domains:

::

    rag.chat.system.prompt=You are a technical documentation assistant. Provide detailed and accurate answers based on the search results. Include code examples when relevant. Always cite your sources using [1], [2], etc.

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

Rate Limiting Considerations
----------------------------

- Consider the LLM provider's rate limits when configuring
- In high-load environments, stricter limits are recommended
- When rate limits are reached, users will see an error message

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
2. Is the LLM provider correctly configured?
3. Is the connection to the LLM provider possible?

Low Response Quality
--------------------

**Improvements**:

1. Use a higher-performance LLM model
2. Increase ``rag.chat.context.max.documents``
3. Customize the system prompt
4. Adjust ``rag.chat.temperature``

Slow Responses
--------------

**Improvements**:

1. Use a faster LLM model (e.g., Gemini Flash)
2. Decrease ``rag.chat.max.tokens``
3. Decrease ``rag.chat.context.max.chars``

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
