==========================
Backup API
==========================

Übersicht
=========

Die Backup API dient zum Anzeigen und Herunterladen der zu sichernden Daten in |Fess|.
Sie können die Liste der Sicherungsziele abrufen und einzelne Sicherungsdateien (Systemeigenschaften, Bulk-Daten der einzelnen Indizes, NDJSON-Daten der Protokolle) herunterladen.

Diese API ist ausschließlich zum Lesen und Herunterladen vorgesehen. Da die Wiederherstellung durch Hochladen von Sicherungsdateien nicht über die API bereitgestellt wird, führen Sie die Wiederherstellung bei Bedarf über Systeminformationen → Sicherung in der Verwaltungsoberfläche durch.

Basis-URL
=========

::

    /api/admin/backup

Authentifizierung
=================

Wie bei anderen Admin-APIs ist eine Authentifizierung über ein Zugriffstoken erforderlich. Das Zugriffstoken benötigt die Berechtigung ``Radmin-api`` (konfiguriert über ``api.admin.access.permissions``, Standardwert: ``Radmin-api``).
Das Zugriffstoken wird im Anfrage-Header angegeben.

::

    Authorization: Bearer <Zugriffstoken>

Weitere Informationen zur Authentifizierung und zum Abrufen von Zugriffstoken finden Sie unter :doc:`api-admin-overview`.

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

Gibt die Liste der Sicherungsziele zurück. Die Ziele basieren auf den Einstellungen ``index.backup.targets`` und ``index.backup.log.targets``; es wird eine kombinierte Liste beider Einstellungen zurückgegeben.

Request
-------

::

    GET /api/admin/backup/files

Response
--------

In ``files`` wird ein Array von Objekten gespeichert, die die Sicherungsziele darstellen, und in ``total`` die Anzahl.
Jedes Objekt hat ``id`` und ``name``, wobei beide auf den Zielnamen gesetzt werden (z. B. ``fess_config.bulk``, ``system.properties``, ``search_log.ndjson``).

Im Folgenden ein Beispiel bei den Standardeinstellungen (``index.backup.targets`` und ``index.backup.log.targets`` mit Standardwerten).

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "files": [
          { "id": "fess_basic_config.bulk", "name": "fess_basic_config.bulk" },
          { "id": "fess_config.bulk", "name": "fess_config.bulk" },
          { "id": "fess_user.bulk", "name": "fess_user.bulk" },
          { "id": "system.properties", "name": "system.properties" },
          { "id": "fess.json", "name": "fess.json" },
          { "id": "doc.json", "name": "doc.json" },
          { "id": "click_log.ndjson", "name": "click_log.ndjson" },
          { "id": "favorite_log.ndjson", "name": "favorite_log.ndjson" },
          { "id": "search_log.ndjson", "name": "search_log.ndjson" },
          { "id": "user_info.ndjson", "name": "user_info.ndjson" }
        ],
        "total": 10
      }
    }

.. note::

   ``version`` enthält die Produktversion der laufenden |Fess|-Instanz. Der Inhalt von ``files``
   hängt von den Einstellungen ``index.backup.targets`` / ``index.backup.log.targets`` ab;
   das obige Beispiel gilt für die Standardwerte.

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
     - Inhalt der Systemeigenschaften (``application/octet-stream``)
   * - ``*.bulk`` oder Indexname ohne Erweiterung
     - Durch Scrollen des gleichnamigen Index erzeugte Bulk-Daten (``application/octet-stream``). Der Name ohne ``.bulk`` wird als Indexname behandelt.
   * - ``*.ndjson`` (``search_log`` / ``user_info`` / ``click_log`` / ``favorite_log``)
     - NDJSON-Daten des entsprechenden Protokolls (``application/x-ndjson``)

.. note::

   ``fess.json`` und ``doc.json`` sind Mapping-Definitionsdateien (Schema) für Indizes.
   Sie sind in der Zielliste (``/files``) enthalten, werden beim Herunterladen über diese API
   jedoch wie ``.bulk``-Dateien als Scroll-Verarbeitung des Index behandelt. Für Sicherung
   und Wiederherstellung einschließlich Mapping-Definitionen verwenden Sie bitte
   Systeminformationen → Sicherung in der Verwaltungsoberfläche.

Wird eine ``{id}`` angegeben, die nicht unter den Sicherungszielen existiert, wird eine Fehlerantwort zurückgegeben, die in ``status`` einen Wert ungleich 0 und eine Fehlermeldung (``Could not find any backup index.``) enthält.

Request
-------

::

    GET /api/admin/backup/file/{id}

Response
--------

Stream der Sicherungsdatei. Im NDJSON-Format wird ``Content-Type: application/x-ndjson`` zurückgegeben, ansonsten ``application/octet-stream``.

.. note::

   Der Export von Protokollen (``*.ndjson``) unterliegt dem Timeout ``index.backup.log.load.timeout``
   (Standardwert ``60000`` Millisekunden). Wenn die Ausgabe länger dauert, können die Protokolldaten
   vorzeitig abgeschnitten werden.

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
