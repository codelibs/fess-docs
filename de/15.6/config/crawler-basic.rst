====================
Grundlegende Crawler-Konfiguration
====================

Übersicht
====

Der Crawler von |Fess| ist eine Funktion, die automatisch Inhalte von Websites, Dateisystemen usw. sammelt und im Suchindex registriert.
Dieser Leitfaden erläutert die grundlegenden Konzepte und Konfigurationsmethoden des Crawlers.

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
   - **Crawl-Intervall**: Häufigkeit der Crawl-Ausführung (z. B. jede Stunde)
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
    Tiefe: Unbegrenzt (-1)
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
    Tiefe: Unbegrenzt (-1)

SMB/CIFS (Windows-Dateifreigabe)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    Name: Dateiserver
    URL: smb://fileserver.example.com/share/
    Crawl-Intervall: Einmal täglich
    Thread-Anzahl: 5
    Tiefe: Unbegrenzt (-1)

Konfiguration von Authentifizierungsinformationen
--------------

Für Sites oder Dateiserver, die Authentifizierung erfordern, konfigurieren Sie Authentifizierungsinformationen.

1. Wählen Sie in der Verwaltungsoberfläche „Crawler" → „Authentifizierung"
2. Klicken Sie auf „Neu erstellen"
3. Geben Sie Authentifizierungsinformationen ein:

   ::

       Hostname: wiki.example.com
       Port: 443
       Authentifizierungsmethode: Basic-Authentifizierung
       Benutzername: crawler_user
       Passwort: ********

4. Klicken Sie auf „Erstellen"

Ausführung des Crawlings
==============

Manuelle Ausführung
--------

Um einen konfigurierten Crawl sofort auszuführen:

1. Wählen Sie die Zielkonfiguration in der Crawl-Konfigurationsliste
2. Klicken Sie auf die Schaltfläche „Starten"
3. Überprüfen Sie den Job-Ausführungsstatus im Menü „Scheduler"

Geplante Ausführung
----------------

Um Crawls regelmäßig auszuführen:

1. Öffnen Sie das Menü „Scheduler"
2. Wählen Sie den Job „Default Crawler"
3. Konfigurieren Sie den Zeitplanausdruck (Cron-Format)

   ::

       # Täglich um 2 Uhr morgens ausführen
       0 0 2 * * ?

       # Jede Stunde zur vollen Stunde ausführen
       0 0 * * * ?

       # Montag bis Freitag um 18 Uhr ausführen
       0 0 18 ? * MON-FRI

4. Klicken Sie auf „Aktualisieren"

Überprüfung des Crawl-Status
------------------

Überprüfung des Status laufender Crawls:

1. Öffnen Sie das Menü „Scheduler"
2. Überprüfen Sie laufende Jobs
3. Überprüfen Sie Details im Protokoll:

   ::

       tail -f /var/log/fess/fess_crawler.log

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
- **-1**: Unbegrenzt (allen Links folgen)

Maximale Zugriffszahl
~~~~~~~~~~~~~~

Obergrenze für die Anzahl zu crawlender Seiten:

::

    Maximale Zugriffszahl: 1000

Stoppt nach dem Crawlen von 1000 Seiten.

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

Crawl-Intervall
------------

Gibt die Häufigkeit der Crawl-Ausführung an.

::

    # Zeitangabe
    Crawl-Intervall: 3600000  # Millisekunden (1 Stunde)

    # Oder im Scheduler konfigurieren
    0 0 2 * * ?  # Täglich um 2 Uhr morgens

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
                    <postConstruct name="addMaxLength">
                            <arg>"application/pdf"</arg>
                            <arg>5242880</arg><!-- 5M -->
                    </postConstruct>
            </component>
    </components>

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

::

    client.nonProxyHosts=localhost|127.0.0.1|*.example.com

Systemweite Proxy-Konfiguration
--------------------------

Wenn alle Crawl-Konfigurationen denselben Proxy verwenden, können Sie dies über Umgebungsvariablen konfigurieren.

::

    export http_proxy=http://proxy.example.com:8080
    export https_proxy=http://proxy.example.com:8080
    export no_proxy=localhost,127.0.0.1,.example.com

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

.. warning::
   Beim Crawlen externer Sites befolgen Sie robots.txt.
   Das Ignorieren kann übermäßige Last auf Server ausüben oder gegen Nutzungsbedingungen verstoßen.

Konfiguration des User-Agent
=================

Sie können den User-Agent des Crawlers ändern.

Konfiguration in der Verwaltungsoberfläche
----------------

Fügen Sie zu den „Konfigurationsparametern" der Crawl-Konfiguration hinzu:

::

    client.userAgent=MyCompanyCrawler/1.0

Systemweite Konfiguration
------------------

Konfigurieren Sie in ``fess_config.properties``:

::

    crawler.user.agent=MyCompanyCrawler/1.0

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

    crawler.document.file.name.encoding=UTF-8

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
       tail -f /var/log/fess/fess_crawler.log

Crawling stoppt mittendrin
------------------------

**Mögliche Ursachen:**

1. **Speichermangel**

   - Überprüfen Sie ``fess_crawler.log`` auf ``OutOfMemoryError``
   - Erhöhen Sie den Crawler-Speicher (Details siehe :doc:`setup-memory`)

2. **Netzwerkfehler**

   - Passen Sie Timeout-Einstellungen an
   - Überprüfen Sie Retry-Einstellungen

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
   Unbegrenzt (-1) nur zum Crawlen der gesamten Site verwenden.

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
