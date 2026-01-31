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
    PUT /api/admin/webconfig/settings

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
            "id": "webconfig_id_1",
            "name": "Example Site",
            "urls": "https://example.com/",
            "includedUrls": ".*example\\.com.*",
            "excludedUrls": ".*\\.(pdf|zip)$",
            "includedDocUrls": "",
            "excludedDocUrls": "",
            "configParameter": "",
            "depth": 3,
            "maxAccessCount": 1000,
            "userAgent": "",
            "numOfThread": 1,
            "intervalTime": 1000,
            "boost": 1.0,
            "available": true,
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

Get Web Crawl Configuration
===========================

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
          "urls": "https://example.com/",
          "includedUrls": ".*example\\.com.*",
          "excludedUrls": ".*\\.(pdf|zip)$",
          "includedDocUrls": "",
          "excludedDocUrls": "",
          "configParameter": "",
          "depth": 3,
          "maxAccessCount": 1000,
          "userAgent": "",
          "numOfThread": 1,
          "intervalTime": 1000,
          "boost": 1.0,
          "available": true,
          "sortOrder": 0,
          "permissions": ["admin"],
          "virtualHosts": [],
          "labelTypeIds": []
        }
      }
    }

Create Web Crawl Configuration
==============================

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
      "depth": 5,
      "maxAccessCount": 5000,
      "numOfThread": 3,
      "intervalTime": 500,
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
   * - ``urls``
     - Yes
     - Crawl start URLs (newline-separated for multiple URLs)
   * - ``includedUrls``
     - No
     - Regex pattern for URLs to crawl
   * - ``excludedUrls``
     - No
     - Regex pattern for URLs to exclude from crawling
   * - ``includedDocUrls``
     - No
     - Regex pattern for URLs to index
   * - ``excludedDocUrls``
     - No
     - Regex pattern for URLs to exclude from indexing
   * - ``configParameter``
     - No
     - Additional configuration parameters
   * - ``depth``
     - No
     - Crawl depth (default: -1 = unlimited)
   * - ``maxAccessCount``
     - No
     - Maximum access count (default: 100)
   * - ``userAgent``
     - No
     - Custom User-Agent
   * - ``numOfThread``
     - No
     - Number of parallel threads (default: 1)
   * - ``intervalTime``
     - No
     - Request interval in milliseconds (default: 0)
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
        "id": "new_webconfig_id",
        "created": true
      }
    }

Update Web Crawl Configuration
==============================

Request
-------

::

    PUT /api/admin/webconfig/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_webconfig_id",
      "name": "Updated Corporate Site",
      "urls": "https://www.example.com/",
      "includedUrls": ".*www\\.example\\.com.*",
      "excludedUrls": ".*\\.(pdf|zip|exe|dmg)$",
      "depth": 10,
      "maxAccessCount": 10000,
      "numOfThread": 5,
      "intervalTime": 300,
      "boost": 1.2,
      "available": true,
      "versionNo": 1
    }

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
==============================

Request
-------

::

    DELETE /api/admin/webconfig/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_webconfig_id",
        "created": false
      }
    }

URL Pattern Examples
====================

includedUrls / excludedUrls
---------------------------

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
----------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Corporate Website",
           "urls": "https://www.example.com/",
           "includedUrls": ".*www\\.example\\.com.*",
           "excludedUrls": ".*/(login|admin|api)/.*",
           "depth": 5,
           "maxAccessCount": 10000,
           "numOfThread": 3,
           "intervalTime": 500,
           "available": true,
           "permissions": ["guest"]
         }'

Documentation Site Crawl Configuration
--------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Documentation Site",
           "urls": "https://docs.example.com/",
           "includedUrls": ".*docs\\.example\\.com.*",
           "excludedUrls": "",
           "includedDocUrls": ".*\\.(html|htm)$",
           "depth": -1,
           "maxAccessCount": 50000,
           "numOfThread": 5,
           "intervalTime": 200,
           "boost": 1.5,
           "available": true,
           "labelTypeIds": ["documentation_label_id"]
         }'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-fileconfig` - File Crawl Configuration API
- :doc:`api-admin-dataconfig` - Data Store Configuration API
- :doc:`../../admin/webconfig-guide` - Web Crawl Configuration Guide

