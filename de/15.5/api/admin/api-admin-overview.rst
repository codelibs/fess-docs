==========================
Admin API Übersicht
==========================

Übersicht
=========

|Fess| Admin API ist eine RESTful API für den programmatischen Zugriff auf Verwaltungsfunktionen.
Die meisten Operationen, die über die Administrationsoberfläche durchgeführt werden können, wie Crawl-Konfiguration, Benutzerverwaltung und Scheduler-Steuerung, können über die API ausgeführt werden.

Mit dieser API können Sie die Konfiguration von |Fess| automatisieren oder mit externen Systemen integrieren.

Basis-URL
=========

Die Basis-URL der Admin API hat folgendes Format:

::

    http://<Server Name>/api/admin/

Beispiel für eine lokale Umgebung:

::

    http://localhost:8080/api/admin/

Authentifizierung
=================

Für den Zugriff auf die Admin API ist eine Authentifizierung mit einem Access Token erforderlich.

Access Token erhalten
---------------------

1. Melden Sie sich in der Administrationsoberfläche an
2. Navigieren Sie zu "System" -> "Access Token"
3. Klicken Sie auf "Neu erstellen"
4. Geben Sie einen Token-Namen ein und wählen Sie die erforderlichen Berechtigungen
5. Klicken Sie auf "Erstellen", um den Token zu erhalten

Token verwenden
---------------

Fügen Sie den Access Token in den Request-Header ein:

::

    Authorization: Bearer <Access Token>

Oder geben Sie ihn als Query-Parameter an:

::

    ?token=<Access Token>

cURL-Beispiel
~~~~~~~~~~~~~

.. code-block:: bash

    curl -H "Authorization: Bearer YOUR_TOKEN" \
         "http://localhost:8080/api/admin/scheduler/settings"

Erforderliche Berechtigungen
----------------------------

Um die Admin API zu verwenden, benötigt der Token folgende Berechtigungen:

- ``admin-*`` - Zugriff auf alle Verwaltungsfunktionen
- ``admin-scheduler`` - Nur Scheduler-Verwaltung
- ``admin-user`` - Nur Benutzerverwaltung
- Andere funktionsspezifische Berechtigungen

Gemeinsame Muster
=================

Liste abrufen (GET/PUT /settings)
---------------------------------

Ruft eine Liste von Einstellungen ab.

Request
~~~~~~~

::

    GET /api/admin/<resource>/settings
    PUT /api/admin/<resource>/settings

Parameter (Paginierung):

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Typ
     - Beschreibung
   * - ``size``
     - Integer
     - Anzahl der Einträge pro Seite (Standard: 20)
   * - ``page``
     - Integer
     - Seitennummer (beginnt bei 0)

Response
~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [...],
        "total": 100
      }
    }

Einzelne Einstellung abrufen (GET /setting/{id})
------------------------------------------------

Ruft eine einzelne Einstellung anhand der ID ab.

Request
~~~~~~~

::

    GET /api/admin/<resource>/setting/{id}

Response
~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {...}
      }
    }

Neu erstellen (POST /setting)
-----------------------------

Erstellt eine neue Einstellung.

Request
~~~~~~~

::

    POST /api/admin/<resource>/setting
    Content-Type: application/json

    {
      "name": "...",
      "...": "..."
    }

Response
~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "created_id",
        "created": true
      }
    }

Aktualisieren (PUT /setting)
----------------------------

Aktualisiert eine bestehende Einstellung.

Request
~~~~~~~

::

    PUT /api/admin/<resource>/setting
    Content-Type: application/json

    {
      "id": "...",
      "name": "...",
      "...": "..."
    }

Response
~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "updated_id",
        "created": false
      }
    }

Löschen (DELETE /setting/{id})
------------------------------

Löscht eine Einstellung.

Request
~~~~~~~

::

    DELETE /api/admin/<resource>/setting/{id}

Response
~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_id",
        "created": false
      }
    }

Response-Format
===============

Erfolgreiche Response
---------------------

.. code-block:: json

    {
      "response": {
        "status": 0,
        ...
      }
    }

``status: 0`` zeigt Erfolg an.

Fehler-Response
---------------

.. code-block:: json

    {
      "response": {
        "status": 1,
        "errors": [
          {"code": "errors.failed_to_create", "args": ["...", "..."]}
        ]
      }
    }

HTTP-Statuscodes
----------------

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Code
     - Beschreibung
   * - 200
     - Request erfolgreich
   * - 400
     - Ungültige Request-Parameter
   * - 401
     - Authentifizierung erforderlich (kein oder ungültiger Token)
   * - 403
     - Keine Zugriffsberechtigung
   * - 404
     - Ressource nicht gefunden
   * - 500
     - Interner Serverfehler

Verfügbare APIs
===============

|Fess| bietet folgende Admin APIs.

Crawl-Konfiguration
-------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpunkt
     - Beschreibung
   * - :doc:`api-admin-webconfig`
     - Web-Crawl-Konfiguration
   * - :doc:`api-admin-fileconfig`
     - Datei-Crawl-Konfiguration
   * - :doc:`api-admin-dataconfig`
     - Datenspeicher-Konfiguration

Index-Verwaltung
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpunkt
     - Beschreibung
   * - :doc:`api-admin-documents`
     - Dokument-Massenoperationen
   * - :doc:`api-admin-crawlinginfo`
     - Crawl-Informationen
   * - :doc:`api-admin-failureurl`
     - Fehlgeschlagene URL-Verwaltung
   * - :doc:`api-admin-backup`
     - Backup/Wiederherstellung

Scheduler
---------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpunkt
     - Beschreibung
   * - :doc:`api-admin-scheduler`
     - Job-Scheduling
   * - :doc:`api-admin-joblog`
     - Job-Protokoll abrufen

Benutzer- und Rechteverwaltung
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpunkt
     - Beschreibung
   * - :doc:`api-admin-user`
     - Benutzerverwaltung
   * - :doc:`api-admin-role`
     - Rollenverwaltung
   * - :doc:`api-admin-group`
     - Gruppenverwaltung
   * - :doc:`api-admin-accesstoken`
     - API-Token-Verwaltung

Such-Tuning
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpunkt
     - Beschreibung
   * - :doc:`api-admin-labeltype`
     - Label-Typen
   * - :doc:`api-admin-keymatch`
     - Key Match
   * - :doc:`api-admin-boostdoc`
     - Dokument-Boost
   * - :doc:`api-admin-elevateword`
     - Elevate Word
   * - :doc:`api-admin-badword`
     - Verbotene Wörter
   * - :doc:`api-admin-relatedcontent`
     - Verwandte Inhalte
   * - :doc:`api-admin-relatedquery`
     - Verwandte Abfragen
   * - :doc:`api-admin-suggest`
     - Suggest-Verwaltung

System
------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpunkt
     - Beschreibung
   * - :doc:`api-admin-general`
     - Allgemeine Einstellungen
   * - :doc:`api-admin-systeminfo`
     - Systeminformationen
   * - :doc:`api-admin-stats`
     - Systemstatistiken
   * - :doc:`api-admin-log`
     - Protokoll abrufen
   * - :doc:`api-admin-storage`
     - Speicherverwaltung
   * - :doc:`api-admin-plugin`
     - Plugin-Verwaltung

Wörterbuch
----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpunkt
     - Beschreibung
   * - :doc:`api-admin-dict`
     - Wörterbuchverwaltung (Synonyme, Stoppwörter usw.)

Verwendungsbeispiele
====================

Web-Crawl-Konfiguration erstellen
---------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Example Site",
           "urls": "https://example.com/",
           "includedUrls": ".*example.com.*",
           "excludedUrls": "",
           "maxAccessCount": 1000,
           "depth": 3,
           "available": true
         }'

Scheduler-Job starten
---------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

Benutzerliste abrufen
---------------------

.. code-block:: bash

    curl "http://localhost:8080/api/admin/user/settings?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Referenzinformationen
=====================

- :doc:`../api-overview` - API-Übersicht
- :doc:`../../admin/accesstoken-guide` - Access Token Verwaltungsanleitung
