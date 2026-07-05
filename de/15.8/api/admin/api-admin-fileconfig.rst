==========================
FileConfig API
==========================

Übersicht
=========

Die FileConfig API dient zur Verwaltung der Datei-Crawl-Konfigurationen in |Fess|.
Sie können Crawl-Einstellungen für lokale Dateisysteme, SMB/CIFS-Freigabeordner, FTP und verschiedene Objektspeicherdienste verwalten.

Basis-URL
=========

::

    /api/admin/fileconfig

.. note::

   Alle Endpunkte erfordern Administratorrechte und ein gültiges Zugriffstoken.
   Informationen zur Authentifizierung finden Sie unter :doc:`api-admin-overview`.

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

.. note::

   Der Listen-Endpunkt ist neben ``GET`` auch über ``PUT`` erreichbar.

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 10 55

   * - Parameter
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``page``
     - Integer
     - Nein
     - Seitennummer (beginnt bei 1, Standard: 1)
   * - ``size``
     - Integer
     - Nein
     - Anzahl der Einträge pro Seite (Standard: 25; richtet sich nach der Einstellung ``paging.page.size``)
   * - ``name``
     - String
     - Nein
     - Filterung nach Konfigurationsname
   * - ``paths``
     - String
     - Nein
     - Filterung nach Crawl-Pfad
   * - ``description``
     - String
     - Nein
     - Filterung nach Beschreibung

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
            "paths": "smb://server/share/documents",
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

``total`` gibt die Gesamtanzahl der Konfigurationen an, die den Suchkriterien entsprechen.

Datei-Crawl-Konfiguration abrufen
==================================

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
          "paths": "smb://server/share/documents",
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
          "createdBy": "admin",
          "createdTime": 1700000000000,
          "updatedBy": "admin",
          "updatedTime": 1700000000000,
          "versionNo": 1
        }
      }
    }

.. note::

   Die Response enthält die vom Server automatisch gesetzten Felder ``createdBy``, ``createdTime``,
   ``updatedBy``, ``updatedTime`` und ``versionNo``.
   ``versionNo`` wird bei der Aktualisierung benötigt (siehe „Datei-Crawl-Konfiguration aktualisieren" weiter unten).

Datei-Crawl-Konfiguration erstellen
=====================================

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
      "permissions": "{role}admin\n{role}user"
    }

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``name``
     - Ja
     - Konfigurationsname (max. 200 Zeichen)
   * - ``description``
     - Nein
     - Beschreibung der Konfiguration (max. 1000 Zeichen)
   * - ``paths``
     - Ja
     - Crawl-Startpfade (bei mehreren durch Zeilenumbruch getrennt). Anzugeben mit einem der Protokolle ``file:``, ``smb:``, ``smb1:``, ``ftp:``, ``storage:``, ``s3:`` oder ``gcs:``
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
     - Zusätzliche Konfigurationsparameter (Format ``key=value``, ein Eintrag pro Zeile)
   * - ``depth``
     - Nein
     - Crawl-Tiefe (0 oder größer)
   * - ``maxAccessCount``
     - Nein
     - Maximale Zugriffsanzahl (0 oder größer)
   * - ``numOfThread``
     - Ja
     - Anzahl paralleler Threads (1 oder größer)
   * - ``intervalTime``
     - Ja
     - Zugriffsintervall (Millisekunden, 0 oder größer)
   * - ``boost``
     - Ja
     - Boost-Wert für Suchergebnisse
   * - ``available``
     - Ja
     - Aktiviert/Deaktiviert (Zeichenkette ``"true"`` / ``"false"``)
   * - ``sortOrder``
     - Ja
     - Anzeigereihenfolge (0 oder größer)
   * - ``permissions``
     - Nein
     - Zugriffsberechtigte Rollen (bei mehreren durch Zeilenumbruch getrennt)
   * - ``virtualHosts``
     - Nein
     - Virtuelle Hosts (bei mehreren durch Zeilenumbruch getrennt)

.. note::

   Audit-Felder wie ``createdBy``, ``createdTime``, ``updatedBy`` und ``updatedTime`` werden
   serverseitig automatisch gesetzt und müssen nicht im Request-Body angegeben werden.

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
=========================================

Request
-------

::

    PUT /api/admin/fileconfig/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

Bei der Aktualisierung sind neben den Feldern aus der Erstellung zusätzlich ``id`` zur Identifikation der Zielkonfiguration und ``versionNo`` als Versionsnummer erforderlich.
Für ``versionNo`` ist der aktuelle Wert aus der Response der Abruf-API (GET) anzugeben.

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

Zusätzliche Felder bei der Aktualisierung
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``id``
     - Ja
     - Konfigurations-ID der zu aktualisierenden Konfiguration (max. 1000 Zeichen)
   * - ``versionNo``
     - Ja
     - Aktuelle Versionsnummer der zu aktualisierenden Konfiguration. Anzugeben ist der ``versionNo``-Wert aus der Response der Abruf-API (GET)

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
====================================

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

Für ``paths`` können folgende Protokolle verwendet werden (die unterstützten Protokolle können über die Einstellung ``crawler.file.protocols`` geändert werden).

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Protokoll
     - Pfadformat
   * - Lokale Datei
     - ``file:///path/to/directory``
   * - SMB/CIFS-Freigabe
     - ``smb://server/share/path``
   * - SMB/CIFS-Freigabe (SMB1)
     - ``smb1://server/share/path``
   * - FTP
     - ``ftp://server/path``
   * - S3-kompatibler Objektspeicher (z. B. MinIO)
     - ``storage://bucket/path``
   * - Amazon S3
     - ``s3://bucket/path``
   * - Google Cloud Storage
     - ``gcs://bucket/path``

.. note::

   Anmeldeinformationen (Benutzername und Passwort) für SMB/CIFS oder FTP sollten nicht in den Pfad eingebettet werden.
   Konfigurieren Sie diese stattdessen in der „Datei-Authentifizierung"-Einstellung. Details finden Sie unter :doc:`../../admin/fileauth-guide`.

Verwendungsbeispiele
====================

Crawl-Konfiguration für lokale Dateien
---------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/fileconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Local Files",
           "paths": "file:///data/documents",
           "includedPaths": ".*\\.(pdf|doc|docx)$",
           "excludedPaths": ".*/(temp|backup)/.*",
           "numOfThread": 2,
           "intervalTime": 500,
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

Crawl-Konfiguration für SMB-Freigaben
---------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/fileconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "SMB Share",
           "paths": "smb://server/documents",
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

.. note::

   Falls für den Zugriff auf die SMB-Freigabe eine Authentifizierung erforderlich ist, registrieren Sie
   vorab die Anmeldeinformationen für den Ziel-Host in der „Datei-Authentifizierung"-Einstellung.

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-webconfig` - Web-Crawl-Konfiguration API
- :doc:`api-admin-dataconfig` - Datenspeicher-Konfiguration API
- :doc:`../../admin/fileconfig-guide` - Datei-Crawl-Konfigurationsanleitung
- :doc:`../../admin/fileauth-guide` - Datei-Authentifizierungsanleitung
