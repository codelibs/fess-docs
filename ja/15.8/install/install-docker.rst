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
=========================

以下のコマンドで Docker および Docker Compose のバージョンを確認します。

::

    $ docker --version
    $ docker compose version

.. note::

   古いバージョンの Docker Compose を使用している場合は、``docker-compose`` コマンドを使用します。
   本ドキュメントでは、新しい ``docker compose`` コマンド形式を使用しています。

Docker イメージについて
=======================

|Fess| を Docker Compose で起動すると、以下の 2 つのコンテナが動作します。

- **Fess** (``fess01``): 全文検索システム本体
- **OpenSearch** (``search01``): 検索エンジン

公式 Docker イメージは `GitHub Container Registry <https://github.com/codelibs/docker-fess/pkgs/container/fess>`__ で公開されています。
Compose ファイルおよび起動手順は `docker-fess <https://github.com/codelibs/docker-fess>`__ リポジトリで管理されています。

ステップ 1: Docker Compose ファイルの取得
=========================================

Docker Compose を使用した起動には、以下のファイルが必要です。

方法 1: ファイルを個別にダウンロード
------------------------------------

以下のファイルをダウンロードします：

::

    $ mkdir fess-docker
    $ cd fess-docker
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.8.0/compose/compose.yaml
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.8.0/compose/compose-opensearch3.yaml

方法 2: Git でリポジトリをクローン
----------------------------------

Git がインストールされている場合は、リポジトリ全体をクローンすることもできます：

::

    $ git clone --depth 1 --branch v15.8.0 https://github.com/codelibs/docker-fess.git
    $ cd docker-fess/compose

ステップ 2: Docker Compose ファイルの確認
=========================================

``compose.yaml`` の内容
-----------------------

``compose.yaml`` には、Fess 本体（``fess01`` サービス）の設定が含まれています。

主な設定項目：

- **ポート番号**: Fess の Web インターフェースのポート（デフォルト: 8080）
- **環境変数**: OpenSearch の接続先 (``SEARCH_ENGINE_HTTP_URL``) や辞書ファイルのパス (``FESS_DICTIONARY_PATH``) など
- **起動順序**: OpenSearch (``search01``) が正常な状態になってから起動するよう ``depends_on`` が設定されています

``compose-opensearch3.yaml`` の内容
-----------------------------------

``compose-opensearch3.yaml`` には、検索エンジン（``search01`` サービス、OpenSearch）の設定が含まれています。

主な設定項目：

- **OpenSearch イメージ**: 使用する OpenSearch イメージ（``ghcr.io/codelibs/fess-opensearch``）
- **メモリ設定**: JVM ヒープサイズ
- **ボリューム**: データ永続化用のボリューム（``search01_data``: インデックスデータ、``search01_dictionary``: 辞書ファイル）

設定のカスタマイズ（オプション）
--------------------------------

デフォルトの設定を変更する場合は、``compose.yaml`` を編集します。

例：ポート番号を変更する場合::

    services:
      fess01:
        ports:
          - "9080:8080"  # ホストの 9080 番ポートにマッピング

例：メモリ設定を変更する場合::

    services:
      fess01:
        environment:
          - "FESS_HEAP_SIZE=2g"  # Fess のヒープサイズを 2GB に設定

ステップ 3: Docker コンテナの起動
=================================

基本的な起動
------------

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
----------

コンテナの状態を確認します::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

以下のようなコンテナが起動していることを確認してください：

- ``fess01``
- ``search01``

.. tip::

   起動には数分かかる場合があります。まず OpenSearch (``search01``) が正常な状態になってから Fess (``fess01``) が起動します。
   ``docker compose ... ps`` で各コンテナの状態を確認し、``fess01`` が起動したらブラウザーで http://localhost:8080/ にアクセスできます。

ステップ 4: ブラウザーでアクセス
================================

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

AI検索モード（LLMプラグイン）の有効化
=====================================

|Fess| 15.8 から、AI検索モード（RAG Chat）機能は ``fess-llm-*`` プラグインとして分離されました。
公式の `docker-fess <https://github.com/codelibs/docker-fess>`__ リポジトリには、主要な LLM プロバイダー向けのオーバーレイファイルが同梱されています。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - オーバーレイ
     - 用途
   * - ``compose-ollama.yaml``
     - Ollama（ローカル LLM、追加の ``ollama01`` サービスを起動）
   * - ``compose-gemini.yaml``
     - Google Gemini（クラウド API）
   * - ``compose-openai.yaml``
     - OpenAI（クラウド API）

各オーバーレイは ``FESS_PLUGINS`` で対応するプラグインを自動取得し、``FESS_JAVA_OPTS`` に
``-Dfess.config.rag.chat.enabled=true`` を設定して RAG Chat を有効化します。
クラウド API を利用する Gemini と OpenAI では、さらに ``-Dfess.system.rag.llm.name`` で使用するプロバイダーを指定し、
API キー (``rag.llm.<provider>.api.key``) とモデル (``rag.llm.<provider>.model``) を設定します。
Ollama では ``rag.llm.name`` の既定値 (``ollama``) がそのまま使われるため明示的な指定はなく、
接続先 (``rag.llm.ollama.api.url``) が設定されます。

Gemini を使う例::

    $ export GEMINI_API_KEY="AIzaSy..."
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-gemini.yaml up -d

OpenAI を使う例::

    $ export OPENAI_API_KEY="sk-..."
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml up -d

.. note::

   使用するモデルは、``GEMINI_MODEL`` および ``OPENAI_MODEL`` 環境変数で変更できます
   （既定値はそれぞれ ``gemini-2.5-flash`` と ``gpt-5-mini`` です）。

Ollama を使う例::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-ollama.yaml up -d
    $ docker exec -it ollama01 ollama pull gpt-oss:20b

.. warning::

   ``compose-ollama.yaml`` の ``ollama01`` サービスは、既定で NVIDIA GPU を使用するように定義されています
   （`NVIDIA Container Toolkit <https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html>`__ が必要です）。
   GPU が搭載されていない環境で実行する場合は、``compose-ollama.yaml`` の ``deploy:`` ブロック（``reservations`` 配下の GPU 指定）を削除またはコメントアウトしてください。

.. tip::

   起動後、管理画面「システム > 全般」の設定画面で、使用する LLM プロバイダー (``rag.llm.name``) や
   各プロバイダー固有の設定を変更できます。ただし、これらの変更はコンテナ内の設定ファイルに保存されるため、
   コンテナを再作成（``docker compose down`` 後に ``up``）すると失われます。
   設定を永続化するには、上記の例のように Compose ファイルの ``FESS_JAVA_OPTS`` で指定してください。

データの永続化
==============

|Fess| のデータ（インデックス、クロールしたドキュメント、ユーザー情報、設定など）は、すべて OpenSearch に保存されます。
これらのデータは OpenSearch のボリュームに永続化されるため、コンテナを削除してもデータは保持されます。
Fess 本体（``fess01``）のコンテナ自体は状態を持たず、専用のボリュームはありません。

ボリュームの確認::

    $ docker volume ls

``compose-opensearch3.yaml`` で定義される主なボリューム：

- ``search01_data``: OpenSearch のインデックスデータ（Fess の全データを含む）
- ``search01_dictionary``: 辞書ファイル

.. note::

   Docker Compose のボリューム名には、プロジェクト名（既定では Compose ファイルのあるディレクトリ名）が接頭辞として付きます。
   たとえば ``compose`` ディレクトリで起動した場合、実際のボリューム名は ``compose_search01_data`` のようになります。

.. important::

   コンテナを削除してもボリュームは削除されません。
   ボリュームを削除するには、明示的に ``docker volume rm`` コマンドを実行する必要があります。

Docker コンテナの停止
=====================

コンテナを停止する::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop

コンテナを停止して削除する::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   ``down`` コマンドはコンテナを削除しますが、ボリュームは削除しません。
   ボリューム（``search01_data`` など）も削除する場合は ``-v`` オプションを追加します::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

   **注意**: このコマンドを実行すると、OpenSearch に保存されたすべてのデータが削除されます。

高度な設定
==========

環境変数のカスタマイズ
----------------------

``compose.yaml`` で環境変数を追加・変更することで、詳細な設定が可能です。

主な環境変数：

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 環境変数
     - 説明
   * - ``FESS_HEAP_SIZE``
     - Fess の JVM ヒープサイズ（Docker イメージの既定値: 512m）
   * - ``FESS_JAVA_OPTS``
     - 追加の JVM オプションの指定（``-Dfess.config.*`` による設定の上書きなど）
   * - ``FESS_PLUGINS``
     - 起動時に自動インストールするプラグイン（スペース区切りの ``name:version`` 形式。例: ``fess-ds-wikipedia:15.8.0``）
   * - ``SEARCH_ENGINE_HTTP_URL``
     - OpenSearch の HTTP エンドポイント（``compose.yaml`` の既定値: ``http://search01:9200``）
   * - ``SEARCH_ENGINE_USERNAME`` / ``SEARCH_ENGINE_PASSWORD``
     - 認証が有効な OpenSearch に接続する際の資格情報
   * - ``FESS_DICTIONARY_PATH``
     - 辞書ファイルのパス（OpenSearch と共有するディレクトリ）
   * - ``FESS_PORT``
     - Fess がコンテナ内で待ち受けるポート（既定値: 8080）

例::

    services:
      fess01:
        environment:
          - "FESS_HEAP_SIZE=4g"

.. note::

   タイムゾーンを変更する場合は、``FESS_JAVA_OPTS`` に ``-Duser.timezone=Asia/Tokyo`` のように指定します。

設定ファイルの反映方法
----------------------

|Fess| の詳細な設定は ``fess_config.properties`` ファイルに記述します。
Docker イメージでは、``fess_config.properties`` はコンテナ内の ``/etc/fess`` に配置されています。
Docker 環境で設定を反映させるには、以下の方法があります。

方法 1: 設定ファイルのマウント
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``/etc/fess`` には Fess の動作に必要な他の設定ファイルも含まれるため、このディレクトリをそのままマウントで置き換えると起動に失敗します。
代わりに、クラスパスの先頭に追加されるオーバーライド用ディレクトリ ``/opt/fess`` を使用します（初期状態は空です）。

1. ホスト側に設定ファイルを用意するためのディレクトリを作成::

       $ mkdir -p /path/to/fess-config

2. 設定ファイルのテンプレートを取得（初回のみ）::

       $ curl -o /path/to/fess-config/fess_config.properties https://raw.githubusercontent.com/codelibs/fess/refs/tags/fess-15.8.0/src/main/resources/fess_config.properties

3. ``/path/to/fess-config/fess_config.properties`` を編集して必要な設定を記述::

       # 例
       crawler.document.cache.enabled=false
       adaptive.load.control=20
       query.facet.fields=label,host

4. ``compose.yaml`` の ``fess01`` サービスにボリュームマウントを追加::

       services:
         fess01:
           volumes:
             - /path/to/fess-config/fess_config.properties:/opt/fess/fess_config.properties

5. コンテナを起動::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   ``/opt/fess`` はクラスパスの先頭に追加されるため、ここに置いた ``fess_config.properties`` が
   イメージ同梱の ``/etc/fess/fess_config.properties`` よりも優先されます。
   プロパティファイルはファイル単位で読み込まれ、項目ごとにマージされません。
   そのため、上書きしたい項目だけでなく **すべての設定項目を含む完全なファイル** を配置する必要があります。
   一部の項目のみを変更したい場合は、次の「方法 2」を利用してください。

方法 2: システムプロパティによる設定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``fess_config.properties`` の設定項目を、環境変数経由でシステムプロパティとして上書きできます。

``fess_config.properties`` に記載される設定項目（例: ``crawler.document.cache.enabled=false``）を、
``-Dfess.config.設定項目名=値`` の形式で指定します。

``compose.yaml`` の ``fess01`` サービスの環境変数に ``FESS_JAVA_OPTS`` を追加::

    services:
      fess01:
        environment:
          - "FESS_JAVA_OPTS=-Dfess.config.crawler.document.cache.enabled=false -Dfess.config.adaptive.load.control=20 -Dfess.config.query.facet.fields=label,host"

.. note::

   ``-Dfess.config.`` の後に続く部分が ``fess_config.properties`` の設定項目名に対応します。
   一部の項目のみを上書きする場合は、こちらの方法が簡単です。

外部の OpenSearch への接続
--------------------------

既存の OpenSearch クラスターを使用する場合は、``compose-opensearch3.yaml`` を使わずに ``compose.yaml`` のみで起動し、接続先を変更します。

1. ``compose-opensearch3.yaml`` を指定せずに起動::

       $ docker compose -f compose.yaml up -d

2. ``compose.yaml`` の ``fess01`` サービスで接続先を設定::

       environment:
         - "SEARCH_ENGINE_HTTP_URL=http://your-opensearch-host:9200"

.. note::

   認証が有効な OpenSearch に接続する場合は、``SEARCH_ENGINE_USERNAME`` と ``SEARCH_ENGINE_PASSWORD`` も指定します。

その他のオーバーレイと構成
--------------------------

``docker-fess`` リポジトリには、上記以外にも用途別の Compose ファイルやディレクトリが含まれています。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - ファイル / ディレクトリ
     - 用途
   * - ``compose-dashboards3.yaml``
     - OpenSearch Dashboards を追加（ポート 5601、データ可視化用）
   * - ``compose-minio.yaml``
     - MinIO（オブジェクトストレージ）を追加し、Fess のストレージ機能の保存先として利用
   * - ``vanilla/``
     - Fess 用プラグインを含まない素の OpenSearch と組み合わせる構成（辞書管理などの一部機能は利用不可）
   * - ``snapshot/``
     - 開発版（snapshot）イメージを使用する構成（クラスター構成や Elasticsearch 8 との組み合わせを含む）
   * - ``multi-instance/``
     - 1 つの OpenSearch を共有する複数の Fess インスタンスを起動する構成

Docker ネットワークの設定
-------------------------

複数のサービスと連携する場合、カスタムネットワークを使用できます。

例::

    networks:
      fess-network:
        driver: bridge

    services:
      fess01:
        networks:
          - fess-network

Docker Compose での本番運用
===========================

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
======================

コンテナが起動しない
--------------------

1. ログを確認::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs

2. ポート番号の競合を確認::

       $ sudo netstat -tuln | grep 8080
       $ sudo netstat -tuln | grep 9200

3. ディスク容量を確認::

       $ df -h

メモリ不足エラー
----------------

OpenSearch がメモリ不足で起動しない場合、``vm.max_map_count`` を増やす必要があります。

Linux の場合::

    $ sudo sysctl -w vm.max_map_count=262144

永続的に設定する場合::

    $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
    $ sudo sysctl -p

データの初期化
--------------

すべてのデータを削除して初期状態に戻す::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v
    $ docker volume prune

.. warning::

   このコマンドを実行すると、すべてのデータが完全に削除されます。

次のステップ
============

インストールが完了したら、以下のドキュメントを参照してください：

- :doc:`run` - |Fess| の起動と初回セットアップ
- :doc:`security` - 本番環境でのセキュリティ設定
- :doc:`troubleshooting` - トラブルシューティング

よくある質問
============

Q: イメージのダウンロードにはどのくらいのディスク容量が必要ですか？
--------------------------------------------------------------------

A: Fess と OpenSearch のイメージは初回起動時にダウンロードされ、あわせて数 GB 程度のディスク容量が必要です。
ネットワーク環境によってはダウンロードに時間がかかる場合があります。

Q: Kubernetes での運用は可能ですか？
------------------------------------

A: 可能です。Docker Compose ファイルを ``kompose`` などのツールで Kubernetes マニフェストに変換するか、
独自のマニフェストを作成して運用できます（公式の Helm チャートは提供されていません）。

Q: コンテナのアップデートはどのように行いますか？
--------------------------------------------------

A: 以下の手順でアップデートします：

1. 最新の Compose ファイルを取得
2. コンテナを停止::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

3. 新しいイメージを取得::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

4. コンテナを起動::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Q: マルチノード構成は可能ですか？
----------------------------------

A: 可能です。``docker-fess`` リポジトリの ``snapshot/compose-cluster.yaml`` を参考に OpenSearch を複数ノードで構成したり、
``multi-instance/`` を参考に 1 つの OpenSearch を共有する複数の Fess インスタンスを構成したりできます。
ただし、本番環境では Kubernetes などのオーケストレーションツールの使用を推奨します。
