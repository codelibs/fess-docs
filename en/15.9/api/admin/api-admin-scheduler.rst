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
     - Number of items per page (default: 25; configurable via ``paging.page.size`` in ``fess_config.properties``)
   * - ``page``
     - Integer
     - No
     - Page number (1-based; default: 1)

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.9",
        "status": 0,
        "settings": [
          {
            "id": "job_id_1",
            "name": "Default Crawler",
            "target": "all",
            "cron_expression": "0 0 * * *",
            "script_type": "javascript",
            "script_data": "...",
            "job_logging": "true",
            "crawler": "true",
            "available": "true",
            "sort_order": 0,
            "version_no": 1,
            "running": false
          }
        ],
        "total": 5
      }
    }

.. note::

   The ``response`` object always includes ``version`` (product version) and ``status`` (result code). See :doc:`api-admin-overview` for the common response format. Later examples may omit ``version`` for brevity.

.. note::

   In responses, ``job_logging`` / ``crawler`` / ``available`` are returned as strings (``"true"`` / ``"false"``). ``running`` is a boolean, response-only field indicating whether the job is currently running (it cannot be set in requests). ``total`` is the total number of jobs matching the query.

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
          "cron_expression": "0 0 * * *",
          "script_type": "javascript",
          "script_data": "return container.getComponent(\"crawlJob\").execute();",
          "job_logging": "true",
          "crawler": "true",
          "available": "true",
          "sort_order": 0,
          "version_no": 1,
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
      "cron_expression": "0 2 * * *",
      "script_type": "javascript",
      "script_data": "return container.getComponent(\"crawlJob\").execute();",
      "job_logging": "true",
      "crawler": "true",
      "available": "true",
      "sort_order": 1
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
     - Job name (max 100 characters)
   * - ``target``
     - Yes
     - Execution target (max 100 characters). Specify ``all`` or a specific target name
   * - ``cron_expression``
     - No
     - Cron expression (five fields: minute hour day month day-of-week, in cron4j format). Max 100 characters, validated as a cron expression. A Quartz-style seconds field and ``?`` cannot be used (``0 0 * * * ?`` is rejected). If empty, the job is not scheduled and can only be started manually
   * - ``script_type``
     - Yes
     - Script type (max 100 characters). Either ``javascript`` (the default for new jobs, determined by the ``job.default.script`` property) or ``groovy`` (requires the ``fess-script-groovy`` plugin)
   * - ``script_data``
     - No
     - Execution script. The maximum size follows ``form.admin.max.input.size`` in ``fess_config.properties``
   * - ``job_logging``
     - No
     - Enable job logging (string)
   * - ``crawler``
     - No
     - Whether this is a crawler job (string)
   * - ``available``
     - No
     - Enabled/disabled (string)
   * - ``sort_order``
     - Yes
     - Display order (integer between 0 and 2147483647)

.. note::

   ``job_logging`` / ``crawler`` / ``available`` are string fields. In requests, specifying ``"on"`` or ``"true"`` (case-insensitive) enables them; any other value (``"false"``, empty string, or unset) is treated as disabled. In responses they are returned as ``"true"`` / ``"false"``.

.. note::

   ``crud_mode`` is set automatically on the server side and does not need to be specified in requests. Audit fields such as ``created_by`` / ``created_time`` are also set on the server side.

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
   * - ``0 2 * * *``
     - Execute daily at 2 AM
   * - ``0 */6 * * *``
     - Execute every 6 hours
   * - ``0 2 * * 1``
     - Execute every Monday at 2 AM (days of the week are ``0`` for Sunday to ``6`` for Saturday)
   * - ``0 2 1 * *``
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
      "cron_expression": "0 3 * * *",
      "script_type": "javascript",
      "script_data": "...",
      "job_logging": "true",
      "crawler": "true",
      "available": "true",
      "sort_order": 1,
      "version_no": 1
    }

.. note::

   For updates, ``id`` (max 1000 characters) and ``version_no`` are required. ``version_no`` is used for optimistic locking; specify the value returned in the get response. If the value does not match, the update fails. Other required fields (``name`` / ``target`` / ``script_type`` / ``sort_order``) are the same as for creation.

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
        "job_log_id": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
      }
    }

Response Fields
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``job_log_id``
     - Job log ID of the started job. Issued when job logging is enabled. If job logging is disabled, it is omitted from the response.

Notes
-----

- If the job is already running, the start fails and an error is returned (``status`` other than ``0``).
- If the job is disabled (``available`` is not enabled), the start likewise fails with an error.
- ``job_log_id`` is issued only when job logging is enabled (``job_logging`` is enabled).

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
           "cron_expression": "0 * * * *",
           "script_type": "javascript",
           "script_data": "return container.getComponent(\"crawlJob\").execute();",
           "job_logging": "true",
           "crawler": "true",
           "available": "true",
           "sort_order": 1
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

