=================
Quick Start Guide
=================

Introduction
============

Fess is an open-source full-text search server that crawls websites and file servers, enabling cross-document search of collected content.

This guide is intended for those who want to quickly try out Fess, describing the minimum steps to get it up and running.

Which Method Should You Use?
============================

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * -
     - Docker (Recommended)
     - ZIP Package
   * - Prerequisites
     - Docker and Docker Compose
     - Java 21, OpenSearch
   * - Ease of Setup
     - ◎ Just a few commands
     - △ Multiple software installations required
   * - Best For
     - Those who want to try it first
     - Those in environments where Docker is unavailable

Method 1: Docker (Recommended)
===============================

Estimated time: **5–10 minutes on first run** (including Docker image download)

Docker provides the fastest and most reliable way to run Fess. All dependencies
are bundled, so there's nothing else to install.

**Step 1: Download the configuration files**

.. code-block:: bash

    mkdir fess-docker && cd fess-docker
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml

**Step 2: Start the containers**

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

**Step 3: Access Fess**

Wait a couple of minutes for the services to initialize, then open your browser:

- **Search Interface:** http://localhost:8080/
- **Admin Panel:** http://localhost:8080/admin
- **Default credentials:** admin / admin

.. warning::

   **Security Notice:** Change the default admin password immediately after your first login.

**Step 4: Stop Fess**

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml down

For advanced Docker configuration (custom settings, external OpenSearch, Kubernetes),
see the :doc:`Docker Installation Guide <15.6/install/install-docker>`.

----

Method 2: ZIP Package
=====================

Estimated time: **20–30 minutes on first run** (including Java and OpenSearch installation)

If you prefer not to use Docker, you can run Fess directly from the ZIP package.

.. note::

   This method is intended for evaluation purposes. For production deployments,
   we recommend using Docker or installing with :doc:`RPM/DEB packages <setup>`.

Prerequisites
-------------

Before starting Fess, please install the following software.

**1. Install Java 21**

We recommend `Eclipse Temurin <https://adoptium.net/temurin>`__ Java 21.

**2. Install and Start OpenSearch**

OpenSearch is required to store Fess data.
Please refer to :doc:`Installation Guide <setup>` to install and start it.

Download and Install
--------------------

1. Download the latest ZIP package from `GitHub Releases <https://github.com/codelibs/fess/releases>`__

2. Extract and enter the directory:

.. code-block:: bash

    unzip fess-x.y.z.zip
    cd fess-x.y.z

Start Fess
----------

.. code-block:: bash

    # Linux/Mac
    ./bin/fess

    # Windows
    bin\fess.bat

Wait about 30 seconds for Fess to start, then access:

- http://localhost:8080/ (Search)
- http://localhost:8080/admin (Admin - login: admin/admin)

.. warning::

   Please change the default password. For production environments, it is strongly
   recommended to change the password immediately after your first login.

Stop Fess (ZIP)
---------------

Press ``Ctrl+C`` in the terminal, or use ``kill`` to stop the fess process.

----

Crawl Configuration and Search
================================

**1. Create a Web Crawl Configuration**

1. Log in to the Admin Panel (http://localhost:8080/admin)
2. Navigate to **Crawler** → **Web** in the left menu
3. Click **New** to create a new configuration
4. Fill in the required fields:

   - **Name:** My First Crawl
   - **URL:** https://www.example.com/ (URL of the site to crawl)
   - **Max Access Count:** 10 (for initial testing, a small value is recommended)
   - **Interval:** 1000 (milliseconds between requests; the default 1000 ms is recommended)

5. Click **Create** to save

.. warning::

   Setting the Max Access Count too high may put excessive load on the target site.
   Always start with a small value (around 10–100) for testing.
   When crawling sites you do not manage, please follow the robots.txt settings.

**2. Run the Crawler**

1. Go to **System** → **Scheduler**
2. Find **Default Crawler** in the list
3. Click **Start Now**
4. Monitor progress in **System** → **Crawling Info**

For scheduled execution, select **Default Crawler** and set the schedule.
If the start time is 10:35 am, enter ``35 10 * * ?`` (format: ``minute hour day month weekday``).

**3. Search**

Once crawling completes (check for WebIndexSize in session info):

Visit http://localhost:8080/ and enter a search term to see your results.

----

What's Next?
============

- :doc:`Full Documentation <documentation>` - Complete reference guide
- :doc:`Installation Guide <setup>` - Production deployment options
- :doc:`Admin Guide <15.6/admin/index>` - Configuration and management
- :doc:`API Reference <15.6/api/index>` - Integrate search into your applications
- `Discussion Forum <https://discuss.codelibs.org/c/fessen/>`__ - Ask questions, share tips
- `GitHub Issues <https://github.com/codelibs/fess/issues>`__ - Report bugs, request features
