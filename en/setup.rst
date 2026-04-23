================
Installation Guide
================

Installation Methods
====================

Fess provides distributions in ZIP archives, RPM/DEB packages, and Docker images.
Using Docker allows you to easily set up Fess on Windows, Mac, and other platforms.

.. note::

   This page explains setup on **Windows using Docker**. Users on Linux or macOS can follow similar steps, but the Docker Desktop installation differs by platform.
   For details, refer to the `Docker <https://docs.docker.com/get-docker/>`_ documentation.

For production environments, be sure to refer to :doc:`15.6/install/index`.
For system requirements, see :doc:`15.6/install/prerequisites`.

.. warning::

   **Important Notes for Production Environments**

   Running with the embedded OpenSearch is not recommended for production environments or load testing.
   Always set up an external OpenSearch server.

Setup Overview
--------------

Follow these steps in order:

1. Install Docker Desktop
2. Configure the OS (adjust vm.max_map_count)
3. Download Fess startup files
4. Start Fess and verify operation

Installing Docker Desktop
==========================

If Docker Desktop is not already installed, please follow these steps.

Download
--------

Download the installer for your OS from `Docker Desktop <https://www.docker.com/products/docker-desktop/>`__.

Running the Installer
----------------------

Double-click the downloaded installer to start installation.

Confirm that "Install required Windows components for WSL 2" or
"Install required Enable Hyper-V Windows Features" is selected, and
click the OK button.

|image0|

When installation is complete, click the "close" button to close the screen.

|image1|

Starting Docker Desktop
-----------------------

Click "Docker Desktop" in the Windows menu to start it.

|image2|

After Docker Desktop starts, the terms of service will be displayed. Check "I accept the terms" and click the "Accept" button.

A tutorial start prompt will appear, but here we'll click "Skip tutorial" to skip it.
After clicking "Skip tutorial", the Dashboard will be displayed.

|image3|

Configuration
=============

To allow OpenSearch to run as a Docker container, adjust the "vm.max_map_count" value on the OS side.
The configuration method differs depending on your environment, so refer to "`Set vm.max_map_count to at least 262144 <https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#_set_vm_max_map_count_to_at_least_262144>`_" for configuration methods for each environment.

Setting Up Fess
===============

Creating Startup Files
----------------------

Create a directory and download `compose.yaml <https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml>`_ and `compose-opensearch3.yaml <https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml>`_.

.. note::

   ``compose-opensearch3.yaml`` is an additional configuration file for using OpenSearch 3.x.
   It is used in combination with ``compose.yaml``.

You can also download them using the curl command as follows:

.. code-block:: bash

    curl -o compose.yaml https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml
    curl -o compose-opensearch3.yaml https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml

Starting Fess
-------------

Start Fess with the docker compose command.

Open a command prompt, navigate to the folder containing the compose.yaml file, and execute the following command:

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   Startup may take several minutes.
   You can check the logs with the following command:

   .. code-block:: bash

       docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f

   You can exit the log display with ``Ctrl+C``.


Verification
============

.. note::

   Once startup is complete, access the following URLs in your browser to verify.

   - **Search:** http://localhost:8080/
   - **Admin UI:** http://localhost:8080/admin/

The default administrator account username/password is admin/admin.

.. warning::

   **Important Security Notice**

   Be sure to change the default password.
   Especially in production environments, it is strongly recommended to change the password immediately after the first login.

The administrator account is managed by the application server.
In Fess's admin UI, users authenticated with the fess role by the application server are treated as administrators.

Other
=====

Stopping Fess
-------------

To stop Fess, execute the following command in the folder where you started Fess:

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml stop

To stop and remove containers:

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   To also remove volumes with the ``down`` command, add the ``-v`` option.
   Note that this will delete all data.

   .. code-block:: bash

       docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

Changing Administrator Password
--------------------------------

You can change the password on the User edit page in the admin UI.

1. Access http://localhost:8080/admin/ and log in.
2. Select "User" from the top-right menu.
3. Open the edit page for the admin user and change the password.

Next Steps
==========

Now that Fess is set up, refer to the following documentation to get started:

- :doc:`15.6/install/run` — Detailed startup, stop, and configuration
- :doc:`15.6/admin/index` — Administrator guide (crawl settings, user management, etc.)
- :doc:`15.6/user/index` — User guide (how to search)

If you encounter any issues, refer to :doc:`15.6/install/troubleshooting`.

.. |image0| image:: ../resources/images/en/install/dockerdesktop-1.png
.. |image1| image:: ../resources/images/en/install/dockerdesktop-2.png
.. |image2| image:: ../resources/images/en/install/dockerdesktop-3.png
.. |image3| image:: ../resources/images/en/install/dockerdesktop-4.png
