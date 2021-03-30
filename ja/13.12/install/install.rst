============
インストール
============

インストール要件
================

|Fess| は以下の環境で利用することができます。

-  OS: Windows や Unix など Java が実行できる OS 環境
-  Java: Java 11
-  (RPMまたはDEB) Elasticsearch: 7.11.X

|Fess| を利用する環境に Java がインストールされていない場合は、`AdoptOpenJDK のサイト <https://adoptopenjdk.net/>`__ より JDK をインストールしてください。
本番環境での利用や負荷検証等では、組み込みElasticsearchでの稼働は推奨しません。

ダウンロード
============

`Fess のダウンロードサイト <https://fess.codelibs.org/ja/downloads.html>`__ から |Fess| と Elasticsearch をダウンロードします。

インストール
============

Elasticsearchのインストール
---------------------------

`Elasticsearch Reference <https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html>`__ を参照して、Elasticsearchをインストールしてください。

ZIP パッケージを利用する場合
----------------------------

Elasticsearch のプラグインを plugins ディレクトリにインストールします。
Elasticsearch を $ES_HOME にインストールしてあるものとします。

::

    $ $ES_HOME/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-fess:7.11.0
    $ $ES_HOME/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-extension:7.11.0
    $ $ES_HOME/bin/elasticsearch-plugin install org.codelibs:elasticsearch-minhash:7.11.0

これらのプラグインは Elasticsearch のバージョンに依存するので注意してください。

次に elasticsearch-configsync をインストールします。

::

    $ curl -o /tmp/configsync.zip https://repo.maven.apache.org/maven2/org/codelibs/elasticsearch-configsync/7.11.0/elasticsearch-configsync-7.11.0.zip
    $ mkdir -p $ES_HOME/modules/configsync
    $ unzip -d $ES_HOME/modules/configsync /tmp/configsync.zip

$ES_HOME/config/elasticsearch.yml に下記の設定を加えます。
configsync.config_path には $ES_HOME/data/config の絶対パスを指定します。

::

    configsync.config_path: [$ES_HOMEの絶対パス]/data/config/

|Fess| の zip ファイルを $FESS_HOME に展開します。
|Fess| を Elasticsearch クラスタへ接続するために、以下の起動オプションで指定します。
$FESS_HOME/bin/fess.in.sh を変更します。

::

    ES_HTTP_URL=http://localhost:9200
    FESS_DICTIONARY_PATH=[$ES_HOMEの絶対パス]/data/config/


ZIP パッケージを利用する場合（Windows）
---------------------------------------

elasticsearch-<version>.zip と fess-<version>.zip を任意の場所に展開します。
今回は、c:\\elasticsearch-<version> と c:\\fess-<version> に展開したものとします。

コマンドプロンプトから Elasticsearch のプラグインをインストールします。

::

    > c:\elasticsearch-<version>\bin\elasticsearch-plugin install org.codelibs:elasticsearch-analysis-fess:7.11.0
    > c:\elasticsearch-<version>\bin\elasticsearch-plugin install org.codelibs:elasticsearch-analysis-extension:7.11.0
    > c:\elasticsearch-<version>\bin\elasticsearch-plugin install org.codelibs:elasticsearch-minhash:7.11.0

これらのプラグインは Elasticsearch のバージョンに依存するので注意してください。

次に elasticsearch-configsync をインストールします。
c:\\elasticsearch-<version>\\modules\\configsync フォルダを作成して、 `elasticsearch-configsync-7.11.0.zip <https://repo.maven.apache.org/maven2/org/codelibs/elasticsearch-configsync/7.11.0/elasticsearch-configsync-7.11.0.zip>`__ をダウンロードして展開します。

c:\\elasticsearch-<version>\\config\\elasticsearch.yml に下記の設定を加えます。

::

    configsync.config_path: c:/elasticsearch-<version>/data/config/

|Fess| を Elasticsearch クラスタへ接続するために、以下の起動オプションで指定します。
c:\\fess-<version>\\bin\\fess.in.bat を変更します。

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.es.http_address=http://localhost:9200
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.dictionary.path="c:/elasticsearch-<version>/data/config/"


RPM/DEB パッケージを利用する場合
----------------------------

|Fess| をインストールする前に Elasticsearch の RPM/DEB パッケージをインストールします。

RPMパッケージの場合

::

    $ sudo rpm -ivh elasticsearch-<version>.rpm

DEBパッケージの場合

::

    $ sudo dpkg -i elasticsearch-<version>.deb

Elasticsearch プラグインを plugins ディレクトリにインストールします。

::

    $ sudo /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-fess:7.11.0
    $ sudo /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-extension:7.11.0
    $ sudo /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-minhash:7.11.0

これらのプラグインは Elasticsearch のバージョンに依存するので注意してください。

次に elasticsearch-configsync をインストールします。

::

    $ curl -o /tmp/configsync.zip https://repo.maven.apache.org/maven2/org/codelibs/elasticsearch-configsync/7.11.0/elasticsearch-configsync-7.11.0.zip
    $ sudo mkdir -p /usr/share/elasticsearch/modules/configsync
    $ sudo unzip -d /usr/share/elasticsearch/modules/configsync /tmp/configsync.zip

/etc/elasticsearch/elasticsearch.yml に下記の設定を加えます。(RPM/DEB共通)

::

    configsync.config_path: /var/lib/elasticsearch/config

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
