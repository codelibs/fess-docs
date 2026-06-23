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

This API requires an access token with the ``Radmin-api`` permission.
See :doc:`api-admin-overview` for authentication details.

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

This endpoint accepts no query parameters.

Response
--------

The response includes ``version`` indicating the product version, ``status`` indicating the
processing result, and the following four property groups. Each property group is an array of
objects that have ``label`` and ``value``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "envProps": [
          {"label": "JAVA_HOME", "value": "/usr/lib/jvm/java-21"},
          {"label": "FESS_DICTIONARY_PATH", "value": "/var/lib/fess/dict"}
        ],
        "systemProps": [
          {"label": "java.version", "value": "21.0.1"},
          {"label": "java.vendor", "value": "Oracle Corporation"},
          {"label": "os.name", "value": "Linux"},
          {"label": "user.dir", "value": "/opt/fess"}
        ],
        "fessProps": [
          {"label": "crawler.document.max.site.length", "value": "100"},
          {"label": "indexer.thread.dump.enabled", "value": "true"},
          {"label": "app.cipher.key", "value": "XXXXXXXX"}
        ],
        "bugReportProps": [
          {"label": "os.name", "value": "Linux"},
          {"label": "java.vm.version", "value": "21.0.1+12"}
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
   * - ``version``
     - |Fess| product version (e.g. ``15.7.0``).
   * - ``status``
     - Result code indicating the processing outcome. ``0`` means success.
   * - ``envProps``
     - List of OS environment variables (array of ``label`` / ``value``). Values are returned verbatim via ``System.getenv()``.
   * - ``systemProps``
     - List of Java system properties (array of ``label`` / ``value``). Values are returned verbatim via ``System.getProperties()``.
   * - ``fessProps``
     - List of |Fess| configuration properties (array of ``label`` / ``value``). Includes values from ``fess_config.properties`` and system properties set via the admin UI. Sensitive items are masked (see note below).
   * - ``bugReportProps``
     - List of information collected for bug reports (array of ``label`` / ``value``). Includes key OS and Java runtime system properties (``os.name``, ``os.version``, ``java.vm.version``, etc.) and |Fess| system property values.

.. note::

   In ``fessProps``, the following sensitive configuration values are masked and returned as ``XXXXXXXX``:
   ``http.proxy.password``, ``ldap.admin.security.credentials``, ``spnego.preauth.password``,
   ``app.cipher.key``, ``oic.client.id``, ``oic.client.secret``.

.. warning::

   ``envProps`` (environment variables) and ``systemProps`` (Java system properties) are NOT masked —
   values are returned as-is. If secrets such as credentials are stored in environment variables
   or system properties, they will appear in the response.

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
         | jq -r '.response.systemProps[] | select(.label == "java.version") | .value'

List Environment Variables
--------------------------

.. code-block:: bash

    # Display environment variables in label=value format
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq -r '.response.envProps[] | "\(.label)=\(.value)"'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-stats` - Stats API
- :doc:`api-admin-general` - General Settings API
- :doc:`../../admin/systeminfo-guide` - System Information Guide
