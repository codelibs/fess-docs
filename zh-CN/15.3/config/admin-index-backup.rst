==================
索引管理
==================

概述
====

|Fess| 处理的数据作为 OpenSearch 的索引管理。
搜索索引的备份和恢复对系统稳定运行必不可少。
本章节介绍索引的备份、恢复和迁移步骤。

索引构成
==================

|Fess| 使用以下索引。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 索引名
     - 说明
   * - ``fess.{日期}``
     - 搜索对象文档的索引(每日创建)
   * - ``fess_log``
     - 搜索日志和点击日志
   * - ``fess_user``
     - 用户信息
   * - ``fess_config``
     - 系统配置信息
   * - ``configsync``
     - 配置同步信息

索引备份和恢复
====================================

可以使用 OpenSearch 的快照功能执行索引的备份和恢复。

快照仓库配置
--------------------------------

首先,配置保存备份数据的仓库。

**文件系统仓库:**

1. 在 OpenSearch 的配置文件 (``config/opensearch.yml``) 中添加仓库路径。

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
   |Fess| 的默认配置中,OpenSearch 在 9201 端口启动。

**AWS S3仓库:**

将 S3 作为备份目标时,请安装并配置 ``repository-s3`` 插件。

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

创建快照(备份)
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

仅备份特定索引。

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_fess_only?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.*,fess_config",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

定期自动备份
~~~~~~~~~~~~~~~~~~~~~~~~

可以使用 cron 等定期执行备份。

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

确认创建的快照列表。

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

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

更改索引名恢复
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

恢复时也可以更改索引名。

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101",
      "rename_pattern": "fess.(.+)",
      "rename_replacement": "restored_fess.$1",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

删除快照
----------------------

可以删除旧快照以节省存储容量。

::

    curl -X DELETE "localhost:9201/_snapshot/fess_backup/snapshot_1"

配置文件备份
==========================

除 OpenSearch 索引外,也请备份以下配置文件。

备份对象文件
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 文件/目录
     - 说明
   * - ``app/WEB-INF/conf/system.properties``
     - 系统配置(zip安装)
   * - ``/etc/fess/system.properties``
     - 系统配置(RPM/DEB软件包)
   * - ``app/WEB-INF/classes/fess_config.properties``
     - Fess 详细配置
   * - ``/etc/fess/fess_config.properties``
     - Fess 详细配置(RPM/DEB软件包)
   * - ``app/WEB-INF/classes/log4j2.xml``
     - 日志配置
   * - ``/etc/fess/log4j2.xml``
     - 日志配置(RPM/DEB软件包)
   * - ``app/WEB-INF/classes/fess_indices/``
     - 索引定义文件
   * - ``thumbnail/``
     - 缩略图(如需要)

配置文件备份示例
----------------------------

::

    #!/bin/bash
    BACKUP_DIR="/backup/fess/$(date +%Y%m%d_%H%M%S)"
    mkdir -p ${BACKUP_DIR}

    # 复制配置文件
    cp -r /etc/fess/ ${BACKUP_DIR}/
    cp -r /var/lib/fess/app/WEB-INF/conf/ ${BACKUP_DIR}/
    cp -r /var/lib/fess/app/WEB-INF/classes/fess_indices/ ${BACKUP_DIR}/

    # 可选: 缩略图
    # cp -r /var/lib/fess/thumbnail/ ${BACKUP_DIR}/

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
   - 必要时修改路径和主机名等。

4. **恢复索引**

   - 配置快照仓库。
   - 从快照恢复索引。

5. **运行确认**

   - 启动 |Fess|。
   - 访问管理页面,确认配置。
   - 确认搜索功能是否正常运行。

版本升级注意事项
----------------------------

在不同版本的 |Fess| 间迁移数据时,请注意以下几点。

- OpenSearch 主版本不同时,可能出现兼容性问题。
- 索引结构有变更时,可能需要重新索引。
- 详情请参考各版本的升级指南。

故障排除
======================

快照创建失败
--------------------------------

1. 请确认仓库路径的权限。
2. 请确认磁盘容量是否充足。
3. 请在 OpenSearch 日志文件中确认错误消息。

恢复失败
------------------

1. 请确认是否已存在同名索引。
2. 请确认 OpenSearch 版本是否兼容。
3. 请确认快照是否损坏。

恢复后无法搜索
------------------------

1. 请确认索引是否正常恢复: ``curl -X GET "localhost:9201/_cat/indices?v"``
2. 请在 |Fess| 日志文件中确认是否有错误。
3. 请确认配置文件是否正确恢复。

参考信息
========

详细信息请参考 OpenSearch 官方文档。

- `快照功能 <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/index/>`_
- `仓库配置 <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/>`_
- `S3仓库 <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/plugins/#s3-repository>`_
