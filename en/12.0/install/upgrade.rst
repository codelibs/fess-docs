=======
Upgrade
=======

Upgrade
=======

To upgrade from a previous version, see the following steps.

Backup Data
-----------

Configuration data are in the following files:

* .fess_basic_config and .fess_user from Backup page(For more details, see Backup of Administration Guide)
* system.properties in /etc/fess or app/WEB-INF/conf
* fess_config.properties in /etc/fess or app/WEB-INF/conf

Upgrade Package
---------------

Stop |Fess| and then install RPM/DEB package, see Installation in Installation Guide.

|Fess| 12 requires Elasticsearch 6.x, and indices for |Fess| 12 is not compatible with |Fess| 11.x.
To upgrade to Elasticsearch 6, remove old indices and then upgrade Elasticsearch package.
For Elasticsearch plugins, if you upgrade Elasticsearch, re-install all Elasticsearch plugins for the proper Elasticsearch version.

Restore Configuration
---------------------

Check and merge settings in fess_config.properties, and then start |Fess|.

For |Fess| 11, to restore data, upload .fess_basic_config.12 and .fess_user.12 bulk files on Backup page.

For |Fess| 12, execute migration process on Upgrade page. For more details, see Upgrade of Administration Guide.

Start Crawler
-------------

To create new search indices, start Default Crawler job on Scheduler page.

