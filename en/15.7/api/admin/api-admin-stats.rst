==========================
Stats API
==========================

Overview
========

Stats API is an API for retrieving system metrics of the server on which |Fess| runs.
You can view statistics information for the JVM, OS, process, search engine (OpenSearch) cluster, and file system.

.. note::

   This API does not return search analytics data such as search queries or clicks.
   To search and manage documents in the index, refer to :doc:`api-admin-searchlist`.

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
     - Get system statistics information

Get System Statistics Information
=================================

Request
-------

::

    GET /api/admin/stats

This endpoint does not accept query parameters.

Response
--------

The response includes ``version`` indicating the product version, ``status`` indicating
the processing result, and a ``stats`` object that stores the system metrics.
``stats`` has five keys: ``jvm`` / ``os`` / ``process`` / ``engine`` / ``fs``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "stats": {
          "jvm": {
            "memory": {
              "heap": {
                "used": 536870912,
                "committed": 1073741824,
                "max": 2147483648,
                "percent": 25
              },
              "nonHeap": {
                "used": 134217728,
                "committed": 268435456
              }
            },
            "pools": [
              {"key": "mapped", "count": 1, "used": 4096, "capacity": 4096}
            ],
            "gc": [
              {"key": "young", "count": 12, "time": 345}
            ],
            "threads": {"count": 80, "peak": 95},
            "classes": {"loaded": 12000, "total_loaded": 12500, "unloaded": 500},
            "uptime": 3600000
          },
          "os": {
            "memory": {
              "physical": {"free": 2147483648, "total": 8589934592},
              "swapSpace": {"free": 0, "total": 0}
            },
            "cpu": {"percent": 12},
            "loadAverages": [0.5, 0.4, 0.3]
          },
          "process": {
            "fileFescriptor": {"open": 256, "max": 65536},
            "cpu": {"percent": 5, "total": 123456},
            "virtualMemory": {"total": 4294967296}
          },
          "engine": {
            "clusterName": "fess",
            "numberOfNodes": 1,
            "numberOfDataNodes": 1,
            "activePrimaryShards": 10,
            "activeShards": 10,
            "activeShardsPercent": 100.0,
            "relocatingShards": 0,
            "initializingShards": 0,
            "unassignedShards": 0,
            "delayedUnassignedShards": 0,
            "numberOfPendingTasks": 0,
            "numberOfInFlightFetch": 0,
            "status": "green"
          },
          "fs": [
            {
              "path": "/",
              "total": 107374182400,
              "free": 53687091200,
              "usable": 53687091200,
              "used": 53687091200,
              "percent": 50
            }
          ]
        }
      }
    }

Response Fields
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Field
     - Description
   * - ``jvm``
     - JVM statistics. Includes ``memory`` (``heap`` / ``nonHeap``), ``pools`` (buffer pools), ``gc`` (GC), ``threads``, ``classes``, and ``uptime`` (milliseconds).
   * - ``os``
     - OS statistics. Includes ``memory`` (``physical`` / ``swapSpace``), ``cpu``, and ``loadAverages`` (array of load averages).
   * - ``process``
     - Process statistics. Includes ``fileFescriptor`` (open/maximum file descriptor count), ``cpu``, and ``virtualMemory``.
   * - ``engine``
     - State of the search engine (OpenSearch) cluster. Includes ``clusterName``, node count, shard count, ``status``, and so on. If the cluster cannot be reached, ``status`` becomes ``"red"`` and ``exception`` contains the error message.
   * - ``fs``
     - Array of file system statistics. For each root, includes ``path``, ``total``, ``free``, ``usable``, ``used`` (bytes), and ``percent`` (usage rate).

.. note::

   The key name ``process.fileFescriptor`` follows the source code implementation (it is not the spelling ``fileDescriptor``).

Usage Examples
==============

Get System Statistics Information
---------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN"

Check JVM Heap Usage
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq '.response.stats.jvm.memory.heap.percent'

Check Search Engine Cluster State
---------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq '.response.stats.engine.status'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-systeminfo` - System Info API
- :doc:`api-admin-searchlist` - Document Search and Management API
