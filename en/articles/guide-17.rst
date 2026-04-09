============================================================
Part 17: Extending Search with Plugins -- Implementing Custom Data Sources and Ingest Pipelines
============================================================

Introduction
============

Fess supports many data sources out of the box, but extending it through plugins may be necessary to accommodate company-specific systems and data formats.

This article explains the plugin architecture of Fess and introduces how to implement custom data source plugins and Ingest plugins.

Target Audience
===============

- Those who want to connect Fess to custom data sources
- Java developers interested in plugin development
- Those who want to understand the internal architecture of Fess

Plugin Architecture
====================

Fess provides the following types of plugins.

.. list-table:: Plugin Types
   :header-rows: 1
   :widths: 25 35 40

   * - Type
     - Role
     - Examples
   * - Data Store (fess-ds-*)
     - Retrieve data from external data sources
     - Slack, Salesforce, DB
   * - Ingest (fess-ingest-*)
     - Process and transform crawled data
     - Example
   * - Theme (fess-theme-*)
     - Search screen design
     - Simple, Code Search
   * - Script (fess-script-*)
     - Scripting language support
     - OGNL
   * - Web App (fess-webapp-*)
     - Web application extensions
     - MCP Server

Plugin Deployment
-----------------

Plugins are provided as JAR files and placed in the Fess plugin directory.
They can be installed and managed from [System] > [Plugins] in the administration console.

Developing a Custom Data Source Plugin
=======================================

This section explains the development process for a data source plugin, assuming you have a proprietary in-house document management system.

Project Structure
-----------------

Create a Maven project by referring to an existing data store plugin (e.g., fess-ds-git).

::

    fess-ds-custom/
    ├── pom.xml
    └── src/
        └── main/
            └── java/
                └── org/codelibs/fess/ds/custom/
                    └── CustomDataStore.java

pom.xml Configuration
---------------------

Specify fess-parent as the parent POM and configure the required dependencies.

.. code-block:: xml

    <parent>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-parent</artifactId>
        <version>15.5.0</version>
    </parent>

    <artifactId>fess-ds-custom</artifactId>
    <packaging>jar</packaging>

    <dependencies>
        <dependency>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess</artifactId>
            <version>${fess.version}</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>

Implementing the Data Store Class
----------------------------------

The core of a data store plugin is the class that retrieves data and registers documents in Fess.

The key implementation points are as follows:

1. Connection and authentication with the external system
2. Data retrieval (API calls, file reading, etc.)
3. Converting retrieved data into the Fess document format
4. Document registration

**Field Mapping**

Map the retrieved data to Fess fields.
The main fields are as follows:

- ``title``: Document title
- ``url``: Document URL (link destination in search results)
- ``content``: Document body (search target)
- ``mimetype``: MIME type
- ``last_modified``: Last modified date and time

Build and Deploy
----------------

::

    $ mvn clean package

Place the generated JAR file in the Fess plugin directory and restart Fess.

Developing an Ingest Plugin
=============================

An Ingest plugin is a mechanism for processing and transforming documents obtained through crawling before they are registered in the index.

Use Cases
---------

- Adding extra fields to crawled documents
- Cleansing body text (removing unnecessary characters)
- Enriching with external APIs (translation, classification, etc.)
- Log output (for debugging)

Implementation Points
---------------------

In an Ingest plugin, you access the document data just before it is registered in the index and perform transformation processing.

For example, you can implement processing to add organization name metadata to all documents, or processing to remove specific patterns from body text.

Developing a Theme Plugin
==========================

If you want to fully customize the search screen design, develop a theme plugin.

Theme Structure
---------------

A theme plugin consists of JSP files, CSS, JavaScript, and image files.

::

    fess-theme-custom/
    ├── pom.xml
    └── src/
        └── main/
            └── resources/
                ├── css/
                ├── js/
                ├── images/
                └── view/
                    ├── index.jsp
                    ├── search.jsp
                    └── header.jsp

Customize the design by modifying JSP and CSS while referring to existing themes.

Development Best Practices
============================

Referring to Existing Plugins
-----------------------------

When developing a new plugin, it is strongly recommended to refer to the source code of existing plugins.
The source code for all plugins is available on the CodeLibs GitHub repository.

For example, ``fess-ds-git`` and ``fess-ds-slack`` are good references for data store plugin development.

Testing
-------

Test plugins from the following perspectives:

- Connection testing with external systems
- Accuracy of data transformation
- Error handling (connection failures, invalid data, etc.)
- Performance (processing time for large volumes of data)

Version Compatibility
---------------------

Verify plugin compatibility when upgrading Fess.
There may be API changes during major version upgrades of Fess.

Summary
=======

This article explained plugin development for Fess.

- Overview of the plugin architecture (data store, Ingest, theme, script)
- Development process for custom data source plugins
- Document processing with Ingest plugins
- UI customization with theme plugins
- Development best practices

Plugins allow you to extend Fess to meet organization-specific requirements.
This concludes the Architecture and Scaling series. Starting from the next article, the AI and Next-Generation Search series will cover the fundamentals of semantic search.

References
==========

- `Fess Plugin Management <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__

- `CodeLibs GitHub <https://github.com/codelibs>`__
