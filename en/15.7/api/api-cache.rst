==========
Cache API
==========

This document describes the v2 Cache API of |Fess|.
For the common response envelope, error model, and CSRF, see :doc:`api-overview`.

The base URL is ``http://<Server Name>/api/v2/`` (local environment example: ``http://localhost:8080/api/v2``).

Fetching a Cached Document
============================

Request
-------

==================  ====================================================
HTTP Method         GET
Endpoint            ``/api/v2/cache/{docId}``
==================  ====================================================

Returns the cached HTML of a document that was stored at crawl time. When ``hq`` is specified, the matching terms are highlighted.

This endpoint applies the same permission (role) filtering as search. A document that the caller's roles cannot access returns ``not_found`` (404), just as if it did not exist.

When the login-required setting (System Settings "Login Required") is enabled and the caller is anonymous, it returns ``auth_required`` (401).

Request Parameters
------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Request Parameters

   * - ``docId``
     - Document identifier (path, required, pattern ``^[A-Za-z0-9_-]+$``).
   * - ``hq``
     - Term to highlight (query). When specified, the matching terms in the cached HTML are wrapped with highlight tags. Can be specified multiple times to pass multiple terms (array).

Table: Request Parameters

Response
--------

On success (200), the following fields are returned directly under ``response`` in the common envelope.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "mimetype": "text/html",
        "content": "<html><body>...</body></html>",
        "url": "https://example.com/",
        "created": "2024-05-31T12:00:00.000Z",
        "charset": "UTF-8"
      }
    }

Each field is described below.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Response Fields

   * - ``doc_id``
     - Document ID (str).
   * - ``mimetype``
     - MIME type of the response body (str). Always fixed to ``text/html``.
   * - ``content``
     - Cached HTML body (str). When ``hq`` is specified, the matching terms are highlighted.
   * - ``url``
     - Document URL (str). Returns the ``url_link`` field value if present, otherwise the ``url`` field value from the index. Omitted when neither is available.
   * - ``created``
     - Document creation timestamp (str, ISO 8601 format, e.g. ``2024-05-31T12:00:00.000Z``). Omitted when the index has no value.
   * - ``charset``
     - Character set parsed from the document's mimetype (str). Defaults to ``UTF-8`` when not available.

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
   * - 401 Unauthorized
     - Authentication is required (the login-required setting is enabled with an anonymous caller).
   * - 404 Not Found
     - The document does not exist, has no cached body, or is not accessible with the caller's permissions.
   * - 405 Method Not Allowed
     - The HTTP method is not allowed.
   * - 500 Internal Server Error
     - An internal server error occurred.

Table: Error Response
