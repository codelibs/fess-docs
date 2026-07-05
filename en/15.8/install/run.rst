=============================
Startup, Shutdown, and Initial Setup
=============================

This page describes the procedures for starting, stopping, and initial setup of the |Fess| server.

.. important::

   Before starting |Fess|, you must start OpenSearch.
   If OpenSearch is not running, |Fess| will not function correctly.

Startup Methods
===============

The startup procedure varies depending on the installation method.

TAR.GZ Version
--------------

Start OpenSearch
~~~~~~~~~~~~~~~~

::

    $ cd /path/to/opensearch-3.7.0
    $ ./bin/opensearch

To start in the background::

    $ ./bin/opensearch -d

Start Fess
~~~~~~~~~~

::

    $ cd /path/to/fess-15.8.0
    $ ./bin/fess

To start in the background::

    $ ./bin/fess -d

.. note::

   Startup may take several minutes.
   You can check the startup status in the log file (``logs/fess.log``).

ZIP Version (Windows)
---------------------

Start OpenSearch
~~~~~~~~~~~~~~~~

1. Open the OpenSearch installation directory
2. Double-click ``opensearch.bat`` in the ``bin`` folder

Or from Command Prompt::

    C:\> cd C:\opensearch-3.7.0
    C:\opensearch-3.7.0> bin\opensearch.bat

Start Fess
~~~~~~~~~~

1. Open the Fess installation directory
2. Double-click ``fess.bat`` in the ``bin`` folder

Or from Command Prompt::

    C:\> cd C:\fess-15.8.0
    C:\fess-15.8.0> bin\fess.bat

RPM/DEB Version (chkconfig)
---------------------------

Start OpenSearch::

    $ sudo service opensearch start

Start Fess::

    $ sudo service fess start

Check startup status::

    $ sudo service fess status

RPM/DEB Version (systemd)
-------------------------

Start OpenSearch::

    $ sudo systemctl start opensearch.service

Start Fess::

    $ sudo systemctl start fess.service

Check startup status::

    $ sudo systemctl status fess.service

Enable automatic startup::

    $ sudo systemctl enable opensearch.service
    $ sudo systemctl enable fess.service

Docker Version
--------------

.. note::

   ``compose.yaml`` and ``compose-opensearch3.yaml`` are not included with
   |Fess| itself. They are provided by the docker-fess project
   (https://github.com/codelibs/docker-fess); obtain the repository and run the
   following commands inside the ``compose`` directory.

Start using Docker Compose::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Check startup status::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

Check logs::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01

Verify Startup
==============

Verify that |Fess| has started successfully.

Health Check
------------

Access the following URL using a browser or curl command::

    http://localhost:8080/

If started successfully, the Fess search screen will be displayed.

Check from command line::

    $ curl -I http://localhost:8080/

If ``HTTP/1.1 200 OK`` is returned, it has started successfully.

Check Logs
----------

Check the startup logs to ensure there are no errors.

TAR.GZ/ZIP version::

    $ tail -f /path/to/fess-15.8.0/logs/fess.log

RPM/DEB version::

    $ sudo tail -f /var/log/fess/fess.log

Or use journalctl::

    $ sudo journalctl -u fess.service -f

Docker version::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01

.. tip::

   When startup completes successfully, a startup-completion message like the
   following is shown on the console and in the log::

       ...Booting the Tomcat: port=8080 contextPath=/
       ...
       Boot successful: url -> http://localhost:8080

Access via Browser
==================

Access the following URLs to verify the web interface.

Search Screen
-------------

**URL**: http://localhost:8080/

The Fess search screen will be displayed. In the initial state, no search results will be displayed because no crawl configuration has been performed.

Admin Screen
------------

**URL**: http://localhost:8080/admin

Default administrator account:

- **Username**: ``admin``
- **Password**: ``admin``

.. warning::

   **Important Security Notice**

   You must change the default password.
   Especially in production environments, it is strongly recommended to change the password immediately after the first login.

Initial Setup
=============

After logging into the admin screen, perform the following initial configuration.

Step 1: Change Administrator Password
--------------------------------------

1. Log in to the admin screen (http://localhost:8080/admin)
2. Click "System" → "User" from the left menu
3. Click the ``admin`` user
4. Enter a new password in the [Password] field
5. Re-enter the same password in the [Password (Confirm)] field
6. Click the [Update] button

.. important::

   Passwords should meet the following criteria:

   - 8 characters or more (the required minimum length set by ``password.min.length``)
   - Combination of uppercase letters, lowercase letters, numbers, and symbols
   - Not easily guessed

   By default, only the minimum length (8 characters) is required; a combination
   of character types is not enforced. Character-type requirements can be enabled
   with settings such as ``password.require.uppercase``.

Step 2: Create Crawl Configuration
-----------------------------------

Create a configuration to crawl target sites or file systems.

1. Click "Crawler" → "Web" from the left menu
2. Click the "New" button
3. Enter required information:

   - **Name**: Name of the crawl configuration (e.g., Company Website)
   - **URL**: Target URL for crawling (e.g., https://www.example.com/). To specify multiple URLs, enter one URL per line
   - **Max Access Count**: Maximum number of documents to crawl (optional)
   - **Interval**: Wait time between accesses (milliseconds; default: ``10000``)

   .. note::

      Other items (such as user agent, number of threads, and depth) use their
      default values when left blank.

4. Click the "Create" button

Step 3: Execute Crawl
---------------------

1. Click "System" → "Scheduler" from the left menu
2. Open the [Default Crawler] job and click the "Start Now" button
3. Wait for the crawl to complete (progress can be checked on the dashboard)

Step 4: Verify Search
---------------------

1. Access the search screen (http://localhost:8080/)
2. Enter a search keyword
3. Verify that search results are displayed

.. note::

   Crawling may take time.
   For large-scale sites, it may take from several hours to several days.

Other Recommended Settings
===========================

For production environments, consider the following settings.

Main Settings via Environment Variables
---------------------------------------

Settings such as the port number, JVM heap size, and the OpenSearch connection
URL can be changed via environment variables. Edit ``bin/fess.in.sh`` for the
TAR.GZ edition, ``/etc/sysconfig/fess`` for the RPM edition, and
``/etc/default/fess`` for the DEB edition. A restart of |Fess| is required after
making changes.

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Environment Variable
     - Default
     - Description
   * - ``FESS_PORT``
     - ``8080``
     - The HTTP port that |Fess| listens on.
   * - ``FESS_HEAP_SIZE``
     - (unset)
     - JVM heap size. Sets the same value for the minimum and maximum. When unset, a minimum of ``256m`` and a maximum of ``2g`` are used (the Windows ZIP edition uses a maximum of ``1g``); the RPM/DEB edition uses ``512m``.
   * - ``SEARCH_ENGINE_HTTP_URL``
     - (unset)
     - URL of the OpenSearch to connect to. When unset, the built-in default ``http://localhost:9201`` is used. Change this when OpenSearch runs on a different port or host (the :doc:`install-linux` procedure sets it to ``http://localhost:9200`` to match the OpenSearch listening port). The RPM/DEB edition sets ``http://localhost:9200`` by default via the package environment file.
   * - ``FESS_LOG_LEVEL``
     - ``warn``
     - Log level of |Fess|.

.. note::

   The Windows ZIP edition's ``bin\fess.in.bat`` does not read these environment
   variables (except the proxy-related ones). The values are written directly in
   the file, so edit ``bin\fess.in.bat`` directly to change them.

Configure Mail Server
---------------------

To receive failure notifications and similar messages by email, configure the
SMTP server and the notification recipient address.

1. In the config file ``app/WEB-INF/classes/fess_env.properties``, specify the
   SMTP server host and port in ``mail.smtp.server.main.host.and.port``
   (default: ``localhost:25``). A restart of |Fess| is required after the change.
2. In the admin UI, click [System] → [General] in the left menu.
3. Enter the recipient email address in the [Notification Mail] field.
4. Click the [Update] button.
5. You can verify that mail is sent correctly with the [Send Test Mail] button.

Configure Time Zone
-------------------

|Fess| uses the server's (OS / JVM) time zone. There is no setting to change the
time zone in the admin UI. To change it, change the OS time zone setting, or add
the JVM option ``-Duser.timezone=Asia/Tokyo`` to ``FESS_JAVA_OPTS`` in
``bin/fess.in.sh`` (on Windows, ``bin\fess.in.bat``).

Adjust Log Level
----------------

In production, you can adjust the log level to reduce disk usage.

The overall log level of |Fess| can be changed with the ``FESS_LOG_LEVEL``
environment variable (default: ``warn``). To control individual loggers in
detail, edit the config file ``app/WEB-INF/classes/log4j2.xml``. Crawling,
suggest, and thumbnail generation run as separate processes, so configure their
log levels individually in
``app/WEB-INF/env/{crawler,suggest,thumbnail}/resources/log4j2.xml``.

See :doc:`../admin/index` for details.

Shutdown Methods
================

TAR.GZ/ZIP Version
------------------

Stop Fess
~~~~~~~~~

Kill the process::

    $ ps aux | grep fess
    $ kill <PID>

Or, stop from the console with ``Ctrl+C`` (if running in the foreground).

Stop OpenSearch::

    $ ps aux | grep opensearch
    $ kill <PID>

RPM/DEB Version (chkconfig)
---------------------------

Stop Fess::

    $ sudo service fess stop

Stop OpenSearch::

    $ sudo service opensearch stop

RPM/DEB Version (systemd)
-------------------------

Stop Fess::

    $ sudo systemctl stop fess.service

Stop OpenSearch::

    $ sudo systemctl stop opensearch.service

Docker Version
--------------

Stop containers::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop

Stop and remove containers::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   To also delete volumes with the ``down`` command, add the ``-v`` option.
   In this case, all data will be deleted, so use with caution.

Restart Methods
===============

TAR.GZ/ZIP Version
------------------

Stop and then start.

RPM/DEB Version
---------------

chkconfig::

    $ sudo service fess restart

systemd::

    $ sudo systemctl restart fess.service

Docker Version
--------------

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml restart

Troubleshooting
===============

Won't Start
-----------

1. **Verify OpenSearch is running**

   ::

       $ curl http://localhost:9200/

   If OpenSearch is not running, start OpenSearch first.

2. **Check for port conflicts**

   ::

       $ sudo netstat -tuln | grep 8080

   If port 8080 is already in use, change the port number.

   - TAR.GZ edition: change ``FESS_PORT`` in ``bin/fess.in.sh``
   - ZIP edition (Windows): edit ``-Dfess.port=8080`` directly in ``bin\fess.in.bat``
   - RPM edition: change ``FESS_PORT`` in ``/etc/sysconfig/fess``
   - DEB edition: change ``FESS_PORT`` in ``/etc/default/fess``

3. **Check logs**

   Identify the problem from error messages.

4. **Verify Java version**

   ::

       $ java -version

   Verify that Java 21 or later is installed.

For detailed troubleshooting, refer to :doc:`troubleshooting`.

Next Steps
==========

After |Fess| has started successfully, refer to the following documentation to begin operation:

- :doc:`../admin/index` - Details on crawl configuration, search settings, and system settings
- :doc:`security` - Security configuration for production environments
- :doc:`troubleshooting` - Common problems and solutions
- :doc:`upgrade` - Version upgrade procedures
- :doc:`uninstall` - Uninstall procedures
