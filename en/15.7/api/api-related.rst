================================
Related Queries and Content API
================================

This page describes two endpoints for retrieving related information for a query.

- ``GET /related-queries`` — Retrieves related query suggestions for a query.
- ``GET /related-content`` — Retrieves related HTML content for a query.

For the common response envelope and error model, see :doc:`api-overview`.

Fetching Related Queries
=========================

Request
-------

==================  ====================================================
HTTP Method         GET
Endpoint            ``/api/v2/related-queries``
==================  ====================================================

By sending a request to |Fess| such as ``http://<Server Name>/api/v2/related-queries?q=fess``, you can receive a list of related query terms for the specified query in JSON format.

If ``q`` is empty or not specified, no error is returned; instead, an empty ``queries`` array is returned. The response is always a success envelope.

Request Parameters
------------------

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Request Parameters

   * - q
     - Search term for which to retrieve related queries. (Example) ``q=fess``

Response
--------

On success, the following response is returned in the common envelope format.

::

    {
      "response": {
        "status": 0,
        "queries": [
          "fess search",
          "fess install"
        ]
      }
    }

Each element of ``response`` is as follows:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Response Information

   * - queries
     - Array of related query terms (array of strings). Returns an empty array when ``q`` is empty or not specified.

Error Response
~~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Error Response

   * - Status Code
     - Description
   * - 405 Method Not Allowed
     - An unsupported HTTP method was specified.
   * - 500 Internal Server Error
     - An internal server error occurred.

Fetching Related Content
=========================

Request
-------

==================  ====================================================
HTTP Method         GET
Endpoint            ``/api/v2/related-content``
==================  ====================================================

By sending a request to |Fess| such as ``http://<Server Name>/api/v2/related-content?q=fess``, you can receive related HTML content for the specified query in JSON format.

If multiple content items match, they are concatenated with newlines.
If ``q`` is empty or not specified, no error is returned; instead, an empty string ``content`` is returned. The response is always a success envelope.

Request Parameters
------------------

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Request Parameters

   * - q
     - Search term for which to retrieve related content. (Example) ``q=fess``

Response
--------

On success, the following response is returned in the common envelope format.

::

    {
      "response": {
        "status": 0,
        "content": "<div>...related HTML content...</div>",
        "content_type": "html"
      }
    }

Each element of ``response`` is as follows:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Response Information

   * - content
     - Related HTML content (string). When multiple items match, they are concatenated with newlines. Returns an empty string when ``q`` is empty or not specified.
   * - content_type
     - Content type. The value is always ``html``.

Error Response
~~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Error Response

   * - Status Code
     - Description
   * - 405 Method Not Allowed
     - An unsupported HTTP method was specified.
   * - 500 Internal Server Error
     - An internal server error occurred.
