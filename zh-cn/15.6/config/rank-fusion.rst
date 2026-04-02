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

|Fess| 支持 RRF (Reciprocal Rank Fusion) 算法。

RRF (Reciprocal Rank Fusion)
----------------------------

RRF 通过对每个结果排名的倒数求和来计算分数。

计算公式::

    score(d) = Σ 1 / (k + rank(d))

- ``k``: 常数参数（默认: 20）
- ``rank(d)``: 文档 d 在各搜索结果中的排名

配置
====

fess_config.properties
----------------------

基本配置::

    # 窗口大小（融合对象的结果数）
    rank.fusion.window_size=200

    # RRF 的 rank_constant（k 参数）
    rank.fusion.rank_constant=20

    # 并行处理的线程数（-1 为默认值）
    rank.fusion.threads=-1

    # 分数字段名
    rank.fusion.score_field=rf_score

与混合搜索的集成
==================

Rank Fusion 在结合关键词搜索和语义搜索的
混合搜索中特别有效。

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

性能注意事项
=============

内存使用
---------

- 由于保留多个搜索结果,内存使用量会增加
- 使用 ``rank.fusion.window_size`` 限制融合对象的最大数量

::

    # 融合对象的窗口大小
    rank.fusion.window_size=200

处理时间
---------

- 由于执行多个搜索,响应时间会增加
- 使用 ``rank.fusion.threads`` 设置并行执行的线程数

::

    # 并行执行的线程数（-1 为默认值）
    rank.fusion.threads=-1

故障排除
========

搜索结果与预期不符
--------------------

**症状**: Rank Fusion 后的结果与预期不符

**检查事项**:

1. 分别确认各搜索类型的结果
2. 调整 ``rank.fusion.rank_constant`` 的值
3. 调整 ``rank.fusion.window_size`` 的值

搜索缓慢
----------

**症状**: 启用 Rank Fusion 时搜索变慢

**解决方法**:

1. 减小 ``rank.fusion.window_size``::

       rank.fusion.window_size=100

2. 调整 ``rank.fusion.threads``::

       rank.fusion.threads=4

内存不足
---------

**症状**: 发生 OutOfMemoryError

**解决方法**:

1. 减小 ``rank.fusion.window_size``
2. 增加 JVM 堆大小

参考信息
========

- :doc:`scripting-overview` - 脚本概述
- :doc:`search-advanced` - 高级搜索设置
- :doc:`llm-overview` - LLM 集成指南（语义搜索）
