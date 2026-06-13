==========================
Storage API
==========================

Übersicht
=========

Die Storage API dient zur Verwaltung des Objektspeichers in |Fess|.
Sie können Dateien und Verzeichnisse im Speicher auflisten sowie Dateien herunterladen, löschen und hochladen.

Basis-URL
=========

::

    /api/admin/storage

Endpunktliste
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Pfad
     - Beschreibung
   * - GET
     - /list/{id}
     - Dateien und Verzeichnisse auflisten
   * - GET
     - /download/{id}
     - Datei herunterladen
   * - DELETE
     - /delete/{id}
     - Datei löschen
   * - PUT
     - /upload/{pathId}
     - Datei hochladen

Dateien und Verzeichnisse auflisten
===================================

Gibt die Liste der Dateien und Verzeichnisse unterhalb des angegebenen Verzeichnisses zurück.
Für ``{id}`` wird ein codierter Pfad angegeben. Wird ``{id}`` weggelassen, wird die Liste des Wurzelverzeichnisses abgerufen.

Request
-------

::

    GET /api/admin/storage/list/{id}

Response
--------

In ``items`` wird ein Array von Objekten gespeichert, die die Informationen der Dateien und Verzeichnisse darstellen (Verzeichnisse zuerst, Dateien danach).
Jedes Objekt hat die folgenden Felder.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beschreibung
   * - ``id``
     - Codierter Bezeichner (wird beim Herunterladen und Löschen als ``{id}`` verwendet)
   * - ``path``
     - Übergeordneter Pfad
   * - ``name``
     - Datei- oder Verzeichnisname
   * - ``hashCode``
     - Hash-Code
   * - ``size``
     - Größe (Byte)
   * - ``directory``
     - Ob es ein Verzeichnis ist (boolean)
   * - ``lastModified``
     - Zeitpunkt der letzten Änderung (nur Dateien)

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "items": [
          {
            "id": "c3ViZGly",
            "path": "/",
            "name": "subdir",
            "hashCode": 12345,
            "size": 0,
            "directory": true
          },
          {
            "id": "c2FtcGxlLnR4dA==",
            "path": "/",
            "name": "sample.txt",
            "hashCode": 67890,
            "size": 1024,
            "directory": false,
            "lastModified": "2025-01-01T00:00:00.000+00:00"
          }
        ]
      }
    }

Datei herunterladen
===================

Lädt eine Datei aus dem Speicher herunter. Für ``{id}`` wird die beim Auflisten erhaltene ``id`` angegeben.
Die Antwort wird als Stream vom Typ ``application/octet-stream`` zurückgegeben.

Request
-------

::

    GET /api/admin/storage/download/{id}

Response
--------

Binärer Stream der Datei (``Content-Type: application/octet-stream``).

Datei löschen
=============

Löscht eine Datei aus dem Speicher. Für ``{id}`` wird die beim Auflisten erhaltene ``id`` angegeben.

Request
-------

::

    DELETE /api/admin/storage/delete/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Datei hochladen
===============

Lädt eine Datei in den Speicher hoch. Die Übertragung erfolgt im Format ``multipart/form-data``.

Request
-------

::

    PUT /api/admin/storage/upload/{pathId}
    Content-Type: multipart/form-data

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``path``
     - Nein
     - Zielpfad des Uploads (bei fehlender Angabe der Standardort)
   * - ``file``
     - Ja
     - Hochzuladende Datei

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Verwendungsbeispiele
====================

Wurzelverzeichnis auflisten
---------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/list/" \
         -H "Authorization: Bearer YOUR_TOKEN"

Datei herunterladen
-------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/download/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o sample.txt

Datei löschen
-------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/storage/delete/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN"

Datei hochladen
---------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/storage/upload/" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "path=/" \
         -F "file=@sample.txt"

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
