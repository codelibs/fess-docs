==========================
Chat API
==========================

概要
====

Chat API は、 |Fess| の AI 検索モード（RAG チャット）機能にプログラムからアクセスするための v2 API です。
検索結果を基にした LLM による回答（補完）を取得できます。

このAPIは以下の3つのエンドポイントを提供します。

.. tabularcolumns:: |p{6cm}|p{9cm}|
.. list-table::
   :header-rows: 1

   * - エンドポイント
     - 説明
   * - ``POST /chat``
     - 一括（非ストリーミング）RAG チャット補完。
   * - ``POST /chat/stream``
     - ストリーミング RAG チャット補完（Server-Sent Events）。
   * - ``DELETE /chat/sessions/{session_id}``
     - チャットセッションの会話履歴をクリア。

ベースURLや共通のレスポンスエンベロープ・エラーコードについては :doc:`api-overview` を参照してください。

::

    http://<Server Name>/api/v2/

ローカル環境の例:

::

    http://localhost:8080/api/v2

前提条件
========

Chat API を使用するには、以下の設定が必要です。

1. AI 検索モード（RAG チャット）機能が有効になっていること（ ``rag.chat.enabled=true`` ）
2. LLM プロバイダーが設定されていること

機能が無効（ ``rag.chat.enabled=false`` ）の場合、リクエストは ``invalid_request`` エラーになります。

詳細な設定方法は :doc:`../config/rag-chat` および :doc:`../config/llm-overview` を参照してください。

認証とCSRF
==========

Chat API のすべてのエンドポイントは状態を変更するリクエスト（ ``POST`` / ``DELETE`` ）であるため、 ``X-Fess-CSRF-Token`` ヘッダーが必要です。
CSRF トークンの取得方法および認証・セッションの詳細は :doc:`api-overview` を参照してください。

レート制限
==========

``POST /chat`` 、 ``POST /chat/stream`` および ``DELETE /chat/sessions/{session_id}`` には、ユーザーごとのレート制限が適用されます。

- 既定値: 1分あたり30リクエスト（ユーザーごと）
- 設定キー: ``api.v2.chat.rate.limit.per.user.per.minute``
- 値を ``0`` 以下に設定するとレート制限は無効になります。

レート制限を超えた場合、 ``rate_limited`` エラー（HTTP 429）が返されます。 ``Retry-After`` ヘッダーには固定値 ``60`` （秒）が設定されます。
このレート制限は ``POST /chat`` 、 ``POST /chat/stream`` 、 ``DELETE /chat/sessions/{session_id}`` で共有されます。

.. note::

   レート制限はユーザーを識別できる場合にのみ適用されます。セッションが確立されておらずユーザーIDを解決できない匿名呼び出しでは、レート制限はスキップされます。

POST /chat
==========

同期的なチャット補完を行います。
セッションは ``session_id`` で識別します。 ``session_id`` を省略した場合、サーバーがセッションを作成し、レスポンスの ``session_id`` で返します。

``fields.label`` や ``extra_queries`` に渡された不正な値は、解決済みリクエストから無言で除去され、レスポンスエンベロープには表面化しません。

エンドポイント
--------------

::

    POST /api/v2/chat

リクエストボディ
----------------

``Content-Type: application/json`` の JSON ボディです。

リクエストボディのサイズ上限は 32 KiB です。これを超えると ``payload_too_large`` エラー（HTTP 413）になります。

.. tabularcolumns:: |p{3.5cm}|p{2.5cm}|p{1.5cm}|p{7cm}|
.. list-table:: ChatRequest
   :header-rows: 1

   * - フィールド
     - 型
     - 必須
     - 説明
   * - ``message``
     - string
     - はい
     - ユーザーのメッセージ（質問）。最大文字数は ``rag.chat.message.max.length`` （既定値 4000）で制限されます。超過した場合は ``invalid_request`` エラー（HTTP 400）になります。
   * - ``session_id``
     - string
     - いいえ
     - セッションID。省略時はサーバーが作成してレスポンスで返します。
   * - ``fields``
     - object
     - いいえ
     - 取得ステップ用の任意フィルターフィールド。
   * - ``fields.label``
     - string / string配列
     - いいえ
     - 許可リスト化されたラベルに取得を制限します。
   * - ``extra_queries``
     - string / string配列
     - いいえ
     - 許可リスト化されたファセットクエリ式。

リクエスト例:

.. code-block:: json

    {
      "message": "Fessとは何ですか？",
      "session_id": "abc123def456",
      "fields": {
        "label": "news"
      },
      "extra_queries": "label:faq"
    }

レスポンス
----------

**成功時（HTTP 200, ChatResponse）**

レスポンスは共通エンベロープ ``response`` に格納されます。 ``session_id`` は常に存在します。

.. tabularcolumns:: |p{3cm}|p{2.5cm}|p{9cm}|
.. list-table:: response の要素
   :header-rows: 1

   * - フィールド
     - 型
     - 説明
   * - ``session_id``
     - string
     - セッションID。
   * - ``content``
     - string (nullable)
     - 生成されたメッセージテキスト。常に存在しますが、モデルが内容を生成しなかった場合は ``null`` になりえます。
   * - ``sources``
     - array
     - 参照元ドキュメントの配列。各要素は ChatSource。

**ChatSource**

.. tabularcolumns:: |p{3cm}|p{2.5cm}|p{9cm}|
.. list-table:: ChatSource の要素
   :header-rows: 1

   * - フィールド
     - 型
     - 説明
   * - ``rank``
     - integer
     - 取得セット内の1始まりの位置。
   * - ``title``
     - string (nullable)
     - ドキュメントのタイトル。
   * - ``url``
     - string (nullable)
     - ドキュメントのURL。
   * - ``doc_id``
     - string (nullable)
     - ドキュメントID。
   * - ``snippet``
     - string (nullable)
     - スニペット。
   * - ``url_link``
     - string (nullable)
     - 表示用のURLリンク。
   * - ``go_url``
     - string (nullable)
     - リダイレクト用のURL。

レスポンス例:

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

HTTPステータスコード
--------------------

.. tabularcolumns:: |p{2cm}|p{13cm}|
.. list-table::
   :header-rows: 1

   * - コード
     - 説明
   * - 200
     - リクエスト成功。
   * - 400
     - リクエストが不正（ ``message`` の欠落、 ``message`` の最大長超過、 ``rag.chat.enabled=false`` など）。
   * - 403
     - CSRF トークンの欠落・失効など。
   * - 405
     - HTTP メソッドが許可されていません。
   * - 413
     - リクエストボディがサイズ上限（32 KiB）を超えています。
   * - 415
     - ``Content-Type`` が ``application/json`` でない、欠落している、または ``charset`` が UTF-8 以外です。
   * - 429
     - レート制限を超えました。
   * - 500
     - サーバー内部エラー。

cURL の例
---------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -d '{"message":"Fessとは何ですか？","session_id":"abc123def456"}'

POST /chat/stream
=================

ストリーミング形式でチャット補完を行います。
リクエストボディは ``POST /chat`` と同じ（ChatRequest）です。

成功レスポンスは ``text/event-stream`` 形式（Server-Sent Events）の名前付きイベントです。
各イベントは ``event: <名前>`` と ``data: <JSON>`` で構成されます。

ストリーム前のバリデーション失敗は、依然として JSON エンベロープを返します（ ``POST /chat`` と同じエラーコード）。
``fields.label`` や ``extra_queries`` に渡された不正な値は無言で除去され、レスポンスエンベロープにも SSE イベントにも表面化しません。

エンドポイント
--------------

::

    POST /api/v2/chat/stream

SSEイベント
-----------

.. tabularcolumns:: |p{2.5cm}|p{12.5cm}|
.. list-table::
   :header-rows: 1

   * - イベント
     - 説明（ペイロード）
   * - ``phase``
     - パイプラインのフェーズ遷移（ ``{ phase, status, message?, keywords?, hit_count?, ... }`` ）。 ``message`` と ``keywords`` は onPhaseStart で出力されます。追加の任意フィールド（例: ``hit_count`` ）は onPhaseComplete のペイロードから流れてきます。
   * - ``chunk``
     - 生成テキストの断片（ ``{ content }`` ）。
   * - ``sources``
     - 取得されたソース（ ``{ sources: [ChatSource] }`` ）。
   * - ``retry``
     - 一時的失敗のバックオフ（ ``{ phase, operation, attempt, max_attempts, sleep_ms, cause? }`` ）。
   * - ``waiting``
     - 長時間フェーズの進捗（ ``{ phase, reason, elapsed_ms, timeout_ms }`` ）。
   * - ``fallback``
     - クエリ書き換え・戦略フォールバック（ ``{ phase, reason, original_query?, new_query? }`` ）。
   * - ``warning``
     - 回復可能な警告（ ``{ phase, code, detail? }`` ）。
   * - ``done``
     - ストリーム終了（ ``{ session_id, html_content? }`` ）。
   * - ``error``
     - 終端のストリーム途中失敗（ ``{ phase?, message, error_code }`` ）。 ``message`` フィールドは ``error_code`` と同じ文字列を持ちます。クライアントは ``error_code`` を基にローカライズすべきです。

SSE ストリーム例:

::

    event: phase
    data: {"phase":"search","status":"start","message":"Searching documents...","keywords":"Fess インストール"}

    event: chunk
    data: {"content":"Fessは"}

    event: sources
    data: {"sources":[{"rank":1,"title":"インストールガイド","url":"https://fess.codelibs.org/ja/install.html"}]}

    event: done
    data: {"session_id":"abc123def456"}

HTTPステータスコード
--------------------

ストリーム前のバリデーションで失敗した場合は、以下のエラーコードが JSON エンベロープで返されます。

.. tabularcolumns:: |p{2cm}|p{13cm}|
.. list-table::
   :header-rows: 1

   * - コード
     - 説明
   * - 200
     - SSE ストリームを開始（成功）。
   * - 400
     - リクエストが不正（ ``message`` の欠落、 ``rag.chat.enabled=false`` など）。
   * - 403
     - CSRF トークンの欠落・失効など。
   * - 405
     - HTTP メソッドが許可されていません。
   * - 413
     - リクエストボディがサイズ上限（32 KiB）を超えています。
   * - 415
     - ``Content-Type`` が ``application/json`` でない、欠落している、または ``charset`` が UTF-8 以外です。
   * - 429
     - レート制限を超えました。
   * - 500
     - サーバー内部エラー。

cURL の例
---------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat/stream" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -H "Accept: text/event-stream" \
         --no-buffer \
         -d '{"message":"Fessの特徴を教えてください"}'

DELETE /chat/sessions/{session_id}
==================================

指定したチャットセッションの会話履歴をクリアします。
セッションはパスの ``session_id`` で識別します。

成功時には ``cleared: true`` が返ります。一致するアクティブセッションがないときは ``not_found`` エラー（HTTP 404）になります。

エンドポイント
--------------

::

    DELETE /api/v2/chat/sessions/{session_id}

パスパラメーター
----------------

.. tabularcolumns:: |p{3cm}|p{2cm}|p{10cm}|
.. list-table::
   :header-rows: 1

   * - パラメーター
     - 型
     - 説明
   * - ``session_id``
     - string
     - クリア対象のセッションID。minLength 1、maxLength 128、パターン ``^[A-Za-z0-9._-]+$`` 。

レスポンス
----------

**成功時（HTTP 200, ChatClearResponse）**

レスポンスは共通エンベロープ ``response`` に格納されます。 ``session_id`` と ``cleared`` は常に存在します。

.. tabularcolumns:: |p{3cm}|p{2.5cm}|p{9cm}|
.. list-table:: response の要素
   :header-rows: 1

   * - フィールド
     - 型
     - 説明
   * - ``session_id``
     - string
     - セッションID。
   * - ``cleared``
     - boolean
     - 常に ``true`` （セッションが見つかりクリアされたとき）。

レスポンス例:

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session_id": "abc123def456",
        "cleared": true
      }
    }

HTTPステータスコード
--------------------

.. tabularcolumns:: |p{2cm}|p{13cm}|
.. list-table::
   :header-rows: 1

   * - コード
     - 説明
   * - 200
     - セッションをクリアしました。
   * - 400
     - リクエストが不正です（ ``session_id`` がパターン ``^[A-Za-z0-9._-]+$`` または長さ制限（1〜128文字）に一致しない、 ``rag.chat.enabled=false`` など）。
   * - 403
     - CSRF トークンの欠落・失効など。
   * - 404
     - 一致するアクティブセッションが見つかりません。
   * - 405
     - HTTP メソッドが許可されていません。
   * - 429
     - レート制限を超えました。
   * - 500
     - サーバー内部エラー。

cURL の例
---------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/v2/chat/sessions/abc123def456" \
         -H "X-Fess-CSRF-Token: <token>"

セキュリティ
============

Chat API を使用する際のセキュリティ上の注意点:

1. **認証**: v2 API はセッションベースの認証を採用しています。詳細は :doc:`api-overview` を参照してください。
2. **CSRF**: 状態変更リクエストには ``X-Fess-CSRF-Token`` ヘッダーが必要です。
3. **レート制限**: DoS 攻撃を防ぐため、ユーザーごとのレート制限（既定 30/分）が適用されます。設定キーは ``api.v2.chat.rate.limit.per.user.per.minute`` です。

参考情報
========

- :doc:`../config/rag-chat` - AI 検索モード機能の設定
- :doc:`../config/llm-overview` - LLM 統合の概要
- :doc:`../user/chat-search` - エンドユーザー向けチャット検索ガイド
- :doc:`api-overview` - API概要
