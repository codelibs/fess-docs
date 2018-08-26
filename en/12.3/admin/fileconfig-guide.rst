==================
File Configuration
==================

Overview
========

File Crawling Configuaration page manages configurations for File crawling on file system or shared network folder.

Management Operations
=====================

Display Configurations
----------------------

Select Crawler > File System in the left menu to display a list page of File Crawling Configuration, as below.

|image0|

Click a configuration name if you want to edit it.

Create Configuration
--------------------

Click Create New button to display a form page for File crawling configuration.

|image1|

Configurations
--------------

Name
::::

Configuration name.

Paths
:::::

This paths are locations to start crawling(ex. file:// or smb://).

Included Paths For Crawling
:::::::::::::::::::::::::::

This regular expression(Java Format) is allowed path patterns for |Fess| crawler.

Excluded Paths For Crawling
:::::::::::::::::::::::::::

This regular expression(Java Format) is rejected path patterns for |Fess| crawler.

Included Paths For Indexing
:::::::::::::::::::::::::::

This regular expression(Java Format) is allowed path patterns for |Fess| indexer.

Excluded Paths For Indexing
:::::::::::::::::::::::::::

This regular expression(Java Format) is rejected path patterns for |Fess| indexer.

Depth
:::::

The depth of the file system structure.

Max Access Count
::::::::::::::::

The number of indexed paths.

The number of Thread
::::::::::::::::::::

The number of crawler threads for this configuration.

Interval time
:::::::::::::

Interval time to crawl paths for each thread.

Boost
:::::

Boost value is a weight for indexed documents of this configuration.

Permissions
:::::::::::

Permissions for this configuration.
This format is "{user/group/role}name".
For example, to display search results on users who belong to developer group, the permission is {group}developer.

Virtual Hosts
:::::::::::::

Virtual Host keys for this configuration.
e.g. fess (if setting Host:fess.codelibs.org=fess in General)

Labels
::::::

Labels for this configuration.

Status
::::::

If enabled, the scheduled job of Default Crawler includes this configuration.

Description
:::::::::::

Comments for this configuration.

Delete Configuration
--------------------

Click a configuration on a list page, and click Delete button to display a confirmation dialog.
Click Delete button to delete the configuration.

Example
=======

Crawling Local File System
--------------------------

If you want to create File crawling configuration to crawl files under /home/share, parameters for config are:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Name
     - Value
   * - Name
     - Share Directory
   * - Paths
     - file:/home/share

For other parameters, use a default value.

Crawling Windows Shared Folder
------------------------------

For crawling files in \\SERVER\SharedFolder, File crawling configuration is:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Name
     - Value
   * - Name
     - Share Folder
   * - Paths
     - smb://SERVER/SharedFolder/

If SharedFolder needs username/password to access it, create File Authentication configuration on Crawler > File Auth of the left menu. The configuration is:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Name
     - Value
   * - Hostname
     - SERVER
   * - Protocol
     - SAMBA
   * - Username
     - (Type your setting)
   * - Password
     - (Type your setting)



.. |image0| image:: ../../../resources/images/en/12.3/admin/fileconfig-1.png
.. |image1| image:: ../../../resources/images/en/12.3/admin/fileconfig-2.png
