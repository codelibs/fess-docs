=======
Upgrade
=======

Upgrade
=======

To upgrade Fess from a previous version, see the following steps.

Backup Data
-----------

Configuration data are in the following files:

* .fess_basic_config and .fess_user from Backup page(For more details, see Backup of Administration Guide)
* system.properties in /etc/fess or app/WEB-INF/conf
* fess_config.properties in /etc/fess or app/WEB-INF/conf

Upgrade Package
---------------

Stop Fess and then install RPM/DEB package, see Installation of Installation Guide.

Restore Configuration
---------------------

Check and merge settings in fess_config.properties, and then start Fess.
To upgrade configuration data, execute migration process on Upgrade page.
For more details, see Upgrade of Administration Guide.

