==========================
Log API
==========================

Übersicht
=========

Die Log API dient zum Anzeigen und Herunterladen von Protokolldateien in |Fess|.
Sie können die auf dem Server ausgegebenen Protokolldateien auflisten und einzelne Protokolldateien herunterladen.

Basis-URL
=========

::

    /api/admin/log

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
     - Protokolldateien auflisten
   * - GET
     - /file/{id}
     - Protokolldatei herunterladen

Protokolldateien auflisten
==========================

Gibt eine Liste der im Protokollausgabeverzeichnis des Servers vorhandenen Protokolldateien (``.log`` und ``.log.gz``) zurück.

Request
-------

::

    GET /api/admin/log/files

Response
--------

In ``files`` wird ein Array von Objekten gespeichert, die die Informationen der einzelnen Protokolldateien darstellen, und in ``total`` die Anzahl.
Jedes Objekt hat die folgenden Felder.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beschreibung
   * - ``id``
     - Base64-URL-codierter Wert des Dateinamens (wird beim Herunterladen als ``{id}`` verwendet)
   * - ``name``
     - Name der Protokolldatei
   * - ``lastModified``
     - Zeitpunkt der letzten Änderung

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "files": [
          {
            "id": "ZmVzcy5sb2c=",
            "name": "fess.log",
            "lastModified": "2025-01-01T00:00:00.000+00:00"
          },
          {
            "id": "ZmVzcy1jcmF3bGVyLmxvZw==",
            "name": "fess-crawler.log",
            "lastModified": "2025-01-01T00:00:00.000+00:00"
          }
        ],
        "total": 2
      }
    }

Protokolldatei herunterladen
============================

Lädt den Inhalt der angegebenen Protokolldatei herunter.
Für ``{id}`` wird die beim Auflisten erhaltene ``id`` (Base64-codierter Wert des Dateinamens) angegeben.
Die Antwort wird als Stream vom Typ ``application/octet-stream`` zurückgegeben.
Wird ein nicht existierender Dateiname oder ein als Protokolldatei nicht zulässiger Name angegeben, wird eine leere Antwort zurückgegeben.

Request
-------

::

    GET /api/admin/log/file/{id}

Response
--------

Binärer Stream der Protokolldatei (``Content-Type: application/octet-stream``).

Verwendungsbeispiele
====================

Protokolldateien auflisten
--------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/files" \
         -H "Authorization: Bearer YOUR_TOKEN"

Protokolldatei herunterladen
----------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/file/ZmVzcy5sb2c=" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess.log

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-backup` - Backup API
