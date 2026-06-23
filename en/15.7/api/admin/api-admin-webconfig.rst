==========================
WebConfig API
==========================

Overview
========

WebConfig API is an API for managing |Fess| web crawl configurations.
You can configure crawl target URLs, crawl depth, exclusion patterns, and more.

Base URL
========

::

    /api/admin/webconfig

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
     - List web crawl configurations
   * - GET
     - /setting/{id}
     - Get web crawl configuration
   * - POST
     - /setting
     - Create web crawl configuration
   * - PUT
     - /setting
     - Update web crawl configuration
   * - DELETE
     - /setting/{id}
     - Delete web crawl configuration

List Web Crawl Configurations
=============================

Request
-------

::

    GET /api/admin/webconfig/settings

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
   * - ``urls``
     - String
     - No
     - Filter by crawl URL
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
            "id": "webconfig_id_1",
            "name": "Example Site",
            "description": "Sample site",
            "urls": "https://example.com/",
            "includedUrls": ".*example\\.com.*",
            "excludedUrls": ".*\\.(pdf|zip)$",
            "includedDocUrls": "",
            "excludedDocUrls": "",
            "configParameter": "",
            "depth": 3,
            "maxAccessCount": 1000,
            "userAgent": "Mozilla/5.0",
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

Get Web Crawl Configuration
============================

Request
-------

::

    GET /api/admin/webconfig/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "webconfig_id_1",
          "name": "Example Site",
          "description": "Sample site",
          "urls": "https://example.com/",
          "includedUrls": ".*example\\.com.*",
          "excludedUrls": ".*\\.(pdf|zip)$",
          "includedDocUrls": "",
          "excludedDocUrls": "",
          "configParameter": "",
          "depth": 3,
          "maxAccessCount": 1000,
          "userAgent": "Mozilla/5.0",
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
   ``versionNo`` is required when updating a configuration (see "Update Web Crawl Configuration" below).

Create Web Crawl Configuration
===============================

Request
-------

::

    POST /api/admin/webconfig/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Corporate Site",
      "urls": "https://www.example.com/",
      "includedUrls": ".*www\\.example\\.com.*",
      "excludedUrls": ".*\\.(pdf|zip|exe)$",
      "userAgent": "Mozilla/5.0",
      "numOfThread": 3,
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
   * - ``urls``
     - Yes
     - Crawl start URLs (newline-separated for multiple URLs). Specify using ``http:`` or ``https:``
   * - ``includedUrls``
     - No
     - Regex pattern for URLs to include in crawling
   * - ``excludedUrls``
     - No
     - Regex pattern for URLs to exclude from crawling
   * - ``includedDocUrls``
     - No
     - Regex pattern for URLs to include in indexing
   * - ``excludedDocUrls``
     - No
     - Regex pattern for URLs to exclude from indexing
   * - ``configParameter``
     - No
     - Additional configuration parameters (``key=value`` format, one entry per line)
   * - ``depth``
     - No
     - Crawl depth (0 or greater)
   * - ``maxAccessCount``
     - No
     - Maximum access count (0 or greater)
   * - ``userAgent``
     - Yes
     - User-Agent string (up to 200 characters)
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
        "id": "new_webconfig_id",
        "created": true
      }
    }

Update Web Crawl Configuration
===============================

Request
-------

::

    PUT /api/admin/webconfig/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

When updating, ``id`` to identify the target configuration and ``versionNo`` are required in addition to the fields used at creation time.
Specify the current value of ``versionNo`` as returned in the GET response.

.. code-block:: json

    {
      "id": "existing_webconfig_id",
      "name": "Updated Corporate Site",
      "urls": "https://www.example.com/",
      "includedUrls": ".*www\\.example\\.com.*",
      "excludedUrls": ".*\\.(pdf|zip|exe|dmg)$",
      "userAgent": "Mozilla/5.0",
      "depth": 10,
      "maxAccessCount": 10000,
      "numOfThread": 5,
      "intervalTime": 300,
      "boost": 1.2,
      "available": "true",
      "sortOrder": 0,
      "versionNo": 1
    }

Additional Fields for Update
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
        "id": "existing_webconfig_id",
        "created": false
      }
    }

Delete Web Crawl Configuration
===============================

Request
-------

::

    DELETE /api/admin/webconfig/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

URL Pattern Examples
====================

``includedUrls`` / ``excludedUrls`` / ``includedDocUrls`` / ``excludedDocUrls`` accept regular expressions.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Pattern
     - Description
   * - ``.*example\\.com.*``
     - All URLs containing example.com
   * - ``https://example\\.com/docs/.*``
     - Only URLs under /docs/
   * - ``.*\\.(pdf|doc|docx)$``
     - PDF, DOC, DOCX files
   * - ``.*\\?.*``
     - URLs with query parameters
   * - ``.*/(login|logout|admin)/.*``
     - URLs containing specific paths

Usage Examples
==============

Corporate Site Crawl Configuration
------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Corporate Website",
           "urls": "https://www.example.com/",
           "includedUrls": ".*www\\.example\\.com.*",
           "excludedUrls": ".*/(login|admin|api)/.*",
           "userAgent": "Mozilla/5.0",
           "depth": 5,
           "maxAccessCount": 10000,
           "numOfThread": 3,
           "intervalTime": 500,
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

Documentation Site Crawl Configuration
----------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Documentation Site",
           "urls": "https://docs.example.com/",
           "includedUrls": ".*docs\\.example\\.com.*",
           "includedDocUrls": ".*\\.(html|htm)$",
           "userAgent": "Mozilla/5.0",
           "maxAccessCount": 50000,
           "numOfThread": 5,
           "intervalTime": 200,
           "boost": 1.5,
           "available": "true",
           "sortOrder": 0
         }'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-fileconfig` - File Crawl Configuration API
- :doc:`api-admin-dataconfig` - Data Store Configuration API
- :doc:`../../admin/webconfig-guide` - Web Crawl Configuration Guide
