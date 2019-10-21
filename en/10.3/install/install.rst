============
Installation
============

Requirements
============

|Fess| can be available in these environments.

-  OS: Windows/Unix with Java environment
-  Java: Java 8 update 20 or later
-  (RPM or DEB) Elasticsearch: 2.4.x

If Java is not installed in your environment, see we want to |Fess| from `Oracle site <http://www.oracle.com/technetwork/java/javase/downloads/index.html>`__ to install JDK.

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
    script.engine.groovy.inline.update: on

Next, install |Fess| RPM package.

::

    $ sudo rpm -ivh fess-<version>.rpm

|Fess| provides elasticsearch plugins to extend elasticsearch's features for |Fess|.
Install the following plugins to plugins directory in elasticsearch.

::

    $ /usr/share/elasticsearch/bin/plugin install org.codelibs/elasticsearch-analysis-fess/2.4.0
    $ /usr/share/elasticsearch/bin/plugin install org.codelibs/elasticsearch-analysis-ja/2.4.0
    $ /usr/share/elasticsearch/bin/plugin install org.codelibs/elasticsearch-analysis-synonym/2.4.0
    $ /usr/share/elasticsearch/bin/plugin install org.codelibs/elasticsearch-configsync/2.4.2
    $ /usr/share/elasticsearch/bin/plugin install org.codelibs/elasticsearch-dataformat/2.4.0
    $ /usr/share/elasticsearch/bin/plugin install org.codelibs/elasticsearch-langfield/2.4.1
    $ /usr/share/elasticsearch/bin/plugin install http://maven.codelibs.org/archive/elasticsearch/plugin/kopf/elasticsearch-kopf-2.0.1.0.zip

For Japanese support, install analysis-kuromoji-neologd plugin.

::

    $ /usr/share/elasticsearch/bin/plugin install org.codelibs/elasticsearch-analysis-kuromoji-neologd/2.4.1

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


Using Your Elasticsearch Cluster On ZIP package
-----------------------------------------------

|Fess| is able to connect to your existing elasticsearch cluster.
For the details to configure elasticsearch for Fess, please see steps in Using RPM package.

To connect to elasticsearch cluster from |Fess|, use JVM options in a launch script file.
For Windows environment, the following settings are put into fess-<version>\\bin\\fess.in.bat.
fess.dictionary.path needs to be set to a path of configsync.config_path in elasticsearch.yml.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.es.http_address=http://localhost:9200
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.es.transport_addresses=localhost:9300
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.dictionary.path="c:/<elasticsearch-<version>/data/"

For Elasticsearch RPM/DEB package, they are in fess-<version>/bin/fess.in.sh.

::

    ES_HTTP_URL=http://localhost:9200
    ES_TRANSPORT_URL=localhost:9300
    FESS_DICTIONARY_PATH=/var/lib/elasticsearch/config/

