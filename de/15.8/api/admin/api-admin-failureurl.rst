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
     - Anzahl der Einträge pro Seite (Standard: 20)
   * - ``page``
     - Integer
     - Nein
     - Seitennummer (beginnt bei 1, Standard: 1)
   * - ``url``
     - String
     - Nein
     - URL-Filter (Wildcards ``*`` ``?`` werden unterstützt)
   * - ``errorCountMin``
     - Integer
     - Nein
     - Untergrenze für die Fehleranzahl (größer als oder gleich dem angegebenen Wert)
   * - ``errorCountMax``
     - Integer
     - Nein
     - Obergrenze für die Fehleranzahl (kleiner als oder gleich dem angegebenen Wert)
   * - ``errorName``
     - String
     - Nein
     - Fehlername-Filter (Wildcard-Abgleich mit dem gespeicherten vollständig qualifizierten Klassennamen; ``*`` ``?`` werden unterstützt)

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
            "errorName": "java.net.ConnectException",
            "errorLog": "Connection refused: connect",
            "errorCount": "3",
            "lastAccessTime": "1738144800000",
            "configId": "webConfig_id_1"
          },
          {
            "id": "failure_id_2",
            "url": "https://example.com/not-found",
            "threadName": "Crawler-2",
            "errorName": "org.codelibs.fess.exception.ContentNotFoundException",
            "errorLog": "Not found: https://example.com/not-found",
            "errorCount": "1",
            "lastAccessTime": "1738143000000",
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
     - Fehlername (vollständig qualifizierter Klassenname der aufgetretenen Ausnahme; z. B. ``java.net.ConnectException``)
   * - ``errorLog``
     - Fehlerprotokoll (Ausnahme-Meldung oder Stack-Trace)
   * - ``errorCount``
     - Anzahl der aufgetretenen Fehler (numerischer Wert als Zeichenkette)
   * - ``lastAccessTime``
     - Letzte Zugriffszeit (Epoch-Millisekunden als Zeichenkette)
   * - ``configId``
     - Crawl-Konfigurations-ID

.. note::

   Alle Antwortfelder werden als Zeichenketten (JSON string) zurückgegeben. ``errorCount`` ist ein numerischer Wert, der als Zeichenkette dargestellt wird, und ``lastAccessTime`` sind Epoch-Millisekunden, die als Zeichenkette dargestellt werden.

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
          "errorName": "java.net.ConnectException",
          "errorLog": "Connection refused: connect",
          "errorCount": "3",
          "lastAccessTime": "1738144800000",
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

``errorName`` speichert den vollständig qualifizierten Klassennamen der Ausnahme, die während des Crawlings aufgetreten ist, genau so wie er erfasst wurde. Es handelt sich nicht um eine feste Aufzählung; je nach ausgelöster Ausnahme kann ein beliebiger Klassenname erscheinen. Im Folgenden sind repräsentative Beispiele aufgeführt.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Fehlername (Beispiel)
     - Beschreibung
   * - ``java.net.ConnectException``
     - Verbindung verweigert (keine Verbindung zum Server möglich)
   * - ``java.net.UnknownHostException``
     - Hostname konnte nicht aufgelöst werden (DNS-Fehler)
   * - ``java.net.SocketTimeoutException``
     - Verbindungs- oder Lese-Timeout
   * - ``javax.net.ssl.SSLException``
     - SSL/TLS-Handshake- oder Zertifikatsfehler
   * - ``java.io.IOException``
     - Ein-/Ausgabefehler
   * - ``org.codelibs.fess.exception.ContentNotFoundException``
     - URL, die einen HTTP-Statuscode zurückgegeben hat, der in ``crawler.failure.url.status.codes`` konfiguriert ist (Standard: 403, 404, 410)
   * - ``org.codelibs.fess.crawler.exception.MaxLengthExceededException``
     - Inhalt hat die maximale Länge überschritten

Verwendungsbeispiele
====================

Fehlgeschlagene URLs auflisten
------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?size=100&page=1" \
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

    # errorName speichert den vollständig qualifizierten Klassennamen, daher mit Wildcard angeben
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?errorName=*ConnectException" \
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
