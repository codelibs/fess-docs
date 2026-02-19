==========================
AI模式功能配置
==========================

概述
====

AI模式（RAG：检索增强生成）是通过LLM（大型语言模型）扩展 |Fess| 搜索结果，
以对话形式提供信息的功能。用户可以用自然语言提问，
获得基于搜索结果的详细回答。

AI模式的工作原理
===================

AI模式通过以下多阶段流程运行。

1. **意图分析阶段**: 分析用户的问题，提取最适合搜索的关键词
2. **搜索阶段**: 使用提取的关键词通过 |Fess| 搜索引擎搜索文档
3. **评估阶段**: 评估搜索结果的相关性，选择最合适的文档
4. **生成阶段**: LLM基于选择的文档生成回答
5. **输出阶段**: 向用户返回回答和来源信息

通过此流程，可以提供比简单关键词搜索更理解上下文的高质量回答。

基本设置
========

启用AI模式功能的基本设置。

``app/WEB-INF/conf/fess_config.properties``:

::

    # 启用AI模式功能
    rag.chat.enabled=true

    # 选择LLM提供商（ollama, openai, gemini）
    rag.llm.type=ollama

LLM提供商的详细设置请参阅以下内容:

- :doc:`llm-ollama` - Ollama配置
- :doc:`llm-openai` - OpenAI配置
- :doc:`llm-gemini` - Google Gemini配置

生成参数
================

控制LLM生成行为的参数。

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
     - 生成的随机性（0.0〜1.0）
     - ``0.7``

temperature设置
---------------

- **0.0**: 确定性回答（对相同输入始终给出相同回答）
- **0.3〜0.5**: 一致性回答（适合基于事实的问题）
- **0.7**: 平衡的回答（默认）
- **1.0**: 创造性回答（适合头脑风暴等）

上下文设置
================

从搜索结果传递给LLM的上下文设置。

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
   * - ``rag.chat.evaluation.max.relevant.docs``
     - 评估阶段选择的最大相关文档数
     - ``3``

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

系统提示词定义LLM的基本行为。

默认设置
--------------

::

    rag.chat.system.prompt=You are an AI assistant for Fess search engine. Answer questions based on the search results provided. Always cite your sources using [1], [2], etc.

自定义示例
--------------

优先使用中文回答时:

::

    rag.chat.system.prompt=你是Fess搜索引擎的AI助手。请根据提供的搜索结果回答问题。回答请使用中文，并务必以[1]、[2]等格式标明出处。

专业领域定制:

::

    rag.chat.system.prompt=You are a technical documentation assistant. Provide detailed and accurate answers based on the search results. Include code examples when relevant. Always cite your sources using [1], [2], etc.

会话管理
==============

聊天会话管理相关设置。

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
     - 对话历史中保持的最大消息数
     - ``20``

会话行为
----------------

- 用户开始新聊天时，创建新会话
- 会话中保存对话历史，可进行保持上下文的对话
- 超过超时时间后，会话自动删除
- 对话历史超过最大消息数时，从旧消息开始删除

速率限制
==========

防止API过载的速率限制设置。

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

速率限制注意事项
--------------------

- 设置时也请考虑LLM提供商端的速率限制
- 高负载环境中建议设置更严格的限制
- 达到速率限制时，将向用户显示错误消息

API使用
=========

AI模式功能可通过REST API使用。

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
   * - ``session``
     - 会话信息（sessionId）
   * - ``phase``
     - 处理阶段的开始/完成（intent_analysis, search, evaluation, generation）
   * - ``chunk``
     - 生成的文本片段
   * - ``sources``
     - 参考文档信息
   * - ``done``
     - 处理完成（sessionId, htmlContent）
   * - ``error``
     - 错误信息

详细的API文档请参阅 :doc:`../api/api-chat`。

Web界面
===================

在 |Fess| 的Web界面中，可以从搜索画面使用AI模式功能。

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

AI模式无法启用
---------------------------

**确认事项**:

1. 是否设置了 ``rag.chat.enabled=true``
2. LLM提供商是否正确配置
3. 是否可以连接到LLM提供商

回答质量低
----------------

**改进方法**:

1. 使用更高性能的LLM模型
2. 增加 ``rag.chat.context.max.documents``
3. 自定义系统提示词
4. 调整 ``rag.chat.temperature``

响应慢
----------------

**改进方法**:

1. 使用更快的LLM模型（例: Gemini Flash）
2. 减少 ``rag.chat.max.tokens``
3. 减少 ``rag.chat.context.max.chars``

会话无法保持
------------------------

**确认事项**:

1. 客户端是否正确发送sessionId
2. ``rag.chat.session.timeout.minutes`` 的设置
3. 会话存储的容量

调试设置
------------

调查问题时，可以调整日志级别输出详细日志。

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm" level="DEBUG"/>
    <Logger name="org.codelibs.fess.api.chat" level="DEBUG"/>
    <Logger name="org.codelibs.fess.chat" level="DEBUG"/>

参考信息
========

- :doc:`llm-overview` - LLM集成概述
- :doc:`llm-ollama` - Ollama配置
- :doc:`llm-openai` - OpenAI配置
- :doc:`llm-gemini` - Google Gemini配置
- :doc:`../api/api-chat` - Chat API参考
- :doc:`../user/chat-search` - 终端用户聊天搜索指南
