=================
Popular Words API
=================

Fetching Popular Words List
============================

Request
-------

==================  ====================================================
HTTP Method         GET
Endpoint            ``/api/v1/popular-words``
==================  ====================================================

By sending a request to |Fess| at ``http://<Server Name>/api/v1/popular-words?seed=123``, you can receive a list of popular words registered in |Fess| in JSON format.
To use the Popular Words API, you need to enable popular words response in the Administration screen under System > General Settings.

Request Parameters
------------------

The available request parameters are as follows:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Request Parameters

   * - seed
     - Seed to retrieve popular words (this value allows you to obtain words in different patterns).
   * - label
     - Filtered label name.
   * - field
     - Field name to generate popular words.


Response
--------

The following response is returned:

::

    {
      "record_count": 3,
      "data": [
        "python",
        "java",
        "javascript"
      ]
    }

Each element is as follows:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Response Information

   * - record_count
     - Number of registered popular words
   * - data
     - Array of popular words

Error Response
==============

When the popular words API fails, the following error response is returned:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Error Response

   * - Status Code
     - Description
   * - 400 Bad Request
     - When request parameters are invalid
   * - 500 Internal Server Error
     - When an internal server error occurs