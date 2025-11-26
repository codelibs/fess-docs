==================
Upgrade Procedure
==================

This page describes the procedures for upgrading |Fess| from a previous version to the latest release.

.. warning::

   **Important Notes Before Upgrade**

   - Always create a backup before upgrading
   - It is strongly recommended to validate the upgrade in a test environment first
   - Services will be stopped during the upgrade, so schedule appropriate maintenance time
   - Configuration file formats may have changed depending on the version

Supported Versions
==================

This upgrade procedure supports upgrades between the following versions:

- Fess 14.x → Fess 15.3
- Fess 15.x → Fess 15.3

.. note::

   When upgrading from older versions (13.x or earlier), a phased upgrade may be necessary.
   For details, check the release notes.

Pre-Upgrade Preparation
=======================

Verify Version Compatibility
-----------------------------

Verify the compatibility between the upgrade target version and the current version.

- `Release Notes <https://github.com/codelibs/fess/releases>`__
- `Upgrade Guide <https://fess.codelibs.org/>`__

Plan Downtime
-------------

The upgrade process requires system shutdown. Plan downtime considering the following:

- Backup time: 10 minutes to several hours (depending on data volume)
- Upgrade time: 10 to 30 minutes
- Verification time: 30 minutes to 1 hour
- Reserve time: 30 minutes

**Recommended Maintenance Time**: Total 2 to 4 hours

Step 1: Data Backup
===================

Back up all data before upgrading.

Configuration Data Backup
--------------------------

1. **Backup from Admin Screen**

   Log in to the admin screen and click "System" → "Backup".

   Download the following files:

   - ``fess_basic_config.bulk``
   - ``fess_user.bulk``

2. **Configuration File Backup**

   TAR.GZ/ZIP version::

       $ cp /path/to/fess/app/WEB-INF/conf/system.properties /backup/
       $ cp /path/to/fess/app/WEB-INF/classes/fess_config.properties /backup/

   RPM/DEB version::

       $ sudo cp /etc/fess/system.properties /backup/
       $ sudo cp /etc/fess/fess_config.properties /backup/

3. **Customized Configuration Files**

   If you have customized configuration files, back up those as well::

       $ cp /path/to/fess/app/WEB-INF/classes/log4j2.xml /backup/

Index Data Backup
-----------------

Back up OpenSearch index data.

Method 1: Use Snapshot Feature (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Back up the index using OpenSearch snapshot feature.

1. Configure repository::

       $ curl -X PUT "http://localhost:9200/_snapshot/fess_backup" -H 'Content-Type: application/json' -d'
       {
         "type": "fs",
         "settings": {
           "location": "/backup/opensearch/snapshots"
         }
       }'

2. Create snapshot::

       $ curl -X PUT "http://localhost:9200/_snapshot/fess_backup/snapshot_1?wait_for_completion=true"

3. Verify snapshot::

       $ curl -X GET "http://localhost:9200/_snapshot/fess_backup/snapshot_1"

Method 2: Backup Entire Directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Stop OpenSearch and back up the data directory.

::

    $ sudo systemctl stop opensearch
    $ sudo tar czf /backup/opensearch-data-$(date +%Y%m%d).tar.gz /var/lib/opensearch/data
    $ sudo systemctl start opensearch

Docker Version Backup
---------------------

Back up Docker volumes::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop
    $ docker run --rm -v fess-es-data:/data -v $(pwd):/backup ubuntu tar czf /backup/fess-es-data-backup.tar.gz /data
    $ docker run --rm -v fess-data:/data -v $(pwd):/backup ubuntu tar czf /backup/fess-data-backup.tar.gz /data
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml start

Step 2: Stop Current Version
=============================

Stop Fess and OpenSearch.

TAR.GZ/ZIP version::

    $ kill <fess_pid>
    $ kill <opensearch_pid>

RPM/DEB version (systemd)::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Docker version::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

Step 3: Install New Version
============================

The procedure varies depending on the installation method.

TAR.GZ/ZIP Version
------------------

1. Download and extract the new version::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.3.2/fess-15.3.2.tar.gz
       $ tar -xzf fess-15.3.2.tar.gz

2. Copy configuration from the old version::

       $ cp /path/to/old-fess/app/WEB-INF/conf/system.properties /path/to/fess-15.3.2/app/WEB-INF/conf/
       $ cp /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.3.2/bin/

3. Verify configuration differences and adjust as necessary

RPM/DEB Version
---------------

Install the new version package::

    # RPM
    $ sudo rpm -Uvh fess-15.3.2.rpm

    # DEB
    $ sudo dpkg -i fess-15.3.2.deb

.. note::

   Configuration files (``/etc/fess/*``) are automatically retained.
   However, if new configuration options have been added, manual adjustment may be necessary.

Docker Version
--------------

1. Obtain Compose files for the new version::

       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.3.2/compose/compose.yaml
       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.3.2/compose/compose-opensearch3.yaml

2. Pull new images::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

Step 4: Upgrade OpenSearch (If Necessary)
==========================================

If you are also upgrading OpenSearch, follow these procedures.

.. warning::

   Be careful when performing major version upgrades of OpenSearch.
   Index compatibility issues may occur.

1. Install the new version of OpenSearch

2. Reinstall plugins::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.1
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.1

3. Start OpenSearch::

       $ sudo systemctl start opensearch.service

Step 5: Start New Version
==========================

TAR.GZ/ZIP version::

    $ cd /path/to/fess-15.3.2
    $ ./bin/fess -d

RPM/DEB version::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

Docker version::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Step 6: Verify Operation
=========================

1. **Check Logs**

   Verify there are no errors::

       $ tail -f /path/to/fess/logs/fess.log

2. **Access Web Interface**

   Access http://localhost:8080/ in a browser.

3. **Log in to Admin Screen**

   Access http://localhost:8080/admin and log in with the administrator account.

4. **Verify System Information**

   Click "System" → "System Info" in the admin screen and verify the version has been updated.

5. **Verify Search Operation**

   Execute a search on the search screen and verify results are returned normally.

Step 7: Recreate Index (Recommended)
=====================================

For major version upgrades, it is recommended to recreate the index.

1. Verify existing crawl schedules
2. Execute "Default Crawler" from "System" → "Scheduler"
3. Wait for crawl to complete
4. Verify search results

Rollback Procedure
==================

If the upgrade fails, you can rollback with the following procedure.

Step 1: Stop New Version
-------------------------

::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Step 2: Restore Old Version
----------------------------

Restore configuration files and data from backup.

For RPM/DEB version::

    $ sudo rpm -Uvh --oldpackage fess-<old-version>.rpm

Or::

    $ sudo dpkg -i fess-<old-version>.deb

Step 3: Restore Data
---------------------

Restore from snapshot::

    $ curl -X POST "http://localhost:9200/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true"

Or restore directory from backup::

    $ sudo systemctl stop opensearch
    $ sudo rm -rf /var/lib/opensearch/data/*
    $ sudo tar xzf /backup/opensearch-data-backup.tar.gz -C /
    $ sudo systemctl start opensearch

Step 4: Start and Verify Service
---------------------------------

::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

Verify operation and confirm it has returned to normal.

Frequently Asked Questions
===========================

Q: Can I upgrade without downtime?
-----------------------------------

A: Upgrading Fess requires service shutdown. To minimize downtime, consider the following:

- Verify procedures in a test environment first
- Create backups in advance
- Secure sufficient maintenance time

Q: Do I need to upgrade OpenSearch too?
----------------------------------------

A: Depending on the Fess version, a specific version of OpenSearch may be required.
Check the recommended OpenSearch version in the release notes.

Q: Do I need to recreate the index?
------------------------------------

A: For minor version upgrades, it is usually not necessary, but for major version upgrades, recreation is recommended.

Q: Search results are not displayed after upgrade
--------------------------------------------------

A: Verify the following:

1. Verify OpenSearch is running
2. Verify indexes exist (``curl http://localhost:9200/_cat/indices``)
3. Re-run crawl

Next Steps
==========

After the upgrade is complete:

- :doc:`run` - Verify startup and initial configuration
- :doc:`security` - Review security configuration
- Check release notes for new features
