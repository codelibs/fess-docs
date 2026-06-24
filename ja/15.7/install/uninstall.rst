==================
アンインストール手順
==================

このページでは、 |Fess| を完全にアンインストールする手順について説明します。

.. warning::

   **アンインストール前の重要な注意事項**

   - アンインストールすると、すべてのデータが削除されます
   - 重要なデータがある場合は、必ずバックアップを取得してください
   - バックアップ手順については :doc:`upgrade` を参照してください

アンインストール前の準備
======================

バックアップの取得
----------------

必要なデータをバックアップしてください：

1. **設定データ**

   管理画面の「システム」→「バックアップ」からダウンロードします。
   この操作で、各種設定（クロール設定を含む）や検索ログなどをまとめてエクスポートできます。

2. **カスタマイズした設定ファイル**

   TAR.GZ/ZIP 版::

       $ cp -r /path/to/fess/app/WEB-INF/conf /backup/
       $ cp -r /path/to/fess/app/WEB-INF/classes /backup/

   RPM/DEB 版::

       $ sudo cp -r /etc/fess /backup/

.. note::

   |Fess| のインデックスや設定の大部分は OpenSearch に保存されます。
   インデックスデータをバックアップする場合は、OpenSearch のスナップショット機能を使用します。
   詳細な手順は :doc:`upgrade` を参照してください。

サービスの停止
------------

アンインストール前に、すべてのサービスを停止します。

TAR.GZ/ZIP 版::

    $ ps aux | grep -E 'fess|opensearch'
    $ kill <fess_pid>
    $ kill <opensearch_pid>

RPM/DEB 版::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Docker 版::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

TAR.GZ/ZIP 版のアンインストール
=============================

ステップ 1: Fess の削除
---------------------

インストールディレクトリを削除します::

    $ rm -rf /path/to/fess-15.7.0

ステップ 2: OpenSearch の削除
--------------------------

OpenSearch のインストールディレクトリを削除します::

    $ rm -rf /path/to/opensearch-3.7.0

ステップ 3: データディレクトリの削除（オプション）
-------------------------------------------

|Fess| のインデックスデータは OpenSearch に保存されます。
デフォルトでは OpenSearch のインストールディレクトリ内（``opensearch-3.7.0/data`` など）に保存されますが、
``path.data`` で別の場所を指定している場合は、そのディレクトリも削除してください::

    $ rm -rf /path/to/data

ステップ 4: ログディレクトリの削除（オプション）
-----------------------------------------

ログファイルを削除します::

    $ rm -rf /path/to/fess-15.7.0/logs
    $ rm -rf /path/to/opensearch-3.7.0/logs

RPM 版のアンインストール
======================

ステップ 1: Fess のアンインストール
---------------------------------

RPM パッケージをアンインストールします::

    $ sudo rpm -e fess

.. note::

   |Fess| パッケージのアンインストール時には、パッケージの削除スクリプトによって
   ``fess`` サービスの停止・無効化と、``fess`` ユーザーおよびグループの削除が自動的に実行されます。
   以降のステップは、これらが確実に削除されたことを確認するため、または
   データや設定ファイルを手動で削除するために実施します。

ステップ 2: OpenSearch のアンインストール
--------------------------------------

::

    $ sudo rpm -e opensearch

ステップ 3: サービスの無効化の確認
-------------------------------

通常はパッケージ削除時にサービスが無効化されますが、念のため確認・無効化する場合は以下を実行します。

systemd の場合::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

古い SysV init（chkconfig）環境の場合::

    $ sudo /sbin/chkconfig --del fess
    $ sudo /sbin/chkconfig --del opensearch

ステップ 4: データディレクトリの削除
----------------------------------

.. warning::

   この操作を実行すると、すべてのインデックスデータが完全に削除されます。

データディレクトリはパッケージのアンインストールでは削除されないため、手動で削除します::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

ステップ 5: 設定ファイルの削除
----------------------------

設定ファイルと環境設定ファイルを削除します::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/sysconfig/fess
    $ sudo rm -rf /etc/opensearch

.. note::

   RPM では ``/etc/fess`` 内の設定ファイルが ``.rpmsave`` という名前で残る場合があります。
   完全に削除するには、上記のように手動で削除してください。

ステップ 6: ログファイルの削除
----------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

ステップ 7: 一時ディレクトリの削除（オプション）
-----------------------------------------

::

    $ sudo rm -rf /var/tmp/fess

ステップ 8: ユーザーとグループの削除（オプション）
-------------------------------------------

通常はパッケージ削除時に ``fess`` ユーザー・グループは削除されます。
残っている場合や、OpenSearch 用のユーザー・グループを削除する場合は、以下を実行します::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

DEB 版のアンインストール
======================

ステップ 1: Fess のアンインストール
---------------------------------

DEB パッケージをアンインストールします::

    $ sudo dpkg -r fess

設定ファイルや環境設定ファイルも含めて完全に削除する場合は、purge を使用します::

    $ sudo dpkg -P fess

.. note::

   ``dpkg -r``（remove）では、設定ファイル（conffile）である ``/etc/default/fess`` などは残ります。
   ``dpkg -P``（purge）を使用すると、これらの設定ファイルと ``fess`` ユーザー・グループも削除されます。

ステップ 2: OpenSearch のアンインストール
--------------------------------------

::

    $ sudo dpkg -r opensearch

または、設定ファイルも含めて削除::

    $ sudo dpkg -P opensearch

ステップ 3: サービスの無効化の確認
-------------------------------

通常はパッケージ削除時にサービスが無効化されます。念のため確認・無効化する場合は以下を実行します::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

ステップ 4: データディレクトリの削除
----------------------------------

.. warning::

   この操作を実行すると、すべてのインデックスデータが完全に削除されます。

::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

ステップ 5: 設定ファイルの削除（dpkg -P を使用しなかった場合）
---------------------------------------------------------

::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/default/fess
    $ sudo rm -rf /etc/opensearch

ステップ 6: ログファイルの削除
----------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

ステップ 7: ユーザーとグループの削除（オプション）
-------------------------------------------

``dpkg -P`` を使用しなかった場合、``fess`` ユーザー・グループが残ります。
削除する場合は以下を実行します::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

Docker 版のアンインストール
=========================

ステップ 1: コンテナとネットワークの削除
------------------------------------

コンテナ、および Docker Compose が作成したネットワーク（``search_net``）を削除します::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

ステップ 2: ボリュームの削除
--------------------------

.. warning::

   この操作を実行すると、すべてのデータが完全に削除されます。

|Fess| のデータ（インデックスや辞書など）は OpenSearch のボリュームに保存されます。
まず、ボリューム一覧を確認します::

    $ docker volume ls

OpenSearch 関連のボリュームを削除します::

    $ docker volume rm <project>_search01_data
    $ docker volume rm <project>_search01_dictionary

.. note::

   ボリューム名には、Docker Compose のプロジェクト名（通常は Compose ファイルを配置した
   ディレクトリ名）が接頭辞として付きます。``docker volume ls`` で実際の名前を確認してください。

コンテナとボリュームを一括で削除する場合は、``down`` に ``-v`` オプションを付けます::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

ステップ 3: イメージの削除（オプション）
------------------------------------

Docker イメージを削除してディスクスペースを解放する場合::

    $ docker images | grep fess
    $ docker rmi ghcr.io/codelibs/fess:15.7.0
    $ docker rmi ghcr.io/codelibs/fess-opensearch:3.7.0

ステップ 4: Compose ファイルの削除
--------------------------------

::

    $ rm compose.yaml compose-opensearch3.yaml

アンインストールの確認
====================

すべてのコンポーネントが削除されたことを確認します。

プロセスの確認
------------

::

    $ ps aux | grep fess
    $ ps aux | grep opensearch

何も表示されなければ、プロセスは停止しています。

ポートの確認
----------

::

    $ sudo netstat -tuln | grep 8080
    $ sudo netstat -tuln | grep 9200

ポートが使用されていないことを確認します。

ファイルの確認
------------

TAR.GZ/ZIP 版::

    $ ls /path/to/fess-15.7.0  # ディレクトリが存在しないことを確認

RPM/DEB 版::

    $ ls /var/lib/fess  # ディレクトリが存在しないことを確認
    $ ls /etc/fess      # ディレクトリが存在しないことを確認

Docker 版::

    $ docker ps -a | grep -E 'fess01|search01'  # コンテナが存在しないことを確認
    $ docker volume ls | grep search01           # ボリュームが存在しないことを確認

パッケージの確認
--------------

RPM 版::

    $ rpm -qa | grep fess
    $ rpm -qa | grep opensearch

DEB 版::

    $ dpkg -l | grep fess
    $ dpkg -l | grep opensearch

何も表示されなければ、パッケージは削除されています。

部分的なアンインストール
======================

Fess のみを削除して OpenSearch を残す
-----------------------------------

OpenSearch を他のアプリケーションでも使用している場合、Fess のみを削除できます。

1. Fess を停止
2. Fess のパッケージまたはディレクトリを削除
3. Fess のデータディレクトリを削除（``/var/lib/fess`` など）
4. OpenSearch 内に作成された |Fess| のインデックス（``fess.*``、``.fess_*`` など）を削除
5. OpenSearch は削除しない

OpenSearch のみを削除して Fess を残す
-----------------------------------

.. warning::

   OpenSearch を削除すると、Fess は動作しなくなります。
   別の OpenSearch クラスターに接続するように設定を変更してください。

1. OpenSearch を停止
2. OpenSearch のパッケージまたはディレクトリを削除
3. OpenSearch のデータディレクトリを削除（``/var/lib/opensearch`` など）
4. Fess の設定を更新して、別の OpenSearch クラスターを指定

トラブルシューティング
====================

パッケージが削除できない
----------------------

**症状:**

``rpm -e`` または ``dpkg -r`` でエラーが発生する。

**解決方法:**

1. サービスが停止していることを確認::

       $ sudo systemctl stop fess.service

2. 依存関係を確認::

       $ rpm -qa | grep fess
       $ dpkg -l | grep fess

3. 強制削除（最終手段）::

       $ sudo rpm -e --nodeps fess
       $ sudo dpkg -r --force-all fess

ディレクトリが削除できない
------------------------

**症状:**

``rm -rf`` でディレクトリが削除できない。

**解決方法:**

1. 権限を確認::

       $ ls -ld /path/to/directory

2. sudo で削除::

       $ sudo rm -rf /path/to/directory

3. プロセスがファイルを使用していないか確認::

       $ sudo lsof | grep /path/to/directory

再インストールの準備
==================

アンインストール後に再インストールする場合は、以下を確認してください：

1. すべてのプロセスが停止していること
2. すべてのファイルとディレクトリが削除されていること
3. ポート 8080 および 9200 が使用されていないこと
4. 以前の設定ファイルが残っていないこと

再インストール手順については、:doc:`install` を参照してください。

次のステップ
==========

アンインストールが完了したら：

- 新しいバージョンをインストールする場合は :doc:`install` を参照
- データを移行する場合は :doc:`upgrade` を参照
- 代替の検索ソリューションを検討する場合は、Fess の公式サイトを参照
