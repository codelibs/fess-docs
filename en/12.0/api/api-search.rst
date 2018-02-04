==================
Search API
==================

.. TODO: lang, ex_q

Search API
==============

Search API returns search results from |Fess| as JSON format.
URL for Search API is ``http://<Server Name>/json/?q=WORD``.
To enable JSON Response at System > General in Administrative page, Search API becomes available.

Request Parameters
--------------------

Search API contains optional parameters for advance searchs, such as ``http://<Server Name>/json/?q=WORD&num=50&field.label=fess``.
Available parameters are as below.

.. TODO: facet.field, facet.query の説明を詳しく

.. list-table:: Request Parameters

   * - q
     - Search query. URL-encode is needed.
   * - start
     - Start position. It is started from 0.
   * - num*
     - The number of returned documents as a search result. The default is 20.
   * - fields.label
     - Label value for filtering a search result.
   * - callback
     - Callback function name. If using JSONP, set this value,
   * - facet.field
     - Facet field. ex. ``facet.field=label``
   * - facet.query
     - Facet query. ex. ``facet.query=timestamp:[now/d-1d TO *]``
   * - facet.size
     - The number of a returned facet for specifying facet.field.
   * - facet.minDocCount
     - Minimum document size in a facet for facet.field.


Response
----------

::

   {
     "response": {
       "version": 12.0,
       "status": 0,
       "q": "Fess",
       "query_id": "bd60f9579a494dfd8c03db7c8aa905b0",
       "exec_time": 0.21,
       "query_time": 171,
       "page_size": 20,
       "page_number": 1,
       "record_count": 31625,
       "page_count": 1582,
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
         "5",
         "6"
       ],
       "partial": false,
       "search_query": "(Fess OR n2sm)",
       "requested_time": 1507822131845,
       "related_query": [
         "n2sm"
       ],
       "related_contents": [],
       "result": [
         {
           "filetype": "html",
           "title": "Open Source Enterprise Search Server: Fess — Fess 11.0 documentation",
           "content_title": "Open Source Enterprise Search Server: Fess — Fe...",
           "digest": "Docs » Open Source Enterprise Search Server: Fess Commercial Support Open Source Enterprise Search Server: Fess What is Fess ? Fess is very powerful and easily deployable Enterprise Search Server. ...",
           "host": "fess.codelibs.org",
           "last_modified": "2017-10-09T22:28:56.000Z",
           "content_length": "29624",
           "timestamp": "2017-10-09T22:28:56.000Z",
           "url_link": "https://fess.codelibs.org/",
           "created": "2017-10-10T15:00:48.609Z",
           "site_path": "fess.codelibs.org/",
           "doc_id": "e79fbfdfb09d4bffb58ec230c68f6f7e",
           "url": "https://fess.codelibs.org/",
           "content_description": "Enterprise Search Server: <strong>Fess</strong> Commercial Support Open...Search Server: <strong>Fess</strong> What is <strong>Fess</strong> ? <strong>Fess</strong> is very powerful...You can install and run <strong>Fess</strong> quickly on any platforms...Java runtime environment. <strong>Fess</strong> is provided under Apache...Apache license. Demo <strong>Fess</strong> is Elasticsearch-based search",
           "site": "fess.codelibs.org/",
           "boost": "10.0",
           "mimetype": "text/html"
         },

         ...

       ]
     }
   }

Descriptions for properties are as below.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Properties in Response

   * - response
     - Root element.
   * - version
     - API Version.
   * - status
     - Response status. (0: successful, 1: search error, 2 or 3: invalid request parameter, 9: service unavailable, -1: invalid API type)
   * - q
     - Search query.
   * - exec_time
     - Response time. (ms)
   * - query_time
     - Query time. (ms)
   * - page_size
     - Returned document size.
   * - page_number
     - Page number.
   * - record_count
     - Total hit count.
   * - page_count
     - The number of pages.
   * - highlight_params
     - Highlight parameters.
   * - next_page
     - true: next pages exist. false: it does not exist.
   * - prev_page
     - true: previous pages exist. false: it does not exist.
   * - start_record_number
     - Start position in a search result.
   * - end_record_number
     - End position in a search result.
   * - page_numbers
     - List of page numbers.
   * - partial
     - true if a request is timeouted.
   * - search_query
     - Search query.
   * - requested_time
     - Request timestamp.
   * - related_query
     - Related query.
   * - related_contents
     - Related contents.
   * - facet_field
     - Facet information for specified facet.field.
   * - facet_query
     - Facet information for specified facet.query.
   * - geo_distance
     - Geo information.
   * - result
     - Search result element.
   * - filetype
     - File type.
   * - created
     - Timestamp for registering a document in an index.
   * - title
     - Document title.
   * - doc_id
     - Document ID.
   * - url
     - URL.
   * - site
     - Site name for URL.
   * - content_description
     - Document description.
   * - host
     - Hostname.
   * - digest
     - Document summary.
   * - boost
     - Boost value.
   * - mimetype
     - MIME type.
   * - last_modified
     - Last modified time.
   * - content_length
     - Document size.
   * - url_link
     - URL as a search result.
   * - timestamp
     - Document timestamp.

