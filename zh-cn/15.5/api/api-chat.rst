==========================
Chat API
==========================

概述
====

Chat API是用于从程序访问 |Fess| AI模式功能的RESTful API。
可以获取基于搜索结果的AI辅助回答。

此API提供两个端点:

- **非流式API**: 一次性获取完整回答
- **流式API**: 以Server-Sent Events（SSE）格式实时获取回答

前提条件
========

使用Chat API需要以下设置:

1. AI模式功能已启用（``rag.chat.enabled=true``）
2. LLM提供商已配置

详细配置方法请参阅 :doc:`../config/rag-chat`。

非流式API
===================

端点
--------------

::

    POST /api/v1/chat

请求参数
----------------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 参数
     - 类型
     - 必需
     - 说明
   * - ``message``
     - String
     - 是
     - 用户消息（问题）
   * - ``sessionId``
     - String
     - 否
     - 会话ID。继续对话时指定
   * - ``clear``
     - String
     - 否
     - 指定 ``"true"`` 时清除会话

响应
----------

**成功时（HTTP 200）**

.. code-block:: json

    {
      "status": "ok",
      "sessionId": "abc123def456",
      "content": "Fess是全文搜索服务器。主要特点有...",
      "sources": [
        {
          "title": "Fess概述",
          "url": "https://fess.codelibs.org/ja/overview.html"
        },
        {
          "title": "功能列表",
          "url": "https://fess.codelibs.org/ja/features.html"
        }
      ]
    }

**错误时**

.. code-block:: json

    {
      "status": "error",
      "message": "Message is required"
    }

HTTP状态码
--------------------

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - 代码
     - 说明
   * - 200
     - 请求成功
   * - 400
     - 请求参数无效（message为空等）
   * - 404
     - 端点未找到
   * - 405
     - 不允许的HTTP方法（仅允许POST）
   * - 500
     - 服务器内部错误

使用示例
------

cURL
~~~~

.. code-block:: bash

    # 开始新聊天
    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "message=什么是Fess？"

    # 继续对话
    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "message=请告诉我安装方法" \
         -d "sessionId=abc123def456"

    # 清除会话
    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "sessionId=abc123def456" \
         -d "clear=true"

JavaScript
~~~~~~~~~~

.. code-block:: javascript

    async function chat(message, sessionId = null) {
      const params = new URLSearchParams();
      params.append('message', message);
      if (sessionId) {
        params.append('sessionId', sessionId);
      }

      const response = await fetch('/api/v1/chat', {
        method: 'POST',
        body: params
      });

      return await response.json();
    }

    // 使用示例
    const result = await chat('请告诉我Fess的功能');
    console.log(result.content);
    console.log('Session ID:', result.sessionId);

Python
~~~~~~

.. code-block:: python

    import requests

    def chat(message, session_id=None):
        data = {'message': message}
        if session_id:
            data['sessionId'] = session_id

        response = requests.post(
            'http://localhost:8080/api/v1/chat',
            data=data
        )
        return response.json()

    # 使用示例
    result = chat('Fess的安装方法是？')
    print(result['content'])
    print(f"Session ID: {result['sessionId']}")

流式API
=================

端点
--------------

::

    POST /api/v1/chat/stream
    GET /api/v1/chat/stream

请求参数
----------------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 参数
     - 类型
     - 必需
     - 说明
   * - ``message``
     - String
     - 是
     - 用户消息（问题）
   * - ``sessionId``
     - String
     - 否
     - 会话ID。继续对话时指定

响应格式
--------------

流式API以 ``text/event-stream`` 格式（Server-Sent Events）返回响应。

每个事件的格式如下:

::

    event: <事件名>
    data: <JSON数据>

SSE事件
-----------

**session**

通知会话信息。在流开始时发送。

.. code-block:: json

    {
      "sessionId": "abc123def456"
    }

**phase**

通知处理阶段的开始/完成。

.. code-block:: json

    {
      "phase": "intent_analysis",
      "status": "start",
      "message": "Analyzing user intent..."
    }

.. code-block:: json

    {
      "phase": "search",
      "status": "start",
      "message": "Searching documents...",
      "keywords": "Fess 安装"
    }

.. code-block:: json

    {
      "phase": "search",
      "status": "complete"
    }

阶段类型:

- ``intent_analysis`` - 意图分析
- ``search`` - 搜索执行
- ``evaluation`` - 结果评估
- ``generation`` - 回答生成

**chunk**

通知生成的文本片段。

.. code-block:: json

    {
      "content": "Fess是"
    }

**sources**

通知参考文档信息。

.. code-block:: json

    {
      "sources": [
        {
          "title": "安装指南",
          "url": "https://fess.codelibs.org/ja/install.html"
        }
      ]
    }

**done**

通知处理完成。

.. code-block:: json

    {
      "sessionId": "abc123def456",
      "htmlContent": "<p>Fess是全文搜索服务器...</p>"
    }

**error**

通知错误。

.. code-block:: json

    {
      "phase": "generation",
      "message": "LLM request failed"
    }

使用示例
------

cURL
~~~~

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v1/chat/stream" \
         -d "message=请告诉我Fess的特点" \
         -H "Accept: text/event-stream" \
         --no-buffer

JavaScript（EventSource）
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: javascript

    function streamChat(message, sessionId = null) {
      const params = new URLSearchParams();
      params.append('message', message);
      if (sessionId) {
        params.append('sessionId', sessionId);
      }

      // POST请求使用fetch
      return fetch('/api/v1/chat/stream', {
        method: 'POST',
        body: params
      }).then(response => {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        function read() {
          return reader.read().then(({ done, value }) => {
            if (done) return;

            const text = decoder.decode(value);
            const lines = text.split('\n');

            for (const line of lines) {
              if (line.startsWith('data: ')) {
                const data = JSON.parse(line.slice(6));
                handleEvent(data);
              }
            }

            return read();
          });
        }

        return read();
      });
    }

    function handleEvent(data) {
      if (data.content) {
        // 显示片段
        document.getElementById('output').textContent += data.content;
      } else if (data.phase) {
        // 显示阶段信息
        console.log(`Phase: ${data.phase} - ${data.status}`);
      } else if (data.sources) {
        // 显示来源信息
        console.log('Sources:', data.sources);
      }
    }

Python
~~~~~~

.. code-block:: python

    import requests

    def stream_chat(message, session_id=None):
        data = {'message': message}
        if session_id:
            data['sessionId'] = session_id

        response = requests.post(
            'http://localhost:8080/api/v1/chat/stream',
            data=data,
            stream=True,
            headers={'Accept': 'text/event-stream'}
        )

        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    import json
                    data = json.loads(line[6:])
                    yield data

    # 使用示例
    for event in stream_chat('请告诉我Fess的功能'):
        if 'content' in event:
            print(event['content'], end='', flush=True)
        elif 'phase' in event:
            print(f"\n[Phase: {event['phase']} - {event['status']}]")

错误处理
==================

使用API时，请实现适当的错误处理。

.. code-block:: javascript

    async function chatWithErrorHandling(message, sessionId = null) {
      try {
        const params = new URLSearchParams();
        params.append('message', message);
        if (sessionId) {
          params.append('sessionId', sessionId);
        }

        const response = await fetch('/api/v1/chat', {
          method: 'POST',
          body: params
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.message || 'API request failed');
        }

        const result = await response.json();

        if (result.status === 'error') {
          throw new Error(result.message);
        }

        return result;

      } catch (error) {
        console.error('Chat API error:', error);
        throw error;
      }
    }

速率限制
==========

Chat API应用速率限制。

默认设置:

- 每分钟10个请求

超过速率限制时，返回HTTP 429错误。

速率限制设置请参阅 :doc:`../config/rag-chat`。

安全性
============

使用Chat API时的安全注意事项:

1. **认证**: 当前版本API不需要认证，但在生产环境中请考虑适当的访问控制
2. **速率限制**: 为防止DoS攻击，请启用速率限制
3. **输入验证**: 客户端也请进行输入验证
4. **CORS**: 根据需要确认CORS设置

参考信息
========

- :doc:`../config/rag-chat` - AI模式功能配置
- :doc:`../config/llm-overview` - LLM集成概述
- :doc:`../user/chat-search` - 终端用户聊天搜索指南
- :doc:`api-overview` - API概述
