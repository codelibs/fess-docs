==================================
Scripting Overview
==================================

Overview
========

|Fess| allows you to implement custom logic using scripts in various scenarios.
By utilizing scripts, you can flexibly control data processing during crawling,
URL transformation, and scheduled job execution.

Supported Scripting Languages
==============================

|Fess| supports the following scripting languages:

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Language
     - Identifier
     - Description
   * - Groovy
     - ``groovy``
     - The scripting language registered by default. Java-compatible with powerful features

.. note::
   The only scripting engine registered in |Fess| by default is Groovy.
   The default scripting language is ``groovy`` (``Constants.DEFAULT_SCRIPT``).
   All script examples in this documentation are written in Groovy syntax.

Use Cases for Scripts
=====================

Data Store Configuration
------------------------

Data store connectors use scripts to map retrieved data to index fields.
Configuration is written one line per entry in the format ``field=expression``,
and each line is evaluated as a single independent Groovy expression.

::

    url=site_url
    title=name
    content=description
    last_modified=updated_at

The variable names available in data store scripts differ depending on the connector type.
For example, in the CSV data store and JSON data store, each column name or field name is
available directly as a variable (no common prefix such as ``data`` is added).
For file-based connectors (Box, Google Drive, OneDrive, etc.) the prefix is ``file.*``,
for Slack it is ``message.*``, and so on — each connector has its own prefix convention.
Refer to the documentation for each data store connector for details on available variables.

.. note::
   Because each line in a data store script is evaluated as a single expression,
   multi-line ``if`` blocks, ``import`` statements, and variable declarations using ``def``
   cannot be used. To conditionally assign a value, use the ternary operator on a per-field basis
   (e.g., ``title=enabled == "true" ? name : null``). When referencing a class, write its
   fully qualified class name (FQCN) inline.

Path Mapping
------------

Path mapping is a feature for normalizing and transforming crawl target URLs.
By default, it is configured as a pair of a regular expression and a replacement string,
and is not a Groovy script.
For example, specifying ``http://`` as the regular expression and ``https://`` as the
replacement string replaces the URL scheme.

A replacement string is evaluated as a Groovy script only when it is prefixed with ``groovy:``.
Inside this script, ``url`` (the URL string being transformed) and ``matcher``
(the ``java.util.regex.Matcher`` for the regular expression) are available.

::

    groovy:url.replaceAll("http://", "https://")

Scheduled Jobs
--------------

Scheduled jobs allow you to write custom processing logic in Groovy scripts.
Because the entire script is evaluated as a single Groovy script,
multi-line expressions, ``import`` statements, and variable declarations using ``def``
are all supported.

::

    return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);

Methods such as ``logLevel("info")`` are methods of the job class (``ExecJob`` and its subclasses)
and can be chained. For the ``executor`` variable, see "Execution Context and Available Objects".

Basic Syntax
============

The following are basic Groovy syntax examples. Comments use ``//`` (line comments) or
``/* */`` (block comments). Note that comments starting with ``#`` cannot be used in Groovy.

Variable Access
---------------

::

    // Access a data store field (in CSV/JSON, access by column name or field name)
    title

    // Retrieve a component from the DI container
    container.getComponent("systemHelper")

String Operations
-----------------

::

    // Concatenation
    title + " - " + category

    // Replacement
    content.replaceAll("old", "new")

    // Splitting
    tags.split(",")

Conditional Branching
---------------------

::

    // Ternary operator
    status == "active" ? "Active" : "Inactive"

    // Default value when null or empty (Elvis operator)
    description ?: "No description"

Date Operations
---------------

::

    // Current date/time
    new Date()

    // Formatting
    new java.text.SimpleDateFormat("yyyy-MM-dd").format(updated_at)

Execution Context and Available Objects
========================================

The objects available inside a script depend on the context in which the script runs.
Only ``container`` is available in all contexts.

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Execution Context
     - Available Objects
     - Description
   * - All contexts
     - ``container``
     - The DI container. Access individual components via
       ``container.getComponent("systemHelper")`` or
       ``container.getComponent("fessConfig")``
   * - Data store scripts
     - Connector-specific field variables
     - Each field retrieved from the data store is available as a variable
       (variable names and prefixes differ by connector; CSV/JSON use the field name directly)
   * - Path mapping
     - ``url`` ``matcher``
     - The URL string being transformed and the ``Matcher`` for the regular expression
       (available only when the replacement is prefixed with ``groovy:``)
   * - Scheduled jobs
     - ``executor``
     - The job execution instance (``JobExecutor``). Used to control job shutdown

.. note::
   Objects other than ``container`` are injected only in specific contexts.
   For example, ``executor`` is available only in scheduled jobs and cannot be used
   in data store scripts or path mapping.

Security
========

.. warning::
   Scripts have powerful capabilities, so only use them from trusted sources.

- Scripts are executed on the server
- Access to the file system and network is possible
- Ensure that only users with administrator privileges can edit scripts
- Script execution is recorded in the audit log (``audit.log``).
  Whether recording is enabled is controlled by ``script.audit.log.enabled``, which defaults to ``true``.
  The maximum length of the script string that is recorded is controlled by
  ``script.audit.log.max.length``, which defaults to ``100`` characters.

Performance
===========

Tips for optimizing script performance:

1. **Avoid complex processing**: Data store scripts are executed for each document
2. **Minimize external resource access**: Network calls cause delays
3. **Use caching**: Consider caching values that are used repeatedly

Debugging
=========

In scheduled job scripts, because the entire script is evaluated as a single Groovy script,
you can use log output for debugging.
(Data store scripts evaluate one line as one expression, so ``import`` statements and
multi-line processing cannot be used.)

::

    import org.apache.logging.log4j.LogManager
    def logger = LogManager.getLogger("fess.script")
    logger.info("executor = {}", executor)

The example above uses a logger named ``fess.script``.
To output this log, add the corresponding logger configuration to
``app/WEB-INF/classes/log4j2.xml``.

::

    <Logger name="fess.script" level="DEBUG"/>

To enable debug logging for the scripting engine itself, set the log level of the
``org.codelibs.fess.script`` package to ``DEBUG``.

::

    <Logger name="org.codelibs.fess.script" level="DEBUG"/>

Reference Information
=====================

- :doc:`scripting-groovy` - Groovy Scripting Guide
- :doc:`../admin/dataconfig-guide` - Data Store Configuration Guide
- :doc:`../admin/scheduler-guide` - Scheduler Configuration Guide
