==================
インデックスの管理
==================

概要
====

|Fess| で扱うデータは OpenSearch のインデックスとして管理されています。
検索インデックスのバックアップとリストアは、システムの安定運用に不可欠です。
本セクションでは、インデックスのバックアップ、リストア、および移行手順について説明します。

インデックスの構成
==================

|Fess| では、以下のインデックスが使用されています。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - インデックス名
     - 説明
   * - ``fess.{日付}``
     - 検索対象ドキュメントのインデックス(日次で作成)
   * - ``fess_log``
     - 検索ログとクリックログ
   * - ``fess_user``
     - ユーザー情報
   * - ``fess_config``
     - システム設定情報
   * - ``configsync``
     - 設定の同期情報

インデックスのバックアップとリストア
====================================

OpenSearch のスナップショット機能を使用して、インデックスのバックアップとリストアを実行できます。

スナップショットリポジトリの設定
--------------------------------

まず、バックアップデータを保存するリポジトリを設定します。

**ファイルシステムリポジトリの場合:**

1. OpenSearch の設定ファイル (``config/opensearch.yml``) にリポジトリのパスを追加します。

::

    path.repo: ["/var/opensearch/backup"]

2. OpenSearch を再起動します。

3. リポジトリを登録します。

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup" -H 'Content-Type: application/json' -d'
    {
      "type": "fs",
      "settings": {
        "location": "/var/opensearch/backup",
        "compress": true
      }
    }'

.. note::
   |Fess| のデフォルト設定では、OpenSearch は 9201 ポートで起動しています。

**AWS S3リポジトリの場合:**

S3をバックアップ先とする場合は、``repository-s3`` プラグインをインストールして設定します。

::

    curl -X PUT "localhost:9201/_snapshot/fess_s3_backup" -H 'Content-Type: application/json' -d'
    {
      "type": "s3",
      "settings": {
        "bucket": "my-fess-backup-bucket",
        "region": "ap-northeast-1",
        "base_path": "fess-snapshots"
      }
    }'

スナップショットの作成(バックアップ)
------------------------------------

全インデックスのバックアップ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

すべてのインデックスをバックアップします。

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_1?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

特定のインデックスのバックアップ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

特定のインデックスのみをバックアップします。

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_fess_only?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.*,fess_config",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

定期的な自動バックアップ
~~~~~~~~~~~~~~~~~~~~~~~~

cronなどを使用して、定期的にバックアップを実行できます。

::

    #!/bin/bash
    DATE=$(date +%Y%m%d_%H%M%S)
    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_${DATE}?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

スナップショットの確認
----------------------

作成されたスナップショットの一覧を確認します。

::

    curl -X GET "localhost:9201/_snapshot/fess_backup/_all?pretty"

特定のスナップショットの詳細を確認します。

::

    curl -X GET "localhost:9201/_snapshot/fess_backup/snapshot_1?pretty"

スナップショットからのリストア
------------------------------

全インデックスのリストア
~~~~~~~~~~~~~~~~~~~~~~~~

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

特定のインデックスのリストア
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

インデックス名を変更してリストア
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

リストア時にインデックス名を変更することもできます。

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101",
      "rename_pattern": "fess.(.+)",
      "rename_replacement": "restored_fess.$1",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

スナップショットの削除
----------------------

古いスナップショットを削除して、ストレージ容量を節約できます。

::

    curl -X DELETE "localhost:9201/_snapshot/fess_backup/snapshot_1"

設定ファイルのバックアップ
==========================

OpenSearch のインデックスとは別に、以下の設定ファイルもバックアップしてください。

バックアップ対象のファイル
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - ファイル/ディレクトリ
     - 説明
   * - ``app/WEB-INF/conf/system.properties``
     - システム設定(zipインストールの場合)
   * - ``/etc/fess/system.properties``
     - システム設定(RPM/DEBパッケージの場合)
   * - ``app/WEB-INF/classes/fess_config.properties``
     - Fess の詳細設定
   * - ``/etc/fess/fess_config.properties``
     - Fess の詳細設定(RPM/DEBパッケージ)
   * - ``app/WEB-INF/classes/log4j2.xml``
     - ログ設定
   * - ``/etc/fess/log4j2.xml``
     - ログ設定(RPM/DEBパッケージ)
   * - ``app/WEB-INF/classes/fess_indices/``
     - インデックス定義ファイル
   * - ``thumbnail/``
     - サムネイル画像(必要に応じて)

設定ファイルのバックアップ例
----------------------------

::

    #!/bin/bash
    BACKUP_DIR="/backup/fess/$(date +%Y%m%d_%H%M%S)"
    mkdir -p ${BACKUP_DIR}

    # 設定ファイルのコピー
    cp -r /etc/fess/ ${BACKUP_DIR}/
    cp -r /var/lib/fess/app/WEB-INF/conf/ ${BACKUP_DIR}/
    cp -r /var/lib/fess/app/WEB-INF/classes/fess_indices/ ${BACKUP_DIR}/

    # オプション: サムネイル画像
    # cp -r /var/lib/fess/thumbnail/ ${BACKUP_DIR}/

    echo "Backup completed: ${BACKUP_DIR}"

データ移行
==========

別環境への移行手順
------------------

1. **移行元でのバックアップ作成**

   - OpenSearch のスナップショットを作成します。
   - 設定ファイルをバックアップします。

2. **移行先の準備**

   - |Fess| を新しい環境にインストールします。
   - OpenSearch を起動します。

3. **設定ファイルのリストア**

   - バックアップした設定ファイルを新しい環境にコピーします。
   - 必要に応じて、パスやホスト名などを修正します。

4. **インデックスのリストア**

   - スナップショットリポジトリを設定します。
   - スナップショットからインデックスをリストアします。

5. **動作確認**

   - |Fess| を起動します。
   - 管理画面にアクセスし、設定を確認します。
   - 検索機能が正常に動作するか確認します。

バージョンアップ時の注意事項
----------------------------

異なるバージョンの |Fess| 間でデータを移行する場合は、以下の点に注意してください。

- OpenSearch のメジャーバージョンが異なる場合、互換性の問題が発生する可能性があります。
- インデックスの構造が変更されている場合、再インデックスが必要になることがあります。
- 詳細は、各バージョンのアップグレードガイドを参照してください。

トラブルシューティング
======================

スナップショットの作成に失敗する
--------------------------------

1. リポジトリのパスに対する権限を確認してください。
2. ディスク容量が十分か確認してください。
3. OpenSearch のログファイルでエラーメッセージを確認してください。

リストアに失敗する
------------------

1. 同名のインデックスが既に存在していないか確認してください。
2. OpenSearch のバージョンが互換性のあるものか確認してください。
3. スナップショットが破損していないか確認してください。

リストア後に検索できない
------------------------

1. インデックスが正常にリストアされたか確認してください: ``curl -X GET "localhost:9201/_cat/indices?v"``
2. |Fess| のログファイルでエラーがないか確認してください。
3. 設定ファイルが正しくリストアされているか確認してください。

参考情報
========

詳細な情報は、OpenSearch の公式ドキュメントを参照してください。

- `スナップショット機能 <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/index/>`_
- `リポジトリ設定 <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/>`_
- `S3リポジトリ <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/plugins/#s3-repository>`_
