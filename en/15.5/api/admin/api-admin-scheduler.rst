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
   * - GET/PUT
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
    PUT /api/admin/scheduler/settings

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
        "settings": [
          {
            "id": "job_id_1",
            "name": "Default Crawler",
            "target": "all",
            "cronExpression": "0 0 0 * * ?",
            "scriptType": "groovy",
            "scriptData": "...",
            "jobLogging": true,
            "crawler": true,
            "available": true,
            "sortOrder": 0,
            "running": false
          }
        ],
        "total": 5
      }
    }

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
          "jobLogging": true,
          "crawler": true,
          "available": true,
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
      "jobLogging": true,
      "crawler": true,
      "available": true,
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
     - Yes
     - Cron expression (seconds minutes hours day month weekday)
   * - ``scriptType``
     - Yes
     - Script type ("groovy")
   * - ``scriptData``
     - Yes
     - Execution script
   * - ``jobLogging``
     - No
     - Enable logging (default: true)
   * - ``crawler``
     - No
     - Whether this is a crawler job (default: false)
   * - ``available``
     - No
     - Enable/disable (default: true)
   * - ``sortOrder``
     - No
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
      "jobLogging": true,
      "crawler": true,
      "available": true,
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
        "status": 0
      }
    }

Notes
-----

- Returns an error if the job is already running
- Returns an error if the job is disabled (``available: false``)

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
           "jobLogging": true,
           "crawler": true,
           "available": true
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

