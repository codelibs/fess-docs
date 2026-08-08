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
動作します。15.7 以前から |Fess| をアップグレードする場合や、``fess-webapp-semantic-search``
プラグインを利用していた場合は、:ref:`semantic-search-migration` を参照してください。

処理の流れ
----------

1. クローラーが通常どおりドキュメントをインデックスに登録します（この時点ではチャンクなし）。
2. スケジューラジョブ **Content Chunk Vector Indexer** が未処理ドキュメントを検出し、
   本文（``content`` フィールド）をチャンクに分割して埋め込みベクトルを生成し、
   ``content_chunk_vector`` フィールドに格納します。このとき ``content`` フィールド自体も
   チャンクの配列に書き換えられます（``content_length`` は元の値のままです）。
3. 処理結果は ``content_chunk_status`` フィールドに記録されます（後述）。
4. ``content_chunker.search.enabled=true`` の場合、検索時にセマンティックサーチャーが
   Rank Fusion に参加します。

前提条件
========

- **OpenSearch（k-NN プラグイン入り）**: |Fess| 15.8 では、コンテンツチャンク機能を有効にしているか
  どうかにかかわらず、検索インデックス（``fess.search``）のマッピングに ``content_chunk_vector``
  フィールド（``nested`` 型。その ``vector`` サブフィールドが ANN 用の ``knn_vector`` 型）が
  常に含まれ、インデックス設定にも ``index.knn: true`` が常に含まれます。そのため OpenSearch に
  k-NN プラグインが入っていないと、インデックスの新規作成自体が失敗し、|Fess| は起動できません。

  .. list-table::
     :header-rows: 1
     :widths: 35 65

     * - 構成
       - k-NN プラグインの対応状況
     * - 組み込み OpenSearch（``bin/fess``、または ``SEARCH_ENGINE_HTTP_URL`` を未設定のままにした
         場合の TAR.GZ/ZIP 版のデフォルト状態）
       - k-NN プラグインが同梱されています。ただし JNI ネイティブライブラリを含まないため、
         対応する ANN エンジンは ``lucene`` のみです。``content_chunker.search.knn.engine`` は
         ``faiss`` も値として受け付けており、ここで設定してもマッピング自体は正常に作成されます
         が、**書き込みのたびに文書が黙って失われ、検索結果も0件になります**\ （この組み合わせの
         まま起動すると、起動時に警告ログが出力されます）。
     * - Docker（``ghcr.io/codelibs/fess-opensearch``）、RPM/DEB 版（常に別途インストールした外部
         OpenSearch に接続します）、または外部 OpenSearch（標準配布）
       - ``faiss`` を含めてフルサポートされます。
     * - 外部 OpenSearch の **minimal 配布**
       - **非対応です**。k-NN プラグインを含まないため、インデックスの新規作成に失敗します。

  ``content_chunker.search.knn.engine`` は、上記いずれの構成でも ``nmslib`` を値として受け付けま
  せん。``content_chunk_vector`` は ``nested`` フィールドであり、k-NN プラグインが nested
  フィールドに対応するエンジンは ``lucene`` / ``faiss`` のみだからです（``nmslib`` は
  OpenSearch 3.0 以降で非推奨・利用制限もされています）。設定すると警告ログとともに ``lucene``
  にフォールバックします。ANN 関連の他の設定値については後述の「設定リファレンス」を参照して
  ください。

- **外部クラスタの OpenSearch バージョン**: 同梱の ``fess.search`` インデックス設定は、
  ``fess_indices/fess.json``\ （および AWS/cloud 版）で ``index.knn`` と
  ``knn.derived_source.enabled`` を常に送信します。後者は k-NN プラグインの比較的新しい設定で、
  これを認識できない古い OpenSearch では、k-NN プラグインの有無にかかわらずインデックスの作成に
  失敗します。|Fess| 15.8 が対応する OpenSearch のバージョンについては
  :doc:`../install/prerequisites` を参照してください。

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

``content_chunker.*`` の設定はすべて「システムプロパティ（``system.properties``）」に統一されて
います。``app/WEB-INF/conf/system.properties``\ （RPM/DEB 版は ``/etc/fess/system.properties``、
Docker 版は ``/opt/fess/system.properties``）に設定するか、起動オプション
``-Dfess.system.<キー名>`` で初期値を指定します。値は実行時に再読み込みされるため、ほとんどの
設定は変更後すぐに反映されます。ただし ``content_chunker.search.enabled`` の有効化
（``false`` → ``true``）だけは、セマンティックサーチャーの登録が起動時にしか行われないため、
**反映には再起動が必要** です。

.. note::

   ``content_chunker.*`` のキー一覧は ``fess_config.properties`` にもコメントとして記載されて
   いますが、これらは ``system.properties`` チャネルからのみ読み込まれます。
   ``fess_config.properties`` や ``-Dfess.config.<キー名>`` に記述しても無視されるため、必ず
   ``system.properties`` に設定してください。なお 管理画面 > システム情報 > 設定情報 は現在値の
   **閲覧専用** の画面で、この画面から ``content_chunker.*`` を設定することはできません。

system.properties の設定
------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 15 45

   * - プロパティ
     - デフォルト
     - 説明
   * - ``content_chunker.enabled``
     - ``false``
     - コンテンツチャンク機能全体のマスタースイッチ
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
   * - ``content_chunker.embedding.name``
     - ``opensearch``
     - 埋め込みプロバイダ（``opensearch`` / ``ollama`` / ``openai`` / ``gemini`` / ``none``）
   * - ``content_chunker.embedding.dimension``
     - ``768``
     - 埋め込みベクトルの次元数。マッピング作成時にこの値が使われるため、使用する埋め込みモデルの
       次元数に **必ず** 合わせて設定してください。この値には読み取り経路が2つあり、挙動が
       異なります。インデックスのマッピング作成時は、未設定・非数値・0 以下・``16000``\ （k-NN
       プラグイン自体の上限）超のいずれでも、警告とともに ``768`` が使われます。一方、埋め込み
       処理の実行時にはフォールバックがなく、未設定・非数値・0 以下はいずれもエラーになります。
       ``16000`` を超える値は実行時には拒否されないため、マッピングだけが ``768`` で作成されて
       次元不一致になります
   * - ``content_chunker.job.concurrency``
     - ``2``
     - インデクサジョブの並列数
   * - ``content_chunker.job.bulk_size``
     - ``20``
     - 1回の取得・書き込み単位
   * - ``content_chunker.job.max_documents_per_run``
     - ``-1``\ （無制限）
     - 1回のジョブ実行で処理する最大ドキュメント数。``0`` 以下の値はすべて無制限として扱われます
   * - ``content_chunker.job.retry_failed``
     - ``false``
     - ``true`` にすると、前回の実行で ``content_chunk_status=fail`` になったドキュメントも次回
       実行時の処理対象に含めます。自動リトライや試行回数の記録はなく、原因を修正した後に
       一時的に有効化して再試行する運用を想定しています
   * - ``content_chunker.chat.top_k``
     - ``3``
     - AI検索モードの回答生成時に選択するチャンク数
   * - ``content_chunker.search.enabled``
     - ``false``
     - セマンティック検索の Rank Fusion 統合（**有効化には再起動が必要**）
   * - ``content_chunker.search.min_score``
     - （未設定）
     - 検索結果に含める最小コサイン類似度（0〜1）。未設定の場合は足切りなし。``ann`` モードでは
       ``search.knn.space_type`` が ``cosinesimil`` 以外の場合、コサイン基準の足切りを定義できない
       ため、警告とともにスキップされます
   * - ``content_chunker.search.knn.method``
     - ``hnsw``
     - ANNインデックスのメソッド。現時点で受け付けられる値は ``hnsw`` のみで、それ以外の値は
       警告とともに ``hnsw`` にフォールバックします（マッピングに反映。変更にはインデックスの
       再作成が必要）
   * - ``content_chunker.search.knn.engine``
     - ``lucene``
     - ANNエンジン。受け付けられる値は ``lucene`` または ``faiss`` のみです（前提条件を参照）。
       それ以外の値は警告とともに ``lucene`` にフォールバックします（マッピングに反映。変更には
       インデックスの再作成が必要）
   * - ``content_chunker.search.knn.space_type``
     - ``cosinesimil``
     - 距離空間。受け付けられる値は ``cosinesimil``、``innerproduct``、``l2`` のみで、それ以外の
       値は警告とともに ``cosinesimil`` にフォールバックします（マッピングに反映。変更には
       インデックスの再作成が必要）
   * - ``content_chunker.search.knn.k``
     - ``100``
     - ANNクエリで取得する近傍数（ページング範囲が大きい場合は自動的に拡大）
   * - ``content_chunker.search.knn.param.ef_search``
     - （未設定）
     - ANNクエリの ``ef_search`` パラメーター

.. note::

   HNSW の ``m`` と ``ef_construction`` パラメーターは ``doc.json`` に固定値
   （``m=16`` / ``ef_construction=100``）として組み込まれており、設定では変更できません。

opensearch プロバイダの接続設定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

内蔵の ``opensearch`` プロバイダ（OpenSearch ML Commons）を使う場合の接続設定です。
上記と同じ ``system.properties`` に設定します。

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
     - 未設定時は検索エンジン接続用の認証情報にフォールバックします。ただしこれは ``api.url``
       が未設定の間（＝接続先が |Fess| 自身が使用している検索エンジンと同じ場合）に限られ、
       ``api.url`` を設定するとフォールバックされません
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

.. warning::

   ``system.properties`` の内容は 管理画面 > システム情報 > 設定情報 の「アプリのプロパティ」で
   閲覧できます。``content_chunker.embedding.opensearch.password`` はこの画面では ``XXXXXXXX``
   にマスクされますが、``username`` はそのまま表示されます。また、``-Dfess.system.<キー名>`` で
   指定した値は同じ画面の「システムのプロパティ」に **マスクされずに** 表示されるため、認証情報は
   起動オプションではなく ``system.properties`` に記述してください。

その他のプロバイダ（ollama / openai / gemini）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ollama`` プロバイダ（``fess-llm-ollama`` プラグイン）は、
``content_chunker.embedding.ollama.`` プレフィックスで同様の設定を行います
（``api.url`` デフォルト ``http://localhost:11434``、``model`` デフォルト ``embeddinggemma``、
``document.prefix`` / ``query.prefix`` デフォルトはそれぞれ ``title: none | text:`` /
``task: search result | query:``）。``nomic-embed-text`` 系のモデルを使用する場合は、
``document.prefix`` / ``query.prefix`` に ``search_document:`` / ``search_query:`` を明示的に
設定してください。これらのプレフィックスは埋め込み対象のテキストへそのまま連結される
（前後の空白はトリムされない）ため、上記のデフォルト値も ``search_document:`` /
``search_query:`` も、いずれも **末尾に半角スペースを1つ含みます**。自分で設定する場合は、
区切りの半角スペースを忘れないでください。
``openai`` / ``gemini`` プロバイダも同様に、それぞれ ``content_chunker.embedding.openai.`` /
``content_chunker.embedding.gemini.`` プレフィックスで設定します。設定キーの詳細は各プラグインの
ドキュメントを参照してください。

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

    # タスクの完了確認と model_id の取得（state が COMPLETED になると model_id が返ります）
    curl "http://localhost:9200/_plugins/_ml/tasks/<task_id>"

    # デプロイ
    curl -XPOST "http://localhost:9200/_plugins/_ml/models/<model_id>/_deploy"

    # 状態確認: model_state が DEPLOYED であること
    curl "http://localhost:9200/_plugins/_ml/models/<model_id>"

.. note::

   モデルは ``REGISTERED`` のままでは使用できません。必ずデプロイして
   ``model_state`` が ``DEPLOYED`` になったことを確認してください。

2. |Fess| の設定
----------------

``app/WEB-INF/conf/system.properties``\ （RPM/DEB 版は ``/etc/fess/system.properties``、
Docker 版は ``/opt/fess/system.properties``。以下はすべて同じファイルに記述します）::

    content_chunker.enabled=true
    content_chunker.embedding.name=opensearch
    content_chunker.embedding.dimension=384
    content_chunker.embedding.opensearch.model.id=<model_id>

セマンティック検索も利用する場合は、続けて以下も追加します::

    content_chunker.search.enabled=true

設定後、|Fess| を再起動します。

3. インデックスの再作成（既存の環境で有効化する場合）
-----------------------------------------------------

``content_chunk_vector`` フィールドのマッピング（設定した次元数・ANNメソッド設定を含む）は、
``fess.search`` インデックスが **新規作成される時点で** 適用されます。

- **新規インストールの場合**: |Fess| を初めて起動する前に、上記の設定を
  ``system.properties`` に反映しておけば、最初のインデックス作成時に正しいマッピングが
  自動的に適用されるため、このステップは不要です。
- **既にインデックスが存在する場合**\ （一度でも |Fess| を起動したことがある場合）: 稼働中の
  インデックスへは反映されません。既存のマッピングへの後付けもできないため、以下の手順で
  インデックスを再作成してください。

  管理画面 > システム情報 > メンテナンス を開き、「再インデクシング」の「エイリアスの更新」を
  有効にした状態で実行してください。

  再作成されたインデックスに、インデックス設定の ``index.knn: true`` と、設定した次元数・ANN
  メソッド設定を持つ ``content_chunk_vector`` マッピングが含まれていることを確認できます
  （``index.knn`` はインデックス設定、ANN メソッド設定はマッピングと、適用先が異なります）。

.. warning::

   「再インデクシング」はバックグラウンドの非同期処理として実行され、管理画面には完了を示す
   通知は表示されません。``_cat/indices`` はインデックスが存在すること（health・件数など）を
   示すだけで、エイリアスがどちらのインデックスを指しているかは分かりません。以下の
   インデクサジョブの手順に進む前に、``_cat/aliases`` で ``fess.search`` と ``fess.update``
   の両方が新しいインデックスを指していることを確認してください。|Fess| のログは失敗時にのみ
   警告を出力するため、ログが静かであることは成功の証拠にはならず、既知の失敗が起きていない
   ことを示すに過ぎません。旧インデックス（それまで ``fess.search`` エイリアスが指していた
   実体インデックスで、``fess.<timestamp>`` という名前を持ちます）は自動削除されないため、
   不要になった時点で手動で削除してください。新旧両方のインデックスが存在する間は、
   インデックス用のディスク使用量がおおむね通常の2倍になります。

4. インデクサジョブの有効化
---------------------------

チャンク分割と埋め込み生成は、スケジューラジョブ **Content Chunk Vector Indexer**
（ID: ``content-chunk-vector-indexer``、デフォルト無効、スケジュール ``0 13 * * *``）が行います。

管理画面 > システム > スケジューラ で本ジョブを有効化し、「今すぐ開始」で実行します。
以後は、クロールの完了とは無関係に、設定したスケジュール（既定は毎日 13:00）で未処理ドキュメントが
処理されます。本ジョブはクロールジョブと連鎖していないため、クロール直後に処理したい場合は、
スケジュールをクロールジョブの想定完了時刻より後に設定してください。

.. note::

   複数ノード構成では、本ジョブの実行対象をいずれか1ノードに固定することを推奨します。
   全ノードで同時実行しても整合性は保たれますが、同じドキュメントを各ノードが重複して
   埋め込み処理するため、プロバイダへの負荷・コストがノード数分増加します。

   固定するには、以下の2つの設定が両方とも必要です（片方だけでは固定されません）。

   1. **実行させたいノード側**\ の ``app/WEB-INF/classes/fess_config.properties``
      （RPM/DEB 版は ``/etc/fess/fess_config.properties``。または
      ``-Dfess.config.scheduler.target.name=<任意の識別名>``）に
      ``scheduler.target.name=<任意の識別名>`` を設定し、そのノードを再起動します
      （既定は空で、他のノードは既定のままにしておきます）。
   2. 管理画面 > システム > スケジューラ で Content Chunk Vector Indexer ジョブを開き、
      「対象」フィールドを ``all`` から、手順1で設定した識別名に変更して保存します。

   「対象」フィールドの意味は :doc:`../admin/scheduler-guide` を参照してください。
   ``scheduler.target.name`` を設定しても、「対象」フィールドを ``all`` のままにしておくと
   **固定されません**。``all`` は常に一致する特別な値として扱われるため、手順1だけ・
   手順2だけでは固定できず、必ず両方を行ってください。

.. warning::

   ピン留めした後は、「今すぐ開始」も **手順1で識別名を設定したノードの管理画面から** 実行して
   ください。対象外のノードで「今すぐ開始」を押すと、画面には「ジョブ … を開始しました。」と
   表示されるにもかかわらず、「対象」の不一致によりジョブは実行されません（そのノードのログに
   ``Ignoring job`` が INFO で出力されるだけです）。

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
     - チャンク分割のみ完了（chunk-onlyモード）。``embedding.name=none`` の場合のほか、
       ``embedding.name`` に指定したプロバイダのプラグインが導入されていない場合もこの状態に
       なります
   * - ``skipped``
     - 処理をスキップ（``max_chunks_per_document`` 超過等）
   * - ``fail``
     - 処理に失敗（ログを確認してください）

状態の分布は検索エンジンに直接問い合わせて確認できます::

    curl -XPOST "http://localhost:9200/fess.search/_search" \
         -H "Content-Type: application/json" -d '
    {"size": 0, "aggs": {"status": {"terms": {"field": "content_chunk_status", "missing": "pending"}}}}'

``missing`` オプションにより、``content_chunk_status`` を持たない（＝未処理の）ドキュメントは
``pending`` というキーのバケットに集計されます。

セマンティック検索の動作
========================

``content_chunker.search.enabled=true`` を設定すると、セマンティックサーチャーが
Rank Fusion に登録され、キーワード検索結果とベクトル検索結果が統合されます
（Rank Fusion の仕組みは :doc:`rank-fusion` を参照）。
なお、検索時には ``content_chunker.enabled`` も参照されます。``content_chunker.enabled=false``
または ``content_chunker.embedding.name=none`` の場合、サーチャーが登録済みでもセマンティック
検索は実行されません（この判定はリクエストごとに行われるため、再起動は不要です）。

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
     - ``index.knn`` と ANN メソッド設定を持つインデックス
     - HNSW による近似近傍検索。大規模インデックス向け
   * - ``exact``
     - 上記以外（``index.knn`` または ANN メソッド設定のいずれかを欠くインデックス。インデックス
       状態の判定に失敗した場合を含む）
     - 全ベクトルとの厳密なコサイン類似度計算。小〜中規模向け

|Fess| 15.8 で新規作成される ``fess.search`` インデックスは、``content_chunker.search.enabled`` の
値にかかわらず常に ``index.knn`` と ANN メソッド設定を持つため、通常は常に ``ann`` モードが
使われます。``exact`` モードは、この仕組みが導入される前に作成された古いインデックスに対する
フォールバックです。既存インデックスに後から k-NN 設定を追加することはできないため、
``exact`` モードのインデックスを ``ann`` モードへ切り替えるには、インデックスの再作成が必要です
（:ref:`semantic-search-migration` を参照）。なお、この判定結果は 60 秒間キャッシュされるため、
インデックスを再作成した直後は反映まで最大 60 秒かかります。

スコアの足切り
--------------

``content_chunker.search.min_score`` にコサイン類似度（0〜1）を設定すると、最も類似度の高い
チャンクでもその値に達しないドキュメントが、セマンティック検索結果から除外されます
（ドキュメントのスコアは最良チャンクのスコアになるため、足切りはドキュメント単位で働きます）。
語彙が一致しないクエリでヒット件数が増えすぎる場合の調整に使用します::

    content_chunker.search.min_score=0.4

設定値は ``exact`` / ``ann`` のどちらのモードでもコサイン類似度として解釈されます
（内部でモードごとのスコアスケールへ変換されます）。

.. note::

   この足切りが適用されるのは、``content_chunker.search.knn.space_type`` が
   ``cosinesimil``\ （デフォルト）の場合のみです。``innerproduct`` / ``l2`` を指定した ``ann``
   モードのインデックスでは、コサイン類似度を定義できないため、足切りは警告ログを1度出力した
   うえでスキップされます。

制限事項
--------

- **検索構文を含むクエリでは、セマンティック検索はスキップ** され、キーワード検索のみが実行され
  ます。判定はクエリの組み立て **後** の文字列に対して行われ、``"`` ``(`` ``)`` ``:`` ``[`` ``]``
  ``{`` ``}`` ``^`` ``~`` ``*`` ``?`` ``\``、``&&``、``||``、先頭または空白直後の ``+`` / ``-``、
  大文字の ``AND`` / ``OR`` / ``NOT`` / ``TO`` のいずれかが含まれると対象になります。
  そのため、利用者が検索構文を入力していなくても、以下の操作は同様にスキップされます。

  - ラベルの指定（内部的に ``label:"..."`` が付加されます）
  - ソート条件の指定（内部的に ``sort:...`` が付加されます）
  - ファセットによる絞り込み（内部的に ``filetype:...`` などが付加されます）
  - 詳細検索のフレーズ検索・除外語・ファイル種別・サイト指定・日時指定
  - 関連クエリが設定された検索語（内部的に ``("A" OR "B")`` に展開されます）

  半角の ``?`` も対象に含まれるため、「〜とは?」のように半角疑問符で終わる自然文はスキップされ
  ます（全角の ``？`` は対象外です）。
- 位置情報検索（ジオフィルタ）や類似ドキュメント検索と併用した場合もスキップされます。
- 深いページではRank Fusion自体が無効化され、キーワード検索のみの結果になります。境界は
  ``rank.fusion.window_size``\ （デフォルト ``200``）で決まり、既定では検索結果の 101 件目以降が
  該当します。
- 埋め込みプロバイダに接続できない場合や検索エラーが発生した場合は、自動的にキーワード検索のみの
  結果になります（検索自体がエラーになることはありません）。
- ロール・仮想ホストによるアクセス制御は、セマンティック検索結果にも適用されます。

AI検索モードとの連携
====================

AI検索モード（:doc:`rag-chat`、``rag.chat.enabled=true``）が有効な場合、
``content_chunk_status`` が ``done`` のドキュメントについては、回答生成時に各チャンクとの
類似度を計算し、最も関連する上位 ``content_chunker.chat.top_k`` 件（デフォルト: ``3``）の
チャンクのみをLLMのコンテキストとして使用します。

このとき埋め込みの対象になるのは、利用者の発話そのものではなく、**意図判定フェーズでLLMが生成
した検索クエリ** です（再検索が発生した場合は再生成後のクエリになります）。ドキュメントの要約を
求めた場合のように検索クエリが生成されない場合は、チャンク選択は行われません。

これにより、長いドキュメントでも関連部分だけがLLMに渡され、回答精度の向上とトークン使用量の
削減が期待できます。``content_chunk_status`` が ``chunked``\ （チャンクはあるがベクトルがない
状態）のドキュメントでは、類似度計算の代わりにキーワード（ハイライト）一致によるチャンク選択が
行われます。``skipped`` / ``fail`` および未処理のドキュメントは、従来どおり本文（または
ハイライト抜粋）が使用されます。

この動作は ``content_chunker.search.enabled`` とは独立していますが、``content_chunker.enabled``
が有効である必要があります。なお、選択されたチャンクを連結したテキストも
``rag.chat.content.fulltext.max.length``\ （デフォルト ``3000``）で切り詰められるため、
``content_chunker.chat.top_k`` や ``content_chunker.length.chunk_size`` を大きくしても、
LLMに渡る文字数はこの上限を超えません。

.. _semantic-search-migration:

15.7 以前からアップグレードする場合の移行
=========================================

15.7 以前から |Fess| をアップグレードする場合、現在の利用状況に応じて以下の
4 パターンのいずれかに該当します。該当するパターンの手順に従ってください。

新規インストールの場合
----------------------

追加の作業は不要です。ベクトル検索を使う場合は、|Fess| を初めて起動する前に、本ページの
「設定リファレンス」に従って ``system.properties`` を設定しておくだけで、最初の
インデックス作成時に正しいマッピングが自動的に適用されます（具体的な手順は
「セットアップ手順」を参照してください）。

.. note::

   既に一度でも |Fess| を起動したことがある（インデックスが作成済みの）場合は、
   このパターンではなく次の「既存ユーザー」のいずれかに従ってください。

既存ユーザーで、ベクトル検索を利用しない場合
--------------------------------------------

作業は不要です。``content_chunker.enabled`` と ``content_chunker.search.enabled`` は
いずれもデフォルトで ``false`` のため、アップグレード後も検索結果や既存インデックスの
挙動は変わりません。新設のスケジューラジョブ **Content Chunk Vector Indexer** は起動時に
自動登録されますが、デフォルトで無効なため実行されず、セマンティックサーチャーも
Rank Fusion に登録されません（このジョブは起動のたびに登録されるため、管理画面から削除しても
次回起動時に無効状態で再作成されます）。

.. note::

   ベクトル検索を利用しない場合でも、|Fess| 15.8 以降でインデックスを **新規作成**\ （再インデ
   クシングを含む）すると、``content_chunk_vector``\ （``knn_vector`` 型）を含むマッピングと
   ``index.knn: true`` が適用されます。OpenSearch に k-NN プラグインが入っていない構成では、
   その時点でインデックスの作成に失敗します。詳細は本ページの「前提条件」を参照してください。

既存ユーザーで、ベクトル検索を利用したい場合
--------------------------------------------

稼働中のインデックスには新しいマッピングが自動的には反映されないため、以下の手順が
必要です。

1. 本ページの「設定リファレンス」に従い、``system.properties`` に設定を投入します
   （opensearch プロバイダを使う場合の具体的な手順は「セットアップ手順」を参照）。
2. |Fess| を再起動します。
3. 管理画面 > システム情報 > メンテナンス の「再インデクシング」を、「エイリアスの更新」を
   有効にした状態で実行します。処理はバックグラウンドで非同期に進み、完了通知は表示されません。
   ``_cat/indices`` はインデックスの存在を示すだけでエイリアスの向き先は分からないため、次の
   手順に進む前に ``_cat/aliases`` で ``fess.search``/``fess.update`` が新しいインデックスを
   指していることを確認してください（|Fess| のログは失敗時のみ警告を出すため、静かなことは
   成功の証拠にはなりません）。旧インデックスは自動削除されないため、不要になったら手動で
   削除してください（新旧両方のインデックスが存在する間、ディスク使用量はおおむね通常の
   2倍になります）。
4. 上記のエイリアス切り替えの完了を確認した後、管理画面 > システム > スケジューラ で
   Content Chunk Vector Indexer ジョブを有効化し、実行します（クロールのやり直しは不要です。
   ジョブは既存インデックスの ``_source`` から ``content`` を読み出してチャンク化・埋め込みを
   行います）。

.. note::

   手順1で ``content_chunker.search.enabled=true`` まで投入すると、手順2の再起動から手順4の完了
   までの間、検索のたびにクエリの埋め込みだけが実行され、結果には反映されない状態になります。
   ``openai`` / ``gemini`` など従量課金のプロバイダを使用する場合は、
   ``content_chunker.search.enabled=true`` の投入と再起動を手順4の完了後に行ってください。

fess-webapp-semantic-search プラグインを利用していた場合
--------------------------------------------------------

|Fess| 15.7 以前でセマンティック検索を提供していた ``fess-webapp-semantic-search``
プラグインは、15.8 でコアに統合されたため **不要になりました（非推奨）**。上記
「既存ユーザーで、ベクトル検索を利用したい場合」の手順に加えて、以下の対応も
必要です。

1. **プラグインの削除**: ``app/WEB-INF/plugin/`` から ``fess-webapp-semantic-search-*.jar`` を
   削除します（Docker の場合は ``FESS_PLUGINS`` から除外します）。

2. **旧設定の削除**: 起動オプションから ``-Dfess.semantic_search.*`` の設定をすべて削除します。
   また、旧プラグイン用に ``-Drank.fusion.searchers=default,semantic`` を指定していた場合は
   削除します。指定したままだと、新しいセマンティックサーチャー（``semantic_chunk``）が
   Rank Fusion から除外され、起動時に警告ログが出力されます。

3. **旧 ingest pipeline のデタッチ**: 旧プラグインは、``-Dfess.semantic_search.pipeline`` を
   設定していた場合、インデックスの作成時に ``default_pipeline``\ （ニューラル検索用の ingest
   pipeline）をインデックス設定へ埋め込みます。**プラグインを削除しても pipeline はインデックス
   側に残り、動作し続ける** ため、「既存ユーザーで、ベクトル検索を利用したい場合」の再インデク
   シングを行う **前に** 解除してください。再インデクシング後の新しいインデックスにはこの設定が
   付かないため、後から実行しても意味がありません。``_cat/aliases`` で ``fess.search`` が指す
   ``fess.<timestamp>`` を確認し、エイリアスではなく実体のインデックス名を指定します::

       curl -XPUT "http://localhost:9200/fess.<timestamp>/_settings" \
            -H "Content-Type: application/json" -d '
       {"index": {"default_pipeline": "_none"}}'

   インデックス設定を解除しても、ingest pipeline 自体は検索エンジン側に残ります。今後使用しない
   場合は削除してください::

       curl -XDELETE "http://localhost:9200/_ingest/pipeline/<pipeline名>"

4. **新設定の追加**: 本ページの設定リファレンスに従い、``content_chunker.*`` の設定を
   ``system.properties`` に行います。ML Commons のモデルを引き続き使用する場合は
   ``content_chunker.embedding.name=opensearch`` を指定し、既存の ``model_id`` を
   ``content_chunker.embedding.opensearch.model.id`` に設定します。

5. **インデックスの再作成とジョブ実行**: 旧プラグインが格納していたベクトルフィールド
   （既定の構成では ``content_vector``）と、新しいコア機能が使う ``content_chunk_vector``
   フィールドは別物のため、旧ベクトルを新機能で利用することはできません。一方で、再インデク
   シングは ``_source`` をそのままコピーするため、旧ベクトルは新しいインデックスにも複製され、
   動的マッピングでディスクを消費し続けます。再インデクシングの **前に** 除去しておくことを
   推奨します（フィールド名を変更していた場合は読み替えてください）::

       curl -XPOST "http://localhost:9200/fess.search/_update_by_query" \
            -H "Content-Type: application/json" -d '
       {
         "query": {"exists": {"field": "content_vector"}},
         "script": {"source": "ctx._source.remove(\"content_vector\")"}
       }'

   その後、管理画面 > システム情報 > メンテナンス で「再インデクシング」を実行し、
   Content Chunk Vector Indexer ジョブを有効化・実行してベクトルを生成し直してください。

注意事項
========

埋め込みモデル（次元数）の変更
------------------------------

埋め込みモデルを次元数の異なるモデルへ変更する場合は、以下の順序で行います。

1. 既存の古いベクトルを削除します。次元数の異なる古いベクトルが残ったまま再インデクシングすると、
   新しいマッピングがそれらを受け付けられず、該当ドキュメントが新インデックスにコピーされない
   まま処理が進みます。|Fess| は再インデクシングの HTTP ステータスしか確認しないため、管理画面
   にはエラーが表示されないままドキュメントが欠落します::

       curl -XPOST "http://localhost:9200/fess.search/_update_by_query" \
            -H "Content-Type: application/json" -d '
       {
         "query": {"exists": {"field": "content_chunk_status"}},
         "script": {"source": "ctx._source.remove(\"content_chunk_vector\"); ctx._source.remove(\"content_chunk_status\")"}
       }'

   .. note::

      対象には ``fess.update``\ （再インデクシングの読み出し元となる更新用エイリアス）を指定して
      も構いません。また、この操作では ``content`` フィールドはチャンクの配列のまま残ります。
      次回のジョブ実行時に連結し直して再分割されるため、``content_chunker.length.overlap`` に
      0 以外を設定している場合は、重複部分が二重に含まれた状態で再分割されます。気になる場合は
      該当ドキュメントを再クロールしてください。

2. ``content_chunker.embedding.dimension`` と各プロバイダのモデル設定を変更します。
3. 「セットアップ手順」の「3. インデックスの再作成（既存の環境で有効化する場合）」に従って
   インデックスを再作成し、インデクサジョブを再実行します。

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

大規模コーパスでのメモリ設定
----------------------------

インデクサジョブの子JVMは、``fess_config.properties`` の ``jvm.chunk.options``
（デフォルトは ``-Xms128m -Xmx1g`` を含む JVM オプション）で起動されます。
``content_chunker.job.max_documents_per_run`` の既定値が無制限のため、1回の実行で保留中の
全ドキュメントIDをメモリ上に保持します。ドキュメントIDは SHA-512 ダイジェスト（128文字）で、
1件あたりおおむね 200 バイトをヒープに保持します。チャンク処理自体にも 200〜250MB 程度を使う
ため、**100〜200万件を超えるコーパス** では ``jvm.chunk.options`` の ``-Xmx`` を引き上げるか、
``content_chunker.job.max_documents_per_run`` に有限値を設定して分割実行してください。
``jvm.chunk.options`` は ``app/WEB-INF/classes/fess_config.properties``\ （RPM/DEB 版は
``/etc/fess/fess_config.properties``）で上書きします（JVMオプションの考え方は
:doc:`setup-memory` を参照してください）。

同じく既定値が無制限になったことで、``openai`` や ``gemini`` など従量課金制の埋め込みプロバイダを
使用している場合はコスト面の影響もあります。初回のインデクサジョブ実行で既存コーパス全体の
埋め込みが一度に生成され、その分の利用料金も一度に発生します。費用を複数回の実行に分散させたい
場合は、``content_chunker.job.max_documents_per_run`` に有限の値を設定してください。

参考情報
========

- :doc:`rank-fusion` - Rank Fusion（ハイブリッド検索）の設定
- :doc:`rag-chat` - AI検索モード機能の設定
- :doc:`llm-overview` - LLM統合の概要
- :doc:`llm-ollama` - Ollamaの設定
- :doc:`setup-memory` - JVMメモリ設定
- :doc:`../install/upgrade` - アップグレード手順
