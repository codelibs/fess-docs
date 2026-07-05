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
   * - GET
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
     - Number of items per page (default: 25)
   * - ``page``
     - Integer
     - No
     - Page number (starts from 1, default: 1)
   * - ``name``
     - String
     - No
     - Filter by configuration name
   * - ``handlerName``
     - String
     - No
     - Filter by handler name
   * - ``description``
     - String
     - No
     - Filter by description

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
            "description": "Database crawler",
            "handlerName": "DatabaseDataStore",
            "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb",
            "handlerScript": "...",
            "boost": 1.0,
            "available": "true",
            "permissions": "{role}admin",
            "virtualHosts": "",
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
          "description": "Database crawler",
          "handlerName": "DatabaseDataStore",
          "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb\nusername=dbuser\npassword=dbpass",
          "handlerScript": "...",
          "boost": 1.0,
          "available": "true",
          "sortOrder": 0,
          "permissions": "{role}admin",
          "virtualHosts": ""
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
      "handlerScript": "url=\"https://example.com/product/\" + product_id\ntitle=product_name\ncontent=description",
      "boost": 1.0,
      "available": "true",
      "sortOrder": 0,
      "permissions": "{role}admin\n{role}user"
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
   * - ``description``
     - No
     - Configuration description
   * - ``handlerName``
     - Yes
     - Data store handler name
   * - ``handlerParameter``
     - No
     - Handler parameters (connection information, etc.)
   * - ``handlerScript``
     - No
     - Data transformation script
   * - ``boost``
     - Yes
     - Search result boost value
   * - ``available``
     - Yes
     - Enable/disable (string ``"true"`` / ``"false"``)
   * - ``sortOrder``
     - Yes
     - Display order
   * - ``permissions``
     - No
     - Access permission roles (newline-separated for multiple values)
   * - ``virtualHosts``
     - No
     - Virtual hosts (newline-separated for multiple values)

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
      "handlerScript": "url=\"https://example.com/product/\" + product_id\ntitle=product_name\ncontent=description + \" \" + features",
      "boost": 1.5,
      "available": "true",
      "sortOrder": 0,
      "versionNo": 1
    }

Update requests require the same required fields as creation (``name``, ``handlerName``, ``boost``, ``available``, ``sortOrder``), plus the following fields:

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Required
     - Description
   * - ``id``
     - Yes
     - ID of the configuration to update
   * - ``versionNo``
     - Yes
     - Version number for optimistic locking (specify the value returned when the setting was retrieved)

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
        "status": 0
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
     - Reads data from a CSV file (processes each row as one document)
   * - ``CsvListDataStore``
     - Reads CSV files and automatically deletes processed files (an extension of ``CsvDataStore`` with timestamp-based filtering)
   * - ``JsonDataStore``
     - Read data from JSON files or JSON APIs

.. note::

   The available handler types depend on the installed data store plugins. The handlers above are included by default. Installing data store plugins such as SharePoint, Slack, or Salesforce makes their corresponding handler names available.

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
           "handlerScript": "url=\"https://example.com/user/\" + user_id\ntitle=username\ncontent=profile",
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0
         }'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-webconfig` - Web Crawl Configuration API
- :doc:`api-admin-fileconfig` - File Crawl Configuration API
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide

