========
Ping API
========

Get Status
==========

By sending a request to ``http://<Server Name>/api/v1/health`` to |Fess|, you can receive the server status of |Fess| in JSON format.

Request Parameters
------------------

There are no available request parameters.

Response
--------

The response will be as follows:

::

    {
      "data": {
        "status": "green",
        "timed_out": false
      }
    }

The elements in the response are described as follows:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - data
     - The parent element of the response.
   * - status
     - The status of the response. "green" is returned for normal status.
   * - timed_out
     - The response result. "false" is returned if the response is received within the specified time.

Table: Response Information