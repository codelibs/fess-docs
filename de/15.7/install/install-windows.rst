====================================================
Installation unter Windows (Detaillierte Anleitung)
====================================================

Diese Seite beschreibt die Installationsschritte von |Fess| in Windows-Umgebungen.
Sie behandelt die Installationsmethode mit dem ZIP-Paket.

.. warning::

   In Produktionsumgebungen wird der Betrieb mit eingebettetem OpenSearch nicht empfohlen.
   Bitte richten Sie unbedingt einen externen OpenSearch-Server ein.

Voraussetzungen
===============

- Die in :doc:`prerequisites` beschriebenen Systemanforderungen sind erfüllt
- Java 21 ist installiert
- OpenSearch 3.7.0 ist verfügbar (oder wird neu installiert)
- Die Windows-Umgebungsvariable ``JAVA_HOME`` ist korrekt konfiguriert

Überprüfung der Java-Installation
==================================

Öffnen Sie die Eingabeaufforderung oder PowerShell und überprüfen Sie die Java-Version mit folgendem Befehl.

Bei Eingabeaufforderung::

    C:\> java -version

Bei PowerShell::

    PS C:\> java -version

Vergewissern Sie sich, dass Java 21 oder höher angezeigt wird.

Konfiguration der Umgebungsvariablen
=====================================

1. Einstellung der ``JAVA_HOME``-Umgebungsvariablen

   Setzen Sie das Verzeichnis, in dem Java installiert ist, als ``JAVA_HOME``.

   Beispiel::

       JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-21.0.1.12-hotspot

2. Hinzufügen zur ``PATH``-Umgebungsvariablen

   Fügen Sie ``%JAVA_HOME%\bin`` zur ``PATH``-Umgebungsvariablen hinzu.

.. tip::

   So konfigurieren Sie Umgebungsvariablen:

   1. Öffnen Sie „Einstellungen" über das „Start"-Menü
   2. Klicken Sie auf „System" → „Info" → „Erweiterte Systemeinstellungen"
   3. Klicken Sie auf die Schaltfläche „Umgebungsvariablen"
   4. Konfigurieren Sie in „Systemvariablen" oder „Benutzervariablen"

Schritt 1: Installation von OpenSearch
=======================================

Download von OpenSearch
-----------------------

1. Laden Sie das ZIP-Paket für Windows von `Download OpenSearch <https://opensearch.org/downloads.html>`__ herunter.

2. Entpacken Sie die heruntergeladene ZIP-Datei in ein beliebiges Verzeichnis.

   Beispiel::

       C:\opensearch-3.7.0

   .. note::

      Es wird empfohlen, ein Verzeichnis ohne japanische Zeichen oder Leerzeichen im Pfad zu wählen.

Installation der OpenSearch-Plugins
------------------------------------

Öffnen Sie die Eingabeaufforderung **mit Administratorrechten** und führen Sie folgende Befehle aus.

::

    C:\> cd C:\opensearch-3.7.0
    C:\opensearch-3.7.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.7.0
    C:\opensearch-3.7.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.7.0
    C:\opensearch-3.7.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.7.0
    C:\opensearch-3.7.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.7.0

.. important::

   Die Plugin-Version muss mit der OpenSearch-Version übereinstimmen.
   Im obigen Beispiel sind alle auf 3.7.0 gesetzt.

Konfiguration von OpenSearch
-----------------------------

Öffnen Sie ``config\opensearch.yml`` mit einem Texteditor und fügen Sie folgende Einstellungen hinzu.

::

    # Pfad für Konfigurationssynchronisation (als absoluter Pfad angeben)
    configsync.config_path: C:/opensearch-3.7.0/data/config/

    # Deaktivierung des Sicherheits-Plugins (nur Entwicklungsumgebung)
    plugins.security.disabled: true

.. warning::

   **Wichtiger Sicherheitshinweis**

   ``plugins.security.disabled: true`` sollte nur in Entwicklungs- oder Testumgebungen verwendet werden.
   In Produktionsumgebungen aktivieren Sie bitte das Sicherheits-Plugin von OpenSearch und konfigurieren Sie entsprechende Authentifizierungs- und Autorisierungseinstellungen.
   Weitere Informationen finden Sie unter :doc:`security`.

.. note::

   Bei Windows verwenden Sie ``/`` anstelle von ``\`` als Pfadtrennzeichen.
   Schreiben Sie ``C:/opensearch-3.7.0/data/config/`` statt ``C:\opensearch-3.7.0\data\config\``.

.. tip::

   Weitere empfohlene Einstellungen::

       cluster.name: fess-cluster
       node.name: fess-node-1
       network.host: 0.0.0.0
       discovery.type: single-node

.. tip::

   Der Heap-Speicher von OpenSearch wird in ``config\jvm.options`` über ``-Xms`` und ``-Xmx`` konfiguriert.
   Es wird empfohlen, beide Werte gleich zu setzen und dabei weniger als die Hälfte des verfügbaren physischen Speichers sowie weniger als 32 GB zu verwenden.

Schritt 2: Installation von Fess
=================================

Download von Fess
-----------------

1. Laden Sie das ZIP-Paket für Windows von der `Download-Site <https://fess.codelibs.org/de/downloads.html>`__ herunter.

2. Entpacken Sie die heruntergeladene ZIP-Datei in ein beliebiges Verzeichnis.

   Beispiel::

       C:\fess-15.7.0

   .. note::

      Es wird empfohlen, ein Verzeichnis ohne japanische Zeichen oder Leerzeichen im Pfad zu wählen.

Konfiguration von Fess
-----------------------

Öffnen Sie ``bin\fess.in.bat`` mit einem Texteditor.
Am Ende dieser Datei sind Einstellungen für die Verbindung zu einem externen OpenSearch-Cluster bereits als auskommentierte Vorlage vorhanden.

Zustand vor der Änderung (Standardzustand)::

    REM External opensearch cluster
    REM set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.search_engine.http_address=http://localhost:9200
    REM set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.dictionary.path=%SEARCH_ENGINE_HOME%/config/

Entfernen Sie das ``REM `` am Anfang der unteren zwei Zeilen, um den Kommentar aufzuheben, und ändern Sie den Wert von ``fess.dictionary.path`` auf den Konfigurationssynchronisationspfad von OpenSearch.

Zustand nach der Änderung::

    REM External opensearch cluster
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.search_engine.http_address=http://localhost:9200
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.dictionary.path=C:/opensearch-3.7.0/data/config/

.. note::

   - Setzen Sie ``fess.dictionary.path`` auf denselben Pfad, der in ``opensearch.yml`` als ``configsync.config_path`` angegeben ist.
   - Wenn OpenSearch auf einem anderen Host ausgeführt wird, ändern Sie den Hostnamen oder die IP-Adresse in ``fess.search_engine.http_address`` entsprechend.
   - Verwenden Sie ``/`` als Pfadtrennzeichen.
   - Fügen Sie keine neuen ``set FESS_JAVA_OPTS=...``-Zeilen hinzu, sondern heben Sie die vorhandenen Kommentarzeilen auf und bearbeiten Sie diese. Die doppelte Angabe derselben Option kann zu unerwünschtem Verhalten führen.

.. tip::

   Um den Heap-Speicher von |Fess| anzupassen, bearbeiten Sie ``FESS_MIN_MEM`` (Standard: ``256m``) und ``FESS_MAX_MEM`` (Standard: ``1g``) in ``bin\fess.in.bat`` oder setzen Sie die Umgebungsvariable ``FESS_HEAP_SIZE``.

Überprüfung der Installation
-----------------------------

Überprüfen Sie, ob die Konfigurationsdateien korrekt bearbeitet wurden.

In der Eingabeaufforderung::

    C:\> findstr "fess.search_engine.http_address" C:\fess-15.7.0\bin\fess.in.bat
    C:\> findstr "fess.dictionary.path" C:\fess-15.7.0\bin\fess.in.bat

Schritt 3: Start
================

Die Startanleitung finden Sie unter :doc:`run`.

Registrierung als Windows-Dienst (Optional)
============================================

Durch Registrierung von |Fess| als Windows-Dienst kann es beim Systemstart automatisch gestartet werden.

|Fess| enthält das mitgelieferte Skript ``bin\service.bat`` zur Registrierung als Windows-Dienst.
Da dieses Skript Apache Commons Daemon (procrun) verwendet, ist kein zusätzliches Drittanbieter-Tool wie NSSM erforderlich.

.. note::

   Stellen Sie sicher, dass die Umgebungsvariable ``JAVA_HOME`` korrekt gesetzt ist, bevor Sie ``service.bat`` ausführen.

Registrierung des |Fess|-Dienstes
-----------------------------------

Öffnen Sie die Eingabeaufforderung **mit Administratorrechten** und führen Sie folgende Befehle aus.

1. Dienst registrieren::

       C:\> cd C:\fess-15.7.0
       C:\fess-15.7.0> bin\service.bat install

   Standardmäßig wird der Dienst in 64-Bit-Umgebungen als ``fess-service-x64`` und in 32-Bit-Umgebungen als ``fess-service-x86`` registriert.
   Um die Dienst-ID explizit anzugeben, übergeben Sie sie als Argument: ``bin\service.bat install <Dienst-ID>``.

2. Dienst starten und stoppen::

       C:\fess-15.7.0> bin\service.bat start
       C:\fess-15.7.0> bin\service.bat stop

3. Dienstkonfiguration anzeigen und ändern (GUI)::

       C:\fess-15.7.0> bin\service.bat manager

4. Dienst entfernen::

       C:\fess-15.7.0> bin\service.bat remove

.. note::

   - Da ``service.bat`` intern ``bin\fess.in.bat`` lädt, werden die im Abschnitt „Konfiguration von Fess" vorgenommenen Verbindungseinstellungen für den externen OpenSearch-Cluster auch für den Dienst übernommen.
   - Der Standardstarttyp ist „Manuell". Um den Dienst beim Systemstart automatisch zu starten, setzen Sie die Umgebungsvariable ``FESS_START_TYPE`` vor der Registrierung auf ``auto``, oder ändern Sie den Starttyp nach der Registrierung im Dienstverwaltungs-Tool (``services.msc``) auf „Automatisch".
   - Mit ``service.bat`` kann nur der |Fess|-Dienst registriert werden. Informationen zur Registrierung von OpenSearch als Dienst finden Sie in der OpenSearch-Dokumentation.

Firewall-Konfiguration
======================

Öffnen Sie die erforderlichen Ports in der Windows Defender Firewall.

1. Öffnen Sie „Systemsteuerung" → „Windows Defender Firewall" → „Erweiterte Einstellungen"

2. Erstellen Sie eine neue Regel unter „Eingehende Regeln"

   - Regeltyp: Port
   - Protokoll und Ports: TCP, 8080
   - Aktion: Verbindung zulassen
   - Name: Fess Web Interface

Oder führen Sie in PowerShell aus::

    PS C:\> New-NetFirewallRule -DisplayName "Fess Web Interface" -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow

Fehlerbehebung
==============

Portnummer-Konflikt
-------------------

Wenn Port 8080 oder 9200 bereits verwendet wird, können Sie dies mit folgendem Befehl überprüfen::

    C:\> netstat -ano | findstr :8080
    C:\> netstat -ano | findstr :9200

Ändern Sie die verwendete Portnummer oder stoppen Sie den konfliktverursachenden Prozess.

Pfadlängenbeschränkung
----------------------

Windows hat eine Pfadlängenbeschränkung. Es wird empfohlen, in einem möglichst kurzen Pfad zu installieren.

Beispiel::

    C:\opensearch  (empfohlen)
    C:\Program Files\opensearch-3.7.0  (nicht empfohlen - Pfad zu lang)

Java wird nicht erkannt
-----------------------

Wenn der Befehl ``java -version`` einen Fehler anzeigt:

1. Überprüfen Sie, ob die ``JAVA_HOME``-Umgebungsvariable korrekt gesetzt ist
2. Überprüfen Sie, ob ``%JAVA_HOME%\bin`` in der ``PATH``-Umgebungsvariablen enthalten ist
3. Starten Sie die Eingabeaufforderung neu, um die Einstellungen zu übernehmen

Nächste Schritte
================

Nach Abschluss der Installation lesen Sie bitte folgende Dokumentation:

- :doc:`run` - Start und Ersteinrichtung von |Fess|
- :doc:`security` - Sicherheitseinstellungen für Produktionsumgebungen
- :doc:`troubleshooting` - Fehlerbehebung

Häufig gestellte Fragen
=======================

F: Wird der Betrieb auf Windows Server empfohlen?
--------------------------------------------------

A: Ja, der Betrieb auf Windows Server ist möglich.
Bei Betrieb auf Windows Server sollten Sie als Windows-Dienst registrieren und entsprechende Überwachung einrichten.

F: Was ist der Unterschied zwischen 64-Bit- und 32-Bit-Version?
----------------------------------------------------------------

A: |Fess| und OpenSearch unterstützen nur die 64-Bit-Version.
Sie funktionieren nicht auf 32-Bit-Windows.

F: Was tun bei japanischen Zeichen im Pfad?
--------------------------------------------

A: Installieren Sie bitte nach Möglichkeit in einem Pfad ohne japanische Zeichen oder Leerzeichen.
Wenn Sie unbedingt japanische Pfade verwenden müssen, müssen Pfade in den Konfigurationsdateien entsprechend maskiert werden.
