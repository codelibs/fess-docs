==========================
SystemInfo API
==========================

Overview
========

SystemInfo API is an API for retrieving |Fess| system information.
You can view version information, environment variables, and JVM information.

Base URL
========

::

    /api/admin/systeminfo

Endpoint List
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Method
     - Path
     - Description
   * - GET
     - /
     - Get system information

Get System Information
======================

Request
-------

::

    GET /api/admin/systeminfo

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "systemInfo": {
          "fessVersion": "15.5.0",
          "opensearchVersion": "2.11.0",
          "javaVersion": "21.0.1",
          "serverName": "Apache Tomcat/10.1.15",
          "osName": "Linux",
          "osVersion": "5.15.0-89-generic",
          "osArchitecture": "amd64",
          "jvmTotalMemory": "2147483648",
          "jvmFreeMemory": "1073741824",
          "jvmMaxMemory": "4294967296",
          "processorCount": "8",
          "fileEncoding": "UTF-8",
          "userLanguage": "en",
          "userTimezone": "UTC"
        },
        "environmentInfo": {
          "JAVA_HOME": "/usr/lib/jvm/java-21",
          "FESS_DICTIONARY_PATH": "/var/lib/fess/dict",
          "FESS_LOG_PATH": "/var/log/fess"
        },
        "systemProperties": {
          "java.version": "21.0.1",
          "java.vendor": "Oracle Corporation",
          "os.name": "Linux",
          "os.version": "5.15.0-89-generic",
          "user.dir": "/opt/fess",
          "user.home": "/home/fess",
          "user.name": "fess"
        }
      }
    }

Response Fields
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``fessVersion``
     - Fess version
   * - ``opensearchVersion``
     - OpenSearch version
   * - ``javaVersion``
     - Java version
   * - ``serverName``
     - Application server name
   * - ``osName``
     - OS name
   * - ``osVersion``
     - OS version
   * - ``osArchitecture``
     - OS architecture
   * - ``jvmTotalMemory``
     - JVM total memory (bytes)
   * - ``jvmFreeMemory``
     - JVM free memory (bytes)
   * - ``jvmMaxMemory``
     - JVM maximum memory (bytes)
   * - ``processorCount``
     - Processor count
   * - ``fileEncoding``
     - File encoding
   * - ``userLanguage``
     - User language
   * - ``userTimezone``
     - User timezone

Usage Examples
==============

Get System Information
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN"

Check Version
-------------

.. code-block:: bash

    # Extract Fess version only
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.systemInfo.fessVersion'

Check Memory Usage
------------------

.. code-block:: bash

    # Extract JVM memory information
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.systemInfo | {total: .jvmTotalMemory, free: .jvmFreeMemory, max: .jvmMaxMemory}'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-stats` - Stats API
- :doc:`api-admin-general` - General Settings API
- :doc:`../../admin/systeminfo-guide` - System Information Guide

