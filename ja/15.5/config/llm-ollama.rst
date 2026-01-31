==========================
Ollamaの設定
==========================

概要
====

Ollamaは、ローカル環境で大規模言語モデル（LLM）を実行するためのオープンソースプラットフォームです。
|Fess| のデフォルトLLMプロバイダーとして設定されており、プライベート環境での利用に適しています。

Ollamaを使用することで、データを外部に送信せずにAIチャット機能を利用できます。

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
- ``gemma3:4b`` - Google社のGemma 3（4Bパラメーター、デフォルト）
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

    # デフォルトモデル（Gemma 3 4B）をダウンロード
    ollama pull gemma3:4b

    # Llama 3.3をダウンロード
    ollama pull llama3.3:70b

    # モデルの動作確認
    ollama run gemma3:4b "Hello, how are you?"

基本設定
========

``app/WEB-INF/conf/system.properties`` に以下の設定を追加します。

最小構成
--------

::

    # AIモード機能を有効にする
    rag.chat.enabled=true

    # LLMプロバイダーをOllamaに設定
    rag.llm.type=ollama

    # OllamaのURL（ローカル環境の場合）
    rag.llm.ollama.api.url=http://localhost:11434

    # 使用するモデル
    rag.llm.ollama.model=gemma3:4b

推奨構成（本番環境）
--------------------

::

    # AIモード機能を有効にする
    rag.chat.enabled=true

    # LLMプロバイダー設定
    rag.llm.type=ollama

    # OllamaのURL
    rag.llm.ollama.api.url=http://localhost:11434

    # モデル設定（大規模モデルを使用）
    rag.llm.ollama.model=llama3.3:70b

    # タイムアウト設定（大規模モデル用に増加）
    rag.llm.ollama.timeout=120000

設定項目
========

Ollamaクライアントで使用可能なすべての設定項目です。

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
     - ``gemma3:4b``
   * - ``rag.llm.ollama.timeout``
     - リクエストのタイムアウト時間（ミリ秒）
     - ``60000``

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
        image: codelibs/fess:15.5.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_TYPE=ollama
          - RAG_LLM_OLLAMA_API_URL=http://ollama:11434
          - RAG_LLM_OLLAMA_MODEL=gemma3:4b
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
   * - ``gemma3:4b``
     - 小〜中
     - 6GB以上
     - バランスの良い汎用用途（デフォルト）
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
    ollama run gemma3:4b --verbose

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

モデルが見つからない
--------------------

**症状**: 「Configured model not found in Ollama」というログが出力される

**解決方法**:

1. モデル名が正確か確認（``:latest`` タグを含める場合がある）::

    # モデル一覧を確認
    ollama list

2. 必要なモデルをダウンロード::

    ollama pull gemma3:4b

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
- :doc:`rag-chat` - AIモード機能の詳細
