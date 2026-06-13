==========================
SearchList API
==========================

Overview
========

SearchList API is an API for searching and managing documents in the |Fess| index.
It can search, retrieve, create, update, and delete documents.

Base URL
========

::

    /api/admin/searchlist

Endpoint List
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Method
     - Path
     - Description
   * - GET / PUT
     - /docs
     - Search documents
   * - GET
     - /doc/{id}
     - Get document
   * - POST
     - /doc
     - Create document
   * - PUT
     - /doc
     - Update document
   * - DELETE
     - /doc/{id}
     - Delete document (by ID)
   * - DELETE
     - /query
     - Delete documents (by query)

Search Documents
================

Search for documents matching the search conditions.

Request
-------

::

    GET /api/admin/searchlist/docs
    PUT /api/admin/searchlist/docs

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Type
     - Required
     - Description
   * - ``q``
     - String
     - No
     - Search query. If not specified, all documents are targeted.
   * - ``sort``
     - String
     - No
     - Sort field and direction
   * - ``start``
     - Integer
     - No
     - Start position of the search results
   * - ``offset``
     - Integer
     - No
     - Paging offset
   * - ``num``
     - Integer
     - No
     - Number of items to retrieve
   * - ``size``
     - Integer
     - No
     - Number of items to retrieve (alias for ``num``)
   * - ``lang``
     - String[]
     - No
     - Language

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "queryId": "...",
        "execTime": "0.05",
        "pageSize": 20,
        "pageNumber": 1,
        "recordCount": 234,
        "recordCountRelation": "EQUAL_TO",
        "pageCount": 12,
        "docs": [
          {
            "doc_id": "abcdef0123456789",
            "url": "https://example.com/page1",
            "title": "Sample Page 1",
            "content_description": "..."
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
   * - ``queryId``
     - Search query ID
   * - ``docs``
     - Array of search result documents
   * - ``execTime``
     - Search execution time
   * - ``pageSize``
     - Number of items per page
   * - ``pageNumber``
     - Current page number
   * - ``recordCount``
     - Number of matching items
   * - ``recordCountRelation``
     - Relation of the matching count (exact match or lower bound)
   * - ``pageCount``
     - Total number of pages

Get Document
============

Retrieve a single document by specifying the document ID.

Request
-------

::

    GET /api/admin/searchlist/doc/{id}

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Type
     - Required
     - Description
   * - ``id``
     - String
     - Yes
     - Document ID (``doc_id``, path parameter)

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "doc": {
          "doc_id": "abcdef0123456789",
          "url": "https://example.com/page1",
          "title": "Sample Page 1"
        }
      }
    }

Create Document
===============

Create a new document in the index.

Request
-------

::

    POST /api/admin/searchlist/doc
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "doc": {
        "url": "https://example.com/page1",
        "title": "Sample Page 1",
        "content": "This is the body text."
      }
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Required
     - Description
   * - ``doc``
     - Yes
     - The document to register. Specified as a map of field names and values.

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "abcdef0123456789",
        "created": true
      }
    }

Update Document
===============

Update an existing document.

Request
-------

::

    PUT /api/admin/searchlist/doc
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "doc": {
        "doc_id": "abcdef0123456789",
        "url": "https://example.com/page1",
        "title": "Updated Title",
        "content": "This is the updated body text."
      }
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Required
     - Description
   * - ``doc``
     - Yes
     - The document to update. Specified as a map of field names and values.

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "abcdef0123456789",
        "created": false
      }
    }

Delete Document (by ID)
=======================

Delete a document by specifying the document ID.

Request
-------

::

    DELETE /api/admin/searchlist/doc/{id}

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Type
     - Required
     - Description
   * - ``id``
     - String
     - Yes
     - Document ID (``doc_id``, path parameter)

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Delete Documents (by query)
===========================

Bulk delete documents matching a search query.

Request
-------

::

    DELETE /api/admin/searchlist/query

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Type
     - Required
     - Description
   * - ``q``
     - String
     - Yes
     - Search query for the documents to delete

Response
--------

Returns the number of deleted documents in ``count``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "count": 150
      }
    }

Usage Examples
==============

Search Documents
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlist/docs?q=Fess&size=20" \
         -H "Authorization: Bearer YOUR_TOKEN"

Get Document
------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlist/doc/abcdef0123456789" \
         -H "Authorization: Bearer YOUR_TOKEN"

Delete Documents by Query
-------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/searchlist/query?q=url:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-documents` - Bulk Document Registration API
- :doc:`api-admin-crawlinginfo` - Crawling Info API
- :doc:`../../admin/searchlist-guide` - Search List Management Guide
