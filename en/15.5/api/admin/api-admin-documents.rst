==========================
Documents API
==========================

Overview
========

Documents API is an API for managing documents in the |Fess| index.
You can perform bulk deletion, update, and search operations on documents.

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
   * - DELETE
     - /
     - Delete documents (by query)
   * - DELETE
     - /{id}
     - Delete document (by ID)

Delete Documents by Query
=========================

Bulk delete documents matching a search query.

Request
-------

::

    DELETE /api/admin/documents

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
     - Search query for documents to delete

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "deleted": 150
      }
    }

Example
~~~~~~~

.. code-block:: bash

    # Delete documents from a specific site
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=url:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Delete old documents
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=lastModified:[* TO 2023-01-01]" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Delete documents by label
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=label:old_label" \
         -H "Authorization: Bearer YOUR_TOKEN"

Delete Document by ID
=====================

Delete a document by specifying its ID.

Request
-------

::

    DELETE /api/admin/documents/{id}

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
     - Document ID (path parameter)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Example
~~~~~~~

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/documents/doc_id_12345" \
         -H "Authorization: Bearer YOUR_TOKEN"

Query Syntax
============

Delete queries use |Fess|'s standard search syntax.

Basic Queries
-------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Query Example
     - Description
   * - ``url:example.com``
     - Documents with "example.com" in the URL
   * - ``url:https://example.com/*``
     - URLs with a specific prefix
   * - ``host:example.com``
     - Documents from a specific host
   * - ``title:keyword``
     - Documents with keyword in the title
   * - ``content:keyword``
     - Documents with keyword in the content
   * - ``label:mylabel``
     - Documents with a specific label

Date Range Queries
------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Query Example
     - Description
   * - ``lastModified:[2023-01-01 TO 2023-12-31]``
     - Documents updated within the specified period
   * - ``lastModified:[* TO 2023-01-01]``
     - Documents updated before the specified date
   * - ``created:[2024-01-01 TO *]``
     - Documents created after the specified date

Compound Queries
----------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Query Example
     - Description
   * - ``url:example.com AND label:blog``
     - AND condition
   * - ``url:example.com OR url:sample.com``
     - OR condition
   * - ``NOT url:example.com``
     - NOT condition
   * - ``(url:example.com OR url:sample.com) AND label:news``
     - Grouping

Cautions
========

Deletion Warnings
-----------------

.. warning::
   Delete operations cannot be undone. Always verify in a test environment before executing in production.

- Deleting a large number of documents may take time to process
- Index performance may be affected during deletion
- It may take some time for deleted documents to be reflected in search results

Recommended Practices
---------------------

1. **Verify before deletion**: Use the search API with the same query to verify targets
2. **Delete in stages**: Split large deletions into multiple operations
3. **Backup**: Back up important data beforehand

Usage Examples
==============

Prepare for Full Site Re-crawl
------------------------------

.. code-block:: bash

    # Delete old documents from a specific site
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=host:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Start crawl job
    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

Cleanup Old Documents
---------------------

.. code-block:: bash

    # Delete documents not updated for more than a year
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=lastModified:[* TO now-1y]" \
         -H "Authorization: Bearer YOUR_TOKEN"

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-crawlinginfo` - Crawling Info API
- :doc:`../../admin/searchlist-guide` - Search List Management Guide

