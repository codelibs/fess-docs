==========================
JobLog API
==========================

Overview
========

JobLog API is an API for viewing and managing |Fess| job execution logs.
You can retrieve and delete the execution history, execution results, and error information
for scheduled jobs and crawl jobs.

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
     - /logs
     - List job logs
   * - GET
     - /log/{id}
     - Get job log
   * - DELETE
     - /log/{id}
     - Delete job log

List Job Logs
=============

Request
-------

::

    GET /api/admin/joblog/logs

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
     - Page number (1-based, default: 1)
   * - ``id``
     - String
     - No
     - Filter by job log ID (exact match)

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
            "startTime": "1738116000000",
            "endTime": "1738118723000"
          },
          {
            "id": "joblog_id_2",
            "jobName": "Default Crawler",
            "jobStatus": "fail",
            "target": "all",
            "scriptType": "groovy",
            "scriptData": "return container.getComponent(\"crawlJob\").execute();",
            "scriptResult": "Error: Connection timeout",
            "startTime": "1738029600000",
            "endTime": "1738030215000"
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
     - Job status (``ok``: success, ``fail``: failure, ``running``: in progress)
   * - ``target``
     - Execution target (scheduler target name; default is ``all``)
   * - ``scriptType``
     - Script type (e.g., ``groovy``)
   * - ``scriptData``
     - Execution script
   * - ``scriptResult``
     - Execution result
   * - ``startTime``
     - Start time (epoch milliseconds; returned as a string)
   * - ``endTime``
     - End time (epoch milliseconds; returned as a string). Not returned for running jobs.

.. note::

   Each log object in the response also includes an internal ``crudMode`` field
   (an integer indicating the CRUD operation mode, always ``0`` for read operations).
   Clients can safely ignore it.

Get Job Log
===========

Request
-------

::

    GET /api/admin/joblog/log/{id}

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
          "startTime": "1738116000000",
          "endTime": "1738118723000"
        }
      }
    }

If no job log exists for the specified ID, an error response is returned with a non-zero
value in ``status``.

Delete Job Log
==============

Request
-------

::

    DELETE /api/admin/joblog/log/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

If no job log exists for the specified ID, an error response is returned with a non-zero
value in ``status``.

Usage Examples
==============

List Job Logs
-------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/logs?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Extract Failed Jobs Only
------------------------

.. code-block:: bash

    # Filter failed jobs with jq
    curl -X GET "http://localhost:8080/api/admin/joblog/logs?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs[] | select(.jobStatus=="fail")'

Get Job Log
-----------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/log/joblog_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Delete Job Log
--------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/joblog/log/joblog_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Calculate Job Success Rate
--------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/logs?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs | {total: length, ok: [.[] | select(.jobStatus=="ok")] | length, fail: [.[] | select(.jobStatus=="fail")] | length}'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-scheduler` - Scheduler API
- :doc:`api-admin-crawlinginfo` - Crawl Information API
- :doc:`../../admin/joblog-guide` - Job Log Management Guide
