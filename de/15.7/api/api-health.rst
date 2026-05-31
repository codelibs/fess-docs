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
Der HTTP-Statuscode ist 200, wenn der Clusterstatus ``green`` oder ``yellow`` ist, und 503 bei ``red``.

Dieser Endpunkt hält die Envelope-Invariante ein: „``status >= 1`` ⇔ HTTP-Status ``>= 400``".

- Bei ``green`` / ``yellow``: Gibt einen Erfolgs-Envelope (``status: 0``) mit ``engine`` zurück.
- Bei ``red``: Gibt einen Fehler-Envelope (``status: 9``, ``error.code: service_unavailable``) zurück und bettet den Engine-Schnappschuss unter ``error.details.engine`` ein (damit Überwachungswerkzeuge die Cluster-Metadaten auswerten können).

Die einzelnen Felder von ``engine`` sind wie folgt:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: engine-Felder

   * - ``cluster_name``
     - Clustername (str).
   * - ``status``
     - Clusterstatus. Einer der Werte ``green`` / ``yellow`` / ``red``.
   * - ``ping_status``
     - Ping-Statuscode (int).

Tabelle: engine-Felder

Anfrageparameter
~~~~~~~~~~~~~~~~

Es sind keine Anfrageparameter verfügbar.

Antwort
-------

Wenn der Cluster ``green`` oder ``yellow`` ist (200), wird ein Erfolgs-Envelope mit ``engine`` zurückgegeben.

::

    {
      "response": {
        "status": 0,
        "engine": {
          "cluster_name": "fess-es",
          "status": "green",
          "ping_status": 0
        }
      }
    }

Wenn der Cluster ``red`` ist (503), wird ein Fehler-Envelope zurückgegeben, und der Engine-Schnappschuss ist unter ``error.details.engine`` eingebettet.

::

    {
      "response": {
        "status": 9,
        "error": {
          "code": "service_unavailable",
          "message": "Cluster is unavailable.",
          "details": {
            "engine": {
              "cluster_name": "fess-es",
              "status": "red",
              "ping_status": 2
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
     - Cluster ist ``green`` oder ``yellow`` und erreichbar. Der Erfolgs-Envelope enthält ``engine``.
   * - 405 Method Not Allowed
     - Wenn die HTTP-Methode nicht erlaubt ist.
   * - 503 Service Unavailable
     - Cluster ist ``red``. Fehler-Envelope (``error.code: service_unavailable``) mit Engine-Schnappschuss unter ``error.details.engine``.

Tabelle: Antwortübersicht
