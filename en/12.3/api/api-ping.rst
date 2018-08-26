==================
Ping API
==================

Ping API
==========

Ping API returns a server status as JSON format.
URL for Ping API is ``http://<Server Name>/json/?type=ping``.

Request Parameter
--------------------

No request parameter exists.

Response
----------

The response is as below.

::

    {
        "response": {
            "version": 12.3,
            "status":0,
        }
    }

Descriptions for properties are as below.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Properties in Response

   * - response
     - Root element
   * - version
     - API Version.
   * - status
     - Response status. (0: successful, 1: search error, 2 or 3: invalid request parameter, 9: service unavailable, -1: invalid API type)


