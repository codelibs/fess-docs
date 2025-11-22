================
Installation Guide
================

Installation Methods
====================

Fess provides distributions in ZIP archives, RPM/DEB packages, and Docker images.
Using Docker allows you to easily set up Fess on Windows, Mac, and other platforms.

For production environments, be sure to refer to :doc:`15.3/install/index`.

.. warning::

   **Important Notes for Production Environments**

   Running with the embedded OpenSearch is not recommended for production environments or load testing.
   Always set up an external OpenSearch server.

Installing Docker Desktop
==========================

This guide explains the installation procedure for Windows.
If Docker Desktop is not already installed, please follow these steps.

The files to download and installation procedures differ by OS, so you need to follow the steps appropriate for your environment.
For details, refer to the `Docker <https://docs.docker.com/get-docker/>`_ documentation.

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

You can also download them using the curl command as follows:

::

    curl -o compose.yaml https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml
    curl -o compose-opensearch3.yaml https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml

Starting Fess
-------------

Start Fess with the docker compose command.

Open a command prompt, navigate to the folder containing the compose.yaml file, and execute the following command:

::

    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   Startup may take several minutes.
   You can check the logs with the following command::

       docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f

   You can exit the log display with ``Ctrl+C``.


Verification
============

Access \http://localhost:8080/ to verify that it has started.

The admin UI is at \http://localhost:8080/admin/.
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

::

    docker compose -f compose.yaml -f compose-opensearch3.yaml stop

To stop and remove containers::

    docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   To also remove volumes with the ``down`` command, add the ``-v`` option.
   Note that this will delete all data::

       docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

Changing Administrator Password
--------------------------------

You can change the password on the User edit page in the admin UI.

.. |image0| image:: ../resources/images/en/install/dockerdesktop-1.png
.. |image1| image:: ../resources/images/en/install/dockerdesktop-2.png
.. |image2| image:: ../resources/images/en/install/dockerdesktop-3.png
.. |image3| image:: ../resources/images/en/install/dockerdesktop-4.png
