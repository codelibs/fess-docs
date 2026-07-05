==========================
JobLog API
==========================

Overview
========

JobLog API is an API for retrieving |Fess| job execution logs.
You can view execution history and error information for scheduled jobs and crawl jobs.

Base URL
========

::

    /api/admin/joblog

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
     - List job logs
   * - GET
     - /{id}
     - Get job log details
   * - DELETE
     - /{id}
     - Delete job log
   * - DELETE
     - /delete-all
     - Delete all job logs

List Job Logs
=============

Request
-------

::

    GET /api/admin/joblog

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
   * - ``status``
     - String
     - No
     - Status filter (ok/fail/running)
   * - ``from``
     - String
     - No
     - Start date/time (ISO 8601 format)
   * - ``to``
     - String
     - No
     - End date/time (ISO 8601 format)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "joblog_id_1",
            "jobName": "Default Crawler",
            "jobStatus": "ok",
            "target": "all",
            "scriptType": "groovy",
            "scriptData": "return container.getComponent(\"crawlJob\").execute();",
            "scriptResult": "Job completed successfully",
            "startTime": "2025-01-29T02:00:00Z",
            "endTime": "2025-01-29T02:45:23Z",
            "executionTime": 2723000
          },
          {
            "id": "joblog_id_2",
            "jobName": "Default Crawler",
            "jobStatus": "fail",
            "target": "all",
            "scriptType": "groovy",
            "scriptData": "return container.getComponent(\"crawlJob\").execute();",
            "scriptResult": "Error: Connection timeout",
            "startTime": "2025-01-28T02:00:00Z",
            "endTime": "2025-01-28T02:10:15Z",
            "executionTime": 615000
          }
        ],
        "total": 100
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
     - Job log ID
   * - ``jobName``
     - Job name
   * - ``jobStatus``
     - Job status (ok/fail/running)
   * - ``target``
     - Execution target
   * - ``scriptType``
     - Script type
   * - ``scriptData``
     - Execution script
   * - ``scriptResult``
     - Execution result
   * - ``startTime``
     - Start time
   * - ``endTime``
     - End time
   * - ``executionTime``
     - Execution time (milliseconds)

Get Job Log Details
===================

Request
-------

::

    GET /api/admin/joblog/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "joblog_id_1",
          "jobName": "Default Crawler",
          "jobStatus": "ok",
          "target": "all",
          "scriptType": "groovy",
          "scriptData": "return container.getComponent(\"crawlJob\").execute();",
          "scriptResult": "Crawl completed successfully.\nDocuments indexed: 1234\nDocuments updated: 567\nDocuments deleted: 12\nErrors: 0",
          "startTime": "2025-01-29T02:00:00Z",
          "endTime": "2025-01-29T02:45:23Z",
          "executionTime": 2723000
        }
      }
    }

Delete Job Log
==============

Request
-------

::

    DELETE /api/admin/joblog/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Job log deleted successfully"
      }
    }

Delete All Job Logs
===================

Request
-------

::

    DELETE /api/admin/joblog/delete-all

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
   * - ``status``
     - String
     - No
     - Delete only logs with this status

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Job logs deleted successfully",
        "deletedCount": 50
      }
    }

Usage Examples
==============

List Job Logs
-------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Get Failed Jobs Only
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?status=fail" \
         -H "Authorization: Bearer YOUR_TOKEN"

Get Job Logs for Specific Period
--------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

Get Job Log Details
-------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/joblog_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Delete Old Job Logs
-------------------

.. code-block:: bash

    # Delete logs older than 30 days
    curl -X DELETE "http://localhost:8080/api/admin/joblog/delete-all?before=2024-12-30T00:00:00Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

Delete Failed Job Logs Only
---------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/joblog/delete-all?status=fail" \
         -H "Authorization: Bearer YOUR_TOKEN"

Detect Long-Running Jobs
------------------------

.. code-block:: bash

    # Extract jobs that took more than 1 hour
    curl -X GET "http://localhost:8080/api/admin/joblog?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs[] | select(.executionTime > 3600000) | {jobName, startTime, executionTime}'

Calculate Job Success Rate
--------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs | {total: length, ok: [.[] | select(.jobStatus=="ok")] | length, fail: [.[] | select(.jobStatus=="fail")] | length}'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-scheduler` - Scheduler API
- :doc:`api-admin-crawlinginfo` - Crawling Info API
- :doc:`../../admin/joblog-guide` - Job Log Management Guide

