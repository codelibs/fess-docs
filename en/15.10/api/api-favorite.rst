==============
Favorites API
==============

This document describes the v2 Favorites API of |Fess|.
For the common response envelope, error model, and CSRF, see :doc:`api-overview`.

The base URL is ``http://<Server Name>/api/v2/`` (local environment example: ``http://localhost:8080/api/v2``).

.. note::

   To use the favorites feature, the ``user.favorite`` setting must be enabled (disabled by default).

Fetching Favorite Documents List
==================================

Request
-------

==================  ====================================================
HTTP Method         GET
Endpoint            ``/api/v2/favorites``
==================  ====================================================

Returns the IDs of documents that the calling user has previously added to favorites, among search results identified by ``query_id``.
``query_id`` is the opaque identifier (``query_id`` field) returned by the search API (``/search``).

An anonymous caller (no user code associated with the session) results in ``auth_required`` (401).
When the ``user.favorite`` feature is disabled, it returns ``invalid_request`` (400).
When ``query_id`` does not match a cached result set in the session, it returns ``200`` with an empty ``data`` array.

Request Parameters
------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Request Parameters

   * - ``query_id``
     - The opaque ``query_id`` returned by the search API (``/search``) (query, required, str).

Table: Request Parameters

Response
--------

On success (200), the following fields are returned directly under ``response`` in the common envelope.

::

    {
      "response": {
        "status": 0,
        "record_count": 2,
        "data": [
          { "doc_id": "a1b2c3d4e5f6" },
          { "doc_id": "f6e5d4c3b2a1" }
        ]
      }
    }

Each field is described below.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Response Fields

   * - ``record_count``
     - Number of favorite documents in ``data`` (int).
   * - ``data``
     - Array of favorite documents in the queried result set, preserving search result order. Each element is ``{doc_id}``.

Table: Response Fields

Error Response
--------------

For details on the error model, see :doc:`api-overview`. The HTTP statuses returned by this endpoint are as follows.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Error Response

   * - Status Code
     - Description
   * - 400 Bad Request
     - The request is invalid (including when the ``user.favorite`` feature is disabled).
   * - 401 Unauthorized
     - Authentication is required (anonymous caller).
   * - 405 Method Not Allowed
     - The HTTP method is not allowed.
   * - 500 Internal Server Error
     - An internal server error occurred.

Table: Error Response

Fetching Favorite Status
==========================

Request
-------

==================  ====================================================
HTTP Method         GET
Endpoint            ``/api/v2/documents/{docId}/favorite``
==================  ====================================================

Retrieves the favorite status of the specified document.

Anonymous (unauthenticated) callers may also use this endpoint. In that case, ``favorite`` returns ``false``, but ``count`` still reflects the stored favorite count (for this reason, this endpoint does not return ``401``).

When the favorites feature (``user.favorite``) is disabled, the endpoint responds with ``invalid_request`` (400).

Request Parameters
------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Request Parameters

   * - ``docId``
     - Document identifier (path, required, pattern ``^[A-Za-z0-9_-]+$``).

Table: Request Parameters

Response
--------

On success (200), the following fields are returned directly under ``response`` in the common envelope.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "favorite": true,
        "count": 5
      }
    }

Each field is described below.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Response Fields

   * - ``doc_id``
     - Document ID (str).
   * - ``favorite``
     - Whether the calling user has favorited this document (bool).
   * - ``count``
     - Total favorite count for this document (int64).

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
   * - 404 Not Found
     - The resource was not found.
   * - 405 Method Not Allowed
     - The HTTP method is not allowed.
   * - 500 Internal Server Error
     - An internal server error occurred.

Table: Error Response

Adding a Favorite
==================

Request
-------

==================  ====================================================
HTTP Method         POST
Endpoint            ``/api/v2/documents/{docId}/favorite``
==================  ====================================================

Adds the specified document to favorites.
Since this is a state-changing request, the ``X-Fess-CSRF-Token`` header is required (see :doc:`api-overview`). In addition, the calling user must be authenticated; anonymous callers receive ``auth_required`` (401).

The ``query_id`` is used to confirm that the target document belongs to a recent search result. When ``query_id`` matches no cached result set in the session, the endpoint responds with ``invalid_request`` (400); when ``docId`` is not contained in that result set, it responds with ``not_found`` (404).

Request Parameters
------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Request Parameters

   * - ``docId``
     - Document identifier (path, required, pattern ``^[A-Za-z0-9_-]+$``).

Table: Request Parameters

Request Body
------------

Send a JSON (FavoritePostRequest) with ``Content-Type: application/json`` (charset UTF-8) containing the following fields. The maximum request body size is 1 KiB (1024 bytes); exceeding this results in ``payload_too_large`` (413).

::

    {
      "query_id": "f8b1c2d3e4a5"
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Request Body

   * - ``query_id``
     - The opaque ``query_id`` returned by the search API (``/search``) (str, required).

Table: Request Body

Response
--------

On success (200), the following fields are returned directly under ``response`` in the common envelope.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "ok": true,
        "favorite": true,
        "count": 6
      }
    }

Each field is described below. The example above is for a new registration; if the favorite was already recorded (an idempotent re-POST), the response additionally includes the ``already_existed`` field (set to ``true``).

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Response Fields

   * - ``doc_id``
     - Document ID (str).
   * - ``ok``
     - Always ``true`` (bool).
   * - ``favorite``
     - Always ``true`` (bool). Whether a new addition or an existing one, the document becomes a favorite of the calling user.
   * - ``count``
     - Current favorite count after the operation (int64). For a new addition, optimistically count + 1 before update; for an idempotent re-POST, reflects the stored count.
   * - ``already_existed``
     - ``true`` if the favorite had been registered previously (bool, idempotent re-POST). Not present in the initial POST that newly registers a favorite.

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
     - Authentication is required.
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
