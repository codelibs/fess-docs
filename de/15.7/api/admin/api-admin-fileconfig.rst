==========================
FileConfig API
==========================

Übersicht
=========

Die FileConfig API dient zur Verwaltung der Datei-Crawl-Konfiguration in |Fess|.
Sie können Crawl-Einstellungen für Dateisysteme und SMB/CIFS-Freigabeordner verwalten.

Basis-URL
=========

::

    /api/admin/fileconfig

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
     - Datei-Crawl-Konfigurationsliste abrufen
   * - GET
     - /setting/{id}
     - Datei-Crawl-Konfiguration abrufen
   * - POST
     - /setting
     - Datei-Crawl-Konfiguration erstellen
   * - PUT
     - /setting
     - Datei-Crawl-Konfiguration aktualisieren
   * - DELETE
     - /setting/{id}
     - Datei-Crawl-Konfiguration löschen

Datei-Crawl-Konfigurationsliste abrufen
=======================================

Request
-------

::

    GET /api/admin/fileconfig/settings

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15.70

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
            "id": "fileconfig_id_1",
            "name": "Shared Documents",
            "description": "Gemeinsame Dokumente",
            "paths": "file://///server/share/documents",
            "includedPaths": ".*\\.pdf$",
            "excludedPaths": ".*/(temp|cache)/.*",
            "includedDocPaths": "",
            "excludedDocPaths": "",
            "configParameter": "",
            "depth": 10,
            "maxAccessCount": 1000,
            "numOfThread": 1,
            "intervalTime": 1000,
            "boost": 1.0,
            "available": "true",
            "permissions": "{role}admin",
            "virtualHosts": "",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

Datei-Crawl-Konfiguration abrufen
=================================

Request
-------

::

    GET /api/admin/fileconfig/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "fileconfig_id_1",
          "name": "Shared Documents",
          "description": "Gemeinsame Dokumente",
          "paths": "file://///server/share/documents",
          "includedPaths": ".*\\.pdf$",
          "excludedPaths": ".*/(temp|cache)/.*",
          "includedDocPaths": "",
          "excludedDocPaths": "",
          "configParameter": "",
          "depth": 10,
          "maxAccessCount": 1000,
          "numOfThread": 1,
          "intervalTime": 1000,
          "boost": 1.0,
          "available": "true",
          "sortOrder": 0,
          "permissions": "{role}admin",
          "virtualHosts": "",
          "labelTypeIds": []
        }
      }
    }

Datei-Crawl-Konfiguration erstellen
===================================

Request
-------

::

    POST /api/admin/fileconfig/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Local Files",
      "paths": "file:///data/documents",
      "includedPaths": ".*\\.(pdf|doc|docx|xls|xlsx)$",
      "excludedPaths": ".*/(temp|backup)/.*",
      "numOfThread": 2,
      "intervalTime": 500,
      "boost": 1.0,
      "available": "true",
      "sortOrder": 0,
      "permissions": "{role}admin\n{role}user",
      "labelTypeIds": ["label_id_1"]
    }

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``name``
     - Ja
     - Konfigurationsname
   * - ``description``
     - Nein
     - Beschreibung der Konfiguration
   * - ``paths``
     - Ja
     - Crawl-Startpfade (bei mehreren durch Zeilenumbruch getrennt)
   * - ``includedPaths``
     - Nein
     - Regex-Muster für zu crawlende Pfade
   * - ``excludedPaths``
     - Nein
     - Regex-Muster für auszuschließende Pfade
   * - ``includedDocPaths``
     - Nein
     - Regex-Muster für zu indexierende Pfade
   * - ``excludedDocPaths``
     - Nein
     - Regex-Muster für vom Index auszuschließende Pfade
   * - ``configParameter``
     - Nein
     - Zusätzliche Konfigurationsparameter
   * - ``depth``
     - Nein
     - Crawl-Tiefe
   * - ``maxAccessCount``
     - Nein
     - Maximale Zugriffsanzahl
   * - ``numOfThread``
     - Ja
     - Anzahl paralleler Threads
   * - ``intervalTime``
     - Ja
     - Zugriffsintervall (Millisekunden)
   * - ``boost``
     - Ja
     - Boost-Wert für Suchergebnisse
   * - ``available``
     - Ja
     - Aktiviert/Deaktiviert (Zeichenkette ``"true"`` / ``"false"``)
   * - ``sortOrder``
     - Ja
     - Anzeigereihenfolge
   * - ``permissions``
     - Nein
     - Zugriffsberechtigte Rollen (bei mehreren durch Zeilenumbrüche getrennt)
   * - ``virtualHosts``
     - Nein
     - Virtuelle Hosts (bei mehreren durch Zeilenumbrüche getrennt)
   * - ``labelTypeIds``
     - Nein
     - Label-Typ-IDs (Array)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_fileconfig_id",
        "created": true
      }
    }

Datei-Crawl-Konfiguration aktualisieren
=======================================

Request
-------

::

    PUT /api/admin/fileconfig/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_fileconfig_id",
      "name": "Updated Local Files",
      "paths": "file:///data/documents",
      "includedPaths": ".*\\.(pdf|doc|docx|xls|xlsx|ppt|pptx)$",
      "excludedPaths": ".*/(temp|backup|archive)/.*",
      "depth": 10,
      "maxAccessCount": 10000,
      "numOfThread": 3,
      "intervalTime": 300,
      "boost": 1.2,
      "available": "true",
      "sortOrder": 0,
      "versionNo": 1
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_fileconfig_id",
        "created": false
      }
    }

Datei-Crawl-Konfiguration löschen
=================================

Request
-------

::

    DELETE /api/admin/fileconfig/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Pfadformate
===========

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Protokoll
     - Pfadformat
   * - Lokale Datei
     - ``file:///path/to/directory``
   * - Windows-Freigabe (SMB)
     - ``file://///server/share/path``
   * - SMB mit Authentifizierung
     - ``smb://username:password@server/share/path``
   * - NFS
     - ``file://///nfs-server/export/path``

Verwendungsbeispiele
====================

SMB-Freigabe-Crawl-Konfiguration
--------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/fileconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "SMB Share",
           "paths": "smb://user:pass@server/documents",
           "includedPaths": ".*\\.(pdf|doc|docx)$",
           "excludedPaths": ".*/(temp|private)/.*",
           "maxAccessCount": 50000,
           "numOfThread": 3,
           "intervalTime": 200,
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-webconfig` - Web-Crawl-Konfiguration API
- :doc:`api-admin-dataconfig` - Datenspeicher-Konfiguration API
- :doc:`../../admin/fileconfig-guide` - Datei-Crawl-Konfigurationsanleitung
