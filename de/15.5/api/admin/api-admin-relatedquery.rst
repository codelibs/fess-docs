==========================
RelatedQuery API
==========================

Übersicht
=========

Die RelatedQuery API dient zur Verwaltung von verwandten Suchabfragen in |Fess|.
Sie können alternative Suchbegriffe definieren, die bei bestimmten Suchanfragen vorgeschlagen werden.

Basis-URL
=========

::

    /api/admin/relatedquery

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
     - Verwandte Abfragen Liste abrufen
   * - GET
     - /setting/{id}
     - Verwandte Abfrage abrufen
   * - POST
     - /setting
     - Verwandte Abfrage erstellen
   * - PUT
     - /setting
     - Verwandte Abfrage aktualisieren
   * - DELETE
     - /setting/{id}
     - Verwandte Abfrage löschen

Verwandte Abfrage erstellen
===========================

Request
-------

::

    POST /api/admin/relatedquery/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "install",
      "queries": "installation\nsetup\ninstallation guide",
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
   * - ``term``
     - Ja
     - Auslösender Suchbegriff
   * - ``queries``
     - Ja
     - Verwandte Abfragen (durch Zeilenumbruch getrennt)
   * - ``sortOrder``
     - Nein
     - Anzeigereihenfolge

Verwendungsbeispiele
====================

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "download",
           "queries": "downloads\nget started\ninstallation",
           "sortOrder": 0
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-relatedcontent` - Verwandte Inhalte API
- :doc:`../../admin/relatedquery-guide` - Verwandte Abfragen Verwaltungsanleitung
