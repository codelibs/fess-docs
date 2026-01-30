==========================
Chat API
==========================

Overview
========

The Chat API is a RESTful API for programmatic access to |Fess|'s RAG chat functionality.
You can obtain AI-assisted answers based on search results.

This API provides two endpoints:

- **Non-Streaming API**: Retrieve complete answers at once
- **Streaming API**: Retrieve answers in real-time using Server-Sent Events (SSE) format

Prerequisites
=============

To use the Chat API, the following configuration is required:

1. RAG chat functionality must be enabled (``rag.chat.enabled=true``)
2. An LLM provider must be configured

For detailed configuration, see :doc:`../config/rag-chat`.

Non-Streaming API
=================

Endpoint
--------

::

    POST /api/v1/chat

Request Parameters
------------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Type
     - Required
     - Description
   * - ``message``
     - String
     - Yes
     - User's message (question)
   * - ``sessionId``
     - String
     - No
     - Session ID. Specify when continuing a conversation
   * - ``clear``
     - String
     - No
     - Specify ``"true"`` to clear the session

Response
--------

**On Success (HTTP 200)**

.. code-block:: json

    {
      "status": "ok",
      "sessionId": "abc123def456",
      "content": "Fess is a full-text search server. Key features include...",
      "sources": [
        {
          "title": "Fess Overview",
          "url": "https://fess.codelibs.org/en/overview.html"
        },
        {
          "title": "Feature List",
          "url": "https://fess.codelibs.org/en/features.html"
        }
      ]
    }

**On Error**

.. code-block:: json

    {
      "status": "error",
      "message": "Message is required"
    }

HTTP Status Codes
-----------------

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Code
     - Description
   * - 200
     - Request successful
   * - 400
     - Invalid request parameter (e.g., message is empty)
   * - 404
     - Endpoint not found
   * - 405
     - HTTP method not allowed (only POST is allowed)
   * - 500
     - Internal server error

Usage Examples
--------------

cURL
~~~~

.. code-block:: bash

    # Start a new chat
    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "message=What is Fess?"

    # Continue a conversation
    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "message=How do I install it?" \
         -d "sessionId=abc123def456"

    # Clear session
    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "sessionId=abc123def456" \
         -d "clear=true"

JavaScript
~~~~~~~~~~

.. code-block:: javascript

    async function chat(message, sessionId = null) {
      const params = new URLSearchParams();
      params.append('message', message);
      if (sessionId) {
        params.append('sessionId', sessionId);
      }

      const response = await fetch('/api/v1/chat', {
        method: 'POST',
        body: params
      });

      return await response.json();
    }

    // Usage example
    const result = await chat('Tell me about Fess features');
    console.log(result.content);
    console.log('Session ID:', result.sessionId);

Python
~~~~~~

.. code-block:: python

    import requests

    def chat(message, session_id=None):
        data = {'message': message}
        if session_id:
            data['sessionId'] = session_id

        response = requests.post(
            'http://localhost:8080/api/v1/chat',
            data=data
        )
        return response.json()

    # Usage example
    result = chat('How do I install Fess?')
    print(result['content'])
    print(f"Session ID: {result['sessionId']}")

Streaming API
=============

Endpoint
--------

::

    POST /api/v1/chat/stream
    GET /api/v1/chat/stream

Request Parameters
------------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Type
     - Required
     - Description
   * - ``message``
     - String
     - Yes
     - User's message (question)
   * - ``sessionId``
     - String
     - No
     - Session ID. Specify when continuing a conversation

Response Format
---------------

The Streaming API returns responses in ``text/event-stream`` format (Server-Sent Events).

Each event follows this format:

::

    event: <event_name>
    data: <JSON_data>

SSE Events
----------

**session**

Notifies session information. Sent at the start of the stream.

.. code-block:: json

    {
      "sessionId": "abc123def456"
    }

**phase**

Notifies processing phase start/completion.

.. code-block:: json

    {
      "phase": "intent_analysis",
      "status": "start",
      "message": "Analyzing user intent..."
    }

.. code-block:: json

    {
      "phase": "search",
      "status": "start",
      "message": "Searching documents...",
      "keywords": "Fess installation"
    }

.. code-block:: json

    {
      "phase": "search",
      "status": "complete"
    }

Phase types:

- ``intent_analysis`` - Intent analysis
- ``search`` - Search execution
- ``evaluation`` - Result evaluation
- ``generation`` - Response generation

**chunk**

Notifies generated text fragments.

.. code-block:: json

    {
      "content": "Fess is"
    }

**sources**

Notifies reference document information.

.. code-block:: json

    {
      "sources": [
        {
          "title": "Installation Guide",
          "url": "https://fess.codelibs.org/en/install.html"
        }
      ]
    }

**done**

Notifies processing completion.

.. code-block:: json

    {
      "sessionId": "abc123def456",
      "htmlContent": "<p>Fess is a full-text search server...</p>"
    }

**error**

Notifies errors.

.. code-block:: json

    {
      "phase": "generation",
      "message": "LLM request failed"
    }

Usage Examples
--------------

cURL
~~~~

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v1/chat/stream" \
         -d "message=Tell me about Fess features" \
         -H "Accept: text/event-stream" \
         --no-buffer

JavaScript (EventSource)
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: javascript

    function streamChat(message, sessionId = null) {
      const params = new URLSearchParams();
      params.append('message', message);
      if (sessionId) {
        params.append('sessionId', sessionId);
      }

      // Use fetch for POST requests
      return fetch('/api/v1/chat/stream', {
        method: 'POST',
        body: params
      }).then(response => {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        function read() {
          return reader.read().then(({ done, value }) => {
            if (done) return;

            const text = decoder.decode(value);
            const lines = text.split('\n');

            for (const line of lines) {
              if (line.startsWith('data: ')) {
                const data = JSON.parse(line.slice(6));
                handleEvent(data);
              }
            }

            return read();
          });
        }

        return read();
      });
    }

    function handleEvent(data) {
      if (data.content) {
        // Display chunk
        document.getElementById('output').textContent += data.content;
      } else if (data.phase) {
        // Display phase information
        console.log(`Phase: ${data.phase} - ${data.status}`);
      } else if (data.sources) {
        // Display source information
        console.log('Sources:', data.sources);
      }
    }

Python
~~~~~~

.. code-block:: python

    import requests

    def stream_chat(message, session_id=None):
        data = {'message': message}
        if session_id:
            data['sessionId'] = session_id

        response = requests.post(
            'http://localhost:8080/api/v1/chat/stream',
            data=data,
            stream=True,
            headers={'Accept': 'text/event-stream'}
        )

        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    import json
                    data = json.loads(line[6:])
                    yield data

    # Usage example
    for event in stream_chat('Tell me about Fess features'):
        if 'content' in event:
            print(event['content'], end='', flush=True)
        elif 'phase' in event:
            print(f"\n[Phase: {event['phase']} - {event['status']}]")

Error Handling
==============

Implement appropriate error handling when using the API.

.. code-block:: javascript

    async function chatWithErrorHandling(message, sessionId = null) {
      try {
        const params = new URLSearchParams();
        params.append('message', message);
        if (sessionId) {
          params.append('sessionId', sessionId);
        }

        const response = await fetch('/api/v1/chat', {
          method: 'POST',
          body: params
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.message || 'API request failed');
        }

        const result = await response.json();

        if (result.status === 'error') {
          throw new Error(result.message);
        }

        return result;

      } catch (error) {
        console.error('Chat API error:', error);
        throw error;
      }
    }

Rate Limiting
=============

Rate limits apply to the Chat API.

Default settings:

- 10 requests per minute

When rate limits are exceeded, HTTP 429 error is returned.

For rate limit configuration, see :doc:`../config/rag-chat`.

Security
========

Security considerations when using the Chat API:

1. **Authentication**: The current version does not require API authentication, but consider appropriate access control for production environments
2. **Rate Limiting**: Enable rate limiting to prevent DoS attacks
3. **Input Validation**: Perform input validation on the client side as well
4. **CORS**: Review CORS settings as needed

References
==========

- :doc:`../config/rag-chat` - RAG Chat Configuration
- :doc:`../config/llm-overview` - LLM Integration Overview
- :doc:`../user/chat-search` - End User Chat Search Guide
- :doc:`api-overview` - API Overview
