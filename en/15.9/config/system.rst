=======================
System-related settings
=======================

Configuration of ports used
===========================

The default port used by |Fess| is 8080. To change it, follow these steps:

For Linux environments, edit ``bin/fess.in.sh``:

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.port=8080"

For Windows environments, edit ``bin\\fess.in.bat``:

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=8080

If you are registering |Fess| as a Windows service, also update the port in ``bin\\service.bat``:

::

    set FESS_PARAMS=-Dfess;-Dfess.home="%FESS_HOME%";-Dfess.es.dir="%SEARCH_ENGINE_HOME%";-Dfess.home="%FESS_HOME%";-Dfess.context.path="/";-Dfess.port=8080;-Dfess.webapp.path="%FESS_HOME%\\app";-Dfess.temp.path="%FESS_HOME%\\temp";-Dfess.log.name="%APP_NAME%";-Dfess.log.path="%FESS_HOME%\\logs";-Dfess.log.level=warn;-Dlasta.env=web;-Dtomcat.config.path=tomcat_config.properties

Configuration of memory used
============================

In Java, each process has a maximum memory limit. Even if your server has 8GB of physical memory, the process won't use more memory than the defined limit. The amount of memory consumed can vary significantly depending on the number of crawling threads and intervals. If you encounter memory issues, follow these steps to adjust the settings.

On servers running OpenSearch, excessive allocation of Java heap memory can degrade performance due to the use of the OS file system cache. Refer to the OpenSearch documentation for appropriate settings.

Changing the maximum heap memory value
--------------------------------------

Depending on the crawl settings, the following OutOfMemory error may occur.

::

    java.lang.OutOfMemoryError: Java heap space

If this occurs, increase the maximum value of heap memory.
Specify the environment variable FESS_HEAP_SIZE as FESS_HEAP_SIZE=2g or change FESS_HEAP_SIZE in ``/etc/sysconfig/fess`` if it is rpm.

Crawler-side heap memory maximum change
---------------------------------------

The maximum heap memory on the crawler side can also be adjusted.
It should be increased if the filesystem or other systems are being heavily crawled.
To make this change, modify the line -Xmx512m in the jvm.crawler.options found in ``app/WEB-INF/classes/fess_config.properties`` or ``/etc/fess/fess_config.properties``.

Configuration of logs
=====================

Log files
---------

|Fess| output log files are listed below.

Table: list of log files

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table:: Table: List of log files
   :header-rows: 1

   * - filename
     - Contents.
   * - ``fess.log``
     - Logs of operations on the admin and search screens.
   * - ``fess_crawler.log``
     - Output logs when crawling is executed.
   * - ``fess_suggest.log``
     - Output logs when suggestions are generated.
   * - ``server_? .log``
     - Outputs the system log.
   * - ``audit.log``
     - Outputs the audit log of logins, etc.


Check the above logs in case of problems with operation.

Change log level
----------------

You can change the log level value of the output log in General on the management screen.
If you want to configure more detailed log settings, you can change them in ``app/WEB-INF/classes/log4j2.xml`` or ``/etc/fess/log4j2.xml``.
By default, the output is at WARN level.

Crawler logs are output at INFO level by default.
If you want to change the log level, specify it using the logLevel(String) method in the crawl job settings on the management screen.
