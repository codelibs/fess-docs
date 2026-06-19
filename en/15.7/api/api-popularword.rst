=================
Popular Words API
=================

Fetching the Popular Words List
================================

Request
-------

==================  ====================================================
HTTP Method         GET
Endpoint            ``/api/v2/popular-words``
==================  ====================================================

By sending a request to |Fess| such as ``http://<Server Name>/api/v2/popular-words?seed=123``, you can receive a list of popular search words in JSON format.

If ``web.api.popularword=false``, this API returns ``invalid_request`` (HTTP 400) (equivalent to the "unsupported operation" behavior in v1).

For the common response envelope and error model, see :doc:`api-overview`.

Request Parameters
------------------

The available request parameters are as follows:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Request Parameters

   * - seed
     - Seed for retrieving popular words (string). This value allows you to obtain words in different patterns. (Example) ``seed=123``
   * - label
     - Label name to filter by. Can be specified multiple times (array). (Example) ``label=java``
   * - field
     - Field name used to generate popular words. Can be specified multiple times (array). (Example) ``field=label``

Response
--------

On success, the following response is returned in the common envelope format.

::

    {
      "response": {
        "status": 0,
        "record_count": 3,
        "popular_words": [
          "python",
          "java",
          "javascript"
        ]
      }
    }

Each element of ``response`` is as follows:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Response Information

   * - record_count
     - Number of popular words (integer).
   * - popular_words
     - Array of popular words (array of strings).

.. note::

   In v2, popular words are returned as ``popular_words`` (an array of strings), not ``data`` as in v1.

Usage Examples
==============

Request example using curl:

::

    curl "http://localhost:8080/api/v2/popular-words?seed=123"

Error Response
==============

When the Popular Words API fails, a common error envelope is returned. For details on the error model, see :doc:`api-overview`.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Error Response

   * - Status Code
     - Description
   * - 400 Bad Request
     - The request is invalid (including when the feature is disabled with ``web.api.popularword=false``). The ``error.code`` is ``invalid_request``.
   * - 405 Method Not Allowed
     - An unsupported HTTP method was specified.
   * - 500 Internal Server Error
     - An internal server error occurred.
