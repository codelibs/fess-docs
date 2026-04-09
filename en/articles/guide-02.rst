============================================================
Part 2: A 5-Minute Search Experience -- First Contact with Fess Using Docker Compose
============================================================

Introduction
============

In the previous article, we introduced the need for an enterprise search platform and provided an overview of Fess.
In this article, we will walk through the shortest path to launching Fess and experiencing search firsthand.

The goal is to quickly understand what kind of search experience Fess provides.
Using Docker Compose, we will set up a Fess environment with just a few commands, crawl a website, and perform a search.

Target Audience
===============

- Those trying Fess for the first time
- Those who want to quickly conduct a PoC (Proof of Concept) for evaluating adoption
- Those with basic Docker knowledge

Prerequisites
=============

- An environment where Docker and Docker Compose are available
- At least 4GB of memory (8GB or more recommended)
- Internet connection

Preparation (Linux / WSL2)
--------------------------

OpenSearch, which Fess uses, requires a large number of memory map areas at startup.
On Linux or WSL2 environments, increase ``vm.max_map_count`` with the following command.

::

    $ sudo sysctl -w vm.max_map_count=262144

This setting resets when the OS is restarted. To make it persistent, add it to ``/etc/sysctl.conf``.

::

    $ echo 'vm.max_map_count=262144' | sudo tee -a /etc/sysctl.conf

.. note::

   This setting is not required when using Docker Desktop on macOS.

Starting Fess
=============

Obtaining the Docker Compose File
----------------------------------

The Docker Compose file for Fess is available in a GitHub repository.
Obtain it with the following commands.

::

    $ git clone https://github.com/codelibs/docker-fess.git
    $ cd docker-fess/compose

The compose directory contains several configuration files.
Let's start with a simple configuration.

Starting Up
-----------

Start Fess and OpenSearch with the following command.

::

    $ docker compose up -d

The first startup may take several minutes as Docker images are downloaded.
You can check the startup status with the following command.

::

    $ docker compose ps

Once all containers show "running", the startup is complete.

Accessing the Search Screen
----------------------------

Open ``http://localhost:8080/`` in your browser.
If the Fess search top page is displayed, the system is running correctly.

At this point, the index is still empty, so no results will be returned when searching.
In the next step, we will register crawl targets and make content searchable.

Exploring the Admin Console
============================

Logging In to the Admin Console
--------------------------------

Access ``http://localhost:8080/admin/`` and log in to the admin console.
The default credentials are as follows.

- Username: ``admin``
- Password: ``admin``

The admin console dashboard provides an overview of the system status.

Admin Console Layout
---------------------

The left-side menu of the admin console lists the main management functions of Fess.
Let's take a brief look at what is available.

**Crawler**

This section is for registering crawl targets. It manages crawl configurations for three types: web, file system, and data store.

**System**

This section provides system-wide management functions such as scheduler, design, and dictionaries. The dictionaries section manages settings related to search quality, including synonyms and stop words.

**System Info**

This section provides various logs and maintenance functions, including search logs, job logs, crawl information, and backups.

Crawling a Website
===================

Registering a Crawl Target
----------------------------

Let's crawl an actual website and make it searchable.
Here, we will use the official Fess website as the target.

1. From the left menu of the admin console, select [Crawler] > [Web]
2. Click [Create New]
3. Enter the following information

   - URL: ``https://fess.codelibs.org/ja/``
   - Included URLs For Crawling: ``https://fess.codelibs.org/ja/.*``
   - Max Access Count: ``50``
   - Number of Thread: ``2``
   - Interval time: ``10000``

4. Click [Create] to save

This completes the configuration to crawl up to 50 pages of the official Fess website (Japanese pages) at 10-second intervals.

Running the Crawl
------------------

Saving the configuration alone does not start crawling.
To start crawling, execute a job from the scheduler.

1. Select [System] > [Scheduler]
2. Select "Default Crawler"
3. Click [Start Now]

The crawl will begin.
You can check the progress from [System Info] > [Crawl Info].
For about 50 pages, the crawl should complete within a few minutes.

Experiencing Search
====================

Trying a Search
----------------

After the crawl is complete, return to the search screen at ``http://localhost:8080/`` and try searching.

For example, entering "install" and searching will display pages from the Fess site related to installation in the search results.

Search Results Elements
------------------------

The search results screen displays the following elements.

**Search Results List**

Each result shows a title, URL, and a text excerpt (snippet).
Portions matching the search keywords are highlighted.

**Result Count and Response Time**

The number of hits and the time taken for the search are displayed at the top of the search results.

**Pagination**

When results span multiple pages, pagination navigation is displayed.

More Useful Search Features
-----------------------------

Fess provides various search features beyond simple keyword search.

**AND/OR Search**

Separating multiple keywords with spaces performs an AND search.
Using ``OR`` enables OR search.

::

    インストール Docker       # AND search (contains both)
    インストール OR Docker    # OR search (contains either)

**Phrase Search**

Enclosing terms in double quotes searches for documents matching that exact word order.

::

    "全文検索サーバー"

**Exclusion Search**

To search for results that do not contain a specific keyword, use the minus sign.

::

    インストール -Windows    # Results not containing "Windows"

Stopping and Restarting the Environment
========================================

Stopping
--------

When you are done with the search experience, stop the environment with the following command.

::

    $ docker compose down

This stops the environment while preserving data (index), so restarting will resume from the same state.

Complete Cleanup Including Data
---------------------------------

To delete volumes as well, execute the following command.

::

    $ docker compose down -v

In this case, the indexes created by crawling will also be deleted.

What the Search Experience Reveals
====================================

Through this hands-on experience, you have confirmed the basic operation of Fess.
At this point, you may have several questions in mind regarding real-world business use.

- "Can internal file servers also be searched?" -- Covered in **Part 4**
- "Can a search box be embedded in an existing internal site?" -- Covered in **Part 3**
- "Can we control what information is visible per department?" -- Covered in **Part 5**
- "Can we search Slack and Confluence too?" -- Covered in **Part 6**
- "Can AI answer questions for us?" -- Covered in **Part 19**

Fess can handle all of these scenarios.
Throughout this series, we will introduce how to implement these step by step.

Summary
=======

In this article, we launched Fess using Docker Compose and experienced the full flow from website crawling to search.

- Start Fess + OpenSearch with a single Docker Compose command
- Register crawl targets from the admin console and run them via the scheduler
- Experience keyword search, AND/OR search, and phrase search on the search screen
- Stopping and restarting the environment is straightforward

In the next article, we will introduce how to embed Fess search functionality into existing websites and portals.

References
==========

- `Fess <https://fess.codelibs.org/ja/>`__

- `Docker Fess <https://github.com/codelibs/docker-fess>`__

- `Fess Installation Guide <https://fess.codelibs.org/ja/15.5/install/index.html>`__
