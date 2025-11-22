================================================
Open Source Full-text Search Server - |Fess| Development Overview
================================================

This page provides an overview of |Fess| development and basic information for getting started with development.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
====

|Fess| is an open-source full-text search server developed in Java.
It aims to make enterprise search easy to build,
providing powerful search capabilities and an easy-to-use administration interface.

|Fess| Features
-------------

- **Easy Setup**: Can be started immediately with a Java environment
- **Powerful Crawler**: Supports diverse data sources including websites, file systems, and databases
- **Japanese Support**: Optimized for Japanese full-text search
- **Extensibility**: Functional extensions possible through plugins
- **REST API**: Search capabilities can be used from other applications

Technology Stack
==========

|Fess| is developed using the following technologies.

Target Versions
------------

This documentation targets the following versions:

- **Fess**: 15.3.0
- **Java**: 21 or later
- **OpenSearch**: 3.3.0
- **Maven**: 3.x

Main Technologies and Frameworks
----------------------

Java 21
~~~~~~~

|Fess| is an application that runs on Java 21 or later.
It leverages the latest Java features to improve performance and maintainability.

- **Recommended**: Eclipse Temurin 21 (formerly AdoptOpenJDK)
- **Minimum version**: Java 21

LastaFlute
~~~~~~~~~~

`LastaFlute <https://github.com/lastaflute/lastaflute>`__ is the framework
used in |Fess|'s web application layer.

**Main features:**

- DI (Dependency Injection) container
- Action-based web framework
- Validation
- Message management
- Configuration management

**Learning resources:**

- `LastaFlute Official Documentation <https://github.com/lastaflute/lastaflute>`__
- You can learn practical usage by reading Fess code

DBFlute
~~~~~~~

`DBFlute <https://dbflute.seasar.org/>`__ is an O/R mapping tool
for database access.
In |Fess|, it is used to automatically generate Java code from OpenSearch schemas.

**Main features:**

- Type-safe SQL builder
- Automatic code generation from schemas
- Automatic database documentation generation

**Learning resources:**

- `DBFlute Official Site <https://dbflute.seasar.org/>`__

OpenSearch
~~~~~~~~~~

`OpenSearch <https://opensearch.org/>`__ is the distributed search and analytics engine
used as |Fess|'s search engine.

**Supported version**: OpenSearch 3.3.0

**Required plugins:**

- opensearch-analysis-fess: Fess-specific morphological analysis plugin
- opensearch-analysis-extension: Additional language analysis features
- opensearch-minhash: Similar document detection
- opensearch-configsync: Configuration synchronization

**Learning resources:**

- `OpenSearch Documentation <https://opensearch.org/docs/latest/>`__

Maven
~~~~~

Maven is used as |Fess|'s build tool.

**Main uses:**

- Dependency library management
- Build process execution
- Test execution
- Package creation

Development Tools
========

Recommended Development Environment
----------------

Eclipse
~~~~~~~

The official documentation explains development methods using Eclipse.

**Recommended version**: Eclipse 2023-09 or later

**Required plugins:**

- Maven Integration for Eclipse (m2e)
- Eclipse Java Development Tools

IntelliJ IDEA
~~~~~~~~~~~~~

Development is also possible with IntelliJ IDEA.

**Recommended edition**: Community Edition or Ultimate Edition

**Required features:**

- Maven support (included by default)
- Java support

VS Code
~~~~~~~

VS Code can also be used for lightweight development.

**Required extensions:**

- Java Extension Pack
- Maven for Java

Version Control
~~~~~~~~~~~~

- **Git**: Source code management
- **GitHub**: Repository hosting, Issue management, Pull requests

Required Knowledge
========

Basic Knowledge
--------

The following knowledge is required for |Fess| development:

**Required**

- **Java programming**: Classes, interfaces, generics, lambda expressions, etc.
- **Object-oriented**: Inheritance, polymorphism, encapsulation
- **Maven**: Basic commands and understanding of pom.xml
- **Git**: clone, commit, push, pull, branch, merge, etc.

**Recommended**

- **LastaFlute**: Concepts of Action, Form, Service
- **DBFlute**: How to use Behavior, ConditionBean
- **OpenSearch/Elasticsearch**: Basics of index, mapping, query
- **Web development**: HTML, CSS, JavaScript (especially for frontend development)
- **Linux commands**: Development and debugging in server environment

Learning Resources
----------

The following resources are useful for first-time |Fess| development:

Official Documentation
~~~~~~~~~~~~~~

- `Fess User Manual <https://fess.codelibs.org/ja/>`__
- `Fess Administrator Guide <https://fess.codelibs.org/ja/15.3/admin/index.html>`__

Community
~~~~~~~~~~

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__: Questions and discussions
- `Issue Tracker <https://github.com/codelibs/fess/issues>`__: Bug reports and feature requests
- `Fess Forum <https://discuss.codelibs.org/c/FessJA>`__: Japanese community forum

Source Code
~~~~~~~~~~

Reading actual code is the most effective learning method:

- Start by reading small features
- Trace code execution using a debugger
- Reference existing test code

Basic Development Flow
==============

|Fess| development generally proceeds as follows:

1. **Check/Create Issue**

   Check GitHub Issues and decide what to work on.
   Create an Issue for new features or bug fixes.

2. **Create Branch**

   Create a working branch:

   .. code-block:: bash

       git checkout -b feature/my-new-feature

3. **Coding**

   Implement features or fix bugs.

4. **Testing**

   Create and run unit tests to verify changes work correctly.

5. **Commit**

   Commit changes:

   .. code-block:: bash

       git add .
       git commit -m "Add new feature"

6. **Pull Request**

   Push to GitHub and create a pull request:

   .. code-block:: bash

       git push origin feature/my-new-feature

See :doc:`workflow` for details.

Project Structure Overview
==================

|Fess| source code has the following structure:

.. code-block:: text

    fess/
    ├── src/
    │   ├── main/
    │   │   ├── java/
    │   │   │   └── org/codelibs/fess/
    │   │   │       ├── app/           # Web application layer
    │   │   │       │   ├── web/       # Search screen
    │   │   │       │   └── service/   # Service layer
    │   │   │       ├── crawler/       # Crawler features
    │   │   │       ├── es/            # OpenSearch related
    │   │   │       ├── helper/        # Helper classes
    │   │   │       ├── job/           # Job processing
    │   │   │       ├── util/          # Utilities
    │   │   │       └── FessBoot.java  # Boot class
    │   │   ├── resources/
    │   │   │   ├── fess_config.properties
    │   │   │   ├── fess_config.xml
    │   │   │   └── ...
    │   │   └── webapp/
    │   │       └── WEB-INF/
    │   │           └── view/          # JSP files
    │   └── test/
    │       └── java/                  # Test code
    ├── pom.xml                        # Maven configuration file
    └── README.md

Main Packages
--------------

app
~~~

Code for the web application layer.
Includes Action, Form, Service for admin and search screens.

crawler
~~~~~~~

Code for data collection features such as web crawler, file crawler,
and data store crawler.

es
~~

Code for OpenSearch integration.
Includes index operations and search query construction.

helper
~~~~~~

Helper classes used throughout the application.

job
~~~

Code for jobs executed on a schedule.
Includes crawl jobs, index optimization jobs, etc.

See :doc:`architecture` for details.

Development Environment Quick Start
=======================

This explains how to set up the development environment and run |Fess| with minimal steps.

Prerequisites
--------

- Java 21 or later is installed
- Git is installed
- Maven 3.x is installed

Steps
----

1. **Clone Repository**

   .. code-block:: bash

       git clone https://github.com/codelibs/fess.git
       cd fess

2. **Download OpenSearch Plugins**

   .. code-block:: bash

       mvn antrun:run

3. **Run**

   Run from Maven:

   .. code-block:: bash

       mvn compile exec:java

   Or, run the ``org.codelibs.fess.FessBoot`` class from your IDE (Eclipse, IntelliJ IDEA, etc.).

4. **Access**

   Access the following in a browser:

   - Search screen: http://localhost:8080/
   - Admin screen: http://localhost:8080/admin/
     - Default user: admin / admin

See :doc:`setup` for detailed setup instructions.

Development Tips
==========

Debug Execution
----------

When running debug in IDE, execute the ``FessBoot`` class.
You can trace code execution in detail by setting breakpoints.

Hot Deploy
------------

LastaFlute can reflect some changes without restarting.
However, changes to class structure require a restart.

Checking Logs
--------

Logs are output to the ``target/fess/logs/`` directory.
Check log files when problems occur.

Operating OpenSearch
----------------

The embedded OpenSearch is located in ``target/fess/es/``.
You can also debug by calling OpenSearch API directly:

.. code-block:: bash

    # Check indices
    curl -X GET http://localhost:9201/_cat/indices?v

    # Search documents
    curl -X GET http://localhost:9201/fess.search/_search?pretty

Community and Support
==================

Questions and Consultation
--------

For questions or consultation during development, use the following:

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__: General questions and discussions
- `GitHub Issues <https://github.com/codelibs/fess/issues>`__: Bug reports and feature requests
- `Fess Forum <https://discuss.codelibs.org/c/FessJA>`__: Japanese forum

How to Contribute
--------

See :doc:`contributing` for how to contribute to |Fess|.

Next Steps
==========

When you're ready to set up the development environment, proceed to :doc:`setup`.

Also refer to the following documents for detailed information:

- :doc:`architecture` - Architecture and code structure
- :doc:`workflow` - Development workflow
- :doc:`building` - Build and test
- :doc:`contributing` - Contribution guide

References
========

Official Resources
----------

- `Fess Official Site <https://fess.codelibs.org/ja/>`__
- `GitHub Repository <https://github.com/codelibs/fess>`__
- `Download Page <https://fess.codelibs.org/ja/downloads.html>`__

Technical Documentation
--------------

- `LastaFlute <https://github.com/lastaflute/lastaflute>`__
- `DBFlute <https://dbflute.seasar.org/>`__
- `OpenSearch <https://opensearch.org/docs/latest/>`__

Community
----------

- `Fess Forum <https://discuss.codelibs.org/c/FessJA>`__
- `Twitter: @codelibs <https://twitter.com/codelibs>`__
