==========================
Chat API
==========================

Overview
========

The Chat API is a v2 API for programmatic access to |Fess|'s AI search mode (RAG chat) feature.
You can obtain LLM-generated answers (completions) based on search results.

This API provides the following three endpoints:

.. tabularcolumns:: |p{6cm}|p{9cm}|
.. list-table::
   :header-rows: 1

   * - Endpoint
     - Description
   * - ``POST /chat``
     - Batch (non-streaming) RAG chat completion.
   * - ``POST /chat/stream``
     - Streaming RAG chat completion (Server-Sent Events).
   * - ``DELETE /chat/sessions/{session_id}``
     - Clears the conversation history of a chat session.

For the base URL, common response envelope, and error codes, see :doc:`api-overview`.

::

    http://<Server Name>/api/v2/

Local environment example:

::

    http://localhost:8080/api/v2

Prerequisites
=============

To use the Chat API, the following configuration is required:

1. The AI search mode (RAG chat) feature must be enabled (``rag.chat.enabled=true``)
2. An LLM provider must be configured

If the feature is disabled (``rag.chat.enabled=false``), requests return an ``invalid_request`` error.

For detailed configuration, see :doc:`../config/rag-chat` and :doc:`../config/llm-overview`.

Authentication and CSRF
========================

All Chat API endpoints are state-changing requests (``POST`` / ``DELETE``), so the ``X-Fess-CSRF-Token`` header is required.
For information on how to obtain the CSRF token and details about authentication and sessions, see :doc:`api-overview`.

Rate Limiting
=============

``POST /chat`` and ``DELETE /chat/sessions/{session_id}`` have per-user rate limits applied.

- Default: 30 requests per minute (per user)
- Configuration key: ``api.v2.chat.rate.limit.per.user.per.minute``

When the rate limit is exceeded, a ``rate_limited`` error (HTTP 429) is returned. The ``Retry-After`` header indicates the number of seconds to wait.
This rate limit is shared between ``POST /chat`` and ``DELETE /chat/sessions/{session_id}``.

POST /chat
==========

Performs synchronous chat completion.
Sessions are identified by ``session_id``. If ``session_id`` is omitted, the server creates a session and returns it in the response's ``session_id``.

Invalid values passed in ``fields.label`` or ``extra_queries`` are silently removed from the resolved request and do not surface in the response envelope.

Endpoint
--------

::

    POST /api/v2/chat

Request Body
------------

A JSON body with ``Content-Type: application/json``.

.. tabularcolumns:: |p{3.5cm}|p{2.5cm}|p{1.5cm}|p{7cm}|
.. list-table:: ChatRequest
   :header-rows: 1

   * - Field
     - Type
     - Required
     - Description
   * - ``message``
     - string
     - Yes
     - User's message (question).
   * - ``session_id``
     - string
     - No
     - Session ID. When omitted, the server creates one and returns it in the response.
   * - ``fields``
     - object
     - No
     - Optional filter fields for the retrieval step.
   * - ``fields.label``
     - string / string array
     - No
     - Restricts retrieval to allowlisted labels.
   * - ``extra_queries``
     - string / string array
     - No
     - Allowlisted facet query expressions.

Request example:

.. code-block:: json

    {
      "message": "What is Fess?",
      "session_id": "abc123def456",
      "fields": {
        "label": "news"
      },
      "extra_queries": "label:faq"
    }

Response
--------

**On success (HTTP 200, ChatResponse)**

The response is stored in the common envelope ``response``. ``session_id`` is always present.

.. tabularcolumns:: |p{3cm}|p{2.5cm}|p{9cm}|
.. list-table:: Elements of response
   :header-rows: 1

   * - Field
     - Type
     - Description
   * - ``session_id``
     - string
     - Session ID.
   * - ``content``
     - string (nullable)
     - Generated message text. Always present, but may be ``null`` if the model generated no content.
   * - ``sources``
     - array
     - Array of source documents. Each element is a ChatSource.

**ChatSource**

.. tabularcolumns:: |p{3cm}|p{2.5cm}|p{9cm}|
.. list-table:: Elements of ChatSource
   :header-rows: 1

   * - Field
     - Type
     - Description
   * - ``rank``
     - integer
     - 1-based position in the retrieval set.
   * - ``title``
     - string (nullable)
     - Document title.
   * - ``url``
     - string (nullable)
     - Document URL.
   * - ``doc_id``
     - string (nullable)
     - Document ID.
   * - ``snippet``
     - string (nullable)
     - Snippet.
   * - ``url_link``
     - string (nullable)
     - Display URL link.
   * - ``go_url``
     - string (nullable)
     - Redirect URL.

Response example:

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session_id": "abc123def456",
        "content": "Fess is a full-text search server. Key features include...",
        "sources": [
          {
            "rank": 1,
            "title": "Fess Overview",
            "url": "https://fess.codelibs.org/ja/overview.html",
            "doc_id": "abcdef0123456789",
            "snippet": "Fess is...",
            "url_link": "https://fess.codelibs.org/ja/overview.html",
            "go_url": "/go/?docId=abcdef0123456789"
          }
        ]
      }
    }

HTTP Status Codes
-----------------

.. tabularcolumns:: |p{2cm}|p{13cm}|
.. list-table::
   :header-rows: 1

   * - Code
     - Description
   * - 200
     - Request successful.
   * - 400
     - Invalid request (missing ``message``, ``rag.chat.enabled=false``, etc.).
   * - 403
     - Missing or expired CSRF token.
   * - 404
     - Resource not found.
   * - 405
     - HTTP method not allowed.
   * - 413
     - Request body exceeds size limit.
   * - 415
     - Unsupported ``Content-Type``.
   * - 429
     - Rate limit exceeded.
   * - 500
     - Internal server error.

cURL Example
------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -d '{"message":"What is Fess?","session_id":"abc123def456"}'

POST /chat/stream
=================

Performs streaming chat completion.
The request body is the same as ``POST /chat`` (ChatRequest).

A successful response is a series of named events in ``text/event-stream`` format (Server-Sent Events).
Each event consists of ``event: <name>`` and ``data: <JSON>``.

Validation failures before the stream begins still return a JSON envelope (same error codes as ``POST /chat``).
Invalid values in ``fields.label`` or ``extra_queries`` are silently removed and do not appear in the response envelope or SSE events.

Endpoint
--------

::

    POST /api/v2/chat/stream

SSE Events
----------

.. tabularcolumns:: |p{2.5cm}|p{12.5cm}|
.. list-table::
   :header-rows: 1

   * - Event
     - Description (payload)
   * - ``phase``
     - Pipeline phase transition (``{ phase, status, message?, keywords?, hit_count?, ... }``). ``message`` and ``keywords`` are emitted on onPhaseStart. Additional optional fields (e.g., ``hit_count``) flow from the onPhaseComplete payload.
   * - ``chunk``
     - Fragment of generated text (``{ content }``).
   * - ``sources``
     - Retrieved sources (``{ sources: [ChatSource] }``).
   * - ``retry``
     - Back-off for transient failure (``{ phase, operation, attempt, max_attempts, sleep_ms, cause? }``).
   * - ``waiting``
     - Progress of a long-running phase (``{ phase, reason, elapsed_ms, timeout_ms }``).
   * - ``fallback``
     - Query rewrite or strategy fallback (``{ phase, reason, original_query?, new_query? }``).
   * - ``warning``
     - Recoverable warning (``{ phase, code, detail? }``).
   * - ``done``
     - Stream end (``{ session_id, html_content? }``).
   * - ``error``
     - Terminal mid-stream failure (``{ phase?, message, error_code }``). The ``message`` field contains the same string as ``error_code``. Clients should localize based on ``error_code``.

SSE stream example:

::

    event: phase
    data: {"phase":"retrieval","status":"start","message":"Searching documents...","keywords":"Fess install"}

    event: chunk
    data: {"content":"Fess is"}

    event: sources
    data: {"sources":[{"rank":1,"title":"Installation Guide","url":"https://fess.codelibs.org/ja/install.html"}]}

    event: done
    data: {"session_id":"abc123def456"}

HTTP Status Codes
-----------------

When pre-stream validation fails, the following error codes are returned in a JSON envelope.

.. tabularcolumns:: |p{2cm}|p{13cm}|
.. list-table::
   :header-rows: 1

   * - Code
     - Description
   * - 200
     - SSE stream started (success).
   * - 400
     - Invalid request (missing ``message``, ``rag.chat.enabled=false``, etc.).
   * - 403
     - Missing or expired CSRF token.
   * - 405
     - HTTP method not allowed.
   * - 413
     - Request body exceeds size limit.
   * - 415
     - Unsupported ``Content-Type``.
   * - 429
     - Rate limit exceeded.
   * - 500
     - Internal server error.

cURL Example
------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat/stream" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -H "Accept: text/event-stream" \
         --no-buffer \
         -d '{"message":"Tell me about the features of Fess"}'

DELETE /chat/sessions/{session_id}
===================================

Clears the conversation history of the specified chat session.
The session is identified by the ``session_id`` in the path.

On success, ``cleared: true`` is returned. When no matching active session exists, a ``not_found`` error (HTTP 404) is returned.

Endpoint
--------

::

    DELETE /api/v2/chat/sessions/{session_id}

Path Parameters
---------------

.. tabularcolumns:: |p{3cm}|p{2cm}|p{10cm}|
.. list-table::
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``session_id``
     - string
     - ID of the session to clear. minLength 1, maxLength 128, pattern ``^[A-Za-z0-9._-]+$``.

Response
--------

**On success (HTTP 200, ChatClearResponse)**

The response is stored in the common envelope ``response``. ``session_id`` and ``cleared`` are always present.

.. tabularcolumns:: |p{3cm}|p{2.5cm}|p{9cm}|
.. list-table:: Elements of response
   :header-rows: 1

   * - Field
     - Type
     - Description
   * - ``session_id``
     - string
     - Session ID.
   * - ``cleared``
     - boolean
     - Always ``true`` (when the session was found and cleared).

Response example:

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session_id": "abc123def456",
        "cleared": true
      }
    }

HTTP Status Codes
-----------------

.. tabularcolumns:: |p{2cm}|p{13cm}|
.. list-table::
   :header-rows: 1

   * - Code
     - Description
   * - 200
     - Session cleared.
   * - 400
     - Invalid request.
   * - 401
     - Authentication required.
   * - 403
     - Missing or expired CSRF token.
   * - 404
     - No matching active session found.
   * - 405
     - HTTP method not allowed.
   * - 429
     - Rate limit exceeded.
   * - 500
     - Internal server error.

cURL Example
------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/v2/chat/sessions/abc123def456" \
         -H "X-Fess-CSRF-Token: <token>"

Security
========

Security considerations when using the Chat API:

1. **Authentication**: The v2 API uses session-based authentication. See :doc:`api-overview` for details.
2. **CSRF**: State-changing requests require the ``X-Fess-CSRF-Token`` header.
3. **Rate Limiting**: Per-user rate limiting (default 30/minute) is applied to prevent DoS attacks. The configuration key is ``api.v2.chat.rate.limit.per.user.per.minute``.

References
==========

- :doc:`../config/rag-chat` - AI search mode feature configuration
- :doc:`../config/llm-overview` - LLM integration overview
- :doc:`../user/chat-search` - End user chat search guide
- :doc:`api-overview` - API Overview
