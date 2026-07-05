=============================
Windows Service Registration
=============================

Registering as a Windows Service
==================================

|Fess| can be registered as a Windows service. Registering as a service allows |Fess| to start automatically when the system boots.
To run |Fess|, OpenSearch must be started first.
This guide assumes |Fess| is installed in ``c:\opt\fess`` and OpenSearch in ``c:\opt\opensearch`` (adjust the paths to match your environment).

.. note::
   |Fess| and OpenSearch support 64-bit editions only.

Prerequisites
-------------

Set ``JAVA_HOME`` as a system environment variable. ``service.bat`` will exit with an error if ``JAVA_HOME`` is not set.

Registering OpenSearch as a Service
------------------------------------

Open a command prompt with administrator privileges and run ``c:\opt\opensearch\bin\opensearch-service.bat``.

::

    > cd c:\opt\opensearch\bin
    > opensearch-service.bat install
    ...
    The service 'opensearch-service-x64' has been installed.

For details, refer to the `OpenSearch documentation <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/windows/>`_.

|Fess| Configuration
---------------------

The service is registered via ``c:\opt\fess\bin\service.bat``. When registering, ``service.bat`` reads ``bin\fess.in.bat`` and applies its contents to the |Fess| startup options.
Add the settings required to connect to OpenSearch to ``c:\opt\fess\bin\fess.in.bat``.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.search_engine.http_address=http://localhost:9200
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.dictionary.path=c:/opt/opensearch/data/config/

.. note::
   - ``fess.search_engine.http_address`` specifies the connection target for the registered OpenSearch service. If this setting is omitted, |Fess| cannot locate the connection target and will start the embedded OpenSearch, which is not recommended for production environments.
   - If OpenSearch is running on a different host, change the hostname or IP address accordingly.
   - Use ``/`` as the path separator.

The default port number for the |Fess| search and administration screens is ``8080``. To change it to a different port, edit ``-Dfess.port`` in ``c:\opt\fess\bin\fess.in.bat``.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=80

.. note::
   When registering as a service, ``-Dfess.port=8080`` is also hardcoded in ``FESS_PARAMS`` inside ``bin\service.bat``. Because this value takes precedence over the settings in ``fess.in.bat``, also edit ``FESS_PARAMS`` in ``service.bat`` when changing the port.

Service Customization (Optional)
---------------------------------

You can change the service configuration by setting environment variables before running ``service.bat install``. The main environment variables are listed below.

.. list-table::
   :header-rows: 1

   * - Environment Variable
     - Description
   * - ``FESS_START_TYPE``
     - Startup type (``auto`` or ``manual``). Default is ``manual``.
   * - ``FESS_HEAP_SIZE``
     - Heap size (e.g. ``1g``). To specify minimum and maximum heap sizes individually, use ``FESS_MIN_MEM`` (default ``256m``) and ``FESS_MAX_MEM`` (default ``1g``).
   * - ``SERVICE_USERNAME`` / ``SERVICE_PASSWORD``
     - Windows account under which the service runs.
   * - ``SERVICE_DISPLAY_NAME``
     - Display name of the service.
   * - ``SERVICE_DESCRIPTION``
     - Description of the service.

Registration Procedure
----------------------

From a command prompt with administrator privileges, run ``c:\opt\fess\bin\service.bat``.

::

    > cd c:\opt\fess\bin
    > service.bat install
    ...
    The service 'fess-service-x64' has been installed.

Service Configuration
---------------------

If starting the service manually, start the OpenSearch service first and then start the |Fess| service.
To start automatically at system boot, configure the startup type and service dependencies.

1. In the service General settings, set the Startup type to "Automatic (Delayed Start)".
2. Configure service dependencies in the registry.

Add the following key and value in the Registry Editor (regedit).

.. list-table::

   * - *Key*
     - ``Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\fess-service-x64\DependOnService``
   * - *Value*
     - ``opensearch-service-x64``

Once added, opensearch-service-x64 will appear in the Dependencies tab of the |Fess| service properties.

.. note::
   Setting the environment variable ``FESS_START_TYPE=auto`` before running ``service.bat install`` registers the service with a startup type of "Automatic". However, "Automatic (Delayed Start)" and dependency configuration cannot be performed through ``service.bat``, so use the procedure described above for those settings.

Service Management
------------------

The following commands are available in ``service.bat`` to manage the service.

.. list-table::
   :header-rows: 1

   * - Command
     - Description
   * - ``service.bat install``
     - Registers the service.
   * - ``service.bat remove``
     - Removes the service.
   * - ``service.bat start``
     - Starts the service.
   * - ``service.bat stop``
     - Stops the service.
   * - ``service.bat manager``
     - Launches the GUI for managing the service.
