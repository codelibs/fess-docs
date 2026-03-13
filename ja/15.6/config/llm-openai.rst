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
     - （必須）
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

- ``rag.llm.openai.{promptType}.temperature`` - 生成のランダム性（0.0〜2.0）
- ``rag.llm.openai.{promptType}.max.tokens`` - 最大トークン数
- ``rag.llm.openai.{promptType}.context.max.chars`` - コンテキストの最大文字数

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

推論モデル対応
==============

o1/o3/o4系やgpt-5系の推論モデルを使用する場合、|Fess| は自動的にOpenAI APIの ``max_completion_tokens`` パラメータを ``max_tokens`` の代わりに使用します。追加の設定変更は不要です。

推論モデル向け追加パラメータ
----------------------------

推論モデルを使用する場合、以下の追加パラメータを ``fess_config.properties`` で設定できます:

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.llm.openai.reasoning.effort``
     - o系モデルの推論effort設定（``low``、``medium``、``high``）
     - （未設定）
   * - ``rag.llm.openai.top.p``
     - トークン選択の確率閾値（0.0〜1.0）
     - （未設定）
   * - ``rag.llm.openai.frequency.penalty``
     - 頻度ペナルティ（-2.0〜2.0）
     - （未設定）
   * - ``rag.llm.openai.presence.penalty``
     - 存在ペナルティ（-2.0〜2.0）
     - （未設定）

設定例
------

::

    # o3-miniで推論effortをhighに設定
    rag.llm.openai.model=o3-mini
    rag.llm.openai.reasoning.effort=high

    # gpt-5でtop_pとペナルティを設定
    rag.llm.openai.model=gpt-5
    rag.llm.openai.top.p=0.9
    rag.llm.openai.frequency.penalty=0.5

環境変数での設定
================

セキュリティ上の理由から、APIキーを環境変数で設定することを推奨します。

Docker環境
----------

::

    docker run -e RAG_LLM_OPENAI_API_KEY=sk-xxx... codelibs/fess:15.6.0

docker-compose.yml
~~~~~~~~~~~~~~~~~~

::

    services:
      fess:
        image: codelibs/fess:15.6.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_NAME=openai
          - RAG_LLM_OPENAI_API_KEY=${OPENAI_API_KEY}
          - RAG_LLM_OPENAI_MODEL=gpt-5-mini

systemd環境
-----------

``/etc/systemd/system/fess.service.d/override.conf``:

::

    [Service]
    Environment="RAG_LLM_OPENAI_API_KEY=sk-xxx..."

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
