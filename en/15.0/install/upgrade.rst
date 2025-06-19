=======
Upgrade
=======

Upgrade
=======

To upgrade from a previous version, see the following steps.

Backup Data
-----------

Configuration data are in the following files:

* fess_basic_config.bulk and fess_user.bulk from Backup page (For more details, see Backup of Administration Guide)
* system.properties in /etc/fess or app/WEB-INF/conf
* fess_config.properties in /etc/fess or app/WEB-INF/conf

Upgrade Package
---------------

Stop |Fess| process and install the RPM or DEB package. See Installation in the Installation Guide for more information.

When upgrading OpenSearch, you may encounter indexes that fail to migrate. For a safe migration, it is recommended to remove indexes related to |Fess| .


Restore the configuration
-------------------------

1. Install |Fess| .
2. Check for configuration differences in fess_config.properties and reflect the configuration in the new environment.
3. Copy system.properties to the new environment.
4. Start |Fess| .
5. Log in from the administration screen.
6. Upload the fess_basic_config.bulk and fess_user.bulk files from the backup page.

Start Crawler
-------------

Start the Default Crawler job on the Scheduler page to generate the index.
