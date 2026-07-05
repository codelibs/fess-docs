==========================
FileConfig API
==========================

Overview
========

FileConfig API is an API for managing |Fess| file crawl configurations.
You can configure crawl settings for local file systems, SMB/CIFS shared folders, FTP, and various object storage services.

Base URL
========

::

    /api/admin/fileconfig

.. note::

   All endpoints require administrator privileges and a valid access token.
   Refer to :doc:`api-admin-overview` for authentication details.

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

.. note::

   The list endpoint is also accessible via ``PUT`` in addition to ``GET``.

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 10 55

   * - Parameter
     - Type
     - Required
     - Description
   * - ``page``
     - Integer
     - No
     - Page number (1-based, default: 1)
   * - ``size``
     - Integer
     - No
     - Number of items per page (default: 25, follows the ``paging.page.size`` setting)
   * - ``name``
     - String
     - No
     - Filter by configuration name
   * - ``paths``
     - String
     - No
     - Filter by crawl path
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
            "id": "fileconfig_id_1",
            "name": "Shared Documents",
            "description": "Shared documents",
            "paths": "smb://server/share/documents",
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

``total`` represents the total number of configurations matching the filter conditions.

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
          "paths": "smb://server/share/documents",
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
          "createdBy": "admin",
          "createdTime": 1700000000000,
          "updatedBy": "admin",
          "updatedTime": 1700000000000,
          "versionNo": 1
        }
      }
    }

.. note::

   The response includes ``createdBy``, ``createdTime``, ``updatedBy``, ``updatedTime``, and ``versionNo``,
   which are automatically populated by the server when a configuration is created or updated.
   ``versionNo`` is required when updating a configuration (see "Update File Crawl Configuration" below).

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
      "permissions": "{role}admin\n{role}user"
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Field
     - Required
     - Description
   * - ``name``
     - Yes
     - Configuration name (up to 200 characters)
   * - ``description``
     - No
     - Configuration description (up to 1000 characters)
   * - ``paths``
     - Yes
     - Crawl start paths (newline-separated for multiple paths). Specify using one of the following protocols: ``file:``, ``smb:``, ``smb1:``, ``ftp:``, ``storage:``, ``s3:``, or ``gcs:``
   * - ``includedPaths``
     - No
     - Regex pattern for paths to include in crawling
   * - ``excludedPaths``
     - No
     - Regex pattern for paths to exclude from crawling
   * - ``includedDocPaths``
     - No
     - Regex pattern for paths to include in indexing
   * - ``excludedDocPaths``
     - No
     - Regex pattern for paths to exclude from indexing
   * - ``configParameter``
     - No
     - Additional configuration parameters (``key=value`` format, one entry per line)
   * - ``depth``
     - No
     - Crawl depth (0 or greater)
   * - ``maxAccessCount``
     - No
     - Maximum access count (0 or greater)
   * - ``numOfThread``
     - Yes
     - Number of parallel threads (1 or greater)
   * - ``intervalTime``
     - Yes
     - Access interval in milliseconds (0 or greater)
   * - ``boost``
     - Yes
     - Search result boost value
   * - ``available``
     - Yes
     - Enable/disable (string ``"true"`` / ``"false"``)
   * - ``sortOrder``
     - Yes
     - Display order (0 or greater)
   * - ``permissions``
     - No
     - Access permission roles (newline-separated for multiple values)
   * - ``virtualHosts``
     - No
     - Virtual hosts (newline-separated for multiple values)

.. note::

   Audit fields such as ``createdBy``, ``createdTime``, ``updatedBy``, and ``updatedTime`` are
   automatically set by the server and do not need to be included in the request body.

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

When updating, ``id`` to identify the target configuration and ``versionNo`` are required in addition to the fields used at creation time.
Specify the current value of ``versionNo`` as returned in the GET response.

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

Additional Fields for Update
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Field
     - Required
     - Description
   * - ``id``
     - Yes
     - ID of the configuration to update (up to 1000 characters)
   * - ``versionNo``
     - Yes
     - Current version number of the configuration to update. Use the ``versionNo`` value from the GET response.

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

The following protocols can be used in ``paths`` (the supported protocols can be changed via the ``crawler.file.protocols`` setting).

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Protocol
     - Path Format
   * - Local file
     - ``file:///path/to/directory``
   * - SMB/CIFS share
     - ``smb://server/share/path``
   * - SMB/CIFS share (SMB1)
     - ``smb1://server/share/path``
   * - FTP
     - ``ftp://server/path``
   * - S3-compatible object storage (MinIO, etc.)
     - ``storage://bucket/path``
   * - Amazon S3
     - ``s3://bucket/path``
   * - Google Cloud Storage
     - ``gcs://bucket/path``

.. note::

   Credentials (username and password) for SMB/CIFS or FTP access should not be embedded in the path.
   Configure them in the File Authentication settings instead. See :doc:`../../admin/fileauth-guide` for details.

Usage Examples
==============

Local File Crawl Configuration
------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/fileconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Local Files",
           "paths": "file:///data/documents",
           "includedPaths": ".*\\.(pdf|doc|docx)$",
           "excludedPaths": ".*/(temp|backup)/.*",
           "numOfThread": 2,
           "intervalTime": 500,
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

SMB Share Crawl Configuration
-----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/fileconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "SMB Share",
           "paths": "smb://server/documents",
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

.. note::

   If authentication is required to access an SMB share, register the credentials for the target host
   in the File Authentication settings beforehand.

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-webconfig` - Web Crawl Configuration API
- :doc:`api-admin-dataconfig` - Data Store Configuration API
- :doc:`../../admin/fileconfig-guide` - File Crawl Configuration Guide
- :doc:`../../admin/fileauth-guide` - File Authentication Configuration Guide
