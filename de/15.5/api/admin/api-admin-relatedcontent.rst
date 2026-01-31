==========================
RelatedContent API
==========================

Übersicht
=========

Die RelatedContent API dient zur Verwaltung von verwandten Inhalten in |Fess|.
Sie können Inhalte definieren, die bei bestimmten Suchbegriffen angezeigt werden.

Basis-URL
=========

::

    /api/admin/relatedcontent

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
     - Verwandte Inhalte Liste abrufen
   * - GET
     - /setting/{id}
     - Verwandten Inhalt abrufen
   * - POST
     - /setting
     - Verwandten Inhalt erstellen
   * - PUT
     - /setting
     - Verwandten Inhalt aktualisieren
   * - DELETE
     - /setting/{id}
     - Verwandten Inhalt löschen

Verwandten Inhalt erstellen
===========================

Request
-------

::

    POST /api/admin/relatedcontent/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "product",
      "content": "<a href=\"/products\">View all products</a>",
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
   * - ``content``
     - Ja
     - Anzuzeigender HTML-Inhalt
   * - ``sortOrder``
     - Nein
     - Anzeigereihenfolge

Verwendungsbeispiele
====================

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedcontent/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "support",
           "content": "<div class=\"related-box\">Need help? <a href=\"/support\">Contact Support</a></div>",
           "sortOrder": 0
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-relatedquery` - Verwandte Abfragen API
- :doc:`../../admin/relatedcontent-guide` - Verwandte Inhalte Verwaltungsanleitung
