==========================
DataConfig API
==========================

Übersicht
=========

Die DataConfig API dient zur Verwaltung der Datenspeicher-Konfiguration in |Fess|.
Sie können Crawl-Einstellungen für Datenquellen wie Datenbanken, CSV und JSON verwalten.

Basis-URL
=========

::

    /api/admin/dataconfig

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
     - Datenspeicher-Konfigurationsliste abrufen
   * - GET
     - /setting/{id}
     - Datenspeicher-Konfiguration abrufen
   * - POST
     - /setting
     - Datenspeicher-Konfiguration erstellen
   * - PUT
     - /setting
     - Datenspeicher-Konfiguration aktualisieren
   * - DELETE
     - /setting/{id}
     - Datenspeicher-Konfiguration löschen

Datenspeicher-Konfigurationsliste abrufen
=========================================

Request
-------

::

    GET /api/admin/dataconfig/settings

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
     - Anzahl der Einträge pro Seite (Standard: 25)
   * - ``page``
     - Integer
     - Nein
     - Seitennummer (beginnt bei 1, Standard: 1)
   * - ``name``
     - String
     - Nein
     - Filtern nach Konfigurationsname
   * - ``handlerName``
     - String
     - Nein
     - Filtern nach Handler-Name
   * - ``description``
     - String
     - Nein
     - Filtern nach Beschreibung

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "dataconfig_id_1",
            "name": "Database Crawler",
            "description": "Datenbank-Crawler",
            "handlerName": "DatabaseDataStore",
            "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb",
            "handlerScript": "...",
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

Datenspeicher-Konfiguration abrufen
===================================

Request
-------

::

    GET /api/admin/dataconfig/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "dataconfig_id_1",
          "name": "Database Crawler",
          "description": "Datenbank-Crawler",
          "handlerName": "DatabaseDataStore",
          "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb\nusername=dbuser\npassword=dbpass",
          "handlerScript": "...",
          "boost": 1.0,
          "available": "true",
          "sortOrder": 0,
          "permissions": "{role}admin",
          "virtualHosts": ""
        }
      }
    }

Datenspeicher-Konfiguration erstellen
=====================================

Request
-------

::

    POST /api/admin/dataconfig/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Product Database",
      "handlerName": "DatabaseDataStore",
      "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/products\nusername=user\npassword=pass",
      "handlerScript": "url=\"https://example.com/product/\" + product_id\ntitle=product_name\ncontent=description",
      "boost": 1.0,
      "available": "true",
      "sortOrder": 0,
      "permissions": "{role}admin\n{role}user"
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
     - Konfigurationsname
   * - ``description``
     - Nein
     - Beschreibung der Konfiguration
   * - ``handlerName``
     - Ja
     - Name des Datenspeicher-Handlers
   * - ``handlerParameter``
     - Nein
     - Handler-Parameter (Verbindungsinformationen usw.)
   * - ``handlerScript``
     - Nein
     - Datenkonvertierungsskript
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

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_dataconfig_id",
        "created": true
      }
    }

Datenspeicher-Konfiguration aktualisieren
=========================================

Request
-------

::

    PUT /api/admin/dataconfig/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_dataconfig_id",
      "name": "Updated Product Database",
      "handlerName": "DatabaseDataStore",
      "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/products\nusername=user\npassword=newpass",
      "handlerScript": "url=\"https://example.com/product/\" + product_id\ntitle=product_name\ncontent=description + \" \" + features",
      "boost": 1.5,
      "available": "true",
      "sortOrder": 0,
      "versionNo": 1
    }

Aktualisierungsanfragen erfordern dieselben Pflichtfelder wie beim Erstellen (``name``, ``handlerName``, ``boost``, ``available``, ``sortOrder``) sowie zusätzlich die folgenden Felder:

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``id``
     - Ja
     - ID der zu aktualisierenden Konfiguration
   * - ``versionNo``
     - Ja
     - Versionsnummer für optimistisches Sperren (den beim Abrufen erhaltenen Wert angeben)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_dataconfig_id",
        "created": false
      }
    }

Datenspeicher-Konfiguration löschen
===================================

Request
-------

::

    DELETE /api/admin/dataconfig/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Handler-Typen
=============

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Handler-Name
     - Beschreibung
   * - ``DatabaseDataStore``
     - Verbindung zur Datenbank über JDBC
   * - ``CsvDataStore``
     - Daten aus CSV-Dateien lesen (jede Zeile wird als ein Dokument verarbeitet)
   * - ``CsvListDataStore``
     - CSV-Dateien lesen und verarbeitete Dateien automatisch löschen (eine Erweiterung von ``CsvDataStore`` mit zeitstempelbasierter Filterung)
   * - ``JsonDataStore``
     - Daten aus JSON-Dateien oder JSON-APIs lesen

.. note::

   Die verfügbaren Handler-Typen hängen von den installierten Datenspeicher-Plugins ab.
   Die oben genannten Handler sind standardmäßig enthalten. Durch die Installation von
   Datenspeicher-Plugins wie SharePoint, Slack oder Salesforce werden die entsprechenden
   Handler-Namen verfügbar.

Verwendungsbeispiele
====================

Datenbank-Crawl-Konfiguration
-----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dataconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "User Database",
           "handlerName": "DatabaseDataStore",
           "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/userdb\nusername=dbuser\npassword=dbpass\nsql=SELECT * FROM users WHERE active=true",
           "handlerScript": "url=\"https://example.com/user/\" + user_id\ntitle=username\ncontent=profile",
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-webconfig` - Web-Crawl-Konfiguration API
- :doc:`api-admin-fileconfig` - Datei-Crawl-Konfiguration API
- :doc:`../../admin/dataconfig-guide` - Datenspeicher-Konfigurationsanleitung
