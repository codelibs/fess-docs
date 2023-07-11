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

For the TAR.GZ/ZIP/RPM/DEB version, you must install the correct version of OpenSearch.

Download
========

Download Fess from the `Download Site <https://fess.codelibs.org/downloads.html>`__.

Installing the TAR.GZ version
=============================

Installing OpenSearch
---------------------

Refer to `Download & Get Started <https://opensearch.org/downloads.html>`__ and download the TAR.GZ version of OpenSearch.

The OpenSearch plugins need to match the version of OpenSearch.
The following explains the installation for OpenSearch 2.8.0.

Install the OpenSearch plugins in the plugins directory.
Assume that OpenSearch is installed in $OPENSEARCH_HOME.

::

    $ $OPENSEARCH_HOME/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:2.8.0
    $ $OPENSEARCH_HOME/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:2.8.0
    $ $OPENSEARCH_HOME/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:2.8.0
    $ $OPENSEARCH_HOME/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:2.8.0

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


Installation with ZIP Version
==============================

Installing OpenSearch
-----------------------

For Windows environments, use the ZIP version for installation.

Refer to `Download & Get Started <https://opensearch.org/downloads.html>`__ and download the ZIP version of OpenSearch.

OpenSearch plugins must be compatible with the version of OpenSearch being installed. Here's an explanation for installing OpenSearch version 2.8.0.

Install the OpenSearch plugins in the plugins directory. Let's assume OpenSearch is installed at $OPENSEARCH_HOME.

::

    $ $OPENSEARCH_HOME\bin\opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:2.8.0
    $ $OPENSEARCH_HOME\bin\opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:2.8.0
    $ $OPENSEARCH_HOME\bin\opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:2.8.0
    $ $OPENSEARCH_HOME\bin\opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:2.8.0

Please note that these plugins are version-dependent, so ensure compatibility with your OpenSearch version.

Add the following settings to $OPENSEARCH_HOME\config\opensearch.yml. If there are existing settings, modify them accordingly.

Specify the absolute path of $OPENSEARCH_HOME\data\config for configsync.config_path.

::

    configsync.config_path: [$absolute path of $OPENSEARCH_HOME]/data/config/
    plugins.security.disabled: true

Installing Fess
-----------------

Extract the ZIP file of |Fess| to $FESS_HOME.
To connect |Fess| to the OpenSearch cluster, specify the following startup options in $FESS_HOME\bin\fess.in.bat.

::

    SEARCH_ENGINE_HTTP_URL=http://localhost:9200
    FESS_DICTIONARY_PATH=[$absolute path of $SEARCH_ENGINE_HOME]/data/config/


Installation with RPM/DEB package
=================================

Installing OpenSearch
----------------------

Please download the RPM/DEB version of OpenSearch from `Download & Get Started <https://opensearch.org/downloads.html>`__ and install it by following the instructions on `Installing OpenSearch <https://opensearch.org/docs/2.7/install-and-configure/install-opensearch/index/>`__.

Do not perform any OpenSearch configuration or startup as we will perform the OpenSearch configuration in the following steps.

Please note that the OpenSearch plugins should match the version of OpenSearch that you installed. The following describes the installation process for OpenSearch 2.8.0.

Install the OpenSearch plugins in the plugins directory:

::

    $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:2.8.0
    $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:2.8.0
    $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:2.8.0
    $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:2.8.0

Please note that these plugins depend on the version of OpenSearch.

Add the following settings to /etc/opensearch/opensearch.yml (common for RPM/DEB). If there are existing settings, please overwrite them:

::

    configsync.config_path: /var/lib/opensearch/data/config/
    plugins.security.disabled: true

Installing Fess
---------------

Next, install the RPM/DEB package of |Fess|.

For RPM package:

::

    $ sudo rpm -ivh fess-<version>.rpm

For DEB package:

::

    $ sudo dpkg -i fess-<version>.deb

To register as a service, enter the following commands. For RPM with chkconfig:

::

    $ sudo /sbin/chkconfig --add OpenSearch
    $ sudo /sbin/chkconfig --add fess

For RPM/DEB with systemd:

::

    $ sudo /bin/systemctl daemon-reload
    $ sudo /bin/systemctl enable opensearch.service
    $ sudo /bin/systemctl enable fess.service

To connect |Fess| to the OpenSearch cluster, specify the following startup options in /usr/share/fess/bin/fess.in.sh:

::

    SEARCH_ENGINE_HTTP_URL=http://localhost:9200
    FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

Installation with Docker
=====================================

For the installation, refer the following files from `https://github.com/codelibs/docker-fess/compose <https://github.com/codelibs/docker-fess/tree/v14.9.0/compose>`__:

- `compose.yaml <https://raw.githubusercontent.com/codelibs/docker-fess/v14.9.0/compose/compose.yaml>`__
- `compose-opensearch2.yaml <https://raw.githubusercontent.com/codelibs/docker-fess/v14.9.0/compose/compose-opensearch2.yaml>`__

