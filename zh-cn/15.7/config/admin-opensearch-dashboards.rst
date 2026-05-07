=======================
搜索日志可视化配置
=======================

关于搜索日志可视化
========================

|Fess| 获取用户的搜索日志和点击日志。
可以使用 `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/index/>`__ 对获取的搜索日志进行数据分析和可视化。

可视化的信息
----------------

在默认配置下,可以可视化以下信息。

-  搜索结果显示平均时间
-  每秒搜索次数
-  访问用户的 User Agent 排名
-  搜索关键词排名
-  搜索结果为0条的搜索关键词排名
-  搜索结果总数
-  时间序列搜索趋势

使用 Visualize 功能创建新图表并添加到 Dashboard,可以构建独特的监控仪表板。

OpenSearch Dashboards 数据可视化配置
==============================================

OpenSearch Dashboards 安装
------------------------------------

OpenSearch Dashboards 是用于可视化 |Fess| 使用的 OpenSearch 数据的工具。
请按照 `OpenSearch 官方文档 <https://opensearch.org/docs/latest/install-and-configure/install-dashboards/index/>`__ 安装 OpenSearch Dashboards。

编辑配置文件
------------------

为了让 OpenSearch Dashboards 识别 |Fess| 使用的 OpenSearch,请编辑配置文件 ``config/opensearch_dashboards.yml``。

::

    opensearch.hosts: ["http://localhost:9201"]

请根据环境将 ``localhost`` 更改为适当的主机名或IP地址。
|Fess| 的默认配置中,OpenSearch 在 9201 端口启动。

.. note::
   如 OpenSearch 端口号不同,请更改为适当的端口号。

启动 OpenSearch Dashboards
-----------------------------

编辑配置文件后,启动 OpenSearch Dashboards。

::

    $ cd /path/to/opensearch-dashboards
    $ ./bin/opensearch-dashboards

启动后,在浏览器中访问 ``http://localhost:5601``。

配置索引模式
--------------------------

1. 从 OpenSearch Dashboards 主页选择"Management"菜单。
2. 选择"Index Patterns"。
3. 点击"Create index pattern"按钮。
4. 在 Index pattern name 中输入 ``fess_log*``。
5. 点击"Next step"按钮。
6. 在 Time field 中选择 ``requestedAt``。
7. 点击"Create index pattern"按钮。

至此,可视化 |Fess| 搜索日志的准备工作完成。

创建可视化和仪表板
----------------------------

创建基本可视化
~~~~~~~~~~~~~~~~~~~~

1. 从左侧菜单选择"Visualize"。
2. 点击"Create visualization"按钮。
3. 选择可视化类型(折线图、饼图、柱状图等)。
4. 选择创建的索引模式 ``fess_log*``。
5. 设置所需的指标和存储桶(聚合单位)。
6. 点击"Save"按钮保存可视化。

创建仪表板
~~~~~~~~~~~~~~~~~~~~

1. 从左侧菜单选择"Dashboard"。
2. 点击"Create dashboard"按钮。
3. 点击"Add"按钮,添加创建的可视化。
4. 调整布局,点击"Save"按钮保存。

时区配置
------------------

如时间显示不正确,请配置时区。

1. 从左侧菜单选择"Management"。
2. 选择"Advanced Settings"。
3. 搜索 ``dateFormat:tz``。
4. 将时区设置为适当的值(例: ``Asia/Tokyo`` 或 ``UTC``)。
5. 点击"Save"按钮。

确认日志数据
----------------

1. 从左侧菜单选择"Discover"。
2. 选择索引模式 ``fess_log*``。
3. 将显示搜索日志数据。
4. 可在右上角的时间范围选择中指定显示期间。

主要搜索日志字段
----------------------

|Fess| 的搜索日志包含以下信息。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 字段名
     - 说明
   * - ``queryId``
     - 搜索查询的唯一标识符
   * - ``searchWord``
     - 搜索关键词
   * - ``requestedAt``
     - 执行搜索的日期时间
   * - ``responseTime``
     - 搜索结果响应时间(毫秒)
   * - ``queryTime``
     - 查询执行时间(毫秒)
   * - ``hitCount``
     - 搜索结果命中数
   * - ``userAgent``
     - 用户的浏览器信息
   * - ``clientIp``
     - 客户端IP地址
   * - ``languages``
     - 使用语言
   * - ``roles``
     - 用户角色信息
   * - ``user``
     - 用户名(登录时)

利用这些字段,可以从各个角度分析搜索日志。

故障排除
----------------------

数据未显示
~~~~~~~~~~~~~~~~~~~~~~~~

- 请确认 OpenSearch 是否正确启动。
- 请确认 ``opensearch_dashboards.yml`` 的 ``opensearch.hosts`` 配置是否正确。
- 请确认在 |Fess| 中是否执行了搜索并记录了日志。
- 请确认索引模式的时间范围是否适当设置。

发生连接错误
~~~~~~~~~~~~~~~~~~~~~~~~

- 请确认 OpenSearch 的端口号是否正确。
- 请确认防火墙和安全组的配置。
- 请在 OpenSearch 日志文件中确认是否有错误。
