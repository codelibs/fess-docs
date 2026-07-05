==========================
ElevateWord API
==========================

Übersicht
=========

Die ElevateWord API dient zur Verwaltung von Elevate Words (Beeinflussung des Suchrangs für bestimmte Schlüsselwörter) in |Fess|.
Für bestimmte Suchanfragen können Sie bestimmte Dokumente höher oder niedriger platzieren.

Basis-URL
=========

::

    /api/admin/elevateword

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
     - Elevate Word Liste abrufen
   * - GET
     - /setting/{id}
     - Elevate Word abrufen
   * - POST
     - /setting
     - Elevate Word erstellen
   * - PUT
     - /setting
     - Elevate Word aktualisieren
   * - DELETE
     - /setting/{id}
     - Elevate Word löschen
   * - PUT
     - /upload
     - Elevate Word CSV hochladen
   * - GET
     - /download
     - Elevate Word CSV herunterladen

Elevate Word Liste abrufen
==========================

Request
-------

::

    GET /api/admin/elevateword/settings

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
     - Seitennummer (beginnt bei 1, Standard: 1)
   * - ``id``
     - String
     - Nein
     - Exact-Match-Filter nach Elevate-Word-ID

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "elevate_id_1",
            "suggestWord": "fess",
            "reading": "フェス",
            "permissions": "{role}guest",
            "boost": 100.0,
            "labelTypeIds": []
          }
        ],
        "total": 5
      }
    }

Elevate Word abrufen
====================

Request
-------

::

    GET /api/admin/elevateword/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "elevate_id_1",
          "suggestWord": "fess",
          "reading": "フェス",
          "permissions": "{role}guest",
          "boost": 100.0,
          "labelTypeIds": []
        }
      }
    }

Elevate Word erstellen
======================

Request
-------

::

    POST /api/admin/elevateword/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "suggestWord": "documentation",
      "reading": "ドキュメンテーション",
      "permissions": "{role}guest",
      "boost": 100.0,
      "labelTypeIds": ["label1"]
    }

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``suggestWord``
     - Ja
     - Das hervorzuhebende Schlüsselwort
   * - ``reading``
     - Nein
     - Lesehilfe (Kana)
   * - ``permissions``
     - Nein
     - Zugriffsberechtigungen (durch Zeilenumbrüche getrennte Zeichenkette, ein Eintrag pro Zeile. Formular-Standardwert: Standard-Anzeigeberechtigung der Suche)
   * - ``boost``
     - Ja
     - Boost-Wert (Formular-Standardwert: 100.0)
   * - ``labelTypeIds``
     - Nein
     - Ziel-Label-IDs (Array von Zeichenketten)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_elevate_id",
        "created": true
      }
    }

Elevate Word aktualisieren
==========================

Request
-------

::

    PUT /api/admin/elevateword/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_elevate_id",
      "suggestWord": "documentation",
      "reading": "ドキュメンテーション",
      "permissions": "{role}guest\n{role}user",
      "boost": 100.0,
      "labelTypeIds": ["label1"],
      "versionNo": 1
    }

.. note::

   Bei einer Aktualisierung sind zusätzlich zu den Feldern, die bei der Erstellung verwendet werden, folgende Felder erforderlich:

   - ``id`` - ID des zu aktualisierenden Elevate Words
   - ``versionNo`` - Versionsnummer für optimistisches Sperren. Geben Sie den Wert an, der über ``GET /setting/{id}`` abgerufen wurde.

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_elevate_id",
        "created": false
      }
    }

Elevate Word löschen
====================

Request
-------

::

    DELETE /api/admin/elevateword/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_elevate_id",
        "created": false
      }
    }

Elevate Word CSV hochladen
==========================

Registriert Elevate Words gesammelt aus einer CSV-Datei. Die Datei wird als ``multipart/form-data`` gesendet. Der Import wird serverseitig asynchron ausgeführt.

Request
-------

::

    PUT /api/admin/elevateword/upload
    Content-Type: multipart/form-data

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``elevateWordFile``
     - Ja
     - Hochzuladende Elevate-Word-CSV-Datei

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Elevate Word CSV herunterladen
==============================

Lädt die registrierten Elevate Words als CSV-Datei (``elevate.csv``) herunter. Die Antwort ist ein Stream vom Typ ``application/octet-stream``.

Request
-------

::

    GET /api/admin/elevateword/download

Verwendungsbeispiele
====================

Produktnamen hervorheben
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/elevateword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "Product X",
           "boost": 100.0,
           "permissions": "{role}guest"
         }'

Hervorheben für ein bestimmtes Label
------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/elevateword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "API reference",
           "boost": 100.0,
           "labelTypeIds": ["technical_docs"],
           "permissions": "{role}guest"
         }'

CSV-Datei hochladen
-------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/elevateword/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "elevateWordFile=@elevate.csv"

CSV-Datei herunterladen
-----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/elevateword/download" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o elevate.csv

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-keymatch` - KeyMatch API
- :doc:`api-admin-boostdoc` - BoostDoc API
- :doc:`../../admin/elevateword-guide` - Elevate Word Verwaltungsanleitung
