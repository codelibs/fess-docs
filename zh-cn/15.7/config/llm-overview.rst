==============================
LLM 集成概述
==============================

概述
====

|Fess| 支持利用大型语言模型（LLM）的 AI 搜索模式（RAG：Retrieval-Augmented Generation）功能。
通过此功能，用户可以以与 AI 助手对话的形式，基于搜索结果获取信息。

LLM 集成功能以 ``fess-llm-*`` 插件的形式提供。请安装与所用 LLM 提供商对应的插件。

支持的提供商
============

|Fess| 支持以下 LLM 提供商。

.. list-table::
   :header-rows: 1
   :widths: 20 20 30 30

   * - 提供商
     - 配置值
     - 插件
     - 说明
   * - Ollama
     - ``ollama``
     - ``fess-llm-ollama``
     - 在本地环境运行的开源 LLM 服务器。可运行 Llama、Mistral、Gemma 等模型。默认配置。
   * - OpenAI
     - ``openai``
     - ``fess-llm-openai``
     - OpenAI 公司的云 API。可使用 GPT-4 等模型。
   * - Google Gemini
     - ``gemini``
     - ``fess-llm-gemini``
     - Google 公司的云 API。可使用 Gemini 模型。

插件安装
========

LLM 功能以插件形式提供。需要将与所用提供商对应的 ``fess-llm-{provider}`` 插件 JAR 文件放置到插件目录。

以使用 OpenAI 提供商为例，请下载 ``fess-llm-openai-15.7.0.jar`` 并放置到以下目录。

::

    app/WEB-INF/plugin/

放置后，重启 |Fess| 即可加载插件。

架构
====

AI 搜索模式功能按以下流程运作。

1. **用户输入**: 用户在聊天界面输入问题
2. **意图解析（intent）**: LLM 分析用户问题，提取搜索关键词
3. **执行搜索（search）**: |Fess| 搜索引擎搜索相关文档
4. **结果评估（evaluate）**: LLM 评估搜索结果的相关性，选择最优文档
5. **查询再生成（根据需要）**: 当没有搜索结果，或评估未找到相关文档时，LLM 重新生成查询并重新搜索
6. **内容获取（fetch）**: 获取所选文档的正文内容
7. **回答生成（answer）**: LLM 基于获取的文档生成回答（支持 Markdown 渲染）
8. **来源引用**: 回答中包含参考文档的链接

.. note::

   内部处理由 ``intent`` 、 ``search`` 、 ``evaluate`` 、 ``fetch`` 、 ``answer`` 五个阶段构成，各阶段的进度通过流式传输（SSE）通知客户端。

基本配置
========

LLM 功能的配置在以下两处进行。

管理界面的通用设置 / system.properties
--------------------------------------

在管理界面的通用设置或 ``system.properties`` 中进行配置。用于选择 LLM 提供商。

::

    # 指定LLM提供商（ollama, openai, gemini）
    rag.llm.name=ollama

fess_config.properties
----------------------

在 ``app/WEB-INF/conf/fess_config.properties`` 中进行配置。用于启用 AI 搜索模式、会话及历史记录相关设置，以及提供商专属配置（连接 URL、API 密钥、生成参数等）。

::

    # 启用AI搜索模式功能
    rag.chat.enabled=true

    # 提供商专属配置示例（以OpenAI为例）
    rag.llm.openai.api.key=sk-...
    rag.llm.openai.answer.temperature=0.7

有关各提供商的详细配置，请参阅以下文档。

- :doc:`llm-ollama` - Ollama 的配置
- :doc:`llm-openai` - OpenAI 的配置
- :doc:`llm-gemini` - Google Gemini 的配置

通用配置
========

所有 LLM 提供商通用的配置项。这些在 ``fess_config.properties`` 中进行设置。

上下文配置
----------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 说明
     - 默认值
   * - ``rag.chat.context.max.documents``
     - 上下文中包含的最大文档数
     - ``5``
   * - ``rag.chat.content.fields``
     - 从文档获取的字段
     - ``title,url,content,doc_id,content_title,content_description``

.. note::

   上下文最大字符数（ ``context.max.chars`` ）已更改为按提供商和提示类型分别配置。请在 ``fess_config.properties`` 中以 ``rag.llm.{provider}.{promptType}.context.max.chars`` 的形式进行设置。

系统提示
--------

系统提示在各插件的 DI XML 文件中进行管理，而非属性文件。

各 ``fess-llm-*`` 插件的 JAR 文件内包含的 ``fess_llm++.xml`` 文件中定义了系统提示。由于该文件是打包在插件 JAR 中的类路径资源，如需自定义提示，需要编辑 JAR 内的 DI XML 文件。

可用性检查
----------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``rag.llm.{provider}.availability.check.interval``
     - 检查 LLM 可用性的间隔（秒）。设为 0 可禁用
     - ``60``

此配置在 ``fess_config.properties`` 中进行。 |Fess| 会定期检查 LLM 提供商的连接状态。

会话管理
========

聊天会话相关配置。这些在 ``fess_config.properties`` 中进行设置。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 说明
     - 默认值
   * - ``rag.chat.session.timeout.minutes``
     - 会话超时时间（分钟）
     - ``30``
   * - ``rag.chat.session.max.size``
     - 最大会话数
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - 对话历史中保留的最大消息数
     - ``30``

并发控制
========

控制对 LLM 请求并发数的配置。在 ``fess_config.properties`` 中进行设置。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``rag.llm.{provider}.max.concurrent.requests``
     - 对提供商的最大并发请求数
     - ``5``
   * - ``rag.llm.{provider}.concurrency.wait.timeout``
     - 并发数达到上限时，等待空闲的最长时间（毫秒）。在此时间内未获得空闲时将返回速率限制错误
     - ``30000``

例如，设置 OpenAI 提供商的并发数时如下所示。

::

    rag.llm.openai.max.concurrent.requests=10

评估配置
========

搜索结果评估相关配置。在 ``fess_config.properties`` 中进行设置。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``rag.llm.{provider}.chat.evaluation.max.relevant.docs``
     - 评估阶段选择的最大相关文档数
     - ``3``

按提示类型配置
==============

可以按提示类型分别设置生成参数。这样可以根据用途进行精细调整。配置在 ``fess_config.properties`` 中进行。

提示类型一览
------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - 提示类型
     - 配置值
     - 说明
   * - 意图解析
     - ``intent``
     - 分析用户问题，提取搜索关键词
   * - 评估
     - ``evaluation``
     - 评估搜索结果的相关性
   * - 问题不明确
     - ``unclear``
     - 当问题不明确时生成响应
   * - 无搜索结果
     - ``noresults``
     - 当未找到搜索结果时生成响应
   * - 文档不存在
     - ``docnotfound``
     - 当对应文档不存在时生成响应
   * - 回答生成
     - ``answer``
     - 基于搜索结果生成回答
   * - 摘要
     - ``summary``
     - 生成文档摘要
   * - FAQ
     - ``faq``
     - 生成 FAQ 形式的回答
   * - 直接回答
     - ``direct``
     - 不经过搜索直接生成回答
   * - 查询再生成
     - ``queryregeneration``
     - 当没有搜索结果时重新生成查询

配置模式
--------

按提示类型的配置以如下模式指定。

::

    rag.llm.{provider}.{promptType}.temperature
    rag.llm.{provider}.{promptType}.max.tokens
    rag.llm.{provider}.{promptType}.context.max.chars

配置示例（以 OpenAI 提供商为例）:

::

    # 将回答生成的temperature设低
    rag.llm.openai.answer.temperature=0.5
    # 回答生成的最大token数
    rag.llm.openai.answer.max.tokens=4096
    # 意图解析只需短回答，设置较低值
    rag.llm.openai.intent.max.tokens=256
    # 摘要的上下文最大字符数
    rag.llm.openai.summary.context.max.chars=8000

.. note::

   ``temperature`` 、 ``max.tokens`` 、 ``context.max.chars`` 可在所有提供商中通用。此外，各提供商还支持 ``thinking.budget`` 、 ``top.p`` 、 ``reasoning.effort`` 等提供商专属参数。详情请参阅各提供商的文档。

后续步骤
========

- :doc:`llm-ollama` - Ollama 详细配置
- :doc:`llm-openai` - OpenAI 详细配置
- :doc:`llm-gemini` - Google Gemini 详细配置
- :doc:`rag-chat` - AI 搜索模式功能详细配置
- :doc:`rank-fusion` - Rank Fusion 配置（混合搜索结果融合）
