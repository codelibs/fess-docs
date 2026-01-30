==========================
LabelType API
==========================

Overview
========

LabelType API is an API for managing |Fess| label types.
You can configure label types for search result classification and filtering.

Base URL
========

::

    /api/admin/labeltype

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
     - List label types
   * - GET
     - /setting/{id}
     - Get label type
   * - POST
     - /setting
     - Create label type
   * - PUT
     - /setting
     - Update label type
   * - DELETE
     - /setting/{id}
     - Delete label type

List Label Types
================

Request
-------

::

    GET /api/admin/labeltype/settings
    PUT /api/admin/labeltype/settings

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
            "id": "label_id_1",
            "name": "Documentation",
            "value": "docs",
            "includedPaths": ".*docs\\.example\\.com.*",
            "excludedPaths": "",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

Get Label Type
==============

Request
-------

::

    GET /api/admin/labeltype/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "label_id_1",
          "name": "Documentation",
          "value": "docs",
          "includedPaths": ".*docs\\.example\\.com.*",
          "excludedPaths": "",
          "sortOrder": 0,
          "permissions": [],
          "virtualHost": ""
        }
      }
    }

Create Label Type
=================

Request
-------

::

    POST /api/admin/labeltype/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "News",
      "value": "news",
      "includedPaths": ".*news\\.example\\.com.*\n.*example\\.com/news/.*",
      "excludedPaths": ".*/(archive|old)/.*",
      "sortOrder": 1,
      "permissions": ["guest"]
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Required
     - Description
   * - ``name``
     - Yes
     - Label display name
   * - ``value``
     - Yes
     - Label value (used in search)
   * - ``includedPaths``
     - No
     - Regex patterns for paths to label (newline-separated for multiple)
   * - ``excludedPaths``
     - No
     - Regex patterns for paths to exclude from labeling (newline-separated for multiple)
   * - ``sortOrder``
     - No
     - Display order
   * - ``permissions``
     - No
     - Access permission roles
   * - ``virtualHost``
     - No
     - Virtual host

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_label_id",
        "created": true
      }
    }

Update Label Type
=================

Request
-------

::

    PUT /api/admin/labeltype/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_label_id",
      "name": "News Articles",
      "value": "news",
      "includedPaths": ".*news\\.example\\.com.*\n.*example\\.com/(news|articles)/.*",
      "excludedPaths": ".*/(archive|old|draft)/.*",
      "sortOrder": 1,
      "permissions": ["guest"],
      "versionNo": 1
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_label_id",
        "created": false
      }
    }

Delete Label Type
=================

Request
-------

::

    DELETE /api/admin/labeltype/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_label_id",
        "created": false
      }
    }

Usage Examples
==============

Create Documentation Label
--------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/labeltype/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Technical Documentation",
           "value": "tech_docs",
           "includedPaths": ".*docs\\.example\\.com.*\n.*example\\.com/documentation/.*",
           "sortOrder": 0,
           "permissions": ["guest"]
         }'

Search with Label
-----------------

.. code-block:: bash

    # Filter by label
    curl "http://localhost:8080/json/?q=search&label=tech_docs"

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`../api-search` - Search API
- :doc:`../../admin/labeltype-guide` - Label Type Management Guide

