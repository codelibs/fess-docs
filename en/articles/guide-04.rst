============================================================
Part 4: Unified Search Across Scattered Files -- Building Cross-Search for Multi-Source Environments
============================================================

Introduction
============

In the previous article, we introduced how to integrate Fess search functionality into an existing website.
However, in real enterprise environments, information is scattered across various locations -- not just websites, but also file servers and cloud storage.

In this article, we will integrate multiple data sources into Fess and build an environment where users can search across all documents from a single search box.

Target Audience
===============

- Those whose internal documents are scattered across multiple locations
- Those who are dissatisfied with searching file servers or cloud storage
- You should have Fess up and running using the procedures from Part 2

Scenario
========

Let us assume a mid-sized company. In this company, documents are scattered across the following locations:

- **Internal website**: Company portal, internal blog
- **File server**: Shared folders for each department (SMB/CIFS)
- **Local files**: Specific directories on the server

When employees think, "Where was that document?", they have to search each tool individually.
We will unify this with Fess so that everything can be found through a single search box.

Designing Data Sources
======================

When building cross-search, the first important step is designing "what to index and how."

Organizing Search Targets
-------------------------

Start by organizing the data sources to be indexed.

.. list-table:: Data Source Overview
   :header-rows: 1
   :widths: 20 25 25 30

   * - Data Source
     - Type
     - Approximate Scale
     - Update Frequency
   * - Company Portal
     - Web Crawl
     - Hundreds of pages
     - Weekly
   * - Technical Blog
     - Web Crawl
     - Tens to hundreds of pages
     - As needed
   * - Shared Folder
     - File Crawl
     - Tens of thousands of files
     - Daily
   * - Archive
     - File Crawl
     - Thousands of files
     - Monthly

Designing Classification with Labels
-------------------------------------

Using Fess's "Label" feature, you can categorize search targets.
Users can select a label when searching to narrow results to a specific category.

In this scenario, we will configure the following labels:

- **Portal**: Information from the company portal and blog
- **Shared Files**: Documents on the file server
- **Archive**: Past documents

Configuring Labels
^^^^^^^^^^^^^^^^^^

1. In the admin panel, go to [Crawler] > [Labels]
2. Click [Create New] to create a label

Set a "Name" and "Value" for each label.
The value should be alphanumeric and is used to associate the label with crawl configurations.

Building Crawl Configurations
=============================

Web Crawl Configuration
-----------------------

This is the crawl configuration for the company portal.

1. Go to [Crawler] > [Web] > [Create New]
2. Configure the following:

   - URL: ``https://portal.example.com/``
   - Included URLs for Crawling: ``https://portal.example.com/.*``
   - Excluded URLs for Crawling: ``https://portal.example.com/admin/.*``
   - Max Access Count: ``500``
   - Number of Threads: ``3``
   - Interval: ``5000``
   - Label: Portal

3. Click [Create]

By setting excluded URLs, you can exclude pages such as admin screens that should not be indexed.

File Crawl Configuration
------------------------

This is the crawl configuration for the shared folder.

1. Go to [Crawler] > [File System] > [Create New]
2. Configure the following:

   - Path: ``smb://fileserver.example.com/shared/``
   - Included Paths for Crawling: ``smb://fileserver.example.com/shared/.*``
   - Excluded Paths for Crawling: ``.*\\.tmp$``
   - Max Access Count: ``10000``
   - Number of Threads: ``5``
   - Interval: ``1000``
   - Label: Shared Files

3. Click [Create]

**SMB Authentication Configuration**

If the file server requires authentication, you need to configure file authentication.

1. Go to [Crawler] > [File Authentication] > [Create New]
2. Configure the following:

   - Hostname: ``fileserver.example.com``
   - Scheme: ``Samba``
   - Username: Service account username
   - Password: Service account password

3. Click [Create]

Local File Crawling
-------------------

To crawl a specific directory on the server, specify the file path directly.

1. Go to [Crawler] > [File System] > [Create New]
2. Configure the following:

   - Path: ``file:///data/archive/``
   - Included Paths for Crawling: ``file:///data/archive/.*``
   - Excluded Paths for Crawling: ``.*\\.(log|bak)$``
   - Max Access Count: ``5000``
   - Label: Archive

3. Click [Create]

Designing a Crawl Schedule
===========================

When crawling multiple data sources, schedule design becomes important.
Running all crawls simultaneously places a heavy load on server resources and on the target servers as well.

Distributing the Schedule
-------------------------

Distribute crawl schedules according to the update frequency of each data source.

.. list-table:: Crawl Schedule Example
   :header-rows: 1
   :widths: 25 25 50

   * - Data Source
     - Execution Timing
     - Reason
   * - Company Portal
     - Daily at 2:00
     - Completes quickly due to the small number of pages
   * - Shared Folder
     - Daily at 3:00
     - Run at night due to the large number of files
   * - Archive
     - Every Sunday at 4:00
     - Weekly is sufficient due to low update frequency

Configuring the Scheduler
-------------------------

From the admin panel, go to [System] > [Scheduler] to configure the execution timing for crawl jobs.
The default "Default Crawler" job executes all crawl configurations at once.

Making Search Results User-Friendly with Path Mapping
=====================================================

Crawled URLs and file paths may be difficult for users to understand.
Path mapping allows you to transform the URLs displayed in search results.

Configuration Example
---------------------

Convert file server paths to URLs that users can access in their browser.

1. Go to [Crawler] > [Path Mapping] > [Create New]
2. Configure the following:

   - Regular Expression: ``smb://fileserver.example.com/shared/(.*)``
   - Replacement: ``https://fileserver.example.com/shared/$1``

This allows users to click on a link in the search results and access the file directly in their browser.

Using Cross-Search
==================

Narrowing Results with Labels
-----------------------------

Once crawling is complete, try out the cross-search on the search screen.

The search screen displays label tabs or a dropdown.
Users can select "All" for cross-search or select a specific label to limit the search to that category.

For example, searching for "project plan" returns mixed results including portal articles, Word files from the shared folder, and PDFs from the archive.
Narrowing by the "Shared Files" label limits the results to documents on the file server only.

Search Result Ordering
----------------------

By default, results are ordered by relevance (score) to the search keywords.
Regardless of the data source type, the most relevant documents appear at the top.

Summary
=======

In this article, we integrated multiple data sources into Fess and built a cross-search environment.

- Crawl configurations for three types of sources: websites, file servers, and local files
- Category classification and filtered search using labels
- Distributed crawl schedule design
- URL transformation via path mapping

By introducing cross-search, users can find the information they need without having to think about where it is stored.

In the next article, we will cover designing role-based search to control search results according to departmental permissions.

References
==========

- `Fess Administrator Guide <https://fess.codelibs.org/ja/15.5/admin/index.html>`__

- `Fess File Crawl Configuration <https://fess.codelibs.org/ja/15.5/admin/filecrawl.html>`__
