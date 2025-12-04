===================================
Docker Installation (Detailed Guide)
===================================

This page describes the installation procedure for |Fess| using Docker and Docker Compose.
Using Docker allows you to set up a |Fess| environment easily and quickly.

Prerequisites
=============

- System requirements described in :doc:`prerequisites` are met
- Docker 20.10 or later is installed
- Docker Compose 2.0 or later is installed

Verify Docker Installation
===========================

Verify the Docker and Docker Compose versions with the following commands.

::

    $ docker --version
    $ docker compose version

.. note::

   If you are using an older version of Docker Compose, use the ``docker-compose`` command.
   This document uses the new ``docker compose`` command format.

About Docker Images
===================

The |Fess| Docker image consists of the following components:

- **Fess**: Full-text search system
- **OpenSearch**: Search engine

Official Docker images are published on `Docker Hub <https://hub.docker.com/r/codelibs/fess>`__.

Step 1: Obtain Docker Compose Files
====================================

The following files are required to start using Docker Compose.

Method 1: Download Files Individually
--------------------------------------

Download the following files:

::

    $ mkdir fess-docker
    $ cd fess-docker
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.4.0/compose/compose.yaml
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.4.0/compose/compose-opensearch3.yaml

Method 2: Clone Repository with Git
------------------------------------

If Git is installed, you can also clone the entire repository:

::

    $ git clone --depth 1 --branch v15.4.0 https://github.com/codelibs/docker-fess.git
    $ cd docker-fess/compose

Step 2: Review Docker Compose Files
====================================

Contents of ``compose.yaml``
-----------------------------

``compose.yaml`` contains the basic Fess configuration.

Main configuration items:

- **Port number**: Fess web interface port (default: 8080)
- **Environment variables**: Settings such as Java heap size
- **Volumes**: Data persistence settings

Contents of ``compose-opensearch3.yaml``
-----------------------------------------

``compose-opensearch3.yaml`` contains the OpenSearch configuration.

Main configuration items:

- **OpenSearch version**: OpenSearch version to use
- **Memory settings**: JVM heap size
- **Volumes**: Index data persistence settings

Customize Configuration (Optional)
-----------------------------------

To change the default settings, edit ``compose.yaml``.

Example: Change port number::

    services:
      fess:
        ports:
          - "9080:8080"  # Map to port 9080 on host

Example: Change memory settings::

    services:
      fess:
        environment:
          - "FESS_HEAP_SIZE=2g"  # Set Fess heap size to 2GB

Step 3: Start Docker Containers
================================

Basic Startup
-------------

Start Fess and OpenSearch with the following command:

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   - The ``-f`` option specifies multiple Compose files
   - The ``-d`` option runs in the background

View startup logs::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f

Press ``Ctrl+C`` to exit the log view.

Verify Startup
--------------

Check the container status::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

Verify that the following containers are running:

- ``fess``
- ``opensearch``

.. tip::

   Startup may take several minutes.
   Wait until you see "Fess is ready" or a similar message in the logs.

Step 4: Access via Browser
===========================

Once startup is complete, access the following URLs:

- **Search Screen**: http://localhost:8080/
- **Admin Screen**: http://localhost:8080/admin

Default administrator account:

- Username: ``admin``
- Password: ``admin``

.. warning::

   **Important Security Notice**

   In production environments, always change the administrator password.
   For details, refer to :doc:`security`.

Data Persistence
================

Volumes are automatically created to retain data even after deleting Docker containers.

Check volumes::

    $ docker volume ls

|Fess| related volumes:

- ``fess-es-data``: OpenSearch index data
- ``fess-data``: Fess configuration data

.. important::

   Volumes are not deleted when containers are removed.
   To delete volumes, explicitly run the ``docker volume rm`` command.

Stop Docker Containers
=======================

Stop containers::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop

Stop and remove containers::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   The ``down`` command removes containers but not volumes.
   To also delete volumes, add the ``-v`` option::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

   **Note**: This command will delete all data.

Advanced Configuration
======================

Customize Environment Variables
--------------------------------

You can add or modify environment variables in ``compose.yaml`` for detailed configuration.

Main environment variables:

.. list-table::
   :header-rows: 1
   :widths: 30 50

   * - Environment Variable
     - Description
   * - ``FESS_HEAP_SIZE``
     - Fess JVM heap size (default: 1g)
   * - ``SEARCH_ENGINE_HTTP_URL``
     - OpenSearch HTTP endpoint
   * - ``TZ``
     - Time zone (e.g., Asia/Tokyo)

Example::

    environment:
      - "FESS_HEAP_SIZE=4g"
      - "TZ=Asia/Tokyo"

How to Apply Configuration Files
---------------------------------

Detailed |Fess| settings are written in the ``fess_config.properties`` file.
In Docker environments, there are the following methods to apply these file settings.

Method 1: Mount Configuration File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By mounting a directory containing ``fess_config.properties`` and other configuration files,
you can apply settings edited on the host side to the container.

1. Create a configuration directory on the host::

       $ mkdir -p /path/to/fess-config

2. Get the configuration file template (first time only)::

       $ curl -o /path/to/fess-config/fess_config.properties https://raw.githubusercontent.com/codelibs/fess/refs/tags/fess-15.4.0/src/main/resources/fess_config.properties

3. Edit ``/path/to/fess-config/fess_config.properties`` to add required settings::

       # Example
       crawler.document.cache.enabled=false
       adaptive.load.control=20
       query.facet.fields=label,host

4. Add volume mount to ``compose.yaml``::

       services:
         fess:
           volumes:
             - /path/to/fess-config:/opt/fess/app/WEB-INF/conf

5. Start the container::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   ``fess_config.properties`` contains search settings, crawler settings,
   mail settings, and other system configurations.
   Even if you delete containers with ``docker compose down``, files on the host side are preserved.

Method 2: Configuration via System Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can override configuration items in ``fess_config.properties`` via environment variables using system properties.

Configuration items written in ``fess_config.properties`` (e.g., ``crawler.document.cache.enabled=false``)
can be specified in the format ``-Dfess.config.setting_name=value``.

Add ``FESS_JAVA_OPTS`` to environment variables in ``compose.yaml``::

    services:
      fess:
        environment:
          - "FESS_JAVA_OPTS=-Dfess.config.crawler.document.cache.enabled=false -Dfess.config.adaptive.load.control=20 -Dfess.config.query.facet.fields=label,host"

.. note::

   The part following ``-Dfess.config.`` corresponds to the configuration item name in ``fess_config.properties``.

Connect to External OpenSearch
-------------------------------

To use an existing OpenSearch cluster, edit ``compose.yaml`` to change the connection destination.

1. Do not use ``compose-opensearch3.yaml``::

       $ docker compose -f compose.yaml up -d

2. Set ``SEARCH_ENGINE_HTTP_URL``::

       environment:
         - "SEARCH_ENGINE_HTTP_URL=http://your-opensearch-host:9200"

Docker Network Configuration
-----------------------------

When integrating with multiple services, you can use a custom network.

Example::

    networks:
      fess-network:
        driver: bridge

    services:
      fess:
        networks:
          - fess-network

Production Operation with Docker Compose
=========================================

Recommended settings when using Docker Compose in production:

1. **Set resource limits**::

       deploy:
         resources:
           limits:
             cpus: '2.0'
             memory: 4G
           reservations:
             cpus: '1.0'
             memory: 2G

2. **Set restart policy**::

       restart: unless-stopped

3. **Configure logging**::

       logging:
         driver: "json-file"
         options:
           max-size: "10m"
           max-file: "3"

4. **Enable security settings**

   Enable OpenSearch security plugin and configure appropriate authentication.
   For details, refer to :doc:`security`.

Troubleshooting
===============

Container Won't Start
---------------------

1. Check logs::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs

2. Check for port conflicts::

       $ sudo netstat -tuln | grep 8080
       $ sudo netstat -tuln | grep 9200

3. Check disk space::

       $ df -h

Out of Memory Error
-------------------

If OpenSearch fails to start due to insufficient memory, you need to increase ``vm.max_map_count``.

On Linux::

    $ sudo sysctl -w vm.max_map_count=262144

For persistent configuration::

    $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
    $ sudo sysctl -p

Initialize Data
---------------

To delete all data and return to the initial state::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v
    $ docker volume prune

.. warning::

   This command will completely delete all data.

Next Steps
==========

After installation is complete, refer to the following documentation:

- :doc:`run` - Starting |Fess| and initial setup
- :doc:`security` - Security configuration for production environments
- :doc:`troubleshooting` - Troubleshooting

Frequently Asked Questions
===========================

Q: How large are the Docker images?
------------------------------------

A: The Fess image is approximately 1GB, and the OpenSearch image is approximately 800MB.
The initial startup may take time to download.

Q: Can I operate on Kubernetes?
--------------------------------

A: Yes, you can. You can operate on Kubernetes by converting Docker Compose files to Kubernetes manifests or using Helm charts.
For details, refer to the official Fess documentation.

Q: How do I update containers?
-------------------------------

A: Update with the following procedure:

1. Obtain the latest Compose files
2. Stop containers::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

3. Pull new images::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

4. Start containers::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Q: Is a multi-node configuration possible?
-------------------------------------------

A: Yes, it is possible. By editing ``compose-opensearch3.yaml`` to define multiple OpenSearch nodes, you can create a cluster configuration. However, for production environments, we recommend using orchestration tools such as Kubernetes.
