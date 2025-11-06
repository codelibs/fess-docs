===================
System Requirements
===================

This page describes the hardware and software requirements for running |Fess|.

Hardware Requirements
=====================

Minimum Requirements
--------------------

The following are minimum requirements for evaluation and development environments:

- CPU: 2 cores or more
- Memory: 4GB or more
- Disk Space: 10GB or more of available space

Recommended Requirements
------------------------

For production environments, the following specifications are recommended:

- CPU: 4 cores or more
- Memory: 8GB or more (scale up according to index size)
- Disk Space:

  - System: 20GB or more
  - Data: 3 times the index size or more (including replicas)

- Network: 1Gbps or faster

.. note::

   When the index size is large or you perform high-frequency crawling,
   increase memory and disk space appropriately.

Software Requirements
=====================

Operating Systems
-----------------

|Fess| runs on the following operating systems:

**Linux**

- Red Hat Enterprise Linux 8 or later
- CentOS 8 or later
- Ubuntu 20.04 LTS or later
- Debian 11 or later
- Other Linux distributions (environments where Java 21 can run)

**Windows**

- Windows Server 2019 or later
- Windows 10 or later

**Others**

- macOS 11 (Big Sur) or later (recommended for development environments only)
- Environments where Docker can run

Required Software
-----------------

The required software varies depending on the installation method:

TAR.GZ/ZIP/RPM/DEB Versions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Java 21**: `Eclipse Temurin <https://adoptium.net/temurin>`__ is recommended

  - OpenJDK 21 or later
  - Eclipse Temurin 21 or later

- **OpenSearch 3.3.0**: Required for production environments (embedded version not recommended)

  - Supported Version: OpenSearch 3.3.0
  - Compatibility with plugins must be considered for other versions

Docker Version
~~~~~~~~~~~~~~

- **Docker**: 20.10 or later
- **Docker Compose**: 2.0 or later

Network Requirements
====================

Required Ports
--------------

The main ports used by |Fess| are as follows:

.. list-table::
   :header-rows: 1
   :widths: 15 15 50

   * - Port
     - Protocol
     - Purpose
   * - 8080
     - HTTP
     - |Fess| Web Interface (search and admin screens)
   * - 9200
     - HTTP
     - OpenSearch HTTP API (communication from |Fess| to OpenSearch)
   * - 9300
     - TCP
     - OpenSearch transport communication (cluster configuration)

.. warning::

   In production environments, strongly recommend restricting direct external access to ports 9200 and 9300.
   These ports should only be used for internal communication between |Fess| and OpenSearch.

Firewall Settings
-----------------

To make |Fess| accessible from external sources, port 8080 must be opened.

**Linux (using firewalld)**

::

    $ sudo firewall-cmd --permanent --add-port=8080/tcp
    $ sudo firewall-cmd --reload

**Linux (using iptables)**

::

    $ sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
    $ sudo iptables-save

Browser Requirements
====================

The following browsers are recommended for |Fess| admin and search screens:

- Google Chrome (latest version)
- Mozilla Firefox (latest version)
- Microsoft Edge (latest version)
- Safari (latest version)

.. note::

   Internet Explorer is not supported.

Prerequisites Checklist
=======================

Before installation, verify the following items:

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Verification Item
     - Status
   * - Hardware requirements met
     - □
   * - Java 21 installed (except Docker version)
     - □
   * - Docker installed (Docker version)
     - □
   * - Required ports available
     - □
   * - Firewall configured appropriately
     - □
   * - Sufficient disk space available
     - □
   * - Network connection working (for crawling external sites)
     - □

Next Steps
==========

After verifying the system requirements, proceed to the installation procedure for your environment:

- :doc:`install-linux` - Linux (TAR.GZ/RPM/DEB) Installation
- :doc:`install-windows` - Windows (ZIP) Installation
- :doc:`install-docker` - Docker Installation
- :doc:`install` - Installation Method Overview
