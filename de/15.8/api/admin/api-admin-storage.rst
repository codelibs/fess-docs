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

Authentifizierung
=================

Alle Endpunkte der Admin API einschließlich der Storage API erfordern eine Authentifizierung mit einem Access Token.
Geben Sie den Access Token im ``Authorization``-Header des Requests an.

::

    Authorization: Bearer <Access Token>

Einzelheiten zur Beschaffung des Access Tokens und zu den erforderlichen Berechtigungen (standardmäßig die Rolle ``admin-api``) finden Sie unter
:doc:`api-admin-overview`.

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
     - /upload
     - Datei hochladen

Dateien und Verzeichnisse auflisten
====================================

Gibt die Liste der Dateien und Verzeichnisse unterhalb des angegebenen Verzeichnisses zurück.
Für ``{id}`` wird die beim Auflisten erhaltene ``id`` eines Verzeichnisses angegeben. Wird ``{id}`` weggelassen, wird die Liste des Wurzelverzeichnisses abgerufen.

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
     - Codierter Bezeichner. Eine URL-sichere Base64-Kodierung des Objektpfads, die beim Herunterladen und Löschen als ``{id}`` verwendet wird.
   * - ``path``
     - Pfad des übergeordneten Verzeichnisses
   * - ``name``
     - Datei- oder Verzeichnisname
   * - ``hashCode``
     - Intern verwendeter Hash-Wert (kein stabiler Wert, der den Inhalt des Objekts repräsentiert)
   * - ``size``
     - Größe (Byte)
   * - ``directory``
     - Ob es ein Verzeichnis ist (boolean)
   * - ``lastModified``
     - Zeitpunkt der letzten Änderung (ISO-8601-Format; nur bei Dateien enthalten)

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
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

.. note::

   Die Antwort dieser API enthält keinen ``Content-Disposition``-Header.
   Der zu speichernde Dateiname muss clientseitig angegeben werden (bei cURL über die Option ``-o``).

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
        "version": "15.8.0",
        "status": 0
      }
    }

Datei hochladen
===============

Lädt eine Datei in den Speicher hoch. Die Übertragung erfolgt im Format ``multipart/form-data``.
Das Zielverzeichnis wird nicht im URL-Pfad, sondern über das Formularfeld ``path`` angegeben.

Request
-------

::

    PUT /api/admin/storage/upload
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
     - Verzeichnispfad des Upload-Ziels (ohne führende und abschließende Schrägstriche). Wird kein Pfad angegeben, wird die Datei im Wurzelverzeichnis (direkt im Bucket) gespeichert.
   * - ``file``
     - Ja
     - Hochzuladende Datei

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

Fehler
======

Schlägt die Verarbeitung an einem Endpunkt fehl, wird eine Antwort mit einem ``status``-Wert ungleich 0 zurückgegeben (bei Validierungsfehlern ``1``).
Das Feld ``message`` im Antwortkörper enthält die Fehlerbeschreibung. Einzelheiten zu Statuswerten und HTTP-Statuscodes finden Sie unter :doc:`api-admin-overview`.

Die häufigsten Fehlerfälle sind wie folgt.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpunkt
     - Häufige Fehlerursachen
   * - Dateien und Verzeichnisse auflisten
     - Wenn die Anzahl der abgerufenen Einträge das Limit überschreitet
   * - Datei herunterladen
     - Wenn ``id`` ungültig ist oder der Download fehlschlägt
   * - Datei löschen
     - Wenn ``id`` ungültig ist oder das Löschen fehlschlägt
   * - Datei hochladen
     - Wenn ``file`` nicht angegeben ist oder der Upload fehlschlägt

Verwendungsbeispiele
====================

Wurzelverzeichnis auflisten
----------------------------

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

    curl -X PUT "http://localhost:8080/api/admin/storage/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "path=subdir" \
         -F "file=@sample.txt"

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
