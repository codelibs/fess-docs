==================================
Plugin-Architektur
==================================

Übersicht
=========

Das Plugin-System von |Fess| ermoglicht die Erweiterung der Kernfunktionen.
Plugins werden als JAR-Dateien verteilt und dynamisch geladen.

Plugin-Typen
============

|Fess| unterstutzt folgende Plugin-Typen:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Typ
     - Beschreibung
   * - DataStore
     - Inhaltserfassung von neuen Datenquellen (Box, Slack usw.)
   * - Script-Engine
     - Unterstutzung neuer Skriptsprachen
   * - WebApp
     - Erweiterung des Web-Interfaces
   * - Ingest
     - Datenverarbeitung beim Indexieren

Plugin-Struktur
===============

Grundstruktur
-------------

::

    fess-ds-example/
    ├── pom.xml
    └── src/main/java/org/codelibs/fess/ds/example/
        ├── ExampleDataStore.java      # DataStore-Implementierung
        └── ExampleDataStoreHandler.java # Handler (optional)

pom.xml-Beispiel
----------------

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                                 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>

        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-ds-example</artifactId>
        <version>15.5.0</version>
        <packaging>jar</packaging>

        <name>fess-ds-example</name>
        <description>Example DataStore for Fess</description>

        <properties>
            <fess.version>15.5.0</fess.version>
            <java.version>21</java.version>
        </properties>

        <dependencies>
            <dependency>
                <groupId>org.codelibs.fess</groupId>
                <artifactId>fess</artifactId>
                <version>${fess.version}</version>
                <scope>provided</scope>
            </dependency>
        </dependencies>
    </project>

Plugin-Registrierung
====================

Registrierung im DI-Container
-----------------------------

Plugins werden in Konfigurationsdateien wie ``fess_ds.xml`` registriert:

.. code-block:: xml

    <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
        <postConstruct name="register"/>
    </component>

Automatische Registrierung
--------------------------

Viele Plugins registrieren sich automatisch mit der ``@PostConstruct``-Annotation:

.. code-block:: java

    @PostConstruct
    public void register() {
        ComponentUtil.getDataStoreManager().add(this);
    }

Plugin-Lebenszyklus
===================

Initialisierung
---------------

1. JAR-Datei wird geladen
2. DI-Container initialisiert Komponenten
3. ``@PostConstruct``-Methoden werden aufgerufen
4. Plugin wird beim Manager registriert

Beendigung
----------

1. ``@PreDestroy``-Methode wird aufgerufen (falls definiert)
2. Ressourcen werden bereinigt

Abhangigkeiten
==============

Abhangigkeit von Fess-Core
--------------------------

.. code-block:: xml

    <dependency>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess</artifactId>
        <version>${fess.version}</version>
        <scope>provided</scope>
    </dependency>

Externe Bibliotheken
--------------------

Plugins konnen eigene Abhangigkeitsbibliotheken enthalten:

.. code-block:: xml

    <dependency>
        <groupId>com.example</groupId>
        <artifactId>example-sdk</artifactId>
        <version>1.0.0</version>
    </dependency>

Abhangigkeitsbibliotheken konnen zusammen mit dem Plugin-JAR verteilt werden,
oder es kann ein Fat-JAR mit dem Maven Shade Plugin erstellt werden.

Konfigurationszugriff
=====================

Zugriff auf FessConfig
----------------------

.. code-block:: java

    public class ExampleDataStore extends AbstractDataStore {

        @Override
        public String getName() {
            return "Example";
        }

        @Override
        protected void storeData(DataConfig dataConfig, IndexUpdateCallback callback,
                Map<String, String> paramMap, Map<String, String> scriptMap,
                Map<String, Object> defaultDataMap) {

            // Parameter abrufen
            String apiKey = paramMap.get("api.key");
            String baseUrl = paramMap.get("base.url");

            // FessConfig abrufen
            FessConfig fessConfig = ComponentUtil.getFessConfig();
        }
    }

Build und Installation
======================

Build
-----

::

    mvn clean package

Installation
------------

1. **Uber die Administrationsoberflache**:

   - "System" -> "Plugins" -> "Installieren"
   - Plugin-Namen eingeben und installieren

2. **Kommandozeile**:

   ::

       ./bin/fess-plugin install fess-ds-example

3. **Manuell**:

   - JAR-Datei in das ``plugins/``-Verzeichnis kopieren
   - |Fess| neu starten

Debugging
=========

Log-Ausgabe
-----------

.. code-block:: java

    private static final Logger logger = LogManager.getLogger(ExampleDataStore.class);

    public void someMethod() {
        logger.debug("Debug message");
        logger.info("Info message");
    }

Entwicklungsmodus
-----------------

Wahrend der Entwicklung kann |Fess| aus der IDE zum Debuggen gestartet werden:

1. ``FessBoot``-Klasse im Debug-Modus ausfuhren
2. Plugin-Quellcode in das Projekt einbinden
3. Breakpoints setzen

Veroffentlichte Plugins
=======================

Wichtige vom |Fess|-Projekt veroffentlichte Plugins:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Plugin
     - Beschreibung
   * - fess-ds-box
     - Box.com-Konnektor
   * - fess-ds-dropbox
     - Dropbox-Konnektor
   * - fess-ds-slack
     - Slack-Konnektor
   * - fess-ds-atlassian
     - Confluence/Jira-Konnektor
   * - fess-ds-git
     - Git-Repository-Konnektor
   * - fess-theme-*
     - Benutzerdefinierte Themes

Diese Plugins sind als Entwicklungsreferenz auf
`GitHub <https://github.com/codelibs>`__ veroffentlicht.

Referenzinformationen
=====================

- :doc:`datastore-plugin` - DataStore-Plugin-Entwicklung
- :doc:`script-engine-plugin` - Script-Engine-Plugin
- :doc:`webapp-plugin` - WebApp-Plugin
- :doc:`ingest-plugin` - Ingest-Plugin
