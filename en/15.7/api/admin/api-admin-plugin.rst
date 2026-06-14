==========================
Plugin API
==========================

Overview
========

Plugin API is an API for managing |Fess| plugins (artifacts).
You can list installed and installable plugins, and install or delete plugins.

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
     - /installed
     - List installed plugins
   * - GET
     - /available
     - List installable plugins
   * - POST
     - /
     - Install plugin
   * - DELETE
     - /
     - Delete plugin

List Installed Plugins
======================

Returns a list of installed plugins.

Request
-------

::

    GET /api/admin/plugin/installed

Response
--------

``plugins`` contains an array of objects representing plugin information.
Each object is a map of string keys and values, including ``name`` (plugin name), ``version`` (version), and so on.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "plugins": [
          {
            "name": "fess-ds-slack",
            "version": "15.7.0"
          }
        ]
      }
    }

List Installable Plugins
========================

Returns a list of installable plugins.

Request
-------

::

    GET /api/admin/plugin/available

Response
--------

``plugins`` contains an array of objects representing installable plugin information.
As with ``installed``, each object is a map of string keys and values.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "plugins": [
          {
            "name": "fess-ds-slack",
            "version": "15.7.0"
          }
        ]
      }
    }

Install Plugin
==============

Installs the plugin with the specified name and version.

Request
-------

::

    POST /api/admin/plugin
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "fess-ds-slack",
      "version": "15.7.0"
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Field
     - Required
     - Description
   * - ``name``
     - Yes
     - Plugin name (max 100 characters)
   * - ``version``
     - Yes
     - Plugin version (max 100 characters)

Response
--------

On success, only ``status`` is returned.
If no artifact matches the specified ``name`` or ``version``, ``status`` becomes ``1`` (BAD_REQUEST) and ``message`` is set to ``invalid name or version``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Delete Plugin
=============

Deletes the plugin with the specified name and version.

Request
-------

::

    DELETE /api/admin/plugin
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "fess-ds-slack",
      "version": "15.7.0"
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Field
     - Required
     - Description
   * - ``name``
     - Yes
     - Plugin name (max 100 characters)
   * - ``version``
     - No
     - Plugin version (max 100 characters)

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Usage Examples
==============

List Installed Plugins
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/plugin/installed" \
         -H "Authorization: Bearer YOUR_TOKEN"

Install Plugin
--------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "fess-ds-slack",
           "version": "15.7.0"
         }'

Delete Plugin
-------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "fess-ds-slack",
           "version": "15.7.0"
         }'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
