============
File Crawling
============

Overview
========

The File Crawling configuration page allows you to configure settings for crawling files in the file system or shared network folders.

Configuration Management
========================

Display Method
--------------

To open the File Crawling configuration list page, click [Crawler > File System] in the left menu.

|image0|

Click the configuration name to edit it.

Creating a Configuration
------------------------

Click the "Create New" button to open the File Crawling configuration page.

|image1|

Configuration Options
---------------------

Name
::::

Configuration name.

Path
::::

This path specifies where to start crawling (e.g., file:/ or smb://).

Included Paths for Crawling
::::::::::::::::::::::::::::

Paths matching this regular expression (Java format) will be crawled by the |Fess| crawler.

Excluded Paths for Crawling
::::::::::::::::::::::::::::

Paths matching this regular expression (Java format) will not be crawled by the |Fess| crawler.

Included Paths for Indexing
::::::::::::::::::::::::::::

Paths matching this regular expression (Java format) will be included in the search index.

Excluded Paths for Indexing
::::::::::::::::::::::::::::

Paths matching this regular expression (Java format) will be excluded from the search index.

Configuration Parameters
::::::::::::::::::::::::

Specifies crawl configuration information.

Depth
:::::

Specifies the depth of the file system structure to crawl.

Max Access Count
::::::::::::::::

The number of paths to index.

Number of Threads
:::::::::::::::::

The number of threads to use for this configuration.

Interval
::::::::

The time interval to wait when threads crawl each path.

Boost Value
:::::::::::

The boost value is the priority of documents indexed by this configuration.

Permissions
:::::::::::

Specifies permissions for this configuration.
The permission format is as follows: to display search results to users in the developer group, specify {group}developer.
User-level: {user}username, Role-level: {role}rolename, Group-level: {group}groupname.

Virtual Host
::::::::::::

Specifies the virtual host hostname.
For details, see :doc:`Virtual Hosts in the Configuration Guide <../config/virtual-host>`.

Status
::::::

If enabled, the default crawler's scheduled job will include this configuration.

Description
:::::::::::

Enter a description.

Deleting a Configuration
------------------------

Click the configuration name on the list page, then click the "Delete" button to display a confirmation screen. Click the "Delete" button to remove the configuration.

Examples
========

Crawling Local Files
--------------------

To crawl files under /home/share, the configuration values are as follows:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Configuration Item
     - Value
   * - Name
     - Share Directory
   * - Path
     - file:/home/share

Other parameters can use default settings.

Crawling Windows Shared Folders
--------------------------------

To crawl files under \\SERVER\SharedFolder, the configuration values are as follows:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Configuration Item
     - Value
   * - Name
     - Shared Folder
   * - Path
     - smb://SERVER/SharedFolder/

If a username and password are required to access the shared folder, you need to create file authentication settings by clicking [Crawler > File Authentication] in the left menu. The configuration values are as follows:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Configuration Item
     - Value
   * - Hostname
     - SERVER
   * - Scheme
     - SAMBA
   * - Username
     - (Please enter)
   * - Password
     - (Please enter)




.. |image0| image:: ../../../resources/images/en/15.3/admin/fileconfig-1.png
.. |image1| image:: ../../../resources/images/en/15.3/admin/fileconfig-2.png
.. pdf            :height: 940 px
