==========================
KeyMatch API
==========================

Übersicht
=========

Die KeyMatch API dient zur Verwaltung von KeyMatch (Verknüpfung von Suchbegriffen mit Ergebnissen) in |Fess|.
Sie können bestimmte Dokumente für bestimmte Suchbegriffe bevorzugt anzeigen lassen.

Basis-URL
=========

::

    /api/admin/keymatch

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
     - KeyMatch-Liste abrufen
   * - GET
     - /setting/{id}
     - KeyMatch abrufen
   * - POST
     - /setting
     - KeyMatch erstellen
   * - PUT
     - /setting
     - KeyMatch aktualisieren
   * - DELETE
     - /setting/{id}
     - KeyMatch löschen

KeyMatch-Liste abrufen
======================

Request
-------

::

    GET /api/admin/keymatch/settings

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
     - Anzahl der Einträge pro Seite (Standard: 25; Konfigurationswert ``paging.page.size``)
   * - ``page``
     - Integer
     - Nein
     - Seitennummer (beginnt bei 1, Standard: 1)
   * - ``term``
     - String
     - Nein
     - Filterung nach Suchbegriff (Platzhalter-Übereinstimmung)
   * - ``query``
     - String
     - Nein
     - Filterung nach Match-Abfrage (Platzhalter-Übereinstimmung)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "keymatch_id_1",
            "term": "download",
            "query": "title:download OR content:download",
            "max_size": 10,
            "boost": 10.0,
            "version_no": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   In ``total`` wird die Gesamtanzahl der Einträge angegeben, die den Filterbedingungen entsprechen (nicht die Anzahl der Einträge auf der aktuellen Seite).
   Jedes Einstellungsobjekt kann zusätzlich zu den oben genannten Feldern ``virtual_host``,
   ``created_by``, ``created_time``, ``updated_by`` und ``updated_time`` enthalten, sofern diese Werte gesetzt sind.

KeyMatch abrufen
================

Request
-------

::

    GET /api/admin/keymatch/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "keymatch_id_1",
          "term": "download",
          "query": "title:download OR content:download",
          "max_size": 10,
          "boost": 10.0,
          "created_by": "admin",
          "created_time": 1700000000000,
          "updated_by": "admin",
          "updated_time": 1700000000000,
          "version_no": 1
        }
      }
    }

.. note::

   ``version_no`` ist die Versionsnummer für optimistisches Sperren. Beim Aktualisieren eines KeyMatch-Eintrags muss der beim Abrufen erhaltene
   ``version_no``-Wert im Request-Body angegeben werden. Falls die angegebene ID nicht existiert, wird ein Fehler zurückgegeben.

KeyMatch erstellen
==================

Request
-------

::

    POST /api/admin/keymatch/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "pricing",
      "query": "url:*/pricing* OR title:pricing",
      "max_size": 5,
      "boost": 20.0
    }

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Feld
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``term``
     - String
     - Ja
     - Suchbegriff (maximal 100 Zeichen)
   * - ``query``
     - String
     - Ja
     - Match-Abfrage (maximale Länge gemäß Konfigurationswert ``form.admin.max.input.size``)
   * - ``max_size``
     - Integer
     - Ja
     - Maximale Anzahl anzuzeigender Einträge (ganzzahlig, mindestens 0; Standardwert im Verwaltungsformular: 10)
   * - ``boost``
     - Float
     - Ja
     - Boost-Wert (Standardwert im Verwaltungsformular: 100.0)
   * - ``virtual_host``
     - String
     - Nein
     - Name des virtuellen Hosts (maximal 1000 Zeichen; anzugeben, wenn KeyMatch-Einträge pro virtuellem Host unterschieden werden sollen)

.. note::

   ``max_size`` und ``boost`` sind bei der Verwendung über die API Pflichtfelder. Die Standardwerte werden im Verwaltungsformular angezeigt und gelten
   nicht automatisch für die API. Werden diese Felder ausgelassen, wird ein Validierungsfehler zurückgegeben.
   Hinweis: ``created_by`` und ``created_time`` werden auch dann vom Server überschrieben, wenn sie im Request angegeben werden.

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_keymatch_id",
        "created": true
      }
    }

KeyMatch aktualisieren
======================

Request
-------

::

    PUT /api/admin/keymatch/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_keymatch_id",
      "term": "pricing",
      "query": "url:*/pricing* OR title:pricing OR content:price",
      "max_size": 10,
      "boost": 15.0,
      "version_no": 1
    }

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

Zusätzlich zu den Feldern beim Erstellen (``term``, ``query``, ``max_size``, ``boost``, ``virtual_host``) sind folgende Felder anzugeben.

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Feld
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``id``
     - String
     - Ja
     - ID des zu aktualisierenden KeyMatch-Eintrags (maximal 1000 Zeichen)
   * - ``version_no``
     - Integer
     - Ja
     - Versionsnummer für optimistisches Sperren; anzugeben ist der beim Abrufen erhaltene Wert

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_keymatch_id",
        "created": false
      }
    }

KeyMatch löschen
================

Request
-------

::

    DELETE /api/admin/keymatch/setting/{id}

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

Produktseiten-KeyMatch erstellen
---------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/keymatch/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product features",
           "query": "url:*/products/* AND (title:features OR content:features)",
           "max_size": 10,
           "boost": 15.0
         }'

KeyMatch für Support-Seiten
----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/keymatch/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "help",
           "query": "url:*/support/* OR url:*/help/* OR url:*/faq/*",
           "max_size": 5,
           "boost": 20.0
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-elevateword` - Elevate Word API
- :doc:`../../admin/keymatch-guide` - KeyMatch Verwaltungsanleitung
