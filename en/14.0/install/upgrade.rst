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

Stop |Fess| and then install RPM/DEB package. For the instruction, see Installation in Installation Guide.

To upgrade to Elasticsearch 8, remove old indices and then upgrade Elasticsearch package.
For Elasticsearch plugins, if you upgrade Elasticsearch, re-install all Elasticsearch plugins for the correct Elasticsearch version.

Restore Configuration
---------------------

Check and merge settings in fess_config.properties, and then start |Fess|.

Upload fess_basic_config.bulk and fess_user.bulk on Backup page to restore data.

Start Crawler
-------------

To create new search indices, start Default Crawler job on Scheduler page.


