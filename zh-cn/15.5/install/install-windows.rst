====================================
在 Windows 上安装（详细步骤）
====================================

本页面说明在 Windows 环境中安装 |Fess| 的步骤。
介绍使用 ZIP 包的安装方法。

.. warning::

   在生产环境中，不推荐使用内嵌 OpenSearch 运行。
   请务必构建外部的 OpenSearch 服务器。

前提条件
========

- 满足 :doc:`prerequisites` 中描述的系统要求
- 已安装 Java 21
- OpenSearch 3.3.2 可用（或新安装）
- 已适当设置 Windows 环境变量 ``JAVA_HOME``

确认 Java 安装
====================

打开命令提示符或 PowerShell，使用以下命令确认 Java 版本。

命令提示符的情况::

    C:\> java -version

PowerShell 的情况::

    PS C:\> java -version

请确认显示 Java 21 或更高版本。

设置环境变量
============

1. 设置 ``JAVA_HOME`` 环境变量

   将 Java 的安装目录设置为 ``JAVA_HOME``。

   例::

       JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-21.0.1.12-hotspot

2. 添加到 ``PATH`` 环境变量

   将 ``%JAVA_HOME%\bin`` 添加到 ``PATH`` 环境变量。

.. tip::

   设置环境变量的方法：

   1. 从「开始」菜单打开「设置」
   2. 点击「系统」→「关于」→「系统高级设置」
   3. 点击「环境变量」按钮
   4. 在「系统环境变量」或「用户环境变量」中设置

步骤 1: 安装 OpenSearch
===================================

下载 OpenSearch
-----------------------

1. 从 `Download OpenSearch <https://opensearch.org/downloads.html>`__ 下载 Windows 用的 ZIP 包。

2. 将下载的 ZIP 文件解压到任意目录。

   例::

       C:\opensearch-3.3.2

   .. note::

      建议选择路径中不包含日文或空格的目录。

安装 OpenSearch 插件
---------------------------------

以**管理员权限**打开命令提示符，执行以下命令。

::

    C:\> cd C:\opensearch-3.3.2
    C:\opensearch-3.3.2> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.1
    C:\opensearch-3.3.2> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.1
    C:\opensearch-3.3.2> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.1
    C:\opensearch-3.3.2> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.1

.. important::

   插件版本必须与 OpenSearch 版本一致。
   在上述示例中，所有版本都指定为 3.3.2。

配置 OpenSearch
---------------

使用文本编辑器打开 ``config\opensearch.yml``，添加以下配置。

::

    # 配置同步路径（使用绝对路径指定）
    configsync.config_path: C:/opensearch-3.3.2/data/config/

    # 禁用安全插件（仅限开发环境）
    plugins.security.disabled: true

.. warning::

   **关于安全的重要注意事项**

   ``plugins.security.disabled: true`` 仅应在开发环境或测试环境中使用。
   在生产环境中，应启用 OpenSearch 的安全插件并进行适当的认证和授权配置。
   详情请参阅 :doc:`security`。

.. note::

   在 Windows 中，路径分隔符请使用 ``/`` 而不是 ``\``。
   应写为 ``C:/opensearch-3.3.2/data/config/`` 而不是 ``C:\opensearch-3.3.2\data\config\``。

.. tip::

   其他推荐配置::

       cluster.name: fess-cluster
       node.name: fess-node-1
       network.host: 0.0.0.0
       discovery.type: single-node

步骤 2: 安装 Fess
=============================

下载 Fess
-----------------

1. 从 `下载站点 <https://fess.codelibs.org/zh-cn/downloads.html>`__ 下载 Windows 用的 ZIP 包。

2. 将下载的 ZIP 文件解压到任意目录。

   例::

       C:\fess-15.5.0

   .. note::

      建议选择路径中不包含日文或空格的目录。

配置 Fess
----------

使用文本编辑器打开 ``bin\fess.in.bat``，添加或更改以下配置。

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.search_engine.http_address=http://localhost:9200
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.dictionary.path=C:/opensearch-3.3.2/data/config/

.. note::

   - 如果 OpenSearch 在其他主机上运行，请将 ``fess.search_engine.http_address`` 更改为适当的主机名或 IP 地址。
   - 路径分隔符请使用 ``/``。

确认安装
----------------

确认配置文件已正确编辑。

在命令提示符中::

    C:\> findstr "fess.search_engine.http_address" C:\fess-15.5.0\bin\fess.in.bat
    C:\> findstr "fess.dictionary.path" C:\fess-15.5.0\bin\fess.in.bat

步骤 3: 启动
==============

关于启动步骤，请参阅 :doc:`run`。

注册为 Windows 服务（可选）
=======================================

通过将 |Fess| 和 OpenSearch 注册为 Windows 服务，可以设置为系统启动时自动启动。

.. note::

   要注册为 Windows 服务，需要使用第三方工具（如 NSSM）。
   详细步骤请参阅各工具的文档。

使用 NSSM 的示例
----------------

1. 下载并解压 `NSSM (Non-Sucking Service Manager) <https://nssm.cc/download>`__。

2. 将 OpenSearch 注册为服务::

       C:\> nssm install OpenSearch C:\opensearch-3.3.2\bin\opensearch.bat

3. 将 Fess 注册为服务::

       C:\> nssm install Fess C:\fess-15.5.0\bin\fess.bat

4. 设置服务依赖关系（Fess 依赖于 OpenSearch）::

       C:\> sc config Fess depend= OpenSearch

5. 启动服务::

       C:\> net start OpenSearch
       C:\> net start Fess

防火墙设置
==================

在 Windows Defender 防火墙中开放必要的端口。

1. 打开「控制面板」→「Windows Defender 防火墙」→「高级设置」

2. 在「入站规则」中创建新规则

   - 规则类型: 端口
   - 协议和端口: TCP、8080
   - 操作: 允许连接
   - 名称: Fess Web Interface

或者，在 PowerShell 中执行::

    PS C:\> New-NetFirewallRule -DisplayName "Fess Web Interface" -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow

故障排除
====================

端口号冲突
--------------

如果端口 8080 或 9200 已被使用，可以使用以下命令确认::

    C:\> netstat -ano | findstr :8080
    C:\> netstat -ano | findstr :9200

请更改使用中的端口号或停止冲突的进程。

路径长度限制
------------

Windows 对路径长度有限制。建议安装到尽可能短的路径。

例::

    C:\opensearch  (推荐)
    C:\Program Files\opensearch-3.3.2  (不推荐 - 路径过长)

Java 未被识别
-----------------

如果 ``java -version`` 命令显示错误：

1. 确认 ``JAVA_HOME`` 环境变量是否正确设置
2. 确认 ``PATH`` 环境变量中是否包含 ``%JAVA_HOME%\bin``
3. 重启命令提示符以反映设置

下一步
==========

安装完成后，请参阅以下文档：

- :doc:`run` - |Fess| 的启动和初始设置
- :doc:`security` - 生产环境的安全配置
- :doc:`troubleshooting` - 故障排除

常见问题
==========

Q: 推荐在 Windows Server 上运行吗？
------------------------------------------

A: 可以在 Windows Server 上运行。
在 Windows Server 上运行时，请注册为 Windows 服务并设置适当的监控。

Q: 64 位版和 32 位版有什么区别？
------------------------------------

A: |Fess| 和 OpenSearch 仅支持 64 位版。
无法在 32 位版的 Windows 上运行。

Q: 路径包含日文时的处理方法？
--------------------------------------

A: 请尽可能安装到不包含日文或空格的路径。
如果必须使用日文路径，需要在配置文件中适当转义路径。
