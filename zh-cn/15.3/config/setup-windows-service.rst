===================
注册为 Windows 服务
===================

注册为 Windows 服务
======================

可以将 |Fess| 注册为 Windows 服务。
要运行 |Fess|,需要先启动 OpenSearch。
本文档假设已将 |Fess| 安装在 ``c:\opt\fess``,OpenSearch 安装在 ``c:\opt\opensearch``。

准备工作
------

请将 JAVA_HOME 设置为系统环境变量。

将 OpenSearch 注册为服务
-------------------------

| 在命令提示符中以管理员身份执行 ``c:\opt\opensearch\bin\opensearch-service.bat``。

::

    > cd c:\opt\opensearch\bin
    > opensearch-service.bat install
    ...
    The service 'opensearch-service-x64' has been installed.

详情请参阅 `OpenSearch 文档 <https://opensearch.org/docs/2.4/install-and-configure/install-opensearch/windows/>`_。

配置
----

编辑 ``c:\opt\fess\bin\fess.in.bat`` 文件,在 SEARCH_ENGINE_HOME 中设置 OpenSearch 的安装路径。

::

    set SEARCH_ENGINE_HOME=c:/opt/opensearch

|Fess| 的搜索页面和管理页面的默认端口号为 8080。如需更改为 80 端口,请修改 ``c:\opt\fess\bin\fess.in.bat`` 中的 fess.port。

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=80


注册方法
------

在命令提示符中以管理员身份执行 ``c:\opt\fess\bin\service.bat``。

::

    > cd c:\opt\fess\bin
    > service.bat install
    ...
    The service 'fess-service-x64' has been installed.


服务配置
-----------

如需手动启动服务,请先启动 OpenSearch 服务,然后再启动 |Fess| 服务。
如需自动启动,请添加依赖关系。

1. 在服务的常规设置中,将启动类型设置为"自动(延迟启动)"。
2. 在注册表中配置服务依赖关系。

在注册表编辑器(regedit)中添加以下键和值。

.. list-table::

   * - *键*
     - ``计算机\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services \fess-service-x64\DependOnService``
   * - *值*
     - ``opensearch-service-x64``

添加后,opensearch-service-x64 将显示在 |Fess| 服务属性的依赖关系中。
