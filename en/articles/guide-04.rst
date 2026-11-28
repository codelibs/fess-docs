============================================
Searching Websites and File Servers Together
============================================

Introduction
============

Internal documents tend to be spread across several places: the intranet portal, departmental shared folders, a directory that holds old documents for archiving, and so on.
Anyone looking for something first has to remember where it lives, and then search each place separately.

In this article, we use Fess 15.9 to crawl the following three locations so that they can all be searched from a single search box.
On the search page, we make it possible to narrow results with labels, such as "portal only" or "shared folder only".

- The intranet portal (a website)
- A shared folder on a Windows file server (SMB)
- An archive directory on the server (local files)

The steps assume the Docker environment started in :doc:`guide-02` (``fess01`` and ``search01``).
Cloud storage such as Google Drive, SharePoint and Box is covered in :doc:`guide-07`.
Points to check before introducing file server search are summarized in :doc:`file-server-search`.

What We Will Build
==================

.. list-table::
   :header-rows: 1
   :widths: 18 40 14 28

   * - Target
     - Path to crawl
     - Label value
     - Crawl schedule
   * - Intranet portal
     - ``https://portal.example.com/``
     - ``portal``
     - Daily at 2:00
   * - Shared folder
     - ``smb://fileserver.example.com/shared/``
     - ``shared``
     - Daily at 3:00
   * - Archive
     - ``file:/data/archive/`` (``/srv/archive`` on the host)
     - ``archive``
     - Every Sunday at 4:00

The host names and directories are examples.
Replace them with those of your own environment.
We assume you have a service account that can read the shared folder (read-only access is enough), and that the ``fess01`` container can connect to the file server's SMB port (445).

Labels are assigned at crawl time, so create them before the crawl configurations.
Follow the sections of this article in order.

Making the Archive Directory Readable from the Container
========================================================

In the ``compose.yaml`` of docker-fess v15.9.0, no volumes are defined for ``fess01``.
As a result, ``/srv/archive`` on the host is not visible from inside the container as is.
Add ``volumes`` to ``fess01`` in ``compose.yaml``, and also add a ``FESS_JAVA_OPTS`` line to ``environment``.

.. code-block:: yaml

    services:
      fess01:
        image: ghcr.io/codelibs/fess:15.9.0
        container_name: fess01
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "FESS_DICTIONARY_PATH=${FESS_DICTIONARY_PATH:-/usr/share/opensearch/config/dictionary/}"
          - "FESS_JAVA_OPTS=-Duser.timezone=Asia/Tokyo -Dfess.system.day.for.cleanup=10"
        volumes:
          - /srv/archive:/data/archive:ro
        # keep ports and everything after it unchanged

- ``/srv/archive:/data/archive:ro`` mounts ``/srv/archive`` on the host at ``/data/archive`` in the container, read-only
- ``-Duser.timezone=Asia/Tokyo`` makes the run times of the jobs configured later be interpreted in Japan time. Neither compose.yaml nor the image specifies a time zone, so without it the jobs run at times shifted from Japan time
- ``-Dfess.system.day.for.cleanup=10`` sets the default document expiration period (in days) to 10 days. The reason is explained later in "Weekly Jobs and Document Expiration"

After making the change, recreate the containers.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Because ``fess01`` is recreated, any settings you changed under [System] > [General] up to this point are lost (see "Stopping and Restarting" in :doc:`guide-02`).
Make any changes in [General] after this step.

Fess inside the container runs as the user ``fess`` (UID 1001).
Confirm that this user can list the files.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml exec -u fess fess01 ls /data/archive

If you get ``Permission denied``, make everything under ``/srv/archive`` on the host readable by UID 1001 (for example, grant read permission to others, plus execute permission on directories).

Creating Labels
===============

A label is assigned when a document's URL matches a regular expression.
The crawl configuration screens have no field for choosing a label (it is hidden by default), so the scope of each label is specified in the label's own "Included Paths".

Under [Crawler] > [Label] > [Create New], create the following three labels.

.. list-table::
   :header-rows: 1
   :widths: 18 14 68

   * - Name
     - Value
     - Included Paths
   * - Portal
     - ``portal``
     - ``https://portal.example.com/.*``
   * - Shared Folder
     - ``shared``
     - ``smb://fileserver.example.com/shared/.*``
   * - Archive
     - ``archive``
     - ``file:/data/archive/.*``

- "Name" is the text shown on the search page, and it can contain non-ASCII characters such as Japanese
- "Value" accepts only alphanumeric characters and underscores (hyphens and non-ASCII characters cause an input error)
- "Included Paths" must match the entire URL, so do not omit the trailing ``.*``. If you leave it empty, the label is not assigned to any document
- "Permissions" contains ``{role}guest``. This shows the label to users who are not logged in as well, so leave it as is

Documents crawled before the labels were created have no labels.
If you add or change labels later, apply them to existing documents either by crawling again or by running "Label Updater" with [Start Now] under [System] > [Scheduler].

Creating Crawl Configurations
=============================

Intranet Portal (Web Crawl)
---------------------------

Under [Crawler] > [Web] > [Create New], enter the following fields and click [Create].

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Field
     - Value
   * - Name
     - ``Intranet Portal``
   * - URLs
     - ``https://portal.example.com/``
   * - Included URLs
     - ``https://portal.example.com/.*``
   * - Excluded URLs
     - Add ``https://portal.example.com/admin/.*`` below the lines already there

"Excluded URLs" comes pre-filled with regular expressions that exclude images, CSS and the like.
Do not delete them; add a line instead.
"Number of Threads" defaults to ``1`` and "Interval" to ``10000`` milliseconds, settings that keep the load on the portal low.

Shared Folder (SMB) and File Authentication
-------------------------------------------

First, create the following configuration under [Crawler] > [File System] > [Create New].

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Field
     - Value
   * - Name
     - ``Shared Folder``
   * - Paths
     - ``smb://fileserver.example.com/shared/``
   * - Included Paths
     - ``smb://fileserver.example.com/shared/.*``
   * - Excluded Paths
     - ``.*\.tmp$``

For file crawling, "Number of Threads" defaults to ``5`` and "Interval" to ``1000`` milliseconds.

Next, link the service account to this configuration.
File authentication is created by selecting a file crawl configuration.
Until at least one file crawl configuration exists, [Create New] is not shown on the [File Authentication] screen.

Under [Crawler] > [File Authentication] > [Create New], enter the following fields and click [Create].

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Field
     - Value
   * - Hostname
     - ``fileserver.example.com`` (written exactly as the host name in the path)
   * - Port
     - Leave empty
   * - Scheme
     - ``Samba``
   * - Username / Password
     - Those of the service account
   * - Parameters
     - For a domain account, specify the domain name, as in ``domain=EXAMPLE``
   * - File Crawl Config
     - ``Shared Folder``

"Hostname" must match the host name in the path literally.
If you wrote the path with an IP address, enter the IP address here too.
An authentication entry whose "Port" is left empty is used for paths that do not specify a port, such as ``smb://hostname/sharename/``.

.. note::

   By default, files crawled over SMB are given roles derived from the file's access permissions (ACL), which are added to the crawl configuration's "Permissions".
   As long as the default ``{role}guest`` remains in "Permissions", everyone can search them, including users who are not logged in.
   To show different search results according to access permissions, see :doc:`file-server-search` and :doc:`guide-05`.

Archive (Local Files)
---------------------

Under [Crawler] > [File System] > [Create New], create the following configuration.
Specify the path as it appears inside the container.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Field
     - Value
   * - Name
     - ``Archive``
   * - Paths
     - ``file:/data/archive/``
   * - Included Paths
     - ``file:/data/archive/.*``
   * - Excluded Paths
     - ``.*\.(log|bak)$``

Write local files with a single slash after ``file:``, as in ``file:/data/archive/``.
The URLs of the files the crawler finds take the form ``file:/data/archive/2020/report.pdf``, and "Included Paths" is matched against these URLs.
If you write ``file:///data/archive/.*``, it matches no files and nothing is indexed.

Creating a Job for Each Configuration
=====================================

The scheduler's "Default Crawler" runs all enabled crawl configurations together every day at 0:00.
To run each target at a different time, create a job for each crawl configuration.

1. Under [Crawler] > [Web], click "Intranet Portal", then click [Create New Job] on the details screen
2. The job creation screen opens with ``Web Crawler - Intranet Portal`` in "Name" and, in "Script", content that crawls only this configuration
3. "Schedule" is empty, so enter a cron expression and click [Create]
4. Do the same for "Shared Folder" and "Archive" under [Crawler] > [File System] (the names look like ``File Crawler - Shared Folder``)

.. list-table::
   :header-rows: 1
   :widths: 40 25 35

   * - Job
     - Schedule
     - Meaning
   * - ``Web Crawler - Intranet Portal``
     - ``0 2 * * *``
     - Daily at 2:00
   * - ``File Crawler - Shared Folder``
     - ``0 3 * * *``
     - Daily at 3:00
   * - ``File Crawler - Archive``
     - ``0 4 * * 0``
     - Every Sunday at 4:00

A cron expression is written in the order "minute hour day month day-of-week", and ``0`` for day of week means Sunday.

Finally, keep "Default Crawler" from crawling the same configurations again at 0:00.
Under [System] > [Scheduler], click "Default Crawler", clear "Schedule" with [Edit], and click [Update].
If you leave "Enabled" checked under "Status", you can still run it with [Start Now] whenever you want to crawl all configurations together (if you disable it, [Start Now] is no longer shown).

Weekly Jobs and Document Expiration
-----------------------------------

Documents indexed by a crawl are given an expiration time, and once it passes, the "Doc Purger" job (which runs every minute) deletes them from the index.
The expiration time is the start time of the crawl plus the number of days in "Delete old documents" under [System] > [General], which defaults to ``3`` days.
If the next crawl finds the same file, its expiration time is extended.

With the default, documents in the archive, which is crawled only on Sundays, can no longer be found by Wednesday.
This number of days therefore has to be larger than the longest crawl interval (7 days).
In this article we set it to ``10`` days, leaving a margin so that documents are not lost even if a job fails once.

- In the Docker environment, the ``-Dfess.system.day.for.cleanup=10`` mentioned above becomes this default. Values set in [General] are lost when ``fess01`` is recreated, so writing it in compose.yaml is more reliable
- In environments other than Docker, set "Delete old documents" in [General] to ``10`` and click [Update]

Increasing this number of days also means that files deleted from the file server remain in search results for up to that many days after the last crawl that found them.

Running the Jobs and Checking the Results
=========================================

Running the Jobs
----------------

Instead of waiting until the next day, click each of the three jobs in turn under [System] > [Scheduler] and click [Start Now] for each.

Confirming Completion
---------------------

1. Under [System Info] > [Job Log], wait for the "Status" of the three jobs to change from "Running" to "OK". If one shows "Fail", click its row and check "Result"
2. Under [System Info] > [Crawling Info], look at "Index Size (Web/File)" for each session and check that the number of indexed documents is close to what you expect
3. If the numbers are low, open [System Info] > [Failure URL]. It records the URLs that could not be fetched, along with the error type and log

Common causes are as follows.

- The shared folder has 0 documents and its paths are recorded in Failure URL: review the "Hostname" in file authentication and how the path is written, the selected "File Crawl Config", and the password. If the log shows connection errors, check that the container can resolve the file server's name and reach port 445
- The archive has 0 documents and Failure URL is empty: check that the path is not written with ``file:///`` and that "Included Paths" has the same form as the path
- Read errors occur for the archive: use the ``exec -u fess`` command shown earlier to check that the container can read the files

Filtering by Label
------------------

At ``http://localhost:8080/``, search for a word likely to appear in all three locations.
The results mix portal pages, Office documents from the shared folder, PDFs from the archive and so on, ordered by relevance.

On the 15.9 search page (theme ``bootstrap``), label filtering is available in two places.

- The "Label" list shown next to the search results: the labels in the results are listed with their counts, and clicking one narrows the results to that label
- The gear button to the right of the search box: it opens "Search Options", where you select one or more entries in the "Labels" list and click [Search]. If you select several, documents with any of those labels are included; if you select none, everything is included

When you filter, a parameter such as ``fields.label=shared`` is added to the URL.
If "Label" does not appear next to the search results, or filtering returns 0 results, check whether you crawled before creating the labels (running "Label Updater" fixes this).
If the "Labels" list does not appear in "Search Options", check that the label's "Permissions" include the role of the person searching.

Search Result Links and Path Mapping
====================================

When you click a search result from the shared folder or the archive, Fess reads the file and returns it to the browser.
This is done by "Search File Proxy" in [General], which is enabled by default.
Files can be opened even though the browser cannot open ``smb://`` or ``file:`` URLs directly.

If the same files as the archive are also published on an internal web server (here ``https://archive.example.com/``) and you want users to open them there, convert the URLs with path mapping.

Under [Crawler] > [Path Mapping] > [Create New], enter the following fields and click [Create].

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Value
   * - Regex
     - ``^file:/data/archive/(.*)$``
   * - Replacement
     - ``https://archive.example.com/$1``
   * - Process Type
     - Displaying

"Process Type" initially has "Crawling" selected, so be sure to change it to "Displaying".

- Displaying: the URL in the index stays ``file:/data/archive/...``; only the destination when a search result link is clicked changes. It takes effect as soon as it is created, and no re-crawl is needed
- Crawling: rewrites the URL stored in the index itself. It has no effect until you re-crawl, and the label's "Included Paths" must also be changed to match the rewritten ``https://`` URLs

After setting it up, search and click an archive result to confirm that it opens on the ``https://archive.example.com/`` web server.

What to Read Next
=================

- To change which search results people see according to their department or position: :doc:`guide-05`
- To review the prerequisites for file server search (supported formats, carrying over access permissions): :doc:`file-server-search`
- To also search files in Google Drive, SharePoint and Box: :doc:`guide-07`
- To improve search quality by looking at search logs: :doc:`guide-08`
- To set up monitoring and backups for production operation: :doc:`guide-10`

References
==========

- `File Crawling (File Server Search) <https://fess.codelibs.org/stable/admin/fileconfig-guide.html>`__
- `File Authentication <https://fess.codelibs.org/stable/admin/fileauth-guide.html>`__
- `Label <https://fess.codelibs.org/stable/admin/labeltype-guide.html>`__
- `Scheduler <https://fess.codelibs.org/stable/admin/scheduler-guide.html>`__
- `General Settings <https://fess.codelibs.org/stable/admin/general-guide.html>`__
- `Path Mapping <https://fess.codelibs.org/stable/admin/pathmap-guide.html>`__
- `Docker Installation (Detailed Guide) <https://fess.codelibs.org/stable/install/install-docker.html>`__
