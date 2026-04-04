==========================
Google Geminiの設定
==========================

概要
====

Google Geminiは、Google社が提供する最先端の大規模言語モデル（LLM）です。
|Fess| ではGoogle AI API（Generative Language API）を使用してGeminiモデルによるAI検索モード機能を実現できます。

Geminiを使用することで、Googleの最新AI技術を活用した高品質な回答生成が可能になります。

主な特徴
--------

- **マルチモーダル対応**: テキストだけでなく画像も処理可能
- **長いコンテキスト**: 大量の文書を一度に処理できる長いコンテキストウィンドウ
- **コスト効率**: Flashモデルは高速かつ低コスト
- **Google統合**: Google Cloudサービスとの連携が容易

対応モデル
----------

Geminiで利用可能な主なモデル:

- ``gemini-3-flash-preview`` - 最新の高速モデル（推奨）
- ``gemini-3.1-pro-preview`` - 最新の高推論モデル
- ``gemini-2.5-flash`` - 安定版の高速モデル
- ``gemini-2.5-pro`` - 安定版の高推論モデル

.. note::
   利用可能なモデルの最新情報は `Google AI for Developers <https://ai.google.dev/models/gemini>`__ で確認できます。

前提条件
========

Geminiを使用する前に、以下を準備してください。

1. **Googleアカウント**: Googleアカウントが必要
2. **Google AI Studioアクセス**: `https://aistudio.google.com/ <https://aistudio.google.com/>`__ にアクセス
3. **APIキー**: Google AI StudioでAPIキーを生成

APIキーの取得
-------------

1. `Google AI Studio <https://aistudio.google.com/>`__ にアクセス
2. 「Get API key」をクリック
3. 「Create API key」を選択
4. プロジェクトを選択または新規作成
5. 生成されたAPIキーを安全に保存

.. warning::
   APIキーは機密情報です。以下の点に注意してください:

   - バージョン管理システムにコミットしない
   - ログに出力しない
   - 環境変数や安全な設定ファイルで管理する

プラグインのインストール
========================

|Fess| 15.6では、Gemini連携機能は ``fess-llm-gemini`` プラグインとして提供されています。
Geminiを使用するには、プラグインのインストールが必要です。

1. `fess-llm-gemini-15.6.0.jar` をダウンロードします
2. |Fess| の ``app/WEB-INF/plugin/`` ディレクトリに配置します
3. |Fess| を再起動します

::

    # プラグインの配置例
    cp fess-llm-gemini-15.6.0.jar /path/to/fess/app/WEB-INF/plugin/

.. note::
   プラグインのバージョンは |Fess| のバージョンと合わせてください。

基本設定
========

|Fess| 15.6では、LLMプロバイダーの選択（ ``rag.llm.name`` ）は管理画面または ``system.properties`` で行い、AI検索モード機能の有効化やGemini固有の設定は ``fess_config.properties`` で行います。

fess_config.propertiesの設定
----------------------------

``app/WEB-INF/conf/fess_config.properties`` にAI検索モード機能の有効化設定を追加します。

::

    # AI検索モード機能を有効にする
    rag.chat.enabled=true

LLMプロバイダーの設定
---------------------

LLMプロバイダー名（ ``rag.llm.name`` ）は管理画面（管理画面 > システム > 全般）で設定するか、``system.properties`` に設定します。Gemini固有の設定は ``fess_config.properties`` に記述します。

最小構成
~~~~~~~~

``system.properties``（管理画面 > システム > 全般 でも設定可能）:

::

    # LLMプロバイダーをGeminiに設定
    rag.llm.name=gemini

``app/WEB-INF/conf/fess_config.properties``:

::

    # AI検索モード機能を有効にする
    rag.chat.enabled=true

    # Gemini APIキー
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # 使用するモデル
    rag.llm.gemini.model=gemini-3-flash-preview

推奨構成（本番環境）
~~~~~~~~~~~~~~~~~~~~

``system.properties``（管理画面 > システム > 全般 でも設定可能）:

::

    # LLMプロバイダーをGeminiに設定
    rag.llm.name=gemini

``app/WEB-INF/conf/fess_config.properties``:

::

    # AI検索モード機能を有効にする
    rag.chat.enabled=true

    # Gemini APIキー
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # モデル設定（高速モデルを使用）
    rag.llm.gemini.model=gemini-3-flash-preview

    # APIエンドポイント（通常は変更不要）
    rag.llm.gemini.api.url=https://generativelanguage.googleapis.com/v1beta

    # タイムアウト設定
    rag.llm.gemini.timeout=60000

設定項目
========

Geminiクライアントで使用可能なすべての設定項目です。 ``rag.llm.name`` 以外はすべて ``fess_config.properties`` に設定します。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.llm.gemini.api.key``
     - Google AI APIキー（Gemini APIを使用するには設定が必要です）
     - ``""``
   * - ``rag.llm.gemini.model``
     - 使用するモデル名
     - ``gemini-3-flash-preview``
   * - ``rag.llm.gemini.api.url``
     - APIのベースURL
     - ``https://generativelanguage.googleapis.com/v1beta``
   * - ``rag.llm.gemini.timeout``
     - リクエストのタイムアウト時間（ミリ秒）
     - ``60000``
   * - ``rag.llm.gemini.availability.check.interval``
     - 可用性チェック間隔（秒）
     - ``60``
   * - ``rag.llm.gemini.max.concurrent.requests``
     - 最大同時リクエスト数
     - ``5``
   * - ``rag.llm.gemini.chat.evaluation.max.relevant.docs``
     - 評価時の最大関連ドキュメント数
     - ``3``
   * - ``rag.llm.gemini.chat.evaluation.description.max.chars``
     - 評価時のドキュメント説明最大文字数
     - ``500``
   * - ``rag.llm.gemini.concurrency.wait.timeout``
     - 同時リクエスト待機タイムアウト（ミリ秒）
     - ``30000``
   * - ``rag.llm.gemini.history.max.chars``
     - チャット履歴の最大文字数
     - ``10000``
   * - ``rag.llm.gemini.intent.history.max.messages``
     - 意図判定時の履歴最大メッセージ数
     - ``10``
   * - ``rag.llm.gemini.intent.history.max.chars``
     - 意図判定時の履歴最大文字数
     - ``5000``
   * - ``rag.llm.gemini.history.assistant.max.chars``
     - アシスタント履歴の最大文字数
     - ``1000``
   * - ``rag.llm.gemini.history.assistant.summary.max.chars``
     - アシスタント要約履歴の最大文字数
     - ``1000``

プロンプトタイプ別設定
======================

|Fess| では、プロンプトの種類ごとにLLMのパラメータを細かく設定できます。
プロンプトタイプ別の設定は ``fess_config.properties`` に記述します。

設定フォーマット
----------------

::

    rag.llm.gemini.{promptType}.temperature
    rag.llm.gemini.{promptType}.max.tokens
    rag.llm.gemini.{promptType}.thinking.budget
    rag.llm.gemini.{promptType}.context.max.chars

利用可能なプロンプトタイプ
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - プロンプトタイプ
     - 説明
   * - ``intent``
     - ユーザーの意図を判定するプロンプト
   * - ``evaluation``
     - ドキュメントの関連性を評価するプロンプト
   * - ``unclear``
     - 質問が不明確な場合のプロンプト
   * - ``noresults``
     - 検索結果がない場合のプロンプト
   * - ``docnotfound``
     - ドキュメントが見つからない場合のプロンプト
   * - ``answer``
     - 回答生成プロンプト
   * - ``summary``
     - 要約生成プロンプト
   * - ``faq``
     - FAQ生成プロンプト
   * - ``direct``
     - 直接応答プロンプト
   * - ``queryregeneration``
     - クエリ再生成プロンプト

プロンプトタイプ別デフォルト値
------------------------------

各プロンプトタイプのデフォルト値は以下の通りです。設定されていない場合、これらの値が使用されます。

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20

   * - プロンプトタイプ
     - temperature
     - max.tokens
     - thinking.budget
   * - ``intent``
     - ``0.1``
     - ``256``
     - ``0``
   * - ``evaluation``
     - ``0.1``
     - ``256``
     - ``0``
   * - ``unclear``
     - ``0.7``
     - ``512``
     - ``0``
   * - ``noresults``
     - ``0.7``
     - ``512``
     - ``0``
   * - ``docnotfound``
     - ``0.7``
     - ``256``
     - ``0``
   * - ``direct``
     - ``0.7``
     - ``2048``
     - ``1024``
   * - ``faq``
     - ``0.7``
     - ``2048``
     - ``1024``
   * - ``answer``
     - ``0.5``
     - ``4096``
     - ``2048``
   * - ``summary``
     - ``0.3``
     - ``4096``
     - ``2048``
   * - ``queryregeneration``
     - ``0.3``
     - ``256``
     - ``0``

設定例
------

::

    # 回答生成の温度設定
    rag.llm.gemini.answer.temperature=0.7

    # 要約生成の最大トークン数
    rag.llm.gemini.summary.max.tokens=2048

    # 回答生成のコンテキスト最大文字数
    rag.llm.gemini.answer.context.max.chars=16000

    # 要約生成のコンテキスト最大文字数
    rag.llm.gemini.summary.context.max.chars=16000

    # FAQ生成のコンテキスト最大文字数
    rag.llm.gemini.faq.context.max.chars=10000

.. note::
   ``context.max.chars`` のデフォルト値はプロンプトタイプによって異なります。
   ``answer`` と ``summary`` は16000、``faq`` は10000、その他のプロンプトタイプは10000です。

思考モデル対応
==============

Geminiでは思考モデル（Thinking Model）をサポートしています。
思考モデルを使用すると、モデルが回答を生成する前に内部的な推論プロセスを実行し、より精度の高い回答を生成できます。

思考バジェットはプロンプトタイプごとに ``fess_config.properties`` で設定できます。

::

    # 回答生成時の思考バジェットの設定
    rag.llm.gemini.answer.thinking.budget=1024

    # 要約生成時の思考バジェットの設定
    rag.llm.gemini.summary.thinking.budget=1024

.. note::
   思考バジェットを設定すると、応答時間が長くなる場合があります。
   用途に応じて適切な値を設定してください。

環境変数での設定
================

セキュリティ上の理由から、APIキーを環境変数で設定することを推奨します。

Docker環境
----------

::

    docker run -e RAG_LLM_GEMINI_API_KEY=AIzaSy... codelibs/fess:15.6.0

docker-compose.yml
~~~~~~~~~~~~~~~~~~

::

    services:
      fess:
        image: codelibs/fess:15.6.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_NAME=gemini
          - RAG_LLM_GEMINI_API_KEY=${GEMINI_API_KEY}
          - RAG_LLM_GEMINI_MODEL=gemini-3-flash-preview

systemd環境
-----------

``/etc/systemd/system/fess.service.d/override.conf``:

::

    [Service]
    Environment="RAG_LLM_GEMINI_API_KEY=AIzaSy..."

Vertex AI経由の使用
===================

Google Cloud Platformを使用している場合、Vertex AI経由でGeminiを使用することもできます。
Vertex AIを使用する場合は、APIエンドポイントと認証方法が異なります。

.. note::
   現在の |Fess| はGoogle AI API（generativelanguage.googleapis.com）を使用しています。
   Vertex AI経由での使用が必要な場合は、カスタム実装が必要になる場合があります。

モデルの選択ガイド
==================

使用目的に応じたモデル選択の指針です。

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - モデル
     - 速度
     - 品質
     - 用途
   * - ``gemini-3-flash-preview``
     - 高速
     - 最高
     - 一般的な用途（推奨）
   * - ``gemini-3.1-pro-preview``
     - 中速
     - 最高
     - 複雑な推論
   * - ``gemini-2.5-flash``
     - 高速
     - 高
     - 安定版、コスト重視
   * - ``gemini-2.5-pro``
     - 中速
     - 高
     - 安定版、長いコンテキスト

コンテキストウィンドウ
----------------------

Geminiモデルは非常に長いコンテキストウィンドウをサポートしています:

- **Gemini 3 Flash / 2.5 Flash**: 最大100万トークン
- **Gemini 3.1 Pro / 2.5 Pro**: 最大100万トークン（3.1 Pro）/ 200万トークン（2.5 Pro）

この特徴を活かして、より多くの検索結果をコンテキストに含めることができます。

::

    # より多くのドキュメントをコンテキストに含める（fess_config.propertiesに設定）
    rag.llm.gemini.answer.context.max.chars=20000

コストの目安
------------

Google AI APIは使用量に基づいて課金されます（無料枠あり）。

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - モデル
     - 入力（100万文字）
     - 出力（100万文字）
   * - Gemini 3 Flash Preview
     - $0.50
     - $3.00
   * - Gemini 3.1 Pro Preview
     - $2.00
     - $12.00
   * - Gemini 2.5 Flash
     - $0.075
     - $0.30
   * - Gemini 2.5 Pro
     - $1.25
     - $5.00

.. note::
   最新の価格と無料枠の情報は `Google AI Pricing <https://ai.google.dev/pricing>`__ で確認してください。

同時リクエスト制御
==================

|Fess| では、Geminiへの同時リクエスト数を制御できます。
``fess_config.properties`` で以下のプロパティを設定してください。

::

    # 最大同時リクエスト数（デフォルト: 5）
    rag.llm.gemini.max.concurrent.requests=5

この設定により、Google AI APIへの過度なリクエストを防ぎ、レート制限エラーを回避できます。

無料枠の制限（参考）
--------------------

Google AI APIには無料枠がありますが、以下の制限があります:

- リクエスト/分: 15 RPM
- トークン/分: 100万 TPM
- リクエスト/日: 1,500 RPD

無料枠を使用する場合は、``rag.llm.gemini.max.concurrent.requests`` を低めに設定することを推奨します。

トラブルシューティング
======================

認証エラー
----------

**症状**: APIキー関連のエラーが発生する

**確認事項**:

1. APIキーが正しく設定されているか確認
2. APIキーがGoogle AI Studio上で有効か確認
3. APIキーに必要な権限があるか確認
4. APIがプロジェクトで有効化されているか確認

レート制限エラー
----------------

**症状**: 「429 Resource has been exhausted」エラーが発生する

**解決方法**:

1. ``fess_config.properties`` で同時リクエスト数を減らす::

    rag.llm.gemini.max.concurrent.requests=3

2. 数分待ってから再試行
3. 必要に応じてクォータの引き上げをリクエスト

リージョン制限
--------------

**症状**: サービスが利用できないというエラー

**確認事項**:

Google AI APIは一部の地域でのみ利用可能です。サポートされる地域については
Googleのドキュメントを確認してください。

タイムアウト
------------

**症状**: リクエストがタイムアウトする

**解決方法**:

1. タイムアウト時間を延長::

    rag.llm.gemini.timeout=120000

2. Flashモデル（より高速）の使用を検討

デバッグ設定
------------

問題を調査する際は、|Fess| のログレベルを調整してGemini関連の詳細なログを出力できます。

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.gemini" level="DEBUG"/>

セキュリティに関する注意
========================

Google AI APIを使用する際は、以下のセキュリティ事項に注意してください。

1. **データプライバシー**: 検索結果の内容がGoogleのサーバーに送信されます
2. **APIキーの管理**: キーの漏洩は不正利用につながります
3. **コンプライアンス**: 機密データを含む場合は、組織のポリシーを確認
4. **利用規約**: Googleの利用規約とAcceptable Use Policyを遵守

参考情報
========

- `Google AI for Developers <https://ai.google.dev/>`__
- `Google AI Studio <https://aistudio.google.com/>`__
- `Gemini API Documentation <https://ai.google.dev/docs>`__
- `Google AI Pricing <https://ai.google.dev/pricing>`__
- :doc:`llm-overview` - LLM統合の概要
- :doc:`rag-chat` - AI検索モード機能の詳細
