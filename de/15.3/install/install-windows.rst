====================================
Installation unter Windows (Detaillierte Anleitung)
====================================

Diese Seite beschreibt die Installationsschritte von |Fess| in Windows-Umgebungen.
Sie behandelt die Installationsmethode mit dem ZIP-Paket.

.. warning::

   In Produktionsumgebungen wird der Betrieb mit eingebettetem OpenSearch nicht empfohlen.
   Bitte richten Sie unbedingt einen externen OpenSearch-Server ein.

Voraussetzungen
===============

- Die in :doc:`prerequisites` beschriebenen Systemanforderungen sind erfüllt
- Java 21 ist installiert
- OpenSearch 3.3.0 ist verfügbar (oder wird neu installiert)
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

       C:\opensearch-3.3.0

   .. note::

      Es wird empfohlen, ein Verzeichnis ohne japanische Zeichen oder Leerzeichen im Pfad zu wählen.

Installation der OpenSearch-Plugins
------------------------------------

Öffnen Sie die Eingabeaufforderung **mit Administratorrechten** und führen Sie folgende Befehle aus.

::

    C:\> cd C:\opensearch-3.3.0
    C:\opensearch-3.3.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.0
    C:\opensearch-3.3.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.0
    C:\opensearch-3.3.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.0
    C:\opensearch-3.3.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.0

.. important::

   Die Plugin-Version muss mit der OpenSearch-Version übereinstimmen.
   Im obigen Beispiel sind alle auf 3.3.0 gesetzt.

Konfiguration von OpenSearch
-----------------------------

Öffnen Sie ``config\opensearch.yml`` mit einem Texteditor und fügen Sie folgende Einstellungen hinzu.

::

    # Pfad für Konfigurationssynchronisation (als absoluter Pfad angeben)
    configsync.config_path: C:/opensearch-3.3.0/data/config/

    # Deaktivierung des Sicherheits-Plugins (nur Entwicklungsumgebung)
    plugins.security.disabled: true

.. warning::

   **Wichtiger Sicherheitshinweis**

   ``plugins.security.disabled: true`` sollte nur in Entwicklungs- oder Testumgebungen verwendet werden.
   In Produktionsumgebungen aktivieren Sie bitte das Sicherheits-Plugin von OpenSearch und konfigurieren Sie entsprechende Authentifizierungs- und Autorisierungseinstellungen.
   Weitere Informationen finden Sie unter :doc:`security`.

.. note::

   Bei Windows verwenden Sie ``/`` anstelle von ``\`` als Pfadtrennzeichen.
   Schreiben Sie ``C:/opensearch-3.3.0/data/config/`` statt ``C:\opensearch-3.3.0\data\config\``.

.. tip::

   Weitere empfohlene Einstellungen::

       cluster.name: fess-cluster
       node.name: fess-node-1
       network.host: 0.0.0.0
       discovery.type: single-node

Schritt 2: Installation von Fess
=================================

Download von Fess
-----------------

1. Laden Sie das ZIP-Paket für Windows von der `Download-Site <https://fess.codelibs.org/ja/downloads.html>`__ herunter.

2. Entpacken Sie die heruntergeladene ZIP-Datei in ein beliebiges Verzeichnis.

   Beispiel::

       C:\fess-15.3.0

   .. note::

      Es wird empfohlen, ein Verzeichnis ohne japanische Zeichen oder Leerzeichen im Pfad zu wählen.

Konfiguration von Fess
-----------------------

Öffnen Sie ``bin\fess.in.bat`` mit einem Texteditor und fügen Sie folgende Einstellungen hinzu oder ändern Sie sie.

::

    set SEARCH_ENGINE_HTTP_URL=http://localhost:9200
    set FESS_DICTIONARY_PATH=C:/opensearch-3.3.0/data/config/

.. note::

   - Wenn OpenSearch auf einem anderen Host ausgeführt wird, ändern Sie ``SEARCH_ENGINE_HTTP_URL`` auf den entsprechenden Hostnamen oder die IP-Adresse.
   - Verwenden Sie ``/`` als Pfadtrennzeichen.

Überprüfung der Installation
-----------------------------

Überprüfen Sie, ob die Konfigurationsdateien korrekt bearbeitet wurden.

In der Eingabeaufforderung::

    C:\> findstr "SEARCH_ENGINE_HTTP_URL" C:\fess-15.3.0\bin\fess.in.bat
    C:\> findstr "FESS_DICTIONARY_PATH" C:\fess-15.3.0\bin\fess.in.bat

Schritt 3: Start
================

Die Startanleitung finden Sie unter :doc:`run`.

Registrierung als Windows-Dienst (Optional)
============================================

Durch Registrierung von |Fess| und OpenSearch als Windows-Dienste können sie beim Systemstart automatisch gestartet werden.

.. note::

   Für die Registrierung als Windows-Dienst ist ein Drittanbieter-Tool (wie NSSM) erforderlich.
   Detaillierte Anweisungen finden Sie in der Dokumentation des jeweiligen Tools.

Beispiel mit NSSM
-----------------

1. Laden Sie `NSSM (Non-Sucking Service Manager) <https://nssm.cc/download>`__ herunter und entpacken Sie es.

2. Registrieren Sie OpenSearch als Dienst::

       C:\> nssm install OpenSearch C:\opensearch-3.3.0\bin\opensearch.bat

3. Registrieren Sie Fess als Dienst::

       C:\> nssm install Fess C:\fess-15.3.0\bin\fess.bat

4. Konfigurieren Sie Dienstabhängigkeiten (Fess hängt von OpenSearch ab)::

       C:\> sc config Fess depend= OpenSearch

5. Starten Sie die Dienste::

       C:\> net start OpenSearch
       C:\> net start Fess

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
    C:\Program Files\opensearch-3.3.0  (nicht empfohlen - Pfad zu lang)

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
