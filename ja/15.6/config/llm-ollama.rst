==========================
Ollamaの設定
==========================

概要
====

Ollamaは、ローカル環境で大規模言語モデル（LLM）を実行するためのオープンソースプラットフォームです。
|Fess| 15.6では、Ollama連携機能はプラグイン ``fess-llm-ollama`` として提供されており、プライベート環境での利用に適しています。

Ollamaを使用することで、データを外部に送信せずにAI検索モード機能を利用できます。

主な特徴
--------

- **ローカル実行**: データは外部に送信されず、プライバシーを確保
- **多様なモデル**: Llama、Mistral、Gemma、CodeLlamaなど多数のモデルに対応
- **コスト効率**: APIコストがかからない（ハードウェアコストのみ）
- **カスタマイズ**: 独自にファインチューニングしたモデルも利用可能

対応モデル
----------

Ollamaで利用可能な主なモデル:

- ``llama3.3:70b`` - Meta社のLlama 3.3（70Bパラメーター）
- ``gemma4:e4b`` - Google社のGemma 4（E4Bパラメーター、デフォルト）
- ``mistral:7b`` - Mistral AI社のMistral（7Bパラメーター）
- ``codellama:13b`` - Meta社のCode Llama（13Bパラメーター）
- ``phi3:3.8b`` - Microsoft社のPhi-3（3.8Bパラメーター）

.. note::
   利用可能なモデルの最新リストは `Ollama Library <https://ollama.com/library>`__ で確認できます。

前提条件
========

Ollamaを使用する前に、以下を確認してください。

1. **Ollamaのインストール**: `https://ollama.com/ <https://ollama.com/>`__ からダウンロードしてインストール
2. **モデルのダウンロード**: 使用するモデルをOllamaにダウンロード
3. **Ollamaサーバーの起動**: Ollamaが動作していることを確認

Ollamaのインストール
--------------------

Linux/macOS
~~~~~~~~~~~

::

    curl -fsSL https://ollama.com/install.sh | sh

Windows
~~~~~~~

公式サイトからインストーラーをダウンロードして実行します。

Docker
~~~~~~

::

    docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

モデルのダウンロード
--------------------

::

    # デフォルトモデル（Gemma 4 E4B）をダウンロード
    ollama pull gemma4:e4b

    # Llama 3.3をダウンロード
    ollama pull llama3.3:70b

    # モデルの動作確認
    ollama run gemma4:e4b "Hello, how are you?"

プラグインのインストール
========================

|Fess| 15.6では、Ollama連携機能はプラグインとして分離されました。
Ollamaを利用するには ``fess-llm-ollama`` プラグインのインストールが必要です。

1. `fess-llm-ollama-15.6.0.jar` をダウンロードします。
2. |Fess| のインストールディレクトリ内の ``app/WEB-INF/plugin/`` ディレクトリに配置します。

::

    cp fess-llm-ollama-15.6.0.jar /path/to/fess/app/WEB-INF/plugin/

3. |Fess| を再起動します。

.. note::
   プラグインのバージョンは |Fess| のバージョンと合わせてください。

基本設定
========

|Fess| 15.6では、LLM関連の設定は複数の設定ファイルに分かれています。

最小構成
--------

``app/WEB-INF/conf/fess_config.properties``:

::

    # AI検索モード機能を有効にする
    rag.chat.enabled=true

``system.properties``（管理画面 > システム > 全般 でも設定可能）:

::

    # LLMプロバイダーをOllamaに設定
    rag.llm.name=ollama

``app/WEB-INF/conf/fess_config.properties``:

::

    # AI検索モード機能を有効にする
    rag.chat.enabled=true

    # OllamaのURL（ローカル環境の場合）
    rag.llm.ollama.api.url=http://localhost:11434

    # 使用するモデル
    rag.llm.ollama.model=gemma4:e4b

.. note::
   LLMプロバイダーの設定は、管理画面（管理画面 > システム > 全般）から ``rag.llm.name`` を設定することもできます。

推奨構成（本番環境）
--------------------

``system.properties``（管理画面 > システム > 全般 でも設定可能）:

::

    # LLMプロバイダー設定
    rag.llm.name=ollama

``app/WEB-INF/conf/fess_config.properties``:

::

    # AI検索モード機能を有効にする
    rag.chat.enabled=true

    # OllamaのURL
    rag.llm.ollama.api.url=http://localhost:11434

    # モデル設定（大規模モデルを使用）
    rag.llm.ollama.model=llama3.3:70b

    # タイムアウト設定（大規模モデル用に増加）
    rag.llm.ollama.timeout=120000

    # 同時リクエスト数の制御
    rag.llm.ollama.max.concurrent.requests=5

設定項目
========

Ollamaクライアントで使用可能なすべての設定項目です。 ``rag.llm.name`` 以外はすべて ``fess_config.properties`` に設定します。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.llm.ollama.api.url``
     - OllamaサーバーのベースURL
     - ``http://localhost:11434``
   * - ``rag.llm.ollama.model``
     - 使用するモデル名（Ollamaにダウンロード済みのモデル）
     - ``gemma4:e4b``
   * - ``rag.llm.ollama.timeout``
     - リクエストのタイムアウト時間（ミリ秒）
     - ``60000``
   * - ``rag.llm.ollama.availability.check.interval``
     - 可用性チェック間隔（秒）
     - ``60``
   * - ``rag.llm.ollama.max.concurrent.requests``
     - 最大同時リクエスト数
     - ``5``
   * - ``rag.llm.ollama.chat.evaluation.max.relevant.docs``
     - 評価最大関連ドキュメント数
     - ``3``

同時実行制御
------------

``rag.llm.ollama.max.concurrent.requests`` を使用して、Ollamaへの同時リクエスト数を制御できます。
デフォルトは5です。Ollamaサーバーのリソースに応じて調整してください。
同時リクエスト数が多すぎるとOllamaサーバーに負荷がかかり、応答速度が低下する場合があります。

プロンプトタイプ別設定
======================

|Fess| では、プロンプトタイプごとにLLMのパラメーターをカスタマイズできます。
設定は ``fess_config.properties`` に記述します。

プロンプトタイプ別に以下のパラメーターを設定できます:

- ``rag.llm.ollama.{promptType}.temperature`` - 生成時のtemperature
- ``rag.llm.ollama.{promptType}.max.tokens`` - 最大トークン数
- ``rag.llm.ollama.{promptType}.context.max.chars`` - コンテキストの最大文字数

利用可能なプロンプトタイプ:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - プロンプトタイプ
     - 説明
   * - ``intent``
     - ユーザーの意図を判定するプロンプト
   * - ``evaluation``
     - 検索結果の評価プロンプト
   * - ``unclear``
     - 不明確なクエリへの応答プロンプト
   * - ``noresults``
     - 検索結果なしの場合のプロンプト
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

設定例::

    # 回答生成時のtemperatureを設定
    rag.llm.ollama.answer.temperature=0.7

    # 要約生成時の最大トークン数を設定
    rag.llm.ollama.summary.max.tokens=2048

    # 意図判定時のコンテキスト最大文字数を設定
    rag.llm.ollama.intent.context.max.chars=4000

Ollamaモデルオプション
======================

Ollamaのモデルパラメーターを ``fess_config.properties`` で設定できます。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.llm.ollama.top.p``
     - Top-Pサンプリングの値（0.0〜1.0）
     - (未設定)
   * - ``rag.llm.ollama.top.k``
     - Top-Kサンプリングの値
     - (未設定)
   * - ``rag.llm.ollama.num.ctx``
     - コンテキストウィンドウサイズ
     - (未設定)
   * - ``rag.llm.ollama.default.*``
     - デフォルトフォールバック設定
     - (未設定)
   * - ``rag.llm.ollama.options.*``
     - グローバルオプション
     - (未設定)

設定例::

    # Top-Pサンプリング
    rag.llm.ollama.top.p=0.9

    # Top-Kサンプリング
    rag.llm.ollama.top.k=40

    # コンテキストウィンドウサイズ
    rag.llm.ollama.num.ctx=4096

思考モデル対応
==============

gemma4やqwen3などの思考モデル（thinking model）を使用する場合、 |Fess| は思考バジェット（thinking budget）の設定をサポートしています。

思考バジェットはプロンプトタイプごとに ``fess_config.properties`` で設定します:

::

    # 回答生成時の思考バジェットの設定
    rag.llm.ollama.answer.thinking.budget=1024

    # 要約生成時の思考バジェットの設定
    rag.llm.ollama.summary.thinking.budget=1024

思考バジェットを設定することで、モデルが回答を生成する前に「考える」ステップに割り当てるトークン数を制御できます。

ネットワーク構成
================

Dockerでの構成
--------------

|Fess| とOllamaの両方をDockerで実行する場合の構成例です。

``docker-compose.yml``:

::

    version: '3'
    services:
      fess:
        image: codelibs/fess:15.6.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_NAME=ollama
          - RAG_LLM_OLLAMA_API_URL=http://ollama:11434
          - RAG_LLM_OLLAMA_MODEL=gemma4:e4b
        depends_on:
          - ollama
        # ... その他の設定

      ollama:
        image: ollama/ollama
        volumes:
          - ollama_data:/root/.ollama
        ports:
          - "11434:11434"

    volumes:
      ollama_data:

.. note::
   Docker Compose環境では、ホスト名として ``ollama`` を使用します（``localhost`` ではなく）。

リモートOllamaサーバー
----------------------

OllamaをFessとは別のサーバーで実行する場合:

::

    rag.llm.ollama.api.url=http://ollama-server.example.com:11434

.. warning::
   Ollamaはデフォルトで認証機能を持たないため、外部からアクセス可能にする場合は
   ネットワークレベルでのセキュリティ対策（ファイアウォール、VPN等）を検討してください。

モデルの選択ガイド
==================

使用目的に応じたモデル選択の指針です。

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - モデル
     - サイズ
     - 必要VRAM
     - 用途
   * - ``phi3:3.8b``
     - 小
     - 4GB以上
     - 軽量環境、シンプルな質問応答
   * - ``gemma4:e4b``
     - 小〜中
     - 8GB以上
     - バランスの良い汎用用途、思考モード対応（デフォルト）
   * - ``mistral:7b``
     - 中
     - 8GB以上
     - 高品質な回答が必要な場合
   * - ``llama3.3:70b``
     - 大
     - 48GB以上
     - 最高品質の回答、複雑な推論

GPU対応
-------

OllamaはGPUアクセラレーションをサポートしています。NVIDIAのGPUを使用することで、
推論速度が大幅に向上します。

::

    # GPU対応の確認
    ollama run gemma4:e4b --verbose

トラブルシューティング
======================

接続エラー
----------

**症状**: チャット機能でエラーが発生する、LLMが利用不可と表示される

**確認事項**:

1. Ollamaが動作しているか確認::

    curl http://localhost:11434/api/tags

2. モデルがダウンロードされているか確認::

    ollama list

3. ファイアウォールの設定を確認

4. ``fess-llm-ollama`` プラグインが ``app/WEB-INF/plugin/`` に配置されているか確認

モデルが見つからない
--------------------

**症状**: 「Configured model not found in Ollama」というログが出力される

**解決方法**:

1. モデル名が正確か確認（``:latest`` タグを含める場合がある）::

    # モデル一覧を確認
    ollama list

2. 必要なモデルをダウンロード::

    ollama pull gemma4:e4b

タイムアウト
------------

**症状**: リクエストがタイムアウトする

**解決方法**:

1. タイムアウト時間を延長::

    rag.llm.ollama.timeout=120000

2. より小さなモデルを使用するか、GPU環境を検討

デバッグ設定
------------

問題を調査する際は、|Fess| のログレベルを調整してOllama関連の詳細なログを出力できます。

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.ollama" level="DEBUG"/>

参考情報
========

- `Ollama公式サイト <https://ollama.com/>`__
- `Ollamaモデルライブラリ <https://ollama.com/library>`__
- `Ollama GitHub <https://github.com/ollama/ollama>`__
- :doc:`llm-overview` - LLM統合の概要
- :doc:`rag-chat` - AI検索モード機能の詳細
