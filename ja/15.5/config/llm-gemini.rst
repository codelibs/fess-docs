==========================
Google Geminiの設定
==========================

概要
====

Google Geminiは、Google社が提供する最先端の大規模言語モデル（LLM）です。
|Fess| ではGoogle AI API（Generative Language API）を使用してGeminiモデルによるAIモード機能を実現できます。

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

基本設定
========

``app/WEB-INF/conf/fess_config.properties`` に以下の設定を追加します。

最小構成
--------

::

    # AIモード機能を有効にする
    rag.chat.enabled=true

    # LLMプロバイダーをGeminiに設定
    rag.llm.type=gemini

    # Gemini APIキー
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # 使用するモデル
    rag.llm.gemini.model=gemini-3-flash-preview

推奨構成（本番環境）
--------------------

::

    # AIモード機能を有効にする
    rag.chat.enabled=true

    # LLMプロバイダー設定
    rag.llm.type=gemini

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

Geminiクライアントで使用可能なすべての設定項目です。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.llm.gemini.api.key``
     - Google AI APIキー
     - （必須）
   * - ``rag.llm.gemini.model``
     - 使用するモデル名
     - ``gemini-3-flash-preview``
   * - ``rag.llm.gemini.api.url``
     - APIのベースURL
     - ``https://generativelanguage.googleapis.com/v1beta``
   * - ``rag.llm.gemini.timeout``
     - リクエストのタイムアウト時間（ミリ秒）
     - ``60000``

環境変数での設定
================

セキュリティ上の理由から、APIキーを環境変数で設定することを推奨します。

Docker環境
----------

::

    docker run -e RAG_LLM_GEMINI_API_KEY=AIzaSy... codelibs/fess:15.5.0

docker-compose.yml
~~~~~~~~~~~~~~~~~~

::

    services:
      fess:
        image: codelibs/fess:15.5.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_TYPE=gemini
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

    # より多くのドキュメントをコンテキストに含める
    rag.chat.context.max.documents=10
    rag.chat.context.max.chars=20000

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

レート制限
==========

Google AI APIにはレート制限があります。|Fess| のレート制限機能と組み合わせて適切に設定してください。

::

    # Fessのレート制限設定
    rag.chat.rate.limit.enabled=true
    rag.chat.rate.limit.requests.per.minute=10

無料枠の制限
------------

Google AI APIには無料枠がありますが、以下の制限があります:

- リクエスト/分: 15 RPM
- トークン/分: 100万 TPM
- リクエスト/日: 1,500 RPD

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

1. |Fess| のレート制限を厳しく設定::

    rag.chat.rate.limit.requests.per.minute=5

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
- :doc:`rag-chat` - AIモード機能の詳細
