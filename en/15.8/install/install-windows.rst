==========================================
Windows Installation (Detailed Procedure)
==========================================

This page describes the installation procedure for |Fess| on Windows environments.
It covers the installation method using ZIP packages.

.. warning::

   Running with the embedded OpenSearch is not recommended for production environments.
   Always set up an external OpenSearch server.

Prerequisites
=============

- System requirements described in :doc:`prerequisites` are met
- Java 21 is installed
- OpenSearch 3.7.0 is available (or new installation)
- Windows environment variable ``JAVA_HOME`` is configured appropriately

Verify Java Installation
=========================

Open Command Prompt or PowerShell and verify the Java version with the following command.

For Command Prompt::

    C:\> java -version

For PowerShell::

    PS C:\> java -version

Verify that Java 21 or later is displayed.

Environment Variable Configuration
===================================

1. Set ``JAVA_HOME`` Environment Variable

   Set the directory where Java is installed as ``JAVA_HOME``.

   Example::

       JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-21.0.1.12-hotspot

2. Add to ``PATH`` Environment Variable

   Add ``%JAVA_HOME%\bin`` to the ``PATH`` environment variable.

.. tip::

   How to configure environment variables:

   1. Open "Settings" from the Start menu
   2. Click "System" → "About" → "Advanced system settings"
   3. Click the "Environment Variables" button
   4. Configure in "System variables" or "User variables"

Step 1: Install OpenSearch
===========================

Download OpenSearch
-------------------

1. Download the ZIP package for Windows from `Download OpenSearch <https://opensearch.org/downloads.html>`__.

2. Extract the downloaded ZIP file to any directory.

   Example::

       C:\opensearch-3.7.0

   .. note::

      It is recommended to select a directory that does not contain Japanese characters or spaces in the path.

Install OpenSearch Plugins
---------------------------

Open Command Prompt **with administrator privileges** and execute the following commands.

::

    C:\> cd C:\opensearch-3.7.0
    C:\opensearch-3.7.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.7.0
    C:\opensearch-3.7.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.7.0
    C:\opensearch-3.7.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.7.0
    C:\opensearch-3.7.0> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.7.0

.. important::

   Plugin versions must match the OpenSearch version.
   In the example above, all are specified as 3.7.0.

Configure OpenSearch
--------------------

Open ``config\opensearch.yml`` with a text editor and add the following settings.

::

    # Configuration synchronization path (specify absolute path)
    configsync.config_path: C:/opensearch-3.7.0/data/config/

    # Disable security plugin (development environment only)
    plugins.security.disabled: true

.. warning::

   **Important Security Notice**

   Use ``plugins.security.disabled: true`` only in development or test environments.
   In production environments, enable the OpenSearch security plugin and configure appropriate authentication and authorization.
   For details, refer to :doc:`security`.

.. note::

   On Windows, use ``/`` instead of ``\`` for path separators.
   Write ``C:/opensearch-3.7.0/data/config/`` instead of ``C:\opensearch-3.7.0\data\config\``.

.. tip::

   Other recommended settings::

       cluster.name: fess-cluster
       node.name: fess-node-1
       network.host: 0.0.0.0
       discovery.type: single-node

.. tip::

   The OpenSearch heap size is configured via ``-Xms`` / ``-Xmx`` in ``config\jvm.options``.
   It is recommended to set both ``-Xms`` and ``-Xmx`` to the same value, targeting no more than half of available physical memory and less than 32 GB.

Step 2: Install Fess
=====================

Download Fess
-------------

1. Download the ZIP package for Windows from the `download site <https://fess.codelibs.org/en/downloads.html>`__.

2. Extract the downloaded ZIP file to any directory.

   Example::

       C:\fess-15.8.0

   .. note::

      It is recommended to select a directory that does not contain Japanese characters or spaces in the path.

Configure Fess
--------------

Open ``bin\fess.in.bat`` with a text editor.
Near the end of this file, the settings for connecting to an external OpenSearch cluster are already present as commented-out lines.

Before (default state)::

    REM External opensearch cluster
    REM set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.search_engine.http_address=http://localhost:9200
    REM set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.dictionary.path=%SEARCH_ENGINE_HOME%/config/

Remove the leading ``REM `` from the bottom two lines to uncomment them, and change the value of ``fess.dictionary.path`` to the configuration synchronization path for OpenSearch.

After::

    REM External opensearch cluster
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.search_engine.http_address=http://localhost:9200
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.dictionary.path=C:/opensearch-3.7.0/data/config/

.. note::

   - Set ``fess.dictionary.path`` to the same path specified for ``configsync.config_path`` in OpenSearch's ``opensearch.yml``.
   - If OpenSearch is running on a different host, change the hostname or IP address in ``fess.search_engine.http_address`` to the appropriate value.
   - Use ``/`` for path separators.
   - Do not add new ``set FESS_JAVA_OPTS=...`` lines; instead, uncomment and edit the existing commented lines. Specifying the same option more than once may cause unexpected behavior.

.. tip::

   To change the |Fess| heap size, edit ``FESS_MIN_MEM`` (default: ``256m``) and ``FESS_MAX_MEM`` (default: ``1g``) in ``bin\fess.in.bat``, or set the ``FESS_HEAP_SIZE`` environment variable.

Verify Installation
-------------------

Verify that the configuration files have been edited correctly.

In Command Prompt::

    C:\> findstr "fess.search_engine.http_address" C:\fess-15.8.0\bin\fess.in.bat
    C:\> findstr "fess.dictionary.path" C:\fess-15.8.0\bin\fess.in.bat

Step 3: Startup
===============

For startup procedures, refer to :doc:`run`.

Register as Windows Service (Optional)
=======================================

By registering |Fess| as a Windows service, you can configure it to start automatically on system startup.

|Fess| ships with ``bin\service.bat`` for registering it as a Windows service.
This script uses Apache Commons Daemon (procrun), so no third-party tools such as NSSM are required.

.. note::

   Before running ``service.bat``, verify that the ``JAVA_HOME`` environment variable is configured correctly.

Register Fess Service
---------------------

Open Command Prompt **with administrator privileges** and execute the following commands.

1. Register the service::

       C:\> cd C:\fess-15.8.0
       C:\fess-15.8.0> bin\service.bat install

   By default, the service is registered with the ID ``fess-service-x64`` on 64-bit systems and ``fess-service-x86`` on 32-bit systems.
   To specify a service ID explicitly, pass it as an argument: ``bin\service.bat install <ServiceID>``.

2. Start and stop the service::

       C:\fess-15.8.0> bin\service.bat start
       C:\fess-15.8.0> bin\service.bat stop

3. View and change service settings (GUI)::

       C:\fess-15.8.0> bin\service.bat manager

4. Remove the service::

       C:\fess-15.8.0> bin\service.bat remove

.. note::

   - ``service.bat`` internally loads ``bin\fess.in.bat``, so the external OpenSearch connection settings configured in the "Configure Fess" section are also applied to the service.
   - The default startup type is "Manual". To start automatically at system boot, either set the environment variable ``FESS_START_TYPE`` to ``auto`` before registering the service, or change the startup type to "Automatic" in the Services management tool (``services.msc``) after registration.
   - ``service.bat`` registers only the |Fess| service. To register OpenSearch as a service, refer to the procedure provided by OpenSearch.

Firewall Configuration
======================

Open the necessary ports in Windows Defender Firewall.

1. Open "Control Panel" → "Windows Defender Firewall" → "Advanced settings"

2. Create a new rule in "Inbound Rules"

   - Rule type: Port
   - Protocol and port: TCP, 8080
   - Action: Allow the connection
   - Name: Fess Web Interface

Or execute in PowerShell::

    PS C:\> New-NetFirewallRule -DisplayName "Fess Web Interface" -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow

Troubleshooting
===============

Port Conflict
-------------

If port 8080 or 9200 is already in use, you can check with the following command::

    C:\> netstat -ano | findstr :8080
    C:\> netstat -ano | findstr :9200

Change the conflicting port number or stop the conflicting process.

Path Length Limitation
----------------------

Windows has a path length limitation. It is recommended to install in a path as short as possible.

Example::

    C:\opensearch  (recommended)
    C:\Program Files\opensearch-3.7.0  (not recommended - path is too long)

Java Not Recognized
-------------------

If the ``java -version`` command displays an error:

1. Verify that the ``JAVA_HOME`` environment variable is configured correctly
2. Verify that ``%JAVA_HOME%\bin`` is included in the ``PATH`` environment variable
3. Restart Command Prompt to reflect the settings

Next Steps
==========

After installation is complete, refer to the following documentation:

- :doc:`run` - Starting |Fess| and initial setup
- :doc:`security` - Security configuration for production environments
- :doc:`troubleshooting` - Troubleshooting

Frequently Asked Questions
===========================

Q: Is operation on Windows Server recommended?
-----------------------------------------------

A: Yes, operation on Windows Server is possible.
When operating on Windows Server, register as a Windows service and configure appropriate monitoring.

Q: What is the difference between 64-bit and 32-bit versions?
--------------------------------------------------------------

A: |Fess| and OpenSearch support only the 64-bit version.
They will not run on 32-bit Windows.

Q: How to handle paths containing non-ASCII characters?
--------------------------------------------------------

A: Install in a path that does not contain non-ASCII characters or spaces whenever possible.
If you must use a non-ASCII path, you need to properly escape the path in configuration files.
