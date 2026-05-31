===========
Suggest API
===========

Fetching the Suggest Words List
================================

Request
-------

==================  ====================================================
HTTP Method         GET
Endpoint            ``/api/v2/suggest-words``
==================  ====================================================

By sending a request to |Fess| such as ``http://<Server Name>/api/v2/suggest-words?q=fes``, you can receive a list of suggest words for the given prefix in JSON format.
To use the Suggest Words API, you need to enable "Suggest by Document" or "Suggest by Search Word" in the Administration screen under System > General Settings.

For the common response envelope and error model, see :doc:`api-overview`.

Request Parameters
------------------

The available request parameters are as follows:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Request Parameters

   * - q
     - Search term (prefix) for suggestion. (Example) ``q=fes``
   * - num
     - Number of suggested words (integer, >= 0). Default ``10``. (Example) ``num=20``
   * - fn
     - Field name to narrow down suggestion targets. Can be specified multiple times (array). (Example) ``fn=content&fn=title``
   * - lang
     - Search language. Can be specified multiple times (array). (Example) ``lang=en``
   * - label
     - Label name to filter by. Can be specified multiple times (array). (Example) ``label=java``

.. note::

   In v2, field names are specified with the ``fn`` parameter (not ``fields`` as in v1).
   Also, labels are specified with the ``label`` parameter (different from the v1 ``labels`` parameter).

Response
--------

On success, the following response is returned in the common envelope format.

::

    {
      "response": {
        "status": 0,
        "q": "fes",
        "page_size": 10,
        "record_count": 355,
        "query_time": 18,
        "suggest_words": [
          {
            "text": "fess",
            "types": [
              "document",
              "query"
            ]
          }
        ]
      }
    }

Each element of ``response`` is as follows:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Response Information

   * - q
     - The requested search term (string).
   * - page_size
     - Page size (integer).
   * - record_count
     - Number of matching suggest words (64-bit integer).
   * - query_time
     - Query processing time in milliseconds (64-bit integer).
   * - suggest_words
     - Array of suggest words. Each element has ``text`` and ``types``.
   * - text
     - Suggest word (string).
   * - types
     - Array of suggest word types (array of strings).

.. note::

   In v2, suggest item fields are ``text`` and ``types`` (not ``labels`` as in v1).

Usage Examples
==============

Request example using curl:

::

    curl "http://localhost:8080/api/v2/suggest-words?q=fes"

Error Response
==============

When the Suggest API fails, a common error envelope is returned. For details on the error model, see :doc:`api-overview`.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Error Response

   * - Status Code
     - Description
   * - 405 Method Not Allowed
     - An unsupported HTTP method was specified.
   * - 500 Internal Server Error
     - An internal server error occurred.
