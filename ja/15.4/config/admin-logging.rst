============
ログ設定
============

概要
====

|Fess| は、システムの動作状況やエラー情報を記録するため、複数のログファイルを出力します。
適切なログ設定により、トラブルシューティングやシステム監視が容易になります。

ログファイルの種類
==================

主要なログファイル
------------------

|Fess| が出力する主要なログファイルは以下の通りです。

.. list-table:: ログファイル一覧
   :header-rows: 1
   :widths: 25 75

   * - ファイル名
     - 内容
   * - ``fess.log``
     - 管理画面や検索画面での操作ログ、アプリケーションエラー、システムイベント
   * - ``fess_crawler.log``
     - クロール実行時のログ、クロール対象URL、取得したドキュメント情報、エラー
   * - ``fess_suggest.log``
     - サジェスト(検索候補)生成時のログ、インデックス更新情報
   * - ``server_?.log``
     - Tomcatなどのアプリケーションサーバーのシステムログ
   * - ``audit.log``
     - ユーザー認証、ログイン/ログアウト、重要な操作の監査ログ

ログファイルの場所
------------------

**Zipインストールの場合:**

::

    {FESS_HOME}/logs/

**RPM/DEBパッケージの場合:**

::

    /var/log/fess/

トラブルシューティング時のログ確認
----------------------------------

問題が発生した場合、以下の手順でログを確認してください。

1. **エラーの種類を特定**

   - アプリケーションエラー → ``fess.log``
   - クロールエラー → ``fess_crawler.log``
   - 認証エラー → ``audit.log``
   - サーバーエラー → ``server_?.log``

2. **最新のエラーを確認**

   ::

       tail -f /var/log/fess/fess.log

3. **特定のエラーを検索**

   ::

       grep -i "error" /var/log/fess/fess.log
       grep -i "exception" /var/log/fess/fess.log

4. **エラーコンテキストの確認**

   エラー発生前後のログを確認することで、原因を特定できます。

   ::

       grep -B 10 -A 10 "OutOfMemoryError" /var/log/fess/fess.log

ログレベルの設定
================

ログレベルとは
--------------

ログレベルは、出力するログの詳細度を制御します。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - レベル
     - 説明
   * - ``FATAL``
     - 致命的なエラー(アプリケーションが継続できない)
   * - ``ERROR``
     - エラー(機能の一部が動作しない)
   * - ``WARN``
     - 警告(潜在的な問題)
   * - ``INFO``
     - 情報(重要なイベント)
   * - ``DEBUG``
     - デバッグ情報(詳細な動作ログ)
   * - ``TRACE``
     - トレース情報(最も詳細)

推奨ログレベル
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - 環境
     - 推奨レベル
     - 理由
   * - 本番環境
     - ``WARN``
     - パフォーマンスとディスク容量を重視
   * - ステージング環境
     - ``INFO``
     - 重要なイベントを記録
   * - 開発環境
     - ``DEBUG``
     - 詳細なデバッグ情報が必要
   * - 問題調査時
     - ``DEBUG`` または ``TRACE``
     - 一時的に詳細ログを有効化

管理画面からの変更
------------------

最も簡単な方法は、管理画面から変更することです。

1. 管理画面にログインします。
2. 「システム」メニューから「全般」を選択します。
3. 「ログレベル」で希望するレベルを選択します。
4. 「更新」ボタンをクリックします。

.. note::
   管理画面での変更は |Fess| の再起動後も保持されます。

設定ファイルによる変更
----------------------

より詳細なログ設定を行う場合は、Log4j2の設定ファイルを編集します。

設定ファイルの場所
~~~~~~~~~~~~~~~~~~

- **Zipインストール**: ``app/WEB-INF/classes/log4j2.xml``
- **RPM/DEBパッケージ**: ``/etc/fess/log4j2.xml``

基本的な設定例
~~~~~~~~~~~~~~

**デフォルトのログレベル:**

::

    <Logger name="org.codelibs.fess" level="warn"/>

**例: DEBUGレベルに変更**

::

    <Logger name="org.codelibs.fess" level="debug"/>

**例: 特定のパッケージのログレベル変更**

::

    <Logger name="org.codelibs.fess.crawler" level="info"/>
    <Logger name="org.codelibs.fess.ds" level="debug"/>
    <Logger name="org.codelibs.fess.app.web" level="warn"/>

.. warning::
   ``DEBUG`` や ``TRACE`` レベルは大量のログを出力するため、
   本番環境では使用しないでください。ディスク容量とパフォーマンスに影響します。

環境変数による設定
~~~~~~~~~~~~~~~~~~

システム起動時にログレベルを指定することもできます。

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dlog.level=debug"

クローラーログの設定
====================

クローラーログはデフォルトで ``INFO`` レベルで出力されます。

管理画面での設定
----------------

1. 管理画面の「クローラー」メニューから対象のクロール設定を開きます。
2. 「設定」タブで「スクリプト」を選択します。
3. スクリプト欄に以下を追加します。

::

    logLevel("DEBUG")

設定可能な値:

- ``FATAL``
- ``ERROR``
- ``WARN``
- ``INFO``
- ``DEBUG``
- ``TRACE``

特定のURLパターンのみログレベルを変更
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    if (url.contains("example.com")) {
        logLevel("DEBUG")
    }

クローラープロセス全体のログレベル変更
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``fess_config.properties`` で設定:

::

    logging.level.org.codelibs.fess.crawler=DEBUG

ログローテーション
==================

概要
----

ログファイルは時間とともに肥大化するため、定期的なローテーション(世代管理)が必要です。

Log4j2による自動ローテーション
-------------------------------

|Fess| では、Log4j2のRollingFileAppenderを使用して自動的にログローテーションを行います。

デフォルトの設定
~~~~~~~~~~~~~~~~

- **ファイルサイズ**: 10MB を超えたらローテーション
- **保持世代数**: 最大10ファイル

設定ファイルの例(``log4j2.xml``):

::

    <RollingFile name="FessFile"
                 fileName="${log.dir}/fess.log"
                 filePattern="${log.dir}/fess.log.%i">
        <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n"/>
        <Policies>
            <SizeBasedTriggeringPolicy size="10MB"/>
        </Policies>
        <DefaultRolloverStrategy max="10"/>
    </RollingFile>

日次ローテーションの設定
~~~~~~~~~~~~~~~~~~~~~~~~

サイズではなく、日次でローテーションする場合:

::

    <RollingFile name="FessFile"
                 fileName="${log.dir}/fess.log"
                 filePattern="${log.dir}/fess.log.%d{yyyy-MM-dd}">
        <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n"/>
        <Policies>
            <TimeBasedTriggeringPolicy interval="1" modulate="true"/>
        </Policies>
        <DefaultRolloverStrategy max="30"/>
    </RollingFile>

圧縮設定
~~~~~~~~

ローテーション時に自動的に圧縮する場合:

::

    <RollingFile name="FessFile"
                 fileName="${log.dir}/fess.log"
                 filePattern="${log.dir}/fess.log.%d{yyyy-MM-dd}.gz">
        <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n"/>
        <Policies>
            <TimeBasedTriggeringPolicy interval="1" modulate="true"/>
        </Policies>
        <DefaultRolloverStrategy max="30"/>
    </RollingFile>

logrotateによるローテーション
------------------------------

Linux環境では、logrotateを使用してログローテーションを管理することもできます。

``/etc/logrotate.d/fess`` の例:

::

    /var/log/fess/*.log {
        daily
        rotate 14
        compress
        delaycompress
        missingok
        notifempty
        create 0644 fess fess
        sharedscripts
        postrotate
            systemctl reload fess > /dev/null 2>&1 || true
        endscript
    }

設定の説明:

- ``daily``: 日次でローテーション
- ``rotate 14``: 14世代保持
- ``compress``: 古いログを圧縮
- ``delaycompress``: 1世代前のログは圧縮しない(アプリケーションが書き込み中の可能性)
- ``missingok``: ログファイルがなくてもエラーにしない
- ``notifempty``: 空のログファイルはローテーションしない
- ``create 0644 fess fess``: 新しいログファイルの権限とオーナー

ログ監視
========

本番環境では、ログファイルを監視してエラーを早期に検知することを推奨します。

監視すべきログパターン
----------------------

重要なエラーパターン
~~~~~~~~~~~~~~~~~~~~

- ``ERROR``、``FATAL`` レベルのログ
- ``OutOfMemoryError``
- ``Connection refused``
- ``Timeout``
- ``Exception``
- ``circuit_breaker_exception``
- ``Too many open files``

警告すべきパターン
~~~~~~~~~~~~~~~~~~

- ``WARN`` レベルのログが頻発
- ``Retrying``
- ``Slow query``
- ``Queue full``

リアルタイム監視
----------------

tailコマンドでリアルタイム監視:

::

    tail -f /var/log/fess/fess.log | grep -i "error\|exception"

複数ログファイルの同時監視:

::

    tail -f /var/log/fess/*.log

監視ツールの例
--------------

**Logwatch**

ログファイルの定期的な分析とレポート。

::

    # インストール(CentOS/RHEL)
    yum install logwatch

    # 日次レポート送信
    logwatch --service fess --mailto admin@example.com

**Logstash + OpenSearch + OpenSearch Dashboards**

リアルタイムログ分析とビジュアライゼーション。

**Fluentd**

ログ収集・転送。

::

    <source>
      @type tail
      path /var/log/fess/fess.log
      pos_file /var/log/fluentd/fess.log.pos
      tag fess.app
      <parse>
        @type multiline
        format_firstline /^\d{4}-\d{2}-\d{2}/
        format1 /^(?<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) \[(?<thread>.*?)\] (?<level>\w+)\s+(?<logger>.*?) - (?<message>.*)/
      </parse>
    </source>

**Prometheus + Grafana**

メトリクス監視とアラート。

アラート設定
------------

エラー検知時の通知例:

::

    # シンプルなメール通知スクリプト
    tail -n 0 -f /var/log/fess/fess.log | while read line; do
        echo "$line" | grep -i "error\|fatal" && \
        echo "$line" | mail -s "Fess Error Alert" admin@example.com
    done

ログフォーマット
================

デフォルトフォーマット
----------------------

|Fess| のデフォルトログフォーマット:

::

    %d{ISO8601} [%t] %-5p %c - %m%n

各要素の説明:

- ``%d{ISO8601}``: タイムスタンプ(ISO8601形式)
- ``[%t]``: スレッド名
- ``%-5p``: ログレベル(5文字幅、左寄せ)
- ``%c``: ロガー名(パッケージ名)
- ``%m``: メッセージ
- ``%n``: 改行

カスタムフォーマット例
----------------------

JSON形式でログ出力
~~~~~~~~~~~~~~~~~~

::

    <PatternLayout>
        <pattern>{"timestamp":"%d{ISO8601}","thread":"%t","level":"%-5p","logger":"%c","message":"%m"}%n</pattern>
    </PatternLayout>

より詳細な情報を含める
~~~~~~~~~~~~~~~~~~~~~~

::

    <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c{1.} [%F:%L] - %m%n"/>

追加される情報:

- ``%c{1.}``: 短縮されたパッケージ名
- ``%F``: ファイル名
- ``%L``: 行番号

パフォーマンスへの影響
======================

ログ出力は、ディスクI/Oとパフォーマンスに影響します。

ベストプラクティス
------------------

1. **本番環境ではWARNレベル以上を使用**

   不要な詳細ログを出力しないようにします。

2. **ログファイルの定期的なクリーンアップ**

   古いログファイルを削除または圧縮します。

3. **非同期ログ出力の使用**

   Log4j2の非同期アペンダーを使用して、ログ出力のオーバーヘッドを削減します。

   ::

       <Async name="AsyncFile">
           <AppenderRef ref="FessFile"/>
       </Async>

4. **適切なディスク容量の確保**

   ログファイル用に十分なディスク容量を確保します。

5. **ログレベルの適切な選択**

   環境に応じたログレベルを設定します。

パフォーマンス測定
------------------

ログ出力の影響を測定:

::

    # ログ出力量の確認
    du -sh /var/log/fess/

    # 1時間あたりのログ増加量
    watch -n 3600 'du -sh /var/log/fess/'

トラブルシューティング
======================

ログが出力されない
------------------

**原因と対策:**

1. **ログディレクトリの権限**

   ::

       ls -ld /var/log/fess/
       # 必要に応じて権限を変更
       sudo chown -R fess:fess /var/log/fess/
       sudo chmod 755 /var/log/fess/

2. **ディスク容量**

   ::

       df -h /var/log
       # 容量不足の場合、古いログを削除
       find /var/log/fess/ -name "*.log.*" -mtime +30 -delete

3. **Log4j2設定ファイル**

   ::

       # 設定ファイルの構文チェック
       xmllint --noout /etc/fess/log4j2.xml

4. **SELinuxの確認**

   ::

       # SELinuxが有効な場合
       getenforce
       # 必要に応じてコンテキストを設定
       restorecon -R /var/log/fess/

ログファイルが大きくなりすぎる
------------------------------

1. **ログレベルの調整**

   ``WARN`` 以上に設定してください。

2. **ログローテーション設定の確認**

   ::

       # log4j2.xmlの設定確認
       grep -A 5 "RollingFile" /etc/fess/log4j2.xml

3. **不要なログ出力の無効化**

   ::

       # 特定のパッケージのログを抑制
       <Logger name="org.apache.http" level="error"/>

4. **一時的な対処**

   ::

       # 古いログファイルの圧縮
       gzip /var/log/fess/fess.log.[1-9]

       # 古いログファイルの削除
       find /var/log/fess/ -name "*.log.*" -mtime +7 -delete

特定のログが見つからない
------------------------

1. **ログレベルの確認**

   ログレベルが低すぎると出力されません。

   ::

       grep "org.codelibs.fess" /etc/fess/log4j2.xml

2. **ログファイルパスの確認**

   ::

       # 実際のログ出力先を確認
       ps aux | grep fess
       lsof -p <PID> | grep log

3. **タイムスタンプの確認**

   システム時刻が正しいか確認してください。

   ::

       date
       timedatectl status

4. **ログバッファリング**

   ログが即座に書き込まれない場合があります。

   ::

       # ログの強制フラッシュ
       systemctl reload fess

ログに文字化けが発生する
------------------------

1. **エンコーディング設定**

   ``log4j2.xml`` で文字エンコーディングを指定:

   ::

       <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n" charset="UTF-8"/>

2. **環境変数の設定**

   ::

       export LANG=ja_JP.UTF-8
       export LC_ALL=ja_JP.UTF-8

参考情報
========

- :doc:`setup-memory` - メモリ設定
- :doc:`crawler-advanced` - クローラー詳細設定
- :doc:`admin-index-backup` - インデックスバックアップ
- `Log4j2 Documentation <https://logging.apache.org/log4j/2.x/>`_
