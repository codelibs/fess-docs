=======================
検索ログ可視化の設定
=======================

検索ログの可視化について
========================

|Fess| ではユーザーの検索ログおよびクリックログを取得しています。
取得した検索ログを `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/index/>`__ を用いて、データ解析・可視化することができます。

可視化できる情報
----------------

デフォルトの設定では、以下の情報を可視化することができます。

-  検索結果表示にかかる平均時間
-  秒あたりの検索回数
-  アクセスユーザーの User Agent ランキング
-  検索キーワードのランキング
-  検索結果が0件の検索キーワードランキング
-  検索結果の合計数
-  時系列での検索トレンド

Visualize機能を使用して新たなグラフを作成し、Dashboardに追加することで、独自の監視ダッシュボードを構築できます。

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

1. OpenSearch Dashboards のホーム画面から「Management」メニューを選択します。
2. 「Index Patterns」を選択します。
3. 「Create index pattern」ボタンをクリックします。
4. Index pattern name に ``fess_log*`` と入力します。
5. 「Next step」ボタンをクリックします。
6. Time field で ``requestedAt`` を選択します。
7. 「Create index pattern」ボタンをクリックします。

これで、|Fess| の検索ログを可視化するための準備が完了しました。

可視化とダッシュボードの作成
----------------------------

基本的な可視化の作成
~~~~~~~~~~~~~~~~~~~~

1. 左側のメニューから「Visualize」を選択します。
2. 「Create visualization」ボタンをクリックします。
3. 可視化のタイプ(折れ線グラフ、円グラフ、棒グラフなど)を選択します。
4. 作成したインデックスパターン ``fess_log*`` を選択します。
5. 必要なメトリクスやバケット(集計単位)を設定します。
6. 「Save」ボタンをクリックして、可視化を保存します。

ダッシュボードの作成
~~~~~~~~~~~~~~~~~~~~

1. 左側のメニューから「Dashboard」を選択します。
2. 「Create dashboard」ボタンをクリックします。
3. 「Add」ボタンをクリックして、作成した可視化を追加します。
4. レイアウトを調整し、「Save」ボタンをクリックして保存します。

タイムゾーンの設定
------------------

時間の表示が正しくない場合は、タイムゾーンを設定します。

1. 左側のメニューから「Management」を選択します。
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

|Fess| の検索ログには以下のような情報が含まれています。

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
     - 検索結果の応答時間(ミリ秒)
   * - ``queryTime``
     - クエリ実行時間(ミリ秒)
   * - ``hitCount``
     - 検索結果のヒット件数
   * - ``userAgent``
     - ユーザーのブラウザ情報
   * - ``clientIp``
     - クライアントのIPアドレス
   * - ``languages``
     - 使用言語
   * - ``roles``
     - ユーザーのロール情報
   * - ``user``
     - ユーザー名(ログイン時)

これらのフィールドを活用して、様々な観点から検索ログを分析できます。

トラブルシューティング
----------------------

データが表示されない場合
~~~~~~~~~~~~~~~~~~~~~~~~

- OpenSearch が正しく起動しているか確認してください。
- ``opensearch_dashboards.yml`` の ``opensearch.hosts`` 設定が正しいか確認してください。
- |Fess| で検索が実行され、ログが記録されているか確認してください。
- インデックスパターンの時間範囲が適切に設定されているか確認してください。

接続エラーが発生する場合
~~~~~~~~~~~~~~~~~~~~~~~~

- OpenSearch のポート番号が正しいか確認してください。
- ファイアウォールやセキュリティグループの設定を確認してください。
- OpenSearch のログファイルでエラーがないか確認してください。
