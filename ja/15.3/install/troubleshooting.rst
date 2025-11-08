==================
トラブルシューティング
==================

このページでは、 |Fess| のインストール、起動、運用時によくある問題とその解決方法について説明します。

インストール時の問題
==================

Java が認識されない
-----------------

**症状:**

::

    -bash: java: command not found

または::

    'java' is not recognized as an internal or external command

**原因:**

Java がインストールされていない、またはPATH環境変数が正しく設定されていない。

**解決方法:**

1. Java がインストールされているか確認::

       $ which java
       $ java -version

2. インストールされていない場合、Java 21 をインストール::

       # Ubuntu/Debian
       $ sudo apt-get update
       $ sudo apt-get install openjdk-21-jdk

       # RHEL/CentOS
       $ sudo yum install java-21-openjdk

3. JAVA_HOME 環境変数を設定::

       $ export JAVA_HOME=/path/to/java
       $ export PATH=$JAVA_HOME/bin:$PATH

   永続的に設定する場合は ``~/.bashrc`` または ``/etc/profile`` に追加します。

プラグインのインストールに失敗する
-------------------------------

**症状:**

::

    ERROR: Plugin installation failed

**原因:**

- ネットワーク接続の問題
- プラグインのバージョンが OpenSearch のバージョンと一致していない
- 権限の問題

**解決方法:**

1. OpenSearch のバージョンを確認::

       $ /path/to/opensearch/bin/opensearch --version

2. プラグインのバージョンを OpenSearch のバージョンに合わせる::

       $ /path/to/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.2

3. 権限を確認::

       $ sudo /path/to/opensearch/bin/opensearch-plugin install ...

4. プロキシ経由でインストールする場合::

       $ export ES_JAVA_OPTS="-Dhttp.proxyHost=proxy.example.com -Dhttp.proxyPort=8080"
       $ /path/to/opensearch/bin/opensearch-plugin install ...

起動時の問題
==========

Fess が起動しない
---------------

**症状:**

Fess の起動コマンドを実行してもエラーが発生する、またはすぐに終了する。

**確認項目:**

1. **OpenSearch が起動しているか確認**::

       $ curl http://localhost:9200/

   正常な場合、JSON レスポンスが返されます。

2. **ポート番号の競合を確認**::

       $ sudo netstat -tuln | grep 8080

   ポート 8080 が既に使用されている場合は、設定ファイルでポート番号を変更してください。

3. **ログファイルを確認**::

       $ tail -f /path/to/fess/logs/fess.log

   エラーメッセージから原因を特定します。

4. **Java のバージョンを確認**::

       $ java -version

   Java 21 以降がインストールされていることを確認してください。

5. **メモリ不足を確認**::

       $ free -h

   メモリが不足している場合、ヒープサイズを調整するか、システムメモリを増設してください。

OpenSearch が起動しない
---------------------

**症状:**

::

    ERROR: bootstrap checks failed

**原因:**

システムの設定が OpenSearch の要件を満たしていない。

**解決方法:**

1. **vm.max_map_count の設定**::

       $ sudo sysctl -w vm.max_map_count=262144

   永続的に設定::

       $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
       $ sudo sysctl -p

2. **ファイル記述子の上限を増やす**::

       $ sudo vi /etc/security/limits.conf

   以下を追加::

       opensearch  -  nofile  65535
       opensearch  -  nproc   4096

3. **メモリロックの設定**::

       $ sudo vi /etc/security/limits.conf

   以下を追加::

       opensearch  -  memlock  unlimited

4. OpenSearch を再起動::

       $ sudo systemctl restart opensearch

ポート番号の競合
--------------

**症状:**

::

    Address already in use

**解決方法:**

1. 使用中のポートを確認::

       $ sudo netstat -tuln | grep 8080
       $ sudo lsof -i :8080

2. 使用中のプロセスを停止、または Fess のポート番号を変更

   設定ファイル (``system.properties``) でポート番号を変更::

       server.port=9080

接続の問題
========

Fess が OpenSearch に接続できない
-------------------------------

**症状:**

ログに以下のようなエラーが表示される::

    Connection refused
    または
    No route to host

**解決方法:**

1. **OpenSearch が起動しているか確認**::

       $ curl http://localhost:9200/

2. **接続URL を確認**

   ``fess.in.sh`` または ``fess.in.bat`` で設定されている URL が正しいか確認::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200

3. **ファイアウォールを確認**::

       $ sudo firewall-cmd --list-all

   ポート 9200 が開放されているか確認します。

4. **ネットワーク接続を確認**

   別のホストで OpenSearch を実行している場合::

       $ ping opensearch-host
       $ telnet opensearch-host 9200

ブラウザーから Fess にアクセスできない
----------------------------------

**症状:**

ブラウザーで http://localhost:8080/ にアクセスできない。

**解決方法:**

1. **Fess が起動しているか確認**::

       $ ps aux | grep fess

2. **ローカルホストでアクセスを試行**::

       $ curl http://localhost:8080/

3. **ファイアウォールを確認**::

       $ sudo firewall-cmd --list-all

   ポート 8080 が開放されているか確認します。

4. **別のホストからアクセスする場合**

   Fess がローカルホスト以外でリッスンしているか確認::

       $ netstat -tuln | grep 8080

   ``127.0.0.1:8080`` の場合は、``0.0.0.0:8080`` または特定の IP アドレスでリッスンするように設定を変更します。

パフォーマンスの問題
==================

検索が遅い
--------

**原因:**

- インデックスサイズが大きい
- メモリ不足
- ディスク I/O が遅い
- クエリが複雑

**解決方法:**

1. **ヒープサイズを増やす**

   ``fess.in.sh`` を編集::

       FESS_HEAP_SIZE=4g

   OpenSearch のヒープサイズも調整::

       export OPENSEARCH_JAVA_OPTS="-Xms4g -Xmx4g"

2. **インデックスの最適化**

   管理画面から「システム」→「スケジューラー」で定期的に最適化を実行します。

3. **SSD を使用する**

   ディスク I/O がボトルネックの場合、SSD に移行します。

4. **キャッシュを有効化**

   設定ファイルでクエリキャッシュを有効化します。

クロールが遅い
-----------

**原因:**

- クロール間隔が長い
- 対象サイトの応答が遅い
- スレッド数が少ない

**解決方法:**

1. **クロール間隔を調整**

   管理画面でクロール設定の「間隔」を短くします（ミリ秒単位）。

   .. warning::

      間隔を短くしすぎると、対象サイトに負荷がかかります。適切な値を設定してください。

2. **スレッド数を増やす**

   設定ファイルでクロールスレッド数を増やします::

       crawler.thread.count=10

3. **タイムアウト値を調整**

   応答の遅いサイトの場合、タイムアウト値を増やします。

データの問題
==========

検索結果が表示されない
--------------------

**原因:**

- インデックスが作成されていない
- クロールが失敗している
- 検索クエリが間違っている

**解決方法:**

1. **インデックスを確認**::

       $ curl http://localhost:9200/_cat/indices?v

   |Fess| のインデックスが存在するか確認します。

2. **クロールログを確認**

   管理画面で「システム」→「ログ」からクロールログを確認し、エラーがないか調べます。

3. **クロールを再実行**

   管理画面で「システム」→「スケジューラー」から「Default Crawler」を実行します。

4. **検索クエリをシンプルにする**

   まず簡単なキーワードで検索して、結果が返されるか確認します。

インデックスが破損している
------------------------

**症状:**

検索時にエラーが発生する、または予期しない結果が返される。

**解決方法:**

1. **インデックスを削除して再作成**

   .. warning::

      インデックスを削除すると、すべての検索データが失われます。必ずバックアップを取得してください。

   ::

       $ curl -X DELETE http://localhost:9200/fess*

2. **クロールを再実行**

   管理画面から「Default Crawler」を実行して、インデックスを再作成します。

Docker 固有の問題
===============

コンテナが起動しない
------------------

**症状:**

``docker compose up`` でコンテナが起動しない。

**解決方法:**

1. **ログを確認**::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs

2. **メモリ不足を確認**

   Docker に割り当てられているメモリを増やします（Docker Desktop の設定から）。

3. **ポート競合を確認**::

       $ docker ps

   他のコンテナがポート 8080 または 9200 を使用していないか確認します。

4. **Docker Compose ファイルを確認**

   YAML ファイルの構文エラーがないか確認します::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml config

コンテナは起動するが Fess にアクセスできない
----------------------------------------

**解決方法:**

1. **コンテナの状態を確認**::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

2. **ログを確認**::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs fess

3. **ネットワーク設定を確認**::

       $ docker network ls
       $ docker network inspect <network_name>

Windows 固有の問題
================

パスの問題
--------

**症状:**

パスに空白や日本語が含まれる場合、エラーが発生する。

**解決方法:**

パスに空白や日本語を含まないディレクトリにインストールしてください。

例::

    C:\opensearch  (推奨)
    C:\Program Files\opensearch  (非推奨)

サービスとして登録できない
------------------------

**解決方法:**

NSSM などのサードパーティツールを使用して、Windows サービスとして登録します。

詳細は :doc:`install-windows` を参照してください。

その他の問題
==========

ログレベルの変更
--------------

詳細なログを確認する場合、ログレベルを DEBUG に変更します。

``log4j2.xml`` を編集::

    <Logger name="org.codelibs.fess" level="debug"/>

データベースのリセット
--------------------

設定をリセットする場合、OpenSearch のインデックスを削除します::

    $ curl -X DELETE http://localhost:9200/.fess_config*

.. warning::

   このコマンドを実行すると、すべての設定データが削除されます。

サポート情報
==========

問題が解決しない場合は、以下のサポートリソースを利用してください：

コミュニティサポート
------------------

- **Issues**: https://github.com/codelibs/fess/issues

  問題を報告する際は、以下の情報を含めてください：

  - Fess のバージョン
  - OpenSearch のバージョン
  - OS とバージョン
  - エラーメッセージ（ログから抜粋）
  - 再現手順

- **フォーラム**: https://discuss.codelibs.org/

商用サポート
----------

商用サポートが必要な場合は、N2SM, Inc. にご相談ください：

- **Web**: https://www.n2sm.net/

デバッグ情報の収集
================

問題を報告する際に、以下の情報を収集しておくと役立ちます：

1. **バージョン情報**::

       $ cat /path/to/fess/VERSION
       $ /path/to/opensearch/bin/opensearch --version
       $ java -version

2. **システム情報**::

       $ uname -a
       $ cat /etc/os-release
       $ free -h
       $ df -h

3. **ログファイル**::

       $ tar czf fess-logs.tar.gz /path/to/fess/logs/

4. **設定ファイル**（機密情報を削除してから）::

       $ tar czf fess-config.tar.gz /path/to/fess/app/WEB-INF/conf/

5. **OpenSearch の状態**::

       $ curl http://localhost:9200/_cluster/health?pretty
       $ curl http://localhost:9200/_cat/indices?v
