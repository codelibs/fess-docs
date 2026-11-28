==============================================
文書数と利用者の増加に合わせて Fess を拡張する
==============================================

はじめに
========

文書や利用者が増えると、「クロールが朝までに終わらない」「検索が遅くなった」「Fess が OutOfMemoryError で止まった」といった問題が出てきます。
このとき、いきなりサーバーを増やしても解決するとは限りません。
Fess は複数の JVM プロセスで動いており、足りなくなるのはそのうちの 1 つであることが多いからです。

本記事では、Fess 15.9 を対象に、次の順序で拡張の手順を説明します。

1. どのプロセスの何が足りないのかを確かめる
2. 1 台のまま、メモリとクロールの並列度を調整する
3. OpenSearch を別のサーバーに分ける
4. OpenSearch を 3 台のクラスターにする
5. Fess を複数台にする

監視の仕組みづくり（ヘルスチェック、ログ、通知）とバックアップは :doc:`guide-10` で扱います。

Fess を構成するプロセス
=======================

Fess を 1 台で動かしていても、メモリ設定は次のように分かれています。

.. list-table::
   :header-rows: 1
   :widths: 20 30 25 25

   * - プロセス
     - 役割
     - ヒープの既定値
     - 設定する場所
   * - Fess 本体
     - 検索画面、管理画面、API、スケジューラ
     - ZIP 版は最小 256m・最大 2g、RPM/DEB 版と Docker イメージは 512m
     - 環境変数 ``FESS_HEAP_SIZE``
   * - クローラー
     - クロールジョブごとに起動する別の JVM
     - 最大 512m
     - ``fess_config.properties`` の ``jvm.crawler.options``
   * - サジェスト生成、サムネイル生成
     - ジョブごとに起動する別の JVM
     - 最大 256m
     - ``jvm.suggest.options``、``jvm.thumbnail.options``
   * - OpenSearch
     - インデックスの保存と検索の実行
     - docker-fess の ``compose-opensearch3.yaml`` では 1g
     - ``OPENSEARCH_JAVA_OPTS`` または ``config/jvm.options``

セマンティック検索で使うチャンク処理にも別の JVM（``jvm.chunk.options`` 、最大 1g）がありますが、これは :doc:`guide-18` で扱います。

``fess-crawler.log`` に OutOfMemoryError が出ている場合、足りないのはクローラーの JVM です。
このとき ``FESS_HEAP_SIZE`` を増やしても効果はありません。

足りないものを確かめる
======================

症状ごとに、次の場所を確認します。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 症状
     - 確認する場所
   * - 検索が遅い
     - ［システム情報］>［検索ログ］の［パフォーマンス］タブで、応答時間の p95・p99 と応答の遅い検索語を見ます。特定の検索語だけが遅いのか、全体が遅いのかを区別します。
   * - クロールが終わらない
     - ［システム情報］>［ジョブログ］で、クロールジョブの開始時間と終了時間の推移を見ます。 ``fess-crawler.log`` に ``Cpu Load XX% is greater than 50%`` が続けて出ていれば、後述の負荷制御で待たされています。
   * - クローラーが止まる
     - ``fess-crawler.log`` の ``OutOfMemoryError`` を探します。
   * - Fess 本体が止まる・管理画面が重い
     - ``fess.log`` の ``OutOfMemoryError`` と、 ``/api/admin/stats`` の ``response.stats.jvm.memory.heap.percent`` を見ます。
   * - OpenSearch が重い
     - ``/api/admin/stats`` の ``response.stats.engine.status`` と、OpenSearch の ``_cat/nodes`` のヒープ使用率を見ます。 ``circuit_breaker_exception`` はヒープ不足の兆候です。

``/api/admin/stats`` が返すのは、リクエストを受けた Fess 本体の JVM と OS、OpenSearch クラスターの状態です。
クローラーの JVM と、OpenSearch の各ノードのヒープは含まれません。
呼び出しには ``admin-api`` 権限のアクセストークンが必要です。
作り方は `Admin API 概要 <https://fess.codelibs.org/ja/stable/api/admin/api-admin-overview.html>`__ 、レスポンスの項目は `Stats API <https://fess.codelibs.org/ja/stable/api/admin/api-admin-stats.html>`__ を参照してください。

OpenSearch の各ノードのヒープは、OpenSearch に直接問い合わせます。

::

    $ curl -s 'http://localhost:9200/_cat/nodes?v&h=name,heap.max,heap.percent,ram.percent,cpu'

インデックスの文書数とサイズは、次のコマンドで確認できます。
``fess.search`` は検索に使うインデックスの別名です。

::

    $ curl -s 'http://localhost:9200/_cat/indices/fess.search?v&h=index,docs.count,pri.store.size,store.size'

1 台のまま調整する
==================

Fess 本体のヒープを変える
-------------------------

Docker の場合は、 ``compose.yaml`` の ``fess01`` の ``environment`` に ``FESS_HEAP_SIZE`` を追加します。

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "FESS_DICTIONARY_PATH=${FESS_DICTIONARY_PATH:-/usr/share/opensearch/config/dictionary/}"
          - "FESS_HEAP_SIZE=2g"

``compose.yaml`` の ``fess01`` の ``environment`` や ``volumes`` を変えて ``docker compose ... up -d`` を実行すると、 ``fess01`` コンテナは作り直されます。
［システム］>［全般］で変えた設定はコンテナ内の ``system.properties`` にあるため、作り直すと消えます。
この記事のほかの手順で ``compose.yaml`` を変える場合も同じです。
先に :doc:`guide-10` の手順でバックアップを取ってください。

RPM 版は ``/etc/sysconfig/fess`` 、DEB 版は ``/etc/default/fess`` の ``FESS_HEAP_SIZE=512m`` を書き換えて、Fess を再起動します。
ZIP 版は、起動する環境で ``FESS_HEAP_SIZE`` を export します。

反映されたかどうかは、実行中のプロセスの引数で確かめます。
Docker の場合は次のとおりです。

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml exec -T fess01 sh -c 'cat /proc/[0-9]*/cmdline 2>/dev/null' | tr '\0' '\n' | grep -e '^-Xmx' -e 'FessBoot' -e 'exec.Crawler'
    -Xmx2g
    org.codelibs.fess.FessBoot

``-Xmx`` の次の行が、そのプロセスの種類です。
``FessBoot`` は Fess 本体、 ``exec.Crawler`` はクローラーです。
RPM/DEB 版と ZIP 版では、 ``sh -c`` の中のコマンドから後を、Fess のサーバーで直接実行します。

クローラーのヒープを変える
--------------------------

``jvm.crawler.options`` は、JVM オプションを ``\n`` で区切って並べた 1 つの値です。
値全体が置き換わるため、 ``-Xmx1g`` だけを書くと G1GC などの既定のオプションがすべて消えます。
既定値を残したまま、 ``-Xmx512m`` の行だけを書き換えます。

::

    -Xms128m\n\
    -Xmx1g\n\

設定ファイルの場所は、RPM/DEB 版が ``/etc/fess/fess_config.properties`` 、ZIP 版が ``app/WEB-INF/classes/fess_config.properties`` です。
Docker では、イメージの ``fess_config.properties`` を手元に取得して編集し、コンテナの ``/opt/fess/fess_config.properties`` にマウントします。
``/opt/fess`` は ``/etc/fess`` より優先して読み込まれます。
この値は複数行にわたるため、 ``FESS_JAVA_OPTS`` の ``-Dfess.config.`` での指定には向きません。
手順は `Docker でのインストール (詳細) <https://fess.codelibs.org/ja/stable/install/install-docker.html>`__ の「設定ファイルの反映方法」を参照してください。

Fess を再起動したら、［システム情報］>［設定情報］の「アプリのプロパティ」で ``jvm.crawler.options`` に ``-Xmx1g`` が含まれていることを確かめます。
変更は次に起動するクローラーから効きます。
クロールの実行中に前の節のコマンドを実行すると、 ``org.codelibs.fess.exec.Crawler`` の前の行に ``-Xmx1g`` が表示されます。

クローラーの JVM はクロールジョブ 1 つにつき 1 つ起動します。
「Default Crawler」ジョブは、すべてのクロール設定を 1 つのクローラーで処理します。
クロール設定の詳細画面の［新しいジョブの作成］で設定ごとにジョブを作ると、それぞれが別のクローラーとして起動し、それぞれが ``-Xmx`` の分だけメモリを使います。
同時に動くクローラーの数に上限を設けるには、 ``fess_config.properties`` の ``job.max.crawler.processes`` （既定値 ``0`` は無制限）を使います。
上限を超えて起動したクロールジョブは、順番を待たずにエラーで終了します。

サジェスト生成とサムネイル生成の JVM も、同じ方法で ``jvm.suggest.options`` と ``jvm.thumbnail.options`` の ``-Xmx256m`` の行を書き換えます。

OpenSearch のヒープを変える
---------------------------

docker-fess では、 ``compose-opensearch3.yaml`` の ``search01`` に次の行があります。

::

    - "OPENSEARCH_JAVA_OPTS=-Xms1g -Xmx1g"

この 2 つの値を同じ値に書き換えます。
ZIP や RPM で入れた OpenSearch は、 ``config/jvm.options`` の ``-Xms`` と ``-Xmx`` を書き換えて再起動します。

上限の目安は、物理メモリの半分以下、かつ 32GB 未満です。
残りのメモリは OS のファイルキャッシュとして検索の速さに効くため、ヒープに割り当てすぎないようにします。
32GB 以上にすると JVM の Compressed OOPs が無効になり、かえって効率が落ちます。
それ以上が必要な規模では、ノードを増やします。

インデックスのサイズとヒープの対応の目安は `メモリ設定 <https://fess.codelibs.org/ja/stable/config/setup-memory.html>`__ にあります。
目安から始め、先に挙げた ``_cat/nodes`` のヒープ使用率と検索の応答時間を見ながら調整します。

Fess と OpenSearch を同じサーバーで動かす場合は、Fess 本体、クローラー、OpenSearch のヒープの合計が物理メモリに収まるようにします。

クロールの並列度を変える
------------------------

クロールの速さは、次の 3 つの設定で決まります。

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - 設定
     - 既定値
     - 場所
   * - スレッド数
     - ウェブ 1、ファイルシステム 5
     - 各クロール設定（［クローラー］>［ウェブ］、［ファイルシステム］）
   * - 間隔
     - ウェブ 10000 ミリ秒、ファイルシステム 1000 ミリ秒
     - 同上。スレッドごとに、URL を取得するたびに待つ時間です
   * - 同時クローラー設定
     - 5
     - ［システム］>［全般］。1 つのクローラーで同時に処理するクロール設定の数です

スレッド数を増やすと、そのクロール設定の取得は速くなりますが、クローラーのメモリ使用量と、クロール先のサーバーの負荷も増えます。
社外のサイトや業務で使っているサーバーをクロールする場合は、間隔を短くしすぎないようにします。

1 台構成で見落としやすいのが、 ``fess_config.properties`` の ``adaptive.load.control`` （既定値 ``50``）です。
Fess が動くサーバーの CPU 使用率がこの値以上の間、クロールとインデックス登録のスレッドは待機します。
OpenSearch が同じサーバーでインデックスへの書き込みや検索に CPU を使っていると、クロールがほとんど進まなくなることがあります。
このとき ``fess-crawler.log`` には ``Cpu Load XX% is greater than 50%`` が出ます。
値を上げることもできますが、CPU が慢性的に足りないのであれば、次の節のように OpenSearch を別のサーバーに分けるのが根本的な対策です。
詳しくは `負荷制御の設定 <https://fess.codelibs.org/ja/stable/config/load-control.html>`__ を参照してください。

OpenSearch を別のサーバーに分ける
=================================

OpenSearch を別のサーバーに移すと、クロールと検索が CPU、メモリ、ディスク I/O を取り合わなくなります。

OpenSearch 側で必要なこと
-------------------------

Fess が使う OpenSearch には、次の 2 つが必要です。

- Fess 用の 4 つのプラグイン（``opensearch-analysis-fess``、``opensearch-analysis-extension``、``opensearch-minhash``、``opensearch-configsync``）。バージョンは OpenSearch と一致させます（Fess 15.9 は OpenSearch 3.9.0）
- ``opensearch.yml`` の ``configsync.config_path`` 。OpenSearch の設定ディレクトリの下にある、辞書ファイル用のディレクトリを絶対パスで指定します

インストールのコマンドは `Linux へのインストール <https://fess.codelibs.org/ja/stable/install/install-linux.html>`__ にあります。
docker-fess の ``ghcr.io/codelibs/fess-opensearch`` イメージには、これらが最初から入っています。

OpenSearch を別のサーバーに置くと、ポート 9200 がネットワークに公開されます。
セキュリティプラグインを無効にしたまま本番で使わないでください。
設定は :doc:`guide-15` と `セキュリティ設定 <https://fess.codelibs.org/ja/stable/install/security.html>`__ を参照してください。

Fess 側で設定すること
---------------------

Fess には、接続先と辞書の場所を 2 つの環境変数で指定します。

- ``SEARCH_ENGINE_HTTP_URL`` : OpenSearch の URL
- ``FESS_DICTIONARY_PATH`` : OpenSearch 側の ``configsync.config_path`` と同じパス

``FESS_DICTIONARY_PATH`` は OpenSearch のサーバー上のパスです。
Fess は辞書ファイルを ``configsync`` プラグイン経由で書き込むため、Fess のサーバーからそのディレクトリをマウントする必要はありません。
設定していないと、Fess はインデックスを作成できず起動しません。

設定する場所は、RPM 版が ``/etc/sysconfig/fess`` 、DEB 版が ``/etc/default/fess`` 、ZIP 版が ``bin/fess.in.sh`` です。
Docker では ``compose-opensearch3.yaml`` を使わず、 ``compose.yaml`` の ``fess01`` の ``environment`` で指定します。
v15.9.0 の ``compose.yaml`` の ``fess01`` には ``search01`` を待つ ``depends_on`` があり、 ``search01`` を定義しない構成では ``service "fess01" depends on undefined service "search01"`` というエラーで起動できません。
``depends_on`` から ``condition: service_healthy`` までの 3 行を削除します。

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://opensearch1.example.com:9200"
          - "FESS_DICTIONARY_PATH=/etc/opensearch/dictionary/"

この場合、以降の ``docker compose`` コマンドは ``-f compose.yaml`` だけで実行します。

ZIP 版では、Fess を起動する前に ``bin/fess-setup check`` で接続、4 つのプラグイン、 ``configsync`` の応答を確かめられます。

::

    $ bin/fess-setup check --url http://opensearch1.example.com:9200

接続先を変えても、既存のインデックスは新しい OpenSearch には移りません。
既存の文書を引き継ぐ場合は、スナップショットで移行します（ `インデックスの管理 <https://fess.codelibs.org/ja/stable/config/admin-index-backup.html>`__ の「データ移行」）。
クロールし直せば済む場合は、空の OpenSearch に接続して再クロールするほうが簡単です。

OpenSearch を 3 台のクラスターにする
====================================

OpenSearch を 1 台で動かしている間は、そのサーバーが止まると検索も止まります。
冗長性が必要になったら、OpenSearch をクラスターにします。

ノードの構成
------------

クラスターの管理を担うノード（cluster manager）の選出には過半数の合意が必要です。
cluster manager になれるノードが 1 台や 2 台では、1 台が止まっただけで選出できなくなります。
そのため、cluster manager になれるノードを 3 台用意します。
3 台すべてにデータも持たせる構成が最も小さい構成です。

各ノードの ``opensearch.yml`` のうち、クラスターの構成にかかわる設定の例です（``node.name`` はノードごとに変えます）。
``network.host`` などのネットワーク設定とセキュリティの設定は、環境に合わせて追加します。

.. code-block:: yaml

    cluster.name: fess-search
    node.name: search01
    node.roles: [ cluster_manager, data, ingest ]
    discovery.seed_hosts: [ "search01", "search02", "search03" ]
    cluster.initial_cluster_manager_nodes: [ "search01", "search02", "search03" ]
    configsync.config_path: /etc/opensearch/dictionary/

Fess 用の 4 つのプラグインは、3 台すべてに同じバージョンで入れます。
``configsync.config_path`` も 3 台で同じパスにします。
Fess はインデックスの設定に ``FESS_DICTIONARY_PATH`` の値を 1 つだけ書き込み、どのノードもそのパスの辞書を読むためです。

docker-fess の ``compose/snapshot/compose-cluster.yaml`` に、Docker で複数ノードを組む例があります。
この例は開発版の Fess イメージと組み合わせる前提のファイルなので、OpenSearch の環境変数の書き方の参考にしてください。

Fess からの接続
---------------

``SEARCH_ENGINE_HTTP_URL`` には、ノードの URL をカンマで区切って並べます。
一部のノードが止まっていても、Fess は残りのノードに接続します。

::

    SEARCH_ENGINE_HTTP_URL=http://search01:9200,http://search02:9200,http://search03:9200

シャードとレプリカ
------------------

Fess は文書用のインデックスを、 ``fess_config.properties`` の ``index.number_of_shards`` （既定値 ``5`` 、プライマリシャードの数）と ``index.auto_expand_replicas`` （既定値 ``0-1`` 、データノードの数に合わせてレプリカを 0〜1 の範囲で自動で増減）で作成します。
既定値の ``0-1`` のため、データノードが 2 台以上になると、Fess の設定を変えなくても各シャードにレプリカが 1 つ作られます。
クラスターの状態が ``green`` になれば、すべてのレプリカが配置されています。

シャードの数は、インデックスを作成した時点で決まり、後から ``index.number_of_shards`` を変えても既存のインデックスには反映されません。
変えるには、［システム情報］>［メンテナンス］の「再インデクシング」を使います。
「シャード数」と「最大レプリカ数」を指定し、「エイリアスの更新」を有効にして開始すると、新しいインデックスを作って文書をコピーし、 ``fess.search`` と ``fess.update`` の別名を新しいインデックスに付け替えます。

再インデクシングには次の注意点があります。

- 文書は、開始した時点で ``fess.update`` が指すインデックスからコピーされます。クロールが動いていない時間帯に実行してください
- 古いインデックスは自動では削除されません。ディスクには新旧両方のインデックスが入る容量が必要です

画面の項目は `メンテナンス <https://fess.codelibs.org/ja/stable/admin/maintenance-guide.html>`__ を参照してください。

クラスターの確認
----------------

::

    $ curl -s 'http://search01:9200/_cat/nodes?v&h=name,node.role,cluster_manager,heap.percent'
    $ curl -s 'http://search01:9200/_cluster/health?pretty'

3 台が表示され、 ``status`` が ``green`` であれば完成です。
Fess の ``/api/admin/stats`` でも、 ``response.stats.engine.number_of_nodes`` と ``response.stats.engine.status`` で同じことを確かめられます。

Fess を複数台にする
===================

検索の利用者が増えて Fess 本体の CPU が足りなくなった場合や、Fess 自体を冗長にしたい場合は、同じ OpenSearch に複数の Fess をつなぎます。
なお、docker-fess の ``compose/multi-instance/`` は Fess ごとに別のインデックスを使う、独立した検索サービスを並べる構成で、ここで説明する構成とは異なります（組織ごとに分ける場合は :doc:`guide-13`）。

クロール設定、ユーザー、ジョブ、ジョブログは OpenSearch に保存されるため、どの Fess から見ても同じです。
一方、次のものは Fess のサーバーごとにあるため、すべての台でそろえる必要があります。

- ［システム］>［全般］の設定（各サーバーの ``system.properties``）。設定画面で変えると、その台の値だけが変わります
- ``fess_config.properties`` と ``FESS_HEAP_SIZE`` などの環境変数
- インストールしたプラグイン
- ``fess_config.properties`` の ``app.cipher.key`` 。クロール設定やデータストア設定のパラメーターのうち、名前が ``password``、``key``、``token``、``secret`` などで終わる値は、この鍵で暗号化して OpenSearch に保存されます。台ごとに鍵が違うと、ほかの台で保存した値を復号できません

クロールを担当する台を決める
----------------------------

既定のジョブは、どれも「対象」が ``all`` です。
``all`` はどの Fess でも一致するため、そのままでは「Default Crawler」がすべての台で同じ時刻に動きます。

クロールを 1 台に任せるには、次の 2 つを両方行います。

1. クロールを担当する台だけ、 ``fess_config.properties`` に ``scheduler.target.name=crawler`` のように識別名を書いて再起動します。Docker では ``FESS_JAVA_OPTS`` に ``-Dfess.config.scheduler.target.name=crawler`` を指定できます。ほかの台は空のままにします
2. ［システム］>［スケジューラ］で「Default Crawler」を開き、「対象」を ``all`` から ``crawler`` に変えて保存します。［新しいジョブの作成］で作ったクロールジョブも同じように変えます

「対象」にはカンマ区切りで複数の識別名を書けます。
手順 1 だけでは、ジョブはこれまでどおりすべての台で動きます。
手順 2 だけでは、識別名が一致する台がないため、クロールはどの台でも動かなくなります。
手順 1 が反映されたかどうかは、クロールを担当する台の［システム情報］>［設定情報］の「アプリのプロパティ」で ``scheduler.target.name`` の値を見て確かめます。

クロール以外のジョブ（ログの集計や古い文書の削除など）は「対象」を ``all`` のままにしておきます。

固定した後は、［今すぐ開始］もクロールを担当する台の管理画面から押します。
ほかの台で押すと、画面には開始したと表示されますが、その台では実行されず、 ``fess.log`` に ``Ignoring job`` と記録されるだけです。
ロードバランサーの配下にある場合は、クロールを担当する台に直接アクセスできる経路を用意しておきます。

ロードバランサーの設定
----------------------

Fess 15.9 のログインセッションは、各 Fess のメモリに保存されます。
ログインして使う検索画面や管理画面をロードバランサーで振り分ける場合は、同じ利用者を同じ台に送り続けるスティッキーセッションを有効にします。
セッションを OpenSearch に保存して台をまたいで共有する機能は、15.10 以降で使えます。

ロードバランサーのヘルスチェックには ``/api/v2/health`` を使えます。
OpenSearch のクラスターが ``RED`` の場合と、OpenSearch に接続できない場合は 503 を返します。

メンテナンス操作の排他
----------------------

［システム情報］>［メンテナンス］の「再インデクシング」「ドキュメントインデックスのリロード」「クロール用インデックスの削除」「設定インデックスの再構築」は、複数台の Fess で同時に実行されないように排他されます。
ほかの台で実行中の場合は、「<ホスト名>で操作が既に実行中です。」と表示されます。
この排他はメンテナンス操作だけが対象で、ジョブや［全般］の設定を台の間で調整するものではありません。

規模の目安について
==================

文書数や利用者数だけで、必要な構成は決まりません。
1 文書あたりの本文の長さ、添付ファイルの割合、検索語の傾向、ログインして使うかどうかで、必要なメモリと CPU は大きく変わるためです。

次のように、計測した値から判断してください。

- インデックスの ``store.size`` から、 `メモリ設定 <https://fess.codelibs.org/ja/stable/config/setup-memory.html>`__ の目安の表で OpenSearch のヒープを決める
- 検索ログの p95 が悪化し、 ``_cat/nodes`` のヒープ使用率や CPU が高止まりしていれば、OpenSearch のヒープかノードを増やす
- ジョブログのクロール時間が延び、 ``Cpu Load`` のログが出ていれば、OpenSearch を別のサーバーに分ける
- OpenSearch に余裕があるのに Fess 本体の CPU が高ければ、Fess を複数台にする

次に読む記事
============

- 監視、ログ、バックアップを整えて本番運用したい: :doc:`guide-10`
- OpenSearch の公開範囲やログインを含めて、アクセスを保護したい: :doc:`guide-15`
- 複数台の設定をそろえる作業をコードで管理したい: :doc:`guide-16`
- 1 つの Fess を組織ごとに使い分けたい: :doc:`guide-13`
- 展開の段階ごとに確認することを整理したい: :doc:`guide-23`

参考資料
========

- `メモリ設定 <https://fess.codelibs.org/ja/stable/config/setup-memory.html>`__
- `ポートとネットワーク設定 <https://fess.codelibs.org/ja/stable/config/setup-port-network.html>`__
- `負荷制御の設定 <https://fess.codelibs.org/ja/stable/config/load-control.html>`__
- `Linux へのインストール <https://fess.codelibs.org/ja/stable/install/install-linux.html>`__
- `Docker でのインストール (詳細) <https://fess.codelibs.org/ja/stable/install/install-docker.html>`__
- `fess-setup コマンド <https://fess.codelibs.org/ja/stable/install/fess-setup.html>`__
- `メンテナンス <https://fess.codelibs.org/ja/stable/admin/maintenance-guide.html>`__
- `スケジューラ <https://fess.codelibs.org/ja/stable/admin/scheduler-guide.html>`__
- `検索ログ <https://fess.codelibs.org/ja/stable/admin/searchlog-guide.html>`__
- `Stats API <https://fess.codelibs.org/ja/stable/api/admin/api-admin-stats.html>`__
- `インデックスの管理 <https://fess.codelibs.org/ja/stable/config/admin-index-backup.html>`__
