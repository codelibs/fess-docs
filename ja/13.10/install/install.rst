============
インストール
============

インストール要件
================

|Fess| は以下の環境で利用することができます。

-  OS: Windows や Unix など Java が実行できる OS 環境
-  Java: Java 11
-  (RPMまたはDEB) Elasticsearch: 7.10.X

|Fess| を利用したい環境に Java がインストールされていない場合は、`AdoptOpenJDK のサイト <https://adoptopenjdk.net/>`__ より JDK をインストールしてください。
本番環境での利用や負荷検証等では、組み込みElasticsearchでの稼働は推奨しません。

ダウンロード
============

`https://github.com/codelibs/fess/releases <https://github.com/codelibs/fess/releases>`__ から最新の |Fess| パッケージをダウンロードします。
Elasticsearch は `https://www.elastic.co/downloads/elasticsearch <https://www.elastic.co/downloads/elasticsearch>`__ から |Fess| のバージョンに合わせたものをダウンロードします。

インストール
============

ZIP パッケージを利用する場合
----------------------------

ダウンロードした elasticsearch-<version>.zip を展開します。 UNIX 環境では、 以下のコマンドを実行します。

::

    $ unzip elasticsearch-<version>.zip

ダウンロードした fess-<version>.zip を展開します。 UNIX 環境では、 以下のコマンドを実行します。

::

    $ unzip fess-<version>.zip

|Fess| には Elasticsearch の機能を拡張するためのプラグインがあります。
プラグインを Elasticsearch の plugins ディレクトリにインストールします。

::

    $ ./elasticsearch-<version>/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-fess:7.10.0
    $ ./elasticsearch-<version>/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-extension:7.10.0
    $ ./elasticsearch-<version>/bin/elasticsearch-plugin install org.codelibs:elasticsearch-configsync:7.10.0
    $ ./elasticsearch-<version>/bin/elasticsearch-plugin install org.codelibs:elasticsearch-dataformat:7.10.0
    $ ./elasticsearch-<version>/bin/elasticsearch-plugin install org.codelibs:elasticsearch-minhash:7.10.0

これらのプラグインは Elasticsearch のバージョンに依存するので注意してください。

|Fess| にアクセスするために、./elasticsearch-<version>/config/elasticsearch.yml に下記の設定を加えます。
./elasticsearch-<version>/data/config のパスを指定します。
設定するパスはインストール先のパスと読み替えてください。

::

    configsync.config_path: /opt/elasticsearch-<version>/data/config/

|Fess| で Elasticsearch クラスタへ接続するためには、起動オプションで指定します。
fess-<version>/bin/fess.in.sh を変更します。

::

    ES_HTTP_URL=http://localhost:9200
    FESS_DICTIONARY_PATH=/opt/elasticsearch-<version>/data/config/


ZIP パッケージを利用する場合（Windows）
------------------------------------------------

ダウンロードした elasticsearch-<version>.zip 、fess-<version>.zip は任意の場所に展開します。

コマンドプロンプトから Elasticsearch のプラグインをインストールします。

::

    > c:\elasticsearch-<version>\bin\elasticsearch-plugin install org.codelibs:elasticsearch-analysis-fess:7.10.0
    > c:\elasticsearch-<version>\bin\elasticsearch-plugin install org.codelibs:elasticsearch-analysis-extension:7.10.0
    > c:\elasticsearch-<version>\bin\elasticsearch-plugin install org.codelibs:elasticsearch-configsync:7.10.0
    > c:\elasticsearch-<version>\bin\elasticsearch-plugin install org.codelibs:elasticsearch-dataformat:7.10.0
    > c:\elasticsearch-<version>\bin\elasticsearch-plugin install org.codelibs:elasticsearch-minhash:7.10.0

これらのプラグインは Elasticsearch のバージョンに依存するので注意してください。

|Fess| にアクセスするために、 <elasticsearch-<version>\\config\\elasticsearch.ymlに下記の設定を加えます。

::

    configsync.config_path: c:/<elasticsearch-<version>/data/config/

|Fess| で Elasticsearch へ接続するためにfess-<version>\\bin\\fess.in.batを変更します。
fess.dictionary.pathにはelasticsearch.ymlに設定したconfigsync.config_pathの値を設定してください。

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.es.http_address=http://localhost:9200
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.dictionary.path="c:/<elasticsearch-<version>/data/config/"


RPM/DEB パッケージを利用する場合
----------------------------

|Fess| をインストールする前に Elasticsearch の RPM/DEB パッケージをインストールする必要があります。

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

    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-fess:7.10.0
    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-extension:7.10.0
    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-configsync:7.10.0
    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-dataformat:7.10.0
    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-minhash:7.10.0

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
