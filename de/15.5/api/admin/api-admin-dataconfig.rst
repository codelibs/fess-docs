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
   * - GET/PUT
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
    PUT /api/admin/dataconfig/settings

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
            "id": "dataconfig_id_1",
            "name": "Database Crawler",
            "handlerName": "DatabaseDataStore",
            "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb",
            "handlerScript": "...",
            "boost": 1.0,
            "available": true,
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
          "handlerName": "DatabaseDataStore",
          "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb\nusername=dbuser\npassword=dbpass",
          "handlerScript": "...",
          "boost": 1.0,
          "available": true,
          "sortOrder": 0,
          "permissions": ["admin"],
          "virtualHosts": [],
          "labelTypeIds": []
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
      "handlerScript": "url=\"https://example.com/product/\" + data.product_id\ntitle=data.product_name\ncontent=data.description",
      "boost": 1.0,
      "available": true,
      "permissions": ["admin", "user"],
      "labelTypeIds": ["label_id_1"]
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
   * - ``handlerName``
     - Ja
     - Name des Datenspeicher-Handlers
   * - ``handlerParameter``
     - Nein
     - Handler-Parameter (Verbindungsinformationen usw.)
   * - ``handlerScript``
     - Ja
     - Datenkonvertierungsskript
   * - ``boost``
     - Nein
     - Boost-Wert für Suchergebnisse (Standard: 1.0)
   * - ``available``
     - Nein
     - Aktiviert/Deaktiviert (Standard: true)
   * - ``sortOrder``
     - Nein
     - Anzeigereihenfolge
   * - ``permissions``
     - Nein
     - Zugriffsberechtigte Rollen
   * - ``virtualHosts``
     - Nein
     - Virtuelle Hosts
   * - ``labelTypeIds``
     - Nein
     - Label-Typ-IDs

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
      "handlerScript": "url=\"https://example.com/product/\" + data.product_id\ntitle=data.product_name\ncontent=data.description + \" \" + data.features",
      "boost": 1.5,
      "available": true,
      "versionNo": 1
    }

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
        "status": 0,
        "id": "deleted_dataconfig_id",
        "created": false
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
     - Daten aus CSV-Dateien lesen
   * - ``JsonDataStore``
     - Daten aus JSON-Dateien oder JSON-APIs lesen

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
           "handlerScript": "url=\"https://example.com/user/\" + data.user_id\ntitle=data.username\ncontent=data.profile",
           "boost": 1.0,
           "available": true
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-webconfig` - Web-Crawl-Konfiguration API
- :doc:`api-admin-fileconfig` - Datei-Crawl-Konfiguration API
- :doc:`../../admin/dataconfig-guide` - Datenspeicher-Konfigurationsanleitung
