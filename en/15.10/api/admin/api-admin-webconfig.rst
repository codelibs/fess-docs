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
            "included_urls": ".*example\\.com.*",
            "excluded_urls": ".*\\.(pdf|zip)$",
            "included_doc_urls": "",
            "excluded_doc_urls": "",
            "config_parameter": "",
            "depth": 3,
            "max_access_count": 1000,
            "user_agent": "Mozilla/5.0",
            "num_of_thread": 1,
            "interval_time": 1000,
            "boost": 1.0,
            "available": "true",
            "permissions": "{role}admin",
            "virtual_hosts": "",
            "sort_order": 0
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
          "included_urls": ".*example\\.com.*",
          "excluded_urls": ".*\\.(pdf|zip)$",
          "included_doc_urls": "",
          "excluded_doc_urls": "",
          "config_parameter": "",
          "depth": 3,
          "max_access_count": 1000,
          "user_agent": "Mozilla/5.0",
          "num_of_thread": 1,
          "interval_time": 1000,
          "boost": 1.0,
          "available": "true",
          "sort_order": 0,
          "permissions": "{role}admin",
          "virtual_hosts": "",
          "created_by": "admin",
          "created_time": 1700000000000,
          "updated_by": "admin",
          "updated_time": 1700000000000,
          "version_no": 1
        }
      }
    }

.. note::

   The response includes ``created_by``, ``created_time``, ``updated_by``, ``updated_time``, and ``version_no``,
   which are automatically populated by the server when a configuration is created or updated.
   ``version_no`` is required when updating a configuration (see "Update Web Crawl Configuration" below).

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
      "included_urls": ".*www\\.example\\.com.*",
      "excluded_urls": ".*\\.(pdf|zip|exe)$",
      "user_agent": "Mozilla/5.0",
      "num_of_thread": 3,
      "interval_time": 500,
      "boost": 1.0,
      "available": "true",
      "sort_order": 0,
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
   * - ``included_urls``
     - No
     - Regex pattern for URLs to include in crawling
   * - ``excluded_urls``
     - No
     - Regex pattern for URLs to exclude from crawling
   * - ``included_doc_urls``
     - No
     - Regex pattern for URLs to include in indexing
   * - ``excluded_doc_urls``
     - No
     - Regex pattern for URLs to exclude from indexing
   * - ``config_parameter``
     - No
     - Additional configuration parameters (``key=value`` format, one entry per line)
   * - ``depth``
     - No
     - Crawl depth (0 or greater)
   * - ``max_access_count``
     - No
     - Maximum access count (0 or greater)
   * - ``user_agent``
     - Yes
     - User-Agent string (up to 200 characters)
   * - ``num_of_thread``
     - Yes
     - Number of parallel threads (1 or greater)
   * - ``interval_time``
     - Yes
     - Access interval in milliseconds (0 or greater)
   * - ``boost``
     - Yes
     - Search result boost value
   * - ``available``
     - Yes
     - Enable/disable (string ``"true"`` / ``"false"``)
   * - ``sort_order``
     - Yes
     - Display order (0 or greater)
   * - ``permissions``
     - No
     - Access permission roles (newline-separated for multiple values)
   * - ``virtual_hosts``
     - No
     - Virtual hosts (newline-separated for multiple values)

.. note::

   Audit fields such as ``created_by``, ``created_time``, ``updated_by``, and ``updated_time`` are
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

When updating, ``id`` to identify the target configuration and ``version_no`` are required in addition to the fields used at creation time.
Specify the current value of ``version_no`` as returned in the GET response.

.. code-block:: json

    {
      "id": "existing_webconfig_id",
      "name": "Updated Corporate Site",
      "urls": "https://www.example.com/",
      "included_urls": ".*www\\.example\\.com.*",
      "excluded_urls": ".*\\.(pdf|zip|exe|dmg)$",
      "user_agent": "Mozilla/5.0",
      "depth": 10,
      "max_access_count": 10000,
      "num_of_thread": 5,
      "interval_time": 300,
      "boost": 1.2,
      "available": "true",
      "sort_order": 0,
      "version_no": 1
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
   * - ``version_no``
     - Yes
     - Current version number of the configuration to update. Use the ``version_no`` value from the GET response.

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

``included_urls`` / ``excluded_urls`` / ``included_doc_urls`` / ``excluded_doc_urls`` accept regular expressions.

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
           "included_urls": ".*www\\.example\\.com.*",
           "excluded_urls": ".*/(login|admin|api)/.*",
           "user_agent": "Mozilla/5.0",
           "depth": 5,
           "max_access_count": 10000,
           "num_of_thread": 3,
           "interval_time": 500,
           "boost": 1.0,
           "available": "true",
           "sort_order": 0,
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
           "included_urls": ".*docs\\.example\\.com.*",
           "included_doc_urls": ".*\\.(html|htm)$",
           "user_agent": "Mozilla/5.0",
           "max_access_count": 50000,
           "num_of_thread": 5,
           "interval_time": 200,
           "boost": 1.5,
           "available": "true",
           "sort_order": 0
         }'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-fileconfig` - File Crawl Configuration API
- :doc:`api-admin-dataconfig` - Data Store Configuration API
- :doc:`../../admin/webconfig-guide` - Web Crawl Configuration Guide
