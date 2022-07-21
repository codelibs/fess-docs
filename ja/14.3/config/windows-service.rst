=======================
Windowsサービスへの登録
=======================

Windowsサービスとしての登録
===========================

|Fess| を Windows のサービスとして登録することができます。
|Fess| を動かすには、Elasticsearch を起動しておく必要があります。
ここでは |Fess| を ``c:\opt\fess`` に、Elasticsearch を ``c:\opt\elasticsearch`` にインストールしてあるものとします。

事前準備
------------------------------------------

システムの環境変数として JAVA_HOME を設定してください。

Elasticsearchをサービスとして登録
------------------------------------------

| コマンドプロンプトから ``c:\opt\elasticsearch\bin\elasticsearch-service.bat`` を管理者で実行します。

::

    > cd c:\opt\elasticsearch\bin
    > elasticsearch-service.bat install
    ...
    The service 'elasticsearch-service-x64' has been installed.

詳細は `Elasticsearch のドキュメント <https://www.elastic.co/guide/en/elasticsearch/reference/5.4/windows.html>`_ を参照してください。

設定
------------------------------------------

``c:\opt\fess\bin\fess.in.bat`` を編集して ES_HOME に Elasticsearch のインストール先を設定します。

::

    set ES_HOME=c:/opt/elasticsearch

|Fess| の検索画面、管理画面のデフォルトのポート番号は 8080 になっています。80 番に変更する場合は ``c:\opt\fess\bin\fess.in.bat`` の fess.port を変更します。

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=80


登録方法
------------------------------------------

コマンドプロンプトから ``c:\opt\fess\bin\service.bat`` を管理者で実行します。

::

    > cd c:\opt\fess\bin
    > service.bat install
    ...
    The service 'fess-service-x64' has been installed.


サービスの設定
------------------------------------------

サービスを手動で起動する場合は Elasticsearch サービスを先に起動し、その後 |Fess| サービスを起動します。
自動起動する場合は依存関係を追加します。

1. サービスの全般設定でスタートアップの種類を「自動（遅延開始）」とします。
2. サービスの依存関係はレジストリで設定します。

レジストリエディタ(regedit)で下記のキーと値を追加します。

.. list-table::

   * - *キー*
     - ``コンピューター\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services \fess-service-x64\DependOnService``
   * - *値*
     - ``elasticsearch-service-x64``

追加すると、 |Fess| サービスのプロパティの依存関係に elasticsearch-service-x64 が表示されます。

