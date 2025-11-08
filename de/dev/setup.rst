====================
Einrichten der Entwicklungsumgebung
====================

Diese Seite erklärt im Detail die Schritte zum Einrichten der |Fess|-Entwicklungsumgebung.
Von der Auswahl der IDE über das Abrufen des Quellcodes bis hin zur Ausführung und zum Debuggen
wird Schritt für Schritt erklärt.

.. contents:: Inhaltsverzeichnis
   :local:
   :depth: 2

Systemanforderungen
==========

Für die Entwicklungsumgebung werden folgende Hardware-Anforderungen empfohlen.

Hardware-Anforderungen
--------------

- **CPU**: 4 Kerne oder mehr
- **Speicher**: 8 GB oder mehr (16 GB empfohlen)
- **Festplatte**: 20 GB oder mehr freier Speicherplatz

.. note::

   Während der Entwicklung laufen |Fess| und das eingebettete OpenSearch gleichzeitig,
   daher sollten Sie ausreichend Speicher und Festplattenspeicher bereitstellen.

Software-Anforderungen
--------------

- **OS**: Windows 10/11, macOS 11 oder höher, Linux (Ubuntu 20.04 oder höher usw.)
- **Java**: JDK 21 oder höher
- **Maven**: 3.x oder höher
- **Git**: 2.x oder höher
- **IDE**: Eclipse, IntelliJ IDEA, VS Code usw.

Installation der erforderlichen Software
==========================

Installation von Java
-----------------

Für die |Fess|-Entwicklung ist Java 21 oder höher erforderlich.

Installation von Eclipse Temurin (empfohlen)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Eclipse Temurin (ehemals AdoptOpenJDK) wird empfohlen.

1. Besuchen Sie `Adoptium <https://adoptium.net/temurin/releases/>`__
2. Laden Sie die LTS-Version von Java 21 herunter
3. Folgen Sie den Anweisungen des Installers zur Installation

Überprüfung der Installation
~~~~~~~~~~~~~~

Führen Sie Folgendes im Terminal oder in der Eingabeaufforderung aus:

.. code-block:: bash

    java -version

Bei Erfolg wird eine Ausgabe wie folgt angezeigt:

.. code-block:: text

    openjdk version "21.0.x" 2024-xx-xx LTS
    OpenJDK Runtime Environment Temurin-21.0.x+x (build 21.0.x+x-LTS)
    OpenJDK 64-Bit Server VM Temurin-21.0.x+x (build 21.0.x+x-LTS, mixed mode, sharing)

Einstellung der Umgebungsvariablen
~~~~~~~~~~~~

**Linux/macOS:**

Fügen Sie Folgendes zu ``~/.bashrc`` oder ``~/.zshrc`` hinzu:

.. code-block:: bash

    export JAVA_HOME=/path/to/java21
    export PATH=$JAVA_HOME/bin:$PATH

**Windows:**

1. Öffnen Sie "Systemumgebungsvariablen bearbeiten"
2. Klicken Sie auf "Umgebungsvariablen"
3. Fügen Sie ``JAVA_HOME`` hinzu: ``C:\Program Files\Eclipse Adoptium\jdk-21.x.x.x-hotspot``
4. Fügen Sie ``%JAVA_HOME%\bin`` zu ``PATH`` hinzu

Installation von Maven
------------------

Installieren Sie Maven 3.x oder höher.

Download und Installation
~~~~~~~~~~~~~~~~~~~~~~~~

1. Besuchen Sie die `Maven-Download-Seite <https://maven.apache.org/download.cgi>`__
2. Laden Sie das Binary zip/tar.gz-Archiv herunter
3. Entpacken Sie es und platzieren Sie es an einem geeigneten Ort

**Linux/macOS:**

.. code-block:: bash

    tar xzvf apache-maven-3.x.x-bin.tar.gz
    sudo mv apache-maven-3.x.x /opt/
    sudo ln -s /opt/apache-maven-3.x.x /opt/maven

**Windows:**

1. Entpacken Sie die ZIP-Datei
2. Platzieren Sie sie unter ``C:\Program Files\Apache\maven`` oder ähnlich

Einstellung der Umgebungsvariablen
~~~~~~~~~~~~

**Linux/macOS:**

Fügen Sie Folgendes zu ``~/.bashrc`` oder ``~/.zshrc`` hinzu:

.. code-block:: bash

    export MAVEN_HOME=/opt/maven
    export PATH=$MAVEN_HOME/bin:$PATH

**Windows:**

1. Fügen Sie ``MAVEN_HOME`` hinzu: ``C:\Program Files\Apache\maven``
2. Fügen Sie ``%MAVEN_HOME%\bin`` zu ``PATH`` hinzu

Überprüfung der Installation
~~~~~~~~~~~~~~

.. code-block:: bash

    mvn -version

Bei Erfolg wird eine Ausgabe wie folgt angezeigt:

.. code-block:: text

    Apache Maven 3.x.x
    Maven home: /opt/maven
    Java version: 21.0.x, vendor: Eclipse Adoptium

Installation von Git
----------------

Wenn Git nicht installiert ist, installieren Sie es von folgenden Quellen.

- **Windows**: `Git for Windows <https://git-scm.com/download/win>`__
- **macOS**: ``brew install git`` oder `Git-Download-Seite <https://git-scm.com/download/mac>`__
- **Linux**: ``sudo apt install git`` (Ubuntu/Debian) oder ``sudo yum install git`` (RHEL/CentOS)

Überprüfung der Installation:

.. code-block:: bash

    git --version

IDE-Einrichtung
===============

Im Fall von Eclipse
------------

Eclipse ist die in der offiziellen |Fess|-Dokumentation empfohlene IDE.

Installation von Eclipse
~~~~~~~~~~~~~~~~~~~~

1. Besuchen Sie die `Eclipse-Download-Seite <https://www.eclipse.org/downloads/>`__
2. Laden Sie "Eclipse IDE for Enterprise Java and Web Developers" herunter
3. Führen Sie den Installer aus und folgen Sie den Anweisungen zur Installation

Empfohlene Plugins
~~~~~~~~~~~~

Eclipse enthält standardmäßig folgende Plugins:

- Maven Integration for Eclipse (m2e)
- Eclipse Java Development Tools

Importieren des Projekts
~~~~~~~~~~~~~~~~~~~~

1. Starten Sie Eclipse
2. Wählen Sie ``File`` > ``Import``
3. Wählen Sie ``Maven`` > ``Existing Maven Projects``
4. Geben Sie das Fess-Quellcodeverzeichnis an
5. Klicken Sie auf ``Finish``

Konfiguration der Ausführungskonfiguration
~~~~~~~~~~~~

1. Wählen Sie ``Run`` > ``Run Configurations...``
2. Rechtsklick auf ``Java Application`` und wählen Sie ``New Configuration``
3. Konfigurieren Sie Folgendes:

   - **Name**: Fess Boot
   - **Project**: fess
   - **Main class**: ``org.codelibs.fess.FessBoot``

4. Klicken Sie auf ``Apply``

Im Fall von IntelliJ IDEA
-------------------

IntelliJ IDEA ist ebenfalls eine weit verbreitete IDE.

Installation von IntelliJ IDEA
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Besuchen Sie die `IntelliJ IDEA-Download-Seite <https://www.jetbrains.com/idea/download/>`__
2. Laden Sie die Community Edition (kostenlos) oder Ultimate Edition herunter
3. Führen Sie den Installer aus und folgen Sie den Anweisungen zur Installation

Importieren des Projekts
~~~~~~~~~~~~~~~~~~~~

1. Starten Sie IntelliJ IDEA
2. Wählen Sie ``Open``
3. Wählen Sie ``pom.xml`` im Fess-Quellcodeverzeichnis
4. Klicken Sie auf ``Open as Project``
5. Es wird automatisch als Maven-Projekt importiert

Konfiguration der Ausführungskonfiguration
~~~~~~~~~~~~

1. Wählen Sie ``Run`` > ``Edit Configurations...``
2. Klicken Sie auf ``+`` und wählen Sie ``Application``
3. Konfigurieren Sie Folgendes:

   - **Name**: Fess Boot
   - **Module**: fess
   - **Main class**: ``org.codelibs.fess.FessBoot``
   - **JRE**: Java 21

4. Klicken Sie auf ``OK``

Im Fall von VS Code
------------

VS Code ist eine Option, wenn Sie eine leichte Entwicklungsumgebung bevorzugen.

Installation von VS Code
~~~~~~~~~~~~~~~~~~~~

1. Besuchen Sie die `VS Code-Download-Seite <https://code.visualstudio.com/>`__
2. Laden Sie den Installer herunter und führen Sie ihn aus

Installation der erforderlichen Erweiterungen
~~~~~~~~~~~~~~~~~~~~~~~~

Installieren Sie folgende Erweiterungen:

- **Extension Pack for Java**: Satz von Erweiterungen für Java-Entwicklung
- **Maven for Java**: Maven-Unterstützung

Projekt öffnen
~~~~~~~~~~~~~~~~

1. Starten Sie VS Code
2. Wählen Sie ``File`` > ``Open Folder``
3. Wählen Sie das Fess-Quellcodeverzeichnis

Abrufen des Quellcodes
==============

Klonen von GitHub
-------------------

Klonen Sie den |Fess|-Quellcode von GitHub.

.. code-block:: bash

    git clone https://github.com/codelibs/fess.git
    cd fess

Bei Verwendung von SSH:

.. code-block:: bash

    git clone git@github.com:codelibs/fess.git
    cd fess

.. tip::

   Wenn Sie mit einem Fork entwickeln, forken Sie zuerst das Fess-Repository auf GitHub und
   klonen Sie dann Ihr geforktes Repository:

   .. code-block:: bash

       git clone https://github.com/YOUR_USERNAME/fess.git
       cd fess
       git remote add upstream https://github.com/codelibs/fess.git

Projekt bauen
==================

Herunterladen der OpenSearch-Plugins
---------------------------------

Für die Ausführung von Fess sind Plugins für OpenSearch erforderlich.
Laden Sie sie mit folgendem Befehl herunter:

.. code-block:: bash

    mvn antrun:run

Dieser Befehl führt Folgendes aus:

- Herunterladen von OpenSearch
- Herunterladen und Installieren der erforderlichen Plugins
- Konfiguration von OpenSearch

.. note::

   Führen Sie diesen Befehl nur beim ersten Mal oder beim Aktualisieren von Plugins aus.
   Sie müssen ihn nicht jedes Mal ausführen.

Erster Build
--------

Bauen Sie das Projekt:

.. code-block:: bash

    mvn clean compile

Der erste Build kann einige Zeit dauern (Download von Abhängigkeiten usw.).

Bei erfolgreichem Build wird folgende Meldung angezeigt:

.. code-block:: text

    [INFO] BUILD SUCCESS
    [INFO] Total time: xx:xx min
    [INFO] Finished at: 2024-xx-xxTxx:xx:xx+09:00

Ausführen von Fess
==========

Ausführung von der Kommandozeile
--------------------

Ausführung mit Maven:

.. code-block:: bash

    mvn compile exec:java

Oder packen Sie es und führen Sie es aus:

.. code-block:: bash

    mvn package
    java -jar target/fess-15.3.x.jar

Ausführung von der IDE
------------

Im Fall von Eclipse
~~~~~~~~~~~~

1. Rechtsklick auf die Klasse ``org.codelibs.fess.FessBoot``
2. Wählen Sie ``Run As`` > ``Java Application``

Oder verwenden Sie die erstellte Ausführungskonfiguration:

1. Klicken Sie auf das Dropdown-Menü der Ausführungsschaltfläche in der Symbolleiste
2. Wählen Sie ``Fess Boot``

Im Fall von IntelliJ IDEA
~~~~~~~~~~~~~~~~~~

1. Rechtsklick auf die Klasse ``org.codelibs.fess.FessBoot``
2. Wählen Sie ``Run 'FessBoot.main()'``

Oder verwenden Sie die erstellte Ausführungskonfiguration:

1. Klicken Sie auf das Dropdown-Menü der Ausführungsschaltfläche in der Symbolleiste
2. Wählen Sie ``Fess Boot``

Im Fall von VS Code
~~~~~~~~~~~~

1. Öffnen Sie ``src/main/java/org/codelibs/fess/FessBoot.java``
2. Wählen Sie ``Run Without Debugging`` aus dem Menü ``Run``

Überprüfung des Starts
--------

Der Start von Fess dauert 1-2 Minuten.
Wenn folgendes Log in der Konsole angezeigt wird, ist der Start abgeschlossen:

.. code-block:: text

    [INFO] Boot Thread: Boot process completed successfully.

Überprüfen Sie den Betrieb durch Zugriff im Browser:

- **Suchseite**: http://localhost:8080/
- **Verwaltungsseite**: http://localhost:8080/admin/

  - Standardbenutzer: ``admin``
  - Standardpasswort: ``admin``

Ändern der Portnummer
--------------

Wenn der Standardport 8080 verwendet wird, können Sie ihn in folgender Datei ändern:

``src/main/resources/fess_config.properties``

.. code-block:: properties

    # Portnummer ändern
    server.port=8080

Debug-Ausführung
==========

Debug-Ausführung in der IDE
------------------

Im Fall von Eclipse
~~~~~~~~~~~~

1. Rechtsklick auf die Klasse ``org.codelibs.fess.FessBoot``
2. Wählen Sie ``Debug As`` > ``Java Application``
3. Setzen Sie Breakpoints und verfolgen Sie das Verhalten des Codes

Im Fall von IntelliJ IDEA
~~~~~~~~~~~~~~~~~~

1. Rechtsklick auf die Klasse ``org.codelibs.fess.FessBoot``
2. Wählen Sie ``Debug 'FessBoot.main()'``
3. Setzen Sie Breakpoints und verfolgen Sie das Verhalten des Codes

Im Fall von VS Code
~~~~~~~~~~~~

1. Öffnen Sie ``src/main/java/org/codelibs/fess/FessBoot.java``
2. Wählen Sie ``Start Debugging`` aus dem Menü ``Run``

Remote-Debugging
--------------

Sie können auch einen Debugger an Fess anschließen, das von der Kommandozeile gestartet wurde.

Starten Sie Fess im Debug-Modus:

.. code-block:: bash

    mvn compile exec:java -Dexec.args="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005"

Remote-Debug-Verbindung von der IDE:

**Eclipse:**

1. Wählen Sie ``Run`` > ``Debug Configurations...``
2. Rechtsklick auf ``Remote Java Application`` und wählen Sie ``New Configuration``
3. Setzen Sie ``Port: 5005``
4. Klicken Sie auf ``Debug``

**IntelliJ IDEA:**

1. Wählen Sie ``Run`` > ``Edit Configurations...``
2. Wählen Sie ``+`` > ``Remote JVM Debug``
3. Setzen Sie ``Port: 5005``
4. Klicken Sie auf ``OK`` und führen Sie ``Debug`` aus

Nützliche Einstellungen für die Entwicklung
==============

Ändern der Log-Ebene
--------------

Das Ändern der Log-Ebene beim Debuggen ermöglicht es Ihnen, detaillierte Informationen zu überprüfen.

Bearbeiten Sie ``src/main/resources/log4j2.xml``:

.. code-block:: xml

    <Configuration status="INFO">
        <Loggers>
            <Logger name="org.codelibs.fess" level="DEBUG"/>
            <Root level="INFO">
                <AppenderRef ref="console"/>
            </Root>
        </Loggers>
    </Configuration>

Aktivieren von Hot Deploy
-------------------

LastaFlute kann einige Änderungen ohne Neustart widerspiegeln.

Setzen Sie Folgendes in ``src/main/resources/fess_config.properties``:

.. code-block:: properties

    # Hot Deploy aktivieren
    development.here=true

Allerdings erfordern folgende Änderungen einen Neustart:

- Änderungen der Klassenstruktur (Hinzufügen/Entfernen von Methoden usw.)
- Änderungen von Konfigurationsdateien
- Änderungen von Abhängigkeitsbibliotheken

Betrieb des eingebetteten OpenSearch
------------------------

In der Entwicklungsumgebung wird das eingebettete OpenSearch verwendet.

Speicherort von OpenSearch:

.. code-block:: text

    target/fess/es/

Direkter Zugriff auf die OpenSearch-API:

.. code-block:: bash

    # Liste der Indizes
    curl -X GET http://localhost:9201/_cat/indices?v

    # Dokumentensuche
    curl -X GET http://localhost:9201/fess.search/_search?pretty

    # Mapping überprüfen
    curl -X GET http://localhost:9201/fess.search/_mapping?pretty

Verwendung von externem OpenSearch
--------------------

Wenn Sie einen externen OpenSearch-Server verwenden,
bearbeiten Sie ``src/main/resources/fess_config.properties``:

.. code-block:: properties

    # Eingebettetes OpenSearch deaktivieren
    opensearch.cluster.name=fess
    opensearch.http.url=http://localhost:9200

Code-Generierung mit DBFlute
======================

|Fess| verwendet DBFlute, um Java-Code automatisch aus dem OpenSearch-Schema zu generieren.

Neugenerierung bei Schemaänderungen
----------------------------

Wenn Sie das OpenSearch-Mapping geändert haben, generieren Sie den entsprechenden Java-Code mit folgendem Befehl neu:

.. code-block:: bash

    rm -rf mydbflute
    mvn antrun:run
    mvn dbflute:freegen
    mvn license:format

Erklärung der Befehle:

- ``rm -rf mydbflute``: Löscht das vorhandene DBFlute-Arbeitsverzeichnis
- ``mvn antrun:run``: Lädt OpenSearch-Plugins herunter
- ``mvn dbflute:freegen``: Generiert Java-Code aus dem Schema
- ``mvn license:format``: Fügt Lizenz-Header hinzu

Fehlerbehebung
==================

Build-Fehler
----------

**Fehler: Java-Version ist veraltet**

.. code-block:: text

    [ERROR] Failed to execute goal ... requires at least Java 21

Lösung: Installieren Sie Java 21 oder höher und setzen Sie ``JAVA_HOME`` entsprechend.

**Fehler: Download von Abhängigkeitsbibliotheken fehlgeschlagen**

.. code-block:: text

    [ERROR] Failed to collect dependencies

Lösung: Überprüfen Sie die Netzwerkverbindung, löschen Sie das lokale Maven-Repository und versuchen Sie es erneut:

.. code-block:: bash

    rm -rf ~/.m2/repository
    mvn clean compile

Ausführungsfehler
--------

**Fehler: Port 8080 wird bereits verwendet**

.. code-block:: text

    Address already in use

Lösung:

1. Beenden Sie den Prozess, der Port 8080 verwendet
2. Oder ändern Sie die Portnummer in ``fess_config.properties``

**Fehler: OpenSearch startet nicht**

Überprüfen Sie die Logdatei ``target/fess/es/logs/``.

Häufige Ursachen:

- Speichermangel: Erhöhen Sie die JVM-Heap-Größe
- Port 9201 wird verwendet: Ändern Sie die Portnummer
- Festplattenspeicher voll: Schaffen Sie Festplattenspeicher

Projekt wird in der IDE nicht erkannt
----------------------------

**Aktualisieren des Maven-Projekts**

- **Eclipse**: Rechtsklick auf Projekt > ``Maven`` > ``Update Project``
- **IntelliJ IDEA**: Klicken Sie im Maven-Tool-Fenster auf ``Reload All Maven Projects``
- **VS Code**: Führen Sie ``Java: Clean Java Language Server Workspace`` aus der Befehlspalette aus

Nächste Schritte
==========

Nachdem Sie die Entwicklungsumgebung eingerichtet haben, lesen Sie folgende Dokumentation:

- :doc:`architecture` - Verständnis der Codestruktur
- :doc:`workflow` - Lernen des Entwicklungsworkflows
- :doc:`building` - Methoden zum Bauen und Testen
- :doc:`contributing` - Erstellen von Pull Requests

Ressourcen
========

- `Eclipse-Download <https://www.eclipse.org/downloads/>`__
- `IntelliJ IDEA-Download <https://www.jetbrains.com/idea/download/>`__
- `VS Code-Download <https://code.visualstudio.com/>`__
- `Maven-Dokumentation <https://maven.apache.org/guides/>`__
- `LastaFlute <https://github.com/lastaflute/lastaflute>`__
- `DBFlute <https://dbflute.seasar.org/>`__
