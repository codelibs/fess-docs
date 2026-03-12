==========
Health API
==========

Fetching Status
===============

Request
-------

==================  ====================================================
HTTP Method         GET
Endpoint            ``/api/v1/health``
==================  ====================================================

By sending a request to |Fess| at ``http://<Server Name>/api/v1/health``, you can receive the server status of |Fess| in JSON format.

Request Parameters
------------------

There are no request parameters that can be specified.

Response
--------

The following response is returned:

::

    {
      "data": {
        "status": "green",
        "timed_out": false
      }
    }

Each element is as follows:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Response Information

   * - data
     - Parent element of search results.
   * - status
     - System status. Returns ``green`` when normal, ``yellow`` when there are warnings, and ``red`` when there are errors.
   * - timed_out
     - Whether a timeout occurred. Returns ``false`` if a response is returned within the specified time, ``true`` if it times out.

Error Response
==============

When the Health API fails, the following error response is returned:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Error Response

   * - Status Code
     - Description
   * - 500 Internal Server Error
     - When an internal server error occurs
