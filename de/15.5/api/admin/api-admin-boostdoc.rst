==========================
BoostDoc API
==========================

Übersicht
=========

Die BoostDoc API dient zur Verwaltung von Dokument-Boost-Einstellungen in |Fess|.
Sie können den Boost-Wert für bestimmte Dokumente in den Suchergebnissen anpassen.

Basis-URL
=========

::

    /api/admin/boostdoc

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
     - Boost-Dokument-Liste abrufen
   * - GET
     - /setting/{id}
     - Boost-Dokument abrufen
   * - POST
     - /setting
     - Boost-Dokument erstellen
   * - PUT
     - /setting
     - Boost-Dokument aktualisieren
   * - DELETE
     - /setting/{id}
     - Boost-Dokument löschen

Boost-Dokument erstellen
========================

Request
-------

::

    POST /api/admin/boostdoc/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "urlExpr": "https://example.com/important-page",
      "boostExpr": "2.0",
      "sortOrder": 0
    }

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``urlExpr``
     - Ja
     - URL-Ausdruck (kann Regex sein)
   * - ``boostExpr``
     - Ja
     - Boost-Ausdruck
   * - ``sortOrder``
     - Nein
     - Anzeigereihenfolge

Verwendungsbeispiele
====================

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": "https://example.com/priority/.*",
           "boostExpr": "3.0",
           "sortOrder": 0
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`../../admin/boostdoc-guide` - Dokument-Boost Verwaltungsanleitung
