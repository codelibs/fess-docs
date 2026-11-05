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
     - /progress
     - Fortschritt laufender Crawls abrufen
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
     - Anzahl der Einträge pro Seite (Standard: 25; änderbar über ``paging.page.size`` in ``fess_config.properties``)
   * - ``page``
     - Integer
     - Nein
     - Seitennummer (1-basiert, Standard: 1)
   * - ``session_id``
     - String
     - Nein
     - Filter nach Sitzungs-ID (Teilübereinstimmung)

Diese Parameter werden im JSON-Anfragekörper angegeben (z. B. ``{"size": 50, "page": 1}``). Werte in der URL-Query-String (z. B. ``?size=50``) werden ignoriert; ohne Angabe im Anfragekörper werden daher immer die ersten 25 Einträge zurückgegeben.

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "crawling_info_id_1",
            "session_id": "20250129100000",
            "name": "Default Crawler",
            "expired_time": "1738200000000",
            "created_time": 1738108800000
          },
          {
            "id": "crawling_info_id_2",
            "session_id": "20250128100000",
            "name": "Default Crawler",
            "expired_time": "1738113600000",
            "created_time": 1738022400000
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
   * - ``session_id``
     - Sitzungs-ID
   * - ``name``
     - Sitzungsname
   * - ``expired_time``
     - Ablaufzeit (Epoch-Millisekunden; wird als Zeichenkette zurückgegeben)
   * - ``created_time``
     - Erstellungszeit (Epoch-Millisekunden; wird als Zahl zurückgegeben)

.. note::

   Jedes Log-Objekt in der Antwort enthält außerdem ein internes ``crud_mode``-Feld
   (eine Ganzzahl, die den CRUD-Operationsmodus angibt; bei Leseoperationen immer ``0``).
   Clients können dieses Feld gefahrlos ignorieren.

Fortschritt laufender Crawls abrufen
====================================

Gibt den Fortschritt der aktuell laufenden Crawls zurück, ein Eintrag je Crawl-Konfiguration (Web, Dateisystem oder Datenspeicher). Es sind dieselben Informationen wie unter „Laufende Crawls" auf der Seite „Crawling-Informationen" der Verwaltungsoberfläche (siehe :doc:`../../admin/crawlinginfo-guide`).

Anfrage
-------

::

    GET /api/admin/crawlinginfo/progress

Dieser Endpunkt akzeptiert keine Parameter.

Antwort
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "progress": [
          {
            "config_id": "Wabc123",
            "name": "Example Site",
            "count": 4200,
            "last_count": 10000,
            "updated_time": 1738144800000,
            "percent": 42
          },
          {
            "config_id": "Ddef456",
            "name": "Example Database",
            "count": 1500,
            "last_count": 0,
            "updated_time": 1738144795000
          }
        ],
        "total": 2
      }
    }

Antwortfelder
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beschreibung
   * - ``progress``
     - Array der laufenden Crawls, sortiert nach dem Namen der Crawl-Konfiguration. Ein leeres Array, wenn kein Crawl läuft
   * - ``total``
     - Anzahl der Elemente von ``progress``

Jedes Element von ``progress`` hat die folgenden Felder.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beschreibung
   * - ``config_id``
     - ID der Crawl-Konfiguration (beginnt mit ``W`` für Web, ``F`` für Dateisystem und ``D`` für Datenspeicher)
   * - ``name``
     - Name der Crawl-Konfiguration (``config_id``, wenn die Konfiguration nicht gefunden wird)
   * - ``count``
     - Anzahl der Dokumente, die der laufende Crawl bisher verarbeitet hat
   * - ``last_count``
     - Dokumentanzahl des vorherigen abgeschlossenen Crawls (``0``, wenn unbekannt)
   * - ``updated_time``
     - Zeitpunkt, zu dem ``count`` geschrieben wurde (Epoch-Millisekunden, eine Zahl)
   * - ``percent``
     - ``count`` in Prozent von ``last_count`` (``0`` bis ``99``). Entfällt, wenn es keinen vorherigen abgeschlossenen Crawl gibt

.. note::

   Ein abgeschlossener oder gestoppter Crawl ist nicht enthalten. Hört der Crawler auf, ohne das zu vermerken (etwa weil der Prozess beendet wird), ist der Crawl nicht mehr enthalten, wenn seit seiner letzten Aktualisierung etwa 30 Sekunden (Standard) vergangen sind. ``count`` eines Web- oder Dateisystem-Crawls ist die Anzahl der Zugriffsergebnisse; ``count`` eines Datenspeicher-Crawls ist die Anzahl der für die Crawl-Konfiguration indexierten Dokumente.

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
          "session_id": "20250129100000",
          "name": "Default Crawler",
          "expired_time": "1738200000000",
          "created_time": 1738108800000
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

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"size": 50, "page": 1}'

Nach einer bestimmten Sitzung filtern
-------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"session_id": "20250129100000"}'

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
