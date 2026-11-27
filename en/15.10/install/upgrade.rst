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

- Fess 14.x → Fess 15.10
- Fess 15.x → Fess 15.10

.. important::

   |Fess| 14.x supports the OpenSearch 2.x series, while |Fess| 15.10 supports OpenSearch 3.10.0.
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
- :doc:`prerequisites` - |Fess| 15.10 system requirements (Java and OpenSearch versions)

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
     failure URLs, job logs, and the thumbnail queue (25 indices in total up to 15.8; 15.9 adds the
     ``tag_type`` index that holds user tags, for 26; 15.10 adds the ``session`` index, for 27 in the
     ``fess_config`` alias, but the file holds no session record, see :ref:`The fess_config.session Index for Sessions <upgrade-1510-session-index>`)
   - ``fess_user.bulk`` - Users, roles, and groups
   - ``system.properties`` - System settings, including general configuration
   - ``fess.json`` - Index settings (shard count, ``index.knn``, and so on)
   - ``doc.json`` - Document mapping (field definitions)

   .. note::

      ``fess_config.bulk`` already includes everything in ``fess_basic_config.bulk``. For a
      configuration backup before upgrading, ``fess_basic_config.bulk``, ``fess_user.bulk``, and
      ``system.properties`` are sufficient. However, if the source is 15.9 or later and you use user tags, also download ``fess_config.bulk``: the ``tag_type`` index that holds the user tags is not part of ``fess_basic_config.bulk`` (see :doc:`../admin/tagtype-guide`).

   .. note::

      Log data such as search logs and click logs (``search_log.ndjson``, ``click_log.ndjson``,
      ``favorite_log.ndjson``, ``user_info.ndjson``; 15.9 also offers ``chat_log.ndjson``) can also
      be downloaded from the same page.
      They are not needed if you only want to back up the configuration. Note that these
      ``*.ndjson`` files cannot be restored by uploading them on the backup page (see "Rollback
      Procedure").

2. **Configuration File Backup**

   ZIP version::

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
      ``SEARCH_ENGINE_HTTP_URL``, and ``FESS_DICTIONARY_PATH``. For the ZIP version, the
      equivalent settings are in ``bin/fess.in.sh``.

3. **Customized Configuration Files**

   If you have customized configuration files, back up those as well::

       $ cp /path/to/fess/app/WEB-INF/classes/log4j2.xml /backup/
       $ cp /path/to/fess/lib/classes/tomcat_config.properties /backup/

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

The ZIP version does not include a stop script. If you started ``bin/fess`` with the
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

.. warning::

   Make sure |Fess| has stopped before you start Step 3, and do not replace the package or the files
   of a |Fess| that is still running. After the DEB package of a running 15.8 |Fess| was replaced
   by the 15.10 one, the search screen answered ``404`` until |Fess| was restarted. For the package
   versions, check with ``systemctl status fess.service``.

Step 3: Install New Version
============================

The procedure varies depending on the installation method.

ZIP Version
------------------

1. Download and extract the new version::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.10.0/fess-15.10.0.zip
       $ unzip fess-15.10.0.zip

   .. note::

      |Fess| archives are distributed only in ZIP format (``fess-15.10.0.tar.gz`` is not
      provided).

2. Copy configuration from the old version::

       $ cp /path/to/old-fess/app/WEB-INF/conf/system.properties /path/to/fess-15.10.0/app/WEB-INF/conf/
       $ cp /path/to/old-fess/app/WEB-INF/classes/fess_config.properties /path/to/fess-15.10.0/app/WEB-INF/classes/
       $ cp /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.10.0/bin/

   .. warning::

      Copied whole, ``fess_config.properties`` and ``fess.in.sh`` keep their old values, including
      values whose default changed in 15.9: jobs created afterwards default to Groovy, for example.
      Before running the last two commands, compare each file with the one in ``fess-15.10.0`` and
      carry over only the values you changed yourself. See :ref:`upgrade-159-carried-over-config`
      (from 15.8) and :ref:`upgrade-1510-carried-over-config` (from 15.9) for what to check.

3. If you have customizations, also copy the following::

       # Tomcat settings (the SAML setting tomcat.sameSiteCookies=none is kept here)
       $ cp /path/to/old-fess/lib/classes/tomcat_config.properties /path/to/fess-15.10.0/lib/classes/
       # Installed plugins
       $ cp -r /path/to/old-fess/app/WEB-INF/plugin/. /path/to/fess-15.10.0/app/WEB-INF/plugin/
       # Themes you uploaded yourself (one directory per theme; never bootstrap)
       $ cp -r /path/to/old-fess/app/themes/<your-theme> /path/to/fess-15.10.0/app/themes/

   .. warning::

      Without ``tomcat_config.properties`` from the old installation, ``tomcat.sameSiteCookies``
      silently returns to the default ``lax``, and SAML login stops working (see
      :ref:`upgrade-159-saml`). The shipped 15.10 file differs from the one of 15.8.0 and 15.9.0
      only by commented-out ``tomcat.compression`` and ``tomcat.compression.mime`` lines, so the
      old file can still be copied as it is.

   .. warning::

      Do not copy ``log4j2.xml`` over the 15.10 file. The 15.10 file keeps the ``RequestLoggingFilter``
      logger at ``warn``, and a file copied from 15.8 removes that setting: with the log level at
      DEBUG, the request headers (including ``Authorization``) and the request parameters (including
      the password typed on the login form) are then written to the log. Compare the two files with
      ``diff`` and reapply only the changes you made yourself to the 15.10 file.

   .. warning::

      Do not copy the whole ``app/themes/`` directory. It also holds ``bootstrap``, the theme
      bundled with |Fess|, and copying it over the 15.10 one replaces the 15.10 search screen with
      the 15.8 version of the theme. Copy only the directories of themes you created yourself.
      For a theme published by the |Fess| project, install the build for 15.10 instead, with
      ``bin/fess-setup install theme <name>`` (see :doc:`fess-setup`).

   .. warning::

      Do not copy JSPs (``app/WEB-INF/view/``) edited via "Design" in the admin UI. The search
      screen of 15.10 is a theme and no longer uses those JSPs; see
      :ref:`upgrade-159-static-theme` for where such changes go now.

   .. note::

      Plugins copied from ``app/WEB-INF/plugin/`` were built for the old version. After copying
      them, run ``bin/fess-setup upgrade plugins`` in ``fess-15.10.0`` to replace each one with the
      version built for 15.10; see :ref:`upgrade-plugin-versions`.

4. Verify configuration differences and adjust as necessary

RPM/DEB Version
---------------

Install the new version package::

    # RPM
    $ sudo rpm -Uvh fess-15.10.0.rpm

    # DEB
    $ sudo dpkg -i fess-15.10.0.deb

.. note::

   For the RPM version, the configuration files under ``/etc/fess/*`` are registered as
   ``%config(noreplace)``, so they are retained across upgrades (the new default files are placed
   alongside them with a ``.rpmnew`` suffix). If new configuration options have been added,
   manual adjustment may be necessary. A ``/etc/fess/fess_config.properties`` that you modified
   keeps its old values in 15.10, just as a file copied in the ZIP procedure does; see
   :ref:`upgrade-159-carried-over-config` and :ref:`upgrade-1510-carried-over-config`.

.. warning::

   For the DEB version, the files under ``/etc/fess`` (such as ``fess_config.properties`` and
   ``tomcat_config.properties``) are registered as conffiles, like ``/etc/default/fess``,
   ``/etc/init.d/fess``, and ``/usr/lib/systemd/system/fess.service``. On the first upgrade from
   15.8, ``dpkg`` treats them as follows:

   - A file you never edited is replaced with the 15.10 file without a question.
   - For a file you edited, ``dpkg`` asks. If you keep your file (the default answer, or
     ``--force-confold``), the 15.10 file is placed beside it as ``<file name>.dpkg-dist``. If you
     install the new file (``Y`` or ``--force-confnew``), your file is saved as
     ``<file name>.dpkg-old``.
   - ``dpkg -i`` and ``apt-get install -y`` stop at the first question when nobody can answer it.
     For an unattended upgrade, pass ``--force-confold`` (``--force-confdef`` also avoids the
     questions), for example ``sudo dpkg --force-confold -i fess-15.10.0.deb`` or
     ``sudo apt-get install -y -o Dpkg::Options::=--force-confold ./fess-15.10.0.deb``.

   Back up ``/etc/fess`` first (Step 1) in any case. A file you keep still has its 15.8 values, so
   compare it with the ``.dpkg-dist`` file instead of using it as it is (see
   :ref:`upgrade-159-carried-over-config`). Note that ``/etc/fess/system.properties`` is a
   runtime-generated file not included in the package, so it is not overwritten.

Docker Version
--------------

1. Obtain Compose files for the new version::

       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.10.0/compose/compose.yaml
       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.10.0/compose/compose-opensearch3.yaml

2. Pull new images::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

.. _upgrade-opensearch:

Step 4: Upgrade OpenSearch
==========================

|Fess| 15.10 supports OpenSearch 3.10.0. If the OpenSearch you connect to is older than that,
upgrade it using the following procedure.

.. note::

   This procedure applies when you are managing OpenSearch manually on a ZIP or RPM/DEB
   installation. For the Docker version, pulling the new images in Step 3 updates OpenSearch and
   its plugins together, so this step is not required, as long as the Compose files come from the
   15.10 tag (``v15.10.0``, as in Step 3). With Compose files that are still on a 15.9 tag, the
   images stay at |Fess| 15.9.0 and OpenSearch 3.9.0; change both image tags together (or use the
   15.10 files), because |Fess| and OpenSearch of different releases are not a supported pair.
   The volume names do not change, so the volumes of OpenSearch 3.9.0 start under 3.10.0 without
   any migration step. The move is one way: see "Rollback Procedure" for going back.

.. important::

   Regardless of whether you use chunk-vector search (semantic search), |Fess| 15.10 always
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

   A snapshot taken on OpenSearch 3.10.0 cannot be restored to OpenSearch 3.9.x or earlier, and
   OpenSearch 3.9.x does not start on a data directory that a 3.10.0 node has opened. Keep the
   snapshot you took before the upgrade in case you need to roll back (see "Rollback Procedure").

   |Fess| 15.10 does not check which OpenSearch 3.x version it runs on: it was observed to start and
   search on an unchanged OpenSearch 3.9.0, and ``bin/fess-setup check`` warns only when the nodes
   of a cluster run different versions. This combination is not supported. The |Fess| plugins of
   OpenSearch must be built for the version of OpenSearch they run in (3.10.0 for |Fess| 15.10).

1. Install the new version of OpenSearch

   For the ZIP version, the OpenSearch home must end up at the same absolute path as the old
   one; see :ref:`ZIP version: keep the OpenSearch home at its old path <upgrade-opensearch-zip-path>` below before you move any data. The RPM/DEB
   packages keep the dictionary directory at ``/etc/opensearch/dictionary``, which is the same
   path before and after the upgrade, so nothing special is needed there. Upgrading the RPM/DEB
   package of OpenSearch does not need ``OPENSEARCH_INITIAL_ADMIN_PASSWORD``; the variable is needed
   only for a fresh installation of the package.

2. Reinstall plugins. Remove the four plugins of the old version first if the OpenSearch directory
   already holds them (``bin/fess-setup install opensearch`` installs the four plugins, too)::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin remove analysis-fess
       $ sudo /usr/share/opensearch/bin/opensearch-plugin remove analysis-extension
       $ sudo /usr/share/opensearch/bin/opensearch-plugin remove minhash
       $ sudo /usr/share/opensearch/bin/opensearch-plugin remove configsync

   Then install the plugins of the new version::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install https://maven.codelibs.org/release/org/codelibs/opensearch/opensearch-analysis-fess/3.10.0/opensearch-analysis-fess-3.10.0.zip
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install https://maven.codelibs.org/release/org/codelibs/opensearch/opensearch-analysis-extension/3.10.0/opensearch-analysis-extension-3.10.0.zip
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install https://maven.codelibs.org/release/org/codelibs/opensearch/opensearch-minhash/3.10.0/opensearch-minhash-3.10.0.zip
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install https://maven.codelibs.org/release/org/codelibs/opensearch/opensearch-configsync/3.10.0/opensearch-configsync-3.10.0.zip

   .. note::

      The version of these plugins must match the version of OpenSearch you use. |Fess| 15.10
      supports OpenSearch 3.10.0. Installation fails if the versions do not match.

      The four |Fess| plugins are published on maven.codelibs.org, so they are installed by URL. The
      ``groupId:artifactId:version`` form of ``opensearch-plugin install`` looks only at Maven
      Central.

   .. warning::

      If a plugin directory already exists, ``opensearch-plugin install`` fails with ``plugin directory [...] already exists`` and leaves the old plugin in place. OpenSearch 3.10.0 then refuses to start with ``Plugin [...] was built for OpenSearch version 3.9.0 but version 3.10.0 is running``. ``bin/fess-setup install opensearch-plugins`` keeps a plugin that is already installed at the requested version; for a plugin of another version it prints the plugin name, the installed and the requested version and the ``opensearch-plugin remove`` command to run, and exits with code ``1``. Remove the old plugins as shown above before you install the new ones.

      ``opensearch-plugin install`` asks for confirmation (``Continue with installation?``) for a
      plugin that requests additional permissions. Where nobody can answer, such a plugin is not
      installed: with input from ``/dev/null`` (or ``sudo`` without a terminal), the command exits
      with code ``1`` after a few seconds with
      ``IllegalStateException: unable to read from standard input``, and with an input that stays
      open but never answers, it waits and does not finish. Answer ``y``, or pass ``--batch``
      (``-b``) to skip the question.

3. Move the dictionary directory under the OpenSearch configuration directory

   OpenSearch 3.8.0 and later refuse to create an index when dictionary files are outside the OpenSearch configuration directory.
   If, following the earlier instructions, ``configsync.config_path`` points outside the configuration directory, such as ``/var/lib/opensearch/data/config/`` (``/path/to/opensearch/data/config/`` for the ZIP version),
   |Fess| cannot create its indices and does not start.
   For the RPM/DEB version, copy the dictionary files to ``/etc/opensearch/dictionary/`` as follows::

       $ sudo install -d -o opensearch -g opensearch -m 0750 /etc/opensearch/dictionary
       $ sudo cp -a /var/lib/opensearch/data/config/. /etc/opensearch/dictionary/
       $ sudo chown -R opensearch:opensearch /etc/opensearch/dictionary

   Then change both ``configsync.config_path`` in ``/etc/opensearch/opensearch.yml`` and ``FESS_DICTIONARY_PATH`` of |Fess| (``/etc/sysconfig/fess`` for the RPM version, ``/etc/default/fess`` for the DEB version) to ``/etc/opensearch/dictionary/``.
   For the ZIP version, use ``config/dictionary/`` of OpenSearch. For details, see :doc:`install-linux`.

4. Start OpenSearch::

       $ sudo systemctl start opensearch.service

.. _upgrade-opensearch-zip-path:

**ZIP version: keep the OpenSearch home at its old path**

.. warning::

   The analyzer settings of an existing index (the ``*_path`` settings) hold the absolute path of
   the dictionary files, for example ``/path/to/fess-15.9.0/opensearch/opensearch-3.9.0/config/dictionary/ja/mapping.txt``.
   OpenSearch opens such an index only when that path is inside its own configuration directory.
   If you install OpenSearch 3.10.0 in another directory, as ``bin/fess-setup install opensearch``
   does (it creates ``opensearch-3.10.0`` beside ``opensearch-3.9.0``), and then move ``data/`` and
   the dictionary files there by hand, the document index and ``fess_suggest_analyzer``, which
   also keeps the absolute ``*_path`` settings of 15.9.0, stay unassigned (``Resource path must
   be inside config directory`` in the allocation explanation) and the cluster is red. The same
   happens when you copy ``data/`` into a home that has already been started once. "Re-indexing"
   in Step 7 does not create ``fess_suggest_analyzer`` again. The same happens when a snapshot taken
   on 15.9.0 is restored into a new 15.10 installation whose OpenSearch home is at another path: the
   restored document index is red with ``Resource path must be inside config directory``. Restore it into an
   engine at the old path, or re-index the documents instead of restoring the document index. The procedure below puts the new
   engine at the path the indices were created with:

   1. With OpenSearch stopped (Step 2), install OpenSearch 3.10.0 and its plugins in another
      directory (for example with ``bin/fess-setup install opensearch`` in ``fess-15.10.0``), and do
      not start it. Copy ``data/`` and ``config/dictionary/`` of the old home into it::

          $ OLD=/path/to/fess-15.9.0/opensearch/opensearch-3.9.0
          $ NEW=/path/to/fess-15.10.0/opensearch/opensearch-3.10.0
          $ mkdir -p $NEW/data $NEW/config/dictionary
          $ cp -a $OLD/data/. $NEW/data/
          $ cp -a $OLD/config/dictionary/. $NEW/config/dictionary/

   2. Move the old home away, outside the ``opensearch/`` directory (keep it until the upgrade is
      done; two OpenSearch directories under ``opensearch/`` leave ``FESS_DICTIONARY_PATH`` unset in
      ``bin/fess.in.sh``), and put the new home at the old path. The directory name keeps the old
      version number::

          $ mv $OLD /path/to/opensearch-3.9.0-orig
          $ mv $NEW $OLD

   3. In ``config/opensearch.yml`` of the moved home, set ``configsync.config_path`` back to the old
      absolute path (the full path of ``$OLD/config/dictionary``, not the variable). For |Fess|,
      set ``FESS_DICTIONARY_PATH=dictionary/`` (with the trailing slash), which is relative to the
      configuration directory of OpenSearch, rather than the old absolute path. With the old
      absolute value, every index that "Re-indexing" creates in Step 7 stores absolute ``*_path``
      settings again; with ``dictionary/``, the new indices store relative ones and are green and
      searchable next to the old indices. A fresh ``bin/fess-setup install opensearch`` of 15.10
      also sets ``dictionary/``. Set it explicitly (environment variable or ``bin/fess.in.sh``),
      because ``bin/fess.in.sh`` sets it on its own only for an OpenSearch under ``opensearch/`` in
      the |Fess| directory: with the ``bin/fess.in.sh`` of 15.9.0 copied in Step 3 and nothing
      set, ``FESS_DICTIONARY_PATH`` is unset in this layout, and "Re-indexing" in Step 7 logs
      ``Failed to create index`` and creates nothing.

   4. Start OpenSearch from ``$OLD``, ask it to retry the allocation of shards that failed (needed
      when the cluster is red because OpenSearch was started at another path before), and check
      the health::

          $ curl -X POST "http://localhost:9200/_cluster/reroute?retry_failed=true"
          $ curl "http://localhost:9200/_cluster/health"

Step 5: Start New Version
==========================

ZIP version::

    $ cd /path/to/fess-15.10.0
    $ ./bin/fess -d -p /path/to/fess-15.10.0/fess.pid

.. note::

   Specifying ``-p`` creates a PID file, which lets you stop |Fess| the next time with
   ``kill $(cat /path/to/fess-15.10.0/fess.pid)``.

RPM/DEB version::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

Docker version::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Step 6: Verify Operation
=========================

1. **Check Logs**

   Verify there are no errors.

   ZIP version::

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

   If you keep a document index created by 15.8 or earlier, also see
   :ref:`upgrade-reindex-new-fields`.

.. warning::

   OpenSearch 3.9.0 and later, including the 3.10.0 that 15.10 uses, refuse dictionary entries that
   15.8 accepted, such as the same ``mapping`` entry saved twice or a ``kuromoji`` token that
   contains a space. With such an entry, "Re-indexing" does not create the new document index:
   ``fess.log`` only says ``Failed to create index``, and the old index keeps serving searches.
   Download the dictionary under "System" → "Dictionary",
   remove the duplicate or invalid lines, upload it again, and run "Re-indexing" again. See
   :ref:`upgrade-159-api-requests` for the entries that 15.10 no longer saves.

1. Verify existing crawl schedules
2. Execute "Default Crawler" from "System" → "Scheduler"
3. Wait for crawl to complete
4. Verify search results

.. warning::

   Re-indexing rebuilds the index with the new mapping, so it fails on an OpenSearch without the
   k-NN plugin. Review the notes in Step 4.

Upgrading from 15.9 to 15.10
============================

The changes in this section apply to every upgrade to 15.10. If you are upgrading from 15.8 or earlier, also read the section "Upgrading from 15.8 to 15.10" that follows.

.. _upgrade-1510-client-ip:

Client IP Address Recorded in Logs
----------------------------------

Up to 15.9, the ``ip`` field of the audit log and the ``clientIp`` field of the search log recorded the value of the request's ``X-Forwarded-For`` header as is, regardless of where the request came from. If it held several addresses, all of them were recorded, and a client could send any value.
15.10 determines the address by the same rules as rate limiting (:doc:`../config/rate-limiting`). Only when the source of the request is in ``rate.limit.trusted.proxies`` (default ``127.0.0.1,::1``) does it use ``X-Forwarded-For`` (all lines, if it is split across several header lines) and ``X-Real-IP``. ``X-Forwarded-For`` is read from the right, and the first address that is not a trusted proxy is recorded. Otherwise the address of the source is recorded. These rules also apply when ``rate.limit.enabled`` is ``false``.

Behind a reverse proxy that is not in ``rate.limit.trusted.proxies``, every request is recorded with the address of the proxy. To record the address of the original client, add the address of the proxy to ``rate.limit.trusted.proxies``.

If a request from an address that is not in ``rate.limit.trusted.proxies`` carries ``X-Forwarded-For`` or ``X-Real-IP``, 15.10 writes a warning to ``fess.log`` that names the address of the source and ``rate.limit.trusted.proxies``. The warning is written once after startup, not for every request, so it names only the first such address, and it does not contain the value of the header. The header is still ignored, so nothing changes except the log. Because the login form uses the same limits (see "Login Form Rate Limit" below), every client behind such a proxy is counted as one address, and once the failed logins reach the limit, logins from all of them are refused. If you see the warning, add the address of the proxy to ``rate.limit.trusted.proxies``.

.. _upgrade-1510-cipher-key:

Check of ``app.cipher.key``
---------------------------

If ``app.cipher.key`` is blank, 15.10 aborts the startup and writes an error that names the key ``app.cipher.key`` to ``fess.log``. Set a key of 16, 24 or 32 characters, or run ``bin/fess-setup init`` before the first start.
If it is still the value shipped in ``fess_config.properties`` (``___change__me___``), the startup continues and 15.10 writes a warning to ``fess.log``. Job processes such as the crawler do not write it.
The key encrypts values such as the passwords stored in crawl configurations and data store configurations, and the shipped value is public. |Fess| does not change the key by itself. Changing it makes values encrypted with the previous key impossible to decrypt, so set it before you start operating.

.. _upgrade-1510-carried-over-config:

Configuration Carried Over from 15.9
------------------------------------

The ZIP procedure in Step 3 copies ``fess_config.properties`` from the old installation, and an RPM or DEB upgrade keeps a ``/etc/fess/fess_config.properties`` that you modified. 15.10 then runs with the 15.9 values, including those whose shipped value changed in 15.10. The following keys of ``fess_config.properties`` have a different value in 15.10 than in 15.9.0.

.. list-table::
   :header-rows: 1

   * - Key
     - 15.9.0
     - 15.10
     - Effect of keeping the 15.9 value
   * - ``crawler.failure.url.status.codes``
     - ``404,403,410,401``
     - ``404,403,410,401,5xx``
     - A page that answers with an HTTP 5xx status, such as 500, is not recorded as a failure URL; see "Failure URLs: HTTP 5xx and Suspected Zip Bombs" below. Add ``5xx``. A file from 15.8.0 holds ``404,403,410``.
   * - ``crawler.metadata.content.excludes``
     - ``resourceName,X-Parsed-By,Content-Encoding.*,Content-Type.*,X-TIKA.*,X-FESS.*``
     - ``resourceName,X-Parsed-By,Content-Encoding.*,Content-Type.*,X-TIKA.*,tk:.*,X-FESS.*,Content-Length``
     - None. 15.10 removes the names that start with ``tk:``, ``X-TIKA:`` or ``zip:`` and does not add ``Content-Length`` to the content, whether or not the list names them (see "Metadata Names" and "``Content-Length`` Is No Longer Added to the Content" below).
   * - ``crawler.document.html.pruned.tags``
     - ``noscript,script,style,header,footer,aside,nav,a[rel=nofollow]``
     - ``noscript,script,style,template,header,footer,aside,nav,a[rel=nofollow]``
     - With the 15.10 value, the content of a ``<template>`` element is no longer part of the indexed text of an HTML page. With the 15.9 value kept, it is indexed as before. Add ``template`` to take the new behavior; documents already indexed change only when they are crawled again.
   * - ``online.help.name.sereq``
     - ``sereq``
     - ``esreq``
     - The help icon of the "Request to OpenSearch" screen (``/admin/sereq/``) opens ``sereq-guide.html``, which does not exist. Use ``esreq``, the name of the guide of that screen.

15.10 also adds the following keys to ``fess_config.properties``: ``api.search.similar.rate.limit.per.minute``, ``authentication.local.username.policy``, ``crawler.progress.interval``, ``crawler.metadata.content.image.includes``, ``passkey.enabled``, ``passkey.origins``, ``passkey.rp.id``, ``passkey.rp.name``, ``password.changed.check.interval``, ``query.boost.fuzzy.cjk.enabled``, ``query.boost.fuzzy.digit.enabled`` and ``search.result.link.schemes``. They are missing from a file carried over from 15.9, so 15.10 uses the value it ships for each of them and writes a warning to ``fess.log`` the first time it reads the key, once per key. A key that nothing reads in your setup (for example ``passkey.rp.id``, ``passkey.origins`` and ``passkey.rp.name`` while passkeys are off) gives no warning. Nothing breaks; add the keys from the 15.10 file to stop the warnings.

.. _upgrade-1510-failure-url:

Failure URLs: HTTP 5xx and Suspected Zip Bombs
----------------------------------------------

Up to 15.9, a page that answered with HTTP 500 was not indexed and was not recorded as a failure URL, because the default of ``crawler.failure.url.status.codes`` was ``404,403,410,401``. 15.10 adds ``5xx``, which stands for every status from 500 to 599, so such a URL is listed under "System Info" → "Failure URL" (see :doc:`../admin/failureurl-guide` and :doc:`../config/crawler-advanced`). A 503 is recorded after the crawler has given up retrying it.

A ``fess_config.properties`` carried over from 15.9 still holds the old list, and then a page that answers with HTTP 500 is still not recorded. Add ``5xx`` to the list, or compare the file with the one of 15.10, and restart |Fess|. A list that you set yourself is not changed by the upgrade, so add ``5xx`` to it, too, if you want these pages recorded. 15.9 and earlier read every entry of the list as a number and cannot read ``5xx``, so remove it before you roll back (see the warning in :ref:`Rollback Procedure <upgrade-1510-rollback-5xx>`).

A document that the Tika extractor rejects as a suspected zip bomb is now recorded as a failure URL and is not indexed, even when ``crawler.ignore.content.exception`` is ``true`` (the default). Up to 15.9, it was indexed with no content. Other content errors that this setting ignores are unchanged. The extractor takes a document for a zip bomb when its extracted text is longer than ``maxUncompressionSize`` (10,000,000 characters) and also more than ``maxCompressionRatio`` times as long as the bytes it was read from; both are set in ``crawler/extractor+tikaExtractor.xml``. The ratio is 100 (the default of Tika), so an ordinary archive or office document of text, which expands by a factor of a few to a few tens, is indexed whatever its size. Raise ``maxCompressionRatio`` if you have to index a more compressible document, or lower it to be stricter.

.. _upgrade-1510-robots-txt:

Request-rate and Visit-time in robots.txt
-----------------------------------------

Up to 15.9, the ``Request-rate`` and ``Visit-time`` lines of a robots.txt were ignored. 15.10 honors them while robots.txt handling is on (``crawler.ignore.robots.txt`` is ``false``, the default). A site that declares ``Request-rate`` is now paced: |Fess| waits for the interval the rate implies (at most 60 seconds) before the next URL of that origin, so a crawl of that site can take longer. A site that declares ``Visit-time`` is crawled only in that time of day (UTC): a URL of that origin that is dequeued outside it is skipped, is not retried in the same crawl and is not recorded as a failure URL. A crawl job that never runs inside the window does not refresh the documents of that site, and with the default "Delete old documents" setting (``day.for.cleanup``, 3 days) they expire about 3 days after the last crawl that reached them. Schedule the crawl job inside the window. There is no setting that turns off ``Request-rate`` or ``Visit-time`` alone; ``crawler.ignore.robots.txt=true`` turns off all of the robots.txt handling. For the details, see :doc:`../config/rate-limiting`.

.. _upgrade-1510-removed-pages-robots:

Removed Pages and Robots Directives
-----------------------------------

- A page that answers ``410 Gone`` on a re-crawl is removed from the index, as a page that answers ``404`` is. Up to 15.9, its document stayed in the index until it expired ("Delete old documents"), and the URL was recorded as a failure URL.
- A document that has no last modified date (the site sends no ``Last-Modified`` header) is removed from the index when its page answers ``404`` or ``410`` on a re-crawl. Up to 15.9, such a document stayed searchable until it expired. The same now applies when the HEAD request cannot decide, for example when the server answers ``405`` to it.
- A ``404`` or ``410`` answer that removes a document is not recorded as a failure URL. A ``404`` or ``410`` answer for a URL that has no document in the index still is.

These three changes apply to HTTP/HTTPS URLs while "Check Last Modified" is on (the default; see :doc:`../admin/general-guide`).

- A document that is not HTML, such as a PDF or an Office file, is not indexed when its ``X-Robots-Tag`` response header gives ``noindex`` or ``none``. Up to 15.9, only HTML pages were checked. The crawl does not delete a copy that was indexed before; delete it on the Search page (System Info > Search) of the admin console.
- The robots meta tag and the ``X-Robots-Tag`` header are read directive by directive. Up to 15.9, the value was searched for ``none``, ``noindex`` and ``nofollow`` as text, so a page with ``max-image-preview:none`` was not indexed and its links were not followed, and a rule for another crawler such as ``googlebot: noindex`` applied to |Fess|. Both are now ignored.

``crawler.ignore.robots.tags=true``, or ``config.ignore.robots.tags=true`` in the "Config Parameters" of a crawl configuration, turns off both robots changes, as it does for HTML. For how the value is read, see :doc:`../config/crawler-basic`.

.. _upgrade-1510-user-agent:

User Agent Saved by the General Screen
--------------------------------------

The default user agent of the crawler contains the version of |Fess| (``Mozilla/5.0 (compatible; Fess/<version>; +http://fess.codelibs.org/bot.html)``). If you saved "System" → "General" in the admin UI in 15.8 or 15.9, the string shown in the "User Agent" field was stored as ``crawling.user.agent`` in ``system.properties``, and a stored value takes precedence over the default. After the upgrade, the crawler therefore keeps announcing the version it was saved with, not 15.10.

To use the new default, delete the ``crawling.user.agent`` line from ``system.properties`` (``app/WEB-INF/conf/`` of the ZIP package, ``/etc/fess/`` of the RPM/DEB package), or clear the "User Agent" field of the General screen and save it (a blank field removes the key). Saving the screen without clearing the field writes the old value again. This applies wherever ``system.properties`` is carried over to 15.10, such as the ZIP, RPM/DEB and Docker procedures when you keep the file.

.. _upgrade-1510-link-schemes:

Schemes of Search Result Links
------------------------------

15.10 decides the schemes a search result link and a ``/go/`` redirect may use with ``search.result.link.schemes`` in ``fess_config.properties``. The default is the same as the schemes the bundled search screen (the ``bootstrap`` theme) allowed in a fixed list up to 15.9.

::

    search.result.link.schemes=http,https,ftp,ftps,file,smb,smb1,storage,s3,gcs

A search result whose URL has a scheme that is not in the list does not become a link. ``/go/`` answers ``404`` for a document whose URL, after the "Displaying" path mappings, has a scheme that is not in the list (a warning is written to ``fess.log``). Up to 15.9, ``/go/`` redirected to a scheme of your own (such as ``hammerspoon://``) that a "Displaying" path mapping produced. If you use such a scheme, add it to ``search.result.link.schemes`` without the colon. Do not add ``javascript``, ``data`` or ``vbscript``. A blank value allows no scheme. For the format and the behavior, see :ref:`search-result-link-schemes`.

.. _upgrade-1510-session-index:

The ``fess_config.session`` Index for Sessions
----------------------------------------------

15.10 adds an opt-in store that keeps the HTTP sessions in the search engine, so that several |Fess| nodes can share them. It is on only when the environment variable ``FESS_SESSION_STORE`` is ``opensearch`` on the node; without it, every node keeps its sessions in memory as before (see :doc:`../config/session-store`).

Even while the store is off, |Fess| creates the index ``fess_config.session`` at every startup. The index is a member of the ``fess_config`` alias, which is why the alias has 27 indices in 15.10 (26 in 15.9). The index is excluded from the backup export, so ``fess_config.bulk`` holds no session record even while sessions are stored.

.. _upgrade-1510-passkey:

The ``fess_user.passkey`` Index for Passkeys
--------------------------------------------

15.10 adds login of a local user with a passkey (WebAuthn). It is off by default; see :doc:`../config/security-passkey` for the settings.

Even while the feature is off, |Fess| creates the new index ``fess_user.passkey`` at startup, because deleting, creating and renaming a user and the user details page of the administration screen use it. Where |Fess| is not allowed to create indices, create ``fess_user.passkey`` before the upgrade from ``fess_indices/fess_user.passkey.json`` and ``fess_indices/fess_user.passkey/passkey.json`` (the prefix is ``index.user.index``, ``fess_user`` by default). The index does not join the ``fess_user`` alias, so passkeys are not in the ``fess_user.bulk`` backup. After a restore, users register their passkeys again.

.. _upgrade-1510-libraries:

Admin Console and Theme Libraries
---------------------------------

The admin console of 15.10 no longer ships Bootstrap, AdminLTE, jQuery, Popper, moment.js, the date and time pickers or the form validator. It uses its own ``css/admin/admin.css`` and ``js/admin/admin.js`` (plain JavaScript) and Font Awesome 7 Free, and it follows the dark or light setting of the operating system. Nothing changes in the data or the settings. If you added an admin page, a theme tweak or a script that relies on a removed library, change it: ``$``, ``jQuery``, ``moment``, ``.modal()``, ``.tooltip()``, ``.daterangepicker()`` and ``.timepicker()`` are not defined on admin pages. The ``data-toggle`` (``modal``, ``collapse``, ``tab``), ``data-target`` and ``data-dismiss="modal"`` attributes of Bootstrap keep working, a tooltip is the ``title`` text of the browser, and a Bootstrap class that ``admin.css`` does not define has no effect. The "Search Log" screen takes its period from two date-time inputs of the browser; the value sent to the server is unchanged.

A search theme no longer gets Bootstrap, Popper or Font Awesome from the web application root. ``css/bootstrap.min.css``, ``css/font-awesome.min.css``, ``css/fonts/``, ``js/bootstrap.min.js`` and ``js/popper.min.js`` are removed and answer ``404``. The bundled ``bootstrap`` theme carries its own copies under ``themes/bootstrap/assets/vendor/`` (Bootstrap 5.3.9, Popper 2.11.8, Font Awesome Free 7.3.1), and so do the themes of the ``fess-themes`` repository that show icons. Font Awesome 7 keeps the icon names of versions 5 and 6 and, with ``v4-shims.min.css``, the old ``-o`` names (``fa fa-star-o``), and only ``woff2`` fonts are shipped.

A theme that still links a removed file loses its styles, scripts or icons. That includes a theme you created or uploaded yourself on 15.9 and copy into 15.10 as the upgrade procedure describes (see :doc:`../dev/theme-development`):

- For a theme published by the |Fess| project, install a build for 15.10 that carries Font Awesome 7 (``bin/fess-setup install theme <name>``, or "System" → "Theme" → "Install" with the newest version in the list). The version list also shows earlier 15.10 builds; they link the removed ``css/font-awesome.min.css`` and show no icons.
- For a theme of your own, copy the libraries into the theme (for example under ``assets/vendor/``) and link them from ``index.html`` as ``{{themePath}}/assets/vendor/...``.

Other Behavior Changes
----------------------

- "Delete all" in the "Search" and "Crawling Info" screens of the admin UI requires the edit role (``admin-searchlist``, ``admin-crawlinginfo``). Up to 15.9, only the button was hidden: requests from a user who had only a view role (a role with the ``-view`` suffix) were still accepted.
- The converted text (``output``) of a mapping dictionary item is required. Up to 15.9, the admin UI and the admin API accepted an item without it and stored nothing.
- In a search, a single word in double quotes (such as ``"less"``) matches only that word. Up to 15.9, a word at least ``query.boost.fuzzy.min.length`` (default ``4``) long also got fuzzy match conditions, so documents containing ``fess`` also matched ``"less"``. Unquoted words and words with a field specified (such as ``content:"less"``) are unchanged.
- In a search, the value of a ``fields.<name>`` parameter (for example ``fields.label=a"b``) is put into the query as one value: |Fess| escapes ``\`` and ``"`` in it. A client that had escaped the quote itself (``fields.label=a\"b``) used to get the quote back, because the query parser dropped the backslash; in 15.10 the backslash is kept as a character of the value, so send the raw value. A value such as ``x" OR label:"other`` is one value and cannot add a clause. A ``"`` with no partner in the search query ``q`` (for example ``5" pipe``) no longer ends on the error page: the search is retried with the quotes escaped. ``ex_q`` is query syntax and is not escaped.
- A logged-in user is identified by the session, not by a ``userCode`` parameter or cookie that the request carries (for example for the favorite API). An anonymous request still uses the ``userCode`` parameter or cookie it carries, but a code that is the code of a logged-in user is ignored and the client gets an ID of its own.
- ``suggest.popular.word.cache.expire`` is read as seconds, as ``fess_config.properties`` and :doc:`../config/properties` describe. Up to 15.9 the value was used as minutes, so the default ``60`` kept popular words cached for 60 minutes; in 15.10 it is 60 seconds. To keep the longer cache, set a larger value in seconds (``3600`` for 60 minutes). The cache is also cleared after every run of the suggest job.
- Looking up a document by its document ID now applies the virtual host filter, as a search does. Up to 15.9, ``/api/v2/cache/{docId}``, the ``/go/`` redirect, thumbnails, the favorite endpoints and the other lookups by document ID applied only the role filter, so when the roles matched they also answered for a document of another virtual host. In 15.10 such a document is treated as not found. As in a search, a document that has no virtual host value is not returned when a virtual host is resolved for the request. Nothing changes for a request with no virtual host resolved (the default host).
- The suggest job no longer takes words from a document that search hides. It skips a document that has no ``role`` value and a document that has a denied entry (a value that starts with ``role.search.denied.prefix`` (default ``D``) followed by the prefix of a user, group or role, that is ``D1``, ``D2`` or ``DR`` by default). Up to 15.9, the words of such documents were suggested to everyone. A document that has both allowed and denied entries is skipped as a whole, because a suggest request cannot express a denial for one user. Suggest entries already created from such documents expire through the usual purge of old suggest data.
- The login rate limit no longer distinguishes upper and lower case in the user name. Up to 15.9, ``Admin`` and ``admin`` were counted as different user names, so failures spread over different spellings never reached the per-account limit (5 failures). 15.10 counts the spellings as the same account, both for the login form (``/login/``) and for ``/api/v2/auth/login``.
- Calling ``POST /login/changePassword`` without the old password returned HTTP 500 up to 15.9. 15.10 returns a validation error, and the password is not changed.
- A POST to an admin screen form that does not include ``crudMode`` (for example from a script) returned HTTP 500 in 15.9 (15.8 and earlier do not return 500). 15.10 returns a validation error.
- Deleting a plugin only affects files directly in the plugin directory. A name or version that contains ``../`` no longer deletes a file outside the directory; a warning is written to ``fess.log`` instead. Up to 15.9, such a name could delete files outside the directory. Deletion runs in the background, so ``DELETE /api/admin/plugin`` returns ``status`` ``0`` whether or not the deletion succeeds. Check ``fess.log`` for the result.
- When the password of a local user is changed, when the roles or the groups of the user are changed, or when the user is deleted, the other login sessions of that user end at their next check (see below). Up to 15.9 the other sessions stayed open, and only the session that made the change ended (and only for a password change through ``/api/v2``); a change of roles or groups and a deletion ended no session. This applies to a change by the user and to a change by an administrator (user management screen and Admin API). Each session looks up the change in the user index at most once per ``password.changed.check.interval`` seconds (default ``60``; see :doc:`security`), so the other sessions end within that time. Users of LDAP and SSO are not checked. A session opened before the upgrade (only where sessions are persisted or replicated; the default configuration does not keep sessions across a restart) ends if the password is changed after its HTTP session was created; a password changed before the upgrade has no recorded time, so such a session stays open. The field ``password_changed_at`` is added to the user index at startup, so no reindex is needed.
- LDAP login drops the blanks around the typed username before using it. Up to 15.9 the name was used as typed (for example with a blank in front of it) for the session user ID, the audit log and the login attempt limit, so it counted as a second spelling of the same account. Likewise, the cut made by ``ldap.max.username.length`` was applied to the bind only up to 15.9, while the user name, the role search, the permission names and the session kept the uncut name. 15.10 uses the cut name for all of them (see :doc:`../config/ldap-integration`).
- A password that is longer than 72 bytes in UTF-8 is refused when it is set or changed (user management screen, forced password change on the login form, ``/api/v2/auth/password`` and the Admin API), whatever ``password.max.length`` (default ``100``) allows. BCrypt reads only the first 72 bytes, so up to 15.9 a longer password was accepted and then verified against its first 72 bytes only: any ending logged in. Characters other than ASCII take more than one byte (3 bytes for most Japanese, Chinese and Korean characters). The refusal says "Password must be no longer than 72 bytes." (``errors.password_too_long``), and ``/api/v2/auth/password`` returns that key as ``reason`` together with ``max_bytes``. Existing accounts are not affected: login does not check the length, so a password longer than 72 bytes set before the upgrade still logs in. It is still verified by its first 72 bytes only, so change it.
- The ``audit.log`` records of 15.10 differ from 15.9 in three ways (see :doc:`security`). ``ACCESS`` records have the new fields ``method`` (HTTP method) and ``id`` (the ``id`` request parameter, when there is one). A new action ``UPDATE_PASSWORD`` records a password change with the acting user (``user``) and the user whose password was changed (``target``). Admin REST API requests rejected by the access token check are now recorded as ``ACCESS_DENIED``. Check a program that parses ``audit.log`` against these.
- A link on another site to ``/logout/`` no longer ends the session. A browser that follows such a link says so in the ``Sec-Fetch-Site`` header (``cross-site``, or ``same-site`` for another host name of the same site), and |Fess| answers the redirect to the login page without ending the session or writing a logout record. A typed address, a bookmark, a link inside |Fess| and the sign-out of the search screen and the admin console are unchanged. A sign-out link that a portal of your own offers for |Fess| therefore stops working; users sign out from |Fess| itself. Browsers send the header only to HTTPS addresses and ``localhost``, so a |Fess| served over plain HTTP from another host is unchanged.
- An out-of-date edit of a user is refused. The edit form of the user management screen carries the version of the stored user, and so does ``version_no`` in the body of ``PUT /api/admin/user/setting``. If the user was changed after it was read (by another administrator, by the user, or by the deletion of a role or group the user had), nothing is written: the screen shows "The user was changed by someone else. Reload it and try again.", and the Admin API answers HTTP 400 with ``status`` ``1`` and the same message. Up to 15.9, the form and any ``version_no`` of the API were saved over the change. The user list returns the real ``version_no`` of each user, so a value read from ``GET /api/admin/user/settings`` or ``GET /api/admin/user/setting/{id}`` can be sent back; read the user again after a refusal. The version also changes when |Fess| itself writes the user (a login that hashes the password again, ending the other sessions of the user when a passkey is removed, a password change), so a client that reads a user and waits across such a write is refused as well (:doc:`../api/admin/api-admin-user`).
- Two ``POST /api/v2/auth/password`` requests of the same local user that carry the same ``current_password`` and arrive at the same moment no longer both succeed. The password is written only while the stored one is still the verified ``current_password``, so the later request answers ``409`` (``conflict``) and changes nothing; the client has to confirm the current password and try again. Up to 15.9 both answered ``200`` and the last write won (:doc:`../api/api-auth`). This applies to local users only: the password of a user who logs in through the directory (LDAP) is changed in the directory, the current password is not compared with a local hash, and simultaneous requests can still both succeed.
- The password hash algorithm is now a component. The id in a stored ``{id}hash`` value and in ``app.password.algorithm`` is resolved as the DI component ``<id>PasswordEncoder`` (|Fess| registers ``bcryptPasswordEncoder``), so a plugin can supply another algorithm with its own length limit (see :ref:`webapp-plugin-password-encoder`). Nothing changes while ``app.password.algorithm`` is ``bcrypt``. If it names an id without a component (for example after the plugin jar was removed), |Fess| still starts and users whose hash has another id still log in, but users whose hash has that id cannot log in, and setting a password fails with an error that names ``app.password.algorithm``. A fresh installation whose ``index.user.initial_password`` is longer than the algorithm accepts (72 bytes for BCrypt) does not start: it stops before it creates the user index, with a message that names the property. An installation whose ``admin`` user already exists only logs a warning.
- New setting ``authentication.local.username.policy`` (default ``preserved``). |Fess| still compares the names of local users exactly as typed, as in 15.9, so ``Alice`` and ``alice`` are two users. With ``mapped``, creating or renaming a local user on the user management screen or with the Admin API is refused when the name is the same as the name of another user, or a different spelling of an entry of ``authentication.admin.users``, once width, case and Unicode composition are ignored. Login, user IDs, stored names, permissions and indexed documents do not change. For the details and the limits, see :ref:`local-username-policy`.
- Scripts, styles and SVG files of 1 KB or more are sent compressed with gzip by default; 15.9 compressed nothing. Pages and JSON are not compressed. ``tomcat.compression`` (``on`` or ``off``) and ``tomcat.compression.mime`` (types added to the list, comma-separated) in ``tomcat_config.properties`` control it. A ``tomcat_config.properties`` carried over from 15.9 has neither key, so the compression is on. Set ``tomcat.compression=off`` when a reverse proxy in front of |Fess| compresses the responses itself.
- The files of the bundled ``bootstrap`` theme are sent with ``Cache-Control: no-cache`` and an ``ETag``, and a browser asks again with ``If-None-Match`` and gets ``304`` while the file is unchanged. Up to 15.9 they carried ``max-age=86400``, so a browser kept an updated file for up to 24 hours.
- A setting can be given as an environment variable instead of a ``-D`` option: ``FESS_CONFIG_<KEY>`` for a key of ``fess_config.properties`` and ``FESS_SYSTEM_<KEY>`` for a key of ``system.properties`` (the key in upper case, every character other than a letter or digit replaced by ``_``; ``search_engine.password`` is ``FESS_CONFIG_SEARCH_ENGINE_PASSWORD``). A ``-D`` option with a value wins over the variable, and the variable wins over ``fess_config.properties``; a key that ``system.properties`` already has is not overridden. A variable, unlike a ``-D`` option, is not shown by ``ps`` or ``docker top``, and System Info masks its value. In 15.9.0, saving the General screen wrote the values that came from ``FESS_SYSTEM_*`` variables into ``system.properties``, and a key stored there wins over the variable, so after the upgrade a ``FESS_SYSTEM_*`` variable has no effect for any key that a save of the General screen stored in 15.9.0, until that line is removed from ``system.properties``. 15.10 no longer writes a value that comes from a variable when the General screen is saved.
- When a secret (a password, an API key or a secret key) is given as a ``-Dfess.config.<key>`` or ``-Dfess.system.<key>`` option, 15.10 writes a warning to ``fess.log`` at startup that names the key and the variable to use instead, never the value.
- The environment variable ``FESS_SESSION_STORE=opensearch`` keeps the HTTP sessions in the search engine so that several nodes share them. It is off by default (see :ref:`The fess_config.session Index for Sessions <upgrade-1510-session-index>` and :doc:`../config/session-store`).
- ``PUT /api/admin/<name>/setting`` of 19 more admin APIs (for example ``webconfig``, ``fileconfig``, ``dataconfig``, ``role``, ``group``, ``labeltype``, ``pathmap`` and ``scheduler``; not ``tagtype``, ``general``, ``theme`` or ``dict``) refuses a stale ``version_no`` like the user API above, with HTTP 400 and ``status`` ``1``. Up to 15.9 the value was never compared and the lists returned ``-1``, so a script that sends a constant ``version_no`` fails now: send the value read from ``GET /api/admin/<name>/setting/{id}`` and read the setting again after a refusal. Concurrent updates of the same setting are refused as well: of 5 ``PUT`` requests sent at the same time with the same ``version_no``, 1 is applied and the other 4 get HTTP 400 with ``status`` ``1``. Send the update again with the current ``version_no``.
- ``POST /api/admin/webconfig/setting``, ``/api/admin/fileconfig/setting`` and ``/api/admin/dataconfig/setting`` without ``permissions`` store ``{role}guest``. Up to 15.9 they stored no permission. ``PUT`` without ``permissions`` keeps the stored value; in 15.9 it left the field empty.
- The login form, the change password form and the password fields of the user management screen no longer remove blanks at the start and the end of a password. Up to 15.9 they did, while ``/api/v2/auth/login`` and the Admin API did not, so a password with surrounding blanks that was set through the API could not log in through the form. Now every entrance takes the password as typed. A user whose blanks were dropped when the password was saved in 15.9 has to type it without them.
- A regular expression that does not compile is refused on save: the include and exclude patterns of web and file crawl configurations, the paths of a label type and the regular expression of a path mapping. A value saved earlier stays as it is, and cannot be saved again unchanged until it is corrected. In 15.9, a stored path mapping with an invalid regular expression makes every search return no hits (``fess.log`` shows ``PatternSyntaxException`` from ``PathMapping``). 15.10 skips such a mapping: searches return hits, the other path mappings still apply, and ``fess.log`` gets one warning such as ``The regex of the path mapping "(" is not valid, so the mapping is skipped``. Correct or delete the mapping.
- The label menu of the search screen, the label choices of the admin forms and the labelling of crawled documents use every label type. Up to 15.9 only the first ``page.labeltype.max.fetch.size`` (1,000) label types were read, so a label type beyond them was missing from the menu and the forms, and the documents it should label were not labelled. The setting now only sizes the pages of the label type list in the admin console. With more than 1,000 label types, ``/api/v2/ui/config`` is larger (about 45 bytes per label type).
- A permission entry written with full-width characters, such as ``（deny）{user}name`` or ``(deny)｛user｝name`` (as a Japanese keyboard types them), is refused on the permission fields of the admin screens and by the Admin API, with a message that asks for the half-width spelling such as ``(deny){user}name``. Up to 15.9 it was stored as a value that matches nobody, or dropped, so a deny that was meant to hide a document had no effect. The name after the marker is not changed, so a role named in Japanese or with full-width letters is still accepted.
- A permission entry that has an invisible character (a zero-width space, a byte order mark or a control character) where the ``(allow)`` / ``(deny)`` prefix or the name starts, such as ``(deny)<U+200B>{user}name``, is refused with a message that asks to delete the character. Such a character is usually pasted in with the text. Up to 15.9 the entry was saved as a value that matches nobody, or dropped. A character of this kind inside a name, or at its end, is not refused.
- A user who is already signed in and opens ``/login/`` is redirected to the page a login would lead to: the dashboard for an administrator, the first admin screen the roles allow for a user with an admin role, and the search screen for anyone else. An anonymous visitor still gets the login form. To sign in as another account, sign out first. A link on another site to ``/logout/`` (see above) keeps the session and therefore also ends on that page.
- A stored ``{bcrypt}`` hash with the ``$2b$`` prefix (Python's bcrypt and many other systems) or the ``$2y$`` prefix (PHP, ``htpasswd -B``) now verifies like a ``$2a$`` one. Up to 15.9 the login of such a user always failed. New hashes are still written as ``$2a$``.
- While the search engine cannot be reached, the admin console answers ``503`` (500 up to 15.9), and the login form shows a notice that the search engine is not available instead of an error page. ``/go/`` (the link of a search result) also answers ``503`` while the search engine is not available (``404`` up to 15.9). These ``503`` answers carry ``Retry-After: 5``. A connection reset by the search engine is treated as unavailable as well, so the answer is ``503`` instead of ``500``.
- ``engine.status`` of ``GET /api/v2/health`` is ``YELLOW`` while a |Fess| index refuses writes (it has a write block) and was ``GREEN`` up to 15.9. A write block on an index that does not belong to |Fess| is ignored.
- The SAML plugin (``fess-sso-saml``) of 15.10 uses saml4j instead of java-saml. A ``saml.*`` property that the old library had and the new one does not use, such as ``saml.security.digest_algorithm`` or ``saml.sp.contact``, is ignored; one warning that names them is written to ``fess.log``. The OpenID Connect plugin (``fess-sso-oidc``) of 15.10 uses PKCE (S256) by default. Set ``oic.pkce=false`` in ``system.properties`` for an OpenID provider that rejects it (see :doc:`../config/sso-oidc`).
- A call of the admin API or of ``/api/v2`` no longer creates an HTTP session: no ``JSESSIONID`` cookie is set for a call with a valid or an invalid access token, or for an anonymous search through ``/api/v2``. Up to 15.9 each such call created a session. A login through ``/api/v2/auth/login`` still creates its session.
- When a request has no ``Accept-Language`` header, the message of an API refusal is in English, even when the default locale of the server is another language; the error code does not change. Up to 15.9 the message followed the default locale of the server. Send ``Accept-Language`` to get the message in another language.
- A request whose ``Accept-Language`` is ``zh-Hans`` gets Simplified Chinese, and one whose ``Accept-Language`` is ``zh-Hant``, ``zh-HK`` or ``zh-MO`` gets Traditional Chinese. Up to 15.9 these fell back to English.
- An HTML page that declares ISO-8859-1 is decoded as ``windows-1252``, so characters in the range 0x80-0x9F, such as curly quotes and the euro sign, are indexed instead of being dropped. A document crawled before the upgrade keeps its old text until it is crawled again.
- The web authentication and file authentication screens never show the stored password: the field is blank, and saving it blank keeps the stored password. A ``PUT`` of the ``webauth`` or ``fileauth`` admin API without a password is refused with HTTP 400 when the stored password cannot be decrypted.
- The role choices of the user form on the user management screen list every role. Up to 15.9 only the first 1,000 roles were offered.
- The admin screens of an access token show the token as a fixed-length mask instead of its value. Copy the value from the page instead of reading it.

.. _upgrade-1510-new-api:

API added in 15.10
------------------

15.10 adds the following APIs. The OpenAPI changes are additions only, so existing clients keep working unchanged.

- ``GET /api/v2/documents/{docId}/similar``: lists documents with the same content (:doc:`../api/api-similar`). Calls are limited by ``api.search.similar.rate.limit.per.minute`` (default ``30``).
- ``theme_settings`` in ``GET /api/v2/ui/config``: the contents of "Theme Settings" under System > General in the admin screen (:doc:`../api/api-uiconfig`).
- ``GET /api/admin/crawlinginfo/progress``: the progress of each running crawl configuration (:doc:`../api/admin/api-admin-crawlinginfo`).
- ``mime_type``, ``http_status_code`` and ``content_length`` in ``/api/admin/failureurl``: information about the response of the failed URL (:doc:`../api/admin/api-admin-failureurl`).
- ``/api/v2/auth/passkey``: login with a passkey (WebAuthn) and registering, listing and deleting passkeys. Off by default; every endpoint answers ``404`` while it is off (:doc:`../config/security-passkey`).
- ``result_link_schemes`` and ``features.passkey_enabled`` in ``GET /api/v2/ui/config``: the schemes a search result may link to, and whether passkeys are available (:doc:`../api/api-uiconfig`).

.. _upgrade-1510-implicit-fuzzy:

Implicit fuzzy matching now uses the analyzed term
--------------------------------------------------

For a plain term without ``~``, |Fess| adds an implicit fuzzy clause with a small boost when the term is at least ``query.boost.fuzzy.min.length`` characters long (default ``4``; see the note in :doc:`../user/search-fuzzy`). Up to 15.9, the clause compared the typed text as it is with the terms in the index, which are stored in the analyzed form (lowercased and so on). A term with an uppercase letter or a stemmed word was therefore measured as farther from the indexed term than it really was, and it rarely matched.

15.10 analyzes the typed text with the search analyzer before the comparison. A difference in spelling that did not match up to 15.9 now does. On the other hand, a term that contains a digit, such as an order number, a model number or a ticket ID (for example ``ZQFZ15`` or ``zqfz15``), no longer gets the implicit fuzzy clause at all. A term with a digit is usually an identifier, and a fuzzy match would also hit a similarly spelled identifier (such as ``ZQFZ14``). This is a change from 15.9, where an identifier typed in lowercase letters and digits only (such as ``zqfz15``) matched similar identifiers; in 15.10 it matches only itself. An identifier made of letters only (such as ``ABCE`` for ``ABCD``) can still match a similarly spelled identifier. A document that contains the typed term itself usually ranks higher, but a document that contains only the similar identifier is added to the results.

To avoid this for an identifier made of letters only, do one of the following.

- Enclose the term in double quotes (``"ABCD"``). A single quoted word is treated as a phrase and matches only that word (see "Other Behavior Changes" above).
- To remove the implicit fuzzy clause from every search, set ``query.boost.fuzzy.min.length=-1`` in ``fess_config.properties`` and restart |Fess|.

To apply the implicit fuzzy clause to terms that contain a digit as well (an identifier then matches similarly spelled identifiers again), set ``query.boost.fuzzy.digit.enabled`` to ``true`` (default ``false``). The workarounds above then apply to such identifiers too.

Text that contains Han, Hiragana, Katakana or Hangul characters gets no implicit fuzzy clause by default: the bundled ``standard_analyzer`` splits it into two-character tokens, for which ``AUTO`` fuzziness allows no edit. The clause in 15.9 did not match a typo in such text either, so the results normally do not change. If you use an analyzer that does not produce such tokens (for example a morphological analyzer) for ``title`` and ``content``, set ``query.boost.fuzzy.cjk.enabled`` to ``true`` (default ``false``) to apply the clause to such text too.

.. _upgrade-1510-tika:

Apache Tika 4 and ``tika.xml``
------------------------------

15.9.0 used Apache Tika 3.3.2; 15.10 uses Apache Tika 4.2.0.
Tika 4 has no XML configuration file, so |Fess| 15.10 builds the Tika parser in code and no longer reads ``tika.xml``.
The ZIP package, the RPM/DEB packages and the Docker images of 15.10 do not contain the file.

Settings you made in ``tika.xml``, such as ``parser-exclude``, are no longer applied: a parser you excluded there runs again.
If a ``tika.xml`` from an earlier version is in the configuration directory, |Fess| ignores it and writes a warning to ``fess.log`` at startup. Delete the file if it is still there after the upgrade.

- ZIP package: in the ZIP of 15.9 and earlier the file is ``app/WEB-INF/classes/tika.xml``. The startup warning of 15.10 checks both ``app/WEB-INF/classes`` and ``app/WEB-INF/conf``. Delete the file by hand.
- RPM/DEB package: the file is ``/etc/fess/tika.xml``, and the upgrade removes it if you have not edited it. If you have edited it, the upgrade keeps your copy as ``/etc/fess/tika.xml.rpmsave`` (RPM) or ``/etc/fess/tika.xml.dpkg-bak`` (DEB). |Fess| does not read these copies and does not warn about them. Delete them when you no longer need them. If you roll back to the old package, the old ``tika.xml`` is installed again.

.. _upgrade-1510-tika-metadata:

Metadata Names
--------------

Tika 4 renamed many metadata names. For example, ``pdf:charsPerPage`` is now ``pdf:chars-per-page``, ``access_permission:*`` is now ``access-permission:*``, and ``Message:*`` is now ``message:*``.
|Fess| converts the names that Tika's ``LegacyKeyMigrationFilter`` knows back to the Tika 3 names, so an entry of ``crawler.metadata.name.mapping`` that uses one of those names keeps working.
A name that the filter does not convert is passed on with its Tika 4 name. For example, ``protected`` of an Excel file is now ``msoffice:excel:protected-worksheet``. If an entry of ``crawler.metadata.name.mapping`` uses such a name, change it to the Tika 4 name.

Metadata that Tika 4 newly adds is handled like any other metadata: it is added to the content unless ``crawler.metadata.content.excludes`` matches its name.

The exception is the names that start with ``tk:``, ``X-TIKA:`` or ``zip:``, which Tika uses for its own bookkeeping (``X-TIKA:Parsed-By`` of Tika 3 is now ``tk:parsed-by``). |Fess| removes them before they reach the document. They are not restored to the Tika 3 names, and they are not added to the content, whether or not ``crawler.metadata.content.excludes`` lists them. If you map ``X-TIKA:*`` or ``tk:*`` names in ``crawler.metadata.name.mapping`` or use them in a script, you no longer get these values.

Metadata of Images in the Content
---------------------------------

Up to 15.9, all the metadata of an image file (PNG, JPEG, TIFF, GIF, BMP, etc.) was added to the content, so the content of an image was a list of values about its pixels, its color profile and its camera settings.
In 15.10, only the metadata whose name matches ``crawler.metadata.content.image.includes`` is added to the content of a document whose MIME type is ``image/*``. By default, these are the title, description, creator, keywords, comments, copyright and place names of EXIF, XMP and IPTC, the Windows Explorer properties, and the text chunks of a PNG.
The other metadata is still extracted, so it can be used in ``crawler.metadata.name.mapping`` and in scripts. ``crawler.metadata.content.excludes`` also applies to the names that the list matches.

The content of an image that was indexed before the upgrade does not change until the image is crawled again. A re-crawl skips an image that has not changed when "Check Last Modified" (incremental crawling) in :doc:`../admin/general-guide` is on, which is the default, so the content stays as it was. To refresh it, turn "Check Last Modified" off for one crawl, or delete the documents from the index and crawl again.

Tesseract and PDF Properties Files of a Crawl Configuration
-----------------------------------------------------------

If a crawl configuration sets ``config.tika.tesseract.config`` or ``config.tika.pdf.config``, check the properties files, because Tika 4 renamed or removed some properties.
For each key that it cannot apply, |Fess| writes a warning to ``fess-crawler.log`` and ignores the key.

- ``timeoutSeconds`` of the Tesseract file is now ``timeoutMillis``. |Fess| converts ``timeoutSeconds`` into ``timeoutMillis`` (the value multiplied by 1000), but write ``timeoutMillis`` in milliseconds from now on. ``crawler.document.ocr.timeout`` is still in seconds.
- Properties of the PDF file such as ``ocrStrategy``, ``ocrDPI``, ``ocrImageType``, ``ocrImageFormatName``, ``ocrImageQuality``, ``ocrRenderingStrategy``, ``accessChecker`` and ``renderer`` were removed from the ``PDFParserConfig`` of Tika 4. |Fess| ignores them and writes a warning to ``fess-crawler.log``. OCR of PDFs then follows the default of Tika 4: automatic, that is, pages with little text are OCR'd when ``tesseract`` is available and OCR is enabled in |Fess|.
- The location of ``tesseract`` can no longer be set in ``tika.xml``, and ``tesseractPath``, ``tessdataPath`` and ``imageMagickPath`` in the Tesseract file have no effect. ``tesseract`` (and ImageMagick, if you use it) must be found on the ``PATH`` of the crawler process.

Character Encoding Detection
----------------------------

The character set names that Tika 4 reports for text files can differ from 15.9. For example, Shift_JIS is reported as ``windows-31j``, ISO-8859-1 as ``windows-1252``, and EUC-JP as ``x-eucJP-Open``.

``Content-Length`` Is No Longer Added to the Content
----------------------------------------------------

15.8.0 and 15.9.0 added the value of the ``Content-Length`` metadata to the content of a document. For a plain text file the value was ``0``, so the indexed content ended with a space and ``0``.
15.10 does not add ``Content-Length`` to the content, whether or not ``crawler.metadata.content.excludes`` lists it. The value is still extracted, so it can be used in ``crawler.metadata.name.mapping`` and in scripts.
The content of a document that was indexed before the upgrade does not change until the document is crawled again. As for images (see "Metadata of Images in the Content" above), a re-crawl skips a document that has not changed, so turn "Check Last Modified" off for one crawl, or delete the documents and crawl again.

Login Form Rate Limit
---------------------

In 15.9 the limits of ``theme.api.login.rate.limit.*`` applied only to ``/api/v2/auth/login`` and not to the login form of the login page (``/login/``).
In 15.10 the login form uses the same limits and the same counters. When failed logins from the same IP address reach 10 per minute, or the password of the same user name is rejected 5 times from the same IP address, logins from that IP address, or from that combination of IP address and user name, are refused for ``theme.api.login.lockout.seconds`` (900 seconds by default).
When the logins are counted, user names are compared without regard to case, so ``alice`` and ``Alice`` from the same IP address share one count. The user name used for authentication and written to the logs is the one that was typed.
While refused, even the correct password does not log in, and the page shows the same message as for a wrong password. A successful login gives back the slot that the attempt used.
Take the limit into account for scripts that may send a wrong password and for sites where many users share one IP address.

When a reverse proxy adds ``X-Forwarded-For`` as a header line of its own (for example HAProxy's ``option forwardfor``), 15.10 reads all the lines and uses the first address from the right that is not a trusted proxy as the client IP (see :doc:`../config/rate-limiting`). Up to 15.9 only the first line, which is the one the client sent, was read, so a client could choose the address that the rate limit used.

(deny) in the Permission Field of a Crawl Configuration
-------------------------------------------------------

If you write ``(deny)`` followed by a space in the permission field of a crawl configuration or a similar setting, such as ``(deny) {user}name``, 15.9 did not store it as a deny: it stored the text with the space as it was. Opening such a configuration in the admin screen and saving it then turned it into an allow (``{user}name``).
15.10 does not convert such an entry. The admin screens and the admin API refuse a permission entry that has a space after ``(deny)`` or ``(allow)``, or a space before ``{user}``, ``{group}`` or ``{role}``, and report an error on the permission field. Write the entry without spaces, as ``(deny){user}name`` or ``(allow){user}name``. A ``(deny)`` line that has none of ``{user}``, ``{group}`` or ``{role}`` is not stored.

A setting saved in 15.9 or earlier is not repaired automatically, and the admin screen shows the entry as it was stored, with a leading space. Saving it unchanged is refused with the error above. Check the permission field of every crawl configuration that uses ``(deny)``, enter each such line again in the form ``(deny){user}name`` (or ``(allow){user}name``), save it, and crawl again.

Control Characters in audit.log
-------------------------------

In the LTSV format, every control character, and the Unicode line separators NEL, LS and PS, in a field is replaced by a space (a tab by an underscore), so a typed user name cannot start a second record. 15.9 replaced only CR and LF.

Roles of Files Read from ACLs
-----------------------------

For a crawl of a local file system (``file:`` URLs) whose files have ACLs, such as NTFS, with ``file.role.from.file`` left at the default ``true``, 15.9 turned every ACL entry of a file into a role that may read the document, whatever the type or the permissions of the entry. A user who was denied reading, or who was granted only write access, therefore became a reader of the indexed document.

15.10 looks at the type and the permissions of each entry:

- An ALLOW entry that includes read data (``READ_DATA``) gives the user or group the role, as before.
- A DENY entry that includes ``READ_DATA`` gives a denied role: the role with ``role.search.denied.prefix`` (default ``D``) in front of it, the same prefix that SMB crawls use. Search hides the document from that user or group.
- AUDIT and ALARM entries, and entries that do not include ``READ_DATA``, are ignored.

The roles read from POSIX permissions (owner and group) are unchanged.

A document keeps the roles it was indexed with until it is crawled again. To apply the new rules to the documents you already have, run the file crawl again. A re-crawl skips a file that has not changed when "Check Last Modified" is on (the default), so turn it off for one crawl, or delete the documents and crawl again.

LDAP Role Organizational Units and Nested Groups
------------------------------------------------

When |Fess| resolves the permissions of an LDAP / Active Directory user (see :doc:`../config/ldap-integration`), the DN of a group entry decides whether it is a role (permission prefix ``role.search.role.prefix``, default ``R``) or a group (``role.search.group.prefix``, default ``2``). Up to 15.9, an entry was a role when its DN contained the text ``ou=role`` anywhere, so an entry under ``OU=Roles-Requests`` or ``OU=RoleOwners`` was a role, too.

15.10 parses the DN and treats an entry as a role only when one of its ``ou`` components is exactly ``Role`` or ``Roles`` (case-insensitive). Every other entry is a group, and so is an entry whose DN cannot be parsed.

The entries under an OU such as ``OU=Roles-Requests`` therefore get the permission name of a group instead of that of a role (``2name`` instead of ``Rname``), and documents whose permissions hold the old name no longer match the users of those groups. If you relied on such an OU, move the entries into ``OU=Role`` or ``OU=Roles``, or update the permission settings that use the old names, and crawl (or reindex) again.

When ``ldap.group.filter`` is set (it is blank by default), |Fess| uses it to look up the groups that contain the groups of the user (nested groups). Up to 15.9, the DNs of the user's groups were put into that filter without escaping. A DN with an escaped character, such as the comma of ``CN=Sales\, EMEA,...``, did not match, so the nested groups of such a group were silently missing, and a DN that contained characters special to LDAP filters changed the filter. 15.10 escapes the DNs (RFC 4515). The nested groups of such groups are now found, so the users concerned get the permissions of those groups, too.

Roles Sent in a Request Without a Cipher
----------------------------------------

|Fess| can read the roles of a user from a request parameter, header or cookie when the ``roleQueryHelper`` component in ``fess.xml`` sets ``parameterKey``, ``headerKey`` or ``cookieKey``. Each value is expected to be encrypted unless ``encryptedParameterValue``, ``encryptedHeaderValue`` or ``encryptedCookieValue`` is set to ``false`` (all three default to ``true``).

Up to 15.9, a value that was expected to be encrypted was read as plain text when no ``cipher`` was set, so any client could send a role list. 15.10 ignores such a value and writes a warning to ``fess.log`` once after startup. A value whose flag is ``false`` is still read as it is, and a value is still decrypted when a ``cipher`` is set.

If your ``roleQueryHelper`` sets one of the keys without a ``cipher``, set a ``cipher`` and send encrypted values, or set the flag to ``false`` for the values you send unencrypted. The shipped ``fess.xml`` has these settings commented out, so a default installation is not affected.

Changes for Plugin Developers
-----------------------------

The following changes affect plugins that use classes of ``fess-crawler``. Rebuild such a plugin against 15.10 (see :ref:`upgrade-plugin-versions`).

- ``ExtractData`` no longer implements the Tika interfaces (``TikaCoreProperties``, ``HttpHeaders`` and so on). ``ExtractData`` itself declares the string constants ``CONTENT_TYPE`` and ``CONTENT_ENCODING``. ``RESOURCE_NAME_KEY`` is still ``"resourceName"``.
- ``TikaExtractor.setTikaConfig`` and the ``tikaConfig`` component of ``fess.xml`` were removed.
- At the ``debug`` log level, ``CrawlJob`` no longer passes ``-Dorg.apache.tika.service.error.warn=true`` to the crawler, because Tika 4 does not read it.

The 15.10 ``WEB-INF/lib`` also no longer contains the following libraries, which 15.9 shipped. The Tika 3 modules brought them in, and the Tika 4 modules that 15.10 uses do not depend on them. No class in the 15.10 WAR refers to them.

- The removed libraries are JAXB (``jakarta.xml.bind-api``, ``jaxb-core``, ``jaxb-runtime``, ``txw2`` and ``istack-commons-runtime``), ``jempbox``, ``xmpbox`` and ``juniversalchardet``. ``jakarta.activation-api`` and ``angus-activation`` are still included.
- If your plugin uses classes of these libraries, include the libraries in the plugin JAR (for example, with the Maven Shade Plugin). A plugin can rely on classes that the WAR provides, but not on classes of another plugin, and the 15.10 WAR no longer provides these. Classes in ``WEB-INF/lib`` are resolved before those in ``WEB-INF/plugin``, so including a library that the WAR does not contain causes no duplication.
- To check whether a plugin is affected, see whether the classes it needs are in the JARs of the 15.10 ``WEB-INF/lib``. A code path that uses a removed class fails at run time, for example with ``NoClassDefFoundError``; code paths that do not use these classes are not affected.

A plugin or a customization that extends ``PasswordHashHelper`` must be changed. The public constants ``BCRYPT_PREFIX`` and ``BCRYPT_MAX_PASSWORD_BYTES`` and the protected members ``getEncoders``, ``ID_BCRYPT``, ``parseBcryptCost``, ``resolveBcryptCost`` and ``getDummyBcryptHash`` were removed. The BCrypt specifics moved to ``BcryptPasswordEncoder`` (which has ``MAX_PASSWORD_BYTES``), and the inner ``PasswordEncoder`` interface is now the public ``org.codelibs.fess.crypto.password.PasswordEncoder`` (see :ref:`webapp-plugin-password-encoder`).

Plugins Built for 15.9
----------------------

Plugins built for 15.9.0 were installed, started and used for crawling on the 15.10 war without being rebuilt. This is the result of a check, not a guarantee of compatibility, and a plugin that uses classes of ``fess-crawler`` still has to be rebuilt, as described in "Changes for Plugin Developers".

Replace the plugins with the 15.10 versions all the same (see :ref:`upgrade-plugin-versions`). ``bin/fess-setup check`` reports a plugin jar of 15.9.0 as FAIL ("built for another release") and points to ``upgrade plugins``.

In particular, do not keep the 15.9.0 jars of ``fess-storage-s3`` and ``fess-storage-gcs``. These plugins of 15.9.0 do not return an error when listing the storage fails. When the storage cannot be reached, the credentials are wrong or the bucket does not exist, ``/api/admin/storage/list`` of the admin API therefore still answers a successful, empty list, ``{"items":[],"status":0}``. The plugins of 15.10 throw the failure, and 15.10 turns it into an error response. With the old jars left in place, this improvement of 15.10 does not take effect.

Upgrading from 15.8 to 15.10
============================

If you are upgrading from 15.8, the following changes are not backward compatible. If you are
upgrading from 15.7 or earlier, they apply to you as well: read every section from "Removal of the
embedded OpenSearch" through "Applying New Fields and Kana Normalization to an Existing Document
Index" (the embedded OpenSearch, the script engine, the S3 and SSO plugins, the Index Exporter job,
and so on), and then "Migration Tasks by Feature" at the end of this page.

Removal of the embedded OpenSearch
----------------------------------

Up to 15.8, starting ``bin/fess`` without setting ``SEARCH_ENGINE_HTTP_URL`` made |Fess| run an
OpenSearch node inside its own JVM. That configuration is gone in 15.10: the search engine is
always a separate server.

``bin/fess.in.sh`` now sets ``SEARCH_ENGINE_HTTP_URL=http://localhost:9200`` by default. |Fess|
refuses to start when no OpenSearch is reachable. ``bin/fess-setup install opensearch`` installs
one (Linux and Windows only; OpenSearch publishes no macOS build, so use Homebrew or Docker
there).

|Fess| also needs ``FESS_DICTIONARY_PATH`` to match ``configsync.config_path`` in the
``opensearch.yml`` of that OpenSearch; without it, |Fess| cannot create its indices. The 15.10
``bin/fess.in.sh`` (``bin\fess.in.bat`` on Windows) sets it on its own when ``opensearch/`` in the
|Fess| directory holds exactly one OpenSearch installed by ``bin/fess-setup install opensearch``.
For any other OpenSearch, set it as described in :doc:`install-linux` or :doc:`install-windows`.

Removed along with it:

- the ``es/`` directory (``es/modules``, ``es/plugins`` and ``es/data``)
- ``-Dfess.es.dir`` and ``SEARCH_ENGINE_HOME``
- ``bin/module.xml`` and ``bin/plugin.xml``
- the fallbacks to the legacy ``elasticsearch.*`` configuration keys

An engine older than OpenSearch 3 also stops startup now, where 15.8 logged an error and carried
on. Those versions do not implement the ``_shard_doc`` sort that every whole-result-set operation
relies on, and over HTTP such a request hangs rather than failing.

.. warning::

   Index data from an embedded installation cannot be carried over. Build a new external
   OpenSearch server, move the settings with the admin Backup page, and re-crawl. The backup
   covers crawl settings, users and logs; it does **not** contain the crawled documents.

.. note::

   Two things to know when you restore a 15.8 backup onto the new 15.10 server:

   - Jobs are restored only when they are newer than the ones on the server. The bundled jobs that
     you never edited on 15.8 therefore keep their 15.10 JavaScript version. A job that you edited or
     created on 15.8 comes back with the script engine it was saved with, which is ``groovy`` for a
     bundled job, and without the ``fess-script-groovy`` plugin it fails with
     ``groovy is not found``. Install the plugin, or switch such jobs to JavaScript; both are
     described in :ref:`upgrade-159-script-engine`.
   - Passwords and secrets stored in the web authentication, crawling configuration and data store
     settings are encrypted with ``app.cipher.key``. Set the value of the old installation in the
     ``fess_config.properties`` of the new server, as described in
     :ref:`upgrade-159-carried-over-config`; otherwise they cannot be decrypted.

Playwright Crawler Moved to a Plugin
------------------------------------

The Playwright crawler, and the Node.js executables it runs, are no longer part of the
distribution. In ``fess-15.8.0.zip`` (457.1 MiB), the Playwright driver bundle that carried the
Node.js executables took up 204.3 MiB.

If a crawl configuration names the Playwright client, for example with
``client.crawlerClients=playwright:http://.*`` in its configuration parameters, install both the
plugin and Node.js. The plugin is also available from the System > Plugin page in the
administration screen. ``bin/fess.in.sh`` discovers Node.js and sets ``PLAYWRIGHT_NODEJS_PATH``.

::

    $ bin/fess-setup install plugin fess-crawler-playwright
    $ bin/fess-setup install nodejs

Without the plugin, such a configuration is still crawled, but with the plain HTTP client, so
text that only JavaScript produces is not indexed. The crawl job still ends successfully and no
failure URL is recorded. For each crawl, ``fess-crawler.log`` records one warning per crawling
configuration that names the plugin and the two commands above.

The ``fess-thumbnail-playwright`` plugin, which generates thumbnails of HTML pages with
Playwright, runs on Node.js as well. If you use it, install Node.js with
``bin/fess-setup install nodejs``; the same installation serves both plugins.

Nothing is needed if you use neither the Playwright crawler nor the ``fess-thumbnail-playwright``
plugin.

Google Cloud Storage Moved to a Plugin
--------------------------------------

The Google Cloud Storage SDK is no longer part of the distribution, so ``gcs://`` crawling
and the ``gcs`` storage type now come from the ``fess-storage-gcs`` plugin. Install it from the
System > Plugin page in the administration screen, or with the command below.

::

    $ bin/fess-setup install plugin fess-storage-gcs

``gcs`` also left the shipped ``crawler.file.protocols``, which is now
``file,smb,smb1,ftp``; the plugin adds it back when it is installed. Until then a file crawl
configuration whose path begins with ``gcs:`` is logged as a warning and crawls nothing. An
installation that upgrades keeps its own ``crawler.file.protocols``, so the path is still
accepted but no crawler client handles it; on a new installation ``gcs:`` is not a configured
protocol, so the administration screen refuses to save the path and a path saved earlier is
read as a local file path. The storage page logs a warning as well and shows the failure as an
error naming the plugin to install, where before it rendered an empty file list.

Nothing is needed if you do not use Google Cloud Storage. Amazon S3 and S3-compatible
storage such as MinIO moved to a plugin in the same way; see the next section.

Amazon S3 Moved to a Plugin
---------------------------

The AWS SDK is no longer part of the distribution, so ``s3://`` crawling and the ``s3`` and
``s3_compat`` storage types now come from the ``fess-storage-s3`` plugin. Install it from the
System > Plugin page in the administration screen, or with the command below.

::

    $ bin/fess-setup install plugin fess-storage-s3

``s3`` also left the shipped ``crawler.file.protocols``, which is now ``file,smb,smb1,ftp``;
the plugin adds it back when it is installed. ``storage.type`` still defaults to ``auto``,
which resolves to S3 when no endpoint is set, so the storage page in the administration screen
does not work until the plugin is installed even if you never named ``s3`` yourself. Your
``storage.*`` values are kept, because they live in ``WEB-INF/conf/system.properties``, and an
existing ``crawler.file.protocols`` is not replaced by the upgrade either.

Nothing is needed if you do not use Amazon S3 or S3-compatible storage such as MinIO.

SSO Authentication Moved to Plugins
-----------------------------------

None of the four SSO authenticators is part of the distribution any more. Each ``sso.type``
value now comes from its own plugin, which carries the identity library it needs: ``saml`` from
``fess-sso-saml``, ``spnego`` from ``fess-sso-spnego``, ``entraid`` (and the legacy ``aad``)
from ``fess-sso-entraid``, and ``oic`` from ``fess-sso-oidc``. Note the last pair: the plugin is
named ``fess-sso-oidc`` while the ``sso.type`` value stays ``oic``, the one place where the two
differ. Install the one you use from the System > Plugin page in the administration screen, or
with the command below.

::

    $ bin/fess-setup install plugin fess-sso-saml

Your settings are kept, because ``sso.type`` and the ``saml.*``, ``spnego.*``, ``entraid.*``,
``aad.*`` and ``oic.*`` keys live in ``WEB-INF/conf/system.properties``. "System" → "General" in
the admin UI also still offers all four types and still shows their settings, because a plugin
cannot supply a JSP, so nothing on that screen reports a missing plugin.

Until the plugin is installed, a request to ``/sso/`` is redirected back to the login page,
which reports that the SSO login failed, and no one can log in through SSO. 15.10 records a
warning in ``fess.log`` naming the component it looked for and the plugin that provides it,
where up to 15.8 nothing was logged at any level.

The ``oic`` plugin is stricter than the 15.8 authenticator. ``oic.token.server.url`` must be
HTTPS (``http`` only for ``localhost``, ``127.x.x.x`` and ``::1``), the ``aud`` and ``exp`` claims
of the ID Token are checked, and ``iss`` is checked when the new ``oic.issuer`` key is set. See
:doc:`../config/sso-oidc`.

In 15.8, ``oic.token.server.url`` could be an ``http`` URL for any host. In 15.10, ``http`` to a Docker Compose service name (such as ``http://keycloak:8080/...``) or an internal host name is refused, even if it points to the same machine. Login then fails and ``fess.log`` records a warning that starts with ``Failed to process the OpenID Connect callback: oic.token.server.url must be https``. Change the token endpoint to an HTTPS URL before you upgrade.

Also set ``oic.issuer`` to the ``issuer`` value of the OP's Discovery document. Without it, ``iss`` is not checked and a warning is logged at the first login after startup. Setting ``oic.issuer`` does not relax the HTTPS rule.

15.10 also checks the ``nonce`` of the ID Token. A ``nonce`` is sent with every authorization request, and a login is refused when the ID Token has no ``nonce`` claim with the same value. OpenID Connect Core requires the OP to echo the ``nonce``, but an OP that does not can no longer be used to log in, and there is no setting to turn this check off. Before updating, make sure that the OP you use returns the ``nonce`` claim. A login that was started before the plugin was updated fails once; retry it.

Nothing is needed if you do not use SSO, that is if ``sso.type`` is ``none`` or unset.

.. _upgrade-159-script-engine:

The Built-in Script Engine Changed from Groovy to JavaScript
------------------------------------------------------------

Up to 15.8 the built-in script engine was Groovy and ``job.default.script`` defaulted to
``groovy``. In 15.10 the built-in engine is JavaScript and the default is ``javascript``. Groovy is
no longer built in: it is provided by the ``fess-script-groovy`` plugin, which has to be installed
before a ``scriptType`` of ``groovy`` can be resolved.

An upgrade does not change the engine stored with a setting, and a setting saved before 15.10 that
records no engine counts as ``groovy``. Without the plugin, the following stop working:

- Scheduled jobs saved as ``groovy``. **This includes the jobs that 15.8 created itself:**
  Default Crawler, Suggest Indexer, Config Reloader, Log Aggregator, Doc Purger and the other
  bundled jobs are all saved as ``groovy``, and at startup 15.10 only adds the bundled jobs that do
  not exist yet, so it leaves them as they are. Each of them fails whenever its schedule fires, so
  Default Crawler no longer crawls. Most bundled jobs have "Logging" turned off, so their failures
  do not appear in the job log, only as ``Failed to execute job`` warnings in ``fess.log``.
- Web and file crawling configurations with field scripts (``field.script.<field name>``) in
  "Config Parameters". Every document of such a configuration fails with a
  ``ScriptEngineException``, recorded as a failure URL, while the crawl job itself still ends
  successfully.
- Data store configurations with a "Script". Values other than a plain parameter name cannot be
  evaluated; see :doc:`../config/datastore/ds-overview`.
- Document boost rules. Such a rule boosts nothing.
- Path mappings whose "Replacement" begins with ``groovy:``. Such a mapping is not applied, and
  URLs are left unchanged.

After the first start, look in ``fess.log`` for a warning that begins with
``Settings use the script engine groovy, which is not registered``. |Fess| checks the settings
above once at startup and lists how many of each kind use an engine that no plugin provides. It
also names ``job.default.script`` when a ``fess_config.properties`` carried over from 15.8 still
sets ``groovy``, in which case jobs created after the upgrade use Groovy too (see
:ref:`upgrade-159-carried-over-config`). Resolve it in one of two ways:

- Install the plugin and restart |Fess|. The stored Groovy scripts then run unchanged, and the
  warning is no longer logged. The plugin can also be installed from "System" → "Plugins" in the
  admin UI.

  ::

      $ bin/fess-setup install plugin fess-script-groovy

- Move each setting to JavaScript. First rewrite any syntax that only Groovy accepts, then select
  JavaScript:

  - Scheduled jobs: under "System" → "Scheduler", set "Execution Method" to ``javascript``. The
    scripts of the bundled jobs are valid JavaScript as they are, with two exceptions: Thumbnail
    Purger uses the Groovy ``long`` literal ``1000L``, which JavaScript rejects (write ``1000``),
    and Index Exporter needs the change described in :ref:`upgrade-159-index-exporter`. A
    JavaScript array literal is converted to a Java ``String[]`` automatically, so the
    ``as String[]`` casts of the Groovy form are dropped:

    ::

        return container.getComponent("crawlJob").logLevel("info").webConfigIds(["1", "2"]).fileConfigIds(["1"]).dataConfigIds([]).execute(executor);

  - Web and file crawling configurations: add ``config.script.type=javascript`` to
    "Config Parameters".
  - Data store configurations: add ``script_type=javascript`` to "Parameters".
  - Document boost rules: set "Script Type" to ``javascript``.
  - Path mappings: begin the "Replacement" with ``javascript:`` instead of ``groovy:``.
  - ``job.default.script``: set it to ``javascript`` in a ``fess_config.properties`` carried over
    from 15.8.

``crawler.default.script`` Was Removed
--------------------------------------

``crawler.default.script`` no longer exists in ``fess_config.properties``. Remove it from your
configuration; a value left under that name has no effect.

The ``storage`` Crawl Protocol Was Removed
------------------------------------------

``storage`` is no longer accepted in ``crawler.file.protocols``; the shipped value is
``file,smb,smb1,ftp``. Use ``s3`` instead, and change any file crawling configuration whose
path begins with ``storage:`` to an ``s3:`` path. ``s3`` needs the ``fess-storage-s3`` plugin.

.. _upgrade-159-index-exporter:

The Index Exporter Job Names a Removed Package
----------------------------------------------

15.10 no longer ships the ``org.opensearch`` classes; the query builders that job scripts use now
live under ``org.codelibs.fesen.opensearch``. The script that 15.8 stored for the Index Exporter
job names ``org.opensearch.index.query.QueryBuilders``, and the upgrade does not replace it, so
the job fails even with ``fess-script-groovy`` installed. The job ships disabled and without a
schedule, so this only matters if you run it. Open it under "System" → "Scheduler" and change the
package in its script to the one 15.10 uses:

::

    return new org.codelibs.fess.job.IndexExportJob().query(org.codelibs.fesen.opensearch.index.query.QueryBuilders.matchAllQuery()).execute()

Change any script of your own that names ``org.opensearch.index.query`` in the same way. See
:doc:`../config/admin-index-export` for more query examples.

.. _upgrade-159-carried-over-config:

Configuration Files Carried Over from 15.8
------------------------------------------

The ZIP procedure in Step 3 copies ``fess_config.properties`` and ``bin/fess.in.sh`` from the old
installation, and an RPM upgrade keeps a ``/etc/fess/fess_config.properties`` that you modified
(the 15.10 file is placed next to it as ``fess_config.properties.rpmnew``). A DEB upgrade does the
same when you keep your version at the question (the 15.10 file is placed next to it as
``fess_config.properties.dpkg-dist``). Either way, 15.10 then runs with the 15.8 values, including
those whose shipped value changed in 15.10. Review at least the following keys.

.. list-table::
   :header-rows: 1

   * - Key
     - 15.8.0
     - 15.10
     - Effect of keeping the 15.8 value
   * - ``job.default.script``
     - ``groovy``
     - ``javascript``
     - Jobs created under "System" → "Scheduler" default to ``groovy`` and fail without the
       ``fess-script-groovy`` plugin.
   * - ``job.template.script``
     - Groovy form with ``as String[]``
     - JavaScript form
     - A job created from a crawling configuration gets a Groovy script.
   * - ``crawler.file.protocols``
     - ``file,smb,smb1,ftp,storage,s3,gcs``
     - ``file,smb,smb1,ftp``
     - A path beginning with ``s3:`` or ``gcs:`` is still accepted without its plugin and is
       skipped with a warning when crawled. ``storage`` is no longer supported.
   * - ``search_engine.http.url``
     - ``http://localhost:9201``
     - ``http://localhost:9200``
     - Used when ``SEARCH_ENGINE_HTTP_URL`` is not set, as in a ``bin/fess.in.sh`` copied from
       15.8 in which you did not set it. |Fess| then looks for OpenSearch on port 9201, the port
       of the embedded OpenSearch that 15.10 removed.
   * - ``jvm.crawler.options``, ``jvm.thumbnail.options``
     - ``-Djcifs.smb.client.*``, ``-Djcifs.smb1.smb.client.*``
     - ``-Djcifs.client.*``
     - The SMB timeouts stay at the jcifs defaults; see :ref:`upgrade-159-jcifs`.
   * - ``response.headers``
     - Includes the row ``text/html=Content-Security-Policy: reflected-xss block``
     - Row removed
     - The login page, the admin console and the other pages |Fess| renders itself are sent with a
       ``Content-Security-Policy: reflected-xss block`` header that no browser recognizes, and the
       browser console logs ``Unrecognized Content-Security-Policy directive 'reflected-xss'``. The
       header restricts nothing. Remove the row, as described below.
   * - ``app.encrypt.property.pattern``
     - ``.*password|.*key|.*token|.*secret``
     - ``.*password|.*passphrase|.*key|.*token|.*secret``
     - A parameter whose name ends with ``passphrase`` (for example ``ssh.passphrase`` of a data
       store configuration) is saved in plain text. A value saved earlier stays in plain text until
       the setting is saved again with the 15.10 pattern.
   * - ``index.backup.log.targets``
     - ``click_log.ndjson,favorite_log.ndjson,search_log.ndjson,user_info.ndjson``
     - ``chat_log.ndjson,click_log.ndjson,favorite_log.ndjson,search_log.ndjson,user_info.ndjson``
     - The "System Info" → "Backup" page does not offer ``chat_log.ndjson``.
   * - ``index.export.exclude.fields``
     - ``cache``
     - ``cache,tag``
     - The ``tag`` field, which holds user tags, is no longer left out of the files that the Index
       Export job writes.
   * - ``crawler.default.script``, ``theme.allowed.archive.extensions``,
       ``theme.assets.cache.max.age``, ``theme.assets.precompressed``,
       ``rag.chat.message.max.length``, ``supported.uploaded.js.extentions``,
       ``supported.uploaded.css.extentions``, ``supported.uploaded.media.extentions``,
       ``supported.uploaded.files``, ``online.help.name.design``
     - Present
     - Removed
     - No effect; remove them.

The shipped ``response.headers`` of 15.0 through 15.8 contains the row
``text/html=Content-Security-Policy: reflected-xss block``. ``reflected-xss`` was a directive of an
early draft of Content-Security-Policy that browsers no longer recognize, so the header restricts
nothing and only adds the console error. 15.10 no longer ships the row (the ``X-XSS-Protection`` and
``X-Frame-Options`` rows are unchanged), but a ``response.headers`` carried over from 15.8 keeps it.
Remove only this row from ``response.headers`` in ``fess_config.properties``. The ``\n\`` at the end
of each row continues the value on the next line, so deleting the whole line leaves the others
intact::

    text/html=Content-Security-Policy: reflected-xss block\n\

If you set ``response.headers`` with ``-Dfess.config.response.headers`` instead, remove the same
entry from that value.

A ``bin/fess.in.sh`` copied from 15.8 also lacks two things that the 15.10 file has. It leaves
``SEARCH_ENGINE_HTTP_URL`` unset unless you set it yourself, where 15.10 sets
``http://localhost:9200``, and it does not look for the Node.js installed by
``bin/fess-setup install nodejs``, so the Playwright plugins cannot find Node.js unless you set
``PLAYWRIGHT_NODEJS_PATH``.

Rather than copying either file whole, start from the file shipped with 15.10 and reapply the values
you changed. ``diff`` shows them::

    $ diff /path/to/old-fess/app/WEB-INF/classes/fess_config.properties /path/to/fess-15.10.0/app/WEB-INF/classes/fess_config.properties
    $ diff /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.10.0/bin/fess.in.sh

For an RPM upgrade, compare ``/etc/fess/fess_config.properties`` with
``/etc/fess/fess_config.properties.rpmnew`` in the same way, and for a DEB upgrade with
``/etc/fess/fess_config.properties.dpkg-dist``. A ``fess_config.properties`` that you never edited
is replaced by the 15.10 file on a DEB upgrade (see Step 3), so it starts from the 15.10 values.

``app.cipher.key`` is the one value you must carry over even though 15.10 did not change it. It is
the key that encrypts the passwords and secrets stored in the parameters of web authentication,
crawling configurations and data store configurations. The installation you upgrade or restore into
must use the same ``app.cipher.key`` as the installation that saved the data: carry the key over
together with the backup.

If the installation runs with a different key, for example because you took the shipped
``fess_config.properties`` or restored a backup onto a server that uses another key, the stored values
cannot be decrypted: ``fess-crawler.log`` records a ``CipherFailureException``, and a crawl that
includes such a configuration can index nothing.

If even one configuration has a value that cannot be decrypted, the crawl stops at that point. The configuration that cannot be decrypted is not simply skipped;
the other configurations targeted by the same crawl are not indexed either. The message of the ``CipherFailureException`` shows the type, name and ID of that
configuration and the key of the parameter that could not be decrypted, and it also says that ``app.cipher.key`` may differ from the key used when the value was saved
(neither the encrypted value nor the key itself is output). Set ``app.cipher.key`` back to the original value.

To change ``app.cipher.key`` on purpose, re-enter the stored secrets after the change. Open every web
authentication, file authentication, crawling configuration and data store configuration that holds a
password or an encrypted parameter, and enter those values again in plain text in the same setting:
the password field, and each parameter value that starts with ``{cipher}``, replaced by its plain
value. |Fess| encrypts them again with the new key when the setting is saved. Re-enter them in place
instead of deleting the setting and creating it again: a re-created setting gets a new ID, while other
settings (such as the web or file configuration of an authentication) and the crawl schedule refer to
the old one.

.. note::

   |Fess| 15.9 also stores the ``password`` of web and file authentication encrypted with ``app.cipher.key``, so
   ``fess_basic_config.bulk`` and ``fess_config.bulk`` in a backup contain the encrypted values. Restore such a
   backup into an installation that uses the same ``app.cipher.key``; with a different key, crawls that use these
   credentials fail with an error until the original key is set. A backup made before 15.9 holds them in plain text
   and keeps working (see :doc:`../admin/backup-guide`).

.. _upgrade-159-jcifs:

SMB Timeouts Use the jcifs 3 Property Names
-------------------------------------------

jcifs, the library |Fess| uses to crawl SMB file servers, renamed its properties in version 3:
``jcifs.smb.client.*`` became ``jcifs.client.*``, and the separate ``jcifs.smb1.smb.client.*``
names for SMB1 were folded into the same properties. Up to 15.8, ``jvm.crawler.options`` and
``jvm.thumbnail.options`` still passed the old names, which jcifs ignores, so SMB crawls ran with
the jcifs defaults. 15.10 passes the new names:

::

    -Djcifs.client.responseTimeout=30000
    -Djcifs.client.soTimeout=35000
    -Djcifs.client.connTimeout=60000
    -Djcifs.client.sessionTimeout=60000

The connect and session timeouts therefore take effect for the first time and grow from the
jcifs default of 35 seconds to 60 seconds: a crawl now waits up to 60 seconds for an SMB server
that does not respond. The response and socket timeouts equal the jcifs defaults, so they do not
change.

If you changed these timeouts, rename them in both options. Under the old names they had no
effect in 15.8 either. A ``fess_config.properties`` carried over from 15.8 keeps the old names,
and with them the jcifs defaults.

Four Properties Without Effect Were Removed
-------------------------------------------

The following keys no longer exist in ``fess_config.properties``. |Fess| never read them from that
file, so a value left under these names has no effect, as before.

- ``theme.allowed.archive.extensions``
- ``theme.assets.cache.max.age``
- ``theme.assets.precompressed``
- ``rag.chat.message.max.length``

The limit that ``rag.chat.message.max.length`` sets still works, but it is read as a system
property: set it in ``app/WEB-INF/conf/system.properties`` or with
``-Dfess.system.rag.chat.message.max.length``, as described in :doc:`../config/rag-chat`.

.. _upgrade-159-static-theme:

The Search Screen Is Now a Theme
---------------------------------------

The search screen is served by the theme ``bootstrap``, which is bundled with |Fess|, unless
another theme is selected. This applies to ``/``, ``/search``, ``/advance``, ``/help``,
``/profile``, ``/cache``, ``/chat`` and the error pages. Up to 15.8, these pages were JSPs unless a
default theme was set.

The switch happens on upgrade as well. A 15.8 installation that never set a default theme has no
``theme.default`` in ``system.properties``, so after the upgrade it shows the theme; nothing is
written to the configuration and nothing is logged. There is no setting that brings back the JSP
search screen. If you had set a default theme in 15.8, that setting is kept; install the 15.10 build
of the theme (``bin/fess-setup install theme <name>``), because a default that names a theme that is
not installed falls back to ``bootstrap`` with a warning in ``fess.log``.

If you changed the JSPs, CSS or images of the search screen, through "Page Design" in the admin UI
or in a JAR theme plugin, those changes no longer show. Make them in a theme: copy the bundled
theme and change the copy, as described in :ref:`theme-customize-bundled`, or install a published
theme from "System" > "Theme" in the admin UI or with ``bin/fess-setup install theme <name>``. A
per-virtual-host look is now a theme named after the virtual host; see
:doc:`../config/security-virtual-host`.

Two more things are gone:

- The per-virtual-host login screen. Up to 15.8, saving "System" > "General" copied JSPs,
  including the login screen, into ``WEB-INF/view/<virtual host name>/``, where each virtual host
  could edit its own copy. 15.10 no longer makes these copies. The login screen (``/login/``) is
  still a JSP, but every virtual host gets the same one from ``WEB-INF/view/admin/login/``. JSPs
  copied earlier are not used.
- JAR theme plugins (``fess-theme-*``). Installing one only places it as a generic JAR of type
  ``jar``; no screen changes. Delete a leftover JAR on the "System" > "Plugin" page or with
  ``bin/fess-setup remove plugin <name>`` (see :doc:`../dev/theme-development`).

If the JSP search results showed a field of your own in 15.8, add that field to
``query.additional.api.response.fields`` as well as ``query.additional.response.fields``. The theme gets its results from ``/api/v2/search``. ``query.additional.response.fields`` only adds a field
to what is fetched from the search engine; the API returns only the fields listed in
``query.additional.api.response.fields`` (see :doc:`../config/search-advanced`). Change the theme to
show the field as well.

What Clients See
~~~~~~~~~~~~~~~~

Errors are now rendered in place, at the URL that was requested and with the real HTTP status. A
browser (a request whose ``Accept`` header includes ``text/html``) gets the theme's error page; any
other client gets a one-line ``text/plain`` body (for example ``Not Found.`` for ``404``). Up to 15.8, most errors
answered with a ``302`` redirect to an ``/error/...`` page that itself returned ``200``. Review
monitoring, health checks and clients that follow ``Location`` headers or expect ``/error/`` URLs.

.. list-table::
   :header-rows: 1

   * - Request
     - Up to 15.8
     - 15.10
   * - ``/go/`` with a missing parameter, or for a document that does not exist
     - ``200``, or ``302`` to ``/error/``
     - ``400`` or ``404``
   * - ``/thumbnail/`` with a missing parameter, for an unknown document, or with no thumbnail
     - ``200`` or ``302``
     - ``400`` or ``404``
   * - ``/sso/metadata`` and ``/sso/logout`` when the configured SSO type does not handle them
     - ``302`` to ``/error/badrequest/``
     - ``400``
   * - ``/api/v1/*``, ``/json`` and any unknown URL
     - ``302`` to ``/error/notfound/``
     - ``404``
   * - An uncaught exception, including in the admin API
     - ``302`` to ``/error/systemerror/``
     - ``500`` with the body ``System Error.`` (not JSON)
   * - ``/error/notfound/``, ``/error/badrequest/``, ``/error/systemerror/`` themselves
     - ``200``
     - ``404``, ``400``, ``500``

With ``login.required=true``, the search pages no longer redirect an anonymous user. They return
``200`` with the theme, which asks the user to log in, and the data behind them is refused instead:
every ``/api/v2/`` endpoint other than ``/health``, ``/auth/*`` and ``/ui/config``, including
``/api/v2/search``, answers ``401`` until the user logs in. ``/go/``, ``/thumbnail/`` and ``/osdd`` still
redirect to the login. A check that expects a redirect for an anonymous request to ``/`` has to test
``/api/v2/search`` for ``401`` instead.

The search screen also searches through ``/api/v2/search``, so a search is logged when that API is
called, not when ``/search`` is requested. A client that does not run JavaScript receives the page
without results.

The HTML of the search screen carries ``X-Frame-Options: DENY`` and a ``Content-Security-Policy`` with
``frame-ancestors 'none'``, so no other page can show it in a frame. The JSP search screen of 15.8 sent
``X-Frame-Options: SAMEORIGIN`` (the default of ``response.headers``) and could be shown in an ``iframe`` on
a page of the same origin. If you embedded the search screen in an ``iframe`` of the same origin, set
``theme.index.frame.ancestors`` in ``fess_config.properties`` (default ``'none'``) to ``'self'``. To embed
it from another origin, name that origin instead (see :doc:`../dev/theme-development`).

The Page Design Editor Was Removed
----------------------------------

[System > Page Design] is no longer in the admin UI, so the JSP, CSS and image files of the search
screen can no longer be edited there. Use a theme to change how the search screen looks (see
:ref:`theme-customize-bundled`).

The following keys were removed from ``fess_config.properties`` as well. A value left under these
names is not used.

- ``supported.uploaded.js.extentions``
- ``supported.uploaded.css.extentions``
- ``supported.uploaded.media.extentions``
- ``supported.uploaded.files``
- ``online.help.name.design``

The ``admin-design`` and ``admin-design-view`` roles no longer grant anything. A user who has only
these roles is taken to the search screen instead of the admin UI after logging in.

``api.access.token.required`` Was Removed
-----------------------------------------

``api.access.token.required`` no longer exists in ``fess_config.properties``. A value left under
that name, including in a ``fess_config.properties`` carried over from 15.8, has no effect. With
``true`` it refused every API request from a user who was not logged in. Because the search screen
now searches through ``/api/v2/search``, it would also have left anonymous users with a search
screen that shows no results.

An installation that set it to ``true`` now answers API requests from anonymous users with the
guest roles, as it does the search screen. To keep anonymous users from searching, set
``login.required=true``. Access tokens work as before: a request with a registered access token is
given the token's permissions, and a request with an unregistered or expired token is refused.

.. _upgrade-159-api-requests:

Requests the API Now Refuses
----------------------------

15.10 refuses the following requests, which 15.8 accepted. Check the clients and scripts you wrote for 15.8.
The admin API answers a refusal with HTTP ``400`` and ``status`` ``1`` in the body.

.. list-table::
   :header-rows: 1

   * - Request
     - Up to 15.8
     - 15.10
   * - ``/api/v2/search`` with ``facet.field`` or ``facet.query``, and a ``facet.size`` of ``0`` or less, or a ``facet.size`` or ``facet.minDocCount`` that is not an integer
     - ``200``, but an empty result: ``record_count`` is ``0`` and ``partial`` is ``true``
     - ``400`` (``invalid_request``). ``facet.size`` must be ``1`` or more
   * - ``track_total_hits=false``. With ``query.track.total.hits`` set to ``false``, every search is affected
     - ``200``, but with no results
     - The search is refused (``/api/v2/search`` answers ``400`` with ``invalid_request``). ``true`` and positive integers work as before
   * - An entry in the ``mapping`` or ``kuromoji`` dictionary that repeats an existing entry, added or updated through the admin API
     - Saved. Loading the dictionary then fails, which can make search unavailable
     - ``400``
   * - An entry in the ``kuromoji`` dictionary whose ``token`` contains a space, or whose ``segmentation`` and ``reading`` have different numbers of space-separated parts, added or updated through the admin API
     - Saved. Loading the dictionary fails in the same way
     - ``400``
   * - ``DELETE /api/admin/searchlist/doc/{doc_id}`` that deletes nothing: a ``doc_id`` that does not exist, or a value that is not a ``doc_id``, such as the ``_id`` shown in the document list
     - ``200`` (``status`` ``0``); the document is not deleted
     - ``400``
   * - A role or group name in ``roles`` or ``groups`` of a user in the admin API
     - Saved, but the name does not act as a role. For some names, reading the user fails
     - ``400``. Give the ID of the role or group (the ``id`` returned by ``GET /api/admin/role/settings`` and ``GET /api/admin/group/settings``)
   * - A user in the admin API whose password breaks the password policy (for example ``password.min.length``, default ``8``); a create request without a password; a ``confirm_password`` that differs from ``password``
     - Saved; the user can log in with that password
     - ``400``
   * - ``GET /api/admin/log/file/{id}`` with a name that is not allowed for a log file (for example one that does not end with ``.log`` or ``.log.gz``), or with a file that is not in the log directory
     - A name that is not allowed: ``200`` with an empty response
     - ``400``
   * - An entry in the ``mapping`` dictionary without ``output``, added or updated through the admin API
     - ``200`` (``id`` is ``0``); nothing is saved
     - ``400``
   * - ``GET /api/admin/storage/list`` when the storage cannot be accessed, including when no storage client plugin is installed
     - ``200`` (``status`` ``0``) with an empty list
     - ``400``. ``message`` gives the cause and, when the plugin is missing, names the plugin to install
   * - Repeated failed logins on the login form (``POST /login/login``) from one IP address, or for one user from one IP address, within a short time
     - No limit
     - Above the per-address or per-user limit (``theme.api.login.rate.limit.per.ip.per.minute``, ``theme.api.login.rate.limit.per.user.per.minute``), further logins from that address (for the per-user limit: for that user from that address) are refused for ``theme.api.login.lockout.seconds`` seconds, even with correct credentials. The response is the same login error as for wrong credentials. The limits and the lockout are shared with ``/api/v2/auth/login`` (see :doc:`../api/api-auth`) Behind a reverse proxy whose address is not in ``rate.limit.trusted.proxies``, all clients are counted as one address, so repeated failures can lock every user out. Add the proxy's address to ``rate.limit.trusted.proxies`` (a warning is logged once to ``fess.log`` when ``X-Forwarded-For`` arrives from an untrusted peer).

Rows of ``/api/v2/documents/all`` no longer carry ``score``. Up to 15.8 every document had its search score;
15.10 walks the whole result with a point in time and ``search_after``, which gives no score.
``/json?type=scroll`` and ``/api/v1/documents/all`` of the legacy API plugins behave the same. A script that
reads ``score`` has to cope with it being absent.

File uploads of the admin API (the six dictionaries, ``badword``, ``elevateword`` and ``storage``) are
accepted by ``POST``. The 15.8 documentation told you to use ``PUT``, but a ``multipart/form-data`` ``PUT``
never delivers the file, so in 15.8 as well as in 15.10 it fails with the validation error that the file is
required. The ``PUT`` endpoints remain; use ``POST`` for uploads.

The following changes are not refusals, but can affect scripts and clients of the API and the admin UI.

- The ``GET`` requests of the ``webauth`` and ``fileauth`` admin APIs (``/api/admin/webauth/settings``, ``/api/admin/webauth/setting/{id}`` and the same under ``fileauth``) no longer return the stored password. A ``PUT`` that omits the password or sends it blank keeps the stored password; a password that is not blank replaces it.
- A logged-in user is identified by the session, not by a ``userCode`` parameter or cookie that the request carries (for example for the favorite API). An anonymous request still uses the ``userCode`` parameter or cookie it carries, but a code that is the code of a logged-in user is ignored and the client gets an ID of its own.
- "Delete all" on the search list and crawling info screens of the admin UI needs the edit role (``admin-searchlist``, ``admin-crawlinginfo``). The request of a user who has only the view role (the role with the ``-view`` suffix) is refused.
- If you enabled ``parameterKey``, ``headerKey`` or ``cookieKey`` in the ``roleQueryHelper`` component of ``fess.xml`` but set no ``cipher``, and the encryption flag (``encryptedParameterValue``, ``encryptedHeaderValue`` or ``encryptedCookieValue``) is still ``true``, the default, 15.8 read the value as unencrypted role information. 15.10 ignores the value and logs a warning once. Set a ``cipher`` if the values are encrypted, or set the flag to ``false`` if they are meant to arrive unencrypted.
- A request whose ``Content-Type`` names a character set that the JVM does not know (for example ``charset=nope``) is handled like a request without a character set. ``/api/v2/search`` used to answer ``500`` (``internal_error``) for it.
- When an upload or download through the admin API fails for the ``kuromoji``, ``mapping``, ``stemmeroverride`` or ``synonym`` dictionary, the message now names that dictionary. In 15.8 it said "protwords file" for every one of them.

``search_engine.type=cloud`` is deprecated
------------------------------------------

15.9 adds the value ``vanilla`` to ``search_engine.type`` for a plain OpenSearch without the CodeLibs plugins (see :doc:`../config/search-engine-type`). ``cloud`` is now a deprecated alias of ``vanilla``: it keeps working, but |Fess| logs a warning at startup. Change it to ``vanilla`` once the installation runs 15.10. ``aws`` keeps working as before.

* ``vanilla`` requires 15.9. |Fess| 15.8 and earlier do not know the value, so keep ``cloud`` as long as you may still roll back to 15.8.
* The index definitions of ``aws`` and ``cloud`` now come from ``fess_indices/_vanilla/``. The bundled ``fess_indices/_aws/`` and ``fess_indices/_cloud/`` directories no longer exist, and a ``fess_indices/_aws/`` or ``fess_indices/_cloud/`` directory that you added yourself is no longer read. Move your changes to ``fess_indices/_vanilla/``. Indices that already exist are not changed.
* The suggest settings that 15.8 stored in the search engine are migrated automatically; you do not have to do anything.

The CSV Data Store Parses Quoted Fields
---------------------------------------

The ``fess-ds-csv`` plugin of 15.10 interprets quotes by default. A field such as ``"Yamada, Taro"``
is one column, where the 15.8.0 plugin split it at the comma. After ``bin/fess-setup upgrade plugins``,
check data store configurations that read CSV files with quoted fields. To keep the 15.8 behavior,
add ``quote_disabled=true`` to "Parameters"; see :doc:`../config/datastore/ds-csv`, which also
describes what an unmatched quote does.

.. _upgrade-reindex-new-fields:

Applying New Fields and Kana Normalization to an Existing Document Index
------------------------------------------------------------------------

At startup 15.10 adds new fields to the configuration, log and user indices. In the document index
it adds only the ``tag`` field (``keyword``), which holds user tags; the rest of the mapping and
the analysis settings are not changed. If you keep using a document index created by 15.8 or
earlier, the following 15.10 changes do not take effect.

- **File owner and last modifier** (``owner``, ``last_modifier``): new fields indexed by file
  system, SMB and FTP crawls. The existing document index has no definition for them, so the first
  crawled value maps them dynamically as ``text``, and searches such as ``owner:alice`` or
  ``facet.field=owner`` do not work as intended.
- **ETag** (``etag``): the field in which the crawler stores the ETag of a crawled page, which 15.10
  sends back as ``If-None-Match`` so that an unchanged page is not fetched again. The existing
  document index has no definition for it either, so it is mapped dynamically as ``text`` instead
  of the bundled non-indexed ``keyword``. Conditional requests still work with that mapping.
- **Normalization of kana variants and of dashes written in place of the long vowel mark** (for
  example, ``サ―バ－`` is treated as the same word as ``サーバー``): the rules live in the analysis
  settings of the document index and in the ``mapping.txt`` dictionary, so an existing index does
  not get them.

To apply both, enable "Replace Aliases" and "Reset Dictionaries" under "System Info" → "Maintenance"
in the admin UI and run "Re-indexing". Re-indexing copies the existing documents into a new index, so
you do not need to crawl again.

.. warning::

   "Reset Dictionaries" overwrites the dictionaries on the OpenSearch side with the bundled
   dictionary files. If you have edited synonyms or other dictionaries under "Dictionary" in the
   admin UI, download them first and apply them again after re-indexing: remove duplicate or
   invalid entries from the downloaded files (see Step 7), upload them, and then click "Reload"
   under Reload Document Index in "System Info" → "Maintenance". Until you do, the analyzers of the
   document index keep using the bundled dictionaries and a restored synonym does not match, however
   long you wait. A dictionary that applies at index time also needs the documents to be crawled
   again; see :ref:`dict-apply-changes`.

.. note::

   Files indexed by 15.8 or earlier have no owner or last modifier values. Incremental crawling does
   not fetch unchanged files again, so to add the values, temporarily disable "Check Last Modified"
   under "System" → "General" and crawl.


Migration Tasks by Feature
==========================

If you are upgrading from 15.7 or earlier to 15.10, the following tasks may be required depending
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

Starting with 15.6, AI search mode (RAG) functionality has been split out into plugins such as
``fess-llm-ollama``, ``fess-llm-openai``, and ``fess-llm-gemini``. Install the plugin that
corresponds to the provider you use from "System" → "Plugins" in the admin UI. 15.9 also adds
``fess-llm-bedrock`` for Amazon Bedrock.

If You Were Using SPNEGO (Windows Integrated Authentication)
------------------------------------------------------------

Starting with 15.8, a SPNEGO login is rejected when the Kerberos realm of the client principal
differs from the server realm. If your users log in from a child domain of an AD domain tree or
from a trusted forest, list those realms in ``spnego.allowed.realms``, separated by commas, from
"System" → "General" in the admin UI or in ``app/WEB-INF/conf/system.properties``. Otherwise
users who could log in up to 15.7 are rejected with ``Kerberos realm is not allowed``. For
details, see :doc:`../config/sso-spnego`.

The coded defaults of ``spnego.allow.unsecure.basic`` and ``spnego.allow.localhost`` also changed
from ``true`` to ``false`` in 15.8. An installation where these keys are absent from
``app/WEB-INF/conf/system.properties`` inherits the stricter behavior on upgrade. In particular,
with ``spnego.allow.unsecure.basic=false`` the SPNEGO library only offers Basic authentication for
requests where ``HttpServletRequest#isSecure()`` returns ``true``, so behind a reverse proxy that
terminates TLS and forwards plain HTTP, clients that used to fall back to Basic authentication can
no longer log in. Set ``tomcat.secure=true`` in ``tomcat_config.properties`` in that case; see
:doc:`../config/sso-spnego` for details.

.. warning::

   A coded default only applies while the key is absent, and "System" → "General" in the admin UI
   writes every ``spnego.*`` key each time you save. An installation that ever pressed Update on
   that screen under 15.7 therefore still has ``spnego.allow.unsecure.basic=true`` and
   ``spnego.allow.localhost=true`` stored, so upgrading to 15.10 does not harden it: the permissive
   behavior is kept silently, and 15.10 only records a warning in ``fess.log`` when SPNEGO is
   initialized. Open "System" → "General" in the admin UI (or edit ``system.properties``) and
   turn both off deliberately. ``spnego.allow.localhost=true`` is the more dangerous of the two,
   because the SPNEGO library then authenticates same-host requests as the server OS user with no
   Kerberos verification at all, which is unsafe behind a same-host reverse proxy.

.. _upgrade-159-saml:

If You Were Using SAML Authentication (SSO)
-------------------------------------------

Starting with 15.8, |Fess| binds every SAML response to the ID of the AuthnRequest it sent, so
IdP-initiated (unsolicited) SSO no longer works. A login started from a |Fess| tile in an IdP
portal, such as the Okta dashboard or the Microsoft Entra ID "My Apps" portal, has no AuthnRequest
to match against and is rejected. It worked up to 15.7 because |Fess| bounced the unmatched
response back to the IdP and the IdP immediately returned a solicited assertion. If you place a
tile on the IdP side, point it at the |Fess| ``/sso/`` endpoint so that the login is SP-initiated.

The IdP also returns the assertion as a cross-site POST, so ``tomcat.sameSiteCookies`` in
``tomcat_config.properties`` must be set to ``none``. With the shipped default ``lax`` the session
cookie is not sent on that request and the SAML login cannot complete. This file is located in
``lib/classes/`` for the ZIP package and in ``/etc/fess/`` for the DEB/RPM packages, and |Fess|
must be restarted after the change. Browsers only accept ``none`` on a cookie that also carries
the ``Secure`` attribute, so |Fess| must be served over HTTPS. Up to 15.7 the same
misconfiguration did not produce a clean error but an endless redirect loop back to the IdP, so
check the setting even on a site that appeared to work; 15.10 fails once instead of looping. For
details, see :doc:`../config/sso-saml`.

If You Were Using Microsoft Entra ID (Azure AD)
-----------------------------------------------

Starting with 15.8, the response mode requested from the authorization endpoint defaults to
``query`` instead of ``form_post``. Up to 15.7 the callback was returned as a cross-site POST,
and the |Fess| default ``tomcat.sameSiteCookies = lax`` does not send the session cookie with
such a request, so ``tomcat.sameSiteCookies = none`` was required. If you set ``none`` only for
that reason, you can restore the default. To keep the previous behaviour, set
``entraid.response.mode=form_post`` and leave ``tomcat.sameSiteCookies = none`` in place.
Browsers only accept ``none`` on a cookie that also carries the ``Secure`` attribute, so that
path requires |Fess| to be served over HTTPS as well.

Starting with 15.8, |Fess| also resolves the user's group and role membership in the background
after login completes, instead of blocking the login on Microsoft Graph. Until resolution
finishes — or if it does not fully succeed — the user holds only their own user-level permission
and whatever ``entraid.default.groups`` and ``entraid.default.roles`` provide. With neither of
those set, which is the shipped default, a search made in that window returns no documents at all,
because a crawling configuration created with the shipped defaults grants ``{role}guest`` and a
logged-in user does not hold that role. The search screen says so while resolution is in progress,
and says something different if it did not fully succeed — the resolution counts as failed unless
both the direct membership lookup and the nested group walk succeeded. Resolution is retried
whenever the access token is renewed, and a later success clears the message, so a failure is not
final for a session that outlives the token; to retry straight away, log out and log in again. For
details, see :doc:`../config/sso-entraid`.

One consequence of resolving in the background: until it lands, the user's resolved roles are not
yet known. An administrator is therefore redirected to the search screen instead of the admin
dashboard, and opening an administration page during that window returns them to the search
screen. The window is up to about a second of scheduling delay plus the Microsoft Graph calls
themselves — one for the direct memberships, then one more for each of those groups to walk the
nested groups, issued one after another on a cold cache — so it grows with the number of groups
the user belongs to. Access is only ever refused, never granted, in that window, and it needs no
configuration to get past: authorization is evaluated again on every request of the same session,
so once resolution has landed the administration screens open normally, without logging in again.

.. warning::

   Do not shorten that window by putting the |Fess| administrator role in
   ``entraid.default.roles``. That property is a single global value that |Fess| applies to every
   Entra ID user at login and re-applies on every later resolution, so it would give every user in
   the tenant permanent |Fess| administrator rights.

If You Use LDAP / Active Directory
----------------------------------

From 15.8, the permission name of a group or role is the value of the entry's RDN rather than a
slice of the DN text. A group whose CN contains a character the DN escapes -- a comma is the
common one -- therefore gets a different permission name than it did in 15.7.

.. list-table::
   :header-rows: 1

   * - Group entry DN
     - Permission name up to 15.7
     - Permission name in 15.10
   * - ``CN=Sales\, EMEA,CN=Users,...``
     - ``2Sales``
     - ``2Sales, EMEA``
   * - ``CN=Sales\, APAC,CN=Users,...``
     - ``2Sales``
     - ``2Sales, APAC``

Up to 15.7 several groups agreeing up to the comma collapsed onto one permission name, so members
of ``Sales, EMEA`` and ``Sales, APAC`` could read each other's documents and those of the ``Sales``
group. In 15.10 each gets its own permission name and that cross-group access does not happen.

In exchange, **documents indexed under the old permission name are no longer visible to members of
that group**. If a crawling configuration's permission setting holds an old permission name, update
it to the new one and crawl (or reindex) again. If you use no group whose CN contains a comma or
another escaped character, no permission name changes.

Change to ``ldap.role.search.user.enabled``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Up to 15.7 the permission derived from the user name (``role.search.user.prefix`` followed by the
user name) was granted even with ``ldap.role.search.user.enabled=false``. From 15.8 the setting
takes effect and the permission is not granted when it is off.

In a deployment that sets it to ``false``, users lose the permission named after themselves after
the upgrade, so documents permissioned to an individual user stop matching for that user. To keep
the previous behaviour, restore the shipped default of ``true``.

If You Changed the /api/v2 Configuration Keys
------------------------------------------------

In 15.8.0, four configuration keys lost their ``api.v2.`` prefix. Their values, defaults and
behaviour are unchanged, but **no backward-compatible alias is kept**: a setting left under its
old name is ignored without any warning, and the shipped default takes effect instead.

.. list-table::
   :header-rows: 1

   * - Up to 15.7
     - 15.8.0 and later
     - Default
   * - ``api.v2.chat.stream.keepalive.interval.ms``
     - ``api.chat.stream.keepalive.interval.ms``
     - ``15000``
   * - ``api.v2.param.max.length``
     - ``api.param.max.length``
     - ``1000``
   * - ``api.v2.param.max.array.size``
     - ``api.param.max.array.size``
     - ``100``
   * - ``api.v2.click.max.rt``
     - ``api.click.max.timestamp``
     - ``9999999999999``

If you set any of these in ``fess_config.properties`` or as a ``-Dfess.config.<key>`` JVM
argument, rename them. Only an explicit setting is affected; an installation that never changed
them needs no action.

The first key controls how often a keep-alive frame is sent while ``POST /api/v2/chat/stream``
is waiting for the model, so AI search mode is where a lost setting becomes visible. The last
key was renamed for accuracy as well: it bounds the ``rt`` value a click log may carry, which is
a timestamp rather than a response time.


.. _upgrade-plugin-versions:

Updating Plugin Versions
------------------------

Plugins installed under ``app/WEB-INF/plugin/`` need to be replaced with versions matching your
|Fess| version. ``bin/fess-setup upgrade plugins`` does this for every installed plugin: it
installs the version built for this |Fess| and deletes the old one. Restart |Fess| afterwards.
``bin/fess-setup check`` then reports on OpenSearch, its plugins and the installed |Fess| plugins,
and exits with code 1 when something is wrong. It does not read ``bin/fess.in.sh``,
``/etc/sysconfig/fess`` or ``/etc/default/fess``, so when OpenSearch is not at
``http://localhost:9200``, pass ``--url`` or set ``SEARCH_ENGINE_HTTP_URL`` in the shell that runs
it; otherwise it reports the engine as unreachable.

::

    $ bin/fess-setup upgrade plugins
    $ bin/fess-setup check

``upgrade plugins`` only handles plugins that are already installed. Install the plugins that
replace parts removed from the distribution in 15.9, such as ``fess-script-groovy``, with
``bin/fess-setup install plugin`` as described in the sections above.

If you specify ``FESS_PLUGINS`` in the Docker version, update the version part, for example to
``fess-ds-wikipedia:15.10.0``.

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

    $ sudo rpm -Uvh --oldpackage --nodeps fess-<old-version>.rpm

Or::

    $ sudo dpkg -i fess-<old-version>.deb

.. note::

   ``--nodeps`` is needed for the RPM. The 15.8.0 package requires the ``fess`` and ``opensearch``
   users and groups, and without it ``rpm`` refuses the downgrade with ``Failed dependencies:
   group(fess) is needed by fess-15.8.0``.

.. warning::

   The 15.8.0 DEB package does not register ``/etc/fess/*`` as conffiles, so ``dpkg -i`` overwrites
   the files you edited, such as ``/etc/fess/fess_config.properties``, without keeping a copy. Restore
   them from the backup you took in Step 1.

.. _upgrade-1510-rollback-5xx:

.. warning::

   **Remove 5xx from the failure URL status codes before you start the old version.**
   15.10 ships ``crawler.failure.url.status.codes`` as ``404,403,410,401,5xx``. |Fess| 15.9.0 and
   earlier read every entry of this list as a number, so with a ``fess_config.properties`` that
   contains ``5xx`` they throw a ``NumberFormatException`` for every crawled page, and every page,
   including a page that was fetched successfully, is recorded as a failure URL (the log shows the
   ``NumberFormatException``). Open the ``fess_config.properties`` that the old version uses
   (``/etc/fess/fess_config.properties`` for RPM/DEB, ``app/WEB-INF/classes/fess_config.properties``
   for ZIP), remove ``5xx`` so that the line reads ``crawler.failure.url.status.codes=404,403,410,401``
   (the 15.9 value), and remove it from the ``-Dfess.config.crawler.failure.url.status.codes`` JVM
   argument as well if you set one. Do this before you start |Fess|; a change takes effect only after
   a restart. A file that you restore from the backup you took before the upgrade holds the 15.9
   value and needs no change.

.. _upgrade-1510-rollback-opensearch:

Step 3: Restore Data
---------------------

.. warning::

   **Go back to OpenSearch 3.9.x as well; the data of OpenSearch 3.10.0 cannot be carried back.**
   OpenSearch 3.9.0 does not start on a data directory that a 3.10.0 node has opened (it exits with
   ``IndexFormatTooNewException``), and a snapshot taken on 3.10.0 cannot be restored to 3.9.x
   (``the snapshot was created with OpenSearch version [3.10.0] which is higher than the version of
   this node``). Roll back to the state before the upgrade like this:

   1. Stop OpenSearch 3.10.0.
   2. Install OpenSearch 3.9.x, the version your old |Fess| used (3.9.0 for 15.9.0), and its four
      plugins built for the same version (the URLs in :ref:`Step 4: Upgrade OpenSearch <upgrade-opensearch>` with ``3.9.0`` in
      place of ``3.10.0``; remove plugins of another version first), with an **empty data
      directory**. Do not copy the data of 3.10.0. Keep the dictionary directory and
      ``configsync.config_path`` as they were, at the same absolute path.
   3. Start OpenSearch 3.9.x and restore the snapshot you took before the upgrade (see
      "Step 1: Data Backup") as described below, including the deletion of the indices that the plugin
      created at startup (``configsync``).

   Running |Fess| 15.9.0 against an OpenSearch 3.10.0 that is left in place was observed to start
   and search after the snapshot was restored on it, but it is not a supported combination.

   For the Docker version, the same applies: the volumes that OpenSearch 3.10.0 has written cannot
   be reused by 3.9.0. Start a new 3.9.0 node on empty volumes and restore the snapshot, or restore
   the archive of the volumes taken before the upgrade, as shown below.

Restore from snapshot. OpenSearch must be running and |Fess| stopped:

1. Start OpenSearch::

       $ sudo systemctl start opensearch.service

2. A snapshot cannot be restored over an index that exists, so delete every Fess index first,
   including the ones created after the upgrade (for example by re-indexing), and the ``configsync``
   index that the OpenSearch plugin creates. If you delete only the indices that are in the
   snapshot, an index created by re-indexing stays behind, ``fess.search`` points at two indices,
   and 15.8.0 does not start::

       $ curl "http://localhost:9200/_cat/indices/fess*,configsync?h=index"
       $ curl -X DELETE "http://localhost:9200/<index name>"

   Run the second command for each index that the first one lists.

3. Restore the snapshot, naming the indices to restore::

       $ curl -X POST "http://localhost:9200/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" \
           -H 'Content-Type: application/json' \
           -d '{"indices":"fess*,.fess*,configsync,.configsync*","include_global_state":false}'

   A snapshot taken as in Step 1 holds every index of the cluster, including system indices of OpenSearch plugins such as ``.opensearch-sap-log-types-config``. Such an index is open on the running cluster, so a restore without the ``indices`` setting is refused with ``cannot restore index [.opensearch-sap-log-types-config] because an open index with same name already exists``. The setting restores only the Fess indices and the ``configsync`` index.

.. note::

   The dictionary directory must exist as before (``configsync.config_path``, with the dictionary
   files). On a machine that has lost it, the restore finishes but the indices that use the
   dictionaries stay red.

Or restore directory from backup (use the name of the archive you created in Step 1)::

    $ sudo systemctl stop opensearch
    $ sudo rm -rf /var/lib/opensearch/data/*
    $ sudo tar xzf /backup/opensearch-data-<YYYYMMDD>.tar.gz -C /
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
   for the ZIP version, ``/etc/fess/`` for the RPM/DEB version).

.. note::

   The import runs asynchronously; the screen only shows that it has started. Check
   ``fess.log`` to confirm whether it actually succeeded.

.. warning::

   15.10 writes a numeric field ``password_changed_at`` (the time of the password change) to the user document (index ``fess_user``) when a user is created and when a user's password is changed. 15.9 and earlier, including the released 15.9.0, cannot read this field. If you start them against an index that still holds a user created or given a new password in 15.10, the login of that user and the user list of the Admin API fail with HTTP 500 (``ClassCastException``). A snapshot taken before the upgrade, restored in Step 3, does not contain such users. Otherwise, delete the users created or changed in 15.10 and create them again, or remove ``password_changed_at`` from the user index before the rollback.

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

A: Each version of |Fess| is released for a specific version of OpenSearch.
|Fess| 15.10 supports OpenSearch 3.10.0. It does not check which OpenSearch 3.x version it
runs on when it starts, but any other version, 3.9.0 for example, is not supported.
The |Fess| OpenSearch plugins such as ``opensearch-analysis-fess`` must exactly match the
OpenSearch version, so if you upgrade OpenSearch, also update the plugins to the corresponding
version (3.10.0).

Also, |Fess| 15.10 requires the k-NN plugin and always sends ``knn.derived_source.enabled`` in the
index settings. With an older OpenSearch, creating a new index fails, so upgrading OpenSearch is
effectively required. See Step 4 for details.

Q: Do I need to recreate the index?
------------------------------------

A: For a |Fess| minor version upgrade (15.x → 15.10) where you do not use chunk-vector search, it
is usually not necessary. The existing index can continue to be used as-is, and settings such as
``content_chunker.enabled`` remain disabled by default, so behavior does not change.

Recreation and re-indexing are required in the following cases:

- **Newly enabling chunk-vector search (semantic search)**: The existing index does not pick up
  the new mapping, so re-indexing is required. See :ref:`semantic-search-migration` (in
  :doc:`../config/search-semantic`) for details.
- **Upgrading from 14.x**: Because OpenSearch undergoes a major version upgrade from 2.x to 3.x,
  recreating the index is recommended.
- **Using owner search or the kana normalization with a document index created by 15.8 or earlier**:
  a re-index is needed. See :ref:`upgrade-reindex-new-fields` for details.

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
