==========================
CrawlingInfo API
==========================

Übersicht
=========

Die CrawlingInfo API dient zum Abrufen von Crawl-Informationen in |Fess|.
Sie können den Status von Crawl-Sitzungen, Fortschritt und statistische Informationen einsehen.

Basis-URL
=========

::

    /api/admin/crawlinginfo

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
     - Crawl-Informationsliste abrufen
   * - GET
     - /{sessionId}
     - Crawl-Sitzungsdetails abrufen
   * - DELETE
     - /{sessionId}
     - Crawl-Sitzung löschen

Crawl-Informationsliste abrufen
===============================

Request
-------

::

    GET /api/admin/crawlinginfo

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

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "sessions": [
          {
            "sessionId": "session_20250129_100000",
            "name": "Default Crawler",
            "status": "running",
            "startTime": "2025-01-29T10:00:00Z",
            "endTime": null,
            "crawlingInfoCount": 567,
            "createdDocCount": 234,
            "updatedDocCount": 123,
            "deletedDocCount": 12
          },
          {
            "sessionId": "session_20250128_100000",
            "name": "Default Crawler",
            "status": "completed",
            "startTime": "2025-01-28T10:00:00Z",
            "endTime": "2025-01-28T10:45:23Z",
            "crawlingInfoCount": 1234,
            "createdDocCount": 456,
            "updatedDocCount": 678,
            "deletedDocCount": 23
          }
        ],
        "total": 10
      }
    }

Response-Felder
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beschreibung
   * - ``sessionId``
     - Sitzungs-ID
   * - ``name``
     - Crawler-Name
   * - ``status``
     - Status (running/completed/failed)
   * - ``startTime``
     - Startzeit
   * - ``endTime``
     - Endzeit
   * - ``crawlingInfoCount``
     - Anzahl der Crawl-Informationen
   * - ``createdDocCount``
     - Anzahl erstellter Dokumente
   * - ``updatedDocCount``
     - Anzahl aktualisierter Dokumente
   * - ``deletedDocCount``
     - Anzahl gelöschter Dokumente

Crawl-Sitzungsdetails abrufen
=============================

Request
-------

::

    GET /api/admin/crawlinginfo/{sessionId}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session": {
          "sessionId": "session_20250129_100000",
          "name": "Default Crawler",
          "status": "running",
          "startTime": "2025-01-29T10:00:00Z",
          "endTime": null,
          "crawlingInfoCount": 567,
          "createdDocCount": 234,
          "updatedDocCount": 123,
          "deletedDocCount": 12,
          "infos": [
            {
              "url": "https://example.com/page1",
              "status": "OK",
              "method": "GET",
              "httpStatusCode": 200,
              "contentLength": 12345,
              "executionTime": 123,
              "lastModified": "2025-01-29T09:55:00Z"
            }
          ]
        }
      }
    }

Crawl-Sitzung löschen
=====================

Request
-------

::

    DELETE /api/admin/crawlinginfo/{sessionId}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Crawling session deleted successfully"
      }
    }

Verwendungsbeispiele
====================

Crawl-Informationsliste abrufen
-------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Laufende Crawl-Sitzungen abrufen
--------------------------------

.. code-block:: bash

    # Alle Sitzungen abrufen und nach running filtern
    curl -X GET "http://localhost:8080/api/admin/crawlinginfo" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.sessions[] | select(.status=="running")'

Details einer bestimmten Sitzung abrufen
----------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/session_20250129_100000" \
         -H "Authorization: Bearer YOUR_TOKEN"

Alte Sitzung löschen
--------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/session_20250101_100000" \
         -H "Authorization: Bearer YOUR_TOKEN"

Fortschritt überwachen
----------------------

.. code-block:: bash

    # Fortschritt der laufenden Sitzung regelmäßig prüfen
    while true; do
      curl -s "http://localhost:8080/api/admin/crawlinginfo" \
           -H "Authorization: Bearer YOUR_TOKEN" | \
           jq '.response.sessions[] | select(.status=="running") | {sessionId, crawlingInfoCount, createdDocCount}'
      sleep 10
    done

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-failureurl` - Fehlgeschlagene URLs API
- :doc:`api-admin-joblog` - Job-Protokoll API
- :doc:`../../admin/crawlinginfo-guide` - Crawl-Informationen Anleitung
