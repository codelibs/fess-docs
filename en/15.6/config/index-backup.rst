================
Index Management
================

Index Backup and Restore
========================

The data to treat in |Fess| are managed as an index of OpenSearch.
About the backup method of the index, OpenSearch provides it as a snapshot function.
Please refer to a `Snapshot Feature <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/index/>`_ for the information such as procedures.

Some setting is stored in ``app/WEB-INF/conf/system.properties`` or ``/etc/fess/system.properties``.
When data shift, please copy these files as needed.