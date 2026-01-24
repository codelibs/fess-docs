=============================
Windows Service Registration
=============================

Registering as a Windows Service
=================================

You can register |Fess| as a Windows service.
To run |Fess|, OpenSearch must be started first.
This guide assumes |Fess| is installed in ``c:\opt\fess`` and OpenSearch in ``c:\opt\opensearch``.

Prerequisites
-------------

Set JAVA_HOME as a system environment variable.

Registering OpenSearch as a Service
------------------------------------

From the command prompt, run ``c:\opt\opensearch\bin\opensearch-service.bat`` as administrator.

::

    > cd c:\opt\opensearch\bin
    > opensearch-service.bat install
    ...
    The service 'opensearch-service-x64' has been installed.

For details, refer to the `OpenSearch documentation <https://opensearch.org/docs/2.4/install-and-configure/install-opensearch/windows/>`_.

Configuration
-------------

Edit ``c:\opt\fess\bin\fess.in.bat`` and set the OpenSearch installation path in SEARCH_ENGINE_HOME.

::

    set SEARCH_ENGINE_HOME=c:/opt/opensearch

The default port number for |Fess| search and administration screens is 8080. To change it to port 80, modify fess.port in ``c:\opt\fess\bin\fess.in.bat``.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=80


Registration Procedure
----------------------

From the command prompt, run ``c:\opt\fess\bin\service.bat`` as administrator.

::

    > cd c:\opt\fess\bin
    > service.bat install
    ...
    The service 'fess-service-x64' has been installed.


Service Configuration
---------------------

If manually starting the service, start the OpenSearch service first, then start the |Fess| service.
For automatic startup, add service dependencies.

1. In the service General settings, set the Startup type to "Automatic (Delayed Start)".
2. Configure service dependencies in the registry.

Add the following key and value in the Registry Editor (regedit).

.. list-table::

   * - *Key*
     - ``Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\fess-service-x64\DependOnService``
   * - *Value*
     - ``opensearch-service-x64``

Once added, opensearch-service-x64 will appear in the |Fess| service properties dependencies.
