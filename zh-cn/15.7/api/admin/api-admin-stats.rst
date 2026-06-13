==========================
Stats API
==========================

概述
====

Stats API是用于获取 |Fess| 运行所在服务器的系统指标的API。
您可以查看JVM、OS、进程、搜索引擎（OpenSearch）集群、文件系统的各项统计信息。

.. note::

   此API不返回搜索查询或点击等搜索分析数据。
   关于索引内文档的搜索与管理，请参阅 :doc:`api-admin-searchlist`。

基础URL
=======

::

    /api/admin/stats

端点列表
========

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 方法
     - 路径
     - 说明
   * - GET
     - /
     - 获取系统统计信息

获取系统统计信息
================

请求
----

::

    GET /api/admin/stats

此端点不接受查询参数。

响应
----

响应包含表示产品版本的 ``version``、表示处理结果的 ``status``，以及
存放系统指标的 ``stats`` 对象。
``stats`` 具有 ``jvm`` / ``os`` / ``process`` / ``engine`` / ``fs`` 这5个键。

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

响应字段
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 字段
     - 说明
   * - ``jvm``
     - JVM统计。包含 ``memory``（``heap`` / ``nonHeap``）、``pools``（缓冲池）、``gc``（GC）、``threads``、``classes``、``uptime``（毫秒）。
   * - ``os``
     - OS统计。包含 ``memory``（``physical`` / ``swapSpace``）、``cpu``、``loadAverages``（负载平均值数组）。
   * - ``process``
     - 进程统计。包含 ``fileFescriptor``（打开/最大文件描述符数）、``cpu``、``virtualMemory``。
   * - ``engine``
     - 搜索引擎（OpenSearch）集群的状态。包含 ``clusterName``、节点数、分片数、``status`` 等。当无法连接到集群时，``status`` 为 ``"red"``，且 ``exception`` 中包含错误消息。
   * - ``fs``
     - 文件系统统计的数组。每个根目录包含 ``path``、``total``、``free``、``usable``、``used``（字节）、``percent``（使用率）。

.. note::

   ``process.fileFescriptor`` 这一键名遵循源代码的实现（并非 ``fileDescriptor`` 的拼写）。

使用示例
========

获取系统统计信息
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN"

确认JVM堆使用率
---------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq '.response.stats.jvm.memory.heap.percent'

确认搜索引擎集群状态
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq '.response.stats.engine.status'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-systeminfo` - 系统信息API
- :doc:`api-admin-searchlist` - 文档搜索与管理API
