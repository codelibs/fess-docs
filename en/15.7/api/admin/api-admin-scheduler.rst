==========================
Scheduler API
==========================

Overview
========

Scheduler API is an API for managing |Fess| scheduled jobs.
You can start/stop crawl jobs, and create/update/delete schedule configurations.

Base URL
========

::

    /api/admin/scheduler

Endpoint List
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Method
     - Path
     - Description
   * - GET
     - /settings
     - List scheduled jobs
   * - GET
     - /setting/{id}
     - Get scheduled job
   * - POST
     - /setting
     - Create scheduled job
   * - PUT
     - /setting
     - Update scheduled job
   * - DELETE
     - /setting/{id}
     - Delete scheduled job
   * - PUT
     - /{id}/start
     - Start job
   * - PUT
     - /{id}/stop
     - Stop job

List Scheduled Jobs
===================

Request
-------

::

    GET /api/admin/scheduler/settings

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

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "job_id_1",
            "name": "Default Crawler",
            "target": "all",
            "cronExpression": "0 0 0 * * ?",
            "scriptType": "groovy",
            "scriptData": "...",
            "jobLogging": "true",
            "crawler": "true",
            "available": "true",
            "sortOrder": 0,
            "running": false
          }
        ],
        "total": 5
      }
    }

.. note::

   ``jobLogging`` / ``crawler`` / ``available`` are treated as strings (``"true"`` / ``"false"``). ``running`` is a boolean value indicating the execution status of the job.

Get Scheduled Job
=================

Request
-------

::

    GET /api/admin/scheduler/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "job_id_1",
          "name": "Default Crawler",
          "target": "all",
          "cronExpression": "0 0 0 * * ?",
          "scriptType": "groovy",
          "scriptData": "return container.getComponent(\"crawlJob\").execute();",
          "jobLogging": "true",
          "crawler": "true",
          "available": "true",
          "sortOrder": 0,
          "running": false
        }
      }
    }

Create Scheduled Job
====================

Request
-------

::

    POST /api/admin/scheduler/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Daily Crawler",
      "target": "all",
      "cronExpression": "0 0 2 * * ?",
      "scriptType": "groovy",
      "scriptData": "return container.getComponent(\"crawlJob\").execute();",
      "jobLogging": "true",
      "crawler": "true",
      "available": "true",
      "sortOrder": 1
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Required
     - Description
   * - ``name``
     - Yes
     - Job name
   * - ``target``
     - Yes
     - Execution target ("all" or specific target)
   * - ``cronExpression``
     - No
     - Cron expression (seconds minutes hours day month weekday)
   * - ``scriptType``
     - Yes
     - Script type ("groovy")
   * - ``scriptData``
     - No
     - Execution script
   * - ``jobLogging``
     - No
     - Enable logging (string ``"true"`` / ``"false"``)
   * - ``crawler``
     - No
     - Whether this is a crawler job (string ``"true"`` / ``"false"``)
   * - ``available``
     - No
     - Enable/disable (string ``"true"`` / ``"false"``)
   * - ``sortOrder``
     - Yes
     - Display order

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_job_id",
        "created": true
      }
    }

Cron Expression Examples
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Cron Expression
     - Description
   * - ``0 0 2 * * ?``
     - Execute daily at 2 AM
   * - ``0 0 0/6 * * ?``
     - Execute every 6 hours
   * - ``0 0 2 * * MON``
     - Execute every Monday at 2 AM
   * - ``0 0 2 1 * ?``
     - Execute on the 1st of every month at 2 AM

Update Scheduled Job
====================

Request
-------

::

    PUT /api/admin/scheduler/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_job_id",
      "name": "Updated Crawler",
      "target": "all",
      "cronExpression": "0 0 3 * * ?",
      "scriptType": "groovy",
      "scriptData": "...",
      "jobLogging": "true",
      "crawler": "true",
      "available": "true",
      "sortOrder": 1,
      "versionNo": 1
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_job_id",
        "created": false
      }
    }

Delete Scheduled Job
====================

Request
-------

::

    DELETE /api/admin/scheduler/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_job_id",
        "created": false
      }
    }

Start Job
=========

Execute a scheduled job immediately.

Request
-------

::

    PUT /api/admin/scheduler/{id}/start

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "jobLogId": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
      }
    }

Response Fields
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``jobLogId``
     - Job log ID of the started job. Issued when job logging is enabled. If job logging is disabled, it becomes ``null``.

Notes
-----

- Returns an error if the job is already running
- Returns an error if the job is disabled (``available`` is ``"false"``)

Stop Job
========

Stop a running job.

Request
-------

::

    PUT /api/admin/scheduler/{id}/stop

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Usage Examples
==============

Create and Run a Crawl Job
--------------------------

.. code-block:: bash

    # Create job
    curl -X POST "http://localhost:8080/api/admin/scheduler/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Hourly Crawler",
           "target": "all",
           "cronExpression": "0 0 * * * ?",
           "scriptType": "groovy",
           "scriptData": "return container.getComponent(\"crawlJob\").execute();",
           "jobLogging": "true",
           "crawler": "true",
           "available": "true"
         }'

    # Run job immediately
    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

Check Job Status
----------------

.. code-block:: bash

    # Check status of all jobs
    curl "http://localhost:8080/api/admin/scheduler/settings" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # The running field indicates execution status

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-joblog` - Job Log API
- :doc:`../../admin/scheduler-guide` - Scheduler Management Guide

