==========================
AI搜索模式功能配置
==========================

概述
====

AI搜索模式（RAG：检索增强生成）是通过LLM（大型语言模型）扩展 |Fess| 搜索结果，
以对话形式提供信息的功能。用户可以用自然语言提问，
获得基于搜索结果的详细回答。

|Fess| 15.6中，LLM功能已作为 ``fess-llm-*`` 插件分离提供。
核心配置及LLM提供商专属配置在 ``fess_config.properties`` 中进行，LLM提供商名称（ ``rag.llm.name`` ）
在 ``system.properties`` 或管理界面中进行。

AI搜索模式的工作原理
================

AI搜索模式通过以下多阶段流程运行。

1. **意图分析阶段**: 分析用户的问题，提取最适合搜索的关键词
2. **搜索阶段**: 使用提取的关键词通过 |Fess| 搜索引擎搜索文档
3. **查询再生成回退**: 当没有搜索结果时，LLM重新生成查询并重试搜索
4. **评估阶段**: 评估搜索结果的相关性，选择最合适的文档
5. **生成阶段**: LLM基于选择的文档生成回答
6. **输出阶段**: 向用户返回回答和来源信息（支持Markdown渲染）

通过此流程，可以提供比简单关键词搜索更理解上下文的高质量回答。
查询再生成可以在初始搜索查询不够理想时提高回答的覆盖范围。

基本配置
========

AI搜索模式功能的配置分为核心配置和提供商配置两部分。

核心配置 (fess_config.properties)
----------------------------------

启用AI搜索模式功能的基本配置。
在 ``app/WEB-INF/conf/fess_config.properties`` 中进行设置。

::

    # 启用AI搜索模式功能
    rag.chat.enabled=true

提供商配置 (system.properties / 管理界面)
-------------------------------------------------

LLM提供商的选择在管理界面或系统属性中进行。

**从管理界面配置时**:

在管理界面 > 系统 > 通用的设置画面中，选择要使用的LLM提供商。

**在system.properties中配置时**:

::

    # 选择LLM提供商（ollama, openai, gemini）
    rag.llm.name=ollama

有关LLM提供商的详细配置，请参阅以下内容:

- :doc:`llm-ollama` - Ollama配置
- :doc:`llm-openai` - OpenAI配置
- :doc:`llm-gemini` - Google Gemini配置

核心配置一览
============

可在 ``fess_config.properties`` 中设置的核心配置一览。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``rag.chat.enabled``
     - 启用AI搜索模式功能
     - ``false``
   * - ``rag.chat.context.max.documents``
     - 上下文中包含的最大文档数
     - ``5``
   * - ``rag.chat.session.timeout.minutes``
     - 会话超时时间（分钟）
     - ``30``
   * - ``rag.chat.session.max.size``
     - 可同时保持的最大会话数
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - 对话历史中保留的最大消息数
     - ``30``
   * - ``rag.chat.content.fields``
     - 从文档获取的字段
     - ``title,url,content,doc_id,content_title,content_description``
   * - ``rag.chat.message.max.length``
     - 用户消息的最大字符数
     - ``4000``
   * - ``rag.chat.highlight.fragment.size``
     - 高亮显示的片段大小
     - ``500``
   * - ``rag.chat.highlight.number.of.fragments``
     - 高亮显示的片段数
     - ``3``
   * - ``rag.chat.history.assistant.content``
     - 助手历史中包含的内容类型（ ``full`` / ``smart_summary`` / ``source_titles`` / ``source_titles_and_urls`` / ``truncated`` / ``none`` ）
     - ``smart_summary``

生成参数
================

|Fess| 15.6中，生成参数（最大token数、temperature等）按提供商
和提示词类型分别进行设置。这些配置不是核心配置，而是作为各 ``fess-llm-*``
插件的配置进行管理。

详情请参阅各提供商的文档:

- :doc:`llm-ollama` - Ollama生成参数配置
- :doc:`llm-openai` - OpenAI生成参数配置
- :doc:`llm-gemini` - Google Gemini生成参数配置

上下文配置
================

从搜索结果传递给LLM的上下文配置。

核心配置
--------

以下配置在 ``fess_config.properties`` 中进行。

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

提供商专属配置
-----------------------

以下配置按提供商在 ``fess_config.properties`` 中进行。

- ``rag.llm.{provider}.{promptType}.context.max.chars`` - 上下文最大字符数
- ``rag.llm.{provider}.chat.evaluation.max.relevant.docs`` - 评估阶段选择的最大相关文档数

``{provider}`` 处填入 ``ollama``、``openai``、``gemini`` 等提供商名称。
``{promptType}`` 处填入 ``chat``、``intent_analysis``、``evaluation`` 等提示词类型。

详情请参阅各提供商的文档。

内容字段
--------------------

``rag.chat.content.fields`` 可指定的字段:

- ``title`` - 文档标题
- ``url`` - 文档URL
- ``content`` - 文档正文
- ``doc_id`` - 文档ID
- ``content_title`` - 内容标题
- ``content_description`` - 内容描述

系统提示词
==================

|Fess| 15.6中，系统提示词不在属性文件中定义，而是在各 ``fess-llm-*``
插件的DI XML（``fess_llm++.xml``）中定义。

自定义提示词
-------------------------

如需自定义系统提示词，请覆盖插件JAR中的 ``fess_llm++.xml``。

1. 从正在使用的插件JAR文件中获取 ``fess_llm++.xml``
2. 进行必要的修改
3. 放置到 ``app/WEB-INF/`` 以下适当位置以进行覆盖

每种提示词类型（意图分析、评估、生成）都定义了不同的系统提示词，
并针对各自用途进行了优化。

详情请参阅各提供商的文档:

- :doc:`llm-ollama` - Ollama提示词配置
- :doc:`llm-openai` - OpenAI提示词配置
- :doc:`llm-gemini` - Google Gemini提示词配置

会话管理
==============

聊天会话管理相关配置。

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
     - 可同时保持的最大会话数
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - 对话历史中保留的最大消息数
     - ``30``

会话行为
----------------

- 用户开始新聊天时，创建新会话
- 会话中保存对话历史，可进行保持上下文的对话
- 超过超时时间后，会话自动删除
- 对话历史超过最大消息数时，从旧消息开始删除

并发控制
============

对LLM的请求并发数按提供商在 ``fess_config.properties`` 中控制。

::

    # 各提供商的最大并发请求数
    rag.llm.ollama.max.concurrent.requests=5
    rag.llm.openai.max.concurrent.requests=10
    rag.llm.gemini.max.concurrent.requests=10

并发控制的注意事项
-----------------------

- 请同时考虑LLM提供商端的速率限制进行设置
- 高负载环境中建议设置更小的值
- 达到并发数上限时，请求将进入队列依次处理

对话历史模式
============

``rag.chat.history.assistant.content`` 可以设置助手响应在对话历史中的存储方式。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 模式
     - 说明
   * - ``smart_summary``
     - （默认）保留响应的开头部分（60%）和结尾部分（40%），中间部分用省略标记替换。同时附加来源标题
   * - ``full``
     - 完整保留响应原文
   * - ``source_titles``
     - 仅保留来源标题
   * - ``source_titles_and_urls``
     - 保留来源标题和URL
   * - ``truncated``
     - 将响应截断到最大字符数
   * - ``none``
     - 不保留历史

.. note::

   在 ``smart_summary`` 模式下，可以高效保留长响应的上下文，同时减少token使用量。
   用户和助手的消息对按轮次分组，在字符预算内进行最优打包。
   历史的最大字符数和摘要的最大字符数由各 ``fess-llm-*`` 插件的 ``LlmClient`` 实现控制。

查询再生成
==========

当没有搜索结果或未找到相关结果时，LLM会自动重新生成查询并重试搜索。

- 搜索结果为零时：以原因 ``no_results`` 执行查询再生成
- 未找到相关文档时：以原因 ``no_relevant_results`` 执行查询再生成
- 再生成失败时回退到原始查询

此功能默认启用，并集成到同步和流式RAG流程中。
查询再生成提示词在各 ``fess-llm-*`` 插件中定义。

Markdown渲染
=============

AI搜索模式的响应以Markdown格式渲染。

- LLM的响应被解析为Markdown并转换为HTML
- 转换后的HTML经过清理，仅允许安全的标签和属性
- 支持标题、列表、代码块、表格、链接等Markdown语法
- 客户端使用 ``marked.js`` 和 ``DOMPurify``，服务端使用OWASP清理器

API使用
=========

AI搜索模式功能可通过REST API使用。

非流式API
-------------------

端点: ``POST /api/v1/chat``

参数:

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - 参数
     - 必需
     - 说明
   * - ``message``
     - 是
     - 用户消息
   * - ``sessionId``
     - 否
     - 会话ID（继续对话时）
   * - ``clear``
     - 否
     - ``true`` 时清除会话

请求示例:

::

    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "message=请告诉我Fess的安装方法"

响应示例:

::

    {
      "status": "ok",
      "sessionId": "abc123",
      "content": "Fess的安装方法是...",
      "sources": [
        {"title": "安装指南", "url": "https://..."}
      ]
    }

流式API
-----------------

端点: ``POST /api/v1/chat/stream``

以Server-Sent Events（SSE）格式流式返回响应。

参数:

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - 参数
     - 必需
     - 说明
   * - ``message``
     - 是
     - 用户消息
   * - ``sessionId``
     - 否
     - 会话ID（继续对话时）

请求示例:

::

    curl -X POST "http://localhost:8080/api/v1/chat/stream" \
         -d "message=请告诉我Fess的特点" \
         -H "Accept: text/event-stream"

SSE事件:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 事件
     - 说明
   * - ``phase``
     - 处理阶段的开始/完成（intent_analysis, search, evaluation, generation）
   * - ``chunk``
     - 生成的文本片段
   * - ``sources``
     - 参考文档信息
   * - ``done``
     - 处理完成（sessionId, htmlContent）。htmlContent包含Markdown渲染后的HTML字符串
   * - ``error``
     - 错误信息。提供超时、上下文长度超出、模型未找到、无效响应、连接错误等类型的具体消息

详细的API文档请参阅 :doc:`../api/api-chat`。

Web界面
===================

在 |Fess| 的Web界面中，可以从搜索画面使用AI搜索模式功能。

开始聊天
--------------

1. 访问 |Fess| 搜索画面
2. 点击聊天图标
3. 显示聊天面板

使用聊天
--------------

1. 在文本框中输入问题
2. 点击发送按钮或按Enter键
3. 显示AI助手的回答
4. 回答中包含参考来源的链接

继续对话
----------

- 可以在同一聊天会话内继续对话
- 可以获得考虑前一个问题上下文的回答
- 点击「新聊天」可重置会话

故障排除
======================

AI搜索模式无法启用
------------------------

**确认事项**:

1. 是否设置了 ``rag.chat.enabled=true``
2. 是否通过 ``rag.llm.name`` 正确配置了LLM提供商
3. 对应的 ``fess-llm-*`` 插件是否已安装
4. 是否可以连接到LLM提供商

回答质量低
----------------

**改进方法**:

1. 使用更高性能的LLM模型
2. 增加 ``rag.chat.context.max.documents``
3. 在DI XML中自定义系统提示词
4. 调整提供商专属的temperature设置（请参阅各 ``fess-llm-*`` 插件的文档）

响应慢
----------------

**改进方法**:

1. 使用更快的LLM模型（例: Gemini Flash）
2. 减少提供商专属的max.tokens设置（请参阅各 ``fess-llm-*`` 插件的文档）
3. 减少 ``rag.chat.context.max.documents``

会话无法保持
------------------------

**确认事项**:

1. 客户端是否正确发送sessionId
2. ``rag.chat.session.timeout.minutes`` 的设置
3. 会话存储的容量

调试设置
------------

调查问题时，可调整日志级别输出详细日志。

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm" level="DEBUG"/>
    <Logger name="org.codelibs.fess.api.chat" level="DEBUG"/>
    <Logger name="org.codelibs.fess.chat" level="DEBUG"/>

主要日志消息带有 ``[RAG]`` 前缀，
各阶段使用 ``[RAG:INTENT]``、``[RAG:EVAL]``、``[RAG:ANSWER]`` 等子前缀。
INFO级别输出聊天完成日志（耗时、来源数），DEBUG级别输出token使用量、
并发控制、历史打包的详细信息。

搜索日志与访问类型
------------------

通过AI搜索模式进行的搜索，会在搜索日志中以LLM提供商名称（如 ``ollama``、``openai``、``gemini``）作为访问类型记录。
这样可以在分析中区分AI搜索模式的搜索与普通Web搜索或API搜索。

参考信息
========

- :doc:`llm-overview` - LLM集成概述
- :doc:`llm-ollama` - Ollama配置
- :doc:`llm-openai` - OpenAI配置
- :doc:`llm-gemini` - Google Gemini配置
- :doc:`../api/api-chat` - Chat API参考
- :doc:`../user/chat-search` - 终端用户聊天搜索指南
