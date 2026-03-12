==================
Memory Configuration
==================

Overview
========

For Java applications, you need to configure the maximum heap memory used by each process.
In |Fess|, memory configuration is performed for the following three components:

- Fess Web Application
- Crawler Process
- OpenSearch

Proper memory configuration enables improved performance and stable operation.

Fess Web Application Memory Configuration
==========================================

When Configuration is Needed
-----------------------------

Consider adjusting the memory size in the following cases:

- OutOfMemory errors are recorded in ``fess.log``
- Need to handle a large number of concurrent requests
- Administration screen operations are slow or timeout

The default memory size is sufficient for typical usage, but high-load environments require an increase.

Configuration via Environment Variables
----------------------------------------

Set the ``FESS_HEAP_SIZE`` environment variable.

::

    export FESS_HEAP_SIZE=2g

Units:

- ``m``: megabytes
- ``g``: gigabytes

For RPM/DEB Packages
---------------------

For RPM package installations, edit ``/etc/sysconfig/fess``.

::

    FESS_HEAP_SIZE=2g

For DEB packages, edit ``/etc/default/fess``.

::

    FESS_HEAP_SIZE=2g

.. warning::
   After changing the memory size, you must restart the |Fess| service.

Recommended Memory Sizes
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Environment
     - Recommended Heap Size
     - Notes
   * - Development/Test
     - 512m-1g
     - Small-scale index
   * - Small Production
     - 1g-2g
     - Tens to hundreds of thousands of documents
   * - Medium Production
     - 2g-4g
     - Hundreds of thousands to millions of documents
   * - Large Production
     - 4g-8g
     - Millions or more documents

Crawler Memory Configuration
=============================

When Configuration is Needed
-----------------------------

You need to increase crawler memory size in the following cases:

- Increasing parallel crawl count
- Crawling large files
- OutOfMemory errors occur during crawling

Configuration Method
--------------------

Edit ``app/WEB-INF/classes/fess_config.properties`` or ``/etc/fess/fess_config.properties``.

::

    jvm.crawler.options=-Xmx512m

For example, to change to 1GB:

::

    jvm.crawler.options=-Xmx1g

.. note::
   This setting applies per crawler process (per scheduler job).
   When running multiple crawl jobs simultaneously, each job uses the specified memory.

Recommended Settings
--------------------

- **Normal Web Crawling**: 512m-1g
- **High-Volume Parallel Crawling**: 1g-2g
- **Large File Crawling**: 2g-4g

Detailed JVM Options
--------------------

Detailed JVM options for the crawler can be configured in ``jvm.crawler.options``.
The default configuration includes the following optimizations:

**Key Options:**

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Option
     - Description
   * - ``-Xms128m -Xmx512m``
     - Initial and maximum heap size
   * - ``-XX:MaxMetaspaceSize=128m``
     - Maximum Metaspace size
   * - ``-XX:+UseG1GC``
     - Use G1 garbage collector
   * - ``-XX:MaxGCPauseMillis=60000``
     - GC pause time goal (60 seconds)
   * - ``-XX:-HeapDumpOnOutOfMemoryError``
     - Disable heap dump on OutOfMemory

OpenSearch Memory Configuration
================================

Important Considerations
------------------------

For OpenSearch, you need to consider the following two points when configuring memory:

1. **Java Heap Memory**: Used by the OpenSearch process
2. **OS Filesystem Cache**: Critical for search performance

.. warning::
   If Java heap memory is set too large, the memory available for OS filesystem cache
   will decrease, resulting in degraded search performance.

Configuration Method
--------------------

Linux Environment
~~~~~~~~~~~~~~~~~

OpenSearch heap memory is specified via environment variables or OpenSearch configuration files.

Configure via environment variable:

::

    export OPENSEARCH_HEAP_SIZE=2g

Or edit ``config/jvm.options``:

::

    -Xms2g
    -Xmx2g

.. note::
   It is recommended to set the minimum heap size (``-Xms``) and maximum heap size (``-Xmx``) to the same value.

Windows Environment
~~~~~~~~~~~~~~~~~~~

Edit the ``config\jvm.options`` file.

::

    -Xms2g
    -Xmx2g

Recommended Memory Sizes
------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Index Size
     - Recommended Heap Size
     - Recommended Total Memory
   * - Up to 10GB
     - 2g
     - 4GB or more
   * - 10GB-50GB
     - 4g
     - 8GB or more
   * - 50GB-100GB
     - 8g
     - 16GB or more
   * - 100GB or more
     - 16g-31g
     - 32GB or more

.. warning::
   Do not configure OpenSearch heap memory to exceed 32GB.
   Exceeding 32GB disables Compressed OOP, reducing memory efficiency.

Best Practices
--------------

1. **Allocate 50% of Physical Memory to Heap**

   Allocate approximately 50% of the server's physical memory to OpenSearch heap.
   The remainder is used for the OS and filesystem cache.

2. **Maximum 31GB**

   Set heap size to a maximum of 31GB; if more is needed, add additional nodes.

3. **Verification in Production**

   Refer to the official OpenSearch documentation for optimal settings based on your environment.

Suggest and Thumbnail Processing Memory Configuration
======================================================

Suggest Generation Process
---------------------------

Memory configuration for suggest generation processing is set in ``jvm.suggest.options``.

::

    jvm.suggest.options=-Xmx256m

The following settings are used by default:

- Initial heap: 128MB
- Maximum heap: 256MB
- Maximum Metaspace: 128MB

Thumbnail Generation Process
-----------------------------

Memory configuration for thumbnail generation processing is set in ``jvm.thumbnail.options``.

::

    jvm.thumbnail.options=-Xmx256m

The following settings are used by default:

- Initial heap: 128MB
- Maximum heap: 256MB
- Maximum Metaspace: 128MB

.. note::
   When processing large images for thumbnail generation, you need to increase memory.

Memory Monitoring and Tuning
=============================

Checking Memory Usage
---------------------

Fess Memory Usage
~~~~~~~~~~~~~~~~~

You can check this on the "System Information" page in the administration screen.

Or use JVM monitoring tools:

::

    jps -l  # Check Fess process
    jstat -gcutil <PID> 1000  # Display GC statistics every second

OpenSearch Memory Usage
~~~~~~~~~~~~~~~~~~~~~~~

::

    curl -X GET "localhost:9201/_nodes/stats/jvm?pretty"
    curl -X GET "localhost:9201/_cat/nodes?v&h=heap.percent,ram.percent"

Signs of Memory Shortage
-------------------------

If the following symptoms appear, there may be a memory shortage.

**Fess Web Application:**

- Slow response
- ``OutOfMemoryError`` recorded in logs
- Process terminates unexpectedly

**Crawler:**

- Crawling stops midway
- ``OutOfMemoryError`` recorded in ``fess_crawler.log``
- Large file crawling fails

**OpenSearch:**

- Slow search
- Slow indexing
- ``circuit_breaker_exception`` errors occur

Tuning Procedure
----------------

1. **Check Current Memory Usage**

   Monitor memory usage for each component.

2. **Identify Bottlenecks**

   Determine which component is experiencing memory shortage.

3. **Increase Gradually**

   Rather than increasing significantly at once, increase by 25-50% and verify effectiveness.

4. **Consider Overall System Balance**

   Ensure total memory for all components does not exceed physical memory.

5. **Continuous Monitoring**

   Continuously monitor memory usage and adjust as needed.

Memory Leak Countermeasures
----------------------------

If a memory leak is suspected:

1. **Obtain Heap Dump**

::

    jmap -dump:format=b,file=heap.bin <PID>

2. **Analyze Heap Dump**

   Analyze using tools such as Eclipse Memory Analyzer (MAT).

3. **Report Issues**

   If you discover a memory leak, please report it on GitHub Issues.

Troubleshooting
===============

OutOfMemoryError Occurs
------------------------

**Fess Web Application:**

1. Increase ``FESS_HEAP_SIZE``.
2. Limit concurrent access count.
3. Lower log level to reduce memory usage from logging.

**Crawler:**

1. Increase ``-Xmx`` in ``jvm.crawler.options``.
2. Reduce parallel crawl count.
3. Adjust crawl settings to exclude large files.

**OpenSearch:**

1. Increase heap size (up to 31GB maximum).
2. Review index shard count.
3. Check query complexity.

Long GC Pause Times
-------------------

1. Adjust G1GC settings.
2. Set heap size appropriately (too large or too small will cause frequent GC).
3. Consider updating to a newer Java version.

Performance Does Not Improve After Memory Configuration
--------------------------------------------------------

1. Check other resources such as CPU, disk I/O, and network.
2. Optimize indexes.
3. Review queries and crawl settings.

References
==========

- :doc:`setup-port-network` - Port and Network Configuration
- :doc:`crawler-advanced` - Advanced Crawler Configuration
- :doc:`admin-logging` - Log Configuration
- `OpenSearch Memory Settings <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/index/#important-settings>`_
- `Java GC Tuning <https://docs.oracle.com/en/java/javase/11/gctuning/>`_
