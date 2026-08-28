===========================
Advanced Crawler Configuration
===========================

Overview
========

This guide explains advanced configuration for the |Fess| crawler.
For basic crawler configuration, refer to :doc:`crawler-basic`.

.. warning::
   The settings on this page can affect the entire system.
   Thoroughly test any changes before applying them to production environments.

General Settings
================

Configuration File Locations
-----------------------------

Detailed crawler settings are configured in the following files:

- **Main configuration**: ``/etc/fess/fess_config.properties`` (or ``app/WEB-INF/classes/fess_config.properties``)
- **Content length configuration**: ``app/WEB-INF/classes/crawler/contentlength.xml``
- **Component configuration**: ``app/WEB-INF/classes/crawler/container.xml``

Default Script
--------------

This property was removed in |Fess| 15.9; each document boost rule now selects its own script type on the :doc:`../admin/boostdoc-guide` screen.

HTTP Thread Pool
----------------

HTTP crawler thread pool settings.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``crawler.http.thread_pool.size``
     - HTTP thread pool size
     - ``0``

::

    # 0 means auto-configuration
    crawler.http.thread_pool.size=0

Document Processing Settings
=============================

Basic Settings
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``crawler.document.max.site.length``
     - Maximum character length for site name field
     - ``100``
   * - ``crawler.document.site.encoding``
     - Document site encoding
     - ``UTF-8``
   * - ``crawler.document.unknown.hostname``
     - Alternative value for unknown hostname
     - ``unknown``
   * - ``crawler.document.use.site.encoding.on.english``
     - Use site encoding for English documents
     - ``false``
   * - ``crawler.document.append.data``
     - Append data to document
     - ``true``
   * - ``crawler.document.append.filename``
     - Append filename to document
     - ``false``

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    crawler.document.max.site.length=100
    crawler.document.site.encoding=UTF-8
    crawler.document.unknown.hostname=unknown
    crawler.document.use.site.encoding.on.english=false
    crawler.document.append.data=true
    crawler.document.append.filename=false

Word Processing Settings
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``crawler.document.max.alphanum.term.size``
     - Maximum alphanumeric word length
     - ``20``
   * - ``crawler.document.max.symbol.term.size``
     - Maximum symbol word length
     - ``10``
   * - ``crawler.document.duplicate.term.removed``
     - Remove duplicate words
     - ``false``

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    # Change maximum alphanumeric length to 50 characters
    crawler.document.max.alphanum.term.size=50

    # Change maximum symbol length to 20 characters
    crawler.document.max.symbol.term.size=20

    # Remove duplicate words
    crawler.document.duplicate.term.removed=true

.. note::
   Increasing ``max.alphanum.term.size`` allows indexing long IDs, tokens, URLs, etc.
   in their complete form, but increases index size.

Character Processing Settings
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``crawler.document.space.chars``
     - Whitespace character definition
     - ``u0009u000A...``
   * - ``crawler.document.fullstop.chars``
     - Period character definition
     - ``u002eu06d4...``

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    # Default values (includes Unicode characters)
    crawler.document.space.chars=u0009u000Au000Bu000Cu000Du001Cu001Du001Eu001Fu0020u00A0u1680u180Eu2000u2001u2002u2003u2004u2005u2006u2007u2008u2009u200Au200Bu200Cu202Fu205Fu3000uFEFFuFFFDu00B6

    crawler.document.fullstop.chars=u002eu06d4u2e3cu3002

Protocol Settings
=================

Supported Protocols
-------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``crawler.web.protocols``
     - Web crawl protocols
     - ``http,https``
   * - ``crawler.file.protocols``
     - File crawl protocols
     - ``file,smb,smb1,ftp,storage,s3,gcs``
   * - ``crawler.crawling.data.encoding``
     - Crawling data encoding
     - ``UTF-8``

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    crawler.web.protocols=http,https
    crawler.file.protocols=file,smb,smb1,ftp,storage,s3,gcs
    crawler.crawling.data.encoding=UTF-8

Environment Variable Parameters
--------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``crawler.data.env.param.key.pattern``
     - Environment variable parameter key pattern
     - ``^FESS_ENV_.*``

::

    # Environment variables starting with FESS_ENV_ can be used in crawl configuration
    crawler.data.env.param.key.pattern=^FESS_ENV_.*

Data Serializer
---------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``crawler.data.serializer``
     - Serialization method for crawl data
     - ``kryo``

::

    crawler.data.serializer=kryo

robots.txt Settings
===================

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``crawler.ignore.robots.txt``
     - Ignore robots.txt
     - ``false``
   * - ``crawler.ignore.robots.tags``
     - Ignore robots meta tags
     - ``false``
   * - ``crawler.ignore.content.exception``
     - Ignore content exceptions
     - ``true``

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    # Ignore robots.txt (not recommended)
    crawler.ignore.robots.txt=false

    # Ignore robots meta tags (including X-Robots-Tag)
    crawler.ignore.robots.tags=false

    # Ignore content exceptions
    crawler.ignore.content.exception=true

.. warning::
   Setting ``crawler.ignore.robots.txt=true`` may violate site terms of service.
   Exercise caution when crawling external sites.

Error Handling Settings
=======================

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``crawler.failure.url.status.codes``
     - HTTP status codes considered failures (comma-separated)
     - ``404,403,410``

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    # In addition to the defaults (404,403,410), also treat 500 as an error
    crawler.failure.url.status.codes=404,403,410,500

System Monitoring Settings
===========================

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``crawler.system.monitor.interval``
     - System monitoring interval (seconds)
     - ``60``

::

    # Monitor system every 30 seconds
    crawler.system.monitor.interval=30

Hot Thread Settings
-------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``crawler.hotthread.ignore_idle_threads``
     - Ignore idle threads
     - ``true``
   * - ``crawler.hotthread.interval``
     - Snapshot interval
     - ``500ms``
   * - ``crawler.hotthread.snapshots``
     - Number of snapshots
     - ``10``
   * - ``crawler.hotthread.threads``
     - Number of threads to monitor
     - ``3``
   * - ``crawler.hotthread.timeout``
     - Timeout
     - ``30s``
   * - ``crawler.hotthread.type``
     - Monitoring type
     - ``cpu``

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    crawler.hotthread.ignore_idle_threads=true
    crawler.hotthread.interval=500ms
    crawler.hotthread.snapshots=10
    crawler.hotthread.threads=3
    crawler.hotthread.timeout=30s
    crawler.hotthread.type=cpu

Metadata Settings
=================

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``crawler.metadata.content.excludes``
     - Metadata to exclude
     - ``resourceName,X-Parsed-By...``
   * - ``crawler.metadata.name.mapping``
     - Metadata name mapping
     - ``title=title:string...``

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    # Metadata to exclude
    crawler.metadata.content.excludes=resourceName,X-Parsed-By,Content-Encoding.*,Content-Type.*,X-TIKA.*,X-FESS.*

    # Metadata name mapping
    crawler.metadata.name.mapping=\
        title=title:string\n\
        Title=title:string\n\
        dc:title=title:string

HTML Crawler Settings
=====================

XPath Settings
--------------

XPath settings for extracting HTML elements.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``crawler.document.html.content.xpath``
     - Content XPath
     - ``//BODY``
   * - ``crawler.document.html.lang.xpath``
     - Language XPath
     - ``//HTML/@lang``
   * - ``crawler.document.html.digest.xpath``
     - Digest XPath
     - ``//META[@name='description']/@content``
   * - ``crawler.document.html.canonical.xpath``
     - Canonical URL XPath
     - ``//LINK[@rel='canonical'][1]/@href``

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    # Default settings
    crawler.document.html.content.xpath=//BODY
    crawler.document.html.lang.xpath=//HTML/@lang
    crawler.document.html.digest.xpath=//META[@name='description']/@content
    crawler.document.html.canonical.xpath=//LINK[@rel='canonical'][1]/@href

Custom XPath Examples
~~~~~~~~~~~~~~~~~~~~~~

::

    # Extract only specific div element as content
    crawler.document.html.content.xpath=//DIV[@id='main-content']

    # Include meta keywords in digest
    crawler.document.html.digest.xpath=//META[@name='description']/@content|//META[@name='keywords']/@content

HTML Tag Processing
-------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``crawler.document.html.pruned.tags``
     - HTML tags to remove
     - ``noscript,script,style,header,footer,aside,nav,a[rel=nofollow]``
   * - ``crawler.document.html.max.digest.length``
     - Maximum digest length
     - ``120``
   * - ``crawler.document.html.default.lang``
     - Default language
     - (empty)

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    # Add tags to remove
    crawler.document.html.pruned.tags=noscript,script,style,header,footer,aside,nav,a[rel=nofollow],form

    # Set digest length to 200 characters
    crawler.document.html.max.digest.length=200

    # Set default language to Japanese
    crawler.document.html.default.lang=ja

URL Pattern Filters
-------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``crawler.document.html.default.include.index.patterns``
     - URL patterns to include in index
     - (empty)
   * - ``crawler.document.html.default.exclude.index.patterns``
     - URL patterns to exclude from index
     - ``(?i).*(css|js|jpeg...)``
   * - ``crawler.document.html.default.include.search.patterns``
     - URL patterns to include in search results
     - (empty)
   * - ``crawler.document.html.default.exclude.search.patterns``
     - URL patterns to exclude from search results
     - (empty)

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    # Default exclusion patterns
    crawler.document.html.default.exclude.index.patterns=(?i).*(css|js|jpeg|jpg|gif|png|bmp|wmv|xml|ico|exe)

    # Index only specific paths
    crawler.document.html.default.include.index.patterns=https://example\\.com/docs/.*

File Crawler Settings
=====================

Basic Settings
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``crawler.document.file.name.encoding``
     - Filename encoding
     - (empty)
   * - ``crawler.document.file.no.title.label``
     - Label for files without title
     - ``No title.``
   * - ``crawler.document.file.ignore.empty.content``
     - Ignore empty content
     - ``false``
   * - ``crawler.document.file.max.title.length``
     - Maximum title length
     - ``100``
   * - ``crawler.document.file.max.digest.length``
     - Maximum digest length
     - ``200``

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    # Process Windows-31J filenames
    crawler.document.file.name.encoding=Windows-31J

    # Label for files without title
    crawler.document.file.no.title.label=No Title

    # Ignore empty files
    crawler.document.file.ignore.empty.content=true

    # Title and digest lengths
    crawler.document.file.max.title.length=200
    crawler.document.file.max.digest.length=500

Content Processing
------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``crawler.document.file.append.meta.content``
     - Append metadata to content
     - ``true``
   * - ``crawler.document.file.append.body.content``
     - Append body to content
     - ``true``
   * - ``crawler.document.file.default.lang``
     - Default language
     - (empty)

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    crawler.document.file.append.meta.content=true
    crawler.document.file.append.body.content=true
    crawler.document.file.default.lang=ja

File URL Pattern Filters
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``crawler.document.file.default.include.index.patterns``
     - Patterns to include in index
     - (empty)
   * - ``crawler.document.file.default.exclude.index.patterns``
     - Patterns to exclude from index
     - (empty)
   * - ``crawler.document.file.default.include.search.patterns``
     - Patterns to include in search results
     - (empty)
   * - ``crawler.document.file.default.exclude.search.patterns``
     - Patterns to exclude from search results
     - (empty)

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    # Index only specific extensions
    crawler.document.file.default.include.index.patterns=.*\\.(pdf|docx|xlsx|pptx)$

    # Exclude temp folders
    crawler.document.file.default.exclude.index.patterns=.*/temp/.*

MIME Type Detection Override
----------------------------

By default, |Fess| uses Apache Tika for content-based MIME type detection.
In some cases, content-based detection can produce incorrect results.
For example, Oracle SQL files starting with ``REM`` comments may be misdetected
as batch files (``application/x-bat``) because the ``REM`` keyword matches
the batch file magic pattern.

The ``crawler.document.mimetype.extension.overrides`` property allows you to
override MIME type detection based on file extensions, bypassing content-based detection
for specific file types.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``crawler.document.mimetype.extension.overrides``
     - Extension-to-MIME-type override mappings (one per line, format: ``.ext=mime/type``)
     - (empty)

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    # Override MIME type detection for SQL files
    crawler.document.mimetype.extension.overrides=\
    .sql=text/x-sql\n\
    .plsql=text/x-plsql\n\
    .pls=text/x-plsql

Each line contains a mapping in the format ``.ext=mime/type``.
Multiple mappings are separated by ``\n`` (newline).
The extension matching is case-insensitive (``.SQL`` and ``.sql`` are treated the same).

.. note::
   When a file extension matches an entry in this map, the configured MIME type
   is returned immediately without performing content-based detection.
   Files with extensions not in the map continue to use normal Tika detection.

Cache Settings
==============

Document Cache
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``crawler.document.cache.enabled``
     - Enable document cache
     - ``true``
   * - ``crawler.document.cache.max.size``
     - Maximum cache size (bytes)
     - ``2621440`` (2.5MB)
   * - ``crawler.document.cache.supported.mimetypes``
     - MIME types to cache
     - ``text/html``
   * - ``crawler.document.cache.html.mimetypes``
     - MIME types to treat as HTML
     - ``text/html``

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    # Enable document cache
    crawler.document.cache.enabled=true

    # Set cache size to 5MB
    crawler.document.cache.max.size=5242880

    # MIME types to cache
    crawler.document.cache.supported.mimetypes=text/html,application/xhtml+xml

    # MIME types to treat as HTML
    crawler.document.cache.html.mimetypes=text/html,application/xhtml+xml

.. note::
   Enabling cache displays cache links in search results,
   allowing users to reference content as it was at crawl time.

JVM Options
===========

You can configure JVM options for the crawler process.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``jvm.crawler.options``
     - Crawler JVM options
     - ``-Xms128m -Xmx512m...``

Default Settings
----------------

::

    jvm.crawler.options=-Xms128m -Xmx512m \
        -XX:MaxMetaspaceSize=128m \
        -XX:+UseG1GC \
        -XX:MaxGCPauseMillis=60000 \
        -XX:-HeapDumpOnOutOfMemoryError

.. note::
   The above shows only the main options. The actual defaults include approximately 40 options covering jcifs SMB timeouts, Netty settings, Log4j configuration, detailed G1GC settings, PDFBox settings, etc.
   See ``fess_config.properties`` for the complete default values.
   When customizing, change only the required options and keep the other defaults.

Key Options Explained
----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Option
     - Description
   * - ``-Xms128m``
     - Initial heap size (128MB)
   * - ``-Xmx512m``
     - Maximum heap size (512MB)
   * - ``-XX:MaxMetaspaceSize=128m``
     - Maximum Metaspace size (128MB)
   * - ``-XX:+UseG1GC``
     - Use G1 garbage collector
   * - ``-XX:MaxGCPauseMillis=60000``
     - GC pause time goal (60 seconds)
   * - ``-XX:-HeapDumpOnOutOfMemoryError``
     - Disable heap dump on OutOfMemory

Custom Configuration Examples
------------------------------

**For crawling large files:**

::

    jvm.crawler.options=-Xms256m -Xmx2g \
        -XX:MaxMetaspaceSize=256m \
        -XX:+UseG1GC \
        -XX:MaxGCPauseMillis=60000

**For debugging:**

::

    jvm.crawler.options=-Xms128m -Xmx512m \
        -XX:MaxMetaspaceSize=128m \
        -XX:+UseG1GC \
        -XX:+HeapDumpOnOutOfMemoryError \
        -XX:HeapDumpPath=/tmp/crawler_dump.hprof

For details, see :doc:`setup-memory`.

Performance Tuning
==================

Optimizing Crawl Speed
----------------------

**1. Adjust Thread Count**

Increase parallel crawl count to improve crawl speed.

::

    # Adjust thread count in crawl configuration on administration screen
    Thread Count: 10

However, be mindful of load on target servers.

**2. Adjust Timeouts**

For slow-responding sites, adjust timeouts.

::

    # Add to "Configuration Parameters" in crawl configuration
    client.connectionTimeout=10000
    client.soTimeout=30000

**3. Exclude Unnecessary Content**

Excluding images, CSS, JavaScript files, etc. improves crawl speed.

::

    # Exclude URL patterns
    .*\.(jpg|jpeg|png|gif|css|js|ico)$

**4. Retry Settings**

The HTTP crawl retry count (default 5) and retry interval (default 500 ms) are built-in fixed values and cannot be changed via the "Config Parameters" field of a crawl configuration. To reduce time spent waiting on unresponsive URLs, adjust the timeouts described above or exclude unnecessary URLs.

Optimizing Memory Usage
------------------------

**1. Adjust Heap Size**

::

    jvm.crawler.options=-Xms256m -Xmx1g

**2. Adjust Cache Size**

::

    crawler.document.cache.max.size=1048576  # 1MB

**3. Exclude Large Files**

::

    # Add to "Configuration Parameters" in crawl configuration
    client.maxContentLength=10485760  # 10MB

For details, see :doc:`setup-memory`.

Improving Index Quality
------------------------

**1. Optimize XPath**

Exclude unnecessary elements (navigation, ads, etc.).

::

    crawler.document.html.content.xpath=//DIV[@id='main-content']
    crawler.document.html.pruned.tags=noscript,script,style,header,footer,aside,nav,form,iframe

**2. Optimize Digest**

::

    crawler.document.html.max.digest.length=200

**3. Metadata Mapping**

::

    crawler.metadata.name.mapping=\
        title=title:string\n\
        description=digest:string\n\
        keywords=label:string

Troubleshooting
===============

Memory Shortage
---------------

**Symptoms:**

- ``OutOfMemoryError`` recorded in ``fess_crawler.log``
- Crawling stops midway

**Solutions:**

1. Increase crawler heap size

   ::

       jvm.crawler.options=-Xms256m -Xmx2g

2. Reduce parallel thread count

3. Exclude large files

For details, see :doc:`setup-memory`.

Slow Crawling
-------------

**Symptoms:**

- Crawling takes too long
- Frequent timeouts

**Solutions:**

1. Increase thread count (be mindful of target server load)

2. Adjust timeouts

   ::

       client.connectionTimeout=5000
       client.soTimeout=10000

3. Exclude unnecessary URLs

Specific Content Cannot Be Extracted
-------------------------------------

**Symptoms:**

- Page text not extracted correctly
- Important information not included in search results

**Solutions:**

1. Check and adjust XPath

   ::

       crawler.document.html.content.xpath=//DIV[@class='content']

2. Check pruned tags

   ::

       crawler.document.html.pruned.tags=script,style

3. For content dynamically generated by JavaScript, consider alternative methods (API crawling, etc.)

Character Encoding Issues
--------------------------

**Symptoms:**

- Character encoding issues in search results
- Specific languages not displayed correctly

**Solutions:**

1. Check encoding settings

   ::

       crawler.document.site.encoding=UTF-8
       crawler.crawling.data.encoding=UTF-8

2. Configure filename encoding

   ::

       crawler.document.file.name.encoding=Windows-31J

3. Check logs for encoding errors

   ::

       grep -i "encoding" /var/log/fess/fess_crawler.log

Best Practices
==============

1. **Verify in Test Environment**

   Thoroughly test in a test environment before applying to production.

2. **Gradual Adjustments**

   Don't change settings drastically at once; adjust gradually and verify effectiveness.

3. **Monitor Logs**

   After changing settings, monitor logs to check for errors or performance issues.

   ::

       tail -f /var/log/fess/fess_crawler.log

4. **Backups**

   Always back up configuration files before making changes.

   ::

       cp /etc/fess/fess_config.properties /etc/fess/fess_config.properties.bak

5. **Documentation**

   Document the settings you changed and the reasons why.

S3/GCS Crawler Configuration
============================

S3 Crawler
----------

Configuration for crawling S3 and S3-compatible storage (such as MinIO).
Add the following to "Configuration Parameters" in the file crawl settings.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Parameter
     - Description
     - Default
   * - ``client.endpoint``
     - S3 endpoint URL
     - (Required)
   * - ``client.accessKey``
     - Access key
     - (Required)
   * - ``client.secretKey``
     - Secret key
     - (Required)
   * - ``client.region``
     - AWS region
     - ``us-east-1``
   * - ``client.maxContentLength``
     - Maximum size (bytes) of objects to fetch. Objects exceeding this are skipped
     - (unlimited)
   * - ``client.maxCachedContentSize``
     - Maximum size (bytes) cached in memory; larger content uses a temporary file
     - ``1048576`` (1MB)
   * - ``client.accessTimeout``
     - Access timeout (seconds). Disabled when not set
     - (unlimited)

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    client.endpoint=https://s3.ap-northeast-1.amazonaws.com
    client.accessKey=AKIAIOSFODNN7EXAMPLE
    client.secretKey=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    client.region=ap-northeast-1

GCS Crawler
-----------

Configuration for crawling Google Cloud Storage.
Add the following to "Configuration Parameters" in the file crawl settings.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Parameter
     - Description
     - Default
   * - ``client.projectId``
     - Google Cloud project ID
     - (Required)
   * - ``client.credentialsFile``
     - Service account JSON file path
     - (Optional)
   * - ``client.endpoint``
     - Custom endpoint
     - (Optional)
   * - ``client.maxContentLength``
     - Maximum size (bytes) of objects to fetch. Objects exceeding this are skipped
     - (unlimited)
   * - ``client.maxCachedContentSize``
     - Maximum size (bytes) cached in memory; larger content uses a temporary file
     - ``1048576`` (1MB)
   * - ``client.accessTimeout``
     - Access timeout (seconds). Disabled when not set
     - (unlimited)

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    client.projectId=my-gcp-project
    client.credentialsFile=/etc/fess/gcs-credentials.json

.. note::
   If ``credentialsFile`` is omitted, the ``GOOGLE_APPLICATION_CREDENTIALS`` environment variable is used.

Crawling Dynamic Content (Playwright)
=====================================

Pages rendered by JavaScript (such as SPAs) return only the pre-rendered HTML to
the ordinary HTTP crawler, so their body text is never indexed. The Playwright
crawler renders the page in a headless browser first and then retrieves the
content.

Enabling
--------

Add the following to the "Configuration Parameters" of a web crawling
configuration.

::

    client.crawlerClients=playwright:http://.*,playwright:https://.*

The part after ``playwright:`` is a regular expression for the URLs to retrieve
with Playwright. In the example above, every HTTP/HTTPS URL is retrieved with
Playwright. To use Playwright for specific sites only, specify them as follows.

::

    client.crawlerClients=playwright:https://example\.com/app/.*

.. note::
   The Playwright browser binaries are not included in the |Fess| package.
   They are downloaded on the first crawl, so in an environment without
   external network access, install them in advance as the OS user that runs
   the crawler.

   ::

       npx playwright install --with-deps

Configuration Parameters
------------------------

The following parameters are written in the "Configuration Parameters" of a
crawling configuration with the ``client.`` prefix.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Parameter
     - Description
     - Default
   * - ``client.renderedState``
     - The load state to wait for before retrieving the content. Specify ``LOAD``, ``DOMCONTENTLOADED`` or ``NETWORKIDLE`` in uppercase
     - ``NETWORKIDLE``
   * - ``client.renderedStateTimeout``
     - The limit for waiting for ``renderedState`` (milliseconds). Zero or less uses the Playwright default (30000)
     - ``0``
   * - ``client.navigationTimeout``
     - The limit for a navigation (milliseconds). Zero or less uses the Playwright default (30000)
     - (not set)
   * - ``client.contentWaitDuration``
     - Additional wait after reaching ``renderedState`` and before retrieving the content (milliseconds)
     - ``0``
   * - ``client.sharedClient``
     - Share the Playwright worker (browser) across all clients
     - ``false``
   * - ``client.blockedResourceTypes``
     - Resource types the browser must not fetch (comma-separated)
     - (empty)
   * - ``client.ignoreHttpsErrors``
     - Ignore HTTPS certificate validation errors
     - ``false``
   * - ``client.proxyBypass``
     - Hosts that bypass the proxy (comma-separated)
     - (empty)

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    client.crawlerClients=playwright:http://.*,playwright:https://.*
    client.renderedState=NETWORKIDLE
    client.renderedStateTimeout=20000
    client.navigationTimeout=60000
    client.contentWaitDuration=1000
    client.blockedResourceTypes=image,media,font,ping,beacon,cspreport

.. note::
   The user agent and the request headers configured in the crawling
   configuration are used as they are. Common parameters such as
   ``client.proxyHost``, ``client.proxyPort`` and ``client.maxContentLength``
   are applied to the browser as well.

.. note::
   One Playwright client uses one browser page, and requests to it are
   processed serially. Increasing the number of threads in the crawling
   configuration does not make retrieval with Playwright proportionally faster.

Items Configurable Only in the DI Definition
--------------------------------------------

The following items cannot be changed from the "Configuration Parameters". To
change them, create
``app/WEB-INF/classes/crawler/client+playwrightClient.xml`` and redefine the
``playwrightClient`` component.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``browserName``
     - The browser to use: ``chromium``, ``firefox`` or ``webkit``
     - ``chromium``
   * - ``launchOptions``
     - Browser launch options (``BrowserType.LaunchOptions``)
     - ``headless=true``
   * - ``newContextOptions``
     - Browser context options (``Browser.NewContextOptions``)
     - (none)
   * - ``downloadTimeout``
     - The limit for waiting for a file download (seconds)
     - ``15``
   * - ``closeTimeout``
     - The limit for waiting for the browser teardown (seconds)
     - ``15``

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components namespace="fessCrawler">
        <include path="crawler/container.xml" />
        <component name="playwrightClient"
            class="org.codelibs.fess.crawler.client.http.PlaywrightClient"
            instance="prototype">
            <property name="downloadTimeout">60</property>
            <property name="closeTimeout">30</property>
            <property name="launchOptions">
                <component
                    class="com.microsoft.playwright.BrowserType$LaunchOptions"
                    instance="prototype">
                    <property name="headless">true</property>
                </component>
            </property>
        </component>
    </components>

.. note::
   Redefining ``playwrightClient`` replaces the component definition from the
   plugin's ``crawler/client++.xml`` entirely. Properties you do not write
   revert to their defaults, so write every property you need, as in the
   example above. Do not simply copy ``crawler/client++.xml`` into place
   either: the same component would be registered twice and startup would
   fail.

.. warning::
   ``downloadTimeout`` and ``closeTimeout`` are in seconds, whereas
   ``navigationTimeout``, ``renderedStateTimeout`` and ``contentWaitDuration``
   are in milliseconds. Take care not to confuse them.

Blocking Unnecessary Resources
------------------------------

``client.blockedResourceTypes`` takes a comma-separated list of the resource
types the browser must not fetch. The values are Playwright resource types
(``stylesheet``, ``image``, ``media``, ``font``, ``script``, ``texttrack``,
``xhr``, ``fetch``, ``eventsource``, ``websocket``, ``manifest``, ``other``,
``ping``, ``cspreport`` and ``beacon``). By default nothing is blocked.

``image``, ``media``, ``font``, ``ping``, ``beacon`` and ``cspreport`` are the
safe set. The last three are beacon-style tracker traffic that nothing on the
page reads back.

::

    client.blockedResourceTypes=image,media,font,ping,beacon,cspreport

Specify only the types a crawl does not read. Fetching fewer of the resources
that a page needs for display reduces both the time a crawl takes and the
amount of data transferred.

.. warning::
   Do not specify ``document``. Retrieving the page itself would be blocked and
   the crawl could not proceed, so it is ignored with a warning.

.. note::
   A type that is not in the list above is also warned about. A plural typo such
   as ``images`` matches no request, so it blocks nothing. The list is the union
   of what the three browser engines report, so some types are never reported by
   the browser in use: ``texttrack`` is reported by Chromium only, and WebKit
   reports neither ``media`` nor ``manifest``. Specifying a type that is not
   reported simply blocks nothing.

.. note::
   Blocking ``script`` or ``xhr`` stops JavaScript from rendering the page,
   which defeats the purpose of using Playwright. It is useful for a crawl that
   targets server-side rendered pages only, but normally choose from the safe
   set listed above.

Changes in 15.9
---------------

When upgrading from 15.7 or earlier, the behavior of the Playwright crawler has
changed as follows.

- **User agent**: The user agent of the crawling configuration is now actually
  sent by the browser. In 15.7 and earlier, the browser default
  ``HeadlessChrome/...`` was sent. On sites that vary their response by user
  agent, the retrieved content may change.

- **Request headers**: The request headers of the crawling configuration are
  now applied to the browser. When the same header name appears more than once,
  the values are joined into a single comma-separated value.

- **Downloads via a redirect**: The recorded URL is now the redirect target
  (the URL that actually returned the file). If the redirect target is a URL
  outside the crawling scope, it is excluded as out of scope.

- **Waiting for ``renderedState``**: A timeout while waiting is no longer
  treated as a failure; the content that had been loaded at that point is used
  as it is. Pages that never reach ``NETWORKIDLE`` can also be indexed.

- **Specifying timeouts**: ``client.navigationTimeout`` and
  ``client.renderedStateTimeout``, which limit the time to load the whole page,
  have been added. ``client.connectionTimeout`` and ``client.soTimeout`` are
  per-socket timeouts and are not applied to the browser.

References
==========

- :doc:`crawler-basic` - Basic Crawler Configuration
- :doc:`crawler-thumbnail` - Thumbnail Configuration
- :doc:`setup-memory` - Memory Configuration
- :doc:`admin-logging` - Log Configuration
- :doc:`search-advanced` - Advanced Search Settings
