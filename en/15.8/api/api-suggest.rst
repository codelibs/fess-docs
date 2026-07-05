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

Suggest words come from three sources:

- **Documents** — Generated from crawled documents. To obtain them, enable "Suggest from Documents" in the Administration screen under System > General.
- **Search terms (search log)** — Generated from users' search logs. To obtain them, enable "Suggest from Search Terms" in the Administration screen under System > General.
- **User dictionary** — Suggest words registered by administrators. These are always returned regardless of the settings above.

Even when "Suggest from Documents" and "Suggest from Search Terms" are disabled, the API does not return an error; the corresponding suggest words are simply omitted from the results.
Suggest words are also automatically filtered based on the roles of the requesting user.

For the common response envelope and error model, see :doc:`api-overview`.

Request Parameters
------------------

The available request parameters are as follows:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Request Parameters

   * - q
     - Search term (prefix) for suggestion. If omitted, suggest words are returned without prefix filtering. (Example) ``q=fes``
   * - num
     - Number of suggested words (integer, >= 0). Default ``10``. If a non-numeric value is specified, the default is used. (Example) ``num=20``
   * - fn
     - Field name to narrow down suggestion targets. Can be specified multiple times (array). (Example) ``fn=content&fn=title``
   * - lang
     - Search language. Can be specified multiple times (array). (Example) ``lang=en``
   * - label
     - Label (tag) name to filter by. Can be specified multiple times (array). The specified values are matched against the ``types`` of each suggest word. (Example) ``label=java``

.. note::

   In v2, field names are specified with the ``fn`` parameter (not ``fields`` as in v1).
   Instead of listing values as a comma-separated string, ``fn`` is repeated to pass multiple values.

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
              "label1"
            ]
          }
        ]
      }
    }

Each element of ``response`` is as follows:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Response Information

   * - q
     - The requested search term (string). Returns an empty string when ``q`` is omitted.
   * - page_size
     - Requested number of suggest words (the value of ``num``, integer).
   * - record_count
     - Total number of matching suggest words (64-bit integer).
   * - query_time
     - Query processing time in milliseconds (64-bit integer).
   * - suggest_words
     - Array of suggest words. Each element has ``text`` and ``types``.
   * - text
     - Suggest word (string).
   * - types
     - Array of tags associated with the suggest word (array of strings). Each tag is derived from the ``label`` or ``virtual_host`` field of a document, or from filter conditions extracted from the search log. Returns an empty array when there are no tags.

.. note::

   ``types`` contains tag values, not the kind of the suggest word (such as ``document`` or ``query``). This array corresponds to the ``labels`` field of suggest items in v1.
   The ``label`` request parameter filters against these ``types`` values.

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
     - An unsupported HTTP method was specified. The ``Allow`` header indicates ``GET``.
   * - 500 Internal Server Error
     - An internal server error occurred.
