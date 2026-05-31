==========
Search API
==========

This document describes the v2 Search API of |Fess|.
For the common response envelope, error model, and CSRF, see :doc:`api-overview`.

The base URL is ``http://<Server Name>/api/v2/`` (local environment example: ``http://localhost:8080/api/v2``).

Document Search
===============

Request
-------

==================  ====================================================
HTTP Method         GET
Endpoint            ``/api/v2/search``
==================  ====================================================

Searches for documents matching the query and returns the results in a common envelope.
All field names in the payload use ``snake_case``.

Request Parameters
~~~~~~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Request Parameters

   * - ``q``
     - Search term (URL-encoded).
   * - ``start``
     - Zero-based start position (integer, ``>=0``, default ``0``).
   * - ``offset``
     - Offset from ``start`` (integer, ``>=0``, default ``0``).
   * - ``num``
     - Page size (integer, ``>=1``, default ``20``). A value of ``<= 0`` results in ``invalid_request``. Values exceeding the configured maximum are silently clamped. Whether clamping occurred can be detected by comparing the request ``num`` with the response ``page_size``.
   * - ``sort``
     - Sort order (e.g., ``score``).
   * - ``lang``
     - Search language. Can be specified multiple times (array). Example: ``en``.
   * - ``ex_q``
     - Additional query expression. Can be specified multiple times.
   * - ``sdh``
     - Similar-document hash.
   * - ``fields.label``
     - Filter by label name. Can be specified multiple times. This is the most common case of the general ``fields.<name>`` family; any ``fields.<name>`` query parameter narrows results to documents where field ``<name>`` matches the specified value.
   * - ``as.*``
     - Advanced search conditions. Any ``as.<name>`` (e.g., ``as.q``, ``as.filetype``) is passed to the advanced search condition builder. Can be specified multiple times per name.
   * - ``track_total_hits``
     - Forwarded to the search engine to control accurate hit count (e.g., ``true`` or an integer threshold). Affects whether ``record_count_relation`` is ``eq`` or ``gte``.
   * - ``facet.field``
     - Facet field. Can be specified multiple times (array).
   * - ``facet.query``
     - Facet query. Can be specified multiple times (array).
   * - ``facet.size``
     - Maximum number of facet terms to return (integer).
   * - ``facet.minDocCount``
     - Minimum number of documents a facet term must appear in (integer).
   * - ``facet.sort``
     - Facet sort order.
   * - ``facet.missing``
     - How to handle faceting for documents that do not have a value.
   * - ``geo.location.point``
     - Center point for geographic coordinates (e.g., ``35.0,139.0``).
   * - ``geo.location.distance``
     - Distance from the center point (e.g., ``10km``).

Table: Request Parameters

Response
--------

On success (200), the following fields are returned directly under ``response`` in the common envelope.

::

    {
      "response": {
        "status": 0,
        "q": "Fess",
        "query_id": "f8b1c2d3e4a5",
        "exec_time": 0.012,
        "query_time": 8,
        "page_size": 20,
        "page_number": 1,
        "record_count": 42,
        "record_count_relation": "eq",
        "page_count": 3,
        "highlight_params": "&hq=Fess",
        "next_page": true,
        "prev_page": false,
        "start_record_number": 1,
        "end_record_number": 20,
        "page_numbers": ["1", "2", "3"],
        "partial": false,
        "search_query": "title:Fess OR content:Fess",
        "requested_time": 1717142400000,
        "related_query": ["enterprise search"],
        "related_contents": [],
        "data": [
          {
            "doc_id": "a1b2c3d4e5f6",
            "url": "https://example.com/",
            "title": "Example",
            "content_description": "An example document about Fess.",
            "score": 1.2345
          }
        ],
        "facet_field": [
          {
            "name": "label",
            "result": [
              { "value": "news", "count": 12 }
            ]
          }
        ],
        "facet_query": [
          { "value": "filetype:html", "count": 30 }
        ]
      }
    }

Each field is described below.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Response Fields

   * - ``q``
     - Search term (nullable).
   * - ``query_id``
     - Query identifier.
   * - ``exec_time``
     - Execution time (double, seconds).
   * - ``query_time``
     - Search engine query time (int64, milliseconds).
   * - ``page_size``
     - Page size.
   * - ``page_number``
     - Current page number.
   * - ``record_count``
     - Number of hits (int64).
   * - ``record_count_relation``
     - When ``eq``, the count is exact; when ``gte``, only the lower bound is known.
   * - ``page_count``
     - Total number of pages.
   * - ``highlight_params``
     - Query parameter string for highlighting.
   * - ``next_page``
     - Whether there is a next page (bool).
   * - ``prev_page``
     - Whether there is a previous page (bool).
   * - ``start_record_number``
     - Starting record number for this page.
   * - ``end_record_number``
     - Ending record number for this page.
   * - ``page_numbers``
     - Array of page numbers to display in the pager (strings).
   * - ``partial``
     - Whether the result is partial (bool).
   * - ``search_query``
     - The actual search query that was executed.
   * - ``requested_time``
     - Request timestamp (int64, epoch milliseconds).
   * - ``related_query``
     - Array of related queries (strings).
   * - ``related_contents``
     - Array of related content (strings).
   * - ``data``
     - Array of search results; one element per document. Only fields permitted by ``QueryFieldConfig#isApiResponseField`` are included; null values and empty keys are excluded.
   * - ``facet_field``
     - Array present only when facet fields were requested. Each element is ``{name, result:[{value, count}]}``.
   * - ``facet_query``
     - Array present only when facet queries were requested. Each element is ``{value, count}``.

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
   * - 405 Method Not Allowed
     - The HTTP method is not allowed.
   * - 500 Internal Server Error
     - An internal server error occurred.

Table: Error Response

Fetching All Documents (Scroll Search / NDJSON)
===============================================

Request
-------

==================  ====================================================
HTTP Method         GET
Endpoint            ``/api/v2/documents/all``
==================  ====================================================

Streams all documents matching the query as NDJSON (``application/x-ndjson``).
Each line is a ``{"data":{...}}`` object containing fields permitted by ``QueryFieldConfig#isApiResponseField``.

If a failure occurs mid-stream, the final line is flushed as follows:

::

    {"error":{"code":"internal_error","message":"stream error"}}

Therefore, clients must check the first key of the last line to distinguish successful completion (``data``) from a server error (``error``).

The query is built using the same parameter set as ``GET /search`` (``q``, ``sort``, ``num``, ``lang``, ``ex_q``, ``sdh``, ``fields.*``, ``as.*``, ``track_total_hits``, ``facet.*``, ``geo.*``).
If scroll search is disabled with ``api.search.scroll=false``, the endpoint returns ``invalid_request`` (400).

Request Parameters
~~~~~~~~~~~~~~~~~~

The parameters explicitly specified in the spec are as follows.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Request Parameters

   * - ``q``
     - Search term.
   * - ``sort``
     - Sort order.
   * - ``num``
     - Page (scroll batch) size (integer, ``>=1``). A value of ``<= 0`` results in ``invalid_request``.
   * - ``lang``
     - Search language. Can be specified multiple times (array).
   * - ``ex_q``
     - Additional query expression. Can be specified multiple times (array).
   * - ``fields.label``
     - Filter by label name. Can be specified multiple times (array). Part of the general ``fields.<name>`` family (see ``GET /search``).
   * - ``sdh``
     - Similar-document hash.

Table: Request Parameters

Response
--------

On success (200), the Content-Type is ``application/x-ndjson``, with one document per line as shown below.

::

    {"data":{"url":"https://example.com/","title":"Example"}}
    {"data":{"url":"https://example.org/","title":"Example Org"}}

Error Response
--------------

For details on the error model, see :doc:`api-overview`. The HTTP statuses returned by this endpoint are as follows.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Error Response

   * - Status Code
     - Description
   * - 400 Bad Request
     - Invalid query, ``num <= 0``, or scroll search disabled with ``api.search.scroll=false``.
   * - 405 Method Not Allowed
     - The HTTP method is not allowed.
   * - 500 Internal Server Error
     - An internal server error occurred.

Table: Error Response
