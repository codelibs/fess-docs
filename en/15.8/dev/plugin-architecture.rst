==================================
Plugin Architecture
==================================

Overview
========

The |Fess| plugin system lets you extend core functionality.
Plugins are distributed as JAR files, and once added to the classpath,
their components are loaded by the DI container (Lasta Di) and
registered with the corresponding factory or manager.

Plugin Types
============

|Fess| determines the plugin type from the prefix of the artifact name
(``PluginHelper.ArtifactType``). The main types are as follows:

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - Type
     - Prefix
     - Description
   * - Data Store
     - ``fess-ds-*``
     - Retrieves content from new data sources (Box, Slack, Git, etc.)
   * - Web App
     - ``fess-webapp-*``
     - Extends the web interface and search functionality
   * - Script Engine
     - ``fess-script-*``
     - Adds support for new scripting languages
   * - Ingest
     - ``fess-ingest-*``
     - Processes documents during index registration
   * - Theme
     - ``fess-theme-*``
     - Customizes the design of the search screen
   * - Thumbnail
     - ``fess-thumbnail-*``
     - Adds new thumbnail generation methods
   * - LLM
     - ``fess-llm-*``
     - Adds LLM providers used for RAG/chat
   * - Crawler
     - ``fess-crawler-*``
     - Extends crawler clients

Plugin Structure
=================

Basic Structure
----------------

Taking `fess-ds-example <https://github.com/codelibs/fess-ds-example>`__,
the implementation template for Data Store plugins, as an example, a
plugin consists of an "implementation class" and a "DI registration
file":

::

    fess-ds-example/
    ├── pom.xml
    └── src/main/
        ├── java/org/codelibs/fess/ds/example/
        │   └── ExampleDataStore.java     # Data Store implementation
        └── resources/
            └── fess_ds++.xml             # DI component registration

pom.xml Example
-----------------

The plugin is built as a jar with ``fess-parent`` as the parent POM.
Libraries such as ``fess`` and ``opensearch``, which are supplied by
the |Fess| core at runtime, are declared with ``provided`` scope.
Version numbers and build settings (formatter, license header, etc.)
are inherited from the parent POM.

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

   On branches under development, the version has a ``-SNAPSHOT``
   suffix, such as ``15.8.0-SNAPSHOT``. Dependencies specific to the
   plugin are declared as ordinary Maven dependencies. Since these are
   not bundled with the |Fess| core, they must be distributed together
   with the plugin.

Plugin Registration
=====================

Registering with the DI Container
------------------------------------

Plugins register components using a DI configuration file whose name
ends in ``++``, such as ``fess_ds++.xml``. Lasta Di automatically
merges any file with a ``++`` suffix found on the classpath into the
corresponding configuration file in the |Fess| core (``fess_ds.xml``
in this example). This mechanism lets a plugin add its own components
without modifying any file in the |Fess| core.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
            <postConstruct name="register"></postConstruct>
        </component>
    </components>

The target file for merging differs depending on the plugin type. For
example, Script Engine plugins use ``fess_se++.xml``, Ingest plugins
use ``fess_ingest++.xml``, LLM providers use ``fess_llm++.xml``, and
Web App plugins use ``app++.xml``.

Component Initialization
--------------------------

``<postConstruct name="register">`` is a Lasta Di lifecycle setting
that specifies the method to invoke after the component is created.
In the case of a Data Store, the ``register()`` method provided by
``AbstractDataStore`` is invoked, which registers the component itself
with the ``DataStoreFactory``:

.. code-block:: java

    // Implementation in AbstractDataStore (normally no need to override)
    public void register() {
        ComponentUtil.getDataStoreFactory().add(getName(), this);
    }

.. note::

   Note that this is not Java's ``@PostConstruct`` annotation, but
   initialization via the ``<postConstruct>`` element in the DI
   configuration file. The name registered here is the return value of
   ``getName()``, and this becomes the name used when selecting the
   plugin in the admin console.

Plugin Lifecycle
==================

Initialization
----------------

1. The plugin JAR is added to the classpath
2. The DI container merges ``fess_*++.xml`` and creates the components
3. The method specified in ``<postConstruct>`` (e.g., ``register``) is
   invoked
4. The plugin is registered with the corresponding factory/manager

Termination
------------

1. When the DI container shuts down, the method specified in
   ``<preDestroy>`` is invoked (if defined)
2. Resources are cleaned up

.. note::

   In the case of a Data Store, an in-progress crawl has its stop flag
   set by ``AbstractDataStore.stop()``, which allows the record
   processing loop to terminate safely.

Dependencies
=============

Dependency on the Fess Core
-----------------------------

Since classes in the |Fess| core are present on the server's classpath
at runtime, declare the dependency with ``provided`` scope (do not
bundle it into the plugin JAR).

.. code-block:: xml

    <dependency>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess</artifactId>
        <scope>provided</scope>
    </dependency>

External Libraries
--------------------

A plugin can include its own dependency libraries:

.. code-block:: xml

    <dependency>
        <groupId>com.example</groupId>
        <artifactId>example-sdk</artifactId>
        <version>1.0.0</version>
    </dependency>

Since these are not bundled with the |Fess| core, they must be
distributed together with the plugin.

Retrieving Configuration
==========================

Retrieving Parameters and FessConfig
--------------------------------------

In a Data Store's ``storeData()``, parameters configured in the admin
console are retrieved from ``DataStoreParams``. Use ``getAsString()``
to retrieve values (since ``DataStoreParams`` does not implement
``Map``, ``get()`` does not return a string). |Fess| configuration
values can also be retrieved from ``ComponentUtil.getFessConfig()``:

.. code-block:: java

    public class ExampleDataStore extends AbstractDataStore {

        @Override
        protected String getName() {
            // Used as the handler name. Convention is to return the class's simple name
            return this.getClass().getSimpleName();
        }

        @Override
        protected void storeData(final DataConfig dataConfig, final IndexUpdateCallback callback,
                final DataStoreParams paramMap, final Map<String, String> scriptMap,
                final Map<String, Object> defaultDataMap) {

            // Retrieve parameters
            final String apiKey = paramMap.getAsString("api.key");
            final String baseUrl = paramMap.getAsString("base.url");

            // Retrieve FessConfig
            final FessConfig fessConfig = ComponentUtil.getFessConfig();
        }
    }

For details on how to implement ``storeData()`` (the flow of data
retrieval, script evaluation, and index registration), see
:doc:`datastore-plugin`.

Build and Installation
========================

Build
------

::

    mvn clean package

A JAR file (e.g., ``fess-ds-example-15.8.0.jar``) is generated in the
``target/`` directory.

Installation
-------------

1. **From the admin console**:

   - Open "System" -> "Plugin" -> "Install"
   - Select from the list of plugin repositories, or upload and
     install the JAR file you built

2. **Manually**:

   - Copy the JAR file to the ``app/WEB-INF/plugin/`` directory
   - Restart |Fess|

For details on the installation procedure, see
:doc:`../admin/plugin-guide`.

Debugging
==========

Logging
--------

|Fess| uses Log4j2. Obtain a logger with ``LogManager.getLogger()``:

.. code-block:: java

    private static final Logger logger = LogManager.getLogger(ExampleDataStore.class);

    public void someMethod() {
        logger.debug("Debug message");
        logger.info("Info message");
    }

.. note::

   Do not output sensitive information such as passwords or tokens to
   the log.

Development Mode
------------------

During development, you can start |Fess| from your IDE for debugging:

1. Debug-run the ``org.codelibs.fess.FessBoot`` class
2. Include the plugin's source code in the project
3. Set breakpoints

List of Published Plugins
===========================

Many plugins are published by the |Fess| project. The following are
representative examples (this is not an exhaustive list):

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Plugin
     - Description
   * - ``fess-ds-box``
     - Box connector
   * - ``fess-ds-dropbox``
     - Dropbox connector
   * - ``fess-ds-slack``
     - Slack connector
   * - ``fess-ds-atlassian``
     - JIRA / Confluence connector
   * - ``fess-ds-git``
     - Git repository connector
   * - ``fess-llm-openai``
     - OpenAI LLM provider
   * - ``fess-theme-*``
     - Custom themes

In addition, Data Store connectors such as ``fess-ds-csv`` /
``fess-ds-db`` / ``fess-ds-json`` / ``fess-ds-microsoft365`` /
``fess-ds-sharepoint``, and LLM providers such as ``fess-llm-ollama`` /
``fess-llm-gemini``, are also published. These plugins are published
on `GitHub <https://github.com/codelibs>`__ as a reference for
development.

Reference
==========

- :doc:`datastore-plugin` - Data Store plugin development
- :doc:`script-engine-plugin` - Script Engine plugin
- :doc:`webapp-plugin` - Web App plugin
- :doc:`ingest-plugin` - Ingest plugin
- :doc:`theme-development` - Theme customization
- :doc:`../admin/plugin-guide` - Plugin installation
</content>
