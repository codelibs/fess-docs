====================================
Amazon Bedrockの設定（AI検索 / RAG）
====================================

概要
====

このページでは、|Fess| がAmazon Bedrockを **AI検索モード（RAG: Retrieval-Augmented Generation）** およびコンテンツチャンクの埋め込みプロバイダーとして利用できるように、 ``fess-llm-bedrock`` プラグインを設定する方法を説明します。

Amazon Bedrockは、Amazonをはじめとする複数のモデルプロバイダーの基盤モデルを、単一のAPIで提供するAWSのサービスです。
プラグインは、指定したAWSリージョンのBedrock Runtime APIを呼び出します。

- **AI検索モード**: Converse API（ストリーミング回答には ``ConverseStream`` ）
- **コンテンツチャンクの埋め込み**: InvokeModel API（Amazon Titan Text Embeddings V2またはCohere Embed）

対応モデル
----------

AI検索モードは、利用するリージョンでConverse APIに対応しているモデルであれば使用できます。
デフォルトは、米国のクロスリージョン推論プロファイル経由のAmazon Nova 2 Lite（ ``us.amazon.nova-2-lite-v1:0`` ）です。
``rag.llm.bedrock.model`` には、モデルID、推論プロファイルID（ ``us.`` 、 ``eu.`` 、 ``global.`` などのプレフィックス付き）、またはARNを指定できます。

コンテンツチャンクの埋め込みでは、以下のモデルに対応しています。

.. list-table::
   :header-rows: 1
   :widths: 40 35 25

   * - モデル
     - ``content_chunker.embedding.dimension``
     - 1リクエストあたりのテキスト数
   * - ``amazon.titan-embed-text-v2:0``
     - ``256`` 、 ``512`` または ``1024``
     - 1
   * - ``cohere.embed-english-v3`` / ``cohere.embed-multilingual-v3``
     - ``1024``
     - 最大96（各テキストは2048文字以内）
   * - ``cohere.embed-v4:0`` （推論プロファイル経由も可）
     - ``256`` 、 ``512`` 、 ``1024`` または ``1536``
     - 最大96

埋め込みモデルは、設定されたID内のベースモデル名で判別されます。ベースモデルID、クロスリージョン推論プロファイルID（ ``us.`` 、 ``eu.`` 、 ``global.`` など）、またはそれらを含むARNが使用できます。
アプリケーション推論プロファイルのIDは不透明な文字列のため、判別できません。

.. note::
   各リージョンで利用可能なモデルについては、 `Supported foundation models in Amazon Bedrock <https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html>`__ を参照してください。

前提条件
========

1. **AWSアカウント**: 利用するリージョンでAmazon Bedrockが利用できること
2. **モデルアクセス**: 設定するモデルが、そのリージョンでアカウントから利用できること
3. **認証情報**: Bedrock APIキー、またはモデルの呼び出しが許可されたAWS認証情報（ :ref:`bedrock-authentication` を参照）

プラグインのインストール
========================

Bedrock連携機能は ``fess-llm-bedrock`` プラグインとして提供されています。
管理画面の「システム」>「プラグイン」からインストールするか、JARファイルを手動で配置して |Fess| を再起動します。

::

    cp fess-llm-bedrock-15.9.0.jar /path/to/fess/app/WEB-INF/plugin/

.. note::
   プラグインのバージョンは |Fess| のバージョンと合わせてください。

基本設定
========

LLMプロバイダー（ ``rag.llm.name`` ）は管理画面（管理画面 > システム > 全般）または ``system.properties`` で選択します。
AI検索モード機能の有効化と ``rag.llm.bedrock.*`` の設定は ``fess_config.properties`` に記述します。

``system.properties``\ （管理画面 > システム > 全般 でも設定可能）:

::

    rag.llm.name=bedrock

``app/WEB-INF/classes/fess_config.properties``\ （パッケージインストールの場合は ``/etc/fess/fess_config.properties`` ）。AWS認証情報を使用する場合:

::

    rag.chat.enabled=true
    rag.llm.bedrock.region=us-east-1
    rag.llm.bedrock.model=us.amazon.nova-2-lite-v1:0

AWS認証情報の代わりにBedrock APIキーを使用する場合:

::

    rag.chat.enabled=true
    rag.llm.bedrock.region=us-east-1
    rag.llm.bedrock.api.key=your-bedrock-api-key

設定項目
========

AI検索モードのクライアントで利用できるすべての設定項目です。 ``fess_config.properties`` （または ``-Dfess.config.<key>`` JVMオプション）で設定します。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.llm.bedrock.api.key``
     - Bedrock APIキー。空の場合はAWS認証情報でリクエストに署名（SigV4）します
     - ``""``
   * - ``rag.llm.bedrock.region``
     - Bedrock RuntimeエンドポイントおよびSigV4署名のAWSリージョン
     - ``us-east-1``
   * - ``rag.llm.bedrock.endpoint``
     - エンドポイントURL（VPCインターフェースエンドポイントなど）。空の場合は ``https://bedrock-runtime.<region>.amazonaws.com``
     - ``""``
   * - ``rag.llm.bedrock.model``
     - モデルID、推論プロファイルID、またはARN
     - ``us.amazon.nova-2-lite-v1:0``
   * - ``rag.llm.bedrock.timeout``
     - リクエストタイムアウト（ミリ秒）
     - ``120000``
   * - ``rag.llm.bedrock.availability.check.interval``
     - 可用性チェック間隔（秒）
     - ``60``
   * - ``rag.llm.bedrock.temperature.enabled``
     - ``false`` にすると、 ``temperature`` を受け付けないモデルやモードのために ``temperature`` を送信しません
     - ``true``
   * - ``rag.llm.bedrock.additional.model.request.fields``
     - モデル固有のパラメーターを ``additionalModelRequestFields`` として送信するJSONオブジェクト
     - ``""``
   * - ``rag.llm.bedrock.max.concurrent.requests``
     - 最大同時リクエスト数
     - ``5``
   * - ``rag.llm.bedrock.concurrency.wait.timeout``
     - 同時リクエスト待機タイムアウト（ミリ秒）
     - ``30000``
   * - ``rag.llm.bedrock.answer.context.max.chars``
     - 回答生成時に取得するコンテキストの最大文字数
     - ``16000``
   * - ``rag.llm.bedrock.summary.context.max.chars``
     - 要約生成時のドキュメントの最大文字数
     - ``16000``
   * - ``rag.llm.bedrock.faq.context.max.chars``
     - FAQ生成時に取得するコンテキストの最大文字数
     - ``10000``
   * - ``rag.llm.bedrock.chat.evaluation.max.relevant.docs``
     - 評価時の最大関連ドキュメント数
     - ``3``
   * - ``rag.llm.bedrock.chat.evaluation.description.max.chars``
     - 評価時のドキュメント説明最大文字数
     - ``500``
   * - ``rag.llm.bedrock.history.max.chars``
     - チャット履歴の最大文字数
     - ``8000``
   * - ``rag.llm.bedrock.intent.history.max.messages``
     - 意図判定時の履歴最大メッセージ数
     - ``8``
   * - ``rag.llm.bedrock.intent.history.max.chars``
     - 意図判定時の履歴最大文字数
     - ``4000``
   * - ``rag.llm.bedrock.history.assistant.max.chars``
     - アシスタント履歴の最大文字数
     - ``800``
   * - ``rag.llm.bedrock.history.assistant.summary.max.chars``
     - アシスタント要約履歴の最大文字数
     - ``800``
   * - ``rag.llm.bedrock.retry.max``
     - HTTPリクエストの最大試行回数（ ``429`` 、 ``500`` 、 ``502`` 、 ``503`` 、 ``504`` の場合）
     - ``10``
   * - ``rag.llm.bedrock.retry.base.delay.ms``
     - 指数バックオフの基準遅延時間（ミリ秒）
     - ``2000``

.. _bedrock-authentication:

認証方式
========

APIキー
-------

``rag.llm.bedrock.api.key`` を設定すると、 ``Authorization: Bearer <key>`` として送信されます。
短期のBedrock APIキーには有効期限があり、作成したリージョンでのみ使用できます。長期のキーはIAMユーザーに紐づきます。
この値は ``fess_config.properties`` に設定した場合、管理画面の「システム情報」でマスクされます（ ``content_chunker.embedding.bedrock.api.key`` の場合は ``system.properties`` ）。
環境変数とJVMシステムプロパティ（ ``-Dfess.config.*`` や ``-Dfess.system.*`` オプションを含む）はマスクされずに表示されるため、これらの方法でキーを渡さないでください。

AWS認証情報（SigV4）
--------------------

APIキーが設定されていない場合、すべてのリクエストはAWS Signature Version 4で署名されます。
認証情報は、以下のうち最初に取得できたものが使用されます。

1. JVMシステムプロパティ ``aws.accessKeyId`` / ``aws.secretAccessKey`` / ``aws.sessionToken``
2. 環境変数 ``AWS_ACCESS_KEY_ID`` / ``AWS_SECRET_ACCESS_KEY`` / ``AWS_SESSION_TOKEN``
3. Web IDフェデレーション（ ``AWS_WEB_IDENTITY_TOKEN_FILE`` と ``AWS_ROLE_ARN`` 。Amazon EKSで使用）
4. 共有の ``~/.aws/credentials`` および ``~/.aws/config`` ファイル（ ``AWS_PROFILE`` でプロファイルを選択）
5. コンテナ認証情報エンドポイント（Amazon ECS）
6. EC2インスタンスメタデータサービス（インスタンスプロファイル）

JVMシステムプロパティ（1番目）が反映されるのは |Fess| のWebプロセスのみです。
コンテンツチャンク（ドキュメント）の埋め込みは別の子JVMで実行されるため、その場合は環境変数、共有の認証情報プロファイル、またはIAMロールを使用するか、 ``jvm.chunk.options`` にも ``-Daws.*`` オプションを指定してください。

リージョンは常に ``rag.llm.bedrock.region`` から取得され、 ``AWS_REGION`` は参照されません。
IAM Identity Center（SSO）を使用するプロファイルには対応していません。

.. warning::
   IAMロール（EC2インスタンスプロファイル、ECSタスクロール、EKS Web IDフェデレーション）、または |Fess| を実行するユーザーの共有認証情報ファイルの使用を推奨します。
   環境変数とJVMシステムプロパティは、管理画面の「システム情報」にマスクされずに表示されるため、長期的なキーはこれらに設定しないでください。

IAMプリンシパルには、使用するモデルに対する ``bedrock:InvokeModel`` （ConverseとInvokeModel）および ``bedrock:InvokeModelWithResponseStream`` （ConverseStream）の権限が必要です。
モデルとして推論プロファイルを使用する場合は、推論プロファイルと、それがルーティングする基盤モデルの両方を許可してください。

リトライ動作
============

リクエストは、 ``429`` 、 ``500`` 、 ``502`` 、 ``503`` 、 ``504`` の場合、およびBedrockへの接続を確立できなかった場合にリトライされます。
リトライ時は指数バックオフ（基準値 ``rag.llm.bedrock.retry.base.delay.ms`` ミリ秒、±20%のジッター付き、最大 ``rag.llm.bedrock.retry.max`` 回）で待機し、 ``Retry-After`` ヘッダーがある場合はそちらが優先されます。
ストリーミングリクエストでは、初回リクエストのみがリトライ対象です。回答のストリーミング開始後に発生したエラー（ストリーム内の例外イベントを含む）はリクエストを終了させます。

プロンプトタイプ別設定
======================

他のプロバイダーと同様に、 ``temperature`` と ``max.tokens`` はプロンプトタイプごとに設定できます。

::

    rag.llm.bedrock.{promptType}.temperature
    rag.llm.bedrock.{promptType}.max.tokens
    rag.llm.bedrock.{promptType}.context.max.chars
    rag.llm.bedrock.{promptType}.additional.model.request.fields

``{promptType}`` は ``intent`` 、 ``evaluation`` 、 ``unclear`` 、 ``noresults`` 、 ``docnotfound`` 、 ``direct`` 、 ``faq`` 、 ``answer`` 、 ``summary`` 、 ``queryregeneration`` のいずれかです。
プロンプトタイプ別の ``additional.model.request.fields`` は、そのプロンプトタイプに限りグローバルな値を置き換えます。

何も設定しなかった場合のデフォルト値:

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - プロンプトタイプ
     - temperature
     - max.tokens
   * - ``intent`` 、 ``evaluation``
     - ``0.1``
     - ``256``
   * - ``unclear`` 、 ``noresults``
     - ``0.7``
     - ``512``
   * - ``docnotfound``
     - ``0.7``
     - ``256``
   * - ``direct`` 、 ``faq``
     - ``0.7``
     - ``1024``
   * - ``answer``
     - ``0.5``
     - ``2048``
   * - ``summary``
     - ``0.3``
     - ``2048``
   * - ``queryregeneration``
     - ``0.3``
     - ``256``

.. note::
   ``rag.llm.bedrock.{promptType}.thinking.budget`` は、Bedrockでは推論（reasoning）の設定がモデルごとに異なるため、サポートされていません。
   設定した値は送信されず、WARNログが出力されます。代わりに ``additional.model.request.fields`` を使用してください。

モデル固有のパラメーター
========================

``additional.model.request.fields`` は、JSONオブジェクトをそのままモデルに渡します。
JSONオブジェクトでない値は送信されず、プロパティ名を含むWARNログが出力されます。

例えば、Anthropic Claudeモデルの拡張思考を回答生成時のみ使用する場合:

::

    rag.llm.bedrock.model=<a Claude model ID or inference profile ID>
    rag.llm.bedrock.temperature.enabled=false
    rag.llm.bedrock.answer.additional.model.request.fields={"thinking":{"type":"enabled","budget_tokens":2048}}
    rag.llm.bedrock.answer.max.tokens=6144

Claudeは、思考が有効な間は ``temperature`` を受け付けません。また、 ``max.tokens`` は ``budget_tokens`` より大きくする必要があります。
推論（reasoning）のテキストはユーザーには表示されず、回答テキストのみが表示されます。

コンテンツチャンクの埋め込み
============================

Bedrockをコンテンツチャンクの埋め込みに使用するには、 ``app/WEB-INF/conf/system.properties``\ （RPM/DEB 版は ``/etc/fess/system.properties``、Docker 版は ``/opt/fess/system.properties``）、または ``-Dfess.system.<key>`` オプションに以下を設定します。
``rag.llm.bedrock.*`` とは異なり、これらのキーは ``fess_config.properties`` からは読み込まれません。

::

    content_chunker.enabled=true
    content_chunker.embedding.name=bedrock
    content_chunker.embedding.dimension=1024
    content_chunker.embedding.bedrock.region=us-east-1
    content_chunker.embedding.bedrock.model=amazon.titan-embed-text-v2:0

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``content_chunker.embedding.bedrock.api.key``
     - Bedrock APIキー。空の場合はAWS認証情報を使用します
     - ``""``
   * - ``content_chunker.embedding.bedrock.region``
     - AWSリージョン
     - ``us-east-1``
   * - ``content_chunker.embedding.bedrock.endpoint``
     - エンドポイントURL。空の場合はリージョンから決定されます
     - ``""``
   * - ``content_chunker.embedding.bedrock.model``
     - 埋め込みモデル（ `対応モデル`_ を参照）
     - ``amazon.titan-embed-text-v2:0``
   * - ``content_chunker.embedding.bedrock.normalize``
     - Titanのみ: ベクトルを正規化するかどうか
     - ``true``
   * - ``content_chunker.embedding.bedrock.truncate``
     - Cohereのみ: ``truncate`` （v3は ``NONE`` / ``START`` / ``END`` 、v4は ``NONE`` / ``LEFT`` / ``RIGHT`` ）。空の場合は送信しません
     - ``""``
   * - ``content_chunker.embedding.bedrock.timeout``
     - リクエストタイムアウト（ミリ秒）
     - ``120000``
   * - ``content_chunker.embedding.bedrock.connect.timeout``
     - 接続タイムアウト（ミリ秒）
     - ``5000``
   * - ``content_chunker.embedding.bedrock.availability.check.interval``
     - 可用性チェック間隔（秒）
     - ``60``
   * - ``content_chunker.embedding.bedrock.retry.max``
     - HTTPリクエストの最大試行回数（ ``429`` 、 ``500`` 、 ``502`` 、 ``503`` 、 ``504`` の場合）
     - ``10``
   * - ``content_chunker.embedding.bedrock.retry.base.delay.ms``
     - 指数バックオフの基準遅延時間（ミリ秒）
     - ``2000``
   * - ``content_chunker.embedding.bedrock.retry.max.delay.ms``
     - 1回のバックオフ待機時間の上限（ ``Retry-After`` を含む、ミリ秒）
     - ``60000``

``content_chunker.embedding.dimension`` には、モデルが出力できる次元数を指定する必要があります（ `対応モデル`_ を参照）。そうでない場合、埋め込みプロバイダーは利用不可と判定され、ERRORログが出力されます。
ドキュメントはCohereの ``input_type=search_document`` で、クエリは ``search_query`` で埋め込まれます。
Cohere Embed v3は、1テキストあたり最大2048文字までを受け付けます。それより長いテキストは、 ``truncate`` の設定にかかわらず、Bedrockから ``400 ValidationException`` で拒否されます。プラグインはテキストを短縮したり分割したりしません。
``truncate`` （未設定の場合は ``END`` ）が適用されるのは、2048文字以内で、かつ512トークンを超えるテキストのみです。

HTTPプロキシ経由の利用
======================

Bedrockへのリクエストは、 |Fess| 全体のHTTPプロキシ設定（ ``fess_config.properties`` の ``http.proxy.host`` 、 ``http.proxy.port`` 、 ``http.proxy.username`` 、 ``http.proxy.password`` ）を使用します。
AWSのエンドポイントを呼び出す認証情報の取得処理（Web IDフェデレーション用のSTS、コンテナ認証情報エンドポイント、インスタンスメタデータサービス）は、これらの設定を使用しません。
VPCインターフェースエンドポイント経由でBedrockに接続する場合は、 ``rag.llm.bedrock.endpoint`` （および ``content_chunker.embedding.bedrock.endpoint`` ）にそのURLを設定してください。署名に使用するリージョンは、引き続きリージョン設定で決まります。

トラブルシューティング
======================

AI検索モードが利用できない
--------------------------

クライアントは、モデルとリージョンが設定され、エンドポイントが有効なURLであり、APIキーが設定されているかAWS認証情報を解決できる場合に、自身を利用可能と判定します。
無効なリージョンやエンドポイントはERRORログに出力されます。認証情報を解決できなかった理由を確認するには、 ``org.codelibs.fess.llm.bedrock`` をDEBUGにしてください。
認証情報の取得失敗は60秒間記憶されるため、後から認証情報が利用可能になった場合も1分以内に反映されます。

アクセス拒否
------------

WARNログに ``type=AccessDeniedException`` を伴う ``403`` が出力される場合、APIキーまたはIAMプリンシパルにモデルの呼び出し権限がありません。
上記のIAM権限と、設定したリージョンでアカウントからモデルを利用できることを確認してください。

検証エラー
----------

``type=ValidationException`` を伴う ``400`` は、多くの場合、モデルIDがそのリージョンで利用できない（モデルによっては推論プロファイルIDのみ使用可能）か、 ``additional.model.request.fields`` にモデルが受け付けないパラメーターが含まれていることを意味します。

デバッグ設定
------------

``org.codelibs.fess.llm.bedrock`` をDEBUGにすると、AI検索モードのリクエストボディとレスポンスボディ、およびAWS認証情報を解決できなかった理由がログに出力されます。
``org.codelibs.fess.embedding.bedrock`` をDEBUGにすると、クエリテキストがどのように正規化されたかと、同じ認証情報の理由が出力されます。埋め込みリクエストは出力されません。
これらのロガーが、APIキー、AWS認証情報、署名を出力することはありません。

.. warning::
   これ以外の2つのロガーは、DEBUGレベルで認証情報を出力します。Apache HttpClientのワイヤーログは ``Authorization`` ヘッダーを、AWS SDKの署名処理（ ``software.amazon.awssdk.http.auth.aws.internal.signer`` ）は、一時認証情報の ``x-amz-security-token`` を含むcanonical requestを出力します。
   ルートのログレベルをDEBUGにして |Fess| を起動すると両方が有効になります。 ``org.apache.hc`` と ``software.amazon.awssdk`` はINFO以上にしてください。

参考情報
========

- :doc:`llm-overview` - LLM統合の概要
- :doc:`rag-chat` - AI検索モードの詳細
- :doc:`search-semantic` - セマンティック検索とコンテンツチャンクの埋め込み
- `Amazon Bedrock User Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html>`__
