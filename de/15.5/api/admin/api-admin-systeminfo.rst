==========================
SystemInfo API
==========================

Übersicht
=========

Die SystemInfo API dient zum Abrufen von Systeminformationen in |Fess|.
Sie können Details über die Systemkonfiguration, Java-Version, OpenSearch-Status und mehr einsehen.

Basis-URL
=========

::

    /api/admin/systeminfo

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
     - Systeminformationen abrufen

Systeminformationen abrufen
===========================

Request
-------

::

    GET /api/admin/systeminfo

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "systemInfo": {
          "version": "15.5.0",
          "buildTime": "2025-01-15T10:00:00Z",
          "javaVersion": "21.0.1",
          "javaVendor": "Eclipse Adoptium",
          "osName": "Linux",
          "osVersion": "5.15.0",
          "osArch": "amd64",
          "availableProcessors": 8,
          "freeMemory": 1073741824,
          "totalMemory": 4294967296,
          "maxMemory": 8589934592
        },
        "searchEngineInfo": {
          "clusterName": "fess",
          "status": "green",
          "numberOfNodes": 1,
          "numberOfDataNodes": 1
        }
      }
    }

Verwendungsbeispiele
====================

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN"

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-stats` - Systemstatistiken API
- :doc:`../../admin/systeminfo-guide` - Systeminformationen Anleitung
