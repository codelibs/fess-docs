==========================
LLM統合の概要
==========================

概要
====

|Fess| 15.6では、大規模言語モデル（LLM）を活用したAI検索モード（RAG: Retrieval-Augmented Generation）機能をサポートしています。
この機能により、ユーザーは検索結果を基にしたAIアシスタントとの対話形式で情報を取得できます。

|Fess| 15.6では、LLM連携機能は ``fess-llm-*`` プラグインとして提供されます。利用するLLMプロバイダーに対応するプラグインを導入してください。

対応プロバイダー
================

|Fess| は以下のLLMプロバイダーをサポートしています。

.. list-table::
   :header-rows: 1
   :widths: 20 20 30 30

   * - プロバイダー
     - 設定値
     - プラグイン
     - 説明
   * - Ollama
     - ``ollama``
     - ``fess-llm-ollama``
     - ローカル環境で動作するオープンソースのLLMサーバー。Llama、Mistral、Gemmaなどのモデルを実行可能。デフォルト設定。
   * - OpenAI
     - ``openai``
     - ``fess-llm-openai``
     - OpenAI社のクラウドAPI。GPT-4などのモデルを利用可能。
   * - Google Gemini
     - ``gemini``
     - ``fess-llm-gemini``
     - Google社のクラウドAPI。Geminiモデルを利用可能。

プラグイン導入
==============

|Fess| 15.6では、LLM機能はプラグインとして分離されています。利用するプロバイダーに対応する ``fess-llm-{provider}`` プラグインのJARファイルをプラグインディレクトリに配置する必要があります。

例として、OpenAIプロバイダーを利用する場合は ``fess-llm-openai-15.6.0.jar`` をダウンロードし、以下のディレクトリに配置します。

::

    app/WEB-INF/plugin/

配置後、 |Fess| を再起動するとプラグインが読み込まれます。

アーキテクチャ
==============

AI検索モード機能は以下のフローで動作します。

1. **ユーザー入力**: ユーザーがチャットインターフェースで質問を入力
2. **意図解析**: LLMがユーザーの質問を分析し、検索キーワードを抽出
3. **検索実行**: |Fess| の検索エンジンで関連ドキュメントを検索
4. **クエリ再生成**: 検索結果が得られない場合、LLMがクエリを再生成して再検索
5. **結果評価**: LLMが検索結果の関連性を評価し、最適なドキュメントを選択
6. **回答生成**: 選択されたドキュメントを基にLLMが回答を生成（Markdownレンダリング対応）
7. **ソース引用**: 回答には参照元ドキュメントへのリンクが含まれる

基本設定
========

LLM機能の設定は、以下の2つの場所で行います。

管理画面の全般設定 / system.properties
--------------------------------------

管理画面の全般設定、または ``system.properties`` で設定します。LLMプロバイダーの選択に使用します。

::

    # LLMプロバイダーを指定（ollama, openai, gemini）
    rag.llm.name=ollama

fess_config.properties
----------------------

``app/WEB-INF/conf/fess_config.properties`` で設定します。AI検索モードの有効化、セッション・履歴関連の設定に加え、プロバイダー固有の設定（接続先URLやAPIキー、生成パラメーターなど）もこのファイルに記述します。

::

    # AI検索モード機能を有効にする
    rag.chat.enabled=true

    # プロバイダー固有設定の例（OpenAIの場合）
    rag.llm.openai.api.key=sk-...
    rag.llm.openai.answer.temperature=0.7

各プロバイダーの詳細な設定については、以下のドキュメントを参照してください。

- :doc:`llm-ollama` - Ollamaの設定
- :doc:`llm-openai` - OpenAIの設定
- :doc:`llm-gemini` - Google Geminiの設定

共通設定
========

すべてのLLMプロバイダーで共通して使用される設定項目です。これらは ``fess_config.properties`` で設定します。

コンテキスト設定
----------------

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
     - ``title,url,content,...``

.. note::

   コンテキストの最大文字数（ ``context.max.chars`` ）はプロバイダーおよびプロンプトタイプごとの設定に変更されました。 ``fess_config.properties`` で ``rag.llm.{provider}.{promptType}.context.max.chars`` として設定してください。

システムプロンプト
------------------

|Fess| 15.6では、システムプロンプトはプロパティファイルではなく、各プラグインのDI XMLファイルで管理されます。

各 ``fess-llm-*`` プラグインに含まれる ``fess_llm++.xml`` ファイルでシステムプロンプトが定義されています。プロンプトをカスタマイズするには、プラグインディレクトリ内のDI XMLファイルを編集してください。

可用性チェック
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.llm.{provider}.availability.check.interval``
     - LLMの可用性をチェックする間隔（秒）。0で無効化
     - ``60``

この設定は ``fess_config.properties`` で行います。 |Fess| は定期的にLLMプロバイダーの接続状態を確認します。

セッション管理
==============

チャットセッションに関する設定です。これらは ``fess_config.properties`` で設定します。

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
     - セッションの最大数
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - 会話履歴に保持する最大メッセージ数
     - ``30``

同時実行制御
============

LLMへのリクエストの同時実行数を制御する設定です。 ``fess_config.properties`` で設定します。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.llm.{provider}.max.concurrent.requests``
     - プロバイダーへの最大同時リクエスト数
     - ``5``

例えば、OpenAIプロバイダーの同時実行数を設定する場合は以下のようになります。

::

    rag.llm.openai.max.concurrent.requests=10

評価設定
========

検索結果の評価に関する設定です。 ``fess_config.properties`` で設定します。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.llm.{provider}.chat.evaluation.max.relevant.docs``
     - 評価フェーズで選択する関連ドキュメントの最大数
     - ``3``

プロンプトタイプ別設定
======================

|Fess| 15.6では、生成パラメーターをプロンプトタイプごとに設定できます。これにより、用途に応じた細かな調整が可能です。設定は ``fess_config.properties`` で行います。

プロンプトタイプ一覧
--------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - プロンプトタイプ
     - 設定値
     - 説明
   * - 意図解析
     - ``intent``
     - ユーザーの質問を分析し、検索キーワードを抽出する
   * - 評価
     - ``evaluation``
     - 検索結果の関連性を評価する
   * - 不明確な質問
     - ``unclear``
     - 質問が不明確な場合の応答を生成する
   * - 検索結果なし
     - ``noresults``
     - 検索結果が見つからない場合の応答を生成する
   * - ドキュメント不在
     - ``docnotfound``
     - 該当するドキュメントが存在しない場合の応答を生成する
   * - 回答生成
     - ``answer``
     - 検索結果を基に回答を生成する
   * - 要約
     - ``summary``
     - ドキュメントの要約を生成する
   * - FAQ
     - ``faq``
     - FAQ形式の回答を生成する
   * - 直接回答
     - ``direct``
     - 検索を介さずに直接回答を生成する
   * - クエリ再生成
     - ``queryregeneration``
     - 検索結果が得られない場合にクエリを再生成する

設定パターン
------------

プロンプトタイプごとの設定は以下のパターンで指定します。

::

    rag.llm.{provider}.{promptType}.temperature
    rag.llm.{provider}.{promptType}.max.tokens
    rag.llm.{provider}.{promptType}.context.max.chars

設定例（OpenAIプロバイダーの場合）:

::

    # 回答生成の温度を低めに設定
    rag.llm.openai.answer.temperature=0.5
    # 回答生成の最大トークン数
    rag.llm.openai.answer.max.tokens=4096
    # 意図解析は短い応答で十分なため低く設定
    rag.llm.openai.intent.max.tokens=256
    # 要約のコンテキスト最大文字数
    rag.llm.openai.summary.context.max.chars=8000

次のステップ
============

- :doc:`llm-ollama` - Ollamaの詳細設定
- :doc:`llm-openai` - OpenAIの詳細設定
- :doc:`llm-gemini` - Google Geminiの詳細設定
- :doc:`rag-chat` - AI検索モード機能の詳細設定
- :doc:`rank-fusion` - Rank Fusion設定（ハイブリッド検索の結果統合）
