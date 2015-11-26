===================
Quick Startup
===================

Overview
========

This document describes a minimum step to install and use |Fess| .

Download
========

Download the latest |Fess| release from https://github.com/codelibs/fess/releases.

Installation
============

Unzip fess-x.y.zip to a directory you want to install. 

::

    $ unzip fess-x.y.zip
    $ cd fess-x.y

Start |Fess| Server
=================

Run fess script file to start |Fess| server.

::

    $ ./bin/fess      # for Unix

    > .\bin\fess.bat  # for Windows

Access to Administrative GUI
============================

Access to http://localhost:8080/fess/admin. The username/password for an
administrator is admin/admin.

Click "Web" link at the left menu pane after logging in as admin user.
Create a web crawling configuration (Name, URL, Max access count,..) 
to crawl a web site.

Click "Scheduler" link at the menu pane. Click "Default Crawler" for
Crawler job and then click "Start" to start Crawler.

If you want to change Crawler schedule and start crawling at 10:35am, 
type "0 35 10 \* \* ?" into Schedule field. The format is 
"Sec Min Hour Day Month Day Year", which is like a cron
format. Click "Update" button to save parameters. If you
set a crawling time as 10:35am, |Fess| start to crawl at 10:35am
automatically.

"Crawling Info" show you the crawling information. If the crawl is
finished, the number of crawled documents is set to WebIndexSize 
at Crawling Info page.

Search
======

Finished a crawling, access to http://localhost:8080/fess/. You can
search indexed documents and see the result.

