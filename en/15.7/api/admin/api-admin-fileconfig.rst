==========================
FileConfig API
==========================

Overview
========

FileConfig API is an API for managing |Fess| file crawl configurations.
You can configure crawl settings for file systems and SMB/CIFS shared folders.

Base URL
========

::

    /api/admin/fileconfig

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
     - List file crawl configurations
   * - GET
     - /setting/{id}
     - Get file crawl configuration
   * - POST
     - /setting
     - Create file crawl configuration
   * - PUT
     - /setting
     - Update file crawl configuration
   * - DELETE
     - /setting/{id}
     - Delete file crawl configuration

List File Crawl Configurations
==============================

Request
-------

::

    GET /api/admin/fileconfig/settings

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
            "id": "fileconfig_id_1",
            "name": "Shared Documents",
            "description": "Shared documents",
            "paths": "file://///server/share/documents",
            "includedPaths": ".*\\.pdf$",
            "excludedPaths": ".*/(temp|cache)/.*",
            "includedDocPaths": "",
            "excludedDocPaths": "",
            "configParameter": "",
            "depth": 10,
            "maxAccessCount": 1000,
            "numOfThread": 1,
            "intervalTime": 1000,
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

Get File Crawl Configuration
============================

Request
-------

::

    GET /api/admin/fileconfig/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "fileconfig_id_1",
          "name": "Shared Documents",
          "description": "Shared documents",
          "paths": "file://///server/share/documents",
          "includedPaths": ".*\\.pdf$",
          "excludedPaths": ".*/(temp|cache)/.*",
          "includedDocPaths": "",
          "excludedDocPaths": "",
          "configParameter": "",
          "depth": 10,
          "maxAccessCount": 1000,
          "numOfThread": 1,
          "intervalTime": 1000,
          "boost": 1.0,
          "available": "true",
          "sortOrder": 0,
          "permissions": "{role}admin",
          "virtualHosts": "",
          "labelTypeIds": []
        }
      }
    }

Create File Crawl Configuration
===============================

Request
-------

::

    POST /api/admin/fileconfig/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Local Files",
      "paths": "file:///data/documents",
      "includedPaths": ".*\\.(pdf|doc|docx|xls|xlsx)$",
      "excludedPaths": ".*/(temp|backup)/.*",
      "numOfThread": 2,
      "intervalTime": 500,
      "boost": 1.0,
      "available": "true",
      "sortOrder": 0,
      "permissions": "{role}admin\n{role}user",
      "labelTypeIds": ["label_id_1"]
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - Field
     - Required
     - Description
   * - ``name``
     - Yes
     - Configuration name
   * - ``description``
     - No
     - Configuration description
   * - ``paths``
     - Yes
     - Crawl start paths (newline-separated for multiple paths)
   * - ``includedPaths``
     - No
     - Regex pattern for paths to crawl
   * - ``excludedPaths``
     - No
     - Regex pattern for paths to exclude from crawling
   * - ``includedDocPaths``
     - No
     - Regex pattern for paths to index
   * - ``excludedDocPaths``
     - No
     - Regex pattern for paths to exclude from indexing
   * - ``configParameter``
     - No
     - Additional configuration parameters
   * - ``depth``
     - No
     - Crawl depth
   * - ``maxAccessCount``
     - No
     - Maximum access count
   * - ``numOfThread``
     - Yes
     - Number of parallel threads
   * - ``intervalTime``
     - Yes
     - Access interval in milliseconds
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
   * - ``labelTypeIds``
     - No
     - Label type IDs (array)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_fileconfig_id",
        "created": true
      }
    }

Update File Crawl Configuration
===============================

Request
-------

::

    PUT /api/admin/fileconfig/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_fileconfig_id",
      "name": "Updated Local Files",
      "paths": "file:///data/documents",
      "includedPaths": ".*\\.(pdf|doc|docx|xls|xlsx|ppt|pptx)$",
      "excludedPaths": ".*/(temp|backup|archive)/.*",
      "depth": 10,
      "maxAccessCount": 10000,
      "numOfThread": 3,
      "intervalTime": 300,
      "boost": 1.2,
      "available": "true",
      "sortOrder": 0,
      "versionNo": 1
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_fileconfig_id",
        "created": false
      }
    }

Delete File Crawl Configuration
===============================

Request
-------

::

    DELETE /api/admin/fileconfig/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Path Formats
============

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Protocol
     - Path Format
   * - Local file
     - ``file:///path/to/directory``
   * - Windows share (SMB)
     - ``file://///server/share/path``
   * - SMB with authentication
     - ``smb://username:password@server/share/path``
   * - NFS
     - ``file://///nfs-server/export/path``

Usage Examples
==============

SMB Share Crawl Configuration
-----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/fileconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "SMB Share",
           "paths": "smb://user:pass@server/documents",
           "includedPaths": ".*\\.(pdf|doc|docx)$",
           "excludedPaths": ".*/(temp|private)/.*",
           "maxAccessCount": 50000,
           "numOfThread": 3,
           "intervalTime": 200,
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-webconfig` - Web Crawl Configuration API
- :doc:`api-admin-dataconfig` - Data Store Configuration API
- :doc:`../../admin/fileconfig-guide` - File Crawl Configuration Guide

