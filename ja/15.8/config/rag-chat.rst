==========================
AI検索モード機能の設定
==========================

概要
====

AI検索モード（RAG: Retrieval-Augmented Generation）は、|Fess| の検索結果をLLM（大規模言語モデル）で拡張し、
対話形式で情報を提供する機能です。ユーザーは自然言語で質問し、検索結果を基にした
詳細な回答を得ることができます。

|Fess| 15.8 では、LLM機能が ``fess-llm-*`` プラグインとして分離されました。
コア設定およびLLMプロバイダー固有の設定は ``fess_config.properties`` で行い、
LLMプロバイダーの選択（ ``rag.llm.name`` ）のみ ``system.properties`` または管理画面から行います。

検索パイプライン
================

AI検索モードは、専用のベクトルインデックスではなく |Fess| の標準の検索パイプライン（Rank Fusion）を通じて
ソースドキュメントを取得します。ロール・ラベルによる |Fess| 通常のアクセス制御もそのまま適用されます。
デフォルトではキーワード（BM25）検索が使用され、LLM自体がドキュメントの検索・ランキング・埋め込み
（embedding）を行うことはありません。

リクエストの種類によって、実行されるパイプラインが若干異なります。

- ``POST /api/v2/chat/stream`` （Web UIで使用）は、**意図検出 → 検索 → LLMによる関連度評価 → 内容取得 → 回答生成** のフルフローを実行します（ストリーミング）。
- ``POST /api/v2/chat`` （非ストリーミング）は、**意図検出 → 検索 → 回答生成** の短縮フローを実行します（関連度評価および独立した内容取得フェーズはありません）。

ストリーミングフローでは、追加のLLM呼び出しにより **検索結果を評価** し、関連性があると判断されたドキュメントのみを回答生成前に残します。

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

設定経路の早見表
================

|Fess| 15.8 では設定が「FessConfig 系」と「SystemProperty 系」の2系統に分かれています。
それぞれで設定方法が異なるため、混同しないように注意してください。

.. list-table::
   :header-rows: 1
   :widths: 35 18 32 15

   * - プロパティ
     - 系統
     - Docker / JVM オプションでの渡し方
     - 管理画面
   * - ``rag.chat.enabled``
     - FessConfig
     - ``-Dfess.config.rag.chat.enabled=true``
     - ×
   * - ``rag.llm.name``
     - SystemProperty
     - ``-Dfess.system.rag.llm.name=gemini`` （初回起動時のデフォルト）
     - ○ （全般の設定）
   * - ``rag.llm.gemini.api.key``
     - FessConfig
     - ``-Dfess.config.rag.llm.gemini.api.key=...``
     - ×
   * - ``rag.llm.gemini.model``
     - FessConfig
     - ``-Dfess.config.rag.llm.gemini.model=...``
     - ×
   * - ``rag.llm.openai.api.key``
     - FessConfig
     - ``-Dfess.config.rag.llm.openai.api.key=...``
     - ×
   * - ``rag.llm.openai.model``
     - FessConfig
     - ``-Dfess.config.rag.llm.openai.model=...``
     - ×
   * - ``rag.llm.ollama.api.url``
     - FessConfig
     - ``-Dfess.config.rag.llm.ollama.api.url=...``
     - ×

.. note::

   ``rag.llm.type`` というプロパティ名は |Fess| 15.5 までの旧名です。15.8 以降は ``rag.llm.name`` に変更されており、
   ``rag.llm.type`` の設定は読み取られません。

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
     - ユーザーメッセージの最大文字数。この値は System Property として読み込まれ、``fess_config.properties`` の項目は使用されません。System Properties か ``-Dfess.system.rag.chat.message.max.length`` で設定します。
     - ``4000``
   * - ``rag.chat.highlight.fragment.size``
     - 検索ハイライトのフラグメントサイズ
     - ``500``
   * - ``rag.chat.highlight.number.of.fragments``
     - 検索ハイライトのフラグメント数
     - ``3``
   * - ``rag.chat.content.fulltext.max.length``
     - この値を超える ``content_length`` のドキュメントは、回答コンテキストで本文全体ではなくハイライト抜粋を使用する閾値
     - ``3000``
   * - ``rag.chat.answer.highlight.fragment.size``
     - 大きなドキュメントから回答コンテキスト用に抜粋する際のハイライトのフラグメントサイズ
     - ``1000``
   * - ``rag.chat.answer.highlight.number.of.fragments``
     - 大きなドキュメントから回答コンテキスト用に抜粋する際のハイライトのフラグメント数
     - ``5``
   * - ``rag.chat.history.assistant.content``
     - アシスタント履歴に含めるコンテンツの種類（ ``full`` / ``smart_summary`` / ``source_titles`` / ``source_titles_and_urls`` / ``truncated`` / ``none`` ）
     - ``smart_summary``
   * - ``rag.chat.history.titles.max.count``
     - ``smart_summary`` モードでターンごとに保持する参照ドキュメントタイトルの最大数
     - ``5``

生成パラメーター
================

|Fess| 15.8 では、生成パラメーター（最大トークン数、temperature等）はプロバイダーごと、
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
``{promptType}`` には ``intent``、``evaluation``、``answer``、``summary``、``faq``、``queryregeneration``、
``unclear``、``noresults``、``docnotfound``、``direct`` 等のプロンプトタイプが入ります。
サポートされるプロンプトタイプの一覧は各プラグインの ``*LlmClient`` 実装に定義されています。

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

|Fess| 15.8 では、システムプロンプトはプロパティファイルではなく、各 ``fess-llm-*``
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

    # プロバイダーごとの最大同時リクエスト数（デフォルト: 5）
    rag.llm.ollama.max.concurrent.requests=5
    rag.llm.openai.max.concurrent.requests=5
    rag.llm.gemini.max.concurrent.requests=5

    # 同時実行パーミット取得待ちのタイムアウト（ミリ秒、デフォルト: 30000）
    rag.llm.ollama.concurrency.wait.timeout=30000

同時実行制御の考慮事項
-----------------------

- LLMプロバイダー側のレート制限も考慮して設定してください
- 高負荷環境では、より小さい値を設定することを推奨します
- 同時実行数の上限に達した場合、リクエストはキューに入り順次処理されます
- パーミット取得待ちが ``concurrency.wait.timeout`` を超えた場合はタイムアウトエラーになります

会話履歴モード
==============

``rag.chat.history.assistant.content`` で、アシスタント応答の会話履歴への保存方法を設定できます。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - モード
     - 説明
   * - ``smart_summary``
     - （デフォルト）アシスタント応答の本文は履歴から省略し、ターンごとに過去の検索クエリと参照ドキュメントのタイトル（先頭から最大 ``rag.chat.history.titles.max.count`` 件）のみを保持
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

   ``smart_summary`` モードでは、長い応答の本文をそのまま保持せず、検索クエリと参照タイトルに置き換えることで
   文脈を効率的に保持しながらトークン使用量を抑えます。
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

AI検索モード機能はREST API（v2 API）を通じて利用できます。
ベースURLは ``http://<サーバー名>/api/v2/`` です。

Chat API は以下の3つのエンドポイントを提供します。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - エンドポイント
     - 説明
   * - ``POST /api/v2/chat``
     - 一括（非ストリーミング）RAGチャット補完
   * - ``POST /api/v2/chat/stream``
     - ストリーミングRAGチャット補完（Server-Sent Events）
   * - ``DELETE /api/v2/chat/sessions/{session_id}``
     - チャットセッションの会話履歴をクリア

リクエストは ``Content-Type: application/json`` のJSONボディで送信します。
状態を変更するリクエスト（ ``POST`` / ``DELETE`` ）には CSRF トークン（ ``X-Fess-CSRF-Token`` ヘッダー）が必要です。
レスポンスは共通エンベロープ ``response`` に格納されます。

.. note::

   |Fess| 15.5 以前で提供されていた ``/api/v1/chat`` 系のフォームパラメーター形式のエンドポイントは廃止されました。
   15.8 では ``/api/v2/`` 配下のJSONベースAPIを使用してください。

非ストリーミングAPI
-------------------

エンドポイント: ``POST /api/v2/chat``

リクエストボディ（JSON）:

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 必須
     - 説明
   * - ``message``
     - はい
     - ユーザーのメッセージ
   * - ``session_id``
     - いいえ
     - セッションID（会話を継続する場合）。省略時はサーバーが作成し、レスポンスで返します
   * - ``fields``
     - いいえ
     - 取得ステップ用の任意フィルターフィールド（object）
   * - ``fields.label``
     - いいえ
     - ラベルによる検索フィルター
   * - ``extra_queries``
     - いいえ
     - ファセットフィルター用の追加クエリ式

リクエスト例:

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -d '{"message":"Fessのインストール方法を教えてください"}'

レスポンス例:

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session_id": "abc123",
        "content": "Fessのインストール方法は...",
        "sources": [
          {
            "rank": 1,
            "title": "インストールガイド",
            "url": "https://...",
            "doc_id": "...",
            "snippet": "..."
          }
        ]
      }
    }

ストリーミングAPI
-----------------

エンドポイント: ``POST /api/v2/chat/stream``

リクエストボディは ``POST /api/v2/chat`` と同じ（JSON）です。
レスポンスは Server-Sent Events（SSE）形式でストリーミングされます。

リクエスト例:

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat/stream" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -H "Accept: text/event-stream" \
         --no-buffer \
         -d '{"message":"Fessの特徴を教えてください"}'

SSEイベント:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - イベント
     - 説明（ペイロード）
   * - ``phase``
     - 処理フェーズの開始/完了（ ``intent`` , ``search`` , ``evaluate`` , ``fetch`` , ``answer`` ）。 ``{ phase, status, message?, keywords?, hit_count?, ... }``
   * - ``chunk``
     - 生成されたテキストの断片（ ``{ content }`` ）
   * - ``retry``
     - LLMリクエストがリトライされるときに通知（ ``{ phase, operation, attempt, max_attempts, sleep_ms, cause? }`` ）
   * - ``waiting``
     - 同時実行パーミット取得待ち等の長時間フェーズの進捗（ ``{ phase, reason, elapsed_ms, timeout_ms }`` ）
   * - ``fallback``
     - 検索結果ゼロ件等によりクエリが再生成されたときに通知（ ``{ phase, reason, original_query?, new_query? }`` 、理由は ``no_results`` または ``no_relevant_results`` ）
   * - ``warning``
     - 回復可能な警告の発生時に通知（ ``{ phase, code, detail? }`` 。推論モデルのトークン枯渇など）
   * - ``sources``
     - 参照元ドキュメントの情報（ ``{ sources: [...] }`` ）
   * - ``done``
     - 処理完了（ ``{ session_id, html_content? }`` ）。 ``html_content`` にはMarkdownレンダリング済みのHTML文字列が含まれる
   * - ``error``
     - 終端のストリーム途中失敗（ ``{ phase?, message, error_code }`` ）。タイムアウト、コンテキスト長超過、モデル未検出、不正なレスポンス、接続エラーなど

セッションのクリア
------------------

エンドポイント: ``DELETE /api/v2/chat/sessions/{session_id}``

指定したセッションの会話履歴をクリアします。成功時は ``cleared: true`` が返ります。

詳細なAPIドキュメント（認証・CSRF・レート制限・HTTPステータスコードを含む）は :doc:`../api/api-chat` を参照してください。

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

AI検索モードボタンが検索画面に表示されない
-------------------------------------------

**症状**: 検索結果ページのヘッダーにAIモードボタンが表示されず、 ``/chat`` にアクセスしてもトップページにリダイレクトされる。

**チェックリスト**: 以下を上から順に確認してください。

1. ``rag.chat.enabled=true`` が設定されているか

   - Docker の場合: ``FESS_JAVA_OPTS`` に ``-Dfess.config.rag.chat.enabled=true`` が含まれているか
   - パッケージインストールの場合: ``app/WEB-INF/conf/fess_config.properties`` に記述されているか

2. 対応する ``fess-llm-*`` プラグインがインストールされているか

   - Docker の場合: ``FESS_PLUGINS=fess-llm-gemini:15.8.0`` （または ``fess-llm-openai`` / ``fess-llm-ollama``）が指定されているか
   - パッケージインストールの場合: ``app/WEB-INF/plugin/`` に該当の JAR ファイルが配置されているか
   - 起動ログに ``Installing fess-llm-XXX-15.8.0.jar`` が出力されているか

3. ``rag.llm.name`` の値がインストール済みプラグインと一致しているか

   - 既定値は ``ollama`` です。Geminiプラグインだけを入れている場合などは、明示的に ``gemini`` （または ``openai``）に変更する必要があります
   - 設定方法 (a): 管理画面 > システム > 全般 の RAG セクションで ``rag.llm.name`` を編集して保存
   - 設定方法 (b): 起動時の ``FESS_JAVA_OPTS`` に ``-Dfess.system.rag.llm.name=gemini`` を含める（OpenSearch にまだ値が保存されていない初回のみデフォルトとして効きます）

4. 起動ログに ``[LLM] LlmClient not found. componentName=ollamaLlmClient`` のような WARN が継続して出ていないか

   - これは ``rag.llm.name`` が ``ollama`` のままで Ollamaプラグインが入っていないときの典型的な症状です
   - ``rag.llm.name`` を実際に使うプロバイダー名に変更すると解消します
   - 同様に ``componentName=geminiLlmClient`` の WARN が出る場合は、``rag.llm.name=gemini`` を設定したのに ``fess-llm-gemini`` プラグインが導入されていないことを示します

5. プロバイダー固有の API キーが正しく設定されているか

   - ``rag.llm.gemini.api.key`` / ``rag.llm.openai.api.key`` 等が空の場合、 ``checkAvailabilityNow`` が ``false`` を返すため AIモードは利用できません
   - 設定後、``log4j2.xml`` で ``org.codelibs.fess.llm.gemini`` を ``DEBUG`` にすると、``[LLM:GEMINI] Gemini is not available. apiKey is blank`` のようなログで確認できます

6. LLMプロバイダーへのネットワーク接続が可能か

   - クラウドAPI（Gemini / OpenAI）の場合、コンテナから外部に到達できる必要があります
   - Proxy 経由が必要なら、 ``fess_config.properties`` の ``http.proxy.host`` / ``http.proxy.port`` （必要に応じて ``http.proxy.username`` / ``http.proxy.password`` ）を設定してください。Docker環境では ``FESS_JAVA_OPTS`` に ``-Dfess.config.http.proxy.host=... -Dfess.config.http.proxy.port=...`` を追加します（ |Fess| 15.8 以降、LLMクライアントは |Fess| 共通のプロキシ設定を参照します）

.. note::

   管理画面「全般の設定」には ``rag.chat.enabled`` のチェックボックスはありません（仕様）。
   この値は FessConfig 系プロパティのため、``fess_config.properties`` または ``-Dfess.config.rag.chat.enabled=true`` 経由でのみ設定できます。

AI検索モードが有効にならない
----------------------------

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
    <Logger name="org.codelibs.fess.api.v2.handlers" level="DEBUG"/>
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
