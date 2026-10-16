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
            "included_paths": ".*\\.pdf$",
            "excluded_paths": ".*/(temp|cache)/.*",
            "included_doc_paths": "",
            "excluded_doc_paths": "",
            "config_parameter": "",
            "depth": 10,
            "max_access_count": 1000,
            "num_of_thread": 1,
            "interval_time": 1000,
            "boost": 1.0,
            "available": "true",
            "permissions": "{role}admin",
            "virtual_hosts": "",
            "sort_order": 0
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
          "included_paths": ".*\\.pdf$",
          "excluded_paths": ".*/(temp|cache)/.*",
          "included_doc_paths": "",
          "excluded_doc_paths": "",
          "config_parameter": "",
          "depth": 10,
          "max_access_count": 1000,
          "num_of_thread": 1,
          "interval_time": 1000,
          "boost": 1.0,
          "available": "true",
          "sort_order": 0,
          "permissions": "{role}admin",
          "virtual_hosts": "",
          "created_by": "admin",
          "created_time": 1700000000000,
          "updated_by": "admin",
          "updated_time": 1700000000000,
          "version_no": 1
        }
      }
    }

.. note::

   Die Response enthält die vom Server automatisch gesetzten Felder ``created_by``, ``created_time``,
   ``updated_by``, ``updated_time`` und ``version_no``.
   ``version_no`` wird bei der Aktualisierung benötigt (siehe „Datei-Crawl-Konfiguration aktualisieren" weiter unten).

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
      "included_paths": ".*\\.(pdf|doc|docx|xls|xlsx)$",
      "excluded_paths": ".*/(temp|backup)/.*",
      "num_of_thread": 2,
      "interval_time": 500,
      "boost": 1.0,
      "available": "true",
      "sort_order": 0,
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
     - Crawl-Startpfade (bei mehreren durch Zeilenumbruch getrennt). Anzugeben mit einem der Protokolle ``file:``, ``smb:``, ``smb1:``, ``ftp:``, ``s3:`` oder ``gcs:``
   * - ``included_paths``
     - Nein
     - Regex-Muster für zu crawlende Pfade
   * - ``excluded_paths``
     - Nein
     - Regex-Muster für auszuschließende Pfade
   * - ``included_doc_paths``
     - Nein
     - Regex-Muster für zu indexierende Pfade
   * - ``excluded_doc_paths``
     - Nein
     - Regex-Muster für vom Index auszuschließende Pfade
   * - ``config_parameter``
     - Nein
     - Zusätzliche Konfigurationsparameter (Format ``key=value``, ein Eintrag pro Zeile)
   * - ``depth``
     - Nein
     - Crawl-Tiefe (0 oder größer)
   * - ``max_access_count``
     - Nein
     - Maximale Zugriffsanzahl (0 oder größer)
   * - ``num_of_thread``
     - Ja
     - Anzahl paralleler Threads (1 oder größer)
   * - ``interval_time``
     - Ja
     - Zugriffsintervall (Millisekunden, 0 oder größer)
   * - ``boost``
     - Ja
     - Boost-Wert für Suchergebnisse
   * - ``available``
     - Ja
     - Aktiviert/Deaktiviert (Zeichenkette ``"true"`` / ``"false"``)
   * - ``sort_order``
     - Ja
     - Anzeigereihenfolge (0 oder größer)
   * - ``permissions``
     - Nein
     - Zugriffsberechtigte Rollen (bei mehreren durch Zeilenumbruch getrennt)
   * - ``virtual_hosts``
     - Nein
     - Virtuelle Hosts (bei mehreren durch Zeilenumbruch getrennt)

.. note::

   Audit-Felder wie ``created_by``, ``created_time``, ``updated_by`` und ``updated_time`` werden
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

Bei der Aktualisierung sind neben den Feldern aus der Erstellung zusätzlich ``id`` zur Identifikation der Zielkonfiguration und ``version_no`` als Versionsnummer erforderlich.
Für ``version_no`` ist der aktuelle Wert aus der Response der Abruf-API (GET) anzugeben.

.. code-block:: json

    {
      "id": "existing_fileconfig_id",
      "name": "Updated Local Files",
      "paths": "file:///data/documents",
      "included_paths": ".*\\.(pdf|doc|docx|xls|xlsx|ppt|pptx)$",
      "excluded_paths": ".*/(temp|backup|archive)/.*",
      "depth": 10,
      "max_access_count": 10000,
      "num_of_thread": 3,
      "interval_time": 300,
      "boost": 1.2,
      "available": "true",
      "sort_order": 0,
      "version_no": 1
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
   * - ``version_no``
     - Ja
     - Aktuelle Versionsnummer der zu aktualisierenden Konfiguration. Anzugeben ist der ``version_no``-Wert aus der Response der Abruf-API (GET)

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
   * - Amazon S3 / S3-kompatibler Objektspeicher (z. B. MinIO)
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
           "included_paths": ".*\\.(pdf|doc|docx)$",
           "excluded_paths": ".*/(temp|backup)/.*",
           "num_of_thread": 2,
           "interval_time": 500,
           "boost": 1.0,
           "available": "true",
           "sort_order": 0,
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
           "included_paths": ".*\\.(pdf|doc|docx)$",
           "excluded_paths": ".*/(temp|private)/.*",
           "max_access_count": 50000,
           "num_of_thread": 3,
           "interval_time": 200,
           "boost": 1.0,
           "available": "true",
           "sort_order": 0,
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
