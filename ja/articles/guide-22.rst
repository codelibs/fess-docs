============================================
OpenSearch Dashboards で検索ログを深掘りする
============================================

はじめに
========

Fess 15.9 では、管理画面の［システム情報］>［検索ログ］で、ゼロヒット率、クリック率、クリック順位の分布、応答時間、曜日・時間帯別の検索数、ロール・グループ別の検索数を確認できます。
各表は CSV でダウンロードできます。
問題のある検索語を見つけて同義語やキーマッチで直す流れは :doc:`guide-08` で説明しています。

一方で、この画面では次のような集計はできません。

- 366 日を超える期間の推移（画面の「カスタム」期間は最大 366 日です）
- ロール別やラベル別に、どの語がゼロヒットになっているか
- 検索語ごとに、実際にどの URL が開かれたか
- 自分で決めた切り口のグラフを並べたダッシュボード

検索ログとクリックログは OpenSearch のインデックスに保存されているので、OpenSearch Dashboards から直接集計できます。
本記事では、docker-fess の Compose ファイルで OpenSearch Dashboards を起動し、Fess 同梱のダッシュボードを読み込み、ログのフィールドを確かめたうえで、上の 4 つの集計を作るところまでを説明します。

始める前に：アクセス制限について
================================

docker-fess の OpenSearch Dashboards は、OpenSearch 側と同じくセキュリティプラグインを外した構成です。
ポート 5601 に届く人は、ログインなしで検索ログのすべてのフィールド（ユーザー ID、IP アドレスなど）を読めます。
さらに Dev Tools から、Fess のユーザーや設定のインデックスを含むすべてのインデックスを変更・削除できます。

そのため、ポート 5601（と 9200）は管理者の端末からだけ届くようにしてください。
管理者以外の人に検索ログの集計を見せたい場合は、OpenSearch Dashboards を公開するのではなく、Fess の［ユーザー］>［ロール］で ``admin-searchlog-view`` という名前のロールを作ってその人に割り当てます。
このロールでは［システム情報］>［検索ログ］を閲覧でき、ログの削除はできません。

OpenSearch Dashboards を起動する
================================

:doc:`guide-02` の手順で ``compose.yaml`` と ``compose-opensearch3.yaml`` を置いたディレクトリに、Dashboards 用のファイルを追加します。
``compose-dashboards3.yaml`` は ``dashboards/`` ディレクトリの Dockerfile からイメージをビルドするので、3 つのファイルが必要です。

::

    $ cd fess-docker
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-dashboards3.yaml
    $ mkdir dashboards
    $ curl -L -o dashboards/Dockerfile https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/dashboards/Dockerfile
    $ curl -L -o dashboards/opensearch_dashboards.yml https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/dashboards/opensearch_dashboards.yml

3 つの Compose ファイルを指定して起動します。

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-dashboards3.yaml up -d

初回の ``up`` で、``opensearch-dashboards:3.9.0`` から ``securityDashboards`` プラグインを削除したイメージがビルドされます。
コンテナはネットワーク ``search_net`` 上で ``OPENSEARCH_HOSTS='["http://search01:9200"]'`` に接続し、ポート 5601 を公開します。

ブラウザーで ``http://localhost:5601`` を開き、ホーム画面が表示されれば起動しています。
停止や状態確認でも、``-f`` で 3 つのファイルを指定してください。
ダッシュボードなどの保存オブジェクトは OpenSearch の ``.kibana`` インデックスに保存されるので、``down -v`` でボリュームを消すと一緒に消えます。

同梱のダッシュボードを読み込む
==============================

Fess には、検索ログ用のダッシュボード定義 ``fess_log.ndjson`` が同梱されています。
Docker の場合はコンテナから取り出します。
ZIP 版では展開したディレクトリの ``extension/kibana/fess_log.ndjson`` にあります。

::

    $ docker cp fess01:/usr/share/fess/extension/kibana/fess_log.ndjson .

GitHub の ``https://raw.githubusercontent.com/codelibs/fess/fess-15.9.0/src/main/assemblies/extension/kibana/fess_log.ndjson`` からも同じファイルを取得できます。

1. 左メニューの［Dashboards Management］を開き、［Saved objects］を選びます
2. ［Import］をクリックし、``fess_log.ndjson`` を選んで読み込みます
3. 左メニューの［Dashboards］から ``fess_log`` ダッシュボードを開きます

読み込むと、インデックスパターン ``fess_log*``\ （時刻フィールドは ``requestedAt``）、6 つのビジュアライゼーション、``fess_log`` ダッシュボードが登録されます。
インデックスパターンも含まれているので、先に手動で ``fess_log*`` を作る必要はありません。
手動で作ったあとに読み込むと、同じ名前のパターンが 2 つになります。

同梱ダッシュボードの数え方に注意する
------------------------------------

``fess_log*`` は ``fess_log`` で始まるすべてのインデックスにまたがり、同梱のビジュアライゼーションはインデックスで絞り込んでいません。
15.9 のクリックログには検索語（``searchWord``）と ``requestedAt`` が入るので、たとえば「search-term-rank」の件数には検索の回数とクリックの回数が合算されます。
AI 検索モードを使っている場合は、チャットのログ（``fess_log.chat_log``）も件数や応答時間に混ざります。

検索だけを数えたい場合は、ダッシュボード上部の検索バーに次の条件を入れてから見てください。

::

    _index : "fess_log.search_log"

また、``fess_log*`` に保存されているフィールドの一覧は古い版のもので、``rank`` などの新しいフィールドを含みません。
自分で集計を作るときは、次の節のインデックスパターンを使います。

集計用のインデックスパターンを作る
==================================

検索ログとクリックログを別々のインデックスパターンにしておくと、混ざる心配がなく、現在のフィールドをすべて選べます。

1. ［Dashboards Management］>［Index patterns］で［Create index pattern］をクリックします
2. 「Index pattern name」に ``fess_log.search_log`` と入力し、［Next step］をクリックします
3. 「Time field」で ``requestedAt`` を選び、［Create index pattern］をクリックします
4. 同じ手順で ``fess_log.click_log``\ （時刻フィールドは ``requestedAt``）も作ります

あとからフィールドが増えた場合（たとえば初めてラベルで絞り込んだ検索が記録されたとき）は、インデックスパターンの画面で［Refresh field list］をクリックします。

時刻の扱い
----------

Fess は日時を UTC で保存します。
OpenSearch Dashboards は既定でブラウザーのタイムゾーンで表示し、日ごとの区切りもそれに従います。
別のタイムゾーンで見たい場合は、［Dashboards Management］>［Advanced settings］の ``dateFormat:tz`` を ``Asia/Tokyo`` などに変えます。

Fess の［検索ログ］画面は、サーバーのタイムゾーンで日付を区切ります。
docker-fess のコンテナは既定で UTC なので、日別の数字を両者で突き合わせると、区切りの違いだけずれることがあります。

ログのフィールド
================

検索ログ（``fess_log.search_log``）は検索 1 回につき 1 件です。
集計によく使うフィールドは次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 型
     - 内容
   * - ``queryId``
     - keyword
     - 検索ごとの ID。クリックログの ``queryId`` と対応します
   * - ``searchWord``
     - keyword
     - 検索語。ラベルで絞り込んだ検索では ``申請 label:"hr"`` のように条件も含みます
   * - ``searchField.*``
     - keyword
     - 検索語をフィールドごとに分けたもの。通常の語は ``searchField._default``、ラベルの絞り込みは ``searchField.label`` に入ります
   * - ``requestedAt``
     - date
     - 検索した日時（UTC で保存）
   * - ``hitCount``
     - long
     - ヒット件数。``0`` がゼロヒットです
   * - ``responseTime`` / ``queryTime``
     - long
     - 検索全体の処理時間と、OpenSearch での検索時間（ミリ秒）
   * - ``queryOffset`` / ``queryPageSize``
     - integer
     - 取得開始位置と 1 ページの件数。2 ページ目以降なら ``queryOffset`` が 0 より大きくなります
   * - ``accessType``
     - keyword
     - ``json``、``gsa``、``admin``、``other``、``web`` のいずれか。標準テーマの検索画面は ``/api/v2/search`` を呼ぶので ``json`` になり、管理画面の［システム情報］>［検索］からの検索は ``admin`` です
   * - ``user`` / ``roles``
     - keyword
     - ログインユーザーの ID と、検索に使われたロールの一覧。``roles`` の値は先頭 1 文字で種類を表し、``R`` がロール、``2`` がグループ、``1`` がユーザーです（例: ``Rguest``）
   * - ``userSessionId`` / ``clientIp`` / ``userAgent`` / ``referer`` / ``virtualHost``
     - keyword
     - 利用者を識別する Cookie の値、IP アドレス、ブラウザー、参照元、仮想ホスト

クリックログ（``fess_log.click_log``）は、検索結果のリンクが ``/go/`` 経由で開かれたときに記録されます。
ただし、ブラウザーが Fess のセッションを持っていない（有効なセッション Cookie を送っていない）リクエストでは記録されません。

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 型
     - 内容
   * - ``queryId``
     - keyword
     - クリック元の検索の ``queryId``
   * - ``url`` / ``docId``
     - keyword
     - 開かれた文書の URL と文書 ID
   * - ``rank``
     - integer
     - 検索結果全体での順位（1 位が 1）。2 ページ目の 1 件目なら 11 です
   * - ``order``
     - integer
     - ページ内での位置（先頭が 0）。順位の集計には ``rank`` を使います
   * - ``searchWord`` / ``accessType``
     - keyword
     - クリック元の検索から写した検索語とアクセス種別。検索ログと結合しなくても検索語ごとに集計できます
   * - ``requestedAt`` / ``queryRequestedAt``
     - date
     - クリックした日時と、クリック元の検索の日時

``searchWord``、``accessType``、``rank`` がクリックログに入るのは 15.9 からです。
それより前に記録されたクリックにはこれらがありません。

集計のレシピ
============

ここでは、冒頭に挙げた「画面ではできない集計」を 4 つ作ります。
1 つ目は Visualize で作り、残りは左メニューの［Dev Tools］から検索 API で実行します。

検索語ごとに開かれた URL
------------------------

検索語ごとに、どの文書がどの順位で開かれたかを表にします。
キーマッチやドキュメントブーストの候補を選ぶときに使えます。

1. 左メニューの［Visualize］で［Create visualization］をクリックし、「Data Table」を選びます
2. ソースに ``fess_log.click_log`` を選びます
3. Metrics の［Add］で Metric を追加し、「Aggregation」に「Average」、「Field」に ``rank`` を選びます
4. Buckets の［Add］>［Split rows］で、「Aggregation」に「Terms」、「Field」に ``searchWord``、「Size」に 20 を指定します
5. もう一度［Split rows］を追加し、「Terms」、「Field」に ``url``、「Size」に 5 を指定します
6. ［Update］をクリックし、右上の期間を選んで保存します

平均の順位が大きい組み合わせは、利用者が下までたどって開いている文書です。

ロール別のゼロヒット語
----------------------

部署ごとにロールを分けている場合、どの部署の検索で何が見つかっていないかを確認します。

.. code-block:: text

    GET fess_log.search_log/_search
    {
      "size": 0,
      "query": {
        "bool": {
          "filter": [
            { "term": { "hitCount": 0 } },
            { "range": { "requestedAt": { "gte": "now-90d/d" } } }
          ]
        }
      },
      "aggs": {
        "roles": {
          "terms": { "field": "roles", "size": 20, "exclude": "1.*" },
          "aggs": {
            "words": { "terms": { "field": "searchWord", "size": 10 } }
          }
        }
      }
    }

``exclude`` で ``1`` から始まる値（ユーザー個人）を除き、ロールとグループだけを並べています。
1 回の検索は、その利用者のすべてのロールとグループに数えられます。
未ログインの検索は ``Rguest`` に入ります。

ラベル別の検索数とゼロヒット数
------------------------------

検索画面でラベルを選んで検索された回数と、そのうちのゼロヒットの回数をラベルごとに数えます。

.. code-block:: text

    GET fess_log.search_log/_search
    {
      "size": 0,
      "query": { "range": { "requestedAt": { "gte": "now-90d/d" } } },
      "aggs": {
        "labels": {
          "terms": { "field": "searchField.label", "size": 20 },
          "aggs": {
            "zero_hit": { "filter": { "term": { "hitCount": 0 } } }
          }
        }
      }
    }

ラベルで絞り込んだ検索が 1 件も記録されていないと、``searchField.label`` フィールドがまだないため、``labels`` のバケットは空になります。

月ごとのゼロヒット率（2 年分）
------------------------------

画面の期間の上限を超えて、ゼロヒット率（件数ではなく比率）の長期の推移を見ます。

.. code-block:: text

    GET fess_log.search_log/_search
    {
      "size": 0,
      "query": {
        "bool": {
          "filter": [ { "range": { "requestedAt": { "gte": "now-2y/d" } } } ],
          "must_not": [ { "term": { "accessType": "admin" } } ]
        }
      },
      "aggs": {
        "per_month": {
          "date_histogram": {
            "field": "requestedAt",
            "calendar_interval": "month",
            "time_zone": "Asia/Tokyo"
          },
          "aggs": {
            "zero_hit": { "filter": { "term": { "hitCount": 0 } } },
            "zero_hit_rate": {
              "bucket_script": {
                "buckets_path": { "zero": "zero_hit>_count", "total": "_count" },
                "script": "params.zero / params.total"
              }
            }
          }
        }
      }
    }

月ごとのバケットに、検索数（``doc_count``）、ゼロヒット数（``zero_hit.doc_count``）、ゼロヒット率（``zero_hit_rate.value``、0〜1）が返ります。
``time_zone`` により月の区切りは日本時間になり、管理画面からの検索は ``must_not`` で除いています。
2 年分のログが残っているかどうかは、次の節の保存期間の設定によります。

保存期間と個人情報
==================

既定では、検索ログはいつまでも残ります。
［システム］>［全般］の「以前の検索ログを削除」が既定で ``-1``\ （削除しない）になっているためです。
日数を指定すると、毎日 0 時に動くジョブ「Log Purger」が、その日数より古い検索ログを削除します。
クリックログ、お気に入りログ、チャットログも同じ日数で削除されます。
利用者の記録は別の設定「以前のユーザーログを削除」で、こちらも既定は ``-1`` です。

長期の推移を見たい期間と、社内の個人情報の扱いの両方を考えて日数を決めてください。
検索ログには、ログインユーザーの ID（``user``、``roles`` の ``1`` で始まる値）、IP アドレス、User-Agent が入ります。
また、既定では検索結果に表示された文書の URL やタイトルも ``documents`` フィールドに記録されます（``logging.search.docs.enabled=true``）。
OpenSearch Dashboards ではこれらがすべて見えるので、冒頭のアクセス制限を守ってください。

うまくいかないとき
==================

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 症状
     - 確認すること
   * - Discover やビジュアライゼーションにデータが出ない
     - 右上の期間にログのある日時が入っているか。検索してからログが書き込まれるまで、1 分ほどかかることがあります（毎分動くジョブ「Log Aggregator」が書き込みます）
   * - ``rank`` や ``searchField.label`` を選べない
     - ``fess_log*`` を使っていないか。専用のインデックスパターンを作るか、［Refresh field list］をクリックする
   * - 件数が［検索ログ］画面より多い
     - ``fess_log*`` でクリックやチャットのログまで数えていないか。アクセス種別の絞り込みと、日付の区切りのタイムゾーンが同じか
   * - クリックの件数が少ない
     - リンクが ``/go/`` を経由していない、［全般］の「検索ログ」が無効、またはブラウザーが Fess のセッションを持たないまま ``/go/`` を開いている。:doc:`guide-08` の前提も確認する

次に読む記事
============

- 見つけた検索語を同義語やキーマッチで改善したい: :doc:`guide-08`
- ロールやグループの設計を見直したい: :doc:`guide-05`
- 監視とバックアップを含めた運用を整えたい: :doc:`guide-10`
- 全社展開の段階ごとに何を測るかを決めたい: :doc:`guide-23`

参考資料
========

- `検索ログ <https://fess.codelibs.org/ja/stable/admin/searchlog-guide.html>`__
- `検索ログ可視化の設定 <https://fess.codelibs.org/ja/stable/config/admin-opensearch-dashboards.html>`__
- `全般 <https://fess.codelibs.org/ja/stable/admin/general-guide.html>`__
- `Docker でのインストール (詳細) <https://fess.codelibs.org/ja/stable/install/install-docker.html>`__
- `docker-fess の Compose ファイル（GitHub） <https://github.com/codelibs/docker-fess/tree/v15.9.0/compose>`__
- `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/index/>`__
