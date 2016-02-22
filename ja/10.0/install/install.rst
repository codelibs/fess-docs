============
Installation
============

インストール要件
================

|Fess| は以下の環境で利用することができます。

-  OS: Windows や Unix など Java が実行できる OS 環境
-  Java: Java 8u20 以上のバージョン

|Fess| を利用したい環境に Java がインストールされていない場合は、`Oracle のサイト <http://www.oracle.com/technetwork/java/javase/downloads/index.html>`__ より JDK をインストールしてください。

ダウンロード
============

`https://github.com/codelibs/fess/releases <https://github.com/codelibs/fess/releases>`__ から最新の |Fess| パッケージをダウンロードします。

インストール
============

ZIP パッケージを利用する場合
----------------------------

ダウンロードした fess-<version>.zip を展開します。 UNIX 環境では、 以下のコマンドを実行します。

::

    $ unzip fess-<version>.zip
    $ cd fess-<version>

RPM パッケージを利用する場合
----------------------------

|Fess| をインストールする前に elasticsearch の RPM パッケージをインストールする必要があります。 `https://www.elastic.co/downloads/elasticsearch> <https://www.elastic.co/downloads/elasticsearch>`__ からダウンロードし、インストールします。

::

    $ sudo rpm -ivh elasticsearch-<version>.rpm

|Fess| にアクセスするために、/etc/elasticsearch/elasticsearch.yml に下記の設定を加えます。

::

    configsync.config_path: /var/lib/elasticsearch/config
    script.engine.groovy.inline.update: on

次に、|Fess| の RPM パッケージをインストールします。

::

    $ sudo rpm -ivh fess-<version>.rpm

|Fess| には elasticsearch の機能を拡張するためのプラグインがあります。プラグインを elasticsearch の plugins ディレクトリにコピーします。

::

    $ sudo cp -r /usr/share/fess/es/plugins /usr/share/elasticsearch

サービスとして登録するには次のコマンドを入力します。 chkconfig を使う場合は

::

    $ sudo /sbin/chkconfig --add elasticsearch
    $ sudo /sbin/chkconfig --add fess

systemd を使う場合は

::

    $ sudo /bin/systemctl daemon-reload
    $ sudo /bin/systemctl enable elasticsearch.service
    $ sudo /bin/systemctl enable fess.service


