============================================
Fess für mehr Dokumente und Nutzer skalieren
============================================

Einleitung
==========

Wenn die Zahl der Dokumente und Nutzer wächst, treten Probleme auf: „Der Crawl ist bis zum Morgen nicht fertig“, „Die Suche ist langsam geworden“, „Fess ist mit einem OutOfMemoryError stehen geblieben“.
Sofort weitere Server hinzuzufügen, löst diese Probleme nicht unbedingt.
Fess läuft in mehreren JVM-Prozessen, und häufig ist es nur einer davon, dem Ressourcen fehlen.

Dieser Artikel bezieht sich auf Fess 15.9 und erklärt die Skalierung in der folgenden Reihenfolge.

1. Ermitteln, welchem Prozess was fehlt
2. Speicher und Crawl-Parallelität auf einem einzelnen Server anpassen
3. OpenSearch auf einen eigenen Server auslagern
4. OpenSearch zu einem Cluster aus drei Knoten ausbauen
5. Mehrere Fess-Server betreiben

Der Aufbau der Überwachung (Health-Checks, Logs, Benachrichtigungen) und Backups werden in :doc:`guide-10` behandelt.

Die Prozesse, aus denen Fess besteht
====================================

Auch wenn Fess auf einem einzelnen Server läuft, sind die Speichereinstellungen wie folgt aufgeteilt.

.. list-table::
   :header-rows: 1
   :widths: 20 30 25 25

   * - Prozess
     - Aufgabe
     - Standard-Heap
     - Wo eingestellt
   * - Fess-Server
     - Suchseite, Administrationsoberfläche, API, Scheduler
     - ZIP-Paket: mindestens 256m, höchstens 2g; RPM/DEB-Pakete und Docker-Image: 512m
     - Umgebungsvariable ``FESS_HEAP_SIZE``
   * - Crawler
     - Eigene JVM, die für jeden Crawl-Job gestartet wird
     - Höchstens 512m
     - ``jvm.crawler.options`` in ``fess_config.properties``
   * - Suggest-Erzeugung, Thumbnail-Erzeugung
     - Eigene JVM, die für jeden Job gestartet wird
     - Höchstens 256m
     - ``jvm.suggest.options``, ``jvm.thumbnail.options``
   * - OpenSearch
     - Speichert den Index und führt Suchen aus
     - 1g in ``compose-opensearch3.yaml`` von docker-fess
     - ``OPENSEARCH_JAVA_OPTS`` oder ``config/jvm.options``

Auch die Chunk-Verarbeitung der semantischen Suche hat eine eigene JVM (``jvm.chunk.options``, höchstens 1g); sie wird in :doc:`guide-18` behandelt.

Erscheint in ``fess-crawler.log`` ein OutOfMemoryError, fehlt der JVM des Crawlers Speicher.
In diesem Fall bringt es nichts, ``FESS_HEAP_SIZE`` zu erhöhen.

Ermitteln, was fehlt
====================

Prüfen Sie je nach Symptom die folgenden Stellen.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Symptom
     - Wo prüfen
   * - Die Suche ist langsam
     - Sehen Sie sich auf dem Tab [Leistung] unter [Systeminformationen] > [Suchprotokoll] die Antwortzeiten p95 und p99 sowie die langsamen Suchbegriffe an. Unterscheiden Sie, ob nur bestimmte Suchbegriffe oder alle Suchen langsam sind.
   * - Crawls werden nicht fertig
     - Verfolgen Sie unter [Systeminformationen] > [Jobprotokoll], wie sich Start- und Endzeiten der Crawl-Jobs entwickeln. Erscheint in ``fess-crawler.log`` fortlaufend ``Cpu Load XX% is greater than 50%``, wird der Crawl durch die weiter unten beschriebene Laststeuerung ausgebremst.
   * - Der Crawler bricht ab
     - Suchen Sie in ``fess-crawler.log`` nach ``OutOfMemoryError``.
   * - Der Fess-Server bricht ab oder die Administrationsoberfläche ist träge
     - Suchen Sie in ``fess.log`` nach ``OutOfMemoryError`` und prüfen Sie ``response.stats.jvm.memory.heap.percent`` in ``/api/admin/stats``.
   * - OpenSearch ist träge
     - Prüfen Sie ``response.stats.engine.status`` in ``/api/admin/stats`` und die Heap-Auslastung in ``_cat/nodes`` von OpenSearch. Eine ``circuit_breaker_exception`` deutet auf zu wenig Heap hin.

``/api/admin/stats`` liefert den Zustand von JVM und Betriebssystem des Fess-Servers, der die Anfrage erhalten hat, sowie den Zustand des OpenSearch-Clusters.
Die JVM des Crawlers und der Heap der einzelnen OpenSearch-Knoten sind nicht enthalten.
Für den Aufruf ist ein Zugriffstoken mit der Berechtigung ``admin-api`` erforderlich.
Wie Sie es erstellen, steht in `Admin API Übersicht <https://fess.codelibs.org/de/stable/api/admin/api-admin-overview.html>`__, die Felder der Antwort in `Stats API <https://fess.codelibs.org/de/stable/api/admin/api-admin-stats.html>`__.

Den Heap der einzelnen OpenSearch-Knoten fragen Sie direkt bei OpenSearch ab.

::

    $ curl -s 'http://localhost:9200/_cat/nodes?v&h=name,heap.max,heap.percent,ram.percent,cpu'

Die Anzahl der Dokumente und die Größe des Index können Sie mit dem folgenden Befehl prüfen.
``fess.search`` ist der Alias des Index, der für die Suche verwendet wird.

::

    $ curl -s 'http://localhost:9200/_cat/indices/fess.search?v&h=index,docs.count,pri.store.size,store.size'

Anpassungen auf einem einzelnen Server
======================================

Den Heap des Fess-Servers ändern
--------------------------------

Bei Docker fügen Sie ``FESS_HEAP_SIZE`` zu ``environment`` von ``fess01`` in ``compose.yaml`` hinzu.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "FESS_DICTIONARY_PATH=${FESS_DICTIONARY_PATH:-/usr/share/opensearch/config/dictionary/}"
          - "FESS_HEAP_SIZE=2g"

Wenn Sie ``environment`` oder ``volumes`` von ``fess01`` in ``compose.yaml`` ändern und ``docker compose ... up -d`` ausführen, wird der Container ``fess01`` neu erstellt.
Einstellungen, die Sie unter [System] > [Allgemein] geändert haben, liegen in ``system.properties`` im Container und gehen bei der Neuerstellung verloren.
Das gilt ebenso, wenn Sie in anderen Schritten dieses Artikels ``compose.yaml`` ändern.
Erstellen Sie vorher ein Backup, wie in :doc:`guide-10` beschrieben.

Beim RPM-Paket ändern Sie ``FESS_HEAP_SIZE=512m`` in ``/etc/sysconfig/fess``, beim DEB-Paket in ``/etc/default/fess``, und starten Fess anschließend neu.
Beim ZIP-Paket exportieren Sie ``FESS_HEAP_SIZE`` in der Umgebung, aus der Fess gestartet wird.

Ob die Änderung wirksam ist, prüfen Sie anhand der Argumente der laufenden Prozesse.
Bei Docker sieht das so aus:

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml exec -T fess01 sh -c 'cat /proc/[0-9]*/cmdline 2>/dev/null' | tr '\0' '\n' | grep -e '^-Xmx' -e 'FessBoot' -e 'exec.Crawler'
    -Xmx2g
    org.codelibs.fess.FessBoot

Die Zeile nach ``-Xmx`` zeigt die Art des Prozesses.
``FessBoot`` ist der Fess-Server, ``exec.Crawler`` der Crawler.
Bei den RPM/DEB-Paketen und dem ZIP-Paket führen Sie den Befehl innerhalb von ``sh -c`` und alles danach direkt auf dem Fess-Server aus.

Den Heap des Crawlers ändern
----------------------------

``jvm.crawler.options`` ist ein einzelner Wert, der JVM-Optionen durch ``\n`` getrennt aufführt.
Da der gesamte Wert ersetzt wird, entfernt ein Eintrag, der nur ``-Xmx1g`` enthält, sämtliche Standardoptionen wie G1GC.
Behalten Sie den Standardwert bei und ändern Sie nur die Zeile ``-Xmx512m``.

::

    -Xms128m\n\
    -Xmx1g\n\

Die Konfigurationsdatei liegt bei den RPM/DEB-Paketen unter ``/etc/fess/fess_config.properties``, beim ZIP-Paket unter ``app/WEB-INF/classes/fess_config.properties``.
Bei Docker kopieren Sie ``fess_config.properties`` aus dem Image auf Ihren Rechner, bearbeiten die Datei und mounten sie im Container unter ``/opt/fess/fess_config.properties``.
``/opt/fess`` wird vorrangig vor ``/etc/fess`` gelesen.
Da sich dieser Wert über mehrere Zeilen erstreckt, eignet er sich nicht für die Angabe mit ``-Dfess.config.`` in ``FESS_JAVA_OPTS``.
Das Vorgehen finden Sie unter „Anwendung von Konfigurationsdateien“ in `Installation mit Docker (Detailliert) <https://fess.codelibs.org/de/stable/install/install-docker.html>`__.

Prüfen Sie nach dem Neustart von Fess unter [Systeminformationen] > [Konfigurationsinformationen] in „App-Eigenschaften“, dass ``jvm.crawler.options`` den Eintrag ``-Xmx1g`` enthält.
Die Änderung wirkt ab dem nächsten gestarteten Crawler.
Wenn Sie während eines laufenden Crawls den Befehl aus dem vorigen Abschnitt ausführen, erscheint ``-Xmx1g`` in der Zeile vor ``org.codelibs.fess.exec.Crawler``.

Pro Crawl-Job wird eine Crawler-JVM gestartet.
Der Job „Default Crawler“ verarbeitet alle Crawl-Konfigurationen in einem einzigen Crawler.
Wenn Sie auf der Detailseite einer Crawl-Konfiguration mit [Neuen Job erstellen] für jede Konfiguration einen eigenen Job anlegen, startet jeder als separater Crawler und belegt jeweils Speicher bis zu seinem ``-Xmx``.
Um die Zahl gleichzeitig laufender Crawler zu begrenzen, verwenden Sie ``job.max.crawler.processes`` in ``fess_config.properties`` (der Standardwert ``0`` bedeutet unbegrenzt).
Ein Crawl-Job, der über diese Grenze hinaus gestartet wird, wartet nicht, bis er an der Reihe ist, sondern endet mit einem Fehler.

Für die JVMs der Suggest-Erzeugung und der Thumbnail-Erzeugung ändern Sie auf dieselbe Weise die Zeile ``-Xmx256m`` in ``jvm.suggest.options`` und ``jvm.thumbnail.options``.

Den Heap von OpenSearch ändern
------------------------------

In docker-fess enthält ``search01`` in ``compose-opensearch3.yaml`` die folgende Zeile.

::

    - "OPENSEARCH_JAVA_OPTS=-Xms1g -Xmx1g"

Setzen Sie beide Werte auf denselben neuen Wert.
Bei einem aus ZIP oder RPM installierten OpenSearch ändern Sie ``-Xms`` und ``-Xmx`` in ``config/jvm.options`` und starten OpenSearch neu.

Als Richtwert gilt als Obergrenze höchstens die Hälfte des physischen Speichers und weniger als 32GB.
Der übrige Speicher dient dem Betriebssystem als Dateicache und trägt zur Suchgeschwindigkeit bei; weisen Sie dem Heap daher nicht zu viel zu.
Ab 32GB werden die Compressed OOPs der JVM deaktiviert, und die Effizienz sinkt sogar.
Wird mehr benötigt, fügen Sie Knoten hinzu.

Richtwerte für das Verhältnis von Indexgröße und Heap finden Sie in `Speicherkonfiguration <https://fess.codelibs.org/de/stable/config/setup-memory.html>`__.
Beginnen Sie mit diesen Richtwerten und passen Sie an, während Sie die Heap-Auslastung in ``_cat/nodes`` (siehe oben) und die Antwortzeiten der Suche beobachten.

Laufen Fess und OpenSearch auf demselben Server, muss die Summe der Heaps von Fess-Server, Crawler und OpenSearch in den physischen Speicher passen.

Die Crawl-Parallelität ändern
-----------------------------

Die Crawl-Geschwindigkeit wird von den folgenden drei Einstellungen bestimmt.

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Einstellung
     - Standardwert
     - Ort
   * - Anzahl der Threads
     - Web 1, Dateisystem 5
     - Jede Crawl-Konfiguration ([Crawler] > [Web], [Dateisystem])
   * - Intervall
     - Web 10000 ms, Dateisystem 1000 ms
     - Wie oben. Die Zeit, die jeder Thread nach jedem Abruf einer URL wartet
   * - Gleichzeitige Crawler-Konfiguration
     - 5
     - [System] > [Allgemein]. Die Anzahl der Crawl-Konfigurationen, die ein Crawler gleichzeitig verarbeitet

Mehr Threads beschleunigen den Abruf für die betreffende Crawl-Konfiguration, erhöhen aber auch den Speicherverbrauch des Crawlers und die Last auf den gecrawlten Servern.
Wenn Sie externe Websites oder produktiv genutzte Server crawlen, wählen Sie das Intervall nicht zu kurz.

Auf einem einzelnen Server leicht übersehen wird ``adaptive.load.control`` in ``fess_config.properties`` (Standardwert ``50``).
Solange die CPU-Auslastung des Servers, auf dem Fess läuft, bei diesem Wert oder darüber liegt, warten die Threads für Crawling und Indexierung.
Nutzt OpenSearch auf demselben Server die CPU für Schreibvorgänge in den Index oder für Suchen, kann der Crawl nahezu zum Stillstand kommen.
In diesem Fall erscheint in ``fess-crawler.log`` die Meldung ``Cpu Load XX% is greater than 50%``.
Sie können den Wert erhöhen; fehlt jedoch dauerhaft CPU, ist die eigentliche Lösung, OpenSearch wie im nächsten Abschnitt beschrieben auf einen eigenen Server auszulagern.
Einzelheiten finden Sie in `Laststeuerung-Konfiguration <https://fess.codelibs.org/de/stable/config/load-control.html>`__.

OpenSearch auf einen eigenen Server auslagern
=============================================

Wenn OpenSearch auf einem eigenen Server läuft, konkurrieren Crawling und Suche nicht mehr um CPU, Speicher und Festplatten-I/O.

Was OpenSearch benötigt
-----------------------

Das von Fess genutzte OpenSearch benötigt die folgenden zwei Dinge.

- Die vier Plugins für Fess (``opensearch-analysis-fess``, ``opensearch-analysis-extension``, ``opensearch-minhash``, ``opensearch-configsync``). Ihre Version muss zu OpenSearch passen (Fess 15.9 verwendet OpenSearch 3.9.0)
- ``configsync.config_path`` in ``opensearch.yml``. Geben Sie als absoluten Pfad ein Verzeichnis für Wörterbuchdateien unterhalb des OpenSearch-Konfigurationsverzeichnisses an

Die Installationsbefehle finden Sie in `Installation unter Linux (Detaillierte Anleitung) <https://fess.codelibs.org/de/stable/install/install-linux.html>`__.
Das Image ``ghcr.io/codelibs/fess-opensearch`` von docker-fess enthält all dies bereits.

Läuft OpenSearch auf einem eigenen Server, ist Port 9200 im Netzwerk erreichbar.
Betreiben Sie es in der Produktion nicht mit deaktiviertem Security-Plugin.
Zur Konfiguration siehe :doc:`guide-15` und `Sicherheitseinstellungen <https://fess.codelibs.org/de/stable/install/security.html>`__.

Was in Fess einzustellen ist
----------------------------

In Fess geben Sie das Verbindungsziel und den Ort der Wörterbücher mit zwei Umgebungsvariablen an.

- ``SEARCH_ENGINE_HTTP_URL`` : die URL von OpenSearch
- ``FESS_DICTIONARY_PATH`` : derselbe Pfad wie ``configsync.config_path`` auf der OpenSearch-Seite

``FESS_DICTIONARY_PATH`` ist ein Pfad auf dem OpenSearch-Server.
Fess schreibt Wörterbuchdateien über das Plugin ``configsync``, daher muss der Fess-Server dieses Verzeichnis nicht mounten.
Ist die Variable nicht gesetzt, kann Fess seine Indizes nicht anlegen und startet nicht.

Eingestellt wird dies beim RPM-Paket in ``/etc/sysconfig/fess``, beim DEB-Paket in ``/etc/default/fess`` und beim ZIP-Paket in ``bin/fess.in.sh``.
Bei Docker verwenden Sie ``compose-opensearch3.yaml`` nicht, sondern geben die Werte in ``environment`` von ``fess01`` in ``compose.yaml`` an.
In v15.9.0 hat ``fess01`` in ``compose.yaml`` ein ``depends_on``, das auf ``search01`` wartet; eine Konfiguration ohne ``search01`` startet daher nicht und meldet den Fehler ``service "fess01" depends on undefined service "search01"``.
Löschen Sie die drei Zeilen von ``depends_on`` bis ``condition: service_healthy``.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://opensearch1.example.com:9200"
          - "FESS_DICTIONARY_PATH=/etc/opensearch/dictionary/"

In diesem Fall führen Sie alle folgenden ``docker compose``-Befehle nur mit ``-f compose.yaml`` aus.

Beim ZIP-Paket können Sie vor dem Start von Fess mit ``bin/fess-setup check`` die Verbindung, die vier Plugins und die Antwort von ``configsync`` prüfen.

::

    $ bin/fess-setup check --url http://opensearch1.example.com:9200

Durch einen Wechsel des Verbindungsziels werden vorhandene Indizes nicht in das neue OpenSearch übertragen.
Um vorhandene Dokumente zu übernehmen, migrieren Sie sie mit Snapshots („Datenmigration“ in `Index-Verwaltung <https://fess.codelibs.org/de/stable/config/admin-index-backup.html>`__).
Genügt ein erneutes Crawlen, ist es einfacher, sich mit einem leeren OpenSearch zu verbinden und neu zu crawlen.

OpenSearch zu einem Cluster aus drei Knoten ausbauen
====================================================

Solange OpenSearch auf einem einzigen Server läuft, steht die Suche still, sobald dieser Server ausfällt.
Wird Redundanz benötigt, bauen Sie OpenSearch zu einem Cluster aus.

Knotenaufbau
------------

Für die Wahl des Knotens, der den Cluster verwaltet (Cluster Manager), ist die Zustimmung einer Mehrheit erforderlich.
Gibt es nur einen oder zwei Knoten, die Cluster Manager werden können, ist nach dem Ausfall eines einzigen Knotens keine Wahl mehr möglich.
Stellen Sie daher drei Knoten bereit, die Cluster Manager werden können.
Der kleinste Aufbau ist einer, in dem alle drei auch Daten halten.

Das folgende Beispiel zeigt die clusterbezogenen Einstellungen in ``opensearch.yml`` jedes Knotens (``node.name`` ändern Sie für jeden Knoten).
Netzwerkeinstellungen wie ``network.host`` sowie Sicherheitseinstellungen ergänzen Sie passend zu Ihrer Umgebung.

.. code-block:: yaml

    cluster.name: fess-search
    node.name: search01
    node.roles: [ cluster_manager, data, ingest ]
    discovery.seed_hosts: [ "search01", "search02", "search03" ]
    cluster.initial_cluster_manager_nodes: [ "search01", "search02", "search03" ]
    configsync.config_path: /etc/opensearch/dictionary/

Installieren Sie die vier Plugins für Fess auf allen drei Knoten in derselben Version.
Verwenden Sie auch für ``configsync.config_path`` auf allen drei Knoten denselben Pfad.
Der Grund: Fess schreibt einen einzigen Wert von ``FESS_DICTIONARY_PATH`` in die Indexeinstellungen, und jeder Knoten liest die Wörterbücher unter diesem Pfad.

``compose/snapshot/compose-cluster.yaml`` von docker-fess enthält ein Beispiel für den Aufbau mehrerer Knoten mit Docker.
Diese Datei ist für die Kombination mit einer Entwicklungsversion des Fess-Images gedacht; nutzen Sie sie als Vorlage dafür, wie die Umgebungsvariablen von OpenSearch geschrieben werden.

Verbindung von Fess aus
-----------------------

Geben Sie in ``SEARCH_ENGINE_HTTP_URL`` die URLs der Knoten durch Kommas getrennt an.
Auch wenn einzelne Knoten ausgefallen sind, verbindet sich Fess mit den übrigen.

::

    SEARCH_ENGINE_HTTP_URL=http://search01:9200,http://search02:9200,http://search03:9200

Shards und Replikate
--------------------

Fess legt den Index für Dokumente mit ``index.number_of_shards`` aus ``fess_config.properties`` (Standardwert ``5``, die Anzahl der primären Shards) und ``index.auto_expand_replicas`` (Standardwert ``0-1``, passt die Replikate je nach Zahl der Datenknoten automatisch zwischen 0 und 1 an) an.
Wegen des Standardwerts ``0-1`` wird, sobald es zwei oder mehr Datenknoten gibt, für jeden Shard ein Replikat erstellt, ohne dass Sie Einstellungen in Fess ändern müssen.
Wechselt der Clusterstatus auf ``green``, sind alle Replikate zugewiesen.

Die Zahl der Shards wird beim Anlegen des Index festgelegt; eine spätere Änderung von ``index.number_of_shards`` wirkt sich nicht auf den vorhandenen Index aus.
Um sie zu ändern, verwenden Sie „Neuindizierung“ unter [Systeminformationen] > [Wartung].
Wenn Sie „Anzahl der Shards“ und „Replikate automatisch erweitern“ angeben, „Aliase ersetzen“ aktivieren und starten, legt Fess einen neuen Index an, kopiert die Dokumente und verlegt die Aliase ``fess.search`` und ``fess.update`` auf den neuen Index.

Bei der Neuindizierung ist Folgendes zu beachten.

- Die Dokumente werden aus dem Index kopiert, auf den ``fess.update`` zum Startzeitpunkt zeigt. Führen Sie sie zu einer Zeit aus, in der kein Crawl läuft
- Der alte Index wird nicht automatisch gelöscht. Auf der Festplatte muss Platz für den alten und den neuen Index zugleich sein

Die Elemente des Bildschirms finden Sie unter `Wartung <https://fess.codelibs.org/de/stable/admin/maintenance-guide.html>`__.

Den Cluster prüfen
------------------

::

    $ curl -s 'http://search01:9200/_cat/nodes?v&h=name,node.role,cluster_manager,heap.percent'
    $ curl -s 'http://search01:9200/_cluster/health?pretty'

Werden drei Knoten angezeigt und ist ``status`` gleich ``green``, ist der Cluster fertig.
Dasselbe können Sie auch über ``/api/admin/stats`` von Fess mit ``response.stats.engine.number_of_nodes`` und ``response.stats.engine.status`` prüfen.

Mehrere Fess-Server betreiben
=============================

Wenn die Zahl der Suchenden steigt und dem Fess-Server CPU fehlt oder wenn Fess selbst redundant sein soll, verbinden Sie mehrere Fess-Server mit demselben OpenSearch.
Beachten Sie, dass ``compose/multi-instance/`` von docker-fess eine Konfiguration ist, in der unabhängige Suchdienste nebeneinander laufen, wobei jedes Fess eigene Indizes verwendet; sie unterscheidet sich von der hier beschriebenen Konfiguration (zur Trennung nach Organisationen siehe :doc:`guide-13`).

Crawl-Konfigurationen, Benutzer, Jobs und Jobprotokolle werden in OpenSearch gespeichert und sehen daher von jedem Fess aus gleich aus.
Die folgenden Dinge existieren dagegen auf jedem Fess-Server separat und müssen auf allen Servern übereinstimmen.

- Die Einstellungen unter [System] > [Allgemein] (``system.properties`` auf jedem Server). Eine Änderung auf der Einstellungsseite ändert nur den Wert auf diesem Server
- ``fess_config.properties`` und Umgebungsvariablen wie ``FESS_HEAP_SIZE``
- Installierte Plugins
- ``app.cipher.key`` in ``fess_config.properties``. Unter den Parametern von Crawl-Konfigurationen und Datenspeicher-Konfigurationen werden Werte, deren Namen auf ``password``, ``key``, ``token``, ``secret`` usw. enden, mit diesem Schlüssel verschlüsselt in OpenSearch gespeichert. Unterscheidet sich der Schlüssel zwischen den Servern, lassen sich auf einem anderen Server gespeicherte Werte nicht entschlüsseln

Den Server für das Crawlen festlegen
------------------------------------

Das „Ziel“ aller Standard-Jobs ist ``all``.
``all`` passt auf jedes Fess; unverändert läuft „Default Crawler“ daher auf allen Servern zur selben Zeit.

Um das Crawlen einem einzigen Server zu überlassen, führen Sie beide der folgenden Schritte aus.

1. Tragen Sie nur auf dem Server, der crawlen soll, in ``fess_config.properties`` einen Bezeichner ein, etwa ``scheduler.target.name=crawler``, und starten Sie neu. Bei Docker können Sie ``-Dfess.config.scheduler.target.name=crawler`` in ``FESS_JAVA_OPTS`` angeben. Auf den anderen Servern bleibt der Wert leer
2. Öffnen Sie unter [System] > [Scheduler] den Job „Default Crawler“, ändern Sie „Ziel“ von ``all`` auf ``crawler`` und speichern Sie. Crawl-Jobs, die mit [Neuen Job erstellen] angelegt wurden, ändern Sie ebenso

In „Ziel“ können Sie mehrere Bezeichner durch Kommas getrennt angeben.
Nur mit Schritt 1 laufen die Jobs weiterhin auf allen Servern.
Nur mit Schritt 2 passt der Bezeichner auf keinen Server, und Crawls laufen nirgends.
Ob Schritt 1 wirksam ist, prüfen Sie auf dem crawlenden Server unter [Systeminformationen] > [Konfigurationsinformationen] in „App-Eigenschaften“ am Wert von ``scheduler.target.name``.

Bei Jobs, die nicht crawlen (etwa Log-Auswertung oder das Löschen alter Dokumente), lassen Sie „Ziel“ auf ``all``.

Nach der Festlegung klicken Sie auch [Jetzt starten] in der Administrationsoberfläche des crawlenden Servers.
Klicken Sie es auf einem anderen Server, meldet die Oberfläche zwar den Start, der Job läuft auf diesem Server aber nicht; in ``fess.log`` wird lediglich ``Ignoring job`` protokolliert.
Stehen die Server hinter einem Load Balancer, sorgen Sie für einen Weg, auf dem Sie den crawlenden Server direkt erreichen.

Einstellungen des Load Balancers
--------------------------------

In Fess 15.9 werden Anmeldesitzungen im Speicher des jeweiligen Fess gehalten.
Wenn ein Load Balancer die Suchseite oder die Administrationsoberfläche mit Anmeldung verteilt, aktivieren Sie Sticky Sessions, damit derselbe Nutzer immer an denselben Server geleitet wird.
Sitzungen in OpenSearch zu speichern und serverübergreifend zu teilen, ist ab 15.10 möglich.

Für den Health-Check des Load Balancers können Sie ``/api/v2/health`` verwenden.
Es liefert 503, wenn der OpenSearch-Cluster ``RED`` ist oder keine Verbindung zu OpenSearch besteht.

Gegenseitiger Ausschluss von Wartungsvorgängen
----------------------------------------------

„Neuindizierung“, „Dokumentenindex neu laden“, „Crawler-Index löschen“ und „Konfigurationsindex neu erstellen“ unter [Systeminformationen] > [Wartung] sind gegenseitig ausgeschlossen, sodass mehrere Fess-Server sie nicht gleichzeitig ausführen.
Läuft der Vorgang bereits auf einem anderen Server, wird „Die Operation wird bereits auf <Hostname> ausgeführt.“ angezeigt.
Dieser Ausschluss betrifft nur Wartungsvorgänge; Jobs und die Einstellungen unter [Allgemein] werden damit nicht zwischen den Servern abgestimmt.

Zu Richtwerten für die Dimensionierung
======================================

Die Zahl der Dokumente oder Nutzer allein bestimmt nicht, welchen Aufbau Sie benötigen.
Der Bedarf an Speicher und CPU hängt stark von der Textlänge je Dokument, dem Anteil an Anhängen, den typischen Suchbegriffen und davon ab, ob sich die Nutzer anmelden.

Entscheiden Sie wie folgt anhand gemessener Werte.

- Bestimmen Sie aus ``store.size`` des Index den Heap von OpenSearch anhand der Richtwerttabelle in `Speicherkonfiguration <https://fess.codelibs.org/de/stable/config/setup-memory.html>`__
- Verschlechtert sich p95 im Suchprotokoll und bleiben Heap-Auslastung oder CPU in ``_cat/nodes`` hoch, erhöhen Sie den Heap von OpenSearch oder fügen Knoten hinzu
- Werden die Crawl-Zeiten im Jobprotokoll länger und erscheinen ``Cpu Load``-Meldungen im Log, lagern Sie OpenSearch auf einen eigenen Server aus
- Hat OpenSearch Reserven, ist aber die CPU des Fess-Servers hoch ausgelastet, betreiben Sie mehrere Fess-Server

Weiterführende Artikel
======================

- Fess mit Überwachung, Logs und Backups produktiv betreiben: :doc:`guide-10`
- Den Zugriff schützen, einschließlich der Erreichbarkeit von OpenSearch und der Anmeldung: :doc:`guide-15`
- Den Abgleich der Einstellungen mehrerer Server als Code verwalten: :doc:`guide-16`
- Ein Fess für mehrere Organisationen getrennt nutzen: :doc:`guide-13`
- Ordnen, was in jeder Phase der Einführung zu prüfen ist: :doc:`guide-23`

Referenzen
==========

- `Speicherkonfiguration <https://fess.codelibs.org/de/stable/config/setup-memory.html>`__
- `Port- und Netzwerkkonfiguration <https://fess.codelibs.org/de/stable/config/setup-port-network.html>`__
- `Laststeuerung-Konfiguration <https://fess.codelibs.org/de/stable/config/load-control.html>`__
- `Installation unter Linux (Detaillierte Anleitung) <https://fess.codelibs.org/de/stable/install/install-linux.html>`__
- `Installation mit Docker (Detailliert) <https://fess.codelibs.org/de/stable/install/install-docker.html>`__
- `Der Befehl fess-setup <https://fess.codelibs.org/de/stable/install/fess-setup.html>`__
- `Wartung <https://fess.codelibs.org/de/stable/admin/maintenance-guide.html>`__
- `Scheduler <https://fess.codelibs.org/de/stable/admin/scheduler-guide.html>`__
- `Suchprotokoll <https://fess.codelibs.org/de/stable/admin/searchlog-guide.html>`__
- `Stats API <https://fess.codelibs.org/de/stable/api/admin/api-admin-stats.html>`__
- `Index-Verwaltung <https://fess.codelibs.org/de/stable/config/admin-index-backup.html>`__
