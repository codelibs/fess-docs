=========================
Basic Crawler Configuration
=========================

Overview
========

The |Fess| crawler is a feature that automatically collects content from websites, file systems, and other sources and registers it in the search index.
This guide explains the basic concepts and configuration methods for the crawler.

Basic Crawler Concepts
=======================

What is a Crawler
-----------------

A crawler is a program that automatically collects content by following links starting from specified URLs or file paths.

The |Fess| crawler has the following features:

- **Multi-protocol support**: HTTP/HTTPS, file systems, SMB, FTP, etc.
- **Scheduled execution**: Periodic automatic crawling
- **Incremental crawling**: Updates only changed content
- **Parallel processing**: Simultaneous crawling of multiple URLs
- **Robots.txt compliance**: Respects robots.txt

Crawler Types
-------------

|Fess| provides the following crawler types depending on the target:

.. list-table:: Crawler Types
   :header-rows: 1
   :widths: 20 40 40

   * - Type
     - Target
     - Use Case
   * - **Web Crawler**
     - Websites (HTTP/HTTPS)
     - Public websites, intranet websites
   * - **File Crawler**
     - File systems, SMB, FTP
     - File servers, shared folders
   * - **Data Store Crawler**
     - Databases
     - RDB, CSV, JSON, and other data sources

Creating Crawl Configurations
==============================

Adding Basic Crawl Configuration
---------------------------------

1. **Access the Administration Screen**

   Access ``http://localhost:8080/admin`` in your browser and log in as administrator.

2. **Open Crawler Configuration Screen**

   Select "Crawler" → "Web" or "File System" from the left menu.

3. **Create New Configuration**

   Click the "New" button.

4. **Enter Basic Information**

   - **Name**: Identifier for the crawl configuration (e.g., Corporate Wiki)
   - **URL**: Crawl start URL (e.g., ``https://wiki.example.com/``)
   - **Crawl Interval**: Crawl execution frequency (e.g., every hour)
   - **Thread Count**: Number of parallel crawls (e.g., 5)
   - **Depth**: Link traversal depth (e.g., 3)

5. **Save**

   Click the "Create" button to save the configuration.

Web Crawler Configuration Examples
-----------------------------------

Crawling Internal Intranet Site
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    Name: Corporate Portal
    URL: http://intranet.example.com/
    Crawl Interval: Once per day
    Thread Count: 10
    Depth: Unlimited (-1)
    Maximum Access Count: 10000

Crawling Public Website
~~~~~~~~~~~~~~~~~~~~~~~~

::

    Name: Product Site
    URL: https://www.example.com/products/
    Crawl Interval: Once per week
    Thread Count: 5
    Depth: 5
    Maximum Access Count: 1000

File Crawler Configuration Examples
------------------------------------

Local File System
~~~~~~~~~~~~~~~~~~

::

    Name: Documents Folder
    URL: file:///home/share/documents/
    Crawl Interval: Once per day
    Thread Count: 3
    Depth: Unlimited (-1)

SMB/CIFS (Windows File Share)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    Name: File Server
    URL: smb://fileserver.example.com/share/
    Crawl Interval: Once per day
    Thread Count: 5
    Depth: Unlimited (-1)

Authentication Configuration
-----------------------------

To access sites or file servers that require authentication, configure authentication credentials.

1. Select "Crawler" → "Authentication" in the administration screen
2. Click "New"
3. Enter authentication information:

   ::

       Hostname: wiki.example.com
       Port: 443
       Authentication Method: Basic Authentication
       Username: crawler_user
       Password: ********

4. Click "Create"

Running Crawls
==============

Manual Execution
----------------

To run a configured crawl immediately:

1. Select the target configuration in the crawl configuration list
2. Click the "Start" button
3. Check job execution status in the "Scheduler" menu

Scheduled Execution
-------------------

To run crawls periodically:

1. Open the "Scheduler" menu
2. Select the "Default Crawler" job
3. Set the schedule expression (Cron format)

   ::

       # Run daily at 2 AM
       0 0 2 * * ?

       # Run every hour at 0 minutes
       0 0 * * * ?

       # Run at 6 PM Monday through Friday
       0 0 18 ? * MON-FRI

4. Click "Update"

Checking Crawl Status
----------------------

To check running crawl status:

1. Open the "Scheduler" menu
2. Check running jobs
3. Check details in logs:

   ::

       tail -f /var/log/fess/fess_crawler.log

Basic Configuration Items
==========================

Restricting Crawl Targets
--------------------------

Restrictions by URL Pattern
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can restrict crawling to specific URL patterns or exclude them.

**Include URL patterns (regular expressions):**

::

    # Crawl only under /docs/
    https://example\.com/docs/.*

**Exclude URL patterns (regular expressions):**

::

    # Exclude specific directories
    .*/admin/.*
    .*/private/.*

    # Exclude specific file extensions
    .*\.(jpg|png|gif|css|js)$

Depth Restriction
~~~~~~~~~~~~~~~~~~

Restrict the depth of link traversal:

- **0**: Start URL only
- **1**: Start URL and pages linked from it
- **-1**: Unlimited (follow all links)

Maximum Access Count
~~~~~~~~~~~~~~~~~~~~

Upper limit on the number of pages to crawl:

::

    Maximum Access Count: 1000

Stops after crawling 1000 pages.

Parallel Crawl Count (Thread Count)
------------------------------------

Specifies the number of URLs to crawl simultaneously.

.. list-table:: Recommended Thread Counts
   :header-rows: 1
   :widths: 40 30 30

   * - Environment
     - Recommended Value
     - Description
   * - Small site (up to 10K pages)
     - 3-5
     - Reduce load on target server
   * - Medium site (10K-100K pages)
     - 5-10
     - Well-balanced setting
   * - Large site (100K+ pages)
     - 10-20
     - High-speed crawling needed
   * - File server
     - 3-5
     - Consider file I/O load

.. warning::
   Increasing thread count too much places excessive load on the crawl target server.
   Set an appropriate value.

Crawl Interval
--------------

Specifies the frequency of crawl execution.

::

    # Time specification
    Crawl Interval: 3600000  # Milliseconds (1 hour)

    # Or set in scheduler
    0 0 2 * * ?  # Daily at 2 AM

File Size Configuration
=======================

You can set upper limits for crawled file sizes.

Maximum File Size to Retrieve
------------------------------

Add the following to "Configuration Parameters" in crawler configuration:

::

    client.maxContentLength=10485760

Retrieves files up to 10MB. Default is unlimited.

.. note::
   When crawling large files, also adjust memory settings.
   See :doc:`setup-memory` for details.

Maximum File Size to Index
---------------------------

You can set upper limits for indexing sizes by file type.

**Default values:**

- HTML files: 2.5MB
- Other files: 10MB

**Configuration file:** ``app/WEB-INF/classes/crawler/contentlength.xml``

::

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
            "http://dbflute.org/meta/lastadi10.dtd">
    <components namespace="fessCrawler">
            <include path="crawler/container.xml" />

            <component name="contentLengthHelper"
                    class="org.codelibs.fess.crawler.helper.ContentLengthHelper" instance="singleton">
                    <property name="defaultMaxLength">10485760</property><!-- 10M -->
                    <postConstruct name="addMaxLength">
                            <arg>"text/html"</arg>
                            <arg>2621440</arg><!-- 2.5M -->
                    </postConstruct>
                    <postConstruct name="addMaxLength">
                            <arg>"application/pdf"</arg>
                            <arg>5242880</arg><!-- 5M -->
                    </postConstruct>
            </component>
    </components>

This adds a configuration to process PDF files up to 5MB.

.. warning::
   When increasing file sizes to handle, also increase crawler memory settings.

Word Length Restrictions
=========================

Overview
--------

Long alphanumeric strings or consecutive symbols cause index size increases and performance degradation.
Therefore, |Fess| sets the following restrictions by default:

- **Consecutive alphanumeric characters**: Up to 20 characters
- **Consecutive symbols**: Up to 10 characters

Configuration Method
--------------------

Edit ``fess_config.properties``.

**Default settings:**

::

    crawler.document.max.alphanum.term.size=20
    crawler.document.max.symbol.term.size=10

**Example: Relaxing restrictions**

::

    crawler.document.max.alphanum.term.size=50
    crawler.document.max.symbol.term.size=20

.. note::
   If you need to search by long alphanumeric strings (e.g., serial numbers, tokens),
   increase this value. However, index size will increase.

Proxy Configuration
===================

Overview
--------

When crawling external sites from within an intranet, they may be blocked by a firewall.
In such cases, crawl via a proxy server.

Configuration Method
--------------------

Add the following to "Configuration Parameters" in the crawl configuration on the administration screen.

**Basic proxy configuration:**

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080

**Authenticated proxy:**

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080
    client.proxyUsername=proxyuser
    client.proxyPassword=proxypass

**Exclude specific hosts from proxy:**

::

    client.nonProxyHosts=localhost|127.0.0.1|*.example.com

System-Wide Proxy Configuration
--------------------------------

To use the same proxy for all crawl configurations, configure via environment variables.

::

    export http_proxy=http://proxy.example.com:8080
    export https_proxy=http://proxy.example.com:8080
    export no_proxy=localhost,127.0.0.1,.example.com

robots.txt Configuration
=========================

Overview
--------

robots.txt is a file that instructs crawlers whether crawling is allowed.
|Fess| respects robots.txt by default.

Configuration Method
--------------------

To ignore robots.txt, edit ``fess_config.properties``.

::

    crawler.ignore.robots.txt=true

.. warning::
   When crawling external sites, respect robots.txt.
   Ignoring it may place excessive load on servers or violate terms of service.

User-Agent Configuration
=========================

You can change the crawler's User-Agent.

Configuration in Administration Screen
---------------------------------------

Add to "Configuration Parameters" in crawl configuration:

::

    client.userAgent=MyCompanyCrawler/1.0

System-Wide Configuration
--------------------------

Configure in ``fess_config.properties``:

::

    crawler.user.agent=MyCompanyCrawler/1.0

Encoding Configuration
======================

Crawl Data Encoding
-------------------

Configure in ``fess_config.properties``:

::

    crawler.crawling.data.encoding=UTF-8

Filename Encoding
-----------------

Filename encoding for file systems:

::

    crawler.document.file.name.encoding=UTF-8

Crawl Troubleshooting
=====================

Crawl Does Not Start
--------------------

**Checks:**

1. Verify scheduler is enabled

   - Check if "Default Crawler" job is enabled in "Scheduler" menu

2. Verify crawl configuration is enabled

   - Check if target configuration is enabled in crawl configuration list

3. Check logs

   ::

       tail -f /var/log/fess/fess.log
       tail -f /var/log/fess/fess_crawler.log

Crawl Stops Midway
-------------------

**Possible causes:**

1. **Memory shortage**

   - Check for ``OutOfMemoryError`` in ``fess_crawler.log``
   - Increase crawler memory (see :doc:`setup-memory`)

2. **Network errors**

   - Adjust timeout settings
   - Check retry settings

3. **Crawl target errors**

   - Check if 404 errors are occurring frequently
   - Check error details in logs

Specific Page Not Crawled
--------------------------

**Checks:**

1. **Check URL patterns**

   - Verify page is not matched by exclude URL patterns

2. **Check robots.txt**

   - Check target site's ``/robots.txt``

3. **Check authentication**

   - For pages requiring authentication, verify authentication settings

4. **Depth restriction**

   - Verify link depth does not exceed depth restriction

5. **Maximum access count**

   - Verify maximum access count has not been reached

Slow Crawling
-------------

**Countermeasures:**

1. **Increase thread count**

   - Increase parallel crawl count (but be mindful of target server load)

2. **Exclude unnecessary URLs**

   - Add images and CSS files to exclude URL patterns

3. **Adjust timeout settings**

   - For slow-responding sites, shorten timeout

4. **Increase crawler memory**

   - See :doc:`setup-memory`

Best Practices
==============

Crawl Configuration Recommendations
------------------------------------

1. **Set appropriate thread count**

   Set an appropriate thread count to avoid placing excessive load on target servers.

2. **Optimize URL patterns**

   Exclude unnecessary files (images, CSS, JavaScript, etc.) to
   reduce crawl time and improve index quality.

3. **Set depth restrictions**

   Set appropriate depth based on site structure.
   Use unlimited (-1) only when crawling the entire site.

4. **Set maximum access count**

   Set an upper limit to avoid crawling unexpectedly large numbers of pages.

5. **Adjust crawl interval**

   Set appropriate intervals based on update frequency.
   - Frequently updated sites: Every 1 hour to several hours
   - Infrequently updated sites: Once per day to once per week

Schedule Configuration Recommendations
---------------------------------------

1. **Night execution**

   Execute during low server load times (e.g., 2 AM).

2. **Avoid duplicate execution**

   Configure to start next crawl after previous crawl completes.

3. **Error notifications**

   Configure email notifications for crawl failures.

References
==========

- :doc:`crawler-advanced` - Advanced Crawler Configuration
- :doc:`crawler-thumbnail` - Thumbnail Configuration
- :doc:`setup-memory` - Memory Configuration
- :doc:`admin-logging` - Log Configuration
