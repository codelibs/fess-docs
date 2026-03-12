==================
Index Management
==================

Overview
========

Data handled by |Fess| is managed as OpenSearch indexes.
Backup and restore of search indexes is essential for stable system operation.
This section explains index backup, restore, and migration procedures.

Index Structure
===============

|Fess| uses the following indexes:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Index Name
     - Description
   * - ``fess.{date}``
     - Search target document index (created daily)
   * - ``fess_log``
     - Search logs and click logs
   * - ``fess_user``
     - User information
   * - ``fess_config``
     - System configuration information
   * - ``configsync``
     - Configuration synchronization information

Index Backup and Restore
=========================

You can execute index backup and restore using OpenSearch's snapshot functionality.

Snapshot Repository Configuration
----------------------------------

First, configure a repository to store backup data.

**For filesystem repository:**

1. Add the repository path to the OpenSearch configuration file (``config/opensearch.yml``).

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
   In |Fess|'s default configuration, OpenSearch starts on port 9201.

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

Back up only specific indexes.

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_fess_only?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.*,fess_config",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Automated Periodic Backups
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Periodic backups can be executed using cron or similar.

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

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Restoring with Index Name Change
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also change the index name when restoring.

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101",
      "rename_pattern": "fess.(.+)",
      "rename_replacement": "restored_fess.$1",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Deleting Snapshots
------------------

You can delete old snapshots to save storage space.

::

    curl -X DELETE "localhost:9201/_snapshot/fess_backup/snapshot_1"

Configuration File Backup
==========================

In addition to OpenSearch indexes, back up the following configuration files.

Files to Back Up
----------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - File/Directory
     - Description
   * - ``app/WEB-INF/conf/system.properties``
     - System configuration (for zip installation)
   * - ``/etc/fess/system.properties``
     - System configuration (for RPM/DEB packages)
   * - ``app/WEB-INF/classes/fess_config.properties``
     - Detailed Fess configuration
   * - ``/etc/fess/fess_config.properties``
     - Detailed Fess configuration (RPM/DEB packages)
   * - ``app/WEB-INF/classes/log4j2.xml``
     - Log configuration
   * - ``/etc/fess/log4j2.xml``
     - Log configuration (RPM/DEB packages)
   * - ``app/WEB-INF/classes/fess_indices/``
     - Index definition files
   * - ``thumbnail/``
     - Thumbnail images (as needed)

Configuration File Backup Example
----------------------------------

::

    #!/bin/bash
    BACKUP_DIR="/backup/fess/$(date +%Y%m%d_%H%M%S)"
    mkdir -p ${BACKUP_DIR}

    # Copy configuration files
    cp -r /etc/fess/ ${BACKUP_DIR}/
    cp -r /var/lib/fess/app/WEB-INF/conf/ ${BACKUP_DIR}/
    cp -r /var/lib/fess/app/WEB-INF/classes/fess_indices/ ${BACKUP_DIR}/

    # Optional: Thumbnail images
    # cp -r /var/lib/fess/thumbnail/ ${BACKUP_DIR}/

    echo "Backup completed: ${BACKUP_DIR}"

Data Migration
==============

Migration Procedure to Different Environment
---------------------------------------------

1. **Create Backup at Source**

   - Create OpenSearch snapshot.
   - Back up configuration files.

2. **Prepare Destination**

   - Install |Fess| in new environment.
   - Start OpenSearch.

3. **Restore Configuration Files**

   - Copy backed up configuration files to new environment.
   - Modify paths, hostnames, etc. as needed.

4. **Restore Indexes**

   - Configure snapshot repository.
   - Restore indexes from snapshot.

5. **Verify Operation**

   - Start |Fess|.
   - Access administration screen and verify configuration.
   - Verify that search functionality works correctly.

Version Upgrade Considerations
-------------------------------

When migrating data between different |Fess| versions, note the following:

- If OpenSearch major versions differ, compatibility issues may occur.
- If index structure has changed, reindexing may be necessary.
- For details, refer to the upgrade guide for each version.

Troubleshooting
===============

Snapshot Creation Fails
------------------------

1. Check permissions for the repository path.
2. Verify sufficient disk space.
3. Check error messages in OpenSearch log files.

Restore Fails
-------------

1. Verify that an index with the same name does not already exist.
2. Verify that the OpenSearch version is compatible.
3. Verify that the snapshot is not corrupted.

Cannot Search After Restore
----------------------------

1. Verify that indexes were restored correctly: ``curl -X GET "localhost:9201/_cat/indices?v"``
2. Check |Fess| log files for errors.
3. Verify that configuration files were restored correctly.

References
==========

For detailed information, refer to the official OpenSearch documentation.

- `Snapshot Functionality <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/index/>`_
- `Repository Configuration <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/>`_
- `S3 Repository <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/plugins/#s3-repository>`_
