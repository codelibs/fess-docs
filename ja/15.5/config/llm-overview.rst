==========================
LLM統合の概要
==========================

概要
====

|Fess| 15.5では、大規模言語モデル（LLM）を活用したRAG（Retrieval-Augmented Generation）チャット機能をサポートしています。
この機能により、ユーザーは検索結果を基にしたAIアシスタントとの対話形式で情報を取得できます。

対応プロバイダー
================

|Fess| は以下のLLMプロバイダーをサポートしています。

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - プロバイダー
     - 設定値
     - 説明
   * - Ollama
     - ``ollama``
     - ローカル環境で動作するオープンソースのLLMサーバー。Llama、Mistral、Gemmaなどのモデルを実行可能。デフォルト設定。
   * - OpenAI
     - ``openai``
     - OpenAI社のクラウドAPI。GPT-4などのモデルを利用可能。
   * - Google Gemini
     - ``gemini``
     - Google社のクラウドAPI。Geminiモデルを利用可能。

アーキテクチャ
==============

RAGチャット機能は以下のフローで動作します。

1. **ユーザー入力**: ユーザーがチャットインターフェースで質問を入力
2. **意図解析**: LLMがユーザーの質問を分析し、検索キーワードを抽出
3. **検索実行**: |Fess| の検索エンジンで関連ドキュメントを検索
4. **結果評価**: LLMが検索結果の関連性を評価し、最適なドキュメントを選択
5. **回答生成**: 選択されたドキュメントを基にLLMが回答を生成
6. **ソース引用**: 回答には参照元ドキュメントへのリンクが含まれる

基本設定
========

LLM機能を有効にするには、``app/WEB-INF/conf/system.properties`` に以下の設定を追加します。

RAGチャットの有効化
-------------------

::

    # RAGチャット機能を有効にする
    rag.chat.enabled=true

LLMプロバイダーの選択
---------------------

::

    # LLMプロバイダーを指定（ollama, openai, gemini）
    rag.llm.type=ollama

各プロバイダーの詳細な設定については、以下のドキュメントを参照してください。

- :doc:`llm-ollama` - Ollamaの設定
- :doc:`llm-openai` - OpenAIの設定
- :doc:`llm-gemini` - Google Geminiの設定

共通設定
========

すべてのLLMプロバイダーで共通して使用される設定項目です。

生成パラメーター
----------------

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
     - 生成のランダム性（0.0〜1.0）。低いほど決定的な回答になる
     - ``0.7``

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
   * - ``rag.chat.context.max.chars``
     - コンテキストの最大文字数
     - ``4000``
   * - ``rag.chat.content.fields``
     - ドキュメントから取得するフィールド
     - ``title,url,content,...``

システムプロンプト
------------------

::

    rag.chat.system.prompt=You are an AI assistant for Fess search engine. Answer questions based on the search results provided. Always cite your sources using [1], [2], etc.

このプロンプトはLLMの基本的な振る舞いを定義します。必要に応じてカスタマイズできます。

可用性チェック
--------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.llm.availability.check.interval``
     - LLMの可用性をチェックする間隔（秒）。0で無効化
     - ``60``

この設定により、|Fess| は定期的にLLMプロバイダーの接続状態を確認します。

セッション管理
==============

チャットセッションに関する設定です。

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
     - ``20``

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

評価設定
========

検索結果の評価に関する設定です。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.chat.evaluation.max.relevant.docs``
     - 評価フェーズで選択する関連ドキュメントの最大数
     - ``3``

次のステップ
============

- :doc:`llm-ollama` - Ollamaの詳細設定
- :doc:`llm-openai` - OpenAIの詳細設定
- :doc:`llm-gemini` - Google Geminiの詳細設定
- :doc:`rag-chat` - RAGチャット機能の詳細設定
