====================================
Docker Installation (Detailed Guide)
====================================

This page describes the installation procedure for |Fess| using Docker and Docker Compose.
Using Docker allows you to set up a |Fess| environment easily and quickly.

Prerequisites
=============

- System requirements described in :doc:`prerequisites` are met
- Docker 20.10 or later is installed
- Docker Compose 2.0 or later is installed

Verify Docker Installation
==========================

Verify the Docker and Docker Compose versions with the following commands.

::

    $ docker --version
    $ docker compose version

.. note::

   If you are using an older version of Docker Compose, use the ``docker-compose`` command.
   This document uses the new ``docker compose`` command format.

About Docker Images
===================

When you start |Fess| with Docker Compose, the following two containers run.

- **Fess** (``fess01``): The full-text search system itself
- **OpenSearch** (``search01``): The search engine

The official Docker image is published on `GitHub Container Registry <https://github.com/codelibs/docker-fess/pkgs/container/fess>`__.
The Compose files and startup instructions are maintained in the `docker-fess <https://github.com/codelibs/docker-fess>`__ repository.

Step 1: Obtain Docker Compose Files
===================================

The following files are required to start using Docker Compose.

Method 1: Download Files Individually
-------------------------------------

Download the following files:

::

    $ mkdir fess-docker
    $ cd fess-docker
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.8.0/compose/compose.yaml
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.8.0/compose/compose-opensearch3.yaml

Method 2: Clone Repository with Git
-----------------------------------

If Git is installed, you can also clone the entire repository:

::

    $ git clone --depth 1 --branch v15.8.0 https://github.com/codelibs/docker-fess.git
    $ cd docker-fess/compose

Step 2: Review Docker Compose Files
===================================

Contents of ``compose.yaml``
----------------------------

``compose.yaml`` contains the configuration for Fess itself (the ``fess01`` service).

Main configuration items:

- **Port number**: The Fess web interface port (default: 8080)
- **Environment variables**: Settings such as the OpenSearch connection endpoint (``SEARCH_ENGINE_HTTP_URL``) and the dictionary file path (``FESS_DICTIONARY_PATH``)
- **Startup order**: ``depends_on`` is configured so that the service starts only after OpenSearch (``search01``) becomes healthy

Contents of ``compose-opensearch3.yaml``
----------------------------------------

``compose-opensearch3.yaml`` contains the configuration for the search engine (the ``search01`` service, OpenSearch).

Main configuration items:

- **OpenSearch image**: The OpenSearch image used (``ghcr.io/codelibs/fess-opensearch``)
- **Memory settings**: JVM heap size
- **Volumes**: Volumes for data persistence (``search01_data``: index data, ``search01_dictionary``: dictionary files)

Customize Configuration (Optional)
----------------------------------

To change the default settings, edit ``compose.yaml``.

Example: Changing the port number::

    services:
      fess01:
        ports:
          - "9080:8080"  # Map to port 9080 on the host

Example: Changing memory settings::

    services:
      fess01:
        environment:
          - "FESS_HEAP_SIZE=2g"  # Set the Fess heap size to 2GB

Step 3: Start Docker Containers
===============================

Basic Startup
-------------

Start Fess and OpenSearch with the following command:

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   - The ``-f`` option specifies multiple Compose files
   - The ``-d`` option runs it in the background

Check the startup logs::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f

You can exit the log view with ``Ctrl+C``.

Verify Startup
--------------

Check the container status::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

Verify that the following containers are running:

- ``fess01``
- ``search01``

.. tip::

   Startup may take several minutes. OpenSearch (``search01``) becomes healthy first, and then Fess (``fess01``) starts.
   Check the status of each container with ``docker compose ... ps``; once ``fess01`` is up, you can access http://localhost:8080/ in your browser.

Step 4: Access via Browser
==========================

Once startup is complete, access the following URLs:

- **Search screen**: http://localhost:8080/
- **Admin screen**: http://localhost:8080/admin

Default administrator account:

- Username: ``admin``
- Password: ``admin``

.. warning::

   **Important Security Notice**

   In production environments, be sure to change the administrator password.
   For details, refer to :doc:`security`.

Enabling AI Search Mode (LLM Plugin)
====================================

Starting with |Fess| 15.8, the AI Search Mode (RAG Chat) feature has been separated into ``fess-llm-*`` plugins.
The official `docker-fess <https://github.com/codelibs/docker-fess>`__ repository includes overlay files for the major LLM providers.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Overlay
     - Purpose
   * - ``compose-ollama.yaml``
     - Ollama (local LLM, starts an additional ``ollama01`` service)
   * - ``compose-gemini.yaml``
     - Google Gemini (cloud API)
   * - ``compose-openai.yaml``
     - OpenAI (cloud API)

Each overlay automatically retrieves the matching plugin via ``FESS_PLUGINS`` and enables RAG Chat by setting
``-Dfess.config.rag.chat.enabled=true`` in ``FESS_JAVA_OPTS``.
For Gemini and OpenAI, which use cloud APIs, the provider to use is additionally specified with ``-Dfess.system.rag.llm.name``,
and the API key (``rag.llm.<provider>.api.key``) and model (``rag.llm.<provider>.model``) are configured.
For Ollama, since the default value of ``rag.llm.name`` (``ollama``) is used as is, no explicit setting is required,
and only the connection endpoint (``rag.llm.ollama.api.url``) is configured.

Example using Gemini::

    $ export GEMINI_API_KEY="AIzaSy..."
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-gemini.yaml up -d

Example using OpenAI::

    $ export OPENAI_API_KEY="sk-..."
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml up -d

.. note::

   The model to use can be changed with the ``GEMINI_MODEL`` and ``OPENAI_MODEL`` environment variables
   (the defaults are ``gemini-2.5-flash`` and ``gpt-5-mini``, respectively).

Example using Ollama::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-ollama.yaml up -d
    $ docker exec -it ollama01 ollama pull gpt-oss:20b

.. warning::

   The ``ollama01`` service in ``compose-ollama.yaml`` is defined to use an NVIDIA GPU by default
   (the `NVIDIA Container Toolkit <https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html>`__ is required).
   If you are running in an environment without a GPU, remove or comment out the ``deploy:`` block (the GPU specification under ``reservations``) in ``compose-ollama.yaml``.

.. tip::

   After startup, you can change the LLM provider to use (``rag.llm.name``) and provider-specific settings
   from the "System > General" settings screen in the administration screen. However, since these changes are saved to
   the configuration file inside the container, they are lost when the container is re-created (``up`` after ``docker compose down``).
   To persist the settings, specify them in ``FESS_JAVA_OPTS`` in the Compose file, as in the examples above.

Data Persistence
================

All |Fess| data (index, crawled documents, user information, settings, etc.) is stored entirely in OpenSearch.
Since this data is persisted in OpenSearch's volumes, it is retained even if the container is removed.
The Fess service itself (``fess01``) is stateless and has no dedicated volume.

Check the volumes::

    $ docker volume ls

Main volumes defined in ``compose-opensearch3.yaml``:

- ``search01_data``: OpenSearch index data (includes all Fess data)
- ``search01_dictionary``: Dictionary files

.. note::

   Docker Compose volume names are prefixed with the project name (by default, the name of the directory containing the Compose file).
   For example, if started from the ``compose`` directory, the actual volume name would be something like ``compose_search01_data``.

.. important::

   Volumes are not deleted when containers are removed.
   To delete a volume, you must explicitly run the ``docker volume rm`` command.

Stop Docker Containers
======================

Stop the containers::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop

Stop and remove the containers::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   The ``down`` command removes containers but does not delete volumes.
   To also delete volumes (such as ``search01_data``), add the ``-v`` option::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

   **Note**: Running this command deletes all data stored in OpenSearch.

Advanced Configuration
======================

Customize Environment Variables
-------------------------------

You can perform detailed configuration by adding or changing environment variables in ``compose.yaml``.

Main environment variables:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Environment Variable
     - Description
   * - ``FESS_HEAP_SIZE``
     - Fess JVM heap size (default in the Docker image: 512m)
   * - ``FESS_JAVA_OPTS``
     - Specify additional JVM options (such as overriding settings with ``-Dfess.config.*``)
   * - ``FESS_PLUGINS``
     - Plugins to automatically install at startup (space-separated ``name:version`` format; e.g., ``fess-ds-wikipedia:15.8.0``)
   * - ``SEARCH_ENGINE_HTTP_URL``
     - OpenSearch HTTP endpoint (default in ``compose.yaml``: ``http://search01:9200``)
   * - ``SEARCH_ENGINE_USERNAME`` / ``SEARCH_ENGINE_PASSWORD``
     - Credentials for connecting to an OpenSearch instance with authentication enabled
   * - ``FESS_DICTIONARY_PATH``
     - Path to the dictionary files (a directory shared with OpenSearch)
   * - ``FESS_PORT``
     - Port on which Fess listens inside the container (default: 8080)

Example::

    services:
      fess01:
        environment:
          - "FESS_HEAP_SIZE=4g"

.. note::

   To change the time zone, specify something like ``-Duser.timezone=Asia/Tokyo`` in ``FESS_JAVA_OPTS``.

How to Apply Configuration Files
--------------------------------

Detailed |Fess| settings are written in the ``fess_config.properties`` file.
In the Docker image, ``fess_config.properties`` is located at ``/etc/fess`` inside the container.
The following methods are available for applying settings in a Docker environment.

Method 1: Mount Configuration File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since ``/etc/fess`` also contains other configuration files required for Fess to run, replacing this entire directory with a mount will cause startup to fail.
Instead, use the override directory ``/opt/fess``, which is added to the front of the classpath (it is empty by default).

1. Create a directory on the host to hold the configuration file::

       $ mkdir -p /path/to/fess-config

2. Obtain the configuration file template (first time only)::

       $ curl -o /path/to/fess-config/fess_config.properties https://raw.githubusercontent.com/codelibs/fess/refs/tags/fess-15.8.0/src/main/resources/fess_config.properties

3. Edit ``/path/to/fess-config/fess_config.properties`` to write the required settings::

       # Example
       crawler.document.cache.enabled=false
       adaptive.load.control=20
       query.facet.fields=label,host

4. Add a volume mount to the ``fess01`` service in ``compose.yaml``::

       services:
         fess01:
           volumes:
             - /path/to/fess-config/fess_config.properties:/opt/fess/fess_config.properties

5. Start the container::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   Since ``/opt/fess`` is added to the front of the classpath, the ``fess_config.properties`` placed here
   takes precedence over the ``/etc/fess/fess_config.properties`` bundled with the image.
   Property files are loaded as whole files and are not merged item by item.
   Therefore, you must place a **complete file containing all configuration items**, not just the items you want to override.
   If you only want to change some items, use "Method 2" below instead.

Method 2: Configuration via System Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can override configuration items in ``fess_config.properties`` as system properties via environment variables.

Configuration items written in ``fess_config.properties`` (e.g., ``crawler.document.cache.enabled=false``)
are specified in the form ``-Dfess.config.setting_name=value``.

Add ``FESS_JAVA_OPTS`` to the environment variables of the ``fess01`` service in ``compose.yaml``::

    services:
      fess01:
        environment:
          - "FESS_JAVA_OPTS=-Dfess.config.crawler.document.cache.enabled=false -Dfess.config.adaptive.load.control=20 -Dfess.config.query.facet.fields=label,host"

.. note::

   The part following ``-Dfess.config.`` corresponds to the configuration item name in ``fess_config.properties``.
   This method is simpler when you only want to override a few items.

Connect to External OpenSearch
------------------------------

To use an existing OpenSearch cluster, start with only ``compose.yaml`` (without ``compose-opensearch3.yaml``) and change the connection destination.

1. Start without specifying ``compose-opensearch3.yaml``::

       $ docker compose -f compose.yaml up -d

2. Set the connection destination in the ``fess01`` service of ``compose.yaml``::

       environment:
         - "SEARCH_ENGINE_HTTP_URL=http://your-opensearch-host:9200"

.. note::

   If connecting to an OpenSearch instance with authentication enabled, also specify ``SEARCH_ENGINE_USERNAME`` and ``SEARCH_ENGINE_PASSWORD``.

Other Overlays and Configurations
---------------------------------

The ``docker-fess`` repository also includes Compose files and directories for other purposes.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - File / Directory
     - Purpose
   * - ``compose-dashboards3.yaml``
     - Adds OpenSearch Dashboards (port 5601, for data visualization)
   * - ``compose-minio.yaml``
     - Adds MinIO (object storage) and uses it as the storage destination for Fess's storage feature
   * - ``vanilla/``
     - A configuration that combines Fess with a plain OpenSearch that does not include the Fess plugin (some features, such as dictionary management, are unavailable)
   * - ``snapshot/``
     - A configuration that uses development (snapshot) images (including cluster configurations and combinations with Elasticsearch 8)
   * - ``multi-instance/``
     - A configuration that starts multiple Fess instances sharing a single OpenSearch

Docker Network Configuration
----------------------------

When integrating with multiple services, you can use a custom network.

Example::

    networks:
      fess-network:
        driver: bridge

    services:
      fess01:
        networks:
          - fess-network

Production Operation with Docker Compose
========================================

Recommended settings when using Docker Compose in a production environment:

1. **Set resource limits**::

       deploy:
         resources:
           limits:
             cpus: '2.0'
             memory: 4G
           reservations:
             cpus: '1.0'
             memory: 2G

2. **Set the restart policy**::

       restart: unless-stopped

3. **Configure logging**::

       logging:
         driver: "json-file"
         options:
           max-size: "10m"
           max-file: "3"

4. **Enable security settings**

   Enable the OpenSearch security plugin and configure appropriate authentication.
   For details, refer to :doc:`security`.

Troubleshooting
===============

Container Won't Start
---------------------

1. Check the logs::

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

To make the setting persistent::

    $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
    $ sudo sysctl -p

Initialize Data
---------------

To delete all data and return to the initial state::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v
    $ docker volume prune

.. warning::

   Running this command completely deletes all data.

Next Steps
==========

After installation is complete, refer to the following documents:

- :doc:`run` - Starting |Fess| and initial setup
- :doc:`security` - Security configuration for production environments
- :doc:`troubleshooting` - Troubleshooting

Frequently Asked Questions
==========================

Q: How much disk space is required to download the images?
----------------------------------------------------------

A: The Fess and OpenSearch images are downloaded on first startup and together require several GB of disk space.
Depending on your network environment, the download may take some time.

Q: Can I run this on Kubernetes?
--------------------------------

A: Yes, it is possible. You can convert the Docker Compose files into Kubernetes manifests using a tool such as ``kompose``,
or create your own manifests to operate on Kubernetes (an official Helm chart is not provided).

Q: How do I update the containers?
----------------------------------

A: Update using the following procedure:

1. Obtain the latest Compose files
2. Stop the containers::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

3. Pull the new images::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

4. Start the containers::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Q: Is a multi-node configuration possible?
------------------------------------------

A: Yes, it is possible. You can configure OpenSearch with multiple nodes by referring to ``snapshot/compose-cluster.yaml`` in the ``docker-fess`` repository,
or configure multiple Fess instances sharing a single OpenSearch by referring to ``multi-instance/``.
However, for production environments, we recommend using an orchestration tool such as Kubernetes.
