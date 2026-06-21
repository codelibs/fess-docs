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

Plugin Information Fields
=========================

Each element of the ``plugins`` array returned by the list endpoints (``/installed`` and ``/available``)
is an object with the following fields.

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Field
     - Description
   * - ``type``
     - The artifact type ID. One of ``fess-ds`` (data store), ``fess-theme`` (theme),
       ``fess-ingest`` (ingest), ``fess-script`` (script), ``fess-webapp`` (web app),
       ``fess-thumbnail`` (thumbnail), ``fess-crawler`` (crawler), ``fess-llm`` (LLM),
       or ``jar`` (generic JAR not matching any of the above).
   * - ``id``
     - Identifier in ``{name}:{version}`` format.
   * - ``name``
     - Plugin name.
   * - ``version``
     - Plugin version.
   * - ``url``
     - URL of the download source. Included only in the ``/available`` response. Omitted
       from ``/installed`` responses because no value exists.

.. note::

   In |Fess| API responses, fields whose value is ``null`` are not output. Therefore,
   ``url`` is not included in each element of installed plugins.

List Installed Plugins
======================

Returns a list of installed plugins. Artifacts in the plugin directory are scanned
by type and returned sorted by name.

Request
-------

::

    GET /api/admin/plugin/installed

Response
--------

``plugins`` contains an array of objects representing plugin information.
See `Plugin Information Fields`_ for the fields of each object.
``url`` is not output for installed plugins.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "plugins": [
          {
            "type": "fess-ds",
            "id": "fess-ds-slack:15.7.0",
            "name": "fess-ds-slack",
            "version": "15.7.0"
          }
        ]
      }
    }

List Installable Plugins
========================

Returns a list of installable plugins. Artifacts of all types are fetched from the
repositories configured in ``plugin.repositories`` in ``fess_config.properties``.
The results are cached for a fixed period (5 minutes by default).

Request
-------

::

    GET /api/admin/plugin/available

Response
--------

``plugins`` contains an array of objects representing installable plugin information.
See `Plugin Information Fields`_ for the fields of each object.
For installable plugins, the download source ``url`` is included.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "plugins": [
          {
            "type": "fess-ds",
            "id": "fess-ds-slack:15.7.0",
            "name": "fess-ds-slack",
            "version": "15.7.0",
            "url": "https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-slack/15.7.0/fess-ds-slack-15.7.0.jar"
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

.. note::

   ``name`` and ``version`` must match one of the installable plugins obtainable via
   ``/available``. If no matching artifact exists, an error is returned.

Response
--------

When the request is accepted, a response with ``status`` ``0`` (OK) is returned.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

If no artifact matching the specified ``name`` or ``version`` exists, ``status`` becomes
``1`` (BAD_REQUEST) and ``message`` is set to ``invalid name or version``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 1,
        "message": "invalid name or version"
      }
    }

.. note::

   Installation is performed asynchronously in the background. A ``status: 0`` response
   indicates that the request was accepted, not that installation has completed. After
   installation completes, any previously installed plugins with the same name but a
   different version are automatically removed. If a download or installation failure
   occurs, it is recorded in the server log but is not reflected in the API response.

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
     - Plugin version (max 100 characters). Recommended to specify in order to uniquely identify the plugin to delete.

Response
--------

When the request is accepted, a response with ``status`` ``0`` (OK) is returned.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

.. note::

   Deletion is performed asynchronously in the background. A ``status: 0`` response
   indicates that the request was accepted; it does not determine whether the target
   plugin exists or whether deletion succeeded. If deletion fails (e.g., the target
   file does not exist), the failure is recorded in the server log but is not reflected
   in the API response.

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
