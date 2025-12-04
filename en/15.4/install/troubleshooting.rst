===============
Troubleshooting
===============

This page describes common problems and solutions during installation, startup, and operation of |Fess|.

Installation Issues
===================

Java Not Recognized
-------------------

**Symptoms:**

::

    -bash: java: command not found

Or::

    'java' is not recognized as an internal or external command

**Cause:**

Java is not installed, or the PATH environment variable is not configured correctly.

**Solution:**

1. Verify Java is installed::

       $ which java
       $ java -version

2. If not installed, install Java 21::

       # Ubuntu/Debian
       $ sudo apt-get update
       $ sudo apt-get install openjdk-21-jdk

       # RHEL/CentOS
       $ sudo yum install java-21-openjdk

3. Set JAVA_HOME environment variable::

       $ export JAVA_HOME=/path/to/java
       $ export PATH=$JAVA_HOME/bin:$PATH

   For persistent configuration, add to ``~/.bashrc`` or ``/etc/profile``.

Plugin Installation Fails
--------------------------

**Symptoms:**

::

    ERROR: Plugin installation failed

**Causes:**

- Network connection issues
- Plugin version does not match OpenSearch version
- Permission issues

**Solution:**

1. Verify OpenSearch version::

       $ /path/to/opensearch/bin/opensearch --version

2. Match plugin version to OpenSearch version::

       $ /path/to/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.1

3. Verify permissions::

       $ sudo /path/to/opensearch/bin/opensearch-plugin install ...

4. For installation through a proxy::

       $ export ES_JAVA_OPTS="-Dhttp.proxyHost=proxy.example.com -Dhttp.proxyPort=8080"
       $ /path/to/opensearch/bin/opensearch-plugin install ...

Startup Issues
==============

Fess Won't Start
----------------

**Symptoms:**

Fess startup command produces an error or exits immediately.

**Verification Items:**

1. **Verify OpenSearch is running**::

       $ curl http://localhost:9200/

   If working correctly, a JSON response will be returned.

2. **Check for port conflicts**::

       $ sudo netstat -tuln | grep 8080

   If port 8080 is already in use, change the port number in the configuration file.

3. **Check log files**::

       $ tail -f /path/to/fess/logs/fess.log

   Identify the cause from error messages.

4. **Verify Java version**::

       $ java -version

   Verify that Java 21 or later is installed.

5. **Check for insufficient memory**::

       $ free -h

   If memory is insufficient, adjust heap size or increase system memory.

OpenSearch Won't Start
----------------------

**Symptoms:**

::

    ERROR: bootstrap checks failed

**Cause:**

System configuration does not meet OpenSearch requirements.

**Solution:**

1. **Set vm.max_map_count**::

       $ sudo sysctl -w vm.max_map_count=262144

   For persistent configuration::

       $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
       $ sudo sysctl -p

2. **Increase file descriptor limits**::

       $ sudo vi /etc/security/limits.conf

   Add the following::

       opensearch  -  nofile  65535
       opensearch  -  nproc   4096

3. **Configure memory locking**::

       $ sudo vi /etc/security/limits.conf

   Add the following::

       opensearch  -  memlock  unlimited

4. Restart OpenSearch::

       $ sudo systemctl restart opensearch

Port Conflict
-------------

**Symptoms:**

::

    Address already in use

**Solution:**

1. Check ports in use::

       $ sudo netstat -tuln | grep 8080
       $ sudo lsof -i :8080

2. Stop the process using the port, or change Fess port number

   Change port number in configuration file (``system.properties``)::

       server.port=9080

Connection Issues
=================

Fess Cannot Connect to OpenSearch
----------------------------------

**Symptoms:**

Logs show errors like the following::

    Connection refused
    or
    No route to host

**Solution:**

1. **Verify OpenSearch is running**::

       $ curl http://localhost:9200/

2. **Verify connection URL**

   Verify the URL configured in ``fess.in.sh`` or ``fess.in.bat`` is correct::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200

3. **Check firewall**::

       $ sudo firewall-cmd --list-all

   Verify port 9200 is open.

4. **Verify network connection**

   If OpenSearch is running on a different host::

       $ ping opensearch-host
       $ telnet opensearch-host 9200

Cannot Access Fess from Browser
--------------------------------

**Symptoms:**

Cannot access http://localhost:8080/ in browser.

**Solution:**

1. **Verify Fess is running**::

       $ ps aux | grep fess

2. **Try accessing on localhost**::

       $ curl http://localhost:8080/

3. **Check firewall**::

       $ sudo firewall-cmd --list-all

   Verify port 8080 is open.

4. **When accessing from another host**

   Verify Fess is listening beyond localhost::

       $ netstat -tuln | grep 8080

   If ``127.0.0.1:8080``, configure to listen on ``0.0.0.0:8080`` or a specific IP address.

Performance Issues
==================

Slow Search
-----------

**Causes:**

- Large index size
- Insufficient memory
- Slow disk I/O
- Complex queries

**Solution:**

1. **Increase heap size**

   Edit ``fess.in.sh``::

       FESS_HEAP_SIZE=4g

   Also adjust OpenSearch heap size::

       export OPENSEARCH_JAVA_OPTS="-Xms4g -Xmx4g"

2. **Optimize index**

   Periodically run optimization from the admin screen at "System" → "Scheduler".

3. **Use SSD**

   If disk I/O is a bottleneck, migrate to SSD.

4. **Enable caching**

   Enable query cache in configuration file.

Slow Crawling
-------------

**Causes:**

- Long crawl interval
- Slow target site response
- Insufficient number of threads

**Solution:**

1. **Adjust crawl interval**

   Shorten the "Interval" in crawl configuration on the admin screen (in milliseconds).

   .. warning::

      If the interval is too short, it may overload the target site. Set an appropriate value.

2. **Increase number of threads**

   Increase crawl thread count in configuration file::

       crawler.thread.count=10

3. **Adjust timeout values**

   For sites with slow responses, increase timeout values.

Data Issues
===========

No Search Results Displayed
----------------------------

**Causes:**

- Index not created
- Crawl failed
- Incorrect search query

**Solution:**

1. **Verify index**::

       $ curl http://localhost:9200/_cat/indices?v

   Verify |Fess| indexes exist.

2. **Check crawl logs**

   Check crawl logs at "System" → "Log" in the admin screen for errors.

3. **Re-run crawl**

   Execute "Default Crawler" from "System" → "Scheduler" in the admin screen.

4. **Simplify search query**

   First search with simple keywords to verify results are returned.

Index Corrupted
---------------

**Symptoms:**

Errors occur during search or unexpected results are returned.

**Solution:**

1. **Delete and recreate index**

   .. warning::

      Deleting the index will lose all search data. Always create a backup first.

   ::

       $ curl -X DELETE http://localhost:9200/fess*

2. **Re-run crawl**

   Execute "Default Crawler" from the admin screen to recreate the index.

Docker-Specific Issues
======================

Container Won't Start
---------------------

**Symptoms:**

Container does not start with ``docker compose up``.

**Solution:**

1. **Check logs**::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs

2. **Check for insufficient memory**

   Increase memory allocated to Docker (from Docker Desktop settings).

3. **Check for port conflicts**::

       $ docker ps

   Verify no other containers are using ports 8080 or 9200.

4. **Verify Docker Compose file**

   Check for syntax errors in YAML file::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml config

Container Starts But Cannot Access Fess
----------------------------------------

**Solution:**

1. **Check container status**::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

2. **Check logs**::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs fess

3. **Verify network settings**::

       $ docker network ls
       $ docker network inspect <network_name>

Windows-Specific Issues
=======================

Path Issues
-----------

**Symptoms:**

Errors occur when paths contain spaces or Japanese characters.

**Solution:**

Install in a directory that does not contain spaces or Japanese characters in the path.

Example::

    C:\opensearch  (recommended)
    C:\Program Files\opensearch  (not recommended)

Cannot Register as Service
---------------------------

**Solution:**

Use third-party tools such as NSSM to register as a Windows service.

For details, refer to :doc:`install-windows`.

Other Issues
============

Change Log Level
----------------

To check detailed logs, change the log level to DEBUG.

Edit ``log4j2.xml``::

    <Logger name="org.codelibs.fess" level="debug"/>

Reset Database
--------------

To reset configuration, delete OpenSearch indexes::

    $ curl -X DELETE http://localhost:9200/.fess_config*

.. warning::

   This command will delete all configuration data.

Support Information
===================

If problems cannot be resolved, use the following support resources:

Community Support
-----------------

- **Issues**: https://github.com/codelibs/fess/issues

  When reporting issues, include the following information:

  - Fess version
  - OpenSearch version
  - OS and version
  - Error messages (excerpts from logs)
  - Reproduction steps

- **Forum**: https://discuss.codelibs.org/

Commercial Support
------------------

For commercial support needs, please contact N2SM, Inc.:

- **Web**: https://www.n2sm.net/

Collecting Debug Information
=============================

When reporting issues, collecting the following information is helpful:

1. **Version information**::

       $ cat /path/to/fess/VERSION
       $ /path/to/opensearch/bin/opensearch --version
       $ java -version

2. **System information**::

       $ uname -a
       $ cat /etc/os-release
       $ free -h
       $ df -h

3. **Log files**::

       $ tar czf fess-logs.tar.gz /path/to/fess/logs/

4. **Configuration files** (after removing sensitive information)::

       $ tar czf fess-config.tar.gz /path/to/fess/app/WEB-INF/conf/

5. **OpenSearch status**::

       $ curl http://localhost:9200/_cluster/health?pretty
       $ curl http://localhost:9200/_cat/indices?v
