==================================
Plugin-Architektur
==================================

Übersicht
=========

Das Plugin-System von |Fess| ermöglicht die Erweiterung der Kernfunktionen.
Plugins werden als JAR-Dateien ausgeliefert; sobald sie dem Klassenpfad
hinzugefügt werden, lädt der DI-Container (Lasta Di) die Komponenten und
registriert sie bei den entsprechenden Factory- bzw. Manager-Klassen.

Plugin-Typen
============

|Fess| unterscheidet die Plugin-Typen anhand des Präfixes des
Artefaktnamens (``PluginHelper.ArtifactType``). Die wichtigsten Typen sind:

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - Typ
     - Präfix
     - Beschreibung
   * - DataStore
     - ``fess-ds-*``
     - Inhaltserfassung aus neuen Datenquellen (Box, Slack, Git usw.)
   * - Webanwendung
     - ``fess-webapp-*``
     - Erweiterung der Web-Oberfläche und der Suchfunktionen
   * - Skript-Engine
     - ``fess-script-*``
     - Unterstützung neuer Skriptsprachen
   * - Ingest
     - ``fess-ingest-*``
     - Dokumentverarbeitung bei der Index-Registrierung
   * - Theme
     - ``fess-theme-*``
     - Anpassung des Erscheinungsbilds der Suchoberfläche
   * - Thumbnail
     - ``fess-thumbnail-*``
     - Hinzufügen von Verfahren zur Thumbnail-Erzeugung
   * - LLM
     - ``fess-llm-*``
     - Hinzufügen von LLM-Anbietern für RAG/Chat
   * - Crawler
     - ``fess-crawler-*``
     - Erweiterung des Crawler-Clients

Plugin-Struktur
===============

Grundstruktur
-------------

Am Beispiel von `fess-ds-example <https://github.com/codelibs/fess-ds-example>`__,
der Implementierungsvorlage für DataStore-Plugins, besteht ein Plugin aus
einer „Implementierungsklasse" und einer „DI-Registrierungsdatei":

::

    fess-ds-example/
    ├── pom.xml
    └── src/main/
        ├── java/org/codelibs/fess/ds/example/
        │   └── ExampleDataStore.java     # DataStore-Implementierung
        └── resources/
            └── fess_ds++.xml             # DI-Komponentenregistrierung

Beispiel für pom.xml
---------------------

Das Plugin wird als jar mit ``fess-parent`` als übergeordnetem POM gebaut.
Bibliotheken wie ``fess`` und ``opensearch``, die zur Laufzeit von |Fess|
selbst bereitgestellt werden, werden mit dem Scope ``provided`` deklariert.
Versionsnummer und Build-Konfiguration (z. B. Formatter und
Lizenzkopfzeilen) werden vom übergeordneten POM geerbt.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                                 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>

        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-ds-example</artifactId>
        <version>15.8.0</version>
        <packaging>jar</packaging>

        <parent>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess-parent</artifactId>
            <version>15.8.0</version>
            <relativePath />
        </parent>

        <dependencies>
            <dependency>
                <groupId>org.codelibs.fess</groupId>
                <artifactId>fess</artifactId>
                <scope>provided</scope>
            </dependency>
            <dependency>
                <groupId>org.opensearch</groupId>
                <artifactId>opensearch</artifactId>
                <scope>provided</scope>
            </dependency>
        </dependencies>
    </project>

.. note::

   In Branches, die sich in der Entwicklung befinden, erhält die Version ein
   Suffix ``-SNAPSHOT``, z. B. ``15.8.0-SNAPSHOT``. Plugin-spezifische
   Abhängigkeitsbibliotheken werden als normale Maven-Abhängigkeiten
   deklariert. Da diese nicht in |Fess| selbst enthalten sind, müssen sie
   zusammen mit dem Plugin verteilt werden.

Plugin-Registrierung
=====================

Registrierung im DI-Container
------------------------------

Ein Plugin registriert seine Komponenten in einer DI-Konfigurationsdatei,
deren Name auf ``++`` endet, wie z. B. ``fess_ds++.xml``. Lasta Di führt
Dateien mit der Endung ``++``, die im Klassenpfad gefunden werden,
automatisch mit der entsprechenden Konfigurationsdatei von |Fess| selbst
zusammen (in diesem Beispiel ``fess_ds.xml``). Durch diesen Mechanismus kann
ein Plugin eigene Komponenten hinzufügen, ohne Dateien von |Fess| selbst zu
bearbeiten.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
            <postConstruct name="register"></postConstruct>
        </component>
    </components>

Je nach Plugin-Typ unterscheidet sich die Ziel-Datei für das Merging.
Beispielsweise verwendet die Skript-Engine ``fess_se++.xml``, Ingest
``fess_ingest++.xml``, der LLM-Anbieter ``fess_llm++.xml`` und die
Webanwendung ``app++.xml``.

Initialisierung der Komponente
--------------------------------

``<postConstruct name="register">`` ist eine Lifecycle-Konfiguration von
Lasta Di, die die nach der Erzeugung der Komponente aufzurufende Methode
angibt. Im Fall eines DataStore wird die von ``AbstractDataStore``
bereitgestellte Methode ``register()`` aufgerufen, wodurch sich die
Komponente selbst bei ``DataStoreFactory`` registriert:

.. code-block:: java

    // Implementierung von AbstractDataStore (in der Regel keine Überschreibung nötig)
    public void register() {
        ComponentUtil.getDataStoreFactory().add(getName(), this);
    }

.. note::

   Dies ist keine Initialisierung über die Java-Annotation
   ``@PostConstruct``, sondern über das Element ``<postConstruct>`` der
   DI-Konfigurationsdatei. Der registrierte Name ist der Rückgabewert von
   ``getName()`` und entspricht dem Namen, der bei der Auswahl des Plugins
   in der Administrationsoberfläche verwendet wird.

Plugin-Lebenszyklus
=====================

Initialisierung
----------------

1. Das Plugin-JAR wird dem Klassenpfad hinzugefügt.
2. Der DI-Container führt ``fess_*++.xml`` zusammen und erzeugt die
   Komponenten.
3. Die in ``<postConstruct>`` angegebene Methode (z. B. ``register``) wird
   aufgerufen.
4. Das Plugin wird bei der entsprechenden Factory- bzw. Manager-Klasse
   registriert.

Beendigung
----------

1. Beim Beenden des DI-Containers wird die in ``<preDestroy>`` angegebene
   Methode aufgerufen (sofern definiert).
2. Bereinigung von Ressourcen.

.. note::

   Im Fall eines DataStore wird ein laufender Crawl-Vorgang durch
   ``AbstractDataStore.stop()`` mit einem Stopp-Flag versehen, sodass die
   Verarbeitungsschleife für die Datensätze sicher beendet wird.

Abhängigkeiten
================

Abhängigkeit von Fess selbst
-------------------------------

Da die Klassen von |Fess| selbst zur Laufzeit im Klassenpfad des Servers
vorhanden sind, wird die Abhängigkeit mit dem Scope ``provided`` deklariert
(sie ist nicht im Plugin-JAR enthalten).

.. code-block:: xml

    <dependency>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess</artifactId>
        <scope>provided</scope>
    </dependency>

Externe Bibliotheken
---------------------

Ein Plugin kann eigene Abhängigkeitsbibliotheken enthalten:

.. code-block:: xml

    <dependency>
        <groupId>com.example</groupId>
        <artifactId>example-sdk</artifactId>
        <version>1.0.0</version>
    </dependency>

Da diese nicht in |Fess| selbst enthalten sind, müssen sie zusammen mit dem
Plugin verteilt werden.

Abrufen der Konfiguration
============================

Abrufen von Parametern und FessConfig
----------------------------------------

In ``storeData()`` eines DataStore werden die in der
Administrationsoberfläche konfigurierten Parameter aus ``DataStoreParams``
abgerufen. Zum Abrufen der Werte wird ``getAsString()`` verwendet (da
``DataStoreParams`` das Interface ``Map`` nicht implementiert, gibt
``get()`` keinen String zurück). Konfigurationswerte von |Fess| lassen sich
außerdem über ``ComponentUtil.getFessConfig()`` abrufen:

.. code-block:: java

    public class ExampleDataStore extends AbstractDataStore {

        @Override
        protected String getName() {
            // Wird als Handler-Name verwendet. Es ist üblich, den einfachen Klassennamen zurückzugeben
            return this.getClass().getSimpleName();
        }

        @Override
        protected void storeData(final DataConfig dataConfig, final IndexUpdateCallback callback,
                final DataStoreParams paramMap, final Map<String, String> scriptMap,
                final Map<String, Object> defaultDataMap) {

            // Abrufen der Parameter
            final String apiKey = paramMap.getAsString("api.key");
            final String baseUrl = paramMap.getAsString("base.url");

            // Abrufen von FessConfig
            final FessConfig fessConfig = ComponentUtil.getFessConfig();
        }
    }

Detaillierte Informationen zur Implementierung von ``storeData()`` (Ablauf
von Datenabruf, Skriptauswertung und Index-Registrierung) finden Sie unter
:doc:`datastore-plugin`.

Build und Installation
========================

Build
-----

::

    mvn clean package

Im Verzeichnis ``target/`` wird eine JAR-Datei erzeugt (z. B.
``fess-ds-example-15.8.0.jar``).

Installation
------------

1. **Über die Administrationsoberfläche**:

   - Öffnen Sie „System" → „Plugin" → „Installieren".
   - Wählen Sie aus der Liste des Plugin-Repositorys aus, oder laden Sie die
     erstellte JAR-Datei hoch, um sie zu installieren.

2. **Manuell**:

   - Kopieren Sie die JAR-Datei in das Verzeichnis
     ``app/WEB-INF/plugin/``.
   - Starten Sie |Fess| neu.

Details zum Installationsvorgang finden Sie unter
:doc:`../admin/plugin-guide`.

Debugging
=========

Log-Ausgabe
------------

|Fess| verwendet Log4j2. Der Logger wird über ``LogManager.getLogger()``
abgerufen:

.. code-block:: java

    private static final Logger logger = LogManager.getLogger(ExampleDataStore.class);

    public void someMethod() {
        logger.debug("Debug message");
        logger.info("Info message");
    }

.. note::

   Geben Sie keine sensiblen Informationen wie Passwörter oder Token in
   Logs aus.

Entwicklungsmodus
------------------

Während der Entwicklung können Sie |Fess| aus der IDE starten und
debuggen:

1. Führen Sie die Klasse ``org.codelibs.fess.FessBoot`` im Debug-Modus aus.
2. Nehmen Sie den Quellcode des Plugins in das Projekt auf.
3. Setzen Sie Breakpoints.

Liste veröffentlichter Plugins
================================

Im |Fess|-Projekt sind zahlreiche Plugins veröffentlicht. Im Folgenden
finden Sie repräsentative Beispiele (diese Liste ist nicht vollständig):

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Plugin
     - Beschreibung
   * - ``fess-ds-box``
     - Box-Konnektor
   * - ``fess-ds-dropbox``
     - Dropbox-Konnektor
   * - ``fess-ds-slack``
     - Slack-Konnektor
   * - ``fess-ds-atlassian``
     - JIRA-/Confluence-Konnektor
   * - ``fess-ds-git``
     - Git-Repository-Konnektor
   * - ``fess-llm-openai``
     - OpenAI-LLM-Anbieter
   * - ``fess-theme-*``
     - Benutzerdefinierte Themes

Darüber hinaus sind DataStore-Konnektoren wie ``fess-ds-csv`` /
``fess-ds-db`` / ``fess-ds-json`` / ``fess-ds-microsoft365`` /
``fess-ds-sharepoint`` sowie LLM-Anbieter wie ``fess-llm-ollama`` /
``fess-llm-gemini`` veröffentlicht. Diese Plugins sind als Referenz für die
Entwicklung auf `GitHub <https://github.com/codelibs>`__ veröffentlicht.

Referenzinformationen
=======================

- :doc:`datastore-plugin` - DataStore-Plugin-Entwicklung
- :doc:`script-engine-plugin` - Skript-Engine-Plugin
- :doc:`webapp-plugin` - Webanwendungs-Plugin
- :doc:`ingest-plugin` - Ingest-Plugin
- :doc:`theme-development` - Anpassung von Themes
- :doc:`../admin/plugin-guide` - Plugin-Installation
