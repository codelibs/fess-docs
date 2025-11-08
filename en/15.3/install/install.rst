============================
Choosing an Installation Method
============================

This page provides an overview of |Fess| installation methods.
Select the appropriate installation method based on your environment.

.. warning::

   **Important Notice for Production Environments**

   Running with the embedded OpenSearch is not recommended for production environments or load testing.
   Always set up an external OpenSearch server.

Verify Prerequisites
====================

Before starting the installation, verify the system requirements.

For details, refer to :doc:`prerequisites`.

Installation Method Comparison
===============================

|Fess| can be installed using the following methods. Choose according to your environment and use case.

.. list-table::
   :header-rows: 1
   :widths: 15 25 30 30

   * - Method
     - Target OS
     - Recommended Use
     - Detailed Documentation
   * - Docker
     - Linux, Windows, macOS
     - Development/evaluation environments, rapid setup
     - :doc:`install-docker`
   * - TAR.GZ
     - Linux, macOS
     - Environments requiring customization
     - :doc:`install-linux`
   * - RPM
     - RHEL, CentOS, Fedora
     - Production environments (RPM-based)
     - :doc:`install-linux`
   * - DEB
     - Debian, Ubuntu
     - Production environments (DEB-based)
     - :doc:`install-linux`
   * - ZIP
     - Windows
     - Development/production on Windows
     - :doc:`install-windows`

Features of Each Installation Method
=====================================

Docker Version
--------------

**Advantages:**

- Fastest setup possible
- No need to manage dependencies
- Ideal for development environments
- Easy to start and stop containers

**Disadvantages:**

- Requires Docker knowledge

**Recommended Environments:** Development environments, evaluation environments, POC, production environments

Details: :doc:`install-docker`

Linux Package Versions (TAR.GZ/RPM/DEB)
----------------------------------------

**Advantages:**

- High performance in native environments
- Can be managed as system services (RPM/DEB)
- Allows detailed customization

**Disadvantages:**

- Requires manual installation of Java and OpenSearch
- Configuration requires more effort

**Recommended Environments:** Production environments, environments requiring customization

Details: :doc:`install-linux`

Windows Version (ZIP)
---------------------

**Advantages:**

- Runs in Windows native environments
- No installer required

**Disadvantages:**

- Requires manual installation of Java and OpenSearch
- Configuration requires more effort

**Recommended Environments:** Development/evaluation on Windows, production operation on Windows Server

Details: :doc:`install-windows`

Basic Installation Flow
========================

The basic flow is the same for all installation methods.

1. **Verify System Requirements**

   Refer to :doc:`prerequisites` to ensure system requirements are met.

2. **Download Software**

   Download |Fess| from the `download site <https://fess.codelibs.org/downloads.html>`__.

   For the Docker version, obtain the Docker Compose file.

3. **Set Up OpenSearch**

   For non-Docker versions, OpenSearch must be set up separately.

   - Install OpenSearch 3.3.2
   - Install required plugins
   - Edit configuration files

4. **Set Up Fess**

   - Install Fess
   - Edit configuration files (connection information to OpenSearch, etc.)

5. **Start and Verify**

   - Start services
   - Verify operation by accessing through a browser

   For details, refer to :doc:`run`.

Required Components
===================

The following components are required to run |Fess|.

Fess Main System
----------------

The main full-text search system. Provides functionality such as web interface, crawler, and indexer.

OpenSearch
----------

OpenSearch is used as the search engine.

- **Supported Version**: OpenSearch 3.3.2
- **Required Plugins**:

  - opensearch-analysis-fess
  - opensearch-analysis-extension
  - opensearch-minhash
  - opensearch-configsync

.. important::

   The OpenSearch version and plugin versions must match.
   Version mismatches can cause startup errors or unexpected behavior.

Java (Non-Docker Versions)
---------------------------

For TAR.GZ/ZIP/RPM/DEB versions, Java 21 or later is required.

- Recommended: `Eclipse Temurin <https://adoptium.net/temurin>`__
- OpenJDK 21 or later can also be used

.. note::

   For the Docker version, Java is included in the Docker image and does not need to be installed separately.

Next Steps
==========

Verify the system requirements and select the appropriate installation method.

1. :doc:`prerequisites` - Verify system requirements
2. Choose an installation method:

   - :doc:`install-docker` - Docker installation
   - :doc:`install-linux` - Linux installation
   - :doc:`install-windows` - Windows installation

3. :doc:`run` - Starting |Fess| and initial setup
4. :doc:`security` - Security configuration (for production environments)

Frequently Asked Questions
===========================

Q: Is OpenSearch required?
---------------------------

A: Yes, it is required. |Fess| uses OpenSearch as its search engine.
For the Docker version, it is automatically set up, but for other methods, manual installation is necessary.

Q: Can I upgrade from a previous version?
------------------------------------------

A: Yes, you can. For details, refer to :doc:`upgrade`.

Q: Can I configure with multiple servers?
------------------------------------------

A: Yes, you can. Fess and OpenSearch can run on separate servers.
Additionally, by configuring OpenSearch as a cluster, high availability and improved performance can be achieved.

Download
========

|Fess| and related components can be downloaded from:

- **Fess**: `Download Site <https://fess.codelibs.org/downloads.html>`__
- **OpenSearch**: `Download OpenSearch <https://opensearch.org/downloads.html>`__
- **Java (Adoptium)**: `Adoptium <https://adoptium.net/>`__
- **Docker**: `Get Docker <https://docs.docker.com/get-docker/>`__

Version Information
===================

This document covers the following versions:

- **Fess**: 15.3.2
- **OpenSearch**: 3.3.2
- **Java**: 21 or later
- **Docker**: 20.10 or later
- **Docker Compose**: 2.0 or later

For documentation on previous versions, please refer to the documentation for each version.
