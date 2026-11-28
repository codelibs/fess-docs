======================================
Running and Searching Fess with Docker
======================================

Introduction
============

When you start evaluating Fess, the first thing you want to know is "what kind of searches can I do if I run it myself?"
In this article, we start Fess 15.9 with Docker, crawl about 20 web pages, and try out the search syntax, step by step.

As our subject, we use the English "Search Guide" on the official Fess website (a set of pages that explain AND search, wildcard search, and so on).
Because the target is limited to one place, the crawl finishes in a few minutes, and you can read the search results to check them.

By following the steps in this article as written, you will be able to:

- Start Fess and OpenSearch with Docker Compose, and stop and restart them
- Complete the administrator's first login and the required password change
- Create a web crawl configuration, run the crawl, and confirm that it has finished
- Try AND, OR, exclusion, phrase and field searches

Settings for production environments (monitoring, backup, SSO, scaling) are not covered.
From "What to Read Next" at the end, move on to the article that fits your goal.

The Environment We Build
========================

The Compose files from the docker-fess repository start the following two containers.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Service
     - Role
     - Where data is stored
   * - ``fess01``
     - Fess itself (image ``ghcr.io/codelibs/fess:15.9.0``). Provides the search page and the admin console on port 8080
     - No volume (inside the container)
   * - ``search01``
     - OpenSearch (image ``ghcr.io/codelibs/fess-opensearch``). Port 9200 is also published
     - Volumes ``search01_data`` and ``search01_dictionary``

The index, crawl configurations, users, job logs and so on are all stored in OpenSearch, so they remain in the ``search01_data`` volume.
On the other hand, settings changed under [System] > [General] in the admin console are stored in ``system.properties`` inside the ``fess01`` container.
This difference matters later, in "Stopping and Restarting".

.. warning::

   In this setup, OpenSearch runs with its security plugin disabled and is published on port 9200 of the host.
   Use it as a setup for trying things out on your own PC; if you run it on a shared server, read :doc:`guide-10` and :doc:`guide-15` first.

Prerequisites
=============

- Docker and Docker Compose (the ``docker compose`` command) are available
- Docker can use at least 4GB of memory (the OpenSearch heap alone takes 1GB)
- You can connect to the internet (used for pulling images and for crawling)

On Linux or WSL2, raise ``vm.max_map_count``, which OpenSearch needs in order to start.

::

    $ sudo sysctl -w vm.max_map_count=262144

This value reverts when the OS restarts.
If you will keep using it, also add it to ``/etc/sysctl.conf``.

::

    $ echo 'vm.max_map_count=262144' | sudo tee -a /etc/sysctl.conf

Starting Fess
=============

Getting the Compose Files for 15.9.0
------------------------------------

The Compose files on the default branch of docker-fess are updated whenever a new version is released.
To pin the version to 15.9.0, get the files from the ``v15.9.0`` tag.

::

    $ mkdir fess-docker
    $ cd fess-docker
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose.yaml
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-opensearch3.yaml

``compose.yaml`` defines only ``fess01``; ``search01``, which ``fess01`` depends on, is in ``compose-opensearch3.yaml``.
For this reason, every ``docker compose`` command from here on specifies both files with ``-f``.
If you run a command with only one of them, neither starting nor stopping works correctly.

Starting and Waiting Until It Is Ready
--------------------------------------

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

The first time takes a few minutes because the images have to be pulled.
Check the status with the following command.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

``fess01`` starts after ``search01`` becomes healthy.
Fess is ready when the STATUS of ``fess01`` shows ``(healthy)``.
The health check of ``fess01`` calls ``/api/v2/health``, and the first 120 seconds after startup are treated as a grace period.

If it takes a long time to become healthy, check the logs.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01

If port 8080 is used by another application, change ``ports`` in ``compose.yaml`` to something like ``"9080:8080"``.
For other startup problems, see `Installation Troubleshooting <https://fess.codelibs.org/stable/install/troubleshooting.html>`__.

Open ``http://localhost:8080/`` in your browser to see the Fess search page.
Nothing has been crawled yet, so searching at this point returns no results.

Logging In to the Admin Console
===============================

Open ``http://localhost:8080/admin/`` and log in with the user name ``admin`` and the password ``admin``.

The initial password ``admin`` is configured so that it cannot be kept, so after logging in you are taken to a screen that says "You need to update your password".

1. Enter the same password in "New Password" and "Confirm New Password" (at least 8 characters)
2. Click [Update]

When the update is done, the admin console dashboard opens.
From then on, log in with the new password.
This password is stored in OpenSearch, so it remains even if you recreate the containers (if you delete the volumes as well, it goes back to ``admin``).

Creating a Crawl Configuration
==============================

Deciding What to Crawl
----------------------

This time, we crawl the English "Search Guide" on the official Fess website.
It consists of about 20 pages under ``https://fess.codelibs.org/stable/user/``, where ``stable`` refers to the documentation of the current stable version (15.9).

Registering a Web Crawl Configuration
-------------------------------------

1. In the left menu of the admin console, open [Crawler] > [Web]
2. Click [Create New]
3. Enter the following fields. Leave all other fields at their defaults

   .. list-table::
      :header-rows: 1
      :widths: 30 70

      * - Field
        - Value
      * - Name
        - ``Fess Search Guide``
      * - URLs
        - ``https://fess.codelibs.org/stable/user/index.html``
      * - Included URLs
        - ``https://fess.codelibs.org/stable/user/.*``
      * - Max Access Count
        - ``50``

4. Click [Create]

The fields mean the following.

- "Name" is required. You cannot create the configuration while it is empty
- "URLs" is the starting point of the crawl
- "Included URLs" is a regular expression; links to URLs that do not match it are not followed. If you leave it empty, the crawler follows links in the pages to other versions, other languages and even external sites
- "Max Access Count" is an upper limit in case the regular expression is written incorrectly

Among the fields left at their defaults, "Number of Threads" is ``1`` and "Interval" is ``10000`` milliseconds.
Because the crawler waits 10 seconds for each page, the load on the target site is kept low.
"Permissions" contains ``{role}guest``, so users who are not logged in can also see the search results.
How to show different results to different departments is covered in :doc:`guide-05`.

.. note::

   If you target URLs with a version number, such as ``/15.9/``, not a single page is registered.
   These pages contain a ``<link rel="canonical">`` that points to ``/stable/``.
   The Fess crawler does not register such a page and follows the canonical URL instead.
   That URL falls outside the "Included URLs" regular expression, so nothing is registered.
   When you target your own company's site, also check that the canonical URLs are covered by the regular expression.

.. tip::

   With [System] > [Wizard], you can also create a crawl configuration just by entering "Name", "Crawl Path", "Max Access Count" and "Depth", and go straight on to [Start Crawling].
   However, a configuration created with the wizard has no "Included URLs", so you cannot narrow the range of links that are followed.
   When you want to narrow the target as in this article, create the configuration from [Crawler] > [Web] as described above.

Running the Crawl and Confirming It Has Finished
================================================

Starting the Crawl
------------------

Saving the configuration does not start the crawl.

1. Open [System] > [Scheduler]
2. Click "Default Crawler" in the list
3. Click [Start Now]

"Default Crawler" is the job that runs all enabled web, file system and data store crawl configurations together.
By default, this job has the cron expression ``0 0 * * *`` and also runs automatically once a day.
If you leave the containers running, the same configurations are crawled again on the following days.

With this configuration, about 20 pages are fetched at 10-second intervals, so expect it to take a few minutes.

Confirming That It Has Finished
-------------------------------

Check in the following order.

1. Open [System Info] > [Job Log]. When the "Status" of the "Default Crawler" row changes from "Running" to "OK", the job has finished. If it shows "Fail", click that row to open the details and check "Result"
2. Open [System Info] > [Crawling Info] and click the top (latest) session in the list. "Index Size (Web/File)" is the number of documents registered by this crawl. This time it will be around 20
3. If the count is lower than expected, open [System Info] > [Failure URL]. URLs that could not be fetched because of connection errors and the like are recorded there, together with the reason

Even when the job shows "OK", the number of registered documents can be 0.
URLs that do not match the "Included URLs" regular expression are treated as out of scope, not as errors, so they are not recorded in Failure URL either.
If the count is 0 and Failure URL is also empty, review how the URL and the regular expression are written (``https`` versus ``http``, whether the trailing ``.*`` is present, and so on).

Trying Some Searches
====================

Open ``http://localhost:8080/`` and search.
The search page uses ``bootstrap``, the theme bundled with Fess.

First, enter ``wildcard`` and search.
Pages such as Wildcard Search and Special Characters appear in the results.
Clicking a result title opens the original page (fess.codelibs.org).

Next, enter the following search terms one by one.
You can check the results of each of them against the pages you just crawled.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Search terms to enter
     - Meaning
   * - ``field URL``
     - Separating terms with a space makes an AND search, so only pages containing both appear
   * - ``wildcard OR fuzzy``
     - Pages containing either term appear. ``OR`` must be uppercase, with a space before and after it
   * - ``search -label``
     - Removes pages containing "label" from the results. Put ``-`` immediately before the term you want to exclude
   * - ``"range search"``
     - Finds pages that contain the quoted words in exactly that order (phrase search)
   * - ``title:sort``
     - Finds only pages whose title contains "sort" (field search)

If you write ``or`` or ``and`` in lowercase, it is not treated as an operator but as an ordinary search term.

The syntax used here, and the rest of the syntax such as wildcard, fuzzy and range searches, are explained in the `Search Guide <https://fess.codelibs.org/stable/user/index.html>`__ you just crawled.
You can also search your own Fess for a piece of syntax you are curious about, then open and read that page.

Stopping and Restarting
=======================

What remains depends on how you stop the containers.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Operation
     - What remains
     - What is lost
   * - ``stop`` → ``start``
     - Everything
     - Nothing
   * - ``down`` → ``up -d``
     - Everything stored in OpenSearch (index, crawl configurations, users and passwords, job logs, and so on)
     - Everything stored inside the ``fess01`` container (settings changed under [System] > [General], and so on)
   * - ``down -v``
     - Nothing
     - Everything (the administrator password also goes back to ``admin``)

For everyday stopping, use ``stop``, and to restart, use ``start``.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml start

``down`` removes the containers.
OpenSearch data remains in the volumes, but the [General] settings are written to ``system.properties`` inside the ``fess01`` container, so they disappear together with the container.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

When you have finished trying Fess out and want to clean up everything, including the data, add ``-v``.
The volumes are deleted as well, and this cannot be undone.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

Some of the settings changed under [General] remain even after the containers are recreated if you specify them in ``FESS_JAVA_OPTS`` in ``compose.yaml`` (some items, such as SSO connection settings, cannot be specified this way).
For the procedure, see `Docker Installation (Detailed Guide) <https://fess.codelibs.org/stable/install/install-docker.html>`__.

What to Read Next
=================

Move on to the next article that fits your goal.

- To understand how Fess is structured and how to read through the articles: :doc:`guide-01`
- To put a search box on an existing intranet site or portal: :doc:`guide-03`
- To search internal websites and file servers together: :doc:`guide-04`
- To change which search results are visible depending on department or position: :doc:`guide-05`
- To also search data in Slack, Confluence, databases and so on: first :doc:`datastore-basics`, then :doc:`guide-06`, :doc:`guide-07` and :doc:`guide-12`
- To have generative AI answer from internal documents: :doc:`guide-19`
- To find documents with similar meaning even when keywords do not match: :doc:`guide-18`
- To set up monitoring and backups for production operation: :doc:`guide-10`
- To configure SSO and access protection: :doc:`guide-15`
- To scale out as documents and users grow: :doc:`guide-14`

References
==========

- `Docker Installation (Detailed Guide) <https://fess.codelibs.org/stable/install/install-docker.html>`__
- `docker-fess (GitHub) <https://github.com/codelibs/docker-fess>`__
- `Web Crawl Configuration <https://fess.codelibs.org/stable/admin/webconfig-guide.html>`__
- `Job Log <https://fess.codelibs.org/stable/admin/joblog-guide.html>`__
- `Search Guide <https://fess.codelibs.org/stable/user/index.html>`__
