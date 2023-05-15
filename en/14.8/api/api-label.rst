=========
Label API
=========

Get Labels
==========

You can retrieve a list of labels registered in |Fess| by sending a request to ``http://<Server Name>/api/v1/labels``. The response will be in JSON format.

Request Parameters
------------------

There are no available request parameters.

Response
--------

The response will be as follows:

::

    {
      "record_count": 9,
      "data": [
        {
          "label": "AWS",
          "value": "aws"
        }
      ]
    }

The elements in the response are described as follows:

.. tabularcolumns:: |p{3cm}|p{12cm}|

.. list-table::

   * - record_count
     - The number of registered labels.
   * - data
     - The parent element of the search results.
   * - label
     - The name of the label.
   * - value
     - The value of the label.

Table: Response Information