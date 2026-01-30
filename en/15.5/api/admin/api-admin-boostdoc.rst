==========================
BoostDoc API
==========================

Overview
========

BoostDoc API is an API for managing |Fess| document boost settings.
You can adjust search ranking for documents matching specific conditions.

Base URL
========

::

    /api/admin/boostdoc

Endpoint List
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Method
     - Path
     - Description
   * - GET/PUT
     - /settings
     - List document boosts
   * - GET
     - /setting/{id}
     - Get document boost
   * - POST
     - /setting
     - Create document boost
   * - PUT
     - /setting
     - Update document boost
   * - DELETE
     - /setting/{id}
     - Delete document boost

List Document Boosts
====================

Request
-------

::

    GET /api/admin/boostdoc/settings
    PUT /api/admin/boostdoc/settings

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

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
            "id": "boostdoc_id_1",
            "urlExpr": ".*docs\\.example\\.com.*",
            "boostExpr": "3.0",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

Get Document Boost
==================

Request
-------

::

    GET /api/admin/boostdoc/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "boostdoc_id_1",
          "urlExpr": ".*docs\\.example\\.com.*",
          "boostExpr": "3.0",
          "sortOrder": 0
        }
      }
    }

Create Document Boost
=====================

Request
-------

::

    POST /api/admin/boostdoc/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "urlExpr": ".*important\\.example\\.com.*",
      "boostExpr": "5.0",
      "sortOrder": 0
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Required
     - Description
   * - ``urlExpr``
     - Yes
     - URL regex pattern
   * - ``boostExpr``
     - Yes
     - Boost expression (number or expression)
   * - ``sortOrder``
     - No
     - Application order

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_boostdoc_id",
        "created": true
      }
    }

Update Document Boost
=====================

Request
-------

::

    PUT /api/admin/boostdoc/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_boostdoc_id",
      "urlExpr": ".*important\\.example\\.com.*",
      "boostExpr": "10.0",
      "sortOrder": 0,
      "versionNo": 1
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_boostdoc_id",
        "created": false
      }
    }

Delete Document Boost
=====================

Request
-------

::

    DELETE /api/admin/boostdoc/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_boostdoc_id",
        "created": false
      }
    }

Boost Expression Examples
=========================

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Boost Expression
     - Description
   * - ``2.0``
     - Fixed value boost
   * - ``doc['boost'].value * 2``
     - Double the document's boost value
   * - ``Math.log(doc['click_count'].value + 1)``
     - Logarithmic scale boost based on click count
   * - ``doc['last_modified'].value > now - 7d ? 3.0 : 1.0``
     - 3x boost if updated within the last week

Usage Examples
==============

Boost Documentation Site
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": ".*docs\\.example\\.com.*",
           "boostExpr": "5.0",
           "sortOrder": 0
         }'

Boost New Content
-----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": ".*",
           "boostExpr": "doc[\"last_modified\"].value > now - 30d ? 2.0 : 1.0",
           "sortOrder": 10
         }'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-elevateword` - Elevate Word API
- :doc:`../../admin/boostdoc-guide` - Document Boost Management Guide

