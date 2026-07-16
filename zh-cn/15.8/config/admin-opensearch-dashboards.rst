=======================
搜索日志可视化配置
=======================

关于搜索日志可视化
========================

|Fess| 获取用户的搜索日志和点击日志。
可以使用 `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/index/>`__ 对获取的搜索日志进行数据分析和可视化。

|Fess| 内附了用于可视化搜索日志的仪表板定义文件 ``extension/kibana/fess_log.ndjson``\ 。
将该文件导入 OpenSearch Dashboards 后，即可立即使用预先准备好的仪表板。

可以可视化的信息
----------------

导入内附的仪表板定义 (``fess_log.ndjson``) 后，将注册 ``fess_log`` 仪表板以及以下6个可视化图表。

-  搜索结果显示的平均响应时间 (``average-response-time``)
-  单位时间内的搜索请求数 (``search-query-counts-per-sec``)
-  访问用户的 User Agent 排名 (``rank-of-UserAgent``)
-  搜索关键词排名 (``search-term-rank``)
-  搜索结果为0条的搜索关键词排名 (``search-term-rank-of-no-results``)
-  搜索结果的平均命中数 (``hit-counts``)

除此之外，还可以使用 Visualize 功能创建新图表并添加到仪表板，从而构建独特的监控仪表板。

OpenSearch Dashboards 数据可视化配置
==============================================

OpenSearch Dashboards 安装
------------------------------------

OpenSearch Dashboards 是用于可视化 |Fess| 所使用的 OpenSearch 数据的工具。
请按照 `OpenSearch 官方文档 <https://opensearch.org/docs/latest/install-and-configure/install-dashboards/index/>`__ 安装 OpenSearch Dashboards。

编辑配置文件
------------------

为了让 OpenSearch Dashboards 识别 |Fess| 使用的 OpenSearch，请编辑配置文件 ``config/opensearch_dashboards.yml``\ 。

::

    opensearch.hosts: ["http://localhost:9201"]

请根据环境将 ``localhost`` 更改为适当的主机名或IP地址。
|Fess| 的默认配置中，OpenSearch 在 9201 端口启动。

.. note::
   如 OpenSearch 端口号不同，请更改为适当的端口号。

启动 OpenSearch Dashboards
-----------------------------

编辑配置文件后，启动 OpenSearch Dashboards。

::

    $ cd /path/to/opensearch-dashboards
    $ ./bin/opensearch-dashboards

启动后，在浏览器中访问 ``http://localhost:5601``\ 。

配置索引模式
--------------------------

创建用于可视化搜索日志的索引模式。

1. 从左侧菜单选择「Management」（根据 OpenSearch Dashboards 版本，可能显示为「Dashboards Management」）。
2. 选择「Index Patterns」。
3. 点击「Create index pattern」按钮。
4. 在 Index pattern name 中输入 ``fess_log*``\ 。
5. 点击「Next step」按钮。
6. 在 Time field 中选择 ``requestedAt``\ 。
7. 点击「Create index pattern」按钮。

.. note::
   |Fess| 的搜索日志记录在以 ``fess_log`` 开头的多个索引中，例如 ``fess_log.search_log``、``fess_log.click_log`` 等。
   指定 ``fess_log*`` 索引模式后，可以将这些索引统一作为目标。

导入仪表板定义
------------------------------

通过导入 |Fess| 内附的仪表板定义，即可使用预先准备好的可视化图表和仪表板。

1. 从左侧菜单选择「Management」（根据 OpenSearch Dashboards 版本，可能显示为「Dashboards Management」）。
2. 选择「Saved Objects」。
3. 点击「Import」。
4. 选择 |Fess| 安装目录中的 ``extension/kibana/fess_log.ndjson``\ 。
5. 点击「Import」执行导入。

导入完成后，将注册6个可视化图表和 ``fess_log`` 仪表板。

显示仪表板
--------------------

1. 从左侧菜单选择「Dashboard」。
2. 选择 ``fess_log`` 仪表板。
3. 将显示搜索日志的可视化结果。
4. 可在右上角的时间范围选择中指定显示期间。

创建自定义可视化
------------------

除内附的仪表板外，还可以创建自定义可视化图表和仪表板。

创建可视化图表
~~~~~~~~~~~~~~~~~~~~

1. 从左侧菜单选择「Visualize」。
2. 点击「Create visualization」按钮。
3. 选择可视化类型（折线图、饼图、柱状图等）。
4. 选择创建的索引模式 ``fess_log*``\ 。
5. 设置所需的指标和存储桶（聚合单位）。
6. 点击「Save」按钮保存可视化图表。

创建仪表板
~~~~~~~~~~~~~~~~~~~~

1. 从左侧菜单选择「Dashboard」。
2. 点击「Create dashboard」按钮。
3. 点击「Add」按钮，添加创建的可视化图表。
4. 调整布局，点击「Save」按钮保存。

时区配置
------------------

如时间显示不正确，请配置时区。

1. 从左侧菜单选择「Management」（根据 OpenSearch Dashboards 版本，可能显示为「Dashboards Management」）。
2. 选择「Advanced Settings」。
3. 搜索 ``dateFormat:tz``\ 。
4. 将时区设置为适当的值（例：``Asia/Tokyo`` 或 ``UTC``）。
5. 点击「Save」按钮。

确认日志数据
----------------

1. 从左侧菜单选择「Discover」。
2. 选择索引模式 ``fess_log*``\ 。
3. 将显示搜索日志数据。
4. 可在右上角的时间范围选择中指定显示期间。

主要搜索日志字段
----------------------

|Fess| 的搜索日志 (``fess_log.search_log``) 包含以下信息。

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
     - 搜索处理整体的响应时间（毫秒）
   * - ``queryTime``
     - 对搜索引擎的查询执行时间（毫秒）
   * - ``hitCount``
     - 搜索结果命中数
   * - ``hitCountRelation``
     - 表示命中数是精确值还是下限值的关系（``eq``：精确数量，``gte``：指定值以上）
   * - ``queryOffset``
     - 搜索结果的获取起始位置
   * - ``queryPageSize``
     - 每页显示件数
   * - ``userAgent``
     - 用户的浏览器信息
   * - ``referer``
     - 执行搜索的页面来源URL
   * - ``clientIp``
     - 客户端IP地址
   * - ``languages``
     - 请求使用的语言
   * - ``accessType``
     - 访问类型（``web``、``json``、``gsa``、``admin``、``other``）
   * - ``roles``
     - 用户的角色信息
   * - ``user``
     - 用户名（登录时）
   * - ``virtualHost``
     - 虚拟主机名（已配置时）

利用这些字段，可以从各种角度分析搜索日志。

故障排除
----------------------

数据未显示
~~~~~~~~~~~~~~~~~~~~~~~~

- 请确认 OpenSearch 是否正确启动。
- 请确认 ``opensearch_dashboards.yml`` 的 ``opensearch.hosts`` 配置是否正确。
- 请确认在 |Fess| 中是否执行了搜索并记录了日志。
- 请确认右上角的时间范围是否包含记录日志的期间。
- 如时间显示有偏差，请确认 ``dateFormat:tz`` 的配置。

发生连接错误
~~~~~~~~~~~~~~~~~~~~~~~~

- 请确认 OpenSearch 的端口号是否正确。
- 请确认防火墙和安全组的配置。
- 请在 OpenSearch 日志文件中确认是否有错误。
