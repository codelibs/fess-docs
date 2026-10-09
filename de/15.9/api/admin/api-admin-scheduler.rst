==========================
Scheduler API
==========================

Übersicht
=========

Die Scheduler API dient zur Verwaltung von geplanten Jobs in |Fess|.
Sie können Crawl-Jobs starten/stoppen sowie Zeitplan-Einstellungen erstellen, aktualisieren und löschen.

Basis-URL
=========

::

    /api/admin/scheduler

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
     - Geplante Jobs auflisten
   * - GET
     - /setting/{id}
     - Geplanten Job abrufen
   * - POST
     - /setting
     - Geplanten Job erstellen
   * - PUT
     - /setting
     - Geplanten Job aktualisieren
   * - DELETE
     - /setting/{id}
     - Geplanten Job löschen
   * - PUT
     - /{id}/start
     - Job starten
   * - PUT
     - /{id}/stop
     - Job stoppen

Geplante Jobs auflisten
=======================

Request
-------

::

    GET /api/admin/scheduler/settings

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
     - Anzahl der Einträge pro Seite (Standard: 25; konfigurierbar über ``paging.page.size`` in ``fess_config.properties``)
   * - ``page``
     - Integer
     - Nein
     - Seitennummer (1-basiert; Standard: 1)

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.9",
        "status": 0,
        "settings": [
          {
            "id": "job_id_1",
            "name": "Default Crawler",
            "target": "all",
            "cron_expression": "0 0 * * *",
            "script_type": "javascript",
            "script_data": "...",
            "job_logging": "true",
            "crawler": "true",
            "available": "true",
            "sort_order": 0,
            "version_no": 1,
            "running": false
          }
        ],
        "total": 5
      }
    }

.. note::

   Das ``response``-Objekt enthält stets ``version`` (Produktversion) und ``status`` (Ergebniscode). Die gemeinsame Antwortstruktur ist in :doc:`api-admin-overview` beschrieben. In späteren Beispielen kann ``version`` der Übersichtlichkeit halber weggelassen werden.

.. note::

   Im Response werden ``job_logging`` / ``crawler`` / ``available`` als Zeichenketten (``"true"`` / ``"false"``) zurückgegeben. ``running`` ist ein boolescher Wert und ein reines Response-Feld, das anzeigt, ob der Job gerade ausgeführt wird (kann im Request nicht gesetzt werden). ``total`` ist die Gesamtanzahl der zur Abfrage passenden Jobs.

Geplanten Job abrufen
=====================

Request
-------

::

    GET /api/admin/scheduler/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "job_id_1",
          "name": "Default Crawler",
          "target": "all",
          "cron_expression": "0 0 * * *",
          "script_type": "javascript",
          "script_data": "return container.getComponent(\"crawlJob\").execute();",
          "job_logging": "true",
          "crawler": "true",
          "available": "true",
          "sort_order": 0,
          "version_no": 1,
          "running": false
        }
      }
    }

Geplanten Job erstellen
=======================

Request
-------

::

    POST /api/admin/scheduler/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Daily Crawler",
      "target": "all",
      "cron_expression": "0 2 * * *",
      "script_type": "javascript",
      "script_data": "return container.getComponent(\"crawlJob\").execute();",
      "job_logging": "true",
      "crawler": "true",
      "available": "true",
      "sort_order": 1
    }

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``name``
     - Ja
     - Job-Name (max. 100 Zeichen)
   * - ``target``
     - Ja
     - Ausführungsziel (max. 100 Zeichen). ``all`` oder einen bestimmten Zielnamen angeben
   * - ``cron_expression``
     - Nein
     - Cron-Ausdruck (fünf Felder: Minute Stunde Tag Monat Wochentag, im cron4j-Format). Max. 100 Zeichen, wird als Cron-Ausdruck validiert. Ein Sekundenfeld im Quartz-Stil und ``?`` sind nicht möglich (``0 0 * * * ?`` wird abgelehnt). Ist das Feld leer, wird der Job nicht geplant und kann nur manuell gestartet werden
   * - ``script_type``
     - Ja
     - Skript-Typ (max. 100 Zeichen). ``javascript`` (Standard für neue Jobs, festgelegt über die Eigenschaft ``job.default.script``) oder ``groovy`` (erfordert das Plugin ``fess-script-groovy``)
   * - ``script_data``
     - Nein
     - Ausführungsskript. Die maximale Größe richtet sich nach ``form.admin.max.input.size`` in ``fess_config.properties``
   * - ``job_logging``
     - Nein
     - Job-Protokollierung aktivieren (Zeichenkette)
   * - ``crawler``
     - Nein
     - Ob es ein Crawler-Job ist (Zeichenkette)
   * - ``available``
     - Nein
     - Aktiviert/Deaktiviert (Zeichenkette)
   * - ``sort_order``
     - Ja
     - Anzeigereihenfolge (Ganzzahl zwischen 0 und 2147483647)

.. note::

   ``job_logging`` / ``crawler`` / ``available`` sind Zeichenkettenfelder. Im Request aktiviert die Angabe von ``"on"`` oder ``"true"`` (Groß-/Kleinschreibung wird nicht berücksichtigt) das jeweilige Feld; jeder andere Wert (``"false"``, leere Zeichenkette oder nicht angegeben) wird als deaktiviert behandelt. Im Response werden die Werte als ``"true"`` / ``"false"`` zurückgegeben.

.. note::

   ``crud_mode`` wird serverseitig automatisch gesetzt und muss im Request nicht angegeben werden. Audit-Felder wie ``created_by`` / ``created_time`` werden ebenfalls serverseitig gesetzt.

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_job_id",
        "created": true
      }
    }

Cron-Ausdrücke Beispiele
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Cron-Ausdruck
     - Beschreibung
   * - ``0 2 * * *``
     - Täglich um 2:00 Uhr ausführen
   * - ``0 */6 * * *``
     - Alle 6 Stunden ausführen
   * - ``0 2 * * 1``
     - Jeden Montag um 2:00 Uhr ausführen (Wochentage: ``0`` für Sonntag bis ``6`` für Samstag)
   * - ``0 2 1 * *``
     - Am 1. jeden Monats um 2:00 Uhr ausführen

Geplanten Job aktualisieren
===========================

Request
-------

::

    PUT /api/admin/scheduler/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_job_id",
      "name": "Updated Crawler",
      "target": "all",
      "cron_expression": "0 3 * * *",
      "script_type": "javascript",
      "script_data": "...",
      "job_logging": "true",
      "crawler": "true",
      "available": "true",
      "sort_order": 1,
      "version_no": 1
    }

.. note::

   Für Aktualisierungen sind ``id`` (max. 1000 Zeichen) und ``version_no`` Pflichtfelder. ``version_no`` wird für optimistisches Sperren verwendet; geben Sie den Wert an, der im GET-Response zurückgegeben wurde. Stimmt der Wert nicht überein, schlägt die Aktualisierung fehl. Die weiteren Pflichtfelder (``name`` / ``target`` / ``script_type`` / ``sort_order``) sind dieselben wie beim Erstellen.

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_job_id",
        "created": false
      }
    }

Geplanten Job löschen
=====================

Request
-------

::

    DELETE /api/admin/scheduler/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_job_id",
        "created": false
      }
    }

Job starten
===========

Führt einen geplanten Job sofort aus.

Request
-------

::

    PUT /api/admin/scheduler/{id}/start

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "job_log_id": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
      }
    }

Response-Felder
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beschreibung
   * - ``job_log_id``
     - Job-Protokoll-ID des gestarteten Jobs. Wird ausgegeben, wenn die Job-Protokollierung aktiviert ist. Ist die Job-Protokollierung deaktiviert, fehlt das Feld in der Antwort.

Hinweise
--------

- Wenn der Job bereits läuft, schlägt der Start fehl und es wird ein Fehler zurückgegeben (``status`` ungleich ``0``).
- Wenn der Job deaktiviert ist (``available`` ist nicht aktiviert), schlägt der Start ebenfalls fehl und es wird ein Fehler zurückgegeben.
- ``job_log_id`` wird nur ausgegeben, wenn die Job-Protokollierung aktiviert ist (``job_logging`` ist aktiviert).

Job stoppen
===========

Stoppt einen laufenden Job.

Request
-------

::

    PUT /api/admin/scheduler/{id}/stop

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

Crawl-Job erstellen und ausführen
---------------------------------

.. code-block:: bash

    # Job erstellen
    curl -X POST "http://localhost:8080/api/admin/scheduler/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Hourly Crawler",
           "target": "all",
           "cron_expression": "0 * * * *",
           "script_type": "javascript",
           "script_data": "return container.getComponent(\"crawlJob\").execute();",
           "job_logging": "true",
           "crawler": "true",
           "available": "true",
           "sort_order": 1
         }'

    # Job sofort ausführen
    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

Job-Status überprüfen
---------------------

.. code-block:: bash

    # Status aller Jobs überprüfen
    curl "http://localhost:8080/api/admin/scheduler/settings" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Das running-Feld zeigt den Ausführungsstatus an

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-joblog` - Job-Protokoll API
- :doc:`../../admin/scheduler-guide` - Scheduler-Verwaltungsanleitung
