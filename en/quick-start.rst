=================
Quick Start Guide
=================

Get Fess Up and Running in Under 5 Minutes
==========================================

Welcome! This guide will help you get Fess running as quickly as possible.
Choose the method that best suits your environment.

.. tip::

   **Fastest Way: Docker (Recommended)**

   If you have Docker installed, you can have Fess running in about 3 minutes
   with just a few commands—no other dependencies required.

----

Method 1: Docker (Recommended)
==============================

Docker provides the fastest and most reliable way to run Fess. All dependencies
are bundled, so there's nothing else to install.

**Requirements:**

- Docker 20.10 or later
- Docker Compose 2.0 or later

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

**Stopping Fess:**

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml down

For advanced Docker configuration (custom settings, external OpenSearch, Kubernetes),
see the `Docker Installation Guide <15.5/install/install-docker.html>`__.

----

Method 2: ZIP Package
=====================

If you prefer not to use Docker, you can run Fess directly from the ZIP package.

.. note::

   This method is intended for evaluation purposes. For production deployments,
   we recommend using Docker or installing with :doc:`RPM/DEB packages <setup>`.

Prerequisites
-------------

**Java 21** is required. We recommend `Eclipse Temurin <https://adoptium.net/temurin>`__.

Verify your Java installation:

.. code-block:: bash

    java -version

Download and Install
--------------------

1. Download the latest ZIP package from `GitHub Releases <https://github.com/codelibs/fess/releases>`__

2. Extract and enter the directory:

.. code-block:: bash

    unzip fess-15.5.0.zip
    cd fess-15.5.0

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

Stop Fess
---------

Press ``Ctrl+C`` in the terminal, or use ``kill`` to stop the fess process.

----

Your First Search: A Quick Tutorial
===================================

Now that Fess is running, let's set up your first web crawl.

Step 1: Create a Web Crawl Configuration
----------------------------------------

1. Log in to the Admin Panel (http://localhost:8080/admin)
2. Navigate to **Crawler** → **Web** in the left menu
3. Click **New** to create a new configuration
4. Fill in the required fields:

   - **Name:** My First Crawl
   - **URL:** https://fess.codelibs.org/ (or any website you want to index)
   - **Max Access Count:** 100 (limits pages to crawl)
   - **Interval:** 1000 (milliseconds between requests)

5. Click **Create** to save

Step 2: Run the Crawler
-----------------------

1. Go to **System** → **Scheduler**
2. Find **Default Crawler** in the list
3. Click **Start Now**
4. Monitor progress in **System** → **Crawling Info**

Step 3: Search Your Content
---------------------------

Once crawling completes (check for WebIndexSize in session info):

1. Visit http://localhost:8080/
2. Enter a search term related to the pages you crawled
3. View your search results!

----

What's Next?
============

**Ready to dive deeper?**

- `Full Documentation <documentation.html>`__ - Complete reference guide
- `Installation Guide <setup.html>`__ - Production deployment options
- `Admin Guide <15.5/admin/index.html>`__ - Configuration and management
- `API Reference <15.5/api/index.html>`__ - Integrate search into your applications

**Need Help?**

- `Discussion Forum <https://discuss.codelibs.org/c/fessen/>`__ - Ask questions, share tips
- `GitHub Issues <https://github.com/codelibs/fess/issues>`__ - Report bugs, request features
- `Commercial Support <support-services.html>`__ - Professional assistance

**Explore More Features:**

- File system crawling (local files, network shares)
- Database integration
- LDAP/Active Directory authentication
- Custom search result ranking
- Multi-language support

