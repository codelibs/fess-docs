===========
Health-API
===========

Dieses Dokument beschreibt die v2-Health-API von |Fess|.
Informationen zum gemeinsamen Antwort-Envelope und zum Fehlermodell finden Sie unter :doc:`api-overview`.

Die Basis-URL lautet ``http://<Server Name>/api/v2/`` (Beispiel für eine lokale Umgebung: ``http://localhost:8080/api/v2``).

Status abrufen
==============

Anfrage
-------

==================  ====================================================
HTTP-Methode         GET
Endpunkt             ``/api/v2/health``
==================  ====================================================

Gibt einen Statusschnappschuss des Suchmaschinenclusters zurück (Tag ``monitor``).
Der HTTP-Statuscode ist 200, wenn der Clusterstatus ``GREEN`` oder ``YELLOW`` ist, und 503 bei ``RED`` oder wenn die Suchmaschine nicht erreichbar ist.

``YELLOW`` wird zurückgegeben, wenn der Clusterstatus ``YELLOW`` ist, und auch dann, wenn der Clusterstatus ``GREEN`` ist, aber einer der Indizes von |Fess| oder der gesamte Cluster eine Sperre trägt, die Schreibzugriffe verweigert. OpenSearch setzt Indizes beispielsweise auf schreibgeschützt, wenn die Festplattenbelegung den Flood-Stage-Watermark überschreitet. Suchen funktionieren in diesem Zustand weiterhin, aber Crawling, Änderungen an den Einstellungen und Aktualisierungen des Index schlagen fehl. Indizes anderer Anwendungen, die sich den Cluster teilen, werden nicht berücksichtigt. Wenn die Sperren nicht gelesen werden können, bleibt der Status ``GREEN``. Da dieser Endpunkt ohne Authentifizierung aufgerufen werden kann, nennt die Antwort nicht den Grund für ``YELLOW``; ein Administrator sollte die Ursache auf der OpenSearch-Seite prüfen.

Dieser Endpunkt hält die Envelope-Invariante ein: „``status >= 1`` ⇔ HTTP-Status ``>= 400``".

- Bei ``GREEN`` / ``YELLOW``: Gibt einen Erfolgs-Envelope (``status: 0``) mit ``engine`` zurück.
- Bei ``RED``: Gibt einen Fehler-Envelope (``status: 9``, ``error.code: service_unavailable``) zurück und bettet den Engine-Schnappschuss unter ``error.details.engine`` ein (damit Überwachungswerkzeuge die Cluster-Metadaten auswerten können).
- Wenn die Suchmaschine nicht erreichbar ist: Gibt wie bei ``RED`` einen Fehler-Envelope zurück (``error.code: service_unavailable``, ``error.message: search engine is not reachable``); ``error.details.engine`` enthält ``status: UNAVAILABLE`` und ``ping_status: 1``.

.. note::

   ``/api/v2/search`` antwortet nicht mit 503, wenn die Suchmaschine nicht erreichbar ist. Es antwortet mit 200, ``partial: true`` und ohne Treffer (siehe :doc:`api-search`). Ein Client, der „keine Ergebnisse“ von „Suchmaschine ausgefallen“ unterscheiden muss, sollte ``partial`` in der Suchantwort prüfen und den Zustand der Suchmaschine über diesen Endpunkt bestätigen.

Die einzelnen Felder von ``engine`` sind wie folgt:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: engine-Felder

   * - ``status``
     - Clusterstatus. Einer der Werte ``GREEN`` / ``YELLOW`` / ``RED`` (Großbuchstaben). Auch bei einem ``GREEN``-Cluster ist der Wert ``YELLOW``, solange ein Index von |Fess| eine Schreibsperre trägt (siehe oben). ``UNAVAILABLE``, wenn die Suchmaschine nicht erreichbar ist.
   * - ``ping_status``
     - Ping-Statuscode (int). Der Wert ist ``1``, wenn der Cluster ``RED`` ist oder die Suchmaschine nicht erreichbar ist, und ``0`` andernfalls (``GREEN`` / ``YELLOW``).

Tabelle: engine-Felder

Der Clustername (``cluster_name``) wird nicht zurückgegeben, da dieser Endpunkt ohne Authentifizierung aufgerufen werden kann.

Anfrageparameter
~~~~~~~~~~~~~~~~

Es sind keine Anfrageparameter verfügbar.

Antwort
-------

Wenn der Cluster ``GREEN`` oder ``YELLOW`` ist (200), wird ein Erfolgs-Envelope mit ``engine`` zurückgegeben.

::

    {
      "response": {
        "status": 0,
        "engine": {
          "status": "GREEN",
          "ping_status": 0
        }
      }
    }

Wenn der Cluster ``RED`` ist (503), wird ein Fehler-Envelope zurückgegeben, und der Engine-Schnappschuss ist unter ``error.details.engine`` eingebettet.

::

    {
      "response": {
        "status": 9,
        "error": {
          "code": "service_unavailable",
          "message": "search engine cluster is red",
          "details": {
            "engine": {
              "status": "RED",
              "ping_status": 1
            }
          }
        }
      }
    }

Verwendungsbeispiel
===================

Beispielanfrage mit curl:

::

    curl "http://localhost:8080/api/v2/health"

Antwort und Fehlerantwort
=========================

Details zum Fehlermodell finden Sie unter :doc:`api-overview`. Folgende HTTP-Statuscodes können von diesem Endpunkt zurückgegeben werden:

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Antwortübersicht

   * - Statuscode
     - Beschreibung
   * - 200 OK
     - Cluster ist ``GREEN`` oder ``YELLOW`` und erreichbar. Der Erfolgs-Envelope enthält ``engine``.
   * - 400 Bad Request
     - Wenn ein Anfrageparameter angegeben wurde, der sich nicht dekodieren lässt (zum Beispiel ``?q=%ff``). ``error.code`` ist ``invalid_request``.
   * - 405 Method Not Allowed
     - Wenn die HTTP-Methode nicht erlaubt ist.
   * - 503 Service Unavailable
     - Cluster ist ``RED`` oder die Suchmaschine ist nicht erreichbar. Fehler-Envelope (``error.code: service_unavailable``) mit Engine-Schnappschuss unter ``error.details.engine``. Ein ``Retry-After: 5``-Header teilt dem Client mit, wie viele Sekunden er vor einem erneuten Versuch warten soll.

Tabelle: Antwortübersicht
