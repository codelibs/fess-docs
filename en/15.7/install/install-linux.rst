========================================
Linux Installation (Detailed Procedure)
========================================

This page describes the installation procedure for |Fess| on Linux environments.
It covers the TAR.GZ, RPM, and DEB package formats.

.. warning::

   Running with the embedded OpenSearch is not recommended for production environments.
   Always set up an external OpenSearch server.

Prerequisites
=============

- The system requirements described in :doc:`prerequisites` are met
- Java 21 is installed
- OpenSearch 3.7.0 is available for use (or is newly installed)

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

System Configuration for Running OpenSearch
============================================

To run OpenSearch stably on Linux, configure the following kernel parameters and resource limits.
These are mainly required for the TAR.GZ version (when installing OpenSearch manually).
For the RPM / DEB versions, the OpenSearch and |Fess| packages configure settings such as the file descriptor limit via systemd, but since ``vm.max_map_count`` is a host-level kernel setting, be sure to check it regardless of which installation method you use.

Maximum Map Count for Virtual Memory
-------------------------------------

Because OpenSearch uses a large number of memory maps, set ``vm.max_map_count`` to ``262144`` or higher.

To set this temporarily::

    $ sudo sysctl -w vm.max_map_count=262144

To set this persistently::

    $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
    $ sudo sysctl -p

File Descriptor Limit
-----------------------

When running OpenSearch manually (TAR.GZ version), set the file descriptor limit for the user running OpenSearch to ``65535`` or higher.

Add the following to ``/etc/security/limits.conf`` (replace ``opensearch`` with the username that runs OpenSearch)::

    opensearch  -  nofile  65535

.. note::

   For the RPM / DEB versions, this setting is not necessary because the file descriptor limit is configured in the systemd service definition.

Installation with TAR.GZ Version
=================================

Step 1: Install OpenSearch
---------------------------

1. Download OpenSearch

   Download the TAR.GZ version from `Download OpenSearch <https://opensearch.org/downloads.html>`__.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.7.0/opensearch-3.7.0-linux-x64.tar.gz
       $ tar -xzf opensearch-3.7.0-linux-x64.tar.gz
       $ cd opensearch-3.7.0

   .. note::

      This example uses OpenSearch 3.7.0.
      |Fess| 15.7 supports OpenSearch 3.7.0.

2. Install OpenSearch Plugins

   Install the plugins required by |Fess|.

   ::

       $ cd /path/to/opensearch-3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.7.0

   .. important::

      Plugin versions must match the OpenSearch version.
      In the example above, all are specified as 3.7.0.

3. Configure OpenSearch

   Add the following settings to ``config/opensearch.yml``.

   ::

       # Path for configuration synchronization (specify an absolute path)
       configsync.config_path: /path/to/opensearch-3.7.0/data/config/

       # Disable the security plugin (development environments only)
       plugins.security.disabled: true

   .. warning::

      **Important Security Notice**

      Use ``plugins.security.disabled: true`` only in development or test environments.
      In production environments, enable the OpenSearch security plugin and configure appropriate authentication and authorization.
      When enabling the security plugin on OpenSearch 2.12 or later, you must set the administrator password (environment variable ``OPENSEARCH_INITIAL_ADMIN_PASSWORD``) at the first startup.
      For details, refer to :doc:`security`.

   .. tip::

      Adjust other settings, such as the cluster name and network settings, according to your environment.
      Example configuration::

          cluster.name: fess-cluster
          node.name: fess-node-1
          network.host: 0.0.0.0
          discovery.type: single-node

   .. tip::

      The OpenSearch heap size is configured with ``-Xms`` / ``-Xmx`` in ``config/jvm.options``.
      As a guideline, use no more than half of the available physical memory and less than 32GB, and it is recommended to specify the same value for ``-Xms`` and ``-Xmx``.

Step 2: Install Fess
---------------------

1. Download and Extract Fess

   Download the TAR.GZ version from the `download site <https://fess.codelibs.org/downloads.html>`__.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.7.0/fess-15.7.0.tar.gz
       $ tar -xzf fess-15.7.0.tar.gz
       $ cd fess-15.7.0

2. Configure Fess

   Edit ``bin/fess.in.sh`` to configure the connection information to OpenSearch.
   This file already contains, in a commented-out state, the settings for connecting to an external OpenSearch cluster.

   ::

       $ vi bin/fess.in.sh

   Uncomment (remove the leading ``#`` from) the following two lines near the top of the file.

   Before (default state)::

       # External opensearch cluster
       #SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       #FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

   After::

       # External opensearch cluster
       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/path/to/opensearch-3.7.0/data/config/

   .. note::

      - Set ``FESS_DICTIONARY_PATH`` to the same path specified for ``configsync.config_path`` in OpenSearch's ``opensearch.yml``.
      - If OpenSearch is running on a different host, change ``SEARCH_ENGINE_HTTP_URL`` to the appropriate hostname or IP address. Example: ``SEARCH_ENGINE_HTTP_URL=http://192.168.1.100:9200``
      - Rather than adding a new ``SEARCH_ENGINE_HTTP_URL=...`` line, uncomment and edit the existing commented-out line.

   .. tip::

      To change the |Fess| heap size, edit ``FESS_MIN_MEM`` (default: ``256m``) and ``FESS_MAX_MEM`` (default: ``2g``) in ``bin/fess.in.sh``, or set the environment variable ``FESS_HEAP_SIZE``.

3. Verify Installation

   Verify that the configuration file has been edited correctly::

       $ grep "SEARCH_ENGINE_HTTP_URL" bin/fess.in.sh
       $ grep "FESS_DICTIONARY_PATH" bin/fess.in.sh

Step 3: Startup
-----------------

For startup procedures, refer to :doc:`run`.

Installation with RPM Version
==============================

The RPM version is used on RPM-based Linux distributions such as Red Hat Enterprise Linux, CentOS, and Fedora.

Step 1: Install OpenSearch
---------------------------

1. Download and Install OpenSearch RPM

   Download the RPM package from `Download OpenSearch <https://opensearch.org/downloads.html>`__ and install it.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.7.0/opensearch-3.7.0-linux-x64.rpm
       $ sudo rpm -ivh opensearch-3.7.0-linux-x64.rpm

   Alternatively, you can add a repository and install from it.
   For details, refer to `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/rpm/>`__.

2. Install OpenSearch Plugins

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.7.0

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

   Download the RPM package from the `download site <https://fess.codelibs.org/downloads.html>`__ and install it.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.7.0/fess-15.7.0.rpm
       $ sudo rpm -ivh fess-15.7.0.rpm

2. Configure Fess

   For the RPM version, edit the environment variable configuration file ``/etc/sysconfig/fess``.
   This file is preserved across package upgrades (do not edit ``/usr/share/fess/bin/fess.in.sh`` directly, since it is overwritten during upgrades).

   ::

       $ sudo vi /etc/sysconfig/fess

   Configure the connection information to OpenSearch. The default values are as follows. Change them as needed::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

   .. note::

      Set ``FESS_DICTIONARY_PATH`` to the same path as ``configsync.config_path`` in ``opensearch.yml``.

3. Register and Enable the Service

   Enable the services using systemd (systemd is the standard on RHEL 8 and later, and CentOS 8 and later)::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

   .. note::

      Because the |Fess| service depends on the OpenSearch service, OpenSearch must be started first.

   .. note::

      On legacy environments that do not use systemd, you can register |Fess| with ``chkconfig``::

          $ sudo /sbin/chkconfig --add fess

Step 3: Startup
-----------------

For startup procedures, refer to :doc:`run`.

Installation with DEB Version
==============================

The DEB version is used on DEB-based Linux distributions such as Debian and Ubuntu.

Step 1: Install OpenSearch
---------------------------

1. Download and Install OpenSearch DEB

   Download the DEB package from `Download OpenSearch <https://opensearch.org/downloads.html>`__ and install it.

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.7.0/opensearch-3.7.0-linux-x64.deb
       $ sudo dpkg -i opensearch-3.7.0-linux-x64.deb

   Alternatively, you can add a repository and install from it.
   For details, refer to `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/debian/>`__.

2. Install OpenSearch Plugins

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.7.0

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

   Download the DEB package from the `download site <https://fess.codelibs.org/downloads.html>`__ and install it.

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.7.0/fess-15.7.0.deb
       $ sudo dpkg -i fess-15.7.0.deb

2. Configure Fess

   For the DEB version, edit the environment variable configuration file ``/etc/default/fess``.
   This file is preserved across package upgrades (do not edit ``/usr/share/fess/bin/fess.in.sh`` directly, since it is overwritten during upgrades).

   ::

       $ sudo vi /etc/default/fess

   Configure the connection information to OpenSearch. The default values are as follows. Change them as needed::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

   .. note::

      Set ``FESS_DICTIONARY_PATH`` to the same path as ``configsync.config_path`` in ``opensearch.yml``.

3. Register and Enable the Service

   Enable the services using systemd::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

   .. note::

      Because the |Fess| service depends on the OpenSearch service, OpenSearch must be started first.

Step 3: Startup
-----------------

For startup procedures, refer to :doc:`run`.

Post-Installation Verification
================================

After the installation is complete, verify the following:

1. **Verify Configuration Files**

   - OpenSearch configuration file (opensearch.yml)
   - |Fess| configuration file

     - TAR.GZ version: ``bin/fess.in.sh``
     - RPM version: ``/etc/sysconfig/fess``
     - DEB version: ``/etc/default/fess``

2. **Directory Permissions**

   Verify that the directories specified in the configuration (``configsync.config_path`` / ``FESS_DICTIONARY_PATH``) exist and have appropriate permissions set.

   For the TAR.GZ version::

       $ ls -ld /path/to/opensearch-3.7.0/data/config/

   For the RPM/DEB versions::

       $ sudo ls -ld /var/lib/opensearch/data/config/

3. **Verify Kernel Parameters**

   ::

       $ sysctl vm.max_map_count

   Verify that the value is ``262144`` or higher.

4. **Verify Java Version**

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
============================

Q: Will other versions of OpenSearch work?
---------------------------------------------

A: |Fess| depends on a specific version of OpenSearch.
To ensure plugin compatibility, it is strongly recommended to use the recommended version (3.7.0).
If you use a different version, you must also adjust the plugin versions appropriately.

Q: Can multiple Fess instances share the same OpenSearch?
-------------------------------------------------------------

A: It is possible, but not recommended. We recommend providing a dedicated OpenSearch cluster for each Fess instance.
If you share OpenSearch among multiple Fess instances, be careful of index name conflicts.

Q: How do I configure OpenSearch as a cluster?
---------------------------------------------------

A: Refer to the official OpenSearch documentation `Cluster formation <https://opensearch.org/docs/latest/tuning-your-cluster/cluster/>`__.
For a cluster configuration, you must remove the ``discovery.type: single-node`` setting and add appropriate cluster settings.
