============================
Register for Windows Service
============================

Registering as a Windows Service
================================

You can register |Fess| as a Windows service. To run |Fess|, you need to have OpenSearch running. In this guide, we assume that |Fess| is installed in ``c:\opt\fess`` and OpenSearch is installed in ``c:\opt\opensearch``.

Preparations
------------

Please set the JAVA_HOME environment variable in your system.

Registering OpenSearch as a Service
-----------------------------------

From a command prompt, run ``c:\opt\fess\bin\service.bat`` as administrator.

::

    > cd c:\opt\opensearch\bin
    > opensearch-service.bat install
    ...
    The service 'opensearch-service-x64' has been installed.

For more details, refer to the `OpenSearch documentation <https://opensearch.org/docs/2.4/install-and-configure/install-opensearch/windows/>`_.

Configuration
-------------

Edit ``c:\opt\fess\bin\fess.in.bat`` and set SEARCH_ENGINE_HOME to the installation path of OpenSearch.

::

    set SEARCH_ENGINE_HOME=c:/opt/opensearch

The default port for |Fess| search and administration interfaces is 8080. If you want to change it to port 80, modify the fess.port in ``c:\opt\fess\bin\fess.in.bat``.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=80

Registration
------------

From a command prompt, run ``c:\opt\fess\bin\service.bat`` as administrator.

::

    > cd c:\opt\fess\bin
    > service.bat install
    ...
    The service 'fess-service-x64' has been installed.

Service Configuration
---------------------

If you want to start the service manually, first start the OpenSearch service, and then start the |Fess| service. If you want it to start automatically, add dependencies.

1. Set the startup type to "Automatic (Delayed Start)" in the service's general settings.
2. Configure the service dependencies in the registry.

In the Registry Editor (regedit), add the following key and value:

.. list-table::

   * - *Key*
     - ``Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services \fess-service-x64\DependOnService``
   * - *Value*
     - ``opensearch-service-x64``

After adding this, opensearch-service-x64 will be listed as a dependency in the properties of the |Fess| service.
