==========================
General API
==========================

Übersicht
=========

Die General API dient zur Verwaltung der allgemeinen Einstellungen in |Fess|.
Sie können systemweite Konfigurationen abrufen und aktualisieren.

Basis-URL
=========

::

    /api/admin/general

Endpunktliste
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Pfad
     - Beschreibung
   * - GET
     - /settings
     - Allgemeine Einstellungen abrufen
   * - PUT
     - /settings
     - Allgemeine Einstellungen aktualisieren

Allgemeine Einstellungen abrufen
================================

Request
-------

::

    GET /api/admin/general/settings

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "loginRequired": false,
          "loginLink": true,
          "thumbnail": true,
          "supportedSearchPath": "/search",
          "pageSize": 20,
          "pageSizeMax": 100
        }
      }
    }

Allgemeine Einstellungen aktualisieren
======================================

Request
-------

::

    PUT /api/admin/general/settings
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "loginRequired": true,
      "pageSize": 25
    }

Verwendungsbeispiele
====================

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/general/settings" \
         -H "Authorization: Bearer YOUR_TOKEN"

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`../../admin/general-guide` - Allgemeine Einstellungen Anleitung
