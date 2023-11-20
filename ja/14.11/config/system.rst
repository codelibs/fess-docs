==================
システム関連の設定
==================

使用ポートの設定
================

|Fess| がデフォルトで利用するポートは 8080 になります。
変更する場合は、Linux 環境であれば bin/fess.in.sh の

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.port=8080"

Windows 環境であれば bin\\fess.in.bat の

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=8080

を変更します。

Windows 環境でサービス登録して使用する場合は bin\\service.bat のポートも変更してください。

::

    set FESS_PARAMS=-Dfess;-Dfess.home="%FESS_HOME%";-Dfess.es.dir="%SEARCH_ENGINE_HOME%";-Dfess.home="%FESS_HOME%";-Dfess.context.path="/";-Dfess.port=8080;-Dfess.webapp.path="%FESS_HOME%\app";-Dfess.temp.path="%FESS_HOME%\temp";-Dfess.log.name="%APP_NAME%";-Dfess.log.path="%FESS_HOME%\logs";-Dfess.log.level=warn;-Dlasta.env=web;-Dtomcat.config.path=tomcat_config.properties

使用メモリーの設定
==================

Java ではプロセスごとに使用する最大メモリが設定されています。
|Fess| のウェブアプリ、クローラー、OpenSearchのそれぞれで適切な上限を指定する必要があります。

ウェブアプリのメモリー設定
--------------------------

`fess.log` にOutOfMemoryのエラーが出た場合などのときに設定を変更してください。
一般的な利用状況であれば、変更する必要はありません。

変更する場合は、環境変数 FESS_HEAP_SIZE に FESS_HEAP_SIZE=2g のように指定するか、rpmであれば /etc/sysconfig/fess でFESS_HEAP_SIZEを変更してください。

クローラーのメモリー設定
------------------------

並列アクセス数が高いクロール設定などでは、使用メモリー量を増やす必要があります。
この設定は、クローラープロセス単位(スケジューラーのジョブ単位)で適用されます。

変更するには、app/WEB-INF/classes/fess_config.properties または /etc/fess/fess_config.properties のjvm.crawler.options で -Xmx512m の行を変更してください。

OpenSearchのメモリー設定
------------------------

OpenSearchのログファイルにOutOfMemoryのエラーが出るなどの場合には、ヒープメモリーの使用量を増やしてください。
OpenSearchを稼働させるサーバーではOSのファイルシステムのキャッシュを利用するため、Javaヒープメモリーを確保しすぎるとパフォーマンスが劣化します。
ですので、十分にメモリーを空けておく必要があります。
OpenSearchのドキュメントを参照して、適切な設定をしてください。

ログの設定
==========

ログのファイル
--------------

|Fess| が出力するログファイルを以下にまとめます。

Table: ログファイル一覧

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table:: Table: ログファイル一覧
   :header-rows: 1

   * - ファイル名
     - 内容
   * - ``fess.log``
     - 管理画面や検索画面で操作した時のログが出力されます。
   * - ``fess_crawler.log``
     - クロール実行時のログが出力されます。
   * - ``fess_suggest.log``
     - サジェスト生成時のログが出力されます。
   * - ``server_?.log``
     - システムのログが出力されます。
   * - ``audit.log``
     - ログイン等の監査ログが出力されます。


動作に問題が発生した場合には上記のログを確認してください。

ログレベルの変更
----------------

ログを出力する内容は、管理画面の全般でログレベルの値を変更することができます。
より細かいログまわりの設定をしたい場合は、app/WEB-INF/classes/log4j2.xml または /etc/fess/log4j2.xml で変更することができます。
デフォルトでは WARN レベルとして出力しています。

クローラーログはデフォルトでは INFO レベルで出力しています。
ログレベルを変更する場合は、管理画面のクロールジョブの設定で、logLevel(String)メソッドで指定してください。
