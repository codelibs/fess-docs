====================================================
Fess Operations: Monitoring, Backup, Troubleshooting
====================================================

Introduction
============

Once Fess is open to everyone in the organization, operators tend to run into situations like these:
learning that search is down only when users start asking about it, not noticing for days that the nightly crawl has been failing, or rebuilding a server only to find that the settings did not come back.

This article explains how to prepare for these situations using the mechanisms built into Fess 15.9.

- Check the state of Fess and OpenSearch from an external monitoring tool with ``/api/v2/health`` and ``/api/admin/stats``
- Send notifications about crawl completion, OpenSearch status changes, and error logs to email, Slack, or Google Chat
- Know what each log file contains and where it is located
- Take configuration backups with cron and restore them on another server
- Know which Fess screens and logs to look at when something goes wrong

Managing configuration as code is covered in :doc:`guide-16`, and scaling for growing document counts and user numbers (including heap tuning) in :doc:`guide-14`.
The example commands assume the Docker setup from :doc:`guide-02` (``fess01`` and ``search01``).
Differences for the ZIP and RPM/DEB packages are noted where they apply.

Monitoring
==========

Liveness Monitoring: /api/v2/health
-----------------------------------

Fess provides a health check API that can be called without authentication.

::

    $ curl -fsS --max-time 10 http://localhost:8080/api/v2/health
    {"response":{"status":0,"engine":{"status":"GREEN","ping_status":0}}}

The HTTP status codes mean the following.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Status
     - Condition
   * - 200
     - Fess is responding, and the OpenSearch cluster is ``GREEN`` or ``YELLOW``
   * - 503
     - The OpenSearch cluster is ``RED``, or Fess cannot connect to OpenSearch (``error.details.engine.status`` is ``UNAVAILABLE``)
   * - No response / timeout
     - The Fess process has stopped, or Fess is waiting for an OpenSearch that does not respond

Your monitoring tool should base its check on this status code.
With ``curl``, adding ``-f`` makes the exit code non-zero on a 503.
If OpenSearch stops responding without its process going down, this API waits for OpenSearch's response for up to ``index.health.timeout`` (default ``10m``).
On the monitoring side, set a timeout, such as ``--max-time 10`` in the example above, and treat a timeout as a failure as well.
Note that ``/api/v1/health``, which earlier versions of this article introduced, is not available in a standard 15.9 setup (``/api/v1`` is provided only when the ``fess-webapp-v1-api`` plugin is installed).

In Docker, ``fess01`` uses this API through two mechanisms.

- The ``healthcheck`` in ``compose.yaml`` calls it every 30 seconds; the result appears as ``(healthy)`` in ``docker compose ps``
- The startup script inside the container also calls it every 60 seconds and, once Fess has started, stops the container after 5 consecutive non-200 responses. Thanks to ``restart: unless-stopped``, the container is then restarted

As a result, if OpenSearch stays ``RED`` for a few minutes, ``fess01`` restarts over and over.
When ``fess01`` keeps restarting, check ``search01`` first.

Resource Monitoring: /api/admin/stats
-------------------------------------

Heap usage and free disk space are available from the admin API ``GET /api/admin/stats``.
[System Info] > [Config Info] only lists properties and does not show memory usage.

The admin API requires an access token.

1. Open [System] > [Access Token] and click [Create New]
2. Enter the purpose in "Name" (e.g. ``monitoring``) and ``{role}admin-api`` in "Permissions", then click [Create]
3. Open the token you created from the list and note the value of "Token"

.. warning::

   A ``{role}admin-api`` token can use every admin API, including those that change or delete settings.
   There is no setting to restrict it to read-only access.
   Store it, for example in a file on the monitoring server, with the same care as the administrator password.

Pass the token in the ``Authorization`` header.
The following example extracts the heap usage (%) and the usage of each file system.

::

    $ curl -fsS -H "Authorization: Bearer <token>" http://localhost:8080/api/admin/stats \
        | jq '{heap: .response.stats.jvm.memory.heap.percent, fs: [.response.stats.fs[] | {path, percent}]}'

The response also includes GC counts and cumulative times (``jvm.gc``), OS CPU usage and load average (``os``), and the OpenSearch cluster state and shard counts (``engine``).
For the full list of fields, see `Stats API <https://fess.codelibs.org/stable/api/admin/api-admin-stats.html>`__.

Keep the following two points in mind when reading the values.

- ``jvm`` reflects the JVM of Fess itself (the web application). Crawls run in a separate JVM process, so the crawler running out of memory does not show up here. Check ``fess-crawler.log`` for that (described later)
- ``fs`` covers the file systems of the host Fess runs on (the container, in Docker). To find the free space in OpenSearch's data area, query OpenSearch directly

::

    $ curl -s "http://localhost:9200/_cat/allocation?v"

For how to change the heap size, see :doc:`guide-14`.

Receiving Notifications
-----------------------

Fess notification destinations are configured with three fields in the "Notify" section of [System] > [General].

- "Notification Mail": recipient email addresses (comma-separated for multiple)
- "Slack Webhook URLs": a Slack Incoming Webhook URL
- "Google Chat Webhook URLs": a Google Chat Webhook URL

Once any one of them is set, the following three kinds of notifications are sent to the same destinations.

.. list-table::
   :header-rows: 1
   :widths: 25 40 35

   * - Notification
     - When it is sent
     - Additional settings required
   * - Crawl completion (subject ``[FESS] Crawler completed``)
     - Sent every time a crawl job finishes, whether it succeeded or not. It includes the status (OK/FAIL) and the number of documents indexed
     - None
   * - OpenSearch status change (subject ``[FESS] Status Change``)
     - The scheduler job "Search Engine Monitor" queries OpenSearch every minute and sends a notification when the cluster turns ``RED`` and when it recovers from ``RED``
     - None
   * - Log notification (subject ``[FESS] ERROR Log Alert``)
     - The job "Log Notification" collects ERROR logs (or logs at or above the specified level) written by Fess, the crawler, and other processes, and sends them together every 5 minutes
     - Enable "Log Notification" under [General] and choose a "Log Notification Level"

If Fess cannot connect to OpenSearch, the "Search Engine Monitor" job itself fails and no status change notification is sent.
Detect loss of connectivity by monitoring ``/api/v2/health`` externally, as described in the previous section.

The default log notification level is ``ERROR``.
Failed scheduled jobs are logged at ``WARN`` (``Failed to execute job: ...``), so if you also want to know about job failures, set "Log Notification Level" to ``WARN``.
In that case, every other ``WARN`` is notified as well.

To receive email, configure the SMTP server in two files and restart Fess.

::

    mail.smtp.server.main.host.and.port=smtp.example.com:587

- ``fess_env_web.properties``: used for log notifications, status change notifications, and the [Send Test Mail] button
- ``fess_env_crawler.properties``: used for crawl completion notifications (because crawls run in a separate process)

These files are in ``app/WEB-INF/classes/`` for the ZIP package and in ``/etc/fess/`` for the RPM/DEB packages.
After configuring them, use [Send Test Mail] under [General] to confirm that mail arrives.

If you want notifications quickly with Docker, a Slack or Google Chat webhook is the easy option, since no files need to be edited.
However, the [General] settings are stored in ``system.properties`` inside the ``fess01`` container, so they are lost when the container is recreated with ``docker compose down`` (see the section on stopping and restarting in :doc:`guide-02`).
Include ``system.properties`` in the backups described later.

Checking Search Response Times and Crawl Results
------------------------------------------------

In addition to external monitoring, check the following three admin screens regularly.

- [System Info] > [Job Log]: the status (OK/Fail) and result of jobs such as "Default Crawler". Jobs that run every minute or every few minutes, such as "Search Engine Monitor" and "Log Notification", are not recorded here
- [System Info] > [Crawling Info]: "Crawler Status", "Index Size (Web/File)", and "Index Size (Data Store)" for each session. Check that they have not dropped sharply since the previous run
- The [Performance] tab of [System Info] > [Search Log]: the median, p95, and p99 response times, and the queries with slow responses. For how to read search logs, see :doc:`guide-08`

Reading Logs
============

Types of Log Files
------------------

Fess writes logs to a separate file for each kind of processing.
Choose the file to open based on what you want to investigate.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - File
     - Contents
   * - ``fess.log``
     - Logs of Fess itself (search pages, admin pages, APIs, scheduler). Startup failures, OpenSearch connection errors, failed backup imports, and so on
   * - ``fess-crawler.log``
     - Logs of the crawler process. Fetch errors per URL, authentication failures, crawler out-of-memory errors, and so on
   * - ``audit.log``
     - Audit log of logins, logouts, and administrative operations
   * - ``fess-suggest.log`` / ``fess-thumbnail.log``
     - Logs of suggestion generation and thumbnail generation
   * - ``fess-llm.log``
     - Logs of AI search mode (RAG) and LLM integration
   * - ``searchlog.log``
     - A record of each search (when "Search Log" is enabled under [General])
   * - ``server_*.log``
     - Tomcat logs

Their location depends on how Fess was installed.

- ZIP package: ``logs/`` in the directory where Fess was extracted
- RPM/DEB packages: ``/var/log/fess/``
- Docker: ``/var/log/fess/`` inside the container. ``fess.log``, ``fess-crawler.log``, ``audit.log``, and others are also sent to standard output, so you can read them with ``docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01``. They are lost when the container is recreated

Whatever the installation method, you can download a file by clicking its name in [System Info] > [Log File].
Staff who cannot log in to the server can check logs from here.

Each log is compressed to ``.log.gz`` and rotated when the date changes or when it exceeds 100 MB.
Compressed files are deleted automatically after 90 days for ``fess.log`` and ``searchlog.log``, and after 360 days for ``audit.log``.
On the other hand, compressed files of the crawler and child process logs, such as ``fess-crawler.log``, ``fess-suggest.log``, and ``fess-thumbnail.log``, are not deleted automatically.
Monitor the size of the log directory and delete old files regularly.

Investigating in More Detail
----------------------------

By default, ``fess.log`` records WARN and above, and ``fess-crawler.log`` records INFO and above.
To make ``fess.log`` more detailed, raise "Log Level" under [System] > [General] to ``INFO`` or ``DEBUG``.
This change reverts when Fess is restarted.
The crawler's log level is determined by the job script.
The "Default Crawler" script contains ``logLevel("info")``; change it to ``logLevel("debug")`` in [System] > [Scheduler], and detailed logs are written from the next crawl.
Change it back when you have finished investigating.
For how to change the level permanently, see `Log Configuration <https://fess.codelibs.org/stable/config/admin-logging.html>`__.

When you ask for help on a forum or elsewhere, [Download Logs] under "Diagnostics" in [System Info] > [Maintenance] is useful.
It downloads a zip file containing the logs, ``system.properties``, ``fess_config.properties``, the contents of the configuration indices, and the state of OpenSearch.
Values such as API keys and ``app.cipher.key`` are replaced with ``XXXXXXXX``, but the log bodies and the contents of the configuration indices are not masked.
Review the contents before handing the file to anyone outside your organization.

Backing Up
==========

What Lives Where
----------------

Fess data is stored in three places.
[System Info] > [Backup] covers only the first of them.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Data
     - Storage location
     - Backup method
   * - Crawl configurations, scheduler, labels, users, [General] settings
     - OpenSearch configuration indices and ``system.properties``
     - [System Info] > [Backup], or the admin API
   * - Crawled documents, dictionaries (synonyms, stopwords, etc.)
     - OpenSearch ``fess.*`` indices and the ``configsync`` index
     - OpenSearch snapshots (for dictionaries alone, copying the files also works)
   * - ``fess_config.properties`` (including ``app.cipher.key``), startup settings, installed plugins
     - Files on the Fess server
     - Copying the files, or configuration management

Crawled documents can be rebuilt by recrawling, as long as the configuration is restored.
Take snapshots only when a recrawl would take too long.

Files Available from [Backup]
-----------------------------

[System Info] > [Backup] lists the following files.
Click a name to download that file.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - File
     - Contents
   * - ``fess_basic_config.bulk``
     - Settings such as crawl configurations, scheduler, labels, key matches, and web/file authentication
   * - ``fess_config.bulk``
     - Everything above, plus crawling info, failure URLs, job logs, user tags, and so on
   * - ``fess_user.bulk``
     - Users, roles, and groups
   * - ``system.properties``
     - The settings under [System] > [General]
   * - ``fess.json`` / ``doc.json``
     - Settings and mappings of the document index
   * - ``*.ndjson``
     - Search logs, click logs, favorites, AI chat logs, and search users. These can be downloaded but cannot be uploaded to restore them

The three files used to restore settings are ``fess_basic_config.bulk``, ``fess_user.bulk``, and ``system.properties``.
If you use user tags, also download ``fess_config.bulk``.

Apart from the credentials described later, ``*.bulk`` files contain setting values unencrypted.
Store them as confidential files.

Taking Daily Backups with cron
------------------------------

The admin API ``GET /api/admin/backup/file/<file-name>/`` returns the same files as the screen.
Create a token using the same steps as in "Resource Monitoring" above, and save it to a file that only the user running the script can read.

::

    $ sudo mkdir -p /etc/fess-backup
    $ sudo sh -c 'umask 077; echo "<token>" > /etc/fess-backup/token'

The following script saves the files in a directory per date and deletes directories older than 30 days (the retention period is an example).

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail

    FESS_URL=http://localhost:8080
    FESS_TOKEN=$(cat /etc/fess-backup/token)
    BASE_DIR=/var/backups/fess
    BACKUP_DIR="${BASE_DIR}/$(date +%Y%m%d)"

    umask 077
    mkdir -p "${BACKUP_DIR}"
    for id in fess_basic_config.bulk fess_config.bulk fess_user.bulk system.properties fess.json doc.json; do
      curl -fsS -H "Authorization: Bearer ${FESS_TOKEN}" \
        -o "${BACKUP_DIR}/${id}" "${FESS_URL}/api/admin/backup/file/${id}/"
      test -s "${BACKUP_DIR}/${id}"
    done

    # Docker setup: also copy the dictionary files
    docker cp search01:/usr/share/opensearch/config/dictionary/. "${BACKUP_DIR}/dictionary"

    find "${BASE_DIR}" -mindepth 1 -maxdepth 1 -type d -mtime +30 -exec rm -rf {} +

Key points:

- The trailing ``/`` in the URL cannot be omitted. Because the file names contain a dot, a request without the ``/`` is treated as a request for a static file and returns 404
- Without ``-f``, ``curl`` saves 404 and other error responses to the file as well, and the script appears to succeed. ``-f`` together with ``set -e`` makes the script stop on failure
- For the ZIP and RPM/DEB packages, replace the ``docker cp`` line with a copy of the dictionary directory on the OpenSearch side (the location that Fess's ``FESS_DICTIONARY_PATH`` points to)

Save the script as ``/usr/local/bin/fess-backup.sh``, make it executable, and register it in root's crontab (this example runs it daily at 2:30).

::

    30 2 * * * /usr/local/bin/fess-backup.sh

After registering it, run it once manually.
Open ``fess_basic_config.bulk`` and check that lines beginning with ``{"index":{"_index":`` alternate with JSON lines containing the settings.
The same process can also be written with ``fessctl`` (see :doc:`guide-16`).

Keeping a Record of app.cipher.key
----------------------------------

Fess 15.9 encrypts passwords for web authentication and file authentication, as well as passwords and secrets stored in the parameters of crawl configurations and data store configurations, using ``app.cipher.key`` in ``fess_config.properties``.
They remain encrypted in ``*.bulk`` files as well.
When restoring to another server, the same ``app.cipher.key`` must be set there.
With a different key, the values cannot be decrypted: ``CipherFailureException`` is logged in ``fess-crawler.log``, and crawls that use those credentials fail.

``fess_config.properties`` is located in ``app/WEB-INF/classes/`` for the ZIP package and in ``/etc/fess/`` for the RPM/DEB packages.
If you have changed the value, treat this file as confidential, just like the ``*.bulk`` files, and store it in a separate place.
To change the value in Docker, specify ``-Dfess.config.app.cipher.key=<value>`` in ``FESS_JAVA_OPTS`` in ``compose.yaml``.
This way, the same key is used even after the container is recreated.

.. warning::

   If you change ``app.cipher.key`` after credentials have been saved, the values saved until then can no longer be decrypted.
   If you change it, do so before registering credentials for web authentication, file authentication, or data stores.
   In an environment that is already in operation, leave the value unchanged and keep a record of it.

Snapshots of the Document Index
-------------------------------

To restore documents without recrawling, use OpenSearch snapshots.
In addition to ``fess*``, always include the ``configsync`` index, which holds the dictionaries.
Without ``configsync``, the dictionary files are missing when you restore to a new OpenSearch, and the document index cannot be opened.

To use snapshots, the repository path (``path.repo``) must be configured on the OpenSearch side.
It is not set in ``compose-opensearch3.yaml`` of docker-fess, so add it if you use snapshots.
The steps for registering a repository, taking snapshots, and restoring are described in `Index Management <https://fess.codelibs.org/stable/config/admin-index-backup.html>`__.
Restore with Fess stopped, and restore ``configsync`` first.

Restoring
=========

What to Know Before Restoring
-----------------------------

Restoring from [Backup] does not replace the contents of OpenSearch wholesale.

- Restoring is done only by uploading. The admin API is download-only, and there is no restore API
- Each setting in a ``*.bulk`` file is written only if the same setting does not exist on the server or is newer than the one on the server. Settings changed after the backup was taken are not reverted to their old contents
- Settings created after the backup was taken are not deleted and remain

For this reason, it is not suited to "rolling back a setting changed by mistake to yesterday's state".
Use it for migrating to a new server or restoring a rebuilt environment.

Restoring Settings on Another Server
------------------------------------

1. Install the same version of Fess on the destination, and set ``app.cipher.key`` in ``fess_config.properties`` to the same value as on the source
2. Install the plugins used on the source (data stores, SSO, etc.) and restart Fess
3. Log in to the admin console and open [System Info] > [Backup]
4. Select ``fess_basic_config.bulk`` in "Bulk File" and click [Upload]. "Started a bulk process." is displayed
5. Upload ``fess_user.bulk`` and ``system.properties`` in the same way. If you use user tags, also upload ``fess_config.bulk`` (this also imports the source's crawling info and job logs)

The import runs in the background.
Wait a moment, then check the following.

- The source's settings appear in [Crawler] > [Web], [File System], and [Data Store], and in [System] > [Scheduler]
- The source's users appear in [User] > [User]
- The notification destinations and other settings in [System] > [General] have the source's values

Finally, restore the dictionaries and rebuild the documents.

- Dictionaries: in [System] > [Dictionary], open the screen for each type and upload the backed-up dictionary file. Then run "Reload Document Index" in [System Info] > [Maintenance]. Search is unavailable for a short time during the reload
- Documents: in [System] > [Scheduler], click [Start Now] for "Default Crawler" to recrawl. To restore from a snapshot, follow the steps described earlier

When the crawl has finished, check the number of indexed documents in [System Info] > [Crawling Info].
If a crawl configuration with authentication shows 0 documents, check ``fess-crawler.log`` for ``CipherFailureException``.
If it is there, ``app.cipher.key`` does not match the source.

Troubleshooting
===============

This section summarizes common symptoms and where to check in Fess.

The Search Page Does Not Open, or /api/v2/health Returns 503
------------------------------------------------------------

1. Check the state of OpenSearch. If ``status`` in ``curl -s "http://localhost:9200/_cluster/health?pretty"`` is ``red``, the problem is on the OpenSearch side. In Docker, check ``docker compose -f compose.yaml -f compose-opensearch3.yaml logs search01``
2. If OpenSearch is healthy but Fess does not respond, check ``fess.log`` for errors at startup
3. If the cluster turns ``red`` right after restoring from a snapshot, ``configsync`` may not have been restored (see above)

Crawls Fail, or the Number of Indexed Documents Has Dropped
-----------------------------------------------------------

1. In [System Info] > [Job Log], open the row of the relevant job and check "Result"
2. In [System Info] > [Crawling Info], compare "Crawler Status" and the index sizes of the latest session with the previous one
3. In [System Info] > [Failure URL], check "Type", "Log", and "Error Count" for the URLs that could not be fetched. HTTP 404, 403, 410, and 401 are also recorded here
4. Details are in ``fess-crawler.log``. Searching for the "Thread Name" shown in the failure URL details lets you follow the surrounding log entries from that time

If ``fess-crawler.log`` contains ``OutOfMemoryError``, the crawler process is running out of heap.
The crawler heap is set by ``jvm.crawler.options`` in ``fess_config.properties`` (default ``-Xmx512m``) and is separate from the heap of Fess itself.
For how to tune it, see :doc:`guide-14`.

Notifications Do Not Arrive
---------------------------

For email, first check whether mail arrives using [Send Test Mail] under [General].
If only the crawl completion mail does not arrive, check the SMTP server in ``fess_env_crawler.properties``.
In Docker, also check that the [General] settings have not been lost because the container was recreated with ``down`` and ``up``.
If only log notifications do not arrive, check that "Log Notification" is enabled, that the "Log Notification" job is enabled, and that "Log Notification Level" is appropriate (``WARN`` for job failures).
Other items to check are listed under "Troubleshooting" in `Log Notification <https://fess.codelibs.org/stable/config/admin-log-notification.html>`__.

Search Is Slow
--------------

1. On the [Performance] tab of [System Info] > [Search Log], check whether specific queries are slow or everything is
2. Compare ``jvm.memory.heap.percent`` and the cumulative time in ``jvm.gc`` from ``/api/admin/stats`` with the values from before the slowdown

Further Reading
===============

- To manage settings with scripts or ``fessctl``: :doc:`guide-16`
- To tune the heap, or to run multiple OpenSearch or Fess nodes: :doc:`guide-14`
- To strengthen access protection with SSO, audit logs, and more: :doc:`guide-15`
- To improve search quality using search logs: :doc:`guide-08`

References
==========

- `Health API <https://fess.codelibs.org/stable/api/api-health.html>`__
- `Stats API <https://fess.codelibs.org/stable/api/admin/api-admin-stats.html>`__
- `Log Notification <https://fess.codelibs.org/stable/config/admin-log-notification.html>`__
- `Log Configuration <https://fess.codelibs.org/stable/config/admin-logging.html>`__
- `Log Files <https://fess.codelibs.org/stable/admin/log-guide.html>`__
- `Backup <https://fess.codelibs.org/stable/admin/backup-guide.html>`__
- `Backup API <https://fess.codelibs.org/stable/api/admin/api-admin-backup.html>`__
- `Index Management <https://fess.codelibs.org/stable/config/admin-index-backup.html>`__
- `Failure URL <https://fess.codelibs.org/stable/admin/failureurl-guide.html>`__
- `Maintenance <https://fess.codelibs.org/stable/admin/maintenance-guide.html>`__
