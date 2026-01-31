==================================
Scripting Overview
==================================

Overview
========

|Fess| allows you to implement custom logic using scripts in various scenarios.
By utilizing scripts, you can flexibly control data processing during crawling,
search result customization, and scheduled job execution.

Supported Scripting Languages
=============================

|Fess| supports the following scripting languages:

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Language
     - Identifier
     - Description
   * - Groovy
     - ``groovy``
     - The default scripting language. Java-compatible with powerful features
   * - JavaScript
     - ``javascript``
     - A familiar language for web developers

.. note::
   Groovy is the most widely used, and the examples in this documentation are written in Groovy.

Use Cases for Scripts
=====================

Data Store Configuration
------------------------

Data store connectors use scripts to map retrieved data to index fields.

::

    url="https://example.com/article/" + data.id
    title=data.name
    content=data.description
    lastModified=data.updated_at

Path Mapping
------------

Scripts can be used for URL normalization and path conversion.

::

    # Transform URL
    url.replaceAll("http://", "https://")

Scheduled Jobs
--------------

Scheduled jobs allow you to write custom processing logic in Groovy scripts.

::

    return container.getComponent("crawlJob").execute();

Basic Syntax
============

Variable Access
---------------

::

    # Access data store data
    data.fieldName

    # Access system components
    container.getComponent("componentName")

String Operations
-----------------

::

    # Concatenation
    title + " - " + category

    # Replacement
    content.replaceAll("old", "new")

    # Splitting
    tags.split(",")

Conditional Branching
---------------------

::

    # Ternary operator
    data.status == "active" ? "Active" : "Inactive"

    # Null check
    data.description ?: "No description"

Date Operations
---------------

::

    # Current date/time
    new Date()

    # Formatting
    new java.text.SimpleDateFormat("yyyy-MM-dd").format(data.date)

Available Objects
=================

Main objects available within scripts:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Object
     - Description
   * - ``data``
     - Data retrieved from the data store
   * - ``container``
     - DI container (access to components)
   * - ``systemHelper``
     - System helper
   * - ``fessConfig``
     - |Fess| configuration

Security
========

.. warning::
   Scripts have powerful capabilities, so only use them from trusted sources.

- Scripts are executed on the server
- Access to the file system and network is possible
- Ensure only users with administrator privileges can edit scripts

Performance
===========

Tips for optimizing script performance:

1. **Avoid complex processing**: Scripts are executed for each document
2. **Minimize external resource access**: Network calls cause delays
3. **Use caching**: Consider caching values that are used repeatedly

Debugging
=========

Use log output to debug scripts:

::

    import org.apache.logging.log4j.LogManager
    def logger = LogManager.getLogger("script")
    logger.info("data.id = {}", data.id)

Log level configuration:

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="script" level="DEBUG"/>

Reference Information
=====================

- :doc:`scripting-groovy` - Groovy Scripting Guide
- :doc:`../admin/dataconfig-guide` - Data Store Configuration Guide
- :doc:`../admin/scheduler-guide` - Scheduler Configuration Guide
