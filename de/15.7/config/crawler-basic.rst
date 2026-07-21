================================================================
Crawler-Konfiguration: Web-, Dateiserver- und Datenbank-Crawling
================================================================

Übersicht
====

Der Crawler von |Fess| ist eine Funktion, die automatisch Inhalte von Websites, Dateisystemen usw. sammelt und im Suchindex registriert.
Mit dem Web-Crawler für die Website-Suche, dem Datei-Crawler für die Dateiserver-Suche und dem Datenspeicher-Crawler für die Suche in Datenbanken und anderen Datenquellen lässt sich mit einem einzigen |Fess| eine seitenübergreifende Volltextsuche aufbauen.
Dieser Leitfaden erläutert die grundlegenden Konzepte und Konfigurationsmethoden des Crawlers.

Informationen zum Crawlen von Datenbanken und anderen Datenquellen finden Sie unter :doc:`datastore/ds-database` und :doc:`datastore/ds-overview`. Um die Relevanz über alle gecrawlten Inhalte hinweg mit hybrider (Keyword- + semantischer) Suche zu verbessern, siehe :doc:`rank-fusion`.

Grundlegende Crawler-Konzepte
====================

Was ist ein Crawler?
--------------

Ein Crawler ist ein Programm, das automatisch Inhalte sammelt, indem es von angegebenen URLs oder Dateipfaden ausgehend Links folgt.

Der Crawler von |Fess| hat folgende Merkmale:

- **Multi-Protokoll-Unterstützung**: HTTP/HTTPS, Dateisystem, SMB, FTP usw.
- **Geplante Ausführung**: Regelmäßiges automatisches Crawlen
- **Inkrementelles Crawlen**: Aktualisierung nur geänderter Inhalte
- **Parallele Verarbeitung**: Gleichzeitiges Crawlen mehrerer URLs
- **Einhaltung von Roboter-Regeln**: Einhaltung von robots.txt

Crawler-Typen
----------------

|Fess| bietet folgende Crawler-Typen je nach Ziel.

.. list-table:: Crawler-Typen
   :header-rows: 1
   :widths: 20 40 40

   * - Typ
     - Ziel
     - Verwendungszweck
   * - **Web-Crawler**
     - Websites (HTTP/HTTPS)
     - Öffentliche Websites, Intranet-Websites
   * - **Datei-Crawler**
     - Dateisystem, SMB, FTP
     - Dateiserver, freigegebene Ordner
   * - **Datenspeicher-Crawler**
     - Datenbanken
     - RDB, CSV, JSON und andere Datenquellen

Erstellen von Crawl-Konfigurationen
==================

Hinzufügen grundlegender Crawl-Konfigurationen
--------------------------

1. **Zugriff auf Verwaltungsoberfläche**

   Öffnen Sie ``http://localhost:8080/admin`` im Browser und melden Sie sich als Administrator an.

2. **Crawler-Konfigurationsbildschirm öffnen**

   Wählen Sie im linken Menü „Crawler" → „Web" oder „Dateisystem".

3. **Neue Konfiguration erstellen**

   Klicken Sie auf die Schaltfläche „Neu erstellen".

4. **Grundinformationen eingeben**

   - **Name**: Identifikationsname der Crawl-Konfiguration (z. B. Firmen-Wiki)
   - **URL**: Start-URL für das Crawling (z. B. ``https://wiki.example.com/``)
   - **Intervall**: Zugriffsintervall pro URL in Millisekunden (z. B. 10000)
   - **Thread-Anzahl**: Anzahl paralleler Crawls (z. B. 5)
   - **Tiefe**: Hierarchietiefe für das Folgen von Links (z. B. 3)

5. **Speichern**

   Klicken Sie auf „Erstellen", um die Konfiguration zu speichern.

Beispiele für Web-Crawler-Konfiguration
---------------------

Crawlen von Firmen-Intranet-Sites
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    Name: Firmenportal
    URL: http://intranet.example.com/
    Crawl-Intervall: Einmal täglich
    Thread-Anzahl: 10
    Tiefe: leer (unbegrenzt)
    Maximale Zugriffszahl: 10000

Crawlen öffentlicher Websites
~~~~~~~~~~~~~~~~~~~~~~~

::

    Name: Produkt-Site
    URL: https://www.example.com/products/
    Crawl-Intervall: Einmal wöchentlich
    Thread-Anzahl: 5
    Tiefe: 5
    Maximale Zugriffszahl: 1000

Beispiele für Datei-Crawler-Konfiguration
--------------------------

Lokales Dateisystem
~~~~~~~~~~~~~~~~~~~~~~~~

::

    Name: Dokumentenordner
    URL: file:///home/share/documents/
    Crawl-Intervall: Einmal täglich
    Thread-Anzahl: 3
    Tiefe: leer (unbegrenzt)

SMB/CIFS (Windows-Dateifreigabe)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    Name: Dateiserver
    URL: smb://fileserver.example.com/share/
    Crawl-Intervall: Einmal täglich
    Thread-Anzahl: 5
    Tiefe: leer (unbegrenzt)

Konfiguration von Authentifizierungsinformationen
--------------

Für Sites oder Dateiserver, die Authentifizierung erfordern, konfigurieren Sie Authentifizierungsinformationen.

1. Wählen Sie in der Verwaltungsoberfläche „Crawler" → „Web-Authentifizierung" (für Dateiserver: „Datei-Authentifizierung")
2. Klicken Sie auf „Neu erstellen"
3. Geben Sie Authentifizierungsinformationen ein:

   ::

       Hostname: wiki.example.com
       Port: 443
       Schema: Basic
       Benutzername: crawler_user
       Passwort: ********

   .. note::
      „Schema" wird aus Basic / Digest / NTLM / Form ausgewählt.
      Wählen Sie außerdem im Feld „Web Config" (bei Datei-Authentifizierung: „Dateisystem-Konfiguration")
      die zugehörige Crawl-Konfiguration aus. Die Authentifizierungsdaten sind
      an eine Crawl-Konfiguration gebunden.

4. Klicken Sie auf „Erstellen"

Ausführung des Crawlings
==============

Manuelle Ausführung
--------

Um einen konfigurierten Crawl sofort auszuführen, starten Sie den Crawler-Job über das Menü „Scheduler".

1. Öffnen Sie das Menü „Scheduler"
2. Wählen Sie den Job „Default Crawler"
3. Klicken Sie auf die Schaltfläche „Jetzt starten"
4. Überprüfen Sie den Job-Ausführungsstatus

.. note::
   Die Listenansicht der Crawl-Konfigurationen (Web / Dateisystem) enthält keinen individuellen
   „Starten"-Button. Crawls werden als Scheduler-Job ausgeführt.
   Der Job „Default Crawler" verarbeitet alle aktivierten Crawl-Konfigurationen.

Geplante Ausführung
----------------

Um Crawls regelmäßig auszuführen:

1. Öffnen Sie das Menü „Scheduler"
2. Wählen Sie den Job „Default Crawler"
3. Konfigurieren Sie den Zeitplanausdruck (Cron-Format)

   ::

       # Täglich um 2 Uhr morgens ausführen
       0 2 * * *

       # Jede Stunde zur vollen Stunde ausführen
       0 * * * *

       # Montag bis Freitag um 18 Uhr ausführen
       0 18 * * 1-5

4. Klicken Sie auf „Aktualisieren"

.. note::
   Der |Fess|-Scheduler verwendet cron4j-Ausdrücke mit 5 Feldern (Minute Stunde Tag Monat Wochentag).
   Es gibt kein Sekundenfeld und kein ``?`` (anders als bei Quartz).
   Der Wochentag wird als ``0`` (Sonntag) bis ``6`` (Samstag) angegeben.

Überprüfung des Crawl-Status
------------------

Überprüfung des Status laufender Crawls:

1. Öffnen Sie das Menü „Scheduler"
2. Überprüfen Sie laufende Jobs
3. Überprüfen Sie Details im Protokoll:

   ::

       tail -f /var/log/fess/fess-crawler.log

   .. note::
      Der obige Pfad gilt für RPM/DEB-Paketinstallationen. Bei zip/tar.gz-Bereitstellungen befinden sich die Protokolle im Verzeichnis ``logs/``.

Grundlegende Konfigurationselemente
================

Beschränkung von Crawl-Zielen
------------------

Beschränkung nach URL-Muster
~~~~~~~~~~~~~~~~~~~~~

Sie können bestimmte URL-Muster als Crawl-Ziele einschließen oder ausschließen.

**Einzuschließende URL-Muster (regulärer Ausdruck):**

::

    # Nur unter /docs/ crawlen
    https://example\.com/docs/.*

**Auszuschließende URL-Muster (regulärer Ausdruck):**

::

    # Bestimmte Verzeichnisse ausschließen
    .*/admin/.*
    .*/private/.*

    # Bestimmte Dateierweiterungen ausschließen
    .*\.(jpg|png|gif|css|js)$

Tiefenbeschränkung
~~~~~~~~~~

Beschränkung der Hierarchietiefe für das Folgen von Links:

- **0**: Nur Start-URL
- **1**: Start-URL und von dort verlinkte Seiten
- **leer (nicht gesetzt)**: Unbegrenzt (allen Links folgen)

.. note::
   Das Tiefe-Feld der Verwaltungsoberfläche akzeptiert nur ganze Zahlen >= 0.
   Für unbegrenztes Crawling lassen Sie das Feld leer (intern als ``-1`` behandelt, was unbegrenzt bedeutet).

Maximale Zugriffszahl
~~~~~~~~~~~~~~

Obergrenze für die Anzahl zu crawlender Seiten:

::

    Maximale Zugriffszahl: 1000

Stoppt nach dem Crawlen von 1000 Seiten. Wird das Feld leer gelassen, ist die Anzahl unbegrenzt (keine Obergrenze).

Anzahl paralleler Crawls (Thread-Anzahl)
--------------------------

Gibt die Anzahl gleichzeitig zu crawlender URLs an.

.. list-table:: Empfohlene Thread-Anzahl
   :header-rows: 1
   :widths: 40 30 30

   * - Umgebung
     - Empfohlener Wert
     - Beschreibung
   * - Kleine Site (~10.000 Seiten)
     - 3–5
     - Last auf Zielserver begrenzen
   * - Mittlere Site (10.000–100.000 Seiten)
     - 5–10
     - Ausgewogene Einstellung
   * - Große Site (über 100.000 Seiten)
     - 10–20
     - Schnelles Crawling erforderlich
   * - Dateiserver
     - 3–5
     - Datei-I/O-Last berücksichtigen

.. warning::
   Zu hohe Thread-Anzahlen belasten den Zielserver übermäßig.
   Konfigurieren Sie angemessene Werte.

.. note::
   Der Standard-Thread-Wert bei Neuerstellung beträgt ``1`` (Web-Crawler) bzw. ``5`` (Datei-Crawler).
   Das Standard-Anforderungsintervall (Intervall) beträgt ``10000`` ms (Web-Crawler) bzw. ``1000`` ms (Datei-Crawler).

Crawl-Intervall
------------

Gibt die Häufigkeit der Crawl-Ausführung an.

::

    # Zeitangabe
    Crawl-Intervall: 3600000  # Millisekunden (1 Stunde)

    # Oder im Scheduler konfigurieren
    0 2 * * *  # Täglich um 2 Uhr morgens

Konfiguration der Dateigröße
====================

Sie können die Obergrenze für zu crawlende Dateigrößen konfigurieren.

Obergrenze für abzurufende Dateigrößen
----------------------------

Fügen Sie Folgendes zu den „Konfigurationsparametern" der Crawler-Konfiguration hinzu:

::

    client.maxContentLength=10485760

Ruft Dateien bis zu 10 MB ab. Standardmäßig keine Beschränkung.

.. note::
   Beim Crawlen großer Dateien passen Sie auch die Speichereinstellungen an.
   Details siehe :doc:`setup-memory`.

Obergrenze für zu indizierende Dateigrößen
------------------------------------

Sie können Obergrenzen für zu indizierende Größen nach Dateityp festlegen.

**Standardwerte:**

- HTML-Dateien: 2,5 MB
- Andere Dateien: 10 MB

**Konfigurationsdatei:** ``app/WEB-INF/classes/crawler/contentlength.xml``

**Standardkonfiguration:**

::

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
            "http://dbflute.org/meta/lastadi10.dtd">
    <components namespace="fessCrawler">
            <include path="crawler/container.xml" />

            <component name="contentLengthHelper"
                    class="org.codelibs.fess.crawler.helper.ContentLengthHelper" instance="singleton">
                    <property name="defaultMaxLength">10485760</property><!-- 10M -->
                    <postConstruct name="addMaxLength">
                            <arg>"text/html"</arg>
                            <arg>2621440</arg><!-- 2.5M -->
                    </postConstruct>
            </component>
    </components>

**Anpassungsbeispiel (PDF-Dateien bis zu 5 MB verarbeiten):**

::

                    <postConstruct name="addMaxLength">
                            <arg>"application/pdf"</arg>
                            <arg>5242880</arg><!-- 5M -->
                    </postConstruct>

Fügt Konfiguration für PDF-Dateien bis zu 5 MB hinzu.

.. warning::
   Bei größeren Dateigrößen erhöhen Sie auch die Crawler-Speichereinstellungen.

.. note::
   Wenn die Dokumentgröße 50 MB überschreitet, müssen Sie auch die OpenSearch-Einstellungen ändern.
   OpenSearch begrenzt die maximale Länge von Zeichenfolgenfeldern in JSON-Inhalten standardmäßig auf 50 MB.

   Fügen Sie Folgendes zu ``opensearch.yml`` hinzu:

   ::

       opensearch.xcontent.string.length.max: 104857600

   Das obige Beispiel setzt das Limit auf 100 MB. Weitere Details finden Sie in der `OpenSearch-Dokumentation <https://docs.opensearch.org/latest/install-and-configure/install-opensearch/index/#important-system-properties>`_.

Längenbeschränkung für Wörter
==============

Übersicht
----

Lange Zeichenfolgen nur aus alphanumerischen Zeichen oder aufeinanderfolgende Symbole verursachen Indexgrößen-Zunahme und Leistungsverschlechterung.
Daher setzt |Fess| standardmäßig folgende Beschränkungen:

- **Aufeinanderfolgende alphanumerische Zeichen**: Bis zu 20 Zeichen
- **Aufeinanderfolgende Symbole**: Bis zu 10 Zeichen

Konfigurationsmethode
--------

Bearbeiten Sie ``fess_config.properties``.

**Standardkonfiguration:**

::

    crawler.document.max.alphanum.term.size=20
    crawler.document.max.symbol.term.size=10

**Beispiel: Lockerung der Beschränkung**

::

    crawler.document.max.alphanum.term.size=50
    crawler.document.max.symbol.term.size=20

.. note::
   Wenn Sie nach langen alphanumerischen Zeichenfolgen suchen müssen (z. B. Seriennummern, Tokens),
   erhöhen Sie diesen Wert. Beachten Sie jedoch, dass die Indexgröße zunimmt.

Proxy-Konfiguration
==============

Übersicht
----

Beim Crawlen externer Sites aus einem Intranet kann die Verbindung durch eine Firewall blockiert werden.
In diesem Fall crawlen Sie über einen Proxy-Server.

Konfigurationsmethode
--------

Fügen Sie in der Verwaltungsoberfläche in der Crawl-Konfiguration unter „Konfigurationsparameter" Folgendes hinzu.

**Grundlegende Proxy-Konfiguration:**

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080

**Proxy mit Authentifizierung:**

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080
    client.proxyUsername=proxyuser
    client.proxyPassword=proxypass

**Bestimmte Hosts vom Proxy ausschließen:**

Hosts, die vom Proxy ausgeschlossen werden sollen, werden nicht in den Konfigurationsparametern der Crawl-Konfiguration, sondern über JVM-Systemeigenschaften konfiguriert.
Setzen Sie die Umgebungsvariable ``FESS_NON_PROXY_HOSTS`` in ``fess.in.sh`` (Linux/Mac) oder ``fess.in.bat`` (Windows).

::

    export FESS_NON_PROXY_HOSTS="localhost|127.0.0.1|*.example.com"

Proxy gemeinsam für alle Crawl-Konfigurationen
----------------------------------------------

Wenn kein Proxy in einer einzelnen Crawl-Konfiguration angegeben ist, wird ein gemeinsamer
Crawler-Proxy aus ``fess_config.properties`` verwendet:

::

    http.proxy.host=proxy.example.com
    http.proxy.port=8080
    http.proxy.username=proxyuser
    http.proxy.password=proxypass

Diese Einstellung gilt für alle Crawl-Konfigurationen, die keinen eigenen Proxy festlegen
(wenn ``client.proxyHost`` / ``client.proxyPort`` in einer Crawl-Konfiguration gesetzt sind,
haben diese Werte Vorrang).

Systemweite Proxy-Konfiguration (JVM)
--------------------------------------

Um nicht nur den Crawler, sondern den gesamten HTTP-Verkehr von |Fess|
(Crawler, SSO, LLM-Integration usw.) über einen Proxy zu leiten,
setzen Sie folgende Umgebungsvariablen in ``fess.in.sh`` (Linux/Mac) bzw. ``fess.in.bat`` (Windows).
Diese werden in JVM-Systemeigenschaften (``-Dhttp.proxyHost`` usw.) umgewandelt:

::

    export FESS_PROXY_HOST=proxy.example.com
    export FESS_PROXY_PORT=8080
    export FESS_NON_PROXY_HOSTS="localhost|127.0.0.1|*.example.com"

.. note::
   ``FESS_PROXY_HOST`` / ``FESS_PROXY_PORT`` gelten sowohl für HTTP als auch für HTTPS.
   Die Shell-Umgebungsvariablen ``http_proxy`` / ``https_proxy`` / ``no_proxy`` werden von der JVM
   nicht ausgewertet und haben daher keine Wirkung.

Konfiguration von robots.txt
=================

Übersicht
----

robots.txt ist eine Datei, die Crawlern anweist, ob das Crawlen erlaubt ist.
|Fess| befolgt standardmäßig robots.txt.

Konfigurationsmethode
--------

Um robots.txt zu ignorieren, bearbeiten Sie ``fess_config.properties``.

::

    crawler.ignore.robots.txt=true

Der Standardwert dieses Eintrags ist ``false``: |Fess| hält sich an robots.txt.
Mit ``true`` wird robots.txt ignoriert.

Um auch HTML-Robots-Meta-Tags (``noindex``, ``nofollow`` usw.) zu ignorieren, verwenden Sie folgenden Eintrag (Standard: ``false``):

::

    crawler.ignore.robots.tags=true

.. warning::
   Beim Crawlen externer Sites befolgen Sie robots.txt.
   Das Ignorieren kann übermäßige Last auf Server ausüben oder gegen Nutzungsbedingungen verstoßen.

Konfiguration des User-Agent
=================

Sie können den User-Agent des Crawlers ändern.

Für den Web-Crawler
-------------------

Der Web-Crawler verfügt über ein dediziertes Feld „User Agent" in der Bearbeitungsmaske der Crawl-Konfiguration.
Tragen Sie dort den gewünschten User-Agent-String ein:

::

    User Agent: MyCompanyCrawler/1.0

.. note::
   Bei Web-Crawl-Konfigurationen wird der Wert von ``client.userAgent`` in den Konfigurationsparametern
   durch das dedizierte Feld „User Agent" überschrieben.
   Verwenden Sie für den Web-Crawler stets das dedizierte Feld.

Für den Datei-Crawler und andere
---------------------------------

Crawler ohne dediziertes User-Agent-Feld konfigurieren Sie über die „Konfigurationsparameter"
der Crawl-Konfiguration:

::

    client.userAgent=MyCompanyCrawler/1.0

Codierungs-Konfiguration
====================

Codierung von Crawl-Daten
--------------------------------

Konfigurieren Sie in ``fess_config.properties``:

::

    crawler.crawling.data.encoding=UTF-8

Codierung von Dateinamen
----------------------------

Codierung von Dateinamen im Dateisystem:

::

    crawler.document.file.name.encoding=

Fehlersuche beim Crawling
================================

Crawling startet nicht
----------------------

**Überprüfungspunkte:**

1. Überprüfen Sie, ob der Scheduler aktiviert ist

   - Überprüfen Sie im Menü „Scheduler", ob der Job „Default Crawler" aktiviert ist

2. Überprüfen Sie, ob die Crawl-Konfiguration aktiviert ist

   - Überprüfen Sie in der Crawl-Konfigurationsliste, ob die Zielkonfiguration aktiviert ist

3. Überprüfen Sie Protokolle

   ::

       tail -f /var/log/fess/fess.log
       tail -f /var/log/fess/fess-crawler.log

Crawling stoppt mittendrin
------------------------

**Mögliche Ursachen:**

1. **Speichermangel**

   - Überprüfen Sie ``fess-crawler.log`` auf ``OutOfMemoryError``
   - Erhöhen Sie den Crawler-Speicher (Details siehe :doc:`setup-memory`)

2. **Netzwerkfehler**

   - Passen Sie Timeouts über die Konfigurationsparameter an:

     ::

         client.connectionTimeout=5000
         client.soTimeout=30000

     ``client.connectionTimeout`` ist der Timeout für den Verbindungsaufbau,
     ``client.soTimeout`` der Timeout für den Datenempfang; beide Angaben in Millisekunden.

3. **Fehler im Crawl-Ziel**

   - Überprüfen Sie, ob viele 404-Fehler auftreten
   - Überprüfen Sie Fehlerdetails im Protokoll

Bestimmte Seiten werden nicht gecrawlt
------------------------------

**Überprüfungspunkte:**

1. **URL-Muster überprüfen**

   - Überprüfen Sie, ob URL dem Ausschlussmuster entspricht

2. **robots.txt überprüfen**

   - Überprüfen Sie ``/robots.txt`` der Ziel-Site

3. **Authentifizierung überprüfen**

   - Bei Seiten, die Authentifizierung erfordern, überprüfen Sie Authentifizierungseinstellungen

4. **Tiefenbeschränkung**

   - Überprüfen Sie, ob Hierarchietiefe der Links die Tiefenbeschränkung überschreitet

5. **Maximale Zugriffszahl**

   - Überprüfen Sie, ob maximale Zugriffszahl erreicht wurde

Crawling ist langsam
--------------

**Gegenmaßnahmen:**

1. **Thread-Anzahl erhöhen**

   - Erhöhen Sie Anzahl paralleler Crawls (beachten Sie jedoch Last auf Zielserver)

2. **Unnötige URLs ausschließen**

   - Fügen Sie Bilder, CSS-Dateien usw. zu Ausschlussmustern hinzu

3. **Timeout-Einstellungen anpassen**

   - Bei langsamen Sites verkürzen Sie Timeout

4. **Crawler-Speicher erhöhen**

   - Details siehe :doc:`setup-memory`

Best Practices
==================

Empfehlungen für Crawl-Konfiguration
----------------------

1. **Angemessene Thread-Anzahl konfigurieren**

   Konfigurieren Sie angemessene Thread-Anzahl, um Zielserver nicht übermäßig zu belasten.

2. **URL-Muster optimieren**

   Durch Ausschluss unnötiger Dateien (Bilder, CSS, JavaScript usw.)
   verkürzen Sie Crawl-Zeit und verbessern Indexqualität.

3. **Tiefenbeschränkung konfigurieren**

   Konfigurieren Sie angemessene Tiefe entsprechend der Site-Struktur.
   Das leere Feld (unbegrenzt) nur zum Crawlen der gesamten Site verwenden.

4. **Maximale Zugriffszahl konfigurieren**

   Legen Sie Obergrenze fest, um unerwartetes Crawlen großer Seitenmengen zu vermeiden.

5. **Crawl-Intervall anpassen**

   Konfigurieren Sie angemessenes Intervall entsprechend der Aktualisierungshäufigkeit.
   - Häufig aktualisierte Sites: Jede Stunde bis alle paar Stunden
   - Selten aktualisierte Sites: Täglich bis wöchentlich

Empfehlungen für Zeitplankonfiguration
--------------------------

1. **Nächtliche Ausführung**

   Führen Sie zu Zeiten niedriger Serverlast aus (z. B. 2 Uhr nachts).

2. **Vermeidung doppelter Ausführung**

   Konfigurieren Sie, dass der nächste Crawl erst nach Abschluss des vorherigen startet.

3. **Benachrichtigung bei Fehlern**

   Konfigurieren Sie E-Mail-Benachrichtigung bei Crawl-Fehlern.

Referenzinformationen
========

- :doc:`crawler-advanced` - Erweiterte Crawler-Konfiguration
- :doc:`crawler-thumbnail` - Thumbnail-Konfiguration
- :doc:`setup-memory` - Speicherkonfiguration
- :doc:`admin-logging` - Protokollkonfiguration
- :doc:`../admin/webconfig-guide` - Web-Crawl (Website-Suche)
- :doc:`../admin/fileconfig-guide` - Datei-Crawl (Dateiserver-Suche)
- :doc:`../admin/dataconfig-guide` - Datenspeicher-Crawl (Datenbank-Suche)
- :doc:`datastore/index` - Datenspeicher-Konnektoren Leitfaden
- :doc:`search-basic` - Suchfunktionen
- :doc:`datastore/ds-overview` - Übersicht Datenspeicher-Crawling (Datenbanken und andere Datenquellen)
- :doc:`datastore/ds-database` - Datenbank-Crawling-Konfiguration
- :doc:`rank-fusion` - Hybride Suche und Rank Fusion
