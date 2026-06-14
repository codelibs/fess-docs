==========================
Suggest API
==========================

Overview
========

The Suggest API is an API for managing the suggest functionality of |Fess|.
You can retrieve statistical information about suggest words and delete suggest words.

Base URL
========

::

    /api/admin/suggest

Endpoint List
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Method
     - Path
     - Description
   * - GET
     - /
     - Retrieve suggest word statistics
   * - DELETE
     - /all
     - Delete all suggest words
   * - DELETE
     - /document
     - Delete document-derived suggest words
   * - DELETE
     - /query
     - Delete search-query-derived suggest words

Retrieve Suggest Word Statistics
================================

Retrieves statistical information about the number of suggest words.

Request
-------

::

    GET /api/admin/suggest

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "totalWordsNum": 1500,
          "documentWordsNum": 1200,
          "queryWordsNum": 300
        }
      }
    }

Response Fields
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``setting.totalWordsNum``
     - Total number of suggest words
   * - ``setting.documentWordsNum``
     - Number of document-derived suggest words
   * - ``setting.queryWordsNum``
     - Number of search-query-derived suggest words

Delete All Suggest Words
========================

Deletes all suggest words.

Request
-------

::

    DELETE /api/admin/suggest/all

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Delete Document-Derived Suggest Words
=====================================

Deletes suggest words generated from documents.

Request
-------

::

    DELETE /api/admin/suggest/document

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Delete Search-Query-Derived Suggest Words
=========================================

Deletes suggest words generated from search queries.

Request
-------

::

    DELETE /api/admin/suggest/query

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Usage Examples
==============

Retrieve Statistics
-------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/suggest" \
         -H "Authorization: Bearer YOUR_TOKEN"

Delete All Suggest Words
------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

Delete Document-Derived Suggest Words
-------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/document" \
         -H "Authorization: Bearer YOUR_TOKEN"

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-badword` - Bad Word API
- :doc:`api-admin-elevateword` - Elevate Word API
- :doc:`../../admin/suggest-guide` - Suggest Management Guide
