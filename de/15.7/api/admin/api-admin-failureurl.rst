==========================
FailureUrl API
==========================

Übersicht
=========

Die FailureUrl API dient zur Verwaltung von fehlgeschlagenen Crawl-URLs in |Fess|.
Sie können URLs, bei denen während des Crawlings ein Fehler aufgetreten ist, auflisten, einzeln abrufen und löschen.

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
     - /logs
     - Fehlgeschlagene URLs auflisten
   * - GET
     - /log/{id}
     - Fehlgeschlagene URL abrufen
   * - DELETE
     - /log/{id}
     - Fehlgeschlagene URL löschen
   * - DELETE
     - /all
     - Alle fehlgeschlagenen URLs löschen

Fehlgeschlagene URLs auflisten
==============================

Request
-------

::

    GET /api/admin/failureurl/logs

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
     - Anzahl der Einträge pro Seite
   * - ``page``
     - Integer
     - Nein
     - Seitennummer
   * - ``url``
     - String
     - Nein
     - Filter nach URL
   * - ``errorCountMin``
     - Integer
     - Nein
     - Filter nach Mindestanzahl der Fehler
   * - ``errorCountMax``
     - Integer
     - Nein
     - Filter nach maximaler Anzahl der Fehler
   * - ``errorName``
     - String
     - Nein
     - Filter nach Fehlername

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "failure_id_1",
            "url": "https://example.com/broken-page",
            "threadName": "Crawler-1",
            "errorName": "ConnectException",
            "errorLog": "Connection refused: connect",
            "errorCount": 3,
            "lastAccessTime": 1738144800000,
            "configId": "webConfig_id_1"
          },
          {
            "id": "failure_id_2",
            "url": "https://example.com/not-found",
            "threadName": "Crawler-2",
            "errorName": "HttpStatusException",
            "errorLog": "404 Not Found",
            "errorCount": 1,
            "lastAccessTime": 1738143000000,
            "configId": "webConfig_id_1"
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
     - Fehlgeschlagene-URL-ID
   * - ``url``
     - Die fehlgeschlagene URL
   * - ``threadName``
     - Thread-Name
   * - ``errorName``
     - Fehlername
   * - ``errorLog``
     - Fehlerprotokoll
   * - ``errorCount``
     - Anzahl der aufgetretenen Fehler
   * - ``lastAccessTime``
     - Letzte Zugriffszeit (Epoch-Millisekunden)
   * - ``configId``
     - Crawl-Konfigurations-ID

Fehlgeschlagene URL abrufen
===========================

Request
-------

::

    GET /api/admin/failureurl/log/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "failure_id_1",
          "url": "https://example.com/broken-page",
          "threadName": "Crawler-1",
          "errorName": "ConnectException",
          "errorLog": "Connection refused: connect",
          "errorCount": 3,
          "lastAccessTime": 1738144800000,
          "configId": "webConfig_id_1"
        }
      }
    }

Fehlgeschlagene URL löschen
===========================

Request
-------

::

    DELETE /api/admin/failureurl/log/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Alle fehlgeschlagenen URLs löschen
==================================

Löscht alle fehlgeschlagenen URLs. Es gibt keine Parameter.

Request
-------

::

    DELETE /api/admin/failureurl/all

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
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

Fehlgeschlagene URLs auflisten
------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?size=100&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Nach Fehleranzahl filtern
-------------------------

.. code-block:: bash

    # Nur URLs mit 3 oder mehr Fehlern abrufen
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?errorCountMin=3" \
         -H "Authorization: Bearer YOUR_TOKEN"

Nach Fehlername filtern
-----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?errorName=ConnectException" \
         -H "Authorization: Bearer YOUR_TOKEN"

Fehlgeschlagene URL abrufen
---------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/log/failure_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Fehlgeschlagene URL löschen
---------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/failureurl/log/failure_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Alle fehlgeschlagenen URLs löschen
----------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/failureurl/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

Nach Fehlertyp aggregieren
--------------------------

.. code-block:: bash

    # Anzahl nach Fehlertyp zählen
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '[.response.logs[].errorName] | group_by(.) | map({error: .[0], count: length})'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-crawlinginfo` - Crawl-Informationen API
- :doc:`api-admin-joblog` - Job-Protokoll API
- :doc:`../../admin/failureurl-guide` - Fehlgeschlagene URLs Verwaltungsanleitung
