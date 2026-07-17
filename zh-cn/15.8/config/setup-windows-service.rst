========================
注册为 Windows 服务
========================

注册为 Windows 服务
====================

可以将 |Fess| 注册为 Windows 服务。注册为服务后，可以在系统启动时自动启动 |Fess|\ 。
要运行 |Fess|，需要先启动 OpenSearch。
本文档假设已将 |Fess| 安装在 ``c:\opt\fess``，OpenSearch 安装在 ``c:\opt\opensearch``\ （请根据实际环境替换路径）。

.. note::
   |Fess| 和 OpenSearch 仅支持 64 位版本。

前期准备
--------

请将 ``JAVA_HOME`` 设置为系统环境变量。若未设置 ``JAVA_HOME``，``service.bat`` 将报错退出。

将 OpenSearch 注册为服务
------------------------

以管理员权限启动命令提示符，执行 ``c:\opt\opensearch\bin\opensearch-service.bat``\ 。

::

    > cd c:\opt\opensearch\bin
    > opensearch-service.bat install
    ...
    The service 'opensearch-service-x64' has been installed.

详情请参阅 `OpenSearch 文档 <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/windows/>`_\ 。

|Fess| 的配置
-------------

服务通过 ``c:\opt\fess\bin\service.bat`` 进行注册。\ ``service.bat`` 在注册时会读取 ``bin\fess.in.bat``，并将其内容反映到 |Fess| 的启动选项中。
请在 ``c:\opt\fess\bin\fess.in.bat`` 中添加连接 OpenSearch 的配置。

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.search_engine.http_address=http://localhost:9200
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.dictionary.path=c:/opt/opensearch/data/config/

.. note::
   - ``fess.search_engine.http_address`` 用于指定已注册的 OpenSearch 服务的连接地址。若不进行此配置，|Fess| 将无法找到连接目标，并会启动不推荐在生产环境中使用的内嵌版 OpenSearch。
   - 若 OpenSearch 运行在其他主机上，请将主机名或 IP 地址修改为适当的值。
   - 路径分隔符请使用 ``/``\ 。

|Fess| 搜索页面和管理页面的默认端口号为 ``8080``\ 。如需更改为其他端口，请编辑 ``c:\opt\fess\bin\fess.in.bat`` 中的 ``-Dfess.port``\ 。

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=80

.. note::
   注册为服务时，``bin\service.bat`` 中的 ``FESS_PARAMS`` 也硬编码了 ``-Dfess.port=8080``\ 。由于该值优先于 ``fess.in.bat`` 的配置，更改端口时请同样编辑 ``service.bat`` 中的 ``FESS_PARAMS``\ 。

服务自定义（可选）
------------------

在执行 ``service.bat install`` 之前设置环境变量，可以更改服务的配置。主要的环境变量如下。

.. list-table::
   :header-rows: 1

   * - 环境变量
     - 说明
   * - ``FESS_START_TYPE``
     - 启动类型（``auto`` 或 ``manual``）。默认为 ``manual``\ 。
   * - ``FESS_HEAP_SIZE``
     - 堆大小（例如：``1g``）。如需分别指定最小和最大堆大小，请使用 ``FESS_MIN_MEM``\ （默认 ``256m``）和 ``FESS_MAX_MEM``\ （默认 ``1g``）。
   * - ``SERVICE_USERNAME`` / ``SERVICE_PASSWORD``
     - 运行服务的 Windows 账户。
   * - ``SERVICE_DISPLAY_NAME``
     - 服务的显示名称。
   * - ``SERVICE_DESCRIPTION``
     - 服务的描述。

注册方法
--------

以管理员权限启动命令提示符，执行 ``c:\opt\fess\bin\service.bat``\ 。

::

    > cd c:\opt\fess\bin
    > service.bat install
    ...
    The service 'fess-service-x64' has been installed.

服务配置
--------

如需手动启动服务，请先启动 OpenSearch 服务，再启动 |Fess| 服务。
如需在系统启动时自动启动，请配置启动类型和依赖关系。

1. 在服务的常规设置中，将启动类型设置为"自动（延迟启动）"。
2. 在注册表中配置服务依赖关系。

在注册表编辑器（regedit）中添加以下键和值。

.. list-table::

   * - *键*
     - ``Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\fess-service-x64\DependOnService``
   * - *值*
     - ``opensearch-service-x64``

添加后，opensearch-service-x64 将显示在 |Fess| 服务属性的依赖关系中。

.. note::
   在执行 ``service.bat install`` 之前设置环境变量 ``FESS_START_TYPE=auto``，可以将启动类型注册为"自动"。但是，"自动（延迟启动）"和依赖关系的配置无法通过 ``service.bat`` 完成，请按照上述步骤进行设置。

服务管理
--------

使用 ``service.bat`` 可以通过以下命令操作服务。

.. list-table::
   :header-rows: 1

   * - 命令
     - 说明
   * - ``service.bat install``
     - 注册服务。
   * - ``service.bat remove``
     - 删除服务。
   * - ``service.bat start``
     - 启动服务。
   * - ``service.bat stop``
     - 停止服务。
   * - ``service.bat manager``
     - 启动服务管理 GUI。
