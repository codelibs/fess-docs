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
   * - ``errorCountMin``
     - Integer
     - No
     - Lower bound for the error count (greater than or equal to the specified value)
   * - ``errorCountMax``
     - Integer
     - No
     - Upper bound for the error count (less than or equal to the specified value)
   * - ``errorName``
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
            "threadName": "Crawler-1",
            "errorName": "java.net.ConnectException",
            "errorLog": "Connection refused: connect",
            "errorCount": "3",
            "lastAccessTime": "1738144800000",
            "configId": "webConfig_id_1"
          },
          {
            "id": "failure_id_2",
            "url": "https://example.com/not-found",
            "threadName": "Crawler-2",
            "errorName": "org.codelibs.fess.exception.ContentNotFoundException",
            "errorLog": "Not found: https://example.com/not-found",
            "errorCount": "1",
            "lastAccessTime": "1738143000000",
            "configId": "webConfig_id_1"
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
   * - ``threadName``
     - Thread name
   * - ``errorName``
     - Error name (fully-qualified class name of the exception that occurred; e.g. ``java.net.ConnectException``)
   * - ``errorLog``
     - Error log (exception message or stack trace)
   * - ``errorCount``
     - Number of error occurrences (a numeric value as a string)
   * - ``lastAccessTime``
     - Last access time (epoch milliseconds as a string)
   * - ``configId``
     - Crawl configuration ID

.. note::

   All response fields are returned as strings (JSON string).
   ``errorCount`` is a numeric value represented as a string, and ``lastAccessTime`` is epoch milliseconds represented as a string.

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
          "threadName": "Crawler-1",
          "errorName": "java.net.ConnectException",
          "errorLog": "Connection refused: connect",
          "errorCount": "3",
          "lastAccessTime": "1738144800000",
          "configId": "webConfig_id_1"
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

``errorName`` stores the fully-qualified class name of the exception that occurred during
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

    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?size=100&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Filter by Error Count
---------------------

.. code-block:: bash

    # Get only URLs with 3 or more errors
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?errorCountMin=3" \
         -H "Authorization: Bearer YOUR_TOKEN"

Filter by Error Name
--------------------

.. code-block:: bash

    # errorName stores the fully-qualified class name, so specify it with a wildcard
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?errorName=*ConnectException" \
         -H "Authorization: Bearer YOUR_TOKEN"

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
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '[.response.logs[].errorName] | group_by(.) | map({error: .[0], count: length})'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-crawlinginfo` - Crawling Info API
- :doc:`api-admin-joblog` - Job Log API
- :doc:`../../admin/failureurl-guide` - Failure URL Management Guide
