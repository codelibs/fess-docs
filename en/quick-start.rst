==============
Quick Start Guide
==============

Introduction
============

This guide is for those who want to quickly try out Fess.
It describes the minimum steps required to use Fess.

The startup procedure described here is for trial purposes, so for production deployment, please refer to :doc:`Installation Guide <setup>` using Docker or similar methods.
(Fess started with this procedure is intended for simple testing and is not recommended for production use.)

Prerequisites
=============

Before starting Fess, please install Java 21.
We recommend `Eclipse Temurin <https://adoptium.net/temurin>`__ for Java 21.

Download
========

Download the latest Fess ZIP package from the `GitHub releases page <https://github.com/codelibs/fess/releases>`__.

Installation
============

Extract the downloaded fess-x.y.z.zip file.

::

    $ unzip fess-x.y.z.zip
    $ cd fess-x.y.z

Starting Fess
=============

Run the fess script to start Fess.
(On Windows, run fess.bat)

::

    $ ./bin/fess

Accessing the Admin UI
======================

Access \http://localhost:8080/admin.
The default administrator account username/password is admin/admin.

.. warning::

   Be sure to change the default password.
   In production environments, it is strongly recommended to change the password immediately after the first login.

Creating a Crawl Configuration
==============================

After logging in, click "Crawler" > "Web" in the left menu.
Click the "New" button to create a web crawl configuration.

Enter the following information:

- **Name**: Name of the crawl configuration (e.g., Company Website)
- **URL**: URL to crawl (e.g., https://www.example.com/)
- **Max Access Count**: Maximum number of pages to crawl
- **Interval**: Crawl interval (milliseconds)

Running the Crawler
===================

Click "System" > "Scheduler" in the left menu.
Click the "Start Now" button for the "Default Crawler" job to start crawling immediately.

To schedule crawling, select "Default Crawler" and configure the schedule.
For a start time of 10:35 am, enter 35 10 \* \* ? (format is "minute hour day month weekday year").
After updating, crawling will start at that time.

You can check if crawling has started in "Crawling Info".
After crawling completes, WebIndexSize information will be displayed in the session information.

Search
======

After crawling completes, access \http://localhost:8080/ to search and view search results.

Stopping Fess
=============

Stop the fess process with Ctrl-C or the kill command.

To Learn More
=============

Please refer to the following documentation:

* `Documentation <documentation>`__
* `[Article Series] Easy Introduction to OSS Full-Text Search Server Fess <https://news.mynavi.jp/techplus/series/_ossfess/>`__
* `Developer Information <development>`__
* `Discussion Forum <https://discuss.codelibs.org/c/fessen/>`__
