==========================
OpenAIの設定
==========================

概要
====

OpenAIは、GPT-4をはじめとする高性能な大規模言語モデル（LLM）を提供するクラウドサービスです。
|Fess| ではOpenAI APIを使用してAI検索モード機能を実現できます。

OpenAIを使用することで、最先端のAIモデルによる高品質な回答生成が可能になります。

主な特徴
--------

- **高品質な回答**: 最先端のGPTモデルによる高精度な回答生成
- **スケーラビリティ**: クラウドサービスのため、スケーリングが容易
- **継続的な改善**: モデルの定期的なアップデートにより性能が向上
- **豊富な機能**: テキスト生成、要約、翻訳など多様なタスクに対応

対応モデル
----------

OpenAIで利用可能な主なモデル:

- ``gpt-5`` - 最新の高性能モデル
- ``gpt-5-mini`` - GPT-5の軽量版（コスト効率が良い）
- ``gpt-4o`` - 高性能マルチモーダルモデル
- ``gpt-4o-mini`` - GPT-4oの軽量版
- ``o3-mini`` - 推論特化の軽量モデル
- ``o4-mini`` - 推論特化の次世代軽量モデル

.. note::
   利用可能なモデルの最新情報は `OpenAI Models <https://platform.openai.com/docs/models>`__ で確認できます。

.. note::
   o1/o3/o4系やgpt-5系のモデルを使用する場合、|Fess| はOpenAI APIの ``max_completion_tokens`` パラメータを自動的に使用します。設定の変更は不要です。

前提条件
========

OpenAIを使用する前に、以下を準備してください。

1. **OpenAIアカウント**: `https://platform.openai.com/ <https://platform.openai.com/>`__ でアカウントを作成
2. **APIキー**: OpenAIダッシュボードでAPIキーを生成
3. **請求設定**: APIの使用には課金が発生するため、請求情報を設定

APIキーの取得
-------------

1. `OpenAI Platform <https://platform.openai.com/>`__ にログイン
2. 「API keys」セクションに移動
3. 「Create new secret key」をクリック
4. キー名を入力して作成
5. 表示されたキーを安全に保存（一度しか表示されません）

.. warning::
   APIキーは機密情報です。以下の点に注意してください:

   - バージョン管理システムにコミットしない
   - ログに出力しない
   - 環境変数や安全な設定ファイルで管理する

プラグインのインストール
========================

|Fess| 15.6では、OpenAI連携機能はプラグインとして提供されています。使用するには ``fess-llm-openai`` プラグインのインストールが必要です。

1. `fess-llm-openai-15.6.0.jar` をダウンロードします
2. |Fess| のインストールディレクトリにある ``app/WEB-INF/plugin/`` ディレクトリにJARファイルを配置します::

    cp fess-llm-openai-15.6.0.jar /path/to/fess/app/WEB-INF/plugin/

3. |Fess| を再起動します

.. note::
   プラグインのバージョンは |Fess| 本体のバージョンと合わせてください。

基本設定
========

|Fess| 15.6では、設定項目は用途に応じて以下の2つのファイルに分かれています。

- ``app/WEB-INF/conf/fess_config.properties`` - |Fess| 本体の設定およびLLMプロバイダー固有の設定
- ``system.properties`` / 管理画面（管理画面 > システム > 全般） - ``rag.llm.name`` の設定のみ

最小構成
--------

``system.properties``（管理画面 > システム > 全般 でも設定可能）:

::

    # LLMプロバイダーをOpenAIに設定
    rag.llm.name=openai

``app/WEB-INF/conf/fess_config.properties``:

::

    # AI検索モード機能を有効にする
    rag.chat.enabled=true

    # OpenAI APIキー
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # 使用するモデル
    rag.llm.openai.model=gpt-5-mini

推奨構成（本番環境）
--------------------

``system.properties``（管理画面 > システム > 全般 でも設定可能）:

::

    # LLMプロバイダー設定
    rag.llm.name=openai

``app/WEB-INF/conf/fess_config.properties``:

::

    # AI検索モード機能を有効にする
    rag.chat.enabled=true

    # OpenAI APIキー
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # モデル設定（高性能モデルを使用）
    rag.llm.openai.model=gpt-4o

    # APIエンドポイント（通常は変更不要）
    rag.llm.openai.api.url=https://api.openai.com/v1

    # タイムアウト設定
    rag.llm.openai.timeout=120000

    # 同時リクエスト数制限
    rag.llm.openai.max.concurrent.requests=5

設定項目
========

OpenAIクライアントで使用可能なすべての設定項目です。 ``rag.llm.name`` 以外はすべて ``fess_config.properties`` に設定します。

.. list-table::
   :header-rows: 1
   :widths: 35 35 15 15

   * - プロパティ
     - 説明
     - デフォルト
     - 設定場所
   * - ``rag.llm.name``
     - LLMプロバイダー名（``openai`` を指定）
     - ``ollama``
     - system.properties
   * - ``rag.llm.openai.api.key``
     - OpenAI APIキー
     - （必須）
     - fess_config.properties
   * - ``rag.llm.openai.model``
     - 使用するモデル名
     - ``gpt-5-mini``
     - fess_config.properties
   * - ``rag.llm.openai.api.url``
     - APIのベースURL
     - ``https://api.openai.com/v1``
     - fess_config.properties
   * - ``rag.llm.openai.timeout``
     - リクエストのタイムアウト時間（ミリ秒）
     - ``120000``
     - fess_config.properties
   * - ``rag.llm.openai.availability.check.interval``
     - 可用性チェック間隔（秒）
     - ``60``
     - fess_config.properties
   * - ``rag.llm.openai.max.concurrent.requests``
     - 最大同時リクエスト数
     - ``5``
     - fess_config.properties
   * - ``rag.llm.openai.chat.evaluation.max.relevant.docs``
     - 評価時の最大関連ドキュメント数
     - ``3``
     - fess_config.properties
   * - ``rag.llm.openai.concurrency.wait.timeout``
     - 同時リクエスト待機タイムアウト（ミリ秒）
     - ``30000``
     - fess_config.properties
   * - ``rag.llm.openai.reasoning.token.multiplier``
     - 推論モデル使用時のmax_tokens倍率
     - ``4``
     - fess_config.properties
   * - ``rag.llm.openai.retry.max``
     - HTTPリトライの最大試行回数（``429`` および ``5xx`` 系エラー時）
     - ``10``
     - fess_config.properties
   * - ``rag.llm.openai.retry.base.delay.ms``
     - 指数バックオフの基準遅延時間（ミリ秒）
     - ``2000``
     - fess_config.properties
   * - ``rag.llm.openai.stream.include.usage``
     - ストリーミング時に ``stream_options.include_usage=true`` を送信し、最終チャンクで使用トークン情報を受け取る
     - ``true``
     - fess_config.properties
   * - ``rag.llm.openai.history.max.chars``
     - 会話履歴の最大文字数
     - ``8000``
     - fess_config.properties
   * - ``rag.llm.openai.intent.history.max.messages``
     - 意図判定時の最大履歴メッセージ数
     - ``8``
     - fess_config.properties
   * - ``rag.llm.openai.intent.history.max.chars``
     - 意図判定時の最大履歴文字数
     - ``4000``
     - fess_config.properties
   * - ``rag.llm.openai.history.assistant.max.chars``
     - アシスタントメッセージの最大文字数
     - ``800``
     - fess_config.properties
   * - ``rag.llm.openai.history.assistant.summary.max.chars``
     - アシスタント要約の最大文字数
     - ``800``
     - fess_config.properties
   * - ``rag.llm.openai.chat.evaluation.description.max.chars``
     - 評価時のドキュメント説明最大文字数
     - ``500``
     - fess_config.properties
   * - ``rag.chat.enabled``
     - AI検索モード機能の有効化
     - ``false``
     - fess_config.properties

プロンプトタイプ別設定
======================

|Fess| では、プロンプトの種類ごとに個別のパラメータを設定できます。設定は ``fess_config.properties`` で行います。

設定パターン
------------

プロンプトタイプ別の設定は以下のパターンで指定します:

- ``rag.llm.openai.{promptType}.temperature`` - 生成のランダム性（0.0〜2.0）。推論モデル（o1/o3/o4/gpt-5系）では無視されます
- ``rag.llm.openai.{promptType}.max.tokens`` - 最大トークン数
- ``rag.llm.openai.{promptType}.context.max.chars`` - コンテキストの最大文字数（デフォルト: answer/summaryは ``16000`` 、その他は ``10000`` ）

プロンプトタイプ
----------------

利用可能なプロンプトタイプ:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - プロンプトタイプ
     - 説明
   * - ``intent``
     - ユーザーの意図を判定するプロンプト
   * - ``evaluation``
     - 検索結果の関連性を評価するプロンプト
   * - ``unclear``
     - 不明確なクエリに対する応答プロンプト
   * - ``noresults``
     - 検索結果がない場合の応答プロンプト
   * - ``docnotfound``
     - ドキュメントが見つからない場合の応答プロンプト
   * - ``answer``
     - 回答を生成するプロンプト
   * - ``summary``
     - 要約を生成するプロンプト
   * - ``faq``
     - FAQを生成するプロンプト
   * - ``direct``
     - 直接応答するプロンプト
   * - ``queryregeneration``
     - 検索クエリを再生成するプロンプト

デフォルト値
------------

各プロンプトタイプのデフォルト値は以下の通りです。推論モデル（o1/o3/o4/gpt-5系）ではtemperatureの設定は無視されます。

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - プロンプトタイプ
     - Temperature
     - Max Tokens
     - 備考
   * - ``intent``
     - 0.1
     - 256
     - 意図判定は決定的に
   * - ``evaluation``
     - 0.1
     - 256
     - 関連性評価は決定的に
   * - ``unclear``
     - 0.7
     - 512
     -
   * - ``noresults``
     - 0.7
     - 512
     -
   * - ``docnotfound``
     - 0.7
     - 256
     -
   * - ``direct``
     - 0.7
     - 1024
     -
   * - ``faq``
     - 0.7
     - 1024
     -
   * - ``answer``
     - 0.5
     - 2048
     - メイン回答生成
   * - ``summary``
     - 0.3
     - 2048
     - 要約生成
   * - ``queryregeneration``
     - 0.3
     - 256
     - クエリ再生成

設定例
------

::

    # answerプロンプトの温度設定
    rag.llm.openai.answer.temperature=0.7

    # answerプロンプトの最大トークン数
    rag.llm.openai.answer.max.tokens=2048

    # summaryプロンプトの温度設定（要約は低めに設定）
    rag.llm.openai.summary.temperature=0.3

    # intentプロンプトの温度設定（意図判定は低めに設定）
    rag.llm.openai.intent.temperature=0.1

リトライ動作
============

OpenAI APIへのリクエストは以下のHTTPステータスコードに対して自動的にリトライされます:

- ``429`` Too Many Requests（レート制限）
- ``500`` Internal Server Error
- ``502`` Bad Gateway（OpenAIが上流過負荷時に返すことがあります）
- ``503`` Service Unavailable
- ``504`` Gateway Timeout

リトライ時は指数バックオフ（基準値 ``rag.llm.openai.retry.base.delay.ms`` ミリ秒、最大 ``rag.llm.openai.retry.max`` 回、±20%のジッター付き）で待機します。
サーバが ``Retry-After`` ヘッダ（整数秒、最大 ``600`` 秒にクランプ）を返した場合は、その値が指数バックオフより優先されます。これはOpenAIの公式ガイダンスに従ったものです。

なお、 ``IOException`` （接続タイムアウト、ソケットリセット、DNS失敗）はリトライされません。リクエストがサーバに到達した可能性がある場合、リトライは二重課金につながる可能性があるためです。
ストリーミングリクエストでは、初回接続のみがリトライ対象であり、レスポンス本体の受信開始後に発生したエラーは即座に伝搬します。

.. note::
   既定設定（最大10回、基準2秒）の最悪ケースでは、9回分のバックオフ合計は ``2 + 4 + 8 + ... + 512 ≈ 1022秒（約17分）`` となります。 ``Retry-After`` （最大600秒）が毎回返るような状況では、最悪 ``9 × 600秒 = 90分`` まで膨らみます。レイテンシをよりタイトに制御したい場合は ``rag.llm.openai.retry.max`` を小さく設定してください。

ストリーミングと使用量情報
==========================

既定では ``stream_options.include_usage=true`` をリクエストに付与し、ストリーミング応答の最終SSEチャンクで ``usage`` オブジェクト（推論モデルでは ``completion_tokens_details.reasoning_tokens`` 、プロンプトキャッシュ利用時は ``prompt_tokens_details.cached_tokens`` を含む）を受信します。

vLLMやAzure OpenAI互換ゲートウェイなど、 ``stream_options.include_usage`` フィールドを受け付けないバックエンドを利用する場合は、以下のように無効化してください::

    rag.llm.openai.stream.include.usage=false

ログ出力と異常検出
==================

|Fess| 15.6.1 以降、OpenAIクライアントは以下の構造化されたログを出力します。これにより、 ``DEBUG`` レベルを有効化しなくても、トークン使用状況や応答異常を監視できます。

- ``[LLM:OPENAI] Stream completed.`` （INFO） - ストリーミング応答完了時にチャンク数、初回チャンクまでの時間、トークン使用情報などを出力
- ``[LLM:OPENAI] Chat response received.`` （INFO） - 非ストリーミング応答完了時に同等の情報を出力
- ``[LLM:OPENAI] Chat finished abnormally`` / ``Stream finished abnormally`` （WARN） - ``finish_reason`` が ``stop`` 以外（``length`` ：max_tokensによる切り詰め、 ``content_filter`` ：モデレーション、 ``tool_calls`` / ``function_call`` ：意図しないツール呼び出し設定など）の場合に出力
- ``[LLM:OPENAI] Stream refusal.`` （WARN） - 構造化出力で ``delta.refusal`` が返された場合に出力

これらのWARNログは、 ``max_tokens`` の調整、コンテンツフィルターの監査、 ``extra_params`` の誤設定の検出に活用できます。

URLログ内の認証情報マスキング
-----------------------------

ログに出力されるURLは、認証情報を含むクエリパラメータ（ ``api_key`` 、 ``apikey`` 、 ``api-key`` 、 ``key`` 、 ``token`` 、 ``access_token`` 、 ``access-token`` 。大文字小文字を区別しません）が自動的に ``***`` でマスクされます。

OpenAI公式エンドポイント（ ``https://api.openai.com`` ）は ``Authorization: Bearer`` ヘッダで認証するためURLには認証情報が含まれませんが、認証情報をクエリパラメータで受け付ける独自プロキシ（一部のAzureデプロイ、vLLMゲートウェイ等）を ``rag.llm.openai.api.url`` に設定する場合でも、APIキーがログに漏洩することを防ぎます。

推論モデル対応
==============

o1/o3/o4系やgpt-5系の推論モデルを使用する場合、|Fess| は自動的にOpenAI APIの ``max_completion_tokens`` パラメータを ``max_tokens`` の代わりに使用します。追加の設定変更は不要です。

.. note::
   推論モデル（o1/o3/o4/gpt-5系）では ``temperature`` の設定は無視され、固定値（1）が使用されます。また、推論モデル使用時はデフォルトの ``max_tokens`` が ``reasoning.token.multiplier``（デフォルト: 4）倍に増加されます。

推論モデル向け追加パラメータ
----------------------------

推論モデルを使用する場合、以下の追加パラメータを ``fess_config.properties`` で設定できます:

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.llm.openai.{promptType}.reasoning.effort``
     - o系モデルの推論effort設定（``low``、``medium``、``high``）
     - ``low``（intent/evaluation/docnotfound/unclear/noresults/queryregeneration）、未設定（その他）
   * - ``rag.llm.openai.{promptType}.top.p``
     - トークン選択の確率閾値（0.0〜1.0）
     - （未設定）
   * - ``rag.llm.openai.{promptType}.frequency.penalty``
     - 頻度ペナルティ（-2.0〜2.0）
     - （未設定）
   * - ``rag.llm.openai.{promptType}.presence.penalty``
     - 存在ペナルティ（-2.0〜2.0）
     - （未設定）

``{promptType}`` には ``intent``、``evaluation``、``answer``、``summary`` 等のプロンプトタイプが入ります。

設定例
------

::

    # o3-miniで回答生成時の推論effortをhighに設定
    rag.llm.openai.model=o3-mini
    rag.llm.openai.answer.reasoning.effort=high

    # gpt-5で回答生成時のtop_pとペナルティを設定
    rag.llm.openai.model=gpt-5
    rag.llm.openai.answer.top.p=0.9
    rag.llm.openai.answer.frequency.penalty=0.5

JVMオプションでの設定
=====================

セキュリティ上の理由から、APIキーをファイルではなく環境（JVMオプション）経由で設定することを推奨します。

Docker環境
----------

|Fess| 公式の `docker-fess <https://github.com/codelibs/docker-fess>`__ には OpenAI 用のオーバーレイ ``compose-openai.yaml`` が同梱されています。最小手順は次の通りです。

::

    export OPENAI_API_KEY="sk-..."
    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml up -d

``compose-openai.yaml`` の内容（同等の構成を自前で書く場合の参考）:

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-openai:15.6.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=${OPENAI_API_KEY:-} -Dfess.config.rag.llm.openai.model=${OPENAI_MODEL:-gpt-5-mini} -Dfess.system.rag.llm.name=openai"

ポイント:

- ``FESS_PLUGINS=fess-llm-openai:15.6.0`` で ``run.sh`` がプラグイン JAR を自動取得して ``app/WEB-INF/plugin/`` に配置します
- ``-Dfess.config.rag.chat.enabled=true`` で AI検索モードを有効化
- ``-Dfess.config.rag.llm.openai.api.key=...`` で API キー、 ``-Dfess.config.rag.llm.openai.model=...`` でモデルを指定
- ``-Dfess.system.rag.llm.name=openai`` は OpenSearch にまだ値が書き込まれていない初回起動時にデフォルトとして効きます。起動後は管理画面「システム > 全般」の RAG セクションでも変更できます

Proxy 経由でインターネットに接続する場合は、 |Fess| の ``http.proxy.*`` 設定を ``FESS_JAVA_OPTS`` 経由で指定してください（後述の「HTTPプロキシ経由の利用」を参照）。

systemd環境
-----------

``/etc/sysconfig/fess`` （または ``/etc/default/fess`` ）の ``FESS_JAVA_OPTS`` に追記します。

::

    FESS_JAVA_OPTS="-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=sk-... -Dfess.system.rag.llm.name=openai"

HTTPプロキシ経由の利用
======================

|Fess| 15.6.1 以降、OpenAIクライアントは |Fess| 全体のHTTPプロキシ設定を共有します。 ``fess_config.properties`` で以下のプロパティを指定してください。

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
   従来のJavaシステムプロパティ（ ``-Dhttps.proxyHost`` 等）はOpenAIクライアントからは参照されません。

Azure OpenAIの使用
==================

Microsoft Azure経由でOpenAIモデルを使用する場合は、APIエンドポイントを変更します。

::

    # Azure OpenAIエンドポイント
    rag.llm.openai.api.url=https://your-resource.openai.azure.com/openai/deployments/your-deployment

    # Azure APIキー
    rag.llm.openai.api.key=your-azure-api-key

    # デプロイ名（モデル名として指定）
    rag.llm.openai.model=your-deployment-name

.. note::
   Azure OpenAIを使用する場合、APIのリクエスト形式が若干異なる場合があります。
   詳細はAzure OpenAIのドキュメントを参照してください。

モデルの選択ガイド
==================

使用目的に応じたモデル選択の指針です。

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - モデル
     - コスト
     - 品質
     - 用途
   * - ``gpt-5-mini``
     - 中
     - 高
     - バランスの取れた用途（推奨）
   * - ``gpt-4o-mini``
     - 低〜中
     - 高
     - コスト重視の用途
   * - ``gpt-5``
     - 高
     - 最高
     - 複雑な推論、高品質が必要な場合
   * - ``gpt-4o``
     - 中〜高
     - 最高
     - マルチモーダル対応が必要な場合
   * - ``o3-mini`` / ``o4-mini``
     - 中
     - 最高
     - 数学・コーディングなどの推論タスク

コストの目安
------------

OpenAI APIは使用量に基づいて課金されます。

.. note::
   最新の価格は `OpenAI Pricing <https://openai.com/pricing>`__ で確認してください。

同時リクエスト制御
==================

|Fess| では、OpenAI APIへの同時リクエスト数を ``fess_config.properties`` の ``rag.llm.openai.max.concurrent.requests`` で制御できます。デフォルト値は ``5`` です。

::

    # 最大同時リクエスト数を設定
    rag.llm.openai.max.concurrent.requests=5

この設定により、OpenAI APIへの過剰なリクエストを防止し、レート制限エラーを回避できます。

OpenAIのTier別制限
------------------

OpenAIアカウントのTierに応じてAPI側の制限が異なります:

- **Free**: 3 RPM（リクエスト/分）
- **Tier 1**: 500 RPM
- **Tier 2**: 5,000 RPM
- **Tier 3+**: さらに高い制限

OpenAIアカウントのTierに応じて ``rag.llm.openai.max.concurrent.requests`` を適切に調整してください。

トラブルシューティング
======================

認証エラー
----------

**症状**: 「401 Unauthorized」エラーが発生する

**確認事項**:

1. APIキーが正しく設定されているか確認
2. APIキーが有効か確認（OpenAIダッシュボードで確認）
3. APIキーに必要な権限があるか確認

レート制限エラー
----------------

**症状**: 「429 Too Many Requests」エラーが発生する

**解決方法**:

1. ``rag.llm.openai.max.concurrent.requests`` の値を小さくする::

    rag.llm.openai.max.concurrent.requests=3

2. OpenAIアカウントのTierをアップグレード

クォータ超過
------------

**症状**: 「You exceeded your current quota」エラー

**解決方法**:

1. OpenAIダッシュボードで使用量を確認
2. 請求設定を確認し、必要に応じて上限を引き上げ

タイムアウト
------------

**症状**: リクエストがタイムアウトする

**解決方法**:

1. タイムアウト時間を延長::

    rag.llm.openai.timeout=180000

2. より高速なモデル（gpt-5-mini等）を検討

デバッグ設定
------------

問題を調査する際は、|Fess| のログレベルを調整してOpenAI関連の詳細なログを出力できます。

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.openai" level="DEBUG"/>

セキュリティに関する注意
========================

OpenAI APIを使用する際は、以下のセキュリティ事項に注意してください。

1. **データプライバシー**: 検索結果の内容がOpenAIのサーバーに送信されます
2. **APIキーの管理**: キーの漏洩は不正利用につながります
3. **コンプライアンス**: 機密データを含む場合は、組織のポリシーを確認
4. **使用ポリシー**: OpenAIの利用規約を遵守

参考情報
========

- `OpenAI Platform <https://platform.openai.com/>`__
- `OpenAI API Reference <https://platform.openai.com/docs/api-reference>`__
- `OpenAI Pricing <https://openai.com/pricing>`__
- :doc:`llm-overview` - LLM統合の概要
- :doc:`rag-chat` - AI検索モード機能の詳細
