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

The list of labels returned is filtered based on the requesting user and request content as follows:

- **Filtering by permissions**: Labels are filtered based on the access permissions configured on each label and the user's roles. Because v2 uses session-based authentication, logged-in users can only retrieve labels accessible under their own roles. Labels whose access permissions do not match are not included in the list.
- **Filtering by locale**: Labels can be registered per locale. Labels registered with a locale matching the ``Accept-Language`` request header, as well as labels registered without a specific locale, are returned.
- **Filtering by virtual host**: When virtual hosts are in use, only labels assigned to the relevant virtual host are returned.

Request Parameters
------------------

There are no query parameters. The filtering of returned labels is performed based on the authenticated user's permissions and the ``Accept-Language`` request header, as described above.

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
     - Number of labels returned (integer).
   * - ``labels``
     - Array of labels.
   * - ``label``
     - Display name of the label (label name).
   * - ``value``
     - Label value. By specifying this value in the ``fields.label`` parameter of the :doc:`api-search`, you can filter search results by that label.

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
     - An HTTP method other than GET was specified. The ``error.code`` is ``method_not_allowed``, and an ``Allow: GET`` header is included in the response.
   * - 500 Internal Server Error
     - An internal server error occurred. The ``error.code`` is ``internal_error``.

Table: Error Response
