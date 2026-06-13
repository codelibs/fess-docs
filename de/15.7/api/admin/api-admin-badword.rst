==========================
BadWord API
==========================

Übersicht
=========

Die BadWord API dient zur Verwaltung von verbotenen Wörtern (Bad Words) in |Fess|.
Diese Wörter werden aus Suchvorschlägen ausgeschlossen.

Basis-URL
=========

::

    /api/admin/badword

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
     - Bad Word Liste abrufen
   * - GET
     - /setting/{id}
     - Bad Word abrufen
   * - POST
     - /setting
     - Bad Word erstellen
   * - PUT
     - /setting
     - Bad Word aktualisieren
   * - DELETE
     - /setting/{id}
     - Bad Word löschen
   * - PUT
     - /upload
     - Bad Word CSV hochladen
   * - GET
     - /download
     - Bad Word CSV herunterladen

Bad Word Liste abrufen
======================

Request
-------

::

    GET /api/admin/badword/settings

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15.70

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

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "badword_id_1",
            "suggestWord": "inappropriate_word"
          }
        ],
        "total": 5
      }
    }

Bad Word abrufen
================

Request
-------

::

    GET /api/admin/badword/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "badword_id_1",
          "suggestWord": "inappropriate_word"
        }
      }
    }

Bad Word erstellen
==================

Request
-------

::

    POST /api/admin/badword/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "suggestWord": "spam_keyword"
    }

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``suggestWord``
     - Ja
     - Das auszuschließende Schlüsselwort (darf keine Leerzeichen enthalten)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_badword_id",
        "created": true
      }
    }

Bad Word aktualisieren
======================

Request
-------

::

    PUT /api/admin/badword/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_badword_id",
      "suggestWord": "updated_spam_keyword",
      "versionNo": 1
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_badword_id",
        "created": false
      }
    }

Bad Word löschen
================

Request
-------

::

    DELETE /api/admin/badword/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_badword_id",
        "created": false
      }
    }

Bad Word CSV hochladen
======================

Registriert Bad Words gesammelt aus einer CSV-Datei. Die Datei wird als ``multipart/form-data`` gesendet. Der Import wird serverseitig asynchron ausgeführt.

Request
-------

::

    PUT /api/admin/badword/upload
    Content-Type: multipart/form-data

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``badWordFile``
     - Ja
     - Hochzuladende Bad-Word-CSV-Datei

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Bad Word CSV herunterladen
==========================

Lädt die registrierten Bad Words als CSV-Datei (``badword.csv``) herunter. Die Antwort ist ein Stream vom Typ ``application/octet-stream``.

Request
-------

::

    GET /api/admin/badword/download

Verwendungsbeispiele
====================

Spam-Schlüsselwörter ausschließen
---------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/badword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "spam"
         }'

CSV-Datei hochladen
-------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/badword/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "badWordFile=@badword.csv"

CSV-Datei herunterladen
-----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/badword/download" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o badword.csv

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-suggest` - Suggest API
- :doc:`api-admin-elevateword` - ElevateWord API
- :doc:`../../admin/badword-guide` - Bad Word Verwaltungsanleitung
