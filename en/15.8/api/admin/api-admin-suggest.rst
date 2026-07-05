==========================
Suggest API
==========================

Overview
========

The Suggest API is an API for managing suggest words used by the suggest feature of |Fess|.
You can retrieve statistical information about the number of suggest words and delete suggest words.

Suggest words include those generated from crawled documents (document-derived) and those
generated from user search queries (search-query-derived). This API allows you to delete
them by type or delete all of them at once.

Authentication
==============

Access to this API requires authentication using an access token. Specify the access token
in the request header.

::

    Authorization: Bearer <access_token>

The access token must be granted the Admin API permission (``Radmin-api`` by default).
For details on how to obtain an access token and about permissions, see :doc:`api-admin-overview`.

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
=================================

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
        "version": "15.8.0",
        "status": 0,
        "setting": {
          "totalWordsNum": 1500,
          "documentWordsNum": 1200,
          "queryWordsNum": 450
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
     - Total number of suggest words (the number of suggest words registered in the suggest index)
   * - ``setting.documentWordsNum``
     - Number of document-derived suggest words (the number of suggest words with a document frequency of 1 or more)
   * - ``setting.queryWordsNum``
     - Number of search-query-derived suggest words (the number of suggest words with a query frequency of 1 or more)

.. note::

   ``documentWordsNum`` and ``queryWordsNum`` are not mutually exclusive. If a single suggest word
   is derived from both a document and a search query, it is included in both counts. Therefore,
   the sum of ``documentWordsNum`` and ``queryWordsNum`` may not equal ``totalWordsNum``.

Delete All Suggest Words
========================

Deletes all suggest words. All suggest words in the suggest index are targeted, regardless of
whether they are document-derived or search-query-derived.

Request
-------

::

    DELETE /api/admin/suggest/all

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

Delete Document-Derived Suggest Words
======================================

Deletes suggest words generated from documents (document-derived suggest words).

Request
-------

::

    DELETE /api/admin/suggest/document

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

Delete Search-Query-Derived Suggest Words
==========================================

Deletes suggest words generated from search queries (search-query-derived suggest words).

Request
-------

::

    DELETE /api/admin/suggest/query

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

Error Response
==============

If a delete operation fails, HTTP status ``400`` is returned, the ``status`` field in the
response body is set to ``1`` (BAD_REQUEST), and ``message`` contains an error message.

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 1,
        "message": "Failed to delete a document."
      }
    }

If the access token is missing or invalid, or if permissions are insufficient, the ``status``
field in the response body is set to ``3`` (UNAUTHORIZED). For a list of ``status`` values and
HTTP status codes, see :doc:`api-admin-overview`.

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
--------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/document" \
         -H "Authorization: Bearer YOUR_TOKEN"

Delete Search-Query-Derived Suggest Words
------------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/query" \
         -H "Authorization: Bearer YOUR_TOKEN"

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-badword` - Bad Word API
- :doc:`api-admin-elevateword` - Elevate Word API
- :doc:`../../admin/suggest-guide` - Suggest Management Guide
