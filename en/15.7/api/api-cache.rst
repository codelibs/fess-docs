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

Returns the cached (highlight-applied) HTML of a document.

When the login-required setting (System Settings "Login Required") is enabled and the caller is anonymous, it returns ``auth_required`` (401).

Request Parameters
------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Request Parameters

   * - ``docId``
     - Document identifier (path, required, pattern ``^[A-Za-z0-9_-]+$``).
   * - ``hq``
     - Highlight query term (query). Can be specified multiple times (array).

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
     - MIME type (enum: ``text/html``).
   * - ``content``
     - Cached HTML body (str).
   * - ``url``
     - Document URL (str). Uses the ``url_link`` field from the index if present, otherwise the raw index URL. Omitted when neither is available.
   * - ``created``
     - Document creation timestamp from the index (str). Omitted when not present.
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
     - The resource was not found.
   * - 405 Method Not Allowed
     - The HTTP method is not allowed.
   * - 500 Internal Server Error
     - An internal server error occurred.

Table: Error Response
