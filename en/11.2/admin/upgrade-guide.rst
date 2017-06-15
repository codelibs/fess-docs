=======
Upgrade
=======

Overview
====

Upgrade page provides data migration tools for previous versions of |Fess|.

|image0|

Operations
========

Backup
------

Download configuration backup files(.fess_basic_config and .fess_user) on Backup page before executing a migration process.

Migration
---------

Type /admin/upgrade/ to URL after logging in as admin user.
Select a target version and then click button to execute data mingration process.

Target Version
::::::::::::::

|Fess| version from which you want to upgrade.

Reindex
-------

Create new fess.YYMMDD index and copy documents from old fess index.

Update Aliases
::::::::::::::

Switch fess.search and fess.update aliases after reindexing if enabled.

.. |image0| image:: ../../../resources/images/en/11.2/admin/upgrade-1.png

