========================================
Windows Installation (Detailed Procedure)
========================================

This page describes the installation procedure for |Fess| on Windows environments.
It covers the installation method using ZIP packages.

.. warning::

   Running with the embedded OpenSearch is not recommended for production environments.
   Always set up an external OpenSearch server.

Prerequisites
=============

- System requirements described in :doc:`prerequisites` are met
- Java 21 is installed
- OpenSearch 3.3.2 is available (or new installation)
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

       C:\opensearch-3.3.2

   .. note::

      It is recommended to select a directory that does not contain Japanese characters or spaces in the path.

Install OpenSearch Plugins
---------------------------

Open Command Prompt **with administrator privileges** and execute the following commands.

::

    C:\> cd C:\opensearch-3.3.2
    C:\opensearch-3.3.2> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.1
    C:\opensearch-3.3.2> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.1
    C:\opensearch-3.3.2> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.1
    C:\opensearch-3.3.2> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.1

.. important::

   Plugin versions must match the OpenSearch version.
   In the example above, all are specified as 3.3.2.

Configure OpenSearch
--------------------

Open ``config\opensearch.yml`` with a text editor and add the following settings.

::

    # Configuration synchronization path (specify absolute path)
    configsync.config_path: C:/opensearch-3.3.2/data/config/

    # Disable security plugin (development environment only)
    plugins.security.disabled: true

.. warning::

   **Important Security Notice**

   Use ``plugins.security.disabled: true`` only in development or test environments.
   In production environments, enable the OpenSearch security plugin and configure appropriate authentication and authorization.
   For details, refer to :doc:`security`.

.. note::

   On Windows, use ``/`` instead of ``\`` for path separators.
   Write ``C:/opensearch-3.3.2/data/config/`` instead of ``C:\opensearch-3.3.2\data\config\``.

.. tip::

   Other recommended settings::

       cluster.name: fess-cluster
       node.name: fess-node-1
       network.host: 0.0.0.0
       discovery.type: single-node

Step 2: Install Fess
=====================

Download Fess
-------------

1. Download the ZIP package for Windows from the `download site <https://fess.codelibs.org/downloads.html>`__.

2. Extract the downloaded ZIP file to any directory.

   Example::

       C:\fess-15.3.2

   .. note::

      It is recommended to select a directory that does not contain Japanese characters or spaces in the path.

Configure Fess
--------------

Open ``bin\fess.in.bat`` with a text editor and add or modify the following settings.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.search_engine.http_address=http://localhost:9200
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.dictionary.path=C:/opensearch-3.3.2/data/config/

.. note::

   - If OpenSearch is running on a different host, change ``fess.search_engine.http_address`` to the appropriate hostname or IP address.
   - Use ``/`` for path separators.

Verify Installation
-------------------

Verify that the configuration files have been edited correctly.

In Command Prompt::

    C:\> findstr "fess.search_engine.http_address" C:\fess-15.3.2\bin\fess.in.bat
    C:\> findstr "fess.dictionary.path" C:\fess-15.3.2\bin\fess.in.bat

Step 3: Startup
===============

For startup procedures, refer to :doc:`run`.

Register as Windows Service (Optional)
=======================================

By registering |Fess| and OpenSearch as Windows services, you can configure them to start automatically on system startup.

.. note::

   To register as a Windows service, you need to use third-party tools (such as NSSM).
   For detailed procedures, refer to the documentation for each tool.

Example Using NSSM
------------------

1. Download and extract `NSSM (Non-Sucking Service Manager) <https://nssm.cc/download>`__.

2. Register OpenSearch as a service::

       C:\> nssm install OpenSearch C:\opensearch-3.3.2\bin\opensearch.bat

3. Register Fess as a service::

       C:\> nssm install Fess C:\fess-15.3.2\bin\fess.bat

4. Set service dependencies (Fess depends on OpenSearch)::

       C:\> sc config Fess depend= OpenSearch

5. Start services::

       C:\> net start OpenSearch
       C:\> net start Fess

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
    C:\Program Files\opensearch-3.3.2  (not recommended - path is too long)

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

Q: How to handle paths containing Japanese characters?
-------------------------------------------------------

A: Install in a path that does not contain Japanese characters or spaces whenever possible.
If you must use a Japanese path, you need to properly escape the path in configuration files.
