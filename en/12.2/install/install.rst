============
Installation
============

Requirements
============

|Fess| can be available in these environments.

-  OS: Windows/Unix with Java environment
-  Java: Java 8 update 131 or later
-  (RPM or DEB) Elasticsearch: 6.2.X

If Java is not installed in your environment, see we want to |Fess| from `Oracle site <http://www.oracle.com/technetwork/java/javase/downloads/index.html>`__ to install JDK.
Embedded Elasticsearch is not recommended for production use.

Download
========

Download the latest |Fess| package from the release site, `https://github.com/codelibs/fess/releases <https://github.com/codelibs/fess/releases>`__.

Installation
============

Using ZIP package
-----------------

Unzip the downloaded fess-<version>.zip.
For UNIX environment, run the following command:

::

    $ unzip fess-<version>.zip
    $ cd fess-<version>

Using RPM package
-----------------

You need to install elasticsearch RPM package before Fess installation.
Download elasticsearch RPM package from elasticsearch site `https://www.elastic.co/downloads/elasticsearch <https://www.elastic.co/downloads/elasticsearch>`__, and then install the package.

::

    $ sudo rpm -ivh elasticsearch-<version>.rpm

To access from Fess, the following configuration needs to be added to /etc/elasticsearch/elasticsearch.yml

::

    configsync.config_path: /var/lib/elasticsearch/config

Next, install |Fess| RPM package.

::

    $ sudo rpm -ivh fess-<version>.rpm

|Fess| provides elasticsearch plugins to extend elasticsearch's features for |Fess|.
Install the following plugins to plugins directory in elasticsearch.

::

    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-fess:6.2.1
    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-ja:6.2.1
    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-synonym:6.2.1
    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-configsync:6.2.3
    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-dataformat:6.2.3
    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-langfield:6.2.1
    $ /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-minhash:6.2.1

Note that these plugins depends on elasticsearch version.

To register them as a service, run the following commands if using chkconfig,

::

    $ sudo /sbin/chkconfig --add elasticsearch
    $ sudo /sbin/chkconfig --add fess

For systemd based system(e.g. CentOS 7),

::

    $ sudo /bin/systemctl daemon-reload
    $ sudo /bin/systemctl enable elasticsearch.service
    $ sudo /bin/systemctl enable fess.service

To change a cluster name for elasticsearch, modify the following value in fess_config.properties.

::

    elasticsearch.cluster.name=elasticsearch


Using Your Elasticsearch Cluster On ZIP package
-----------------------------------------------

|Fess| is able to connect to your existing elasticsearch cluster.
For the details to configure elasticsearch for Fess, please see steps in Using RPM package.

To connect to elasticsearch cluster from |Fess|, use JVM options in a launch script file.
For Windows environment, the following settings are put into fess-<version>\\bin\\fess.in.bat.
fess.dictionary.path needs to be set to a path of configsync.config_path in elasticsearch.yml.

::

    set FESS_PARAMS=%FESS_PARAMS% -Dfess.es.http_address=http://localhost:9200
    set FESS_PARAMS=%FESS_PARAMS% -Dfess.es.transport_addresses=localhost:9300
    set FESS_PARAMS=%FESS_PARAMS% -Dfess.dictionary.path="c:/<elasticsearch-<version>/config/"

For Elasticsearch RPM/DEB package, they are in fess-<version>/bin/fess.in.sh.

::

    ES_HTTP_URL=http://localhost:9200
    ES_TRANSPORT_URL=localhost:9300
    FESS_DICTIONARY_PATH=/var/lib/elasticsearch/config/

If you change a cluster name of Elasticsearch, modify the following setting in fess_config.properties.

::

    elasticsearch.cluster.name=elasticsearch

