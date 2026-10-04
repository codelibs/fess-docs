==========================
FailureUrl API
==========================

Overview
========

FailureUrl API is an API for managing |Fess| crawl failure URLs.
You can list, retrieve individual entries, and delete URLs that encountered errors during crawling.

Base URL
========

::

    /api/admin/failureurl

Endpoint List
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Method
     - Path
     - Description
   * - GET
     - /logs
     - List failure URLs
   * - GET
     - /log/{id}
     - Get failure URL
   * - DELETE
     - /log/{id}
     - Delete failure URL
   * - DELETE
     - /all
     - Delete all failure URLs

List Failure URLs
=================

Request
-------

::

    GET /api/admin/failureurl/logs

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Type
     - Required
     - Description
   * - ``size``
     - Integer
     - No
     - Number of items per page (default: 20)
   * - ``page``
     - Integer
     - No
     - Page number (starts at 1, default: 1)
   * - ``url``
     - String
     - No
     - URL filter (wildcards ``*`` ``?`` supported)
   * - ``error_count_min``
     - Integer
     - No
     - Lower bound for the error count (greater than or equal to the specified value)
   * - ``error_count_max``
     - Integer
     - No
     - Upper bound for the error count (less than or equal to the specified value)
   * - ``error_name``
     - String
     - No
     - Error name filter (wildcard match against the stored fully-qualified class name; ``*`` ``?`` supported)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "failure_id_1",
            "url": "https://example.com/broken-page",
            "thread_name": "Crawler-1",
            "error_name": "java.net.ConnectException",
            "error_log": "Connection refused: connect",
            "error_count": "3",
            "last_access_time": "1738144800000",
            "config_id": "webConfig_id_1"
          },
          {
            "id": "failure_id_2",
            "url": "https://example.com/not-found",
            "thread_name": "Crawler-2",
            "error_name": "org.codelibs.fess.exception.ContentNotFoundException",
            "error_log": "Not found: https://example.com/not-found",
            "error_count": "1",
            "last_access_time": "1738143000000",
            "config_id": "webConfig_id_1"
          }
        ],
        "total": 45
      }
    }

Response Fields
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``id``
     - Failure URL ID
   * - ``url``
     - Failed URL
   * - ``thread_name``
     - Thread name
   * - ``error_name``
     - Error name (fully-qualified class name of the exception that occurred; e.g. ``java.net.ConnectException``)
   * - ``error_log``
     - Error log (exception message or stack trace)
   * - ``error_count``
     - Number of error occurrences (a numeric value as a string)
   * - ``last_access_time``
     - Last access time (epoch milliseconds as a string)
   * - ``config_id``
     - Crawl configuration ID

.. note::

   All response fields are returned as strings (JSON string).
   ``error_count`` is a numeric value represented as a string, and ``last_access_time`` is epoch milliseconds represented as a string.

Get Failure URL
===============

Request
-------

::

    GET /api/admin/failureurl/log/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "failure_id_1",
          "url": "https://example.com/broken-page",
          "thread_name": "Crawler-1",
          "error_name": "java.net.ConnectException",
          "error_log": "Connection refused: connect",
          "error_count": "3",
          "last_access_time": "1738144800000",
          "config_id": "webConfig_id_1"
        }
      }
    }

Delete Failure URL
==================

Request
-------

::

    DELETE /api/admin/failureurl/log/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Delete All Failure URLs
=======================

Deletes all failure URLs. There are no parameters.

Request
-------

::

    DELETE /api/admin/failureurl/all

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Error Types
===========

``error_name`` stores the fully-qualified class name of the exception that occurred during
crawling, exactly as captured. It is not a fixed enumeration; any class name may appear
depending on the exception that was raised. The following are representative examples.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Error Name (example)
     - Description
   * - ``java.net.ConnectException``
     - Connection refused (cannot connect to the server)
   * - ``java.net.UnknownHostException``
     - Host name could not be resolved (DNS error)
   * - ``java.net.SocketTimeoutException``
     - Connection or read timeout
   * - ``javax.net.ssl.SSLException``
     - SSL/TLS handshake or certificate error
   * - ``java.io.IOException``
     - I/O error
   * - ``org.codelibs.fess.exception.ContentNotFoundException``
     - URL that returned an HTTP status code configured in ``crawler.failure.url.status.codes`` (default: 403, 404, 410)
   * - ``org.codelibs.fess.crawler.exception.MaxLengthExceededException``
     - Content exceeded the maximum length

Usage Examples
==============

List Failure URLs
-----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"size": 100, "page": 1}'

Filter by Error Count
---------------------

.. code-block:: bash

    # Get only URLs with 3 or more errors
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"error_count_min": 3}'

Filter by Error Name
--------------------

.. code-block:: bash

    # error_name stores the fully-qualified class name, so specify it with a wildcard
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"error_name": "*ConnectException"}'

Get Failure URL
---------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/log/failure_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Delete Failure URL
------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/failureurl/log/failure_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Delete All Failure URLs
-----------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/failureurl/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

Aggregate by Error Type
-----------------------

.. code-block:: bash

    # Count by error type
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"size": 1000}' | \
         jq '[.response.logs[].error_name] | group_by(.) | map({error: .[0], count: length})'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-crawlinginfo` - Crawling Info API
- :doc:`api-admin-joblog` - Job Log API
- :doc:`../../admin/failureurl-guide` - Failure URL Management Guide
