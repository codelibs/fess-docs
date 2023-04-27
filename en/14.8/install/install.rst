============
Installation
============

Requirements
============

Fess can be used in the following environments:

- OS: Operating system that can run Java or Docker (such as Windows or Linux)
- `Java 17 <https://adoptium.net/>`__ (for installing the TAR.GZ/ZIP/RPM/DEB version)
- `Docker <https://docs.docker.com/get-docker/>`__ (for installing the Docker version)

Using Fess in a production environment or for load testing is not recommended with the embedded OpenSearch.

For the TAR.GZ/ZIP/RPM/DEB version, you must install the correct version of Elasticsearch/OpenSearch.

Download
========

Download Fess from the `Download Site <https://fess.codelibs.org/ja/downloads.html>`__.

Installing the TAR.GZ version (OpenSearch)
==========================================

Installing OpenSearch
---------------------

Refer to `Download & Get Started <https://opensearch.org/downloads.html>`__ and download the TAR.GZ version of OpenSearch.

The OpenSearch plugins need to match the version of OpenSearch.
The following explains the installation for OpenSearch 2.6.0.

Install the OpenSearch plugins in the plugins directory.
Assume that OpenSearch is installed in $OPENSEARCH_HOME.

::

    $ $OPENSEARCH_HOME/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:2.6.0
    $ $OPENSEARCH_HOME/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:2.6.0
    $ $OPENSEARCH_HOME/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:2.6.0
    $ $OPENSEARCH_HOME/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:2.6.0

Note that these plugins depend on the version of OpenSearch.

Add the following settings to $OPENSEARCH_HOME/config/opensearch.yml.
If there are existing settings, overwrite them.

Specify the absolute path of $OPENSEARCH_HOME/data/config in configsync.config_path.

::

    configsync.config_path: [absolute path of $OPENSEARCH_HOME]/data/config/
    plugins.security.disabled: true

Installing Fess
---------------

Extract the Fess zip file to $FESS_HOME.
To connect Fess to the OpenSearch cluster, specify the following startup options.
Modify $FESS_HOME/bin/fess.in.sh.

::

    SEARCH_ENGINE_HTTP_URL=http://localhost:9200
    FESS_DICTIONARY_PATH=[absolute path of $SEARCH_ENGINE_HOME]/data/config/

Installation with Docker (OpenSearch)
=====================================

For the installation, refer the following files from `https://github.com/codelibs/docker-fess/compose <https://github.com/codelibs/docker-fess/tree/v14.8.0/compose>`__:

- `compose.yaml <https://raw.githubusercontent.com/codelibs/docker-fess/v14.8.0/compose/compose.yaml>`__
- `compose-opensearch2.yaml <https://raw.githubusercontent.com/codelibs/docker-fess/v14.8.0/compose/compose-opensearch2.yaml>`__

Installation with TAR.GZ (Elasticsearch)
========================================

Installing Elasticsearch
------------------------

Refer to `Installing Elasticsearch <https://www.elastic.co/guide/en/elasticsearch/reference/8.6/install-elasticsearch.html>`__ to download and install the TAR.GZ version of Elasticsearch.

Elasticsearch plugins must match the Elasticsearch version.
We will explain how to install them with Elasticsearch version 8.6.0.

Install Elasticsearch plugins in the plugins directory. Assuming Elasticsearch is installed in $SEARCH_ENGINE_HOME:

::

    $ $SEARCH_ENGINE_HOME/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-fess:8.6.0.0
    $ $SEARCH_ENGINE_HOME/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-extension:8.6.0.0
    $ $SEARCH_ENGINE_HOME/bin/elasticsearch-plugin install org.codelibs:elasticsearch-minhash:8.6.0.0

Note that these plugins depend on the Elasticsearch version.

Next, install elasticsearch-configsync.

::

    $ curl -o /tmp/configsync.zip https://repo.maven.apache.org/maven2/org/codelibs/elasticsearch-configsync/8.6.0.0/elasticsearch-configsync-8.6.0.0.zip
    $ mkdir -p $SEARCH_ENGINE_HOME/modules/configsync
    $ unzip -d $SEARCH_ENGINE_HOME/modules/configsync /tmp/configsync.zip

Add the following settings to $SEARCH_ENGINE_HOME/config/elasticsearch.yml. If there are existing settings, overwrite them.

Specify the absolute path of $SEARCH_ENGINE_HOME/data/config to configsync.config_path.

::

    configsync.config_path: [$SEARCH_ENGINE_HOME absolute path]/data/config/
    xpack.security.enabled: false

Installing Fess
---------------

Extract the Fess zip file to $FESS_HOME.
To connect Fess to the Elasticsearch cluster, specify the following startup options in $FESS_HOME/bin/fess.in.sh.

::

    SEARCH_ENGINE_HTTP_URL=http://localhost:9200
    FESS_DICTIONARY_PATH=[$SEARCH_ENGINE_HOME absolute path]/data/config/

Installation with ZIP (Elasticsearch)
=====================================

Installing Elasticsearch
------------------------

Refer to `Installing Elasticsearch <https://www.elastic.co/guide/en/elasticsearch/reference/8.6/install-elasticsearch.html>`__ and download/install the ZIP version of Elasticsearch. Do not configure or start Elasticsearch since we will configure it in the following steps.

The Elasticsearch plugin must match the Elasticsearch version. Here, we describe the installation for Elasticsearch 8.6.0.

Extract elasticsearch-<version>.zip and fess-<version>.zip to any location. Let's assume that they are extracted to c:\elasticsearch-<version> and c:\fess-<version>, respectively.

Install the Elasticsearch plugin from the command prompt:

::

    > c:\elasticsearch-<version>\bin\elasticsearch-plugin install org.codelibs:elasticsearch-analysis-fess:8.6.0.0
    > c:\elasticsearch-<version>\bin\elasticsearch-plugin install org.codelibs:elasticsearch-analysis-extension:8.6.0.0
    > c:\elasticsearch-<version>\bin\elasticsearch-plugin install org.codelibs:elasticsearch-minhash:8.6.0.0

Note that these plugins depend on the Elasticsearch version.

Next, install elasticsearch-configsync.
Create the c:\elasticsearch-<version>\modules\configsync folder and download and extract `elasticsearch-configsync-8.6.0.0.zip <https://repo.maven.apache.org/maven2/org/codelibs/elasticsearch-configsync/8.6.0.0/elasticsearch-configsync-8.6.0.0.zip>`__.

Add the following settings to c:\elasticsearch-<version>\config\elasticsearch.yml. If there are existing settings, overwrite them.

::

    configsync.config_path: c:/elasticsearch-<version>/data/config/
    xpack.security.enabled: false

Installing Fess
---------------

Extract the Fess zip file to %FESS_HOME%. To connect Fess to the Elasticsearch cluster, specify the following startup options in c:\fess-<version>\bin\fess.in.bat.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.search_engine.http_address=http://localhost:9200
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.dictionary.path="c:/elasticsearch-<version>/data/config/"

Installation with RPM/DEB (Elasticsearch)
=========================================

Installing Elasticsearch
------------------------

Refer to `Installing Elasticsearch <https://www.elastic.co/guide/en/elasticsearch/reference/8.6/install-elasticsearch.html>`__ to download and install the RPM/DEB version of Elasticsearch.
As configuration for Elasticsearch will be performed later, please do not configure or start Elasticsearch at this time.

Note that Elasticsearch plugins must match the version of Elasticsearch you have installed. Here we describe installation for Elasticsearch 8.6.0.

Install the Elasticsearch plugins in the plugins directory:

::

    $ sudo /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-fess:8.6.0.0
    $ sudo /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-analysis-extension:8.6.0.0
    $ sudo /usr/share/elasticsearch/bin/elasticsearch-plugin install org.codelibs:elasticsearch-minhash:8.6.0.0

Note that these plugins depend on the Elasticsearch version.

Next, install elasticsearch-configsync:

::

    $ curl -o /tmp/configsync.zip https://repo.maven.apache.org/maven2/org/codelibs/elasticsearch-configsync/8.6.0.0/elasticsearch-configsync-8.6.0.0.zip
    $ sudo mkdir -p /usr/share/elasticsearch/modules/configsync
    $ sudo unzip -d /usr/share/elasticsearch/modules/configsync /tmp/configsync.zip

Add the following settings to /etc/elasticsearch/elasticsearch.yml (common for RPM/DEB).
If you have existing settings, rewrite them.

::

    configsync.config_path: /var/lib/elasticsearch/config
    xpack.security.enabled: false

Installing Fess
---------------

Next, install the Fess RPM/DEB package.

For RPM packages:

::

    $ sudo rpm -ivh fess-<version>.rpm

For DEB packages:

::

    $ sudo dpkg -i fess-<version>.deb

To register as a service, enter the following command. If using chkconfig (RPM):

::

    $ sudo /sbin/chkconfig --add elasticsearch
    $ sudo /sbin/chkconfig --add fess

If using systemd (RPM/DEB):

::

    $ sudo /bin/systemctl daemon-reload
    $ sudo /bin/systemctl enable elasticsearch.service
    $ sudo /bin/systemctl enable fess.service


Installation with Docker (Elasticsearch)
========================================

For the installation, refer the following files from `https://github.com/codelibs/docker-fess/compose <https://github.com/codelibs/docker-fess/tree/v14.8.0/compose>`__:

- `compose.yaml <https://raw.githubusercontent.com/codelibs/docker-fess/v14.8.0/compose/compose.yaml>`__
- `compose-elasticsearch8.yaml <https://raw.githubusercontent.com/codelibs/docker-fess/v14.8.0/compose/compose-elasticsearch8.yaml>`__
- `.env.elasticsearch <https://raw.githubusercontent.com/codelibs/docker-fess/v14.8.0/compose/.env.elasticsearch>`__


