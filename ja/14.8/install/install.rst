============
インストール
============

インストール要件
================

|Fess| は以下の環境で利用することができます。

- OS: JavaまたはDockerが実行可能なOS環境 (WindowsやLinuxなど)
- `Java 17 <https://adoptium.net/>`__ (TAR.GZ/ZIP/RPM/DEB版をインストールする場合)
- `Docker <https://docs.docker.com/get-docker/>`__ (Docker版をインストールする場合)

本番環境での利用や負荷検証等では、組み込みOpenSearchでの稼働は推奨しません。

TAR.GZ/ZIP/RPM/DEB版はOpenSearchの正しいバージョンをインストールする必要があります。

ダウンロード
============

`ダウンロードサイト <https://fess.codelibs.org/ja/downloads.html>`__ から |Fess| をダウンロードします。

TAR.GZ版でのインストール
========================

OpenSearchのインストール
------------------------

`Download & Get Started <https://opensearch.org/downloads.html>`__ を参照して、TAR.GZ版のOpenSearchをダウンロードしてください。

OpenSearchのプラグインはOpenSearchのバージョンに合わせる必要があります。
OpenSearch 2.7.0をインストール場合を説明します。

OpenSearchのプラグインを plugins ディレクトリにインストールします。
OpenSearchを $OPENSEARCH_HOME にインストールしてあるものとします。

::

    $ $OPENSEARCH_HOME/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:2.7.0
    $ $OPENSEARCH_HOME/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:2.7.0
    $ $OPENSEARCH_HOME/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:2.7.0
    $ $OPENSEARCH_HOME/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:2.7.0


これらのプラグインはOpenSearchのバージョンに依存するので注意してください。

$OPENSEARCH_HOME/config/opensearch.yml に下記の設定を加えます。
既存の設定がある場合は、書き換えてください。

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

    SEARCH_ENGINE_HTTP_URL=http://localhost:9200
    FESS_DICTIONARY_PATH=[$SEARCH_ENGINE_HOMEの絶対パス]/data/config/


ZIP版でのインストール
===================

OpenSearchのインストール
-----------------------

Windows 環境へのインストールはZIP版を使用します。

`Download & Get Started <https://opensearch.org/downloads.html>`__ を参照して、ZIP版のOpenSearchをダウンロードしてください。

OpenSearchのプラグインはOpenSearchのバージョンに合わせる必要があります。
OpenSearch 2.7.0をインストール場合を説明します。

OpenSearchのプラグインを plugins ディレクトリにインストールします。
OpenSearchを $OPENSEARCH_HOME にインストールしてあるものとします。

::

    $ $OPENSEARCH_HOME\bin\opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:2.7.0
    $ $OPENSEARCH_HOME\bin\opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:2.7.0
    $ $OPENSEARCH_HOME\bin\opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:2.7.0
    $ $OPENSEARCH_HOME\bin\opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:2.7.0

これらのプラグインはOpenSearchのバージョンに依存するので注意してください。

$OPENSEARCH_HOME\config\opensearch.yml に下記の設定を加えます。
既存の設定がある場合は、書き換えてください。

configsync.config_path には $OPENSEARCH_HOME\data\config の絶対パスを指定します。

::

    configsync.config_path: [$OPENSEARCH_HOMEの絶対パス]/data/config/
    plugins.security.disabled: true

Fessのインストール
-----------------

|Fess| の zip ファイルを $FESS_HOME に展開します。
|Fess| をOpenSearchクラスタへ接続するために、以下の起動オプションで指定します。
$FESS_HOME\bin\fess.in.bat を変更します。

::

    SEARCH_ENGINE_HTTP_URL=http://localhost:9200
    FESS_DICTIONARY_PATH=[$SEARCH_ENGINE_HOMEの絶対パス]/data/config/


RPM/DEB版でのインストール
=========================

OpenSearchのインストール
------------------------

`Download & Get Started <https://opensearch.org/downloads.html>`__ を参照して、RPM/DEB版のOpenSearchをダウンロードしてください。

`Installing OpenSearch <https://opensearch.org/docs/2.7/install-and-configure/install-opensearch/index/>`__ を参照してインストールしてください。

以降でOpenSearchに関する設定を行うので、OpenSearchの設定や起動は行わないでください。

OpenSearchのプラグインはOpenSearchのバージョンに合わせる必要があります。
OpenSearch 2.7.0をインストールする場合を説明します。

OpenSearch プラグインを plugins ディレクトリにインストールします。

::

    $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:2.7.0
    $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:2.7.0
    $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:2.7.0
    $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:2.7.0

これらのプラグインは OpenSearch のバージョンに依存するので注意してください。

/etc/opensearch/opensearch.yml に下記の設定を加えます。(RPM/DEB共通)
既存の設定がある場合は、書き換えてください。

::

    configsync.config_path: /var/lib/opensearch/data/config/
    plugins.security.disabled: true

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

    $ sudo /sbin/chkconfig --add OpenSearch
    $ sudo /sbin/chkconfig --add fess

systemd を使う場合(RPM/DEB)は

::

    $ sudo /bin/systemctl daemon-reload
    $ sudo /bin/systemctl enable opensearch.service
    $ sudo /bin/systemctl enable fess.service

|Fess| をOpenSearchクラスタへ接続するために、以下の起動オプションで指定します。
/usr/share/fess/bin/fess.in.sh を変更します。

::

    SEARCH_ENGINE_HTTP_URL=http://localhost:9200
    FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/


Docker版でのインストール
========================

`https://github.com/codelibs/docker-fess/compose <https://github.com/codelibs/docker-fess/tree/v14.8.0/compose>`__ から以下のファイルを取得します。

- `compose.yaml <https://raw.githubusercontent.com/codelibs/docker-fess/v14.8.0/compose/compose.yaml>`__
- `compose-opensearch2.yaml <https://raw.githubusercontent.com/codelibs/docker-fess/v14.8.0/compose/compose-opensearch2.yaml>`__

