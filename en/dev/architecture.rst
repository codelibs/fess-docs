============================
Architecture and Code Structure
============================

This page explains |Fess|'s architecture, code structure,
and main components.
Understanding the internal structure of |Fess| allows you to develop efficiently.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overall Architecture
================

|Fess| consists of the following main components:

.. code-block:: text

    ┌─────────────────────────────────────────────────┐
    │          User Interface                         │
    │  ┌──────────────┐      ┌──────────────┐        │
    │  │ Search Screen│      │  Admin Screen│        │
    │  │  (JSP/HTML)  │      │  (JSP/HTML)  │        │
    │  └──────────────┘      └──────────────┘        │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │          Web Application Layer                  │
    │  ┌──────────────────────────────────────────┐  │
    │  │           LastaFlute                       │  │
    │  │  ┌────────┐  ┌─────────┐  ┌──────────┐  │  │
    │  │  │ Action │  │  Form   │  │  Service │  │  │
    │  │  └────────┘  └─────────┘  └──────────┘  │  │
    │  └──────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │          Business Logic Layer                   │
    │  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
    │  │ Crawler  │  │  Job     │  │  Helper  │    │
    │  └──────────┘  └──────────┘  └──────────┘    │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │          Data Access Layer                      │
    │  ┌──────────────────────────────────────────┐  │
    │  │          DBFlute / OpenSearch             │  │
    │  │  ┌────────┐  ┌─────────┐  ┌──────────┐  │  │
    │  │  │Behavior│  │ Entity  │  │  Query   │  │  │
    │  │  └────────┘  └─────────┘  └──────────┘  │  │
    │  └──────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │               Data Store                        │
    │              OpenSearch 3.3.0                   │
    └─────────────────────────────────────────────────┘

Layer Descriptions
------------

User Interface Layer
~~~~~~~~~~~~~~~~~~~~~~~~

The screens that users interact with directly.
Implemented using JSP, HTML, and JavaScript.

- Search Screen: Search interface for end users
- Admin Screen: Configuration and management interface for system administrators

Web Application Layer
~~~~~~~~~~~~~~~~~~~~

Web application layer using the LastaFlute framework.

- **Action**: Processes HTTP requests and calls business logic
- **Form**: Receives request parameters and performs validation
- **Service**: Implements business logic

Business Logic Layer
~~~~~~~~~~~~~~~~

Layer that implements |Fess|'s main features.

- **Crawler**: Collects data from websites and file systems
- **Job**: Tasks executed on a schedule
- **Helper**: Helper classes used throughout the application

Data Access Layer
~~~~~~~~~~~~~~

Access layer to OpenSearch using DBFlute.

- **Behavior**: Interface for data operations
- **Entity**: Data entity
- **Query**: Building search queries

Data Store Layer
~~~~~~~~~~~~

Uses OpenSearch 3.3.0 as the search engine.

Project Structure
==============

Directory Structure
--------------

.. code-block:: text

    fess/
    ├── src/
    │   ├── main/
    │   │   ├── java/org/codelibs/fess/
    │   │   │   ├── app/              # Web application
    │   │   │   │   ├── web/          # Search screen
    │   │   │   │   │   ├── admin/    # Admin screen
    │   │   │   │   │   │   ├── ...Action.java
    │   │   │   │   │   │   └── ...Form.java
    │   │   │   │   │   └── ...Action.java
    │   │   │   │   └── service/      # Service layer
    │   │   │   ├── crawler/          # Crawler
    │   │   │   │   ├── client/       # Crawler client
    │   │   │   │   ├── extractor/    # Content extraction
    │   │   │   │   ├── filter/       # Filter
    │   │   │   │   └── transformer/  # Data transformation
    │   │   │   ├── es/               # OpenSearch related
    │   │   │   │   ├── client/       # OpenSearch client
    │   │   │   │   ├── query/        # Query builder
    │   │   │   │   └── config/       # Configuration management
    │   │   │   ├── helper/           # Helper classes
    │   │   │   │   ├── ...Helper.java
    │   │   │   ├── job/              # Jobs
    │   │   │   │   ├── ...Job.java
    │   │   │   ├── util/             # Utilities
    │   │   │   ├── entity/           # Entities (auto-generated)
    │   │   │   ├── mylasta/          # LastaFlute configuration
    │   │   │   │   ├── action/       # Action base classes
    │   │   │   │   ├── direction/    # Application configuration
    │   │   │   │   └── mail/         # Mail configuration
    │   │   │   ├── Constants.java    # Constant definitions
    │   │   │   └── FessBoot.java     # Boot class
    │   │   ├── resources/
    │   │   │   ├── fess_config.properties  # Configuration file
    │   │   │   ├── fess_config.xml         # Additional configuration
    │   │   │   ├── fess_message_ja.properties  # Messages (Japanese)
    │   │   │   ├── fess_message_en.properties  # Messages (English)
    │   │   │   ├── log4j2.xml              # Log configuration
    │   │   │   └── ...
    │   │   └── webapp/
    │   │       ├── WEB-INF/
    │   │       │   ├── view/          # JSP files
    │   │       │   │   ├── admin/     # Admin screen JSP
    │   │       │   │   └── ...
    │   │       │   └── web.xml
    │   │       ├── css/               # CSS files
    │   │       ├── js/                # JavaScript files
    │   │       └── images/            # Image files
    │   └── test/
    │       └── java/org/codelibs/fess/
    │           ├── ...Test.java       # Test classes
    │           └── it/                # Integration tests
    ├── pom.xml                        # Maven configuration
    ├── dbflute_fess/                  # DBFlute configuration
    │   ├── dfprop/                    # DBFlute properties
    │   └── freegen/                   # FreeGen configuration
    └── README.md

Main Package Details
==================

app Package
------------

Code for the web application layer.

app.web Package
~~~~~~~~~~~~~~~~

Implements search screen and end-user features.

**Main classes:**

- ``SearchAction.java``: Search processing
- ``LoginAction.java``: Login processing

**Example:**

.. code-block:: java

    @Execute
    public HtmlResponse index(SearchForm form) {
        // Search processing implementation
        return asHtml(path_IndexJsp);
    }

app.web.admin Package
~~~~~~~~~~~~~~~~~~~~~~~

Implements admin screen features.

**Main classes:**

- ``BwCrawlingConfigAction.java``: Web crawl configuration
- ``BwSchedulerAction.java``: Scheduler management
- ``BwUserAction.java``: User management

**Naming conventions:**

- ``Bw`` prefix: Admin Action
- ``Action`` suffix: Action class
- ``Form`` suffix: Form class

app.service Package
~~~~~~~~~~~~~~~~~~~~

Service layer that implements business logic.

**Main classes:**

- ``SearchService.java``: Search service
- ``UserService.java``: User management service
- ``ScheduledJobService.java``: Job management service

**Example:**

.. code-block:: java

    public class SearchService {
        public SearchResponse search(SearchRequestParams params) {
            // Search logic implementation
        }
    }

crawler Package
----------------

Implements data collection features.

crawler.client Package
~~~~~~~~~~~~~~~~~~~~~~~

Implements access to various data sources.

**Main classes:**

- ``FessClient.java``: Base class for crawler clients
- ``WebClient.java``: Website crawling
- ``FileSystemClient.java``: File system crawling
- ``DataStoreClient.java``: Database crawling, etc.

crawler.extractor Package
~~~~~~~~~~~~~~~~~~~~~~~~~~

Extracts text from documents.

**Main classes:**

- ``ExtractorFactory.java``: Extractor factory
- ``TikaExtractor.java``: Extraction using Apache Tika

crawler.transformer Package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Transforms crawled data into search format.

**Main classes:**

- ``Transformer.java``: Transformation processing interface
- ``BasicTransformer.java``: Basic transformation processing

es Package
-----------

Implements integration with OpenSearch.

es.client Package
~~~~~~~~~~~~~~~~~~

OpenSearch client implementation.

**Main classes:**

- ``FessEsClient.java``: OpenSearch client
- ``SearchEngineClient.java``: Search engine client interface

es.query Package
~~~~~~~~~~~~~~~~~

Implements search query construction.

**Main classes:**

- ``QueryHelper.java``: Query construction helper
- ``FunctionScoreQueryBuilder.java``: Scoring adjustment

helper Package
---------------

Helper classes used throughout the application.

**Main classes:**

- ``SystemHelper.java``: System-wide helper
- ``CrawlingConfigHelper.java``: Crawl configuration helper
- ``SearchLogHelper.java``: Search log helper
- ``UserInfoHelper.java``: User information helper
- ``ViewHelper.java``: View-related helper

**Example:**

.. code-block:: java

    public class SystemHelper {
        public void initializeSystem() {
            // System initialization processing
        }
    }

job Package
------------

Implements jobs executed on a schedule.

**Main classes:**

- ``CrawlJob.java``: Crawl job
- ``SuggestJob.java``: Suggest job
- ``ScriptExecutorJob.java``: Script execution job

**Example:**

.. code-block:: java

    public class CrawlJob extends LaJob {
        @Override
        public void run() {
            // Crawl processing implementation
        }
    }

entity Package
---------------

Entity classes corresponding to OpenSearch documents.
This package is auto-generated by DBFlute.

**Main classes:**

- ``SearchLog.java``: Search log
- ``ClickLog.java``: Click log
- ``FavoriteLog.java``: Favorite log
- ``User.java``: User information
- ``Role.java``: Role information

.. note::

   Do not edit code in the entity package directly
   as it is auto-generated.
   Update by changing the schema and regenerating.

mylasta Package
----------------

LastaFlute configuration and customization.

mylasta.action Package
~~~~~~~~~~~~~~~~~~~~~~~

Defines Action base classes.

- ``FessUserBean.java``: User information
- ``FessHtmlPath.java``: HTML path definitions

mylasta.direction Package
~~~~~~~~~~~~~~~~~~~~~~~~~~

Application-wide configuration.

- ``FessConfig.java``: Configuration loading
- ``FessFwAssistantDirector.java``: Framework configuration

Design Patterns and Implementation Patterns
============================

|Fess| uses the following design patterns.

MVC Pattern
----------

Implemented using MVC pattern with LastaFlute.

- **Model**: Service, Entity
- **View**: JSP
- **Controller**: Action

Example:

.. code-block:: java

    // Controller (Action)
    public class SearchAction extends FessBaseAction {
        @Resource
        private SearchService searchService;  // Model (Service)

        @Execute
        public HtmlResponse index(SearchForm form) {
            SearchResponse response = searchService.search(form);
            return asHtml(path_IndexJsp).renderWith(data -> {
                data.register("response", response);  // Pass data to View (JSP)
            });
        }
    }

DI Pattern
---------

Uses LastaFlute's DI container.

.. code-block:: java

    public class SearchService {
        @Resource
        private SearchEngineClient searchEngineClient;

        @Resource
        private UserInfoHelper userInfoHelper;
    }

Factory Pattern
--------------

Used for creating various components.

.. code-block:: java

    public class ExtractorFactory {
        public Extractor createExtractor(String mimeType) {
            // Create Extractor according to MIME type
        }
    }

Strategy Pattern
---------------

Used in crawlers and transformers.

.. code-block:: java

    public interface Transformer {
        Map<String, Object> transform(Map<String, Object> data);
    }

    public class HtmlTransformer implements Transformer {
        // Transformation processing for HTML
    }

Configuration Management
======

|Fess| configuration is managed in multiple files.

fess_config.properties
--------------------

Defines main application configuration.

.. code-block:: properties

    # Port number
    server.port=8080

    # OpenSearch connection settings
    opensearch.http.url=http://localhost:9201

    # Crawl settings
    crawler.document.max.size=10000000

fess_config.xml
--------------

Additional configuration in XML format.

.. code-block:: xml

    <component name="searchService" class="...SearchService">
        <property name="maxSearchResults">1000</property>
    </component>

fess_message_*.properties
------------------------

Message files for internationalization.

- ``fess_message_ja.properties``: Japanese
- ``fess_message_en.properties``: English

Data Flow
==========

Search Flow
--------

.. code-block:: text

    1. User searches on search screen
       ↓
    2. SearchAction receives search request
       ↓
    3. SearchService executes business logic
       ↓
    4. SearchEngineClient sends search query to OpenSearch
       ↓
    5. OpenSearch returns search results
       ↓
    6. SearchService formats results
       ↓
    7. SearchAction passes results to JSP for display

Crawl Flow
------------

.. code-block:: text

    1. CrawlJob is executed on schedule
       ↓
    2. CrawlingConfigHelper retrieves crawl configuration
       ↓
    3. FessClient accesses target site
       ↓
    4. Extractor extracts text from content
       ↓
    5. Transformer converts data to search format
       ↓
    6. SearchEngineClient registers documents in OpenSearch

Extension Points
==========

|Fess| can be extended at the following points.

Adding Custom Crawlers
--------------------

Inherit ``FessClient`` to support custom data sources.

Adding Custom Transformers
----------------------------

Implement ``Transformer`` to add custom data transformation processing.

Adding Custom Extractors
--------------------------

Implement ``Extractor`` to add custom content extraction processing.

Adding Custom Plugins
--------------------

Implement the ``Plugin`` interface to create custom plugins.

References
======

Frameworks
------------

- `LastaFlute Reference <https://github.com/lastaflute/lastaflute>`__
- `DBFlute Documentation <https://dbflute.seasar.org/>`__

Technical Documentation
--------------

- `OpenSearch API Reference <https://opensearch.org/docs/latest/api-reference/>`__
- `Apache Tika <https://tika.apache.org/>`__

Next Steps
==========

After understanding the architecture, refer to the following documents:

- :doc:`workflow` - Actual development flow
- :doc:`building` - Build and test
- :doc:`contributing` - Creating pull requests
