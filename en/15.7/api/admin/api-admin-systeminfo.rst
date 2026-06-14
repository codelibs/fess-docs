==========================
SystemInfo API
==========================

Overview
========

SystemInfo API is an API for retrieving |Fess| system information.
You can view environment variables, Java system properties, |Fess| configuration properties, and bug report information.

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

The response includes ``version`` indicating the product version, ``status`` indicating the
processing result, and the following four property groups. Each property group is an array of
objects that have ``key`` and ``value``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "envProps": [
          {"key": "JAVA_HOME", "value": "/usr/lib/jvm/java-21"},
          {"key": "FESS_DICTIONARY_PATH", "value": "/var/lib/fess/dict"}
        ],
        "systemProps": [
          {"key": "java.version", "value": "21.0.1"},
          {"key": "java.vendor", "value": "Oracle Corporation"},
          {"key": "os.name", "value": "Linux"},
          {"key": "user.dir", "value": "/opt/fess"}
        ],
        "fessProps": [
          {"key": "crawler.document.max.site.length", "value": "50"},
          {"key": "indexer.thread.dump.enabled", "value": "true"}
        ],
        "bugReportProps": [
          {"key": "os.name", "value": "Linux"},
          {"key": "java.vm.version", "value": "21.0.1+12"}
        ]
      }
    }

Response Fields
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``envProps``
     - List of environment variables (array of ``key`` / ``value``)
   * - ``systemProps``
     - List of Java system properties (array of ``key`` / ``value``)
   * - ``fessProps``
     - List of |Fess| configuration properties (array of ``key`` / ``value``)
   * - ``bugReportProps``
     - List of information collected for bug reports (array of ``key`` / ``value``)

Usage Examples
==============

Get System Information
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN"

Extract a Specific System Property
----------------------------------

.. code-block:: bash

    # Extract only the value of java.version
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq -r '.response.systemProps[] | select(.key == "java.version") | .value'

List Environment Variables
--------------------------

.. code-block:: bash

    # Display environment variables in key=value format
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq -r '.response.envProps[] | "\(.key)=\(.value)"'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-stats` - Stats API
- :doc:`api-admin-general` - General Settings API
- :doc:`../../admin/systeminfo-guide` - System Information Guide
