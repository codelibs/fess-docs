==================================
Plugin Architecture
==================================

Overview
========

The |Fess| plugin system allows you to extend core functionality.
Plugins are distributed as JAR files and are loaded dynamically.

Plugin Types
============

|Fess| supports the following types of plugins:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Type
     - Description
   * - DataStore
     - Content retrieval from new data sources (Box, Slack, etc.)
   * - Script Engine
     - Support for new scripting languages
   * - Web App
     - Web interface extensions
   * - Ingest
     - Data processing during indexing

Plugin Structure
================

Basic Structure
---------------

::

    fess-ds-example/
    ├── pom.xml
    └── src/main/java/org/codelibs/fess/ds/example/
        ├── ExampleDataStore.java      # DataStore implementation
        └── ExampleDataStoreHandler.java # Handler (optional)

pom.xml Example
---------------

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

Plugin Registration
===================

DI Container Registration
-------------------------

Plugins are registered via configuration files such as ``fess_ds.xml``:

.. code-block:: xml

    <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
        <postConstruct name="register"/>
    </component>

Auto Registration
-----------------

Many plugins auto-register using the ``@PostConstruct`` annotation:

.. code-block:: java

    @PostConstruct
    public void register() {
        ComponentUtil.getDataStoreManager().add(this);
    }

Plugin Lifecycle
================

Initialization
--------------

1. JAR file is loaded
2. DI container initializes components
3. ``@PostConstruct`` methods are called
4. Plugin is registered with the manager

Shutdown
--------

1. ``@PreDestroy`` methods are called (if defined)
2. Resources are cleaned up

Dependencies
============

Fess Core Dependency
--------------------

.. code-block:: xml

    <dependency>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess</artifactId>
        <version>${fess.version}</version>
        <scope>provided</scope>
    </dependency>

External Libraries
------------------

Plugins can include their own dependency libraries:

.. code-block:: xml

    <dependency>
        <groupId>com.example</groupId>
        <artifactId>example-sdk</artifactId>
        <version>1.0.0</version>
    </dependency>

Dependency libraries can be distributed with the plugin JAR or
bundled into a fat JAR using Maven Shade Plugin.

Configuration Retrieval
=======================

Getting from FessConfig
-----------------------

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

            // Get parameters
            String apiKey = paramMap.get("api.key");
            String baseUrl = paramMap.get("base.url");

            // Get FessConfig
            FessConfig fessConfig = ComponentUtil.getFessConfig();
        }
    }

Build and Installation
======================

Build
-----

::

    mvn clean package

Installation
------------

1. **From Admin Console**:

   - Go to "System" -> "Plugins" -> "Install"
   - Enter the plugin name and install

2. **Command Line**:

   ::

       ./bin/fess-plugin install fess-ds-example

3. **Manual**:

   - Copy JAR file to ``plugins/`` directory
   - Restart |Fess|

Debugging
=========

Log Output
----------

.. code-block:: java

    private static final Logger logger = LogManager.getLogger(ExampleDataStore.class);

    public void someMethod() {
        logger.debug("Debug message");
        logger.info("Info message");
    }

Development Mode
----------------

During development, you can debug |Fess| from your IDE:

1. Debug run the ``FessBoot`` class
2. Include the plugin source in your project
3. Set breakpoints

Published Plugins
=================

Main plugins published by the |Fess| project:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Plugin
     - Description
   * - fess-ds-box
     - Box.com connector
   * - fess-ds-dropbox
     - Dropbox connector
   * - fess-ds-slack
     - Slack connector
   * - fess-ds-atlassian
     - Confluence/Jira connector
   * - fess-ds-git
     - Git repository connector
   * - fess-theme-*
     - Custom themes

These plugins are available on
`GitHub <https://github.com/codelibs>`__ as development references.

Reference
=========

- :doc:`datastore-plugin` - DataStore Plugin Development
- :doc:`script-engine-plugin` - Script Engine Plugin
- :doc:`webapp-plugin` - Web App Plugin
- :doc:`ingest-plugin` - Ingest Plugin

