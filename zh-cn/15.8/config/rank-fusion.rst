===========================================
混合搜索与 Rank Fusion（语义 + 关键词）
===========================================

概述
====

**混合搜索**在 |Fess| 中结合了传统的关键词搜索（BM25）与**语义（向量）搜索**，并通过 **Rank Fusion** 将两组结果合并，以生成更准确、更相关的排名。Rank Fusion 会将多个搜索器的结果整合为单一的优化排名。

要启用语义搜索，请安装 Semantic Search 插件（``fess-webapp-semantic-search``），并在 ``-Drank.fusion.searchers`` 中添加 ``semantic``。

|Fess| 的 Rank Fusion 功能可以整合多个搜索结果，
提供更精确的搜索结果。

什么是 Rank Fusion
==================

Rank Fusion 是一种将多个搜索算法或评分方法（例如关键词/BM25 与语义/向量搜索）的结果
组合起来，生成单一优化排名的技术。

主要优点：

- 结合不同算法的优势
- 提高搜索精度
- 提供多样化的搜索结果

支持的算法
==========

|Fess| 支持 RRF（Reciprocal Rank Fusion）算法进行 Rank Fusion。

RRF (Reciprocal Rank Fusion)
----------------------------

RRF 通过对每个搜索结果中文档排名的倒数求和来计算分数。
当一个文档被多个搜索器检索到时，其各项分数会被累加。

计算公式::

    score(d) = Σ 1 / (k + rank(d))

- ``k``: 调整排名影响程度的常数参数（默认值：20）
- ``rank(d)``: 文档 d 在各搜索结果中的排名（从 0 开始）
- ``Σ``: 对文档 d 出现的所有搜索器求和

配置
====

fess_config.properties
----------------------

基本配置::

    # 窗口大小（融合目标的结果数量）
    # 注意：必须 >= paging.search.page.max.size × 2。
    # 如果设定值低于此最小值，将自动使用最小值。
    rank.fusion.window_size=200

    # RRF 的 rank_constant（k 参数）
    rank.fusion.rank_constant=20

    # 并行处理的线程数（0 或以下时，使用可用 CPU 核心数 × 1.5 + 1）
    rank.fusion.threads=-1

    # 分数字段名（存储融合后分数的字段）
    rank.fusion.score_field=rf_score

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - 属性
     - 默认值
     - 说明
   * - ``rank.fusion.window_size``
     - ``200``
     - 从各搜索器中获取用于融合的最大结果数量。必须 >= ``paging.search.page.max.size × 2``\ （默认为 ``200``）；若设定值低于此最小值，将自动提升至该最小值。
   * - ``rank.fusion.rank_constant``
     - ``20``
     - RRF 计算公式中的常数 ``k``\ 。值越大，高排名与低排名结果之间的分数差越小。
   * - ``rank.fusion.threads``
     - ``-1``
     - 并行运行多个搜索器时的线程数。指定 ``0`` 或以下时，将自动使用 ``可用 CPU 核心数 × 1.5 + 1``\ 。
   * - ``rank.fusion.score_field``
     - ``rf_score``
     - 用于存储融合后分数的结果文档字段名。

JVM 系统属性
------------

使用的搜索器通过 JVM 系统属性指定。
在 ``fess.in.sh``\ （或 ``fess.in.bat``）中添加如下内容::

    # 指定使用的搜索器（逗号分隔）
    -Drank.fusion.searchers=default,semantic

此属性的行为如下：

- 以 JVM 选项形式设置，而非在 ``fess_config.properties`` 中配置。
- ``default`` 是执行标准关键词搜索的搜索器，始终可用。
- ``semantic`` 是执行语义搜索（向量搜索）的搜索器，安装 Semantic Search 插件（``fess-webapp-semantic-search``）后可用。
- 若未指定此属性，将使用所有已注册的搜索器。若指定的名称与任何已注册搜索器均不匹配，则仅使用 ``default`` 搜索器。
- 结果融合仅在可用搜索器为 2 个或以上时执行。若只有 1 个搜索器可用，则不进行融合，直接返回普通搜索结果。

与混合搜索的集成
================

Rank Fusion 在结合关键词搜索与语义搜索的
混合搜索中尤为有效。
要使用语义搜索，需安装 Semantic Search 插件（``fess-webapp-semantic-search``），
并在 ``-Drank.fusion.searchers`` 中添加 ``semantic``\ 。

使用示例
========

基本混合搜索
------------

1. 通过关键词搜索计算 BM25 分数
2. 通过语义搜索计算向量相似度
3. 使用 RRF 融合两种结果
4. 生成最终排名

搜索流程::

    User Query
        ↓
    ┌──────────────────┬──────────────────┐
    │  Keyword Search  │ Semantic Search  │
    │    (BM25)        │  (Vector)        │
    └────────┬─────────┴────────┬─────────┘
             ↓                  ↓
         Rank List 1        Rank List 2
             └────────┬─────────┘
                      ↓
              Rank Fusion (RRF)
                      ↓
              Final Ranking

性能注意事项
============

内存使用
--------

- 由于需要保留多个搜索结果，内存使用量会增加。
- 可使用 ``rank.fusion.window_size`` 限制融合目标的最大数量。主搜索器（排在首位的 ``default`` 搜索器）最多获取 ``window_size`` 条结果，其他搜索器各获取 ``window_size ÷ 搜索器数量`` 条结果。

::

    # 融合目标的窗口大小
    rank.fusion.window_size=200

处理时间
--------

- 由于需要执行多次搜索，响应时间会增加。
- 使用 ``rank.fusion.threads`` 设置并行执行的线程数。

::

    # 并行执行的线程数（0 或以下时，使用可用 CPU 核心数 × 1.5 + 1）
    rank.fusion.threads=-1

故障排除
========

搜索结果与预期不符
------------------

**症状**：Rank Fusion 后的结果与预期不符

**检查事项**：

1. 分别确认各搜索类型的结果
2. 调整 ``rank.fusion.rank_constant`` 的值
3. 调整 ``rank.fusion.window_size`` 的值
4. 在翻页较深的页面（``起始位置 × 2`` 大于等于 ``rank.fusion.window_size`` 的位置），不会执行融合，仅使用主搜索器进行搜索。若希望在更多页面上获得融合结果，请增大 ``rank.fusion.window_size``\ 。

搜索缓慢
--------

**症状**：启用 Rank Fusion 时搜索变慢

**解决方法**：

1. 减小 ``rank.fusion.window_size``::

       rank.fusion.window_size=100

2. 调整 ``rank.fusion.threads``::

       rank.fusion.threads=4

内存不足
--------

**症状**：发生 OutOfMemoryError

**解决方法**：

1. 减小 ``rank.fusion.window_size``
2. 增加 JVM 堆大小

参考信息
========

- :doc:`scripting-overview` - 脚本概述
- :doc:`search-advanced` - 高级搜索设置
- :doc:`llm-overview` - LLM 集成指南（语义搜索）
