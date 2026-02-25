==========================
SearchLog API
==========================

Overview
========

SearchLog API is an API for retrieving and managing |Fess| search logs.
It can be used for user search behavior analysis and search quality improvement.

Base URL
========

::

    /api/admin/searchlog

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
     - List search logs
   * - GET
     - /{id}
     - Get search log details
   * - DELETE
     - /{id}
     - Delete search log
   * - DELETE
     - /delete-all
     - Bulk delete search logs
   * - GET
     - /stats
     - Get search statistics

List Search Logs
================

Request
-------

::

    GET /api/admin/searchlog

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
   * - ``from``
     - String
     - No
     - Start date/time (ISO 8601 format)
   * - ``to``
     - String
     - No
     - End date/time (ISO 8601 format)
   * - ``query``
     - String
     - No
     - Filter by search query
   * - ``user``
     - String
     - No
     - Filter by user ID

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "searchlog_id_1",
            "searchWord": "Fess installation",
            "requestedAt": "2025-01-29T10:00:00Z",
            "responseTime": 125,
            "hitCount": 234,
            "queryOffset": 0,
            "queryPageSize": 10,
            "user": "user001",
            "userSessionId": "session_abc123",
            "clientIp": "192.168.1.100",
            "referer": "https://example.com/",
            "userAgent": "Mozilla/5.0 ...",
            "roles": ["user", "admin"],
            "languages": ["ja"]
          },
          {
            "id": "searchlog_id_2",
            "searchWord": "search configuration",
            "requestedAt": "2025-01-29T09:55:00Z",
            "responseTime": 98,
            "hitCount": 567,
            "queryOffset": 0,
            "queryPageSize": 10,
            "user": "user002",
            "userSessionId": "session_def456",
            "clientIp": "192.168.1.101",
            "referer": "",
            "userAgent": "Mozilla/5.0 ...",
            "roles": ["user"],
            "languages": ["ja", "en"]
          }
        ],
        "total": 10000
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
     - Search log ID
   * - ``searchWord``
     - Search keyword
   * - ``requestedAt``
     - Search date/time
   * - ``responseTime``
     - Response time (milliseconds)
   * - ``hitCount``
     - Hit count
   * - ``queryOffset``
     - Result offset
   * - ``queryPageSize``
     - Page size
   * - ``user``
     - User ID
   * - ``userSessionId``
     - Session ID
   * - ``clientIp``
     - Client IP address
   * - ``referer``
     - Referer
   * - ``userAgent``
     - User agent
   * - ``roles``
     - User roles
   * - ``languages``
     - Search languages

Get Search Log Details
======================

Request
-------

::

    GET /api/admin/searchlog/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "searchlog_id_1",
          "searchWord": "Fess installation",
          "requestedAt": "2025-01-29T10:00:00Z",
          "responseTime": 125,
          "hitCount": 234,
          "queryOffset": 0,
          "queryPageSize": 10,
          "user": "user001",
          "userSessionId": "session_abc123",
          "clientIp": "192.168.1.100",
          "referer": "https://example.com/",
          "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
          "roles": ["user", "admin"],
          "languages": ["ja"],
          "clickLogs": [
            {
              "url": "https://fess.codelibs.org/install.html",
              "docId": "doc_123",
              "order": 1,
              "clickedAt": "2025-01-29T10:00:15Z"
            }
          ]
        }
      }
    }

Delete Search Log
=================

Request
-------

::

    DELETE /api/admin/searchlog/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Search log deleted successfully"
      }
    }

Bulk Delete Search Logs
=======================

Request
-------

::

    DELETE /api/admin/searchlog/delete-all

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Type
     - Required
     - Description
   * - ``before``
     - String
     - No
     - Delete logs before this date/time (ISO 8601 format)
   * - ``user``
     - String
     - No
     - Delete logs for specific user only

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Search logs deleted successfully",
        "deletedCount": 5000
      }
    }

Get Search Statistics
=====================

Request
-------

::

    GET /api/admin/searchlog/stats

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Type
     - Required
     - Description
   * - ``from``
     - String
     - No
     - Start date/time (ISO 8601 format)
   * - ``to``
     - String
     - No
     - End date/time (ISO 8601 format)
   * - ``interval``
     - String
     - No
     - Aggregation interval (hour/day/week/month)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "stats": {
          "totalSearches": 50000,
          "uniqueUsers": 1234,
          "averageResponseTime": 156,
          "averageHitCount": 345,
          "zeroHitRate": 0.05,
          "topSearchWords": [
            {"word": "Fess", "count": 1500},
            {"word": "installation", "count": 800},
            {"word": "configuration", "count": 650}
          ],
          "searchesByDate": [
            {"date": "2025-01-29", "count": 2500},
            {"date": "2025-01-28", "count": 2300},
            {"date": "2025-01-27", "count": 2100}
          ]
        }
      }
    }

Usage Examples
==============

List Search Logs
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?size=100&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Get Logs for Time Period
------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?from=2025-01-01T00:00:00Z&to=2025-01-31T23:59:59Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

Get Logs for Specific User
--------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?user=user001" \
         -H "Authorization: Bearer YOUR_TOKEN"

Get Logs for Specific Keyword
-----------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?query=Fess" \
         -H "Authorization: Bearer YOUR_TOKEN"

Get Search Statistics
---------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog/stats?from=2025-01-01&to=2025-01-31&interval=day" \
         -H "Authorization: Bearer YOUR_TOKEN"

Delete Old Search Logs
----------------------

.. code-block:: bash

    # Delete logs older than 30 days
    curl -X DELETE "http://localhost:8080/api/admin/searchlog/delete-all?before=2024-12-30T00:00:00Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

Extract Popular Search Keywords
-------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog/stats?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.stats.topSearchWords'

Analyze Search Quality
----------------------

.. code-block:: bash

    # Check zero hit rate
    curl -X GET "http://localhost:8080/api/admin/searchlog/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '{zeroHitRate: .response.stats.zeroHitRate, averageHitCount: .response.stats.averageHitCount}'

Get Daily Search Trends
-----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog/stats?interval=day&from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.stats.searchesByDate'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-stats` - System Stats API
- :doc:`../../admin/searchlog-guide` - Search Log Management Guide
- :doc:`../../config/admin-opensearch-dashboards` - Search Analytics Settings Guide

