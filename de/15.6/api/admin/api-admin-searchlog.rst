==========================
SearchLog API
==========================

Übersicht
=========

Die SearchLog API dient zum Abrufen und Verwalten von Suchprotokollen in |Fess|.
Sie können Suchanfragen analysieren und Statistiken über das Suchverhalten der Benutzer einsehen.

Basis-URL
=========

::

    /api/admin/searchlog

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
     - Suchprotokolle auflisten
   * - GET
     - /stats
     - Suchstatistiken abrufen
   * - DELETE
     - /
     - Suchprotokolle löschen

Suchprotokolle auflisten
========================

Request
-------

::

    GET /api/admin/searchlog

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``size``
     - Integer
     - Nein
     - Anzahl der Einträge pro Seite (Standard: 20)
   * - ``page``
     - Integer
     - Nein
     - Seitennummer (beginnt bei 0)
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
        "logs": [
          {
            "id": "log_1",
            "searchWord": "fess installation",
            "hitCount": 25,
            "responseTime": 150,
            "requestedAt": "2025-01-29T10:00:00Z",
            "userAgent": "Mozilla/5.0...",
            "clientIp": "192.168.1.1"
          }
        ],
        "total": 1000
      }
    }

Suchstatistiken abrufen
=======================

Request
-------

::

    GET /api/admin/searchlog/stats

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
          "totalSearches": 10000,
          "uniqueKeywords": 2500,
          "averageResponseTime": 125,
          "zeroResultSearches": 150,
          "topKeywords": [
            {"word": "fess", "count": 500},
            {"word": "install", "count": 300},
            {"word": "configuration", "count": 200}
          ]
        }
      }
    }

Suchprotokolle löschen
======================

Request
-------

::

    DELETE /api/admin/searchlog

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``before``
     - String
     - Nein
     - Protokolle vor diesem Datum löschen (ISO 8601)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Search logs deleted successfully",
        "deletedCount": 5000
      }
    }

Verwendungsbeispiele
====================

Suchprotokolle auflisten
------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?size=50" \
         -H "Authorization: Bearer YOUR_TOKEN"

Suchstatistiken abrufen
-----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog/stats?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

Alte Protokolle löschen
-----------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/searchlog?before=2024-01-01" \
         -H "Authorization: Bearer YOUR_TOKEN"

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`../../admin/searchlog-guide` - Suchprotokoll Verwaltungsanleitung
