=====================
Uninstallation Procedure
=====================

This page describes the procedures for complete uninstallation of |Fess|.

.. warning::

   **Important Notes Before Uninstallation**

   - Uninstalling will delete all data
   - If you have important data, create a backup first
   - For backup procedures, refer to :doc:`upgrade`

Pre-Uninstallation Preparation
===============================

Create Backup
-------------

Back up necessary data:

1. **Configuration Data Backup**

   Download from the admin screen at "System" → "Backup".

   Download the following files:

   - ``fess_basic_config.bulk``
   - ``fess_user.bulk``

2. **Configuration File Backup**

   TAR.GZ/ZIP version::

       $ cp /path/to/fess/app/WEB-INF/conf/system.properties /backup/
       $ cp /path/to/fess/app/WEB-INF/classes/fess_config.properties /backup/

   RPM/DEB version::

       $ sudo cp /etc/fess/system.properties /backup/
       $ sudo cp /etc/fess/fess_config.properties /backup/

3. **Customized Configuration Files**

   If you have customized configuration files, back up those as well::

       $ cp /path/to/fess/app/WEB-INF/classes/log4j2.xml /backup/

Stop Services
-------------

Before uninstallation, stop all services.

TAR.GZ/ZIP version::

    $ ps aux | grep fess
    $ kill <fess_pid>
    $ kill <opensearch_pid>

RPM/DEB version::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Docker version::

    $ docker compose -f compose.yaml -f compose-opensearch2.yaml down

Uninstall TAR.GZ/ZIP Version
=============================

Step 1: Remove Fess
-------------------

Delete the installation directory::

    $ rm -rf /path/to/fess-15.3.0

Step 2: Remove OpenSearch
--------------------------

Delete the OpenSearch installation directory::

    $ rm -rf /path/to/opensearch-3.3.0

Step 3: Delete Data Directory (Optional)
-----------------------------------------

By default, the data directory is within the Fess installation directory, but if you specified a different location, delete that directory as well::

    $ rm -rf /path/to/data

Step 4: Delete Log Directory (Optional)
----------------------------------------

Delete log files::

    $ rm -rf /path/to/fess/logs
    $ rm -rf /path/to/opensearch/logs

Uninstall RPM Version
=====================

Step 1: Uninstall Fess
----------------------

Uninstall the RPM package::

    $ sudo rpm -e fess

Step 2: Uninstall OpenSearch
-----------------------------

::

    $ sudo rpm -e opensearch

Step 3: Disable and Remove Service
-----------------------------------

For chkconfig::

    $ sudo /sbin/chkconfig --del fess
    $ sudo /sbin/chkconfig --del opensearch

For systemd::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

Step 4: Delete Data Directory
------------------------------

.. warning::

   This operation will completely delete all index data and configuration.

::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

Step 5: Delete Configuration Files
-----------------------------------

::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/opensearch

Step 6: Delete Log Files
-------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

Step 7: Delete Users and Groups (Optional)
-------------------------------------------

To delete system users and groups::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

Uninstall DEB Version
======================

Step 1: Uninstall Fess
----------------------

Uninstall the DEB package::

    $ sudo dpkg -r fess

To completely remove including configuration files::

    $ sudo dpkg -P fess

Step 2: Uninstall OpenSearch
-----------------------------

::

    $ sudo dpkg -r opensearch

Or to remove including configuration files::

    $ sudo dpkg -P opensearch

Step 3: Disable Service
-----------------------

::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

Step 4: Delete Data Directory
------------------------------

.. warning::

   This operation will completely delete all index data and configuration.

::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

Step 5: Delete Configuration Files (if dpkg -P was not used)
-------------------------------------------------------------

::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/opensearch

Step 6: Delete Log Files
-------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

Step 7: Delete Users and Groups (Optional)
-------------------------------------------

To delete system users and groups::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

Uninstall Docker Version
=========================

Step 1: Remove Containers and Networks
---------------------------------------

::

    $ docker compose -f compose.yaml -f compose-opensearch2.yaml down

Step 2: Remove Volumes
-----------------------

.. warning::

   This operation will completely delete all data.

Verify volume list::

    $ docker volume ls

Remove Fess-related volumes::

    $ docker volume rm fess-es-data
    $ docker volume rm fess-data

Or remove all volumes at once::

    $ docker compose -f compose.yaml -f compose-opensearch2.yaml down -v

Step 3: Remove Images (Optional)
---------------------------------

To remove Docker images to free up disk space::

    $ docker images | grep fess
    $ docker rmi codelibs/fess:15.3.0

    $ docker images | grep opensearch
    $ docker rmi opensearchproject/opensearch:3.3.0

Step 4: Remove Networks (Optional)
-----------------------------------

Remove networks created by Docker Compose::

    $ docker network ls
    $ docker network rm <network_name>

Step 5: Remove Compose Files
-----------------------------

::

    $ rm compose.yaml compose-opensearch2.yaml

Verify Uninstallation
======================

Verify that all components have been removed.

Verify Processes
----------------

::

    $ ps aux | grep fess
    $ ps aux | grep opensearch

If nothing is displayed, processes are stopped.

Verify Ports
------------

::

    $ sudo netstat -tuln | grep 8080
    $ sudo netstat -tuln | grep 9200

Verify ports are not in use.

Verify Files
------------

TAR.GZ/ZIP version::

    $ ls /path/to/fess-15.3.0  # Verify directory does not exist

RPM/DEB version::

    $ ls /var/lib/fess  # Verify directory does not exist
    $ ls /etc/fess      # Verify directory does not exist

Docker version::

    $ docker ps -a | grep fess  # Verify containers do not exist
    $ docker volume ls | grep fess  # Verify volumes do not exist

Verify Packages
---------------

RPM version::

    $ rpm -qa | grep fess
    $ rpm -qa | grep opensearch

DEB version::

    $ dpkg -l | grep fess
    $ dpkg -l | grep opensearch

If nothing is displayed, packages have been removed.

Partial Uninstallation
=======================

Remove Only Fess, Keep OpenSearch
----------------------------------

If OpenSearch is also used by other applications, you can remove only Fess.

1. Stop Fess
2. Remove Fess package or directory
3. Remove Fess data directory (e.g., ``/var/lib/fess``)
4. Do not remove OpenSearch

Remove Only OpenSearch, Keep Fess
----------------------------------

.. warning::

   Removing OpenSearch will cause Fess to stop functioning.
   Change configuration to connect to a different OpenSearch cluster.

1. Stop OpenSearch
2. Remove OpenSearch package or directory
3. Remove OpenSearch data directory (e.g., ``/var/lib/opensearch``)
4. Update Fess configuration to specify a different OpenSearch cluster

Troubleshooting
===============

Cannot Remove Package
---------------------

**Symptoms:**

Error occurs with ``rpm -e`` or ``dpkg -r``.

**Solution:**

1. Verify service is stopped::

       $ sudo systemctl stop fess.service

2. Check dependencies::

       $ rpm -qa | grep fess
       $ dpkg -l | grep fess

3. Force removal (last resort)::

       $ sudo rpm -e --nodeps fess
       $ sudo dpkg -r --force-all fess

Cannot Delete Directory
------------------------

**Symptoms:**

Cannot delete directory with ``rm -rf``.

**Solution:**

1. Verify permissions::

       $ ls -ld /path/to/directory

2. Delete with sudo::

       $ sudo rm -rf /path/to/directory

3. Verify no processes are using files::

       $ sudo lsof | grep /path/to/directory

Preparing for Reinstallation
=============================

Before reinstalling after uninstallation, verify the following:

1. All processes are stopped
2. All files and directories are deleted
3. Ports 8080 and 9200 are not in use
4. No previous configuration files remain

For reinstallation procedures, refer to :doc:`install`.

Next Steps
==========

After uninstallation is complete:

- To install a new version, refer to :doc:`install`
- To migrate data, refer to :doc:`upgrade`
- For alternative search solutions, refer to the official Fess website
