===========
Suggest API
===========

Fetching Suggest Words List
============================

Request
-------

==================  ====================================================
HTTP Method         GET
Endpoint            ``/api/v1/suggest-words``
==================  ====================================================

By sending a request to |Fess| at ``http://<Server Name>/api/v1/suggest-words?q=suggest_word``, you can receive a list of suggest words registered in |Fess| in JSON format.
To use the Suggest Words API, you need to enable "Suggest by Document" or "Suggest by Search Word" in the Administration screen under System > General Settings.

Request Parameters
------------------

The available request parameters are as follows:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Request Parameters

   * - q
     - Keyword for suggestion. (Example) ``q=fess``
   * - num
     - Number of suggested words. Default is 10. (Example) ``num=20``
   * - label
     - Filtered label name. (Example) ``label=java``
   * - fields
     - Field name to narrow down suggestion targets. Default is no filtering. (Example) ``fields=content,title``
   * - lang
     - Search language specification. (Example) ``lang=en``


Response
--------

The following response is returned:

::

    {
      "query_time": 18,
      "record_count": 355,
      "page_size": 10,
      "data": [
        {
          "text": "fess",
          "labels": [
            "java",
            "python"
          ]
        }
      ]
    }

Each element is as follows:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Response Information

   * - query_time
     - Query processing time (in milliseconds).
   * - record_count
     - Number of registered suggest words.
   * - page_size
     - Page size.
   * - data
     - Parent element of search results.
   * - text
     - Suggest word.
   * - labels
     - Array of label values.

Error Response
==============

When the suggest API fails, the following error response is returned:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Error Response

   * - Status Code
     - Description
   * - 400 Bad Request
     - When request parameters are invalid
   * - 500 Internal Server Error
     - When an internal server error occurs
