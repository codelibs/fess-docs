======================
ポートとネットワーク設定
======================

概要
====

本セクションでは、|Fess| のネットワーク関連の設定について説明します。
ポート番号の変更、プロキシ設定、HTTP通信の設定など、ネットワーク接続に関する設定を取り扱います。

使用ポートの設定
================

デフォルトポート
----------------

|Fess| はデフォルトで以下のポートを使用します。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - サービス
     - ポート番号
   * - Fess ウェブアプリケーション
     - 8080
   * - OpenSearch (HTTP)
     - 9201
   * - OpenSearch (Transport)
     - 9301

Fess ウェブアプリケーションのポート変更
--------------------------------------

Linux環境での設定
~~~~~~~~~~~~~~~~~

Linux 環境でポート番号を変更する場合は、``bin/fess.in.sh`` を編集します。

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.port=8080"

例えば、ポート 80 を使用する場合:

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.port=80"

.. note::
   1024 以下のポート番号を使用する場合は、root 権限または適切な権限設定(CAP_NET_BIND_SERVICE)が必要です。

環境変数による設定
~~~~~~~~~~~~~~~~~~

環境変数でポート番号を指定することもできます。

::

    export FESS_PORT=8080

RPM/DEBパッケージの場合
~~~~~~~~~~~~~~~~~~~~~~~~

RPMパッケージでは ``/etc/sysconfig/fess``、DEBパッケージでは ``/etc/default/fess`` を編集します。

::

    FESS_PORT=8080

Windows環境での設定
~~~~~~~~~~~~~~~~~~~

Windows 環境では、``bin\fess.in.bat`` を編集します。

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=8080

Windowsサービスとして登録する場合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Windows 環境でサービス登録して使用する場合は、``bin\service.bat`` のポート設定も変更してください。
詳細は :doc:`setup-windows-service` を参照してください。

コンテキストパスの設定
----------------------

|Fess| をサブディレクトリで公開する場合、コンテキストパスを設定できます。

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.context.path=/search"

この設定により、``http://localhost:8080/search/`` でアクセスできるようになります。

.. warning::
   コンテキストパスを変更した場合、静的ファイルのパスも適切に設定する必要があります。

プロキシ設定
============

概要
----

イントラネット内から外部サイトをクロールする場合や、外部APIにアクセスする場合、
ファイアウォールによって通信がブロックされることがあります。
そのような環境では、プロキシサーバー経由で通信を行う設定が必要です。

クローラー用プロキシの設定
--------------------------

基本設定
~~~~~~~~

管理画面のクロール設定で、設定パラメーターに以下のように指定します。

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080

認証が必要なプロキシの設定
~~~~~~~~~~~~~~~~~~~~~~~~~~

プロキシサーバーで認証が必要な場合は、以下のように追加します。

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080
    client.proxyUsername=proxyuser
    client.proxyPassword=proxypass

特定のホストをプロキシから除外
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

特定のホスト(イントラネット内のサーバーなど)をプロキシ経由せずに接続する場合:

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080
    client.nonProxyHosts=localhost|*.local|192.168.*

システム全体のHTTPプロキシ設定
------------------------------

|Fess| アプリケーション全体でHTTPプロキシを使用する場合は、``fess_config.properties`` で設定します。

::

    http.proxy.host=proxy.example.com
    http.proxy.port=8080
    http.proxy.username=proxyuser
    http.proxy.password=proxypass

.. warning::
   パスワードは暗号化されずに保存されます。適切なファイルパーミッションを設定してください。

環境変数によるプロキシ設定
~~~~~~~~~~~~~~~~~~~~~~~~~~

SSO認証などのJavaライブラリがプロキシを使用する場合は、環境変数で設定する必要があります。
これらの環境変数はJavaシステムプロパティ（``http.proxyHost``、``https.proxyHost`` 等）に変換されます。

::

    FESS_PROXY_HOST=proxy.example.com
    FESS_PROXY_PORT=8080
    FESS_NON_PROXY_HOSTS=localhost|*.local|192.168.*

RPMパッケージでは ``/etc/sysconfig/fess``、DEBパッケージでは ``/etc/default/fess`` に設定します。

.. note::
   ``fess_config.properties`` の ``http.proxy.*`` 設定は Fess 内部のHTTP通信で使用されます。
   SSO認証などの外部Javaライブラリがプロキシを使用する場合は、上記の環境変数も設定してください。

HTTP通信設定
============

ファイルアップロードの制限
--------------------------

管理画面からのファイルアップロードサイズを制限できます。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 設定項目
     - 説明
   * - ``http.fileupload.max.size``
     - 最大ファイルアップロードサイズ(デフォルト: 262144000バイト = 250MB)
   * - ``http.fileupload.threshold.size``
     - メモリ上に保持する閾値サイズ(デフォルト: 262144バイト = 256KB)
   * - ``http.fileupload.max.file.count``
     - 一度にアップロードできるファイル数(デフォルト: 10)

``fess_config.properties`` での設定例:

::

    http.fileupload.max.size=524288000
    http.fileupload.threshold.size=524288
    http.fileupload.max.file.count=20

接続タイムアウト設定
--------------------

OpenSearchへの接続タイムアウトを設定できます。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 設定項目
     - 説明
   * - ``search_engine.http.url``
     - OpenSearchのURL(デフォルト: http://localhost:9201)
   * - ``search_engine.heartbeat_interval``
     - ヘルスチェック間隔(ミリ秒、デフォルト: 10000)

OpenSearchの接続先変更
----------------------

外部のOpenSearchクラスタに接続する場合:

::

    search_engine.http.url=http://opensearch-cluster.example.com:9200

複数ノードへの接続
~~~~~~~~~~~~~~~~~~

複数のOpenSearchノードに接続する場合は、カンマ区切りで指定します。

::

    search_engine.http.url=http://node1:9200,http://node2:9200,http://node3:9200

SSL/TLS接続の設定
-----------------

OpenSearchへHTTPSで接続する場合:

::

    search_engine.http.url=https://opensearch.example.com:9200
    search_engine.http.ssl.certificate_authorities=/path/to/ca.crt
    search_engine.username=admin
    search_engine.password=admin_password

.. note::
   証明書の検証を行う場合は、``certificate_authorities`` に CA証明書のパスを指定します。

仮想ホスト設定
==============

概要
----

|Fess| にアクセスされたホスト名によって、検索結果を出し分けることができます。
詳細は :doc:`security-virtual-host` を参照してください。

基本設定
--------

``fess_config.properties`` で仮想ホストのヘッダーを設定します。

::

    virtual.host.headers=X-Forwarded-Host,Host

リバースプロキシとの連携
========================

Nginx の設定例
--------------

::

    server {
        listen 80;
        server_name search.example.com;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-Host $host;
        }
    }

Apache の設定例
---------------

::

    <VirtualHost *:80>
        ServerName search.example.com

        ProxyPreserveHost On
        ProxyPass / http://localhost:8080/
        ProxyPassReverse / http://localhost:8080/

        RequestHeader set X-Forwarded-Proto "http"
        RequestHeader set X-Forwarded-Host "search.example.com"
    </VirtualHost>

SSL/TLS終端
-----------

リバースプロキシでSSL/TLS終端を行う場合の設定例(Nginx):

::

    server {
        listen 443 ssl http2;
        server_name search.example.com;

        ssl_certificate /path/to/cert.pem;
        ssl_certificate_key /path/to/key.pem;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto https;
            proxy_set_header X-Forwarded-Host $host;
        }
    }

ファイアウォール設定
====================

必要なポートの開放
------------------

|Fess| を外部からアクセス可能にする場合、以下のポートを開放します。

**iptables の設定例:**

::

    # Fess ウェブアプリケーション
    iptables -A INPUT -p tcp --dport 8080 -j ACCEPT

    # HTTPSでアクセスする場合(リバースプロキシ経由)
    iptables -A INPUT -p tcp --dport 443 -j ACCEPT

**firewalld の設定例:**

::

    # Fess ウェブアプリケーション
    firewall-cmd --permanent --add-port=8080/tcp
    firewall-cmd --reload

セキュリティグループの設定(クラウド環境)
------------------------------------------

AWS、GCP、Azureなどのクラウド環境では、セキュリティグループやネットワークACLで
適切なポートを開放してください。

推奨設定:
- インバウンド: 80/443ポート(HTTPリバースプロキシ経由)
- 8080ポートは内部からのみアクセス可能に制限
- OpenSearchの9201/9301ポートは内部からのみアクセス可能に制限

トラブルシューティング
======================

ポート変更後にアクセスできない
------------------------------

1. |Fess| を再起動したか確認してください。
2. ファイアウォールで該当ポートが開放されているか確認してください。
3. ログファイル(``fess.log``)でエラーを確認してください。

プロキシ経由でクロールできない
------------------------------

1. プロキシサーバーのホスト名とポートが正しいか確認してください。
2. プロキシサーバーで認証が必要な場合、ユーザー名とパスワードを設定してください。
3. プロキシサーバーのログで接続試行が記録されているか確認してください。
4. ``nonProxyHosts`` の設定が適切か確認してください。

OpenSearchに接続できない
-------------------------

1. OpenSearchが起動しているか確認してください。
2. ``search_engine.http.url`` の設定が正しいか確認してください。
3. ネットワーク接続を確認してください: ``curl http://localhost:9201``
4. OpenSearchのログでエラーを確認してください。

リバースプロキシ経由でアクセスすると正常に動作しない
----------------------------------------------------

1. ``X-Forwarded-Host`` ヘッダーが正しく設定されているか確認してください。
2. ``X-Forwarded-Proto`` ヘッダーが正しく設定されているか確認してください。
3. コンテキストパスが正しく設定されているか確認してください。
4. リバースプロキシのログでエラーを確認してください。

参考情報
========

- :doc:`setup-memory` - メモリ設定
- :doc:`setup-windows-service` - Windowsサービス設定
- :doc:`security-virtual-host` - 仮想ホスト設定
- :doc:`crawler-advanced` - クローラー詳細設定
- `OpenSearch Configuration <https://opensearch.org/docs/latest/install-and-configure/configuration/>`_
