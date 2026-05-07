==========================
Suggest API
==========================

Übersicht
=========

Die Suggest API dient zur Verwaltung der Suggest-Funktion (Suchvorschläge) in |Fess|.
Sie können die Suggest-Datenbank verwalten und aktualisieren.

Basis-URL
=========

::

    /api/admin/suggest

Endpunktliste
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Pfad
     - Beschreibung
   * - GET
     - /status
     - Suggest-Status abrufen
   * - PUT
     - /reindex
     - Suggest-Index neu erstellen

Suggest-Status abrufen
======================

Request
-------

::

    GET /api/admin/suggest/status

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "documentCount": 12345,
        "wordCount": 5678,
        "lastUpdated": "2025-01-29T10:00:00Z"
      }
    }

Suggest-Index neu erstellen
===========================

Request
-------

::

    PUT /api/admin/suggest/reindex

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Suggest reindex started"
      }
    }

Verwendungsbeispiele
====================

Suggest-Status prüfen
---------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/suggest/status" \
         -H "Authorization: Bearer YOUR_TOKEN"

Suggest-Index neu erstellen
---------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/suggest/reindex" \
         -H "Authorization: Bearer YOUR_TOKEN"

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-badword` - Bad Word API
- :doc:`api-admin-elevateword` - Elevate Word API
- :doc:`../../admin/suggest-guide` - Suggest Verwaltungsanleitung
