==========================
Documents API
==========================

Overview
========

Documents API is an API for bulk registration of documents into the |Fess| index.
It allows multiple documents to be added to the index at once.

Base URL
========

::

    /api/admin/documents

Endpoint List
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Method
     - Path
     - Description
   * - PUT
     - /bulk
     - Bulk register documents

Bulk Register Documents
=======================

Bulk register multiple documents into the index.

Request
-------

::

    PUT /api/admin/documents/bulk
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "documents": [
        {
          "url": "https://example.com/page1",
          "title": "Sample Page 1",
          "content": "This is the body text of page 1."
        },
        {
          "url": "https://example.com/page2",
          "title": "Sample Page 2",
          "content": "This is the body text of page 2."
        }
      ]
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Required
     - Description
   * - ``documents``
     - Yes
     - Array of documents to register. Each document is specified as a map of field names and values. An empty array cannot be specified.

For each document, you can freely specify index fields such as ``url``, ``title``, and ``content``.
If fields such as ``content_length``, ``favorite_count``, ``click_count``, ``boost``, ``role``, ``last_modified``, and ``timestamp`` are omitted, default values are automatically filled in.
In addition, ``doc_id`` and the ID are automatically generated upon registration.

Response
--------

The response returns the processing result of each registered document in the ``items`` array.
Successful items include ``result`` and ``id``, while failed items include ``result`` and ``message``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "items": [
          {
            "result": "CREATED",
            "id": "abcdef0123456789"
          },
          {
            "result": "CREATED",
            "id": "0123456789abcdef"
          }
        ]
      }
    }

If registration fails for any item, ``status`` becomes ``9`` (FAILED), and the corresponding item includes a ``message`` field.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 9,
        "items": [
          {
            "result": "CREATED",
            "id": "abcdef0123456789"
          },
          {
            "result": "BAD_REQUEST",
            "message": "failure reason ..."
          }
        ]
      }
    }

Response Fields
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``items``
     - Array of processing results for each document
   * - ``items[].result``
     - Processing result status (e.g., ``CREATED``)
   * - ``items[].id``
     - ID of the registered document (on success)
   * - ``items[].message``
     - Failure reason message (on failure)

Usage Examples
==============

Bulk Register Documents
-----------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/documents/bulk" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "documents": [
             {
               "url": "https://example.com/page1",
               "title": "Sample Page 1",
               "content": "This is the body text of page 1."
             }
           ]
         }'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-searchlist` - Document Search and Management API
- :doc:`api-admin-crawlinginfo` - Crawling Info API
- :doc:`../../admin/searchlist-guide` - Search List Management Guide
