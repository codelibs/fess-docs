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

    $ cd /path/to/opensearch-3.3.2
    $ ./bin/opensearch

Für Hintergrundstart::

    $ ./bin/opensearch -d

Start von Fess
~~~~~~~~~~~~~~

::

    $ cd /path/to/fess-15.4.0
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

    C:\> cd C:\opensearch-3.3.2
    C:\opensearch-3.3.2> bin\opensearch.bat

Start von Fess
~~~~~~~~~~~~~~

1. Öffnen Sie das Fess-Installationsverzeichnis
2. Doppelklicken Sie auf ``fess.bat`` im ``bin``-Ordner

Oder von der Eingabeaufforderung::

    C:\> cd C:\fess-15.4.0
    C:\fess-15.4.0> bin\fess.bat

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

Start mit Docker Compose::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Überprüfung des Startstatus::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

Überprüfung der Protokolle::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess

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

    $ tail -f /path/to/fess-15.4.0/logs/fess.log

RPM/DEB-Version::

    $ sudo tail -f /var/log/fess/fess.log

Oder mit journalctl::

    $ sudo journalctl -u fess.service -f

Docker-Version::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess

.. tip::

   Bei erfolgreichem Start wird folgende Meldung im Protokoll angezeigt::

       INFO  Boot - Fess is ready.

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
4. Geben Sie ein neues Passwort in das Feld „Passwort" ein
5. Klicken Sie auf die Schaltfläche „Bestätigen"
6. Klicken Sie auf die Schaltfläche „Aktualisieren"

.. important::

   Es wird empfohlen, dass Passwörter folgende Bedingungen erfüllen:

   - 8 Zeichen oder mehr
   - Kombination aus Groß- und Kleinbuchstaben, Zahlen und Sonderzeichen
   - Nicht leicht zu erraten

Schritt 2: Erstellung der Crawl-Konfiguration
----------------------------------------------

Erstellen Sie eine Konfiguration zum Crawlen der zu durchsuchenden Websites oder Dateisysteme.

1. Klicken Sie im linken Menü auf „Crawler" → „Web"
2. Klicken Sie auf die Schaltfläche „Neu erstellen"
3. Geben Sie die erforderlichen Informationen ein:

   - **Name**: Name der Crawl-Konfiguration (z.B.: Firmen-Website)
   - **URL**: URL des Crawl-Ziels (z.B.: https://www.example.com/)
   - **Maximale Zugriffe**: Obergrenze der zu crawlenden Seiten
   - **Intervall**: Crawl-Intervall (Millisekunden)

4. Klicken Sie auf die Schaltfläche „Erstellen"

Schritt 3: Ausführung des Crawls
---------------------------------

1. Klicken Sie im linken Menü auf „System" → „Scheduler"
2. Klicken Sie auf die Schaltfläche „Jetzt starten" beim Job „Default Crawler"
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

Konfiguration des Mail-Servers
-------------------------------

Konfigurieren Sie einen Mail-Server, um Störungsmeldungen und Berichte per E-Mail zu erhalten.

1. Klicken Sie im linken Menü auf „System" → „Allgemein"
2. Klicken Sie auf den Tab „E-Mail"
3. Geben Sie die SMTP-Serverinformationen ein
4. Klicken Sie auf die Schaltfläche „Aktualisieren"

Zeitzoneneinstellung
--------------------

1. Klicken Sie im linken Menü auf „System" → „Allgemein"
2. Setzen Sie „Zeitzone" auf einen geeigneten Wert (z.B.: Europe/Berlin)
3. Klicken Sie auf die Schaltfläche „Aktualisieren"

Anpassung des Protokollniveaus
-------------------------------

In Produktionsumgebungen kann das Protokollniveau angepasst werden, um die Festplattennutzung zu reduzieren.

Bearbeiten Sie die Konfigurationsdatei (``app/WEB-INF/classes/log4j2.xml``).

Weitere Informationen finden Sie im Administratorhandbuch.

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

   Wenn Port 8080 bereits verwendet wird, ändern Sie die Portnummer in der Konfigurationsdatei.

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

- **Administratorhandbuch**: Details zu Crawl-Konfiguration, Such-Konfiguration und Systemeinstellungen
- :doc:`security` - Sicherheitseinstellungen für Produktionsumgebungen
- :doc:`troubleshooting` - Häufige Probleme und Lösungen
- :doc:`upgrade` - Upgrade-Verfahren
- :doc:`uninstall` - Deinstallationsverfahren
