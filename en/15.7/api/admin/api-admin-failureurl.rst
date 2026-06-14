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
     - Number of items per page
   * - ``page``
     - Integer
     - No
     - Page number
   * - ``url``
     - String
     - No
     - URL filter
   * - ``errorCountMin``
     - Integer
     - No
     - Minimum error count filter
   * - ``errorCountMax``
     - Integer
     - No
     - Maximum error count filter
   * - ``errorName``
     - String
     - No
     - Error name filter

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
            "errorName": "ConnectException",
            "errorLog": "Connection refused: connect",
            "errorCount": 3,
            "lastAccessTime": 1738144800000,
            "configId": "webConfig_id_1"
          },
          {
            "id": "failure_id_2",
            "url": "https://example.com/not-found",
            "threadName": "Crawler-2",
            "errorName": "HttpStatusException",
            "errorLog": "404 Not Found",
            "errorCount": 1,
            "lastAccessTime": 1738143000000,
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
     - Error name
   * - ``errorLog``
     - Error log
   * - ``errorCount``
     - Number of error occurrences
   * - ``lastAccessTime``
     - Last access time (epoch milliseconds)
   * - ``configId``
     - Crawl configuration ID

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
          "errorName": "ConnectException",
          "errorLog": "Connection refused: connect",
          "errorCount": 3,
          "lastAccessTime": 1738144800000,
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

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Error Name
     - Description
   * - ``ConnectException``
     - Connection error
   * - ``HttpStatusException``
     - HTTP status error (404, 500, etc.)
   * - ``SocketTimeoutException``
     - Timeout error
   * - ``UnknownHostException``
     - Host name resolution error
   * - ``SSLException``
     - SSL certificate error
   * - ``IOException``
     - I/O error

Usage Examples
==============

List Failure URLs
-----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?size=100&page=0" \
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

    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?errorName=ConnectException" \
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
