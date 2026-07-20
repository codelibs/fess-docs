==========================
Chat API
==========================

概述
====

Chat API 是用于以编程方式访问 |Fess| AI 搜索模式（RAG 聊天）功能的 v2 API。
可基于搜索结果获取 LLM 生成的回答（补全）。

本 API 提供以下 3 个端点。

.. tabularcolumns:: |p{6cm}|p{9cm}|
.. list-table::
   :header-rows: 1

   * - 端点
     - 说明
   * - ``POST /chat``
     - 批量（非流式）RAG 聊天补全。
   * - ``POST /chat/stream``
     - 流式 RAG 聊天补全（Server-Sent Events）。
   * - ``DELETE /chat/sessions/{session_id}``
     - 清除聊天会话的对话历史。

有关基础 URL、公共响应信封及错误码，请参阅 :doc:`api-overview`。

::

    http://<Server Name>/api/v2/

本地环境示例：

::

    http://localhost:8080/api/v2

前提条件
========

使用 Chat API 需要满足以下配置：

1. AI 搜索模式（RAG 聊天）功能已启用（\ ``rag.chat.enabled=true``\ ）
2. 已配置 LLM 提供商

当功能未启用（\ ``rag.chat.enabled=false``\ ）时，请求会返回 ``invalid_request`` 错误。

详细配置方法请参阅 :doc:`../config/rag-chat` 和 :doc:`../config/llm-overview`。

认证与 CSRF
===========

Chat API 的所有端点均为修改状态的请求（\ ``POST`` / ``DELETE``\ ），因此需要携带 ``X-Fess-CSRF-Token`` 头。
有关 CSRF 令牌的获取方式及认证与会话的详情，请参阅 :doc:`api-overview`。

速率限制
========

``POST /chat`` 、 ``POST /chat/stream`` 和 ``DELETE /chat/sessions/{session_id}`` 适用每用户速率限制。

- 默认值：每分钟 30 个请求（每用户）
- 配置键：\ ``api.v2.chat.rate.limit.per.user.per.minute``
- 将值设置为 ``0`` 以下时，速率限制将被禁用。

超过速率限制时，返回 ``rate_limited`` 错误（HTTP 429）。\ ``Retry-After`` 头将设为固定值 ``60``\ （秒）。
该速率限制由 ``POST /chat`` 、 ``POST /chat/stream`` 、 ``DELETE /chat/sessions/{session_id}`` 共享。

.. note::

   速率限制仅在能够识别用户时适用。未建立会话且无法解析用户 ID 的匿名调用，将跳过速率限制。

POST /chat
==========

以同步方式进行聊天补全。
会话由 ``session_id`` 标识。省略 ``session_id`` 时，服务器会创建会话并在响应的 ``session_id`` 中返回。

``fields.label`` 或 ``extra_queries`` 中传入的无效值，会从已解析的请求中静默移除，不会出现在响应信封中。

端点
----

::

    POST /api/v2/chat

请求体
------

以 ``Content-Type: application/json`` 发送 JSON 请求体。

请求体大小上限为 32 KiB。超过该限制将返回 ``payload_too_large`` 错误（HTTP 413）。

.. tabularcolumns:: |p{3.5cm}|p{2.5cm}|p{1.5cm}|p{7cm}|
.. list-table:: ChatRequest
   :header-rows: 1

   * - 字段
     - 类型
     - 必填
     - 说明
   * - ``message``
     - string
     - 是
     - 用户消息（问题）。最大长度由 ``rag.chat.message.max.length``\ （默认值 4000）限制，超过时返回 ``invalid_request`` 错误（HTTP 400）。
   * - ``session_id``
     - string
     - 否
     - 会话 ID。省略时由服务器创建并在响应中返回。
   * - ``fields``
     - object
     - 否
     - 用于检索步骤的任意过滤字段。
   * - ``fields.label``
     - string / string 数组
     - 否
     - 将检索限制在允许列表中的标签。
   * - ``extra_queries``
     - string / string 数组
     - 否
     - 允许列表中的分面查询表达式。

请求示例：

.. code-block:: json

    {
      "message": "Fessとは何ですか？",
      "session_id": "abc123def456",
      "fields": {
        "label": "news"
      },
      "extra_queries": "label:faq"
    }

响应
----

**成功时（HTTP 200，ChatResponse）**

响应存储在公共信封 ``response`` 中。\ ``session_id`` 始终存在。

.. tabularcolumns:: |p{3cm}|p{2.5cm}|p{9cm}|
.. list-table:: response 的元素
   :header-rows: 1

   * - 字段
     - 类型
     - 说明
   * - ``session_id``
     - string
     - 会话 ID。
   * - ``content``
     - string (nullable)
     - 生成的消息文本。始终存在，但模型未生成内容时可为 ``null``\ 。
   * - ``sources``
     - array
     - 引用来源文档的数组。每个元素为 ChatSource。

**ChatSource**

.. tabularcolumns:: |p{3cm}|p{2.5cm}|p{9cm}|
.. list-table:: ChatSource 的元素
   :header-rows: 1

   * - 字段
     - 类型
     - 说明
   * - ``rank``
     - integer
     - 在检索集中从 1 开始的位置。
   * - ``title``
     - string (nullable)
     - 文档标题。
   * - ``url``
     - string (nullable)
     - 文档 URL。
   * - ``doc_id``
     - string (nullable)
     - 文档 ID。
   * - ``snippet``
     - string (nullable)
     - 摘要片段。
   * - ``url_link``
     - string (nullable)
     - 用于显示的 URL 链接。
   * - ``go_url``
     - string (nullable)
     - 用于重定向的 URL。

响应示例：

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session_id": "abc123def456",
        "content": "Fessは全文検索サーバーです。主な特徴として...",
        "sources": [
          {
            "rank": 1,
            "title": "Fessの概要",
            "url": "https://fess.codelibs.org/ja/overview.html",
            "doc_id": "abcdef0123456789",
            "snippet": "Fessは...",
            "url_link": "https://fess.codelibs.org/ja/overview.html",
            "go_url": "/go/?docId=abcdef0123456789"
          }
        ]
      }
    }

HTTP 状态码
-----------

.. tabularcolumns:: |p{2cm}|p{13cm}|
.. list-table::
   :header-rows: 1

   * - 状态码
     - 说明
   * - 200
     - 请求成功。
   * - 400
     - 请求不合法（缺少 ``message``\ 、\ ``message`` 超过最大长度、\ ``rag.chat.enabled=false`` 等）。
   * - 403
     - CSRF 令牌缺失或过期等。
   * - 405
     - 不允许使用该 HTTP 方法。
   * - 413
     - 请求体超过大小限制（32 KiB）。
   * - 415
     - ``Content-Type`` 不是 ``application/json``\ 、缺失或 ``charset`` 不是 UTF-8。
   * - 429
     - 超过速率限制。
   * - 500
     - 服务器内部错误。

cURL 示例
---------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -d '{"message":"Fessとは何ですか？","session_id":"abc123def456"}'

POST /chat/stream
=================

以流式方式进行聊天补全。
请求体与 ``POST /chat`` 相同（ChatRequest）。

成功响应为 ``text/event-stream`` 格式（Server-Sent Events）的命名事件。
每个事件由 ``event: <名称>`` 和 ``data: <JSON>`` 组成。

流式传输前的验证失败仍会返回 JSON 信封（与 ``POST /chat`` 相同的错误码）。
``fields.label`` 或 ``extra_queries`` 中传入的无效值会被静默移除，不会出现在响应信封或 SSE 事件中。

端点
----

::

    POST /api/v2/chat/stream

SSE 事件
--------

.. tabularcolumns:: |p{2.5cm}|p{12.5cm}|
.. list-table::
   :header-rows: 1

   * - 事件
     - 说明（载荷）
   * - ``phase``
     - 流水线阶段转换（\ ``{ phase, status, message?, keywords?, hit_count?, ... }``\ ）。\ ``message`` 和 ``keywords`` 在 onPhaseStart 时输出。附加的可选字段（例如 ``hit_count``\ ）来自 onPhaseComplete 的载荷。
   * - ``chunk``
     - 生成文本的片段（\ ``{ content }``\ ）。
   * - ``sources``
     - 已检索到的来源（\ ``{ sources: [ChatSource] }``\ ）。
   * - ``retry``
     - 临时失败的退避（\ ``{ phase, operation, attempt, max_attempts, sleep_ms, cause? }``\ ）。
   * - ``waiting``
     - 长时间阶段的进度（\ ``{ phase, reason, elapsed_ms, timeout_ms }``\ ）。
   * - ``fallback``
     - 查询改写或策略回退（\ ``{ phase, reason, original_query?, new_query? }``\ ）。
   * - ``warning``
     - 可恢复的警告（\ ``{ phase, code, detail? }``\ ）。
   * - ``done``
     - 流结束（\ ``{ session_id, html_content? }``\ ）。
   * - ``error``
     - 流终止的中途失败（\ ``{ phase?, message, error_code }``\ ）。\ ``message`` 字段与 ``error_code`` 持有相同字符串。客户端应基于 ``error_code`` 进行本地化。

SSE 流示例：

::

    event: phase
    data: {"phase":"search","status":"start","message":"Searching documents...","keywords":"Fess インストール"}

    event: chunk
    data: {"content":"Fessは"}

    event: sources
    data: {"sources":[{"rank":1,"title":"インストールガイド","url":"https://fess.codelibs.org/ja/install.html"}]}

    event: done
    data: {"session_id":"abc123def456"}

HTTP 状态码
-----------

流式传输前的验证失败时，以下错误码以 JSON 信封返回。

.. tabularcolumns:: |p{2cm}|p{13cm}|
.. list-table::
   :header-rows: 1

   * - 状态码
     - 说明
   * - 200
     - SSE 流已启动（成功）。
   * - 400
     - 请求不合法（缺少 ``message``\ 、\ ``rag.chat.enabled=false`` 等）。
   * - 403
     - CSRF 令牌缺失或过期等。
   * - 405
     - 不允许使用该 HTTP 方法。
   * - 413
     - 请求体超过大小限制（32 KiB）。
   * - 415
     - ``Content-Type`` 不是 ``application/json``\ 、缺失或 ``charset`` 不是 UTF-8。
   * - 429
     - 超过速率限制。
   * - 500
     - 服务器内部错误。

cURL 示例
---------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat/stream" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -H "Accept: text/event-stream" \
         --no-buffer \
         -d '{"message":"Fessの特徴を教えてください"}'

DELETE /chat/sessions/{session_id}
===================================

清除指定聊天会话的对话历史。
会话由路径中的 ``session_id`` 标识。

成功时返回 ``cleared: true``\ 。当没有匹配的活动会话时，返回 ``not_found`` 错误（HTTP 404）。

端点
----

::

    DELETE /api/v2/chat/sessions/{session_id}

路径参数
--------

.. tabularcolumns:: |p{3cm}|p{2cm}|p{10cm}|
.. list-table::
   :header-rows: 1

   * - 参数
     - 类型
     - 说明
   * - ``session_id``
     - string
     - 要清除的会话 ID。minLength 为 1，maxLength 为 100，格式 ``^[A-Za-z0-9._-]+$``\ 。

响应
----

**成功时（HTTP 200，ChatClearResponse）**

响应存储在公共信封 ``response`` 中。\ ``session_id`` 和 ``cleared`` 始终存在。

.. tabularcolumns:: |p{3cm}|p{2.5cm}|p{9cm}|
.. list-table:: response 的元素
   :header-rows: 1

   * - 字段
     - 类型
     - 说明
   * - ``session_id``
     - string
     - 会话 ID。
   * - ``cleared``
     - boolean
     - 始终为 ``true``\ （当会话已找到并清除时）。

响应示例：

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session_id": "abc123def456",
        "cleared": true
      }
    }

HTTP 状态码
-----------

.. tabularcolumns:: |p{2cm}|p{13cm}|
.. list-table::
   :header-rows: 1

   * - 状态码
     - 说明
   * - 200
     - 会话已清除。
   * - 400
     - 请求不合法（\ ``session_id`` 不符合格式 ``^[A-Za-z0-9._-]+$`` 或长度限制（1～100 字符）、\ ``rag.chat.enabled=false`` 等）。
   * - 403
     - CSRF 令牌缺失或过期等。
   * - 404
     - 找不到匹配的活动会话。
   * - 405
     - 不允许使用该 HTTP 方法。
   * - 429
     - 超过速率限制。
   * - 500
     - 服务器内部错误。

cURL 示例
---------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/v2/chat/sessions/abc123def456" \
         -H "X-Fess-CSRF-Token: <token>"

安全注意事项
============

使用 Chat API 时的安全注意事项：

1. **认证**：v2 API 采用基于会话的认证方式。详情请参阅 :doc:`api-overview`。
2. **CSRF**：修改状态的请求需要携带 ``X-Fess-CSRF-Token`` 头。
3. **速率限制**：为防止 DoS 攻击，适用每用户速率限制（默认 30 次/分钟）。配置键为 ``api.v2.chat.rate.limit.per.user.per.minute``\ 。

参考信息
========

- :doc:`../config/rag-chat` - AI 搜索模式功能配置
- :doc:`../config/llm-overview` - LLM 集成概述
- :doc:`../user/chat-search` - 终端用户聊天搜索指南
- :doc:`api-overview` - API 概述
