===========================================
使用 OpenSearch Dashboards 深入分析搜索日志
===========================================

前言
====

在 Fess 15.9 中，可以在管理页面的 [系统信息] > [搜索日志] 中查看零结果率、点击率、点击位置分布、响应时间、按星期和时段统计的搜索次数，以及按角色和组统计的搜索次数。
各个表格都可以下载为 CSV。
找出有问题的搜索词并用同义词或关键词匹配加以改进的流程，请参见 :doc:`guide-08`。

不过，该页面无法进行以下统计：

- 超过 366 天的期间内的趋势（页面中「自定义」期间最长为 366 天）
- 按角色或按标签查看哪些词出现零结果
- 每个搜索词实际打开了哪些 URL
- 按自己选定的维度排列图表的仪表板

搜索日志和点击日志保存在 OpenSearch 的索引中，因此可以直接在 OpenSearch Dashboards 中进行统计。
本文将使用 docker-fess 的 Compose 文件启动 OpenSearch Dashboards，导入 Fess 自带的仪表板，确认日志字段，然后完成上述 4 种统计。

开始之前：访问限制
==================

docker-fess 中的 OpenSearch Dashboards 与 OpenSearch 一样，采用移除了安全插件的配置。
能够访问端口 5601 的任何人，都可以在不登录的情况下读取搜索日志的所有字段（用户 ID、IP 地址等）。
此外，还可以通过 Dev Tools 修改或删除包括 Fess 用户和设置索引在内的所有索引。

因此，请确保只有管理员的终端能够访问端口 5601（以及 9200）。
如果希望向管理员以外的人展示搜索日志的统计结果，请不要公开 OpenSearch Dashboards，而是在 Fess 的 [用户] > [角色] 中创建名为 ``admin-searchlog-view`` 的角色，并将其分配给这些人。
拥有该角色可以查看 [系统信息] > [搜索日志]，但不能删除日志。

启动 OpenSearch Dashboards
==========================

在按照 :doc:`guide-02` 的步骤放置了 ``compose.yaml`` 和 ``compose-opensearch3.yaml`` 的目录中，添加 Dashboards 所需的文件。
``compose-dashboards3.yaml`` 会根据 ``dashboards/`` 目录中的 Dockerfile 构建镜像，因此需要 3 个文件。

::

    $ cd fess-docker
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-dashboards3.yaml
    $ mkdir dashboards
    $ curl -L -o dashboards/Dockerfile https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/dashboards/Dockerfile
    $ curl -L -o dashboards/opensearch_dashboards.yml https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/dashboards/opensearch_dashboards.yml

指定 3 个 Compose 文件启动。

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-dashboards3.yaml up -d

首次 ``up`` 时，会基于 ``opensearch-dashboards:3.9.0`` 构建一个移除了 ``securityDashboards`` 插件的镜像。
容器在网络 ``search_net`` 上连接到 ``OPENSEARCH_HOSTS='["http://search01:9200"]'``，并公开端口 5601。

在浏览器中打开 ``http://localhost:5601``，如果显示主页，说明已经启动。
停止或查看状态时，也请用 ``-f`` 指定这 3 个文件。
仪表板等已保存对象存放在 OpenSearch 的 ``.kibana`` 索引中，因此如果用 ``down -v`` 删除卷，它们也会一并被删除。

导入自带的仪表板
================

Fess 自带用于搜索日志的仪表板定义 ``fess_log.ndjson``。
使用 Docker 时，从容器中取出该文件。
ZIP 版位于解压后目录中的 ``extension/kibana/fess_log.ndjson``。

::

    $ docker cp fess01:/usr/share/fess/extension/kibana/fess_log.ndjson .

也可以从 GitHub 的 ``https://raw.githubusercontent.com/codelibs/fess/fess-15.9.0/src/main/assemblies/extension/kibana/fess_log.ndjson`` 获取同一文件。

1. 打开左侧菜单中的 [Dashboards Management]，选择 [Saved objects]
2. 点击 [Import]，选择 ``fess_log.ndjson`` 并导入
3. 从左侧菜单的 [Dashboards] 中打开 ``fess_log`` 仪表板

导入后，会注册索引模式 ``fess_log*``\ （时间字段为 ``requestedAt``）、6 个可视化以及 ``fess_log`` 仪表板。
由于其中包含索引模式，因此无需事先手动创建 ``fess_log*``。
如果手动创建后再导入，就会出现 2 个同名的模式。

注意自带仪表板的计数方式
------------------------

``fess_log*`` 涵盖所有以 ``fess_log`` 开头的索引，而自带的可视化没有按索引进行筛选。
15.9 的点击日志中包含搜索词（``searchWord``）和 ``requestedAt``，因此例如“search-term-rank”中的件数是搜索次数与点击次数的合计。
如果使用 AI搜索模式，聊天日志（``fess_log.chat_log``）也会混入件数和响应时间中。

如果只想统计搜索，请先在仪表板顶部的搜索栏中输入以下条件，然后再查看。

::

    _index : "fess_log.search_log"

另外，``fess_log*`` 中保存的字段列表来自旧版本，不包含 ``rank`` 等新字段。
自行创建统计时，请使用下一节中的索引模式。

创建用于统计的索引模式
======================

将搜索日志和点击日志分别设为不同的索引模式，就不必担心二者混在一起，并且可以选择当前所有字段。

1. 在 [Dashboards Management] > [Index patterns] 中点击 [Create index pattern]
2. 在「Index pattern name」中输入 ``fess_log.search_log``，然后点击 [Next step]
3. 在「Time field」中选择 ``requestedAt``，然后点击 [Create index pattern]
4. 按同样的步骤创建 ``fess_log.click_log``\ （时间字段为 ``requestedAt``）

之后如果字段有所增加（例如首次记录了用标签筛选的搜索时），请在索引模式页面中点击 [Refresh field list]。

时间的处理
----------

Fess 以 UTC 保存日期和时间。
OpenSearch Dashboards 默认以浏览器的时区显示，按天划分也遵循该时区。
如果希望以其他时区查看，请将 [Dashboards Management] > [Advanced settings] 中的 ``dateFormat:tz`` 改为您所在的时区，例如 ``Asia/Tokyo``。

Fess 的 [搜索日志] 页面按服务器的时区划分日期。
docker-fess 的容器默认使用 UTC，因此在两边核对每日数字时，可能会因日期划分不同而产生偏差。

日志字段
========

搜索日志（``fess_log.search_log``）每次搜索记录 1 条。
统计时常用的字段如下。

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 类型
     - 内容
   * - ``queryId``
     - keyword
     - 每次搜索的 ID。与点击日志中的 ``queryId`` 对应
   * - ``searchWord``
     - keyword
     - 搜索词。在用标签筛选的搜索中，还会像 ``申请 label:"hr"`` 这样包含条件
   * - ``searchField.*``
     - keyword
     - 按字段拆分后的搜索词。普通的词存入 ``searchField._default``，标签筛选条件存入 ``searchField.label``
   * - ``requestedAt``
     - date
     - 搜索的日期时间（以 UTC 保存）
   * - ``hitCount``
     - long
     - 命中件数。``0`` 表示零结果
   * - ``responseTime`` / ``queryTime``
     - long
     - 整个搜索的处理时间，以及在 OpenSearch 中的搜索时间（毫秒）
   * - ``queryOffset`` / ``queryPageSize``
     - integer
     - 获取的起始位置和每页件数。从第 2 页起，``queryOffset`` 大于 0
   * - ``accessType``
     - keyword
     - ``json``、``gsa``、``admin``、``other``、``web`` 之一。标准主题的搜索页面调用 ``/api/v2/search``，因此为 ``json``；从管理页面的 [系统信息] > [搜索] 进行的搜索为 ``admin``
   * - ``user`` / ``roles``
     - keyword
     - 登录用户的 ID，以及搜索时使用的角色列表。``roles`` 的值以首字符表示类型：``R`` 为角色，``2`` 为组，``1`` 为用户（例：``Rguest``）
   * - ``userSessionId`` / ``clientIp`` / ``userAgent`` / ``referer`` / ``virtualHost``
     - keyword
     - 识别用户的 Cookie 值、IP 地址、浏览器、来源页面、虚拟主机

点击日志（``fess_log.click_log``）在通过 ``/go/`` 打开搜索结果中的链接时记录。
但是，如果浏览器没有 Fess 的会话（未发送有效的会话 Cookie），该请求不会被记录。

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 类型
     - 内容
   * - ``queryId``
     - keyword
     - 点击来源搜索的 ``queryId``
   * - ``url`` / ``docId``
     - keyword
     - 被打开文档的 URL 和文档 ID
   * - ``rank``
     - integer
     - 在全部搜索结果中的排名（第 1 名为 1）。第 2 页的第 1 条为 11
   * - ``order``
     - integer
     - 在页面内的位置（第一个为 0）。统计排名时请使用 ``rank``
   * - ``searchWord`` / ``accessType``
     - keyword
     - 从点击来源搜索复制的搜索词和访问类型。无需与搜索日志关联，即可按搜索词进行统计
   * - ``requestedAt`` / ``queryRequestedAt``
     - date
     - 点击的日期时间，以及点击来源搜索的日期时间

``searchWord``、``accessType``、``rank`` 从 15.9 起才会写入点击日志。
在此之前记录的点击中没有这些字段。

统计示例
========

这里将完成开头列出的 4 种“页面上无法完成的统计”。
第 1 种使用 Visualize 创建，其余的从左侧菜单的 [Dev Tools] 中通过搜索 API 执行。

每个搜索词打开的 URL
--------------------

将每个搜索词下哪些文档在第几名被打开整理成表格。
可用于挑选关键词匹配或文档提升的候选项。

1. 在左侧菜单的 [Visualize] 中点击 [Create visualization]，选择「Data Table」
2. 数据源选择 ``fess_log.click_log``
3. 用 Metrics 的 [Add] 添加 Metric，在「Aggregation」中选择「Average」，在「Field」中选择 ``rank``
4. 在 Buckets 的 [Add] > [Split rows] 中，将「Aggregation」设为「Terms」，「Field」设为 ``searchWord``，「Size」设为 20
5. 再添加一个 [Split rows]，选择「Terms」，将「Field」设为 ``url``，「Size」设为 5
6. 点击 [Update]，在右上角选择期间后保存

平均排名较大的组合，是用户一直往下翻才打开的文档。

按角色统计的零结果查询词
------------------------

如果按部门划分了角色，可以确认哪个部门的搜索中有哪些内容没有找到。

.. code-block:: text

    GET fess_log.search_log/_search
    {
      "size": 0,
      "query": {
        "bool": {
          "filter": [
            { "term": { "hitCount": 0 } },
            { "range": { "requestedAt": { "gte": "now-90d/d" } } }
          ]
        }
      },
      "aggs": {
        "roles": {
          "terms": { "field": "roles", "size": 20, "exclude": "1.*" },
          "aggs": {
            "words": { "terms": { "field": "searchWord", "size": 10 } }
          }
        }
      }
    }

通过 ``exclude`` 排除以 ``1`` 开头的值（单个用户），只列出角色和组。
一次搜索会计入该用户的所有角色和组。
未登录的搜索计入 ``Rguest``。

按标签统计的搜索次数和零结果次数
--------------------------------

按标签统计在搜索页面中选择标签进行搜索的次数，以及其中零结果的次数。

.. code-block:: text

    GET fess_log.search_log/_search
    {
      "size": 0,
      "query": { "range": { "requestedAt": { "gte": "now-90d/d" } } },
      "aggs": {
        "labels": {
          "terms": { "field": "searchField.label", "size": 20 },
          "aggs": {
            "zero_hit": { "filter": { "term": { "hitCount": 0 } } }
          }
        }
      }
    }

如果尚未记录任何用标签筛选的搜索，``searchField.label`` 字段还不存在，因此 ``labels`` 的桶为空。

每月零结果率（2 年）
--------------------

超出页面的期间上限，查看零结果率（比率而非件数）的长期趋势。

.. code-block:: text

    GET fess_log.search_log/_search
    {
      "size": 0,
      "query": {
        "bool": {
          "filter": [ { "range": { "requestedAt": { "gte": "now-2y/d" } } } ],
          "must_not": [ { "term": { "accessType": "admin" } } ]
        }
      },
      "aggs": {
        "per_month": {
          "date_histogram": {
            "field": "requestedAt",
            "calendar_interval": "month",
            "time_zone": "Asia/Tokyo"
          },
          "aggs": {
            "zero_hit": { "filter": { "term": { "hitCount": 0 } } },
            "zero_hit_rate": {
              "bucket_script": {
                "buckets_path": { "zero": "zero_hit>_count", "total": "_count" },
                "script": "params.zero / params.total"
              }
            }
          }
        }
      }
    }

每个月的桶会返回搜索次数（``doc_count``）、零结果次数（``zero_hit.doc_count``）和零结果率（``zero_hit_rate.value``，0～1）。
通过 ``time_zone``，月份按指定的时区划分（此处为 ``Asia/Tokyo``，请改为您所在的时区），并通过 ``must_not`` 排除了来自管理页面的搜索。
是否保留了 2 年的日志，取决于下一节中的保存期限设置。

保存期限与个人信息
==================

默认情况下，搜索日志会一直保留。
这是因为 [系统] > [通用] 中的「删除以前的搜索日志」默认为 ``-1``\ （不删除）。
指定天数后，每天 0 点运行的作业「Log Purger」会删除早于该天数的搜索日志。
点击日志、收藏日志和聊天日志也会按相同的天数删除。
用户记录由另一项设置「删除以前的用户日志」控制，其默认值同样为 ``-1``。

请同时考虑希望查看长期趋势的期间，以及组织内部对个人信息的处理规定，再决定天数。
搜索日志中包含登录用户的 ID（``user``，以及 ``roles`` 中以 ``1`` 开头的值）、IP 地址和 User-Agent。
此外，默认情况下，搜索结果中显示的文档的 URL 和标题也会记录在 ``documents`` 字段中（``logging.search.docs.enabled=true``）。
这些信息在 OpenSearch Dashboards 中全部可见，因此请遵守开头所述的访问限制。

故障排除
========

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 症状
     - 确认事项
   * - Discover 或可视化中没有显示数据
     - 右上角的期间是否包含有日志的日期时间。从搜索到日志写入可能需要 1 分钟左右（由每分钟运行的作业「Log Aggregator」写入）
   * - 无法选择 ``rank`` 或 ``searchField.label``
     - 是否在使用 ``fess_log*``。请创建专用的索引模式，或点击 [Refresh field list]
   * - 件数比 [搜索日志] 页面多
     - 是否在 ``fess_log*`` 中把点击日志或聊天日志也计算在内。访问类型的筛选条件以及日期划分所用的时区是否一致
   * - 点击件数偏少
     - 链接没有经过 ``/go/``，[通用] 中的「搜索日志」未启用，或者浏览器在没有 Fess 会话的情况下打开了 ``/go/``。也请确认 :doc:`guide-08` 的前提条件

延伸阅读
========

- 希望用同义词或关键词匹配改进找到的搜索词：:doc:`guide-08`
- 希望重新审视角色和组的设计：:doc:`guide-05`
- 希望建立包括监控和备份在内的运维体系：:doc:`guide-10`
- 希望确定在全公司推广的各个阶段衡量什么：:doc:`guide-23`

参考资料
========

- `搜索日志 <https://fess.codelibs.org/zh-cn/stable/admin/searchlog-guide.html>`__
- `搜索日志可视化配置 <https://fess.codelibs.org/zh-cn/stable/config/admin-opensearch-dashboards.html>`__
- `常规 <https://fess.codelibs.org/zh-cn/stable/admin/general-guide.html>`__
- `使用 Docker 安装（详细） <https://fess.codelibs.org/zh-cn/stable/install/install-docker.html>`__
- `docker-fess 的 Compose 文件（GitHub） <https://github.com/codelibs/docker-fess/tree/v15.9.0/compose>`__
- `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/index/>`__
