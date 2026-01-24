==================
Log Configuration
==================

Overview
========

|Fess| outputs multiple log files to record system operation status and error information.
Proper log configuration facilitates troubleshooting and system monitoring.

Log File Types
==============

Main Log Files
--------------

The main log files output by |Fess| are as follows:

.. list-table:: Log File List
   :header-rows: 1
   :widths: 25 75

   * - File Name
     - Contents
   * - ``fess.log``
     - Administration and search screen operation logs, application errors, system events
   * - ``fess_crawler.log``
     - Crawl execution logs, crawl target URLs, retrieved document information, errors
   * - ``fess_suggest.log``
     - Suggest (search suggestions) generation logs, index update information
   * - ``server_?.log``
     - Application server system logs such as Tomcat
   * - ``audit.log``
     - User authentication, login/logout, important operation audit logs

Log File Locations
------------------

**For ZIP installation:**

::

    {FESS_HOME}/logs/

**For RPM/DEB packages:**

::

    /var/log/fess/

Checking Logs During Troubleshooting
-------------------------------------

When problems occur, check logs using the following procedure:

1. **Identify Error Type**

   - Application errors → ``fess.log``
   - Crawl errors → ``fess_crawler.log``
   - Authentication errors → ``audit.log``
   - Server errors → ``server_?.log``

2. **Check Latest Errors**

   ::

       tail -f /var/log/fess/fess.log

3. **Search for Specific Errors**

   ::

       grep -i "error" /var/log/fess/fess.log
       grep -i "exception" /var/log/fess/fess.log

4. **Check Error Context**

   Check logs before and after error occurrence to identify causes.

   ::

       grep -B 10 -A 10 "OutOfMemoryError" /var/log/fess/fess.log

Log Level Configuration
=======================

About Log Levels
----------------

Log levels control the detail of logs to output.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Level
     - Description
   * - ``FATAL``
     - Fatal errors (application cannot continue)
   * - ``ERROR``
     - Errors (some functionality does not work)
   * - ``WARN``
     - Warnings (potential issues)
   * - ``INFO``
     - Information (important events)
   * - ``DEBUG``
     - Debug information (detailed operation logs)
   * - ``TRACE``
     - Trace information (most detailed)

Recommended Log Levels
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Environment
     - Recommended Level
     - Reason
   * - Production
     - ``WARN``
     - Prioritize performance and disk space
   * - Staging
     - ``INFO``
     - Record important events
   * - Development
     - ``DEBUG``
     - Need detailed debug information
   * - Problem Investigation
     - ``DEBUG`` or ``TRACE``
     - Temporarily enable detailed logs

Changing from Administration Screen
------------------------------------

The easiest method is changing from the administration screen.

1. Log in to the administration screen.
2. Select "General" from the "System" menu.
3. Select the desired level in "Log Level".
4. Click the "Update" button.

.. note::
   Changes made from the administration screen are retained after |Fess| restart.

Changing via Configuration File
--------------------------------

For more detailed log configuration, edit the Log4j2 configuration file.

Configuration File Location
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **ZIP installation**: ``app/WEB-INF/classes/log4j2.xml``
- **RPM/DEB packages**: ``/etc/fess/log4j2.xml``

Basic Configuration Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Default log level:**

::

    <Logger name="org.codelibs.fess" level="warn"/>

**Example: Change to DEBUG level**

::

    <Logger name="org.codelibs.fess" level="debug"/>

**Example: Change log level for specific package**

::

    <Logger name="org.codelibs.fess.crawler" level="info"/>
    <Logger name="org.codelibs.fess.ds" level="debug"/>
    <Logger name="org.codelibs.fess.app.web" level="warn"/>

.. warning::
   ``DEBUG`` and ``TRACE`` levels output large amounts of logs.
   Do not use in production environments as it affects disk space and performance.

Configuration via Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also specify log level at system startup.

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dlog.level=debug"

Crawler Log Configuration
==========================

Crawler logs are output at ``INFO`` level by default.

Configuration from Administration Screen
-----------------------------------------

1. Open the target crawl configuration from the "Crawler" menu in the administration screen.
2. Select "Script" in the "Settings" tab.
3. Add the following to the script field.

::

    logLevel("DEBUG")

Configurable values:

- ``FATAL``
- ``ERROR``
- ``WARN``
- ``INFO``
- ``DEBUG``
- ``TRACE``

Change Log Level for Specific URL Patterns Only
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    if (url.contains("example.com")) {
        logLevel("DEBUG")
    }

Change Log Level for Entire Crawler Process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configure in ``fess_config.properties``:

::

    logging.level.org.codelibs.fess.crawler=DEBUG

Log Rotation
============

Overview
--------

Log files grow over time, so periodic rotation (generation management) is necessary.

Automatic Rotation with Log4j2
-------------------------------

|Fess| automatically performs log rotation using Log4j2's RollingFileAppender.

Default Configuration
~~~~~~~~~~~~~~~~~~~~~

- **File Size**: Rotate when exceeding 10MB
- **Generations to Keep**: Maximum 10 files

Configuration file example (``log4j2.xml``):

::

    <RollingFile name="FessFile"
                 fileName="${log.dir}/fess.log"
                 filePattern="${log.dir}/fess.log.%i">
        <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n"/>
        <Policies>
            <SizeBasedTriggeringPolicy size="10MB"/>
        </Policies>
        <DefaultRolloverStrategy max="10"/>
    </RollingFile>

Daily Rotation Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For daily rotation instead of size-based:

::

    <RollingFile name="FessFile"
                 fileName="${log.dir}/fess.log"
                 filePattern="${log.dir}/fess.log.%d{yyyy-MM-dd}">
        <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n"/>
        <Policies>
            <TimeBasedTriggeringPolicy interval="1" modulate="true"/>
        </Policies>
        <DefaultRolloverStrategy max="30"/>
    </RollingFile>

Compression Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

For automatic compression during rotation:

::

    <RollingFile name="FessFile"
                 fileName="${log.dir}/fess.log"
                 filePattern="${log.dir}/fess.log.%d{yyyy-MM-dd}.gz">
        <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n"/>
        <Policies>
            <TimeBasedTriggeringPolicy interval="1" modulate="true"/>
        </Policies>
        <DefaultRolloverStrategy max="30"/>
    </RollingFile>

Rotation with logrotate
------------------------

In Linux environments, you can also manage log rotation using logrotate.

Example of ``/etc/logrotate.d/fess``:

::

    /var/log/fess/*.log {
        daily
        rotate 14
        compress
        delaycompress
        missingok
        notifempty
        create 0644 fess fess
        sharedscripts
        postrotate
            systemctl reload fess > /dev/null 2>&1 || true
        endscript
    }

Configuration explanation:

- ``daily``: Daily rotation
- ``rotate 14``: Keep 14 generations
- ``compress``: Compress old logs
- ``delaycompress``: Don't compress one generation back (application may be writing)
- ``missingok``: Don't error if log file is missing
- ``notifempty``: Don't rotate empty log files
- ``create 0644 fess fess``: New log file permissions and owner

Log Monitoring
==============

In production environments, it is recommended to monitor log files for early error detection.

Log Patterns to Monitor
-----------------------

Important Error Patterns
~~~~~~~~~~~~~~~~~~~~~~~~~

- ``ERROR``, ``FATAL`` level logs
- ``OutOfMemoryError``
- ``Connection refused``
- ``Timeout``
- ``Exception``
- ``circuit_breaker_exception``
- ``Too many open files``

Patterns to Warn On
~~~~~~~~~~~~~~~~~~~

- Frequent ``WARN`` level logs
- ``Retrying``
- ``Slow query``
- ``Queue full``

Real-Time Monitoring
--------------------

Real-time monitoring with tail command:

::

    tail -f /var/log/fess/fess.log | grep -i "error\|exception"

Simultaneous monitoring of multiple log files:

::

    tail -f /var/log/fess/*.log

Monitoring Tool Examples
-------------------------

**Logwatch**

Periodic log file analysis and reporting.

::

    # Install (CentOS/RHEL)
    yum install logwatch

    # Send daily report
    logwatch --service fess --mailto admin@example.com

**Logstash + OpenSearch + OpenSearch Dashboards**

Real-time log analysis and visualization.

**Fluentd**

Log collection and forwarding.

::

    <source>
      @type tail
      path /var/log/fess/fess.log
      pos_file /var/log/fluentd/fess.log.pos
      tag fess.app
      <parse>
        @type multiline
        format_firstline /^\d{4}-\d{2}-\d{2}/
        format1 /^(?<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) \[(?<thread>.*?)\] (?<level>\w+)\s+(?<logger>.*?) - (?<message>.*)/
      </parse>
    </source>

**Prometheus + Grafana**

Metrics monitoring and alerting.

Alert Configuration
-------------------

Example notification on error detection:

::

    # Simple email notification script
    tail -n 0 -f /var/log/fess/fess.log | while read line; do
        echo "$line" | grep -i "error\|fatal" && \
        echo "$line" | mail -s "Fess Error Alert" admin@example.com
    done

Log Format
==========

Default Format
--------------

|Fess| default log format:

::

    %d{ISO8601} [%t] %-5p %c - %m%n

Explanation of each element:

- ``%d{ISO8601}``: Timestamp (ISO8601 format)
- ``[%t]``: Thread name
- ``%-5p``: Log level (5 character width, left-aligned)
- ``%c``: Logger name (package name)
- ``%m``: Message
- ``%n``: Newline

Custom Format Examples
-----------------------

JSON Format Log Output
~~~~~~~~~~~~~~~~~~~~~~

::

    <PatternLayout>
        <pattern>{"timestamp":"%d{ISO8601}","thread":"%t","level":"%-5p","logger":"%c","message":"%m"}%n</pattern>
    </PatternLayout>

Include More Detailed Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c{1.} [%F:%L] - %m%n"/>

Additional information:

- ``%c{1.}``: Abbreviated package name
- ``%F``: File name
- ``%L``: Line number

Performance Impact
==================

Log output affects disk I/O and performance.

Best Practices
--------------

1. **Use WARN level or higher in production**

   Avoid outputting unnecessary detailed logs.

2. **Regularly clean up log files**

   Delete or compress old log files.

3. **Use asynchronous log output**

   Use Log4j2's asynchronous appender to reduce log output overhead.

   ::

       <Async name="AsyncFile">
           <AppenderRef ref="FessFile"/>
       </Async>

4. **Ensure adequate disk space**

   Secure sufficient disk space for log files.

5. **Choose appropriate log level**

   Set log level appropriate for the environment.

Performance Measurement
-----------------------

Measure log output impact:

::

    # Check log output volume
    du -sh /var/log/fess/

    # Log increase per hour
    watch -n 3600 'du -sh /var/log/fess/'

Troubleshooting
===============

Logs Not Being Output
---------------------

**Causes and Solutions:**

1. **Log Directory Permissions**

   ::

       ls -ld /var/log/fess/
       # Change permissions if necessary
       sudo chown -R fess:fess /var/log/fess/
       sudo chmod 755 /var/log/fess/

2. **Disk Space**

   ::

       df -h /var/log
       # If insufficient space, delete old logs
       find /var/log/fess/ -name "*.log.*" -mtime +30 -delete

3. **Log4j2 Configuration File**

   ::

       # Check configuration file syntax
       xmllint --noout /etc/fess/log4j2.xml

4. **Check SELinux**

   ::

       # If SELinux is enabled
       getenforce
       # Set context if necessary
       restorecon -R /var/log/fess/

Log Files Become Too Large
---------------------------

1. **Adjust Log Level**

   Set to ``WARN`` or higher.

2. **Check Log Rotation Configuration**

   ::

       # Check log4j2.xml configuration
       grep -A 5 "RollingFile" /etc/fess/log4j2.xml

3. **Disable Unnecessary Log Output**

   ::

       # Suppress logs for specific packages
       <Logger name="org.apache.http" level="error"/>

4. **Temporary Measures**

   ::

       # Compress old log files
       gzip /var/log/fess/fess.log.[1-9]

       # Delete old log files
       find /var/log/fess/ -name "*.log.*" -mtime +7 -delete

Cannot Find Specific Logs
--------------------------

1. **Check Log Level**

   If log level is too low, logs won't be output.

   ::

       grep "org.codelibs.fess" /etc/fess/log4j2.xml

2. **Check Log File Path**

   ::

       # Check actual log output destination
       ps aux | grep fess
       lsof -p <PID> | grep log

3. **Check Timestamp**

   Verify that system time is correct.

   ::

       date
       timedatectl status

4. **Log Buffering**

   Logs may not be written immediately.

   ::

       # Force log flush
       systemctl reload fess

Logs Have Character Encoding Issues
------------------------------------

1. **Encoding Configuration**

   Specify character encoding in ``log4j2.xml``:

   ::

       <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n" charset="UTF-8"/>

2. **Environment Variable Configuration**

   ::

       export LANG=ja_JP.UTF-8
       export LC_ALL=ja_JP.UTF-8

References
==========

- :doc:`setup-memory` - Memory Configuration
- :doc:`crawler-advanced` - Advanced Crawler Configuration
- :doc:`admin-index-backup` - Index Backup
- `Log4j2 Documentation <https://logging.apache.org/log4j/2.x/>`_
