==========================
CrawlingInfo API
==========================

Übersicht
=========

Die CrawlingInfo API dient zum Anzeigen und Verwalten von Crawl-Informationen (Crawl-Sitzungen) in |Fess|.
Sie können Crawl-Sitzungen auflisten, einzeln abrufen und löschen.

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
     - /logs
     - Crawl-Informationen auflisten
   * - GET
     - /log/{id}
     - Crawl-Information abrufen
   * - DELETE
     - /log/{id}
     - Crawl-Information löschen
   * - DELETE
     - /all
     - Crawl-Sitzungen gesammelt löschen (laufende ausgenommen)

Crawl-Informationen auflisten
=============================

Request
-------

::

    GET /api/admin/crawlinginfo/logs

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
     - Seitennummer (1-basiert, Standard: 1)
   * - ``sessionId``
     - String
     - Nein
     - Filter nach Sitzungs-ID (Teilübereinstimmung)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "crawling_info_id_1",
            "sessionId": "20250129100000",
            "name": "Default Crawler",
            "expiredTime": "1738200000000",
            "createdTime": 1738108800000
          },
          {
            "id": "crawling_info_id_2",
            "sessionId": "20250128100000",
            "name": "Default Crawler",
            "expiredTime": "1738113600000",
            "createdTime": 1738022400000
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
   * - ``id``
     - Crawl-Informations-ID
   * - ``sessionId``
     - Sitzungs-ID
   * - ``name``
     - Sitzungsname
   * - ``expiredTime``
     - Ablaufzeit (Epoch-Millisekunden; wird als Zeichenkette zurückgegeben)
   * - ``createdTime``
     - Erstellungszeit (Epoch-Millisekunden; wird als Zahl zurückgegeben)

.. note::

   Jedes Log-Objekt in der Antwort enthält außerdem ein internes ``crudMode``-Feld
   (eine Ganzzahl, die den CRUD-Operationsmodus angibt; bei Leseoperationen immer ``0``).
   Clients können dieses Feld gefahrlos ignorieren.

Crawl-Information abrufen
=========================

Request
-------

::

    GET /api/admin/crawlinginfo/log/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "crawling_info_id_1",
          "sessionId": "20250129100000",
          "name": "Default Crawler",
          "expiredTime": "1738200000000",
          "createdTime": 1738108800000
        }
      }
    }

Crawl-Information löschen
=========================

Request
-------

::

    DELETE /api/admin/crawlinginfo/log/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Crawl-Sitzungen gesammelt löschen
======================================

Löscht alle Crawl-Sitzungen (einschließlich ihrer Parameterdaten), mit Ausnahme der gerade
laufenden Sitzungen. Es gibt keine Zeit- oder Altersgrenze; jede Sitzung, die nicht aktiv
läuft, wird gelöscht.

Request
-------

::

    DELETE /api/admin/crawlinginfo/all

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Verwendungsbeispiele
====================

Crawl-Informationen auflisten
-----------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Nach einer bestimmten Sitzung filtern
-------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs?sessionId=20250129100000" \
         -H "Authorization: Bearer YOUR_TOKEN"

Crawl-Information abrufen
-------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/log/crawling_info_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Crawl-Information löschen
-------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/log/crawling_info_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Sitzungen gesammelt löschen
---------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-failureurl` - Fehlgeschlagene URLs API
- :doc:`api-admin-joblog` - Job-Protokoll API
- :doc:`../../admin/crawlinginfo-guide` - Crawl-Informationen Anleitung
