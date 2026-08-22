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
     - 爬取 Google Drive
   * - :doc:`ds-microsoft365`
     - fess-ds-microsoft365
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
     - fess-ds-db
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

数据存储连接器插件可以通过管理界面安装。

从管理界面安装
~~~~~~~~~~~~

1. 登录管理界面
2. 进入"系统"→"插件"
3. 点击"安装"按钮
4. 在"远程"选项卡中选择要安装的插件（或在"本地"选项卡上传 JAR 文件）
5. 点击"安装"
6. 重启 |Fess|

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
   * - 描述
     - 设置的说明文本
   * - 处理器名
     - 使用的连接器处理器名（例如：``CsvDataStore``）
   * - 参数
     - 连接器特定的设置参数（key=value格式）
   * - 脚本
     - 索引字段映射脚本
   * - 权重
     - 搜索结果的优先级
   * - 权限
     - 从此数据存储获取的文档的访问权限
   * - 虚拟主机
     - 应用此设置的虚拟主机
   * - 显示顺序
     - 在设置列表中的显示顺序
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

脚本将获取的数据映射到 |Fess| 的索引字段。
左侧为 |Fess| 的索引字段，右侧为从连接器获取的字段。

以下是 CSV 连接器（头部列名为 ``link`` 、 ``subject`` 、 ``body`` ）的示例：

::

    url=link
    title=subject
    content=body

.. note::

   脚本中可引用的字段名因连接器而异。
   Box/Dropbox/Google Drive/OneDrive 使用 ``file.*`` 前缀引用获取的对象；Slack 使用 ``message.*`` ；Jira 使用 ``issue.*`` 。
   而 CSV、JSON 和数据库连接器不使用前缀，直接引用字段名：

   - CSV：头部行的列名（ ``has_header_line=true`` 时），或 ``cell1`` 、 ``cell2`` ...（从 1 开始的列索引）；此外还可使用 ``csvfile`` 和 ``csvfilename`` 。
   - JSON：JSON 对象的字段名。
   - 数据库：SELECT 结果的列名（别名）。

   各连接器的详细信息请参阅各自的文档。

认证设置
========

许多数据存储连接器需要OAuth 2.0、API密钥、服务账户等方式进行认证。

认证参数因连接器而异。
各连接器的认证设置详情请参阅各自的文档。

通用参数
================

所有数据存储连接器可使用的通用参数：

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - 参数
     - 默认值
     - 说明
   * - ``readInterval``
     - ``0``
     - 各记录处理间的等待时间（毫秒）。在处理大量数据时，用于减轻服务器负载。
   * - ``script_type``
     - ``groovy``
     - 用于索引字段映射的脚本引擎类型。默认仅提供 ``groovy`` 。

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

调查问题时，调整日志级别。数据存储的抓取在爬虫进程中执行，因此需要编辑爬虫用的日志配置文件：

``app/WEB-INF/env/crawler/resources/log4j2.xml``：

::

    <Logger name="org.codelibs.fess.ds" level="DEBUG"/>

参考信息
========

- :doc:`../../admin/dataconfig-guide` - 数据存储设置指南
- :doc:`../../admin/plugin-guide` - 插件管理指南
- :doc:`../../api/admin/api-admin-dataconfig` - 数据存储设置API
