==========================
Plugin API
==========================

Übersicht
=========

Die Plugin API dient zur Verwaltung von Plugins in |Fess|.
Sie können Plugins installieren, deinstallieren und auflisten.

Basis-URL
=========

::

    /api/admin/plugin

Endpunktliste
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Pfad
     - Beschreibung
   * - GET
     - /
     - Installierte Plugins auflisten
   * - GET
     - /available
     - Verfügbare Plugins auflisten
   * - POST
     - /install
     - Plugin installieren
   * - DELETE
     - /{name}
     - Plugin deinstallieren

Installierte Plugins auflisten
==============================

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
            "name": "fess-ds-csv",
            "version": "15.5.0",
            "status": "active"
          },
          {
            "name": "fess-webapp-classic-api",
            "version": "15.5.0",
            "status": "active"
          }
        ]
      }
    }

Verfügbare Plugins auflisten
============================

Request
-------

::

    GET /api/admin/plugin/available

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "plugins": [
          {
            "name": "fess-ds-slack",
            "version": "15.5.0",
            "description": "Slack DataStore connector"
          }
        ]
      }
    }

Plugin installieren
===================

Request
-------

::

    POST /api/admin/plugin/install
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "fess-ds-slack",
      "version": "15.5.0"
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Plugin installed successfully"
      }
    }

Plugin deinstallieren
=====================

Request
-------

::

    DELETE /api/admin/plugin/{name}

Verwendungsbeispiele
====================

Installierte Plugins auflisten
------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN"

Plugin installieren
-------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/plugin/install" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "fess-ds-slack",
           "version": "15.5.0"
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`../../admin/plugin-guide` - Plugin Verwaltungsanleitung
