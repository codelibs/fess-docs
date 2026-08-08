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

- Fess 14.x → Fess 15.8
- Fess 15.x → Fess 15.8

.. important::

   |Fess| 14.x supports the OpenSearch 2.x series, while |Fess| 15.8 supports OpenSearch 3.8.0.
   Because the OpenSearch plugins for |Fess| must exactly match the OpenSearch version, upgrading
   from 14.x also requires a major version upgrade of OpenSearch.
   See :ref:`upgrade-opensearch` for details.

.. note::

   When upgrading from older versions (13.x or earlier), a phased upgrade may be necessary.
   For details, check the release notes.

Pre-Upgrade Preparation
=======================

Verify Version Compatibility
-----------------------------

Verify the compatibility between the upgrade target version and the current version.

- `Release Notes <https://github.com/codelibs/fess/releases>`__
- :doc:`prerequisites` - |Fess| 15.8 system requirements (Java and OpenSearch versions)

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

   Log in to the admin screen and click "System Info" → "Backup".

   The backup page lists the following configuration data as individual items.
   Click each row to download it (these are individual files per item, not a single ZIP; there is
   no bulk-download feature, so download the items you need one at a time).

   - ``fess_basic_config.bulk`` - Configuration indices (19 indices covering crawl settings,
     scheduler, labels, key matches, roles, web/file authentication, and so on)
   - ``fess_config.bulk`` - The same 19 indices plus runtime data such as crawling information,
     failure URLs, job logs, and the thumbnail queue (25 indices in total)
   - ``fess_user.bulk`` - Users, roles, and groups
   - ``system.properties`` - System settings, including general configuration
   - ``fess.json`` - Index settings (shard count, ``index.knn``, and so on)
   - ``doc.json`` - Document mapping (field definitions)

   .. note::

      ``fess_config.bulk`` already includes everything in ``fess_basic_config.bulk``. For a
      configuration backup before upgrading, ``fess_basic_config.bulk``, ``fess_user.bulk``, and
      ``system.properties`` are sufficient.

   .. note::

      Log data such as search logs and click logs (``search_log.ndjson``, ``click_log.ndjson``,
      ``favorite_log.ndjson``, ``user_info.ndjson``) can also be downloaded from the same page.
      They are not needed if you only want to back up the configuration. Note that these
      ``*.ndjson`` files cannot be restored by uploading them on the backup page (see "Rollback
      Procedure").

2. **Configuration File Backup**

   TAR.GZ/ZIP version::

       $ cp /path/to/fess/app/WEB-INF/conf/system.properties /backup/
       $ cp /path/to/fess/app/WEB-INF/classes/fess_config.properties /backup/
       $ cp /path/to/fess/bin/fess.in.sh /backup/

   RPM version::

       $ sudo cp /etc/fess/system.properties /backup/
       $ sudo cp /etc/fess/fess_config.properties /backup/
       $ sudo cp /etc/sysconfig/fess /backup/

   DEB version::

       $ sudo cp /etc/fess/system.properties /backup/
       $ sudo cp /etc/fess/fess_config.properties /backup/
       $ sudo cp /etc/default/fess /backup/

   .. note::

      ``/etc/sysconfig/fess`` (RPM version) and ``/etc/default/fess`` (DEB version) are
      environment variable files that set values such as ``FESS_PORT``, ``FESS_HEAP_SIZE``,
      ``SEARCH_ENGINE_HTTP_URL``, and ``FESS_DICTIONARY_PATH``. For the TAR.GZ/ZIP version, the
      equivalent settings are in ``bin/fess.in.sh``.

3. **Customized Configuration Files**

   If you have customized configuration files, back up those as well::

       $ cp /path/to/fess/app/WEB-INF/classes/log4j2.xml /backup/

   .. note::

      ``app/WEB-INF/classes/log4j2.xml`` is the log configuration for the |Fess| main (web)
      process. Child processes such as the crawler use separate files (for example,
      ``app/WEB-INF/env/crawler/resources/log4j2.xml``, one each for ``crawler``, ``suggest``,
      ``thumbnail``, and ``chunk`` — four in total), so back those up too if you have customized
      them.

Index Data Backup
-----------------

Back up OpenSearch index data.

Method 1: Use Snapshot Feature (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Back up the index using OpenSearch snapshot feature.

.. note::

   To register a filesystem (``fs``) repository, you must first specify the backup destination
   directory in ``path.repo`` in OpenSearch's ``opensearch.yml`` and restart OpenSearch.

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

OpenSearch data is stored in Docker volumes. ``compose-opensearch3.yaml`` defines two volumes:
``search01_data`` for index data and ``search01_dictionary`` for dictionary files.

.. note::

   The actual volume names are prefixed with the Compose project name (by default, the name of
   the directory containing the Compose files). Check the exact names with::

       $ docker volume ls

Stop the containers, then back up the volumes. Specify the actual volume name, including the
prefix, for ``-v`` in ``docker run``::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop
    $ PROJECT=$(basename "$(pwd)")
    $ docker run --rm -v ${PROJECT}_search01_data:/data -v $(pwd):/backup ubuntu tar czf /backup/search01-data-backup.tar.gz /data
    $ docker run --rm -v ${PROJECT}_search01_dictionary:/data -v $(pwd):/backup ubuntu tar czf /backup/search01-dictionary-backup.tar.gz /data
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml start

.. warning::

   If you specify ``-v`` with the unprefixed name ``search01_data``, Docker does not reference the
   existing volume — it creates a new, empty volume with the same name instead. The command does
   not report an error, and an archive with empty contents is created, so it can look as though
   the backup succeeded.

.. note::

   The |Fess| main container (``fess01``) has no dedicated volume of its own, so the two volumes
   above are the only backup targets. However, general settings changed from the admin UI and
   plugins installed from the admin UI are stored only inside the container and are lost when the
   container is recreated. Persist these instead by specifying them via ``FESS_JAVA_OPTS`` or
   ``FESS_PLUGINS`` in the Compose file.

Step 2: Stop Current Version
=============================

Stop Fess and OpenSearch.

The TAR.GZ/ZIP version does not include a stop script. If you started ``bin/fess`` with the
``-p`` option, stop it using the PID file::

    $ kill $(cat /path/to/fess/fess.pid)
    $ kill <opensearch_pid>

If you started it without ``-p``, find the process ID and ``kill`` it manually (``-d`` alone does
not create a PID file).

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

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.8.0/fess-15.8.0.zip
       $ unzip fess-15.8.0.zip

   .. note::

      |Fess| archives are distributed only in ZIP format (``fess-15.8.0.tar.gz`` is not
      provided).

2. Copy configuration from the old version::

       $ cp /path/to/old-fess/app/WEB-INF/conf/system.properties /path/to/fess-15.8.0/app/WEB-INF/conf/
       $ cp /path/to/old-fess/app/WEB-INF/classes/fess_config.properties /path/to/fess-15.8.0/app/WEB-INF/classes/
       $ cp /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.8.0/bin/

3. If you have customizations, also copy the following::

       # Log configuration
       $ cp /path/to/old-fess/app/WEB-INF/classes/log4j2.xml /path/to/fess-15.8.0/app/WEB-INF/classes/
       # Installed plugins
       $ cp -r /path/to/old-fess/app/WEB-INF/plugin/. /path/to/fess-15.8.0/app/WEB-INF/plugin/
       # Theme
       $ cp -r /path/to/old-fess/app/themes/. /path/to/fess-15.8.0/app/themes/

   .. warning::

      Do not copy JSPs (``app/WEB-INF/view/``) edited via "Design" in the admin UI as-is. If
      their structure differs from the JSPs in the new version, pages may not render correctly.
      Reapply your changes to the new version's JSPs instead.

4. If you are using the embedded OpenSearch (starting ``bin/fess`` without setting
   ``SEARCH_ENGINE_HTTP_URL``), also copy the index data::

       $ cp -r /path/to/old-fess/es/data/. /path/to/fess-15.8.0/es/data/

5. Verify configuration differences and adjust as necessary

RPM/DEB Version
---------------

Install the new version package::

    # RPM
    $ sudo rpm -Uvh fess-15.8.0.rpm

    # DEB
    $ sudo dpkg -i fess-15.8.0.deb

.. note::

   For the RPM version, the configuration files under ``/etc/fess/*`` are registered as
   ``%config(noreplace)``, so they are retained across upgrades (the new default files are placed
   alongside them with a ``.rpmnew`` suffix). If new configuration options have been added,
   manual adjustment may be necessary.

.. warning::

   For the DEB version, ``/etc/fess/*`` is not registered as a conffile (the only conffiles are
   ``/etc/default/fess``, ``/etc/init.d/fess``, and ``/usr/lib/systemd/system/fess.service``).
   As a result, running ``dpkg -i`` overwrites files such as ``/etc/fess/fess_config.properties``
   with the new version's files. Reapply the configuration you backed up in Step 1 after
   upgrading. Note that ``/etc/fess/system.properties`` is a runtime-generated file not included
   in the package, so it is not overwritten.

Docker Version
--------------

1. Obtain Compose files for the new version::

       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.8.0/compose/compose.yaml
       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.8.0/compose/compose-opensearch3.yaml

2. Pull new images::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

.. _upgrade-opensearch:

Step 4: Upgrade OpenSearch
==========================

|Fess| 15.8 supports OpenSearch 3.8.0. If the OpenSearch you connect to is older than that,
upgrade it using the following procedure.

.. note::

   This procedure applies when you are managing OpenSearch manually on a TAR.GZ/ZIP or RPM/DEB
   installation. For the Docker version, pulling the new image in Step 3 updates OpenSearch and
   its plugins together, so this step is not required.

.. important::

   Regardless of whether you use chunk-vector search (semantic search), |Fess| 15.8 always
   includes ``index.knn`` in the search index settings and ``content_chunk_vector`` (a
   ``knn_vector`` type) in the mapping. Because of this, the OpenSearch you connect to **must
   have the k-NN plugin installed**.

   - It is bundled with the standard OpenSearch distribution and the Docker version's image.
   - **It is not included in the minimal distribution, so creating a new index fails and |Fess|
     cannot start.**
   - The index settings also always send ``knn.derived_source.enabled``. An older OpenSearch
     that does not recognize this setting fails to create the index regardless of whether the
     k-NN plugin is present.

   See "Prerequisites" in :doc:`../config/search-semantic` for details.

.. warning::

   Be careful when performing major version upgrades of OpenSearch.
   Index compatibility issues may occur.
   |Fess| 14.x uses the OpenSearch 2.x series, so upgrading from 14.x always falls into this
   case.

1. Install the new version of OpenSearch

2. Reinstall plugins::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.8.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.8.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.8.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.8.0

   .. note::

      The version of these plugins must match the version of OpenSearch you use. |Fess| 15.8
      supports OpenSearch 3.8.0. Installation fails if the versions do not match.

3. Start OpenSearch::

       $ sudo systemctl start opensearch.service

Step 5: Start New Version
==========================

TAR.GZ/ZIP version::

    $ cd /path/to/fess-15.8.0
    $ ./bin/fess -d -p /path/to/fess-15.8.0/fess.pid

.. note::

   Specifying ``-p`` creates a PID file, which lets you stop |Fess| the next time with
   ``kill $(cat /path/to/fess-15.8.0/fess.pid)``.

RPM/DEB version::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

Docker version::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Step 6: Verify Operation
=========================

1. **Check Logs**

   Verify there are no errors.

   TAR.GZ/ZIP version::

       $ tail -f /path/to/fess/logs/fess.log

   RPM/DEB version::

       $ sudo tail -f /var/log/fess/fess.log

   Docker version::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01

   .. note::

      The same log directory also contains ``fess-crawler.log`` for crawl processing,
      ``audit.log`` for authentication and admin operations, and ``searchlog.log`` for search
      requests.

2. **Access Web Interface**

   Access http://localhost:8080/ in a browser.

3. **Log in to Admin Screen**

   Access http://localhost:8080/admin and log in with the administrator account.

4. **Check the Version**

   In the admin UI, click "System Info" → "Config Info" and confirm that ``fess.version``
   shown under "System Properties" reflects the new version.

5. **Verify Search Operation**

   Execute a search on the search screen and verify results are returned normally.

Step 7: Recreate Index (Recommended)
=====================================

For major version upgrades, it is recommended to recreate the index.

.. note::

   The steps below re-run the crawl; they do not update the index mapping (field definitions).
   If you need a re-index that updates the mapping — for example, to newly enable chunk-vector
   search (semantic search) — separately run "Re-indexing" under "System Info" → "Maintenance" in
   the admin UI. See :ref:`semantic-search-migration` (in :doc:`../config/search-semantic`) for
   details.

1. Verify existing crawl schedules
2. Execute "Default Crawler" from "System" → "Scheduler"
3. Wait for crawl to complete
4. Verify search results

.. warning::

   Re-indexing rebuilds the index with the new mapping, so it fails on an OpenSearch without the
   k-NN plugin. Review the notes in Step 4.

15.8-Specific Migration Tasks
=============================

If you are upgrading from 15.7 or earlier to 15.8, the following tasks may be required depending
on which features you use.

If You Were Using Semantic Search
---------------------------------

The ``fess-webapp-semantic-search`` plugin, which provided semantic search in 15.7 and earlier,
is no longer needed (deprecated) because this functionality is now integrated into the core in
15.8. You need to remove the plugin, remove ``-Dfess.semantic_search.*`` and
``-Drank.fusion.searchers=default,semantic``, and detach the old ingest pipeline. For the
procedure, see :ref:`semantic-search-migration` (in :doc:`../config/search-semantic`).

If You Were Using AI Search Mode (RAG)
--------------------------------------

Starting with 15.8, AI search mode (RAG) functionality has been split out into plugins such as
``fess-llm-ollama``, ``fess-llm-openai``, and ``fess-llm-gemini``. Install the plugin that
corresponds to the provider you use from "System" → "Plugins" in the admin UI.

Updating Plugin Versions
------------------------

Plugins installed under ``app/WEB-INF/plugin/`` need to be replaced with versions matching your
|Fess| version. If you specify ``FESS_PLUGINS`` in the Docker version, update the version part,
for example to ``fess-ds-wikipedia:15.8.0``.

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

For the Docker version, revert to the old version's Compose files, then restore the volume
contents::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down
    $ PROJECT=$(basename "$(pwd)")
    $ docker run --rm -v ${PROJECT}_search01_data:/data -v $(pwd):/backup ubuntu \
        sh -c "rm -rf /data/* && tar xzf /backup/search01-data-backup.tar.gz -C /"
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   Configuration data downloaded from the admin screen can be re-imported after starting |Fess|
   via the upload feature on the "System Info" → "Backup" page. You can upload ``*.bulk`` files,
   ``*.properties`` files starting with ``system``, ``*.xml`` files starting with ``gsa``,
   ``*.json`` files starting with ``fess``, and ``*.json`` files starting with ``doc`` — one file
   per operation. ``*.ndjson`` files such as search logs are not accepted and result in an error.

.. warning::

   Uploading ``fess.json`` or ``doc.json`` overwrites the index definition files bundled with
   |Fess| itself. If you upload the ``fess.json`` or ``doc.json`` from an older version after
   upgrading, you lose the new version's index settings and mapping. Do not upload these files
   except for rollback purposes.

.. note::

   The uploaded ``system.properties`` is loaded into memory only and is not written back to a
   file, so its contents are lost when |Fess| is restarted. To restore it reliably, place the
   backed-up file directly in its proper location before starting |Fess| (``app/WEB-INF/conf/``
   for the TAR.GZ/ZIP version, ``/etc/fess/`` for the RPM/DEB version).

.. note::

   The import runs asynchronously; the screen only shows that it has started. Check
   ``fess.log`` to confirm whether it actually succeeded.

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

A: Each version of |Fess| requires a specific version of OpenSearch.
|Fess| 15.8 requires OpenSearch 3.8.0.
The |Fess| OpenSearch plugins such as ``opensearch-analysis-fess`` must exactly match the
OpenSearch version, so if you upgrade OpenSearch, also update the plugins to the corresponding
version (3.8.0).

Also, |Fess| 15.8 requires the k-NN plugin and always sends ``knn.derived_source.enabled`` in the
index settings. With an older OpenSearch, creating a new index fails, so upgrading OpenSearch is
effectively required. See Step 4 for details.

Q: Do I need to recreate the index?
------------------------------------

A: For a |Fess| minor version upgrade (15.x → 15.8) where you do not use chunk-vector search, it
is usually not necessary. The existing index can continue to be used as-is, and settings such as
``content_chunker.enabled`` remain disabled by default, so behavior does not change.

Recreation and re-indexing are required in the following cases:

- **Newly enabling chunk-vector search (semantic search)**: The existing index does not pick up
  the new mapping, so re-indexing is required. See :ref:`semantic-search-migration` (in
  :doc:`../config/search-semantic`) for details.
- **Upgrading from 14.x**: Because OpenSearch undergoes a major version upgrade from 2.x to 3.x,
  recreating the index is recommended.

.. warning::

   Operations that create a new index (including re-indexing) fail on an OpenSearch without the
   k-NN plugin. Review the notes in Step 4.

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
- :doc:`../config/search-semantic` - Chunk-vector search (semantic search) configuration and migration steps
- Check release notes for new features
