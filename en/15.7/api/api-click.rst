================
Click Log API
================

This document describes the v2 Click Log API of |Fess|.
For the common response envelope, error model, and CSRF, see :doc:`api-overview`.

The base URL is ``http://<Server Name>/api/v2/`` (local environment example: ``http://localhost:8080/api/v2``).

Recording a Click
==================

Request
-------

==================  ====================================================
HTTP Method         POST
Endpoint            ``/api/v2/click``
==================  ====================================================

Records a search result click in the search log.
For anonymous callers and installations where the search log feature is disabled, a success response with ``logged: false`` is returned (no error).

Since this is a state-changing request, the ``X-Fess-CSRF-Token`` header is required (see :doc:`api-overview`).

Request Body
------------

Send a JSON (ClickRequest) with ``Content-Type: application/json`` containing the following fields.

::

    {
      "doc_id": "a1b2c3d4e5f6",
      "query_id": "f8b1c2d3e4a5",
      "rank": 1,
      "rt": 1717142400000
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Request Body

   * - ``doc_id``
     - Document ID (str, required, pattern ``^[A-Za-z0-9_-]+$``).
   * - ``query_id``
     - The ``query_id`` returned by the search API (str).
   * - ``rank``
     - 1-based position in the result list (int, ``>=1``).
   * - ``rt``
     - Epoch milliseconds of the original search request (int64). Defaults to the server's current time when not specified.

Table: Request Body

Response
--------

On success (200), the following fields are returned directly under ``response`` in the common envelope.

::

    {
      "response": {
        "status": 0,
        "ok": true,
        "logged": true
      }
    }

Each field is described below.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Response Fields

   * - ``ok``
     - Always ``true`` (bool).
   * - ``logged``
     - ``false`` (bool) when search log persistence is disabled or the caller is anonymous. A ``200`` response is still returned in that case.

Table: Response Fields

Error Response
--------------

For details on the error model, see :doc:`api-overview`. The HTTP statuses returned by this endpoint are as follows.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Error Response

   * - Status Code
     - Description
   * - 400 Bad Request
     - The request is invalid.
   * - 403 Forbidden
     - Not permitted due to missing or expired CSRF token.
   * - 404 Not Found
     - The resource was not found.
   * - 405 Method Not Allowed
     - The HTTP method is not allowed.
   * - 413 Payload Too Large
     - The request body exceeds the size limit.
   * - 415 Unsupported Media Type
     - The ``Content-Type`` is not supported.
   * - 500 Internal Server Error
     - An internal server error occurred.

Table: Error Response
