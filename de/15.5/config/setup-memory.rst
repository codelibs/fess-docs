============
Speicherkonfiguration
============

Übersicht
====

Java-Anwendungen erfordern die Konfiguration des maximalen Heap-Speichers pro Prozess.
Bei |Fess| werden Speichereinstellungen für die folgenden drei Komponenten separat konfiguriert.

- Fess-Webanwendung
- Crawler-Prozess
- OpenSearch

Durch angemessene Speicherkonfiguration können Leistungsverbesserungen und stabiler Betrieb erreicht werden.

Speicherkonfiguration der Fess-Webanwendung
======================================

Situationen, in denen Konfiguration erforderlich ist
----------------

Erwägen Sie die Anpassung der Speichergröße in folgenden Fällen:

- OutOfMemory-Fehler werden in ``fess.log`` aufgezeichnet
- Hohe Anzahl gleichzeitiger Zugriffe muss verarbeitet werden
- Verwaltungsoberfläche ist langsam oder läuft in einen Timeout

Die Standardspeichergröße ist für normale Nutzung ausreichend, aber in Umgebungen mit hoher Last ist eine Erhöhung erforderlich.

Konfiguration über Umgebungsvariablen
------------------

Setzen Sie die Umgebungsvariable ``FESS_HEAP_SIZE``.

::

    export FESS_HEAP_SIZE=2g

Einheiten:

- ``m``: Megabyte
- ``g``: Gigabyte

Bei RPM/DEB-Paketen
------------------------

Bei Installation über RPM-Paket bearbeiten Sie ``/etc/sysconfig/fess``.

::

    FESS_HEAP_SIZE=2g

Bei DEB-Paketen bearbeiten Sie ``/etc/default/fess``.

::

    FESS_HEAP_SIZE=2g

.. warning::
   Nach Änderung der Speichergröße muss der |Fess|-Dienst neu gestartet werden.

Empfohlene Speichergrößen
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Umgebung
     - Empfohlene Heap-Größe
     - Anmerkungen
   * - Entwicklungs-/Testumgebung
     - 512m–1g
     - Kleine Indizes
   * - Kleine Produktionsumgebung
     - 1g–2g
     - Zehntausende bis hunderttausende Dokumente
   * - Mittlere Produktionsumgebung
     - 2g–4g
     - Hunderttausende bis Millionen Dokumente
   * - Große Produktionsumgebung
     - 4g–8g
     - Mehrere Millionen Dokumente

Speicherkonfiguration des Crawlers
======================

Situationen, in denen Konfiguration erforderlich ist
----------------

In folgenden Fällen muss die Speichergröße des Crawlers erhöht werden:

- Bei Erhöhung der Anzahl paralleler Crawls
- Beim Crawlen großer Dateien
- Bei Auftreten von OutOfMemory-Fehlern während der Crawler-Ausführung

Konfigurationsmethode
--------

Bearbeiten Sie ``app/WEB-INF/classes/fess_config.properties`` oder ``/etc/fess/fess_config.properties``.

::

    jvm.crawler.options=-Xmx512m

Beispiel für Änderung auf 1 GB:

::

    jvm.crawler.options=-Xmx1g

.. note::
   Diese Einstellung wird pro Crawler-Prozess (pro Scheduler-Job) angewendet.
   Bei gleichzeitiger Ausführung mehrerer Crawler-Jobs wird für jeden Job der angegebene Speicher verwendet.

Empfohlene Einstellungen
--------

- **Normales Web-Crawling**: 512m–1g
- **Massiv paralleles Crawling**: 1g–2g
- **Crawlen großer Dateien**: 2g–4g

Detaillierte JVM-Optionen
------------------

Detaillierte JVM-Optionen für den Crawler können über ``jvm.crawler.options`` konfiguriert werden.
Die Standardkonfiguration umfasst folgende Optimierungen:

**Hauptoptionen:**

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Option
     - Beschreibung
   * - ``-Xms128m -Xmx512m``
     - Initiale und maximale Heap-Größe
   * - ``-XX:MaxMetaspaceSize=128m``
     - Maximale Metaspace-Größe
   * - ``-XX:+UseG1GC``
     - Verwendung des G1-Garbage-Collectors
   * - ``-XX:MaxGCPauseMillis=60000``
     - Ziel für GC-Pausenzeit (60 Sekunden)
   * - ``-XX:-HeapDumpOnOutOfMemoryError``
     - Deaktivierung von Heap-Dumps bei OutOfMemory

Speicherkonfiguration von OpenSearch
=======================

Wichtige Überlegungen
--------------

Bei OpenSearch müssen folgende zwei Punkte für die Speicherkonfiguration berücksichtigt werden:

1. **Java-Heap-Speicher**: Verwendet vom OpenSearch-Prozess
2. **OS-Dateisystem-Cache**: Wichtig für Such-Performance

.. warning::
   Wenn der Java-Heap-Speicher zu groß eingestellt wird, verringert sich
   der für den OS-Dateisystem-Cache verfügbare Speicher,
   was die Such-Performance beeinträchtigt.

Konfigurationsmethode
--------

Linux-Umgebungen
~~~~~~~~~

Der Heap-Speicher von OpenSearch wird über Umgebungsvariablen oder die OpenSearch-Konfigurationsdatei angegeben.

Konfiguration über Umgebungsvariable:

::

    export OPENSEARCH_HEAP_SIZE=2g

Oder bearbeiten Sie ``config/jvm.options``:

::

    -Xms2g
    -Xmx2g

.. note::
   Es wird empfohlen, die minimale Heap-Größe (``-Xms``) und die maximale Heap-Größe (``-Xmx``) auf denselben Wert zu setzen.

Windows-Umgebungen
~~~~~~~~~~~

Bearbeiten Sie die Datei ``config\jvm.options``.

::

    -Xms2g
    -Xmx2g

Empfohlene Speichergrößen
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Indexgröße
     - Empfohlene Heap-Größe
     - Empfohlener Gesamtspeicher
   * - ~10 GB
     - 2g
     - 4 GB oder mehr
   * - 10 GB–50 GB
     - 4g
     - 8 GB oder mehr
   * - 50 GB–100 GB
     - 8g
     - 16 GB oder mehr
   * - Über 100 GB
     - 16g–31g
     - 32 GB oder mehr

.. warning::
   Der Heap-Speicher von OpenSearch sollte 32 GB nicht überschreiten.
   Bei über 32 GB wird Compressed OOP deaktiviert und die Speichereffizienz nimmt ab.

Best Practices
------------------

1. **50% des physischen Speichers dem Heap zuweisen**

   Weisen Sie etwa 50% des physischen Speichers des Servers dem OpenSearch-Heap zu.
   Der Rest wird für OS und Dateisystem-Cache verwendet.

2. **Maximum von 31 GB**

   Die Heap-Größe sollte maximal 31 GB betragen. Bei höherem Bedarf sollten zusätzliche Knoten hinzugefügt werden.

3. **Überprüfung in Produktionsumgebungen**

   Konsultieren Sie die offizielle OpenSearch-Dokumentation für optimale umgebungsspezifische Einstellungen.

Speicherkonfiguration für Vorschlag- und Thumbnail-Verarbeitung
======================================

Vorschlags-Generierungsprozess
----------------------

Die Speicherkonfiguration für die Vorschlags-Generierung wird über ``jvm.suggest.options`` konfiguriert.

::

    jvm.suggest.options=-Xmx256m

Standardmäßig werden folgende Einstellungen verwendet:

- Initialer Heap: 128 MB
- Maximaler Heap: 256 MB
- Maximaler Metaspace: 128 MB

Thumbnail-Generierungsprozess
----------------------

Die Speicherkonfiguration für die Thumbnail-Generierung wird über ``jvm.thumbnail.options`` konfiguriert.

::

    jvm.thumbnail.options=-Xmx256m

Standardmäßig werden folgende Einstellungen verwendet:

- Initialer Heap: 128 MB
- Maximaler Heap: 256 MB
- Maximaler Metaspace: 128 MB

.. note::
   Bei der Verarbeitung großer Bilder für die Thumbnail-Generierung muss der Speicher erhöht werden.

Speicherüberwachung und -Tuning
========================

Überprüfung der Speichernutzung
--------------------

Speichernutzung von Fess
~~~~~~~~~~~~~~~~~~~~~

Kann in der Verwaltungsoberfläche unter „Systeminformationen" überprüft werden.

Oder verwenden Sie JVM-Überwachungstools:

::

    jps -l  # Fess-Prozesse anzeigen
    jstat -gcutil <PID> 1000  # GC-Statistiken jede Sekunde anzeigen

Speichernutzung von OpenSearch
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    curl -X GET "localhost:9201/_nodes/stats/jvm?pretty"
    curl -X GET "localhost:9201/_cat/nodes?v&h=heap.percent,ram.percent"

Anzeichen von Speichermangel
----------------

Bei folgenden Symptomen besteht möglicherweise Speichermangel.

**Fess-Webanwendung:**

- Langsame Antwortzeiten
- ``OutOfMemoryError`` in Protokollen aufgezeichnet
- Prozess beendet sich unerwartet

**Crawler:**

- Crawling stoppt mittendrin
- ``OutOfMemoryError`` in ``fess_crawler.log`` aufgezeichnet
- Crawlen großer Dateien schlägt fehl

**OpenSearch:**

- Langsame Suche
- Langsame Indexerstellung
- ``circuit_breaker_exception``-Fehler treten auf

Tuning-Verfahren
----------------

1. **Aktuelle Speichernutzung überprüfen**

   Überwachen Sie die Speichernutzung jeder Komponente.

2. **Engpass identifizieren**

   Identifizieren Sie, welche Komponente Speichermangel hat.

3. **Schrittweise erhöhen**

   Erhöhen Sie nicht auf einmal stark, sondern in Schritten von 25–50% und überprüfen Sie die Wirkung.

4. **Gesamtsystembalance berücksichtigen**

   Stellen Sie sicher, dass die Gesamtsumme des Speichers aller Komponenten den physischen Speicher nicht überschreitet.

5. **Kontinuierliche Überwachung**

   Überwachen Sie kontinuierlich die Speichernutzung und passen Sie bei Bedarf an.

Maßnahmen gegen Speicherlecks
----------------

Bei Verdacht auf Speicherlecks:

1. **Heap-Dump erstellen**

::

    jmap -dump:format=b,file=heap.bin <PID>

2. **Heap-Dump analysieren**

   Analysieren Sie mit Tools wie Eclipse Memory Analyzer (MAT).

3. **Problem melden**

   Wenn Sie ein Speicherleck entdecken, melden Sie es bitte über GitHub Issues.

Fehlersuche
======================

OutOfMemoryError tritt auf
---------------------------

**Fess-Webanwendung:**

1. Erhöhen Sie ``FESS_HEAP_SIZE``.
2. Beschränken Sie die Anzahl gleichzeitiger Zugriffe.
3. Senken Sie den Log-Level, um Speichernutzung durch Protokollierung zu reduzieren.

**Crawler:**

1. Erhöhen Sie ``-Xmx`` in ``jvm.crawler.options``.
2. Reduzieren Sie die Anzahl paralleler Crawls.
3. Passen Sie die Crawler-Konfiguration an, um große Dateien auszuschließen.

**OpenSearch:**

1. Erhöhen Sie die Heap-Größe (bis maximal 31 GB).
2. Überprüfen Sie die Anzahl der Index-Shards.
3. Überprüfen Sie die Komplexität der Abfragen.

Lange Pausenzeiten durch GC
----------------------

1. Passen Sie die G1GC-Einstellungen an.
2. Konfigurieren Sie die Heap-Größe angemessen (sowohl zu groß als auch zu klein führt zu häufigen GCs).
3. Erwägen Sie ein Update auf eine neuere Java-Version.

Leistung verbessert sich nicht trotz Speicherkonfiguration
------------------------------

1. Überprüfen Sie andere Ressourcen wie CPU, Disk-I/O, Netzwerk.
2. Führen Sie eine Indexoptimierung durch.
3. Überprüfen Sie Abfragen und Crawler-Konfigurationen.

Referenzinformationen
========

- :doc:`setup-port-network` - Port- und Netzwerkkonfiguration
- :doc:`crawler-advanced` - Erweiterte Crawler-Konfiguration
- :doc:`admin-logging` - Protokollkonfiguration
- `OpenSearch Memory Settings <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/index/#important-settings>`_
- `Java GC Tuning <https://docs.oracle.com/en/java/javase/11/gctuning/>`_
