=====================================
Linux Installation (Detailed Procedure)
=====================================

This page describes the installation procedure for |Fess| on Linux environments.
It covers TAR.GZ, RPM, and DEB package formats.

.. warning::

   Running with the embedded OpenSearch is not recommended for production environments.
   Always set up an external OpenSearch server.

Prerequisites
=============

- System requirements described in :doc:`prerequisites` are met
- Java 21 is installed
- OpenSearch 3.3.2 is available (or new installation)

Choosing an Installation Method
================================

For Linux environments, you can choose from the following installation methods:

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Method
     - Recommended Environments
     - Features
   * - TAR.GZ
     - Development environments, environments requiring customization
     - Can be extracted to any directory
   * - RPM
     - RHEL, CentOS, Fedora systems
     - Service management via systemd possible
   * - DEB
     - Debian, Ubuntu systems
     - Service management via systemd possible

Installation with TAR.GZ Version
=================================

Step 1: Install OpenSearch
---------------------------

1. Download OpenSearch

   Download the TAR.GZ version from `Download OpenSearch <https://opensearch.org/downloads.html>`__.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.3.2/opensearch-3.3.2-linux-x64.tar.gz
       $ tar -xzf opensearch-3.3.2-linux-x64.tar.gz
       $ cd opensearch-3.3.2

   .. note::

      This example uses OpenSearch 3.3.2.
      Verify the version supported by |Fess|.

2. Install OpenSearch Plugins

   Install the plugins required by |Fess|.

   ::

       $ cd /path/to/opensearch-3.3.2
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.2
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.2
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.2
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.2

   .. important::

      Plugin versions must match the OpenSearch version.
      In the example above, all are specified as 3.3.2.

3. Configure OpenSearch

   Add the following settings to ``config/opensearch.yml``.

   ::

       # Configuration synchronization path (specify absolute path)
       configsync.config_path: /path/to/opensearch-3.3.2/data/config/

       # Disable security plugin (development environment only)
       plugins.security.disabled: true

   .. warning::

      **Important Security Notice**

      Use ``plugins.security.disabled: true`` only in development or test environments.
      In production environments, enable the OpenSearch security plugin and configure appropriate authentication and authorization.
      For details, refer to :doc:`security`.

   .. tip::

      Adjust other settings such as cluster name and network settings according to your environment.
      Configuration example::

          cluster.name: fess-cluster
          node.name: fess-node-1
          network.host: 0.0.0.0
          discovery.type: single-node

Step 2: Install Fess
---------------------

1. Download and Extract Fess

   Download the TAR.GZ version from the `download site <https://fess.codelibs.org/en/downloads.html>`__.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.3.2/fess-15.3.2.tar.gz
       $ tar -xzf fess-15.3.2.tar.gz
       $ cd fess-15.3.2

2. Configure Fess

   Edit ``bin/fess.in.sh`` to set the connection information to OpenSearch.

   ::

       $ vi bin/fess.in.sh

   Add or modify the following settings::

       # OpenSearch HTTP endpoint
       SEARCH_ENGINE_HTTP_URL=http://localhost:9200

       # Dictionary file location path (same as OpenSearch's configsync.config_path)
       FESS_DICTIONARY_PATH=/path/to/opensearch-3.3.2/data/config/

   .. note::

      If OpenSearch is running on a different host, change ``SEARCH_ENGINE_HTTP_URL`` to the appropriate hostname or IP address.
      Example: ``SEARCH_ENGINE_HTTP_URL=http://192.168.1.100:9200``

3. Verify Installation

   Verify that the configuration files have been edited correctly::

       $ grep "SEARCH_ENGINE_HTTP_URL" bin/fess.in.sh
       $ grep "FESS_DICTIONARY_PATH" bin/fess.in.sh

Step 3: Startup
---------------

For startup procedures, refer to :doc:`run`.

Installation with RPM Version
==============================

The RPM version is used on RPM-based Linux distributions such as Red Hat Enterprise Linux, CentOS, and Fedora.

Step 1: Install OpenSearch
---------------------------

1. Download and Install OpenSearch RPM

   Download the RPM package from `Download OpenSearch <https://opensearch.org/downloads.html>`__ and install it.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.3.2/opensearch-3.3.2-linux-x64.rpm
       $ sudo rpm -ivh opensearch-3.3.2-linux-x64.rpm

   Or you can add a repository and install from it.
   For details, refer to `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/rpm/>`__.

2. Install OpenSearch Plugins

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.2

3. Configure OpenSearch

   Add the following settings to ``/etc/opensearch/opensearch.yml``.

   ::

       $ sudo vi /etc/opensearch/opensearch.yml

   Settings to add::

       configsync.config_path: /var/lib/opensearch/data/config/
       plugins.security.disabled: true

   .. warning::

      Do not use ``plugins.security.disabled: true`` in production environments.
      Refer to :doc:`security` for appropriate security configuration.

Step 2: Install Fess
---------------------

1. Install Fess RPM

   Download the RPM package from the `download site <https://fess.codelibs.org/en/downloads.html>`__ and install it.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.3.2/fess-15.3.2.rpm
       $ sudo rpm -ivh fess-15.3.2.rpm

2. Configure Fess

   Edit ``/usr/share/fess/bin/fess.in.sh``.

   ::

       $ sudo vi /usr/share/fess/bin/fess.in.sh

   Add or modify the following settings::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

3. Register Service

   **Using chkconfig**::

       $ sudo /sbin/chkconfig --add opensearch
       $ sudo /sbin/chkconfig --add fess

   **Using systemd** (recommended)::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

Step 3: Startup
---------------

For startup procedures, refer to :doc:`run`.

Installation with DEB Version
==============================

The DEB version is used on DEB-based Linux distributions such as Debian and Ubuntu.

Step 1: Install OpenSearch
---------------------------

1. Download and Install OpenSearch DEB

   Download the DEB package from `Download OpenSearch <https://opensearch.org/downloads.html>`__ and install it.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.3.2/opensearch-3.3.2-linux-x64.deb
       $ sudo dpkg -i opensearch-3.3.2-linux-x64.deb

   Or you can add a repository and install from it.
   For details, refer to `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/debian/>`__.

2. Install OpenSearch Plugins

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.2

3. Configure OpenSearch

   Add the following settings to ``/etc/opensearch/opensearch.yml``.

   ::

       $ sudo vi /etc/opensearch/opensearch.yml

   Settings to add::

       configsync.config_path: /var/lib/opensearch/data/config/
       plugins.security.disabled: true

   .. warning::

      Do not use ``plugins.security.disabled: true`` in production environments.
      Refer to :doc:`security` for appropriate security configuration.

Step 2: Install Fess
---------------------

1. Install Fess DEB

   Download the DEB package from the `download site <https://fess.codelibs.org/en/downloads.html>`__ and install it.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.3.2/fess-15.3.2.deb
       $ sudo dpkg -i fess-15.3.2.deb

2. Configure Fess

   Edit ``/usr/share/fess/bin/fess.in.sh``.

   ::

       $ sudo vi /usr/share/fess/bin/fess.in.sh

   Add or modify the following settings::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

3. Register Service

   Enable the service using systemd::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

Step 3: Startup
---------------

For startup procedures, refer to :doc:`run`.

Post-Installation Verification
===============================

After installation is complete, verify the following:

1. **Verify Configuration Files**

   - OpenSearch configuration file (opensearch.yml)
   - Fess configuration file (fess.in.sh)

2. **Directory Permissions**

   Verify that the directories specified in the configuration exist and have appropriate permissions.

   For TAR.GZ version::

       $ ls -ld /path/to/opensearch-3.3.2/data/config/

   For RPM/DEB version::

       $ sudo ls -ld /var/lib/opensearch/data/config/

3. **Verify Java Version**

   ::

       $ java -version

   Verify that Java 21 or later is installed.

Next Steps
==========

After installation is complete, refer to the following documentation:

- :doc:`run` - Starting |Fess| and initial setup
- :doc:`security` - Security configuration for production environments
- :doc:`troubleshooting` - Troubleshooting

Frequently Asked Questions
===========================

Q: Will other versions of OpenSearch work?
-------------------------------------------

A: |Fess| depends on a specific version of OpenSearch.
It is strongly recommended to use the recommended version (3.3.2) to ensure plugin compatibility.
If you use a different version, you must also adjust the plugin versions appropriately.

Q: Can multiple Fess instances share the same OpenSearch?
----------------------------------------------------------

A: Possible, but not recommended. We recommend providing a dedicated OpenSearch cluster for each Fess instance.
If you share OpenSearch among multiple Fess instances, be careful of index name conflicts.

Q: How do I configure OpenSearch as a cluster?
-----------------------------------------------

A: Refer to the OpenSearch official documentation `Cluster formation <https://opensearch.org/docs/latest/tuning-your-cluster/cluster/>`__.
For cluster configuration, remove the ``discovery.type: single-node`` setting and add appropriate cluster settings.
