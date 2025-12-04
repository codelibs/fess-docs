========================
Erweiterte Crawler-Konfiguration
========================

Übersicht
====

Dieser Leitfaden beschreibt erweiterte Konfigurationen für den |Fess|-Crawler.
Für grundlegende Crawler-Konfigurationen siehe :doc:`crawler-basic`.

.. warning::
   Die Einstellungen auf dieser Seite können systemweite Auswirkungen haben.
   Testen Sie Konfigurationsänderungen gründlich, bevor Sie sie in Produktionsumgebungen anwenden.

Allgemeine Konfiguration
========

Speicherort der Konfigurationsdateien
------------------

Erweiterte Crawler-Konfigurationen werden in folgenden Dateien vorgenommen:

- **Hauptkonfiguration**: ``/etc/fess/fess_config.properties`` (oder ``app/WEB-INF/classes/fess_config.properties``)
- **Inhaltslängen-Konfiguration**: ``app/WEB-INF/classes/crawler/contentlength.xml``
- **Komponenten-Konfiguration**: ``app/WEB-INF/classes/crawler/container.xml``

Standard-Skriptsprache
--------------------

Legt die Standard-Skriptsprache für den Crawler fest.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``crawler.default.script``
     - Crawler-Skriptsprache
     - ``groovy``

::

    crawler.default.script=groovy

HTTP-Thread-Pool
------------------

Thread-Pool-Konfiguration für den HTTP-Crawler.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``crawler.http.thread_pool.size``
     - HTTP-Thread-Pool-Größe
     - ``0``

::

    # Bei 0 automatische Konfiguration
    crawler.http.thread_pool.size=0

Dokumentverarbeitungs-Konfiguration
====================

Grundkonfiguration
--------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``crawler.document.max.site.length``
     - Maximale Zeilenanzahl für Dokumentsite
     - ``100``
   * - ``crawler.document.site.encoding``
     - Codierung der Dokumentsite
     - ``UTF-8``
   * - ``crawler.document.unknown.hostname``
     - Ersatzwert für unbekannte Hostnamen
     - ``unknown``
   * - ``crawler.document.use.site.encoding.on.english``
     - Site-Codierung für englische Dokumente verwenden
     - ``false``
   * - ``crawler.document.append.data``
     - Daten zum Dokument hinzufügen
     - ``true``
   * - ``crawler.document.append.filename``
     - Dateinamen zum Dokument hinzufügen
     - ``false``

Konfigurationsbeispiel
~~~~~~

::

    crawler.document.max.site.length=100
    crawler.document.site.encoding=UTF-8
    crawler.document.unknown.hostname=unknown
    crawler.document.use.site.encoding.on.english=false
    crawler.document.append.data=true
    crawler.document.append.filename=false

Wortverarbeitungs-Konfiguration
------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``crawler.document.max.alphanum.term.size``
     - Maximale Länge alphanumerischer Wörter
     - ``20``
   * - ``crawler.document.max.symbol.term.size``
     - Maximale Länge von Symbol-Wörtern
     - ``10``
   * - ``crawler.document.duplicate.term.removed``
     - Entfernung doppelter Wörter
     - ``false``

Konfigurationsbeispiel
~~~~~~

::

    # Maximale Länge alphanumerischer Zeichen auf 50 ändern
    crawler.document.max.alphanum.term.size=50

    # Maximale Länge von Symbolen auf 20 ändern
    crawler.document.max.symbol.term.size=20

    # Doppelte Wörter entfernen
    crawler.document.duplicate.term.removed=true

.. note::
   Das Erhöhen von ``max.alphanum.term.size`` ermöglicht die vollständige Indizierung langer IDs, Tokens, URLs usw., erhöht jedoch die Indexgröße.

Zeichenverarbeitungs-Konfiguration
------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``crawler.document.space.chars``
     - Definition von Leerzeichen
     - ``\u0009\u000A...``
   * - ``crawler.document.fullstop.chars``
     - Definition von Satzendzeichen
     - ``\u002e\u06d4...``

Konfigurationsbeispiel
~~~~~~

::

    # Standardwerte (einschließlich Unicode-Zeichen)
    crawler.document.space.chars=\u0009\u000A\u000B\u000C\u000D\u001C\u001D\u001E\u001F\u0020\u00A0\u1680\u180E\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u200B\u200C\u202F\u205F\u3000\uFEFF\uFFFD\u00B6

    crawler.document.fullstop.chars=\u002e\u06d4\u2e3c\u3002

Protokoll-Konfiguration
==============

Unterstützte Protokolle
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``crawler.web.protocols``
     - Protokolle für Web-Crawling
     - ``http,https``
   * - ``crawler.file.protocols``
     - Protokolle für Datei-Crawling
     - ``file,smb,smb1,ftp,storage``

Konfigurationsbeispiel
~~~~~~

::

    crawler.web.protocols=http,https
    crawler.file.protocols=file,smb,smb1,ftp,storage

Umgebungsvariablen-Parameter
--------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``crawler.data.env.param.key.pattern``
     - Muster für Umgebungsvariablen-Parameterschlüssel
     - ``^FESS_ENV_.*``

::

    # Umgebungsvariablen beginnend mit FESS_ENV_ können in Crawl-Konfigurationen verwendet werden
    crawler.data.env.param.key.pattern=^FESS_ENV_.*

robots.txt-Konfiguration
===============

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``crawler.ignore.robots.txt``
     - robots.txt ignorieren
     - ``false``
   * - ``crawler.ignore.robots.tags``
     - Zu ignorierende Robots-Tags
     - (leer)
   * - ``crawler.ignore.content.exception``
     - Inhaltsausnahmen ignorieren
     - ``true``

Konfigurationsbeispiel
~~~~~~

::

    # robots.txt ignorieren (nicht empfohlen)
    crawler.ignore.robots.txt=false

    # Bestimmte Robots-Tags ignorieren
    crawler.ignore.robots.tags=

    # Inhaltsausnahmen ignorieren
    crawler.ignore.content.exception=true

.. warning::
   Die Einstellung ``crawler.ignore.robots.txt=true`` kann gegen Nutzungsbedingungen von Websites verstoßen. Seien Sie vorsichtig beim Crawlen externer Sites.

Fehlerbehandlungs-Konfiguration
==============

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``crawler.failure.url.status.codes``
     - Als Fehler behandelte HTTP-Statuscodes
     - ``404``

Konfigurationsbeispiel
~~~~~~

::

    # Zusätzlich zu 404 auch 403 als Fehler behandeln
    crawler.failure.url.status.codes=404,403

Systemüberwachungs-Konfiguration
================

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``crawler.system.monitor.interval``
     - Systemüberwachungsintervall (Sekunden)
     - ``60``

::

    # System alle 30 Sekunden überwachen
    crawler.system.monitor.interval=30

Hot-Thread-Konfiguration
------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``crawler.hotthread.ignore_idle_threads``
     - Leerlaufende Threads ignorieren
     - ``true``
   * - ``crawler.hotthread.interval``
     - Snapshot-Intervall
     - ``500ms``
   * - ``crawler.hotthread.snapshots``
     - Anzahl Snapshots
     - ``10``
   * - ``crawler.hotthread.threads``
     - Anzahl überwachter Threads
     - ``3``
   * - ``crawler.hotthread.timeout``
     - Timeout
     - ``30s``
   * - ``crawler.hotthread.type``
     - Überwachungstyp
     - ``cpu``

Konfigurationsbeispiel
~~~~~~

::

    crawler.hotthread.ignore_idle_threads=true
    crawler.hotthread.interval=500ms
    crawler.hotthread.snapshots=10
    crawler.hotthread.threads=3
    crawler.hotthread.timeout=30s
    crawler.hotthread.type=cpu

Metadaten-Konfiguration
==============

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``crawler.metadata.content.excludes``
     - Auszuschließende Metadaten
     - ``resourceName,X-Parsed-By...``
   * - ``crawler.metadata.name.mapping``
     - Metadaten-Namen-Mapping
     - ``title=title:string...``

Konfigurationsbeispiel
~~~~~~

::

    # Auszuschließende Metadaten
    crawler.metadata.content.excludes=resourceName,X-Parsed-By,Content-Encoding.*,Content-Type.*,X-TIKA.*,X-FESS.*

    # Metadaten-Namen-Mapping
    crawler.metadata.name.mapping=\
        title=title:string\n\
        Title=title:string\n\
        dc:title=title:string

HTML-Crawler-Konfiguration
===================

XPath-Konfiguration
----------

XPath-Konfiguration zum Extrahieren von HTML-Elementen.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``crawler.document.html.content.xpath``
     - XPath für Inhalt
     - ``//BODY``
   * - ``crawler.document.html.lang.xpath``
     - XPath für Sprache
     - ``//HTML/@lang``
   * - ``crawler.document.html.digest.xpath``
     - XPath für Digest
     - ``//META[@name='description']/@content``
   * - ``crawler.document.html.canonical.xpath``
     - XPath für kanonische URL
     - ``//LINK[@rel='canonical'][1]/@href``

Konfigurationsbeispiel
~~~~~~

::

    # Standardkonfiguration
    crawler.document.html.content.xpath=//BODY
    crawler.document.html.lang.xpath=//HTML/@lang
    crawler.document.html.digest.xpath=//META[@name='description']/@content
    crawler.document.html.canonical.xpath=//LINK[@rel='canonical'][1]/@href

Beispiele für benutzerdefinierte XPath
~~~~~~~~~~~~~~~~~~~

::

    # Nur bestimmte div-Elemente als Inhalt extrahieren
    crawler.document.html.content.xpath=//DIV[@id='main-content']

    # Auch Meta-Keywords in Digest einbeziehen
    crawler.document.html.digest.xpath=//META[@name='description']/@content|//META[@name='keywords']/@content

HTML-Tag-Verarbeitung
-------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``crawler.document.html.pruned.tags``
     - Zu entfernende HTML-Tags
     - ``noscript,script,style,header,footer,aside,nav,a[rel=nofollow]``
   * - ``crawler.document.html.max.digest.length``
     - Maximale Digest-Länge
     - ``120``
   * - ``crawler.document.html.default.lang``
     - Standardsprache
     - (leer)

Konfigurationsbeispiel
~~~~~~

::

    # Tags zum Entfernen hinzufügen
    crawler.document.html.pruned.tags=noscript,script,style,header,footer,aside,nav,a[rel=nofollow],form

    # Digest-Länge auf 200 Zeichen
    crawler.document.html.max.digest.length=200

    # Standardsprache auf Deutsch
    crawler.document.html.default.lang=de

URL-Musterfilter
---------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``crawler.document.html.default.include.index.patterns``
     - In Index einzuschließende URL-Muster
     - (leer)
   * - ``crawler.document.html.default.exclude.index.patterns``
     - Aus Index auszuschließende URL-Muster
     - ``(?i).*(css|js|jpeg...)``
   * - ``crawler.document.html.default.include.search.patterns``
     - In Suchergebnisse einzuschließende URL-Muster
     - (leer)
   * - ``crawler.document.html.default.exclude.search.patterns``
     - Aus Suchergebnissen auszuschließende URL-Muster
     - (leer)

Konfigurationsbeispiel
~~~~~~

::

    # Standard-Ausschlussmuster
    crawler.document.html.default.exclude.index.patterns=(?i).*(css|js|jpeg|jpg|gif|png|bmp|wmv|xml|ico|exe)

    # Nur bestimmte Pfade indizieren
    crawler.document.html.default.include.index.patterns=https://example\\.com/docs/.*

Datei-Crawler-Konfiguration
======================

Grundkonfiguration
--------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``crawler.document.file.name.encoding``
     - Dateinamen-Codierung
     - (leer)
   * - ``crawler.document.file.no.title.label``
     - Label für Dateien ohne Titel
     - ``No title.``
   * - ``crawler.document.file.ignore.empty.content``
     - Leere Inhalte ignorieren
     - ``false``
   * - ``crawler.document.file.max.title.length``
     - Maximale Titellänge
     - ``100``
   * - ``crawler.document.file.max.digest.length``
     - Maximale Digest-Länge
     - ``200``

Konfigurationsbeispiel
~~~~~~

::

    # Windows-31J-Dateinamen verarbeiten
    crawler.document.file.name.encoding=Windows-31J

    # Label für Dateien ohne Titel
    crawler.document.file.no.title.label=Kein Titel

    # Leere Dateien ignorieren
    crawler.document.file.ignore.empty.content=true

    # Titel- und Digest-Länge
    crawler.document.file.max.title.length=200
    crawler.document.file.max.digest.length=500

Inhaltsverarbeitung
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``crawler.document.file.append.meta.content``
     - Metadaten zum Inhalt hinzufügen
     - ``true``
   * - ``crawler.document.file.append.body.content``
     - Haupttext zum Inhalt hinzufügen
     - ``true``
   * - ``crawler.document.file.default.lang``
     - Standardsprache
     - (leer)

Konfigurationsbeispiel
~~~~~~

::

    crawler.document.file.append.meta.content=true
    crawler.document.file.append.body.content=true
    crawler.document.file.default.lang=de

Datei-URL-Musterfilter
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``crawler.document.file.default.include.index.patterns``
     - In Index einzuschließende Muster
     - (leer)
   * - ``crawler.document.file.default.exclude.index.patterns``
     - Aus Index auszuschließende Muster
     - (leer)
   * - ``crawler.document.file.default.include.search.patterns``
     - In Suchergebnisse einzuschließende Muster
     - (leer)
   * - ``crawler.document.file.default.exclude.search.patterns``
     - Aus Suchergebnissen auszuschließende Muster
     - (leer)

Konfigurationsbeispiel
~~~~~~

::

    # Nur bestimmte Erweiterungen indizieren
    crawler.document.file.default.include.index.patterns=.*\\.(pdf|docx|xlsx|pptx)$

    # Temp-Ordner ausschließen
    crawler.document.file.default.exclude.index.patterns=.*/temp/.*

Cache-Konfiguration
==============

Dokumenten-Cache
----------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``crawler.document.cache.enabled``
     - Dokumenten-Cache aktivieren
     - ``true``
   * - ``crawler.document.cache.max.size``
     - Maximale Cache-Größe (Bytes)
     - ``2621440`` (2,5 MB)
   * - ``crawler.document.cache.supported.mimetypes``
     - Zu cachende MIME-Typen
     - ``text/html``
   * - ``crawler.document.cache.html.mimetypes``
     - Als HTML zu behandelnde MIME-Typen
     - ``text/html``

Konfigurationsbeispiel
~~~~~~

::

    # Dokumenten-Cache aktivieren
    crawler.document.cache.enabled=true

    # Cache-Größe auf 5 MB
    crawler.document.cache.max.size=5242880

    # Zu cachende MIME-Typen
    crawler.document.cache.supported.mimetypes=text/html,application/xhtml+xml

    # Als HTML zu behandelnde MIME-Typen
    crawler.document.cache.html.mimetypes=text/html,application/xhtml+xml

.. note::
   Bei aktiviertem Cache wird in Suchergebnissen ein Cache-Link angezeigt,
   über den Benutzer den Inhalt zum Zeitpunkt des Crawlings einsehen können.

JVM-Optionen
==============

Sie können JVM-Optionen für den Crawler-Prozess konfigurieren.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``jvm.crawler.options``
     - JVM-Optionen für Crawler
     - ``-Xms128m -Xmx512m...``

Standardkonfiguration
--------------

::

    jvm.crawler.options=-Xms128m -Xmx512m \
        -XX:MaxMetaspaceSize=128m \
        -XX:+UseG1GC \
        -XX:MaxGCPauseMillis=60000 \
        -XX:-HeapDumpOnOutOfMemoryError

Erklärung wichtiger Optionen
----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Option
     - Beschreibung
   * - ``-Xms128m``
     - Initiale Heap-Größe (128 MB)
   * - ``-Xmx512m``
     - Maximale Heap-Größe (512 MB)
   * - ``-XX:MaxMetaspaceSize=128m``
     - Maximale Metaspace-Größe (128 MB)
   * - ``-XX:+UseG1GC``
     - G1-Garbage-Collector verwenden
   * - ``-XX:MaxGCPauseMillis=60000``
     - Ziel für GC-Pausenzeit (60 Sekunden)
   * - ``-XX:-HeapDumpOnOutOfMemoryError``
     - Heap-Dumps bei OutOfMemory deaktivieren

Beispiele für benutzerdefinierte Konfiguration
--------------

**Beim Crawlen großer Dateien:**

::

    jvm.crawler.options=-Xms256m -Xmx2g \
        -XX:MaxMetaspaceSize=256m \
        -XX:+UseG1GC \
        -XX:MaxGCPauseMillis=60000

**Beim Debuggen:**

::

    jvm.crawler.options=-Xms128m -Xmx512m \
        -XX:MaxMetaspaceSize=128m \
        -XX:+UseG1GC \
        -XX:+HeapDumpOnOutOfMemoryError \
        -XX:HeapDumpPath=/tmp/crawler_dump.hprof

Details siehe :doc:`setup-memory`.

Leistungsoptimierung
==========================

Optimierung der Crawl-Geschwindigkeit
--------------------

**1. Thread-Anzahl anpassen**

Durch Erhöhung der Anzahl paralleler Crawls kann die Crawl-Geschwindigkeit verbessert werden.

::

    # Thread-Anzahl in Crawl-Konfiguration der Verwaltungsoberfläche anpassen
    Thread-Anzahl: 10

Beachten Sie jedoch die Last auf dem Zielserver.

**2. Timeout anpassen**

Bei langsamen Sites passen Sie Timeouts an.

::

    # Zu „Konfigurationsparametern" der Crawl-Konfiguration hinzufügen
    client.connectionTimeout=10000
    client.socketTimeout=30000

**3. Unnötige Inhalte ausschließen**

Durch Ausschluss von Bildern, CSS, JavaScript-Dateien usw. wird die Crawl-Geschwindigkeit verbessert.

::

    # URL-Ausschlussmuster
    .*\.(jpg|jpeg|png|gif|css|js|ico)$

**4. Retry-Einstellungen**

Passen Sie Anzahl und Intervall von Wiederholungsversuchen bei Fehlern an.

::

    # Zu „Konfigurationsparametern" der Crawl-Konfiguration hinzufügen
    client.maxRetry=3
    client.retryInterval=1000

Optimierung der Speichernutzung
--------------------

**1. Heap-Größe anpassen**

::

    jvm.crawler.options=-Xms256m -Xmx1g

**2. Cache-Größe anpassen**

::

    crawler.document.cache.max.size=1048576  # 1 MB

**3. Große Dateien ausschließen**

::

    # Zu „Konfigurationsparametern" der Crawl-Konfiguration hinzufügen
    client.maxContentLength=10485760  # 10 MB

Details siehe :doc:`setup-memory`.

Verbesserung der Indexqualität
----------------------

**1. XPath optimieren**

Schließen Sie unnötige Elemente (Navigation, Werbung usw.) aus.

::

    crawler.document.html.content.xpath=//DIV[@id='main-content']
    crawler.document.html.pruned.tags=noscript,script,style,header,footer,aside,nav,form,iframe

**2. Digest optimieren**

::

    crawler.document.html.max.digest.length=200

**3. Metadaten-Mapping**

::

    crawler.metadata.name.mapping=\
        title=title:string\n\
        description=digest:string\n\
        keywords=label:string

Fehlersuche
======================

Speichermangel
----------

**Symptome:**

- ``OutOfMemoryError`` in ``fess_crawler.log`` aufgezeichnet
- Crawling stoppt mittendrin

**Gegenmaßnahmen:**

1. Crawler-Heap-Größe erhöhen

   ::

       jvm.crawler.options=-Xms256m -Xmx2g

2. Anzahl paralleler Threads reduzieren

3. Große Dateien ausschließen

Details siehe :doc:`setup-memory`.

Crawling ist langsam
--------------

**Symptome:**

- Crawling dauert zu lange
- Häufige Timeouts

**Gegenmaßnahmen:**

1. Thread-Anzahl erhöhen (Last auf Zielserver beachten)

2. Timeouts anpassen

   ::

       client.connectionTimeout=5000
       client.socketTimeout=10000

3. Unnötige URLs ausschließen

Bestimmte Inhalte können nicht extrahiert werden
------------------------------

**Symptome:**

- Seitentext wird nicht korrekt extrahiert
- Wichtige Informationen fehlen in Suchergebnissen

**Gegenmaßnahmen:**

1. XPath überprüfen und anpassen

   ::

       crawler.document.html.content.xpath=//DIV[@class='content']

2. Zu entfernende Tags überprüfen

   ::

       crawler.document.html.pruned.tags=script,style

3. Bei dynamisch durch JavaScript generierten Inhalten alternative Methoden (z. B. API-Crawling) in Betracht ziehen

Zeichenkodierungsprobleme treten auf
------------------

**Symptome:**

- Zeichenkodierungsprobleme in Suchergebnissen
- Bestimmte Sprachen werden nicht korrekt angezeigt

**Gegenmaßnahmen:**

1. Codierungseinstellungen überprüfen

   ::

       crawler.document.site.encoding=UTF-8
       crawler.crawling.data.encoding=UTF-8

2. Dateinamen-Codierung konfigurieren

   ::

       crawler.document.file.name.encoding=Windows-31J

3. Codierungsfehler im Protokoll überprüfen

   ::

       grep -i "encoding" /var/log/fess/fess_crawler.log

Best Practices
==================

1. **In Testumgebung validieren**

   Validieren Sie gründlich in Testumgebung, bevor Sie in Produktionsumgebung anwenden.

2. **Schrittweise Anpassung**

   Ändern Sie Konfigurationen nicht auf einmal stark, sondern passen Sie schrittweise an und überprüfen Sie die Wirkung.

3. **Protokolle überwachen**

   Überwachen Sie nach Konfigurationsänderungen Protokolle auf Fehler oder Leistungsprobleme.

   ::

       tail -f /var/log/fess/fess_crawler.log

4. **Backup**

   Erstellen Sie vor Änderung von Konfigurationsdateien unbedingt ein Backup.

   ::

       cp /etc/fess/fess_config.properties /etc/fess/fess_config.properties.bak

5. **Dokumentation**

   Dokumentieren Sie geänderte Konfigurationen und deren Begründung.

Referenzinformationen
========

- :doc:`crawler-basic` - Grundlegende Crawler-Konfiguration
- :doc:`crawler-thumbnail` - Thumbnail-Konfiguration
- :doc:`setup-memory` - Speicherkonfiguration
- :doc:`admin-logging` - Protokollkonfiguration
- :doc:`search-advanced` - Erweiterte Suchkonfiguration
