====================
起動、停止、初期設定
====================

このページでは、 |Fess| サーバーの起動、停止、および初回セットアップの手順について説明します。

.. important::

   |Fess| を起動する前に、必ず OpenSearch を起動してください。
   OpenSearch が起動していない場合、 |Fess| は正しく動作しません。

起動方法
========

インストール方法により、起動手順が異なります。

TAR.GZ 版の場合
-------------

OpenSearch の起動
~~~~~~~~~~~~~~~~

::

    $ cd /path/to/opensearch-3.3.2
    $ ./bin/opensearch

バックグラウンドで起動する場合::

    $ ./bin/opensearch -d

Fess の起動
~~~~~~~~~~

::

    $ cd /path/to/fess-15.3.2
    $ ./bin/fess

バックグラウンドで起動する場合::

    $ ./bin/fess -d

.. note::

   起動には数分かかる場合があります。
   ログファイル（``logs/fess.log``）で起動状況を確認できます。

ZIP 版の場合（Windows）
---------------------

OpenSearch の起動
~~~~~~~~~~~~~~~~

1. OpenSearch のインストールディレクトリを開きます
2. ``bin`` フォルダー内の ``opensearch.bat`` をダブルクリックします

または、コマンドプロンプトから::

    C:\> cd C:\opensearch-3.3.2
    C:\opensearch-3.3.2> bin\opensearch.bat

Fess の起動
~~~~~~~~~~

1. Fess のインストールディレクトリを開きます
2. ``bin`` フォルダー内の ``fess.bat`` をダブルクリックします

または、コマンドプロンプトから::

    C:\> cd C:\fess-15.3.2
    C:\fess-15.3.2> bin\fess.bat

RPM/DEB 版の場合 (chkconfig)
--------------------------

OpenSearch の起動::

    $ sudo service opensearch start

Fess の起動::

    $ sudo service fess start

起動状態の確認::

    $ sudo service fess status

RPM/DEB 版の場合 (systemd)
------------------------

OpenSearch の起動::

    $ sudo systemctl start opensearch.service

Fess の起動::

    $ sudo systemctl start fess.service

起動状態の確認::

    $ sudo systemctl status fess.service

サービスの自動起動を有効化::

    $ sudo systemctl enable opensearch.service
    $ sudo systemctl enable fess.service

Docker 版の場合
-------------

Docker Compose を使用して起動::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

起動状態の確認::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

ログの確認::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess

起動の確認
==========

|Fess| が正常に起動したことを確認します。

ヘルスチェック
------------

ブラウザーまたは curl コマンドで以下の URL にアクセスします::

    http://localhost:8080/

正常に起動している場合、Fess の検索画面が表示されます。

コマンドラインでの確認::

    $ curl -I http://localhost:8080/

``HTTP/1.1 200 OK`` が返ってくれば、正常に起動しています。

ログの確認
--------

起動ログを確認して、エラーがないことを確認します。

TAR.GZ/ZIP 版::

    $ tail -f /path/to/fess-15.3.2/logs/fess.log

RPM/DEB 版::

    $ sudo tail -f /var/log/fess/fess.log

または journalctl を使用::

    $ sudo journalctl -u fess.service -f

Docker 版::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess

.. tip::

   正常に起動した場合、ログに以下のようなメッセージが表示されます::

       INFO  Boot - Fess is ready.

ブラウザーでのアクセス
====================

以下の URL にアクセスして、Web インターフェースを確認します。

検索画面
--------

**URL**: http://localhost:8080/

Fess の検索画面が表示されます。初期状態では、クロール設定が行われていないため、検索結果は表示されません。

管理画面
--------

**URL**: http://localhost:8080/admin

デフォルトの管理者アカウント：

- **ユーザー名**: ``admin``
- **パスワード**: ``admin``

.. warning::

   **セキュリティに関する重要な注意**

   デフォルトのパスワードは必ず変更してください。
   特に本番環境では、初回ログイン後すぐにパスワードを変更することを強く推奨します。

初回セットアップ
==============

管理画面にログインしたら、以下の初期設定を行います。

ステップ 1: 管理者パスワードの変更
-------------------------------

1. 管理画面にログイン（http://localhost:8080/admin）
2. 左メニューから「システム」→「ユーザー」をクリック
3. ``admin`` ユーザーをクリック
4. 「パスワード」フィールドに新しいパスワードを入力
5. 「確認」ボタンをクリック
6. 「更新」ボタンをクリック

.. important::

   パスワードは以下の条件を満たすことを推奨します：

   - 8文字以上
   - 英大文字、英小文字、数字、記号を組み合わせる
   - 推測されにくいもの

ステップ 2: クロール設定の作成
---------------------------

検索対象のサイトや ファイルシステムをクロールする設定を作成します。

1. 左メニューから「クローラー」→「ウェブ」をクリック
2. 「新規作成」ボタンをクリック
3. 必要な情報を入力：

   - **名前**: クロール設定の名前（例：会社のWebサイト）
   - **URL**: クロール対象の URL（例：https://www.example.com/）
   - **最大アクセス数**: クロールするページ数の上限
   - **間隔**: クロールの間隔（ミリ秒）

4. 「作成」ボタンをクリック

ステップ 3: クロールの実行
-----------------------

1. 左メニューから「システム」→「スケジューラー」をクリック
2. 「Default Crawler」ジョブの「今すぐ開始」ボタンをクリック
3. クロールが完了するまで待ちます（進行状況はダッシュボードで確認可能）

ステップ 4: 検索の確認
-------------------

1. 検索画面（http://localhost:8080/）にアクセス
2. 検索キーワードを入力
3. 検索結果が表示されることを確認

.. note::

   クロールには時間がかかる場合があります。
   大規模なサイトの場合、数時間から数日かかることもあります。

その他の推奨設定
==============

本番環境で運用する場合、以下の設定も検討してください。

メールサーバーの設定
------------------

障害通知やレポートをメールで受信するために、メールサーバーの設定を行います。

1. 左メニューから「システム」→「全般」をクリック
2. 「メール」タブをクリック
3. SMTP サーバー情報を入力
4. 「更新」ボタンをクリック

タイムゾーンの設定
----------------

1. 左メニューから「システム」→「全般」をクリック
2. 「タイムゾーン」を適切な値に設定（例：Asia/Tokyo）
3. 「更新」ボタンをクリック

ログレベルの調整
--------------

本番環境では、ログレベルを調整してディスク使用量を抑えることができます。

設定ファイル（``app/WEB-INF/classes/log4j2.xml``）を編集します。

詳細は管理者ガイドを参照してください。

停止方法
========

TAR.GZ/ZIP 版の場合
-----------------

Fess の停止
~~~~~~~~~~

プロセスを kill します::

    $ ps aux | grep fess
    $ kill <PID>

または、``Ctrl+C`` でコンソールから停止できます（フォアグラウンドで実行している場合）。

OpenSearch の停止::

    $ ps aux | grep opensearch
    $ kill <PID>

RPM/DEB 版の場合 (chkconfig)
--------------------------

Fess の停止::

    $ sudo service fess stop

OpenSearch の停止::

    $ sudo service opensearch stop

RPM/DEB 版の場合 (systemd)
------------------------

Fess の停止::

    $ sudo systemctl stop fess.service

OpenSearch の停止::

    $ sudo systemctl stop opensearch.service

Docker 版の場合
-------------

コンテナの停止::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop

コンテナの停止と削除::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   ``down`` コマンドでボリュームも削除する場合は ``-v`` オプションを追加します。
   この場合、すべてのデータが削除されるため注意してください。

再起動方法
==========

TAR.GZ/ZIP 版の場合
-----------------

停止してから起動します。

RPM/DEB 版の場合
--------------

chkconfig::

    $ sudo service fess restart

systemd::

    $ sudo systemctl restart fess.service

Docker 版の場合
-------------

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml restart

トラブルシューティング
====================

起動しない場合
------------

1. **OpenSearch が起動しているか確認**

   ::

       $ curl http://localhost:9200/

   OpenSearch が起動していない場合、まず OpenSearch を起動してください。

2. **ポート番号の競合を確認**

   ::

       $ sudo netstat -tuln | grep 8080

   ポート 8080 が既に使用されている場合、設定ファイルでポート番号を変更してください。

3. **ログを確認**

   エラーメッセージを確認して、問題を特定します。

4. **Java のバージョンを確認**

   ::

       $ java -version

   Java 21 以降がインストールされていることを確認してください。

詳細なトラブルシューティングについては、:doc:`troubleshooting` を参照してください。

次のステップ
==========

|Fess| が正常に起動したら、以下のドキュメントを参照して運用を開始してください：

- **管理者ガイド**: クロール設定、検索設定、システム設定の詳細
- :doc:`security` - 本番環境でのセキュリティ設定
- :doc:`troubleshooting` - よくある問題と解決方法
- :doc:`upgrade` - バージョンアップ手順
- :doc:`uninstall` - アンインストール手順

