==================
起動および停止方法
==================

起動方法
========

ZIP パッケージの場合
--------------------

Windows 環境で |Fess| を起動するには、 bin フォルダ中の fess.bat をダブルクリックします。UNIX 環境では、以下のコマンドを実行します。

::

    $ ./bin/fess

RPM パッケージの場合(chkconfig)
--------------------

|Fess| を起動する前に elasticsearch を起動する必要があります。

::

    $ sudo service elasticsearch start

そして |Fess| を起動します。

::

    $ sudo service fess start

RPM パッケージの場合(systemd)
--------------------

|Fess| を起動する前に elasticsearch を起動する必要があります。

::

    $ sudo systemctl start elasticsearch.service

そして |Fess| を起動します。

::

    $ sudo systemctl start fess.service

ブラウザー UI へのアクセス
==========================

|Fess| は http://localhost:8080/ で利用可能です。

管理 UI は http://localhost:8080/admin です。
デフォルトの管理者アカウントのユーザー名/パスワードは、admin/admin になります。
管理 UI のユーザーページでパスワードを変えることができます。

停止方法
========

ZIP パッケージの場合
--------------------

|Fess| サーバーを停止させるには |Fess| のプロセスを kill します。

RPM パッケージの場合
--------------------

|Fess| サーバーを停止させるには次のコマンドを入力します。

::

    $ sudo service fess stop

