==========================
FailureUrl API
==========================

Overview
========

FailureUrl API is an API for managing |Fess| crawl failure URLs.
You can view and delete URLs that encountered errors during crawling.

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
     - /
     - List failure URLs
   * - DELETE
     - /{id}
     - Delete failure URL
   * - DELETE
     - /delete-all
     - Delete all failure URLs

List Failure URLs
=================

Request
-------

::

    GET /api/admin/failureurl

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
     - Page number (starts from 0)
   * - ``errorCountMin``
     - Integer
     - No
     - Minimum error count filter
   * - ``configId``
     - String
     - No
     - Configuration ID filter

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "failures": [
          {
            "id": "failure_id_1",
            "url": "https://example.com/broken-page",
            "configId": "webconfig_id_1",
            "errorName": "ConnectException",
            "errorLog": "Connection refused: connect",
            "errorCount": 3,
            "lastAccessTime": "2025-01-29T10:00:00Z",
            "threadName": "Crawler-1"
          },
          {
            "id": "failure_id_2",
            "url": "https://example.com/not-found",
            "configId": "webconfig_id_1",
            "errorName": "HttpStatusException",
            "errorLog": "404 Not Found",
            "errorCount": 1,
            "lastAccessTime": "2025-01-29T09:30:00Z",
            "threadName": "Crawler-2"
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
   * - ``configId``
     - Crawl configuration ID
   * - ``errorName``
     - Error name
   * - ``errorLog``
     - Error log
   * - ``errorCount``
     - Number of error occurrences
   * - ``lastAccessTime``
     - Last access time
   * - ``threadName``
     - Thread name

Delete Failure URL
==================

Request
-------

::

    DELETE /api/admin/failureurl/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Failure URL deleted successfully"
      }
    }

Delete All Failure URLs
=======================

Request
-------

::

    DELETE /api/admin/failureurl/delete-all

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Type
     - Required
     - Description
   * - ``configId``
     - String
     - No
     - Delete only failure URLs for this configuration ID
   * - ``errorCountMin``
     - Integer
     - No
     - Delete only URLs with at least this many errors

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "All failure URLs deleted successfully",
        "deletedCount": 45
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

    curl -X GET "http://localhost:8080/api/admin/failureurl?size=100&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Filter by Error Count
---------------------

.. code-block:: bash

    # Get only URLs with 3 or more errors
    curl -X GET "http://localhost:8080/api/admin/failureurl?errorCountMin=3" \
         -H "Authorization: Bearer YOUR_TOKEN"

Get Failure URLs for Specific Configuration
-------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl?configId=webconfig_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Delete Failure URL
------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/failureurl/failure_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Delete All Failure URLs
-----------------------

.. code-block:: bash

    # Delete all failure URLs
    curl -X DELETE "http://localhost:8080/api/admin/failureurl/delete-all" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Delete failure URLs only for a specific configuration
    curl -X DELETE "http://localhost:8080/api/admin/failureurl/delete-all?configId=webconfig_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Delete only URLs with 3 or more errors
    curl -X DELETE "http://localhost:8080/api/admin/failureurl/delete-all?errorCountMin=3" \
         -H "Authorization: Bearer YOUR_TOKEN"

Aggregate by Error Type
-----------------------

.. code-block:: bash

    # Count by error type
    curl -X GET "http://localhost:8080/api/admin/failureurl?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '[.response.failures[].errorName] | group_by(.) | map({error: .[0], count: length})'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-crawlinginfo` - Crawling Info API
- :doc:`api-admin-joblog` - Job Log API
- :doc:`../../admin/failureurl-guide` - Failure URL Management Guide

