==========================
ElevateWord API
==========================

Übersicht
=========

Die ElevateWord API dient zur Verwaltung von Elevate Words (bevorzugten Begriffen) in |Fess|.
Sie können bestimmte Wörter priorisieren, um entsprechende Dokumente in den Suchergebnissen höher zu ranken.

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
   * - GET/PUT
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
      "suggestWord": "important product",
      "reading": "",
      "boost": 10.0,
      "permissions": ["guest"]
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
     - Das bevorzugte Wort
   * - ``reading``
     - Nein
     - Lesehilfe (für japanische Begriffe)
   * - ``boost``
     - Nein
     - Boost-Wert (Standard: 1.0)
   * - ``permissions``
     - Nein
     - Zugriffsberechtigte Rollen

Verwendungsbeispiele
====================

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/elevateword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "new feature",
           "boost": 15.0,
           "permissions": ["guest"]
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-keymatch` - KeyMatch API
- :doc:`../../admin/elevateword-guide` - Elevate Word Verwaltungsanleitung
