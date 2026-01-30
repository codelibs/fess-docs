==========================
LabelType API
==========================

Übersicht
=========

Die LabelType API dient zur Verwaltung von Label-Typen in |Fess|.
Sie können Label-Typen für die Kategorisierung und Filterung von Suchergebnissen verwalten.

Basis-URL
=========

::

    /api/admin/labeltype

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
     - Label-Typ-Liste abrufen
   * - GET
     - /setting/{id}
     - Label-Typ abrufen
   * - POST
     - /setting
     - Label-Typ erstellen
   * - PUT
     - /setting
     - Label-Typ aktualisieren
   * - DELETE
     - /setting/{id}
     - Label-Typ löschen

Label-Typ-Liste abrufen
=======================

Request
-------

::

    GET /api/admin/labeltype/settings
    PUT /api/admin/labeltype/settings

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
     - Seitennummer (beginnt bei 0)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "label_id_1",
            "name": "Documentation",
            "value": "docs",
            "includedPaths": ".*docs\\.example\\.com.*",
            "excludedPaths": "",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

Label-Typ erstellen
===================

Request
-------

::

    POST /api/admin/labeltype/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "News",
      "value": "news",
      "includedPaths": ".*news\\.example\\.com.*\n.*example\\.com/news/.*",
      "excludedPaths": ".*/(archive|old)/.*",
      "sortOrder": 1,
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
   * - ``name``
     - Ja
     - Anzeigename des Labels
   * - ``value``
     - Ja
     - Label-Wert (verwendet bei der Suche)
   * - ``includedPaths``
     - Nein
     - Regex für Label-Zielpfade (mehrere durch Zeilenumbruch getrennt)
   * - ``excludedPaths``
     - Nein
     - Regex für ausgeschlossene Pfade (mehrere durch Zeilenumbruch getrennt)
   * - ``sortOrder``
     - Nein
     - Anzeigereihenfolge
   * - ``permissions``
     - Nein
     - Zugriffsberechtigte Rollen
   * - ``virtualHost``
     - Nein
     - Virtueller Host

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_label_id",
        "created": true
      }
    }

Verwendungsbeispiele
====================

Dokumentations-Label erstellen
------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/labeltype/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Technical Documentation",
           "value": "tech_docs",
           "includedPaths": ".*docs\\.example\\.com.*\n.*example\\.com/documentation/.*",
           "sortOrder": 0,
           "permissions": ["guest"]
         }'

Suche mit Label
---------------

.. code-block:: bash

    # Mit Label filtern
    curl "http://localhost:8080/json/?q=search&label=tech_docs"

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`../api-search` - Such-API
- :doc:`../../admin/labeltype-guide` - Label-Typ Verwaltungsanleitung
