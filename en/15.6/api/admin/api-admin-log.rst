==========================
Log API
==========================

Overview
========

Log API is an API for retrieving |Fess| log information.
You can view search logs, click logs, and favorite logs.

Base URL
========

::

    /api/admin/log

Endpoint List
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Method
     - Path
     - Description
   * - GET
     - /search
     - Get search logs
   * - GET
     - /click
     - Get click logs
   * - GET
     - /favorite
     - Get favorite logs
   * - DELETE
     - /search/delete
     - Delete search logs

Get Search Logs
===============

Request
-------

::

    GET /api/admin/log/search

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
     - Search query filter

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "log_id_1",
            "queryId": "query_id_1",
            "query": "fess search",
            "requestedAt": "2025-01-29T10:30:00Z",
            "responseTime": 123,
            "hitCount": 567,
            "user": "guest",
            "roles": ["guest"],
            "languages": ["ja"],
            "clientIp": "192.168.1.100",
            "userAgent": "Mozilla/5.0..."
          }
        ],
        "total": 1234
      }
    }

Get Click Logs
==============

Request
-------

::

    GET /api/admin/log/click

Parameters
~~~~~~~~~~

In addition to the same parameters as search logs, the following can be specified:

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Type
     - Required
     - Description
   * - ``url``
     - String
     - No
     - Clicked URL filter
   * - ``queryId``
     - String
     - No
     - Search query ID filter

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "click_log_id_1",
            "queryId": "query_id_1",
            "url": "https://example.com/doc1",
            "docId": "doc_id_1",
            "order": 1,
            "clickedAt": "2025-01-29T10:31:00Z",
            "user": "guest",
            "clientIp": "192.168.1.100"
          }
        ],
        "total": 567
      }
    }

Get Favorite Logs
=================

Request
-------

::

    GET /api/admin/log/favorite

Parameters
~~~~~~~~~~

Same parameters as click logs.

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "favorite_log_id_1",
            "url": "https://example.com/doc1",
            "docId": "doc_id_1",
            "createdAt": "2025-01-29T10:32:00Z",
            "user": "user123"
          }
        ],
        "total": 123
      }
    }

Delete Search Logs
==================

Request
-------

::

    DELETE /api/admin/log/search/delete

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
     - Yes
     - Delete logs before this date/time (ISO 8601 format)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "deletedCount": 5678
      }
    }

Usage Examples
==============

Get Recent Search Logs
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/search?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Get Search Logs for Time Period
-------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/search?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

Get Search Logs for Specific Query
----------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/search?query=fess" \
         -H "Authorization: Bearer YOUR_TOKEN"

Get Click Logs
--------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/click?size=100" \
         -H "Authorization: Bearer YOUR_TOKEN"

Delete Old Search Logs
----------------------

.. code-block:: bash

    # Delete logs older than 30 days
    curl -X DELETE "http://localhost:8080/api/admin/log/search/delete?before=2024-12-30T00:00:00Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-stats` - Stats API
- :doc:`../../admin/log-guide` - Log Management Guide

