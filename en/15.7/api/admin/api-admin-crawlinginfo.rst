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
     - Number of items per page (default: 20)
   * - ``page``
     - Integer
     - No
     - Page number (1-based, default: 1)
   * - ``sessionId``
     - String
     - No
     - Session ID filter (partial match)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "crawling_info_id_1",
            "sessionId": "20250129100000",
            "name": "Default Crawler",
            "expiredTime": "1738200000000",
            "createdTime": 1738108800000
          },
          {
            "id": "crawling_info_id_2",
            "sessionId": "20250128100000",
            "name": "Default Crawler",
            "expiredTime": "1738113600000",
            "createdTime": 1738022400000
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
   * - ``sessionId``
     - Session ID
   * - ``name``
     - Session name
   * - ``expiredTime``
     - Expiration time (epoch milliseconds; returned as a string)
   * - ``createdTime``
     - Created time (epoch milliseconds; returned as a number)

.. note::

   Each log object in the response also includes an internal ``crudMode`` field
   (an integer indicating the CRUD operation mode, always ``0`` for read operations).
   Clients can safely ignore it.

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
          "sessionId": "20250129100000",
          "name": "Default Crawler",
          "expiredTime": "1738200000000",
          "createdTime": 1738108800000
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

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Filter by Specific Session
--------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs?sessionId=20250129100000" \
         -H "Authorization: Bearer YOUR_TOKEN"

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
