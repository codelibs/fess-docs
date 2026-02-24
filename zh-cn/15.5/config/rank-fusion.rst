==================================
Rank Fusion 配置
==================================

概述
====

|Fess| 的 Rank Fusion 功能可以整合多个搜索结果,
提供更精确的搜索结果。

什么是 Rank Fusion
===================

Rank Fusion 是一种将多个搜索算法或评分方法的结果
组合起来,生成单一优化排名的技术。

主要优点:

- 结合不同算法的优势
- 提高搜索精度
- 提供多样化的搜索结果

支持的算法
===========

|Fess| 支持以下 Rank Fusion 算法:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 算法
     - 说明
   * - RRF (Reciprocal Rank Fusion)
     - 使用排名倒数的融合算法
   * - Score Fusion
     - 通过分数归一化和加权平均进行融合
   * - Borda Count
     - 基于投票的排名融合

RRF (Reciprocal Rank Fusion)
----------------------------

RRF 通过对每个结果排名的倒数求和来计算分数。

计算公式::

    score(d) = Σ 1 / (k + rank(d))

- ``k``: 常数参数（默认: 60）
- ``rank(d)``: 文档 d 在各搜索结果中的排名

配置
====

fess_config.properties
----------------------

基本配置::

    # 启用 Rank Fusion
    rank.fusion.enabled=true

    # 使用的算法
    rank.fusion.algorithm=rrf

    # RRF 的 k 参数
    rank.fusion.rrf.k=60

    # 融合对象的搜索类型
    rank.fusion.search.types=keyword,semantic

按算法配置
-----------

RRF 配置::

    rank.fusion.algorithm=rrf
    rank.fusion.rrf.k=60

Score Fusion 配置::

    rank.fusion.algorithm=score
    rank.fusion.score.normalize=true
    rank.fusion.score.weights=0.7,0.3

Borda Count 配置::

    rank.fusion.algorithm=borda
    rank.fusion.borda.top_n=100

与混合搜索的集成
==================

Rank Fusion 在结合关键词搜索和语义搜索的
混合搜索中特别有效。

配置示例
---------

::

    # 启用混合搜索
    search.hybrid.enabled=true

    # 融合关键词搜索和语义搜索的结果
    rank.fusion.enabled=true
    rank.fusion.algorithm=rrf
    rank.fusion.rrf.k=60

    # 各搜索类型的权重
    search.hybrid.keyword.weight=0.6
    search.hybrid.semantic.weight=0.4

使用示例
========

基本混合搜索
--------------

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

自定义评分
-----------

组合多个评分因素的示例::

    # 基本搜索分数 + 日期提升 + 热门度
    rank.fusion.enabled=true
    rank.fusion.algorithm=score
    rank.fusion.score.factors=relevance,recency,popularity
    rank.fusion.score.weights=0.5,0.3,0.2

性能注意事项
=============

内存使用
---------

- 由于保留多个搜索结果,内存使用量会增加
- 使用 ``rank.fusion.max.results`` 限制融合对象的最大数量

::

    # 融合对象的最大结果数
    rank.fusion.max.results=1000

处理时间
---------

- 由于执行多个搜索,响应时间会增加
- 考虑通过并行执行进行优化

::

    # 启用并行执行
    rank.fusion.parallel=true
    rank.fusion.thread.pool.size=4

缓存
------

- 对频繁的查询使用缓存

::

    # Rank Fusion 结果缓存
    rank.fusion.cache.enabled=true
    rank.fusion.cache.size=1000
    rank.fusion.cache.expire=300

故障排除
========

搜索结果与预期不符
--------------------

**症状**: Rank Fusion 后的结果与预期不符

**检查事项**:

1. 分别确认各搜索类型的结果
2. 确认权重是否适当
3. 调整 k 参数值

搜索缓慢
----------

**症状**: 启用 Rank Fusion 时搜索变慢

**解决方法**:

1. 启用并行执行::

       rank.fusion.parallel=true

2. 限制融合对象的结果数::

       rank.fusion.max.results=500

3. 启用缓存::

       rank.fusion.cache.enabled=true

内存不足
---------

**症状**: 发生 OutOfMemoryError

**解决方法**:

1. 减少融合对象的最大结果数
2. 增加 JVM 堆大小
3. 禁用不需要的搜索类型

参考信息
========

- :doc:`scripting-overview` - 脚本概述
- :doc:`../admin/search-settings` - 搜索设置指南
- :doc:`llm-overview` - LLM 集成指南（语义搜索）
