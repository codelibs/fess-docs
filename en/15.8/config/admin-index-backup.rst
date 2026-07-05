==================
Index Management
==================

Overview
========

Data handled by |Fess| is managed as OpenSearch indexes.
Backup and restore of search indexes is essential for stable system operation.
This section explains index backup, restore, and migration procedures using OpenSearch's snapshot functionality.

.. note::
   In addition to the OpenSearch snapshot-based index backup described in this section, |Fess| also provides a feature to export/import configuration information (crawl configuration, user information, system settings, etc.) from the administration screen. If you only need to back up or migrate configuration information, refer to :doc:`../admin/backup-guide`. OpenSearch snapshots are suited for physically backing up entire indexes including search documents.

Index Structure
===============

|Fess| uses the following indexes:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Index Name
     - Description
   * - ``fess.{timestamp}``
     - Search document index. Created in ``fess.{yyyyMMddHHmmssSSS}`` format (millisecond-precision timestamp) when the index is rebuilt, and referenced via the ``fess.search`` (for searching) and ``fess.update`` (for updating) aliases.
   * - ``fess_config.*``
     - System configuration (composed of multiple sub-indices such as ``fess_config.web_config``, ``fess_config.scheduled_job``, ``fess_config.data_config``, etc.)
   * - ``fess_user.*``
     - User information (``fess_user.user``, ``fess_user.role``, ``fess_user.group``)
   * - ``fess_log.*``
     - Search logs, click logs, etc. (``fess_log.search_log``, ``fess_log.click_log``, ``fess_log.favorite_log``, ``fess_log.user_info``, ``fess_log.notification_queue``)
   * - ``fess_crawler.*``
     - Temporary indexes used during crawling (``fess_crawler.queue``, ``fess_crawler.data``, ``fess_crawler.filter``). These are not needed after crawling completes and generally do not need to be included in backups.

Index Backup and Restore
=========================

You can execute index backup and restore using OpenSearch's snapshot functionality.

Snapshot Repository Configuration
----------------------------------

First, configure a repository to store backup data.

**For filesystem repository:**

1. Add the repository path to the OpenSearch configuration file (``opensearch.yml``).

::

    path.repo: ["/var/opensearch/backup"]

2. Restart OpenSearch.

3. Register the repository.

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
   In the default configuration of the |Fess| zip/tar.gz distribution, OpenSearch starts on port 9201 (``search_engine.http.url`` in ``fess_config.properties``). For RPM/DEB packages, the default configuration connects to port 9200 (``SEARCH_ENGINE_HTTP_URL`` in the environment configuration file ``/etc/sysconfig/fess`` (RPM) or ``/etc/default/fess`` (DEB)). Adjust the port number to match your environment.

**For AWS S3 repository:**

To use S3 as a backup destination, install and configure the ``repository-s3`` plugin.

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

Creating Snapshots (Backup)
----------------------------

Backing Up All Indexes
~~~~~~~~~~~~~~~~~~~~~~~

Back up all indexes.

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_1?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Backing Up Specific Indexes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Back up only specific indexes. The following example targets only |Fess|-related indexes (indexes starting with ``fess``).

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_fess_only?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Automated Periodic Backups
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Periodic backups can be executed using cron or similar tools.

::

    #!/bin/bash
    DATE=$(date +%Y%m%d_%H%M%S)
    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_${DATE}?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Checking Snapshots
------------------

Check the list of created snapshots.

::

    curl -X GET "localhost:9201/_snapshot/fess_backup/_all?pretty"

Check details of a specific snapshot.

::

    curl -X GET "localhost:9201/_snapshot/fess_backup/snapshot_1?pretty"

Restoring from Snapshots
-------------------------

Restoring All Indexes
~~~~~~~~~~~~~~~~~~~~~~

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Restoring Specific Indexes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The search document index name is in the format ``fess.{yyyyMMddHHmmssSSS}``. Verify the actual index name using ``_cat/indices`` or similar before restoring.

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101000000000",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Restoring with Index Name Change
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also change the index name when restoring.

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
   After restoring the search document index (``fess.{timestamp}``), always verify that the ``fess.search`` and ``fess.update`` aliases point to the restored index. Snapshots include alias information, so when all indexes are restored with their original names, aliases are typically restored as well. However, if you restored with a renamed index using ``rename_pattern``, or migrated to a different cluster, aliases may not be configured correctly. In that case, manually reconfigure the aliases as shown below (replace the index name with the actual one).

   ::

       curl -X POST "localhost:9201/_aliases" -H 'Content-Type: application/json' -d'
       {
         "actions": [
           { "add": { "index": "restored_fess.20250101000000000", "alias": "fess.search" } },
           { "add": { "index": "restored_fess.20250101000000000", "alias": "fess.update" } }
         ]
       }'

Deleting Snapshots
------------------

You can delete old snapshots to save storage space.

::

    curl -X DELETE "localhost:9201/_snapshot/fess_backup/snapshot_1"

Configuration File Backup
==========================

In addition to OpenSearch indexes, back up the following configuration files. The location of configuration files varies depending on the installation method.

Files to Back Up
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - File/Directory
     - Installation Method
     - Description
   * - ``app/WEB-INF/conf/system.properties``
     - zip/tar.gz
     - System configuration (general settings)
   * - ``/etc/fess/system.properties``
     - RPM/DEB
     - System configuration (general settings)
   * - ``app/WEB-INF/classes/fess_config.properties``
     - zip/tar.gz
     - Detailed |Fess| configuration
   * - ``/etc/fess/fess_config.properties``
     - RPM/DEB
     - Detailed |Fess| configuration
   * - ``app/WEB-INF/classes/log4j2.xml``
     - zip/tar.gz
     - Log configuration
   * - ``/usr/share/fess/app/WEB-INF/classes/log4j2.xml``
     - RPM/DEB
     - Log configuration
   * - ``app/WEB-INF/classes/fess_indices/``
     - zip/tar.gz
     - Index definition files
   * - ``/usr/share/fess/app/WEB-INF/classes/fess_indices/``
     - RPM/DEB
     - Index definition files
   * - ``app/WEB-INF/thumbnails/``
     - zip/tar.gz
     - Thumbnail images (as needed)
   * - ``/var/lib/fess/thumbnails/``
     - RPM/DEB
     - Thumbnail images (as needed)

.. note::
   In the RPM/DEB package installation, the ``/etc/fess/`` directory contains not only ``fess_config.properties`` but also other configuration files such as ``fess_env_crawler.properties`` and other ``fess_env_*.properties`` files, as well as ``tika.xml``. It is recommended to back up the entire ``/etc/fess/`` directory. The ``system.properties`` file is created and updated as ``/etc/fess/system.properties`` when settings are saved in the administration screen under "System > General".

Configuration File Backup Example
----------------------------------

The following is an example of backing up configuration files for the RPM/DEB package installation.

::

    #!/bin/bash
    BACKUP_DIR="/backup/fess/$(date +%Y%m%d_%H%M%S)"
    mkdir -p ${BACKUP_DIR}

    # Copy configuration files (including system.properties, fess_config.properties, etc.)
    cp -r /etc/fess/ ${BACKUP_DIR}/

    # Index definition files and log configuration
    cp -r /usr/share/fess/app/WEB-INF/classes/fess_indices/ ${BACKUP_DIR}/
    cp /usr/share/fess/app/WEB-INF/classes/log4j2.xml ${BACKUP_DIR}/

    # Optional: Thumbnail images
    # cp -r /var/lib/fess/thumbnails/ ${BACKUP_DIR}/

    echo "Backup completed: ${BACKUP_DIR}"

Data Migration
==============

Migration Procedure to a Different Environment
-----------------------------------------------

1. **Create Backup at Source**

   - Create an OpenSearch snapshot.
   - Back up configuration files.

2. **Prepare Destination**

   - Install |Fess| in the new environment.
   - Start OpenSearch.

3. **Restore Configuration Files**

   - Copy the backed-up configuration files to the new environment.
   - Modify paths, hostnames, etc. as needed.

4. **Restore Indexes**

   - Configure the snapshot repository.
   - Restore indexes from the snapshot.
   - After restoring, verify that the ``fess.search`` and ``fess.update`` aliases point to the restored index.

5. **Verify Operation**

   - Start |Fess|.
   - Access the administration screen and verify the configuration.
   - Verify that search functionality works correctly.

Version Upgrade Considerations
-------------------------------

When migrating data between different |Fess| versions, note the following:

- If OpenSearch major versions differ, compatibility issues may occur.
- If the index structure has changed, reindexing may be necessary.
- If you want to migrate configuration information across index structure changes, consider using the administration screen backup feature (:doc:`../admin/backup-guide`) for logical export/import rather than OpenSearch snapshots.
- For details, refer to the upgrade guide for each version.

Troubleshooting
===============

Snapshot Creation Fails
------------------------

1. Check permissions for the repository path.
2. Verify that sufficient disk space is available.
3. Check error messages in OpenSearch log files.

Restore Fails
-------------

1. Verify that an index with the same name does not already exist. In OpenSearch, you cannot restore to an open index with the same name. Before restoring, either close (``_close``) or delete the target index, or restore under a different name using ``rename_pattern``.
2. Verify that the OpenSearch version is compatible.
3. Verify that the snapshot is not corrupted.

Cannot Search After Restore
----------------------------

1. Verify that indexes were restored correctly: ``curl -X GET "localhost:9201/_cat/indices?v"``
2. Verify that the ``fess.search`` and ``fess.update`` aliases point to the restored index: ``curl -X GET "localhost:9201/_cat/aliases?v"``. If aliases are not configured, reconfigure them using the ``_aliases`` API.
3. Check |Fess| log files for errors.
4. Verify that configuration files were restored correctly.

Related Topics
==============

- :doc:`../admin/backup-guide` - Backup/restore of configuration information from the administration screen
- :doc:`admin-index-export` - Index export functionality
- :doc:`admin-logging` - Log configuration

References
==========

For detailed information, refer to the official OpenSearch documentation.

- `Snapshot Functionality <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/index/>`_
- `Repository Configuration <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/>`_
- `S3 Repository <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/plugins/#s3-repository>`_
