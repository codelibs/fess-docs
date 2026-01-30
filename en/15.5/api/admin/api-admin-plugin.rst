==========================
Plugin API
==========================

Overview
========

Plugin API is an API for managing |Fess| plugins.
You can install, enable, disable, and delete plugins.

Base URL
========

::

    /api/admin/plugin

Endpoint List
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Method
     - Path
     - Description
   * - GET
     - /
     - List plugins
   * - POST
     - /install
     - Install plugin
   * - DELETE
     - /{id}
     - Delete plugin

List Plugins
============

Request
-------

::

    GET /api/admin/plugin

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "plugins": [
          {
            "id": "analysis-kuromoji",
            "name": "Japanese (kuromoji) Analysis Plugin",
            "version": "2.11.0",
            "description": "Japanese language analysis plugin",
            "enabled": true,
            "installed": true
          },
          {
            "id": "analysis-icu",
            "name": "ICU Analysis Plugin",
            "version": "2.11.0",
            "description": "Unicode normalization and collation",
            "enabled": true,
            "installed": true
          }
        ],
        "total": 2
      }
    }

Response Fields
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``id``
     - Plugin ID
   * - ``name``
     - Plugin name
   * - ``version``
     - Plugin version
   * - ``description``
     - Plugin description
   * - ``enabled``
     - Enabled status
   * - ``installed``
     - Installation status

Install Plugin
==============

Request
-------

::

    POST /api/admin/plugin/install
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "url": "https://example.com/plugins/my-plugin-1.0.0.zip"
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Required
     - Description
   * - ``url``
     - Yes
     - Plugin download URL

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Plugin installed successfully. Restart required.",
        "pluginId": "my-plugin"
      }
    }

Delete Plugin
=============

Request
-------

::

    DELETE /api/admin/plugin/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Plugin deleted successfully. Restart required."
      }
    }

Usage Examples
==============

List Plugins
------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN"

Install Plugin
--------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/plugin/install" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "url": "https://artifacts.opensearch.org/releases/plugins/analysis-icu/2.11.0/analysis-icu-2.11.0.zip"
         }'

Delete Plugin
-------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/plugin/analysis-icu" \
         -H "Authorization: Bearer YOUR_TOKEN"

Important Notes
===============

- A Fess restart is required after installing or deleting plugins
- Installing incompatible plugins may prevent Fess from starting
- Delete plugins carefully. If there are dependencies, it may affect the system

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-systeminfo` - System Info API
- :doc:`../../admin/plugin-guide` - Plugin Management Guide

