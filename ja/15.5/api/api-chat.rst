==========================
Chat API
==========================

概要
====

Chat APIは、|Fess| のRAGチャット機能にプログラムからアクセスするためのRESTful APIです。
検索結果を基にしたAI支援の回答を取得できます。

このAPIは2つのエンドポイントを提供します:

- **非ストリーミングAPI**: 完全な回答を一度に取得
- **ストリーミングAPI**: Server-Sent Events（SSE）形式でリアルタイムに回答を取得

前提条件
========

Chat APIを使用するには、以下の設定が必要です:

1. RAGチャット機能が有効になっていること（``rag.chat.enabled=true``）
2. LLMプロバイダーが設定されていること

詳細な設定方法は :doc:`../config/rag-chat` を参照してください。

非ストリーミングAPI
===================

エンドポイント
--------------

::

    POST /api/v1/chat

リクエストパラメーター
----------------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``message``
     - String
     - はい
     - ユーザーのメッセージ（質問）
   * - ``sessionId``
     - String
     - いいえ
     - セッションID。会話を継続する場合に指定
   * - ``clear``
     - String
     - いいえ
     - ``"true"`` を指定するとセッションをクリア

レスポンス
----------

**成功時（HTTP 200）**

.. code-block:: json

    {
      "status": "ok",
      "sessionId": "abc123def456",
      "content": "Fessは全文検索サーバーです。主な特徴として...",
      "sources": [
        {
          "title": "Fessの概要",
          "url": "https://fess.codelibs.org/ja/overview.html"
        },
        {
          "title": "機能一覧",
          "url": "https://fess.codelibs.org/ja/features.html"
        }
      ]
    }

**エラー時**

.. code-block:: json

    {
      "status": "error",
      "message": "Message is required"
    }

HTTPステータスコード
--------------------

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - コード
     - 説明
   * - 200
     - リクエスト成功
   * - 400
     - リクエストパラメーターが不正（messageが空など）
   * - 404
     - エンドポイントが見つからない
   * - 405
     - 許可されていないHTTPメソッド（POSTのみ許可）
   * - 500
     - サーバー内部エラー

使用例
------

cURL
~~~~

.. code-block:: bash

    # 新しいチャットを開始
    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "message=Fessとは何ですか？"

    # 会話を継続
    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "message=インストール方法を教えてください" \
         -d "sessionId=abc123def456"

    # セッションをクリア
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

    // 使用例
    const result = await chat('Fessの機能を教えてください');
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

    # 使用例
    result = chat('Fessのインストール方法は？')
    print(result['content'])
    print(f"Session ID: {result['sessionId']}")

ストリーミングAPI
=================

エンドポイント
--------------

::

    POST /api/v1/chat/stream
    GET /api/v1/chat/stream

リクエストパラメーター
----------------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``message``
     - String
     - はい
     - ユーザーのメッセージ（質問）
   * - ``sessionId``
     - String
     - いいえ
     - セッションID。会話を継続する場合に指定

レスポンス形式
--------------

ストリーミングAPIは ``text/event-stream`` 形式（Server-Sent Events）でレスポンスを返します。

各イベントは以下の形式です:

::

    event: <イベント名>
    data: <JSONデータ>

SSEイベント
-----------

**session**

セッション情報を通知します。ストリームの開始時に送信されます。

.. code-block:: json

    {
      "sessionId": "abc123def456"
    }

**phase**

処理フェーズの開始/完了を通知します。

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
      "keywords": "Fess インストール"
    }

.. code-block:: json

    {
      "phase": "search",
      "status": "complete"
    }

フェーズの種類:

- ``intent_analysis`` - 意図解析
- ``search`` - 検索実行
- ``evaluation`` - 結果評価
- ``generation`` - 回答生成

**chunk**

生成されたテキストの断片を通知します。

.. code-block:: json

    {
      "content": "Fessは"
    }

**sources**

参照元ドキュメントの情報を通知します。

.. code-block:: json

    {
      "sources": [
        {
          "title": "インストールガイド",
          "url": "https://fess.codelibs.org/ja/install.html"
        }
      ]
    }

**done**

処理完了を通知します。

.. code-block:: json

    {
      "sessionId": "abc123def456",
      "htmlContent": "<p>Fessは全文検索サーバーです...</p>"
    }

**error**

エラーを通知します。

.. code-block:: json

    {
      "phase": "generation",
      "message": "LLM request failed"
    }

使用例
------

cURL
~~~~

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v1/chat/stream" \
         -d "message=Fessの特徴を教えてください" \
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

      // POSTリクエストにはfetchを使用
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
        // チャンクを表示
        document.getElementById('output').textContent += data.content;
      } else if (data.phase) {
        // フェーズ情報を表示
        console.log(`Phase: ${data.phase} - ${data.status}`);
      } else if (data.sources) {
        // ソース情報を表示
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

    # 使用例
    for event in stream_chat('Fessの機能について教えてください'):
        if 'content' in event:
            print(event['content'], end='', flush=True)
        elif 'phase' in event:
            print(f"\n[Phase: {event['phase']} - {event['status']}]")

エラーハンドリング
==================

APIを使用する際は、適切なエラーハンドリングを実装してください。

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

レート制限
==========

Chat APIにはレート制限が適用されます。

デフォルト設定:

- 1分あたり10リクエスト

レート制限を超えた場合、HTTP 429エラーが返されます。

レート制限の設定は :doc:`../config/rag-chat` を参照してください。

セキュリティ
============

Chat APIを使用する際のセキュリティ上の注意点:

1. **認証**: 現在のバージョンではAPIに認証は不要ですが、本番環境では適切なアクセス制御を検討してください
2. **レート制限**: DoS攻撃を防ぐため、レート制限を有効にしてください
3. **入力検証**: クライアント側でも入力の検証を行ってください
4. **CORS**: 必要に応じてCORS設定を確認してください

参考情報
========

- :doc:`../config/rag-chat` - RAGチャット機能の設定
- :doc:`../config/llm-overview` - LLM統合の概要
- :doc:`../user/chat-search` - エンドユーザー向けチャット検索ガイド
- :doc:`api-overview` - API概要
