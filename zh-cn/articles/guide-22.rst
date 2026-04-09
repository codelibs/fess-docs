============================================================
第22回 从搜索数据描绘组织的知识地图 -- 通过分析仪表板了解信息利用的实态
============================================================

前言
====

搜索系统是用于"查找"信息的工具，但搜索日志本身也是宝贵的信息来源。
"搜索了什么"、"什么找不到"、"哪些信息被频繁浏览"——这些数据是映射组织信息需求和知识缺口的一面镜子。

本文将 Fess 的搜索日志与 OpenSearch Dashboards 相结合，构建一个可视化组织知识利用状况的分析仪表板。

目标读者
========

- 希望定量了解搜索系统使用情况的人员
- 希望为信息利用战略收集数据的人员
- 希望了解 OpenSearch Dashboards 基本操作的人员

搜索数据的价值
===============

从搜索日志中可以读取的信息
----------------------------

搜索日志是一种稀有的数据，可以定量把握组织的信息需求。

.. list-table:: 从搜索数据获得的洞察
   :header-rows: 1
   :widths: 30 70

   * - 数据
     - 洞察
   * - 搜索关键词
     - 员工在寻找什么（信息需求）
   * - 零命中查询
     - 组织中缺少的信息（知识缺口）
   * - 点击日志
     - 哪些搜索结果有用（内容价值）
   * - 搜索频率的时序变化
     - 信息需求的变化（趋势）
   * - 热门词汇
     - 组织整体的关注点

Fess 收集的数据
================

Fess 自动收集和存储以下数据。

搜索日志（``fess_log.search_log``）
-------------------------------------

可在管理界面的 [系统信息] > [搜索日志] 中查看。
存储在 OpenSearch 的索引 ``fess_log.search_log`` 中。

主要字段：

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 字段名
     - 类型
     - 说明
   * - ``searchWord``
     - keyword
     - 搜索关键词
   * - ``requestedAt``
     - date
     - 搜索日期时间
   * - ``hitCount``
     - long
     - 搜索结果数量（为 0 时即为零命中）
   * - ``queryTime``
     - long
     - 查询执行时间（毫秒）
   * - ``responseTime``
     - long
     - 总响应时间（毫秒）
   * - ``userAgent``
     - keyword
     - 用户代理
   * - ``clientIp``
     - keyword
     - 客户端 IP 地址
   * - ``accessType``
     - keyword
     - 访问类型（web、json、gsa、admin 等）
   * - ``queryId``
     - keyword
     - 查询 ID（用于与点击日志关联）

点击日志（``fess_log.click_log``）
------------------------------------

记录搜索结果链接被点击的信息。
存储在 OpenSearch 的索引 ``fess_log.click_log`` 中。

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 字段名
     - 类型
     - 说明
   * - ``url``
     - keyword
     - 被点击的 URL
   * - ``queryId``
     - keyword
     - 搜索日志的 queryId（标识从哪次搜索点击而来）
   * - ``order``
     - integer
     - 搜索结果中的显示位置
   * - ``requestedAt``
     - date
     - 点击日期时间
   * - ``docId``
     - keyword
     - 文档 ID

热门词汇
----------

搜索画面上显示的热门词汇是基于搜索日志汇总到 Fess 的 suggest 索引中的。
超过一定搜索命中数的查询将根据搜索次数进行排名。

使用 OpenSearch Dashboards 进行可视化
========================================

由于 Fess 的搜索日志存储在 OpenSearch 中，因此可以使用 OpenSearch Dashboards 进行高级可视化。

OpenSearch Dashboards 的设置
-------------------------------

在 Docker Compose 配置中添加 OpenSearch Dashboards。

.. code-block:: yaml

    services:
      opensearch-dashboards:
        image: opensearchproject/opensearch-dashboards:3.6.0
        ports:
          - "5601:5601"
        environment:
          OPENSEARCH_HOSTS: '["http://opensearch:9200"]'
          DISABLE_SECURITY_DASHBOARDS_PLUGIN: "true"

访问 ``http://localhost:5601`` 使用 Dashboards 界面。

创建索引模式
--------------

要在 OpenSearch Dashboards 中可视化 Fess 的日志数据，首先需要创建索引模式。

1. 访问 Dashboards，从左侧菜单选择 [Stack Management] > [Index Patterns]
2. 点击 [Create index pattern]
3. 创建以下索引模式

.. list-table::
   :header-rows: 1
   :widths: 35 25 40

   * - 索引模式
     - 时间字段
     - 用途
   * - ``fess_log.search_log``
     - ``requestedAt``
     - 搜索日志分析
   * - ``fess_log.click_log``
     - ``requestedAt``
     - 点击日志分析

仪表板设计
===========

按以下分析视角设计仪表板。
从左侧菜单的 [Visualize] 创建各项可视化，并汇总到 [Dashboard] 中。

搜索使用概况
--------------

**每日搜索次数趋势**

了解搜索使用量的变化情况。

- 索引模式：``fess_log.search_log``
- 可视化：Line（折线图）
- X 轴：Date Histogram（字段：``requestedAt``，间隔：1d）
- Y 轴：Count

如果使用量在增加，说明搜索系统已经得到普及；如果在减少，则需要改进。

**按时间段的搜索次数**

了解搜索集中在哪些时间段。

- 可视化：Vertical Bar（柱状图）
- X 轴：Date Histogram（字段：``requestedAt``，间隔：1h）
- Y 轴：Count

如果上班时间或午餐后搜索较多，说明信息收集已成为日常工作的一部分。

搜索质量分析
--------------

**零命中率趋势**

零命中率是衡量搜索质量的重要指标。
搜索日志中 ``hitCount`` 字段为 ``0`` 的记录即为零命中查询。

- 索引模式：``fess_log.search_log``
- 过滤器：添加 ``hitCount: 0`` 以提取零命中查询
- 可视化：Line（折线图）
- X 轴：Date Histogram（字段：``requestedAt``，间隔：1d）
- Y 轴：Count

如果零命中率较高，则需要添加同义词或扩大爬取范围（参见第8回）。

另外，在管理界面的 [系统信息] > [搜索日志] 中也可以查看零命中查询的列表。

**零命中查询的词云**

将零命中查询以词云形式展示，可以一目了然地了解缺少哪些信息。

- 过滤器：``hitCount: 0``
- 可视化：Tag Cloud
- 字段：Terms Aggregation（字段：``searchWord``，大小：50）

内容价值分析
--------------

**点击量最多的搜索结果**

经常被点击的搜索结果是对组织而言价值较高的内容。

- 索引模式：``fess_log.click_log``
- 可视化：Data Table
- 字段：Terms Aggregation（字段：``url``，大小：20，排序：Count 降序）

应优先维护和更新这些内容。

**点击位置分布**

查看搜索结果中第几位被点击的分布情况。

- 索引模式：``fess_log.click_log``
- 可视化：Vertical Bar（柱状图）
- X 轴：Histogram（字段：``order``，间隔：1）
- Y 轴：Count

如果第1~3位的点击较多，说明搜索质量良好；如果第10位以后的点击较多，则需要改进排名。

信息需求趋势分析
-------------------

**热门关键词排名**

了解组织整体关注什么。

- 索引模式：``fess_log.search_log``
- 可视化：Data Table
- 字段：Terms Aggregation（字段：``searchWord``，大小：20，排序：Count 降序）

热门关键词的变化反映了组织课题和关注点的变化。

分析结果的活用
================

搜索数据的分析结果可以应用于以下举措。

内容战略
---------

- **零命中查询**：确定缺少的内容并委托创建
- **热门关键词**：充实经常被搜索的主题信息
- **点击率低的结果**：考虑改进或删除内容

搜索质量改进
--------------

- **添加同义词**：从零命中查询中发现同义词候选
- **Key Match 设置**：为热门查询设置最佳结果
- **Boost 调整**：基于点击率改进排名

IT 投资决策
-------------

- **使用量增加**：规划服务器资源扩容
- **新的信息需求**：考虑对接额外的数据源
- **AI 功能需求**：决定是否引入 AI 搜索模式（参见第19回）

定期报告的制作
================

将分析结果定期整理成报告，与相关人员共享。

月度报告项目示例
------------------

1. 搜索使用情况摘要（总搜索次数、环比）
2. 零命中率趋势与改进状况
3. 热门关键词 Top 10
4. 新发现的知识缺口
5. 已实施的改进措施及其效果
6. 下月改进计划

总结
====

本文介绍了如何利用搜索日志实现组织知识的可视化。

- 从搜索日志获得的洞察（信息需求、知识缺口、内容价值）
- 使用 OpenSearch Dashboards 构建可视化仪表板
- 将分析结果应用于内容战略、搜索质量改进和 IT 投资
- 通过定期报告实现持续改进

搜索数据是描绘"组织知识地图"的宝贵资产。
AI 及下一代搜索篇到此结束。下一回作为最终回，将对整个系列进行总结。

参考资料
========

- `Fess 搜索日志 <https://fess.codelibs.org/ja/15.5/admin/searchlog.html>`__

- `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/>`__
