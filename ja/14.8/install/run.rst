==================
起動および停止方法
==================

起動方法
========

TAR.GZ/ZIP版の場合 (Elasticsearch)
----------------------------------

|Fess| を起動する前に Elasticsearch を起動する必要があります。

Windows 環境で Elasticsearch を起動するには、 bin フォルダ中の elasticsearch.bat をダブルクリックします。
Linux/Mac環境では、以下のコマンドを実行します。

::

    $ cd $SEARCH_ENGINE_HOME
    $ ./bin/elasticsearch

次に |Fess| を起動します。Windows 環境で |Fess| を起動するには、 bin フォルダ中の fess.bat をダブルクリックします。
Linux/Mac環境では、以下のコマンドを実行します。

::

    $ cd $FESS_HOME
    $ ./bin/fess

TAR.GZ版の場合 (OpenSearch)
---------------------------

|Fess| を起動する前にOpenSearchを起動する必要があります。

以下のコマンドを実行します。

::

    $ cd $OPENSEARCH_HOME
    $ ./bin/opensearch

次に |Fess| を起動します。以下のコマンドを実行します。

::

    $ cd $FESS_HOME
    $ ./bin/fess

RPM/DEB版の場合 (chkconfig)
---------------------------

|Fess| を起動する前に Elasticsearch を起動する必要があります。

::

    $ sudo service elasticsearch start

次に |Fess| を起動します。

::

    $ sudo service fess start

RPM/DEB版の場合 (systemd)
-------------------------

|Fess| を起動する前に Elasticsearch を起動する必要があります。

::

    $ sudo systemctl start elasticsearch.service

次に |Fess| を起動します。

::

    $ sudo systemctl start fess.service

Docker版の場合 (Elasticsearch)
------------------------------

以下のコマンドを実行して、Elasticsearch と |Fess| を起動します。

::

    $ docker-compose -f docker-compose.yml -f docker-compose.standalone.yml up -d

Docker版の場合 (OpenSearch)
---------------------------

以下のコマンドを実行して、OpenSearchと |Fess| を起動します。

::

    $ docker-compose --env-file .env.opensearch -f docker-compose.yml -f docker-compose.opensearch.yml up -d

ブラウザー UI へのアクセス
==========================

|Fess| は http://localhost:8080/ で利用可能です。

管理 UI は http://localhost:8080/admin です。
デフォルトの管理者アカウントのユーザー名/パスワードは、admin/admin になります。
管理 UI のユーザーページでパスワードを変えることができます。

停止方法
========

TAR.GZ/ZIP版の場合
------------------

|Fess| サーバーを停止させるには |Fess| のプロセスを kill します。

RPM/DEB版の場合 (chkconfig)
---------------------------

|Fess| サーバーを停止させるには次のコマンドを入力します。

::

    $ sudo service fess stop

RPM/DEB版の場合 (systemd)
-------------------------

|Fess| サーバーを停止させるには次のコマンドを入力します。

::

    $ sudo systemctl stop fess.service


Docker版の場合 (Elasticsearch)
------------------------------

以下のコマンドを実行して、Elasticsearch と |Fess| を停止します。

::

    $ docker-compose -f docker-compose.yml -f docker-compose.standalone.yml down

Docker版の場合 (OpenSearch)
---------------------------

以下のコマンドを実行して、OpenSearchと |Fess| を停止します。

::

    $ docker-compose --env-file .env.opensearch -f docker-compose.yml -f docker-compose.opensearch.yml down

