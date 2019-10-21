============
インストール
============

インストール要件
================

|Fess| は以下の環境で利用することができます。

-  OS: Windows や Unix など Java が実行できる OS 環境
-  Java: Java 8u20 以上のバージョン
-  (RPMまたはDEB) Elasticsearch: 5.6.X

|Fess| を利用したい環境に Java がインストールされていない場合は、`Oracle のサイト <http://www.oracle.com/technetwork/java/javase/downloads/index.html>`__ より JDK をインストールしてください。
本番環境での利用では、組み込みElasticsearchでの稼働は推奨しません。

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

RPM/DEB パッケージを利用する場合
----------------------------

|Fess| をインストールする前に elasticsearch の RPM/DEB パッケージをインストールする必要があります。 `https://www.elastic.co/downloads/elasticsearch <https://www.elastic.co/downloads/elasticsearch>`__ からダウンロードし、インストールします。

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

|Fess| には elasticsearch の機能を拡張するためのプラグインがあります。
プラグインを elasticsearch の plugins ディレクトリにインストールします。

::

    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-fess:5.6.2
    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-ja:5.6.2
    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-synonym:5.6.1
    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-configsync:5.6.2
    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-dataformat:5.6.3
    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-langfield:5.6.1
    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-minhash:5.6.1

これらのプラグインはelasticsearchのバージョンに依存するので注意してください。

サービスとして登録するには次のコマンドを入力します。 chkconfig を使う場合(RPM)は

::

    $ sudo /sbin/chkconfig --add elasticsearch
    $ sudo /sbin/chkconfig --add fess

systemd を使う場合(RPM/DEB)は

::

    $ sudo /bin/systemctl daemon-reload
    $ sudo /bin/systemctl enable elasticsearch.service
    $ sudo /bin/systemctl enable fess.service

Elasticsearchクラスタの利用方法
----------------------------

|Fess| では RPM/DEB パッケージでは外部のElasticsearchを標準で利用しますが、ZIPパッケージでのインストールにおいてElasticsearchクラスタを構築しておき、そのElasticsearchクラスタへ接続して利用することができます。
Elasticsearchの設定方法についてはRPMでの設定方法を参照してください。

|Fess| でElasticsearchクラスタへ接続するためには、起動オプションで指定します。
Windows環境では fess-<version>\\bin\\fess.in.batを変更します。
fess.dictionary.pathにはelasticsearch.ymlに設定したconfigsync.config_pathの値を設定してください。

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.es.http_address=http://localhost:9200
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.es.transport_addresses=localhost:9300
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.dictionary.path="c:/<elasticsearch-<version>/config/"

ElasticsearchのRPM/DEBパッケージでは fess-<version>/bin/fess.in.shを変更します。

::

    ES_HTTP_URL=http://localhost:9200
    ES_TRANSPORT_URL=localhost:9300
    FESS_DICTIONARY_PATH=/var/lib/elasticsearch/config/

