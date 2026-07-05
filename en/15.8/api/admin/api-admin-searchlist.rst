==========================
SearchList API
==========================

Overview
========

SearchList API is an Admin API for searching and managing documents in the |Fess| index.
It can search, retrieve, create, update, and delete documents.

All field names in the response are in ``snake_case``. Fields whose value is ``null`` are omitted from the response.

Base URL
========

::

    /api/admin/searchlist

Authentication
==============

Calling this API requires authentication with an access token as described in :doc:`api-admin-overview`.
The token must be granted the Admin API access permission (``Radmin-api`` by default).
This permission can be changed with the configuration key ``api.admin.access.permissions``.

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
     - Search query (max 1000 characters). If not specified, all documents are targeted.
   * - ``sort``
     - String
     - No
     - Sort field and direction (e.g. ``last_modified.desc``).
   * - ``start``
     - Integer
     - No
     - Zero-based start position (default ``0``).
   * - ``offset``
     - Integer
     - No
     - Offset from ``start`` (default ``0``).
   * - ``pn``
     - Integer
     - No
     - Page number.
   * - ``num``
     - Integer
     - No
     - Number of items to retrieve (default ``10``). Values exceeding the configured maximum (default ``100``) or values of ``0`` or less are clamped to the maximum.
   * - ``size``
     - Integer
     - No
     - Number of items to retrieve (alias for ``num``, provided for compatibility with other Admin APIs).
   * - ``lang``
     - String[]
     - No
     - Search language. Can be specified repeatedly (array). e.g. ``en``.
   * - ``ex_q``
     - String[]
     - No
     - Additional query expressions. Can be specified repeatedly (array).
   * - ``fields.<name>``
     - String[]
     - No
     - Filters by field value. The most common case is ``fields.label`` (filter by label name); any ``fields.<name>`` narrows results to those whose document field ``<name>`` matches the given value. Can be specified repeatedly.
   * - ``as.<name>``
     - String[]
     - No
     - Advanced search conditions. Any ``as.<name>`` (e.g. ``as.q``) is passed to the advanced search condition builder. Can be specified repeatedly per name.
   * - ``sdh``
     - String
     - No
     - Similar-document hash.

.. note::

   This endpoint does not support faceting, highlighting, or geo search. Such parameters are ignored if specified.

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "query_id": "f8b1c2d3e4a5",
        "exec_time": "0.05",
        "query_time": 8,
        "page_size": 20,
        "page_number": 1,
        "record_count": 234,
        "record_count_relation": "eq",
        "page_count": 12,
        "next_page": true,
        "prev_page": false,
        "start_record_number": 1,
        "end_record_number": 20,
        "page_numbers": ["1", "2", "3", "4", "5"],
        "partial": false,
        "search_query": "title:Fess OR content:Fess",
        "requested_time": 1717142400000,
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
   * - ``version``
     - The version of the running |Fess| (the example value is illustrative).
   * - ``status``
     - Status code (``0`` for success; see "Status Codes").
   * - ``query_id``
     - Search query ID.
   * - ``docs``
     - Array of search result documents. Each document is a map of field names and values, using the index field names as-is (``doc_id``, ``url``, ``title``, ``content_description``, etc.).
   * - ``exec_time``
     - Search execution time (seconds, string).
   * - ``query_time``
     - Search engine query time (milliseconds).
   * - ``page_size``
     - Number of items per page.
   * - ``page_number``
     - Current page number.
   * - ``record_count``
     - Number of matching items.
   * - ``record_count_relation``
     - Relation of the matching count. ``eq`` means an exact count, ``gte`` means only a lower bound is known.
   * - ``page_count``
     - Total number of pages.
   * - ``next_page``
     - Whether a next page exists (bool).
   * - ``prev_page``
     - Whether a previous page exists (bool).
   * - ``start_record_number``
     - Start record number of this page.
   * - ``end_record_number``
     - End record number of this page.
   * - ``page_numbers``
     - Array of page numbers to display in the pager (strings).
   * - ``partial``
     - Whether the results are partial (bool).
   * - ``search_query``
     - The actual search query that was executed.
   * - ``requested_time``
     - Request time (epoch milliseconds).
   * - ``highlight_params``
     - Highlight query parameter string (usually empty for this Admin API).

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
     - Document ID (the ``doc_id`` value, path parameter).

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "doc": {
          "doc_id": "abcdef0123456789",
          "url": "https://example.com/page1",
          "title": "Sample Page 1"
        }
      }
    }

If no document exists for the specified ID, an error response (``status`` = ``1``) is returned.

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
        "content": "This is the body text.",
        "role": ["{role}guest"],
        "boost": 1.0
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
     - The document to register. Specified as a map of index field names and values.

Among the fields specified in ``doc``, all required fields configured in ``index.admin.required.fields`` (default ``url,title,role,boost``) must be provided.
Unlike the bulk :doc:`Documents API <api-admin-documents>`, this endpoint does not auto-complete defaults such as ``role`` or ``boost``, so the required fields must be specified explicitly in the request.
``doc_id`` is generated automatically on the server side and is not specified when creating.

Each field value is validated according to the field type configuration. If the type does not match, an error (``status`` = ``1``) is returned.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Configuration Key
     - Default
   * - ``index.admin.array.fields``
     - ``lang,role,label,anchor,virtual_host``
   * - ``index.admin.date.fields``
     - ``expires,created,timestamp,last_modified``
   * - ``index.admin.integer.fields``
     - (empty)
   * - ``index.admin.long.fields``
     - ``content_length,favorite_count,click_count``
   * - ``index.admin.float.fields``
     - ``boost``
   * - ``index.admin.double.fields``
     - (empty)

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "abcdef0123456789",
        "created": true
      }
    }

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``id``
     - The ``doc_id`` of the registered document.
   * - ``created``
     - ``true`` when created.

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
        "content": "This is the updated body text.",
        "role": ["{role}guest"],
        "boost": 1.0
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
     - The document to update. Specified as a map of index field names and values.

The document to update is identified by ``doc_id`` within ``doc``. If ``doc_id`` is not specified, or no matching document exists, an error (``status`` = ``1``) is returned.
As with creation, all required fields configured in ``index.admin.required.fields`` (default ``url,title,role,boost``) must be provided, and each field value is validated according to the type configuration.

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "abcdef0123456789",
        "created": false
      }
    }

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``id``
     - The ``doc_id`` of the updated document.
   * - ``created``
     - ``false`` when updated.

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
     - Document ID (the ``doc_id`` value, path parameter).

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
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
     - Search query for the documents to delete.

The deletion target is built with the same query as "Search Documents", so narrowing parameters such as ``fields.<name>`` and ``ex_q`` can be used together. If ``q`` is not specified, an error (``status`` = ``1``) is returned.

Response
--------

Returns the number of deleted documents in ``count``.

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "count": 150
      }
    }

Status Codes
============

The ``status`` field in the response is set to one of the following values.

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - Value
     - Name
     - Description
   * - ``0``
     - OK
     - Success.
   * - ``1``
     - BAD_REQUEST
     - The request is invalid (missing required field, type mismatch, target document not found, invalid query, etc.).
   * - ``2``
     - SYSTEM_ERROR
     - System error.
   * - ``3``
     - UNAUTHORIZED
     - Authentication error.
   * - ``9``
     - FAILED
     - Processing failed.

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

Create Document
---------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/searchlist/doc" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "doc": {
             "url": "https://example.com/page1",
             "title": "Sample Page 1",
             "content": "This is the body text.",
             "role": ["{role}guest"],
             "boost": 1.0
           }
         }'

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
