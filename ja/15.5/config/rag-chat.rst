==========================
RAGチャット機能の設定
==========================

概要
====

RAG（Retrieval-Augmented Generation）チャットは、|Fess| の検索結果をLLM（大規模言語モデル）で拡張し、
対話形式で情報を提供する機能です。ユーザーは自然言語で質問し、検索結果を基にした
詳細な回答を得ることができます。

RAGチャットの仕組み
===================

RAGチャットは以下の多段階フローで動作します。

1. **意図解析フェーズ**: ユーザーの質問を分析し、検索に最適なキーワードを抽出
2. **検索フェーズ**: 抽出したキーワードで |Fess| の検索エンジンを使用して文書を検索
3. **評価フェーズ**: 検索結果の関連性を評価し、最も適切な文書を選択
4. **生成フェーズ**: 選択した文書を基にLLMが回答を生成
5. **出力フェーズ**: 回答とソース情報をユーザーに返す

このフローにより、単純なキーワード検索よりも文脈を理解した高品質な回答が可能になります。

基本設定
========

RAGチャット機能を有効にするための基本設定です。

``app/WEB-INF/conf/system.properties``:

::

    # RAGチャット機能を有効にする
    rag.chat.enabled=true

    # LLMプロバイダーを選択（ollama, openai, gemini）
    rag.llm.type=ollama

LLMプロバイダーの詳細設定については、以下を参照してください:

- :doc:`llm-ollama` - Ollamaの設定
- :doc:`llm-openai` - OpenAIの設定
- :doc:`llm-gemini` - Google Geminiの設定

生成パラメーター
================

LLMの生成動作を制御するパラメーターです。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.chat.max.tokens``
     - 生成する最大トークン数
     - ``4096``
   * - ``rag.chat.temperature``
     - 生成のランダム性（0.0〜1.0）
     - ``0.7``

temperature設定
---------------

- **0.0**: 決定的な回答（同じ入力に対して常に同じ回答）
- **0.3〜0.5**: 一貫性のある回答（事実に基づく質問に適切）
- **0.7**: バランスの取れた回答（デフォルト）
- **1.0**: 創造的な回答（ブレインストーミング等に適切）

コンテキスト設定
================

検索結果からLLMに渡すコンテキストの設定です。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.chat.context.max.documents``
     - コンテキストに含める最大ドキュメント数
     - ``5``
   * - ``rag.chat.context.max.chars``
     - コンテキストの最大文字数
     - ``4000``
   * - ``rag.chat.content.fields``
     - ドキュメントから取得するフィールド
     - ``title,url,content,...``
   * - ``rag.chat.evaluation.max.relevant.docs``
     - 評価フェーズで選択する最大関連ドキュメント数
     - ``3``

コンテンツフィールド
--------------------

``rag.chat.content.fields`` で指定できるフィールド:

- ``title`` - ドキュメントのタイトル
- ``url`` - ドキュメントのURL
- ``content`` - ドキュメントの本文
- ``doc_id`` - ドキュメントID
- ``content_title`` - コンテンツのタイトル
- ``content_description`` - コンテンツの説明

システムプロンプト
==================

システムプロンプトは、LLMの基本的な振る舞いを定義します。

デフォルト設定
--------------

::

    rag.chat.system.prompt=You are an AI assistant for Fess search engine. Answer questions based on the search results provided. Always cite your sources using [1], [2], etc.

カスタマイズ例
--------------

日本語での回答を優先する場合:

::

    rag.chat.system.prompt=あなたはFess検索エンジンのAIアシスタントです。提供された検索結果に基づいて質問に回答してください。回答は日本語で行い、出典を[1]、[2]などの形式で必ず明記してください。

専門分野向けのカスタマイズ:

::

    rag.chat.system.prompt=You are a technical documentation assistant. Provide detailed and accurate answers based on the search results. Include code examples when relevant. Always cite your sources using [1], [2], etc.

セッション管理
==============

チャットセッションの管理に関する設定です。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.chat.session.timeout.minutes``
     - セッションのタイムアウト時間（分）
     - ``30``
   * - ``rag.chat.session.max.size``
     - 同時に保持できるセッションの最大数
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - 会話履歴に保持する最大メッセージ数
     - ``20``

セッションの動作
----------------

- ユーザーが新しいチャットを開始すると、新しいセッションが作成されます
- セッションには会話履歴が保存され、文脈を維持した対話が可能です
- タイムアウト時間を経過すると、セッションは自動的に削除されます
- 会話履歴が最大メッセージ数を超えると、古いメッセージから削除されます

レート制限
==========

APIの過負荷を防ぐためのレート制限設定です。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.chat.rate.limit.enabled``
     - レート制限を有効にする
     - ``true``
   * - ``rag.chat.rate.limit.requests.per.minute``
     - 1分あたりの最大リクエスト数
     - ``10``

レート制限の考慮事項
--------------------

- LLMプロバイダー側のレート制限も考慮して設定してください
- 高負荷環境では、より厳しい制限を設定することを推奨します
- レート制限に達した場合、ユーザーにはエラーメッセージが表示されます

APIの使用
=========

RAGチャット機能はREST APIを通じて利用できます。

非ストリーミングAPI
-------------------

エンドポイント: ``POST /api/v1/chat``

パラメーター:

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - パラメーター
     - 必須
     - 説明
   * - ``message``
     - はい
     - ユーザーのメッセージ
   * - ``sessionId``
     - いいえ
     - セッションID（会話を継続する場合）
   * - ``clear``
     - いいえ
     - ``true`` でセッションをクリア

リクエスト例:

::

    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "message=Fessのインストール方法を教えてください"

レスポンス例:

::

    {
      "status": "ok",
      "sessionId": "abc123",
      "content": "Fessのインストール方法は...",
      "sources": [
        {"title": "インストールガイド", "url": "https://..."}
      ]
    }

ストリーミングAPI
-----------------

エンドポイント: ``POST /api/v1/chat/stream``

Server-Sent Events（SSE）形式でレスポンスをストリーミングします。

パラメーター:

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - パラメーター
     - 必須
     - 説明
   * - ``message``
     - はい
     - ユーザーのメッセージ
   * - ``sessionId``
     - いいえ
     - セッションID（会話を継続する場合）

リクエスト例:

::

    curl -X POST "http://localhost:8080/api/v1/chat/stream" \
         -d "message=Fessの特徴を教えてください" \
         -H "Accept: text/event-stream"

SSEイベント:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - イベント
     - 説明
   * - ``session``
     - セッション情報（sessionId）
   * - ``phase``
     - 処理フェーズの開始/完了（intent_analysis, search, evaluation, generation）
   * - ``chunk``
     - 生成されたテキストの断片
   * - ``sources``
     - 参照元ドキュメントの情報
   * - ``done``
     - 処理完了（sessionId, htmlContent）
   * - ``error``
     - エラー情報

詳細なAPIドキュメントは :doc:`../api/api-chat` を参照してください。

Webインターフェース
===================

|Fess| のWebインターフェースでは、検索画面からRAGチャット機能を利用できます。

チャットの開始
--------------

1. |Fess| の検索画面にアクセス
2. チャットアイコンをクリック
3. チャットパネルが表示される

チャットの使用
--------------

1. テキストボックスに質問を入力
2. 送信ボタンをクリックまたはEnterキーを押す
3. AIアシスタントの回答が表示される
4. 回答には参照元へのリンクが含まれる

会話の継続
----------

- 同じチャットセッション内で会話を継続できます
- 前の質問の文脈を考慮した回答が得られます
- 「新しいチャット」をクリックすると、セッションがリセットされます

トラブルシューティング
======================

RAGチャットが有効にならない
---------------------------

**確認事項**:

1. ``rag.chat.enabled=true`` が設定されているか
2. LLMプロバイダーが正しく設定されているか
3. LLMプロバイダーへの接続が可能か

回答の品質が低い
----------------

**改善方法**:

1. より高性能なLLMモデルを使用
2. ``rag.chat.context.max.documents`` を増加
3. システムプロンプトをカスタマイズ
4. ``rag.chat.temperature`` を調整

レスポンスが遅い
----------------

**改善方法**:

1. より高速なLLMモデルを使用（例: Gemini Flash）
2. ``rag.chat.max.tokens`` を減少
3. ``rag.chat.context.max.chars`` を減少

セッションが維持されない
------------------------

**確認事項**:

1. クライアント側でsessionIdが正しく送信されているか
2. ``rag.chat.session.timeout.minutes`` の設定
3. セッションストレージの容量

デバッグ設定
------------

問題を調査する際は、ログレベルを調整して詳細なログを出力できます。

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm" level="DEBUG"/>
    <Logger name="org.codelibs.fess.api.chat" level="DEBUG"/>
    <Logger name="org.codelibs.fess.chat" level="DEBUG"/>

参考情報
========

- :doc:`llm-overview` - LLM統合の概要
- :doc:`llm-ollama` - Ollamaの設定
- :doc:`llm-openai` - OpenAIの設定
- :doc:`llm-gemini` - Google Geminiの設定
- :doc:`../api/api-chat` - Chat API リファレンス
- :doc:`../user/chat-search` - エンドユーザー向けチャット検索ガイド
