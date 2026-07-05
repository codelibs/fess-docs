==========================
CrawlingInfo API
==========================

Overview
========

CrawlingInfo API is an API for retrieving |Fess| crawl information.
You can view crawl session status, progress, and statistics.

Base URL
========

::

    /api/admin/crawlinginfo

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
     - List crawl information
   * - GET
     - /{sessionId}
     - Get crawl session details
   * - DELETE
     - /{sessionId}
     - Delete crawl session

List Crawl Information
======================

Request
-------

::

    GET /api/admin/crawlinginfo

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

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "sessions": [
          {
            "sessionId": "session_20250129_100000",
            "name": "Default Crawler",
            "status": "running",
            "startTime": "2025-01-29T10:00:00Z",
            "endTime": null,
            "crawlingInfoCount": 567,
            "createdDocCount": 234,
            "updatedDocCount": 123,
            "deletedDocCount": 12
          },
          {
            "sessionId": "session_20250128_100000",
            "name": "Default Crawler",
            "status": "completed",
            "startTime": "2025-01-28T10:00:00Z",
            "endTime": "2025-01-28T10:45:23Z",
            "crawlingInfoCount": 1234,
            "createdDocCount": 456,
            "updatedDocCount": 678,
            "deletedDocCount": 23
          }
        ],
        "total": 10
      }
    }

Response Fields
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``sessionId``
     - Session ID
   * - ``name``
     - Crawler name
   * - ``status``
     - Status (running/completed/failed)
   * - ``startTime``
     - Start time
   * - ``endTime``
     - End time
   * - ``crawlingInfoCount``
     - Number of crawl info records
   * - ``createdDocCount``
     - Number of created documents
   * - ``updatedDocCount``
     - Number of updated documents
   * - ``deletedDocCount``
     - Number of deleted documents

Get Crawl Session Details
=========================

Request
-------

::

    GET /api/admin/crawlinginfo/{sessionId}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session": {
          "sessionId": "session_20250129_100000",
          "name": "Default Crawler",
          "status": "running",
          "startTime": "2025-01-29T10:00:00Z",
          "endTime": null,
          "crawlingInfoCount": 567,
          "createdDocCount": 234,
          "updatedDocCount": 123,
          "deletedDocCount": 12,
          "infos": [
            {
              "url": "https://example.com/page1",
              "status": "OK",
              "method": "GET",
              "httpStatusCode": 200,
              "contentLength": 12345,
              "executionTime": 123,
              "lastModified": "2025-01-29T09:55:00Z"
            }
          ]
        }
      }
    }

Delete Crawl Session
====================

Request
-------

::

    DELETE /api/admin/crawlinginfo/{sessionId}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Crawling session deleted successfully"
      }
    }

Usage Examples
==============

List Crawl Information
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Get Running Crawl Sessions
--------------------------

.. code-block:: bash

    # Get all sessions and filter for running ones
    curl -X GET "http://localhost:8080/api/admin/crawlinginfo" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.sessions[] | select(.status=="running")'

Get Specific Session Details
----------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/session_20250129_100000" \
         -H "Authorization: Bearer YOUR_TOKEN"

Delete Old Sessions
-------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/session_20250101_100000" \
         -H "Authorization: Bearer YOUR_TOKEN"

Monitor Progress
----------------

.. code-block:: bash

    # Periodically check progress of running sessions
    while true; do
      curl -s "http://localhost:8080/api/admin/crawlinginfo" \
           -H "Authorization: Bearer YOUR_TOKEN" | \
           jq '.response.sessions[] | select(.status=="running") | {sessionId, crawlingInfoCount, createdDocCount}'
      sleep 10
    done

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-failureurl` - Failure URL API
- :doc:`api-admin-joblog` - Job Log API
- :doc:`../../admin/crawlinginfo-guide` - Crawl Information Guide

