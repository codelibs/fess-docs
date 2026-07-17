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

访问此API需要具有 ``Radmin-api`` 权限的访问令牌。
有关认证方式的详情，请参阅 :doc:`api-admin-overview`。

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

.. note::

   ``stats`` 下各对象的字段名以蛇形命名法（snake_case，即小写字母加下划线分隔，例如 ``non_heap``）输出。
   值为 ``null`` 的字段将从响应中省略。

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

响应字段（顶层）
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 字段
     - 说明
   * - ``version``
     - |Fess| 的产品版本（例如 ``15.7.0``）。
   * - ``status``
     - 表示处理结果的状态码。\ ``0`` 表示成功完成。
   * - ``stats``
     - 存放系统指标的对象。具有 ``jvm`` / ``os`` / ``process`` / ``engine`` / ``fs`` 这5个键。

``jvm``：JVM 统计
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 字段
     - 说明
   * - ``memory.heap.used``
     - 已使用的堆内存（字节）。
   * - ``memory.heap.committed``
     - 已提交的堆内存（字节）。
   * - ``memory.heap.max``
     - 最大堆内存（字节）。
   * - ``memory.heap.percent``
     - 堆内存使用率（%）。
   * - ``memory.non_heap.used``
     - 已使用的非堆内存（字节）。
   * - ``memory.non_heap.committed``
     - 已提交的非堆内存（字节）。
   * - ``memory.non_heap.max``
     - 最大非堆内存（字节）。当前实现中该值未设置，始终返回 ``0``\ 。
   * - ``memory.non_heap.percent``
     - 非堆内存使用率（%）。当前实现中该值未设置，始终返回 ``0``\ 。
   * - ``pools``
     - 缓冲池数组。每个元素包含 ``key``\ （池名称）、``count``\ （缓冲区数量）、``used``\ （已用内存，字节）、``capacity``\ （总容量，字节）。
   * - ``gc``
     - 垃圾回收器数组。每个元素包含 ``key``\ （回收器名称）、``count``\ （回收次数）、``time``\ （累计回收时间，毫秒）。
   * - ``threads.count``
     - 当前线程数。
   * - ``threads.peak``
     - 线程数峰值。
   * - ``classes.loaded``
     - 当前已加载的类数量。
   * - ``classes.total_loaded``
     - 自JVM启动以来已加载的类总数。
   * - ``classes.unloaded``
     - 已卸载的类总数。
   * - ``uptime``
     - JVM运行时间（毫秒）。

``os``：OS 统计
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 字段
     - 说明
   * - ``memory.physical.free``
     - 空闲物理内存（字节）。
   * - ``memory.physical.total``
     - 物理内存总量（字节）。
   * - ``memory.swap_space.free``
     - 空闲交换空间（字节）。
   * - ``memory.swap_space.total``
     - 交换空间总量（字节）。
   * - ``cpu.percent``
     - 系统整体CPU使用率（%）。
   * - ``load_averages``
     - 负载平均值数组（1分钟、5分钟、15分钟）。无法获取的值可能为 ``-1``\ 。

``process``：进程统计
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 字段
     - 说明
   * - ``file_fescriptor.open``
     - 当前已打开的文件描述符数量。
   * - ``file_fescriptor.max``
     - 可打开的文件描述符最大数量。
   * - ``cpu.percent``
     - 进程CPU使用率（%）。
   * - ``cpu.total``
     - 进程累计CPU时间（毫秒）。
   * - ``virtual_memory.total``
     - 进程虚拟内存总大小（字节）。

.. note::

   键名 ``process.file_fescriptor`` 是源代码字段名 ``fileFescriptor``
   （源自 ``fileDescriptor`` 的拼写错误）的蛇形命名法转换形式。这与实现保持一致，并非文档中的笔误。

``engine``：搜索引擎集群统计
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

搜索引擎（OpenSearch）集群的健康状态信息。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 字段
     - 说明
   * - ``cluster_name``
     - 集群名称。
   * - ``number_of_nodes``
     - 集群中的节点总数。
   * - ``number_of_data_nodes``
     - 数据节点数量。
   * - ``active_primary_shards``
     - 活跃主分片数量。
   * - ``active_shards``
     - 活跃分片数量。
   * - ``active_shards_percent``
     - 活跃分片百分比（%）。
   * - ``relocating_shards``
     - 正在迁移的分片数量。
   * - ``initializing_shards``
     - 正在初始化的分片数量。
   * - ``unassigned_shards``
     - 未分配的分片数量。
   * - ``delayed_unassigned_shards``
     - 延迟未分配的分片数量。
   * - ``number_of_pending_tasks``
     - 待处理任务数量。
   * - ``number_of_in_flight_fetch``
     - 正在执行的fetch操作数量。
   * - ``status``
     - 集群健康状态（``green`` / ``yellow`` / ``red``）。
   * - ``exception``
     - 仅在发生错误（例如无法连接到集群）时包含的错误消息。此时 ``status`` 为 ``red``\ 。

``fs``：文件系统统计
~~~~~~~~~~~~~~~~~~~~

包含各根目录（通过 ``File.listRoots()`` 获取的根目录）统计信息的数组。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 字段
     - 说明
   * - ``path``
     - 根目录的绝对路径。
   * - ``total``
     - 总容量（字节）。
   * - ``free``
     - 空闲容量（字节）。
   * - ``usable``
     - 可用容量（字节）。
   * - ``used``
     - 已用容量（字节）。即 ``total`` 减去 ``usable`` 的值。
   * - ``percent``
     - 使用率（%）。

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
