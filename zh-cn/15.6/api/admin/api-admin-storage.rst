==========================
Storage API
==========================

概述
====

Storage API是用于管理 |Fess| 存储的API。
您可以操作索引的存储使用情况和优化。

基础URL
=======

::

    /api/admin/storage

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
     - 获取存储信息
   * - POST
     - /optimize
     - 优化索引
   * - POST
     - /flush
     - 刷新索引

获取存储信息
============

请求
----

::

    GET /api/admin/storage

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "storage": {
          "indices": [
            {
              "name": "fess.20250129",
              "status": "open",
              "health": "green",
              "docsCount": 123456,
              "docsDeleted": 234,
              "storeSize": "5.2gb",
              "primariesStoreSize": "2.6gb",
              "shards": 5,
              "replicas": 1
            }
          ],
          "totalStoreSize": "5.2gb",
          "totalDocsCount": 123456,
          "clusterHealth": "green",
          "diskUsage": {
            "total": "107374182400",
            "available": "53687091200",
            "used": "53687091200",
            "usedPercent": 50.0
          }
        }
      }
    }

响应字段
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``indices``
     - 索引列表
   * - ``name``
     - 索引名称
   * - ``status``
     - 索引状态（open/close）
   * - ``health``
     - 健康状态（green/yellow/red）
   * - ``docsCount``
     - 文档数量
   * - ``docsDeleted``
     - 已删除文档数量
   * - ``storeSize``
     - 存储大小
   * - ``primariesStoreSize``
     - 主分片大小
   * - ``shards``
     - 分片数量
   * - ``replicas``
     - 副本数量
   * - ``totalStoreSize``
     - 总存储大小
   * - ``totalDocsCount``
     - 总文档数量
   * - ``clusterHealth``
     - 集群健康状态
   * - ``diskUsage``
     - 磁盘使用情况

优化索引
========

请求
----

::

    POST /api/admin/storage/optimize
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "index": "fess.20250129",
      "maxNumSegments": 1,
      "onlyExpungeDeletes": false,
      "flush": true
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 必需
     - 说明
   * - ``index``
     - 否
     - 索引名称（未指定时为所有索引）
   * - ``maxNumSegments``
     - 否
     - 最大段数（默认：1）
   * - ``onlyExpungeDeletes``
     - 否
     - 仅删除已删除文档（默认：false）
   * - ``flush``
     - 否
     - 优化后刷新（默认：true）

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Index optimization started"
      }
    }

刷新索引
========

请求
----

::

    POST /api/admin/storage/flush
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "index": "fess.20250129"
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 必需
     - 说明
   * - ``index``
     - 否
     - 索引名称（未指定时为所有索引）

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Index flushed successfully"
      }
    }

使用示例
========

获取存储信息
------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage" \
         -H "Authorization: Bearer YOUR_TOKEN"

优化所有索引
------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/optimize" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "maxNumSegments": 1,
           "flush": true
         }'

优化特定索引
------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/optimize" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "index": "fess.20250129",
           "maxNumSegments": 1,
           "onlyExpungeDeletes": false
         }'

删除已删除文档
--------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/optimize" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "onlyExpungeDeletes": true
         }'

刷新索引
--------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/flush" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "index": "fess.20250129"
         }'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-systeminfo` - 系统信息API
- :doc:`../../admin/storage-guide` - 存储管理指南

