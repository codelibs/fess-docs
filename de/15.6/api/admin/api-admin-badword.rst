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
   * - GET/PUT
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
      "suggestWord": "inappropriate term"
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
     - Das zu blockierende Wort

Verwendungsbeispiele
====================

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/badword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "blocked term"
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-suggest` - Suggest API
- :doc:`../../admin/badword-guide` - Bad Word Verwaltungsanleitung
