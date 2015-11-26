===============================================================
Open source full-text search server - |Fess| development overview
===============================================================

Overview
========

This page describes steps to develop the |Fess|.

Requirements
============

|Fess| runs on Java 8 or more. To develop |Fess|, The following knowledge
is required:

-  Java

-  LastaFlute

-  DBFlute

-  Elasticsearch

How To Develop |Fess|
=====================

1. Install Java 8, Eclipse, and Maven 3.x

2. Clone the source code of the |Fess| from github:

   ::

       $ git clone https://github.com/codelibs/fess.git

4. Download Elasticsearch Plugins

   ::

       $ mvn antrun:run

4. Import it as Maven project into the Eclipse

5. Launch org.codelibs.fess.FessBoot as Debug

Create |Fess| Package
=====================

Run package goal to create a release file, fess-x.y.zip.
You need to execute antrun:run goal before package goal.

::

    $ mvn antrun:run
    $ mvn package

Reference material
==================

-  `LastaFlute <https://github.com/lastaflute>`__

-  `DBFlute <https://github.com/dbflute>`__

-  `Elasticsearch <https://www.elastic.co/>`__
