==========================
AI検索モード機能の設定
==========================

概要
====

AI検索モード（RAG: Retrieval-Augmented Generation）は、|Fess| の検索結果をLLM（大規模言語モデル）で拡張し、
対話形式で情報を提供する機能です。ユーザーは自然言語で質問し、検索結果を基にした
詳細な回答を得ることができます。

|Fess| 15.6 では、LLM機能が ``fess-llm-*`` プラグインとして分離されました。
コア設定およびLLMプロバイダー固有の設定は ``fess_config.properties`` で行い、
LLMプロバイダーの選択（ ``rag.llm.name`` ）のみ ``system.properties`` または管理画面から行います。

AI検索モードの仕組み
================

AI検索モードは以下の多段階フローで動作します。

1. **意図解析フェーズ**: ユーザーの質問を分析し、検索に最適なキーワードを抽出
2. **検索フェーズ**: 抽出したキーワードで |Fess| の検索エンジンを使用して文書を検索
3. **クエリ再生成フォールバック**: 検索結果が得られない場合、LLMがクエリを再生成して再検索
4. **評価フェーズ**: 検索結果の関連性を評価し、最も適切な文書を選択
5. **生成フェーズ**: 選択した文書を基にLLMが回答を生成
6. **出力フェーズ**: 回答とソース情報をユーザーに返す（Markdownレンダリング対応）

このフローにより、単純なキーワード検索よりも文脈を理解した高品質な回答が可能になります。
検索クエリが適切でない場合も、クエリ再生成により回答の網羅性が向上します。

基本設定
========

AI検索モード機能の設定は、コア設定とプロバイダー設定の2つに分かれます。

コア設定 (fess_config.properties)
----------------------------------

AI検索モード機能を有効にするための基本設定です。
``app/WEB-INF/conf/fess_config.properties`` に設定します。

::

    # AI検索モード機能を有効にする
    rag.chat.enabled=true

プロバイダー設定 (system.properties / 管理画面)
-------------------------------------------------

LLMプロバイダーの選択は、管理画面またはシステムプロパティで行います。

**管理画面から設定する場合**:

管理画面 > システム > 全般 の設定画面で、使用するLLMプロバイダーを選択します。

**system.properties で設定する場合**:

::

    # LLMプロバイダーを選択（ollama, openai, gemini）
    rag.llm.name=ollama

LLMプロバイダーの詳細設定については、以下を参照してください:

- :doc:`llm-ollama` - Ollamaの設定
- :doc:`llm-openai` - OpenAIの設定
- :doc:`llm-gemini` - Google Geminiの設定

コア設定一覧
============

``fess_config.properties`` で設定できるコア設定の一覧です。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.chat.enabled``
     - AI検索モード機能を有効にする
     - ``false``
   * - ``rag.chat.context.max.documents``
     - コンテキストに含める最大ドキュメント数
     - ``5``
   * - ``rag.chat.session.timeout.minutes``
     - セッションのタイムアウト時間（分）
     - ``30``
   * - ``rag.chat.session.max.size``
     - 同時に保持できるセッションの最大数
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - 会話履歴に保持する最大メッセージ数
     - ``30``
   * - ``rag.chat.content.fields``
     - ドキュメントから取得するフィールド
     - ``title,url,content,doc_id,content_title,content_description``
   * - ``rag.chat.message.max.length``
     - ユーザーメッセージの最大文字数
     - ``4000``
   * - ``rag.chat.highlight.fragment.size``
     - ハイライト表示のフラグメントサイズ
     - ``500``
   * - ``rag.chat.highlight.number.of.fragments``
     - ハイライト表示のフラグメント数
     - ``3``
   * - ``rag.chat.history.assistant.content``
     - アシスタント履歴に含めるコンテンツの種類（ ``full`` / ``smart_summary`` / ``source_titles`` / ``source_titles_and_urls`` / ``truncated`` / ``none`` ）
     - ``smart_summary``

生成パラメーター
================

|Fess| 15.6 では、生成パラメーター（最大トークン数、temperature等）はプロバイダーごと、
プロンプトタイプごとに設定します。これらの設定はコア設定ではなく、各 ``fess-llm-*``
プラグインの設定として管理されます。

詳細は各プロバイダーのドキュメントを参照してください:

- :doc:`llm-ollama` - Ollamaの生成パラメーター設定
- :doc:`llm-openai` - OpenAIの生成パラメーター設定
- :doc:`llm-gemini` - Google Geminiの生成パラメーター設定

コンテキスト設定
================

検索結果からLLMに渡すコンテキストの設定です。

コア設定
--------

以下の設定は ``fess_config.properties`` で行います。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.chat.context.max.documents``
     - コンテキストに含める最大ドキュメント数
     - ``5``
   * - ``rag.chat.content.fields``
     - ドキュメントから取得するフィールド
     - ``title,url,content,doc_id,content_title,content_description``

プロバイダー固有の設定
-----------------------

以下の設定はプロバイダーごとに ``fess_config.properties`` で行います。

- ``rag.llm.{provider}.{promptType}.context.max.chars`` - コンテキストの最大文字数
- ``rag.llm.{provider}.chat.evaluation.max.relevant.docs`` - 評価フェーズで選択する最大関連ドキュメント数

``{provider}`` には ``ollama``、``openai``、``gemini`` 等のプロバイダー名が入ります。
``{promptType}`` には ``intent``、``evaluation``、``answer``、``summary``、``faq`` 等のプロンプトタイプが入ります。

詳細は各プロバイダーのドキュメントを参照してください。

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

|Fess| 15.6 では、システムプロンプトはプロパティファイルではなく、各 ``fess-llm-*``
プラグインのDI XML（``fess_llm++.xml``）で定義されています。

プロンプトのカスタマイズ
-------------------------

システムプロンプトをカスタマイズするには、プラグインJAR内の ``fess_llm++.xml`` を
オーバーライドします。

1. 使用しているプラグインのJARファイルから ``fess_llm++.xml`` を取得
2. 必要な変更を加える
3. ``app/WEB-INF/`` 以下の適切な場所に配置してオーバーライド

各プロンプトタイプ（意図解析、評価、生成）ごとに異なるシステムプロンプトが
定義されており、用途に応じた最適化が行われています。

詳細は各プロバイダーのドキュメントを参照してください:

- :doc:`llm-ollama` - Ollamaのプロンプト設定
- :doc:`llm-openai` - OpenAIのプロンプト設定
- :doc:`llm-gemini` - Google Geminiのプロンプト設定

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
     - ``30``

セッションの動作
----------------

- ユーザーが新しいチャットを開始すると、新しいセッションが作成されます
- セッションには会話履歴が保存され、文脈を維持した対話が可能です
- タイムアウト時間を経過すると、セッションは自動的に削除されます
- 会話履歴が最大メッセージ数を超えると、古いメッセージから削除されます

同時実行制御
============

LLMへのリクエストの同時実行数は、プロバイダーごとに ``fess_config.properties`` で制御します。

::

    # プロバイダーごとの最大同時リクエスト数
    rag.llm.ollama.max.concurrent.requests=5
    rag.llm.openai.max.concurrent.requests=10
    rag.llm.gemini.max.concurrent.requests=10

同時実行制御の考慮事項
-----------------------

- LLMプロバイダー側のレート制限も考慮して設定してください
- 高負荷環境では、より小さい値を設定することを推奨します
- 同時実行数の上限に達した場合、リクエストはキューに入り順次処理されます

会話履歴モード
==============

``rag.chat.history.assistant.content`` で、アシスタント応答の会話履歴への保存方法を設定できます。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - モード
     - 説明
   * - ``smart_summary``
     - （デフォルト）応答の先頭部分（60%）と末尾部分（40%）を保持し、中間部分を省略マーカーで置換。ソースタイトルも付加
   * - ``full``
     - 応答全体をそのまま保持
   * - ``source_titles``
     - ソースタイトルのみを保持
   * - ``source_titles_and_urls``
     - ソースタイトルとURLを保持
   * - ``truncated``
     - 応答を最大文字数で切り詰めて保持
   * - ``none``
     - 履歴を保持しない

.. note::

   ``smart_summary`` モードでは、長い応答の文脈を効率的に保持しながらトークン使用量を抑えます。
   ユーザーとアシスタントのメッセージペアはターン単位でグループ化され、文字数バジェット内で最適にパッキングされます。
   履歴の最大文字数やサマリーの最大文字数は、各 ``fess-llm-*`` プラグインの ``LlmClient`` 実装で制御されます。

クエリ再生成
============

検索結果が得られない場合、または関連する結果が見つからない場合、LLMが自動的にクエリを再生成して再検索します。

- 検索結果ゼロ件の場合: 理由 ``no_results`` としてクエリ再生成を実行
- 関連ドキュメントが見つからない場合: 理由 ``no_relevant_results`` としてクエリ再生成を実行
- 再生成に失敗した場合は元のクエリにフォールバック

この機能はデフォルトで有効であり、同期・ストリーミングの両方のRAGフローに統合されています。
クエリ再生成のプロンプトは各 ``fess-llm-*`` プラグインで定義されます。

Markdownレンダリング
====================

AI検索モードの応答はMarkdown形式でレンダリングされます。

- LLMの応答がMarkdownとしてパースされ、HTMLに変換されます
- 変換後のHTMLはサニタイズされ、安全なタグ・属性のみが許可されます
- 見出し、リスト、コードブロック、テーブル、リンク等のMarkdown記法に対応
- クライアント側では ``marked.js`` と ``DOMPurify`` を使用し、サーバー側ではOWASPサニタイザーを使用

APIの使用
=========

AI検索モード機能はREST APIを通じて利用できます。

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
   * - ``phase``
     - 処理フェーズの開始/完了（intent_analysis, search, evaluation, generation）
   * - ``chunk``
     - 生成されたテキストの断片
   * - ``sources``
     - 参照元ドキュメントの情報
   * - ``done``
     - 処理完了（sessionId, htmlContent）。htmlContentにはMarkdownレンダリング済みのHTML文字列が含まれる
   * - ``error``
     - エラー情報。タイムアウト、コンテキスト長超過、モデル未検出、不正なレスポンス、接続エラーなど種別に応じたメッセージ

詳細なAPIドキュメントは :doc:`../api/api-chat` を参照してください。

Webインターフェース
===================

|Fess| のWebインターフェースでは、検索画面からAI検索モード機能を利用できます。

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

AI検索モードが有効にならない
------------------------

**確認事項**:

1. ``rag.chat.enabled=true`` が設定されているか
2. ``rag.llm.name`` でLLMプロバイダーが正しく設定されているか
3. 対応する ``fess-llm-*`` プラグインがインストールされているか
4. LLMプロバイダーへの接続が可能か

回答の品質が低い
----------------

**改善方法**:

1. より高性能なLLMモデルを使用
2. ``rag.chat.context.max.documents`` を増加
3. DI XMLでシステムプロンプトをカスタマイズ
4. プロバイダー固有のtemperature設定を調整（各 ``fess-llm-*`` プラグインのドキュメントを参照）

レスポンスが遅い
----------------

**改善方法**:

1. より高速なLLMモデルを使用（例: Gemini Flash）
2. プロバイダー固有のmax.tokens設定を減少（各 ``fess-llm-*`` プラグインのドキュメントを参照）
3. ``rag.chat.context.max.documents`` を減少

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

主要なログメッセージには ``[RAG]`` プレフィックスが付与されており、
フェーズごとに ``[RAG:INTENT]``、``[RAG:EVAL]``、``[RAG:ANSWER]`` 等のサブプレフィックスが使用されます。
INFOレベルではチャット完了ログ（所要時間、ソース数）が出力され、DEBUGレベルではトークン使用量、
同時実行制御、履歴パッキングの詳細が出力されます。

検索ログとアクセスタイプ
------------------------

AI検索モードを通じた検索は、検索ログのアクセスタイプとしてLLMプロバイダー名（例: ``ollama``、``openai``、``gemini``）が
記録されます。これにより、通常のWeb検索やAPI検索とAI検索モード経由の検索を区別して分析できます。

参考情報
========

- :doc:`llm-overview` - LLM統合の概要
- :doc:`llm-ollama` - Ollamaの設定
- :doc:`llm-openai` - OpenAIの設定
- :doc:`llm-gemini` - Google Geminiの設定
- :doc:`../api/api-chat` - Chat API リファレンス
- :doc:`../user/chat-search` - エンドユーザー向けチャット検索ガイド
