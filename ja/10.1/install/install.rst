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

|Fess| には elasticsearch の機能を拡張するためのプラグインがあります。
プラグインを elasticsearch の plugins ディレクトリにインストールします。

::

    $ /usr/share/elasticsearch/bin/plugin install org.codelibs/elasticsearch-analysis-kuromoji-neologd/2.3.0
    $ /usr/share/elasticsearch/bin/plugin install org.codelibs/elasticsearch-analysis-ja/2.3.0
    $ /usr/share/elasticsearch/bin/plugin install org.codelibs/elasticsearch-analysis-synonym/2.3.0
    $ /usr/share/elasticsearch/bin/plugin install org.codelibs/elasticsearch-configsync/2.3.0
    $ /usr/share/elasticsearch/bin/plugin install org.codelibs/elasticsearch-dataformat/2.3.0
    $ /usr/share/elasticsearch/bin/plugin install org.codelibs/elasticsearch-langfield/2.3.0
    $ /usr/share/elasticsearch/bin/plugin install http://maven.codelibs.org/archive/elasticsearch/plugin/kopf/elasticsearch-kopf-2.0.1.0.zip
    $ /usr/share/elasticsearch/bin/plugin install org.bitbucket.eunjeon/elasticsearch-analysis-seunjeon/2.3.3.0

サービスとして登録するには次のコマンドを入力します。 chkconfig を使う場合は

::

    $ sudo /sbin/chkconfig --add elasticsearch
    $ sudo /sbin/chkconfig --add fess

systemd を使う場合は

::

    $ sudo /bin/systemctl daemon-reload
    $ sudo /bin/systemctl enable elasticsearch.service
    $ sudo /bin/systemctl enable fess.service

Elasticsearchクラスタの利用方法
----------------------------
Elasticsearchクラスタを利用するにはelasticsearchを起動しておく必要があります。
elasticsearchの設定方法についてはRPMでの設定方法と同様です。
Fessの起動オプションを変更します。
Windows環境では fess-<version>\bin\fess.in.batを変更します。
elasticss.dictionary.pathにはelasticsearch.ymlに設定したconfigsync.config_pathの値を設定してください。

::

    set FESS_PARAMS=%FESS_PARAMS% -Dfess.es.http_address=http://localhost:9200
    set FESS_PARAMS=%FESS_PARAMS% -Dfess.es.transport_addresses=localhost:9300
    set FESS_PARAMS=%FESS_PARAMS% -Dfess.dictionary.path="/<elasticsearch-<version>/data/"
    （最終行）

Linux/Unix環境では fess-<version>/bin/fess.in.shを変更します。

::

    ESS_CLASSPATH=$FESS_HOME/lib/classes # 左記の行の下

    ES_HTTP_URL=http://localhost:9200
    ES_TRANSPORT_URL=localhost:9300
    FESS_DICTIONARY_PATH="/elasticsearch-<version>/data/"
