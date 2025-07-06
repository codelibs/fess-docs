========
JSON API
========

JSON API
========

|Fess| supports JSON API response.

Request
-------

The request URL for JSON API is ``http://localhost:8080/json?q=SearchWords``.
Available request parameters are as below.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - q
     - Search query.
   * - start
     - Start position(default 0)
   * - num
     - The number of documents in search result page to display them(default 20).
   * - fields.label
     - Label to filter documents with the label.
   * - callback
     - JSONP callback name. (default response is JSON)
   * - facet.field
     - Facet Field query. ex. facet.field=label
   * - facet.query
     - Facet query. ex. facet.query=timestamp:[now/d-1d TO \*]
   * - facet.size
     - The number of facet results.

Table: Request parameters


Response
--------

Response example is as below.

::

    {
        "response": {
            "version": 15.1,
            "status": 0,
            "q": "Apple",
            "exec_time": 0.11,
            "query_time": 55,
            "page_size": 20,
            "page_number": 1,
            "record_count": 178,
            "page_count": 9,
            "result": [
                {
                    "filetype": "html",
                    "url_link": "https://www.yahoo.com/155245319.html",
                    "created": "2016-08-31T17:28:27.489Z",
                    "site_path": "www.yahoo.com/beauty/13-reasons-apple-cider-vin...",
                    "title": "13 Reasons Apple Cider Vinegar Is the Magic Potion You Need in Your Life",
                    "doc_id": "f269c7ade50f475ca5dc2112ee5f2d7f",
                    "url": "https://www.yahoo.com/155245319.html",
                    "content_description": "GoodsConfidenceDudes FoodVideoHo <strong>Apple</strong> cider ...",
                    "content_title": "13 Reasons Apple Cider Vinegar Is the Magic Pot...",
                    "site": "www.yahoo.com/beauty/13-reasons-apple-cider-vin...",
                    "host": "www.yahoo.com",
                    "digest": "Science says the grocery store staple can be crazy effective.",
                    "boost": "1.0",
                    "mimetype": "text/html",
                    "content_length": "583740",
                    "timestamp": "2016-08-31T17:28:27.489Z"
                },
    ...
            ]
        }
    }

Each element is as follows.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - response
     - The root element.
   * - version
     - Format version.
   * - status
     - The status of the response. the status value is 0: normal, 1: search error, 2 or 3: request parameter error, 9: in service, 1: API type of error is.
   * - query
     - Search query.
   * - exec_time
     - Response time(seconds).
   * - page_size
     - The number of documents in search result.
   * - page_number
     - Page number.
   * - record_count
     - The number of hits for the search query.
   * - page_count
     - Total page size.
   * - result
     - Parent element of the search results.
   * - site
     - Site name.
   * - content_description
     - Description of the document.
   * - host
     - Host name.
   * - last_modified
     - Last modified date.
   * - cache
     - Content cache.
   * - score
     - Search score of the document.
   * - digest
     - Digest content of the document.
   * - created
     - Indexed date.
   * - url
     - URL of the document.
   * - doc_id
     - ID of the document.
   * - mimetype
     - MIME type.
   * - title
     - Title of the document.
   * - content_title
     - Title of the document for search view.
   * - content_length
     - Size of the document.
   * - url_link
     - URL as the search results.

Table: Response information


