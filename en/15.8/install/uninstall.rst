========================
Uninstallation Procedure
========================

This page describes the procedures for completely uninstalling |Fess|.

.. warning::

   **Important Notes Before Uninstallation**

   - Uninstalling will delete all data
   - If you have important data, be sure to create a backup first
   - For backup procedures, refer to :doc:`upgrade`

Preparation Before Uninstallation
=================================

Create Backup
-------------

Back up the necessary data:

1. **Configuration Data**

   Download it from "System" → "Backup" in the admin screen.
   This operation lets you export various settings (including crawl settings), search logs, and more all at once.

2. **Customized Configuration Files**

   TAR.GZ/ZIP version::

       $ cp -r /path/to/fess/app/WEB-INF/conf /backup/
       $ cp -r /path/to/fess/app/WEB-INF/classes /backup/

   RPM/DEB version::

       $ sudo cp -r /etc/fess /backup/

.. note::

   Most of |Fess|'s indexes and settings are stored in OpenSearch.
   To back up index data, use OpenSearch's snapshot feature.
   For detailed procedures, refer to :doc:`upgrade`.

Stop Services
-------------

Before uninstallation, stop all services.

TAR.GZ/ZIP version::

    $ ps aux | grep -E 'fess|opensearch'
    $ kill <fess_pid>
    $ kill <opensearch_pid>

RPM/DEB version::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Docker version::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

Uninstalling the TAR.GZ/ZIP Version
===================================

Step 1: Remove Fess
-------------------

Delete the installation directory::

    $ rm -rf /path/to/fess-15.8.0

Step 2: Remove OpenSearch
-------------------------

Delete the OpenSearch installation directory::

    $ rm -rf /path/to/opensearch-3.7.0

Step 3: Delete the Data Directory (Optional)
--------------------------------------------

|Fess|'s index data is stored in OpenSearch.
By default it is stored inside the OpenSearch installation directory (such as ``opensearch-3.7.0/data``),
but if you have specified a different location with ``path.data``, delete that directory as well::

    $ rm -rf /path/to/data

Step 4: Delete the Log Directory (Optional)
-------------------------------------------

Delete the log files::

    $ rm -rf /path/to/fess-15.8.0/logs
    $ rm -rf /path/to/opensearch-3.7.0/logs

Uninstalling the RPM Version
============================

Step 1: Uninstall Fess
----------------------

Uninstall the RPM package::

    $ sudo rpm -e fess

.. note::

   When the |Fess| package is uninstalled, the package's removal script automatically
   stops and disables the ``fess`` service and removes the ``fess`` user and group.
   The following steps are performed to confirm that these have been reliably removed, or
   to manually delete data and configuration files.

Step 2: Uninstall OpenSearch
----------------------------

::

    $ sudo rpm -e opensearch

Step 3: Confirm the Service Is Disabled
---------------------------------------

The service is usually disabled when the package is removed, but to confirm or disable it just in case, run the following.

For systemd::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

For older SysV init (chkconfig) environments::

    $ sudo /sbin/chkconfig --del fess
    $ sudo /sbin/chkconfig --del opensearch

Step 4: Delete the Data Directory
---------------------------------

.. warning::

   Performing this operation completely deletes all index data.

The data directory is not removed when the package is uninstalled, so delete it manually::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

Step 5: Delete the Configuration Files
--------------------------------------

Delete the configuration files and environment settings files::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/sysconfig/fess
    $ sudo rm -rf /etc/opensearch

.. note::

   With RPM, configuration files in ``/etc/fess`` may remain with a name like ``.rpmsave``.
   To delete them completely, remove them manually as shown above.

Step 6: Delete the Log Files
----------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

Step 7: Delete the Temporary Directory (Optional)
-------------------------------------------------

::

    $ sudo rm -rf /var/tmp/fess

Step 8: Delete the User and Group (Optional)
--------------------------------------------

The ``fess`` user and group are usually removed when the package is deleted.
If they remain, or to remove the user and group for OpenSearch, run the following::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

Uninstalling the DEB Version
============================

Step 1: Uninstall Fess
----------------------

Uninstall the DEB package::

    $ sudo dpkg -r fess

To completely remove it including configuration files and environment settings files, use purge::

    $ sudo dpkg -P fess

.. note::

   With ``dpkg -r`` (remove), configuration files (conffiles) such as ``/etc/default/fess`` remain.
   Using ``dpkg -P`` (purge) also deletes these configuration files and the ``fess`` user and group.

Step 2: Uninstall OpenSearch
----------------------------

::

    $ sudo dpkg -r opensearch

Or remove it including configuration files::

    $ sudo dpkg -P opensearch

Step 3: Confirm the Service Is Disabled
---------------------------------------

The service is usually disabled when the package is removed. To confirm or disable it just in case, run the following::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

Step 4: Delete the Data Directory
---------------------------------

.. warning::

   Performing this operation completely deletes all index data.

::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

Step 5: Delete the Configuration Files (if dpkg -P was not used)
----------------------------------------------------------------

::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/default/fess
    $ sudo rm -rf /etc/opensearch

Step 6: Delete the Log Files
----------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

Step 7: Delete the User and Group (Optional)
--------------------------------------------

If you did not use ``dpkg -P``, the ``fess`` user and group remain.
To remove them, run the following::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

Uninstalling the Docker Version
===============================

Step 1: Remove Containers and Networks
--------------------------------------

Remove the containers and the network created by Docker Compose (``search_net``)::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

Step 2: Remove Volumes
----------------------

.. warning::

   Performing this operation completely deletes all data.

|Fess|'s data (such as indexes and dictionaries) is stored in OpenSearch volumes.
First, check the list of volumes::

    $ docker volume ls

Remove the OpenSearch-related volumes::

    $ docker volume rm <project>_search01_data
    $ docker volume rm <project>_search01_dictionary

.. note::

   Volume names are prefixed with the Docker Compose project name (usually the name of the
   directory where the Compose files are located). Check the actual names with ``docker volume ls``.

To remove the containers and volumes all at once, add the ``-v`` option to ``down``::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

Step 3: Remove Images (Optional)
--------------------------------

To remove the Docker images and free up disk space::

    $ docker images | grep fess
    $ docker rmi ghcr.io/codelibs/fess:15.8.0
    $ docker rmi ghcr.io/codelibs/fess-opensearch:3.7.0

Step 4: Remove Compose Files
----------------------------

::

    $ rm compose.yaml compose-opensearch3.yaml

Verifying the Uninstallation
============================

Verify that all components have been removed.

Verify Processes
----------------

::

    $ ps aux | grep fess
    $ ps aux | grep opensearch

If nothing is displayed, the processes are stopped.

Verify Ports
------------

::

    $ sudo netstat -tuln | grep 8080
    $ sudo netstat -tuln | grep 9200

Verify that the ports are not in use.

Verify Files
------------

TAR.GZ/ZIP version::

    $ ls /path/to/fess-15.8.0  # Verify that the directory does not exist

RPM/DEB version::

    $ ls /var/lib/fess  # Verify that the directory does not exist
    $ ls /etc/fess      # Verify that the directory does not exist

Docker version::

    $ docker ps -a | grep -E 'fess01|search01'  # Verify that the containers do not exist
    $ docker volume ls | grep search01           # Verify that the volumes do not exist

Verify Packages
---------------

RPM version::

    $ rpm -qa | grep fess
    $ rpm -qa | grep opensearch

DEB version::

    $ dpkg -l | grep fess
    $ dpkg -l | grep opensearch

If nothing is displayed, the packages have been removed.

Partial Uninstallation
======================

Remove Only Fess, Keeping OpenSearch
------------------------------------

If OpenSearch is also used by other applications, you can remove only Fess.

1. Stop Fess
2. Remove the Fess package or directory
3. Remove the Fess data directory (such as ``/var/lib/fess``)
4. Delete the |Fess| indexes created in OpenSearch (such as ``fess.*`` and ``.fess_*``)
5. Do not remove OpenSearch

Remove Only OpenSearch, Keeping Fess
------------------------------------

.. warning::

   Removing OpenSearch will cause Fess to stop functioning.
   Change the configuration to connect to a different OpenSearch cluster.

1. Stop OpenSearch
2. Remove the OpenSearch package or directory
3. Remove the OpenSearch data directory (such as ``/var/lib/opensearch``)
4. Update the Fess configuration to specify a different OpenSearch cluster

Troubleshooting
===============

Cannot Remove the Package
-------------------------

**Symptoms:**

An error occurs with ``rpm -e`` or ``dpkg -r``.

**Solution:**

1. Verify that the service is stopped::

       $ sudo systemctl stop fess.service

2. Check dependencies::

       $ rpm -qa | grep fess
       $ dpkg -l | grep fess

3. Force removal (last resort)::

       $ sudo rpm -e --nodeps fess
       $ sudo dpkg -r --force-all fess

Cannot Delete the Directory
---------------------------

**Symptoms:**

Cannot delete a directory with ``rm -rf``.

**Solution:**

1. Check permissions::

       $ ls -ld /path/to/directory

2. Delete with sudo::

       $ sudo rm -rf /path/to/directory

3. Verify that no process is using the files::

       $ sudo lsof | grep /path/to/directory

Preparing for Reinstallation
============================

When reinstalling after uninstallation, verify the following:

1. All processes are stopped
2. All files and directories are deleted
3. Ports 8080 and 9200 are not in use
4. No previous configuration files remain

For reinstallation procedures, refer to :doc:`install`.

Next Steps
==========

Once uninstallation is complete:

- To install a new version, refer to :doc:`install`
- To migrate data, refer to :doc:`upgrade`
- To consider an alternative search solution, refer to the official Fess website
