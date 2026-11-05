==========================
CrawlingInfo API
==========================

Overview
========

CrawlingInfo API is an API for viewing and managing |Fess| crawl information (crawl sessions).
You can list, retrieve individual entries, and delete crawl sessions.

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
     - /logs
     - List crawl information
   * - GET
     - /progress
     - Get the progress of running crawls
   * - GET
     - /log/{id}
     - Get crawl information
   * - DELETE
     - /log/{id}
     - Delete crawl information
   * - DELETE
     - /all
     - Bulk delete crawl sessions (excluding running)

List Crawl Information
======================

Request
-------

::

    GET /api/admin/crawlinginfo/logs

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
     - Number of items per page (default: 25; can be changed with ``paging.page.size`` in ``fess_config.properties``)
   * - ``page``
     - Integer
     - No
     - Page number (1-based, default: 1)
   * - ``session_id``
     - String
     - No
     - Session ID filter (partial match)

These parameters are given in the JSON request body (for example, ``{"size": 50, "page": 1}``). Values given in the URL query string (for example, ``?size=50``) are ignored, so the first 25 items are always returned unless you specify them in the body.

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "crawling_info_id_1",
            "session_id": "20250129100000",
            "name": "Default Crawler",
            "expired_time": "1738200000000",
            "created_time": 1738108800000
          },
          {
            "id": "crawling_info_id_2",
            "session_id": "20250128100000",
            "name": "Default Crawler",
            "expired_time": "1738113600000",
            "created_time": 1738022400000
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
   * - ``id``
     - Crawl information ID
   * - ``session_id``
     - Session ID
   * - ``name``
     - Session name
   * - ``expired_time``
     - Expiration time (epoch milliseconds; returned as a string)
   * - ``created_time``
     - Created time (epoch milliseconds; returned as a number)

.. note::

   Each log object in the response also includes an internal ``crud_mode`` field
   (an integer indicating the CRUD operation mode, always ``0`` for read operations).
   Clients can safely ignore it.

Get Progress of Running Crawls
==============================

Returns the progress of the crawls that are running now, one entry for each web, file system or data store crawl configuration. It is the same information as "Running Crawls" on the Crawling Info page of the admin UI (see :doc:`../../admin/crawlinginfo-guide`).

Request
-------

::

    GET /api/admin/crawlinginfo/progress

This endpoint does not accept parameters.

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "progress": [
          {
            "config_id": "Wabc123",
            "name": "Example Site",
            "count": 4200,
            "last_count": 10000,
            "updated_time": 1738144800000,
            "percent": 42
          },
          {
            "config_id": "Ddef456",
            "name": "Example Database",
            "count": 1500,
            "last_count": 0,
            "updated_time": 1738144795000
          }
        ],
        "total": 2
      }
    }

Response Fields
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``progress``
     - Array of the running crawls, ordered by the name of the crawl configuration. An empty array when no crawl is running
   * - ``total``
     - Number of elements of ``progress``

Each element of ``progress`` has the following fields.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``config_id``
     - ID of the crawl configuration (starts with ``W`` for web, ``F`` for file system and ``D`` for data store)
   * - ``name``
     - Name of the crawl configuration (``config_id`` when the configuration is not found)
   * - ``count``
     - Number of documents the running crawl has processed so far
   * - ``last_count``
     - Number of documents of the previous completed crawl (``0`` when unknown)
   * - ``updated_time``
     - Time ``count`` was written (epoch milliseconds, a number)
   * - ``percent``
     - ``count`` as a percentage of ``last_count`` (``0`` to ``99``). Omitted when there is no previous completed crawl

.. note::

   A crawl that has finished or been stopped is not included. When the crawler stops without recording that (for example the process is killed), the crawl is not included once about 30 seconds (by default) have passed since its last update. ``count`` of a web or file system crawl is the number of access results; ``count`` of a data store crawl is the number of documents indexed for the crawl configuration.

Get Crawl Information
=====================

Request
-------

::

    GET /api/admin/crawlinginfo/log/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "crawling_info_id_1",
          "session_id": "20250129100000",
          "name": "Default Crawler",
          "expired_time": "1738200000000",
          "created_time": 1738108800000
        }
      }
    }

Delete Crawl Information
========================

Request
-------

::

    DELETE /api/admin/crawlinginfo/log/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Bulk Delete Crawl Sessions
==========================

Deletes all crawl sessions (and their parameter data) except those that are currently
running. There is no age or time threshold; every session that is not currently running
is deleted.

Request
-------

::

    DELETE /api/admin/crawlinginfo/all

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

List Crawl Information
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"size": 50, "page": 1}'

Filter by Specific Session
--------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"session_id": "20250129100000"}'

Get Crawl Information
---------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/log/crawling_info_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Delete Crawl Information
------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/log/crawling_info_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Bulk Delete Sessions
--------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-failureurl` - Failure URL API
- :doc:`api-admin-joblog` - Job Log API
- :doc:`../../admin/crawlinginfo-guide` - Crawl Information Guide
