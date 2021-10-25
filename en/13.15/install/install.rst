============
Installation
============

Requirements
============

|Fess| can be available in the following environment:

-  OS: Windows/Unix with Java environment
-  Java: Java 11
-  (RPM or DEB) Elasticsearch: 7.15.X

If Java is not installed in your environment where Fess will be used, install JDK from `Adoptium site <https://adoptium.net/>`__ .
Embedded Elasticsearch is not recommended for production use or load testing.


Download
========

Download a pakcage for Fess and Elasticsearch from `Download site <https://fess.codelibs.org/ja/downloads.html>`__.

Installation
============

Install Elasticsearch
---------------------

Install Elasticsearch by referring to `Elasticsearch Reference <https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html>`__.

Using ZIP Package
-----------------

After installing Elasticsearch, install Elasticsearch plugins to plugins directory.
In this guide, Elasticsearch is installed to $ES_HOME.

::

    $ $ES_HOME/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-fess:7.15.0
    $ $ES_HOME/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-extension:7.15.0
    $ $ES_HOME/bin/elasticsearch-plugin install org.codelibs:elasticsearch-minhash:7.15.0

Notice that these plugins depend on a version of Elasticsearch.

Next, install elasticsearch-configsync,

::

    $ curl -o /tmp/configsync.zip https://repo.maven.apache.org/maven2/org/codelibs/elasticsearch-configsync/7.15.0/elasticsearch-configsync-7.15.0.zip
    $ mkdir -p $ES_HOME/modules/configsync
    $ unzip -d $ES_HOME/modules/configsync /tmp/configsync.zip

and add the following setting to $ES_HOME/config/elasticsearch.yml.
For configsync.config_path, the value is an absolute path of $ES_HOME/data/config.

::

    configsync.config_path: [absolute path of $ES_HOME]/data/config/

Unzip |Fess| file to $FESS_HOME, and specify the following settings in $FESS_HOME/bin/fess.in.sh.

::

    ES_HTTP_URL=http://localhost:9200
    FESS_DICTIONARY_PATH=[absolute path of $ES_HOME]/data/config/


Using Zip Package on Windows
----------------------------

Download and unzipped |Fess| and Elasticsearch to c:\\elasticsearch-<version> and c:\\fess-<version> respectively.

Open a command propt and install Elasticsearch plugins to plugins directory.

::

    > c:\elasticsearch-<version>\bin\elasticsearch-plugin install org.codelibs:elasticsearch-analysis-fess:7.15.0
    > c:\elasticsearch-<version>\bin\elasticsearch-plugin install org.codelibs:elasticsearch-analysis-extension:7.15.0
    > c:\elasticsearch-<version>\bin\elasticsearch-plugin install org.codelibs:elasticsearch-minhash:7.15.0

Notice that these plugins depend on a version of Elasticsearch.

Next, to install elasticsearch-configsync, create c:\\elasticsearch-<version>\\modules\\configsync folder and then download and unzip `elasticsearch-configsync-7.15.0.zip <https://repo.maven.apache.org/maven2/org/codelibs/elasticsearch-configsync/7.15.0/elasticsearch-configsync-7.15.0.zip>`__.

Moreover, add the following setting to c:\\elasticsearch-<version>\\config\\elasticsearch.yml.

::

    configsync.config_path: c:/elasticsearch-<version>/data/config/

To connect |Fess| to Elasticsearch, specify the following settings in c:\\fess-<version>\\bin\\fess.in.bat.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.es.http_address=http://localhost:9200
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.dictionary.path="c:/elasticsearch-<version>/data/config/"


Using RPM/DEB Package
---------------------

First, install RPM/DEB package of Elasticsearch before installing |Fess| package.

For RPM package:

::

    $ sudo rpm -ivh elasticsearch-<version>.rpm

For DEB package:

::

    $ sudo dpkg -i elasticsearch-<version>.deb

Install Elasticsearch plugins to plugins directory.

::

    $ sudo /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-fess:7.15.0
    $ sudo /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-extension:7.15.0
    $ sudo /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-minhash:7.15.0

Notice that these plugins depend on a version of Elasticsearch.

Next, install elasticsearch-configsync,

::

    $ curl -o /tmp/configsync.zip https://repo.maven.apache.org/maven2/org/codelibs/elasticsearch-configsync/7.15.0/elasticsearch-configsync-7.15.0.zip
    $ sudo mkdir -p /usr/share/elasticsearch/modules/configsync
    $ sudo unzip -d /usr/share/elasticsearch/modules/configsync /tmp/configsync.zip

and add the following setting to /etc/elasticsearch/elasticsearch.yml.

::

    configsync.config_path: /var/lib/elasticsearch/config

After installing Elasticsearch, install RPM/DEB package of |Fess|.

For RPM package:

::

    $ sudo rpm -ivh fess-<version>.rpm

For DEB package:

::

    $ sudo dpkg -i fess-<version>.deb

To add |Fess| and Elasticsearch as a service, run the following command.

If you use systemctl command,

::

    $ sudo /bin/systemctl daemon-reload
    $ sudo /bin/systemctl enable elasticsearch.service
    $ sudo /bin/systemctl enable fess.service

and if you use chkconfig command,

::

    $ sudo /sbin/chkconfig --add elasticsearch
    $ sudo /sbin/chkconfig --add fess
