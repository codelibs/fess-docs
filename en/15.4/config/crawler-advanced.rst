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

Configure the default script language for the crawler.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``crawler.default.script``
     - Crawler script language
     - ``groovy``

::

    crawler.default.script=groovy

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
     - Maximum lines for document site
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
     - ``\u0009\u000A...``
   * - ``crawler.document.fullstop.chars``
     - Period character definition
     - ``\u002e\u06d4...``

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    # Default values (includes Unicode characters)
    crawler.document.space.chars=\u0009\u000A\u000B\u000C\u000D\u001C\u001D\u001E\u001F\u0020\u00A0\u1680\u180E\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u200B\u200C\u202F\u205F\u3000\uFEFF\uFFFD\u00B6

    crawler.document.fullstop.chars=\u002e\u06d4\u2e3c\u3002

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
     - ``file,smb,smb1,ftp,storage``

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    crawler.web.protocols=http,https
    crawler.file.protocols=file,smb,smb1,ftp,storage

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
     - Robots tags to ignore
     - (empty)
   * - ``crawler.ignore.content.exception``
     - Ignore content exceptions
     - ``true``

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    # Ignore robots.txt (not recommended)
    crawler.ignore.robots.txt=false

    # Ignore specific robots tags
    crawler.ignore.robots.tags=

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
     - HTTP status codes considered failures
     - ``404``

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

::

    # Treat 403 as error in addition to 404
    crawler.failure.url.status.codes=404,403

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
    client.socketTimeout=30000

**3. Exclude Unnecessary Content**

Excluding images, CSS, JavaScript files, etc. improves crawl speed.

::

    # Exclude URL patterns
    .*\.(jpg|jpeg|png|gif|css|js|ico)$

**4. Retry Settings**

Adjust retry count and interval on errors.

::

    # Add to "Configuration Parameters" in crawl configuration
    client.maxRetry=3
    client.retryInterval=1000

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
       client.socketTimeout=10000

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

References
==========

- :doc:`crawler-basic` - Basic Crawler Configuration
- :doc:`crawler-thumbnail` - Thumbnail Configuration
- :doc:`setup-memory` - Memory Configuration
- :doc:`admin-logging` - Log Configuration
- :doc:`search-advanced` - Advanced Search Settings
