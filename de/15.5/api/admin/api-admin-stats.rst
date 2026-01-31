==========================
Stats API
==========================

Übersicht
=========

Die Stats API dient zum Abrufen von Systemstatistiken in |Fess|.
Sie können Metriken über Suchanfragen, Crawling, Indexierung und Systemressourcen einsehen.

Basis-URL
=========

::

    /api/admin/stats

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
     - Statistiken abrufen

Statistiken abrufen
===================

Request
-------

::

    GET /api/admin/stats

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``from``
     - String
     - Nein
     - Startdatum (ISO 8601)
   * - ``to``
     - String
     - Nein
     - Enddatum (ISO 8601)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "stats": {
          "searchCount": 12345,
          "searchErrorCount": 12,
          "averageResponseTime": 125,
          "documentCount": 50000,
          "indexSize": "1.5GB"
        }
      }
    }

Verwendungsbeispiele
====================

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Mit Zeitraum
    curl -X GET "http://localhost:8080/api/admin/stats?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-systeminfo` - Systeminformationen API
