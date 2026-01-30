==================================
Entwicklerdokumentation Ubersicht
==================================

Ubersicht
=========

Dieser Abschnitt beschreibt die Erweiterungsentwicklung von |Fess|.
Er bietet Informationen zur Plugin-Entwicklung, Erstellung benutzerdefinierter Konnektoren,
Theme-Anpassung und anderen Moglichkeiten zur Erweiterung von |Fess|.

Zielgruppe
==========

- Entwickler, die benutzerdefinierte Funktionen fur |Fess| entwickeln mochten
- Entwickler, die Plugins erstellen mochten
- Entwickler, die den Quellcode von |Fess| verstehen mochten

Voraussetzungen
---------------

- Grundkenntnisse in Java 21
- Grundlagen von Maven (Build-System)
- Erfahrung in der Webanwendungsentwicklung

Entwicklungsumgebung
====================

Empfohlene Umgebung
-------------------

- **JDK**: OpenJDK 21 oder hoher
- **IDE**: IntelliJ IDEA / Eclipse / VS Code
- **Build-Tool**: Maven 3.9 oder hoher
- **Git**: Versionskontrolle

Setup
-----

1. Quellcode abrufen:

::

    git clone https://github.com/codelibs/fess.git
    cd fess

2. Build:

::

    mvn package -DskipTests

3. Entwicklungsserver starten:

::

    ./bin/fess

Architekturuberblick
====================

|Fess| besteht aus folgenden Hauptkomponenten:

Komponentenstruktur
-------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Komponente
     - Beschreibung
   * - Web-Schicht
     - MVC-Implementierung mit LastaFlute-Framework
   * - Service-Schicht
     - Geschaftslogik
   * - Datenzugriffsschicht
     - OpenSearch-Integration mit DBFlute
   * - Crawler
     - Inhaltserfassung mit der fess-crawler-Bibliothek
   * - Suchmaschine
     - Volltextsuche mit OpenSearch

Hauptframeworks
---------------

- **LastaFlute**: Web-Framework (Actions, Forms, Validierung)
- **DBFlute**: Datenzugriffs-Framework (OpenSearch-Integration)
- **Lasta Di**: Dependency-Injection-Container

Verzeichnisstruktur
===================

::

    fess/
    ├── src/main/java/org/codelibs/fess/
    │   ├── app/
    │   │   ├── web/         # Controller (Action)
    │   │   ├── service/     # Services
    │   │   └── pager/       # Paginierung
    │   ├── api/             # REST API
    │   ├── helper/          # Hilfsklassen
    │   ├── crawler/         # Crawler-bezogen
    │   ├── opensearch/      # OpenSearch-Integration (DBFlute-generiert)
    │   ├── llm/             # LLM-Integration
    │   └── ds/              # DataStore-Konnektoren
    ├── src/main/resources/
    │   ├── fess_config.properties  # Konfiguration
    │   └── fess_*.xml              # DI-Konfiguration
    └── src/main/webapp/
        └── WEB-INF/view/    # JSP-Templates

Erweiterungspunkte
==================

|Fess| bietet folgende Erweiterungspunkte:

Plugins
-------

Mit Plugins konnen Funktionen hinzugefugt werden.

- **DataStore-Plugins**: Crawling von neuen Datenquellen
- **Script-Engine-Plugins**: Unterstutzung neuer Skriptsprachen
- **WebApp-Plugins**: Erweiterung des Web-Interfaces
- **Ingest-Plugins**: Datenverarbeitung beim Indexieren

Details: :doc:`plugin-architecture`

Themes
------

Das Design der Suchoberflache kann angepasst werden.

Details: :doc:`theme-development`

Konfiguration
-------------

Viele Verhaltensweisen konnen uber ``fess_config.properties`` angepasst werden.

Details: :doc:`../config/intro`

Plugin-Entwicklung
==================

Fur Details zur Plugin-Entwicklung siehe:

- :doc:`plugin-architecture` - Plugin-Architektur
- :doc:`datastore-plugin` - DataStore-Plugin-Entwicklung
- :doc:`script-engine-plugin` - Script-Engine-Plugin
- :doc:`webapp-plugin` - WebApp-Plugin
- :doc:`ingest-plugin` - Ingest-Plugin

Theme-Entwicklung
=================

- :doc:`theme-development` - Theme-Anpassung

Best Practices
==============

Coding-Konventionen
-------------------

- Dem bestehenden Codestil von |Fess| folgen
- ``mvn formatter:format`` fur Code-Formatierung
- ``mvn license:format`` fur Lizenz-Header

Tests
-----

- Unit-Tests schreiben (``*Test.java``)
- Integrationstests sind ``*Tests.java``

Logging
-------

- Log4j2 verwenden
- ``logger.debug()`` / ``logger.info()`` / ``logger.warn()`` / ``logger.error()``
- Keine sensiblen Informationen in Logs ausgeben

Ressourcen
==========

- `GitHub Repository <https://github.com/codelibs/fess>`__
- `Issue Tracker <https://github.com/codelibs/fess/issues>`__
- `Discussions <https://github.com/codelibs/fess/discussions>`__
