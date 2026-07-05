==========================
Stats API
==========================

Übersicht
=========

Die Stats API ist eine API zum Abrufen der Systemmetriken des Servers, auf dem |Fess| läuft.
Sie können statistische Informationen zu JVM, OS, Prozess, dem Suchmaschinen-Cluster (OpenSearch) und dem Dateisystem einsehen.

.. note::

   Diese API gibt keine Suchanalysedaten wie Suchanfragen oder Klicks zurück.
   Für die Suche und Verwaltung der Dokumente im Index siehe :doc:`api-admin-searchlist`.

Basis-URL
=========

::

    /api/admin/stats

Für den Zugriff auf diese API ist ein Access Token mit der Berechtigung ``Radmin-api`` erforderlich.
Informationen zur Authentifizierung finden Sie unter :doc:`api-admin-overview`.

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

.. note::

   Die Feldnamen der Objekte unter ``stats`` werden in snake_case ausgegeben (Kleinbuchstaben, durch Unterstriche getrennt, z. B. ``non_heap``).
   Felder, deren Wert ``null`` ist, werden aus der Antwort weggelassen.

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
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
              "non_heap": {
                "used": 134217728,
                "committed": 268435456,
                "max": 0,
                "percent": 0
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
              "swap_space": {"free": 0, "total": 0}
            },
            "cpu": {"percent": 12},
            "load_averages": [0.5, 0.4, 0.3]
          },
          "process": {
            "file_fescriptor": {"open": 256, "max": 65536},
            "cpu": {"percent": 5, "total": 123456},
            "virtual_memory": {"total": 4294967296}
          },
          "engine": {
            "cluster_name": "fess",
            "number_of_nodes": 1,
            "number_of_data_nodes": 1,
            "active_primary_shards": 10,
            "active_shards": 10,
            "active_shards_percent": 100.0,
            "relocating_shards": 0,
            "initializing_shards": 0,
            "unassigned_shards": 0,
            "delayed_unassigned_shards": 0,
            "number_of_pending_tasks": 0,
            "number_of_in_flight_fetch": 0,
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

Response-Felder (oberste Ebene)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Feld
     - Beschreibung
   * - ``version``
     - Die Produktversion von |Fess| (z. B. ``15.8.0``).
   * - ``status``
     - Ein Code, der das Verarbeitungsergebnis angibt. ``0`` bedeutet erfolgreiche Ausführung.
   * - ``stats``
     - Ein Objekt, das die Systemmetriken speichert. Es hat die fünf Schlüssel ``jvm`` / ``os`` / ``process`` / ``engine`` / ``fs``.

``jvm``: JVM-Statistiken
~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Feld
     - Beschreibung
   * - ``memory.heap.used``
     - Verwendeter Heap-Speicher (Bytes).
   * - ``memory.heap.committed``
     - Reservierter Heap-Speicher (Bytes).
   * - ``memory.heap.max``
     - Maximaler Heap-Speicher (Bytes).
   * - ``memory.heap.percent``
     - Heap-Speicherauslastung in Prozent (%).
   * - ``memory.non_heap.used``
     - Verwendeter Nicht-Heap-Speicher (Bytes).
   * - ``memory.non_heap.committed``
     - Reservierter Nicht-Heap-Speicher (Bytes).
   * - ``memory.non_heap.max``
     - Maximaler Nicht-Heap-Speicher (Bytes). In der aktuellen Implementierung ist dieser Wert nicht gesetzt und gibt stets ``0`` zurück.
   * - ``memory.non_heap.percent``
     - Nicht-Heap-Speicherauslastung in Prozent (%). In der aktuellen Implementierung ist dieser Wert nicht gesetzt und gibt stets ``0`` zurück.
   * - ``pools``
     - Array der Buffer-Pools. Jedes Element enthält ``key`` (Pool-Name), ``count`` (Anzahl der Puffer), ``used`` (verwendeter Speicher, Bytes) und ``capacity`` (Gesamtkapazität, Bytes).
   * - ``gc``
     - Array der Garbage Collectors. Jedes Element enthält ``key`` (Collector-Name), ``count`` (Anzahl der Durchläufe) und ``time`` (kumulierte Laufzeit in Millisekunden).
   * - ``threads.count``
     - Aktuelle Anzahl der Threads.
   * - ``threads.peak``
     - Maximale Anzahl der Threads.
   * - ``classes.loaded``
     - Anzahl der aktuell geladenen Klassen.
   * - ``classes.total_loaded``
     - Gesamtanzahl der seit dem JVM-Start geladenen Klassen.
   * - ``classes.unloaded``
     - Gesamtanzahl der entladenen Klassen.
   * - ``uptime``
     - JVM-Laufzeit (Millisekunden).

``os``: OS-Statistiken
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Feld
     - Beschreibung
   * - ``memory.physical.free``
     - Freier physischer Speicher (Bytes).
   * - ``memory.physical.total``
     - Gesamter physischer Speicher (Bytes).
   * - ``memory.swap_space.free``
     - Freier Auslagerungsspeicher (Bytes).
   * - ``memory.swap_space.total``
     - Gesamter Auslagerungsspeicher (Bytes).
   * - ``cpu.percent``
     - Systemweite CPU-Auslastung in Prozent (%).
   * - ``load_averages``
     - Array der Lastdurchschnittswerte (1, 5 und 15 Minuten). Werte, die nicht ermittelt werden können, können ``-1`` sein.

``process``: Prozess-Statistiken
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Feld
     - Beschreibung
   * - ``file_fescriptor.open``
     - Anzahl der aktuell geöffneten Dateideskriptoren.
   * - ``file_fescriptor.max``
     - Maximale Anzahl der öffenbaren Dateideskriptoren.
   * - ``cpu.percent``
     - CPU-Auslastung des Prozesses in Prozent (%).
   * - ``cpu.total``
     - Kumulierte vom Prozess verwendete CPU-Zeit (Millisekunden).
   * - ``virtual_memory.total``
     - Gesamte virtuelle Speichergröße des Prozesses (Bytes).

.. note::

   Der Schlüsselname ``process.file_fescriptor`` ist die snake_case-Umwandlung des Quellcode-Feldnamens
   ``fileFescriptor`` (der auf einer Falschschreibung von ``fileDescriptor`` beruht). Er entspricht der
   Implementierung und ist kein Tippfehler in diesem Dokument.

``engine``: Suchmaschinen-Cluster-Statistiken
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Zustandsinformationen des Suchmaschinen-Clusters (OpenSearch).

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Feld
     - Beschreibung
   * - ``cluster_name``
     - Cluster-Name.
   * - ``number_of_nodes``
     - Gesamtanzahl der Knoten im Cluster.
   * - ``number_of_data_nodes``
     - Anzahl der Datenknoten.
   * - ``active_primary_shards``
     - Anzahl der aktiven primären Shards.
   * - ``active_shards``
     - Anzahl der aktiven Shards.
   * - ``active_shards_percent``
     - Anteil der aktiven Shards in Prozent (%).
   * - ``relocating_shards``
     - Anzahl der verschobenen Shards.
   * - ``initializing_shards``
     - Anzahl der initialisierenden Shards.
   * - ``unassigned_shards``
     - Anzahl der nicht zugewiesenen Shards.
   * - ``delayed_unassigned_shards``
     - Anzahl der verzögert nicht zugewiesenen Shards.
   * - ``number_of_pending_tasks``
     - Anzahl der ausstehenden Aufgaben.
   * - ``number_of_in_flight_fetch``
     - Anzahl der laufenden Fetch-Operationen.
   * - ``status``
     - Cluster-Integritätsstatus (``green`` / ``yellow`` / ``red``).
   * - ``exception``
     - Eine Fehlermeldung, die nur bei einem Fehler enthalten ist, z. B. wenn der Cluster nicht erreichbar ist. In diesem Fall wird ``status`` zu ``red``.

``fs``: Dateisystem-Statistiken
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ein Array mit Statistiken für jede Wurzel (die über ``File.listRoots()`` ermittelten Wurzeln).

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Feld
     - Beschreibung
   * - ``path``
     - Absoluter Pfad der Wurzel.
   * - ``total``
     - Gesamtkapazität (Bytes).
   * - ``free``
     - Freie Kapazität (Bytes).
   * - ``usable``
     - Nutzbare Kapazität (Bytes).
   * - ``used``
     - Verwendete Kapazität (Bytes). Dies entspricht ``total`` minus ``usable``.
   * - ``percent``
     - Auslastung in Prozent (%).

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
