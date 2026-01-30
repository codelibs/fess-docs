==========================
FailureUrl API
==========================

Übersicht
=========

Die FailureUrl API dient zur Verwaltung von fehlgeschlagenen Crawl-URLs in |Fess|.
Sie können URLs überprüfen und löschen, bei denen während des Crawlings Fehler aufgetreten sind.

Basis-URL
=========

::

    /api/admin/failureurl

Endpunktliste
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Pfad
     - Beschreibung
   * - GET
     - /
     - Liste der fehlgeschlagenen URLs abrufen
   * - DELETE
     - /{id}
     - Fehlgeschlagene URL löschen
   * - DELETE
     - /delete-all
     - Alle fehlgeschlagenen URLs löschen

Liste der fehlgeschlagenen URLs abrufen
=======================================

Request
-------

::

    GET /api/admin/failureurl

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
   * - ``errorCountMin``
     - Integer
     - Nein
     - Mindestanzahl der Fehler zum Filtern
   * - ``configId``
     - String
     - Nein
     - Konfigurations-ID zum Filtern

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "failures": [
          {
            "id": "failure_id_1",
            "url": "https://example.com/broken-page",
            "configId": "webconfig_id_1",
            "errorName": "ConnectException",
            "errorLog": "Connection refused: connect",
            "errorCount": 3,
            "lastAccessTime": "2025-01-29T10:00:00Z",
            "threadName": "Crawler-1"
          },
          {
            "id": "failure_id_2",
            "url": "https://example.com/not-found",
            "configId": "webconfig_id_1",
            "errorName": "HttpStatusException",
            "errorLog": "404 Not Found",
            "errorCount": 1,
            "lastAccessTime": "2025-01-29T09:30:00Z",
            "threadName": "Crawler-2"
          }
        ],
        "total": 45
      }
    }

Response-Felder
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beschreibung
   * - ``id``
     - Fehlgeschlagene URL ID
   * - ``url``
     - Die fehlgeschlagene URL
   * - ``configId``
     - Crawl-Konfigurations-ID
   * - ``errorName``
     - Fehlername
   * - ``errorLog``
     - Fehlerprotokoll
   * - ``errorCount``
     - Anzahl der aufgetretenen Fehler
   * - ``lastAccessTime``
     - Letzte Zugriffszeit
   * - ``threadName``
     - Thread-Name

Fehlgeschlagene URL löschen
===========================

Request
-------

::

    DELETE /api/admin/failureurl/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Failure URL deleted successfully"
      }
    }

Alle fehlgeschlagenen URLs löschen
==================================

Request
-------

::

    DELETE /api/admin/failureurl/delete-all

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``configId``
     - String
     - Nein
     - Nur fehlgeschlagene URLs einer bestimmten Konfiguration löschen
   * - ``errorCountMin``
     - Integer
     - Nein
     - Nur URLs mit mindestens der angegebenen Fehleranzahl löschen

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "All failure URLs deleted successfully",
        "deletedCount": 45
      }
    }

Fehlertypen
===========

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Fehlername
     - Beschreibung
   * - ``ConnectException``
     - Verbindungsfehler
   * - ``HttpStatusException``
     - HTTP-Statusfehler (404, 500 usw.)
   * - ``SocketTimeoutException``
     - Timeout-Fehler
   * - ``UnknownHostException``
     - Host-Auflösungsfehler
   * - ``SSLException``
     - SSL-Zertifikatsfehler
   * - ``IOException``
     - Ein-/Ausgabefehler

Verwendungsbeispiele
====================

Liste der fehlgeschlagenen URLs abrufen
---------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl?size=100&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Nach Fehleranzahl filtern
-------------------------

.. code-block:: bash

    # Nur URLs mit 3 oder mehr Fehlern abrufen
    curl -X GET "http://localhost:8080/api/admin/failureurl?errorCountMin=3" \
         -H "Authorization: Bearer YOUR_TOKEN"

Fehlgeschlagene URLs einer bestimmten Konfiguration abrufen
-----------------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl?configId=webconfig_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Fehlgeschlagene URL löschen
---------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/failureurl/failure_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Alle fehlgeschlagenen URLs löschen
----------------------------------

.. code-block:: bash

    # Alle fehlgeschlagenen URLs löschen
    curl -X DELETE "http://localhost:8080/api/admin/failureurl/delete-all" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Nur fehlgeschlagene URLs einer bestimmten Konfiguration löschen
    curl -X DELETE "http://localhost:8080/api/admin/failureurl/delete-all?configId=webconfig_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Nur URLs mit 3 oder mehr Fehlern löschen
    curl -X DELETE "http://localhost:8080/api/admin/failureurl/delete-all?errorCountMin=3" \
         -H "Authorization: Bearer YOUR_TOKEN"

Fehlertypen aggregieren
-----------------------

.. code-block:: bash

    # Anzahl nach Fehlertyp zählen
    curl -X GET "http://localhost:8080/api/admin/failureurl?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '[.response.failures[].errorName] | group_by(.) | map({error: .[0], count: length})'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-crawlinginfo` - Crawl-Informationen API
- :doc:`api-admin-joblog` - Job-Protokoll API
- :doc:`../../admin/failureurl-guide` - Fehlgeschlagene URLs Verwaltungsanleitung
