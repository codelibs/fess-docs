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

Dieser Endpunkt hält die Envelope-Invariante ein: „``status >= 1`` ⇔ HTTP-Status ``>= 400``".

- Bei ``GREEN`` / ``YELLOW``: Gibt einen Erfolgs-Envelope (``status: 0``) mit ``engine`` zurück.
- Bei ``RED``: Gibt einen Fehler-Envelope (``status: 9``, ``error.code: service_unavailable``) zurück und bettet den Engine-Schnappschuss unter ``error.details.engine`` ein (damit Überwachungswerkzeuge die Cluster-Metadaten auswerten können).
- Wenn die Suchmaschine nicht erreichbar ist: Gibt wie bei ``RED`` einen Fehler-Envelope zurück (``error.code: service_unavailable``, ``error.message: search engine is not reachable``); ``error.details.engine`` enthält ``status: UNAVAILABLE`` und ``ping_status: 1``.

Die einzelnen Felder von ``engine`` sind wie folgt:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: engine-Felder

   * - ``status``
     - Clusterstatus. Einer der Werte ``GREEN`` / ``YELLOW`` / ``RED`` (Großbuchstaben). ``UNAVAILABLE``, wenn die Suchmaschine nicht erreichbar ist.
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
   * - 405 Method Not Allowed
     - Wenn die HTTP-Methode nicht erlaubt ist.
   * - 503 Service Unavailable
     - Cluster ist ``RED`` oder die Suchmaschine ist nicht erreichbar. Fehler-Envelope (``error.code: service_unavailable``) mit Engine-Schnappschuss unter ``error.details.engine``.

Tabelle: Antwortübersicht
