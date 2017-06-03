=========
Dashboard
=========

Overview
========

Dashboard provides a web administration tool for elasticsearch to manage cluster and indices.

|image0|

|Fess| manages the following indices:

+------------------+----------------------------------+
| Name             | Description                      |
+==================+==================================+
| fess.YYYYMMDD    | indexed documents                |
+------------------+----------------------------------+
| fess_log         | search logs                      |
+------------------+----------------------------------+
| fess.suggest     | suggest words                    |
+------------------+----------------------------------+
| .fess_config     | configurations                   |
+------------------+----------------------------------+
| .fess_user       | user/role/group data             |
+------------------+----------------------------------+
| .configsync      | configuration file data          |
+------------------+----------------------------------+
| .suggest         | suggest meta data                |
+------------------+----------------------------------+
| .suggest-array   | suggest meta data                |
+------------------+----------------------------------+
| .suggest-badword | excluding word list for suggest  |
+------------------+----------------------------------+

Check The Number Of Indexed Documents
=====================================

The number of indexed documents is displayed in fess index as the following figure.

|image1|


.. |image0| image:: ../../../resources/images/en/11.2/admin/dashboard-1.png
.. |image1| image:: ../../../resources/images/en/11.2/admin/dashboard-2.png
