==========================
OpenAIの設定
==========================

概要
====

OpenAIは、GPT-4をはじめとする高性能な大規模言語モデル（LLM）を提供するクラウドサービスです。
|Fess| ではOpenAI APIを使用してAIモード機能を実現できます。

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

- ``gpt-4o`` - 高性能マルチモーダルモデル
- ``gpt-4o-mini`` - GPT-4oの軽量版（コスト効率が良い）
- ``o3-mini`` - 推論特化の軽量モデル
- ``o4-mini`` - 推論特化の次世代軽量モデル
- ``gpt-4-turbo`` - GPT-4の高速版
- ``gpt-3.5-turbo`` - コストパフォーマンスに優れたモデル

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

基本設定
========

``app/WEB-INF/conf/fess_config.properties`` に以下の設定を追加します。

最小構成
--------

::

    # AIモード機能を有効にする
    rag.chat.enabled=true

    # LLMプロバイダーをOpenAIに設定
    rag.llm.type=openai

    # OpenAI APIキー
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # 使用するモデル
    rag.llm.openai.model=gpt-4o-mini

推奨構成（本番環境）
--------------------

::

    # AIモード機能を有効にする
    rag.chat.enabled=true

    # LLMプロバイダー設定
    rag.llm.type=openai

    # OpenAI APIキー
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # モデル設定（高性能モデルを使用）
    rag.llm.openai.model=gpt-4o

    # APIエンドポイント（通常は変更不要）
    rag.llm.openai.api.url=https://api.openai.com/v1

    # タイムアウト設定
    rag.llm.openai.timeout=60000

設定項目
========

OpenAIクライアントで使用可能なすべての設定項目です。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.llm.openai.api.key``
     - OpenAI APIキー
     - （必須）
   * - ``rag.llm.openai.model``
     - 使用するモデル名
     - ``gpt-4o-mini``
   * - ``rag.llm.openai.api.url``
     - APIのベースURL
     - ``https://api.openai.com/v1``
   * - ``rag.llm.openai.timeout``
     - リクエストのタイムアウト時間（ミリ秒）
     - ``60000``

環境変数での設定
================

セキュリティ上の理由から、APIキーを環境変数で設定することを推奨します。

Docker環境
----------

::

    docker run -e RAG_LLM_OPENAI_API_KEY=sk-xxx... codelibs/fess:15.5.0

docker-compose.yml
~~~~~~~~~~~~~~~~~~

::

    services:
      fess:
        image: codelibs/fess:15.5.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_TYPE=openai
          - RAG_LLM_OPENAI_API_KEY=${OPENAI_API_KEY}
          - RAG_LLM_OPENAI_MODEL=gpt-4o-mini

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
   * - ``gpt-3.5-turbo``
     - 低
     - 良好
     - 一般的な質問応答、コスト重視
   * - ``gpt-4o-mini``
     - 中
     - 高
     - バランスの取れた用途（推奨）
   * - ``gpt-4o``
     - 高
     - 最高
     - 複雑な推論、高品質が必要な場合
   * - ``o3-mini`` / ``o4-mini``
     - 中
     - 最高
     - 数学・コーディングなどの推論タスク
   * - ``gpt-4-turbo``
     - 高
     - 最高
     - 高速レスポンスが必要な場合

コストの目安
------------

OpenAI APIは使用量に基づいて課金されます。以下は2024年時点の参考価格です。

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - モデル
     - 入力（1Kトークン）
     - 出力（1Kトークン）
   * - gpt-3.5-turbo
     - $0.0005
     - $0.0015
   * - gpt-4o-mini
     - $0.00015
     - $0.0006
   * - gpt-4o
     - $0.005
     - $0.015

.. note::
   最新の価格は `OpenAI Pricing <https://openai.com/pricing>`__ で確認してください。

レート制限
==========

OpenAI APIにはレート制限があります。|Fess| のレート制限機能と組み合わせて適切に設定してください。

::

    # Fessのレート制限設定
    rag.chat.rate.limit.enabled=true
    rag.chat.rate.limit.requests.per.minute=10

OpenAIのTier別制限
------------------

OpenAIアカウントのTierに応じて制限が異なります:

- **Free**: 3 RPM（リクエスト/分）
- **Tier 1**: 500 RPM
- **Tier 2**: 5,000 RPM
- **Tier 3+**: さらに高い制限

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

1. |Fess| のレート制限を厳しく設定::

    rag.chat.rate.limit.requests.per.minute=5

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

    rag.llm.openai.timeout=120000

2. より高速なモデル（gpt-3.5-turbo等）を検討

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
- :doc:`rag-chat` - AIモード機能の詳細
