=====================
Similar Documents API
=====================

This document describes the v2 Similar Documents API of |Fess|, which lists the documents that have the same content as a given document. For the common response envelope and error model, see :doc:`api-overview`.

The base URL is ``http://<Server Name>/api/v2/`` (local environment example: ``http://localhost:8080/api/v2``).

.. note::

   This API finds copies and near-identical documents. It does not find documents that are merely on the same topic (see "Which Documents Are Returned" below).

Listing Similar Documents
=========================

Request
-------

==================  ====================================================
HTTP Method         GET
Endpoint            ``/api/v2/documents/{docId}/similar``
==================  ====================================================

Returns the documents that have the same content signature as the document ``docId``, so that a client can offer a "similar documents" link next to a hit.

- The same role filter, virtual host filter and additional query as ``/api/v2/search`` apply to the given document and to the returned documents. A document that does not exist and a document the caller cannot see both return ``not_found`` (404). The given document, and any other document with the same URL, is never returned.
- With ``login.required=true``, an anonymous caller gets ``auth_required`` (401). An access token can be used the same way as with ``/api/v2/search``.
- Requests are limited to ``api.search.similar.rate.limit.per.minute`` (default: ``30``; ``0`` means unlimited) per minute, counted per logged-in user, or per client IP for a guest. Over the limit the endpoint answers ``429`` with a ``Retry-After`` header.
- Only one page is returned, ordered by URL and then document ID. There is no ``start`` or offset parameter.
- A request for which no virtual host is determined (the default host) gets no virtual host filter, so documents that have a virtual host value are also covered (the same as ``/api/v2/search``). Restrict documents that the users of the default host must not see by role.
- When the content of a document changes and it is crawled again, its ``doc_id`` changes. A saved ``doc_id`` may become ``not_found`` (404) after the re-crawl.

Which Documents Are Returned
----------------------------

|Fess| computes a content signature (``content_minhash_bits``) for each document when it is indexed. The API returns the documents whose signature is the same as that of the given document. It is the grouping used by the duplicate report (:doc:`../admin/docreport-guide`), the ``sdh`` search parameter and the ``similar_docs_*`` fields, but it works without result collapsing.

- The documents are copies or have almost the same content. A document whose content was edited enough to change the signature is not returned, so this is not a search for documents on a similar topic.
- ``data`` is an empty array (not an error) when the given document has no content or no word, and when the search engine runs without the CodeLibs plugins (``search_engine.type`` of ``vanilla``, ``aws`` or the deprecated ``cloud``; see :doc:`../config/search-engine-type`).

Request Parameters
------------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Request Parameters
   :widths: 27 73
   :header-rows: 1

   * - Parameter
     - Description
   * - ``docId``
     - Document identifier (path, required, pattern ``[A-Za-z0-9_-]{1,512}``). A value that does not match produces ``invalid_request`` (400).
   * - ``num``
     - Number of documents to return (query, default ``10``). A value above ``20`` or above ``paging.search.page.max.size`` is reduced to the smaller of the two, and ``page_size`` in the response shows the result. A value of ``0`` or less produces ``invalid_request`` (400). A value that is not a number is ignored and the default is used.

Table: Request Parameters

Response
--------

On success (200), the following fields are returned directly under ``response`` in the common envelope.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "exec_time": "0.01",
        "query_time": 5,
        "page_size": 10,
        "record_count": 1,
        "record_count_relation": "EQUAL_TO",
        "partial": false,
        "timed_out": false,
        "shard_failed": false,
        "data": [
          {
            "doc_id": "f6e5d4c3b2a1",
            "url": "https://example.com/copy/",
            "title": "Example",
            "content_description": "An example document about Fess."
          }
        ]
      }
    }

Each field is described below.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Response Fields
   :widths: 27 73
   :header-rows: 1

   * - Field
     - Description
   * - ``doc_id``
     - ID of the given document.
   * - ``exec_time``
     - Execution time in seconds (a decimal string such as ``"0.01"``).
   * - ``query_time``
     - Search engine query time (int64, milliseconds).
   * - ``page_size``
     - Number of documents asked for, after the limit described above.
   * - ``record_count``
     - Number of documents that have the same signature, not only those in ``data``. The exact count is tracked only up to ``query.track.total.hits`` (default: ``10000``).
   * - ``record_count_relation``
     - When ``EQUAL_TO``, the count is exact; when ``GREATER_THAN_OR_EQUAL_TO``, only the lower bound is known.
   * - ``partial``
     - Whether the result may be incomplete (bool). The query timeout (``query.timeout``) applies, as in a search.
   * - ``timed_out``
     - Whether the query timeout elapsed (bool).
   * - ``shard_failed``
     - Whether one or more shards failed (bool).
   * - ``data``
     - Array of documents, ordered by URL and then document ID. Each element has the same fields as a hit of ``/api/v2/search`` (see :doc:`api-search`), including ``tags`` (the tags visible to the caller, see :doc:`api-tag`). There is no query to highlight, so ``content_description`` is the digest of the content, and there is no ``score``.

Table: Response Fields

Error Response
--------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Error Response
   :widths: 25 75
   :header-rows: 1

   * - Status Code
     - Description
   * - 400 Bad Request
     - ``docId`` does not match the pattern, or ``num`` is ``0`` or less.
   * - 401 Unauthorized
     - Authentication is required (the login-required setting is enabled with an anonymous caller, or the request carries an access token that is not registered or has expired).
   * - 404 Not Found
     - The given document does not exist or is not visible to the caller (``not_found``).
   * - 405 Method Not Allowed
     - The HTTP method is not allowed.
   * - 429 Too Many Requests
     - The per-minute request limit is exceeded. A ``Retry-After`` header gives the number of seconds to wait (``60``).
   * - 500 Internal Server Error
     - An internal server error occurred.
   * - 503 Service Unavailable
     - The search engine could not take the request: it is not reachable, or it refused the request for lack of capacity. ``error.code`` is ``service_unavailable``, and a ``Retry-After`` header gives the number of seconds to wait (``5``). The request itself is fine, so retry after a short wait.

Table: Error Response
