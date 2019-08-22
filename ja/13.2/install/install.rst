============
インストール
============

インストール要件
================

|Fess| は以下の環境で利用することができます。

-  OS: Windows や Unix など Java が実行できる OS 環境
-  Java: Java 11
-  (RPMまたはDEB) Elasticsearch: 7.2.X

|Fess| を利用したい環境に Java がインストールされていない場合は、`AdoptOpenJDK のサイト <https://adoptopenjdk.net/>`__ より JDK をインストールしてください。
本番環境での利用や負荷検証等では、組み込みElasticsearchでの稼働は推奨しません。

ダウンロード
============

`https://github.com/codelibs/fess/releases <https://github.com/codelibs/fess/releases>`__ から最新の |Fess| パッケージをダウンロードします。

インストール
============

ZIP パッケージを利用する場合
----------------------------

|Fess| をインストールする前に Elasticsearch をインストールする必要があります。 `https://www.elastic.co/downloads/elasticsearch <https://www.elastic.co/downloads/elasticsearch>`__ からダウンロードし、インストールします。
ダウンロードした elasticsearch-<version>.zip を展開します。 UNIX 環境では、 以下のコマンドを実行します。

::

    $ unzip elasticsearch-<version>.zip

ダウンロードした fess-<version>.zip を展開します。 UNIX 環境では、 以下のコマンドを実行します。

::

    $ unzip fess-<version>.zip

|Fess| には Elasticsearch の機能を拡張するためのプラグインがあります。
プラグインを Elasticsearch の plugins ディレクトリにインストールします。

::

    $ ./elasticsearch-<version>/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-fess:7.2.0
    $ ./elasticsearch-<version>/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-extension:7.2.0
    $ ./elasticsearch-<version>/bin/elasticsearch-plugin install org.codelibs:elasticsearch-configsync:7.2.0
    $ ./elasticsearch-<version>/bin/elasticsearch-plugin install org.codelibs:elasticsearch-dataformat:7.2.0
    $ ./elasticsearch-<version>/bin/elasticsearch-plugin install org.codelibs:elasticsearch-minhash:7.2.0

これらのプラグインは Elasticsearch のバージョンに依存するので注意してください。

起動する前に  :ref:`elasticsearch-cluster`  を実施してください。

RPM/DEB パッケージを利用する場合
----------------------------

|Fess| をインストールする前に Elasticsearch の RPM/DEB パッケージをインストールする必要があります。 `https://www.elastic.co/downloads/elasticsearch <https://www.elastic.co/downloads/elasticsearch>`__ からダウンロードし、インストールします。

RPMパッケージの場合

::

    $ sudo rpm -ivh elasticsearch-<version>.rpm

DEBパッケージの場合

::

    $ sudo dpkg -i elasticsearch-<version>.deb

|Fess| にアクセスするために、/etc/elasticsearch/elasticsearch.yml に下記の設定を加えます。(RPM/DEB共通)

::

    configsync.config_path: /var/lib/elasticsearch/config

次に、|Fess| の RPM/DEB パッケージをインストールします。

RPMパッケージの場合

::

    $ sudo rpm -ivh fess-<version>.rpm

DEBパッケージの場合

::

    $ sudo dpkg -i fess-<version>.deb

|Fess| には Elasticsearch の機能を拡張するためのプラグインがあります。
プラグインを Elasticsearch の plugins ディレクトリにインストールします。

::

    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-fess:7.2.0
    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-extension:7.2.0
    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-configsync:7.2.0
    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-dataformat:7.2.0
    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-minhash:7.2.0

これらのプラグインは Elasticsearch のバージョンに依存するので注意してください。

サービスとして登録するには次のコマンドを入力します。 chkconfig を使う場合(RPM)は

::

    $ sudo /sbin/chkconfig --add elasticsearch
    $ sudo /sbin/chkconfig --add fess

systemd を使う場合(RPM/DEB)は

::

    $ sudo /bin/systemctl daemon-reload
    $ sudo /bin/systemctl enable elasticsearch.service
    $ sudo /bin/systemctl enable fess.service

.. _elasticsearch-cluster:

Elasticsearchクラスタの利用方法
----------------------------

|Fess| では RPM/DEB パッケージでは外部の Elasticsearch を標準で利用しますが、ZIPパッケージでのインストールにおいては Elasticsearch クラスタを構築しておき、その Elasticsearch クラスタへ接続して利用することができます。その際は、 Elasticsearch のプラグインのインストールが必要です。
Elasticsearch の設定方法についてはRPM/DEBでの設定方法を参照してください。

|Fess| で Elasticsearch クラスタへ接続するためには、起動オプションで指定します。
Elasticsearch のRPM/DEBパッケージでは fess-<version>/bin/fess.in.sh を変更します。

::

    ES_HTTP_URL=http://localhost:9200
    FESS_DICTIONARY_PATH=/var/lib/elasticsearch/config/

Elasticsearch と接続する際のポート番号を指定するために、fess_config.properties を変更します。

::

    elasticsearch.http.url=http://localhost:9200

Windows環境でElasticsearchクラスタを利用する場合
------------------------------------------------

Elasticsearch のzip版をインストールし、展開します。

コマンドプロンプトから Elasticsearch のプラグインをインストールします。

::

    > c:\elasticsearch-<version>\bin\elasticsearch-plugin install org.codelibs:elasticsearch-analysis-fess:7.2.0
    > c:\elasticsearch-<version>\bin\elasticsearch-plugin install org.codelibs:elasticsearch-analysis-extension:7.2.0
    > c:\elasticsearch-<version>\bin\elasticsearch-plugin install org.codelibs:elasticsearch-configsync:7.2.0
    > c:\elasticsearch-<version>\bin\elasticsearch-plugin install org.codelibs:elasticsearch-dataformat:7.2.0
    > c:\elasticsearch-<version>\bin\elasticsearch-plugin install org.codelibs:elasticsearch-minhash:7.2.0

これらのプラグインは Elasticsearch のバージョンに依存するので注意してください。

|Fess| にアクセスするために、 <elasticsearch-<version>\\config\\elasticsearch.ymlに下記の設定を加えます。

::

    configsync.config_path: c:/<elasticsearch-<version>/config/

ダウンロードした fess-<version>.zip を展開します。

|Fess| で Elasticsearch へ接続するためにfess-<version>\\bin\\fess.in.batを変更します。
fess.dictionary.pathにはelasticsearch.ymlに設定したconfigsync.config_pathの値を設定してください。

::

    set FESS_PARAMS=%FESS_PARAMS% -Dfess.es.http_address=http://localhost:9200
    set FESS_PARAMS=%FESS_PARAMS% -Dfess.dictionary.path="c:/<elasticsearch-<version>/config/"

Elasticsearch と接続する際のポート番号を指定するために、fess-<version>\\app\\WEB-INF\\classes\\fess_config.properties を変更します。

::

    elasticsearch.http.url=http://localhost:9200
