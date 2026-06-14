==========================
RelatedQuery API
==========================

Overview
========

RelatedQuery API is an API for managing |Fess| related queries.
You can suggest related search keywords for specific search queries.

Base URL
========

::

    /api/admin/relatedquery

Endpoint List
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Method
     - Path
     - Description
   * - GET
     - /settings
     - List related queries
   * - GET
     - /setting/{id}
     - Get related query
   * - POST
     - /setting
     - Create related query
   * - PUT
     - /setting
     - Update related query
   * - DELETE
     - /setting/{id}
     - Delete related query

List Related Queries
====================

Request
-------

::

    GET /api/admin/relatedquery/settings

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15.70

   * - Parameter
     - Type
     - Required
     - Description
   * - ``size``
     - Integer
     - No
     - Number of items per page (default: 20)
   * - ``page``
     - Integer
     - No
     - Page number (starts from 0)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "query_id_1",
            "term": "fess",
            "queries": "fess tutorial\nfess installation\nfess configuration"
          }
        ],
        "total": 5
      }
    }

Get Related Query
=================

Request
-------

::

    GET /api/admin/relatedquery/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "query_id_1",
          "term": "fess",
          "queries": "fess tutorial\nfess installation\nfess configuration",
          "virtualHost": ""
        }
      }
    }

Create Related Query
====================

Request
-------

::

    POST /api/admin/relatedquery/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "search",
      "queries": "search tutorial\nsearch syntax\nadvanced search",
      "virtualHost": ""
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - Field
     - Required
     - Description
   * - ``term``
     - Yes
     - Search keyword
   * - ``queries``
     - Yes
     - Related queries (newline-separated string, one per line)
   * - ``virtualHost``
     - No
     - Virtual host

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_query_id",
        "created": true
      }
    }

Update Related Query
====================

Request
-------

::

    PUT /api/admin/relatedquery/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_query_id",
      "term": "search",
      "queries": "search tutorial\nsearch syntax\nadvanced search\nsearch tips",
      "virtualHost": "",
      "versionNo": 1
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_query_id",
        "created": false
      }
    }

Delete Related Query
====================

Request
-------

::

    DELETE /api/admin/relatedquery/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Usage Examples
==============

Product Related Queries
-----------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product",
           "queries": "product features\nproduct pricing\nproduct comparison\nproduct reviews"
         }'

Help Related Queries
--------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "help",
           "queries": "help center\nhelp documentation\nhelp contact support"
         }'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-relatedcontent` - Related Content API
- :doc:`api-admin-suggest` - Suggest Management API
- :doc:`../../admin/relatedquery-guide` - Related Query Management Guide

