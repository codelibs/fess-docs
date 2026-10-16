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
            "included_urls": ".*example\\.com.*",
            "excluded_urls": ".*\\.(pdf|zip)$",
            "included_doc_urls": "",
            "excluded_doc_urls": "",
            "config_parameter": "",
            "depth": 3,
            "max_access_count": 1000,
            "user_agent": "Mozilla/5.0",
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
          "included_urls": ".*example\\.com.*",
          "excluded_urls": ".*\\.(pdf|zip)$",
          "included_doc_urls": "",
          "excluded_doc_urls": "",
          "config_parameter": "",
          "depth": 3,
          "max_access_count": 1000,
          "user_agent": "Mozilla/5.0",
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
   ``version_no`` wird bei der Aktualisierung benötigt (siehe „Web-Crawl-Konfiguration aktualisieren" weiter unten).

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
      "included_urls": ".*www\\.example\\.com.*",
      "excluded_urls": ".*\\.(pdf|zip|exe)$",
      "user_agent": "Mozilla/5.0",
      "num_of_thread": 3,
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
   * - ``urls``
     - Ja
     - Crawl-Start-URLs (bei mehreren durch Zeilenumbruch getrennt). Anzugeben mit ``http:`` oder ``https:``
   * - ``included_urls``
     - Nein
     - Regex-Muster für zu crawlende URLs
   * - ``excluded_urls``
     - Nein
     - Regex-Muster für auszuschließende URLs
   * - ``included_doc_urls``
     - Nein
     - Regex-Muster für zu indexierende URLs
   * - ``excluded_doc_urls``
     - Nein
     - Regex-Muster für vom Index auszuschließende URLs
   * - ``config_parameter``
     - Nein
     - Zusätzliche Konfigurationsparameter (Format ``key=value``, ein Eintrag pro Zeile)
   * - ``depth``
     - Nein
     - Crawl-Tiefe (0 oder größer)
   * - ``max_access_count``
     - Nein
     - Maximale Zugriffsanzahl (0 oder größer)
   * - ``user_agent``
     - Ja
     - User-Agent-Zeichenkette (max. 200 Zeichen)
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

Bei der Aktualisierung sind neben den Feldern aus der Erstellung zusätzlich ``id`` zur Identifikation der Zielkonfiguration und ``version_no`` als Versionsnummer erforderlich.
Für ``version_no`` ist der aktuelle Wert aus der Response der Abruf-API (GET) anzugeben.

.. code-block:: json

    {
      "id": "existing_webconfig_id",
      "name": "Updated Corporate Site",
      "urls": "https://www.example.com/",
      "included_urls": ".*www\\.example\\.com.*",
      "excluded_urls": ".*\\.(pdf|zip|exe|dmg)$",
      "user_agent": "Mozilla/5.0",
      "depth": 10,
      "max_access_count": 10000,
      "num_of_thread": 5,
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

Für ``included_urls`` / ``excluded_urls`` / ``included_doc_urls`` / ``excluded_doc_urls`` werden reguläre Ausdrücke angegeben.

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
           "included_urls": ".*www\\.example\\.com.*",
           "excluded_urls": ".*/(login|admin|api)/.*",
           "user_agent": "Mozilla/5.0",
           "depth": 5,
           "max_access_count": 10000,
           "num_of_thread": 3,
           "interval_time": 500,
           "boost": 1.0,
           "available": "true",
           "sort_order": 0,
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
           "included_urls": ".*docs\\.example\\.com.*",
           "included_doc_urls": ".*\\.(html|htm)$",
           "user_agent": "Mozilla/5.0",
           "max_access_count": 50000,
           "num_of_thread": 5,
           "interval_time": 200,
           "boost": 1.5,
           "available": "true",
           "sort_order": 0
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-fileconfig` - Datei-Crawl-Konfiguration API
- :doc:`api-admin-dataconfig` - Datenspeicher-Konfiguration API
- :doc:`../../admin/webconfig-guide` - Web-Crawl-Konfigurationsanleitung
