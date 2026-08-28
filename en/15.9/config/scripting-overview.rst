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
   * - JavaScript
     - ``javascript`` (aliases: ``js`` , ``sai`` )
     - The scripting language built into |Fess| by default, and the default scripting
       language ( ``Constants.DEFAULT_SCRIPT`` ). It runs on Sai (a Nashorn fork by
       CodeLibs that |Fess| already uses for its DI XML expressions); scripts are
       executed as ECMAScript 6.
   * - Groovy
     - ``groovy``
     - Provided as the ``fess-script-groovy`` plugin. It is bundled with the 15.9
       distribution, so it works out of the box, but **it will no longer be bundled
       starting with 15.10**, when it must be installed from the administration screen.

.. note::
   A script configuration that has no recorded script type is treated as Groovy.
   This is not a temporary transition measure but a permanent behavior: a configuration
   created before 15.9 keeps its Groovy-syntax script without a recorded script type, so
   this default is what keeps it working unchanged after an upgrade. A configuration
   created from 15.9 onward has its script type explicitly recorded as ``javascript``.

   Unless noted otherwise, the script examples in this documentation are written in
   JavaScript syntax. For Groovy syntax, see :doc:`scripting-groovy`.

Use Cases for Scripts
=====================

Data Store Configuration
------------------------

Data store connectors use scripts to map retrieved data to index fields.
Configuration is written one line per entry in the format ``field=expression``,
and each line is evaluated as a single independent script expression (JavaScript
by default).

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
   multi-line ``if`` blocks and variable-declaration statements such as ``let`` / ``const``
   cannot be used. To conditionally assign a value, use the ternary operator on a per-field
   basis (e.g., ``title=enabled === "true" ? name : null``). When referencing a class, write
   its fully qualified class name (FQCN) inline.

Path Mapping
------------

Path mapping is a feature for normalizing and transforming crawl target URLs.
By default, it is configured as a pair of a regular expression and a replacement string,
and is not a script.
For example, specifying ``http://`` as the regular expression and ``https://`` as the
replacement string replaces the URL scheme.

When a replacement string starts with ``(engine name):``, the part before the colon is
read as the name of a scripting engine, and if it matches a registered engine, the rest
of the string is evaluated as a script by that engine. For example, ``groovy:`` selects
the Groovy engine (which requires the ``fess-script-groovy`` plugin), and
``javascript:`` (aliases ``js:``, ``sai:``) selects the JavaScript engine. If the part
before the colon does not match any registered engine name — ``https://`` in an ordinary
replacement string, for example — the whole string is not treated as a script at all and
is instead used as-is as a plain regular-expression replacement. When the string is
evaluated as a script, ``url`` (the URL string being transformed) and ``matcher`` (the
``java.util.regex.Matcher`` for the regular expression) are available inside it.

::

    javascript:url.replace(/http:\/\//g, "https://")

Scheduled Jobs
--------------

Scheduled jobs allow you to write custom processing logic in a script.
Because the entire script is evaluated as a single script, multi-line statements are
supported, including — for JavaScript — ``let`` / ``const`` variable declarations and
control-flow statements.

::

    return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);

A top-level ``return`` statement is normally a syntax error in JavaScript. |Fess|'s
scripting engine first tries to compile the script as an expression, and only falls back
to compiling it as a block of statements when that fails. This example cannot be compiled
as an expression, so it is compiled as a statement block and runs as shown. See
:doc:`scripting-javascript` for details.

Methods such as ``logLevel("info")`` are methods of the job class (``ExecJob`` and its subclasses)
and can be chained. For the ``executor`` variable, see "Execution Context and Available Objects".

Basic Syntax
============

The following are basic JavaScript syntax examples. Comments use ``//`` (line comments) or
``/* */`` (block comments). Note that comments starting with ``#`` cannot be used in
JavaScript either.

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

    // Replacement (using a regular expression; ECMAScript 6 has no String#replaceAll)
    content.replace(/old/g, "new")

    // Splitting
    tags.split(",")

Conditional Branching
---------------------

::

    // Ternary operator
    status === "active" ? "Active" : "Inactive"

    // Default value when null or empty (logical OR operator; JavaScript has no Elvis operator)
    description || "No description"

Date Operations
---------------

::

    // Current date/time
    new Date()

    // Formatting (Java interop uses the same notation as Groovy)
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
       (available only when the replacement is prefixed with ``(engine name):``; the
       prefixed name, e.g. ``groovy`` or ``javascript``, selects which language runs)
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

In scheduled job scripts, because the entire script is evaluated as a single script,
you can use log output for debugging.
(Data store scripts evaluate one line as one expression, so multi-line processing
cannot be used.)

::

    const logger = org.apache.logging.log4j.LogManager.getLogger("fess.script");
    logger.info("executor = {}", executor);

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

- :doc:`scripting-javascript` - JavaScript Scripting Guide
- :doc:`scripting-groovy` - Groovy Scripting Guide (plugin)
- :doc:`../admin/dataconfig-guide` - Data Store Configuration Guide
- :doc:`../admin/scheduler-guide` - Scheduler Configuration Guide
