==================================
数据存储连接器概述
==================================

概述
====

|Fess| 的数据存储连接器提供从网站和文件系统以外的数据源
获取内容并建立索引的功能。

使用数据存储连接器，可以使以下来源的数据变得可搜索：

- 云存储（Box、Dropbox、Google Drive、OneDrive）
- 协作工具（Confluence、Jira、Slack）
- 数据库（MySQL、PostgreSQL、Oracle等）
- 其他系统（Git、Salesforce、Elasticsearch等）

可用的连接器
==================

|Fess| 提供支持多种数据源的连接器。
许多连接器以插件形式提供，可根据需要安装。

云存储
------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - 连接器
     - 插件
     - 说明
   * - :doc:`ds-box`
     - fess-ds-box
     - 抓取Box.com的文件和文件夹
   * - :doc:`ds-dropbox`
     - fess-ds-dropbox
     - 抓取Dropbox的文件和文件夹
   * - :doc:`ds-gsuite`
     - fess-ds-gsuite
     - 抓取Google Drive、Gmail等
   * - :doc:`ds-microsoft365`
     - fess-ds-office365
     - 抓取OneDrive、SharePoint等

协作工具
----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - 连接器
     - 插件
     - 说明
   * - :doc:`ds-atlassian`
     - fess-ds-atlassian
     - 抓取Confluence、Jira
   * - :doc:`ds-slack`
     - fess-ds-slack
     - 抓取Slack的消息和文件

开发运维工具
----------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - 连接器
     - 插件
     - 说明
   * - :doc:`ds-git`
     - fess-ds-git
     - 抓取Git仓库的源代码
   * - :doc:`ds-elasticsearch`
     - fess-ds-elasticsearch
     - 从Elasticsearch/OpenSearch获取数据
   * - :doc:`ds-salesforce`
     - fess-ds-salesforce
     - 抓取Salesforce对象

数据库和文件
----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - 连接器
     - 插件
     - 说明
   * - :doc:`ds-database`
     - （内置）
     - 从JDBC兼容数据库获取数据
   * - :doc:`ds-csv`
     - fess-ds-csv
     - 从CSV文件获取数据
   * - :doc:`ds-json`
     - fess-ds-json
     - 从JSON文件获取数据

连接器安装
======================

插件安装
------------------------

数据存储连接器插件可以通过管理界面或 `plugin` 命令安装。

从管理界面安装
~~~~~~~~~~~~

1. 登录管理界面
2. 进入"系统"→"插件"
3. 在"Available"标签页搜索目标插件
4. 点击"安装"
5. 重启 |Fess|

命令行安装
~~~~~~~~~~~~~~

::

    # 安装插件
    ./bin/fess-plugin install fess-ds-box

    # 确认已安装的插件
    ./bin/fess-plugin list

Docker环境
~~~~~~~~~~

::

    # 启动时安装插件
    docker run -e FESS_PLUGINS="fess-ds-box,fess-ds-dropbox" codelibs/fess:15.5.0

数据存储设置基础
======================

数据存储连接器的配置在管理界面的"爬虫"→"数据存储"中进行。

通用设置项
------------

所有数据存储连接器共通的设置项：

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 项目
     - 说明
   * - 名称
     - 设置的标识名
   * - 处理器名
     - 使用的连接器处理器名（例如：``BoxDataStore``）
   * - 参数
     - 连接器特定的设置参数（key=value格式）
   * - 脚本
     - 索引字段映射脚本
   * - 权重
     - 搜索结果的优先级
   * - 启用
     - 是否启用此设置

参数设置
----------------

参数以换行分隔的 ``key=value`` 格式指定：

::

    api.key=xxxxxxxxxxxxx
    folder.id=0
    max.depth=3

脚本设置
--------------

脚本将获取的数据映射到 |Fess| 的索引字段：

::

    url=data.url
    title=data.name
    content=data.content
    mimetype=data.mimetype
    filetype=data.filetype
    filename=data.filename
    created=data.created
    lastModified=data.lastModified
    contentLength=data.contentLength

认证设置
========

许多数据存储连接器需要OAuth 2.0或API密钥认证。

OAuth 2.0认证
-------------

常见的OAuth 2.0设置参数：

::

    client.id=客户端ID
    client.secret=客户端密钥
    refresh.token=刷新令牌

或者：

::

    access.token=访问令牌

API密钥认证
-----------

::

    api.key=API密钥
    api.secret=API密钥

服务账户认证
----------------------

::

    service.account.email=服务账户的电子邮件地址
    service.account.key=私钥（JSON格式或密钥文件路径）

性能调优
==========================

处理大量数据时的设置：

::

    # 批处理大小
    batch.size=100

    # 请求间的等待时间（毫秒）
    interval=1000

    # 并行处理数
    thread.size=1

    # 超时（毫秒）
    timeout=30000

故障排除
======================

连接器不显示
----------------------

1. 确认插件是否正确安装
2. 重启 |Fess|
3. 检查日志是否有错误

认证错误
----------

1. 确认认证信息是否正确
2. 确认令牌的有效期
3. 确认是否授予了必要的权限
4. 确认服务端是否允许API访问

无法获取数据
--------------------

1. 确认参数格式是否正确
2. 确认对目标文件夹/文件的访问权限
3. 确认过滤器设置
4. 检查日志中的详细错误消息

调试设置
------------

调查问题时，调整日志级别：

``app/WEB-INF/classes/log4j2.xml``：

::

    <Logger name="org.codelibs.fess.ds" level="DEBUG"/>

参考信息
========

- :doc:`../../admin/dataconfig-guide` - 数据存储设置指南
- :doc:`../../admin/plugin-guide` - 插件管理指南
- :doc:`../api/admin/api-admin-dataconfig` - 数据存储设置API
