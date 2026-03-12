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
   * - GET/PUT
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
    PUT /api/admin/keymatch/settings

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
            "maxSize": 10,
            "boost": 10.0
          }
        ],
        "total": 5
      }
    }

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
      "maxSize": 5,
      "boost": 20.0
    }

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``term``
     - Ja
     - Suchbegriff
   * - ``query``
     - Ja
     - Match-Abfrage
   * - ``maxSize``
     - Nein
     - Maximale Anzahl (Standard: 10)
   * - ``boost``
     - Nein
     - Boost-Wert (Standard: 1.0)

Verwendungsbeispiele
====================

Produktseiten-KeyMatch erstellen
--------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/keymatch/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product features",
           "query": "url:*/products/* AND (title:features OR content:features)",
           "maxSize": 10,
           "boost": 15.0
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-elevateword` - Elevate Word API
- :doc:`../../admin/keymatch-guide` - KeyMatch Verwaltungsanleitung
