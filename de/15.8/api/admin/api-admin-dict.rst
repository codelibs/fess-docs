==========================
Dict API
==========================

Übersicht
=========

Die Dict API dient zur Verwaltung von Wörterbüchern in |Fess|.
Über den Stamm-Endpunkt können Sie die Liste der verfügbaren Wörterbücher abrufen.
Das Anzeigen, Erstellen, Aktualisieren und Löschen einzelner Wörterbucheinträge sowie das Hochladen und Herunterladen von Wörterbuchdateien
erfolgen über die Sub-Endpunkte je Wörterbuchtyp (synonym, kuromoji, mapping, protwords, stopwords, stemmeroverride).

Basis-URL
=========

::

    /api/admin/dict

Endpunktliste
=============

Wörterbuch-Stamm
----------------

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Pfad
     - Beschreibung
   * - GET
     - /
     - Wörterbücher auflisten

Endpunkte je Wörterbuchtyp
--------------------------

Für ``{type}`` wird einer der Werte ``synonym``, ``kuromoji``, ``mapping``, ``protwords``, ``stopwords``, ``stemmeroverride`` angegeben.
Diese Werte entsprechen dem Wert des Felds ``type``, das in der Antwort der Wörterbuchliste enthalten ist.
``{dictId}`` ist die ID des Wörterbuchs, die beim Auflisten der Wörterbücher zurückgegeben wird.

.. list-table::
   :header-rows: 1
   :widths: 15 50 35

   * - Methode
     - Pfad
     - Beschreibung
   * - GET
     - /{type}/settings/{dictId}
     - Wörterbucheinträge auflisten
   * - GET
     - /{type}/setting/{dictId}/{id}
     - Wörterbucheintrag abrufen
   * - POST
     - /{type}/setting/{dictId}
     - Wörterbucheintrag erstellen
   * - PUT
     - /{type}/setting/{dictId}
     - Wörterbucheintrag aktualisieren
   * - DELETE
     - /{type}/setting/{dictId}/{id}
     - Wörterbucheintrag löschen
   * - PUT
     - /{type}/upload/{dictId}
     - Wörterbuchdatei hochladen
   * - GET
     - /{type}/download/{dictId}
     - Wörterbuchdatei herunterladen

Wörterbücher auflisten
======================

Ruft die Liste der verfügbaren Wörterbuchdateien ab.

Request
-------

::

    GET /api/admin/dict

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [
          {
            "id": "ZjA5...synonym.txt",
            "type": "synonym",
            "path": "/var/lib/fess/dict/synonym.txt",
            "timestamp": "2025-01-29T10:00:00.000+0000"
          },
          {
            "id": "ZjA5...mapping.txt",
            "type": "mapping",
            "path": "/var/lib/fess/dict/mapping.txt",
            "timestamp": "2025-01-28T15:30:00.000+0000"
          }
        ],
        "total": 2
      }
    }

Response-Felder
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beschreibung
   * - ``settings[].id``
     - Wörterbuch-ID (wird bei einzelnen Wörterbuchoperationen als ``{dictId}`` verwendet)
   * - ``settings[].type``
     - Wörterbuchtyp
   * - ``settings[].path``
     - Pfad der Wörterbuchdatei
   * - ``settings[].timestamp``
     - Zeitpunkt der Änderung der Wörterbuchdatei
   * - ``total``
     - Gesamtanzahl der Wörterbuchdateien

Wörterbucheinträge auflisten
============================

Listet die Einträge im angegebenen Wörterbuch auf.

Request
-------

::

    GET /api/admin/dict/{type}/settings/{dictId}

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``dictId``
     - String
     - Ja
     - Wörterbuch-ID (Pfadparameter)
   * - ``size``
     - Integer
     - Nein
     - Anzahl der Einträge pro Seite (Standard: 25)
   * - ``page``
     - Integer
     - Nein
     - Seitennummer (beginnt bei 1, Standard: 1)

Response
--------

Die Felder der einzelnen Einträge im Array ``settings`` der Antwort unterscheiden sich je nach Wörterbuchtyp (siehe weiter unten „Eintragsfelder je Wörterbuchtyp“).

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [
          {
            "id": 1,
            "dictId": "ZjA5...synonym.txt",
            "inputs": "検索,サーチ",
            "outputs": "検索,サーチ,リサーチ"
          }
        ],
        "total": 1
      }
    }

Das obige Beispiel zeigt das ``synonym``-Wörterbuch.

Wörterbucheintrag abrufen
=========================

Ruft einen bestimmten Eintrag im Wörterbuch ab.

Request
-------

::

    GET /api/admin/dict/{type}/setting/{dictId}/{id}

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``dictId``
     - String
     - Ja
     - Wörterbuch-ID (Pfadparameter)
   * - ``id``
     - Long
     - Ja
     - Eintrags-ID (Pfadparameter)

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "setting": {
          "id": 1,
          "dictId": "ZjA5...synonym.txt",
          "inputs": "検索,サーチ",
          "outputs": "検索,サーチ,リサーチ"
        }
      }
    }

Wörterbucheintrag erstellen
===========================

Erstellt einen neuen Eintrag im Wörterbuch.

Request
-------

::

    POST /api/admin/dict/{type}/setting/{dictId}
    Content-Type: application/json

Request-Body (Synonym-Beispiel)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "inputs": "検索,サーチ",
      "outputs": "検索,サーチ,リサーチ"
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "1",
        "created": true
      }
    }

Wörterbucheintrag aktualisieren
===============================

Aktualisiert einen bestehenden Eintrag im Wörterbuch.

Request
-------

::

    PUT /api/admin/dict/{type}/setting/{dictId}
    Content-Type: application/json

Request-Body (Synonym-Beispiel)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": 1,
      "inputs": "検索,サーチ",
      "outputs": "検索,サーチ,リサーチ,search"
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "1",
        "created": false
      }
    }

Wörterbucheintrag löschen
=========================

Löscht einen Eintrag im Wörterbuch.

Request
-------

::

    DELETE /api/admin/dict/{type}/setting/{dictId}/{id}

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``dictId``
     - String
     - Ja
     - Wörterbuch-ID (Pfadparameter)
   * - ``id``
     - Long
     - Ja
     - Eintrags-ID (Pfadparameter)

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "1",
        "created": false
      }
    }

Wörterbuchdatei hochladen
=========================

Lädt die gesamte Wörterbuchdatei hoch und ersetzt sie.

Request
-------

::

    PUT /api/admin/dict/{type}/upload/{dictId}
    Content-Type: multipart/form-data

Der Name des Dateifelds unterscheidet sich je Wörterbuchtyp (siehe weiter unten „Eintragsfelder je Wörterbuchtyp“).

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

Wörterbuchdatei herunterladen
=============================

Lädt die Wörterbuchdatei herunter.

Request
-------

::

    GET /api/admin/dict/{type}/download/{dictId}

Die Antwort ist die Binärdatei des Wörterbuchs (``application/octet-stream``).

Eintragsfelder je Wörterbuchtyp
===============================

Die Felder im Request-Body zum Erstellen/Aktualisieren von Wörterbucheinträgen sowie in der Antwort unterscheiden sich je Wörterbuchtyp.
``id`` (Eintrags-ID) und ``dictId`` (Wörterbuch-ID) sind in der Antwort gemeinsam enthalten.

.. list-table::
   :header-rows: 1
   :widths: 18 42 40

   * - Typ
     - Eintragsfelder
     - Upload-Dateifeld
   * - ``synonym``
     - ``inputs`` (erforderlich), ``outputs`` (erforderlich)
     - ``synonymFile``
   * - ``kuromoji``
     - ``token`` (erforderlich), ``segmentation`` (erforderlich), ``reading`` (erforderlich), ``pos`` (erforderlich)
     - ``kuromojiFile``
   * - ``mapping``
     - ``inputs`` (erforderlich), ``output``
     - ``charMappingFile``
   * - ``protwords``
     - ``input`` (erforderlich)
     - ``protwordsFile``
   * - ``stopwords``
     - ``input`` (erforderlich)
     - ``stopwordsFile``
   * - ``stemmeroverride``
     - ``input`` (erforderlich), ``output`` (erforderlich)
     - ``stemmerOverrideFile``

Verwendungsbeispiele
====================

Wörterbücher auflisten
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict" \
         -H "Authorization: Bearer YOUR_TOKEN"

Einträge des Synonymwörterbuchs auflisten
-----------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict/synonym/settings/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN"

Eintrag zum Synonymwörterbuch hinzufügen
----------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dict/synonym/setting/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "inputs": "検索,サーチ",
           "outputs": "検索,サーチ,リサーチ"
         }'

Synonymwörterbuchdatei hochladen
--------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/dict/synonym/upload/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "synonymFile=@synonym.txt"

Synonymwörterbuchdatei herunterladen
------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict/synonym/download/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o synonym.txt

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`../../admin/dict-guide` - Wörterbuch Verwaltungsanleitung
- :doc:`../../admin/synonym-guide` - Synonym Verwaltungsanleitung
