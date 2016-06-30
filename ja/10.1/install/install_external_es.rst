=============================
外部のElasticsearchを利用する
=============================

インストール
============

インストールがまだの場合は`http://fess.codelibs.org/ja/10.1/install/install.html#id3<http://fess.codelibs.org/ja/10.1/install/install.html#id3>`を参照してください。
Linux環境の場合はelasticsearchのプラグインまで実施していることとします。

外部のElasticsearch  を利用する場合
----------------------------

起動オプション変更の項目までWindows環境での手順となるため、
Linux環境では elasticsearchを起動し、起動オプション変更の項目を参照ください。

Windowsは ZIP パッケージをインストールする必要があります。 `https://www.elastic.co/downloads/elasticsearch> <https://www.elastic.co/downloads/elasticsearch>`__ からダウンロードし、インストールします。
|Fess| をインストールする前に elasticsearch をインストールする必要があります。

|Fess| にアクセスするために、/etc/elasticsearch/elasticsearch.yml に下記の設定を加えます。

::

    configsync.config_path: elasticsearch-<version>/data
    script.engine.groovy.inline.update: on

|Fess| には elasticsearch の機能を拡張するためのプラグインがあります。
プラグインを elasticsearch の plugins ディレクトリにインストールします。

::

    $ elasticsearch-<version>/bin/plugin.bat install org.codelibs/elasticsearch-analysis-kuromoji-neologd/2.3.0
    $ elasticsearch-<version>/bin/plugin.bat install org.codelibs/elasticsearch-analysis-ja/2.3.0
    $ elasticsearch-<version>/bin/plugin.bat install org.codelibs/elasticsearch-analysis-synonym/2.3.0
    $ elasticsearch-<version>/bin/plugin.bat install org.codelibs/elasticsearch-configsync/2.3.0
    $ elasticsearch-<version>/bin/plugin.bat install org.codelibs/elasticsearch-dataformat/2.3.0
    $ elasticsearch-<version>/bin/plugin.bat install org.codelibs/elasticsearch-langfield/2.3.0
    $ elasticsearch-<version>/bin/plugin.bat install http://maven.codelibs.org/archive/elasticsearch/plugin/kopf/elasticsearch-kopf-2.0.1.0.zip
    $ elasticsearch-<version>/bin/plugin.bat install org.bitbucket.eunjeon/elasticsearch-analysis-seunjeon/2.3.3.0

elasticsearchを起動します。

::

    $ elasticsearch-<version>\bin\elasticsearch.bat

起動オプション変更
----------------------------
Fessの起動オプションを変更します。
Windows環境では fess-<version>\bin\fess.in.batを変更します。

::

    set FESS_PARAMS="%FESS_PARAMS% -Dfess.es.http_address=http://localhost:9200
    set FESS_PARAMS="%FESS_PARAMS% -Dfess.es.transport_addresses=localhost:9300
    set FESS_PARAMS="%FESS_PARAMS% -Dfess.dictionary.path=/<elasticsearch-<version>/data/
    （最終行）

Linux/Unix環境では fess-<version>/bin/fess.in.shを変更します。

::

    ESS_CLASSPATH=$FESS_HOME/lib/classes # 左記の行の下 
 
    ES_HTTP_URL=http://localhost:9200
    ES_TRANSPORT_URL=localhost:9300
    FESS_DICTIONARY_PATH="/elasticsearch-<version>/data/" 

Windowsサービスとして登録するには `http://fess.codelibs.org/ja/10.1/config/windows-service.html <http://fess.codelibs.org/ja/10.1/config/windows-service.html>`を参照ください。

