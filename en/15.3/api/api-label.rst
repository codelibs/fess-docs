=========
Label API
=========

Fetching Labels
===============

Request
-------

==================  ====================================================
HTTP Method         GET
Endpoint            ``/api/v1/labels``
==================  ====================================================

By sending a request to |Fess| at ``http://<Server Name>/api/v1/labels``, you can receive a list of labels registered in |Fess| in JSON format.

Request Parameters
------------------

There are no available request parameters.

Response
--------

The following response is returned:

::

    {
      "record_count": 9,
      "data": [
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

Each element is as follows:

.. tabularcolumns:: |p{3cm}|p{12cm}|

.. list-table::

   * - record_count
     - Number of registered labels.
   * - data
     - Parent element of search results.
   * - label
     - Label name.
   * - value
     - Label value.

Table: Response Information

Usage Examples
==============

Request example using curl command:

::

    curl "http://localhost:8080/api/v1/labels"

Request example using JavaScript:

::

    fetch('http://localhost:8080/api/v1/labels')
      .then(response => response.json())
      .then(data => {
        console.log('Label list:', data.data);
      });

Error Response
==============

When the label API fails, the following error response is returned:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Error Response

   * - Status Code
     - Description
   * - 500 Internal Server Error
     - When an internal server error occurs