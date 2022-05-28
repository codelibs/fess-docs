============
インストール
============

インストール要件
================

|Fess| は以下の環境で利用することができます。

- OS: JavaまたはDockerが実行可能なOS環境 (WindowsやLinuxなど)
- `Java 17 <https://adoptium.net/>`__ (TAR.GZ/ZIP/RPM/DEB版をインストールする場合)
- `Docker <https://docs.docker.com/get-docker/>`__ および `Docker Compose <https://docs.docker.com/compose/install/>`__ (Docker版をインストールする場合)

本番環境での利用や負荷検証等では、組み込みElasticsearchでの稼働は推奨しません。

TAR.GZ/ZIP/RPM/DEB版はElasticsearch/OpenSearchの正しいバージョンをインストールする必要があります。

ダウンロード
============

`ダウンロードサイト <https://fess.codelibs.org/ja/downloads.html>`__ から |Fess| をダウンロードします。

TAR.GZ版でのインストール (Elasticsearch)
========================================

Elasticsearchのインストール
---------------------------

`Installing Elasticsearch <https://www.elastic.co/guide/en/elasticsearch/reference/8.2/install-elasticsearch.html>`__ を参照して、TAR.GZ版のElasticsearchをダウンロードおよびインストールしてください。
以降でElasticsearchに関する設定を行うので、Elasticsearchの設定や起動は行わないでください。

ElasticsearchのプラグインはElasticseaarchのバージョンに合わせる必要があります。
Elasticsearch 8.2.2をインストール場合を説明します。

Elasticsearch のプラグインを plugins ディレクトリにインストールします。
Elasticsearch を $ES_HOME にインストールしてあるものとします。

::

    $ $ES_HOME/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-fess:8.2.2.0
    $ $ES_HOME/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-extension:8.2.2.0
    $ $ES_HOME/bin/elasticsearch-plugin install org.codelibs:elasticsearch-minhash:8.2.2.0

これらのプラグインは Elasticsearch のバージョンに依存するので注意してください。

次に elasticsearch-configsync をインストールします。

::

    $ curl -o /tmp/configsync.zip https://repo.maven.apache.org/maven2/org/codelibs/elasticsearch-configsync/8.2.2.0/elasticsearch-configsync-8.2.2.0.zip
    $ mkdir -p $ES_HOME/modules/configsync
    $ unzip -d $ES_HOME/modules/configsync /tmp/configsync.zip

$ES_HOME/config/elasticsearch.yml に下記の設定を加えます。
configsync.config_path には $ES_HOME/data/config の絶対パスを指定します。

::

    configsync.config_path: [$ES_HOMEの絶対パス]/data/config/
    xpack.security.enabled: false

Fessのインストール
------------------

|Fess| の zip ファイルを $FESS_HOME に展開します。
|Fess| を Elasticsearch クラスタへ接続するために、以下の起動オプションで指定します。
$FESS_HOME/bin/fess.in.sh を変更します。

::

    ES_HTTP_URL=http://localhost:9200
    FESS_DICTIONARY_PATH=[$ES_HOMEの絶対パス]/data/config/


ZIP版でのインストール (Elasticsearch)
=====================================

Elasticsearchのインストール
---------------------------

`Installing Elasticsearch <https://www.elastic.co/guide/en/elasticsearch/reference/8.2/install-elasticsearch.html>`__ を参照して、ZIP版のElasticsearchをダウンロードおよびインストールしてください。
以降でElasticsearchに関する設定を行うので、Elasticsearchの設定や起動は行わないでください。

ElasticsearchのプラグインはElasticseaarchのバージョンに合わせる必要があります。
Elasticsearch 8.2.2をインストール場合を説明します。

elasticsearch-<version>.zip と fess-<version>.zip を任意の場所に展開します。
今回は、c:\\elasticsearch-<version> と c:\\fess-<version> に展開したものとします。

コマンドプロンプトから Elasticsearch のプラグインをインストールします。

::

    > c:\elasticsearch-<version>\bin\elasticsearch-plugin install org.codelibs:elasticsearch-analysis-fess:8.2.2.0
    > c:\elasticsearch-<version>\bin\elasticsearch-plugin install org.codelibs:elasticsearch-analysis-extension:8.2.2.0
    > c:\elasticsearch-<version>\bin\elasticsearch-plugin install org.codelibs:elasticsearch-minhash:8.2.2.0

これらのプラグインは Elasticsearch のバージョンに依存するので注意してください。

次に elasticsearch-configsync をインストールします。
c:\\elasticsearch-<version>\\modules\\configsync フォルダを作成して、 `elasticsearch-configsync-8.2.2.0.zip <https://repo.maven.apache.org/maven2/org/codelibs/elasticsearch-configsync/8.2.2.0/elasticsearch-configsync-8.2.2.0.zip>`__ をダウンロードして展開します。

c:\\elasticsearch-<version>\\config\\elasticsearch.yml に下記の設定を加えます。

::

    configsync.config_path: c:/elasticsearch-<version>/data/config/
    xpack.security.enabled: false

Fessのインストール
------------------

|Fess| の zip ファイルを %FESS_HOME% に展開します。
|Fess| を Elasticsearch クラスタへ接続するために、以下の起動オプションで指定します。
c:\\fess-<version>\\bin\\fess.in.bat を変更します。

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.es.http_address=http://localhost:9200
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.dictionary.path="c:/elasticsearch-<version>/data/config/"


RPM/DEB版でのインストール (Elasticsearch)
=========================================

Elasticsearchのインストール
---------------------------

`Installing Elasticsearch <https://www.elastic.co/guide/en/elasticsearch/reference/8.2/install-elasticsearch.html>`__ を参照して、RPM/DEB版のElasticsearchをダウンロードおよびインストールしてください。
以降でElasticsearchに関する設定を行うので、Elasticsearchの設定や起動は行わないでください。

ElasticsearchのプラグインはElasticseaarchのバージョンに合わせる必要があります。
Elasticsearch 8.2.2をインストール場合を説明します。

Elasticsearch プラグインを plugins ディレクトリにインストールします。

::

    $ sudo /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-fess:8.2.2.0
    $ sudo /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-extension:8.2.2.0
    $ sudo /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-minhash:8.2.2.0

これらのプラグインは Elasticsearch のバージョンに依存するので注意してください。

次に elasticsearch-configsync をインストールします。

::

    $ curl -o /tmp/configsync.zip https://repo.maven.apache.org/maven2/org/codelibs/elasticsearch-configsync/8.2.2.0/elasticsearch-configsync-8.2.2.0.zip
    $ sudo mkdir -p /usr/share/elasticsearch/modules/configsync
    $ sudo unzip -d /usr/share/elasticsearch/modules/configsync /tmp/configsync.zip

/etc/elasticsearch/elasticsearch.yml に下記の設定を加えます。(RPM/DEB共通)

::

    configsync.config_path: /var/lib/elasticsearch/config
    xpack.security.enabled: false

Fessのインストール
------------------

次に、|Fess| の RPM/DEB パッケージをインストールします。

RPMパッケージの場合

::

    $ sudo rpm -ivh fess-<version>.rpm

DEBパッケージの場合

::

    $ sudo dpkg -i fess-<version>.deb

サービスとして登録するには次のコマンドを入力します。 chkconfig を使う場合(RPM)は

::

    $ sudo /sbin/chkconfig --add elasticsearch
    $ sudo /sbin/chkconfig --add fess

systemd を使う場合(RPM/DEB)は

::

    $ sudo /bin/systemctl daemon-reload
    $ sudo /bin/systemctl enable elasticsearch.service
    $ sudo /bin/systemctl enable fess.service


Docker版でのインストール (Elasticsearch)
========================================

`https://github.com/codelibs/docker-fess/compose <https://github.com/codelibs/docker-fess/tree/v14.2.0/compose>`__ から以下のファイルを取得します。

- `docker-compose.yml <https://raw.githubusercontent.com/codelibs/docker-fess/v14.2.0/compose/docker-compose.yml>`__
- `docker-compose.standalone.yml <https://raw.githubusercontent.com/codelibs/docker-fess/v14.2.0/compose/docker-compose.standalone.yml>`__


TAR.GZ版でのインストール (OpenSearch)
=====================================

OpenSearchのインストール
------------------------

`Download & Get Started <https://opensearch.org/downloads.html>`__ を参照して、TAR.GZ版のOpenSearchをダウンロードしてください。

OpenSearchのプラグインはOpenSearchのバージョンに合わせる必要があります。
OpenSearch 1.3.1をインストール場合を説明します。

OpenSearchのプラグインを plugins ディレクトリにインストールします。
OpenSearchを $OPENSEARCH_HOME にインストールしてあるものとします。

::

    $ $OPENSEARCH_HOME/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:1.3.0
    $ $OPENSEARCH_HOME/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:1.3.0
    $ $OPENSEARCH_HOME/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:1.3.0
    $ $OPENSEARCH_HOME/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:1.3.0


これらのプラグインはOpenSearchのバージョンに依存するので注意してください。

$OPENSEARCH_HOME/config/opensearch.yml に下記の設定を加えます。
configsync.config_path には $OPENSEARCH_HOME/data/config の絶対パスを指定します。

::

    configsync.config_path: [$OPENSEARCH_HOMEの絶対パス]/data/config/
    plugins.security.disabled: true

Fessのインストール
------------------

|Fess| の zip ファイルを $FESS_HOME に展開します。
|Fess| をOpenSearchクラスタへ接続するために、以下の起動オプションで指定します。
$FESS_HOME/bin/fess.in.sh を変更します。

::

    ES_HTTP_URL=http://localhost:9200
    FESS_DICTIONARY_PATH=[$ES_HOMEの絶対パス]/data/config/


Docker版でのインストール (OpenSearch)
=====================================

`https://github.com/codelibs/docker-fess/compose <https://github.com/codelibs/docker-fess/tree/v14.2.0/compose>`__ から以下のファイルを取得します。

- `docker-compose.yml <https://raw.githubusercontent.com/codelibs/docker-fess/v14.2.0/compose/docker-compose.yml>`__
- `docker-compose.opensearch.yml <https://raw.githubusercontent.com/codelibs/docker-fess/v14.2.0/compose/docker-compose.opensearch.yml>`__
- `.env.opensearch <https://raw.githubusercontent.com/codelibs/docker-fess/v14.2.0/compose/.env.opensearch>`__

