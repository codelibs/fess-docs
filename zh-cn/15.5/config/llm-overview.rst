==========================
LLM集成概述
==========================

概述
====

|Fess| 15.5支持利用大型语言模型（LLM）的RAG（Retrieval-Augmented Generation）聊天功能。
通过此功能，用户可以以与AI助手对话的形式，基于搜索结果获取信息。

支持的提供商
============

|Fess| 支持以下LLM提供商。

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - 提供商
     - 配置值
     - 说明
   * - Ollama
     - ``ollama``
     - 在本地环境运行的开源LLM服务器。可运行Llama、Mistral、Gemma等模型。默认配置。
   * - OpenAI
     - ``openai``
     - OpenAI公司的云API。可使用GPT-4等模型。
   * - Google Gemini
     - ``gemini``
     - Google公司的云API。可使用Gemini模型。

架构
====

RAG聊天功能按以下流程运作。

1. **用户输入**: 用户在聊天界面输入问题
2. **意图分析**: LLM分析用户问题，提取搜索关键词
3. **执行搜索**: |Fess| 搜索引擎搜索相关文档
4. **结果评估**: LLM评估搜索结果的相关性，选择最佳文档
5. **生成回答**: LLM基于选定的文档生成回答
6. **来源引用**: 回答中包含参考文档的链接

基本配置
========

要启用LLM功能，请在 ``app/WEB-INF/conf/system.properties`` 中添加以下配置。

启用RAG聊天
-----------

::

    # 启用RAG聊天功能
    rag.chat.enabled=true

选择LLM提供商
-------------

::

    # 指定LLM提供商（ollama, openai, gemini）
    rag.llm.type=ollama

有关各提供商的详细配置，请参阅以下文档。

- :doc:`llm-ollama` - Ollama配置
- :doc:`llm-openai` - OpenAI配置
- :doc:`llm-gemini` - Google Gemini配置

通用配置
========

所有LLM提供商通用的配置项。

生成参数
--------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 说明
     - 默认值
   * - ``rag.chat.max.tokens``
     - 生成的最大令牌数
     - ``4096``
   * - ``rag.chat.temperature``
     - 生成的随机性（0.0~1.0）。越低回答越确定
     - ``0.7``

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
   * - ``rag.chat.context.max.chars``
     - 上下文的最大字符数
     - ``4000``
   * - ``rag.chat.content.fields``
     - 从文档获取的字段
     - ``title,url,content,...``

系统提示词
----------

::

    rag.chat.system.prompt=You are an AI assistant for Fess search engine. Answer questions based on the search results provided. Always cite your sources using [1], [2], etc.

此提示词定义LLM的基本行为。可根据需要自定义。

可用性检查
----------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 说明
     - 默认值
   * - ``rag.llm.availability.check.interval``
     - 检查LLM可用性的间隔（秒）。设为0禁用
     - ``60``

此配置使 |Fess| 定期检查LLM提供商的连接状态。

会话管理
========

聊天会话相关配置。

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
     - 对话历史保留的最大消息数
     - ``20``

速率限制
========

防止API过载的速率限制配置。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 说明
     - 默认值
   * - ``rag.chat.rate.limit.enabled``
     - 启用速率限制
     - ``true``
   * - ``rag.chat.rate.limit.requests.per.minute``
     - 每分钟最大请求数
     - ``10``

评估配置
========

搜索结果评估相关配置。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 说明
     - 默认值
   * - ``rag.chat.evaluation.max.relevant.docs``
     - 评估阶段选择的最大相关文档数
     - ``3``

后续步骤
========

- :doc:`llm-ollama` - Ollama详细配置
- :doc:`llm-openai` - OpenAI详细配置
- :doc:`llm-gemini` - Google Gemini详细配置
- :doc:`rag-chat` - RAG聊天功能详细配置

