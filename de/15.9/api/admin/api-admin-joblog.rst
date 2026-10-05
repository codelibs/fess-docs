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
            "job_name": "Default Crawler",
            "job_status": "ok",
            "target": "all",
            "script_type": "javascript",
            "script_data": "return container.getComponent(\"crawlJob\").execute();",
            "script_result": "Job completed successfully",
            "start_time": "1738116000000",
            "end_time": "1738118723000"
          },
          {
            "id": "joblog_id_2",
            "job_name": "Default Crawler",
            "job_status": "fail",
            "target": "all",
            "script_type": "javascript",
            "script_data": "return container.getComponent(\"crawlJob\").execute();",
            "script_result": "Error: Connection timeout",
            "start_time": "1738029600000",
            "end_time": "1738030215000"
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
   * - ``job_name``
     - Job-Name
   * - ``job_status``
     - Job-Status (``ok``: Erfolg, ``fail``: Fehlgeschlagen, ``running``: Wird ausgeführt)
   * - ``target``
     - Ausführungsziel (Zielname des Schedulers; Standardwert ist ``all``)
   * - ``script_type``
     - Skript-Typ (z. B. ``javascript``)
   * - ``script_data``
     - Ausführungsskript
   * - ``script_result``
     - Ausführungsergebnis
   * - ``start_time``
     - Startzeit (Epoch-Millisekunden; wird als Zeichenkette zurückgegeben)
   * - ``end_time``
     - Endzeit (Epoch-Millisekunden; wird als Zeichenkette zurückgegeben). Bei laufenden Jobs nicht vorhanden.

.. note::

   Jedes Log-Objekt in der Antwort enthält außerdem ein internes ``crud_mode``-Feld
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
          "job_name": "Default Crawler",
          "job_status": "ok",
          "target": "all",
          "script_type": "javascript",
          "script_data": "return container.getComponent(\"crawlJob\").execute();",
          "script_result": "Crawl completed successfully.\nDocuments indexed: 1234\nDocuments updated: 567\nDocuments deleted: 12\nErrors: 0",
          "start_time": "1738116000000",
          "end_time": "1738118723000"
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

    curl -X GET "http://localhost:8080/api/admin/joblog/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"size": 50, "page": 1}'

Nur fehlgeschlagene Jobs filtern
---------------------------------

.. code-block:: bash

    # Fehlgeschlagene Jobs mit jq filtern
    curl -X GET "http://localhost:8080/api/admin/joblog/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"size": 1000}' | \
         jq '.response.logs[] | select(.job_status=="fail")'

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

    curl -X GET "http://localhost:8080/api/admin/joblog/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"size": 1000}' | \
         jq '.response.logs | {total: length, ok: [.[] | select(.job_status=="ok")] | length, fail: [.[] | select(.job_status=="fail")] | length}'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-scheduler` - Scheduler API
- :doc:`api-admin-crawlinginfo` - Crawl-Informationen API
- :doc:`../../admin/joblog-guide` - Job-Protokoll Verwaltungsanleitung
