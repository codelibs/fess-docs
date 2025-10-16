==========
Search API
==========

Fetching Search Results
=======================

You can retrieve search results from |Fess| in JSON format by sending a request to ``http://<Server Name>/api/v1/documents?q=search term``. To use the search API, you need to enable JSON responses in the Administration screen under "General Settings."

Request Parameters
------------------

You can specify request parameters to perform advanced searches, such as ``http://<Server Name>/api/v1/documents?q=search term&num=50&fields.label=fess``. The available request parameters are as follows:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - q
     - The search term. Encode it in the URL.
   * - start
     - The starting position of the search results. It starts from 0.
   * - num
     - The number of results to display. The default is 20, and you can display up to 100.
   * - sort
     - Sorting. Used to sort the search results.
   * - fields.label
     - Label value. Used to specify a label.
   * - facet.field
     - Specify a facet field. (e.g., ``facet.field=label``)
   * - facet.query
     - Specify a facet query. (e.g., ``facet.query=timestamp:[now/d-1d TO *]``)
   * - facet.size
     - Specify the maximum number of facets to retrieve. This is valid when facet.field is specified.
   * - facet.minDocCount
     - Retrieve facets with a count equal to or greater than this value. This is valid when facet.field is specified.
   * - geo.location.point
     - Specify latitude and longitude. (e.g., ``geo.location.point=35.0,139.0``)
   * - geo.location.distance
     - Specify the distance from the center point. (e.g., ``geo.location.distance=10km``)
   * - lang
     - Specify the search language. (e.g., ``lang=en``)
   * - preference
     - Specify a string to determine the shard to use during search. (e.g., ``preference=abc``)
   * - callback
     - The callback name when using JSONP. It is not necessary to specify if JSONP is not used.

Table: Request Parameters

Response
--------

| The response returned will be as follows:
| (Formatted version)

::

    {
      "q": "Fess",
      "query_id": "bd60f9579a494dfd8c03db7c8aa905b0",
      "exec_time": 0.21,
      "query_time": 0,
      "page_size": 20,
      "page_number": 1,
      "record_count": 31625,
      "page_count": 1,
      "highlight_params": "&hq=n2sm&hq=Fess",
      "next_page": true,
      "prev_page": false,
      "start_record_number": 1,
      "end_record_number": 20,
      "page_numbers": [
        "1",
        "2",
        "3",
        "4",
        "5"
      ],
      "partial": false,
      "search_query": "(Fess OR n2sm)",
      "requested_time": 1507822131845,
      "related_query": [
        "aaa"
      ],
      "related_contents": [],
      "data": [
        {
          "filetype": "html",
          "title": "Open Source Enterprise Search Server: Fess — Fess 11.0 documentation",
          "content_title": "Open Source Enterprise Search Server: Fess — Fe...",
          "digest": "Docs » Open Source Enterprise Search Server: Fess Commercial Support Open Source Enterprise Search Server: Fess What is Fess? Fess is a powerful and easily deployable Enterprise Search Server. ...",
          "host": "fess.codelibs.org",
          "last_modified": "2017-10-09T22:28:56.000Z",
          "content_length": "29624",
          "timestamp": "2017-10-09T22:28:56.000Z",
          "url_link": "https://fess.codelibs.org/",
          "created": "2017-10-10T15.30:48.609Z",
          "site_path": "fess.codelibs.org/",
          "doc_id": "e79fbfdfb09d4bffb58ec230c68f6f7e",
          "url": "https://fess.codelibs.org/",
          "content_description": "Enterprise Search Server: Fess Commercial Support Open...Search Server: Fess What is Fess? Fess is a very powerful...You can quickly install and run Fess on any platform...Fess is provided under the Apache license...Apache license. Demo Fess is an OpenSearch-based search",
          "site": "fess.codelibs.org/",
          "boost": "10.0",
          "mimetype": "text/html"
        }
      ]
    }

The response will be as follows:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Response Information

   * - q
     - Search term
   * - exec_time
     - Response time (in seconds)
   * - query_time
     - Query processing time (in milliseconds)
   * - page_size
     - Number of items per page
   * - page_number
     - Page number
   * - record_count
     - Total number of hits for the search term
   * - page_count
     - Number of pages for the search term
   * - highlight_params
     - Highlighting parameters
   * - next_page
     - true: Next page exists, false: Next page does not exist
   * - prev_page
     - true: Previous page exists, false: Previous page does not exist
   * - start_record_number
     - Starting record number
   * - end_record_number
     - Ending record number
   * - page_numbers
     - Array of page numbers
   * - partial
     - true if the search was truncated due to a timeout or other reasons
   * - search_query
     - Search query
   * - requested_time
     - Request time (in epoch milliseconds)
   * - related_query
     - Related queries
   * - related_contents
     - Queries related to the content
   * - facet_field
     - Information about documents that match the given facet field (only if the request parameter "facet.field" is provided)
   * - facet_query
     - Number of documents that match the given facet query (only if the request parameter "facet.query" is provided)
   * - result
     - Parent element of search results
   * - filetype
     - File type
   * - created
     - Document creation date and time
   * - title
     - Document title
   * - doc_id
     - Document ID
   * - url
     - Document URL
   * - site
     - Site name
   * - content_description
     - Description of the content
   * - host
     - Host name
   * - digest
     - Digest string of the document
   * - boost
     - Document boost value
   * - mimetype
     - MIME type
   * - last_modified
     - Last modified date and time
   * - content_length
     - Document size
   * - url_link
     - URL as part of the search result
   * - timestamp
     - Document update date and time


Searching All Documents
=======================

To search all documents, send the following request: ``http://<Server Name>/api/v1/documents/all?q=search_term```

To use this feature, you need to set ``api.search.scroll`` to true in the ``fess_config.properties`` file.

Request Parameters
------------------

The available request parameters are as follows:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - q
     - Search term. Pass it after URL encoding.
   * - num
     - Number of items to display. The default value is 20, and you can display up to 100 items.
   * - sort
     - Sort order. Used to sort the search results.

Table: Request Parameters
