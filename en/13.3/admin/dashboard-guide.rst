=========
Dashboard
=========

Overview
========

Dashboard provides a web administration tool for elasticsearch to manage cluster and indices.

|image0|

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table:: |Fess| manages the following indices
   :header-rows: 1

   * - Name
     - Description
   * - fess.YYYYMMDD
     - indexed documents
   * - fess_log
     - search logs
   * - fess.suggest
     - suggest words
   * - .fess_config
     - configurations
   * - .fess_user
     - user/role/group data
   * - .configsync
     - configuration file data
   * - .suggest
     - suggest meta data
   * - .suggest-array
     - suggest meta data
   * - .suggest-badword
     - excluding word list for suggest
   * - .crawler
     - crawling cache data


Check The Number Of Indexed Documents
=====================================

The number of indexed documents is displayed in fess.YYYYMMDD index as the following figure.

|image1|


.. |image0| image:: ../../../resources/images/en/13.3/admin/dashboard-1.png
.. |image1| image:: ../../../resources/images/en/13.3/admin/dashboard-2.png
.. pdf            :width: 400 px
