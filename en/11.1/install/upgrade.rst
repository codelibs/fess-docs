=======
Upgrade
=======

Upgrade From |Fess| 10
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

|Fess| 11 requires Elasticsearch 5.1 or the above, and indices for |Fess| 11 is not compatible with |Fess| 10.x.
To upgrade to Elasticsearch 5, remove old indices and then upgrade Elasticsearch package.
For Elasticsearch plugins, if you upgrade Elasticsearch, re-install all Elasticsearch plugins for the proper Elasticsearch version.

Restore Configuration
---------------------

Check and merge settings in fess_config.properties, and then start |Fess|.
To restore data, upload .fess_basic_config and .fess_user bulk files on Backup page.

Start Crawler
-------------

To create new search indices, start Default Crawler job on Scheduler page.

