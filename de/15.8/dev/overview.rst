==================================
Entwicklerdokumentation Übersicht
==================================

Übersicht
=========

Dieser Abschnitt beschreibt die Erweiterungsentwicklung von |Fess|.
Er bietet Informationen zur Plugin-Entwicklung, zur Erstellung benutzerdefinierter Konnektoren,
zur Theme-Anpassung und zu weiteren Möglichkeiten, |Fess| zu erweitern.

Zielgruppe
==========

- Entwickler, die benutzerdefinierte Funktionen für |Fess| entwickeln möchten
- Entwickler, die Plugins erstellen möchten
- Entwickler, die den Quellcode von |Fess| verstehen möchten

Voraussetzungen
----------------

- Grundkenntnisse in Java 21
- Grundlagen von Maven (Build-System)
- Erfahrung in der Webanwendungsentwicklung
- Grundkenntnisse von OpenSearch (|Fess| verwendet OpenSearch als Suchmaschine)

Entwicklungsumgebung
=====================

Empfohlene Umgebung
--------------------

- **JDK**: OpenJDK 21 oder höher
- **IDE**: IntelliJ IDEA / Eclipse / VS Code
- **Build-Tool**: Maven (für den Build ist keine Mindestversion vorgeschrieben, empfohlen wird jedoch eine neuere 3.x-Version, die Java 21 unterstützt)
- **Git**: Versionskontrolle
- **OpenSearch**: Backend der Suchmaschine (beim Start aus der IDE werden die benötigten Module und Plugins beim Build heruntergeladen)

Setup
-----

|Fess| wird als Maven-Projekt gebaut. Bei der Entwicklung ist es am einfachsten, es aus der IDE zu starten.

1. Quellcode abrufen:

   ::

       git clone https://github.com/codelibs/fess.git

2. Import in die IDE:

   Importieren Sie das abgerufene Verzeichnis als Maven-Projekt in Ihre IDE.

3. Module und Plugins für OpenSearch herunterladen:

   Nur beim ersten Mal werden mit folgendem Befehl die Module und Plugins der Suchmaschine in das Verzeichnis ``plugins`` geladen.

   ::

       mvn antrun:run

4. Entwicklungsserver starten (aus der IDE):

   Führen Sie in der IDE ``org.codelibs.fess.FessBoot`` aus oder starten Sie ihn im Debug-Modus,
   und öffnen Sie im Browser http://localhost:8080/.
   Der Administrationsbereich ist unter http://localhost:8080/admin/ erreichbar (Standardkonto: ``admin`` / ``admin``).

5. Paket bauen (Erstellung des Verteilungspakets):

   Falls ein Verteilungspaket benötigt wird, führen Sie das Ziel ``package`` aus.
   Die Artefakte werden unter ``target/releases`` erzeugt (um Unit-Tests zu überspringen, fügen Sie ``-DskipTests`` hinzu).

   ::

       mvn package

   Entpacken Sie das erzeugte Verteilungspaket, um das Startskript ``bin/fess`` nutzen zu können.

   ::

       unzip target/releases/fess-*.zip
       ./fess-*/bin/fess

.. note::

    Das Startskript ``bin/fess`` ist im Verteilungspaket (zip/rpm/deb) enthalten.
    Wird ``mvn package`` lediglich im Quellverzeichnis ausgeführt, wird ``bin/fess`` nicht direkt im Wurzelverzeichnis des Repositorys erzeugt.
    Führen Sie bei der Entwicklung aus dem Quellcode wie oben beschrieben ``FessBoot`` in der IDE aus,
    oder verwenden Sie ``bin/fess`` aus dem entpackten Verteilungspaket.

Architekturüberblick
=====================

|Fess| besteht aus den folgenden Hauptkomponenten:

Komponentenstruktur
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Komponente
     - Beschreibung
   * - Web-Schicht
     - MVC-Implementierung mit dem LastaFlute-Framework
   * - Service-Schicht
     - Geschäftslogik
   * - Datenzugriffsschicht
     - Typsicherer OpenSearch-Zugriff mit DBFlute (ESFlute/FreeGen)
   * - Crawler
     - Inhaltserfassung mit der fess-crawler-Bibliothek
   * - Suchmaschine
     - Volltextsuche mit OpenSearch

Hauptframeworks
----------------

- **LastaFlute**: Web-Framework (Actions, Forms, Validierung)
- **DBFlute**: Datenzugriffs-Framework. Die typsicheren Zugriffsklassen für OpenSearch (``Bhv`` / ``ConditionBean``)
  werden durch die FreeGen-Funktion von DBFlute und ESFlute-Templates generiert
  (zur Neugenerierung: ``mvn dbflute:freegen``)
- **Lasta Di**: Dependency-Injection-Container

Verzeichnisstruktur
=====================

::

    fess/
    ├── src/main/java/org/codelibs/fess/
    │   ├── app/
    │   │   ├── web/         # Controller (Action)
    │   │   ├── service/     # Services
    │   │   ├── logic/       # Logik
    │   │   └── pager/       # Paginierung
    │   ├── api/             # REST API (z. B. api/v2)
    │   ├── helper/          # Hilfsklassen
    │   ├── crawler/         # Crawler-bezogen
    │   ├── indexer/         # Indexverarbeitung
    │   ├── opensearch/      # OpenSearch-Zugriff (ESFlute/FreeGen-generiert)
    │   ├── llm/             # LLM-Integration
    │   ├── ds/              # DataStore-Konnektoren
    │   ├── ingest/          # Ingest (Datenverarbeitung beim Indexieren)
    │   ├── script/          # Skript-Engine
    │   ├── entity/          # Entitäten
    │   └── mylasta/         # LastaFlute-Konfiguration (DI, Meldungen, typsichere Einstellungen)
    ├── src/main/resources/
    │   ├── fess_config.properties  # Konfiguration
    │   └── fess_*.xml              # DI-Konfiguration (app.xml, fess_ds.xml usw.)
    └── src/main/webapp/
        └── WEB-INF/view/    # JSP-Templates

Erweiterungspunkte
====================

|Fess| bietet folgende Erweiterungspunkte:

Plugins
-------

Mit Plugins können Funktionen hinzugefügt werden.

- **DataStore-Plugin**: Crawling von neuen Datenquellen (erbt von ``AbstractDataStore``)
- **Script-Engine-Plugin**: Unterstützung neuer Skriptsprachen (implementiert ``ScriptEngine``)
- **WebApp-Plugin**: Erweiterung der Weboberfläche (Überschreiben von Lasta-Di-Komponenten und Zusammenführen von Ressourcen)
- **Ingest-Plugin**: Datenverarbeitung beim Indexieren (erbt von ``Ingester``)

Details: :doc:`plugin-architecture`

.. note::

    |Fess| selbst wird als ``war`` paketiert. Wenn beim lokalen Erstellen eines Plugins
    |Fess| nicht als Abhängigkeit aufgelöst werden kann, ändern Sie in der ``pom.xml`` das ``<packaging>``
    vorübergehend auf ``jar``, führen Sie ``mvn clean install -DskipTests`` aus
    und setzen Sie es anschließend wieder auf ``war`` zurück.

Themes
------

Das Design der Suchoberfläche kann angepasst werden.

Details: :doc:`theme-development`

Konfiguration
--------------

Viele Verhaltensweisen können über ``fess_config.properties`` angepasst werden.

Details: :doc:`../config/intro`

Plugin-Entwicklung
====================

Für Details zur Plugin-Entwicklung siehe:

- :doc:`plugin-architecture` - Plugin-Architektur
- :doc:`datastore-plugin` - DataStore-Plugin-Entwicklung
- :doc:`script-engine-plugin` - Script-Engine-Plugin
- :doc:`webapp-plugin` - WebApp-Plugin
- :doc:`ingest-plugin` - Ingest-Plugin

Theme-Entwicklung
====================

- :doc:`theme-development` - Theme-Anpassung

Best Practices
================

Coding-Konventionen
---------------------

- Dem bestehenden Codestil von |Fess| folgen
- ``mvn formatter:format`` für die Code-Formatierung
- ``mvn license:format`` zum Hinzufügen des Lizenz-Headers

Tests
-----

- Unit-Tests (``*Test.java``): werden mit dem Standardprofil ``build`` über ``mvn test`` ausgeführt
- Integrationstests (``*Tests.java``): werden mit ``mvn test -P integrationTests`` ausgeführt.
  Für die Ausführung der Integrationstests sind ein laufender |Fess|-Server und OpenSearch erforderlich

Logging
-------

- Log4j2 verwenden
- ``logger.debug()`` / ``logger.info()`` / ``logger.warn()`` / ``logger.error()``
- Keine sensiblen Informationen in Logs ausgeben

Ressourcen
===========

- `GitHub Repository <https://github.com/codelibs/fess>`__
- `Issue Tracker <https://github.com/codelibs/fess/issues>`__
- `Discussions <https://github.com/codelibs/fess/discussions>`__
