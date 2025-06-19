===============
検索ログ可視化の設定
===============

検索ログの可視化について
==================

|Fess| ではユーザーの検索ログおよびクリックログを取得しています。
取得した検索ログを `Kibana <https://www.elastic.co/jp/products/kibana>`__\ を用いて、データ解析・可視化することができます。
デフォルトの設定では、

-  検索結果表示にかかる平均の時間

-  秒あたりの検索回数

-  アクセスユーザーの User Agent ランキング

-  検索語のランキング

-  検索結果が0件の検索語ランキング

-  検索結果の合計数

を可視化することができます。
Visualizeから新たなグラフを作成してDashboardに追加することで、独自のモニタを構築できます。

Kibana 5 によるデータ可視化の設定
===========================

Kibana 5 インストール
------------------

`https://www.elastic.co/downloads/kibana <https://www.elastic.co/downloads/kibana>`__  に従い、Kibana 5をインストールします。
Kibana に |Fess| で用いる OpenSearch を認識させるため、 Kibanaのディレクトリ/config/kibana.yml の elasticsearch.url を以下のように編集します。

::

    elasticsearch.url: "http://localhost:9201"

localhost は環境に合わせて設定してください。

詳細な設定
--------

|Fess| を起動した状態でKibanaを起動し、`http://localhost:5601 <http://localhost:5601>`__ にアクセスします。

Kibana のホーム画面が表示されるので、まずは可視化対象のインデックスを指定します。
Index name or pattern のパターンに fess_log と入力し、Time-field name で requestedAt を選択して、Create ボタンを押下します。
次に、デフォルトの設定をインポートします。
画面上部から Settings、その後 Objects を選択します。
ここで Import ボタンを押下すると、ファイルを選択するウィンドウが表示されるので src/main/assemblies/extension/kibana/fess_log.json を選択し、インポートします。

そして、 Dashboardでグラフを表示します。
画面上部より Dashboard を選択した後、画面右上部 Load Saved Dashboard を押下して、fess_logを選択します。
必要であれば、右上部からデータを適用する期間を指定できます。

このとき、時間の基準が Browser になっていると、正確なログデータが表示できない場合があります。
そのようなときは、タイムゾーンを設定することで正しく表示できる場合があります。
上部より Settings, その後 Advanced を選択します。その中で dateFormat:tz という項目を編集します。
Actions の列のボタンを押下し、 dateFormat:tz を UTC に変更し、再度データを適用する期間を指定してください。
