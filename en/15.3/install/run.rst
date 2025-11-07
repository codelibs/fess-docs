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

    $ cd /path/to/opensearch-3.3.0
    $ ./bin/opensearch

To start in the background::

    $ ./bin/opensearch -d

Start Fess
~~~~~~~~~~

::

    $ cd /path/to/fess-15.3.0
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

    C:\> cd C:\opensearch-3.3.0
    C:\opensearch-3.3.0> bin\opensearch.bat

Start Fess
~~~~~~~~~~

1. Open the Fess installation directory
2. Double-click ``fess.bat`` in the ``bin`` folder

Or from Command Prompt::

    C:\> cd C:\fess-15.3.0
    C:\fess-15.3.0> bin\fess.bat

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

Start using Docker Compose::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Check startup status::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

Check logs::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess

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

    $ tail -f /path/to/fess-15.3.0/logs/fess.log

RPM/DEB version::

    $ sudo tail -f /var/log/fess/fess.log

Or use journalctl::

    $ sudo journalctl -u fess.service -f

Docker version::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess

.. tip::

   When started successfully, a message like the following will be displayed in the logs::

       INFO  Boot - Fess is ready.

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
4. Enter a new password in the "Password" field
5. Click the "Confirm" button
6. Click the "Update" button

.. important::

   Passwords should meet the following criteria:

   - 8 characters or more
   - Combination of uppercase letters, lowercase letters, numbers, and symbols
   - Not easily guessed

Step 2: Create Crawl Configuration
-----------------------------------

Create a configuration to crawl target sites or file systems.

1. Click "Crawler" → "Web" from the left menu
2. Click the "New" button
3. Enter required information:

   - **Name**: Name of the crawl configuration (e.g., Company Website)
   - **URL**: Target URL for crawling (e.g., https://www.example.com/)
   - **Max Access Count**: Maximum number of pages to crawl
   - **Interval**: Crawl interval (milliseconds)

4. Click the "Create" button

Step 3: Execute Crawl
---------------------

1. Click "System" → "Scheduler" from the left menu
2. Click the "Start Now" button for the "Default Crawler" job
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

Configure Mail Server
---------------------

Configure the mail server to receive failure notifications and reports via email.

1. Click "System" → "General" from the left menu
2. Click the "Mail" tab
3. Enter SMTP server information
4. Click the "Update" button

Configure Time Zone
-------------------

1. Click "System" → "General" from the left menu
2. Set "Time Zone" to an appropriate value (e.g., Asia/Tokyo)
3. Click the "Update" button

Adjust Log Level
----------------

In production environments, you can adjust the log level to reduce disk usage.

Edit the configuration file (``app/WEB-INF/classes/log4j2.xml``).

For details, refer to the administrator guide.

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

   If port 8080 is already in use, change the port number in the configuration file.

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

- **Administrator Guide**: Details on crawl configuration, search settings, and system settings
- :doc:`security` - Security configuration for production environments
- :doc:`troubleshooting` - Common problems and solutions
- :doc:`upgrade` - Version upgrade procedures
- :doc:`uninstall` - Uninstall procedures
