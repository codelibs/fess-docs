=======================
Development Information
=======================

Overview
========

This page describes development steps for |Fess|.

Requirements
============

|Fess| runs on Java 17 or the above. To develop |Fess|, the following knowledge is required:

-  Java 17

-  `LastaFlute <https://github.com/lastaflute>`__

-  `DBFlute <https://github.com/dbflute>`__

-  `Elasticsearch <https://github.com/elastic/elasticsearch>`__ or `OpenSearch <https://github.com/opensearch-project/OpenSearch>`__

How To Develop |Fess|
=====================

1. Install Java 17, IDE(ex. eclipse), and Maven 3.x

2. Clone the source code of |Fess| from github:

   ::

       $ git clone https://github.com/codelibs/fess.git

4. Download OpenSearch plugins

   ::

       $ mvn antrun:run

4. Import it as Maven project into the eclipse

5. Build |Fess|

   ::

       $ mvn package

6. Launch org.codelibs.fess.FessBoot with Debug mode and then access to http://localhost:8080/

Create |Fess| Package
=====================

Run package goal to create a release file, fess-x.y.zip.
You need to execute antrun:run goal before package goal.

::

    $ mvn antrun:run
    $ mvn package
