==============================
Docker でのインストール (詳細)
==============================

このページでは、Docker および Docker Compose を使用した |Fess| のインストール手順を説明します。
Docker を使用することで、簡単かつ迅速に |Fess| 環境を構築できます。

前提条件
========

- :doc:`prerequisites` に記載されているシステム要件を満たしていること
- Docker 20.10 以降がインストールされていること
- Docker Compose 2.0 以降がインストールされていること

Docker のインストール確認
=======================

以下のコマンドで Docker および Docker Compose のバージョンを確認します。

::

    $ docker --version
    $ docker compose version

.. note::

   古いバージョンの Docker Compose を使用している場合は、``docker-compose`` コマンドを使用します。
   本ドキュメントでは、新しい ``docker compose`` コマンド形式を使用しています。

Docker イメージについて
=====================

|Fess| の Docker イメージは以下のコンポーネントで構成されています：

- **Fess**: 全文検索システム本体
- **OpenSearch**: 検索エンジン

公式 Docker イメージは `Docker Hub <https://hub.docker.com/r/codelibs/fess>`__ で公開されています。

ステップ 1: Docker Compose ファイルの取得
=======================================

Docker Compose を使用した起動には、以下のファイルが必要です。

方法 1: ファイルを個別にダウンロード
----------------------------------

以下のファイルをダウンロードします：

::

    $ mkdir fess-docker
    $ cd fess-docker
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.3.2/compose/compose.yaml
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.3.2/compose/compose-opensearch3.yaml

方法 2: Git でリポジトリをクローン
--------------------------------

Git がインストールされている場合は、リポジトリ全体をクローンすることもできます：

::

    $ git clone --depth 1 --branch v15.3.2 https://github.com/codelibs/docker-fess.git
    $ cd docker-fess/compose

ステップ 2: Docker Compose ファイルの確認
=======================================

``compose.yaml`` の内容
----------------------

``compose.yaml`` には、Fess の基本的な設定が含まれています。

主な設定項目：

- **ポート番号**: Fess の Web インターフェースのポート（デフォルト: 8080）
- **環境変数**: Java のヒープサイズなどの設定
- **ボリューム**: データの永続化設定

``compose-opensearch3.yaml`` の内容
---------------------------------

``compose-opensearch3.yaml`` には、OpenSearch の設定が含まれています。

主な設定項目：

- **OpenSearch のバージョン**: 使用する OpenSearch のバージョン
- **メモリ設定**: JVM ヒープサイズ
- **ボリューム**: インデックスデータの永続化設定

設定のカスタマイズ（オプション）
------------------------------

デフォルトの設定を変更する場合は、``compose.yaml`` を編集します。

例：ポート番号を変更する場合::

    services:
      fess:
        ports:
          - "9080:8080"  # ホストの 9080 番ポートにマッピング

例：メモリ設定を変更する場合::

    services:
      fess:
        environment:
          - "FESS_HEAP_SIZE=2g"  # Fess のヒープサイズを 2GB に設定

ステップ 3: Docker コンテナの起動
================================

基本的な起動
----------

以下のコマンドで、Fess と OpenSearch を起動します：

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   - ``-f`` オプションで複数の Compose ファイルを指定します
   - ``-d`` オプションでバックグラウンドで実行します

起動ログの確認::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f

``Ctrl+C`` でログ表示を終了できます。

起動の確認
--------

コンテナの状態を確認します::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

以下のようなコンテナが起動していることを確認してください：

- ``fess``
- ``opensearch``

.. tip::

   起動には数分かかる場合があります。
   ログで「Fess is ready」または類似のメッセージが表示されるまで待ちます。

ステップ 4: ブラウザーでアクセス
==============================

起動が完了したら、以下の URL にアクセスします：

- **検索画面**: http://localhost:8080/
- **管理画面**: http://localhost:8080/admin

デフォルトの管理者アカウント：

- ユーザー名: ``admin``
- パスワード: ``admin``

.. warning::

   **セキュリティに関する重要な注意**

   本番環境では、管理者パスワードを必ず変更してください。
   詳細は :doc:`security` を参照してください。

データの永続化
============

Docker コンテナを削除してもデータを保持するために、ボリュームが自動的に作成されます。

ボリュームの確認::

    $ docker volume ls

|Fess| 関連のボリューム：

- ``fess-es-data``: OpenSearch のインデックスデータ
- ``fess-data``: Fess の設定データ

.. important::

   コンテナを削除してもボリュームは削除されません。
   ボリュームを削除するには、明示的に ``docker volume rm`` コマンドを実行する必要があります。

Docker コンテナの停止
===================

コンテナを停止する::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop

コンテナを停止して削除する::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   ``down`` コマンドはコンテナを削除しますが、ボリュームは削除しません。
   ボリュームも削除する場合は ``-v`` オプションを追加します::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

   **注意**: このコマンドを実行すると、すべてのデータが削除されます。

高度な設定
========

環境変数のカスタマイズ
--------------------

``compose.yaml`` で環境変数を追加・変更することで、詳細な設定が可能です。

主な環境変数：

.. list-table::
   :header-rows: 1
   :widths: 30 50

   * - 環境変数
     - 説明
   * - ``FESS_HEAP_SIZE``
     - Fess の JVM ヒープサイズ（デフォルト: 1g）
   * - ``SEARCH_ENGINE_HTTP_URL``
     - OpenSearch の HTTP エンドポイント
   * - ``TZ``
     - タイムゾーン（例: Asia/Tokyo）

例::

    environment:
      - "FESS_HEAP_SIZE=4g"
      - "TZ=Asia/Tokyo"

設定ファイルの反映方法
--------------------

|Fess| の詳細な設定は ``fess_config.properties`` ファイルに記述します。
Docker 環境では、このファイルの設定を反映させるために以下の方法があります。

方法 1: 設定ファイルのマウント
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``fess_config.properties`` などの設定ファイルを含むディレクトリをマウントすることで、
ホスト側で編集した設定ファイルをコンテナに反映できます。

1. ホスト側に設定ディレクトリを作成::

       $ mkdir -p /path/to/fess-config

2. 設定ファイルのテンプレートを取得（初回のみ）::

       $ curl -o /path/to/fess-config/fess_config.properties https://raw.githubusercontent.com/codelibs/fess/refs/tags/fess-15.3.2/src/main/resources/fess_config.properties

3. ``/path/to/fess-config/fess_config.properties`` を編集して必要な設定を記述::

       # 例
       crawler.document.cache.enabled=false
       adaptive.load.control=20
       query.facet.fields=label,host

4. ``compose.yaml`` にボリュームマウントを追加::

       services:
         fess:
           volumes:
             - /path/to/fess-config:/opt/fess/app/WEB-INF/conf

5. コンテナを起動::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   ``fess_config.properties`` には、検索設定、クローラー設定、
   メール設定、その他のシステム設定を記述します。
   ``docker compose down`` でコンテナを削除しても、ホスト側のファイルは保持されます。

方法 2: システムプロパティによる設定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``fess_config.properties`` の設定項目を、環境変数経由でシステムプロパティとして上書きできます。

``fess_config.properties`` に記載される設定項目（例: ``crawler.document.cache.enabled=false``）を、
``-Dfess.config.設定項目名=値`` の形式で指定します。

``compose.yaml`` の環境変数に ``FESS_JAVA_OPTS`` を追加::

    services:
      fess:
        environment:
          - "FESS_JAVA_OPTS=-Dfess.config.crawler.document.cache.enabled=false -Dfess.config.adaptive.load.control=20 -Dfess.config.query.facet.fields=label,host"

.. note::

   ``-Dfess.config.`` の後に続く部分が ``fess_config.properties`` の設定項目名に対応します。

外部の OpenSearch への接続
------------------------

既存の OpenSearch クラスターを使用する場合、``compose.yaml`` を編集して接続先を変更します。

1. ``compose-opensearch3.yaml`` を使用しない::

       $ docker compose -f compose.yaml up -d

2. ``SEARCH_ENGINE_HTTP_URL`` を設定::

       environment:
         - "SEARCH_ENGINE_HTTP_URL=http://your-opensearch-host:9200"

Docker ネットワークの設定
-----------------------

複数のサービスと連携する場合、カスタムネットワークを使用できます。

例::

    networks:
      fess-network:
        driver: bridge

    services:
      fess:
        networks:
          - fess-network

Docker Compose での本番運用
=========================

本番環境で Docker Compose を使用する場合の推奨設定：

1. **リソース制限の設定**::

       deploy:
         resources:
           limits:
             cpus: '2.0'
             memory: 4G
           reservations:
             cpus: '1.0'
             memory: 2G

2. **再起動ポリシーの設定**::

       restart: unless-stopped

3. **ログの設定**::

       logging:
         driver: "json-file"
         options:
           max-size: "10m"
           max-file: "3"

4. **セキュリティ設定の有効化**

   OpenSearch のセキュリティプラグインを有効にし、適切な認証を設定します。
   詳細は :doc:`security` を参照してください。

トラブルシューティング
====================

コンテナが起動しない
------------------

1. ログを確認::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs

2. ポート番号の競合を確認::

       $ sudo netstat -tuln | grep 8080
       $ sudo netstat -tuln | grep 9200

3. ディスク容量を確認::

       $ df -h

メモリ不足エラー
--------------

OpenSearch がメモリ不足で起動しない場合、``vm.max_map_count`` を増やす必要があります。

Linux の場合::

    $ sudo sysctl -w vm.max_map_count=262144

永続的に設定する場合::

    $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
    $ sudo sysctl -p

データの初期化
------------

すべてのデータを削除して初期状態に戻す::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v
    $ docker volume prune

.. warning::

   このコマンドを実行すると、すべてのデータが完全に削除されます。

次のステップ
==========

インストールが完了したら、以下のドキュメントを参照してください：

- :doc:`run` - |Fess| の起動と初回セットアップ
- :doc:`security` - 本番環境でのセキュリティ設定
- :doc:`troubleshooting` - トラブルシューティング

よくある質問
==========

Q: Docker イメージのサイズはどのくらいですか？
--------------------------------------------

A: Fess のイメージは約 1GB、OpenSearch のイメージは約 800MB です。
初回起動時にはダウンロードに時間がかかる場合があります。

Q: Kubernetes での運用は可能ですか？
----------------------------------

A: 可能です。Docker Compose ファイルを Kubernetes のマニフェストに変換するか、
Helm チャートを使用することで Kubernetes 上での運用が可能です。
詳細は Fess の公式ドキュメントを参照してください。

Q: コンテナのアップデートはどのように行いますか？
----------------------------------------------

A: 以下の手順でアップデートします：

1. 最新の Compose ファイルを取得
2. コンテナを停止::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

3. 新しいイメージを取得::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

4. コンテナを起動::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Q: マルチノード構成は可能ですか？
--------------------------------

A: 可能です。``compose-opensearch3.yaml`` を編集して、複数の OpenSearch ノードを定義することで、
クラスター構成にすることができます。ただし、本番環境では Kubernetes などのオーケストレーションツールの使用を推奨します。
