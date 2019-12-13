=======
Maintenance
=======

Overview
====

Maintenance page provides system tools for managing |Fess|.

|image0|

To display this page, select System Info > Maintenance in a left menu.


Operations
========

Reindex
-------

Create new fess.YYMMDD index and copy documents from old fess index.

Update Aliases
::::::::::::::

Switch fess.search and fess.update aliases after reindexing if enabled.

Reset Dictionaries
::::::::::::::::::

Select Enabled if using factory default dictionaries.

The number of shards
::::::::::::::::::::

Specify the number of shards(index.number_of_shards).

Auto expand replicas
::::::::::::::::::::

Specify auto-expand the number of replicas(index.auto_expand_replicas).

Reload Doc Index
----------------

Reload(Close/Open) fess index to apply index settings.

Crawler Indices
---------------

Remove .crawler index to clear crawling data.
Do not execute this task when Crawler is running.

Diagnostic
----------

Download log files and system state information.

.. |image0| image:: ../../../resources/images/en/13.5/admin/maintenance-1.png

