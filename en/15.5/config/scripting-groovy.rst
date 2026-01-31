==================================
Groovy Scripting Guide
==================================

Overview
========

Groovy is the default scripting language for |Fess|.
It runs on the Java Virtual Machine (JVM) and, while maintaining high compatibility with Java,
allows you to write scripts with a more concise syntax.

Basic Syntax
============

Variable Declaration
--------------------

::

    // Type inference (def)
    def name = "Fess"
    def count = 100

    // Explicit type specification
    String title = "Document Title"
    int pageNum = 1

String Operations
-----------------

::

    // String interpolation (GString)
    def id = 123
    def url = "https://example.com/doc/${id}"

    // Multi-line strings
    def content = """
    This is a
    multi-line string
    """

    // Replacement
    title.replace("old", "new")
    title.replaceAll(/\s+/, " ")  // Regular expression

    // Split and join
    def tags = "tag1,tag2,tag3".split(",")
    def joined = tags.join(", ")

    // Case conversion
    title.toUpperCase()
    title.toLowerCase()

Collection Operations
---------------------

::

    // Lists
    def list = [1, 2, 3, 4, 5]
    list.each { println it }
    def doubled = list.collect { it * 2 }
    def filtered = list.findAll { it > 3 }

    // Maps
    def map = [name: "Fess", version: "15.5"]
    println map.name
    println map["version"]

Conditional Branching
---------------------

::

    // if-else
    if (data.status == "active") {
        return "Active"
    } else {
        return "Inactive"
    }

    // Ternary operator
    def result = data.count > 0 ? "Present" : "None"

    // Elvis operator (null coalescing operator)
    def value = data.title ?: "Untitled"

    // Safe navigation operator
    def length = data.content?.length() ?: 0

Loop Processing
---------------

::

    // for-each
    for (item in items) {
        println item
    }

    // Closure
    items.each { item ->
        println item
    }

    // Range
    (1..10).each { println it }

Data Store Scripts
==================

Examples of scripts for data store configuration.

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
    url=data.external_url ?: "https://example.com/default/" + data.id

Content Processing
------------------

::

    // Remove HTML tags
    content=data.html_content.replaceAll(/<[^>]+>/, "")

    // Combine multiple fields
    content=data.title + "\n" + data.description + "\n" + data.body

    // Length limitation
    content=data.content.length() > 10000 ? data.content.substring(0, 10000) : data.content

Date Processing
---------------

::

    // Date parsing
    import java.text.SimpleDateFormat
    def sdf = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss")
    lastModified=sdf.parse(data.date_string)

    // Conversion from epoch seconds
    lastModified=new Date(data.timestamp * 1000L)

Scheduled Job Scripts
=====================

Examples of Groovy scripts used in scheduled jobs.

Execute Crawl Job
-----------------

::

    return container.getComponent("crawlJob").execute();

Conditional Crawling
--------------------

::

    import java.util.Calendar

    def cal = Calendar.getInstance()
    def hour = cal.get(Calendar.HOUR_OF_DAY)

    // Crawl only outside business hours
    if (hour < 9 || hour >= 18) {
        return container.getComponent("crawlJob").execute()
    }
    return "Skipped during business hours"

Execute Multiple Jobs Sequentially
----------------------------------

::

    def results = []

    // Index optimization
    results << container.getComponent("optimizeJob").execute()

    // Execute crawl
    results << container.getComponent("crawlJob").execute()

    return results.join("\n")

Using Java Classes
==================

Within Groovy scripts, you can use Java standard libraries and Fess classes.

Date and Time
-------------

::

    import java.time.LocalDateTime
    import java.time.format.DateTimeFormatter

    def now = LocalDateTime.now()
    def formatted = now.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME)

File Operations
---------------

::

    import java.nio.file.Files
    import java.nio.file.Paths

    def content = new String(Files.readAllBytes(Paths.get("/path/to/file.txt")))

HTTP Communication
------------------

::

    import java.net.URL

    def url = new URL("https://api.example.com/data")
    def response = url.text

.. warning::
   Access to external resources affects performance,
   so keep it to a minimum.

Accessing Fess Components
=========================

You can access Fess components using ``container``.

System Helper
-------------

::

    def systemHelper = container.getComponent("systemHelper")
    def currentTime = systemHelper.getCurrentTimeAsLong()

Getting Configuration Values
----------------------------

::

    def fessConfig = container.getComponent("fessConfig")
    def indexName = fessConfig.getIndexDocumentUpdateIndex()

Executing Searches
------------------

::

    def searchHelper = container.getComponent("searchHelper")
    // Set search parameters and execute search

Error Handling
==============

::

    try {
        def result = processData(data)
        return result
    } catch (Exception e) {
        import org.apache.logging.log4j.LogManager
        def logger = LogManager.getLogger("script")
        logger.error("Error processing data: {}", e.message, e)
        return "Error: " + e.message
    }

Debugging and Log Output
========================

Log Output
----------

::

    import org.apache.logging.log4j.LogManager
    def logger = LogManager.getLogger("script")

    logger.debug("Debug message: {}", data.id)
    logger.info("Processing document: {}", data.title)
    logger.warn("Warning: {}", message)
    logger.error("Error: {}", e.message)

Debug Output
------------

::

    // Console output (development only)
    println "data.id = ${data.id}"
    println "data.title = ${data.title}"

Best Practices
==============

1. **Keep it simple**: Avoid complex logic and write readable code
2. **Null checks**: Utilize ``?.`` and ``?:`` operators
3. **Exception handling**: Handle unexpected errors with appropriate try-catch
4. **Log output**: Output logs for easier debugging
5. **Performance**: Minimize external resource access

Reference Information
=====================

- `Groovy Official Documentation <https://groovy-lang.org/documentation.html>`__
- :doc:`scripting-overview` - Scripting Overview
- :doc:`../admin/dataconfig-guide` - Data Store Configuration Guide
- :doc:`../admin/scheduler-guide` - Scheduler Configuration Guide
