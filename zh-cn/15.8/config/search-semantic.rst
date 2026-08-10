===================================================
语义搜索（内容分块 + 向量搜索）
===================================================

概述
====

在 |Fess| 15.8 中，**内容分块功能**\ ——将文档正文拆分为若干分块，并为每个分块生成并存储嵌入
向量——已被整合进核心。生成的向量用于以下两个用途：

- **语义搜索**：一种通过 Rank Fusion 将关键词（BM25）搜索与向量搜索结合起来的混合搜索。即使没有
  精确的关键词匹配，语义上与查询相近的文档也可以被匹配到。
- **AI 搜索模式（RAG）**：在生成回答时，仅选取与问题语义最相近的分块作为 LLM 的上下文，从而提升
  回答质量并提高 token 使用效率。

以上功能默认全部禁用。除非您启用它们，否则 |Fess| 会继续像以往一样仅使用关键词搜索。如果您正在
从 15.7 或更早版本升级 |Fess|，或此前一直在使用 ``fess-webapp-semantic-search`` 插件，请参阅
:ref:`semantic-search-migration`\ 。

处理流程
--------

1. 爬虫像往常一样对文档进行索引（此时尚不存在任何分块）。
2. 调度器任务 **Content Chunk Vector Indexer** 会查找尚未处理的文档，将其正文（``content`` 字段）
   拆分为分块并生成嵌入向量，然后存入 ``content_chunk_vector`` 字段。此时 ``content`` 字段本身也会
   被改写为分块数组（``content_length`` 仍保留原来的值）。
3. 该处理的结果会被记录到 ``content_chunk_status`` 字段中（说明见下文）。
4. 当 ``content_chunker.search.enabled=true`` 时，语义搜索器会在搜索时参与 Rank Fusion。

前提条件
========

- **带 k-NN 插件的 OpenSearch**：在 |Fess| 15.8 中，无论内容分块功能是否启用，搜索索引
  （``fess.search``）的映射中始终包含 ``content_chunk_vector`` 字段（``nested`` 类型，其
  ``vector`` 子字段才是用于 ANN 的 ``knn_vector`` 类型），并且索引设置中也始终包含
  ``index.knn: true``\ 。因此，如果 OpenSearch 未安装 k-NN 插件，创建新索引会直接失败，
  |Fess| 也无法启动。

  .. list-table::
     :header-rows: 1
     :widths: 35 65

     * - 配置
       - k-NN 插件支持情况
     * - 内置 OpenSearch（``bin/fess``，或 ``SEARCH_ENGINE_HTTP_URL`` 未设置时的 TAR.GZ/ZIP
         软件包默认状态）
       - 内置了 k-NN 插件。但不包含 JNI 原生库，因此唯一支持的 ANN 引擎是 ``lucene``\ 。
         ``content_chunker.search.knn.engine`` 也接受 ``faiss`` 作为取值，在此设置后映射仍会
         创建成功——但\ **每次写入时文档都会被静默丢失，搜索结果也会变为 0 条**\ （以这种组合
         启动时，会在启动时输出一条警告日志）。
     * - Docker（``ghcr.io/codelibs/fess-opensearch``）、始终连接到单独安装的外部 OpenSearch 的
         RPM/DEB 软件包，或其他外部 OpenSearch（标准发行版）
       - 完全支持，包括 ``faiss``\ 。
     * - 外部 OpenSearch 的\ **最小化发行版**
       - **不支持。** 由于不包含 k-NN 插件，创建新索引会失败。

  ``content_chunker.search.knn.engine`` 在上述任何配置下都不接受 ``nmslib`` 作为取值：
  ``content_chunk_vector`` 是一个 ``nested`` 字段，而 k-NN 插件仅对 ``lucene``/``faiss`` 引擎
  支持 nested 字段（``nmslib`` 从 OpenSearch 3.0 起也已被弃用并受限）。设置该值会回退为
  ``lucene`` 并记录一条警告；其他 ANN 相关设置的可接受取值请参阅下方的配置参考。

- **外部集群的 OpenSearch 版本**：内置的 ``fess.search`` 索引设置会在
  ``fess_indices/fess.json``\ （及其 AWS/cloud 变体）中始终发送 ``index.knn`` 和
  ``knn.derived_source.enabled``\ 。后者是 k-NN 插件中较新的设置，无法识别该设置的旧版
  OpenSearch 无论是否安装 k-NN 插件，创建索引都会失败。关于 |Fess| 15.8 支持的 OpenSearch
  版本，请参阅 :doc:`../install/prerequisites`\ 。

- **嵌入提供商**：使用以下之一。

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - 配置值
     - 提供方
     - 说明
   * - ``opensearch``
     - |Fess| 核心（内置）
     - 使用部署到 OpenSearch ML Commons 的嵌入模型。无需额外插件。默认设置。
   * - ``ollama``
     - ``fess-llm-ollama`` 插件
     - 使用 Ollama 嵌入模型（例如 ``nomic-embed-text``）。
   * - ``openai``
     - ``fess-llm-openai`` 插件
     - 使用 OpenAI 嵌入 API。
   * - ``gemini``
     - ``fess-llm-gemini`` 插件
     - 使用 Google Gemini 嵌入 API。
   * - ``none``
     - |Fess| 核心（内置）
     - 仅将文档拆分为分块，不生成向量（仅分块模式）。

配置参考
========

所有 ``content_chunker.*`` 配置都统一在\ **系统属性**\ （``system.properties``）这一个通道中。
可以设置在 ``app/WEB-INF/conf/system.properties``\ （RPM/DEB 软件包为
``/etc/fess/system.properties``\ ，Docker 为 ``/opt/fess/system.properties``）中，也可以通过启动
选项 ``-Dfess.system.<键名>`` 提供初始值。配置值会在运行时被重新加载，因此大多数设置在更改后会立即
生效。唯一的例外是启用 ``content_chunker.search.enabled``\ （``false`` → ``true``）：由于语义
搜索器仅在启动时注册，**此项更改需要重启才能生效**。

.. note::

   ``content_chunker.*`` 的键名也以注释的形式列在 ``fess_config.properties`` 中，但这些配置项
   只会从 ``system.properties`` 通道读取。写在 ``fess_config.properties`` 或
   ``-Dfess.config.<键名>`` 中都会被忽略，因此请务必设置在 ``system.properties`` 中。另外，
   管理界面的「系统信息」→「配置信息」是查看当前值的\ **只读**\ 页面，无法通过该页面设置
   ``content_chunker.*``\ 。

system.properties 配置
------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 15 45

   * - 属性
     - 默认值
     - 说明
   * - ``content_chunker.enabled``
     - ``false``
     - 整个内容分块功能的总开关
   * - ``content_chunker.chunker.name``
     - ``length``
     - 分块方式
   * - ``content_chunker.length.chunk_size``
     - ``800``
     - 每个分块的目标字符数。启用边界感知切分（默认）时，这是目标值而非硬性上限：分块可能比该值短
       ``boundary.lookback_percent``\ ，也可能长 ``max(lookahead, 32)`` 个字符（默认配置下为
       640～840 个字符）。请针对嵌入模型的 token 上限预留这一余量
   * - ``content_chunker.length.overlap``
     - ``0``
     - 各分块之间重叠的字符数。重启位置同样会对齐到边界，而对齐只会将其前移，因此实际重叠介于
       该值与该值的两倍之间
   * - ``content_chunker.length.boundary.enabled``
     - ``true``
     - 将每个切分点移动到合适的文本边界，而不是恰好在 ``chunk_size`` 个字符处切分。候选项分为
       多个层级，取所存在的最高层级中距离最近的一个：换行或句末优先，其次是分句符号或空格，最后是
       书写体系变化。设为 ``false`` 可恢复此前的固定长度行为
   * - ``content_chunker.length.boundary.lookback_percent``
     - ``20``
     - 在理想切分点之前搜索边界的范围（占 ``chunk_size`` 的百分比，0～50）
   * - ``content_chunker.length.boundary.lookahead_percent``
     - ``5``
     - 在理想切分点之后搜索句末或换行的范围（占 ``chunk_size`` 的百分比，0～25）。仅在切分点
       之前未找到候选时使用
   * - ``content_chunker.max_chunks_per_document``
     - ``1000``
     - 每个文档的最大分块数。超过此值的文档将被标记为 ``skipped``，并且不会生成嵌入。由于边界感知切分会使分块变短，一个文档生成的分块数比固定长度切分
       约多 3%～25%，因此包含超大文档的语料可能需要调高此值
   * - ``content_chunker.embedding.name``
     - ``opensearch``
     - 嵌入提供商（``opensearch`` / ``ollama`` / ``openai`` / ``gemini`` / ``none``）
   * - ``content_chunker.embedding.dimension``
     - ``768``
     - 嵌入向量的维度。创建映射时会使用该值，因此它\ **必须**\ 与您所用嵌入模型的维度一致。该值有
       两条读取路径，行为并不相同。创建索引映射时，未设置、非数字、小于等于 0、以及超过
       ``16000``\ （k-NN 插件自身的上限）的情况，都会带警告回退为 ``768``\ 。而在执行嵌入处理时
       没有任何回退，未设置、非数字、小于等于 0 都会直接出错。由于超过 ``16000`` 的值在运行时并
       不会被拒绝，届时只有映射会以 ``768`` 创建，从而导致维度不一致
   * - ``content_chunker.job.concurrency``
     - ``2``
     - 索引器任务的并行工作线程数
   * - ``content_chunker.job.bulk_size``
     - ``20``
     - 每批获取并写入的文档数
   * - ``content_chunker.job.max_documents_per_run``
     - ``-1``\ （无限制）
     - 每次任务运行处理的最大文档数。任何小于等于 ``0`` 的值都视为无限制
   * - ``content_chunker.job.retry_failed``
     - ``false``
     - 设置为 ``true`` 时，上一次运行中以 ``content_chunk_status=fail`` 结束的文档也会被纳入下一次
       运行的处理对象。没有自动重试或尝试次数跟踪；预期的使用方式是先修复根本原因，然后临时启用
       此项以进行重试
   * - ``content_chunker.chat.top_k``
     - ``3``
     - AI 搜索模式生成回答时选取的分块数
   * - ``content_chunker.search.enabled``
     - ``false``
     - 语义搜索的 Rank Fusion 集成（**启用此项需要重启**）
   * - ``content_chunker.search.min_score``
     - （未设置）
     - 结果被纳入所需的最小余弦相似度（0-1）。未设置时不进行截断。在 ``ann`` 模式下，若
       ``search.knn.space_type`` 不是 ``cosinesimil``\ ，则无法定义基于余弦的阈值，因此会带警告
       跳过该截断
   * - ``content_chunker.search.knn.method``
     - ``hnsw``
     - ANN 索引方法。目前唯一支持的取值是 ``hnsw``，其他取值会带警告回退为 ``hnsw``\ （会反映到
       映射中；更改需要重新创建索引）
   * - ``content_chunker.search.knn.engine``
     - ``lucene``
     - ANN 引擎。仅支持 ``lucene`` 或 ``faiss``\ （参见上方的前提条件），其他取值会带警告回退为
       ``lucene``\ （会反映到映射中；更改需要重新创建索引）
   * - ``content_chunker.search.knn.space_type``
     - ``cosinesimil``
     - 距离空间。仅支持 ``cosinesimil``、``innerproduct``、``l2``，其他取值会带警告回退为
       ``cosinesimil``\ （会反映到映射中；更改需要重新创建索引）
   * - ``content_chunker.search.knn.k``
     - ``100``
     - 每次 ANN 查询检索的邻居数量（深分页时会自动放大）
   * - ``content_chunker.search.knn.param.ef_search``
     - （未设置）
     - ANN 查询的 ``ef_search`` 参数

.. note::
   将 ``content_chunker.length.boundary.enabled`` 设为 ``false``\ ，或将两个百分比都设为
   ``0``\ ，可完全复现此前的固定长度行为。修改这些设置只影响之后切分的文档：已经以分块数组形式
   保存的文档会保留原有边界，直到被重新爬取。

.. note::

   HNSW 的 ``m`` 和 ``ef_construction`` 参数被硬编码在 ``doc.json`` 中（``m=16`` /
   ``ef_construction=100``），无法通过配置更改。

opensearch 提供商的连接配置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

内置 ``opensearch`` 提供商（OpenSearch ML Commons）的连接配置。这些配置项设置在与上面相同的
``system.properties`` 文件中。

.. list-table::
   :header-rows: 1
   :widths: 50 20 30

   * - 属性
     - 默认值
     - 说明
   * - ``content_chunker.embedding.opensearch.model.id``
     - （必填）
     - 已部署到 ML Commons 的模型 ID
   * - ``content_chunker.embedding.opensearch.api.url``
     - 搜索引擎的地址
     - ML Commons API 端点。未设置时，默认为 |Fess| 已在使用的搜索引擎（例如
       ``http://localhost:9200``）
   * - ``content_chunker.embedding.opensearch.username`` / ``password``
     - 搜索引擎的凭据
     - 未设置时，回退使用搜索引擎连接所用的凭据——但仅在 ``api.url`` 未配置期间（即目标与
       |Fess| 已在使用的集群相同）才会如此。一旦设置了 ``api.url``，则不再回退
   * - ``content_chunker.embedding.opensearch.timeout``
     - ``60000``
     - 请求超时（毫秒）
   * - ``content_chunker.embedding.opensearch.connect.timeout``
     - ``5000``
     - 连接超时（毫秒）
   * - ``content_chunker.embedding.opensearch.retry.max``
     - ``3``
     - 针对瞬时错误（429、5xx 等）的重试次数
   * - ``content_chunker.embedding.opensearch.retry.base.delay.ms``
     - ``2000``
     - 重试的基础退避延迟（毫秒）
   * - ``content_chunker.embedding.opensearch.availability.check.interval``
     - ``60``
     - 提供商可用性检查的间隔（秒）
   * - ``content_chunker.embedding.opensearch.document.prefix`` / ``query.prefix``
     - （空）
     - 在进行嵌入之前添加到文档/查询文本前面的前缀

.. warning::

   ``system.properties`` 的内容可以在管理界面的「系统信息」→「配置信息」页面的「应用程序属性」
   面板中查看。其中 ``content_chunker.embedding.opensearch.password`` 会在该页面上被掩码为
   ``XXXXXXXX``\ ，但 ``username`` 会原样显示。此外，通过 ``-Dfess.system.<键名>`` 指定的值会
   在同一页面的「系统属性」面板中\ **不加掩码地**\ 显示，因此凭据请写入 ``system.properties``\ ，
   而不要放在启动选项中。

其他提供商（ollama / openai / gemini）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ollama`` 提供商（``fess-llm-ollama`` 插件）在 ``content_chunker.embedding.ollama.`` 前缀下
使用同样风格的配置（``api.url`` 默认值为 ``http://localhost:11434``\ ，``model`` 默认值为
``embeddinggemma``\ ，``document.prefix`` / ``query.prefix`` 默认值分别为
``title: none | text:`` / ``task: search result | query:``）。如果要使用 ``nomic-embed-text``
系列的模型，请将 ``document.prefix`` / ``query.prefix`` 显式设置为 ``search_document:`` /
``search_query:``\ 。这些前缀会原样拼接到待嵌入的文本前（前后空白不会被去除），因此上述默认值
以及 ``search_document:`` / ``search_query:`` 都 **在末尾包含一个半角空格**\ 。自行设置前缀时，
请不要遗漏这个分隔用的空格。

``openai`` 与 ``gemini`` 提供商的配置方式相同，
分别对应 ``content_chunker.embedding.openai.`` 和 ``content_chunker.embedding.gemini.`` 前缀。
完整的配置项列表请参阅各插件自身的文档。

配置步骤（以 opensearch 提供商为例）
=====================================

本节以内置的 ``opensearch`` 提供商（ML Commons）为例，介绍一个完整的配置示例。

1. 部署嵌入模型
----------------

向 OpenSearch ML Commons 注册并部署一个嵌入模型。在单节点集群上，必须先应用以下设置。

.. code-block:: bash

    curl -XPUT "http://localhost:9200/_cluster/settings" \
         -H "Content-Type: application/json" -d '
    {"persistent": {"plugins.ml_commons.only_run_on_ml_node": false}}'

注册并部署模型（示例：384 维的句子嵌入模型）：

.. code-block:: bash

    # 注册模型（从响应的 task_id 中获取 model_id）
    curl -XPOST "http://localhost:9200/_plugins/_ml/models/_register" \
         -H "Content-Type: application/json" -d '
    {
      "name": "huggingface/sentence-transformers/all-MiniLM-L6-v2",
      "version": "1.0.2",
      "model_format": "TORCH_SCRIPT"
    }'

    # 确认任务完成并获取 model_id（state 变为 COMPLETED 后会返回 model_id）
    curl "http://localhost:9200/_plugins/_ml/tasks/<task_id>"

    # 部署
    curl -XPOST "http://localhost:9200/_plugins/_ml/models/<model_id>/_deploy"

    # 检查状态：model_state 应为 DEPLOYED
    curl "http://localhost:9200/_plugins/_ml/models/<model_id>"

.. note::

   仍处于 ``REGISTERED`` 状态的模型无法使用。请务必先部署它，并确认 ``model_state`` 已变为
   ``DEPLOYED``\ 。

2. 配置 |Fess|
----------------

``app/WEB-INF/conf/system.properties``\ （RPM/DEB 软件包为 ``/etc/fess/system.properties``\ ，
Docker 为 ``/opt/fess/system.properties``\ 。以下各项均写入同一个文件）::

    content_chunker.enabled=true
    content_chunker.embedding.name=opensearch
    content_chunker.embedding.dimension=384
    content_chunker.embedding.opensearch.model.id=<model_id>

如果您还想使用语义搜索，请再添加以下内容::

    content_chunker.search.enabled=true

完成这些更改后重启 |Fess|\ 。

3. 重新创建索引（在现有部署上启用时）
---------------------------------------

``content_chunk_vector`` 字段的映射——包括您配置的维度和 ANN 方法设置——会在 ``fess.search``
索引\ **被新建的那一刻**\ 应用。

- **全新安装**：如果您在首次启动 |Fess| 之前就已将上述设置应用到 ``system.properties``\ ，则
  正确的映射会在索引首次创建时自动应用，因此不需要执行此步骤。
- **索引已存在的情况**\ （即您此前至少启动过一次 |Fess|）：正在运行的索引不会自动获取新的映射，
  已有的映射事后也无法修改。请按以下方式重新创建索引：

  打开「系统信息」→「维护」，在「重新索引」中启用「更新别名」后执行。

  之后您可以确认，重新创建的索引的索引设置中包含 ``index.knn: true``\ ，并且包含带有您所配置的
  维度与 ANN 方法设置的 ``content_chunk_vector`` 映射（``index.knn`` 属于索引设置，而 ANN 方法
  设置属于映射，两者的应用位置不同）。

.. warning::

   「重新索引」以后台异步方式运行，管理界面不会显示完成通知。``_cat/indices`` 只能说明新索引
   已经存在（状态、文档数等），并不能说明别名指向的是哪个索引。在进行下面的索引器任务步骤
   之前，请改用 ``_cat/aliases`` 确认 ``fess.search`` 和 ``fess.update`` 是否都已指向新索引；
   |Fess| 的日志只会在失败时记录警告，因此日志安静并不代表成功，只说明没有出现已知的失败。
   旧索引（此前 ``fess.search`` 别名所指向的实体索引，名称形如 ``fess.<timestamp>``）不会被
   自动删除，请在不再需要时手动删除。在新旧两个索引同时存在期间，索引磁盘占用大约会是平时的
   两倍。

4. 启用索引器任务
-------------------

分块与嵌入生成由调度器任务 **Content Chunk Vector Indexer**\ （ID：
``content-chunk-vector-indexer``；默认禁用；调度 ``0 13 * * *``）执行。

请在「系统」→「调度器」中启用此任务，然后通过「立即开始」运行一次。此后，系统会与爬取是否完成
无关地，按照所配置的调度（默认为每天 13:00）处理尚未处理的文档。该任务并未与爬取任务串联，
因此如果希望在爬取结束后立即处理，请将其调度时间设置在爬取任务的预计完成时刻之后。

.. note::

   在多节点部署中，建议将此任务固定到某一个节点上运行。在每个节点上同时运行并不会破坏正确性，
   但每个节点都会冗余地处理并嵌入相同的文档，从而使嵌入提供商承受的负载与成本随节点数量成倍
   增加。

   固定该任务需要\ **同时**\ 满足以下两项设置——仅设置其中一项无法完成固定。

   1. **在您希望运行该任务的节点上**：在 ``app/WEB-INF/classes/fess_config.properties``\ （RPM/DEB
      软件包为 ``/etc/fess/fess_config.properties``）中设置
      ``scheduler.target.name=<某个标识符>``\ （或通过
      ``-Dfess.config.scheduler.target.name=<某个标识符>`` 指定），然后重启该节点。（默认值为
      空；其他所有节点保持默认值不变。）
   2. 在管理界面的「系统」→「调度器」中打开 Content Chunk Vector Indexer 任务，将其「目标」字段
      从 ``all`` 更改为与步骤 1 中设置的相同标识符，然后保存。

   关于「目标」字段的含义，请参阅 :doc:`../admin/scheduler-guide`\ 。如果仅设置了
   ``scheduler.target.name``\ ，而「目标」字段仍保留为 ``all``\ ，任务将\ **不会**\ 被固定：``all``
   被视为始终匹配的特殊值，因此仅执行步骤 1 或仅执行步骤 2 都是不够的——必须同时完成两者。

.. warning::

   固定之后，「立即开始」也必须\ **从步骤 1 中设置了标识符的那个节点的管理界面**\ 执行。如果在
   非目标节点上点击「立即开始」，界面上虽然会显示「作业 … 已启动。」，但由于「目标」不匹配，
   任务实际上不会运行（只会在该节点的日志中输出一条 INFO 级别的 ``Ignoring job``）。

5. 检查处理状态
-----------------

您可以在每个文档的 ``content_chunk_status`` 字段中查看其处理结果。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 值
     - 含义
   * - （字段不存在）
     - 尚未处理（将在下次任务运行时被处理）。重新爬取后的文档也会回到此状态
   * - ``done``
     - 分块与向量生成均已完成
   * - ``chunked``
     - 仅完成分块（仅分块模式）。除了 ``embedding.name=none`` 的情况之外，当 ``embedding.name``
       所指定的提供商对应的插件未安装时，也会进入此状态
   * - ``skipped``
     - 处理被跳过（例如超过了 ``max_chunks_per_document``）
   * - ``fail``
     - 处理失败（请检查日志）

您可以直接查询搜索引擎来查看状态分布::

    curl -XPOST "http://localhost:9200/fess.search/_search" \
         -H "Content-Type: application/json" -d '
    {"size": 0, "aggs": {"status": {"terms": {"field": "content_chunk_status", "missing": "pending"}}}}'

借助 ``missing`` 选项，不带 ``content_chunk_status``\ （即尚未处理）的文档会被聚合到键名为
``pending`` 的分桶中。

语义搜索的工作方式
====================

设置 ``content_chunker.search.enabled=true`` 会将语义搜索器注册到 Rank Fusion 中，之后它会将
关键词搜索结果与向量搜索结果合并。（有关 Rank Fusion 的工作原理，请参阅 :doc:`rank-fusion`\ 。）
另外，搜索时还会参照 ``content_chunker.enabled``\ 。当 ``content_chunker.enabled=false`` 或
``content_chunker.embedding.name=none`` 时，即使搜索器已经注册，也不会执行语义搜索（该判断按每次
请求进行，因此无需重启）。

.. warning::

   由于语义搜索器是在启动时注册的，**启用此项需要重启**。禁用它（将值改回 ``false``）是按请求
   逐次判断的，因此会立即生效。

exact 模式与 ann 模式
------------------------

搜索方式会根据索引的状态自动选择。

.. list-table::
   :header-rows: 1
   :widths: 12 44 44

   * - 模式
     - 条件
     - 特点
   * - ``ann``
     - 具有 ``index.knn`` 和 ANN 方法设置的索引
     - 使用 HNSW 进行近似最近邻搜索。适合大规模索引
   * - ``exact``
     - 除上述之外的情况（缺少 ``index.knn`` 或 ANN 方法设置中任意一项的索引，包括索引状态判定
       失败的情况）
     - 对所有向量进行精确的余弦相似度计算。适合中小规模索引

在 |Fess| 15.8 下新创建的任何 ``fess.search`` 索引，无论 ``content_chunker.search.enabled`` 的
值如何，始终具有 ``index.knn`` 和 ANN 方法设置——因此通常总是使用 ``ann`` 模式。``exact`` 模式
是为该机制引入之前创建的旧索引提供的后备方案。由于无法在事后为现有索引添加 k-NN 设置，将
``exact`` 模式的索引切换为 ``ann`` 模式需要重新创建索引（参阅 :ref:`semantic-search-migration`）。
另外，该判定结果会被缓存 60 秒，因此在重新创建索引之后，最多需要 60 秒才会反映出来。

分数阈值
----------

将 ``content_chunker.search.min_score`` 设置为某个余弦相似度（0-1）后，即使是相似度最高的分块
也达不到该值的文档，会被从语义搜索结果中排除（由于文档的分数取自其最佳分块的分数，因此该阈值
是以文档为单位生效的）。当没有词汇重叠的查询匹配范围过广时，可用它来控制命中数量::

    content_chunker.search.min_score=0.4

无论在 ``exact`` 还是 ``ann`` 模式下，该设置值都会被解释为余弦相似度（内部会转换为各模式对应的
分数标度）。

.. note::

   仅当 ``content_chunker.search.knn.space_type`` 为 ``cosinesimil``\ （默认值）时，该阈值才会
   生效。对于指定了 ``innerproduct`` / ``l2`` 的 ``ann`` 模式索引，由于无法定义余弦相似度，
   该阈值会在输出一次警告日志后被跳过。

限制事项
--------

- **若查询中包含检索语法，将跳过语义搜索**\ ，仅执行关键词搜索。该判定是针对查询组装\ **之后**\ 的
  字符串进行的：只要其中出现 ``"`` ``(`` ``)`` ``:`` ``[`` ``]`` ``{`` ``}`` ``^`` ``~`` ``*``
  ``?`` ``\``、``&&``、``||``、位于开头或紧跟空白之后的 ``+`` / ``-``\ ，或者大写的 ``AND`` /
  ``OR`` / ``NOT`` / ``TO``\ ，就会命中该判定。因此，即使用户本身并未输入检索语法，以下操作
  同样会被跳过。

  - 指定标签（内部会附加 ``label:"..."``\ ）
  - 指定排序条件（内部会附加 ``sort:...``\ ）
  - 通过分面进行筛选（内部会附加 ``filetype:...`` 等）
  - 高级搜索中的短语搜索、排除词、文件类型、站点指定、日期时间指定
  - 配置了相关查询的检索词（内部会展开为 ``("A" OR "B")``\ ）

  半角的 ``?`` 同样在判定范围内，因此像“……是什么?”这样以半角问号结尾的自然语句也会被跳过
  （全角的 ``？`` 不在范围内）。
- 与地理位置搜索（地理过滤）或相似文档搜索结合使用时，同样会被跳过。
- 在较深的页码上，Rank Fusion 本身会被禁用，结果将仅来自关键词搜索。分界由
  ``rank.fusion.window_size``\ （默认 ``200``）决定，默认情况下对应搜索结果的第 101 条及以后。
- 如果嵌入提供商不可访问，或发生搜索错误，|Fess| 会自动回退为仅使用关键词搜索的结果（搜索本身
  不会因此失败）。
- 基于角色和虚拟主机的访问控制同样适用于语义搜索结果。

与 AI 搜索模式的集成
======================

当启用 AI 搜索模式（:doc:`rag-chat`\ ，``rag.chat.enabled=true``）时，对于
``content_chunk_status`` 为 ``done`` 的文档，在生成回答时会计算各个分块的相似度，并
仅将相关性最高的前 ``content_chunker.chat.top_k`` 个分块（默认值：``3``）用作 LLM 的上下文。

此时用于计算嵌入的并不是用户的原始提问，而是\ **意图判定阶段由 LLM 生成的检索查询**\ （若发生
重新检索，则使用重新生成后的查询）。当没有生成检索查询时——例如用户要求对文档进行摘要——则不会
进行分块选择。

因此，即使是长文档，也只有相关部分会被传递给 LLM，这有助于提高回答准确性并减少 token 用量。
对于 ``content_chunk_status`` 为 ``chunked``\ （已有分块但没有向量）的文档，会改为基于关键词
（高亮）匹配来选择分块，而不是计算相似度。``skipped`` / ``fail`` 以及尚未处理的文档，仍会像
以前一样使用完整正文（或高亮摘录）。

此行为与 ``content_chunker.search.enabled`` 无关，但需要 ``content_chunker.enabled`` 处于启用
状态。另外，将所选分块拼接而成的文本同样会被 ``rag.chat.content.fulltext.max.length``\ （默认
``3000``）截断，因此即使调大 ``content_chunker.chat.top_k`` 或
``content_chunker.length.chunk_size``\ ，传递给 LLM 的字符数也不会超过该上限。

.. _semantic-search-migration:

从 15.7 及更早版本迁移
========================

如果您正在从 15.7 或更早版本升级 |Fess|，根据您当前对这些功能的使用情况，会属于以下四种情形之
一。请遵循适用于您的情形的说明。

全新安装
--------

无需额外操作。如果您想使用向量搜索，只需在首次启动 |Fess| 之前，按照本页的\ *配置参考*\ 章节配置
``system.properties``，正确的映射就会在索引首次创建时自动应用。（具体步骤请参阅上文的\ *配置步骤*\ 。）

.. note::

   如果您此前至少启动过一次 |Fess|\ （即索引已经存在），请改为遵循下面的\ *现有用户*\ 相关情形之
   一，而不是本情形。

现有用户且不想使用向量搜索
--------------------------

无需任何操作。``content_chunker.enabled`` 与 ``content_chunker.search.enabled`` 默认均为
``false``，因此升级后您的搜索结果和现有索引行为不会改变。新增的调度器任务 **Content Chunk
Vector Indexer** 会在启动时自动注册，但由于默认处于禁用状态，它不会运行，语义搜索器也不会被
注册到 Rank Fusion 中（该任务在每次启动时都会被注册，因此即使在管理界面中将其删除，下次启动时
也会以禁用状态重新创建）。

.. note::

   即使您不使用向量搜索，只要在 |Fess| 15.8 及以后\ **新建**\ 索引（包括重新索引），就会应用
   包含 ``content_chunk_vector``\ （``knn_vector`` 类型）的映射以及 ``index.knn: true``\ 。在
   OpenSearch 未安装 k-NN 插件的环境中，索引会在这一时刻创建失败。详情请参阅本页的“前提条件”。

现有用户且想启用向量搜索
------------------------

正在运行的索引不会自动获取新的映射，因此需要执行以下步骤。

1. 按照本页\ *配置参考*\ 中的说明，将设置应用到 ``system.properties``\ （若使用 opensearch
   提供商，具体步骤请参阅上文的\ *配置步骤*\ ）。
2. 重启 |Fess|\ 。
3. 在管理界面中，于「系统信息」→「维护」下运行「重新索引」，并启用「更新别名」。该操作会以
   后台异步方式进行，不会显示完成通知。``_cat/indices`` 只能说明新索引已存在，不能说明别名是否
   已切换——请改用 ``_cat/aliases`` 确认 ``fess.search``/``fess.update`` 是否已指向新索引
   （|Fess| 的日志只在失败时发出警告，安静不代表成功）。旧索引不会被自动删除（请在不再需要时
   手动删除），在此之前索引磁盘占用会大约翻倍。
4. 仅在确认上述别名切换已完成后，才在「系统」→「调度器」中启用并运行 Content Chunk Vector
   Indexer 任务（无需重新爬取：该任务会从现有索引的 ``_source`` 中读取 ``content`` 字段
   进行分块和嵌入）。

.. note::

   如果在步骤 1 中就一并写入 ``content_chunker.search.enabled=true``\ ，那么从步骤 2 的重启到
   步骤 4 完成之前，每次搜索都只会执行查询侧的嵌入，而结果中并不会体现出来。使用 ``openai`` /
   ``gemini`` 等按量计费的提供商时，请在步骤 4 完成之后再写入
   ``content_chunker.search.enabled=true`` 并重启。

若您之前使用 fess-webapp-semantic-search 插件
------------------------------------------------

在 |Fess| 15.7 及更早版本中提供语义搜索功能的 ``fess-webapp-semantic-search`` 插件，已在
15.8 中并入核心，现已\ **不再需要（已弃用）**\ 。除了上文\ *现有用户且想启用向量搜索*\ 中的步骤外，
您还需要执行以下操作。

1. **移除插件**：从 ``app/WEB-INF/plugin/`` 中删除 ``fess-webapp-semantic-search-*.jar``
   （在 Docker 中，请将其从 ``FESS_PLUGINS`` 中排除）。

2. **移除旧设置**：删除所有 ``-Dfess.semantic_search.*`` 启动选项。此外，如果您曾为旧插件指定
   ``-Drank.fusion.searchers=default,semantic``\ ，也请将其删除。若保留该设置，会导致新的语义
   搜索器（``semantic_chunk``）被排除在 Rank Fusion 之外，并在启动时记录警告日志。

3. **解除旧的 ingest pipeline**：如果之前设置过 ``-Dfess.semantic_search.pipeline``\ ，旧插件会在
   创建索引时把 ``default_pipeline``\ （用于神经搜索的 ingest pipeline）写入索引设置。
   **移除插件并不会移除该 pipeline**——它会继续留在索引上并持续运行——因此请务必在执行\ *现有用户且
   想启用向量搜索*\ 中的重新索引\ **之前**\ 将其解除。重新索引之后生成的新索引本来就不带该设置，
   所以之后再执行也没有意义。请先用 ``_cat/aliases`` 确认 ``fess.search`` 指向的
   ``fess.<timestamp>``\ ，并指定实体索引名而不是别名::

       curl -XPUT "http://localhost:9200/fess.<timestamp>/_settings" \
            -H "Content-Type: application/json" -d '
       {"index": {"default_pipeline": "_none"}}'

   即使解除了索引设置，ingest pipeline 本身仍会留在搜索引擎中。如果今后不再使用，请将其删除::

       curl -XDELETE "http://localhost:9200/_ingest/pipeline/<pipeline名>"

4. **添加新设置**：按照本页\ *配置参考*\ 中的说明，在 ``system.properties`` 中配置
   ``content_chunker.*``\ 。如果您要继续使用现有的 ML Commons 模型，请设置
   ``content_chunker.embedding.name=opensearch``\ ，并将其现有的 ``model_id`` 填入
   ``content_chunker.embedding.opensearch.model.id``\ 。

5. **重新创建索引并运行任务**：旧插件存储的向量字段（默认配置下为 ``content_vector``）与新的核心
   功能所使用的 ``content_chunk_vector`` 字段是不同的字段，因此旧的向量无法被新功能使用。另一
   方面，重新索引会原样复制 ``_source``\ ，所以旧向量仍会被复制到新索引中，并通过动态映射持续
   占用磁盘空间。建议在重新索引\ **之前**\ 先将其清除（如果您更改过字段名，请相应替换）::

       curl -XPOST "http://localhost:9200/fess.search/_update_by_query" \
            -H "Content-Type: application/json" -d '
       {
         "query": {"exists": {"field": "content_vector"}},
         "script": {"source": "ctx._source.remove(\"content_vector\")"}
       }'

   之后，请在「系统信息」→「维护」下运行「重新索引」，然后启用并运行 Content Chunk Vector
   Indexer 任务，重新生成向量。

注意事项
========

更改嵌入模型（维度）
----------------------

若要切换到维度不同的嵌入模型，请按以下顺序操作。

1. 删除现有的旧向量。如果残留着维度不同的旧向量就执行重新索引，新映射将无法接受这些向量，相应
   的文档不会被复制到新索引中，而处理仍会继续进行。由于 |Fess| 只检查重新索引的 HTTP 状态码，
   管理界面不会显示任何错误，文档却已经缺失::

       curl -XPOST "http://localhost:9200/fess.search/_update_by_query" \
            -H "Content-Type: application/json" -d '
       {
         "query": {"exists": {"field": "content_chunk_status"}},
         "script": {"source": "ctx._source.remove(\"content_chunk_vector\"); ctx._source.remove(\"content_chunk_status\")"}
       }'

   .. note::

      操作对象也可以指定为 ``fess.update``\ （重新索引时的读取来源别名）。另外，此操作不会改变
      ``content`` 字段，它仍保持分块数组的形态。下次任务运行时会重新拼接并再次切分，因此如果您为
      ``content_chunker.length.overlap`` 设置了非 0 的值，重叠部分会被重复计入后再切分。若对此
      有顾虑，请重新爬取相应的文档。

2. 更改 ``content_chunker.embedding.dimension`` 以及所用提供商的模型设置。
3. 按照“配置步骤”中的“3. 重新创建索引（在现有部署上启用时）”重新创建索引，并重新运行索引器
   任务。

磁盘使用量
----------

除搜索索引结构外，分块向量还会保留在 ``_source`` 中，因此每个文档会额外消耗与「分块数 ×
向量维度」成正比的磁盘空间。如果磁盘空间成为问题，请调整 ``content_chunker.length.chunk_size``
或 ``content_chunker.max_chunks_per_document``\ 。

chunk-only 模式
-----------------

设置 ``content_chunker.embedding.name=none`` 后，将只执行分块而不生成嵌入向量
（``content_chunk_status`` 会变为 ``chunked``）。这样一来，您可以在嵌入提供商就绪之前提前进行
分块；之后配置好提供商并重新运行任务时，系统只会为已存储的分块生成向量（不会重新分块）。

大规模语料库的内存配置
------------------------

索引器任务的子 JVM 通过 ``fess_config.properties`` 中的 ``jvm.chunk.options``\ （默认包含
``-Xms128m -Xmx1g`` 的 JVM 选项）启动。由于 ``content_chunker.job.max_documents_per_run``
默认无限制，单次运行会将所有待处理的文档 ID 保留在内存中。文档 ID 是 SHA-512 摘要（128 个字符），
每条约占用 200 字节堆内存；分块处理本身还需要 200-250MB 左右。因此，对于\ **超过 100 万至 200 万
文档**\ 的语料库，请提高 ``jvm.chunk.options`` 中的 ``-Xmx`` 值，或者为
``content_chunker.job.max_documents_per_run`` 设置一个有限值以分批执行。``jvm.chunk.options``
在 ``app/WEB-INF/classes/fess_config.properties``\ （RPM/DEB 软件包为
``/etc/fess/fess_config.properties``）中覆盖（有关 JVM 选项的概念，请参阅
:doc:`setup-memory`）。

同样的无限制默认值，在使用按量计费的嵌入提供商（``openai``、``gemini``）时还会带来成本上的
影响：首次索引器运行会一次性为现有语料库全部生成嵌入，相应的费用也会一次性产生。如果希望
将费用分摊到多次运行中，请为 ``content_chunker.job.max_documents_per_run`` 设置一个有限值。

参考信息
========

- :doc:`rank-fusion` - Rank Fusion（混合搜索）配置
- :doc:`rag-chat` - AI 搜索模式配置
- :doc:`llm-overview` - LLM 集成概述
- :doc:`llm-ollama` - Ollama 配置
- :doc:`setup-memory` - JVM 内存设置
- :doc:`../install/upgrade` - 升级步骤
