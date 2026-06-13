==========================
Stats API
==========================

Übersicht
=========

Die Stats API dient zum Abrufen der Systemmetriken des Servers, auf dem |Fess| läuft.
Sie können statistische Informationen zu JVM, OS, Prozess, dem Suchmaschinen-Cluster (OpenSearch) und dem Dateisystem einsehen.

.. note::

   Diese API gibt keine Suchanalysedaten wie Suchanfragen oder Klicks zurück.
   Für die Suche und Verwaltung der Dokumente im Index siehe :doc:`api-admin-searchlist`.

Basis-URL
=========

::

    /api/admin/stats

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
     - Systemstatistiken abrufen

Systemstatistiken abrufen
=========================

Request
-------

::

    GET /api/admin/stats

Dieser Endpunkt akzeptiert keine Query-Parameter.

Response
--------

Die Antwort enthält ``version`` (die Produktversion), ``status`` (das Verarbeitungsergebnis) sowie
das Objekt ``stats``, das die Systemmetriken speichert.
``stats`` hat die fünf Schlüssel ``jvm`` / ``os`` / ``process`` / ``engine`` / ``fs``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "stats": {
          "jvm": {
            "memory": {
              "heap": {
                "used": 536870912,
                "committed": 1073741824,
                "max": 2147483648,
                "percent": 25
              },
              "nonHeap": {
                "used": 134217728,
                "committed": 268435456
              }
            },
            "pools": [
              {"key": "mapped", "count": 1, "used": 4096, "capacity": 4096}
            ],
            "gc": [
              {"key": "young", "count": 12, "time": 345}
            ],
            "threads": {"count": 80, "peak": 95},
            "classes": {"loaded": 12000, "total_loaded": 12500, "unloaded": 500},
            "uptime": 3600000
          },
          "os": {
            "memory": {
              "physical": {"free": 2147483648, "total": 8589934592},
              "swapSpace": {"free": 0, "total": 0}
            },
            "cpu": {"percent": 12},
            "loadAverages": [0.5, 0.4, 0.3]
          },
          "process": {
            "fileFescriptor": {"open": 256, "max": 65536},
            "cpu": {"percent": 5, "total": 123456},
            "virtualMemory": {"total": 4294967296}
          },
          "engine": {
            "clusterName": "fess",
            "numberOfNodes": 1,
            "numberOfDataNodes": 1,
            "activePrimaryShards": 10,
            "activeShards": 10,
            "activeShardsPercent": 100.0,
            "relocatingShards": 0,
            "initializingShards": 0,
            "unassignedShards": 0,
            "delayedUnassignedShards": 0,
            "numberOfPendingTasks": 0,
            "numberOfInFlightFetch": 0,
            "status": "green"
          },
          "fs": [
            {
              "path": "/",
              "total": 107374182400,
              "free": 53687091200,
              "usable": 53687091200,
              "used": 53687091200,
              "percent": 50
            }
          ]
        }
      }
    }

Response-Felder
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Feld
     - Beschreibung
   * - ``jvm``
     - JVM-Statistik. Enthält ``memory`` (``heap`` / ``nonHeap``), ``pools`` (Buffer-Pools), ``gc`` (GC), ``threads``, ``classes`` und ``uptime`` (Millisekunden).
   * - ``os``
     - OS-Statistik. Enthält ``memory`` (``physical`` / ``swapSpace``), ``cpu`` und ``loadAverages`` (Array der Load Averages).
   * - ``process``
     - Prozess-Statistik. Enthält ``fileFescriptor`` (Anzahl offener/maximaler Dateideskriptoren), ``cpu`` und ``virtualMemory``.
   * - ``engine``
     - Zustand des Suchmaschinen-Clusters (OpenSearch). Enthält ``clusterName``, Anzahl der Knoten, Anzahl der Shards, ``status`` usw. Kann keine Verbindung zum Cluster hergestellt werden, wird ``status`` zu ``"red"`` und in ``exception`` ist eine Fehlermeldung enthalten.
   * - ``fs``
     - Array der Dateisystem-Statistiken. Enthält für jede Wurzel ``path``, ``total``, ``free``, ``usable``, ``used`` (Byte) und ``percent`` (Auslastung).

.. note::

   Der Schlüsselname ``process.fileFescriptor`` entspricht der Implementierung im Quellcode (es ist nicht die Schreibweise ``fileDescriptor``).

Verwendungsbeispiele
====================

Systemstatistiken abrufen
-------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN"

JVM-Heap-Auslastung prüfen
--------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq '.response.stats.jvm.memory.heap.percent'

Zustand des Suchmaschinen-Clusters prüfen
-----------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq '.response.stats.engine.status'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-systeminfo` - Systeminformationen API
- :doc:`api-admin-searchlist` - Dokumentsuche- und -verwaltungs-API
