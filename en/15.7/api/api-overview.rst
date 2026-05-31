============
API Overview
============


APIs Provided by |Fess|
=======================

This document describes the Web API (v2) provided by |Fess|.
By using the API, you can use |Fess| as a search server from existing web systems, single-page applications (SPAs), and other clients.

.. note::

   In |Fess| 15.7, the API has been updated to **v2**. The former ``/api/v1``
   JSON search API and chat API have been discontinued and consolidated into ``/api/v2``.
   Clients using ``/api/v1`` should migrate to ``/api/v2``.

Base URL
========

The |Fess| v2 API endpoints are provided at the following base URL:

::

    http://<Server Name>/api/v2/

For example, when running in a local environment:

::

    http://localhost:8080/api/v2/

Response Envelope
=================

All v2 JSON responses are returned in a common envelope structure.

::

    {
      "response": {
        "status": 0,
        ...
      }
    }

``response.status`` represents the processing result, following the convention established in v1.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Values of status

   * - 0
     - Success
   * - 1
     - Client error
   * - 9
     - System error

Table: Values of status

Note that ``response.status >= 1`` always corresponds to an HTTP status code of ``400`` or higher.

Field Names
-----------

All JSON keys — including request bodies, response bodies, and SSE event data — use ``snake_case`` consistently.

Error Response
==============

On error, an ``error`` object is added to the envelope.

::

    {
      "response": {
        "status": 1,
        "error": {
          "code": "invalid_request",
          "message": "..."
        }
      }
    }

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Elements of error

   * - code
     - A stable error code (``snake_case``). Clients are recommended to use this value for localization.
   * - message
     - A human-readable error message (in English). When displaying messages, clients should localize based on ``code``.

Table: Elements of error

Error Codes and HTTP Status Codes
----------------------------------

The default HTTP status code is determined by ``error.code``.

.. tabularcolumns:: |p{5cm}|p{3cm}|p{7cm}|
.. list-table:: Error Code List

   * - error.code
     - HTTP Status
     - Description
   * - ``invalid_request``
     - 400
     - The request is invalid.
   * - ``auth_required``
     - 401
     - Authentication is required, or the credentials are invalid.
   * - ``forbidden``
     - 403
     - Not permitted (e.g., missing or expired CSRF token).
   * - ``not_found``
     - 404
     - The resource was not found.
   * - ``method_not_allowed``
     - 405
     - The HTTP method is not allowed. Supported methods are listed in the ``Allow`` header.
   * - ``not_acceptable``
     - 406
     - The request is not acceptable.
   * - ``conflict``
     - 409
     - A resource conflict occurred.
   * - ``payload_too_large``
     - 413
     - The request body exceeds the size limit.
   * - ``unsupported_media_type``
     - 415
     - The ``Content-Type`` is not supported (most endpoints require ``application/json``).
   * - ``rate_limited``
     - 429
     - The rate limit has been exceeded. The ``Retry-After`` header indicates the number of seconds to wait.
   * - ``internal_error``
     - 500
     - An internal server error occurred.
   * - ``service_unavailable``
     - 503
     - The service is temporarily unavailable.

Table: Error Code List

.. note::

   Responses with ``method_not_allowed`` include an ``Allow`` header listing
   the supported HTTP methods.

Authentication and Sessions
===========================

The v2 API uses session-based authentication.
Log in via ``POST /auth/login``; on success, a session is established and a CSRF token is issued.
The current authentication state can be checked with ``GET /auth/me``. See :doc:`api-auth` for details.

Endpoints such as search that do not require login can be used anonymously (depending on settings such as ``app.login.required``).

CSRF Token
----------

Requests that change state (``POST`` / ``PUT`` / ``DELETE``) require the ``X-Fess-CSRF-Token`` header.
A CSRF token can be obtained in the following ways:

- The ``csrf_token`` field in the response from ``POST /auth/login``
- The response from ``GET /ui/config`` (the ``csrf_token`` field when ``csrf_required=true``)

The token is rotated on every login, logout, and password change.

.. note::

   CSRF validation is performed **before** authentication. Therefore, a state-changing request
   that has neither a valid session nor a valid CSRF token will receive
   ``403 forbidden`` rather than ``401 auth_required``.
   ``/auth/login`` is exempt from CSRF validation because no token exists before login.

Streaming Format
================

Some endpoints return responses in a streaming format rather than plain JSON.

.. tabularcolumns:: |p{4cm}|p{4cm}|p{7cm}|
.. list-table:: Streaming Formats

   * - Endpoint
     - Content-Type
     - Description
   * - ``/chat/stream``
     - ``text/event-stream``
     - Server-Sent Events (SSE). See :doc:`api-chat` for details.
   * - ``/documents/all``
     - ``application/x-ndjson``
     - NDJSON (each line is one document in ``{"data":{...}}`` format. Only if a failure occurs mid-stream does the final line become ``{"error":{...}}``). See :doc:`api-search` for details.

Table: Streaming Formats

Types of APIs
=============

|Fess| provides the following v2 APIs.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - search
     - API for searching documents, retrieving label lists, and fetching all documents (scroll).
   * - suggest
     - API for retrieving suggest words.
   * - popularword
     - API for retrieving popular words.
   * - related
     - API for retrieving related queries and related content.
   * - monitor
     - API for retrieving the state of the server (search engine cluster).
   * - auth
     - API for authentication and session operations (login, logout, authentication state retrieval, password change).
   * - ui
     - API for retrieving initial configuration (UI settings) for SPAs.
   * - favorite
     - API for managing favorite documents.
   * - click
     - API for recording search result clicks.
   * - cache
     - API for retrieving cached document content.
   * - chat
     - API for using the AI search mode (RAG chat) feature.

Table: Types of APIs
