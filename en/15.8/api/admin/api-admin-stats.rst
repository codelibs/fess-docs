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

Accessing this API requires an access token with the ``Radmin-api`` permission.
For details on authentication, refer to :doc:`api-admin-overview`.

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

.. note::

   The field names of the objects under ``stats`` are output in snake_case (lowercase words separated by underscores, e.g. ``non_heap``).
   Fields whose value is ``null`` are omitted from the response.

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
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
              "non_heap": {
                "used": 134217728,
                "committed": 268435456,
                "max": 0,
                "percent": 0
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
              "swap_space": {"free": 0, "total": 0}
            },
            "cpu": {"percent": 12},
            "load_averages": [0.5, 0.4, 0.3]
          },
          "process": {
            "file_fescriptor": {"open": 256, "max": 65536},
            "cpu": {"percent": 5, "total": 123456},
            "virtual_memory": {"total": 4294967296}
          },
          "engine": {
            "cluster_name": "fess",
            "number_of_nodes": 1,
            "number_of_data_nodes": 1,
            "active_primary_shards": 10,
            "active_shards": 10,
            "active_shards_percent": 100.0,
            "relocating_shards": 0,
            "initializing_shards": 0,
            "unassigned_shards": 0,
            "delayed_unassigned_shards": 0,
            "number_of_pending_tasks": 0,
            "number_of_in_flight_fetch": 0,
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

Response Fields (Top Level)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Field
     - Description
   * - ``version``
     - The product version of |Fess| (e.g. ``15.8.0``).
   * - ``status``
     - A code indicating the processing result. ``0`` indicates successful completion.
   * - ``stats``
     - An object that stores the system metrics. It has five keys: ``jvm`` / ``os`` / ``process`` / ``engine`` / ``fs``.

``jvm``: JVM Statistics
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Field
     - Description
   * - ``memory.heap.used``
     - Used heap memory (bytes).
   * - ``memory.heap.committed``
     - Committed heap memory (bytes).
   * - ``memory.heap.max``
     - Maximum heap memory (bytes).
   * - ``memory.heap.percent``
     - Heap memory usage percentage (%).
   * - ``memory.non_heap.used``
     - Used non-heap memory (bytes).
   * - ``memory.non_heap.committed``
     - Committed non-heap memory (bytes).
   * - ``memory.non_heap.max``
     - Maximum non-heap memory (bytes). In the current implementation this value is not set and always returns ``0``.
   * - ``memory.non_heap.percent``
     - Non-heap memory usage percentage (%). In the current implementation this value is not set and always returns ``0``.
   * - ``pools``
     - Array of buffer pools. Each element includes ``key`` (pool name), ``count`` (number of buffers), ``used`` (used memory, bytes), and ``capacity`` (total capacity, bytes).
   * - ``gc``
     - Array of garbage collectors. Each element includes ``key`` (collector name), ``count`` (number of collections), and ``time`` (cumulative collection time, milliseconds).
   * - ``threads.count``
     - Current number of threads.
   * - ``threads.peak``
     - Peak number of threads.
   * - ``classes.loaded``
     - Number of currently loaded classes.
   * - ``classes.total_loaded``
     - Total number of classes loaded since the JVM started.
   * - ``classes.unloaded``
     - Total number of unloaded classes.
   * - ``uptime``
     - JVM uptime (milliseconds).

``os``: OS Statistics
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Field
     - Description
   * - ``memory.physical.free``
     - Free physical memory (bytes).
   * - ``memory.physical.total``
     - Total physical memory (bytes).
   * - ``memory.swap_space.free``
     - Free swap space (bytes).
   * - ``memory.swap_space.total``
     - Total swap space (bytes).
   * - ``cpu.percent``
     - System-wide CPU usage percentage (%).
   * - ``load_averages``
     - Array of load averages (1, 5, and 15 minutes). Values that cannot be obtained may be ``-1``.

``process``: Process Statistics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Field
     - Description
   * - ``file_fescriptor.open``
     - Number of currently open file descriptors.
   * - ``file_fescriptor.max``
     - Maximum number of file descriptors that can be opened.
   * - ``cpu.percent``
     - Process CPU usage percentage (%).
   * - ``cpu.total``
     - Cumulative CPU time used by the process (milliseconds).
   * - ``virtual_memory.total``
     - Total virtual memory size of the process (bytes).

.. note::

   The key name ``process.file_fescriptor`` is the snake_case conversion of the source code field name
   ``fileFescriptor`` (which originates from a misspelling of ``fileDescriptor``). It matches the
   implementation and is not a typo in this document.

``engine``: Search Engine Cluster Statistics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Health information of the search engine (OpenSearch) cluster.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Field
     - Description
   * - ``cluster_name``
     - Cluster name.
   * - ``number_of_nodes``
     - Total number of nodes in the cluster.
   * - ``number_of_data_nodes``
     - Number of data nodes.
   * - ``active_primary_shards``
     - Number of active primary shards.
   * - ``active_shards``
     - Number of active shards.
   * - ``active_shards_percent``
     - Percentage of active shards (%).
   * - ``relocating_shards``
     - Number of relocating shards.
   * - ``initializing_shards``
     - Number of initializing shards.
   * - ``unassigned_shards``
     - Number of unassigned shards.
   * - ``delayed_unassigned_shards``
     - Number of delayed unassigned shards.
   * - ``number_of_pending_tasks``
     - Number of pending tasks.
   * - ``number_of_in_flight_fetch``
     - Number of in-flight fetch operations.
   * - ``status``
     - Cluster health status (``green`` / ``yellow`` / ``red``).
   * - ``exception``
     - An error message that is included only when an error occurs, such as when the cluster cannot be reached. In this case, ``status`` becomes ``red``.

``fs``: File System Statistics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An array of statistics for each root (the roots obtained from ``File.listRoots()``).

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Field
     - Description
   * - ``path``
     - Absolute path of the root.
   * - ``total``
     - Total capacity (bytes).
   * - ``free``
     - Free capacity (bytes).
   * - ``usable``
     - Usable capacity (bytes).
   * - ``used``
     - Used capacity (bytes). This is ``total`` minus ``usable``.
   * - ``percent``
     - Usage percentage (%).

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
