==========================
Windowsサービスへの登録
==========================

Windowsサービスとしての登録
============================

|Fess| を Windows のサービスとして登録することができます。サービスとして登録すると、システム起動時に |Fess| を自動的に起動できます。
|Fess| を動かすには、OpenSearch を起動しておく必要があります。
ここでは |Fess| を ``c:\opt\fess`` に、OpenSearch を ``c:\opt\opensearch`` にインストールしてあるものとします（パスは環境に合わせて読み替えてください）。

.. note::
   |Fess| および OpenSearch は 64 ビット版のみをサポートしています。

事前準備
--------

システムの環境変数として ``JAVA_HOME`` を設定してください。``service.bat`` は ``JAVA_HOME`` が設定されていない場合、エラーで終了します。

OpenSearchをサービスとして登録
------------------------------

コマンドプロンプトを管理者権限で起動し、``c:\opt\opensearch\bin\opensearch-service.bat`` を実行します。

::

    > cd c:\opt\opensearch\bin
    > opensearch-service.bat install
    ...
    The service 'opensearch-service-x64' has been installed.

詳細は `OpenSearch のドキュメント <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/windows/>`_ を参照してください。

|Fess| の設定
-------------

サービスは ``c:\opt\fess\bin\service.bat`` から登録します。``service.bat`` は登録時に ``bin\fess.in.bat`` を読み込み、その内容を |Fess| の起動オプションに反映します。
OpenSearch へ接続するための設定を ``c:\opt\fess\bin\fess.in.bat`` に追加してください。

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.search_engine.http_address=http://localhost:9200
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.dictionary.path=c:/opt/opensearch/data/config/

.. note::
   - ``fess.search_engine.http_address`` には、登録した OpenSearch サービスの接続先を指定します。この設定を行わない場合、|Fess| は接続先を見つけられず、本番環境では非推奨の埋め込み版 OpenSearch を起動します。
   - OpenSearch を別のホストで実行している場合は、ホスト名または IP アドレスを適切に変更してください。
   - パスの区切り文字には ``/`` を使用してください。

|Fess| の検索画面・管理画面のデフォルトのポート番号は ``8080`` です。別のポートに変更する場合は ``c:\opt\fess\bin\fess.in.bat`` の ``-Dfess.port`` を編集します。

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=80

.. note::
   サービスとして登録する場合、``bin\service.bat`` 内の ``FESS_PARAMS`` にも ``-Dfess.port=8080`` がハードコードされています。この値は ``fess.in.bat`` の設定よりも優先されるため、ポートを変更する際は ``service.bat`` の ``FESS_PARAMS`` も同様に編集してください。

サービスのカスタマイズ（任意）
------------------------------

``service.bat install`` を実行する前に環境変数を設定することで、サービスの構成を変更できます。主な環境変数は次のとおりです。

.. list-table::
   :header-rows: 1

   * - 環境変数
     - 説明
   * - ``FESS_START_TYPE``
     - スタートアップの種類（``auto`` または ``manual``）。デフォルトは ``manual`` です。
   * - ``FESS_HEAP_SIZE``
     - ヒープサイズ（例: ``1g``）。最小・最大ヒープサイズを個別に指定する場合は ``FESS_MIN_MEM``（デフォルト ``256m``）と ``FESS_MAX_MEM``（デフォルト ``1g``）を使用します。
   * - ``SERVICE_USERNAME`` / ``SERVICE_PASSWORD``
     - サービスを実行する Windows アカウント。
   * - ``SERVICE_DISPLAY_NAME``
     - サービスの表示名。
   * - ``SERVICE_DESCRIPTION``
     - サービスの説明。

登録方法
--------

管理者権限のコマンドプロンプトから ``c:\opt\fess\bin\service.bat`` を実行します。

::

    > cd c:\opt\fess\bin
    > service.bat install
    ...
    The service 'fess-service-x64' has been installed.

サービスの設定
--------------

サービスを手動で起動する場合は、OpenSearch サービスを先に起動し、その後 |Fess| サービスを起動します。
システム起動時に自動的に起動する場合は、スタートアップの種類と依存関係を設定します。

1. サービスの全般設定でスタートアップの種類を「自動（遅延開始）」とします。
2. サービスの依存関係はレジストリで設定します。

レジストリエディター(regedit)で下記のキーと値を追加します。

.. list-table::

   * - *キー*
     - ``コンピューター\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\fess-service-x64\DependOnService``
   * - *値*
     - ``opensearch-service-x64``

追加すると、 |Fess| サービスのプロパティの依存関係に opensearch-service-x64 が表示されます。

.. note::
   ``service.bat install`` の前に環境変数 ``FESS_START_TYPE=auto`` を設定しておくと、スタートアップの種類を「自動」で登録できます。ただし「自動（遅延開始）」や依存関係の設定は ``service.bat`` では行えないため、上記の手順で設定してください。

サービスの管理
--------------

``service.bat`` では、以下のコマンドでサービスを操作できます。

.. list-table::
   :header-rows: 1

   * - コマンド
     - 説明
   * - ``service.bat install``
     - サービスを登録します。
   * - ``service.bat remove``
     - サービスを削除します。
   * - ``service.bat start``
     - サービスを起動します。
   * - ``service.bat stop``
     - サービスを停止します。
   * - ``service.bat manager``
     - サービス管理用の GUI を起動します。
