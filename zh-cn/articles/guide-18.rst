================================
启用语义搜索，查找意思相近的文档
================================

前言
====

用户搜索“我想换一张领薪水的银行卡”，而公司规章里写的是“工资账户变更手续”，关键词搜索就找不到这份文档。
在 Fess 15.9 中，将正文转换为表示语义的向量再进行搜索的“语义搜索”已内置于本体，无需插件即可使用（根据嵌入模型的连接目标，有时需要添加插件）。

按照本文的步骤操作后，您将能够：

- 区分语义搜索能发挥作用的场景与关键词搜索就已足够的场景
- 使用 Docker 立即运行已配置好语义搜索的环境
- 在现有的 Fess 上配置 ``content_chunker.*``，并通过索引器任务生成向量
- 通过 ``searcher`` 字段确认搜索结果是否由向量搜索找到

AI 搜索模式（RAG）的配置在 :doc:`guide-19` 中介绍。

语义搜索能发挥作用的场景
========================

Fess 的语义搜索并不取代关键词搜索（BM25）。
它以“混合搜索”的方式工作：同时执行关键词搜索和向量搜索，再用 Rank Fusion（RRF）将结果合并为一个排名。

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 语义搜索能发挥作用
     - 关键词搜索就已足够
   * - 用户与文档的用词不同（“领薪水的银行卡”与“工资账户”，“在家上班”与“远程办公”）
     - 使用与文档相同的字符串查找，如产品型号、错误代码、人名等
   * - 用句子提问（“怎么申请新电脑”）
     - 换种说法的组合很少，可以全部登记到同义词词典中
   * - 想用中文搜索找到英文文档（需要支持多语言的嵌入模型）
     - 使用短语、通配符等搜索语法（此时向量搜索本身不会执行）

如果换种说法的组合有限，先尝试同义词词典会更简便。
根据搜索日志中的零命中词登记同义词的步骤，请参阅 :doc:`guide-08`。

Fess 内部的处理流程
===================

#. 爬虫照常将文档登记到索引中。此时还没有向量。
#. 调度器任务 ``Content Chunk Vector Indexer`` 找出未处理的文档，将正文切分为分块（片段），为每个分块生成嵌入向量并保存到 ``content_chunk_vector`` 字段。结果记录在 ``content_chunk_status`` 字段中。
#. 当 ``content_chunker.search.enabled=true`` 时，每次搜索都会执行关键词搜索（搜索器名 ``default``）和向量搜索（搜索器名 ``semantic_chunk``），并用 RRF 融合。

该任务默认处于禁用状态，也不与爬取联动。
请注意，仅添加配置并不会生成向量，搜索结果也仍然只是关键词搜索的结果。

前提条件
========

**带有 k-NN 插件的 OpenSearch**

无论是否使用语义搜索，Fess 15.9 创建的搜索索引都包含 ``knn_vector`` 类型的字段。
Docker 的 ``ghcr.io/codelibs/fess-opensearch`` 镜像和标准发行版 OpenSearch 都包含 k-NN 插件。
在不包含 k-NN 插件的 minimal 发行版中，无法创建索引，Fess 也无法启动。

**嵌入提供商**

通过 ``content_chunker.embedding.name`` 选择将文本转换为向量的模型的连接目标。

.. list-table::
   :header-rows: 1
   :widths: 18 32 50

   * - 设置值
     - 所需条件
     - 说明
   * - ``opensearch``\ （默认）
     - 无需额外插件
     - 使用部署在 OpenSearch ML Commons 中的模型
   * - ``ollama``
     - 插件 ``fess-llm-ollama``
     - 使用 Ollama 的嵌入模型（默认模型为 ``embeddinggemma``）
   * - ``openai``
     - 插件 ``fess-llm-openai``
     - 使用 OpenAI 的嵌入 API（默认模型为 ``text-embedding-3-small``）
   * - ``gemini``
     - 插件 ``fess-llm-gemini``
     - 使用 Google Gemini 的嵌入 API
   * - ``bedrock``
     - 插件 ``fess-llm-bedrock``
     - 使用 Amazon Bedrock 的嵌入模型

请安装与 Fess 相同次版本（15.9.x）的插件，并在安装后重启 Fess。
OpenAI、Gemini 和 Bedrock 按用量计费，首次执行任务时会一次性产生全部现有文档的使用费用。

最快的方法：用 docker-semanticsearch 试用
=========================================

docker-semanticsearch 仓库通过 Docker Compose 启动已配置好语义搜索的 Fess 15.9。
它会自动将多语言嵌入模型（``paraphrase-multilingual-MiniLM-L12-v2``，384 维）部署到 OpenSearch 的 ML Commons，并完成索引器任务的启用。

::

    $ git clone --branch v15.9.0 https://github.com/codelibs/docker-semanticsearch.git
    $ cd docker-semanticsearch
    $ FESS_THEMES_REF=15.9.x bash ./bin/setup.sh
    $ docker compose up -d
    $ docker compose logs -f init-semantic init-fess-chunk

``setup.sh`` 会从 ``fess-themes`` 仓库获取搜索页面的主题 ``semanticlens``。
``v15.9.0`` 的默认获取来源 ``main`` 上的主题面向 Fess 15.10 及以后版本（``minFessVersion: 15.10``），因此通过 ``FESS_THEMES_REF`` 指定包含 15.9 用主题的 ``15.9.x`` 分支。

首次启动时下载模型（约 490MB）需要几分钟。
当 ``docker compose ps -a`` 中 ``fess01`` 变为 healthy，且 ``init-semantic`` 和 ``init-fess-chunk`` 变为 ``Exited (0)`` 时，即准备就绪。

之后与普通 Fess 一样，在管理界面（\ ``http://localhost:8080/admin``\ ）中创建爬取配置并执行爬取。
在此配置中，索引器任务每小时运行一次。
如需立即生成向量，请在 [系统] > [调度器] 中打开 ``Content Chunk Vector Indexer``，然后点击 [立即开始]。

除本文后半部分说明的配置外，此配置还使用以下值：

- 在 OpenSearch 端进行融合（\ ``rank.fusion.engine.enabled=true``\ ）
- 分块长度为 250 个字符（因为模型的输入上限为 128 个 token）
- 相似度下限 ``content_chunker.search.min_score=0.5``
- 主题 ``semanticlens``，为每条搜索结果显示其是由关键词搜索、语义搜索还是两者共同找到的

值的修改方法请参阅仓库 README 中的 Configuration 部分。

在现有的 Fess 上启用语义搜索
============================

这里以使用 Ollama 的 ``embeddinggemma``\ （768 维，支持多语言）为例说明步骤。
使用内置的 ``opensearch`` 提供商时，请代替步骤 1、2，将模型部署到 ML Commons，并设置 ``content_chunker.embedding.name=opensearch`` 和 ``content_chunker.embedding.opensearch.model.id``。
具体步骤见 `语义搜索 <https://fess.codelibs.org/zh-cn/stable/config/search-semantic.html>`__ 中的“配置步骤（以 opensearch 提供商为例）”。

步骤 1：安装插件
----------------

在 [系统] > [插件] > [安装] 中选择 ``fess-llm-ollama`` 的 15.9.x 进行安装，然后重启 Fess。
使用 Docker 时，在 ``compose.yaml`` 的 ``fess01`` 中指定 ``FESS_PLUGINS=fess-llm-ollama:15.9.0``。

步骤 2：准备嵌入模型
--------------------

在运行 Ollama 的服务器上拉取模型。

::

    $ ollama pull embeddinggemma

步骤 3：在 system.properties 中写入配置
---------------------------------------

``content_chunker.*`` 的配置只从 ``system.properties`` 读取。
写在 ``fess_config.properties`` 中或通过 ``-Dfess.config.`` 指定都会被忽略。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 安装方式
     - 写入位置
   * - ZIP 版
     - ``app/WEB-INF/conf/system.properties``
   * - RPM/DEB 版
     - ``/etc/fess/system.properties``
   * - Docker（docker-fess）
     - 在 ``compose.yaml`` 的 ``FESS_JAVA_OPTS`` 中以 ``-Dfess.system.<键名>=<值>`` 的形式指定

Docker 容器内的 ``/opt/fess/system.properties`` 也会被读取，但 docker-fess 的 ``fess01`` 没有卷，执行 ``docker compose down`` 后就会消失。

写入以下内容：

::

    content_chunker.enabled=true
    content_chunker.embedding.name=ollama
    content_chunker.embedding.dimension=768
    content_chunker.embedding.ollama.api.url=http://localhost:11434
    content_chunker.embedding.ollama.model=embeddinggemma
    content_chunker.search.enabled=true

``api.url`` 是从 Fess 看到的 Ollama 地址。
如果 Fess 运行在 Docker 中，``localhost`` 指向容器自身，请改为从容器可以访问到的地址。

``content_chunker.embedding.dimension`` 必须与模型的输出维数一致。
该值会在创建索引时写入映射，之后无法更改。

步骤 4：重启 Fess
-----------------

将 ``content_chunker.search.enabled`` 改为 ``true`` 的变更在重启之前不会生效（其他 ``content_chunker.*`` 会在运行中重新读取）。

步骤 5：重新创建现有索引
------------------------

在曾经启动过 Fess 的环境中，新维数的映射尚未反映到索引上。
在 [系统信息] > [维护] 的「重新索引」中启用「更新别名」，然后点击 [开始]。
在首次启动前就已完成步骤 3 的新环境中无需此操作。

重新索引在后台异步进行，界面上不会显示完成。
进入下一步之前，请确认 ``fess.search`` 和 ``fess.update`` 两个别名都指向新索引（\ ``fess.<时间戳>``\ ）。

::

    $ curl -s "http://localhost:9200/_cat/aliases/fess.search,fess.update?v"

旧索引不会被自动删除，确认完成后请手动删除。
无需重新爬取。
索引器任务会根据已保存的正文生成向量。

步骤 6：启用并执行索引器任务
----------------------------

#. 在 [系统] > [调度器] 中打开 ``Content Chunk Vector Indexer``，点击 [编辑]。
#. 勾选「状态」中的「启用」，如有需要修改调度计划，然后点击 [更新]。默认调度计划为 ``0 13 * * *``\ （每天 13:00）。
#. 返回详情页面后会显示 [立即开始]，点击它执行一次。

由于该任务不与爬取联动，爬取到的文档虽然可以立即通过关键词搜索到，但要等到该任务下次运行之后才会成为向量搜索的对象。
请将调度时间设置在爬取任务结束之后。

确认运行情况
============

确认向量是否已生成
------------------

让 OpenSearch 汇总每个文档的处理结果。

::

    $ curl -s -XPOST "http://localhost:9200/fess.search/_search" \
        -H "Content-Type: application/json" -d '
    {"size": 0, "aggs": {"status": {"terms": {"field": "content_chunk_status", "missing": "pending"}}}}'

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 值
     - 含义
   * - ``pending``
     - 未处理（将在下次任务执行时处理）。被重新爬取的文档也会回到此状态
   * - ``done``
     - 分块切分和向量生成已完成
   * - ``chunked``
     - 仅完成分块切分。未安装提供商插件时也会处于此状态
   * - ``skipped``
     - 正文为空，或分块数超过上限（默认 1000）
   * - ``fail``
     - 失败。请在日志文件 ``fess-chunk.log`` 中确认原因

如果每次执行任务后 ``pending`` 减少、``done`` 增加，说明运行顺利。

确认结果是否由向量搜索找到
--------------------------

搜索结果的 ``searcher`` 字段中包含找到该文档的搜索器名称。
默认情况下它不包含在搜索 API 的响应中，因此请在 ``fess_config.properties`` 中添加以下一行并重启（Docker 中为 ``-Dfess.config.query.additional.api.response.fields=searcher``）。

::

    query.additional.api.response.fields=searcher

用关键词与文档不一致的换种说法进行搜索。
如果有说明“工资账户变更手续”的文档，可以这样搜索：

::

    $ curl -s -G "http://localhost:8080/api/v2/search" \
        --data-urlencode "q=我想换一张领薪水的银行卡" \
      | jq '.response.data[] | {title, searcher}'

``searcher`` 为 ``["semantic_chunk"]`` 的结果是仅由向量搜索找到的文档，``["default", "semantic_chunk"]`` 则是两者都找到的文档。
如果所有结果都只有 ``["default"]``，说明向量搜索没有返回结果。
请查看下一节。

常见问题
========

**残留了旧插件时代的 rank.fusion.searchers**

15.7 及更早版本的 ``fess-webapp-semantic-search`` 插件需要指定 ``-Drank.fusion.searchers=default,semantic``。
15.9 的搜索器名为 ``semantic_chunk``，如果此设置仍然存在，语义搜索不会执行，只返回关键词搜索的结果。
启动时会输出 ``rank.fusion.searchers allows 'semantic' but not 'semantic_chunk'`` 这条 WARN 日志。
请同时检查 JVM 选项和 [系统] > [通用] 中的「系统属性」栏，删除此设置（不指定时会使用全部搜索器）。
从旧插件迁移的步骤请参阅 `语义搜索 <https://fess.codelibs.org/zh-cn/stable/config/search-semantic.html>`__ 中的“从 15.7 及更早版本迁移”。

**包含搜索语法的查询不会执行向量搜索**

以下查询只通过关键词搜索处理：

- 短语（\ ``"..."``\ ）、通配符、模糊搜索、范围指定
- 以半角 ``?`` 结尾的句子（如“……是什么?”）。全角“？”不在此列
- 排除（\ ``-词``\ 、\ ``NOT 词``\ ）和加权（\ ``词^2``\ ）
- 指定了排序的搜索

使用 ``label:``\ 、\ ``site:`` 或分面进行筛选不会有问题，因为它们也会作为过滤条件应用于向量搜索。

**维数不一致，或在未设置的情况下创建了索引**

如果未设置 ``content_chunker.embedding.dimension`` 就创建了索引，映射会变为 768 维，任务会将文档标记为 ``fail``。
如果模型的维数不是 768，请设置正确的值，然后重新执行步骤 5 的重新索引。
``fail`` 和 ``skipped`` 即使再次执行任务也不会被重新处理。
排除原因后，请临时设置 ``content_chunker.job.retry_failed=true`` 并执行任务。

**更换了嵌入模型**

已保存的向量是用旧模型生成的，因此只更换模型会破坏搜索精度（即使维数相同也不会报错）。
删除 ``content_chunk_vector`` 和 ``content_chunk_status`` 并重新执行任务的步骤，见参考文档的“注意事项”。

**关联不大的文档也排到了前面**

向量搜索会按相近程度依次返回文档，即使相似度很低。
在 ``content_chunker.search.min_score`` 中设置余弦相似度的下限（0～1），即可排除未达到该值的文档。
合适的值因模型和文档而异，请一边用曾经零命中的词和无关的词进行搜索，一边调整。

**第 2 页以后的后半部分结果倾向发生变化**

在 Fess 端进行融合的默认配置中，只有各搜索器的前 200 条（\ ``rank.fusion.window_size``\ ）参与融合，第 101 条以后的结果只来自关键词搜索。
命中数也会增加仅由向量搜索找到的文档数。
融合机制和调整项（\ ``rank.fusion.rank_constant``\ 、在 OpenSearch 端融合）请参阅 `混合搜索与 Rank Fusion <https://fess.codelibs.org/zh-cn/stable/config/rank-fusion.html>`__。

与 AI 搜索模式、多模态搜索的关系
================================

AI 搜索模式（RAG）在不启用语义搜索的情况下也可以使用。
对于已通过 ``content_chunker.enabled=true`` 生成向量的文档，用于回答的正文会被限定为与问题相近的分块，因此即使是长文档也能将相关部分传给 LLM。
AI 搜索模式的配置请参阅 :doc:`guide-19`。

同时搜索图像和文本的多模态搜索（\ ``fess-webapp-multimodal``\ ）不能在同一个 Fess 中与本文的文本语义搜索同时使用。
详情请参阅 :doc:`guide-21`。

延伸阅读
========

- 想用同义词或关键词匹配改善搜索日志中的零命中词：:doc:`guide-08`
- 想让生成式 AI 根据内部文档回答问题：:doc:`guide-19`
- 想连同图像一起搜索：:doc:`guide-21`
- 想通过搜索 API 从业务系统中搜索：:doc:`guide-11`

参考资料
========

- `语义搜索（内容分块 + 向量搜索） <https://fess.codelibs.org/zh-cn/stable/config/search-semantic.html>`__
- `混合搜索与 Rank Fusion（语义 + 关键词） <https://fess.codelibs.org/zh-cn/stable/config/rank-fusion.html>`__
- `Ollama配置（本地 LLM / RAG） <https://fess.codelibs.org/zh-cn/stable/config/llm-ollama.html>`__
- `调度器 <https://fess.codelibs.org/zh-cn/stable/admin/scheduler-guide.html>`__
- `维护 <https://fess.codelibs.org/zh-cn/stable/admin/maintenance-guide.html>`__
- `插件 <https://fess.codelibs.org/zh-cn/stable/admin/plugin-guide.html>`__
- `docker-semanticsearch（GitHub） <https://github.com/codelibs/docker-semanticsearch>`__
