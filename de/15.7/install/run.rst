====================
Start, Stopp, Erstkonfiguration
====================

Diese Seite beschreibt die Verfahren zum Starten, Stoppen und zur Ersteinrichtung des |Fess|-Servers.

.. important::

   Starten Sie vor dem Start von |Fess| unbedingt OpenSearch.
   Wenn OpenSearch nicht läuft, funktioniert |Fess| nicht ordnungsgemäß.

Startmethoden
=============

Die Startverfahren unterscheiden sich je nach Installationsmethode.

TAR.GZ-Version
--------------

Start von OpenSearch
~~~~~~~~~~~~~~~~~~~~

::

    $ cd /path/to/opensearch-3.7.0
    $ ./bin/opensearch

Für Hintergrundstart::

    $ ./bin/opensearch -d

Start von Fess
~~~~~~~~~~~~~~

::

    $ cd /path/to/fess-15.7.0
    $ ./bin/fess

Für Hintergrundstart::

    $ ./bin/fess -d

.. note::

   Der Start kann einige Minuten dauern.
   Der Startstatus kann in der Protokolldatei (``logs/fess.log``) überprüft werden.

ZIP-Version (Windows)
---------------------

Start von OpenSearch
~~~~~~~~~~~~~~~~~~~~

1. Öffnen Sie das OpenSearch-Installationsverzeichnis
2. Doppelklicken Sie auf ``opensearch.bat`` im ``bin``-Ordner

Oder von der Eingabeaufforderung::

    C:\> cd C:\opensearch-3.7.0
    C:\opensearch-3.7.0> bin\opensearch.bat

Start von Fess
~~~~~~~~~~~~~~

1. Öffnen Sie das Fess-Installationsverzeichnis
2. Doppelklicken Sie auf ``fess.bat`` im ``bin``-Ordner

Oder von der Eingabeaufforderung::

    C:\> cd C:\fess-15.7.0
    C:\fess-15.7.0> bin\fess.bat

RPM/DEB-Version (chkconfig)
----------------------------

Start von OpenSearch::

    $ sudo service opensearch start

Start von Fess::

    $ sudo service fess start

Überprüfung des Startstatus::

    $ sudo service fess status

RPM/DEB-Version (systemd)
--------------------------

Start von OpenSearch::

    $ sudo systemctl start opensearch.service

Start von Fess::

    $ sudo systemctl start fess.service

Überprüfung des Startstatus::

    $ sudo systemctl status fess.service

Aktivierung des automatischen Starts::

    $ sudo systemctl enable opensearch.service
    $ sudo systemctl enable fess.service

Docker-Version
--------------

.. note::

   ``compose.yaml`` und ``compose-opensearch3.yaml`` sind nicht im Lieferumfang von |Fess| selbst enthalten. Sie werden vom docker-fess-Projekt (https://github.com/codelibs/docker-fess) bereitgestellt. Laden Sie das Repository herunter und führen Sie die folgenden Befehle im Verzeichnis ``compose`` aus.

Start mit Docker Compose::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Überprüfung des Startstatus::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

Überprüfung der Protokolle::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01

Überprüfung des Starts
======================

Überprüfen Sie, dass |Fess| erfolgreich gestartet wurde.

Gesundheitsprüfung
------------------

Greifen Sie über den Browser oder mit dem curl-Befehl auf folgende URL zu::

    http://localhost:8080/

Bei erfolgreichem Start wird die Fess-Suchseite angezeigt.

Überprüfung über die Kommandozeile::

    $ curl -I http://localhost:8080/

Wenn ``HTTP/1.1 200 OK`` zurückgegeben wird, ist der Start erfolgreich.

Überprüfung der Protokolle
---------------------------

Überprüfen Sie die Startprotokolle und stellen Sie sicher, dass keine Fehler vorliegen.

TAR.GZ/ZIP-Version::

    $ tail -f /path/to/fess-15.7.0/logs/fess.log

RPM/DEB-Version::

    $ sudo tail -f /var/log/fess/fess.log

Oder mit journalctl::

    $ sudo journalctl -u fess.service -f

Docker-Version::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01

.. tip::

   Wenn der Start erfolgreich abgeschlossen wurde, wird auf der Konsole und in der Protokolldatei eine Startabschlussmeldung wie die folgende angezeigt:

   ::

       ...Booting the Tomcat: port=8080 contextPath=/
       ...
       Boot successful: url -> http://localhost:8080

Zugriff über den Browser
=========================

Greifen Sie auf folgende URLs zu und überprüfen Sie die Weboberfläche.

Suchseite
---------

**URL**: http://localhost:8080/

Die Fess-Suchseite wird angezeigt. Im Ausgangszustand werden keine Suchergebnisse angezeigt, da noch keine Crawl-Konfiguration vorgenommen wurde.

Verwaltungsseite
----------------

**URL**: http://localhost:8080/admin

Standard-Administratorkonto:

- **Benutzername**: ``admin``
- **Passwort**: ``admin``

.. warning::

   **Wichtiger Sicherheitshinweis**

   Ändern Sie unbedingt das Standardpasswort.
   Besonders in Produktionsumgebungen wird dringend empfohlen, das Passwort unmittelbar nach der ersten Anmeldung zu ändern.

Erstkonfiguration
=================

Nach Anmeldung in der Verwaltungsseite führen Sie folgende Erstkonfigurationen durch.

Schritt 1: Änderung des Administratorpassworts
-----------------------------------------------

1. Anmeldung in der Verwaltungsseite (http://localhost:8080/admin)
2. Klicken Sie im linken Menü auf „System" → „Benutzer"
3. Klicken Sie auf den Benutzer ``admin``
4. Geben Sie ein neues Passwort in das Feld [Passwort] ein
5. Geben Sie dasselbe Passwort erneut in das Feld [Passwort (bestätigen)] ein
6. Klicken Sie auf die Schaltfläche [Aktualisieren]

.. important::

   Es wird empfohlen, dass Passwörter folgende Bedingungen erfüllen:

   - 8 Zeichen oder mehr (die erforderliche Mindestlänge, festgelegt durch ``password.min.length``)
   - Kombination aus Groß- und Kleinbuchstaben, Zahlen und Sonderzeichen
   - Nicht leicht zu erraten

   Standardmäßig wird nur die Mindestlänge (8 Zeichen) geprüft; eine Kombination aus verschiedenen Zeichentypen wird nicht erzwungen. Anforderungen an Zeichentypen können mit Einstellungen wie ``password.require.uppercase`` aktiviert werden.

Schritt 2: Erstellung der Crawl-Konfiguration
----------------------------------------------

Erstellen Sie eine Konfiguration zum Crawlen der zu durchsuchenden Websites oder Dateisysteme.

1. Klicken Sie im linken Menü auf „Crawler" → „Web"
2. Klicken Sie auf die Schaltfläche „Neu erstellen"
3. Geben Sie die erforderlichen Informationen ein:

   - **Name**: Name der Crawl-Konfiguration (z.B.: Firmen-Website)
   - **URL**: Ziel-URL für das Crawling (z.B.: https://www.example.com/). Um mehrere URLs anzugeben, geben Sie eine URL pro Zeile ein
   - **Maximale Zugriffe**: Maximale Anzahl der zu crawlenden Dokumente (optional)
   - **Intervall**: Wartezeit zwischen den Zugriffen (Millisekunden; Standard: ``10000``)

   .. note::

      Andere Felder (wie Benutzeragent, Anzahl der Threads und Tiefe) verwenden
      ihre Standardwerte, wenn sie leer gelassen werden.

4. Klicken Sie auf die Schaltfläche „Erstellen"

Schritt 3: Ausführung des Crawls
---------------------------------

1. Klicken Sie im linken Menü auf [System] → [Scheduler]
2. Öffnen Sie den Job [Default Crawler] und klicken Sie auf die Schaltfläche „Jetzt starten"
3. Warten Sie, bis der Crawl abgeschlossen ist (Fortschritt kann im Dashboard überprüft werden)

Schritt 4: Überprüfung der Suche
---------------------------------

1. Greifen Sie auf die Suchseite zu (http://localhost:8080/)
2. Geben Sie ein Suchwort ein
3. Überprüfen Sie, dass Suchergebnisse angezeigt werden

.. note::

   Das Crawlen kann Zeit in Anspruch nehmen.
   Bei großen Websites kann es mehrere Stunden bis Tage dauern.

Weitere empfohlene Einstellungen
=================================

Bei Betrieb in Produktionsumgebungen sollten Sie auch folgende Einstellungen in Betracht ziehen.

Haupteinstellungen über Umgebungsvariablen
------------------------------------------

Einstellungen wie Portnummer, JVM-Heap-Größe und die OpenSearch-Verbindungs-URL können über Umgebungsvariablen geändert werden. Bearbeiten Sie ``bin/fess.in.sh`` für die TAR.GZ-Version, ``/etc/sysconfig/fess`` für die RPM-Version und ``/etc/default/fess`` für die DEB-Version. Nach Änderungen ist ein Neustart von |Fess| erforderlich.

.. list-table::
   :widths: 30 25 45
   :header-rows: 1

   * - Umgebungsvariable
     - Standardwert
     - Beschreibung
   * - ``FESS_PORT``
     - ``8080``
     - Der HTTP-Port, auf dem |Fess| lauscht.
   * - ``FESS_HEAP_SIZE``
     - (nicht gesetzt)
     - JVM-Heap-Größe. Setzt denselben Wert für Minimum und Maximum. Wenn nicht gesetzt, werden mindestens ``256m`` und maximal ``2g`` verwendet (die Windows-ZIP-Version verwendet maximal ``1g``); die RPM/DEB-Version verwendet ``512m``.
   * - ``SEARCH_ENGINE_HTTP_URL``
     - (nicht gesetzt)
     - URL des OpenSearch, zu dem eine Verbindung hergestellt wird. Wenn nicht gesetzt, wird der eingebaute Standardwert ``http://localhost:9201`` verwendet. Ändern Sie dies, wenn OpenSearch auf einem anderen Port oder Host läuft (das Verfahren :doc:`install-linux` setzt diesen Wert auf ``http://localhost:9200``, um dem OpenSearch-Lauschport zu entsprechen). Die RPM/DEB-Version setzt ``http://localhost:9200`` standardmäßig über die Paketumgebungsdatei.
   * - ``FESS_LOG_LEVEL``
     - ``warn``
     - Protokollniveau von |Fess|.

.. note::

   Die Datei ``bin\fess.in.bat`` der Windows-ZIP-Version liest diese Umgebungsvariablen nicht (außer den Proxy-bezogenen). Die Werte werden direkt in der Datei eingetragen; bearbeiten Sie daher ``bin\fess.in.bat`` direkt, um sie zu ändern.

Konfiguration des Mail-Servers
-------------------------------

Um Fehlermeldungen und ähnliche Nachrichten per E-Mail zu erhalten, konfigurieren Sie den SMTP-Server und die Empfängeradresse für Benachrichtigungen.

1. Geben Sie in der Konfigurationsdatei ``app/WEB-INF/classes/fess_env.properties`` den SMTP-Serverhost und -port in ``mail.smtp.server.main.host.and.port`` an (Standard: ``localhost:25``). Nach der Änderung ist ein Neustart von |Fess| erforderlich.
2. Klicken Sie in der Administrator-Oberfläche im linken Menü auf [System] → [Allgemein].
3. Geben Sie die Empfänger-E-Mail-Adresse in das Feld [Benachrichtigungs-E-Mail] ein.
4. Klicken Sie auf die Schaltfläche [Aktualisieren].
5. Mit der Schaltfläche [Test-E-Mail senden] können Sie überprüfen, ob E-Mails korrekt versendet werden.

Zeitzoneneinstellung
--------------------

|Fess| verwendet die Zeitzone des Servers (Betriebssystem / JVM). Es gibt keine Einstellung zur Änderung der Zeitzone in der Administrator-Oberfläche. Um sie zu ändern, passen Sie die Zeitzoneneinstellung des Betriebssystems an oder fügen Sie die JVM-Option ``-Duser.timezone=Asia/Tokyo`` zu ``FESS_JAVA_OPTS`` in ``bin/fess.in.sh`` hinzu (unter Windows: ``bin\fess.in.bat``).

Anpassung des Protokollniveaus
-------------------------------

In Produktionsumgebungen kann das Protokollniveau angepasst werden, um die Festplattennutzung zu reduzieren.

Das Gesamtprotokollniveau von |Fess| kann mit der Umgebungsvariable ``FESS_LOG_LEVEL`` geändert werden (Standard: ``warn``). Zur detaillierten Steuerung einzelner Logger bearbeiten Sie die Konfigurationsdatei ``app/WEB-INF/classes/log4j2.xml``. Crawling, Vorschläge und die Thumbnail-Generierung laufen als separate Prozesse; konfigurieren Sie deren Protokollniveaus daher separat in ``app/WEB-INF/env/{crawler,suggest,thumbnail}/resources/log4j2.xml``.

Weitere Informationen finden Sie unter :doc:`../admin/index`.

Stoppmethoden
=============

TAR.GZ/ZIP-Version
------------------

Stoppen von Fess
~~~~~~~~~~~~~~~~

Beenden Sie den Prozess mit kill::

    $ ps aux | grep fess
    $ kill <PID>

Oder stoppen Sie über die Konsole mit ``Ctrl+C`` (bei Vordergrundausführung).

Stoppen von OpenSearch::

    $ ps aux | grep opensearch
    $ kill <PID>

RPM/DEB-Version (chkconfig)
----------------------------

Stoppen von Fess::

    $ sudo service fess stop

Stoppen von OpenSearch::

    $ sudo service opensearch stop

RPM/DEB-Version (systemd)
--------------------------

Stoppen von Fess::

    $ sudo systemctl stop fess.service

Stoppen von OpenSearch::

    $ sudo systemctl stop opensearch.service

Docker-Version
--------------

Stoppen der Container::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop

Stoppen und Löschen der Container::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   Zum Löschen auch der Volumes mit dem Befehl ``down`` fügen Sie die Option ``-v`` hinzu.
   In diesem Fall werden alle Daten gelöscht, seien Sie also vorsichtig.

Neustartmethoden
================

TAR.GZ/ZIP-Version
------------------

Stoppen Sie zuerst und starten Sie dann neu.

RPM/DEB-Version
---------------

chkconfig::

    $ sudo service fess restart

systemd::

    $ sudo systemctl restart fess.service

Docker-Version
--------------

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml restart

Fehlerbehebung
==============

Wenn es nicht startet
---------------------

1. **Überprüfen Sie, ob OpenSearch läuft**

   ::

       $ curl http://localhost:9200/

   Wenn OpenSearch nicht läuft, starten Sie zunächst OpenSearch.

2. **Überprüfen Sie Portnummer-Konflikte**

   ::

       $ sudo netstat -tuln | grep 8080

   Wenn Port 8080 bereits verwendet wird, ändern Sie die Portnummer:

   - TAR.GZ-Version: Ändern Sie ``FESS_PORT`` in ``bin/fess.in.sh``
   - ZIP-Version (Windows): Bearbeiten Sie ``-Dfess.port=8080`` direkt in ``bin\fess.in.bat``
   - RPM-Version: Ändern Sie ``FESS_PORT`` in ``/etc/sysconfig/fess``
   - DEB-Version: Ändern Sie ``FESS_PORT`` in ``/etc/default/fess``

3. **Überprüfen Sie die Protokolle**

   Identifizieren Sie das Problem anhand der Fehlermeldungen.

4. **Überprüfen Sie die Java-Version**

   ::

       $ java -version

   Vergewissern Sie sich, dass Java 21 oder höher installiert ist.

Detaillierte Fehlerbehebung finden Sie unter :doc:`troubleshooting`.

Nächste Schritte
================

Nach erfolgreichem Start von |Fess| beginnen Sie den Betrieb unter Bezugnahme auf folgende Dokumentation:

- :doc:`../admin/index` - Details zu Crawl-Konfiguration, Such-Konfiguration und Systemeinstellungen
- :doc:`security` - Sicherheitseinstellungen für Produktionsumgebungen
- :doc:`troubleshooting` - Häufige Probleme und Lösungen
- :doc:`upgrade` - Upgrade-Verfahren
- :doc:`uninstall` - Deinstallationsverfahren
