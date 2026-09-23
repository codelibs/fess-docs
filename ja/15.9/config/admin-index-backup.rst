==================
インデックスの管理
==================

概要
====

|Fess| で扱うデータは OpenSearch のインデックスとして管理されています。
検索インデックスのバックアップとリストアは、システムの安定運用に不可欠です。
本セクションでは、OpenSearch のスナップショット機能を使用したインデックスのバックアップ、リストア、および移行手順について説明します。

.. note::
   |Fess| には、本セクションで説明する OpenSearch スナップショットによるインデックスのバックアップとは別に、管理画面から設定情報（クロール設定、ユーザー情報、システム設定など）をエクスポート/インポートする機能もあります。設定情報のみをバックアップまたは移行したい場合は :doc:`../admin/backup-guide` を参照してください。OpenSearch のスナップショットは、検索ドキュメントを含むインデックス全体を物理的にバックアップする用途に適しています。

インデックスの構成
==================

|Fess| では、以下のインデックスが使用されています。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - インデックス名
     - 説明
   * - ``fess.{タイムスタンプ}``
     - 検索対象ドキュメントのインデックス。インデックス再構築時に ``fess.{yyyyMMddHHmmssSSS}`` 形式（ミリ秒精度のタイムスタンプ）で作成され、 ``fess.search`` （検索用）および ``fess.update`` （更新用）エイリアスで参照されます。
   * - ``fess_config.*``
     - システム設定情報（ ``fess_config.web_config`` 、 ``fess_config.scheduled_job`` 、 ``fess_config.data_config`` など複数のサブインデックスで構成）
   * - ``fess_user.*``
     - ユーザー情報（ ``fess_user.user`` 、 ``fess_user.role`` 、 ``fess_user.group`` ）
   * - ``fess_log.*``
     - 検索ログやクリックログなど（ ``fess_log.search_log`` 、 ``fess_log.click_log`` 、 ``fess_log.favorite_log`` 、 ``fess_log.user_info`` 、 ``fess_log.notification_queue`` ）
   * - ``fess_crawler.*``
     - クロール処理中に使用される一時インデックス（ ``fess_crawler.queue`` 、 ``fess_crawler.data`` 、 ``fess_crawler.filter`` ）。クロール完了後は不要なため、通常はバックアップ対象に含める必要はありません。
   * - ``configsync``
     - 辞書ファイル（同義語、ストップワード、マッピングなど）の内容。OpenSearch の configsync プラグインが管理し、OpenSearch の ``config/dictionary`` 配下のファイルへ書き出します。検索対象ドキュメントのインデックスやサジェスト用のインデックスはこれらのファイルを参照しているため、必ずバックアップ対象に含めてください。

.. warning::
   スナップショットに含まれるのはインデックスだけで、OpenSearch の ``config/dictionary`` 配下の辞書ファイルそのものは含まれません。
   ``configsync`` インデックスをバックアップしていないと、新しい OpenSearch へリストアしたときに辞書ファイルが存在せず、 ``fess.{タイムスタンプ}`` と ``fess_suggest_analyzer`` が ``IOException while reading ..._path: file not readable`` で開けません（クラスタの状態が red になります）。

インデックスのバックアップとリストア
====================================

OpenSearch のスナップショット機能を使用して、インデックスのバックアップとリストアを実行できます。

スナップショットリポジトリの設定
--------------------------------

まず、バックアップデータを保存するリポジトリを設定します。

**ファイルシステムリポジトリの場合:**

1. OpenSearch の設定ファイル (``opensearch.yml``) にリポジトリのパスを追加します。

::

    path.repo: ["/var/opensearch/backup"]

2. OpenSearch を再起動します。

3. リポジトリを登録します。

::

    curl -X PUT "localhost:9200/_snapshot/fess_backup" -H 'Content-Type: application/json' -d'
    {
      "type": "fs",
      "settings": {
        "location": "/var/opensearch/backup",
        "compress": true
      }
    }'

.. note::
   |Fess| は既定で 9200 ポートの OpenSearch に接続します（ZIP 版は ``bin/fess.in.sh`` の ``SEARCH_ENGINE_HTTP_URL`` 、RPM/DEB 版は環境設定ファイル ``/etc/sysconfig/fess`` （RPM）または ``/etc/default/fess`` （DEB））。別のポートで OpenSearch を稼働させている場合は、ポート番号を読み替えてください。

**AWS S3リポジトリの場合:**

S3をバックアップ先とする場合は、``repository-s3`` プラグインをインストールして設定します。

::

    curl -X PUT "localhost:9200/_snapshot/fess_s3_backup" -H 'Content-Type: application/json' -d'
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

    curl -X PUT "localhost:9200/_snapshot/fess_backup/snapshot_1?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

特定のインデックスのバックアップ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

特定のインデックスのみをバックアップします。以下は、|Fess| 関連のインデックス（ ``fess`` で始まるインデックス）と、辞書ファイルを保持する ``configsync`` インデックスを対象とする例です。 ``configsync`` を省くと、辞書ファイルを復元できません。

::

    curl -X PUT "localhost:9200/_snapshot/fess_backup/snapshot_fess_only?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess*,configsync",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

定期的な自動バックアップ
~~~~~~~~~~~~~~~~~~~~~~~~

cronなどを使用して、定期的にバックアップを実行できます。

::

    #!/bin/bash
    DATE=$(date +%Y%m%d_%H%M%S)
    curl -X PUT "localhost:9200/_snapshot/fess_backup/snapshot_${DATE}?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

スナップショットの確認
----------------------

作成されたスナップショットの一覧を確認します。

::

    curl -X GET "localhost:9200/_snapshot/fess_backup/_all?pretty"

特定のスナップショットの詳細を確認します。

::

    curl -X GET "localhost:9200/_snapshot/fess_backup/snapshot_1?pretty"

スナップショットからのリストア
------------------------------

全インデックスのリストア
~~~~~~~~~~~~~~~~~~~~~~~~

先に ``configsync`` インデックスをリストアして辞書ファイルを書き出し、その後で |Fess| のインデックス（ ``fess*`` ）をリストアします。リストアは |Fess| を停止した状態で実行してください。

``"indices": "*"`` で一度にリストアすることはできません。OpenSearch は起動時に ``configsync`` などのインデックスを自身で作成するため、新しい OpenSearch に対しても ``cannot restore index [configsync] because an open index with same name already exists in the cluster`` で失敗します。
また、 ``fess*`` だけをリストアすると辞書ファイルが存在しないため、 ``fess.{タイムスタンプ}`` と ``fess_suggest_analyzer`` が開けずクラスタが red になり、そのまま |Fess| を起動しても起動に失敗します（すべてのページが 404 になります）。

1. configsync プラグインが起動時に作成した空の ``configsync`` インデックスを削除し、スナップショットから ``configsync`` をリストアします。

::

    curl -X DELETE "localhost:9200/configsync"

    curl -X POST "localhost:9200/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "configsync",
      "include_global_state": false
    }'

2. リストアした辞書の内容を OpenSearch の ``config/dictionary`` 配下へ書き出します。

::

    curl -X POST "localhost:9200/_configsync/flush"

3. |Fess| のインデックスをリストアします。

::

    curl -X POST "localhost:9200/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

4. クラスタの状態が ``green`` （レプリカを割り当てられない構成では ``yellow`` ）になったことを確認してから、 |Fess| を起動します。

::

    curl -X GET "localhost:9200/_cluster/health?wait_for_status=yellow&timeout=60s&pretty"

.. note::
   稼働中のクラスタへ同じ名前のままリストアし直す場合は、リストアするインデックスがオープン状態だと失敗します。手順 3 の前に、対象のインデックスをクローズ（ ``_close`` ）してください。

特定のインデックスのリストア
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

検索対象ドキュメントのインデックスは ``fess.{yyyyMMddHHmmssSSS}`` 形式の名前になります。\ ``_cat/indices`` などで実際のインデックス名を確認してからリストアしてください。

::

    curl -X POST "localhost:9200/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101000000000",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

インデックス名を変更してリストア
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

リストア時にインデックス名を変更することもできます。

::

    curl -X POST "localhost:9200/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101000000000",
      "rename_pattern": "fess\\.(.+)",
      "rename_replacement": "restored_fess.$1",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

.. note::
   検索対象ドキュメントのインデックス（ ``fess.{タイムスタンプ}`` ）をリストアした場合、 ``fess.search`` および ``fess.update`` エイリアスがリストアしたインデックスを指しているかを必ず確認してください。スナップショットにはエイリアス情報も含まれるため、全インデックスをそのままの名前でリストアした場合は通常エイリアスも復元されます。ただし、 ``rename_pattern`` でインデックス名を変更してリストアした場合や、別クラスタへ移行した場合は、エイリアスが正しく設定されないことがあります。その場合は、以下のようにエイリアスを手動で再設定してください（インデックス名は実際のものに置き換えてください）。

   ::

       curl -X POST "localhost:9200/_aliases" -H 'Content-Type: application/json' -d'
       {
         "actions": [
           { "add": { "index": "restored_fess.20250101000000000", "alias": "fess.search" } },
           { "add": { "index": "restored_fess.20250101000000000", "alias": "fess.update" } }
         ]
       }'

スナップショットの削除
----------------------

古いスナップショットを削除して、ストレージ容量を節約できます。

::

    curl -X DELETE "localhost:9200/_snapshot/fess_backup/snapshot_1"

設定ファイルのバックアップ
==========================

OpenSearch のインデックスとは別に、以下の設定ファイルもバックアップしてください。設定ファイルの配置場所はインストール方法によって異なります。

バックアップ対象のファイル
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - ファイル/ディレクトリ
     - インストール方法
     - 説明
   * - ``app/WEB-INF/conf/system.properties``
     - ZIP
     - システム設定（全般設定）
   * - ``/etc/fess/system.properties``
     - RPM/DEB
     - システム設定（全般設定）
   * - ``app/WEB-INF/classes/fess_config.properties``
     - ZIP
     - |Fess| の詳細設定
   * - ``/etc/fess/fess_config.properties``
     - RPM/DEB
     - |Fess| の詳細設定
   * - ``app/WEB-INF/classes/log4j2.xml``
     - ZIP
     - ログ設定
   * - ``/usr/share/fess/app/WEB-INF/classes/log4j2.xml``
     - RPM/DEB
     - ログ設定
   * - ``app/WEB-INF/classes/fess_indices/``
     - ZIP
     - インデックス定義ファイル
   * - ``/usr/share/fess/app/WEB-INF/classes/fess_indices/``
     - RPM/DEB
     - インデックス定義ファイル
   * - ``app/WEB-INF/thumbnails/``
     - ZIP
     - サムネイル画像（必要に応じて）
   * - ``/var/lib/fess/thumbnails/``
     - RPM/DEB
     - サムネイル画像（必要に応じて）

.. note::
   RPM/DEB パッケージ版では、 ``/etc/fess/`` ディレクトリに ``fess_config.properties`` のほか、 ``fess_env_crawler.properties`` などの ``fess_env_*.properties`` や ``tika.xml`` といった設定ファイルも格納されています。\ ``/etc/fess/`` ディレクトリ全体をバックアップすることを推奨します。\ ``system.properties`` は、管理画面の「システム > 全般」で設定を保存した際に ``/etc/fess/system.properties`` として作成・更新されます。

設定ファイルのバックアップ例
----------------------------

以下は RPM/DEB パッケージ版での設定ファイルのバックアップ例です。

::

    #!/bin/bash
    BACKUP_DIR="/backup/fess/$(date +%Y%m%d_%H%M%S)"
    mkdir -p ${BACKUP_DIR}

    # 設定ファイルのコピー（system.properties や fess_config.properties などを含む）
    cp -r /etc/fess/ ${BACKUP_DIR}/

    # インデックス定義ファイルとログ設定
    cp -r /usr/share/fess/app/WEB-INF/classes/fess_indices/ ${BACKUP_DIR}/
    cp /usr/share/fess/app/WEB-INF/classes/log4j2.xml ${BACKUP_DIR}/

    # オプション: サムネイル画像
    # cp -r /var/lib/fess/thumbnails/ ${BACKUP_DIR}/

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
   - 「全インデックスのリストア」の手順に従い、 ``configsync`` をリストアして辞書ファイルを書き出してから、 |Fess| のインデックスをリストアします。
   - リストア後、 ``fess.search`` および ``fess.update`` エイリアスがリストアしたインデックスを指しているか確認します。
   - クラスタの状態が ``green`` （または ``yellow`` ）であることを確認します。 ``red`` のまま |Fess| を起動すると、 |Fess| は起動に失敗します。

5. **動作確認**

   - |Fess| を起動します。
   - 管理画面にアクセスし、設定を確認します。
   - 検索機能が正常に動作するか確認します。

バージョンアップ時の注意事項
----------------------------

異なるバージョンの |Fess| 間でデータを移行する場合は、以下の点に注意してください。

- OpenSearch のメジャーバージョンが異なる場合、互換性の問題が発生する可能性があります。
- インデックスの構造が変更されている場合、再インデックスが必要になることがあります。
- インデックス構造の変更をまたいで設定情報を移行したい場合は、OpenSearch スナップショットではなく、管理画面のバックアップ機能（ :doc:`../admin/backup-guide` ）による論理的なエクスポート/インポートの利用を検討してください。
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

1. 同名のインデックスが既に存在していないか確認してください。OpenSearch では、オープン状態の同名インデックスへはリストアできません。リストア前に対象のインデックスをクローズ（ ``_close`` ）または削除するか、 ``rename_pattern`` で別名にリストアしてください。
2. OpenSearch のバージョンが互換性のあるものか確認してください。
3. スナップショットが破損していないか確認してください。

リストア後にクラスタが red になる
---------------------------------

``fess*`` をリストアした後にクラスタの状態が ``red`` になり、次のような状態になる場合は、辞書ファイルがありません。

- ``_cluster/allocation/explain`` に ``IOException while reading mappings_path: file not readable`` （ ``keywords_path`` などの場合もあります）が出ている
- |Fess| を起動すると ``fess.log`` に ``Failed to initialize Lasta Di`` （ ``SuggestHelper`` の ``init`` での ``NullPointerException`` ）が出て、すべてのページが 404 になる

``_cluster/reroute?retry_failed=true`` を実行しても、また辞書ファイルを配置しただけでも回復しません。リストアに失敗したシャードは、そのインデックスをクローズまたは削除して、もう一度リストアするまで割り当てられないためです。次の手順で回復します。

1. 「全インデックスのリストア」の手順 1 と 2 に従い、 ``configsync`` をリストアして辞書ファイルを書き出します。
2. ``red`` のインデックスを確認します。

   ::

       curl -X GET "localhost:9200/_cat/indices?v&health=red"

3. ``red`` のインデックスをクローズし、スナップショットからもう一度リストアします（インデックス名は実際のものに置き換えてください）。

   ::

       curl -X POST "localhost:9200/fess.20250101000000000,fess_suggest_analyzer/_close"

       curl -X POST "localhost:9200/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
       {
         "indices": "fess.20250101000000000,fess_suggest_analyzer",
         "include_global_state": false
       }'

リストア後に検索できない
------------------------

1. インデックスが正常にリストアされたか確認してください: ``curl -X GET "localhost:9200/_cat/indices?v"``
2. ``fess.search`` および ``fess.update`` エイリアスがリストアしたインデックスを指しているか確認してください: ``curl -X GET "localhost:9200/_cat/aliases?v"`` 。エイリアスが設定されていない場合は、 ``_aliases`` API で再設定してください。
3. |Fess| のログファイルでエラーがないか確認してください。
4. 設定ファイルが正しくリストアされているか確認してください。

関連トピック
============

- :doc:`../admin/backup-guide` - 管理画面からの設定情報のバックアップ/リストア
- :doc:`admin-index-export` - インデックスのエクスポート機能
- :doc:`admin-logging` - ログ設定

参考情報
========

詳細な情報は、OpenSearch の公式ドキュメントを参照してください。

- `スナップショット機能 <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/index/>`_
- `リポジトリ設定 <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/>`_
- `S3リポジトリ <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/plugins/#s3-repository>`_
