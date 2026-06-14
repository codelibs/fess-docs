==========================
Backup API
==========================

Übersicht
=========

Die Backup API dient zum Anzeigen und Herunterladen der zu sichernden Daten in |Fess|.
Sie können die Liste der Sicherungsziele abrufen und einzelne Sicherungsdateien (Systemeigenschaften, Bulk-Daten der einzelnen Indizes, NDJSON-Daten der Protokolle) herunterladen.

Basis-URL
=========

::

    /api/admin/backup

Endpunktliste
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Pfad
     - Beschreibung
   * - GET
     - /files
     - Sicherungsziele auflisten
   * - GET
     - /file/{id}
     - Sicherungsdatei herunterladen

Sicherungsziele auflisten
=========================

Gibt die Liste der Sicherungsziele zurück. Die Ziele basieren auf den Einstellungen ``index.backup.targets`` und ``index.backup.log.targets``.

Request
-------

::

    GET /api/admin/backup/files

Response
--------

In ``files`` wird ein Array von Objekten gespeichert, die die Sicherungsziele darstellen, und in ``total`` die Anzahl.
Jedes Objekt hat ``id`` und ``name``, wobei beide auf den Zielnamen gesetzt werden (z. B. ``fess_config.bulk``, ``system.properties``, ``search_log.ndjson``).

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "files": [
          {
            "id": "fess_config.bulk",
            "name": "fess_config.bulk"
          },
          {
            "id": "system.properties",
            "name": "system.properties"
          },
          {
            "id": "search_log.ndjson",
            "name": "search_log.ndjson"
          }
        ],
        "total": 3
      }
    }

Sicherungsdatei herunterladen
=============================

Lädt den Inhalt der angegebenen Sicherungsdatei herunter. Für ``{id}`` wird die beim Auflisten erhaltene ``id`` (der Zielname) angegeben.
Je nach Art von ``{id}`` wechselt der Antwortinhalt wie folgt.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - ID
     - Inhalt
   * - ``system.properties``
     - Inhalt der Systemeigenschaften
   * - ``*.bulk`` oder Indexname ohne die Endung ``.bulk``
     - Durch Scrollen des Zielindex erzeugte Bulk-Daten
   * - ``*.ndjson`` (``search_log`` / ``user_info`` / ``click_log`` / ``favorite_log``)
     - NDJSON-Daten des entsprechenden Protokolls

Wird eine ``{id}`` angegeben, die nicht unter den Sicherungszielen existiert, tritt ein Fehler auf.

Request
-------

::

    GET /api/admin/backup/file/{id}

Response
--------

Stream der Sicherungsdatei. Im NDJSON-Format wird ``Content-Type: application/x-ndjson`` zurückgegeben, ansonsten ``application/octet-stream``.

Verwendungsbeispiele
====================

Sicherungsziele auflisten
-------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/files" \
         -H "Authorization: Bearer YOUR_TOKEN"

Konfigurationsindex herunterladen
---------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/file/fess_config.bulk" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess_config.bulk

Suchprotokoll herunterladen
---------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/file/search_log.ndjson" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o search_log.ndjson

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-log` - Log API
