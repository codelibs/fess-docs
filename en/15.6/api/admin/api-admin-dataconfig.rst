==========================
DataConfig API
==========================

Overview
========

DataConfig API is an API for managing |Fess| data store configurations.
You can configure crawl settings for data sources such as databases, CSV, and JSON.

Base URL
========

::

    /api/admin/dataconfig

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
     - List data store configurations
   * - GET
     - /setting/{id}
     - Get data store configuration
   * - POST
     - /setting
     - Create data store configuration
   * - PUT
     - /setting
     - Update data store configuration
   * - DELETE
     - /setting/{id}
     - Delete data store configuration

List Data Store Configurations
==============================

Request
-------

::

    GET /api/admin/dataconfig/settings
    PUT /api/admin/dataconfig/settings

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
            "id": "dataconfig_id_1",
            "name": "Database Crawler",
            "handlerName": "DatabaseDataStore",
            "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb",
            "handlerScript": "...",
            "boost": 1.0,
            "available": true,
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

Get Data Store Configuration
============================

Request
-------

::

    GET /api/admin/dataconfig/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "dataconfig_id_1",
          "name": "Database Crawler",
          "handlerName": "DatabaseDataStore",
          "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb\nusername=dbuser\npassword=dbpass",
          "handlerScript": "...",
          "boost": 1.0,
          "available": true,
          "sortOrder": 0,
          "permissions": ["admin"],
          "virtualHosts": [],
          "labelTypeIds": []
        }
      }
    }

Create Data Store Configuration
===============================

Request
-------

::

    POST /api/admin/dataconfig/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Product Database",
      "handlerName": "DatabaseDataStore",
      "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/products\nusername=user\npassword=pass",
      "handlerScript": "url=\"https://example.com/product/\" + data.product_id\ntitle=data.product_name\ncontent=data.description",
      "boost": 1.0,
      "available": true,
      "permissions": ["admin", "user"],
      "labelTypeIds": ["label_id_1"]
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
     - Configuration name
   * - ``handlerName``
     - Yes
     - Data store handler name
   * - ``handlerParameter``
     - No
     - Handler parameters (connection information, etc.)
   * - ``handlerScript``
     - Yes
     - Data transformation script
   * - ``boost``
     - No
     - Search result boost value (default: 1.0)
   * - ``available``
     - No
     - Enable/disable (default: true)
   * - ``sortOrder``
     - No
     - Display order
   * - ``permissions``
     - No
     - Access permission roles
   * - ``virtualHosts``
     - No
     - Virtual hosts
   * - ``labelTypeIds``
     - No
     - Label type IDs

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_dataconfig_id",
        "created": true
      }
    }

Update Data Store Configuration
===============================

Request
-------

::

    PUT /api/admin/dataconfig/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_dataconfig_id",
      "name": "Updated Product Database",
      "handlerName": "DatabaseDataStore",
      "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/products\nusername=user\npassword=newpass",
      "handlerScript": "url=\"https://example.com/product/\" + data.product_id\ntitle=data.product_name\ncontent=data.description + \" \" + data.features",
      "boost": 1.5,
      "available": true,
      "versionNo": 1
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_dataconfig_id",
        "created": false
      }
    }

Delete Data Store Configuration
===============================

Request
-------

::

    DELETE /api/admin/dataconfig/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_dataconfig_id",
        "created": false
      }
    }

Handler Types
=============

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Handler Name
     - Description
   * - ``DatabaseDataStore``
     - Connect to databases via JDBC
   * - ``CsvDataStore``
     - Read data from CSV files
   * - ``JsonDataStore``
     - Read data from JSON files or JSON APIs

Usage Examples
==============

Database Crawl Configuration
----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dataconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "User Database",
           "handlerName": "DatabaseDataStore",
           "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/userdb\nusername=dbuser\npassword=dbpass\nsql=SELECT * FROM users WHERE active=true",
           "handlerScript": "url=\"https://example.com/user/\" + data.user_id\ntitle=data.username\ncontent=data.profile",
           "boost": 1.0,
           "available": true
         }'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-webconfig` - Web Crawl Configuration API
- :doc:`api-admin-fileconfig` - File Crawl Configuration API
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide

