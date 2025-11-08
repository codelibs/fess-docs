====================
アップグレード手順
====================

このページでは、 |Fess| を以前のバージョンから最新版にアップグレードする手順について説明します。

.. warning::

   **アップグレード前の重要な注意事項**

   - アップグレード前に必ずバックアップを取得してください
   - テスト環境で事前にアップグレードを検証することを強く推奨します
   - アップグレード中はサービスが停止するため、適切なメンテナンス時間を設定してください
   - バージョンによっては、設定ファイルの形式が変更されている場合があります

対応バージョン
============

このアップグレード手順は、以下のバージョン間のアップグレードに対応しています：

- Fess 14.x → Fess 15.3
- Fess 15.x → Fess 15.3

.. note::

   さらに古いバージョン（13.x 以前）からアップグレードする場合は、段階的なアップグレードが必要な場合があります。
   詳細はリリースノートを確認してください。

アップグレード前の準備
====================

バージョン互換性の確認
--------------------

アップグレード先のバージョンと現在のバージョンの互換性を確認してください。

- `リリースノート <https://github.com/codelibs/fess/releases>`__
- `アップグレードガイド <https://fess.codelibs.org/ja/>`__

ダウンタイムの計画
----------------

アップグレード作業には、システムの停止が必要です。以下を考慮してダウンタイムを計画してください：

- バックアップ時間: 10分 〜 数時間（データ量による）
- アップグレード時間: 10 〜 30分
- 動作確認時間: 30分 〜 1時間
- 予備時間: 30分

**推奨メンテナンス時間**: 合計 2 〜 4時間

ステップ 1: データのバックアップ
==============================

アップグレード前に、すべてのデータをバックアップしてください。

設定データのバックアップ
----------------------

1. **管理画面からのバックアップ**

   管理画面にログインし、「システム」→「バックアップ」をクリックします。

   以下のファイルをダウンロード：

   - ``fess_basic_config.bulk``
   - ``fess_user.bulk``

2. **設定ファイルのバックアップ**

   TAR.GZ/ZIP 版::

       $ cp /path/to/fess/app/WEB-INF/conf/system.properties /backup/
       $ cp /path/to/fess/app/WEB-INF/classes/fess_config.properties /backup/

   RPM/DEB 版::

       $ sudo cp /etc/fess/system.properties /backup/
       $ sudo cp /etc/fess/fess_config.properties /backup/

3. **カスタマイズした設定ファイル**

   カスタマイズした設定ファイルがある場合、それらもバックアップします::

       $ cp /path/to/fess/app/WEB-INF/classes/log4j2.xml /backup/

インデックスデータのバックアップ
------------------------------

OpenSearch のインデックスデータをバックアップします。

方法 1: スナップショット機能を使用（推奨）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OpenSearch のスナップショット機能を使用して、インデックスをバックアップします。

1. リポジトリの設定::

       $ curl -X PUT "http://localhost:9200/_snapshot/fess_backup" -H 'Content-Type: application/json' -d'
       {
         "type": "fs",
         "settings": {
           "location": "/backup/opensearch/snapshots"
         }
       }'

2. スナップショットの作成::

       $ curl -X PUT "http://localhost:9200/_snapshot/fess_backup/snapshot_1?wait_for_completion=true"

3. スナップショットの確認::

       $ curl -X GET "http://localhost:9200/_snapshot/fess_backup/snapshot_1"

方法 2: ディレクトリごとバックアップ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OpenSearch を停止してから、データディレクトリをバックアップします。

::

    $ sudo systemctl stop opensearch
    $ sudo tar czf /backup/opensearch-data-$(date +%Y%m%d).tar.gz /var/lib/opensearch/data
    $ sudo systemctl start opensearch

Docker 版のバックアップ
---------------------

Docker ボリュームをバックアップします::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop
    $ docker run --rm -v fess-es-data:/data -v $(pwd):/backup ubuntu tar czf /backup/fess-es-data-backup.tar.gz /data
    $ docker run --rm -v fess-data:/data -v $(pwd):/backup ubuntu tar czf /backup/fess-data-backup.tar.gz /data
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml start

ステップ 2: 現在のバージョンの停止
================================

Fess と OpenSearch を停止します。

TAR.GZ/ZIP 版::

    $ kill <fess_pid>
    $ kill <opensearch_pid>

RPM/DEB 版 (systemd)::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Docker 版::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

ステップ 3: 新しいバージョンのインストール
======================================

インストール方法により、手順が異なります。

TAR.GZ/ZIP 版
-----------

1. 新しいバージョンをダウンロードして展開::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.3.2/fess-15.3.2.tar.gz
       $ tar -xzf fess-15.3.2.tar.gz

2. 古いバージョンの設定をコピー::

       $ cp /path/to/old-fess/app/WEB-INF/conf/system.properties /path/to/fess-15.3.2/app/WEB-INF/conf/
       $ cp /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.3.2/bin/

3. 設定差分を確認し、必要に応じて調整します

RPM/DEB 版
--------

新しいバージョンのパッケージをインストール::

    # RPM
    $ sudo rpm -Uvh fess-15.3.2.rpm

    # DEB
    $ sudo dpkg -i fess-15.3.2.deb

.. note::

   設定ファイル（``/etc/fess/*``）は自動的に保持されます。
   ただし、新しい設定オプションが追加されている場合は、手動で調整が必要です。

Docker 版
-------

1. 新しいバージョンの Compose ファイルを取得::

       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.3.2/compose/compose.yaml
       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.3.2/compose/compose-opensearch3.yaml

2. 新しいイメージを取得::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

ステップ 4: OpenSearch のアップグレード（必要な場合）
=================================================

OpenSearch もアップグレードする場合は、以下の手順に従ってください。

.. warning::

   OpenSearch のメジャーバージョンアップグレードは慎重に行ってください。
   インデックスの互換性に問題が発生する可能性があります。

1. 新しいバージョンの OpenSearch をインストール

2. プラグインを再インストール::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.2

3. OpenSearch を起動::

       $ sudo systemctl start opensearch.service

ステップ 5: 新しいバージョンの起動
================================

TAR.GZ/ZIP 版::

    $ cd /path/to/fess-15.3.2
    $ ./bin/fess -d

RPM/DEB 版::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

Docker 版::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

ステップ 6: 動作確認
==================

1. **ログの確認**

   エラーがないことを確認します::

       $ tail -f /path/to/fess/logs/fess.log

2. **Web インターフェースへのアクセス**

   ブラウザーで http://localhost:8080/ にアクセスします。

3. **管理画面へのログイン**

   http://localhost:8080/admin にアクセスし、管理者アカウントでログインします。

4. **システム情報の確認**

   管理画面で「システム」→「システム情報」をクリックし、バージョンが更新されていることを確認します。

5. **検索の動作確認**

   検索画面で検索を実行し、正常に結果が返されることを確認します。

ステップ 7: インデックスの再作成（推奨）
====================================

メジャーバージョンアップの場合、インデックスを再作成することを推奨します。

1. 既存のクロールスケジュールを確認
2. 「システム」→「スケジューラー」から「Default Crawler」を実行
3. クロールが完了するまで待機
4. 検索結果を確認

ロールバック手順
==============

アップグレードに失敗した場合、以下の手順でロールバックできます。

ステップ 1: 新しいバージョンの停止
------------------------------

::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

ステップ 2: 古いバージョンの復元
----------------------------

バックアップから設定ファイルとデータを復元します。

RPM/DEB 版の場合::

    $ sudo rpm -Uvh --oldpackage fess-<old-version>.rpm

または::

    $ sudo dpkg -i fess-<old-version>.deb

ステップ 3: データの復元
----------------------

スナップショットから復元::

    $ curl -X POST "http://localhost:9200/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true"

または、バックアップからディレクトリを復元::

    $ sudo systemctl stop opensearch
    $ sudo rm -rf /var/lib/opensearch/data/*
    $ sudo tar xzf /backup/opensearch-data-backup.tar.gz -C /
    $ sudo systemctl start opensearch

ステップ 4: サービスの起動と確認
----------------------------

::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

動作を確認し、正常に戻ったことを確認します。

よくある質問
==========

Q: ダウンタイムなしでアップグレードできますか？
--------------------------------------------

A: Fess のアップグレードには、サービスの停止が必要です。ダウンタイムを最小限にするには、以下を検討してください：

- 事前にテスト環境で手順を確認する
- バックアップを事前に取得しておく
- メンテナンス時間を十分に確保する

Q: OpenSearch もアップグレードする必要がありますか？
-------------------------------------------------

A: Fess のバージョンによっては、特定のバージョンの OpenSearch が必要です。
リリースノートで推奨される OpenSearch のバージョンを確認してください。

Q: インデックスを再作成する必要がありますか？
------------------------------------------

A: マイナーバージョンアップの場合は通常不要ですが、メジャーバージョンアップの場合は再作成を推奨します。

Q: アップグレード後、検索結果が表示されません
------------------------------------------

A: 以下を確認してください：

1. OpenSearch が起動しているか確認
2. インデックスが存在するか確認（``curl http://localhost:9200/_cat/indices``）
3. クロールを再実行

次のステップ
==========

アップグレードが完了したら：

- :doc:`run` - 起動と初期設定の確認
- :doc:`security` - セキュリティ設定の見直し
- リリースノートで新機能を確認

