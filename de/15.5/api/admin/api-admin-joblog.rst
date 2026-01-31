==========================
JobLog API
==========================

Übersicht
=========

Die JobLog API dient zum Abrufen von Job-Ausführungsprotokollen in |Fess|.
Sie können die Ausführungshistorie von geplanten Jobs und Crawl-Jobs sowie Fehlerinformationen einsehen.

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
     - /
     - Job-Protokollliste abrufen
   * - GET
     - /{id}
     - Job-Protokolldetails abrufen
   * - DELETE
     - /{id}
     - Job-Protokoll löschen
   * - DELETE
     - /delete-all
     - Alle Job-Protokolle löschen

Job-Protokollliste abrufen
==========================

Request
-------

::

    GET /api/admin/joblog

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
   * - ``status``
     - String
     - Nein
     - Status-Filter (ok/fail/running)
   * - ``from``
     - String
     - Nein
     - Startdatum (ISO 8601 Format)
   * - ``to``
     - String
     - Nein
     - Enddatum (ISO 8601 Format)

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
            "startTime": "2025-01-29T02:00:00Z",
            "endTime": "2025-01-29T02:45:23Z",
            "executionTime": 2723000
          },
          {
            "id": "joblog_id_2",
            "jobName": "Default Crawler",
            "jobStatus": "fail",
            "target": "all",
            "scriptType": "groovy",
            "scriptData": "return container.getComponent(\"crawlJob\").execute();",
            "scriptResult": "Error: Connection timeout",
            "startTime": "2025-01-28T02:00:00Z",
            "endTime": "2025-01-28T02:10:15Z",
            "executionTime": 615000
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
     - Job-Status (ok/fail/running)
   * - ``target``
     - Ausführungsziel
   * - ``scriptType``
     - Skript-Typ
   * - ``scriptData``
     - Ausführungsskript
   * - ``scriptResult``
     - Ausführungsergebnis
   * - ``startTime``
     - Startzeit
   * - ``endTime``
     - Endzeit
   * - ``executionTime``
     - Ausführungszeit (Millisekunden)

Job-Protokolldetails abrufen
============================

Request
-------

::

    GET /api/admin/joblog/{id}

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
          "startTime": "2025-01-29T02:00:00Z",
          "endTime": "2025-01-29T02:45:23Z",
          "executionTime": 2723000
        }
      }
    }

Job-Protokoll löschen
=====================

Request
-------

::

    DELETE /api/admin/joblog/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Job log deleted successfully"
      }
    }

Alle Job-Protokolle löschen
===========================

Request
-------

::

    DELETE /api/admin/joblog/delete-all

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
     - Protokolle vor diesem Datum löschen (ISO 8601 Format)
   * - ``status``
     - String
     - Nein
     - Nur Protokolle mit diesem Status löschen

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Job logs deleted successfully",
        "deletedCount": 50
      }
    }

Verwendungsbeispiele
====================

Job-Protokollliste abrufen
--------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Nur fehlgeschlagene Jobs abrufen
--------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?status=fail" \
         -H "Authorization: Bearer YOUR_TOKEN"

Job-Protokolle eines bestimmten Zeitraums
-----------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

Job-Protokolldetails abrufen
----------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/joblog_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Alte Job-Protokolle löschen
---------------------------

.. code-block:: bash

    # Protokolle älter als 30 Tage löschen
    curl -X DELETE "http://localhost:8080/api/admin/joblog/delete-all?before=2024-12-30T00:00:00Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

Nur fehlgeschlagene Job-Protokolle löschen
------------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/joblog/delete-all?status=fail" \
         -H "Authorization: Bearer YOUR_TOKEN"

Jobs mit langer Ausführungszeit finden
--------------------------------------

.. code-block:: bash

    # Jobs extrahieren, die länger als 1 Stunde gedauert haben
    curl -X GET "http://localhost:8080/api/admin/joblog?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs[] | select(.executionTime > 3600000) | {jobName, startTime, executionTime}'

Job-Erfolgsrate berechnen
-------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs | {total: length, ok: [.[] | select(.jobStatus=="ok")] | length, fail: [.[] | select(.jobStatus=="fail")] | length}'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-scheduler` - Scheduler API
- :doc:`api-admin-crawlinginfo` - Crawl-Informationen API
- :doc:`../../admin/joblog-guide` - Job-Protokoll Verwaltungsanleitung
