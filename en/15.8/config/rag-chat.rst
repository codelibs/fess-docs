==========================
AI Mode Configuration
==========================

Overview
========

AI mode (RAG: Retrieval-Augmented Generation) extends |Fess| search results with LLM (Large Language Model) capabilities,
providing information through conversational interaction. Users can ask questions in natural language and receive
detailed answers based on search results.

In |Fess| 15.8, LLM functionality has been separated as ``fess-llm-*`` plugins.
Core settings and LLM provider-specific settings are configured in ``fess_config.properties``, while
the LLM provider selection (``rag.llm.name``) is configured in ``system.properties`` or from the administration screen.

How AI Mode Works
=================

AI mode operates through the following multi-stage flow.

1. **Intent Analysis Phase**: Analyzes the user's question and extracts optimal keywords for search
2. **Search Phase**: Uses |Fess| search engine to find documents with the extracted keywords
3. **Query Regeneration Fallback**: When no search results are found, LLM regenerates the query and retries
4. **Evaluation Phase**: Evaluates relevance of search results and selects the most appropriate documents
5. **Generation Phase**: LLM generates a response based on the selected documents
6. **Output Phase**: Returns the response and source information to the user (with Markdown rendering)

This flow enables higher quality responses that understand context better than simple keyword searches.
Query regeneration improves answer coverage when the initial search query is not optimal.

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

Configuration Path Quick Reference
==================================

In |Fess| 15.8, settings are split into two families: the FessConfig family
(``fess_config.properties``) and the SystemProperty family (``system.properties``,
persisted in OpenSearch). The configuration path differs between the two, so do
not mix them up.

.. list-table::
   :header-rows: 1
   :widths: 35 18 32 15

   * - Property
     - Family
     - How to pass via Docker / JVM options
     - Admin UI
   * - ``rag.chat.enabled``
     - FessConfig
     - ``-Dfess.config.rag.chat.enabled=true``
     - No
   * - ``rag.llm.name``
     - SystemProperty
     - ``-Dfess.system.rag.llm.name=gemini`` (initial default only)
     - Yes (General settings)
   * - ``rag.llm.gemini.api.key``
     - FessConfig
     - ``-Dfess.config.rag.llm.gemini.api.key=...``
     - Yes
   * - ``rag.llm.gemini.model``
     - FessConfig
     - ``-Dfess.config.rag.llm.gemini.model=...``
     - Yes
   * - ``rag.llm.openai.api.key``
     - FessConfig
     - ``-Dfess.config.rag.llm.openai.api.key=...``
     - Yes
   * - ``rag.llm.openai.model``
     - FessConfig
     - ``-Dfess.config.rag.llm.openai.model=...``
     - Yes
   * - ``rag.llm.ollama.api.url``
     - FessConfig
     - ``-Dfess.config.rag.llm.ollama.api.url=...``
     - Yes

.. note::

   ``rag.llm.type`` is the legacy property name from |Fess| 15.5 and earlier.
   In 15.8 and later it has been renamed to ``rag.llm.name``; values written
   under ``rag.llm.type`` are not read.

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
     - ``30``
   * - ``rag.chat.content.fields``
     - Fields to retrieve from documents
     - ``title,url,content,doc_id,content_title,content_description``
   * - ``rag.chat.message.max.length``
     - Maximum number of characters in user messages
     - ``4000``
   * - ``rag.chat.highlight.fragment.size``
     - Search highlight fragment size
     - ``500``
   * - ``rag.chat.highlight.number.of.fragments``
     - Number of search highlight fragments
     - ``3``
   * - ``rag.chat.content.fulltext.max.length``
     - Threshold above which documents (by ``content_length``) use highlighted passages instead of full content in the answer context.
     - ``3000``
   * - ``rag.chat.answer.highlight.fragment.size``
     - Highlight fragment size used when extracting passages from large documents for the answer context.
     - ``1000``
   * - ``rag.chat.answer.highlight.number.of.fragments``
     - Number of highlight fragments used when extracting passages from large documents for the answer context.
     - ``5``
   * - ``rag.chat.history.assistant.content``
     - Type of content to include in assistant history ( ``full`` / ``smart_summary`` / ``source_titles`` / ``source_titles_and_urls`` / ``truncated`` / ``none`` )
     - ``smart_summary``
   * - ``rag.chat.history.titles.max.count``
     - Maximum number of referenced document titles kept per turn in ``smart_summary`` history mode.
     - ``5``

Generation Parameters
=====================

In |Fess| 15.8, generation parameters (maximum tokens, temperature, etc.) are configured
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
``{promptType}`` is replaced with the prompt type: ``intent``, ``evaluation``, ``answer``, ``summary``, ``faq``, ``queryregeneration``,
``unclear``, ``noresults``, ``docnotfound``, ``direct``.
The list of supported prompt types is defined in each plugin's ``*LlmClient`` implementation.

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

In |Fess| 15.8, system prompts are defined in the DI XML (``fess_llm++.xml``) of each ``fess-llm-*``
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
     - ``30``

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

    # Maximum concurrent requests per provider (default: 5)
    rag.llm.ollama.max.concurrent.requests=5
    rag.llm.openai.max.concurrent.requests=5
    rag.llm.gemini.max.concurrent.requests=5

    # Timeout for acquiring a concurrency permit (milliseconds, default: 30000)
    rag.llm.ollama.concurrency.wait.timeout=30000

Concurrency Control Considerations
------------------------------------

- Configure with the LLM provider's rate limits in mind
- In high-load environments, it is recommended to set lower values
- When the concurrency limit is reached, requests are queued and processed sequentially
- If waiting for a permit exceeds ``concurrency.wait.timeout``, the request fails with a timeout error.

Conversation History Mode
=========================

``rag.chat.history.assistant.content`` controls how assistant responses are stored in conversation history.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Mode
     - Description
   * - ``smart_summary``
     - (Default) Drops the assistant response body from history and keeps only, per turn, the past search query and the referenced document titles (up to ``rag.chat.history.titles.max.count`` items).
   * - ``full``
     - Preserves the entire response as-is
   * - ``source_titles``
     - Preserves only source titles
   * - ``source_titles_and_urls``
     - Preserves source titles and URLs
   * - ``truncated``
     - Truncates the response to the maximum character limit
   * - ``none``
     - Does not preserve history

.. note::

   In ``smart_summary`` mode, the assistant response body is not kept verbatim; instead it is replaced with the search query and the referenced document titles. This preserves context efficiently while reducing token usage.
   User and assistant message pairs are grouped as turns and optimally packed within a character budget.
   Maximum character limits for history and summary are controlled by the ``LlmClient`` implementation of each ``fess-llm-*`` plugin.

Query Regeneration
==================

When no search results are found or no relevant results are identified, the LLM automatically regenerates the query and retries the search.

- When zero search results: Query regeneration with reason ``no_results``
- When no relevant documents found: Query regeneration with reason ``no_relevant_results``
- Falls back to the original query if regeneration fails

This feature is enabled by default and integrated into both synchronous and streaming RAG flows.
Query regeneration prompts are defined in each ``fess-llm-*`` plugin.

Markdown Rendering
==================

AI mode responses are rendered in Markdown format.

- LLM responses are parsed as Markdown and converted to HTML
- Converted HTML is sanitized, allowing only safe tags and attributes
- Supports headings, lists, code blocks, tables, links, and other Markdown syntax
- Client-side uses ``marked.js`` and ``DOMPurify``; server-side uses OWASP sanitizer

API Usage
=========

AI mode functionality is available through the REST API (v2 API).
The base URL is ``http://<server name>/api/v2/``.

The Chat API provides the following three endpoints.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Endpoint
     - Description
   * - ``POST /api/v2/chat``
     - Batch (non-streaming) RAG chat completion.
   * - ``POST /api/v2/chat/stream``
     - Streaming RAG chat completion (Server-Sent Events).
   * - ``DELETE /api/v2/chat/sessions/{session_id}``
     - Clears the conversation history of a chat session.

Requests are sent as a JSON body with ``Content-Type: application/json``.
State-changing requests (``POST`` / ``DELETE``) require the CSRF token (``X-Fess-CSRF-Token`` header).
Responses are wrapped in the common ``response`` envelope.

.. note::

   The ``/api/v1/chat`` form-parameter endpoints provided in |Fess| 15.5 and earlier have been removed.
   Use the ``/api/v2/`` JSON-based API in 15.8.

Non-Streaming API
-----------------

Endpoint: ``POST /api/v2/chat``

Request body (JSON):

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Required
     - Description
   * - ``message``
     - Yes
     - User's message.
   * - ``session_id``
     - No
     - Session ID (when continuing a conversation). If omitted, the server creates one and returns it in the response.
   * - ``fields``
     - No
     - Optional filter fields for the retrieval step (object).
   * - ``fields.label``
     - No
     - Restricts retrieval by label.
   * - ``extra_queries``
     - No
     - Additional query expressions for facet filtering.

Request example:

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -d '{"message":"How do I install Fess?"}'

Response example:

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session_id": "abc123",
        "content": "To install Fess...",
        "sources": [
          {
            "rank": 1,
            "title": "Installation Guide",
            "url": "https://...",
            "doc_id": "...",
            "snippet": "..."
          }
        ]
      }
    }

Streaming API
-------------

Endpoint: ``POST /api/v2/chat/stream``

The request body is the same as ``POST /api/v2/chat`` (JSON).
Responses are streamed in Server-Sent Events (SSE) format.

Request example:

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat/stream" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -H "Accept: text/event-stream" \
         --no-buffer \
         -d '{"message":"What are the features of Fess?"}'

SSE Events:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Event
     - Description (payload)
   * - ``phase``
     - Pipeline phase transition (``{ phase, status, message?, keywords?, hit_count?, ... }``). Phases: ``intent``, ``search``, ``evaluate``, ``fetch``, ``answer``.
   * - ``chunk``
     - Fragment of generated text (``{ content }``).
   * - ``retry``
     - Back-off for a transient failure (``{ phase, operation, attempt, max_attempts, sleep_ms, cause? }``).
   * - ``waiting``
     - Progress of a long-running phase such as waiting for a concurrency permit (``{ phase, reason, elapsed_ms, timeout_ms }``).
   * - ``fallback``
     - Notification that the query was regenerated (``{ phase, reason, original_query?, new_query? }``). Reason is ``no_results`` or ``no_relevant_results``.
   * - ``warning``
     - Recoverable warning (``{ phase, code, detail? }``), e.g. reasoning-model token exhaustion.
   * - ``sources``
     - Retrieved source documents (``{ sources: [...] }``).
   * - ``done``
     - Stream end (``{ session_id, html_content? }``). ``html_content`` holds the Markdown-rendered HTML string.
   * - ``error``
     - Terminal mid-stream failure (``{ phase?, message, error_code }``). Covers timeout, context length exceeded, model not found, invalid response, connection errors, etc.

Clearing a Session
------------------

Endpoint: ``DELETE /api/v2/chat/sessions/{session_id}``

Clears the conversation history of the specified session. On success, ``cleared: true`` is returned.

For full API documentation (authentication, CSRF, rate limits, and HTTP status codes), see :doc:`../api/api-chat`.

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

AI Mode Button Does Not Appear on the Search Screen
---------------------------------------------------

**Symptom**: The AI mode button is not shown in the search results header,
and accessing ``/chat`` redirects back to the top page.

**Checklist**: Verify the items below in order.

1. Is ``rag.chat.enabled=true`` set?

   - Docker: confirm that ``-Dfess.config.rag.chat.enabled=true`` is included in ``FESS_JAVA_OPTS``
   - Package install: confirm it is written in ``app/WEB-INF/conf/fess_config.properties``

2. Is the matching ``fess-llm-*`` plugin installed?

   - Docker: ``FESS_PLUGINS=fess-llm-gemini:15.8.0`` (or ``fess-llm-openai`` / ``fess-llm-ollama``) must be set
   - Package install: the JAR must be placed in ``app/WEB-INF/plugin/``
   - Startup logs should include ``Installing fess-llm-XXX-15.8.0.jar``

3. Does ``rag.llm.name`` match an installed plugin?

   - The default value is ``ollama``. If only the Gemini plugin is installed, you must explicitly set ``gemini`` (likewise ``openai`` for the OpenAI plugin)
   - Method (a): edit ``rag.llm.name`` from Administration > System > General (RAG section) and save
   - Method (b): include ``-Dfess.system.rag.llm.name=gemini`` in ``FESS_JAVA_OPTS`` at startup. This only acts as the initial default before a value is persisted in OpenSearch

4. Is a WARN like ``[LLM] LlmClient not found. componentName=ollamaLlmClient`` repeating in the startup log?

   - This is the typical symptom when ``rag.llm.name`` is still ``ollama`` but the Ollama plugin is not installed
   - Setting ``rag.llm.name`` to the actual provider in use clears it
   - Similarly, ``componentName=geminiLlmClient`` indicates that ``rag.llm.name=gemini`` is set but the ``fess-llm-gemini`` plugin is not installed

5. Is the provider-specific API key configured?

   - When ``rag.llm.gemini.api.key`` / ``rag.llm.openai.api.key`` is empty, ``checkAvailabilityNow`` returns ``false`` and AI mode is disabled
   - Enabling DEBUG on ``org.codelibs.fess.llm.gemini`` in ``log4j2.xml`` surfaces messages such as ``[LLM:GEMINI] Gemini is not available. apiKey is blank``

6. Can the Fess host reach the LLM provider?

   - For cloud APIs (Gemini / OpenAI), the container must have outbound Internet access
   - When a proxy is required, set ``http.proxy.host`` / ``http.proxy.port`` (and optionally ``http.proxy.username`` / ``http.proxy.password``) in ``fess_config.properties``. In Docker environments, append ``-Dfess.config.http.proxy.host=... -Dfess.config.http.proxy.port=...`` to ``FESS_JAVA_OPTS`` (since |Fess| 15.8, the LLM clients consult the |Fess|-wide proxy configuration)

.. note::

   The "General" settings page does not expose a checkbox for ``rag.chat.enabled``
   (by design). It is a FessConfig-family property and can only be set through
   ``fess_config.properties`` or ``-Dfess.config.rag.chat.enabled=true``.

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
    <Logger name="org.codelibs.fess.api.v2.handlers" level="DEBUG"/>
    <Logger name="org.codelibs.fess.chat" level="DEBUG"/>

Log messages use the ``[RAG]`` prefix, with sub-prefixes such as ``[RAG:INTENT]``, ``[RAG:EVAL]``, and ``[RAG:ANSWER]`` for each phase.
At INFO level, chat completion logs (elapsed time, source count) are output. At DEBUG level, token usage, concurrency control, and history packing details are output.

Search Log and Access Type
--------------------------

Searches through AI mode are recorded with the LLM provider name (e.g., ``ollama``, ``openai``, ``gemini``) as the access type in search logs. This allows distinguishing AI mode searches from regular web or API searches in analytics.

References
==========

- :doc:`llm-overview` - LLM Integration Overview
- :doc:`llm-ollama` - Ollama Configuration
- :doc:`llm-openai` - OpenAI Configuration
- :doc:`llm-gemini` - Google Gemini Configuration
- :doc:`../api/api-chat` - Chat API Reference
- :doc:`../user/chat-search` - End User Chat Search Guide
