=======================
検索ログ可視化の設定
=======================

検索ログの可視化について
========================

|Fess| ではユーザーの検索ログおよびクリックログを取得しています。
取得した検索ログを `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/index/>`__ を用いて、データ解析・可視化することができます。

|Fess| には、検索ログを可視化するためのダッシュボード定義ファイル ``extension/kibana/fess_log.ndjson`` が同梱されています。
このファイルを OpenSearch Dashboards にインポートすることで、あらかじめ用意されたダッシュボードをすぐに利用できます。

可視化できる情報
----------------

同梱のダッシュボード定義 (``fess_log.ndjson``) をインポートすると、``fess_log`` ダッシュボードと、以下の6つのビジュアライゼーションが登録されます。

-  検索結果表示にかかる平均応答時間 (``average-response-time``)
-  一定時間あたりの検索リクエスト数 (``search-query-counts-per-sec``)
-  アクセスユーザーの User Agent ランキング (``rank-of-UserAgent``)
-  検索キーワードのランキング (``search-term-rank``)
-  検索結果が0件の検索キーワードのランキング (``search-term-rank-of-no-results``)
-  検索結果の平均ヒット件数 (``hit-counts``)

これらに加えて、Visualize 機能を使用して新たなグラフを作成し、ダッシュボードに追加することで、独自の監視ダッシュボードを構築することもできます。

OpenSearch Dashboards によるデータ可視化の設定
==============================================

OpenSearch Dashboards のインストール
------------------------------------

OpenSearch Dashboards は |Fess| で使用している OpenSearch のデータを可視化するためのツールです。
`OpenSearch の公式ドキュメント <https://opensearch.org/docs/latest/install-and-configure/install-dashboards/index/>`__ に従い、OpenSearch Dashboards をインストールします。

設定ファイルの編集
------------------

OpenSearch Dashboards に |Fess| で使用している OpenSearch を認識させるため、設定ファイル ``config/opensearch_dashboards.yml`` を編集します。

::

    opensearch.hosts: ["http://localhost:9201"]

``localhost`` は環境に合わせて適切なホスト名またはIPアドレスに変更してください。
|Fess| のデフォルト設定では、OpenSearch は 9201 ポートで起動しています。

.. note::
   OpenSearch のポート番号が異なる場合は、適切なポート番号に変更してください。

OpenSearch Dashboards の起動
-----------------------------

設定ファイルを編集した後、OpenSearch Dashboards を起動します。

::

    $ cd /path/to/opensearch-dashboards
    $ ./bin/opensearch-dashboards

起動後、ブラウザで ``http://localhost:5601`` にアクセスします。

インデックスパターンの設定
--------------------------

検索ログを可視化するためのインデックスパターンを作成します。

1. 左側のメニューから「Management」(OpenSearch Dashboards のバージョンによっては「Dashboards Management」)を選択します。
2. 「Index Patterns」を選択します。
3. 「Create index pattern」ボタンをクリックします。
4. Index pattern name に ``fess_log*`` と入力します。
5. 「Next step」ボタンをクリックします。
6. Time field で ``requestedAt`` を選択します。
7. 「Create index pattern」ボタンをクリックします。

.. note::
   |Fess| の検索ログは ``fess_log.search_log`` 、クリックログは ``fess_log.click_log`` といった ``fess_log`` で始まる複数のインデックスに記録されます。
   ``fess_log*`` というインデックスパターンを指定することで、これらをまとめて対象にできます。

ダッシュボード定義のインポート
------------------------------

|Fess| に同梱されているダッシュボード定義をインポートすることで、あらかじめ用意されたビジュアライゼーションとダッシュボードを利用できます。

1. 左側のメニューから「Management」(OpenSearch Dashboards のバージョンによっては「Dashboards Management」)を選択します。
2. 「Saved Objects」を選択します。
3. 「Import」をクリックします。
4. |Fess| のインストールディレクトリにある ``extension/kibana/fess_log.ndjson`` を選択します。
5. 「Import」をクリックして、インポートを実行します。

インポートが完了すると、6つのビジュアライゼーションと ``fess_log`` ダッシュボードが登録されます。

ダッシュボードの表示
--------------------

1. 左側のメニューから「Dashboard」を選択します。
2. ``fess_log`` ダッシュボードを選択します。
3. 検索ログの可視化結果が表示されます。
4. 右上の時間範囲選択で、表示する期間を指定できます。

独自の可視化の作成
------------------

同梱のダッシュボードに加えて、独自のビジュアライゼーションやダッシュボードを作成することもできます。

ビジュアライゼーションの作成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. 左側のメニューから「Visualize」を選択します。
2. 「Create visualization」ボタンをクリックします。
3. 可視化のタイプ(折れ線グラフ、円グラフ、棒グラフなど)を選択します。
4. 作成したインデックスパターン ``fess_log*`` を選択します。
5. 必要なメトリクスやバケット(集計単位)を設定します。
6. 「Save」ボタンをクリックして、ビジュアライゼーションを保存します。

ダッシュボードの作成
~~~~~~~~~~~~~~~~~~~~

1. 左側のメニューから「Dashboard」を選択します。
2. 「Create dashboard」ボタンをクリックします。
3. 「Add」ボタンをクリックして、作成したビジュアライゼーションを追加します。
4. レイアウトを調整し、「Save」ボタンをクリックして保存します。

タイムゾーンの設定
------------------

時間の表示が正しくない場合は、タイムゾーンを設定します。

1. 左側のメニューから「Management」(OpenSearch Dashboards のバージョンによっては「Dashboards Management」)を選択します。
2. 「Advanced Settings」を選択します。
3. ``dateFormat:tz`` を検索します。
4. タイムゾーンを適切な値(例: ``Asia/Tokyo`` または ``UTC``)に設定します。
5. 「Save」ボタンをクリックします。

ログデータの確認
----------------

1. 左側のメニューから「Discover」を選択します。
2. インデックスパターン ``fess_log*`` を選択します。
3. 検索ログのデータが表示されます。
4. 右上の時間範囲選択で、表示する期間を指定できます。

主な検索ログフィールド
----------------------

|Fess| の検索ログ (``fess_log.search_log``) には以下のような情報が含まれています。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - フィールド名
     - 説明
   * - ``queryId``
     - 検索クエリの一意な識別子
   * - ``searchWord``
     - 検索キーワード
   * - ``requestedAt``
     - 検索が実行された日時
   * - ``responseTime``
     - 検索処理全体の応答時間(ミリ秒)
   * - ``queryTime``
     - 検索エンジンへのクエリ実行時間(ミリ秒)
   * - ``hitCount``
     - 検索結果のヒット件数
   * - ``hitCountRelation``
     - ヒット件数が正確な値か下限値かを表す関係(``eq``: 正確な件数、``gte``: 指定値以上)
   * - ``queryOffset``
     - 検索結果の取得開始位置
   * - ``queryPageSize``
     - 1ページあたりの表示件数
   * - ``userAgent``
     - ユーザーのブラウザ情報
   * - ``referer``
     - 検索を実行したページの参照元URL
   * - ``clientIp``
     - クライアントのIPアドレス
   * - ``languages``
     - リクエストの使用言語
   * - ``accessType``
     - アクセス種別(``web``、``json``、``gsa``、``admin``、``other``)
   * - ``roles``
     - ユーザーのロール情報
   * - ``user``
     - ユーザー名(ログイン時)
   * - ``virtualHost``
     - 仮想ホスト名(設定されている場合)

これらのフィールドを活用して、様々な観点から検索ログを分析できます。

トラブルシューティング
----------------------

データが表示されない場合
~~~~~~~~~~~~~~~~~~~~~~~~

- OpenSearch が正しく起動しているか確認してください。
- ``opensearch_dashboards.yml`` の ``opensearch.hosts`` 設定が正しいか確認してください。
- |Fess| で検索が実行され、ログが記録されているか確認してください。
- 右上の時間範囲が、ログが記録されている期間を含むように設定されているか確認してください。
- 時間の表示がずれている場合は、``dateFormat:tz`` の設定を確認してください。

接続エラーが発生する場合
~~~~~~~~~~~~~~~~~~~~~~~~

- OpenSearch のポート番号が正しいか確認してください。
- ファイアウォールやセキュリティグループの設定を確認してください。
- OpenSearch のログファイルでエラーがないか確認してください。
