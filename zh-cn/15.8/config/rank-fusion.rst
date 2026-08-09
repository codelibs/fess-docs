===========================================
混合搜索与 Rank Fusion（语义 + 关键词）
===========================================

概述
====

**混合搜索**\ 在 |Fess| 中结合了传统的关键词搜索（BM25）与\ **语义（向量）搜索**，并通过 **Rank Fusion** 将两组结果合并，以生成更准确、更相关的排名。Rank Fusion 会将多个搜索器的结果整合为单一的优化排名。

在 |Fess| 15.8 中，语义搜索（内容分块 + 向量搜索）作为核心功能提供。启用后，语义搜索器会自动
注册到 Rank Fusion 中。有关如何配置，请参阅 :doc:`search-semantic`。

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

.. note::

   融合算法固定为 RRF，没有可切换到其他算法的设置。
   此外，也不支持按搜索器设置权重。各搜索器的贡献会以相同的权重进行合计。
   唯一能够调整排名倾向的设置是 ``rank.fusion.rank_constant``\ 。

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

    # 并行处理的线程数（0 或以下时，使用可用 CPU 核心数 × 3 ÷ 2 + 1）
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
     - 从各搜索器中获取用于融合的最大结果数量。必须 >= ``paging.search.page.max.size × 2``\ （默认为 ``200``）；若设定值低于此最小值，将自动提升至该最小值（启动时会输出 WARN 日志）。
   * - ``rank.fusion.rank_constant``
     - ``20``
     - RRF 计算公式中的常数 ``k``\ 。值越大，高排名与低排名结果之间的分数差越小。
   * - ``rank.fusion.threads``
     - ``-1``
     - 并行运行多个搜索器的固定线程池的线程数。指定 ``0`` 或以下时，将自动使用 ``可用 CPU 核心数 × 3 ÷ 2 + 1``\ （由于是整数运算，小数部分会被舍去。例如：4 核 → 7，5 核 → 8）。
   * - ``rank.fusion.score_field``
     - ``rf_score``
     - 用于存储融合后分数的结果文档字段名。

.. note::

   **配置的生效时机**

   以上 4 项配置的更改均需要重启 |Fess| 才能生效。从 ``fess_config.properties``
   读取的值会被缓存在 JVM 内，因此在运行过程中改写该文件不会生效。

   另外，``rank.fusion.window_size`` 仅在启动时读取一次，\ ``rank.fusion.threads``
   则在创建线程池时读取。线程池是在注册了 ``default`` 以外的搜索器
   （例如语义搜索器）时创建的，因此在语义搜索未启用的情况下，线程池本身不会被创建。

JVM 系统属性
------------

使用的搜索器通过 JVM 系统属性指定。
在 ``fess.in.sh`` 中添加如下内容::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Drank.fusion.searchers=default,semantic_chunk"

如果是 ``fess.in.bat``\ ，则按如下方式添加::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Drank.fusion.searchers=default,semantic_chunk

此属性的行为如下：

- 以 JVM 选项形式设置，而非在 ``fess_config.properties`` 中配置。键名请直接指定
  ``rank.fusion.searchers`` 本身。其他设置中常用的 ``-Dfess.config.`` 或 ``-Dfess.system.``
  前缀形式（例如 ``-Dfess.config.rank.fusion.searchers``\ ）不会被识别。
- 除了 JVM 选项之外，也可以在管理界面“系统 > 常规”的“系统属性”栏中，以
  ``rank.fusion.searchers=default,semantic_chunk`` 这样的形式写成一行。
  但该栏中的值仅在同名系统属性尚未设置时才会被应用。
  因此，若已通过 ``-D`` 指定，则 JVM 选项优先；而要更改已经应用的值，
  需要重启 |Fess|\ 。
- ``default`` 是执行标准关键词搜索的搜索器，始终可用。
- 搜索器的名称由其实现类名去掉末尾的 ``Searcher``\ ，再转换为小写蛇形命名（snake_case）得来
  （``SemanticChunkSearcher`` → ``semantic_chunk``）。核心集成的语义搜索器
  （:doc:`search-semantic`）注册的名称为 ``semantic_chunk``\ 。
- 若未指定此属性，将使用所有已注册的搜索器。若指定的名称与任何已注册搜索器均不匹配，则仅使用 ``default`` 搜索器。如果您使用核心集成的语义搜索器（:doc:`search-semantic`），通常完全不需要设置此属性。
- 结果融合仅在可用搜索器为 2 个或以上时执行。若只有 1 个搜索器可用，则不进行融合，直接返回普通搜索结果。

.. warning::

   如果您此前在 |Fess| 15.7 或更早版本中使用过 ``fess-webapp-semantic-search`` 插件，可能曾被
   告知要将此属性设置为 ``-Drank.fusion.searchers=default,semantic``\ 。该插件将其搜索器注册为
   名称 ``semantic``\ ，这与 15.8 中引入的核心集成搜索器名称 ``semantic_chunk`` 是\ **不同的
   搜索器**\ 。如果您原样将这个 15.7 时代的设置带入 15.8，允许列表中将永远不包含
   ``semantic_chunk``\ ，导致核心集成的语义搜索（内容分块 + 向量搜索）\ **完全无法工作**\ ——|Fess|
   会静默地继续返回普通关键词搜索结果（启动时会记录一条警告日志，但每次请求的排除行为本身仅以
   DEBUG 级别记录）。如果您的配置中指定了 ``default,semantic``\ ，请移除该设置，或为其添加
   ``semantic_chunk``\ 。详情请参阅 :doc:`search-semantic` 中的“从 15.7 及更早版本迁移”一节。

与混合搜索的集成
================

Rank Fusion 在结合关键词搜索与语义搜索的
混合搜索中尤为有效。要使用语义搜索，请在配置内容分块功能之后设置
``content_chunker.search.enabled=true``\ 。

.. warning::

   ``content_chunker.enabled`` 和 ``content_chunker.search.enabled`` 等
   ``content_chunker.*`` 配置属于\ **系统属性**\ ，而不是 ``fess_config.properties``\ 。
   请将其写入 ``conf/system.properties``\ ，或以
   ``-Dfess.system.content_chunker.search.enabled=true`` 这样的形式指定为 JVM 选项。
   即使写入 ``fess_config.properties`` 也不会生效。
   另外，``content_chunker.search.enabled`` 仅在启动时评估，因此启用后需要重启 |Fess|\ 。

详情请参阅 :doc:`search-semantic`\ 。

融合结果的确认
==============

要确认 Rank Fusion 是否确实在工作，可以查看搜索结果中附加的以下两个字段。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 字段
     - 内容
   * - ``searcher``
     - 检索到该文档的搜索器名称数组（例如 ``["default", "semantic_chunk"]``）。若两者都包含在内，则表示该文档在关键词搜索和语义搜索中均被命中。
   * - ``rf_score``
     - 通过 RRF 计算出的融合后分数。字段名可通过 ``rank.fusion.score_field`` 更改。

这两个字段都是在搜索时动态附加的值，不会保存到索引中。
此外，默认情况下它们不会包含在 ``/api/v2/search`` 的响应中，若要确认，请在
``fess_config.properties`` 中进行以下设置并重启 |Fess|::

    query.additional.api.response.fields=rf_score,searcher

.. note::

   ``query.additional.api.response.fields`` 用于向“允许包含在 v2 搜索 API 响应中的字段”
   许可列表中追加条目。如果追加 ``role`` 或 ``virtual_host`` 等访问控制用字段，
   访问控制信息将暴露在搜索 API 的响应中，因此请勿追加这类字段。

对命中数量的影响
================

执行 Rank Fusion 时，返回的总命中数量并非直接使用主搜索器（注册在首位的 ``default``
搜索器）的数量，而是按如下方式进行修正::

    总命中数量 = 主搜索器的总命中数量 + 修正值

修正值是指：在融合后的前 ``window_size ÷ 2`` 条结果中，未包含在主搜索器前
``window_size ÷ 2`` 条结果内的文档数量。也就是说，命中数量会增加仅由语义搜索找到的
文档数量。
因此，即使是相同的查询，启用与不启用混合搜索时的命中数量也可能不同。

另外，当主搜索器的总命中数量以概算值（下限值）返回时，不会进行此修正。

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
- 可使用 ``rank.fusion.window_size`` 限制融合目标的最大数量。主搜索器（排在首位的 ``default`` 搜索器）最多获取 ``window_size`` 条结果，其他搜索器各获取 ``window_size ÷ 搜索器数量`` 条结果（``搜索器数量`` 是包含主搜索器在内的总数，除法会向下取整）。
- 例如，当有 2 个搜索器（``default`` 和 ``semantic_chunk``）且 ``window_size=200`` 时，主搜索器获取 200 条、语义搜索器获取 100 条，因此最多会保留 300 条文档。

::

    # 融合目标的窗口大小
    rank.fusion.window_size=200

.. warning::

   ``rank.fusion.window_size`` 不能低于 ``paging.search.page.max.size × 2``\ 。
   当 ``paging.search.page.max.size`` 为默认值 ``100`` 时，下限即为 ``200``\ ，这与
   ``rank.fusion.window_size`` 的默认值相同。也就是说，\ **在默认配置下无法将 window_size
   设置为小于默认值**\ 。即使设置了更小的值，启动时也会输出 WARN 日志并将其提升至 ``200``\ 。
   若要实际减小该值，需要先降低 ``paging.search.page.max.size``\ ，但这同时也会降低搜索界面
   和 API 中每页可请求的最大结果数量。

处理时间
--------

- 由于需要执行多次搜索，响应时间会增加。
- 使用 ``rank.fusion.threads`` 设置并行执行的线程数。

::

    # 并行执行的线程数（0 或以下时，使用可用 CPU 核心数 × 3 ÷ 2 + 1）
    rank.fusion.threads=-1

.. note::

   搜索器的执行没有设置超时。如果存在不返回响应的搜索器，搜索请求将一直等待其完成。

搜索器故障时的行为
==================

当任一搜索器因异常而失败时，该搜索器的结果会被视为空，在输出 WARN 日志之后，
仅使用其余搜索器的结果继续进行融合。搜索请求本身不会变成错误。

但查询语法错误（``InvalidQueryException``）和分页上限超出
（``ResultOffsetExceededException``）除外，它们会直接作为错误返回。
此外，在不进行融合的深层页面（``起始位置 × 2`` 大于等于 ``rank.fusion.window_size`` 的位置），
主搜索器中发生的异常会直接作为搜索请求的错误返回。

语义搜索器在无法连接到嵌入提供商或嵌入处理失败时，会返回空结果。
这种情况下同样不会产生错误，而是仅返回关键词搜索的结果。

故障排除
========

搜索结果与预期不符
------------------

**症状**：Rank Fusion 后的结果与预期不符

**检查事项**：

1. 确认 ``searcher`` 字段（请参阅“融合结果的确认”）。如果所有文档都仅为
   ``["default"]``\ ，则说明语义搜索器没有返回结果。
2. 确认语义搜索是否被跳过。除了包含搜索语法（如 ``"`` ``:`` ``AND`` 等）的查询之外，
   在通过标签、排序、分面进行筛选，以及位置信息搜索、相似文档搜索时，语义搜索器也不会返回
   结果，仅返回关键词搜索的结果。
   跳过条件的详细信息请参阅 :doc:`search-semantic`\ 。
3. 分别确认各搜索类型的结果
4. 调整 ``rank.fusion.rank_constant`` 的值
5. 在翻页较深的页面（``起始位置 × 2`` 大于等于 ``rank.fusion.window_size`` 的位置，默认情况下
   为第 101 条之后）不会执行融合，仅使用主搜索器进行搜索。若希望在更多页面上获得融合结果，
   请增大 ``rank.fusion.window_size``\ 。

搜索缓慢
--------

**症状**：启用 Rank Fusion 时搜索变慢

**解决方法**：

1. 调整 ``rank.fusion.threads``::

       rank.fusion.threads=4

2. 减小 ``rank.fusion.window_size``\ 。但由于不能低于下限
   （``paging.search.page.max.size × 2``），在默认配置下需要将以下两项成对设置::

       paging.search.page.max.size=50
       rank.fusion.window_size=100

   请注意，每页可请求的最大结果数量也会随之下降。设置后需要重启。

内存不足
--------

**症状**：发生 OutOfMemoryError

**解决方法**：

1. 按照“搜索缓慢”中的相同步骤减小 ``rank.fusion.window_size``
2. 增加 JVM 堆大小

参考信息
========

- :doc:`search-semantic` - 语义搜索（内容分块）的配置
- :doc:`scripting-overview` - 脚本概述
- :doc:`search-advanced` - 高级搜索设置
- :doc:`llm-overview` - LLM 集成指南（语义搜索）
