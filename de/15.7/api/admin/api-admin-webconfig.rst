==========================
WebConfig API
==========================

Übersicht
=========

Die WebConfig API dient zur Verwaltung der Web-Crawl-Konfiguration in |Fess|.
Sie können Einstellungen wie Crawl-Ziel-URLs, Crawl-Tiefe und Ausschlussmuster verwalten.

Basis-URL
=========

::

    /api/admin/webconfig

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
=====================================

Request
-------

::

    GET /api/admin/webconfig/settings

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

Web-Crawl-Konfiguration abrufen
===============================

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
          "labelTypeIds": []
        }
      }
    }

Web-Crawl-Konfiguration erstellen
=================================

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
   * - ``urls``
     - Ja
     - Crawl-Start-URLs (bei mehreren durch Zeilenumbruch getrennt)
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
     - Zusätzliche Konfigurationsparameter
   * - ``depth``
     - Nein
     - Crawl-Tiefe
   * - ``maxAccessCount``
     - Nein
     - Maximale Zugriffsanzahl
   * - ``userAgent``
     - Ja
     - User-Agent-Zeichenkette
   * - ``numOfThread``
     - Ja
     - Anzahl paralleler Threads
   * - ``intervalTime``
     - Ja
     - Anfrage-Intervall (Millisekunden)
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
        "id": "new_webconfig_id",
        "created": true
      }
    }

Web-Crawl-Konfiguration aktualisieren
=====================================

Request
-------

::

    PUT /api/admin/webconfig/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

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
===============================

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

includedUrls / excludedUrls
---------------------------

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
-------------------------------------------

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
---------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Documentation Site",
           "urls": "https://docs.example.com/",
           "includedUrls": ".*docs\\.example\\.com.*",
           "excludedUrls": "",
           "includedDocUrls": ".*\\.(html|htm)$",
           "userAgent": "Mozilla/5.0",
           "maxAccessCount": 50000,
           "numOfThread": 5,
           "intervalTime": 200,
           "boost": 1.5,
           "available": "true",
           "sortOrder": 0,
           "labelTypeIds": ["documentation_label_id"]
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-fileconfig` - Datei-Crawl-Konfiguration API
- :doc:`api-admin-dataconfig` - Datenspeicher-Konfiguration API
- :doc:`../../admin/webconfig-guide` - Web-Crawl-Konfigurationsanleitung
