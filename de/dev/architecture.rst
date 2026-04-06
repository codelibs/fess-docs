============================
Architektur und Codestruktur
============================

Diese Seite erklärt die Architektur, Codestruktur
und Hauptkomponenten von |Fess|.
Durch das Verständnis der internen Struktur von |Fess| können Sie effizient entwickeln.

.. contents:: Inhaltsverzeichnis
   :local:
   :depth: 2

Gesamtarchitektur
================

|Fess| besteht aus folgenden Hauptkomponenten:

.. code-block:: text

    ┌─────────────────────────────────────────────────┐
    │          Benutzerschnittstelle                  │
    │  ┌──────────────┐      ┌──────────────┐        │
    │  │  Suchseite    │      │ Verwaltung   │        │
    │  │  (JSP/HTML)   │      │   (JSP/HTML) │        │
    │  └──────────────┘      └──────────────┘        │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │           Webanwendungsschicht                   │
    │  ┌──────────────────────────────────────────┐  │
    │  │           LastaFlute                       │  │
    │  │  ┌────────┐  ┌─────────┐  ┌──────────┐  │  │
    │  │  │ Action │  │  Form   │  │  Service │  │  │
    │  │  └────────┘  └─────────┘  └──────────┘  │  │
    │  └──────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │           Geschäftslogikschicht                  │
    │  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
    │  │ Crawler  │  │  Job     │  │  Helper  │    │
    │  └──────────┘  └──────────┘  └──────────┘    │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │           Datenzugriffsschicht                   │
    │  ┌──────────────────────────────────────────┐  │
    │  │          DBFlute / OpenSearch             │  │
    │  │  ┌────────┐  ┌─────────┐  ┌──────────┐  │  │
    │  │  │Behavior│  │ Entity  │  │  Query   │  │  │
    │  │  └────────┘  └─────────┘  └──────────┘  │  │
    │  └──────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │               Datenspeicher                      │
    │              OpenSearch 3.5.0                   │
    └─────────────────────────────────────────────────┘

Beschreibung der Schichten
------------

Benutzerschnittstellenschicht
~~~~~~~~~~~~~~~~~~~~~~~~

Dies ist die Oberfläche, die Benutzer direkt bedienen.
Sie ist mit JSP, HTML und JavaScript implementiert.

- Suchseite: Suchoberfläche für Endbenutzer
- Verwaltungsseite: Konfigurations- und Verwaltungsoberfläche für Systemadministratoren

Webanwendungsschicht
~~~~~~~~~~~~~~~~~~~~

Dies ist die Webanwendungsschicht, die das LastaFlute-Framework verwendet.

- **Action**: Verarbeitet HTTP-Anfragen und ruft Geschäftslogik auf
- **Form**: Empfang von Anfrageparametern und Validierung
- **Service**: Implementierung der Geschäftslogik

Geschäftslogikschicht
~~~~~~~~~~~~~~~~

Dies ist die Schicht, die die Hauptfunktionen von |Fess| implementiert.

- **Crawler**: Sammelt Daten von Websites und Dateisystemen
- **Job**: Geplant ausgeführte Aufgaben
- **Helper**: In der gesamten Anwendung verwendete Hilfsklassen

Datenzugriffsschicht
~~~~~~~~~~~~~~

Dies ist die Zugriffsschicht auf OpenSearch mit DBFlute.

- **Behavior**: Schnittstelle für Datenoperationen
- **Entity**: Datenentität
- **Query**: Aufbau von Suchabfragen

Datenspeicherschicht
~~~~~~~~~~~~

Verwendet OpenSearch 3.5.0 als Suchmaschine.

Projektstruktur
==============

Verzeichnisstruktur
--------------

.. code-block:: text

    fess/
    ├── src/
    │   ├── main/
    │   │   ├── java/org/codelibs/fess/
    │   │   │   ├── app/              # Webanwendung
    │   │   │   │   ├── web/          # Suchseite
    │   │   │   │   │   ├── admin/    # Verwaltungsseite
    │   │   │   │   │   │   ├── ...Action.java
    │   │   │   │   │   │   └── ...Form.java
    │   │   │   │   │   └── ...Action.java
    │   │   │   │   └── service/      # Service-Schicht
    │   │   │   ├── crawler/          # Crawler
    │   │   │   │   ├── helper/       # Crawler helper
    │   │   │   │   ├── processor/    # Crawl processing
    │   │   │   │   ├── service/      # Crawler service
    │   │   │   │   └── transformer/  # Data transformation
    │   │   │   ├── opensearch/       # OpenSearch related
    │   │   │   │   ├── client/       # OpenSearch client
    │   │   │   │   ├── config/       # Configuration management
    │   │   │   │   ├── log/          # Log management
    │   │   │   │   ├── query/        # Query builder
    │   │   │   │   └── user/         # User management
    │   │   │   ├── helper/           # Hilfsklassen
    │   │   │   │   ├── ...Helper.java
    │   │   │   ├── job/              # Jobs
    │   │   │   │   ├── ...Job.java
    │   │   │   ├── util/             # Utilities
    │   │   │   ├── entity/           # Entitäten (automatisch generiert)
    │   │   │   ├── mylasta/          # LastaFlute-Konfiguration
    │   │   │   │   ├── action/       # Action-Basisklassen
    │   │   │   │   ├── direction/    # Anwendungskonfiguration
    │   │   │   │   └── mail/         # Mail-Konfiguration
    │   │   │   ├── Constants.java    # Konstantendefinitionen
    │   │   │   └── FessBoot.java     # Startklasse
    │   │   ├── resources/
    │   │   │   ├── fess_config.properties  # Konfigurationsdatei
    │   │   │   ├── fess_config.xml         # LastaDi component configuration
    │   │   │   ├── fess_message_ja.properties  # Nachrichten (Japanisch)
    │   │   │   ├── fess_message_en.properties  # Nachrichten (Englisch)
    │   │   │   └── ...
    │   │   └── webapp/
    │   │       ├── WEB-INF/
    │   │       │   ├── view/          # JSP-Dateien
    │   │       │   │   ├── admin/     # Verwaltungs-JSPs
    │   │       │   │   └── ...
    │   │       │   └── web.xml
    │   │       ├── css/               # CSS-Dateien
    │   │       ├── js/                # JavaScript-Dateien
    │   │       └── images/            # Bilddateien
    │   └── test/
    │       └── java/org/codelibs/fess/
    │           ├── ...Test.java       # Testklassen
    │           └── it/                # Integrationstests
    ├── pom.xml                        # Maven-Konfiguration
    ├── dbflute_fess/                  # DBFlute-Konfiguration
    │   ├── dfprop/                    # DBFlute-Eigenschaften
    │   └── freegen/                   # FreeGen-Konfiguration
    └── README.md

Details zu Hauptpaketen
==================

app-Paket
------------

Code der Webanwendungsschicht.

app.web-Paket
~~~~~~~~~~~~~~~~

Implementiert Suchseite und Endbenutzerfunktionen.

**Hauptklassen:**

- ``SearchAction.java``: Suchverarbeitung
- ``LoginAction.java``: Login-Verarbeitung

**Beispiel:**

.. code-block:: java

    @Execute
    public HtmlResponse index(SearchForm form) {
        // Implementierung der Suchverarbeitung
        return asHtml(path_IndexJsp);
    }

app.web.admin-Paket
~~~~~~~~~~~~~~~~~~~~~~~

Implementiert Funktionen der Verwaltungsseite.

**Hauptklassen:**

- ``AdminWebconfigAction.java``: Web-Crawl-Konfiguration
- ``AdminSchedulerAction.java``: Scheduler-Verwaltung
- ``AdminUserAction.java``: Benutzerverwaltung

**Namenskonventionen:**

- ``Admin``-Präfix: Admin-Action
- ``Action``-Suffix: Action-Klasse
- ``Form``-Suffix: Form-Klasse

app.service-Paket
~~~~~~~~~~~~~~~~~~~~

Service-Schicht, die Geschäftslogik implementiert.

**Hauptklassen:**

- ``SearchLogService.java``: Suchprotokolldienst
- ``UserService.java``: Benutzerverwaltungsdienst
- ``ScheduledJobService.java``: Job-Verwaltungsdienst

**Beispiel:**

.. code-block:: java

    public class ScheduledJobService {
        @Resource
        private ScheduledJobBhv scheduledJobBhv;

        // Job CRUD operations implementation
    }

crawler-Paket (fess-crawler-Bibliothek)
----------------------------------------

Implementiert Datensammlungsfunktionen.

**Hauptklassen:**

- ``CrawlerClient.java``: Basisklasse für Crawler-Client
- ``HcHttpClient.java``: HTTP-Crawling-Client
- ``FileSystemClient.java``: Crawlen von Dateisystemen
- ``ExtractorFactory.java``: Extractor-Factory
- ``TikaExtractor.java``: Extraktion mit Apache Tika
- ``Transformer.java``: Schnittstelle für Transformationsverarbeitung

crawler-Paket (fess main)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Crawler-Integration in der Fess-Hauptanwendung.

**Hauptklassen:**

- ``FessStandardTransformer.java``: Standard-Transformationsverarbeitung
- ``FessXpathTransformer.java``: XPath-basierte Transformationsverarbeitung

opensearch-Paket
-------------------

Implementiert Integration mit OpenSearch.

opensearch.client-Paket
~~~~~~~~~~~~~~~~~~~~~~~~~~

Implementierung des OpenSearch-Clients.

**Hauptklassen:**

- ``SearchEngineClient.java``: OpenSearch-Client

opensearch.query-Paket
~~~~~~~~~~~~~~~~~~~~~~~~~

Implementiert Aufbau von Suchabfragen.

**Hauptklassen:**

- ``QueryCommand.java``: Abfragebefehl
- ``QueryProcessor.java``: Abfrageverarbeitung

helper-Paket
---------------

In der gesamten Anwendung verwendete Hilfsklassen.

**Hauptklassen:**

- ``SystemHelper.java``: Systemweites Hilfsprogramm
- ``CrawlingConfigHelper.java``: Hilfsprogramm für Crawl-Konfiguration
- ``SearchLogHelper.java``: Hilfsprogramm für Suchprotokolle
- ``UserInfoHelper.java``: Hilfsprogramm für Benutzerinformationen
- ``ViewHelper.java``: Hilfsprogramm für Ansichten
- ``QueryHelper.java``: Hilfsprogramm für Abfrage-Aufbau

**Beispiel:**

.. code-block:: java

    public class SystemHelper {
        @PostConstruct
        public void init() {
            // Systeminitialisierungsverarbeitung
        }
    }

job-Paket
------------

Implementiert geplant ausgeführte Jobs.

**Hauptklassen:**

- ``CrawlJob.java``: Crawl-Job
- ``SuggestJob.java``: Suggest-Job
- ``ScriptExecutorJob.java``: Skriptausführungs-Job

**Beispiel:**

.. code-block:: java

    public class CrawlJob extends ExecJob {
        @Override
        public void execute() {
            // Implementierung der Crawl-Verarbeitung
        }
    }

entity-Paket
---------------

Entitätsklassen, die OpenSearch-Dokumenten entsprechen.
Dieses Paket wird automatisch von DBFlute generiert.

**Hauptklassen:**

- ``SearchLog.java``: Suchprotokoll
- ``ClickLog.java``: Klickprotokoll
- ``FavoriteLog.java``: Favoritenprotokoll
- ``User.java``: Benutzerinformationen
- ``Role.java``: Rolleninformationen

.. note::

   Der Code im entity-Paket wird automatisch generiert,
   bearbeiten Sie ihn daher nicht direkt.
   Aktualisieren Sie durch Ändern des Schemas und Neugenerierung.

mylasta-Paket
----------------

Führt Konfiguration und Anpassung von LastaFlute durch.

mylasta.action-Paket
~~~~~~~~~~~~~~~~~~~~~~~

Definiert Basisklassen für Actions.

- ``FessUserBean.java``: Benutzerinformationen
- ``FessHtmlPath.java``: HTML-Pfaddefinition

mylasta.direction-Paket
~~~~~~~~~~~~~~~~~~~~~~~~~~

Führt anwendungsweite Konfiguration durch.

- ``FessConfig.java``: Laden der Konfiguration
- ``FessFwAssistantDirector.java``: Framework-Konfiguration

Entwurfsmuster und Implementierungsmuster
============================

In |Fess| werden folgende Entwurfsmuster verwendet.

MVC-Muster
----------

Mit LastaFlute im MVC-Muster implementiert.

- **Model**: Service, Entity
- **View**: JSP
- **Controller**: Action

Beispiel:

.. code-block:: java

    // Controller (Action)
    public class SearchAction extends FessSearchAction {
        @Resource
        private SearchHelper searchHelper;  // Model (Service)

        @Execute
        public HtmlResponse index(SearchForm form) {
            return search(form);
        }
    }

DI-Muster
---------

Verwendet den DI-Container von LastaFlute.

.. code-block:: java

    public class SearchService {
        @Resource
        private SearchEngineClient searchEngineClient;

        @Resource
        private UserInfoHelper userInfoHelper;
    }

Factory-Muster
--------------

Wird zur Erzeugung verschiedener Komponenten verwendet.

.. code-block:: java

    public class ExtractorFactory {
        public Extractor getExtractor(String key) {
            // Erzeugt Extractor entsprechend dem MIME-Typ
        }
    }

Strategy-Muster
---------------

Wird in Crawlern und Transformern verwendet.

.. code-block:: java

    public interface Transformer {
        ResultData transform(ResponseData responseData);
    }

    public class HtmlTransformer implements Transformer {
        // Transformationsverarbeitung für HTML
    }

Konfigurationsverwaltung
======

Die Konfiguration von |Fess| wird in mehreren Dateien verwaltet.

fess_config.properties
--------------------

Definiert Hauptkonfiguration der Anwendung.

.. code-block:: properties

    # OpenSearch-Verbindungskonfiguration
    search_engine.http.url=http://localhost:9201

    # Crawl-Konfiguration
    crawler.document.max.site.length=100
    crawler.document.cache.enabled=true

fess_config.xml
--------------

LastaDi-Komponentenkonfigurationsdatei.

.. code-block:: xml

    <component name="systemProperties" class="org.codelibs.core.misc.DynamicProperties">
        <arg>
            org.codelibs.fess.util.ResourceUtil.getConfPath("system.properties")
        </arg>
    </component>

fess_message_*.properties
------------------------

Nachrichtendateien für mehrsprachige Unterstützung.

- ``fess_message_ja.properties``: Japanisch
- ``fess_message_en.properties``: Englisch

Datenfluss
==========

Suchablauf
--------

.. code-block:: text

    1. Benutzer sucht auf der Suchseite
       ↓
    2. SearchAction empfängt Suchanfrage
       ↓
    3. SearchService führt Geschäftslogik aus
       ↓
    4. SearchEngineClient sendet Suchabfrage an OpenSearch
       ↓
    5. OpenSearch gibt Suchergebnisse zurück
       ↓
    6. SearchService formatiert Ergebnisse
       ↓
    7. SearchAction gibt Ergebnisse an JSP weiter und zeigt sie an

Crawl-Ablauf
------------

.. code-block:: text

    1. CrawlJob wird geplant ausgeführt
       ↓
    2. CrawlingConfigHelper ruft Crawl-Konfiguration ab
       ↓
    3. CrawlerClient greift auf Zielseite zu
       ↓
    4. Extractor extrahiert Text aus Inhalt
       ↓
    5. Transformer transformiert Daten in Suchformat
       ↓
    6. SearchEngineClient registriert Dokument in OpenSearch

Erweiterungspunkte
==========

|Fess| kann an folgenden Punkten erweitert werden.

Hinzufügen benutzerdefinierter Crawler
--------------------

Durch Implementieren der ``CrawlerClient interface`` können Sie benutzerdefinierte Datenquellen unterstützen.

Hinzufügen benutzerdefinierter Transformer
----------------------------

Durch Implementieren von ``Transformer`` können Sie benutzerdefinierte Datentransformationsverarbeitung hinzufügen.

Hinzufügen benutzerdefinierter Extractoren
--------------------------

Durch Implementieren von ``Extractor`` können Sie benutzerdefinierte Inhaltsextraktionsverarbeitung hinzufügen.

Hinzufügen benutzerdefinierter Plugins
--------------------

Plugins können über die Admin-UI-Plugin-Verwaltungsseite verwaltet werden.

Referenzmaterialien
======

Frameworks
------------

- `LastaFlute-Referenz <https://github.com/lastaflute/lastaflute>`__
- `DBFlute-Dokumentation <https://dbflute.seasar.org/>`__

Technische Dokumentation
--------------

- `OpenSearch-API-Referenz <https://opensearch.org/docs/latest/api-reference/>`__
- `Apache Tika <https://tika.apache.org/>`__

Nächste Schritte
==========

Nachdem Sie die Architektur verstanden haben, lesen Sie folgende Dokumentation:

- :doc:`workflow` - Tatsächlicher Entwicklungsablauf
- :doc:`building` - Build und Test
- :doc:`contributing` - Erstellen von Pull Requests
