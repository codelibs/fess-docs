=======================
Development Information
=======================

Overview
========

This page describes development steps for |Fess|.

Requirements
============

|Fess| runs on Java 11 or more. To develop |Fess|, The following knowledge is required:

-  Java 11

-  `LastaFlute <https://github.com/lastaflute>`__

-  `DBFlute <https://github.com/dbflute>`__

-  `Elasticsearch <https://www.elastic.co/>`__

How To Develop |Fess|
=====================

1. Install Java 11, IDE(ex. eclipse), and Maven 3.x

2. Clone the source code of |Fess| from github:

   ::

       $ git clone https://github.com/codelibs/fess.git

4. Download elasticsearch plugins

   ::

       $ mvn antrun:run

4. If using eclipse, Import it as Maven project into the eclipse

5. Build |Fess|

   ::

       $ mvn package

6. Launch org.codelibs.fess.FessBoot as Debug mode and then access to http://localhost:8080/

Create |Fess| Package
=====================

Run package goal to create a release file, fess-x.y.zip.
You need to execute antrun:run goal before package goal.

::

    $ mvn antrun:run
    $ mvn package
