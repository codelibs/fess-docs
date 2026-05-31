=========
Label API
=========

This document describes the v2 Label API of |Fess|.
For the common response envelope and error model, see :doc:`api-overview`.

The base URL is ``http://<Server Name>/api/v2/`` (local environment example: ``http://localhost:8080/api/v2``).

Fetching Labels
===============

Request
-------

==================  ====================================================
HTTP Method         GET
Endpoint            ``/api/v2/labels``
==================  ====================================================

Retrieves a list of configured labels registered in |Fess| using the common envelope.

Request Parameters
------------------

There are no available request parameters.

Response
--------

On success (200), the following fields are returned directly under ``response`` in the common envelope.

::

    {
      "response": {
        "status": 0,
        "record_count": 2,
        "labels": [
          {
            "label": "AWS",
            "value": "aws"
          },
          {
            "label": "Azure",
            "value": "azure"
          }
        ]
      }
    }

Each field is described below.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Response Fields

   * - ``record_count``
     - Number of registered labels (integer).
   * - ``labels``
     - Array of labels.
   * - ``label``
     - Label name.
   * - ``value``
     - Label value.

Table: Response Fields

Usage Examples
==============

Request example using curl:

::

    curl "http://localhost:8080/api/v2/labels"

Error Response
==============

For details on the error model, see :doc:`api-overview`. The HTTP statuses returned by this endpoint are as follows.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Error Response

   * - Status Code
     - Description
   * - 405 Method Not Allowed
     - The HTTP method is not allowed.
   * - 500 Internal Server Error
     - An internal server error occurred.

Table: Error Response
