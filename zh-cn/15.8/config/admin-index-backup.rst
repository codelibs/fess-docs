==================
索引管理
==================

概述
====

|Fess| 处理的数据作为 OpenSearch 的索引进行管理。
搜索索引的备份与恢复对系统稳定运行不可或缺。
本章节介绍使用 OpenSearch 快照功能进行索引备份、恢复及迁移的操作步骤。

.. note::
   |Fess| 除了本章节介绍的 OpenSearch 快照索引备份之外，还提供通过管理界面导出/导入配置信息（爬取配置、用户信息、系统设置等）的功能。若仅需备份或迁移配置信息，请参考 :doc:`../admin/backup-guide`。OpenSearch 快照适用于对包含搜索文档的完整索引进行物理备份的场景。

索引构成
==================

|Fess| 使用以下索引。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 索引名
     - 说明
   * - ``fess.{时间戳}``
     - 搜索文档索引。重建索引时以 ``fess.{yyyyMMddHHmmssSSS}`` 格式（毫秒精度时间戳）创建，通过 ``fess.search`` （用于搜索）和 ``fess.update`` （用于更新）别名引用。
   * - ``fess_config.*``
     - 系统配置信息（由 ``fess_config.web_config``、``fess_config.scheduled_job``、``fess_config.data_config`` 等多个子索引构成）
   * - ``fess_user.*``
     - 用户信息（``fess_user.user``、``fess_user.role``、``fess_user.group``）
   * - ``fess_log.*``
     - 搜索日志及点击日志等（``fess_log.search_log``、``fess_log.click_log``、``fess_log.favorite_log``、``fess_log.user_info``、``fess_log.notification_queue``）
   * - ``fess_crawler.*``
     - 爬取过程中使用的临时索引（``fess_crawler.queue``、``fess_crawler.data``、``fess_crawler.filter``）。爬取完成后不再需要，通常无需纳入备份范围。

索引备份与恢复
====================================

可以使用 OpenSearch 的快照功能执行索引的备份与恢复。

快照仓库配置
--------------------------------

首先，配置用于保存备份数据的仓库。

**文件系统仓库:**

1. 在 OpenSearch 配置文件 (``opensearch.yml``) 中添加仓库路径。

::

    path.repo: ["/var/opensearch/backup"]

2. 重启 OpenSearch。

3. 注册仓库。

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
   |Fess| zip/tar.gz 版的默认配置中，OpenSearch 在 9201 端口启动（``fess_config.properties`` 的 ``search_engine.http.url``）。RPM/DEB 软件包版默认配置为连接 9200 端口（环境配置文件 ``/etc/sysconfig/fess`` （RPM）或 ``/etc/default/fess`` （DEB）中的 ``SEARCH_ENGINE_HTTP_URL``）。请根据您的实际环境替换相应的端口号。

**AWS S3仓库:**

将 S3 作为备份目标时，请安装并配置 ``repository-s3`` 插件。

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

创建快照（备份）
------------------------------------

备份所有索引
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

备份所有索引。

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_1?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

备份特定索引
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

仅备份特定索引。以下是仅针对 |Fess| 相关索引（以 ``fess`` 开头的索引）的示例。

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_fess_only?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

定期自动备份
~~~~~~~~~~~~~~~~~~~~~~~~

可以使用 cron 等方式定期执行备份。

::

    #!/bin/bash
    DATE=$(date +%Y%m%d_%H%M%S)
    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_${DATE}?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

确认快照
----------------------

确认已创建的快照列表。

::

    curl -X GET "localhost:9201/_snapshot/fess_backup/_all?pretty"

确认特定快照的详情。

::

    curl -X GET "localhost:9201/_snapshot/fess_backup/snapshot_1?pretty"

从快照恢复
------------------------------

恢复所有索引
~~~~~~~~~~~~~~~~~~~~~~~~

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

恢复特定索引
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

搜索文档索引的名称格式为 ``fess.{yyyyMMddHHmmssSSS}``。请通过 ``_cat/indices`` 等方式确认实际索引名后再执行恢复。

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101000000000",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

更改索引名恢复
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

恢复时也可以更改索引名。

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101000000000",
      "rename_pattern": "fess\\.(.+)",
      "rename_replacement": "restored_fess.$1",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

.. note::
   恢复搜索文档索引（``fess.{时间戳}``）后，请务必确认 ``fess.search`` 和 ``fess.update`` 别名是否指向已恢复的索引。快照中包含别名信息，因此以原名称恢复全部索引时，别名通常也会一并还原。但是，若使用 ``rename_pattern`` 更改索引名恢复，或迁移至其他集群时，别名可能无法正确设置。此时请按如下方式手动重新设置别名（请将索引名替换为实际名称）。

   ::

       curl -X POST "localhost:9201/_aliases" -H 'Content-Type: application/json' -d'
       {
         "actions": [
           { "add": { "index": "restored_fess.20250101000000000", "alias": "fess.search" } },
           { "add": { "index": "restored_fess.20250101000000000", "alias": "fess.update" } }
         ]
       }'

删除快照
----------------------

可以删除旧快照以节省存储容量。

::

    curl -X DELETE "localhost:9201/_snapshot/fess_backup/snapshot_1"

配置文件备份
==========================

除 OpenSearch 索引外，还请备份以下配置文件。配置文件的存放位置因安装方式不同而有所差异。

备份对象文件
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - 文件/目录
     - 安装方式
     - 说明
   * - ``app/WEB-INF/conf/system.properties``
     - zip/tar.gz
     - 系统设置（通用设置）
   * - ``/etc/fess/system.properties``
     - RPM/DEB
     - 系统设置（通用设置）
   * - ``app/WEB-INF/classes/fess_config.properties``
     - zip/tar.gz
     - |Fess| 详细配置
   * - ``/etc/fess/fess_config.properties``
     - RPM/DEB
     - |Fess| 详细配置
   * - ``app/WEB-INF/classes/log4j2.xml``
     - zip/tar.gz
     - 日志配置
   * - ``/usr/share/fess/app/WEB-INF/classes/log4j2.xml``
     - RPM/DEB
     - 日志配置
   * - ``app/WEB-INF/classes/fess_indices/``
     - zip/tar.gz
     - 索引定义文件
   * - ``/usr/share/fess/app/WEB-INF/classes/fess_indices/``
     - RPM/DEB
     - 索引定义文件
   * - ``app/WEB-INF/thumbnails/``
     - zip/tar.gz
     - 缩略图（按需备份）
   * - ``/var/lib/fess/thumbnails/``
     - RPM/DEB
     - 缩略图（按需备份）

.. note::
   RPM/DEB 软件包版中，``/etc/fess/`` 目录除 ``fess_config.properties`` 外，还存放有 ``fess_env_crawler.properties`` 等 ``fess_env_*.properties`` 文件以及 ``tika.xml`` 等配置文件。建议备份整个 ``/etc/fess/`` 目录。``system.properties`` 在管理界面的"系统 > 通用"中保存设置时，将以 ``/etc/fess/system.properties`` 的形式创建或更新。

配置文件备份示例
----------------------------

以下是 RPM/DEB 软件包版的配置文件备份示例。

::

    #!/bin/bash
    BACKUP_DIR="/backup/fess/$(date +%Y%m%d_%H%M%S)"
    mkdir -p ${BACKUP_DIR}

    # 复制配置文件（包含 system.properties、fess_config.properties 等）
    cp -r /etc/fess/ ${BACKUP_DIR}/

    # 索引定义文件与日志配置
    cp -r /usr/share/fess/app/WEB-INF/classes/fess_indices/ ${BACKUP_DIR}/
    cp /usr/share/fess/app/WEB-INF/classes/log4j2.xml ${BACKUP_DIR}/

    # 可选：缩略图
    # cp -r /var/lib/fess/thumbnails/ ${BACKUP_DIR}/

    echo "Backup completed: ${BACKUP_DIR}"

数据迁移
==========

迁移到其他环境的步骤
------------------

1. **在迁移源创建备份**

   - 创建 OpenSearch 快照。
   - 备份配置文件。

2. **准备迁移目标**

   - 在新环境安装 |Fess|。
   - 启动 OpenSearch。

3. **恢复配置文件**

   - 将备份的配置文件复制到新环境。
   - 根据需要修改路径和主机名等。

4. **恢复索引**

   - 配置快照仓库。
   - 从快照恢复索引。
   - 恢复后，确认 ``fess.search`` 和 ``fess.update`` 别名是否指向已恢复的索引。

5. **运行确认**

   - 启动 |Fess|。
   - 访问管理界面，确认配置。
   - 确认搜索功能是否正常运行。

版本升级注意事项
----------------------------

在不同版本的 |Fess| 之间迁移数据时，请注意以下几点。

- OpenSearch 主版本不同时，可能出现兼容性问题。
- 索引结构有变更时，可能需要重新索引。
- 若需跨越索引结构变更迁移配置信息，请考虑使用管理界面的备份功能（:doc:`../admin/backup-guide`）进行逻辑导出/导入，而非使用 OpenSearch 快照。
- 详情请参考各版本的升级指南。

故障排除
======================

快照创建失败
--------------------------------

1. 请确认仓库路径的访问权限。
2. 请确认磁盘容量是否充足。
3. 请在 OpenSearch 日志文件中确认错误消息。

恢复失败
------------------

1. 请确认是否已存在同名索引。OpenSearch 无法恢复至已处于打开状态的同名索引。请在恢复前关闭（``_close``）或删除目标索引，或使用 ``rename_pattern`` 以其他名称恢复。
2. 请确认 OpenSearch 版本是否兼容。
3. 请确认快照是否损坏。

恢复后无法搜索
------------------------

1. 请确认索引是否正常恢复：``curl -X GET "localhost:9201/_cat/indices?v"``
2. 请确认 ``fess.search`` 和 ``fess.update`` 别名是否指向已恢复的索引：``curl -X GET "localhost:9201/_cat/aliases?v"``。若别名未设置，请通过 ``_aliases`` API 重新配置。
3. 请在 |Fess| 日志文件中确认是否有错误。
4. 请确认配置文件是否已正确恢复。

相关主题
============

- :doc:`../admin/backup-guide` - 通过管理界面备份/恢复配置信息
- :doc:`admin-index-export` - 索引导出功能
- :doc:`admin-logging` - 日志配置

参考信息
========

详细信息请参考 OpenSearch 官方文档。

- `快照功能 <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/index/>`_
- `仓库配置 <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/>`_
- `S3仓库 <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/plugins/#s3-repository>`_
