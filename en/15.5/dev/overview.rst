==================================
Developer Documentation Overview
==================================

Overview
========

This section explains how to extend |Fess|.
It provides information on plugin development, custom connector creation, theme customization,
and other ways to extend |Fess|.

Target Audience
===============

- Developers who want to create custom features for |Fess|
- Developers who want to create plugins
- Developers who want to understand the |Fess| source code

Prerequisites
-------------

- Basic knowledge of Java 21
- Basics of Maven (build system)
- Experience with web application development

Development Environment
=======================

Recommended Environment
-----------------------

- **JDK**: OpenJDK 21 or higher
- **IDE**: IntelliJ IDEA / Eclipse / VS Code
- **Build Tool**: Maven 3.9 or higher
- **Git**: Version control

Setup
-----

1. Get the source code:

::

    git clone https://github.com/codelibs/fess.git
    cd fess

2. Build:

::

    mvn package -DskipTests

3. Start the development server:

::

    ./bin/fess

Architecture Overview
=====================

|Fess| consists of the following major components:

Component Structure
-------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Component
     - Description
   * - Web Layer
     - MVC implementation using LastaFlute framework
   * - Service Layer
     - Business logic
   * - Data Access Layer
     - OpenSearch integration using DBFlute
   * - Crawler
     - Content collection using fess-crawler library
   * - Search Engine
     - Full-text search using OpenSearch

Major Frameworks
----------------

- **LastaFlute**: Web framework (actions, forms, validation)
- **DBFlute**: Data access framework (OpenSearch integration)
- **Lasta Di**: Dependency injection container

Directory Structure
===================

::

    fess/
    ├── src/main/java/org/codelibs/fess/
    │   ├── app/
    │   │   ├── web/         # Controllers (Action)
    │   │   ├── service/     # Services
    │   │   └── pager/       # Pagination
    │   ├── api/             # REST API
    │   ├── helper/          # Helper classes
    │   ├── crawler/         # Crawler related
    │   ├── opensearch/      # OpenSearch integration (DBFlute generated)
    │   ├── llm/             # LLM integration
    │   └── ds/              # DataStore connectors
    ├── src/main/resources/
    │   ├── fess_config.properties  # Configuration
    │   └── fess_*.xml              # DI configuration
    └── src/main/webapp/
        └── WEB-INF/view/    # JSP templates

Extension Points
================

|Fess| provides the following extension points:

Plugins
-------

You can add features using plugins.

- **DataStore Plugin**: Crawl from new data sources
- **Script Engine Plugin**: Support for new scripting languages
- **Web App Plugin**: Extend the web interface
- **Ingest Plugin**: Process data during indexing

Details: :doc:`plugin-architecture`

Themes
------

You can customize the design of the search screen.

Details: :doc:`theme-development`

Configuration
-------------

Many behaviors can be customized via ``fess_config.properties``.

Details: :doc:`../config/intro`

Plugin Development
==================

For details on plugin development, see the following:

- :doc:`plugin-architecture` - Plugin Architecture
- :doc:`datastore-plugin` - DataStore Plugin Development
- :doc:`script-engine-plugin` - Script Engine Plugin
- :doc:`webapp-plugin` - Web App Plugin
- :doc:`ingest-plugin` - Ingest Plugin

Theme Development
=================

- :doc:`theme-development` - Theme Customization

Best Practices
==============

Coding Standards
----------------

- Follow the existing |Fess| code style
- Format code with ``mvn formatter:format``
- Add license headers with ``mvn license:format``

Testing
-------

- Write unit tests (``*Test.java``)
- Integration tests use ``*Tests.java``

Logging
-------

- Use Log4j2
- Use ``logger.debug()`` / ``logger.info()`` / ``logger.warn()`` / ``logger.error()``
- Do not log sensitive information

Resources
=========

- `GitHub Repository <https://github.com/codelibs/fess>`__
- `Issue Tracker <https://github.com/codelibs/fess/issues>`__
- `Discussions <https://github.com/codelibs/fess/discussions>`__

