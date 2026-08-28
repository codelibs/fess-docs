==================================
JavaScript Scripting Guide
==================================

Overview
========

JavaScript is the default scripting language for |Fess| starting with 15.9.
It runs on Sai (a Nashorn fork by CodeLibs that |Fess| already uses for its DI XML
expressions), and scripts are executed as ECMAScript 6. Its identifier is
``javascript``, and it can also be specified using the aliases ``js`` and ``sai``.

.. _javascript-statement-null:

How Scripts Are Evaluated
==========================

|Fess|'s scripting engine first tries to compile the script text as a single
"expression." Only if that fails to parse does it recompile the text as a block of
"statements."

Because of this, a simple expression that just returns a value:

::

    content.length()

and a script that contains a top-level ``return`` statement:

::

    return container.getComponent("crawlJob").execute();

both work without issue. The latter is normally a syntax error in plain JavaScript,
because a top-level ``return`` is not allowed. But since it cannot be compiled as an
expression, it is reinterpreted as a statement block and runs as a valid script.

In places where each line is treated as a single expression, such as data store
scripts, a script consisting of multiple statements cannot be used. In places where
the entire script is evaluated, such as scheduled jobs, you can freely use multi-line
statements, ``let`` / ``const`` variable declarations, and control-flow constructs.

.. warning::

   A script that is compiled as a statement block returns a value only when it contains an
   explicit ``return``. When the text fails to parse as an expression it is wrapped in a
   function and run as a block of statements, and a block with no ``return`` evaluates to
   ``null``. A single trailing semicolon is enough to cross that line:

   .. list-table::
      :header-rows: 1
      :widths: 40 15 45

      * - Script
        - Result
        - Reason
      * - ``content.length()``
        - ``11``
        - Parses as an expression; the value of the expression is the result
      * - ``content.length();``
        - ``null``
        - Parses only as a statement block, which contains no ``return``
      * - ``var x = 1; x + 2``
        - ``null``
        - Parses only as a statement block, which contains no ``return``

   Under Groovy all three returned a value, because the value of the last statement evaluated
   is the script's return value. JavaScript has no such rule.

   This is the one difference in the migration that produces no error, no log line and no
   symptom other than a field quietly going empty: a data store mapping whose script returns
   ``null`` simply does not set that field. Write each data store ``field=expression`` line as
   a bare expression with no trailing semicolon, and give every scheduled job script an
   explicit ``return``.

Basic Syntax
============

A line with no trailing semicolon below is an **expression** and can be used anywhere,
including a data store ``field=expression`` line. Declarations ( ``let`` / ``const`` ),
``if`` blocks and loops are **statements**: they can only be used where the whole script is
evaluated, such as a scheduled job, and the script must contain an explicit ``return`` to
produce a value. See "How Scripts Are Evaluated" above.

Variable Declaration
--------------------

::

    // let (reassignable variable)
    let name = "Fess";
    let count = 100;

    // const (non-reassignable constant)
    const title = "Document Title";
    const pageNum = 1;

String Operations
-----------------

::

    // Template literals (ES6)
    const id = 123;
    const url = `https://example.com/doc/${id}`;

    // Multi-line strings (template literal)
    const content = `
    This is a
    multi-line string
    `;

    // Replacement (using a regular expression; ECMAScript 6 has no String#replaceAll)
    title.replace(/old/g, "new")
    title.replace(/\s+/g, " ")  // Collapse runs of whitespace into one space

    // Split and join
    const tags = "tag1,tag2,tag3".split(",");
    const joined = tags.join(", ");

    // Case conversion
    title.toUpperCase()
    title.toLowerCase()

Collection Operations
---------------------

::

    // Arrays
    const list = [1, 2, 3, 4, 5];
    const doubled = list.map(item => item * 2);
    const filtered = list.filter(item => item > 3);
    const total = list.reduce((sum, item) => sum + item, 0);

    // Objects
    const map = { name: "Fess", version: "15.9" };
    map.name
    map["version"]

Conditional Branching
---------------------

::

    // if-else
    if (data.status === "active") {
        return "Active";
    } else {
        return "Inactive";
    }

    // Ternary operator
    data.count > 0 ? "Present" : "None"

    // Default value (logical OR operator; JavaScript has no Elvis operator)
    data.title || "Untitled"

    // Optional chaining (?.) is ES2020 syntax and is not available under ES6.
    // Check for null explicitly instead.
    (data.content != null) ? data.content.length() : 0

Loop Processing
---------------

::

    // for...of (ES6)
    for (const item of items) {
        // process each item
    }

    // forEach (arrow function)
    items.forEach(item => {
        // process each item
    });

    // For a range, build an array or use a for loop
    // (JavaScript has no Groovy-style range expression)
    for (let i = 1; i <= 10; i++) {
        // ...
    }

Data Store Scripts
==================

Examples of scripts for data store configuration.

.. note::
   In data store scripts, each ``field=expression`` line is evaluated independently as a single expression.
   Therefore, ``let`` / ``const`` variable-declaration statements and multi-line control structures that set several fields at once (such as ``if`` blocks) cannot be used.
   When using Java classes, write them as a single expression with a fully qualified class name (FQCN), and use a per-field ternary operator for conditional values (for example, ``url=data.published ? data.url : null`` ).
   Also, the variable name ``data`` used here is only an example; the actual variable name depends on the data store connector you use. See :doc:`../admin/dataconfig-guide` for details.
   Write the expression without a trailing semicolon: a line that can only be parsed as a statement block evaluates to ``null`` and the field is left unset — see :ref:`javascript-statement-null`.

Basic Mapping
-------------

::

    url=data.url
    title=data.title
    content=data.content
    lastModified=data.updated_at

URL Generation
--------------

::

    // URL generation based on ID
    url="https://example.com/article/" + data.id

    // Combination of multiple fields
    url="https://example.com/" + data.category + "/" + data.slug + ".html"

    // Conditional URL
    url=data.external_url || "https://example.com/default/" + data.id

Content Processing
------------------

::

    // Remove HTML tags
    content=data.html_content.replace(/<[^>]+>/g, "")

    // Combine multiple fields
    content=data.title + "\n" + data.description + "\n" + data.body

    // Length limitation
    content=data.content.length() > 10000 ? data.content.substring(0, 10000) : data.content

Date Processing
---------------

::

    // Date parsing (single expression using FQCN; Java interop uses the same notation as Groovy)
    lastModified=new java.text.SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss").parse(data.date_string)

    // Conversion from epoch seconds (no long-literal L suffix needed)
    lastModified=new Date(data.timestamp * 1000)

Available Objects
=================

The objects available in scripts vary depending on the execution context.

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Context
     - Object
     - Description
   * - All contexts
     - ``container``
     - DI container. Used to access components via ``container.getComponent("...")``
   * - Scheduled jobs
     - ``executor``
     - Job execution control ( ``JobExecutor`` ). Required for job stop support
   * - Data store
     - (connector-specific)
     - Data record variables provided by each data store. The variable name depends on the connector
   * - Path mapping
     - ``url`` , ``matcher``
     - The URL string to convert and the regular-expression match result ( ``Matcher`` ). Available when the replacement is prefixed with a registered engine name, such as ``javascript:`` (aliases ``js:``, ``sai:``)
   * - Document boost
     - (document fields)
     - Each field of the target document is available as a variable (used in condition and boost-value expressions)

Scheduled Job Scripts
=====================

Examples of JavaScript scripts used in scheduled jobs.
In scheduled jobs, ``container`` and ``executor`` are available.
Passing ``executor`` to the job's ``execute()`` method enables job stop control.

.. note::
   A scheduled job script is evaluated as a single, complete script.
   The scripting engine first tries to compile it as an expression and reinterprets it as a
   block of statements only if that fails, so multi-line statements, ``let`` / ``const``
   declarations, control-flow constructs, and a top-level ``return`` statement can all be used
   (see "How Scripts Are Evaluated" above for details).
   The "Using Java Classes", "Accessing Fess Components", "Error Handling", and "Debugging and
   Log Output" examples below also assume this complete-script context.

Execute Crawl Job
-----------------

::

    return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);

Conditional Crawling
--------------------

::

    const cal = java.util.Calendar.getInstance();
    const hour = cal.get(java.util.Calendar.HOUR_OF_DAY);

    // Crawl only outside business hours
    if (hour < 9 || hour >= 18) {
        return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);
    }
    return "Skipped during business hours";

Execute Multiple Jobs Sequentially
----------------------------------

::

    const results = [];

    // Update suggest
    results.push(container.getComponent("suggestJob").logLevel("info").sessionId("SUGGEST").execute(executor));

    // Execute crawl
    results.push(container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor));

    return results.join("\n");

Using Java Classes
==================

Within JavaScript scripts, Sai's (Nashorn's) Java interoperability lets you use Java
standard libraries and |Fess| classes directly. JavaScript has no ``import`` statement,
so classes are always written by their fully qualified name (FQCN).

::

    new java.io.File("/var/log/fess/fess.log")
    java.lang.System.getProperty("user.home")
    new org.codelibs.fess.job.IndexExportJob()

Date and Time
-------------

::

    const now = java.time.LocalDateTime.now();
    const formatted = now.format(java.time.format.DateTimeFormatter.ISO_LOCAL_DATE_TIME);

File Operations
---------------

::

    const content = new java.lang.String(
        java.nio.file.Files.readAllBytes(java.nio.file.Paths.get("/path/to/file.txt")));

HTTP Communication
------------------

::

    const client = java.net.http.HttpClient.newHttpClient();
    const request = java.net.http.HttpRequest.newBuilder()
        .uri(java.net.URI.create("https://api.example.com/data"))
        .build();
    const response = client.send(request, java.net.http.HttpResponse.BodyHandlers.ofString());
    const body = response.body();

.. warning::
   Access to external resources affects performance,
   so keep it to a minimum.

Accessing Fess Components
=========================

You can access Fess components using ``container``.

System Helper
-------------

::

    const systemHelper = container.getComponent("systemHelper");
    const currentTime = systemHelper.getCurrentTimeAsLong();

Getting Configuration Values
----------------------------

::

    const fessConfig = container.getComponent("fessConfig");
    const indexName = fessConfig.getIndexDocumentUpdateIndex();

Executing Searches
------------------

::

    const searchHelper = container.getComponent("searchHelper");
    // Set search parameters and execute search

Error Handling
==============

JavaScript has no ``import`` statement, so there is no Groovy-style placement
restriction to worry about. You can catch exceptions with ``try-catch`` to control
job errors.

::

    const logger = org.apache.logging.log4j.LogManager.getLogger("script");

    try {
        return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);
    } catch (e) {
        logger.error("Failed to execute crawl job: {}", e.getMessage(), e);
        return "Error: " + e.getMessage();
    }

Debugging and Log Output
========================

Log Output
----------

::

    const logger = org.apache.logging.log4j.LogManager.getLogger("script");

    logger.debug("Debug message: {}", value);
    logger.info("Processing: {}", title);
    logger.warn("Warning: {}", message);
    logger.error("Error: {}", e.getMessage(), e);

Debug Output
------------

If you want to quickly inspect the contents of a variable, stringify it with
``JSON.stringify`` and log it.

::

    logger.debug("data = {}", JSON.stringify({ id: data.id, title: data.title }));

Porting from Groovy
====================

Keep the following differences in mind when porting an existing Groovy script to
JavaScript.

Arithmetic Precision
---------------------

JavaScript number arithmetic is always double-precision floating point. For example,
the following expression returns the integer ``34`` in Groovy, but a floating-point
``34.0`` in JavaScript.

::

    10 * boost1 + boost2

On the other hand, the return type of a method called through Java interop keeps its
Java-side type, so ``content.length()`` still returns an integer.

Rewriting Groovy-Only Syntax
------------------------------

The following Groovy-only syntax must be rewritten for JavaScript.

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Groovy
     - JavaScript
     - Description
   * - ``1000L``
     - ``1000``
     - The ``L`` long-literal suffix is not needed; write the number literal as-is
   * - ``["a", "b"] as String[]``
     - ``["a", "b"]``
     - A JavaScript array is automatically converted to a Java array when passed to a
       method that takes ``String[]``, so no cast is needed

Java Interoperability
----------------------

Java interoperability uses the same notation as Nashorn, and is nearly identical to
Groovy's. Fully qualified constructor calls such as ``new java.io.File(...)``,
``java.lang.System.getProperty(...)``, and
``new org.codelibs.fess.job.IndexExportJob()`` all resolve as-is.

ES6 Syntax
----------

Because |Fess|'s JavaScript engine runs as ECMAScript 6, you can use ES6 syntax such as
``let`` / ``const``, arrow functions, template literals, destructuring, ``for...of``,
and ``class``. However, optional chaining (``?.``) and the nullish coalescing operator
(``??``) are ES2020-and-later syntax and cannot be used.

Best Practices
==============

1. **Keep it simple**: Avoid complex logic and write readable code
2. **Default values**: Use the logical OR operator (``||``) in place of the Elvis operator
3. **Exception handling**: Handle unexpected errors with appropriate try-catch
4. **Log output**: Output logs for easier debugging
5. **Performance**: Minimize external resource access
6. **Numeric arithmetic**: Where an integer is expected, either use the result of a Java
   interop method call directly, or convert explicitly where needed

Reference Information
=====================

- `MDN JavaScript Reference <https://developer.mozilla.org/en-US/docs/Web/JavaScript>`__
- :doc:`scripting-overview` - Scripting Overview
- :doc:`scripting-groovy` - Groovy Scripting Guide (plugin)
- :doc:`../admin/dataconfig-guide` - Data Store Configuration Guide
- :doc:`../admin/scheduler-guide` - Scheduler Configuration Guide
