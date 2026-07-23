========================================================
セマンティック検索（コンテンツチャンク＋ベクトル検索）
========================================================

概要
====

|Fess| 15.8 では、ドキュメント本文をチャンク（断片）に分割し、各チャンクの埋め込みベクトルを
生成・格納する **コンテンツチャンク機能** がコアに統合されました。生成したベクトルは以下の2つの
用途で利用されます。

- **セマンティック検索**: キーワード（BM25）検索とベクトル検索を Rank Fusion で統合した
  ハイブリッド検索。キーワードが一致しなくても意味的に近いドキュメントがヒットします。
- **AI検索モード（RAG）**: 回答生成時に、質問と意味的に近いチャンクだけをLLMのコンテキストとして
  選択し、回答品質とトークン効率を向上させます。

本機能はすべてデフォルトで無効です。有効にしない場合、|Fess| は従来どおりキーワード検索のみで
動作します。15.7 以前の ``fess-webapp-semantic-search`` プラグインを利用していた場合は、
:ref:`semantic-search-migration` を参照してください。

処理の流れ
----------

1. クローラーが通常どおりドキュメントをインデックスに登録します（この時点ではチャンクなし）。
2. スケジューラジョブ **Content Chunk Vector Indexer** が未処理ドキュメントを検出し、
   本文をチャンクに分割して埋め込みベクトルを生成し、``content_chunk_vector`` フィールドに格納します。
3. 処理結果は ``content_chunk_status`` フィールドに記録されます（後述）。
4. ``content_chunker.search.enabled=true`` の場合、検索時にセマンティックサーチャーが
   Rank Fusion に参加します。

前提条件
========

- **OpenSearch（knnプラグイン入り）**: ベクトル検索には OpenSearch の k-NN プラグインが必要です。
  ``ghcr.io/codelibs/fess-opensearch`` イメージには同梱されています。
- **埋め込みプロバイダ**: 以下のいずれかを使用します。

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - 設定値
     - 提供元
     - 説明
   * - ``opensearch``
     - |Fess| 本体（内蔵）
     - OpenSearch ML Commons にデプロイした埋め込みモデルを使用します。追加プラグイン不要。デフォルト設定値。
   * - ``ollama``
     - ``fess-llm-ollama`` プラグイン
     - Ollama の埋め込みモデル（``nomic-embed-text`` 等）を使用します。
   * - ``openai``
     - ``fess-llm-openai`` プラグイン
     - OpenAI の埋め込みAPIを使用します。
   * - ``gemini``
     - ``fess-llm-gemini`` プラグイン
     - Google Gemini の埋め込みAPIを使用します。
   * - ``none``
     - |Fess| 本体（内蔵）
     - チャンク分割のみ実行し、ベクトルは生成しません（chunk-onlyモード）。

設定リファレンス
================

設定は「SystemProperty 系（``system.properties``）」と「FessConfig 系（``fess_config.properties``）」の
2系統に分かれています。**設定するファイルを間違えると、エラーにならずに単に無視されます** ので、
必ず以下の表のとおりのチャネルで設定してください。

system.properties の設定
------------------------

``app/WEB-INF/conf/system.properties`` に設定します（または起動オプション
``-Dfess.system.<キー名>`` で初期値を指定できます）。実行時に再読み込みされます。

.. list-table::
   :header-rows: 1
   :widths: 40 15 45

   * - プロパティ
     - デフォルト
     - 説明
   * - ``content_chunker.enabled``
     - ``false``
     - コンテンツチャンク機能全体のマスタースイッチ
   * - ``content_chunker.embedding.name``
     - ``opensearch``
     - 埋め込みプロバイダ（``opensearch`` / ``ollama`` / ``openai`` / ``gemini`` / ``none``）
   * - ``content_chunker.embedding.dimension``
     - （未設定）
     - 埋め込みベクトルの次元数。使用するモデルに合わせて **必ず設定** します（マッピング作成と検証に使用）
   * - ``content_chunker.chunker.name``
     - ``length``
     - チャンク分割方式
   * - ``content_chunker.length.chunk_size``
     - ``800``
     - 1チャンクの文字数
   * - ``content_chunker.length.overlap``
     - ``0``
     - チャンク間で重複させる文字数
   * - ``content_chunker.max_chunks_per_document``
     - ``1000``
     - 1ドキュメントあたりの最大チャンク数。超過したドキュメントは ``skipped`` になります
   * - ``content_chunker.job.concurrency``
     - ``2``
     - インデクサジョブの並列数
   * - ``content_chunker.job.bulk_size``
     - ``20``
     - 1回の取得・書き込み単位
   * - ``content_chunker.job.max_documents_per_run``
     - ``10000``
     - 1回のジョブ実行で処理する最大ドキュメント数
   * - ``content_chunker.chat.top_k``
     - ``3``
     - AI検索モードの回答生成時に選択するチャンク数
   * - ``content_chunker.search.enabled``
     - ``false``
     - セマンティック検索の Rank Fusion 統合（**有効化には再起動が必要**）
   * - ``content_chunker.search.min_score``
     - （未設定）
     - 検索結果に含める最小コサイン類似度（0〜1）。未設定の場合は足切りなし
   * - ``content_chunker.search.knn.method``
     - ``hnsw``
     - ANNインデックスのメソッド（マッピングに反映）
   * - ``content_chunker.search.knn.engine``
     - ``lucene``
     - ANNエンジン
   * - ``content_chunker.search.knn.space_type``
     - ``cosinesimil``
     - 距離空間
   * - ``content_chunker.search.knn.param.m``
     - ``16``
     - HNSW の ``m`` パラメーター
   * - ``content_chunker.search.knn.param.ef_construction``
     - ``100``
     - HNSW の ``ef_construction`` パラメーター
   * - ``content_chunker.search.knn.k``
     - ``100``
     - ANNクエリで取得する近傍数（ページング範囲が大きい場合は自動的に拡大）
   * - ``content_chunker.search.knn.param.ef_search``
     - （未設定）
     - ANNクエリの ``ef_search`` パラメーター

fess_config.properties の設定
-----------------------------

プロバイダ固有の接続設定は ``app/WEB-INF/conf/fess_config.properties`` に設定します
（Docker等では ``-Dfess.config.<キー名>`` でも指定できます）。反映には再起動が必要です。

**opensearch プロバイダ（内蔵、ML Commons）**:

.. list-table::
   :header-rows: 1
   :widths: 50 20 30

   * - プロパティ
     - デフォルト
     - 説明
   * - ``content_chunker.embedding.opensearch.model.id``
     - （必須）
     - ML Commons にデプロイ済みのモデルID
   * - ``content_chunker.embedding.opensearch.api.url``
     - 検索エンジンのアドレス
     - ML Commons API の接続先。未設定時は |Fess| が使用している検索エンジン（``http://localhost:9200`` 等）
   * - ``content_chunker.embedding.opensearch.username`` / ``password``
     - 検索エンジンの認証情報
     - 未設定時は検索エンジン接続用の認証情報にフォールバックします
   * - ``content_chunker.embedding.opensearch.timeout``
     - ``60000``
     - リクエストタイムアウト（ミリ秒）
   * - ``content_chunker.embedding.opensearch.connect.timeout``
     - ``5000``
     - 接続タイムアウト（ミリ秒）
   * - ``content_chunker.embedding.opensearch.retry.max``
     - ``3``
     - 一時的エラー（429/5xx等）のリトライ回数
   * - ``content_chunker.embedding.opensearch.retry.base.delay.ms``
     - ``2000``
     - リトライの基準待機時間（ミリ秒）
   * - ``content_chunker.embedding.opensearch.availability.check.interval``
     - ``60``
     - プロバイダ可用性チェックの間隔（秒）
   * - ``content_chunker.embedding.opensearch.document.prefix`` / ``query.prefix``
     - （空）
     - 埋め込み前にドキュメント/クエリテキストへ付与するプレフィックス

**ollama プロバイダ（fess-llm-ollama プラグイン）**:

``content_chunker.embedding.ollama.`` プレフィックスで同様の設定を行います
（``api.url`` デフォルト ``http://localhost:11434``、``model`` デフォルト ``nomic-embed-text``、
``document.prefix`` / ``query.prefix`` デフォルトはそれぞれ ``search_document:`` / ``search_query:``）。
詳細は各プラグインのドキュメントを参照してください。

セットアップ手順（opensearch プロバイダの例）
=============================================

ここでは、内蔵の ``opensearch`` プロバイダ（ML Commons）を使用した設定例を示します。

1. 埋め込みモデルのデプロイ
---------------------------

OpenSearch の ML Commons に埋め込みモデルを登録・デプロイします。
単一ノード構成では、事前に以下の設定が必要です。

.. code-block:: bash

    curl -XPUT "http://localhost:9200/_cluster/settings" \
         -H "Content-Type: application/json" -d '
    {"persistent": {"plugins.ml_commons.only_run_on_ml_node": false}}'

モデルの登録とデプロイ（例: 384次元の文埋め込みモデル）:

.. code-block:: bash

    # モデルの登録（レスポンスのtask_idからmodel_idを取得）
    curl -XPOST "http://localhost:9200/_plugins/_ml/models/_register" \
         -H "Content-Type: application/json" -d '
    {
      "name": "huggingface/sentence-transformers/all-MiniLM-L6-v2",
      "version": "1.0.2",
      "model_format": "TORCH_SCRIPT"
    }'

    # デプロイ
    curl -XPOST "http://localhost:9200/_plugins/_ml/models/<model_id>/_deploy"

    # 状態確認: model_state が DEPLOYED であること
    curl "http://localhost:9200/_plugins/_ml/models/<model_id>"

.. note::

   モデルは ``REGISTERED`` のままでは使用できません。必ずデプロイして
   ``model_state`` が ``DEPLOYED`` になったことを確認してください。

2. |Fess| の設定
----------------

``app/WEB-INF/conf/system.properties``::

    content_chunker.enabled=true
    content_chunker.embedding.name=opensearch
    content_chunker.embedding.dimension=384

``app/WEB-INF/conf/fess_config.properties``::

    content_chunker.embedding.opensearch.model.id=<model_id>

セマンティック検索も利用する場合は ``system.properties`` に以下も追加します::

    content_chunker.search.enabled=true

設定後、|Fess| を再起動します。

3. インデックスの再作成（必須）
-------------------------------

ベクトルを格納する ``content_chunk_vector`` フィールドのマッピングは、
**インデックスの新規作成時にのみ** 追加されます。既存のインデックスには反映されないため、
新規インストールの場合でも **必ずインデックスの再作成が必要** です。

管理画面 > システム > メンテナンス を開き、「再インデックス」を実行してください
（エイリアス更新を有効にした状態で実行します）。

再作成されたインデックスに、設定した次元数の ``content_chunk_vector`` マッピング
（``content_chunker.search.enabled=true`` の場合は ``index.knn: true`` と HNSW メソッド設定も）が
含まれていることを確認できます。

4. インデクサジョブの有効化
---------------------------

チャンク分割と埋め込み生成は、スケジューラジョブ **Content Chunk Vector Indexer**
（ID: ``content-chunk-vector-indexer``、デフォルト無効、スケジュール ``0 13 * * *``）が行います。

管理画面 > システム > スケジューラ で本ジョブを有効化し、「今すぐ開始」で実行します。
以後はクロール完了後にスケジュールに従って未処理ドキュメントが処理されます。

.. note::

   複数ノード構成では、本ジョブの実行対象をいずれか1ノードに固定することを推奨します。
   全ノードで同時実行しても整合性は保たれますが、同じドキュメントを各ノードが重複して
   埋め込み処理するため、プロバイダへの負荷・コストがノード数分増加します。

5. 処理状態の確認
-----------------

処理結果は各ドキュメントの ``content_chunk_status`` フィールドで確認できます。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 値
     - 意味
   * - （フィールドなし）
     - 未処理（次回のジョブ実行で処理対象）。再クロールされたドキュメントもこの状態に戻ります
   * - ``done``
     - チャンク分割とベクトル生成が完了
   * - ``chunked``
     - チャンク分割のみ完了（``embedding.name=none`` のchunk-onlyモード時）
   * - ``skipped``
     - 処理をスキップ（``max_chunks_per_document`` 超過等）
   * - ``fail``
     - 処理に失敗（ログを確認してください）

状態の分布は検索エンジンに直接問い合わせて確認できます::

    curl -XPOST "http://localhost:9200/fess.search/_search" \
         -H "Content-Type: application/json" -d '
    {"size": 0, "aggs": {"status": {"terms": {"field": "content_chunk_status", "missing": "pending"}}}}'

セマンティック検索の動作
========================

``content_chunker.search.enabled=true`` を設定すると、セマンティックサーチャーが
Rank Fusion に登録され、キーワード検索結果とベクトル検索結果が統合されます
（Rank Fusion の仕組みは :doc:`rank-fusion` を参照）。

.. warning::

   セマンティックサーチャーの登録は起動時に行われるため、**有効化には再起動が必要** です。
   無効化（``false`` への変更）はリクエストごとに判定されるため即時反映されます。

exact モードと ann モード
-------------------------

検索方式はインデックスの状態から自動選択されます。

.. list-table::
   :header-rows: 1
   :widths: 12 44 44

   * - モード
     - 条件
     - 特徴
   * - ``ann``
     - ``content_chunker.search.enabled=true`` の状態で再作成したインデックス
       （``index.knn`` と HNSW メソッド設定を持つ）
     - HNSW による近似近傍検索。大規模インデックス向け
   * - ``exact``
     - 上記以外（ベクトルはあるが k-NN 設定のないインデックス）
     - 全ベクトルとの厳密なコサイン類似度計算。小〜中規模向け

``ann`` モードを利用するには、``content_chunker.search.enabled=true`` を設定した状態で
インデックスを再作成する必要があります。既存インデックスに後から k-NN 設定を追加することは
できません。

スコアの足切り
--------------

``content_chunker.search.min_score`` にコサイン類似度（0〜1）を設定すると、
類似度がその値未満のチャンクはセマンティック検索結果から除外されます。
語彙が一致しないクエリでヒット件数が増えすぎる場合の調整に使用します::

    content_chunker.search.min_score=0.4

制限事項
--------

- フィールド指定（``title:xxx`` 等）、ブール演算子、ワイルドカード等の **検索構文を含むクエリでは、
  セマンティック検索はスキップ** され、キーワード検索のみが実行されます。ラベルやソート条件も
  内部的にクエリ構文として扱われるため、同様にスキップされます。
- 位置情報検索（ジオフィルタ）や類似ドキュメント検索と併用した場合もスキップされます。
- 埋め込みプロバイダに接続できない場合や検索エラーが発生した場合は、自動的にキーワード検索のみの
  結果になります（検索自体がエラーになることはありません）。
- ロール・仮想ホストによるアクセス制御は、セマンティック検索結果にも適用されます。

AI検索モードとの連携
====================

AI検索モード（:doc:`rag-chat`、``rag.chat.enabled=true``）が有効な場合、
``content_chunk_status`` が ``done`` のドキュメントについては、回答生成時に質問文と各チャンクの
類似度を計算し、最も関連する上位 ``content_chunker.chat.top_k`` 件（デフォルト: ``3``）の
チャンクのみをLLMのコンテキストとして使用します。

これにより、長いドキュメントでも関連部分だけがLLMに渡され、回答精度の向上とトークン使用量の
削減が期待できます。チャンク未生成のドキュメントは従来どおり本文（またはハイライト抜粋）が
使用されます。この動作は ``content_chunker.search.enabled`` とは独立しており、
チャンクとベクトルが生成されていれば利用されます。

.. _semantic-search-migration:

旧 fess-webapp-semantic-search プラグインからの移行
===================================================

|Fess| 15.7 以前でセマンティック検索を提供していた ``fess-webapp-semantic-search``
プラグインは、15.8 でコアに統合されたため **不要になりました（非推奨）**。
15.8 へアップグレードする場合は、以下の手順で移行してください。

1. **プラグインの削除**: ``app/WEB-INF/plugin/`` から ``fess-webapp-semantic-search-*.jar`` を
   削除します（Docker の場合は ``FESS_PLUGINS`` から除外します）。

2. **旧設定の削除**: 起動オプションから ``-Dfess.semantic_search.*`` の設定をすべて削除します。
   また、旧プラグイン用に ``-Drank.fusion.searchers=default,semantic`` を指定していた場合は
   削除します（指定したままだと新しいセマンティックサーチャーが使用されません）。

3. **旧 ingest pipeline のデタッチ**: 旧プラグインはインデックスに ``default_pipeline``
   （ニューラル検索用の ingest pipeline）を設定しています。**プラグインを削除しても
   pipeline はインデックス側に残り、動作し続ける** ため、必ず解除してください::

       curl -XPUT "http://localhost:9200/fess.search/_settings" \
            -H "Content-Type: application/json" -d '
       {"index": {"default_pipeline": null}}'

4. **新設定の追加**: 本ページの設定リファレンスに従い、``content_chunker.*`` の設定を
   行います。ML Commons のモデルを引き続き使用する場合は
   ``content_chunker.embedding.name=opensearch`` を指定し、既存の ``model_id`` を
   ``content_chunker.embedding.opensearch.model.id`` に設定します。

5. **インデックスの再作成とジョブ実行**: 管理画面 > システム > メンテナンス で再インデックスを
   実行し、Content Chunk Vector Indexer ジョブを有効化・実行します。

注意事項
========

埋め込みモデル（次元数）の変更
------------------------------

埋め込みモデルを次元数の異なるモデルへ変更する場合は、以下の順序で行います。

1. 既存の古いベクトルを削除します（次元数の異なる古いベクトルが残っていると、
   新しいマッピングへの再インデックスが失敗します）::

       curl -XPOST "http://localhost:9200/fess.search/_update_by_query" \
            -H "Content-Type: application/json" -d '
       {
         "query": {"exists": {"field": "content_chunk_status"}},
         "script": {"source": "ctx._source.remove(\"content_chunk_vector\"); ctx._source.remove(\"content_chunk_status\")"}
       }'

2. ``content_chunker.embedding.dimension`` と各プロバイダのモデル設定を変更します。
3. インデックスを再作成し、インデクサジョブを再実行します。

ディスク使用量
--------------

チャンクベクトルは検索用のインデックス構造に加えて ``_source`` にも保持されるため、
ドキュメントあたり「チャンク数 × 次元数」に比例したディスク容量を追加で消費します。
容量が問題になる場合は ``content_chunker.length.chunk_size`` や
``content_chunker.max_chunks_per_document`` で調整してください。

chunk-only モード
-----------------

``content_chunker.embedding.name=none`` を設定すると、埋め込みベクトルを生成せずに
チャンク分割のみを行います（``content_chunk_status`` は ``chunked``）。
埋め込みプロバイダの準備前にチャンク分割だけを先行して実行しておき、後からプロバイダを設定して
ジョブを再実行すると、格納済みのチャンクに対してベクトルだけが追加生成されます
（再分割は行われません）。

参考情報
========

- :doc:`rank-fusion` - Rank Fusion（ハイブリッド検索）の設定
- :doc:`rag-chat` - AI検索モード機能の設定
- :doc:`llm-overview` - LLM統合の概要
- :doc:`llm-ollama` - Ollamaの設定
