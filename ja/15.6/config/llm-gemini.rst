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

- ``gemini-3.1-flash-lite-preview`` - 軽量・低コストの高速モデル（デフォルト）
- ``gemini-3-flash-preview`` - 標準のFlashモデル
- ``gemini-3.1-pro`` / ``gemini-3-pro`` - 高推論モデル
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
    rag.llm.gemini.model=gemini-3.1-flash-lite-preview

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
     - ``gemini-3.1-flash-lite-preview``
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
   * - ``rag.llm.gemini.retry.max``
     - HTTPリトライの最大試行回数（``429`` および ``5xx`` 系エラー時）
     - ``10``
   * - ``rag.llm.gemini.retry.base.delay.ms``
     - 指数バックオフの基準遅延時間（ミリ秒）
     - ``2000``

認証方式
========

|Fess| 15.6.1 以降、APIキーは ``x-goog-api-key`` HTTPリクエストヘッダで送信されます（Googleの推奨方式）。
従来のように ``?key=...`` クエリパラメータでURLに付与することはなくなったため、APIキーがアクセスログに残ることはありません。

リトライ動作
============

Gemini APIへのリクエストは以下のHTTPステータスコードに対して自動的にリトライされます:

- ``429`` Resource Exhausted（クォータ超過・レート制限）
- ``500`` Internal Server Error
- ``503`` Service Unavailable
- ``504`` Gateway Timeout

リトライ時は指数バックオフ（基準値 ``rag.llm.gemini.retry.base.delay.ms`` ミリ秒、最大 ``rag.llm.gemini.retry.max`` 回、±20%のジッター付き）で待機します。
ストリーミングリクエストでは、初回接続のみがリトライ対象で、レスポンス本体の受信開始後に発生したエラーは即座に伝搬します。

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

思考バジェットはプロンプトタイプごとに ``fess_config.properties`` で設定します。 |Fess| はリクエスト時に ``rag.llm.gemini.{promptType}.thinking.budget`` の整数値（トークン数）を、解決されたモデル世代に応じて適切なAPIフィールドに自動変換します。

::

    # 回答生成時の思考バジェットの設定
    rag.llm.gemini.answer.thinking.budget=1024

    # 要約生成時の思考バジェットの設定
    rag.llm.gemini.summary.thinking.budget=1024

モデル世代によるマッピング
--------------------------

- **Gemini 2.x** （例: ``gemini-2.5-flash`` ）: 設定した整数値をそのまま ``thinkingConfig.thinkingBudget`` として送信します。 ``0`` を指定すると思考は完全に無効化されます。
- **Gemini 3.x** （例: ``gemini-3.1-flash-lite-preview`` ）: 整数値を ``thinkingConfig.thinkingLevel`` の列挙値（ ``MINIMAL`` / ``LOW`` / ``MEDIUM`` / ``HIGH`` ）にバケット化して送信します。

Gemini 3.x のバケットマッピングは以下のとおりです:

.. list-table::
   :header-rows: 1
   :widths: 35 25 40

   * - バジェット値
     - thinkingLevel
     - 備考
   * - ``<=0``
     - ``MINIMAL`` または ``LOW``
     - Flash / Flash-Lite モデルでは ``MINIMAL`` 、 ``MINIMAL`` をサポートしないPro系モデル（ ``gemini-3-pro`` / ``gemini-3.1-pro`` ）では ``LOW``
   * - ``<=4096``
     - ``MEDIUM``
     -
   * - ``>4096``
     - ``HIGH``
     -

.. note::
   Gemini 3.x はどのバケットでも一定の思考トークンを必ず消費します（ ``thinkingLevel=MINIMAL`` でも数百トークン消費する場合があります）。
   このため、 |Fess| は Gemini 3.x モデル使用時に既定の ``maxOutputTokens`` に対して自動的に追加のヘッドルーム（1024トークン）を加え、 ``finishReason=MAX_TOKENS`` による回答切り詰めを防ぎます。
   Gemini 2.x では ``thinkingBudget=0`` で思考自体が無効化されるため、ヘッドルームの追加は行いません。

.. note::
   思考バジェットを大きく設定すると、応答時間が長くなる場合があります。
   用途に応じて適切な値を設定してください。

JVMオプションでの設定
=====================

セキュリティ上の理由から、APIキーをファイルではなく環境（JVMオプション）経由で設定することを推奨します。

Docker環境
----------

|Fess| 公式の `docker-fess <https://github.com/codelibs/docker-fess>`__ には Gemini 用のオーバーレイ ``compose-gemini.yaml`` が同梱されています。最小手順は次の通りです。

::

    export GEMINI_API_KEY="AIzaSy..."
    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-gemini.yaml up -d

``compose-gemini.yaml`` の内容（同等の構成を自前で書く場合の参考）:

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-gemini:15.6.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.gemini.api.key=${GEMINI_API_KEY:-} -Dfess.config.rag.llm.gemini.model=${GEMINI_MODEL:-gemini-3.1-flash-lite-preview} -Dfess.system.rag.llm.name=gemini"

ポイント:

- ``FESS_PLUGINS=fess-llm-gemini:15.6.0`` で ``run.sh`` がプラグイン JAR を自動取得して ``app/WEB-INF/plugin/`` に配置します
- ``-Dfess.config.rag.chat.enabled=true`` で AI検索モードを有効化
- ``-Dfess.config.rag.llm.gemini.api.key=...`` で API キー、 ``-Dfess.config.rag.llm.gemini.model=...`` でモデルを指定
- ``-Dfess.system.rag.llm.name=gemini`` は OpenSearch にまだ値が書き込まれていない初回起動時にデフォルトとして効きます。起動後は管理画面「システム > 全般」の RAG セクションでも変更できます

Proxy 経由でインターネットに接続する場合は、 |Fess| の ``http.proxy.*`` 設定を ``FESS_JAVA_OPTS`` 経由で指定してください（後述の「HTTPプロキシ経由の利用」を参照）。

systemd環境
-----------

``/etc/sysconfig/fess`` （または ``/etc/default/fess`` ）の ``FESS_JAVA_OPTS`` に追記します。

::

    FESS_JAVA_OPTS="-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.gemini.api.key=AIzaSy... -Dfess.system.rag.llm.name=gemini"

HTTPプロキシ経由の利用
======================

|Fess| 15.6.1 以降、Geminiクライアントは |Fess| 全体のHTTPプロキシ設定を共有します。 ``fess_config.properties`` で以下のプロパティを指定してください。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``http.proxy.host``
     - プロキシホスト名（空文字列の場合はプロキシを使用しない）
     - ``""``
   * - ``http.proxy.port``
     - プロキシポート番号
     - ``8080``
   * - ``http.proxy.username``
     - プロキシ認証のユーザー名（任意。指定するとBasic認証が有効化される）
     - ``""``
   * - ``http.proxy.password``
     - プロキシ認証のパスワード
     - ``""``

Docker環境では ``FESS_JAVA_OPTS`` に以下のように指定します::

    -Dfess.config.http.proxy.host=proxy.example.com
    -Dfess.config.http.proxy.port=8080

.. note::
   この設定はクローラーなど |Fess| 全体のHTTPアクセスにも影響します。
   従来のJavaシステムプロパティ（ ``-Dhttps.proxyHost`` 等）はGeminiクライアントからは参照されません。

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
   * - ``gemini-3.1-flash-lite-preview``
     - 高速
     - 高
     - 軽量・低コスト（デフォルト、 ``thinkingLevel=MINIMAL`` 対応）
   * - ``gemini-3-flash-preview``
     - 高速
     - 最高
     - 一般的な用途（ ``thinkingLevel=MINIMAL`` 対応）
   * - ``gemini-3.1-pro`` / ``gemini-3-pro``
     - 中速
     - 最高
     - 複雑な推論（ ``MINIMAL`` 非対応・最低でも ``LOW`` ）
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
