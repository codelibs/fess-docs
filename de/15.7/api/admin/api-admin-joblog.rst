==========================
JobLog API
==========================

Übersicht
=========

Die JobLog API dient zum Anzeigen und Verwalten von Job-Ausführungsprotokollen in |Fess|.
Sie können die Ausführungshistorie von geplanten Jobs und Crawl-Jobs, Ausführungsergebnisse und Fehlerinformationen abrufen und löschen.

Basis-URL
=========

::

    /api/admin/joblog

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
     - Job-Protokolle auflisten
   * - GET
     - /log/{id}
     - Job-Protokoll abrufen
   * - DELETE
     - /log/{id}
     - Job-Protokoll löschen

Job-Protokolle auflisten
========================

Request
-------

::

    GET /api/admin/joblog/logs

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
   * - ``id``
     - String
     - Nein
     - Filter nach Job-Protokoll-ID (vollständige Übereinstimmung)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "joblog_id_1",
            "jobName": "Default Crawler",
            "jobStatus": "ok",
            "target": "all",
            "scriptType": "groovy",
            "scriptData": "return container.getComponent(\"crawlJob\").execute();",
            "scriptResult": "Job completed successfully",
            "startTime": "1738116000000",
            "endTime": "1738118723000"
          },
          {
            "id": "joblog_id_2",
            "jobName": "Default Crawler",
            "jobStatus": "fail",
            "target": "all",
            "scriptType": "groovy",
            "scriptData": "return container.getComponent(\"crawlJob\").execute();",
            "scriptResult": "Error: Connection timeout",
            "startTime": "1738029600000",
            "endTime": "1738030215000"
          }
        ],
        "total": 100
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
     - Job-Protokoll-ID
   * - ``jobName``
     - Job-Name
   * - ``jobStatus``
     - Job-Status (``ok``: Erfolg, ``fail``: Fehlgeschlagen, ``running``: Wird ausgeführt)
   * - ``target``
     - Ausführungsziel (Zielname des Schedulers; Standardwert ist ``all``)
   * - ``scriptType``
     - Skript-Typ (z. B. ``groovy``)
   * - ``scriptData``
     - Ausführungsskript
   * - ``scriptResult``
     - Ausführungsergebnis
   * - ``startTime``
     - Startzeit (Epoch-Millisekunden; wird als Zeichenkette zurückgegeben)
   * - ``endTime``
     - Endzeit (Epoch-Millisekunden; wird als Zeichenkette zurückgegeben). Bei laufenden Jobs nicht vorhanden.

.. note::

   Jedes Log-Objekt in der Antwort enthält außerdem ein internes ``crudMode``-Feld
   (eine Ganzzahl, die den CRUD-Operationsmodus angibt; bei Leseoperationen immer ``0``).
   Clients können dieses Feld gefahrlos ignorieren.

Job-Protokoll abrufen
=====================

Request
-------

::

    GET /api/admin/joblog/log/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "joblog_id_1",
          "jobName": "Default Crawler",
          "jobStatus": "ok",
          "target": "all",
          "scriptType": "groovy",
          "scriptData": "return container.getComponent(\"crawlJob\").execute();",
          "scriptResult": "Crawl completed successfully.\nDocuments indexed: 1234\nDocuments updated: 567\nDocuments deleted: 12\nErrors: 0",
          "startTime": "1738116000000",
          "endTime": "1738118723000"
        }
      }
    }

Wenn das Job-Protokoll mit der angegebenen ID nicht vorhanden ist, wird eine Fehler-Response
zurückgegeben, bei der ``status`` einen von 0 verschiedenen Wert enthält.

Job-Protokoll löschen
=====================

Request
-------

::

    DELETE /api/admin/joblog/log/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Wenn das Job-Protokoll mit der angegebenen ID nicht vorhanden ist, wird eine Fehler-Response
zurückgegeben, bei der ``status`` einen von 0 verschiedenen Wert enthält.

Verwendungsbeispiele
====================

Job-Protokolle auflisten
------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/logs?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Nur fehlgeschlagene Jobs filtern
---------------------------------

.. code-block:: bash

    # Fehlgeschlagene Jobs mit jq filtern
    curl -X GET "http://localhost:8080/api/admin/joblog/logs?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs[] | select(.jobStatus=="fail")'

Job-Protokoll abrufen
---------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/log/joblog_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Job-Protokoll löschen
---------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/joblog/log/joblog_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Job-Erfolgsrate berechnen
-------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/logs?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs | {total: length, ok: [.[] | select(.jobStatus=="ok")] | length, fail: [.[] | select(.jobStatus=="fail")] | length}'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-scheduler` - Scheduler API
- :doc:`api-admin-crawlinginfo` - Crawl-Informationen API
- :doc:`../../admin/joblog-guide` - Job-Protokoll Verwaltungsanleitung
