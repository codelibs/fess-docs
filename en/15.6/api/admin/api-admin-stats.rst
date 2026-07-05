==========================
Stats API
==========================

Overview
========

Stats API is an API for retrieving |Fess| statistics information.
You can view statistics data for search queries, clicks, and favorites.

Base URL
========

::

    /api/admin/stats

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
     - Get statistics information

Get Statistics Information
==========================

Request
-------

::

    GET /api/admin/stats

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
   * - ``type``
     - String
     - No
     - Statistics type (query/click/favorite)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "stats": {
          "totalQueries": 12345,
          "uniqueQueries": 5678,
          "totalClicks": 9876,
          "totalFavorites": 543,
          "averageResponseTime": 123.45,
          "topQueries": [
            {
              "query": "fess",
              "count": 567
            },
            {
              "query": "search",
              "count": 432
            }
          ],
          "topClickedDocuments": [
            {
              "url": "https://example.com/doc1",
              "title": "Document 1",
              "count": 234
            }
          ],
          "queryTrends": [
            {
              "date": "2025-01-01",
              "count": 234
            },
            {
              "date": "2025-01-02",
              "count": 267
            }
          ]
        }
      }
    }

Response Fields
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``totalQueries``
     - Total search query count
   * - ``uniqueQueries``
     - Unique search query count
   * - ``totalClicks``
     - Total click count
   * - ``totalFavorites``
     - Total favorite count
   * - ``averageResponseTime``
     - Average response time (milliseconds)
   * - ``topQueries``
     - Popular search queries
   * - ``topClickedDocuments``
     - Popular documents
   * - ``queryTrends``
     - Query trends

Search Query Statistics
=======================

Request
-------

::

    GET /api/admin/stats?type=query&from=2025-01-01&to=2025-01-31

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "stats": {
          "totalQueries": 5678,
          "uniqueQueries": 2345,
          "topQueries": [
            {
              "query": "documentation",
              "count": 234,
              "avgResponseTime": 98.7
            }
          ],
          "queriesByHour": [
            {
              "hour": 0,
              "count": 45
            },
            {
              "hour": 1,
              "count": 23
            }
          ],
          "queriesByDay": [
            {
              "day": "Monday",
              "count": 567
            }
          ]
        }
      }
    }

Click Statistics
================

Request
-------

::

    GET /api/admin/stats?type=click&from=2025-01-01&to=2025-01-31

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "stats": {
          "totalClicks": 3456,
          "topClickedDocuments": [
            {
              "url": "https://example.com/popular-doc",
              "title": "Popular Document",
              "count": 234,
              "clickThroughRate": 0.45
            }
          ],
          "clicksByPosition": [
            {
              "position": 1,
              "count": 1234
            },
            {
              "position": 2,
              "count": 567
            }
          ]
        }
      }
    }

Usage Examples
==============

Get All Statistics
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN"

Get Statistics for Time Period
------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

Get Search Query Statistics
---------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats?type=query&from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

Get Top 10 Popular Queries
--------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats?type=query" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.stats.topQueries[:10]'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-log` - Log API
- :doc:`api-admin-systeminfo` - System Info API

