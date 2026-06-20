==========================
Documents API
==========================

Overview
========

The Documents API is an Admin API for bulk registration of documents into the |Fess| index.
External systems can add documents directly to the index without going through the crawler.
Multiple documents can be registered in a single request.

Base URL
========

::

    /api/admin/documents

Authentication
==============

Calling this API requires authentication using an access token as described in :doc:`api-admin-overview`.
The token must be granted permission to access the Admin API (``Radmin-api`` by default).
This permission can be changed via the configuration key ``api.admin.access.permissions``.

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

.. note::

   This endpoint accepts only the ``PUT`` method.

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
     - Array of documents to register. Each document is specified as a map of field names and values. If ``null`` or an empty array is provided, an error is returned (``status`` = ``1``).

Document Fields
~~~~~~~~~~~~~~~

For each document, index fields can be freely specified as a map of field names and values.
At a minimum, ``url`` and ``title`` must be provided (as governed by the required fields setting
``index.admin.required.fields``, whose default value is ``url,title,role,boost``; since
``role`` and ``boost`` are auto-populated as described below, ``url`` and ``title`` are
effectively required).

The following fields are automatically populated when omitted:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Default value when omitted
   * - ``content_length``
     - Total character count of ``title`` and ``content``
   * - ``favorite_count``
     - ``0``
   * - ``click_count``
     - ``0``
   * - ``boost``
     - ``1.0``
   * - ``role``
     - Search guest role (the search role configured for guest users)
   * - ``last_modified``
     - Current timestamp
   * - ``timestamp``
     - Current timestamp

The following fields are generated automatically at registration time:

- ``id`` — Deterministically generated from the document's ``url`` (and ``role``, ``virtual_host``),
  and used as the OpenSearch document ID (``_id``). This value is returned in ``items[].id`` in the response.
- ``doc_id`` — A random UUID generated for each registration and stored as a document field.

.. note::

   Because ``id`` is deterministically generated from ``url``, registering a document with the
   same ``url`` again will update the existing document (``items[].result`` will be ``OK``).

Notes
~~~~~

- Including ``"auto"`` in the ``lang`` field causes the language to be automatically detected from the body text.
- Specifying ``config_id`` applies the ingest pipeline of the corresponding crawl configuration.
- When thumbnail generation is enabled (``thumbnail.crawler.enabled``), thumbnail generation is attempted at registration time.
- Values for each field are validated against the field type settings (``index.admin.array.fields``,
  ``index.admin.date.fields``, ``index.admin.long.fields``, etc.).
  A type mismatch results in an error (``status`` = ``1``).

Response
--------

The response returns the processing result for each registered document in the ``items`` array.
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

A ``status`` of ``0`` indicates that all documents were registered successfully.
``items[].result`` is set to ``CREATED`` for newly created documents, and ``OK`` for updates to existing documents.

If registration fails for any item, ``status`` becomes ``9`` (FAILED), and the failed item includes
a ``message`` field (``result`` is set to an error status name such as ``CONFLICT`` or ``BAD_REQUEST``).
Successfully registered items still return their ``id``.

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

.. note::

   If the request itself is invalid (``documents`` is missing or empty, required fields are absent,
   field type mismatches, etc.), no document registration is performed, and an error response containing
   ``status`` = ``1`` (BAD_REQUEST) and a ``message`` is returned.
   In this case, the ``items`` array is not included in the response.

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
     - Processing result status name: ``CREATED`` for new documents, ``OK`` for updates, or an error status name such as ``BAD_REQUEST`` for failures
   * - ``items[].id``
     - ID of the registered document (on success only)
   * - ``items[].message``
     - Failure reason message (on failure only)

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
