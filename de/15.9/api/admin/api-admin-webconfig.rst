==========================
WebConfig API
==========================

Übersicht
=========

Die WebConfig API dient zur Verwaltung der Web-Crawl-Konfigurationen in |Fess|.
Sie können Einstellungen wie Crawl-Ziel-URLs, Crawl-Tiefe und Ausschlussmuster verwalten.

Basis-URL
=========

::

    /api/admin/webconfig

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
     - Web-Crawl-Konfigurationsliste abrufen
   * - GET
     - /setting/{id}
     - Web-Crawl-Konfiguration abrufen
   * - POST
     - /setting
     - Web-Crawl-Konfiguration erstellen
   * - PUT
     - /setting
     - Web-Crawl-Konfiguration aktualisieren
   * - DELETE
     - /setting/{id}
     - Web-Crawl-Konfiguration löschen

Web-Crawl-Konfigurationsliste abrufen
======================================

Request
-------

::

    GET /api/admin/webconfig/settings

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
   * - ``urls``
     - String
     - Nein
     - Filterung nach Crawl-URL
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
            "id": "webconfig_id_1",
            "name": "Example Site",
            "description": "Beispielseite",
            "urls": "https://example.com/",
            "includedUrls": ".*example\\.com.*",
            "excludedUrls": ".*\\.(pdf|zip)$",
            "includedDocUrls": "",
            "excludedDocUrls": "",
            "configParameter": "",
            "depth": 3,
            "maxAccessCount": 1000,
            "userAgent": "Mozilla/5.0",
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

Web-Crawl-Konfiguration abrufen
================================

Request
-------

::

    GET /api/admin/webconfig/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "webconfig_id_1",
          "name": "Example Site",
          "description": "Beispielseite",
          "urls": "https://example.com/",
          "includedUrls": ".*example\\.com.*",
          "excludedUrls": ".*\\.(pdf|zip)$",
          "includedDocUrls": "",
          "excludedDocUrls": "",
          "configParameter": "",
          "depth": 3,
          "maxAccessCount": 1000,
          "userAgent": "Mozilla/5.0",
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
   ``versionNo`` wird bei der Aktualisierung benötigt (siehe „Web-Crawl-Konfiguration aktualisieren" weiter unten).

Web-Crawl-Konfiguration erstellen
===================================

Request
-------

::

    POST /api/admin/webconfig/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Corporate Site",
      "urls": "https://www.example.com/",
      "includedUrls": ".*www\\.example\\.com.*",
      "excludedUrls": ".*\\.(pdf|zip|exe)$",
      "userAgent": "Mozilla/5.0",
      "numOfThread": 3,
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
   * - ``urls``
     - Ja
     - Crawl-Start-URLs (bei mehreren durch Zeilenumbruch getrennt). Anzugeben mit ``http:`` oder ``https:``
   * - ``includedUrls``
     - Nein
     - Regex-Muster für zu crawlende URLs
   * - ``excludedUrls``
     - Nein
     - Regex-Muster für auszuschließende URLs
   * - ``includedDocUrls``
     - Nein
     - Regex-Muster für zu indexierende URLs
   * - ``excludedDocUrls``
     - Nein
     - Regex-Muster für vom Index auszuschließende URLs
   * - ``configParameter``
     - Nein
     - Zusätzliche Konfigurationsparameter (Format ``key=value``, ein Eintrag pro Zeile)
   * - ``depth``
     - Nein
     - Crawl-Tiefe (0 oder größer)
   * - ``maxAccessCount``
     - Nein
     - Maximale Zugriffsanzahl (0 oder größer)
   * - ``userAgent``
     - Ja
     - User-Agent-Zeichenkette (max. 200 Zeichen)
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
        "id": "new_webconfig_id",
        "created": true
      }
    }

Web-Crawl-Konfiguration aktualisieren
=======================================

Request
-------

::

    PUT /api/admin/webconfig/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

Bei der Aktualisierung sind neben den Feldern aus der Erstellung zusätzlich ``id`` zur Identifikation der Zielkonfiguration und ``versionNo`` als Versionsnummer erforderlich.
Für ``versionNo`` ist der aktuelle Wert aus der Response der Abruf-API (GET) anzugeben.

.. code-block:: json

    {
      "id": "existing_webconfig_id",
      "name": "Updated Corporate Site",
      "urls": "https://www.example.com/",
      "includedUrls": ".*www\\.example\\.com.*",
      "excludedUrls": ".*\\.(pdf|zip|exe|dmg)$",
      "userAgent": "Mozilla/5.0",
      "depth": 10,
      "maxAccessCount": 10000,
      "numOfThread": 5,
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
        "id": "existing_webconfig_id",
        "created": false
      }
    }

Web-Crawl-Konfiguration löschen
=================================

Request
-------

::

    DELETE /api/admin/webconfig/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

URL-Muster-Beispiele
====================

Für ``includedUrls`` / ``excludedUrls`` / ``includedDocUrls`` / ``excludedDocUrls`` werden reguläre Ausdrücke angegeben.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Muster
     - Beschreibung
   * - ``.*example\\.com.*``
     - Alle URLs, die example.com enthalten
   * - ``https://example\\.com/docs/.*``
     - Nur unter /docs/
   * - ``.*\\.(pdf|doc|docx)$``
     - PDF-, DOC-, DOCX-Dateien
   * - ``.*\\?.*``
     - URLs mit Query-Parametern
   * - ``.*/(login|logout|admin)/.*``
     - URLs mit bestimmten Pfaden

Verwendungsbeispiele
====================

Crawl-Konfiguration für Unternehmenswebsite
--------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Corporate Website",
           "urls": "https://www.example.com/",
           "includedUrls": ".*www\\.example\\.com.*",
           "excludedUrls": ".*/(login|admin|api)/.*",
           "userAgent": "Mozilla/5.0",
           "depth": 5,
           "maxAccessCount": 10000,
           "numOfThread": 3,
           "intervalTime": 500,
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

Crawl-Konfiguration für Dokumentationswebsite
----------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Documentation Site",
           "urls": "https://docs.example.com/",
           "includedUrls": ".*docs\\.example\\.com.*",
           "includedDocUrls": ".*\\.(html|htm)$",
           "userAgent": "Mozilla/5.0",
           "maxAccessCount": 50000,
           "numOfThread": 5,
           "intervalTime": 200,
           "boost": 1.5,
           "available": "true",
           "sortOrder": 0
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-fileconfig` - Datei-Crawl-Konfiguration API
- :doc:`api-admin-dataconfig` - Datenspeicher-Konfiguration API
- :doc:`../../admin/webconfig-guide` - Web-Crawl-Konfigurationsanleitung
